"""Ampliación independiente: solo directorios temporales y firmas artificiales.

Ejecutar desde el repositorio. Reutiliza únicamente nuestra fixture independiente
anterior, no las fixtures del autor de la implementación. Emite cada resultado;
un exitcode cero no implica que hayan pasado todos los adversarios.
"""
import contextlib
import hashlib
import io
import json
import runpy
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
with contextlib.redirect_stdout(io.StringIO()) as original_output:
    prior = runpy.run_path(str(Path(__file__).with_name("revision_failclosed_independiente_20260926.py")))
original = json.loads(original_output.getvalue())
b = prior["b"]
write, csvwrite, nominal, nominalwrite, fixture, digest, j = (
    prior[name] for name in ("write", "csvwrite", "nominal", "nominalwrite", "fixture", "digest", "j")
)
RESULTS = []


def record(name, fn):
    try:
        detail = fn()
        RESULTS.append({"case": name, "result": "PASS", "detail": detail})
    except Exception as exc:
        RESULTS.append({"case": name, "result": "FAIL", "detail": f"{type(exc).__name__}: {exc}"})


def insist(value, detail):
    if not value:
        raise AssertionError(detail)


def source_fixture(root):
    source = {
        "clave": "S01", "autores": "Autor artificial", "año": "2026",
        "título": "Publicación artificial para infraestructura",
        "publicación o repositorio": "Revista artificial", "tipo": "primaria",
        "DOI en forma https://doi.org/10.xxxx/... o URL resoluble si no hay DOI": "https://example.org/artificial",
        "notas de calidad": "Texto que no concede ninguna aprobación.",
    }
    csvwrite(root, "data/apendices/A_fuentes.csv", list(source), [source])
    frozen = [{
        "clave_inicial": f"S{n:02d}", "metadata": "Histórica artificial",
        "identidad_bibliografica": "Histórica artificial", "tipo": "primaria",
        "estado_editorial": "Histórico artificial", "acceso": "NO VERIFICABLE",
        "doi_url": "https://example.org/artificial", "uso": "Histórico artificial", "soporte_unico": "NO",
        "veredicto": "CONFORME", "severidad": "NINGUNA", "accion": "Conservar",
        "evidencia_auditoria": "Artificial", "fecha_verificacion": "2026-08-08",
        "huella_corpus_inicial_sha256": b.source_fingerprint(source) if n == 1 else "a" * 64,
    } for n in range(1, 526)]
    removed = csvwrite(root, "removed.csv", ["clave", "motivo", "destino_documental"], [
        {"clave": r["clave_inicial"], "motivo": "Retirada artificial", "destino_documental": "Historia artificial"}
        for r in frozen[1:]
    ])
    nominalwrite(root, [nominal(root, key="S01", sha=b.source_fingerprint(source), axis=a) for a in b.SOURCE_REVIEW_AXES])
    return source, frozen, removed


def prepare_mutation(root, mode):
    rows = b.read_dicts(root / b.NOMINAL_REVIEWS)[1]
    if mode == "artifact_only":
        extra = write(root, "docs/extra.txt", "Artefacto adicional nominal original.")
        for row in rows:
            artifacts = json.loads(row["artefactos_inspeccionados"])
            artifacts["docs/extra.txt"] = digest(extra)
            row["artefactos_inspeccionados"] = j(artifacts)
        nominalwrite(root, rows)
    elif mode == "symlink_target":
        target = write(root, "docs/destino.txt", "Prueba por enlace original.")
        (root / "docs/enlace.txt").symlink_to(target)
        for row in rows:
            row["evidencia_local"] = "docs/enlace.txt"
            row["huella_evidencia_sha256"] = digest(target)
        nominalwrite(root, rows)

    def mutate():
        if mode == "proof_content":
            write(root, "docs/prueba.txt", "Documento nominal cambiado antes del retorno.")
        elif mode == "proof_absent":
            (root / "docs/prueba.txt").unlink()
        elif mode == "registry_changed":
            rows[0]["dictamen"] += " Nueva adjudicación artificial."
            nominalwrite(root, rows)
        elif mode == "registry_absent":
            (root / b.NOMINAL_REVIEWS).unlink()
        elif mode == "artifact_only":
            write(root, "docs/extra.txt", "Artefacto adicional cambiado antes del retorno.")
        elif mode == "symlink_target":
            write(root, "docs/destino.txt", "Destino cambiado antes del retorno.")
        else:
            raise AssertionError(mode)
    return mutate


