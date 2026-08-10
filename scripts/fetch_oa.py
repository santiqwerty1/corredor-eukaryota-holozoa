#!/usr/bin/env python3
"""Resuelve y descarga las fuentes del apéndice A que están en acceso abierto.

El corpus cita 523 fuentes y de muchas sólo se pudo leer el resumen. Este script
busca cuáles de ellas son legalmente accesibles y trae el PDF.

**Qué hace y qué no.** Consulta OpenAlex y Europe PMC —dos catálogos abiertos—
para preguntar por cada DOI si existe una versión de acceso abierto, y descarga
únicamente lo que esos catálogos declaran abierto. No accede a repositorios
piratas, no sortea muros de pago y no toca las fuentes cerradas: esas se listan
en el informe como lo que son, un hueco declarado.

**El informe importa tanto como los PDF.** `exports/acceso_fuentes.csv` deja por
escrito, fuente a fuente, si hay versión abierta, por qué vía, y si no la hay,
la razón. Una fuente que no se pudo obtener nunca desaparece en silencio: ése es
el mismo principio que gobierna las búsquedas negativas del corpus.

**Los PDF no se versionan.** Van a `fuentes_pdf/`, que está en .gitignore. Sus
licencias son heterogéneas —«bronze» significa legible en la web del editor,
sin licencia abierta explícita— y mezclarlos con un repositorio CC BY 4.0
rompería la frontera de licencias del proyecto.

Uso:
    python3 scripts/fetch_oa.py --mailto tu@correo            # resolver y descargar
    python3 scripts/fetch_oa.py --mailto tu@correo --solo-informe
    python3 scripts/fetch_oa.py --mailto tu@correo --limite 20
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APENDICE_A = ROOT / "data" / "apendices" / "A_fuentes.csv"
INFORME = ROOT / "exports" / "acceso_fuentes.csv"
DESTINO = ROOT / "fuentes_pdf"

OPENALEX = "https://api.openalex.org/works"
EUROPEPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
LOTE = 50  # tope de la API de OpenAlex por consulta

# Identificarse es la norma de cortesía de estas APIs y da acceso al «polite
# pool», más estable. La pausa entre descargas evita castigar a los servidores
# de los editores, que ceden estos PDF de buena fe.
AGENTE = "corredor-eukaryota-holozoa/fetch_oa (+https://github.com/santiqwerty1/corredor-eukaryota-holozoa)"
PAUSA_API = 0.3
PAUSA_DESCARGA = 1.0

CABECERA_INFORME = [
    "clave", "año", "título", "doi", "acceso", "vía", "url_pdf",
    "fichero", "resultado", "detalle",
]


def _pedir(url: str, timeout: int = 40, binario: bool = False):
    req = urllib.request.Request(url, headers={
        "User-Agent": AGENTE,
        "Accept": "application/pdf,*/*" if binario else "application/json",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read() if binario else json.load(r)


def leer_apendice_a() -> list[dict]:
    """Las fuentes tal como las declara el corpus. No se modifica nada aquí."""
    with APENDICE_A.open(encoding="utf-8", newline="") as fh:
        filas = list(csv.reader(fh))
    cab, cuerpo = filas[0], filas[1:]
    idx = {n: i for i, n in enumerate(cab)}
    col_doi = next(i for n, i in idx.items() if n.startswith("DOI"))
    fuentes = []
    for f in cuerpo:
        if not f or not f[0].strip():
            continue
        bruto = f[col_doi] if len(f) > col_doi else ""
        m = re.search(r"10\.\d{4,9}/\S+", bruto or "")
        fuentes.append({
            "clave": f[0].strip(),
            "año": f[2].strip() if len(f) > 2 else "",
            "titulo": f[3].strip() if len(f) > 3 else "",
            "doi": m.group(0).rstrip(".").lower() if m else "",
            "url": (bruto or "").strip(),
        })
    return fuentes


def resolver_openalex(dois: list[str], mailto: str) -> dict[str, dict]:
    """Pregunta a OpenAlex, en lotes, si cada DOI tiene versión abierta."""
    hallado: dict[str, dict] = {}
    for i in range(0, len(dois), LOTE):
        trozo = dois[i:i + LOTE]
        filtro = "doi:" + "|".join("https://doi.org/" + d for d in trozo)
        url = (f"{OPENALEX}?per-page={LOTE}&mailto={urllib.parse.quote(mailto)}"
               "&select=doi,open_access,best_oa_location,publication_year"
               "&filter=" + urllib.parse.quote(filtro, safe=":|/.-"))
        try:
            datos = _pedir(url)
        except Exception as exc:                      # noqa: BLE001
            print(f"  aviso: lote {i // LOTE + 1} no resuelto ({exc})", file=sys.stderr)
            time.sleep(PAUSA_API)
            continue
        for w in datos.get("results", []):
            clave = (w.get("doi") or "").replace("https://doi.org/", "").lower()
            oa = w.get("open_access") or {}
            loc = w.get("best_oa_location") or {}
            hallado[clave] = {
                "abierto": bool(oa.get("is_oa")),
                "estado": oa.get("oa_status") or "",
                "pdf": loc.get("pdf_url") or oa.get("oa_url") or "",
                "via": "openalex",
            }
        print(f"  lote {i // LOTE + 1}/{(len(dois) + LOTE - 1) // LOTE} · "
              f"{len(hallado)} resueltos", file=sys.stderr)
        time.sleep(PAUSA_API)
    return hallado


def resolver_europepmc(doi: str) -> dict | None:
    """Segunda oportunidad: Europe PMC indexa textos completos que OpenAlex a
    veces no enlaza, sobre todo en ciencias de la vida —justo este corpus."""
    url = (f"{EUROPEPMC}?query={urllib.parse.quote(f'DOI:{doi}')}"
           "&format=json&pageSize=1&resultType=core")
    try:
        datos = _pedir(url, timeout=25)
    except Exception:                                  # noqa: BLE001
        return None
    res = (datos.get("resultList") or {}).get("result") or []
    if not res:
        return None
    r = res[0]
    if r.get("isOpenAccess") != "Y":
        return None
    pmcid = r.get("pmcid")
    if not pmcid:
        return None
    return {
        "abierto": True,
        "estado": "open (europepmc)",
        "pdf": f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextPDF",
        "via": "europepmc",
    }


def nombre_fichero(f: dict) -> str:
    """`S056 [2024] Reconstructing the last common ancestor.pdf`.

    La clave va delante para que el fichero se rastree hasta la fila del
    apéndice A sin depender del título, que se trunca.
    """
    t = unicodedata.normalize("NFKD", f["titulo"])
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^\w\s-]", "", t).strip()
    t = re.sub(r"\s+", " ", t)[:70].strip()
    return f"{f['clave']} [{f['año'] or 's.f.'}] {t}.pdf".replace("/", "-")


def descargar(url: str, destino: Path) -> tuple[str, str]:
    """Devuelve (resultado, detalle). Rechaza lo que no sea un PDF de verdad.

    Un muro de pago responde 200 con una página HTML de «inicie sesión»; sin
    esta comprobación el directorio se llenaría de ficheros .pdf que son avisos
    de acceso denegado, y el informe diría que se obtuvo algo que no se obtuvo.
    """
    try:
        cuerpo = _pedir(url, timeout=90, binario=True)
    except urllib.error.HTTPError as exc:
        return "error", f"HTTP {exc.code}"
    except Exception as exc:                           # noqa: BLE001
        return "error", str(exc)[:80]

    if not cuerpo.startswith(b"%PDF"):
        cabeza = cuerpo[:200].lower()
        que = "HTML" if b"<html" in cabeza or b"<!doctype" in cabeza else "desconocido"
        return "rechazado", f"la respuesta no es un PDF ({que}, {len(cuerpo)} bytes)"
    if len(cuerpo) < 8192:
        return "rechazado", f"PDF sospechosamente pequeño ({len(cuerpo)} bytes)"

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(cuerpo)
    return "descargado", f"{len(cuerpo) // 1024} KB"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Descarga las fuentes del apéndice A que están en acceso abierto")
    ap.add_argument("--mailto", required=True,
                    help="tu correo: lo exigen OpenAlex y Europe PMC para identificar al que consulta")
    ap.add_argument("--solo-informe", action="store_true",
                    help="resolver el acceso sin descargar nada")
    ap.add_argument("--limite", type=int, default=0,
                    help="procesar sólo las primeras N fuentes (para probar)")
    ap.add_argument("--destino", type=Path, default=DESTINO)
    args = ap.parse_args()

    fuentes = leer_apendice_a()
    if args.limite:
        fuentes = fuentes[:args.limite]
    con_doi = [f for f in fuentes if f["doi"]]
    print(f"{len(fuentes)} fuentes en el apéndice A · {len(con_doi)} con DOI", file=sys.stderr)

    print("resolviendo en OpenAlex…", file=sys.stderr)
    oa = resolver_openalex([f["doi"] for f in con_doi], args.mailto)

    # A las que OpenAlex no da por abiertas se les pregunta a Europe PMC.
    pendientes = [f for f in con_doi if not oa.get(f["doi"], {}).get("abierto")]
    if pendientes:
        print(f"consultando Europe PMC por {len(pendientes)} fuentes sin OA en OpenAlex…",
              file=sys.stderr)
        for i, f in enumerate(pendientes, 1):
            alt = resolver_europepmc(f["doi"])
            if alt:
                oa[f["doi"]] = alt
            if i % 25 == 0:
                print(f"  {i}/{len(pendientes)}", file=sys.stderr)
            time.sleep(PAUSA_API)

    filas, cuenta = [], {}
    def marcar(k): cuenta[k] = cuenta.get(k, 0) + 1

    for f in fuentes:
        info = oa.get(f["doi"], {}) if f["doi"] else {}
        fichero = resultado = detalle = ""
        if not f["doi"]:
            acceso, via, url = "sin doi", "", f["url"]
            resultado, detalle = "no resoluble", "la fuente no declara DOI; sólo URL"
        elif not info:
            acceso, via, url = "desconocido", "", ""
            resultado, detalle = "no resoluble", "ningún catálogo abierto reconoce este DOI"
        elif not info.get("abierto"):
            acceso, via, url = "cerrado", info.get("via", ""), ""
            resultado, detalle = "cerrada", "sin versión de acceso abierto declarada"
        else:
            acceso, via, url = info.get("estado", "abierto"), info.get("via", ""), info.get("pdf", "")
            if not url:
                resultado, detalle = "sin url", "declarada abierta pero sin PDF enlazado"
            elif args.solo_informe:
                resultado, detalle = "no intentado", "modo --solo-informe"
            else:
                fichero = nombre_fichero(f)
                ruta = args.destino / fichero
                if ruta.exists() and ruta.stat().st_size > 8192:
                    resultado, detalle = "ya estaba", f"{ruta.stat().st_size // 1024} KB"
                else:
                    resultado, detalle = descargar(url, ruta)
                    time.sleep(PAUSA_DESCARGA)
                    # El enlace «mejor» de OpenAlex apunta a veces a la página
                    # del artículo, no al PDF, y algunos editores rechazan a los
                    # clientes automáticos. Europe PMC sirve el mismo trabajo por
                    # otra vía legal, así que se prueba antes de darlo por perdido.
                    if resultado != "descargado" and info.get("via") != "europepmc":
                        alt = resolver_europepmc(f["doi"])
                        if alt and alt.get("pdf"):
                            r2, d2 = descargar(alt["pdf"], ruta)
                            time.sleep(PAUSA_DESCARGA)
                            if r2 == "descargado":
                                resultado, detalle = r2, d2 + " (vía Europe PMC)"
                                via, url = "europepmc", alt["pdf"]
                            else:
                                detalle += f"; Europe PMC tampoco ({d2})"
                    if resultado != "descargado":
                        fichero = ""
        marcar(resultado)
        filas.append([f["clave"], f["año"], f["titulo"], f["doi"], acceso, via,
                      url, fichero, resultado, detalle])
        if resultado in ("descargado", "rechazado", "error"):
            print(f"  {f['clave']:6} {resultado:11} {detalle}", file=sys.stderr)

    INFORME.parent.mkdir(parents=True, exist_ok=True)
    with INFORME.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(CABECERA_INFORME)
        w.writerows(filas)

    print("\n" + "=" * 62, file=sys.stderr)
    print(f"informe: {INFORME.relative_to(ROOT)}", file=sys.stderr)
    for k in sorted(cuenta, key=lambda x: -cuenta[x]):
        print(f"  {cuenta[k]:5}  {k}", file=sys.stderr)
    faltan = sum(v for k, v in cuenta.items() if k not in ("descargado", "ya estaba"))
    print(f"\n{faltan} fuentes siguen sin texto completo, y el informe dice por qué "
          f"una a una.\nNo hay huecos silenciosos: ésa es la regla del corpus.",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
