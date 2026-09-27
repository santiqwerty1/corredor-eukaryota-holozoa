"""Segunda inspección propia; no modifica evidencia inicial ni producción."""
import importlib.util
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INITIAL = ROOT / "docs/auditorias/fixtures/revision_independiente_segmentacion_ncden02_20260927.py"
spec = importlib.util.spec_from_file_location("ncden02_initial_independent", INITIAL)
initial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(initial)
trace = initial.trace


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def run():
    start = now()
    paths = [ROOT / "scripts/build_content_trace.py", ROOT / "tests/test_content_trace_sentence_boundaries.py",
             INITIAL, Path(__file__), trace.OUTPUT]
    hashes_before = {str(p.relative_to(ROOT)): sha(p) for p in paths}
    rerun = initial.run()
    tests = []

    def exact(name, first, second):
        text = first + " " + second
        spans = trace.sentence_spans(text)
        actual = trace.split_sentences(text)
        expected = [first, second]
        tests.append({"case": name, "text": text, "expected": expected, "actual": actual,
                      "spans": spans, "diagnostics": trace.sentence_boundary_diagnostics(text),
                      "pass": actual == expected,
                      "slice_roundtrip": [text[a:b] for a, b in spans] == actual,
                      "nonblank_conservation": "".join(text.split()) == "".join("".join(actual).split())})

    for name, first in [
        ("parenthesis_then_period", "(Dato. [C-001])."),
        ("bold_then_period", "**Dato. [C-001]**."),
        ("nested_wrappers_then_period", "(«**Dato. [C-001]**»)."),
        ("curly_single_quotes", "‘Dato. [C-001]’"),
        ("nested_curly_single_quotes", "(‘Dato. [C-001]’)"),
        ("multiple_closure_groups", "(Dato. [C-001]) [S01 §Resultados]."),
        ("relative_link", "Dato. [C-001](../article.pdf#resultados)"),
        ("url_balanced_parentheses", "Dato. [C-001](https://example.org/a_(b_(c)))"),
        ("url_escaped_parenthesis", "Dato. [C-001](https://example.org/a\\)b)"),
        ("title_balanced_parentheses", 'Dato. [C-001](https://example.org "Figura (a). Texto")'),
        ("title_unbalanced_open_parenthesis", 'Dato. [C-001](https://example.org "Figura (a")'),
        ("title_unbalanced_close_parenthesis", 'Dato. [C-001](https://example.org "Figura a)")'),
        ("angle_destination_unbalanced_parenthesis", "Dato. [C-001](<https://example.org/a(b>)"),
        ("quoted_title_single", "Dato. [C-001](https://example.org 'Título (dato')"),
        ("adjacent_link_citations", "Dato.[C-001](https://example.org)[S01](https://example.org/2)"),
        ("italic_diacritic_context", "Ámbito _D. discoideum_. [C-001]"),
    ]:
        exact(name, first, "Otro dato. [C-002]")

    # Diagnóstico ambiguo permitido; no adjudicar su lectura final por heurística.
    for name, text in [
        ("complex_italic_taxon", "Hubo _B. cf. floridanus_ [C-001]."),
        ("bold_taxon", "Hubo **B. floridanus**. [C-001]"),
        ("abbreviation_numeric_following", "Se analizaron spp. 12 casos se midieron. [C-001]"),
        ("abbreviation_quoted_following", "Se analizaron spp. «Otra proposición». [C-001]"),
        ("abbreviation_unregistered_lowercase", "Se analizaron spp. otra proposición. [C-001]"),
    ]:
        diagnostics = trace.sentence_boundary_diagnostics(text)
        result = initial.fixture_main(text)
        tests.append({"case": name, "text": text, "expected": "DIAGNOSTICAR_Y_BLOQUEAR",
                      "diagnostics": diagnostics, "main": result,
                      "pass": bool(diagnostics) and result["main_write_exit"] != 0 and not result["output_written"]})

    pipelines = []
    for name, text in [
        ("prose_masked_as_link", "Se observó. [C-001](La proteína actúa. Otra cambia.)"),
        ("prose_after_uri_masked_as_title", "Se observó. [C-001](https://example.org La proteína actúa. Otra cambia.)"),
        ("empty_angle_and_bare_prose", "Se observó. [C-001](<> La proteína actúa. Otra cambia.)"),
        ("nominal_link_missing_outer_close", "Se observó. [C-001](https://example.org"),
        ("nominal_group_missing_close", "Se observó. [C-001; S01 fig. 2"),
    ]:
        result = initial.fixture_main(text)
        pipelines.append({"case": name, "text": text, "expected": "RECHAZAR_SIN_ESCRIBIR",
                          "pass": result["main_write_exit"] != 0 and not result["output_written"], **result})
    for name, text in [
        ("valid_link_with_open_parenthesis_title", 'Dato. [C-001](https://example.org "Figura (a") Otro. [C-002]'),
        ("valid_link_with_close_parenthesis_title", 'Dato. [C-001](https://example.org "Figura a)") Otro. [C-002]'),
        ("valid_angle_destination", "Dato. [C-001](<https://example.org/a(b>) Otro. [C-002]"),
    ]:
        result = initial.fixture_main(text)
        pipelines.append({"case": name, "text": text, "expected": "ACEPTAR_DOS_SEGMENTOS_CON_C_PROPIA",
                          "pass": result["main_write_exit"] == result["main_check_exit"] == 0
                              and len(result["segments"]) == 2
                              and all(x["claims"] for x in result["segments"])
                              and result["output_unchanged_second_run"], **result})

    hashes_after = {str(p.relative_to(ROOT)): sha(p) for p in paths}
    return {"revisor": "/root/inspeccion_relojes",
            "independencia": "Sin participación en la implementación revisada.",
            "inicio_utc": start, "fin_utc": now(), "hashes_before": hashes_before, "hashes_after": hashes_after,
            "inputs_stable": hashes_before == hashes_after, "initial_suite_reexecuted": rerun,
            "additional_tests": tests, "additional_pipelines": pipelines,
            "counts": {"checks": len(tests), "pass": sum(x["pass"] for x in tests),
                       "fail": sum(not x["pass"] for x in tests), "pipelines": len(pipelines),
                       "pipeline_pass": sum(x["pass"] for x in pipelines),
                       "pipeline_fail": sum(not x["pass"] for x in pipelines)},
            "markdown_normative_reference": {"url": "https://spec.commonmark.org/0.31.2/#links",
                "section": "6.3 Links; link destination/link title",
                "scope": "Gramática de destinos y títulos, no evidencia científica ni exigencia de implementar todo CommonMark."},
            "limites": "No modifica producción; la NC inicial se conserva; no adjudica densidad, fuentes ni corpus científico."}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