def nominal_race(stratum, mode, disable_guard=False):
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        if stratum == "C":
            claim, _, _, _ = fixture(root)
            mutate = prepare_mutation(root, mode)
            load = b.load_claims
            def load_then_change(repository):
                answer = load(repository)
                mutate()
                return answer
            function = lambda: b.claim_closure(b.final_claim_axes([claim], b.load_claim_review_evidence(root)))
            hook = "load_claims"
        else:
            _, frozen, removed = source_fixture(root)
            mutate = prepare_mutation(root, mode)
            load = b.load_sources
            def load_then_change(repository):
                answer = load(repository)
                mutate()
                return answer
            function = lambda: next(r for r in b.build_source_matrix(frozen, root, [], removed) if r["clave_final"] == "S01")["estado_hallazgo"]
            hook = "load_sources"
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(b, hook, side_effect=load_then_change))
            if disable_guard:
                stack.enter_context(patch.object(b, "assert_nominal_reviews_current", return_value=None))
            try:
                result = function()
            except b.BuildError as exc:
                insist(not disable_guard, "El control negativo no aisló la nueva comprobación: " + str(exc))
                return "Rechazo por BuildError: " + str(exc)
        if disable_guard:
            insist(result == "CERRADO", "Control negativo no ejercita el guard añadido: " + result)
            return "Control negativo SOLO en memoria: sin el guard se reproduce CERRADO."
        insist(result != "CERRADO", "La mutación nominal anterior al retorno produjo CERRADO")
        return "Queda abierto."


def source_live_change():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        source, frozen, removed = source_fixture(root)
        baseline = b.build_source_matrix(frozen, root, [], removed)
        insist(next(r for r in baseline if r["clave_final"] == "S01")["estado_hallazgo"] == "CERRADO", "Fixture inicial no cerrada")
        load = b.load_sources
        changed = {**source, "título": "Otra identidad artificial, no revisada"}
        def load_then_change(repository):
            answer = load(repository)
            csvwrite(root, "data/apendices/A_fuentes.csv", list(changed), [changed])
            return answer
        with patch.object(b, "load_sources", side_effect=load_then_change):
            try:
                out = next(r for r in b.build_source_matrix(frozen, root, [], removed) if r["clave_final"] == "S01")
            except b.BuildError as exc:
                return "Cambio de A detectado: " + str(exc)
        live = load(root)[0]
        insist(out["estado_hallazgo"] != "CERRADO" or out["huella_final_sha256"] == b.source_fingerprint(live),
               "S01 devuelta CERRADO con SHA anterior=" + out["huella_final_sha256"] + "; A viva=" + b.source_fingerprint(live))
        return "No devuelve un cierre de la identidad obsoleta."


def pending_closed_all_requirements():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        reqs = [{"id_requisito": f"R-{n:04d}"} for n in range(1, 484)]
        trace = csvwrite(root, "trace.csv", ["tipo", "id_segmento"], [])
        generated = b.build_second_review([], [], reqs, trace, None, root=root)
        signatures = [{**r, "estado_cierre": "CERRADO"} for r in generated]
        path = csvwrite(root, "global.csv", b.SECOND_REVIEW_COLUMNS, signatures)
        try:
            out = b.build_second_review([], [], reqs, trace, path, root=root)
        except b.BuildError as exc:
            return "Entradas incoherentes rechazadas: " + str(exc)
        unexpected = sum(r["resultado"] == "PENDIENTE" and r["estado_cierre"] == "CERRADO" for r in out)
        after = dict.fromkeys(("claims", "sources", "entities", "events", "dates", "hypotheses", "magnitudes", "negative_active", "tables"), 0)
        report = b.report_markdown([], [], [], [], out, after, {k: {} for k in "BCDEFG"}).decode()
        insist(unexpected == 0 and "CERRADA: la segunda revisión" not in report,
               f"{unexpected}/483 revisiones PENDIENTE/CERRADO; informe declara CERRADA=" + str("CERRADA: la segunda revisión" in report))
        return "Ninguna fila pendiente puede cerrar el informe."


