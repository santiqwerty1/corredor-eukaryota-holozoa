from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest import mock

from scripts import audit_requirement_controls as controls
from scripts import corpus_io


class RequirementControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.corpus = controls.Corpus(cls.root)
        _, rows = controls.load_control_rows(cls.root)
        cls.controls_by_id = {
            row["id_requisito"]: row for row in rows
            if row["tipo"] == "CONTROL_ESTRUCTURAL"
        }
        cls.literals = controls.load_requirement_literals(cls.root)

    def valid_manual_row(self, rid: str = "R-0052"):
        result = controls.evaluate(self.corpus, self.controls_by_id[rid])
        row = controls.manual_template_row(
            self.corpus, result, self.literals[rid],
        )
        row.update({
            "prueba_nominal": (
                "Se inspeccionaron uno por uno los destinos censados contra "
                "el mandato literal y se registraron las excepciones."
            ),
            "resultado": "CONFORME",
            "evidencia": (
                "La inspección exhaustiva no encontró una infracción del "
                "mandato en el alcance identificado."
            ),
            "localizadores_evidencia": "data/table_index.json",
            "revisor": "Fermat / revisión independiente",
            "declaracion_independencia": controls.INDEPENDENCE_DECLARATION,
            "fecha_revision": "2026-08-08",
        })
        return result, row

    def test_generic_target_existence_cannot_verify_a_control(self) -> None:
        corpus = mock.Mock()
        corpus.index_path = Path("data/table_index.json")
        row = {
            "id_requisito": "R-9999",
            "control_o_rollup": "CONTROL::MANDATO_NO_IMPLEMENTADO",
        }

        def generic_target_check(_corpus, _row, result) -> None:
            result.check(True, "destino existe", "destino ausente")

        with (
            mock.patch.object(controls, "add_targets", generic_target_check),
            mock.patch.object(controls, "check_specific", lambda *_: None),
        ):
            result = controls.evaluate(corpus, row)

        self.assertEqual(len(result.errors), 1)
        self.assertIn("PENDIENTE_AUTOMATIZACION_NOMINAL", result.errors[0])

    def test_supplementary_s_labels_are_not_sources(self) -> None:
        self.assertIs(controls.expand_source_refs, corpus_io.expand_source_refs)
        value = "S27 Results; figs. S62–S63; tabla S8"
        self.assertEqual(controls.expand_source_refs(value), ["S27"])

    def test_real_source_ranges_expand_and_descending_ranges_fail(self) -> None:
        self.assertEqual(
            controls.expand_source_refs("S08–S10 resultados; S12 discusión"),
            ["S08", "S09", "S10", "S12"],
        )
        with self.assertRaisesRegex(ValueError, "[Rr]ango S descendente"):
            controls.expand_source_refs("S10–S08")

    def test_many_generic_targets_still_leave_control_pending(self) -> None:
        result = controls.evaluate(
            self.corpus, self.controls_by_id["R-0052"],
        )
        self.assertFalse(result.automated)
        self.assertGreater(result.metrics["C_objetivo"], 0)
        self.assertTrue(any(
            "PENDIENTE_AUTOMATIZACION_NOMINAL" in error
            for error in result.errors
        ))

    def test_manual_review_binds_literal_and_live_scope(self) -> None:
        result, row = self.valid_manual_row()
        self.assertEqual(
            controls.validate_manual_review(
                self.corpus, result, self.literals[result.requirement_id], row,
            ),
            [],
        )
        row["huella_alcance_sha256"] = "0" * 64
        errors = controls.validate_manual_review(
            self.corpus, result, self.literals[result.requirement_id], row,
        )
        self.assertTrue(any("alcance live desactualizada" in error for error in errors))

    def test_bare_manual_attestation_is_rejected(self) -> None:
        result, row = self.valid_manual_row()
        row["prueba_nominal"] = "CUMPLE"
        row["evidencia"] = "OK"
        errors = controls.validate_manual_review(
            self.corpus, result, self.literals[result.requirement_id], row,
        )
        self.assertTrue(any("prueba nominal" in error for error in errors))
        self.assertTrue(any("evidencia manual" in error for error in errors))

    def test_manual_evidence_locator_must_resolve(self) -> None:
        result, row = self.valid_manual_row()
        row["localizadores_evidencia"] = "docs/no-existe.md:L1"
        errors = controls.validate_manual_review(
            self.corpus, result, self.literals[result.requirement_id], row,
        )
        self.assertTrue(any("no resoluble" in error for error in errors))

    def test_manual_ledger_accepts_exactly_one_valid_pending_row(self) -> None:
        result, row = self.valid_manual_row()
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "ledger.csv"
            path.write_bytes(controls.csv_bytes(controls.MANUAL_LEDGER_HEADER, [row]))
            with mock.patch.object(controls, "MANUAL_LEDGER", path):
                reviews, errors = controls.load_manual_reviews(
                    self.corpus, {result.requirement_id: result},
                    require_ledger=True,
                )
        self.assertEqual(errors, [])
        self.assertEqual(set(reviews), {result.requirement_id})
        self.assertTrue(reviews[result.requirement_id].conforms)

    def test_manual_ledger_rejects_duplicate_rows(self) -> None:
        result, row = self.valid_manual_row()
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "ledger.csv"
            path.write_bytes(
                controls.csv_bytes(controls.MANUAL_LEDGER_HEADER, [row, row])
            )
            with mock.patch.object(controls, "MANUAL_LEDGER", path):
                reviews, errors = controls.load_manual_reviews(
                    self.corpus, {result.requirement_id: result},
                    require_ledger=True,
                )
        self.assertEqual(reviews, {})
        self.assertTrue(any("aparece 2 veces" in error for error in errors))

    def test_manual_ledger_rejects_truncated_rows_without_crashing(self) -> None:
        result, _ = self.valid_manual_row()
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "ledger.csv"
            path.write_text(
                ",".join(controls.MANUAL_LEDGER_HEADER) + "\nR-0052\n",
                encoding="utf-8",
            )
            with mock.patch.object(controls, "MANUAL_LEDGER", path):
                reviews, errors = controls.load_manual_reviews(
                    self.corpus, {result.requirement_id: result},
                    require_ledger=True,
                )
        self.assertEqual(reviews, {})
        self.assertTrue(any("cardinalidad inválida" in error for error in errors))

    def test_schema_mutation_fails_named_source_catalog_family(self) -> None:
        original = self.corpus.appendices["A"]
        header, rows = original
        self.corpus.appendices["A"] = (header[:-1], rows)
        try:
            result = controls.evaluate(
                self.corpus, self.controls_by_id["R-0405"],
            )
        finally:
            self.corpus.appendices["A"] = original
        self.assertTrue(result.automated)
        self.assertEqual(result.automation_families, {"CATALOGO_FUENTES"})
        self.assertTrue(any("cabecera A distinta" in error for error in result.errors))

    def test_enum_mutation_fails_named_source_catalog_family(self) -> None:
        header, rows = self.corpus.appendices["A"]
        mutated = [dict(row) for row in rows]
        mutated[0]["tipo"] = "prestigiosa"
        original = self.corpus.appendices["A"]
        self.corpus.appendices["A"] = (header, mutated)
        try:
            result = controls.evaluate(
                self.corpus, self.controls_by_id["R-0406"],
            )
        finally:
            self.corpus.appendices["A"] = original
        self.assertTrue(result.automated)
        self.assertTrue(any("fuera del enum" in error for error in result.errors))

    def test_trace_mutation_fails_content_trace_family(self) -> None:
        semantic = self.corpus.semantic_result
        trace = self.corpus.content_trace_result
        self.corpus.semantic_result = (0, "semántica simulada correcta")
        self.corpus.content_trace_result = (1, "mutación: segmento sin C")
        try:
            result = controls.evaluate(
                self.corpus, self.controls_by_id["R-0340"],
            )
        finally:
            self.corpus.semantic_result = semantic
            self.corpus.content_trace_result = trace
        self.assertTrue(result.automated)
        self.assertEqual(
            result.automation_families, {"TRAZABILIDAD_CONTENIDO_EXACTA"},
        )
        self.assertIn("mutación: segmento sin C", result.errors)

    def test_teleological_sentence_mutation_is_rejected(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "docs/secciones/003-mutacion.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "Este linaje es más evolucionado y constituye un paso obligatorio.\n",
                encoding="utf-8",
            )
            corpus = SimpleNamespace(
                root=root, section_paths=[path], claim_paths={},
                index={"tables": []}, appendix_paths={},
            )
            result = controls.Result("R-0002", "LITERAL_PROMPT_COMPLETO")
            controls.check_teleology_candidates(corpus, result)
        self.assertTrue(any("candidatos no clasificados" in error for error in result.errors))

    def test_trivial_motive_mutation_is_rejected(self) -> None:
        claim_id = next(iter(self.corpus.claims))
        original = self.corpus.claims[claim_id]["Motivo"]
        self.corpus.claims[claim_id]["Motivo"] = "ok"
        try:
            result = controls.evaluate(
                self.corpus, self.controls_by_id["R-0365"],
            )
        finally:
            self.corpus.claims[claim_id]["Motivo"] = original
        self.assertTrue(result.automated)
        self.assertTrue(any("Motivo vacío/trivial" in error for error in result.errors))

    def test_final_question_mutation_fails_closure_family(self) -> None:
        table_id = "table-77-19-respuestas-a-las-seis-preguntas-de-cierre"
        original = self.corpus.table_rows[table_id]
        header, rows = original
        self.corpus.table_rows[table_id] = (header, rows[:-1])
        try:
            result = controls.evaluate(
                self.corpus, self.controls_by_id["R-0477"],
            )
        finally:
            self.corpus.table_rows[table_id] = original
        self.assertTrue(result.automated)
        self.assertTrue(any("cierre contiene 5 preguntas" in error for error in result.errors))

    def test_all_controls_are_explicitly_automated_or_pending(self) -> None:
        results = [
            controls.evaluate(self.corpus, row)
            for row in self.controls_by_id.values()
        ]
        self.assertEqual(len(results), 252)
        for result in results:
            if result.automated:
                self.assertGreater(result.metrics["pruebas_nominales"], 0)
                self.assertFalse(any(
                    "PENDIENTE_AUTOMATIZACION_NOMINAL" in error
                    for error in result.errors
                ))
            else:
                self.assertTrue(any(
                    "PENDIENTE_AUTOMATIZACION_NOMINAL" in error
                    for error in result.errors
                ))


if __name__ == "__main__":
    unittest.main()
