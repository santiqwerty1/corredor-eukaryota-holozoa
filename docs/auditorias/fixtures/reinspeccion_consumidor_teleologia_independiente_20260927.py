"""Adversarios independientes del consumidor; solo escribe fixtures temporales.

Las adjudicaciones sintéticas son datos de pruebas, nunca firmas del corpus.
Adaptación explícita del expediente ficticio a versión 2; la fixture y los
resultados originales se preservan. Añade adversarios de la ligadura reparada.
"""
import copy
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from scripts import audit_requirement_controls as controls
from scripts import check_teleology_contexts as consumer


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


class Fixture:
    def __init__(self, root):
        self.root = root
        self.path = root / "docs/secciones/015-14-14-nombres-y-nomenclatura.md"
        self.context = root / "docs/secciones/z-contexto.md"
        self.path.parent.mkdir(parents=True)
        self.path.write_text("El cuartil superior es numérico.\nEl término «primitivo» se critica.\n", encoding="utf-8")
        self.context.write_text("Contexto leído y preservado.\n", encoding="utf-8")
        self.paths = [self.path, self.context]
        self.review = root / consumer.REVIEW_PATH
        self.review.parent.mkdir(parents=True)
        self.document = {
            "version": 2,
            "alcance": "EXPEDIENTE FICTICIO: contrato técnico, no revisión real",
            "revisor": "REVISOR_FICTICIO_INDEPENDIENTE",
            "declaracion_independencia": "REVISION_INDEPENDIENTE_DE_CONTEXTOS_SIN_AUTORIA_DEL_TEXTO",
            "fecha_revision_utc": "2026-09-27T02:00:00Z",
            "fecha_snapshot_utc": "2026-09-27T02:00:01Z",
            "algoritmo_huella": "SHA256(UTF8(texto+LF))",
            "huellas_rutas": {p.relative_to(root).as_posix(): sha(p.read_bytes()) for p in self.paths},
            "candidatos": [],
        }
        for number, literal, verdict, motive in (
            (1, "superior", "USO_CUANTITATIVO", "Califica un cuartil, no un linaje."),
            (2, "primitivo", "CRITICA_TERMINOLOGICA", "Objeto literal de una crítica, no cualidad atribuida."),
        ):
            text = self.path.read_text().splitlines()[number - 1]
            start = text.index(literal)
            self.document["candidatos"].append({
                "ruta": self.path.relative_to(root).as_posix(), "linea": number,
                "localizador_logico": f"FIXTURE-L{number}", "texto": text,
                "sha256_texto": sha((text + "\n").encode()),
                "revisor": self.document["revisor"],
                "declaracion_independencia": self.document["declaracion_independencia"],
                "fecha_revision_utc": self.document["fecha_revision_utc"],
                "conflicto_autoria": "NO",
                "ocurrencias": [{"inicio": start, "fin": start + len(literal),
                    "literal": literal, "celda_o_clausula": text, "dictamen": verdict, "motivo": motive}],
            })

    def save(self):
        self.review.write_text(json.dumps(self.document, ensure_ascii=False), encoding="utf-8")

    def check(self):
        return consumer.check_context_reviews(self.root, self.paths)

    def corpus(self):
        return SimpleNamespace(root=self.root, section_paths=self.paths, claim_paths={},
            index={"tables": []}, appendix_paths={})


results = []


def record(name, expected, operation, diagnostic_v1=False):
    with TemporaryDirectory(prefix="teleologia-independiente-") as directory:
        fixture = Fixture(Path(directory))
        try:
            observation = operation(fixture)
            accepted = not observation[2]
            results.append({"id": name, "expediente_ficticio_sin_firma_real": True,
                "expected_accepted": expected, "accepted": accepted,
                "candidates": observation[0], "occurrences": observation[1], "errors": observation[2],
                "result": "PASS" if expected == accepted else "FAIL"})
        except Exception as exc:
            results.append({"id": name, "expected_accepted": expected,
                "exception": f"{type(exc).__name__}: {exc}", "result": "FAIL"})