def global_nominal_bound(stratum, date, expected):
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        if stratum == "C":
            claim, _, _, _ = fixture(root)
            rows = b.read_dicts(root / b.NOMINAL_REVIEWS)[1]
            rows[-1]["fecha_revision_utc"] = "2026-09-26T15:00:00Z"
            nominalwrite(root, rows)
            ev = b.load_claim_review_evidence(root)
            dossier = {"clave_inicial": "C-001", "estado_inicial": "CORREGIR", "severidad_inicial": "P0",
                       "huella_final_sha256": b.claim_fingerprint(claim), "estado_hallazgo": "CERRADO", "evidencia_final": ev.evidence([claim])}
            cs, ss = [dossier], []
        else:
            _, frozen, removed = source_fixture(root)
            rows = b.read_dicts(root / b.NOMINAL_REVIEWS)[1]
            rows[-1]["fecha_revision_utc"] = "2026-09-26T15:00:00Z"
            nominalwrite(root, rows)
            dossier = next(r for r in b.build_source_matrix(frozen, root, [], removed) if r["clave_final"] == "S01")
            dossier.update({"severidad_inicial": "P0", "veredicto_inicial": "CORREGIR"})
            cs, ss = [], [dossier]
        reqs = [{"id_requisito": f"R-{n:04d}"} for n in range(1, 484)]
        trace = csvwrite(root, "trace.csv", ["tipo", "id_segmento"], [])
        row = b.build_second_review(cs, ss, reqs, trace, None, root=root)[0]
        row.update({"resultado": "CONFORME", "estado_cierre": "CERRADO", "fecha": date,
                    "revisor_independiente": "Global artificial", "declaracion_independencia": "INDEPENDIENTE_DEL_AUTOR_DE_LA_CORRECCION",
                    "evidencia": "Prueba artificial expediente_sha256=" + b.row_fingerprint(dossier), "accion": "Sin cambio artificial"})
        path = csvwrite(root, "global.csv", b.SECOND_REVIEW_COLUMNS, [row])
        out = b.build_second_review(cs, ss, reqs, trace, path, root=root)[0]
        insist(out["resultado"] == expected, str(out))
        return "Máximo nominal 15:00Z; fecha global=" + date + "; resultado=" + out["resultado"]


for stratum in ("C", "S"):
    for mode in ("proof_content", "proof_absent", "registry_changed", "registry_absent", "artifact_only", "symlink_target"):
        record(f"nominal_{stratum}_{mode}", lambda stratum=stratum, mode=mode: nominal_race(stratum, mode))
    record(f"negative_control_{stratum}", lambda stratum=stratum: nominal_race(stratum, "proof_content", True))
    for date, expected in (("2026-09-26T14:59:59Z", "PENDIENTE"), ("2026-09-26T15:00:00Z", "CONFORME"), ("2026-09-26", "PENDIENTE")):
        record(f"global_bound_{stratum}_{date}", lambda stratum=stratum, date=date, expected=expected: global_nominal_bound(stratum, date, expected))
record("source_canonical_changed_before_return", source_live_change)
record("all_pending_closed_cannot_close_report", pending_closed_all_requirements)
files = ("scripts/build_audit_deliverables.py", "scripts/audit_chronology.py", "tests/test_build_audit_closure.py",
         "docs/auditorias/fixtures/revision_failclosed_independiente_20260926.py", str(Path(__file__).relative_to(ROOT)))
print(json.dumps({
    "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "scope": "Reinspección técnica independiente; solo fixtures temporales, sin aprobación científica ni global.",
    "hashes": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in files},
    "original": original,
    "extension": {"tests": len(RESULTS), "passed": sum(r["result"] == "PASS" for r in RESULTS), "results": RESULTS},
}, ensure_ascii=False, indent=2))
