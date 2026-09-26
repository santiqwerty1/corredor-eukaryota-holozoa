from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

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

    def test_full_ledger_shaped_dictamen_is_reduced_to_signed_fields(self) -> None:
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
        self.assertEqual(set(rows[0]), set(assembler.REVIEW_COLUMNS))
        self.assertEqual(rows[0]["resultado"], "CONFORME")

    def test_final_review_may_close_a_previous_nonconformity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            paths = []
            for name, result in (("first.csv", "NO_CONFORME"), ("second.csv", "CONFORME")):
                path = Path(directory) / name
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=assembler.REVIEW_COLUMNS)
                    writer.writeheader()
                    writer.writerow({
                        "id_requisito": "R-0008",
                        "resultado": result,
                        "prueba_nominal": f"prueba independiente de {name}",
                        "evidencia": f"evidencia independiente de {name}",
                        "localizadores_evidencia": "C-001",
                        "revisor": "Codex-Revisor-A",
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
                    writer = csv.DictWriter(handle, fieldnames=assembler.REVIEW_COLUMNS)
                    writer.writeheader()
                    writer.writerow({
                        "id_requisito": "R-0008",
                        "resultado": "CONFORME",
                        "prueba_nominal": f"prueba independiente de {name}",
                        "evidencia": f"evidencia independiente de {name}",
                        "localizadores_evidencia": "C-001",
                        "revisor": "Codex-Revisor-A",
                    })
                paths.append(path)
            _, errors = assembler.select_final_reviews(paths)
        self.assertEqual(len(errors), 1)
        self.assertIn("CONFORME previo", errors[0])


if __name__ == "__main__":
    unittest.main()