def mutate(fixture, path, value):
    target = fixture.document
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    fixture.save()
    return fixture.check()


def baseline(fixture):
    fixture.save()
    return fixture.check()


record("schema_v2_current_must_accept", True, lambda f: mutate(f, ["version"], 2), False)
record("schema_v1_not_current_must_reject", False, lambda f: mutate(f, ["version"], 1), False)
record("baseline_v2", True, baseline)

for name, path, value in (
    ("top_extra", ["extra"], "inadmisible"),
    ("version_boolean", ["version"], True),
    ("version_string", ["version"], "1"),
    ("entries_mapping", ["candidatos"], {}),
    ("hashes_list", ["huellas_rutas"], []),
    ("scope_blank", ["alcance"], " "),
    ("reviewer_placeholder", ["revisor"], "TBD"),
    ("independence_blank", ["declaracion_independencia"], ""),
    ("utc_nozone", ["fecha_revision_utc"], "2026-09-27T02:00:00"),
    ("utc_badcalendar", ["fecha_revision_utc"], "2026-02-30T02:00:00Z"),
    ("utc_badseconds", ["fecha_revision_utc"], "2026-09-27T02:00:61Z"),
    ("utc_snapshot_earlier", ["fecha_snapshot_utc"], "2026-09-26T02:00:00Z"),
    ("utc_entry_later", ["candidatos", 0, "fecha_revision_utc"], "2026-09-28T02:00:00Z"),
    ("entry_extra", ["candidatos", 0, "extra"], 1),
    ("entry_path_traversal", ["candidatos", 0, "ruta"], "docs/../x.md"),
    ("entry_line_boolean", ["candidatos", 0, "linea"], True),
    ("entry_line_wrong", ["candidatos", 0, "linea"], 3),
    ("entry_text_stale", ["candidatos", 0, "texto"], "Otra línea"),
    ("entry_hash_stale", ["candidatos", 0, "sha256_texto"], "0" * 64),
    ("entry_locator_placeholder", ["candidatos", 0, "localizador_logico"], "sin revisar"),
    ("entry_reviewer_other", ["candidatos", 0, "revisor"], "OTRO"),
    ("entry_conflict_yes", ["candidatos", 0, "conflicto_autoria"], "SI"),
    ("entry_conflict_boolean", ["candidatos", 0, "conflicto_autoria"], False),
    ("entry_independence_missing", ["candidatos", 0, "declaracion_independencia"], "NO"),
    ("occurrence_missing", ["candidatos", 0, "ocurrencias"], []),
    ("occurrence_mapping", ["candidatos", 0, "ocurrencias"], {}),
    ("occurrence_extra", ["candidatos", 0, "ocurrencias", 0, "extra"], 1),
    ("offset_boolean", ["candidatos", 0, "ocurrencias", 0, "inicio"], False),
    ("offset_wrong", ["candidatos", 0, "ocurrencias", 0, "fin"], 99),
    ("literal_wrong", ["candidatos", 0, "ocurrencias", 0, "literal"], "inferior"),
    ("reason_placeholder", ["candidatos", 0, "ocurrencias", 0, "motivo"], "pendiente"),
    ("clause_blank", ["candidatos", 0, "ocurrencias", 0, "celda_o_clausula"], ""),
    ("verdict_unknown", ["candidatos", 0, "ocurrencias", 0, "dictamen"], "CONFORME"),
    ("verdict_list", ["candidatos", 0, "ocurrencias", 0, "dictamen"], []),
    ("verdict_teleology", ["candidatos", 0, "ocurrencias", 0, "dictamen"], "TELEOLOGICO"),
    ("verdict_unverifiable", ["candidatos", 0, "ocurrencias", 0, "dictamen"], "NO_VERIFICABLE"),
    ("verdict_independence_conflict", ["candidatos", 0, "ocurrencias", 0, "dictamen"], "NO_VERIFICABLE_POR_INDEPENDENCIA"),
):
    record(name, False, lambda f, p=path, v=value: mutate(f, p, v))


