"""Adversarios propios de NC-DEN02. Sólo fixtures temporales; no canon."""
from __future__ import annotations

import contextlib
import csv
import hashlib
import io
import json
import re
import sys
import tempfile
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from scripts import build_content_trace as trace

REVIEWER = "/root/inspeccion_relojes"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def fixture_main(text):
    """Ejecuta main real dos veces; parchea sólo rutas y argv, no validadores."""
    with tempfile.TemporaryDirectory(prefix="review-ncden02-") as temporary:
        root = Path(temporary)
        source = root / "docs/secciones/003-02-fixture.md"
        source.parent.mkdir(parents=True)
        source.write_text(text + "\n", encoding="utf-8")
        claimfile = root / "data/afirmaciones/03.csv"
        claimfile.parent.mkdir(parents=True)
        with claimfile.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["#", "Afirmación", "Sujeto", "Predicado", "Objeto", "Fuente", "Motivo", "Resolución"])
            for key in ("C-001", "C-002", "C-003"):
                writer.writerow([key, "Resultado ficticio registrado", "fixture", "posee_rasgo", "resultado", "S01 p. 1", "Fixture, no ciencia", "resuelta"])
        (root / "data/table_index.json").write_text('{"tables": []}\n', encoding="utf-8")
        manifest = root / "data/auditoria/mapeo_celdas_afirmaciones.csv"
        manifest.parent.mkdir(parents=True)
        with manifest.open("w", encoding="utf-8", newline="") as handle:
            csv.writer(handle).writerow(trace.CELL_MANIFEST_HEADER)
        output = root / "docs/auditorias/traza.csv"
        before = {p.relative_to(root).as_posix(): digest(p.read_bytes()) for p in root.rglob("*") if p.is_file()}
        with patch.object(trace, "ROOT", root), patch.object(trace, "CELL_MANIFEST", manifest), patch.object(trace, "OUTPUT", output):
            segments = trace.narrative_segments()
            payload_errors = trace.validate_payload(trace.csv_bytes(segments))
            ambiguities = trace.narrative_ambiguities()
            stdout, stderr = io.StringIO(), io.StringIO()
            with patch.object(sys, "argv", ["build_content_trace.py"]), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                first = trace.main()
            first_bytes = output.read_bytes() if output.exists() else None
            with patch.object(sys, "argv", ["build_content_trace.py", "--check"]), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                second = trace.main()
            last_bytes = output.read_bytes() if output.exists() else None
        after = {p.relative_to(root).as_posix(): digest(p.read_bytes()) for p in root.rglob("*") if p.is_file() and p != output}
        return {
            "main_write_exit": first, "main_check_exit": second,
            "output_written": first_bytes is not None,
            "output_sha256": digest(first_bytes) if first_bytes is not None else None,
            "output_unchanged_second_run": first_bytes == last_bytes,
            "inputs_unchanged": before == after,
            "segments": [asdict(s) for s in segments],
            "payload_errors": payload_errors, "ambiguities": ambiguities,
            "stdout": stdout.getvalue(), "stderr": stderr.getvalue(),
        }


