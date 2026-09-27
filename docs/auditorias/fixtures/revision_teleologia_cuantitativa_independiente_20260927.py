"""Adversarios propios del delta cuantitativo, sin editar detector ni corpus.

La ablación solo desactiva en memoria la rama nueva para comparar el cambio;
no representa una versión histórica completa del script.
"""
import ast
import hashlib
import inspect
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from scripts import audit_requirement_controls as c


class WithoutNewBranch(ast.NodeTransformer):
    def visit_Name(self, node):
        if node.id == "quantified_occurrences" and isinstance(node.ctx, ast.Load):
            return ast.copy_location(ast.Constant(False), node)
        return node


tree = ast.parse(inspect.getsource(c.check_teleology_candidates))
tree = ast.fix_missing_locations(WithoutNewBranch().visit(tree))
namespace = dict(vars(c))
exec(compile(tree, "<independent-in-memory-ablation>", "exec"), namespace)
before = namespace["check_teleology_candidates"]


def inspect_fixture(root, path, text, detector):
    path.write_text(text + "\n", encoding="utf-8")
    corpus = SimpleNamespace(root=root, section_paths=[path], claim_paths={"C-9000": path},
                             index={"tables": [{"csv_path": path.relative_to(root).as_posix()}]},
                             appendix_paths={"A": path})
    result = c.Result("R-0002", "FIXTURE_NO_CONTROL_REAL")
    detector(corpus, result)
    return {"accepted": not result.errors, "candidates": result.metrics["candidatos_teleologia"],
            "scope": [p.relative_to(root).as_posix() for p in sorted(result.scope_paths)], "errors": result.errors}


positive = (
    "Se informa el cuartil superior.",
    "Se informa el CUARTIL INFERIOR.",
    "Se registra identidad proteica superior al 70 %.",
    "Se registra identidad proteica inferior al 70.5%.",
    "Se registra identidad superior al 70,5 %.",
    "Se registra identidad inferior al 0 %.",
    "Se comparan el cuartil superior y el cuartil inferior.",
    "Identidad superior al 100 % e identidad inferior al 70 %.",
)
forbidden = (
    "este linaje es superior", "este linaje es inferior", "este linaje es primitivo",
    "este linaje es avanzado", "este linaje es más evolucionado", "es un intento fallido",
    "es un paso obligatorio", "es un fósil viviente", "es el eslabón perdido",
    "es un eucariota primitivo", "es un organismo simple", "es una versión antigua",
    "es una versión detenida", "apareció para llegar a animales", "todavía no había desarrollado complejidad",
)
cases = [("quantitative", sentence, True, 1) for sentence in positive]
cases += [("teleology", sentence + ".", False, 1) for sentence in forbidden]
for good in positive:
    for bad in forbidden:
        cases += [("mixed_suffix", good + "; " + bad + ".", False, 1),
                  ("mixed_prefix", bad + "; " + good, False, 1)]
cases += [
    ("not_identity", "El linaje es superior al 70 % de los restantes.", False, 1),
    ("not_numeric", "Su identidad proteica es superior.", False, 1),
    ("no_percentage", "Su identidad proteica superior al 70 se describe aquí.", False, 1),
    ("not_quartile", "Se trata de un cuartil de linajes superior.", False, 1),
    ("line_boundary", "Se informa el cuartil superior.\nEste linaje es primitivo.", False, 2),
]
results = []
with tempfile.TemporaryDirectory() as raw:
    root = Path(raw)
    path = root / "fixture.md"
    for kind, sentence, expected, count in cases:
        old = inspect_fixture(root, path, sentence, before)
        new = inspect_fixture(root, path, sentence, c.check_teleology_candidates)
        passed = new["accepted"] == expected and old["candidates"] == new["candidates"] == count and old["scope"] == new["scope"] == ["fixture.md"]
        results.append({"kind": kind, "text": sentence, "expected_accepted": expected, "before_ablation": old, "after": new, "result": "PASS" if passed else "FAIL"})
    # Límites preexistentes: la excepción nueva no debe adjudicarse su origen.
    legacy = []
    for text in ("La identidad es superior a 70 %; este linaje es primitivo.",
                 "Hay un criterio; este linaje es más evolucionado."):
        legacy.append({"text": text, "before_ablation": inspect_fixture(root, path, text, before),
                       "after": inspect_fixture(root, path, text, c.check_teleology_candidates)})

live = c.Corpus(ROOT)
old_result = c.Result("R-0002", "LECTURA_DIAGNOSTICA_NO_CIERRE")
new_result = c.Result("R-0002", "LECTURA_DIAGNOSTICA_NO_CIERRE")
before(live, old_result)
c.check_teleology_candidates(live, new_result)
same_population = old_result.metrics == new_result.metrics and old_result.scope_paths == new_result.scope_paths
files = ("scripts/audit_requirement_controls.py", "tests/test_audit_requirement_controls.py", str(Path(__file__).relative_to(ROOT)))
print(json.dumps({
    "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "scope": "Revisión técnica independiente del delta cuantitativo; no firma R0001–7 ni ciencia.",
    "hashes": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in files},
    "tests": len(results), "passed": sum(r["result"] == "PASS" for r in results), "results": results,
    "legacy_limitations_not_introduced": legacy,
    "live_corpus": {"same_population_and_scope": same_population,
                    "scope_paths": len(new_result.scope_paths), "candidates_before": old_result.metrics["candidatos_teleologia"],
                    "candidates_after": new_result.metrics["candidatos_teleologia"],
                    "errors_without_new_branch": old_result.errors, "errors_after": new_result.errors},
}, ensure_ascii=False, indent=2))