def list_change(f, kind):
    if kind == "missing_candidate":
        f.document["candidatos"].pop()
    elif kind == "duplicate_candidate":
        f.document["candidatos"].append(copy.deepcopy(f.document["candidatos"][0]))
    else:
        entry = copy.deepcopy(f.document["candidatos"][0])
        entry["linea"] = 99
        f.document["candidatos"].append(entry)
    return baseline(f)


for kind in ("missing_candidate", "duplicate_candidate", "extra_candidate"):
    record(kind, False, lambda f, k=kind: list_change(f, k))


def changed_context(f, kind):
    f.save()
    if kind == "same_candidate_changed_context":
        f.context.write_text("Se altera el contexto, no las candidatas.\n")
    elif kind == "same_heading_changed_body":
        f.path.write_text(f.path.read_text() + "El cuerpo ya no es el que leyó el revisor.\n")
    elif kind == "new_route":
        extra = f.root / "docs/secciones/new.md"
        extra.write_text("Sin palabras candidatas.\n")
        f.paths.append(extra)
    elif kind == "missing_route":
        f.paths.remove(f.context)
    elif kind == "missing_file":
        f.context.unlink()
    elif kind == "outside_route":
        f.paths.append(f.root.parent / "no-autorizado.md")
    elif kind == "parent_component":
        f.paths.append(f.root / "docs/../no-autorizado.md")
    return f.check()


for kind in ("same_candidate_changed_context", "same_heading_changed_body", "new_route",
             "missing_route", "missing_file", "outside_route", "parent_component"):
    record(kind, False, lambda f, k=kind: changed_context(f, k))


def symlink(f, target):
    f.save()
    path = {"review": f.review, "corpus": f.path, "parent_directory": f.path.parent}[target]
    moved = path.with_name(path.name + ".original")
    path.rename(moved)
    path.symlink_to(moved, target_is_directory=target == "parent_directory")
    return f.check()


for kind in ("review", "corpus", "parent_directory"):
    record("symlink_" + kind, False, lambda f, k=kind: symlink(f, k))


def duplicate_key(f):
    f.save()
    f.review.write_text('{"version": 1, ' + f.review.read_text()[1:])
    return f.check()


record("duplicate_json_key", False, duplicate_key)


def nc_old(f, sentence, with_partial_review):
    f.path.write_text(sentence + "\n")
    f.document["huellas_rutas"][f.path.relative_to(f.root).as_posix()] = sha(f.path.read_bytes())
    f.document["candidatos"] = []
    if with_partial_review:
        literal = "superior"
        start = sentence.index(literal)
        f.document["candidatos"].append({
            "ruta": f.path.relative_to(f.root).as_posix(), "linea": 1, "localizador_logico": "FICTICIO-NC1",
            "texto": sentence, "sha256_texto": sha((sentence + "\n").encode()),
            "revisor": f.document["revisor"], "declaracion_independencia": f.document["declaracion_independencia"],
            "fecha_revision_utc": f.document["fecha_revision_utc"], "conflicto_autoria": "NO",
            "ocurrencias": [{"inicio": start, "fin": start + len(literal), "literal": literal,
                "celda_o_clausula": "La identidad es superior a 70 %", "dictamen": "USO_CUANTITATIVO",
                "motivo": "Solo cubre esta comparación; el linaje no fue adjudicado."}],
        })
    f.save()
    result = controls.Result("R-0002", "FICTICIO_NO_CONTROL_REAL")
    controls.check_teleology_candidates(f.corpus(), result)
    return result.metrics["candidatos_teleologia"], result.metrics["ocurrencias_teleologia"], result.errors