def run():
    started = utc()
    paths = [
        "scripts/build_content_trace.py",
        "tests/test_content_trace_sentence_boundaries.py",
        "docs/auditorias/ENTREGA_AUTORAL_SEGMENTACION_NCDEN02_2026-09-27.md",
        "docs/auditorias/PROPUESTA_CONTRATO_CENSO_ORACIONES_DENSIDAD_2026-09-27.md",
        str(Path(__file__).relative_to(ROOT)),
        str(trace.OUTPUT.relative_to(ROOT)),
    ]
    before = {p: digest((ROOT / p).read_bytes()) for p in paths}
    results = []

    def exact(name, text, expected, category):
        spans = trace.sentence_spans(text)
        actual = trace.split_sentences(text)
        results.append({"case": name, "category": category, "text": text, "expected": expected,
            "actual": actual, "spans": spans, "diagnostics": trace.sentence_boundary_diagnostics(text),
            "pass": actual == expected, "text_sha256_lf": digest((text + "\n").encode())})
        invariant = (
            [text[a:b] for a, b in spans] == actual
            and all(0 <= a < b <= len(text) for a, b in spans)
            and all(a[1] <= b[0] for a, b in zip(spans, spans[1:]))
            and "".join(text.split()) == "".join("".join(actual).split())
        )
        results.append({"case": name + "_exact_span_invariants", "category": "spans",
                        "pass": invariant, "spans": spans})

    exact("postposed_two", "Dato. [C-001; S01 §Resultados] Otro dato. [C-002]",
          ["Dato. [C-001; S01 §Resultados]", "Otro dato. [C-002]"], "baseline")
    exact("postposed_multiple", "Dato.[C-001][S01 p. 2] [BN-001] otro dato.",
          ["Dato.[C-001][S01 p. 2] [BN-001]", "otro dato."], "baseline")
    exact("nested_locator", "Dato. [C-001; S01 Fig. 2 [a.], p. 3] Otro.",
          ["Dato. [C-001; S01 Fig. 2 [a.], p. 3]", "Otro."], "baseline")
    exact("sin_fuente_prefix", "Dato. [C-001] [SIN FUENTE] Otro dato.",
          ["Dato. [C-001]", "[SIN FUENTE] Otro dato."], "baseline")
    exact("noncitation_bracket", "Dato. [La otra proposición usa C-002]",
          ["Dato.", "[La otra proposición usa C-002]"], "baseline")
    exact("unicode_whitespace_offsets", "  Ácido α. [C-001]\r\n\t🧬 β. [C-002]  ",
          ["Ácido α. [C-001]", "🧬 β. [C-002]"], "unicode")
    exact("decomposed_accent", "A\u0301mbito. [C-001]\u00a0Otra oración.",
          ["A\u0301mbito. [C-001]", "Otra oración."], "unicode")
    exact("decimal_exponent", "El valor fue 3.14e-5. [C-001] Otro.",
          ["El valor fue 3.14e-5. [C-001]", "Otro."], "numbers")
    exact("decimal_span_range", "Se transcribe 10.89–13.61. [C-001] Otro.",
          ["Se transcribe 10.89–13.61. [C-001]", "Otro."], "numbers")
    exact("inline_abbreviations", "Smith et al. vieron Bacillus sp. y varias spp. [C-001] Otro.",
          ["Smith et al. vieron Bacillus sp. y varias spp. [C-001]", "Otro."], "abbreviations")
    exact("italic_taxon", "Hubo cambios en *B. floridanus*. [C-001] Otro.",
          ["Hubo cambios en *B. floridanus*. [C-001]", "Otro."], "taxon")
    exact("url_internal", "Consulte https://example.org/a!b?x=3.14. [C-001] Otro.",
          ["Consulte https://example.org/a!b?x=3.14. [C-001]", "Otro."], "url")
    exact("url_autolink", "Consulte <https://example.org/a>. [C-001] Otro.",
          ["Consulte <https://example.org/a>. [C-001]", "Otro."], "url")
    exact("markdown_link", "Consulte [fuente](https://example.org/a). [C-001] Otro.",
          ["Consulte [fuente](https://example.org/a). [C-001]", "Otro."], "url")
    exact("closing_before_citation", "«Dato.» [C-001] Otro.",
          ["«Dato.» [C-001]", "Otro."], "quote")
    exact("punctuation_cluster", "¿Dato?! [C-001] ¡Otro! [C-002] Fin.",
          ["¿Dato?! [C-001]", "¡Otro! [C-002]", "Fin."], "punctuation")
    exact("ascii_ellipsis", "Dato... [C-001] Otro.",
          ["Dato... [C-001]", "Otro."], "punctuation")

    wrappers = [
        ("parenthesis_after_citation", "(", ")"),
        ("guillemet_after_citation", "«", "»"),
        ("doublequote_after_citation", '"', '"'),
        ("curlyquote_after_citation", "“", "”"),
        ("singlequote_after_citation", "'", "'"),
        ("italic_after_citation", "*", "*"),
        ("bold_after_citation", "**", "**"),
        ("underscore_bold_after_citation", "__", "__"),
        ("nested_closings_after_citation", "(«", "»)"),
    ]
    failing_inputs = []
    for name, left, right in wrappers:
        first = left + "Se observó. [C-001]" + right
        text = first + " Otro resultado carece de C."
        exact(name, text, [first, "Otro resultado carece de C."], "postcitation_closers")
        failing_inputs.append((name, text))
    exact("linked_citation", "Dato. [C-001](https://example.org) Otro.",
          ["Dato. [C-001](https://example.org)", "Otro."], "postcitation_link")
    exact("unicode_ellipsis", "Dato… [C-001] Otro resultado carece de C.",
          ["Dato… [C-001]", "Otro resultado carece de C."], "unicode_punctuation")
    failing_inputs.append(("unicode_ellipsis", "Dato… [C-001] Otro resultado carece de C."))
    exact("adjacent_following_sentence", "Dato. [C-001]Otro resultado carece de C.",
          ["Dato. [C-001]", "Otro resultado carece de C."], "adjacency")
    exact("underscored_taxon", "Hubo cambios en _B. floridanus_. [C-001] Otro.",
          ["Hubo cambios en _B. floridanus_. [C-001]", "Otro."], "taxon")

    for name, text in [
        ("plain_initial", "Hubo cambios en B. floridanus. [C-001]"),
        ("plain_initial_chain", "B. floridanus y B. pennsylvanicus divergen. [C-001]"),
    ]:
        diags = trace.sentence_boundary_diagnostics(text)
        valid = bool(diags) and all(
            d["razon"] == "AMBIGUA_INICIAL_EPITETO"
            and d["lectura_corte"] != d["lectura_abreviatura"]
            and all(0 <= a < b <= len(text) for k in ["lectura_corte", "lectura_abreviatura"] for a, b in d[k])
            for d in diags
        )
        results.append({"case": name, "category": "ambiguity", "text": text,
                        "diagnostics": diags, "pass": valid})
    # Misma abreviatura legítima en función final: no exigir una elección,
    # sí conservar ambigüedad o exponer una unidad sin C en vez de aprobar fusión.
    ambiguous = "Se analizaron otras spp. El segundo resultado no está registrado. [C-001]"
    amb_splits = trace.split_sentences(ambiguous)
    amb_diag = trace.sentence_boundary_diagnostics(ambiguous)
    results.append({"case": "terminal_spp_not_autoapproved", "category": "ambiguity",
                    "text": ambiguous, "actual": amb_splits, "diagnostics": amb_diag,
                    "pass": bool(amb_diag) or any(not trace.claim_refs(x) for x in amb_splits)})

    pipelines = []
    for name, text in [
        ("normal_uncited_following", "Se observó. [C-001] Otro resultado carece de C."),
        ("plain_initial_pending", "Hubo cambios en B. floridanus. [C-001]"),
        *[(n, t) for n, t in failing_inputs if n in {"parenthesis_after_citation", "guillemet_after_citation", "bold_after_citation", "unicode_ellipsis"}],
        ("terminal_spp_not_autoapproved", ambiguous),
        ("unclosed_nominal_citation", "Se observó [C-001; S01 p. 1 sin cierre."),
    ]:
        data = fixture_main(text)
        expected_reject = data["main_write_exit"] != 0 and not data["output_written"]
        pipelines.append({"case": name, "text": text, "expected": "RECHAZAR_SIN_ESCRIBIR",
                          "pass": expected_reject, **data})
    positive = fixture_main("Se observó. [C-001] Otro resultado. [C-002]")
    pipelines.append({"case": "positive_two_explicit_claims", "expected": "DOS_SEGMENTOS_DETERMINISTAS",
                     "pass": positive["main_write_exit"] == positive["main_check_exit"] == 0
                         and len(positive["segments"]) == 2 and positive["output_unchanged_second_run"]
                         and positive["inputs_unchanged"], **positive})

    after = {p: digest((ROOT / p).read_bytes()) for p in paths}
    return {
        "reviewer": REVIEWER, "independence": "No participación en la implementación revisada; autoría científica S240/S352 excluida.",
        "started_utc": started, "finished_utc": utc(), "hashes_before": before, "hashes_after": after,
        "reviewed_files_stable": before == after, "tests": results, "pipelines": pipelines,
        "counts": {"checks": len(results), "pass": sum(x["pass"] for x in results),
                   "fail": sum(not x["pass"] for x in results),
                   "pipelines": len(pipelines), "pipeline_pass": sum(x["pass"] for x in pipelines),
                   "pipeline_fail": sum(not x["pass"] for x in pipelines)},
        "scope": "Segmentación y puerta técnica; no adjudicación científica de candidatos, NC-DEN01, censo C ni cierre global.",
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
