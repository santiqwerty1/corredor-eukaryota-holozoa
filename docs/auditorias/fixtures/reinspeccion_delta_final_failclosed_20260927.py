"""Adversarios independientes adicionales de la reparación 1bba155d.

Solo archivos temporales. No modifica producción, corpus ni firmas reales.
"""
import contextlib
import io
import json
import runpy
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

with contextlib.redirect_stdout(io.StringIO()) as captured:
    previous = runpy.run_path(str(Path(__file__).with_name("reinspeccion_failclosed_independiente_20260927.py")))
previous_results = json.loads(captured.getvalue())
b, source_fixture, write, csvwrite, digest = (previous[n] for n in ("b", "source_fixture", "write", "csvwrite", "digest"))
ROOT = previous["ROOT"]
RESULTS = []


def insist(value, detail):
    if not value:
        raise AssertionError(detail)


def record(name, function):
    try:
        RESULTS.append({"case": name, "result": "PASS", "detail": function()})
    except Exception as exc:
        RESULTS.append({"case": name, "result": "FAIL", "detail": f"{type(exc).__name__}: {exc}"})


def late_source(mode, negative=False):
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        source, frozen, removed = source_fixture(root)
        catalogue = root / "data/apendices/A_fuentes.csv"
        old_hash = digest(catalogue)
        calls = 0
        load = b.load_sources
        hash_file = b.sha256_file
        if mode == "duplicate":
            csvwrite(root, catalogue.relative_to(root), list(source), [source, source])
        def load_then_mutate(repository):
            nonlocal calls
            result = load(repository)
            calls += 1
            if calls == 2:
                if mode == "title":
                    csvwrite(root, catalogue.relative_to(root), list(source), [{**source, "título": "Identidad cambiada tras segunda lectura"}])
                elif mode == "bytes_only":
                    catalogue.write_bytes(catalogue.read_bytes().replace(b"\n", b"\r\n"))
                    insist(load(root) == result, "El adversario alteró las celdas en vez de solo bytes")
                elif mode == "absent":
                    catalogue.unlink()
            return result
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(b, "load_sources", side_effect=load_then_mutate))
            if negative:
                stack.enter_context(patch.object(b, "sha256_file", side_effect=lambda p: old_hash if p == catalogue else hash_file(p)))
            try:
                out = next(r for r in b.build_source_matrix(frozen, root, [], removed) if r["clave_final"] == "S01")
            except b.BuildError as exc:
                insist(not negative, "Control negativo no aisló el rehash: " + str(exc))
                return "Rechazo: " + str(exc)
        if negative:
            insist(out["estado_hallazgo"] == "CERRADO", "Control negativo no ejercita el rehash")
            return "Solo en memoria: fijar la SHA de A permite reproducir el cierre obsoleto."
        raise AssertionError("Aceptó " + mode + ": " + out["estado_hallazgo"])


def global_invalid_pair(result, state):
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        trace = csvwrite(root, "trace.csv", ["tipo", "id_segmento"], [])
        reqs = [{"id_requisito": f"R-{n:04d}"} for n in range(1, 484)]
        row = b.build_second_review([], [], reqs, trace, None, root=root)[0]
        row.update({"resultado": result, "estado_cierre": state})
        path = csvwrite(root, "global.csv", b.SECOND_REVIEW_COLUMNS, [row])
        try:
            b.build_second_review([], [], reqs, trace, path, root=root)
        except b.BuildError as exc:
            return "Rechazo: " + str(exc)
        raise AssertionError("Par incompatible importado")


def direct_report(result):
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        row = b.pending_review_row("REQUISITO", "R-0001", b.REQUIREMENT_REVIEW_TYPE, "CENSO_100_PCT", "a" * 64)
        row.update({"resultado": result, "estado_cierre": "CERRADO"})
        after = dict.fromkeys(("claims", "sources", "entities", "events", "dates", "hypotheses", "magnitudes", "negative_active", "tables"), 0)
        report = b.report_markdown([], [], [], [], [row], after, {k: {} for k in "BCDEFG"}).decode()
        insist("EN CURSO" in report and "CERRADA: la segunda revisión" not in report, "Markdown promueve firma inválida")
        for name in ("data/table_lineage.csv", "docs/auditorias/mapa_claves_inicial_final_2026-08-08.csv", "docs/auditorias/matriz_trazabilidad_contenido_2026-08-08.csv"):
            write(root, name, "Fixture artificial.\n")
        removed = write(root, "removed.csv", "Fixture artificial.\n")
        data = json.loads(b.build_reproducible_json(root, root / "inputs", {}, after, [row], [], removed, unclosed_objects=0))
        insist(data["verdict"] == "REVISION_INDEPENDIENTE_PENDIENTE", "JSON promueve firma inválida")
        return "Markdown y JSON quedan pendientes incluso con estado_cierre=CERRADO."


for mode in ("title", "bytes_only", "absent", "duplicate"):
    record("source_final_" + mode, lambda mode=mode: late_source(mode))
record("source_final_negative_control", lambda: late_source("title", True))
for result, state in (("PENDIENTE", "CERRADO"), ("NO_CONFORME", "CERRADO"), ("CONFORME", "ABIERTO"), ("FALLO_CORREGIDO", "ABIERTO")):
    record("global_pair_" + result + "_" + state, lambda result=result, state=state: global_invalid_pair(result, state))
for result in ("PENDIENTE", "NO_CONFORME", "CONFORME"):
    record("direct_outputs_" + result, lambda result=result: direct_report(result))
print(json.dumps({
    "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "hashes": {**previous_results["hashes"], str(Path(__file__).relative_to(ROOT)): digest(Path(__file__))},
    "previous": previous_results,
    "final_delta": {"tests": len(RESULTS), "passed": sum(r["result"] == "PASS" for r in RESULTS), "results": RESULTS},
}, ensure_ascii=False, indent=2))
