import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import fetch_oa


class SourceImpactTests(unittest.TestCase):
    def counts(self, sources):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "exports").mkdir()
            with (root / "exports/afirmaciones.csv").open("w", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["#", "Afirmación", "Sujeto", "Predicado", "Objeto", "Atribución", "Fuente"])
                for number, source in enumerate(sources):
                    writer.writerow([f"C-{number:03d}", "", "", "", "", "expresa", source])
            with patch.object(fetch_oa, "ROOT", root):
                return fetch_oa.impacto_por_fuente()

    def test_expands_ranges_and_counts_each_source_once_per_claim(self):
        uses, sole = self.counts(["S177–S181 resultados; S180 discusión", "S180 resumen"])
        self.assertEqual(uses, {"S177": 1, "S178": 1, "S179": 1, "S180": 2, "S181": 1})
        self.assertEqual(sole, {"S180": 1})

    def test_short_range_and_supplement_label_are_not_confused(self):
        uses, sole = self.counts(["S126 supl. fig. S3", "S177–179 métodos"])
        self.assertEqual(uses, {"S126": 1, "S177": 1, "S178": 1, "S179": 1})
        self.assertEqual(sole, {"S126": 1})

    def test_negative_and_editorial_entries_do_not_create_source_uses(self):
        self.assertEqual(self.counts(["BN-083", "n/a; recuento canónico"]), ({}, {}))

    def test_report_writer_uses_lf_without_changing_cells(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "exports/access.csv"
            row = ["S01", "1964", "Título, con coma"] + [""] * 12
            with patch.object(fetch_oa, "INFORME", report), patch.object(fetch_oa, "escribir_listado"):
                fetch_oa.volcar([row], [])
            self.assertNotIn(b"\r\n", report.read_bytes())
            with report.open(encoding="utf-8", newline="") as handle:
                self.assertEqual(list(csv.reader(handle)), [fetch_oa.CABECERA_INFORME, row])


if __name__ == "__main__":
    unittest.main()
