"""Reinspección R4: sustitución de URL, cierres anidados y C no prestadas."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIOR = ROOT / "docs/auditorias/fixtures/reinspeccion_independiente_segmentacion_ncden02_r3_20260927.py"
spec = importlib.util.spec_from_file_location("review_prior_r3", PRIOR)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
trace = prior.trace


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def cases():
    result = []
    urls = ["https://example.org/a_(b)/v1.2?q=O'Reilly&v=4.5#sec-2.3",
            "https://example.org/a_*_", "https://example.org/%27?q=a%2Eb",
            "https://example.org/#fig.2"]
    for index, url in enumerate(urls):
        for ending, opening, closing in [("?!", "[‘", "’]"), ("…", "(**", "**)"),
                                         (".", "‹_", "_›")]:
            first = opening + "El resultado de _S. rosetta_ consta en " + url + ending + closing
            citation = " [C-001](<../fuente con espacio.pdf#p.2>) [S01 p. 2]"
            second = "3.5 células respondieron. [C-002]"
            result.append((f"url_substitution_{index}_{ord(ending[0])}", first + citation, second))
    result.extend([
        ("multiple_citations_closers", "([‘La evidencia consta en https://example.org/.’]) [C-001] [S01 Fig. 2].", "otro resultado. [C-002]"),
        ("angle_url_with_trailing_literal_dot", "La evidencia consta en <https://example.org/a.>. [C-001]", "Otro. [C-002]"),
        ("two_bare_urls_one_sentence", "Se contrastaron https://example.org/a.2 y https://example.net/b.3. [C-001]", "Otro. [C-002]"),
        ("url_encoded_terminators", "Consta en https://example.org/a%2Eb%21%3F. [C-001]", "Otro. [C-002]"),
        ("single_quote_inside_url", "Consta en https://example.org/O'Reilly_v2.1/result. [C-001]", "Otro. [C-002]"),
        ("unicode_apostrophe_inside_url", "Consta en https://example.org/O’Neill_v2.1/result. [C-001]", "Otro. [C-002]"),
        ("escaped_title_in_link", r'Dato. [C-001](url "Figura \"a\". Dato")', "Otro. [C-002]"),
        ("nobracket_marker_not_postposed_citation", "Dato. [C-001]", "[SIN FUENTE] Otra proposición. [C-002]"),
    ])
    return result


def digest_only():
    items = []
    for name, first, second in cases():
        text = first + "\u00a0\t" + second
        items.append({"case": name, "spans": trace.sentence_spans(text),
                      "diagnostics": trace.sentence_boundary_diagnostics(text)})
    return sha(json.dumps(items, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode())


def run():
    start = utc()
    before = prior.input_hashes()
    before[str(Path(__file__).relative_to(ROOT))] = sha(Path(__file__).read_bytes())
    historical = prior.run()
    r2 = historical["historical_suites_reexecuted"]
    initial = r2["initial_suite_reexecuted"]
    summary = {"sha256_complete_rerun_canonical_json": sha((json.dumps(historical, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode()),
               "initial": initial["counts"], "r2": r2["counts"], "r3": historical["counts"],
               "failures": [item for collection in (initial["tests"], initial["pipelines"], r2["additional_tests"],
                   r2["additional_pipelines"], historical["additional_checks"], historical["additional_pipelines"])
                   for item in collection if not item["pass"]]}
    tests, pipelines = [], []
    for name, first, second in cases():
        text = first + "\u00a0\t" + second
        spans = trace.sentence_spans(text)
        actual = trace.split_sentences(text)
        tests.append({"case": name, "text": text, "expected": [first, second], "actual": actual,
                      "spans": spans, "diagnostics": trace.sentence_boundary_diagnostics(text),
                      "pass": actual == [first, second],
                      "slice_roundtrip": [text[a:b] for a,b in spans] == actual,
                      "nonblank_conservation": "".join(text.split()) == "".join("".join(actual).split())})
        # Cada caso se ejecuta con ambas C y con una C retirada de cada lado.
        for variant in ("both", "first_missing", "second_missing"):
            selected_first = first.replace("C-001", "S01") if variant == "first_missing" else first
            selected_second = second.replace("C-002", "S02") if variant == "second_missing" else second
            actual_text = selected_first + " " + selected_second
            result = prior.prior.initial.fixture_main(actual_text)
            expected_accept = variant == "both"
            passed = (result["main_write_exit"] == result["main_check_exit"] == 0
                      and len(result["segments"]) == 2
                      and all(s["claims"] for s in result["segments"])) if expected_accept else (
                          result["main_write_exit"] != 0 and not result["output_written"])
            pipelines.append({"case": name + "_" + variant, "text": actual_text,
                              "expected_accept": expected_accept, "pass": passed, **result})
    seeds = []
    for seed in ("2", "29", "977"):
        process = subprocess.run([sys.executable, str(Path(__file__)), "--digest"], cwd=ROOT,
            env=dict(os.environ, PYTHONHASHSEED=seed), capture_output=True, text=True, check=False)
        seeds.append({"seed": seed, "exit": process.returncode, "stdout": process.stdout.strip(), "stderr": process.stderr})
    after = prior.input_hashes()
    after[str(Path(__file__).relative_to(ROOT))] = sha(Path(__file__).read_bytes())
    return {"reviewer": "/root/inspeccion_relojes", "author": "/root/verificacion_fuentes_nuevas",
            "independence": "El revisor no escribió el segmentador ni sus reparaciones.",
            "start_utc": start, "end_utc": utc(), "hashes_before": before, "hashes_after": after,
            "inputs_stable": before == after, "historical_rerun": summary,
            "additional_tests": tests, "additional_pipelines": pipelines,
            "counts": {"checks": len(tests), "pass": sum(t["pass"] for t in tests),
                       "fail": sum(not t["pass"] for t in tests), "pipelines": len(pipelines),
                       "pipeline_pass": sum(t["pass"] for t in pipelines),
                       "pipeline_fail": sum(not t["pass"] for t in pipelines)},
            "seed_runs": seeds, "seeds_identical": all(x["exit"] == 0 for x in seeds)
                and len({x["stdout"] for x in seeds}) == 1,
            "census_in_memory": historical["census_in_memory"],
            "scope": "Sólo NC-DEN02 técnico; no adjudicación de las192fronteras ni42unidades sinC, NC-DEN01, ciencia o cierre global."}


if __name__ == "__main__":
    print(digest_only() if "--digest" in sys.argv else json.dumps(run(), ensure_ascii=False, indent=2))
