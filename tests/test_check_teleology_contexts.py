"""Datos ficticios de contrato: no son revisiones del corpus de producción."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

from scripts import check_teleology_contexts as contexts


def fictitious_review(root: Path, paths: list[Path], verdicts: list[str]) -> dict:
    """Solo fixture explícita; quien llama adjudica cada ocurrencia sintética."""
    candidates, snapshots = contexts.collect(root, paths)
    decisions = iter(verdicts)
    document = {
        "version": 2, "alcance": "Contrato ficticio unitario; no firma de producción",
        "revisor": "REVISOR_FICTICIO_SOLO_TEST",
        "declaracion_independencia": contexts.INDEPENDENCE,
        "fecha_revision_utc": "2026-09-27T01:00:00Z",
        "fecha_snapshot_utc": "2026-09-27T01:00:01Z",
        "algoritmo_huella": "SHA256(UTF8(texto+LF))",
        "huellas_rutas": {path: contexts.digest(payload) for path, payload in snapshots.items()},
        "candidatos": [],
    }
    for (path, line), (text, hits) in candidates.items():
        entry = {
            "ruta": path, "linea": line, "localizador_logico": f"fixture:{line}",
            "texto": text, "sha256_texto": contexts.digest((text + "\n").encode()),
            "revisor": document["revisor"],
            "declaracion_independencia": contexts.INDEPENDENCE,
            "fecha_revision_utc": document["fecha_revision_utc"],
            "conflicto_autoria": "NO", "ocurrencias": [],
        }
        for hit in hits:
            entry["ocurrencias"].append({
                "inicio": hit.start(), "fin": hit.end(), "literal": hit.group(),
                "celda_o_clausula": text, "dictamen": next(decisions),
                "motivo": "Adjudicación sintética explícita para esta prueba, no para el corpus",
            })
        document["candidatos"].append(entry)
    if next(decisions, None) is not None:
        raise AssertionError("sobran dictámenes ficticios")
    write_review(root, document)
    return document


def write_review(root: Path, document: dict) -> None:
    path = root / contexts.REVIEW_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")


class TeleologyContextTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.path = self.root / "docs/secciones/014-contexto.md"
        self.path.parent.mkdir(parents=True)
        self.path.write_text("El valor es superior a 70 %.\nContexto sin candidato.\n", encoding="utf-8")
        self.paths = [self.path]
        self.document = fictitious_review(self.root, self.paths, ["USO_CUANTITATIVO"])

    def check(self):
        return contexts.check_context_reviews(self.root, self.paths)

    def rejected(self, document=None):
        if document is not None:
            write_review(self.root, document)
        self.assertTrue(self.check()[2])

    def test_exact_review_and_counts(self):
        self.assertEqual(self.check(), (1, 1, []))

    def test_previous_schema_is_not_accepted(self):
        self.document["version"] = 1
        self.rejected(self.document)

    def test_missing_review_does_not_approve_quantitative_text(self):
        (self.root / contexts.REVIEW_PATH).unlink()
        self.rejected()

    def test_two_real_line_exemptions_are_not_available(self):
        for text in (
            "La identidad es superior a 70 %; este linaje es primitivo.",
            "Hay un criterio; este linaje es más evolucionado.",
        ):
            with self.subTest(text=text):
                self.path.write_text(text + "\n", encoding="utf-8")
                self.rejected()

    def test_context_change_with_unchanged_candidate_is_rejected(self):
        self.path.write_text("El valor es superior a 70 %.\nAhora hablamos de linajes.\n", encoding="utf-8")
        self.rejected()

    def test_added_candidate_with_new_context_hash_still_needs_review(self):
        self.path.write_text("El valor es superior a 70 %.\nEs un organismo simple.\n", encoding="utf-8")
        self.document["huellas_rutas"][self.path.relative_to(self.root).as_posix()] = contexts.digest(self.path.read_bytes())
        self.rejected(self.document)

    def test_added_non_candidate_route_changes_scope(self):
        path = self.root / "docs/secciones/nueva.md"
        path.write_text("Contexto adicional.\n", encoding="utf-8")
        self.paths.append(path)
        self.rejected()

    def test_deleted_candidate_cannot_leave_orphan_review(self):
        self.path.write_text("Nada aquí.\n", encoding="utf-8")
        self.document["huellas_rutas"][self.path.relative_to(self.root).as_posix()] = contexts.digest(self.path.read_bytes())
        self.rejected(self.document)

    def test_unknown_fields_and_wrong_types_fail_closed(self):
        mutations = [
            ((), "extra", 1), ((), "version", True), ((), "candidatos", {}),
            (("candidatos", 0), "linea", True),
            (("candidatos", 0), "ocurrencias", {}),
            (("candidatos", 0, "ocurrencias", 0), "inicio", False),
            (("candidatos", 0, "ocurrencias", 0), "dictamen", []),
        ]
        for path, key, value in mutations:
            with self.subTest(path=path, key=key):
                document = copy.deepcopy(self.document)
                target = document
                for component in path:
                    target = target[component]
                target[key] = value
                self.rejected(document)

    def test_all_non_conforming_and_unknown_verdicts_block(self):
        for verdict in contexts.NEGATIVE | {"CONFORME", "PENDIENTE"}:
            with self.subTest(verdict=verdict):
                self.document["candidatos"][0]["ocurrencias"][0]["dictamen"] = verdict
                self.rejected(self.document)

    def test_one_good_occurrence_cannot_exempt_another(self):
        self.path.write_text("El valor es superior a 70 %; el linaje es primitivo.\n", encoding="utf-8")
        self.document = fictitious_review(self.root, self.paths, ["USO_CUANTITATIVO", "TELEOLOGICO"])
        self.rejected()
        self.document["candidatos"][0]["ocurrencias"].pop()
        self.rejected(self.document)

    def test_offsets_literal_and_hash_are_exact(self):
        for key, value in (("inicio", 1), ("fin", 2), ("literal", "inferior")):
            document = copy.deepcopy(self.document)
            document["candidatos"][0]["ocurrencias"][0][key] = value
            self.rejected(document)
        for key, value in (("texto", "otro"), ("sha256_texto", "0" * 64)):
            document = copy.deepcopy(self.document)
            document["candidatos"][0][key] = value
            self.rejected(document)

    def test_missing_and_duplicate_entries_block(self):
        for entries in ([], self.document["candidatos"] * 2):
            document = copy.deepcopy(self.document)
            document["candidatos"] = entries
            self.rejected(document)

    def test_nominal_independence_and_reason_required(self):
        for key, value in (("conflicto_autoria", "SI"), ("revisor", "otro"),
                           ("declaracion_independencia", ""), ("localizador_logico", "n/a")):
            document = copy.deepcopy(self.document)
            document["candidatos"][0][key] = value
            self.rejected(document)
        for key in ("motivo", "celda_o_clausula"):
            document = copy.deepcopy(self.document)
            document["candidatos"][0]["ocurrencias"][0][key] = ""
            self.rejected(document)

    def test_invalid_or_misordered_utc_is_rejected(self):
        for stamp in ("2026-09-27", "2026-02-30T01:00:00Z", "2026-09-27T25:00:00Z", 1):
            document = copy.deepcopy(self.document)
            document["fecha_revision_utc"] = stamp
            self.rejected(document)
        document = copy.deepcopy(self.document)
        document["fecha_snapshot_utc"] = "2026-09-26T01:00:00Z"
        self.rejected(document)
        document = copy.deepcopy(self.document)
        document["candidatos"][0]["fecha_revision_utc"] = "2026-09-28T01:00:00Z"
        self.rejected(document)

    def test_duplicate_json_keys_are_not_silently_overwritten(self):
        path = self.root / contexts.REVIEW_PATH
        path.write_text('{"version": 1, ' + path.read_text()[1:], encoding="utf-8")
        self.rejected()

    def test_symlink_corpus_and_review_rejected(self):
        original = self.path.read_bytes()
        other = self.root / "other.md"
        other.write_bytes(original)
        self.path.unlink()
        self.path.symlink_to(other)
        self.rejected()
        self.path.unlink()
        self.path.write_bytes(original)
        review = self.root / contexts.REVIEW_PATH
        destination = self.root / "review.json"
        review.rename(destination)
        review.symlink_to(destination)
        self.rejected()

    def test_outside_and_parent_paths_rejected(self):
        for path in (self.root.parent / "outside.md", self.root / ".." / "outside.md"):
            self.paths = [path]
            self.rejected()

    def test_changed_context_or_review_during_validation_rejected(self):
        validate = contexts.validate_review
        for target in (self.path, self.root / contexts.REVIEW_PATH):
            original = target.read_bytes()
            def mutate(*args):
                validate(*args)
                target.write_bytes(original + b"\n")
            with mock.patch.object(contexts, "validate_review", side_effect=mutate):
                self.rejected()
            target.write_bytes(original)

    def test_context_changed_by_final_review_read_is_rejected(self):
        original = Path.read_bytes
        reads = 0
        def mutate(path):
            nonlocal reads
            payload = original(path)
            if path == self.root / contexts.REVIEW_PATH:
                reads += 1
                if reads == 2:
                    self.path.write_bytes(original(self.path) + b"Contexto cambiado.\n")
            return payload
        with mock.patch.object(Path, "read_bytes", mutate):
            self.rejected()

    def test_attestation_contains_only_successful_exact_bytes(self):
        hashes = {}
        self.assertFalse(contexts.check_context_reviews(self.root, self.paths, verified_hashes=hashes)[2])
        self.assertEqual(hashes[self.path], contexts.digest(self.path.read_bytes()))
        self.assertIn(self.root / contexts.REVIEW_PATH, hashes)
        self.path.write_text("Un linaje primitivo.\n", encoding="utf-8")
        self.assertTrue(contexts.check_context_reviews(self.root, self.paths, verified_hashes=hashes)[2])
        self.assertEqual(hashes, {})

    def test_empty_candidate_set_still_needs_scope_bound_review(self):
        self.path.write_text("Sin candidatos.\n", encoding="utf-8")
        fictitious_review(self.root, self.paths, [])
        self.assertEqual(self.check(), (0, 0, []))
        (self.root / contexts.REVIEW_PATH).unlink()
        self.rejected()


if __name__ == "__main__":
    unittest.main()