record("NC_TEL_01_empty_ledger", False, lambda f: nc_old(f, "La identidad es superior a 70 %; este linaje es primitivo.", False))
record("NC_TEL_01_partial_occurrence", False, lambda f: nc_old(f, "La identidad es superior a 70 %; este linaje es primitivo.", True))
record("NC_TEL_02_empty_ledger", False, lambda f: nc_old(f, "Hay un criterio; este linaje es más evolucionado.", False))


def race(f, stage, target):
    f.save()
    if stage == "after_validate":
        original = consumer.validate_review
        def changed(*args):
            original(*args)
            destination = f.context if target == "context" else f.review
            destination.write_bytes(destination.read_bytes() + b"\n")
        with patch.object(consumer, "validate_review", side_effect=changed):
            return f.check()
    original = Path.read_bytes
    ledger_reads = 0
    def final_read(path):
        nonlocal ledger_reads
        payload = original(path)
        if path == f.review:
            ledger_reads += 1
            if ledger_reads == 2:
                # El consumidor ya releyó todo el contexto, pero todavía no retornó.
                f.context.write_bytes(original(f.context) + b"Contexto nuevo al final.\n")
        return payload
    with patch.object(Path, "read_bytes", final_read):
        return f.check()


record("race_context_after_validation", False, lambda f: race(f, "after_validate", "context"))
record("race_ledger_after_validation", False, lambda f: race(f, "after_validate", "review"))
record("race_context_during_final_ledger_read", False, lambda f: race(f, "final_read", "context"))


def stale_artifact(f):
    f.save()
    result = controls.Result("R-0002", "FICTICIO_NO_CONTROL_REAL")
    corpus = f.corpus()
    corpus.scoped_digest = lambda paths: sha("".join(
        str(path.relative_to(f.root)) + "\x1f" + sha(path.read_bytes()) + "\n" for path in sorted(paths)
    ).encode())
    controls.check_teleology_candidates(corpus, result)
    f.context.write_text("Contexto alterado después del cotejo y antes de materializar.\n")
    artifact = controls.artifact_row(corpus, result)
    errors = [] if artifact["resultado_control"] == "CERO_FALLOS" else [artifact["resultado_control"]]
    return result.metrics["candidatos_teleologia"], result.metrics["ocurrencias_teleologia"], errors


record("integration_changed_context_before_artifact", False, stale_artifact)


def verified_output(f, failing):
    f.save()
    approved = {f.root / "stale.md": "0" * 64}
    if failing:
        f.context.write_text("Contexto diferente del revisado.\n")
    observation = consumer.check_context_reviews(f.root, f.paths, verified_hashes=approved)
    if failing:
        assert approved == {}, "el fallo deja hashes aprobados residuales"
    else:
        expected = {p: sha(p.read_bytes()) for p in [*f.paths, f.review]}
        assert approved == expected, "los hashes aprobados no son el snapshot preciso"
    return observation


record("verified_hashes_exact_and_no_stale", True, lambda f: verified_output(f, False))
record("verified_hashes_cleared_on_failure", False, lambda f: verified_output(f, True))


def mutate_and_restore(f, target):
    f.save()
    original = consumer.validate_review
    destination = f.context if target == "context" else f.review
    def changing(*args):
        original(*args)
        payload = destination.read_bytes()
        destination.write_bytes(payload + b"cambio transitorio\n")
        destination.write_bytes(payload)
    with patch.object(consumer, "validate_review", side_effect=changing):
        return f.check()


record("transient_context_mutation_restored_bytes", False, lambda f: mutate_and_restore(f, "context"))
record("transient_ledger_mutation_restored_bytes", False, lambda f: mutate_and_restore(f, "ledger"))


def final_symlink(f):
    f.save()
    original = Path.read_bytes
    reads = 0
    def reading(path):
        nonlocal reads
        payload = original(path)
        if path == f.review:
            reads += 1
            if reads == 2:
                moved = f.context.with_suffix(".original")
                f.context.rename(moved)
                f.context.symlink_to(moved)
        return payload
    with patch.object(Path, "read_bytes", reading):
        return f.check()


