"""Reinspección R3 propia. No escribe canon ni modifica fixtures anteriores."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIOR = ROOT / "docs/auditorias/fixtures/reinspeccion_independiente_segmentacion_ncden02_20260927.py"
spec = importlib.util.spec_from_file_location("ncden02_prior_r2_independent", PRIOR)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
trace = prior.trace


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


WRAPPERS = [
    ("curly_single", "‘", "’"),
    ("single_guillemets", "‹", "›"),
    ("ascii_single", "'", "'"),
    ("asterisk", "*", "*"),
    ("underscore", "_", "_"),
    ("backtick", "`", "`"),
    ("double_guillemets_control", "«", "»"),
    ("ascii_double_control", '"', '"'),
    ("parentheses_control", "(", ")"),
]

VALID_LINK_BODIES = [
    ("empty_destination_title", '<> "Figura. Dato"'),
    ("angle_contains_spaces_and_period", '<ruta con espacios.a> "Título. Uno"'),
    ("escaped_double_backslash_angle", r"<ruta\\>"),
    ("escaped_open_close_bare", r"ruta\(a\)"),
    ("double_escaped_parenthesis_bare", r"ruta\\(a)"),
    ("quoted_paren_and_sentence", 'ruta "Figura (a. Dato"'),
    ("single_quote_title_unbalanced_paren", "ruta 'Figura a). Dato'"),
    ("parenthesized_title_escaped_open", r"ruta (Figura \(a. Dato)"),
    ("relative_file_colon_fragment", "../archivo.pdf#fig.2"),
    ("angle_close_escape_and_real_close", r"<ruta\>dato>"),
]

INVALID_LINK_BODIES = [
    ("bare_unquoted_after_destination", "ruta Otra proposición. Dato"),
    ("text_after_complete_title", 'ruta "Título" Otra proposición. Dato'),
    ("angle_open_inside_angle", "<ruta<dato>"),
    ("escaped_angle_only_close", r"<ruta\>"),
    ("unclosed_nested_bare", "ruta(a(b)"),
    ("nested_parenthesized_title", "ruta (Título (anidado))"),
    ("quoted_title_no_closing_quote", 'ruta "Título (a'),
    ("empty_destination_bare_prose", "<> Otra proposición. Dato"),
]


def deterministic_sample():
    texts = [a + "El dato consta en https://example.org." + b + " [C-001] Otra proposición. [C-002]"
             for _, a, b in WRAPPERS]
    texts.extend("Dato. [C-001](" + body + ") Otro. [C-002]" for _, body in VALID_LINK_BODIES)
    data = [{"text": text, "spans": trace.sentence_spans(text),
             "diagnostics": trace.sentence_boundary_diagnostics(text)} for text in texts]
    return sha(json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def input_hashes():
    paths = set((ROOT / "docs/secciones").glob("*.md"))
    paths.update((ROOT / "data/afirmaciones").glob("*.csv"))
    paths.update({ROOT / "data/table_index.json", trace.CELL_MANIFEST, trace.OUTPUT,
                  ROOT / "scripts/build_content_trace.py", ROOT / "tests/test_content_trace_sentence_boundaries.py",
                  Path(__file__), PRIOR})
    index = json.loads((ROOT / "data/table_index.json").read_text())
    paths.update(ROOT / row["csv_path"] for row in index["tables"])
    return {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in sorted(paths)}


def run():
    start = now()
    before = input_hashes()
    rerun = prior.run()
    checks, pipelines = [], []

    def exact(name, first, second):
        text = first + " " + second
        spans = trace.sentence_spans(text)
        actual = trace.split_sentences(text)
        checks.append({"case": name, "text": text, "expected": [first, second], "actual": actual,
                       "spans": spans, "diagnostics": trace.sentence_boundary_diagnostics(text),
                       "pass": actual == [first, second],
                       "slice_roundtrip": [text[a:b] for a,b in spans] == actual,
                       "nonblank_conservation": "".join(text.split()) == "".join("".join(actual).split())})

    def pipeline(name, text, accept):
        result = prior.initial.fixture_main(text)
        success = (result["main_write_exit"] == result["main_check_exit"] == 0
                   and len(result["segments"]) == 2
                   and all(s["claims"] for s in result["segments"])) if accept else (
                       result["main_write_exit"] != 0 and not result["output_written"])
        pipelines.append({"case": name, "text": text,
                          "expected": "ACEPTAR_DOS_CON_C_PROPIA" if accept else "RECHAZAR_SIN_ESCRIBIR",
                          "pass": success, **result})

    for name, opening, closing in WRAPPERS:
        first = opening + "El dato consta en https://example.org." + closing + " [C-001]"
        exact("url_terminal_" + name, first, "Otra proposición. [C-002]")
        pipeline("url_terminal_missing_" + name, first + " Otra proposición sin cita.", False)

    for name, body in VALID_LINK_BODIES:
        first = "Dato. [C-001](" + body + ")"
        exact("link_grammar_" + name, first, "Otro dato. [C-002]")
        end = trace.citation_end(first, first.index("["))
        checks.append({"case": "link_end_" + name, "text": first, "expected": len(first),
                       "actual": end, "pass": end == len(first)})
        pipeline("link_pipeline_" + name, first + " Otro dato. [C-002]", True)

    for name, body in INVALID_LINK_BODIES:
        text = "Dato. [C-001](" + body + ")"
        end = trace.citation_end(text, text.index("["))
        checks.append({"case": "invalid_link_end_" + name, "text": text, "actual": end,
                       "expected": None, "pass": end is None})
        pipeline("invalid_link_pipeline_" + name, text, False)

    # Estas combinaciones son ambiguas, no adjudicaciones científicas.
    for name, text in [
        ("spp_after_quote", "‘Se analizaron spp.’ otra proposición. [C-001]"),
        ("cf_italic_extended_taxon", "Se examinó _B. cf. floridanus_ [C-001]."),
        ("unmarked_initial", "Se examinó B. floridanus [C-001]."),
    ]:
        result = prior.initial.fixture_main(text)
        checks.append({"case": name, "text": text, "expected": "AMBIGUA_Y_BLOQUEADA",
                       "pass": bool(result["ambiguities"]) and result["main_write_exit"] != 0
                           and not result["output_written"], "pipeline": result})

    seeds = []
    for seed in ("1", "17", "981"):
        environment = dict(os.environ, PYTHONHASHSEED=seed)
        process = subprocess.run([sys.executable, str(Path(__file__)), "--digest"],
                                 cwd=ROOT, env=environment, capture_output=True, text=True, check=False)
        seeds.append({"seed": seed, "exit": process.returncode, "stdout": process.stdout.strip(),
                      "stderr": process.stderr})

    # Censo independiente sólo en memoria. Dos materializaciones, sin main vivo.
    narrative = trace.narrative_segments()
    cells = trace.table_cells()
    manifest, manifest_errors = trace.load_cell_manifest()
    manifest_errors.extend(trace.cell_manifest_errors(cells, manifest))
    tables = trace.table_segments(cells, manifest)
    first_payload = trace.csv_bytes(narrative + tables)
    second_payload = trace.csv_bytes(trace.narrative_segments() + trace.table_segments(trace.table_cells(), manifest))
    ambiguities = trace.narrative_ambiguities()
    reasons = Counter(f["razon"] for item in ambiguities for f in item["fronteras"])
    after = input_hashes()
    return {"revisor": "/root/inspeccion_relojes", "autor_implementacion": "/root/verificacion_fuentes_nuevas",
            "independencia": "Sin participación en esta implementación; autoría científica distinta excluida del dictamen.",
            "inicio_utc": start, "fin_utc": now(), "hashes_before": before, "hashes_after": after,
            "inputs_stable": before == after, "historical_suites_reexecuted": rerun,
            "additional_checks": checks, "additional_pipelines": pipelines,
            "counts": {"checks": len(checks), "pass": sum(x["pass"] for x in checks),
                       "fail": sum(not x["pass"] for x in checks), "pipelines": len(pipelines),
                       "pipeline_pass": sum(x["pass"] for x in pipelines),
                       "pipeline_fail": sum(not x["pass"] for x in pipelines)},
            "hashseed_runs": seeds, "hashseed_identical": all(x["exit"] == 0 for x in seeds)
                and len({x["stdout"] for x in seeds}) == 1,
            "census_in_memory": {"narrative": len(narrative), "tables": len(tables),
                "total": len(narrative) + len(tables), "without_C": sum(not s.claims for s in narrative+tables),
                "ambiguous_blocks": len(ambiguities), "ambiguous_frontiers": sum(reasons.values()),
                "reasons": dict(reasons), "manifest_errors": manifest_errors,
                "payload_errors": trace.validate_payload(first_payload),
                "first_sha256": sha(first_payload), "second_sha256": sha(second_payload),
                "two_runs_identical": first_payload == second_payload,
                "no_adjudication": True},
            "limites": "NC-DEN01, ciencia y cierre global excluidos. Ninguna traza canónica escrita. Los casos sintéticos prueban comportamiento, no un error científico existente en las fuentes."}


if __name__ == "__main__":
    if "--digest" in sys.argv:
        print(deterministic_sample())
    else:
        print(json.dumps(run(), ensure_ascii=False, indent=2))
