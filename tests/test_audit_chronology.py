from __future__ import annotations

import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import audit_chronology as chronology
from scripts import audit_full, build_audit_deliverables as builder


def write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


class ChronologyTests(unittest.TestCase):
    def test_calendar_is_strict_at_both_precisions(self) -> None:
        for value in ("2026-09-26", "2026-09-26T21:00:00Z", "2024-02-29"):
            self.assertIsNotNone(chronology.parse_date(value), value)
        for value in ("2026-02-29", "2026-09-31", "20260926", "2026-W39-6", "2026-9-26", "2026-09-26T24:00:00Z", "2026-09-26T21:00:00+00:00", "2026-09-26 "):
            self.assertIsNone(chronology.parse_date(value), value)

    def test_day_does_not_claim_order_within_a_day(self) -> None:
        bound = ("2026-09-26T21:00:00Z",)
        self.assertTrue(chronology.review_date_errors("2026-09-26", bound))
        self.assertTrue(chronology.review_date_errors("2026-09-26T20:59:59Z", bound))
        self.assertFalse(chronology.review_date_errors("2026-09-26T21:00:00Z", bound))
        self.assertFalse(chronology.review_date_errors("2026-09-27", bound))

    def test_declared_future_date_is_not_authenticated_by_calendar(self) -> None:
        # Deliberadamente sin reloj: esto solo afirma coherencia del calendario.
        self.assertFalse(chronology.review_date_errors("2099-01-01"))
        self.assertTrue(chronology.review_date_errors("2099-01-01", ("2099-01-02",)))

    def test_start_date_is_not_misused_as_signature_date(self) -> None:
        self.assertTrue(chronology.review_date_errors("2026-08-12"))
        self.assertFalse(chronology.review_date_errors("2026-09-26"))

    def object_row(self, root: Path) -> dict[str, str]:
        evidence = root / "inspection.md"
        evidence.write_text("Observación de fixture, no firma real.\n", encoding="utf-8")
        return {
            "estrato": "AFIRMACION", "clave_objeto": "C-001",
            "huella_objeto_sha256": "a" * 64,
            "fecha_version": "2026-09-26T20:00:00Z",
            "evidencia_local": "inspection.md",
            "huella_evidencia_sha256": hashlib.sha256(evidence.read_bytes()).hexdigest(),
            "localizador_evidencia": "línea 1",
        }

    def test_metadata_is_bound_to_object_version_and_local_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row = self.object_row(root)
            write_csv(root / chronology.OBJECT_DATES, chronology.OBJECT_HEADER, [row])
            registry = chronology.load_object_dates(root)
            self.assertFalse(registry.errors)
            self.assertEqual(registry.object_date("AFIRMACION", "C-001", "a" * 64), (row["fecha_version"],))
            self.assertEqual(registry.object_date("AFIRMACION", "C-001", "b" * 64), ())
            (root / "inspection.md").write_text("mutación", encoding="utf-8")
            registry = chronology.load_object_dates(root)
            self.assertTrue(registry.errors)
            self.assertEqual(registry.rows, {})

    def test_duplicates_external_paths_and_derived_dates_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row = self.object_row(root)
            for rows in (
                [row, row],
                [{**row, "evidencia_local": "../outside"}],
                [{**row, "evidencia_local": "docs/auditorias/matriz_fuentes_2026-08-08.csv"}],
                [{**row, "fecha_version": "2026-02-30"}],
            ):
                write_csv(root / chronology.OBJECT_DATES, chronology.OBJECT_HEADER, rows)
                registry = chronology.load_object_dates(root)
                self.assertTrue(registry.errors)
                self.assertFalse(registry.rows)