record("symlink_same_bytes_during_final_ledger_read", False, final_symlink)


def materialization(f, kind):
    f.save()
    result = controls.Result("R-0002", "FICTICIO_NO_CONTROL_REAL")
    corpus = f.corpus()
    controls.check_teleology_candidates(corpus, result)
    assert not result.errors and len(result.reviewed_inputs) == 3
    if kind == "ledger_changed":
        f.review.write_bytes(f.review.read_bytes() + b"\n")
    elif kind == "context_missing":
        f.context.unlink()
    elif kind == "scope_missing":
        result.scope_paths.remove(f.context)
    elif kind == "context_symlink":
        moved = f.context.with_suffix(".original")
        f.context.rename(moved)
        f.context.symlink_to(moved)
    elif kind == "same_bytes_rewrite":
        f.context.write_bytes(f.context.read_bytes())
    if kind == "race_later_hash_changes_earlier":
        original = controls.sha256_file
        def hashing(path):
            value = original(path)
            if path == f.context:
                f.path.write_bytes(f.path.read_bytes() + b"Cambio de contexto posterior.\n")
            return value
        with patch.object(controls, "sha256_file", hashing):
            artifact = controls.artifact_row(corpus, result)
    else:
        artifact = controls.artifact_row(corpus, result)
    if kind in {"repeat_identical", "same_bytes_rewrite"}:
        assert artifact == controls.artifact_row(corpus, result), "artefacto no idempotente"
    if artifact["resultado_control"] == "NO_CONFORME":
        assert result.metrics["fallos"] == len(result.errors) > 0
        assert "fallos=0" not in artifact["evidencia"]
    return result.metrics["candidatos_teleologia"], result.metrics["ocurrencias_teleologia"], result.errors


for kind in ("ledger_changed", "context_missing", "scope_missing", "context_symlink", "race_later_hash_changes_earlier"):
    record("materialization_" + kind, False, lambda f, k=kind: materialization(f, k))
for kind in ("repeat_identical", "same_bytes_rewrite"):
    record("materialization_" + kind, True, lambda f, k=kind: materialization(f, k))


def invalid_unicode(f):
    f.save()
    f.context.write_bytes(b"\xff\xfe")
    return f.check()


record("invalid_utf8_fail_closed", False, invalid_unicode)


def failed_recheck(f):
    f.save()
    result = controls.Result("R-0002", "FICTICIO_NO_CONTROL_REAL")
    controls.check_teleology_candidates(f.corpus(), result)
    assert result.reviewed_inputs
    f.document["candidatos"].pop()
    f.save()
    controls.check_teleology_candidates(f.corpus(), result)
    assert result.reviewed_inputs == {}
    return result.metrics["candidatos_teleologia"], result.metrics["ocurrencias_teleologia"], result.errors


record("failed_recheck_drops_previous_hashes", False, failed_recheck)

live_result = controls.Result("R-0002", "LECTURA_DIAGNOSTICA_NO_CIERRE")
controls.check_teleology_candidates(controls.Corpus(ROOT), live_result)
files = (
    "scripts/check_teleology_contexts.py", "scripts/audit_requirement_controls.py",
    "tests/test_check_teleology_contexts.py", "tests/test_audit_requirement_controls.py",
    "docs/auditorias/censo_contextos_teleologia_v2_contexto_2026-09-27.json",
    str(Path(__file__).relative_to(ROOT)),
)
print(json.dumps({
    "utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    "scope": "Consumidor e integración técnica; revisor autor del ledger, no del consumidor. Sin aprobación de ciencia ni controles globales.",
    "hashes": {p: sha((ROOT / p).read_bytes()) for p in files},
    "tests": len(results), "passed": sum(row["result"] == "PASS" for row in results), "results": results,
    "live": {"metrics": dict(live_result.metrics), "errors": live_result.errors,
             "verified_hashes": len(live_result.reviewed_inputs)},
}, ensure_ascii=False, indent=2))
