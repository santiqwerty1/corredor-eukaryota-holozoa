"""Pruebas independientes de ligadura, no dictámenes científicos reales.

Todos los datos y firmas artificiales se crean exclusivamente en /tmp.
"""
import contextlib
import copy
import csv
import hashlib
import io
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from scripts import residual_semantic_dispositions as d
from scripts import build_atomic_cell_claims as a


def write(root, path, value):
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(value.encode() if isinstance(value, str) else value)
    return p


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def jsonwrite(root, path, value):
    return write(root, path, json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n")


def csvwrite(root, path, fields, rows):
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=fields, quoting=csv.QUOTE_ALL, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return write(root, path, output.getvalue())


class Fixture:
    def __init__(self, root):
        self.root = root
        self.claim = dict.fromkeys(a.CLAIM_HEADER, "Ensayo técnico artificial")
        self.claim.update({"#": "C-9000", "Atribución": "expresa", "Fuente": "S01 Results, párrafo 1", "Fuerza": "alta"})
        self.claim_path = csvwrite(root, "data/afirmaciones/15.csv", a.CLAIM_HEADER, [self.claim])
        self.source = write(root, "fuentes/S01 ensayo.txt", "Dato artificial de fixture, no evidencia científica real.")
        self.author = write(root, "docs/autor.md", "Propuesta artificial, no usar para aprobar el corpus.")
        self.residual = {"claim_id": "C-2708", "csv_path": "data/tablas/09/ensayo.csv", "fila": "2", "columna": "valor", "contenido_anterior": "valor rechazado", "contenido_sha256": d.cell_hash("valor rechazado"), "resultado": "NO_CONFORME"}
        identity = {k: self.residual[k] for k in ("claim_id", "csv_path", "fila", "columna")}
        self.target = {**identity, "contenido": "hueco histórico", "contenido_sha256": d.cell_hash("hueco histórico")}
        self.correction = {**identity, "contenido_previo": self.target["contenido"], "contenido_previo_sha256": self.target["contenido_sha256"], "contenido_corregido": "Dato artificial [C-9000]", "contenido_corregido_sha256": d.cell_hash("Dato artificial [C-9000]"), "autor_correccion": "Autor-Ensayo", "evidencia_correccion": "docs/autor.md"}
        self.record = {**identity, "bn": "BN-147", "sha256_residual": d.row_hash(self.residual), "contenido_previo": self.target["contenido"], "sha256_previo": self.target["contenido_sha256"], "contenido_nuevo": self.correction["contenido_corregido"], "sha256_nuevo": self.correction["contenido_corregido_sha256"], "autor": "Autor-Ensayo", "fecha_utc": "2026-09-27T01:00:00Z", "componentes": ["dato artificial"], "limites_pendientes": "No aprueba ciencia; fixture artificial.", "afirmaciones_soporte": {"C-9000": d.row_hash(self.claim)}, "artefactos_soporte": {"fuentes/S01 ensayo.txt": sha(self.source)}, "evidencia_autor": {"ruta": "docs/autor.md", "sha256": sha(self.author)}}
        self.review = {"version": 1, "claim_id": "C-2708", "disposicion_sha256": "", "revisor": "Revisor-Ensayo", "fecha_utc": "2026-09-27T01:01:00Z", "dictamen": "CONFORME", "independencia": d.DECLARATION, "cobertura": {"dato artificial": [0]}, "pasajes": [self.passage("fuentes/S01 ensayo.txt")], "limitaciones": "Solo test; no dictamen científico."}
        self.save()

    def passage(self, path):
        return {"artefacto": path, "sha256_artefacto": sha(self.root / path), "localizador": "párrafo 1", "fragmento_control": "Dato artificial de fixture", "sha256_pasaje": hashlib.sha256(b"Dato artificial de fixture").hexdigest()}

    def save(self):
        csvwrite(self.root, "data/afirmaciones/15.csv", a.CLAIM_HEADER, [self.claim])
        self.record["afirmaciones_soporte"] = {self.claim["#"]: d.row_hash(self.claim)}
        self.review["disposicion_sha256"] = d.proposal_hash(self.record)
        review = jsonwrite(self.root, "docs/revision.json", self.review)
        self.record["revision_independiente"] = {"ruta": "docs/revision.json", "sha256": sha(review)}
        jsonwrite(self.root, d.REGISTRY, {"version": 1, "disposiciones": [self.record]})

    def load(self):
        return d.load(self.root, [self.residual], [self.target], [self.correction], start_bn=147, positive_claims={"C-2472", "C-2489"})


RESULTS = []


def insist(value, message):
    if not value:
        raise AssertionError(message)


def record(name, function):
    try:
        RESULTS.append({"case": name, "result": "PASS", "detail": function()})
    except Exception as exc:
        RESULTS.append({"case": name, "result": "FAIL", "detail": f"{type(exc).__name__}: {exc}"})


def rejects(f):
    try:
        f.load()
    except RuntimeError as exc:
        return "Rechazo: " + str(exc)
    raise AssertionError("Admite la disposición adversaria como vigente")


def baseline():
    with tempfile.TemporaryDirectory() as raw:
        f = Fixture(Path(raw))
        before = copy.deepcopy((f.residual, f.target, f.correction))
        insist(f.load() == f.load(), "No determinista")
        insist(before == (f.residual, f.target, f.correction), "Mutación de historia")
        return "Fixture íntegra repetible, historia intacta."


def review_identity(value):
    with tempfile.TemporaryDirectory() as raw:
        f = Fixture(Path(raw))
        f.review["revisor"] = value
        f.save()
        return rejects(f)


def source_range():
    with tempfile.TemporaryDirectory() as raw:
        f = Fixture(Path(raw))
        f.claim["Fuente"] = "S01–S03 Results, párrafo 1"
        source = write(f.root, "fuentes/S03 ensayo.txt", "Otra fuente artificial.")
        f.record["artefactos_soporte"]["fuentes/S03 ensayo.txt"] = sha(source)
        f.review["pasajes"].append(f.passage("fuentes/S03 ensayo.txt"))
        f.review["cobertura"]["dato artificial"] = [0, 1]
        f.save()
        return rejects(f)


def source_alias():
    with tempfile.TemporaryDirectory() as raw:
        f = Fixture(Path(raw))
        f.claim["Fuente"] = "S1 Results, párrafo 1"
        f.save()
        insist(set(f.load()) == {"C-2708"}, "Alias canónico S1/S01 no reconocido")
        return "Alias normalizado a identidad canónica."


def claim_symlink():
    with tempfile.TemporaryDirectory() as raw:
        base = Path(raw)
        root = base / "corpus"
        f = Fixture(root)
        outside = write(base, "fuera.csv", f.claim_path.read_bytes())
        f.claim_path.unlink()
        f.claim_path.symlink_to(outside)
        return rejects(f)


def declaration(value):
    with tempfile.TemporaryDirectory() as raw:
        f = Fixture(Path(raw))
        f.review["independencia"] = value
        f.save()
        return rejects(f)


def mutation(kind):
    with tempfile.TemporaryDirectory() as raw:
        f = Fixture(Path(raw))
        original = d._artifact
        count = 0
        def read_then_change(root, reference):
            nonlocal count
            result = original(root, reference)
            count += 1
            if count == 1:
                path = {"source": f.source, "review": root / "docs/revision.json", "registry": root / d.REGISTRY}[kind]
                path.write_bytes(path.read_bytes() + b" ")
            return result
        with patch.object(d, "_artifact", side_effect=read_then_change):
            return rejects(f)


def changed_proposal():
    with tempfile.TemporaryDirectory() as raw:
        f = Fixture(Path(raw))
        f.record["limites_pendientes"] = "Propuesta distinta no firmada."
        jsonwrite(f.root, d.REGISTRY, {"version": 1, "disposiciones": [f.record]})
        return rejects(f)


def main():
    record("valid_history_determinism", baseline)
    for name in ("Autor-Ensayo", " autor-ensayo ", "AUTOR-ENSAYO", "NO_ASIGNADO", "pendiente"):
        record("review_identity_" + name, lambda name=name: review_identity(name))
    record("range_missing_middle_source", source_range)
    record("canonical_source_alias", source_alias)
    record("claim_catalog_external_symlink", claim_symlink)
    for value in ("", "self-certification", d.DECLARATION.lower()):
        record("independence_" + value, lambda value=value: declaration(value))
    for kind in ("source", "review", "registry"):
        record("mutation_" + kind, lambda kind=kind: mutation(kind))
    record("changed_proposal", changed_proposal)
    print(json.dumps({"utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "hashes": {p: sha(ROOT / p) for p in ("scripts/residual_semantic_dispositions.py", "scripts/remediate_trace_residuals.py", "scripts/build_atomic_cell_claims.py", str(Path(__file__).relative_to(ROOT)))}, "tests": len(RESULTS), "passed": sum(x["result"] == "PASS" for x in RESULTS), "results": RESULTS}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