class SearchChronologyTests(unittest.TestCase):
    def bn(self) -> dict[str, str]:
        return {"clave": "BN-557", "hueco": "hueco de fixture", "términos exactos": "consulta literal", "resultado": "resultado negativo acotado"}

    def build(self, root: Path, bn: dict[str, str]) -> list[dict[str, str]]:
        with mock.patch.object(builder, "FROZEN_SEARCH_COUNT", 0), mock.patch.object(builder, "ADDITIONAL_SEARCHES", []):
            return builder.build_search_matrix([], {bn["clave"]}, {}, {bn["clave"]: bn}, {}, root=root)

    def test_new_search_without_evidence_is_not_backdated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            row = self.build(Path(directory), self.bn())[0]
            self.assertEqual(row["fecha"], chronology.UNKNOWN_DATE)
            self.assertIn("falta ejecución fechada", row["evidencia_final"])

    def test_reinspection_date_is_not_original_date_and_is_version_bound(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "run.md"
            evidence.write_text("Observación de fixture", encoding="utf-8")
            bn = self.bn()
            dated = {
                "clave_bn": bn["clave"], "huella_fila_bn_sha256": builder.row_fingerprint(bn),
                "clase_fecha": "REINSPECCION", "fecha_ejecucion": "2026-09-26T21:00:00Z",
                "evidencia_local": "run.md", "huella_evidencia_sha256": hashlib.sha256(evidence.read_bytes()).hexdigest(),
                "localizador_evidencia": "línea 1",
            }
            write_csv(root / chronology.SEARCH_DATES, chronology.SEARCH_HEADER, [dated])
            built = self.build(root, bn)[0]
            self.assertEqual(built["fecha"], dated["fecha_ejecucion"])
            self.assertIn("no acredita la fecha original", built["evidencia_final"])
            self.assertEqual(self.build(root, {**bn, "resultado": "otro resultado"})[0]["fecha"], chronology.UNKNOWN_DATE)

    def test_the_165_historical_dates_and_fingerprints_are_unchanged(self) -> None:
        frozen = builder.load_and_validate_reconstructed(builder.ROOT / builder.DEFAULT_RECONSTRUCTED_INPUTS)
        history = {
            row["clave_original"]: {"desencadenante": "fixture", "delta_auditoria_2026_08_08": "fixture"}
            for row in frozen["history"]
        }
        with tempfile.TemporaryDirectory() as directory:
            rows = builder.build_search_matrix(frozen["searches"], set(), history, {}, {}, root=Path(directory))
        self.assertEqual([row["fecha"] for row in rows[:165]], [row["fecha"] for row in frozen["searches"]])
        items = [(row["id_busqueda"], row["huella_inicial_sha256"]) for row in rows[:165]]
        self.assertEqual(audit_full.aggregate_keyed_fingerprints(items), audit_full.BASELINE_SEARCH_AUDIT_SHA256)

    def test_historical_bn_reinspection_gets_separate_q_without_rewriting_frozen_date(self) -> None:
        frozen = builder.load_and_validate_reconstructed(builder.ROOT / builder.DEFAULT_RECONSTRUCTED_INPUTS)
        history = {
            row["clave_original"]: {
                "desencadenante": "fixture", "delta_auditoria_2026_08_08": "fixture",
                "prioridad_final": "P1",
            } for row in frozen["history"]
        }
        bn = {**self.bn(), "clave": "BN-025"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "reinspection.md"
            evidence.write_text("Registro de reinspección de fixture.", encoding="utf-8")
            dated = {
                "clave_bn": "BN-025", "huella_fila_bn_sha256": builder.row_fingerprint(bn),
                "clase_fecha": "REINSPECCION", "fecha_ejecucion": "2026-09-26T21:00:00Z",
                "evidencia_local": "reinspection.md", "huella_evidencia_sha256": hashlib.sha256(evidence.read_bytes()).hexdigest(),
                "localizador_evidencia": "línea 1",
            }
            write_csv(root / chronology.SEARCH_DATES, chronology.SEARCH_HEADER, [dated])
            rows = builder.build_search_matrix(frozen["searches"], {"BN-025"}, history, {"BN-025": bn}, {}, root=root)
            original = [row for row in rows[:165] if row["clave_bn"] == "BN-025"]
            later = [row for row in rows[165:] if row["clave_bn"] == "BN-025"]
            self.assertEqual(len(original), 1)
            self.assertEqual(len(later), 1)
            self.assertEqual(original[0]["fecha"], "2026-08-08")
            self.assertEqual(later[0]["fecha"], dated["fecha_ejecucion"])
            self.assertEqual(later[0]["cambio_realizado"], "REINSPECCION_DOCUMENTADA")
            write_csv(root / audit_full.SEARCH_MATRIX, builder.SEARCH_MATRIX_COLUMNS, rows)
            write_csv(root / audit_full.NEGATIVE_HISTORY, ["clave_original", "prioridad_final"], [
                {"clave_original": key, "prioridad_final": row["prioridad_final"]} for key, row in history.items()
            ])
            bn_relative = "data/negative.csv"
            write_csv(root / bn_relative, list(bn), [bn])
            (root / "data/table_index.json").write_text(json.dumps({"tables": [{"category": "negative", "csv_path": bn_relative}]}), encoding="utf-8")
            findings = []
            audit_full.audit_searches(audit_full.AuditContext(root), findings)
            self.assertNotIn("AF613", {finding.code for finding in findings})
            self.assertNotIn("AF628", {finding.code for finding in findings})
            later[0]["fecha"] = "2026-08-13"
            write_csv(root / audit_full.SEARCH_MATRIX, builder.SEARCH_MATRIX_COLUMNS, rows)
            findings = []
            audit_full.audit_searches(audit_full.AuditContext(root), findings)
            self.assertIn("AF613", {finding.code for finding in findings})
            dated["fecha_ejecucion"] = "2026-08-07"
            write_csv(root / chronology.SEARCH_DATES, chronology.SEARCH_HEADER, [dated])
            with self.assertRaisesRegex(builder.BuildError, "incompatible con Q original"):
                builder.build_search_matrix(frozen["searches"], {"BN-025"}, history, {"BN-025": bn}, {}, root=root)
            later[0]["fecha"] = dated["fecha_ejecucion"]
            write_csv(root / audit_full.SEARCH_MATRIX, builder.SEARCH_MATRIX_COLUMNS, rows)
            findings = []
            audit_full.audit_searches(audit_full.AuditContext(root), findings)
            self.assertTrue(any(finding.code == "AF613" and "Q original" in finding.message for finding in findings))


class BuilderTemporalIntegrationTests(unittest.TestCase):
    def test_new_source_dates_are_not_copied_from_cutoff(self) -> None:
        frozen = builder.load_and_validate_reconstructed(builder.ROOT / builder.DEFAULT_RECONSTRUCTED_INPUTS)
        claims, _ = builder.load_claims(builder.ROOT)
        with mock.patch.object(builder, "load_object_dates", return_value=chronology.DateRegistry({}, [])):
            rows = builder.build_source_matrix(
                frozen["sources"], builder.ROOT, claims,
                builder.ROOT / builder.DEFAULT_RECONSTRUCTED_INPUTS / "fuentes_retiradas.csv",
            )
        new = [row for row in rows if row["clave_inicial"].startswith("NUEVA:")]
        self.assertTrue(new)
        self.assertEqual({row["fecha_verificacion"] for row in new}, {chronology.UNKNOWN_DATE})
        self.assertEqual({row["estado_hallazgo"] for row in new}, {"ABIERTO"})
        # Una fecha histórica pertenece a su versión; no verifica la S viva.
        live = [row for row in rows if row["clave_final"] != "NO_APLICA"]
        self.assertEqual({row["fecha_verificacion"] for row in live}, {chronology.UNKNOWN_DATE})

    def test_second_review_cannot_precede_the_version_or_manual_signature(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = root / audit_full.CONTENT_TRACE
            write_csv(trace, audit_full.CONTENT_TRACE_COLUMNS, [])
            claims = [{
                **dict.fromkeys(builder.CLAIM_MATRIX_COLUMNS, "n/a"),
                "clave_inicial": "C-001", "severidad_inicial": "P0",
                "estado_inicial": "CORREGIR", "huella_final_sha256": "a" * 64,
                "estado_hallazgo": "CERRADO",
            }]
            requirements = [
                {**dict.fromkeys(builder.REQUIREMENT_MATRIX_COLUMNS, "n/a"), "id_requisito": f"R-{number:04d}"}
                for number in range(1, 484)
            ]
            rows = builder.build_second_review(claims, [], requirements, trace, None, root=root)
            for row in rows:
                row.update({
                    "resultado": "CONFORME", "revisor_independiente": "Fixture-independent-reviewer",
                    "declaracion_independencia": "INDEPENDIENTE_DEL_AUTOR_DE_LA_CORRECCION",
                    "fecha": "2026-09-26T21:00:00Z", "evidencia": "Fixture probatoria, no revisión real.",
                    "accion": "Sin cambio", "estado_cierre": "CERRADO",
                })
                if row["estrato"] == "AFIRMACION":
                    row["evidencia"] += " expediente_sha256=" + builder.row_fingerprint(claims[0])
            signed = root / audit_full.SECOND_REVIEW
            write_csv(signed, builder.SECOND_REVIEW_COLUMNS, rows)
            preserved = builder.build_second_review(claims, [], requirements, trace, signed, root=root)
            self.assertTrue(all(row["resultado"] == "CONFORME" for row in preserved))
            metadata = ChronologyTests().object_row(root)
            metadata["fecha_version"] = "2026-09-26T22:00:00Z"
            write_csv(root / chronology.OBJECT_DATES, chronology.OBJECT_HEADER, [metadata])
            write_csv(root / chronology.MANUAL_LEDGER, ["id_requisito", "fecha_revision"], [
                {"id_requisito": "R-0001", "fecha_revision": "2026-09-27T00:00:00Z"},
            ])
            rebuilt = builder.build_second_review(claims, [], requirements, trace, signed, root=root)
            pending = {row["clave_matriz"] for row in rebuilt if row["resultado"] == "PENDIENTE"}
            self.assertEqual(pending, {"C-001", "R-0001"})

            write_csv(root / audit_full.CLAIM_MATRIX, builder.CLAIM_MATRIX_COLUMNS, claims)
            write_csv(root / audit_full.SOURCE_MATRIX, builder.SOURCE_MATRIX_COLUMNS, [])
            write_csv(root / audit_full.REQUIREMENT_MATRIX, builder.REQUIREMENT_MATRIX_COLUMNS, requirements)
            findings = []
            audit_full.audit_second_review(audit_full.AuditContext(root), findings)
            errors = {finding.key for finding in findings if finding.code == "AF751"}
            self.assertEqual(errors, {"C-001", "R-0001"})


if __name__ == "__main__":
    unittest.main()
