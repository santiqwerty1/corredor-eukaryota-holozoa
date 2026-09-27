"""Adversarios complementarios y expectativa S canónica corregida del revisor.

Conserva la fixture inicial y su FAIL erróneo sobre S1/S01 sin reescribirlos.
No se admiten alias bibliográficos no declarados por el corpus canónico.
"""
import hashlib
import json
import runpy
import tempfile
from datetime import datetime, timezone
from pathlib import Path

n = runpy.run_path(str(Path(__file__).with_name("revision_disposiciones_independiente_20260927.py")))
ROOT, d, a, Fixture, csvwrite, jsonwrite, write, sha, record, insists = (n[k] for k in ("ROOT", "d", "a", "Fixture", "csvwrite", "jsonwrite", "write", "sha", "record", "insist"))

# Adaptación EXPLÍCITA al campo prospectivo nuevo. La fixture original queda
# intacta y no puede aprobar por omitir identidad_fila en el contrato ampliado.
OldFixture = Fixture
class Fixture(OldFixture):
    def save(self):
        self.record["identidad_fila"] = {"sistema": "Sistema artificial"}
        csvwrite(self.root, self.residual["csv_path"], ["sistema", "valor"],
                 [{"sistema": "Sistema artificial", "valor": self.target["contenido"]}])
        super().save()

for helper in ("baseline", "review_identity", "source_range", "claim_symlink", "declaration", "mutation", "changed_proposal"):
    n[helper].__globals__["Fixture"] = Fixture


def claim_range():
    with tempfile.TemporaryDirectory() as raw:
        f = Fixture(Path(raw))
        second = {**f.claim, "#": "C-9002"}
        csvwrite(f.root, "data/afirmaciones/15.csv", a.CLAIM_HEADER, [f.claim, second])
        value = "Dato artificial [C-9000–C-9002]"
        f.record.update({"contenido_nuevo": value, "sha256_nuevo": d.cell_hash(value), "afirmaciones_soporte": {"C-9000": d.row_hash(f.claim), "C-9002": d.row_hash(second)}})
        f.correction.update({"contenido_corregido": value, "contenido_corregido_sha256": d.cell_hash(value)})
        f.review["disposicion_sha256"] = d.proposal_hash(f.record)
        p = jsonwrite(f.root, "docs/revision.json", f.review)
        f.record["revision_independiente"] = {"ruta": "docs/revision.json", "sha256": sha(p)}
        jsonwrite(f.root, d.REGISTRY, {"version": 1, "disposiciones": [f.record]})
        return n["rejects"](f)


def noncanonical_source():
    with tempfile.TemporaryDirectory() as raw:
        f = Fixture(Path(raw))
        f.claim["Fuente"] = "S1 Results, párrafo 1"
        f.source.rename(f.root / "fuentes/S1 ensayo.txt")
        f.record["artefactos_soporte"] = {"fuentes/S1 ensayo.txt": sha(f.root / "fuentes/S1 ensayo.txt")}
        f.review["pasajes"] = [f.passage("fuentes/S1 ensayo.txt")]
        f.save()
        return n["rejects"](f)


def figure_not_source():
    with tempfile.TemporaryDirectory() as raw:
        f = Fixture(Path(raw))
        f.claim["Fuente"] = "S01 Results; Fig. S02"
        f.save()
        insists(set(f.load()) == {"C-2708"}, "Figura S02 interpretada como clave bibliográfica")
        return "La figura suplementaria S02 no requiere un artefacto de una segunda fuente."


def changed_row_identity():
    with tempfile.TemporaryDirectory() as raw:
        f = Fixture(Path(raw))
        csvwrite(f.root, f.residual["csv_path"], ["sistema", "valor"],
                 [{"sistema": "Otro sujeto no revisado", "valor": f.target["contenido"]}])
        return n["rejects"](f)


record("valid_history_determinism", n["baseline"])
for name in ("Autor-Ensayo", " autor-ensayo ", "AUTOR-ENSAYO", "NO_ASIGNADO", "pendiente", "Ａｕｔｏｒ-Ｅｎｓａｙｏ"):
    record("review_identity_" + name, lambda name=name: n["review_identity"](name))
record("range_missing_middle_source", n["source_range"])
record("range_missing_middle_claim", claim_range)
record("noncanonical_source_in_claim_and_artifact", noncanonical_source)
record("supplementary_figure_is_not_source", figure_not_source)
record("claim_catalog_external_symlink", n["claim_symlink"])
for value in ("", "self-certification", d.DECLARATION.lower()):
    record("independence_" + value, lambda value=value: n["declaration"](value))
for kind in ("source", "review", "registry"):
    record("mutation_" + kind, lambda kind=kind: n["mutation"](kind))
record("changed_proposal", n["changed_proposal"])
record("changed_subject_at_same_coordinates", changed_row_identity)
print(json.dumps({"utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "hashes": {p: sha(ROOT / p) for p in ("scripts/residual_semantic_dispositions.py", "scripts/remediate_trace_residuals.py", "scripts/build_atomic_cell_claims.py", str(Path(__file__).relative_to(ROOT)))}, "tests": len(n["RESULTS"]), "passed": sum(x["result"] == "PASS" for x in n["RESULTS"]), "results": n["RESULTS"]}, ensure_ascii=False, indent=2))
