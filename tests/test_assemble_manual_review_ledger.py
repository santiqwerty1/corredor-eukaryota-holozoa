from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import assemble_manual_review_ledger as assembler


class ManualReviewInputTests(unittest.TestCase):
    def test_review_payload_is_read_without_promoting_the_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=assembler.REVIEW_COLUMNS)
                writer.writeheader()
                writer.writerow({
                    "id_requisito": "R-0008",
                    "resultado": "NO_CONFORME",
                    "prueba_nominal": "prueba humana nominal y específica",
                    "evidencia": "evidencia independiente conservada literalmente",
                    "localizadores_evidencia": "C-001",
                    "revisor": "Codex-Revisor-A",
                })
            rows = assembler.read_reviews(path)
        self.assertEqual(rows[0]["resultado"], "NO_CONFORME")

    def test_review_payload_rejects_a_weakened_header(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review.csv"
            path.write_text("id_requisito,resultado\nR-0008,CONFORME\n", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                assembler.read_reviews(path)

    def test_full_ledger_preserves_every_signed_field(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=assembler.controls.MANUAL_LEDGER_HEADER,
                )
                writer.writeheader()
                row = {
                    column: "PENDIENTE_FIRMA"
                    for column in assembler.controls.MANUAL_LEDGER_HEADER
                }
                row.update({
                    "id_requisito": "R-0008",
                    "resultado": "CONFORME",
                    "prueba_nominal": "prueba nominal suficientemente larga",
                    "evidencia": "evidencia independiente suficientemente larga",
                    "localizadores_evidencia": "C-001",
                    "revisor": "Codex-Revisor-A",
                })
                writer.writerow(row)
            rows = assembler.read_reviews(path)
        self.assertEqual(rows[0], row)

    def test_final_review_may_close_a_previous_nonconformity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            paths = []
            for name, result in (("first.csv", "NO_CONFORME"), ("second.csv", "CONFORME")):
                path = Path(directory) / name
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=assembler.controls.MANUAL_LEDGER_HEADER)
                    writer.writeheader()
                    writer.writerow({
                        "id_requisito": "R-0008",
                        "resultado": result,
                        "prueba_nominal": f"prueba independiente de {name}",
                        "evidencia": f"evidencia independiente de {name}",
                        "localizadores_evidencia": "C-001",
                        "revisor": "Codex-Revisor-A",
                        "fecha_revision": "2026-09-26T20:00:00Z",
                    })
                paths.append(path)
            selected, errors = assembler.select_final_reviews(paths)
        self.assertEqual(errors, [])
        self.assertEqual(selected["R-0008"]["resultado"], "CONFORME")

    def test_a_closed_review_cannot_be_silently_replaced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            paths = []
            for name in ("first.csv", "second.csv"):
                path = Path(directory) / name
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=assembler.controls.MANUAL_LEDGER_HEADER)
                    writer.writeheader()
                    writer.writerow({
                        "id_requisito": "R-0008",
                        "resultado": "CONFORME",
                        "prueba_nominal": f"prueba independiente de {name}",
                        "evidencia": f"evidencia independiente de {name}",
                        "localizadores_evidencia": "C-001",
                        "revisor": "Codex-Revisor-A",
                        "fecha_revision": "2026-09-26T20:00:00Z",
                    })
                paths.append(path)
            _, errors = assembler.select_final_reviews(paths)
        self.assertEqual(len(errors), 1)
        self.assertIn("CONFORME previo", errors[0])

    def test_six_column_conforming_attestation_cannot_close(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "short.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=assembler.REVIEW_COLUMNS)
                writer.writeheader()
                writer.writerow({**dict.fromkeys(assembler.REVIEW_COLUMNS, "test"), "resultado": "CONFORME"})
            with self.assertRaisesRegex(RuntimeError, "seis columnas"):
                assembler.read_reviews(path)

    def test_excess_fields_are_not_dropped_before_cardinality_check(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.csv"
            path.write_text(
                ",".join(assembler.REVIEW_COLUMNS) + "\nR-0008,NO_CONFORME,p,e,l,r,extra\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RuntimeError, "cardinalidad"):
                assembler.read_reviews(path)


class SignedLedgerAssemblyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.corpus = assembler.controls.Corpus(cls.root)
        _, rows = assembler.controls.load_control_rows(cls.root)
        cls.disposition = next(row for row in rows if row["id_requisito"] == "R-0052")
        cls.result = assembler.controls.evaluate(cls.corpus, cls.disposition)
        cls.literals = assembler.controls.load_requirement_literals(cls.root)

    def signed_row(self) -> dict[str, str]:
        row = assembler.controls.manual_template_row(self.corpus, self.result, self.literals["R-0052"])
        row.update({
            "prueba_nominal": "Se inspeccionó el literal y cada destino del alcance para este test de preservación de firmas.",
            "resultado": "CONFORME",
            "evidencia": "Fixture de prueba con firma independiente y huellas explícitas que no pueden recalcularse.",
            "localizadores_evidencia": "data/table_index.json",
            "revisor": "Fixture-Revisor-independiente",
            "declaracion_independencia": assembler.controls.INDEPENDENCE_DECLARATION,
            "fecha_revision": "2026-09-26T20:00:00Z",
        })
        return row

    def assemble_row(self, row: dict[str, str]) -> bytes:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "signed.csv"
            path.write_bytes(assembler.csv_payload([row]))
            with mock.patch.object(assembler.controls, "load_control_rows", return_value=([], [self.disposition])):
                return assembler.assemble(self.root, [path])

    def test_assembly_keeps_date_identity_and_all_hashes_byte_for_byte(self) -> None:
        row = self.signed_row()
        self.assertEqual(self.assemble_row(row), assembler.csv_payload([row]))

    def test_old_signature_cannot_be_rebound_to_live_scope(self) -> None:
        row = self.signed_row()
        row["huella_alcance_sha256"] = "0" * 64
        with self.assertRaisesRegex(RuntimeError, "alcance live desactualizada"):
            self.assemble_row(row)

    def test_unsigned_independence_and_date_are_never_filled_by_assembler(self) -> None:
        for field in ("fecha_revision", "declaracion_independencia", "huella_literal_sha256"):
            row = self.signed_row()
            row[field] = ""
            with self.assertRaises(RuntimeError, msg=field):
                self.assemble_row(row)

    def test_chronological_file_order_does_not_override_signed_dates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = self.signed_row()
            first["resultado"] = "NO_CONFORME"
            second = self.signed_row()
            second["fecha_revision"] = "2026-09-25T20:00:00Z"
            paths = [Path(directory) / name for name in ("first.csv", "second.csv")]
            for path, row in zip(paths, (first, second)):
                path.write_bytes(assembler.csv_payload([row]))
            _, errors = assembler.select_final_reviews(paths)
            self.assertTrue(any("historial temporal" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
