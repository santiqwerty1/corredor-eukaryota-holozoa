from __future__ import annotations

import csv
import json
import math
import tempfile
import unittest
from pathlib import Path

from scripts import audit_full


class AuditFullMutationTests(unittest.TestCase):
    def _claim_context(self, rows: list[list[str]]) -> audit_full.AuditContext:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        claims = root / "data" / "afirmaciones" / "00.csv"
        claims.parent.mkdir(parents=True)
        with claims.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(audit_full.CLAIM_COLUMNS)
            writer.writerows(rows)
        (root / "data" / "table_index.json").write_text(
            json.dumps({
                "tables": [{
                    "category": "claims",
                    "section": "00",
                    "csv_path": "data/afirmaciones/00.csv",
                }],
            }),
            encoding="utf-8",
        )
        return audit_full.AuditContext(root)

    @staticmethod
    def _row(
        cid: str,
        predicate: str = "posee_rasgo",
        subject: str = "sujeto",
        obj: str = "objeto",
        attribution: str = "expresa",
        source: str = "S01, Results, p. 1",
    ) -> list[str]:
        return [
            cid, "Afirmación de prueba", subject, predicate, obj,
            attribution, source, "no evaluado", "media",
            "Pasaje localizado para la prueba.", "resuelta", "vigente",
        ]

    def test_custom_predicate_without_star_is_rejected(self) -> None:
        context = self._claim_context([self._row("C-001", "predicado_nuevo")])
        findings: list[audit_full.Finding] = []
        audit_full.audit_claims(context, findings)
        self.assertIn("AF110", {finding.code for finding in findings})

    def test_closed_predicate_with_star_is_rejected(self) -> None:
        context = self._claim_context([self._row("C-001", "posee_rasgo*")])
        findings: list[audit_full.Finding] = []
        audit_full.audit_claims(context, findings)
        self.assertIn("AF111", {finding.code for finding in findings})

    def test_locator_is_not_inherited_from_longer_source_id(self) -> None:
        context = self._claim_context([
            self._row("C-001", source="S10; S100 Results"),
        ])
        findings: list[audit_full.Finding] = []
        audit_full.audit_claims(context, findings)
        messages = [finding.message for finding in findings if finding.code == "AF202"]
        self.assertIn("Fuente sin localizador propio: S10", messages)

    def test_expressa_may_use_honest_unlocated_marker(self) -> None:
        context = self._claim_context([
            self._row("C-001", source="S01 sin localizar"),
        ])
        findings: list[audit_full.Finding] = []
        audit_full.audit_claims(context, findings)
        self.assertNotIn("AF201", {finding.code for finding in findings})
        self.assertNotIn("AF202", {finding.code for finding in findings})

    def test_glosa_cannot_keep_bibliographic_source(self) -> None:
        context = self._claim_context([
            self._row("C-001", attribution="glosa", source="S01 Results"),
        ])
        findings: list[audit_full.Finding] = []
        audit_full.audit_claims(context, findings)
        self.assertIn("AF203", {finding.code for finding in findings})

    def test_glosa_may_keep_bounded_operational_reference(self) -> None:
        context = self._claim_context([
            self._row("C-001", attribution="glosa", source="BN-001"),
        ])
        findings: list[audit_full.Finding] = []
        audit_full.audit_claims(context, findings)
        self.assertNotIn("AF203", {finding.code for finding in findings})

    def test_contradiction_without_claim_destination_is_rejected(self) -> None:
        context = self._claim_context([
            self._row("C-001"),
            self._row("C-002", "cuestionado_por", obj="objeto sin clave C"),
        ])
        findings: list[audit_full.Finding] = []
        audit_full.audit_claims(context, findings)
        self.assertIn("AF120", {finding.code for finding in findings})

    def test_invalid_synthesis_is_rejected(self) -> None:
        context = self._claim_context([
            self._row("C-001"),
            self._row("C-002", attribution="sintesis(C-999)"),
        ])
        findings: list[audit_full.Finding] = []
        audit_full.audit_claims(context, findings)
        self.assertIn("AF131", {finding.code for finding in findings})

    def test_derived_quantity_language_is_rejected(self) -> None:
        context = self._claim_context([
            self._row("C-001", obj="punto medio derivado de los extremos"),
        ])
        findings: list[audit_full.Finding] = []
        audit_full.audit_claims(context, findings)
        self.assertIn("AF400", {finding.code for finding in findings})

    def test_claim_fingerprint_changes_with_semantics(self) -> None:
        first = dict(zip(audit_full.CLAIM_COLUMNS, self._row("C-001")))
        second = dict(first)
        second["Objeto"] = "objeto mutado"
        self.assertNotEqual(
            audit_full.claim_fingerprint(first),
            audit_full.claim_fingerprint(second),
        )

    def test_synthesis_range_expands_deterministically(self) -> None:
        self.assertEqual(
            audit_full.parse_synthesis_refs("sintesis(C-001–C-003,C-005)"),
            ["C-001", "C-002", "C-003", "C-005"],
        )

    def test_frozen_row_hash_and_aggregate_detect_mutation_and_reorder(self) -> None:
        first = {"clave": "C-001", "texto": "árbol"}
        second = {"clave": "C-002", "texto": "rama"}
        first_hash = audit_full.canonical_row_fingerprint(first)
        second_hash = audit_full.canonical_row_fingerprint(second)
        baseline = audit_full.aggregate_keyed_fingerprints([
            ("C-001", first_hash), ("C-002", second_hash),
        ])
        mutated = dict(first)
        mutated["texto"] = "árbol mutado"
        self.assertNotEqual(first_hash, audit_full.canonical_row_fingerprint(mutated))
        self.assertNotEqual(
            baseline,
            audit_full.aggregate_keyed_fingerprints([
                ("C-002", second_hash), ("C-001", first_hash),
            ]),
        )

    def test_reference_ranges_expand_without_losing_interior_keys(self) -> None:
        self.assertEqual(
            audit_full.expanded_refs("C-998–C-1001; C-1003", "C-"),
            ["C-998", "C-999", "C-1000", "C-1001", "C-1003"],
        )
        self.assertEqual(
            audit_full.expanded_refs("S08–S10", "S"),
            ["S08", "S09", "S10"],
        )
        self.assertEqual(
            audit_full.expanded_refs(
                "S27 Results; figs. S62–S63; tabla S8", "S",
            ),
            ["S27"],
        )

    def test_iso_date_rejects_impossible_and_post_cutoff_values(self) -> None:
        self.assertTrue(audit_full.valid_iso_date("2026-08-08"))
        self.assertFalse(audit_full.valid_iso_date("2026-02-30"))
        self.assertFalse(audit_full.valid_iso_date("2026-08-09"))
        self.assertFalse(audit_full.valid_iso_date("08/08/2026"))

    def test_stratified_sample_is_stable_and_uses_ceiling(self) -> None:
        keys = {f"C-{number:03d}" for number in range(1, 8)}
        first = audit_full.deterministic_sample(keys, "AFIRMACION")
        second = audit_full.deterministic_sample(set(reversed(sorted(keys))), "AFIRMACION")
        self.assertEqual(first, second)
        self.assertEqual(len(first), math.ceil(len(keys) * 0.15))

    def _answer_context(self, questions: list[str], answer_suffix: str = "") -> audit_full.AuditContext:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        table = root / "data/tablas/19/table-77-19-respuestas-a-las-seis-preguntas-de-cierre.csv"
        table.parent.mkdir(parents=True)
        with table.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["pregunta", "secciones con material integrado", "respuesta breve con citas"])
            for question in questions:
                writer.writerow([question, "1", f"Resultado provisional científico {answer_suffix} [C-001; S01]"])
        return audit_full.AuditContext(root)

    def test_scientific_use_of_provisional_is_not_an_editorial_placeholder(self) -> None:
        context = self._answer_context(audit_full.FINAL_QUESTIONS)
        findings: list[audit_full.Finding] = []
        audit_full.audit_final_answers(context, findings)
        self.assertNotIn("AF712", {finding.code for finding in findings})
        self.assertNotIn("AF713", {finding.code for finding in findings})

    def test_final_question_literal_mutation_is_rejected(self) -> None:
        questions = list(audit_full.FINAL_QUESTIONS)
        questions[0] = questions[0].replace("estable", "duradera")
        context = self._answer_context(questions)
        findings: list[audit_full.Finding] = []
        audit_full.audit_final_answers(context, findings)
        self.assertIn("AF713", {finding.code for finding in findings})

    def test_explicit_editorial_placeholder_is_rejected(self) -> None:
        context = self._answer_context(
            audit_full.FINAL_QUESTIONS, "[PENDIENTE]",
        )
        findings: list[audit_full.Finding] = []
        audit_full.audit_final_answers(context, findings)
        self.assertIn("AF712", {finding.code for finding in findings})

    def _source_context(self, source_rows: list[list[str]]) -> audit_full.AuditContext:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        appendix = root / "data/apendices/A_fuentes.csv"
        appendix.parent.mkdir(parents=True)
        header = [
            "clave", "autores", "año", "título", "publicación o repositorio",
            "DOI en forma https://doi.org/10.xxxx/... o URL resoluble si no hay DOI",
            "tipo", "notas de calidad", "fecha de consulta",
        ]
        with appendix.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(header)
            writer.writerows(source_rows)
        (root / "data/table_index.json").write_text(
            json.dumps({"tables": []}), encoding="utf-8",
        )
        (root / "docs").mkdir()
        (root / "docs/order.txt").write_text("", encoding="utf-8")
        return audit_full.AuditContext(root)

    @staticmethod
    def _source_row(key: str, notes: str) -> list[str]:
        return [
            key, "Autor", "2026", f"Título {key}", "Revista",
            f"https://doi.org/10.0000/{key.casefold()}", "investigación primaria",
            notes, "2026-08-08",
        ]

    def test_single_use_is_not_confused_with_sole_support(self) -> None:
        usage = "[USO EN UNA SOLA C] C-001."
        context = self._source_context([
            self._source_row("S01", usage), self._source_row("S02", usage),
        ])
        claim = dict(zip(
            audit_full.CLAIM_COLUMNS,
            self._row("C-001", source="S01 Results; S02 Results"),
        ))
        findings: list[audit_full.Finding] = []
        audit_full.audit_sources(context, findings, [claim])
        self.assertNotIn("AF224", {finding.code for finding in findings})

    def test_sole_support_without_declaration_is_rejected(self) -> None:
        context = self._source_context([
            self._source_row("S01", "[USO EN UNA SOLA C] C-001."),
        ])
        claim = dict(zip(
            audit_full.CLAIM_COLUMNS,
            self._row("C-001", source="S01 Results"),
        ))
        findings: list[audit_full.Finding] = []
        audit_full.audit_sources(context, findings, [claim])
        self.assertIn("AF224", {finding.code for finding in findings})

    def test_source_ranges_count_interior_usage(self) -> None:
        context = self._source_context([
            self._source_row(
                "S08",
                "[SOPORTE ÚNICO ACTUAL] C-001. "
                "[USO EN UNA SOLA C] C-001.",
            ),
            self._source_row(
                "S09",
                "[SOPORTE ÚNICO ACTUAL] C-001.",
            ),
            self._source_row(
                "S10",
                "[SOPORTE ÚNICO ACTUAL] C-001. "
                "[USO EN UNA SOLA C] C-001.",
            ),
        ])
        claims = [
            dict(zip(
                audit_full.CLAIM_COLUMNS,
                self._row("C-001", source="S08–S10 Results"),
            )),
            dict(zip(
                audit_full.CLAIM_COLUMNS,
                self._row("C-002", source="S09 Results"),
            )),
        ]
        findings: list[audit_full.Finding] = []
        audit_full.audit_sources(context, findings, claims)
        self.assertNotIn("AF227", {finding.code for finding in findings})

    def test_content_trace_detects_a_mutated_content_hash(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        target = root / "docs/secciones/001-test.md"
        target.parent.mkdir(parents=True)
        target.write_text("Contenido. [C-001]\n", encoding="utf-8")
        ledger = root / audit_full.CONTENT_TRACE
        ledger.parent.mkdir(parents=True)
        with ledger.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(audit_full.CONTENT_TRACE_COLUMNS)
            writer.writerow([
                "TC-00001", "prosa", "docs/secciones/001-test.md", "L1",
                "n/a", "Contenido. [C-001]", "0" * 64, "C-001",
                "cita_en_segmento", "REVISADA",
            ])
        findings: list[audit_full.Finding] = []
        audit_full.audit_content_trace(
            audit_full.AuditContext(root), findings, {"C-001"},
        )
        self.assertIn("AF734", {finding.code for finding in findings})

    def test_content_trace_rejects_lexical_mapping_and_missing_claim(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        target = root / "docs/secciones/001-test.md"
        target.parent.mkdir(parents=True)
        target.write_text("Contenido.\n", encoding="utf-8")
        content = "Contenido."
        ledger = root / audit_full.CONTENT_TRACE
        ledger.parent.mkdir(parents=True)
        with ledger.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(audit_full.CONTENT_TRACE_COLUMNS)
            writer.writerow([
                "TC-00001", "prosa", "docs/secciones/001-test.md", "L1",
                "n/a", content,
                audit_full.sha256_bytes((content + "\n").encode("utf-8")),
                "C-001", "correspondencia_lexica_oracion", "REVISADA",
            ])
        findings: list[audit_full.Finding] = []
        audit_full.audit_content_trace(
            audit_full.AuditContext(root), findings, {"C-001", "C-002"},
        )
        codes = {finding.code for finding in findings}
        self.assertIn("AF739", codes)
        self.assertIn("AF738", codes)

    def test_report_mutation_reopens_the_gate(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        report = root / audit_full.AUDIT_REPORT
        report.parent.mkdir(parents=True)
        report.write_text(
            "\n".join([
                "# Auditoría", "## Metodología", "## Veredicto",
                "## Hallazgos por severidad", "P0 abiertos: 0",
                "P1 abiertos: 0", "## Correcciones", "## Límites restantes",
                audit_full.CUTOFF, audit_full.PROMPT_SHA256,
                audit_full.FROZEN_FINDINGS_MANIFEST_SHA256,
                Path(audit_full.SECOND_REVIEW).name, "make verify", "",
            ]),
            encoding="utf-8",
        )
        context = audit_full.AuditContext(root)
        findings: list[audit_full.Finding] = []
        audit_full.audit_report(context, findings)
        self.assertFalse(findings)
        report.write_text(
            report.read_text(encoding="utf-8").replace("P1 abiertos: 0", "P1 abiertos: 1"),
            encoding="utf-8",
        )
        findings = []
        audit_full.audit_report(context, findings)
        self.assertIn("AF072", {finding.code for finding in findings})

    def test_pending_second_review_is_rejected(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)

        def write(relative: str, header: list[str], rows: list[list[str]]) -> None:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(header)
                writer.writerows(rows)

        claim = {column: "n/a" for column in audit_full.CLAIM_MATRIX_COLUMNS}
        claim.update({
            "clave_inicial": "C-001", "severidad_inicial": "P0",
            "estado_inicial": "CORREGIR", "huella_final_sha256": "a" * 64,
        })
        write(audit_full.CLAIM_MATRIX, audit_full.CLAIM_MATRIX_COLUMNS, [
            [claim[column] for column in audit_full.CLAIM_MATRIX_COLUMNS],
        ])
        write(audit_full.SOURCE_MATRIX, audit_full.SOURCE_MATRIX_COLUMNS, [])
        write(audit_full.REQUIREMENT_MATRIX, audit_full.REQUIREMENT_MATRIX_COLUMNS, [])
        write(audit_full.CONTENT_TRACE, audit_full.CONTENT_TRACE_COLUMNS, [])
        review = {column: "n/a" for column in audit_full.SECOND_REVIEW_COLUMNS}
        review.update({
            "id_revision": "REV-00001", "estrato": "AFIRMACION",
            "clave_matriz": "C-001", "tipo_revision": "CORRECCION_P0_P1",
            "seleccion": "CENSO_100_PCT", "resultado": "PENDIENTE",
            "revisor_independiente": "NO_ASIGNADO",
            "declaracion_independencia": "PENDIENTE", "estado_cierre": "ABIERTO",
            "huella_objeto_sha256": "a" * 64,
        })
        write(audit_full.SECOND_REVIEW, audit_full.SECOND_REVIEW_COLUMNS, [
            [review[column] for column in audit_full.SECOND_REVIEW_COLUMNS],
        ])
        findings: list[audit_full.Finding] = []
        audit_full.audit_second_review(audit_full.AuditContext(root), findings)
        codes = {finding.code for finding in findings}
        self.assertTrue({"AF748", "AF749", "AF750", "AF751", "AF752"} <= codes)

    def test_open_failure_is_honest_and_triggers_full_expansion(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)

        def write(relative: str, header: list[str], rows: list[list[str]]) -> None:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(header)
                writer.writerows(rows)

        claim_rows: list[dict[str, str]] = []
        correction = {column: "n/a" for column in audit_full.CLAIM_MATRIX_COLUMNS}
        correction.update({
            "clave_inicial": "C-001", "severidad_inicial": "P0",
            "estado_inicial": "CORREGIR", "huella_final_sha256": "a" * 64,
        })
        claim_rows.append(correction)
        for number in range(2, 9):
            row = {column: "n/a" for column in audit_full.CLAIM_MATRIX_COLUMNS}
            row.update({
                "clave_inicial": f"C-{number:03d}",
                "severidad_inicial": "NINGUNA", "estado_inicial": "CONFORME",
                "huella_final_sha256": f"{number:x}" * 64,
            })
            claim_rows.append(row)
        write(audit_full.CLAIM_MATRIX, audit_full.CLAIM_MATRIX_COLUMNS, [
            [row[column] for column in audit_full.CLAIM_MATRIX_COLUMNS]
            for row in claim_rows
        ])
        write(audit_full.SOURCE_MATRIX, audit_full.SOURCE_MATRIX_COLUMNS, [])
        write(audit_full.REQUIREMENT_MATRIX, audit_full.REQUIREMENT_MATRIX_COLUMNS, [])
        write(audit_full.CONTENT_TRACE, audit_full.CONTENT_TRACE_COLUMNS, [])

        review_rows: list[dict[str, str]] = []
        correction_review = {column: "n/a" for column in audit_full.SECOND_REVIEW_COLUMNS}
        correction_review.update({
            "estrato": "AFIRMACION", "clave_matriz": "C-001",
            "tipo_revision": "CORRECCION_P0_P1", "seleccion": "CENSO_100_PCT",
            "resultado": "CONFORME", "revisor_independiente": "Revisor B",
            "declaracion_independencia": "INDEPENDIENTE_DEL_AUTOR_DE_LA_CORRECCION",
            "fecha": audit_full.CUTOFF, "evidencia": "Revisión literal.",
            "accion": "Sin cambio adicional.", "estado_cierre": "CERRADO",
            "huella_objeto_sha256": "a" * 64,
        })
        review_rows.append(correction_review)
        conforming_keys = {f"C-{number:03d}" for number in range(2, 9)}
        sample = sorted(audit_full.deterministic_sample(conforming_keys, "AFIRMACION"))
        for offset, key in enumerate(sample):
            number = int(key.split("-")[1])
            row = {column: "n/a" for column in audit_full.SECOND_REVIEW_COLUMNS}
            row.update({
                "estrato": "AFIRMACION", "clave_matriz": key,
                "tipo_revision": "MUESTRA_CONFORME_15",
                "seleccion": "MUESTRA_ESTRATIFICADA_15_PCT",
                "resultado": "NO_CONFORME" if offset == 0 else "CONFORME",
                "revisor_independiente": "Revisor B",
                "declaracion_independencia": "INDEPENDIENTE_DEL_AUTOR_DE_LA_CORRECCION",
                "fecha": audit_full.CUTOFF, "evidencia": "Fallo reproducido.",
                "accion": "Corregir y volver a revisar.",
                "estado_cierre": "ABIERTO" if offset == 0 else "CERRADO",
                "huella_objeto_sha256": f"{number:x}" * 64,
            })
            review_rows.append(row)
        for number, row in enumerate(review_rows, 1):
            row["id_revision"] = f"REV-{number:05d}"
        write(audit_full.SECOND_REVIEW, audit_full.SECOND_REVIEW_COLUMNS, [
            [row[column] for column in audit_full.SECOND_REVIEW_COLUMNS]
            for row in review_rows
        ])

        findings: list[audit_full.Finding] = []
        audit_full.audit_second_review(audit_full.AuditContext(root), findings)
        codes = {finding.code for finding in findings}
        self.assertIn("AF761", codes)
        self.assertIn("AF757", codes)
        self.assertNotIn("AF748", codes)
        self.assertNotIn("AF752", codes)

    def test_requirement_review_population_includes_initial_failures(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)

        def write(relative: str, header: list[str], rows: list[list[str]]) -> None:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(header)
                writer.writerows(rows)

        write(audit_full.CLAIM_MATRIX, audit_full.CLAIM_MATRIX_COLUMNS, [])
        write(audit_full.SOURCE_MATRIX, audit_full.SOURCE_MATRIX_COLUMNS, [])
        requirement = {
            column: "n/a" for column in audit_full.REQUIREMENT_MATRIX_COLUMNS
        }
        requirement.update({
            "id_requisito": "R-0001", "estado_inicial": "INCUMPLE",
        })
        write(audit_full.REQUIREMENT_MATRIX, audit_full.REQUIREMENT_MATRIX_COLUMNS, [[
            requirement[column] for column in audit_full.REQUIREMENT_MATRIX_COLUMNS
        ]])
        write(audit_full.CONTENT_TRACE, audit_full.CONTENT_TRACE_COLUMNS, [])
        write(audit_full.SECOND_REVIEW, audit_full.SECOND_REVIEW_COLUMNS, [])

        findings: list[audit_full.Finding] = []
        audit_full.audit_second_review(audit_full.AuditContext(root), findings)
        self.assertIn("AF758", {finding.code for finding in findings})


if __name__ == "__main__":
    unittest.main()
