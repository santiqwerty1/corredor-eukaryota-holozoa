"""Cotejo mecánico independiente y sólo lectura de la propuesta S10 v2.

No adjudica ciencia, no ejecuta el consumidor contra archivos futuros y no
escribe corpus ni derivados. Los dictámenes son externos a esta fixture.
"""
import csv
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROPOSAL = ROOT / "docs/auditorias/PROPUESTA_AUTOR_S10_C028_C036_V2_2026-09-27.json"
EVIDENCE = ROOT / "docs/auditorias/EVIDENCIA_AUTOR_S10_C028_C036_V2_FINAL_2026-09-27.json"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def rowhash(value):
    return sha((json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode())


def cellhash(text):
    return sha((text + "\n").encode())


def csvrows(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


p = json.loads(PROPOSAL.read_bytes())
e = json.loads(EVIDENCE.read_bytes())
paths = set(p["huellas_base"]) | set(p["fuentes"])
paths.add("data/auditoria/residuales_trazabilidad_no_conformes_v3.csv")
paths |= {str(PROPOSAL.relative_to(ROOT)), str(EVIDENCE.relative_to(ROOT)), str(Path(__file__).relative_to(ROOT))}
before = {name: sha((ROOT / name).read_bytes()) for name in sorted(paths)}
checks = []


def check(kind, identity, truth):
    checks.append({"tipo": kind, "id": identity, "pass": bool(truth)})


for path, digest in p["huellas_base"].items():
    check("huella_base", path, before[path] == digest)
for path, info in p["fuentes"].items():
    check("artefacto", path, before[path] == info["sha256"] and (ROOT / path).stat().st_size == info["bytes"])
catalog = {}
for file in sorted((ROOT / "data/afirmaciones").glob("*.csv")):
    for row in csvrows(file):
        check("C_unica_viva", row["#"], row["#"] not in catalog)
        catalog[row["#"]] = row
future = dict(catalog)
for item in p["objetos"] + p["materializacion_atomica_prospectiva"]:
    ident = item["tipo"] + ":" + item["identidad"]
    old, new = item["antes"], item["despues"]
    for label, value in (("antes", old), ("despues", new)):
        check("huella_objeto", ident + ":" + label,
              item["sha256_" + label] == (None if value is None else rowhash(value)))
    if old is not None:
        actual = csvrows(item["ruta"]) if item["ruta"].endswith(".csv") else (ROOT / item["ruta"]).read_text()
        check("antes_vivo", ident, (sum(row == old for row in actual) == 1) if isinstance(actual, list) else actual.count(old) == 1)
    if "campos_modificados" in item:
        check("delta_campos", ident, item["campos_modificados"] == [k for k in old if old[k] != new[k]])
    if item["tipo"] in {"C", "C_ALTA", "C_ATOMICA_VISTA_PROSPECTIVA"}:
        if item["tipo"] == "C_ALTA":
            check("alta_no_existente", ident, new["#"] not in catalog)
        future[new["#"]] = new
for item in p["conservados"]:
    check("conservado", item["identidad"], item["fila"] == catalog[item["identidad"]])
for item in e["C_propuestas"]:
    check("evidencia_autor_C", item["identidad"], item["fila"] == future[item["identidad"]] and item["sha256"] == rowhash(item["fila"]))
tables = {x["fila_csv"]: x for x in p["objetos"] if x["tipo"].startswith("TABLA_")}
maps = csvrows("data/auditoria/mapeo_celdas_afirmaciones.csv")
for item in p["mapeos_propuestos"]:
    a, b = item["antes"], item["despues"]
    check("mapa_antes", item["identidad"], sum(x == a for x in maps) == 1)
    check("mapa_texto", item["identidad"], b["contenido"] == tables[int(b["fila"])]["despues"][b["columna"]] and b["contenido_sha256"] == cellhash(b["contenido"]))
    check("mapa_C_existe_prospectivamente", item["identidad"], all(k in future for k in re.findall(r"C-\d+", b["afirmaciones"])))
for item in p["correcciones_celdas_propuestas"]:
    table = tables[int(item["fila"])]
    key = item["claim_id"]
    check("correccion_textos", key,
          table["antes"][item["columna"]] == item["contenido_previo"]
          and table["despues"][item["columna"]] == item["contenido_corregido"]
          and cellhash(item["contenido_previo"]) == item["contenido_previo_sha256"]
          and cellhash(item["contenido_corregido"]) == item["contenido_corregido_sha256"])
# La identidad histórica se contrasta con el v3 que recibe el consumidor,
# no con el manifiesto de objetivos de celda v2 (son objetos distintos).
residual = {x["claim_id"]: x for x in csvrows("data/auditoria/residuales_trazabilidad_no_conformes_v3.csv")}
dispositions = []
for item in p["disposiciones_propuestas"]:
    key = item["claim_id"]
    check("residual_historico", key, rowhash(residual[key]) == item["sha256_residual"])
    check("C_soporte_prospectivo", key, all(rowhash(future[c]) == h and future[c]["Atribución"] == "expresa" for c, h in item["afirmaciones_soporte"].items()))
    check("evidencia_ligada", key, item["evidencia_autor"]["sha256"] == sha(EVIDENCE.read_bytes()))
    dispositions.append({"claim_id": key, "sha256_propuesta": rowhash({k: v for k, v in item.items() if k != "revision_independiente"}), "componentes": item["componentes"]})
xmlpath = next(x for x in p["fuentes"] if x.endswith(".xml"))
xml = ET.parse(ROOT / xmlpath).getroot()
supplement = next(x for x in p["fuentes"] if x.startswith("/tmp/"))
for key, info in p["pasajes"].items():
    if key.startswith("supl_pdf_"):
        page = key.rsplit("_", 1)[-1]
        raw = subprocess.run(["pdftotext", "-layout", "-f", page, "-l", page, supplement, "-"], capture_output=True, check=True).stdout.decode()
    else:
        raw = "".join(xml.find(f'.//*[@id="{key}"]').itertext())
    check("pasaje", key, cellhash(" ".join(raw.split())) == info["sha256"])
first_appearances = []
for item in p["objetos"]:
    if not item["tipo"].startswith("B_"):
        continue
    row = item["despues"]
    label = row["etiqueta preferida"]
    terms = [label]
    if label == "probabilidad posterior":
        terms += ["PP"]
    if label == "Heimdallarchaeia":
        terms += ["Heimdallarchaeota"]
    if label == "log-verosimilitud":
        terms += ["log-verosimilitudes", "log likelihood", "lnL"]
    matches = []
    for claim in sorted(future, key=lambda k: int(k.split("-")[1])):
        text = " ".join(future[claim].values())
        if any(re.search(r"(?<!\w)" + re.escape(t) + r"(?!\w)", text, re.I) for t in terms):
            matches.append(claim)
    first_appearances.append({"etiqueta": label, "formas_buscadas": terms,
                              "primera_literal": matches[0] if matches else None,
                              "propuesta": row["# de la fila del registro donde aparece por primera vez"],
                              "limite": "Búsqueda nominal literal, no prueba automática de sinonimia taxonómica."})
after = {name: sha((ROOT / name).read_bytes()) for name in sorted(paths)}
print(json.dumps({"utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
                  "rol": "COMPROBACION_MECANICA_NO_DICTAMEN_CIENTIFICO", "inputs_before": before,
                  "inputs_after": after, "inputs_stable": before == after,
                  "n_comprobaciones": len(checks), "fallos": [x for x in checks if not x["pass"]],
                  "comprobaciones_no_censo_C": [x for x in checks if x["tipo"] != "C_unica_viva"],
                  "primeras_apariciones_B": first_appearances, "disposiciones": dispositions,
                  "suplemento_futuro_existe": (ROOT / p["destino_suplemento"]).exists(),
                  "consumidor_real_ejecutado": False}, ensure_ascii=False, separators=(",", ":")))
