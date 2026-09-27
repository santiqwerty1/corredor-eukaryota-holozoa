"""Regresión del hueco S180 dentro de la antigua cita de BN-117."""

import unittest
from unittest.mock import patch

from scripts import corpus_io

with patch.dict("sys.modules", {"corpus_io": corpus_io}):
    from scripts import validate


class ValidateSourceRangesTests(unittest.TestCase):
    def test_missing_interior_source_fails(self):
        valid = {"S177", "S178", "S179", "S181"}
        for separator in ("–", "-"):
            with self.subTest(separator=separator):
                self.assertEqual(
                    validate.source_reference_errors(f"S177{separator}S181", valid),
                    ["Referencias S indefinidas: ['S180']"],
                )

    def test_corrected_split_range_passes(self):
        self.assertEqual(validate.source_reference_errors(
            "S177–S179; S181", {"S177", "S178", "S179", "S181"},
        ), [])

    def test_abbreviated_range_cannot_hide_a_missing_interior(self):
        self.assertEqual(validate.source_reference_errors(
            "S177–181", {"S177", "S181"},
        ), ["Referencias S indefinidas: ['S178', 'S179', 'S180']"])

    def test_literal_missing_key_still_fails(self):
        self.assertEqual(validate.source_reference_errors("S180", set()),
                         ["Referencias S indefinidas: ['S180']"])

    def test_supplementary_label_does_not_expand_as_bibliography(self):
        self.assertEqual(validate.source_reference_errors(
            "S01 figs. S62–S64", {"S01", "S62", "S64"},
        ), [])

    def test_descending_range_fails_even_when_endpoints_exist(self):
        errors = validate.source_reference_errors("S181–S177", {"S177", "S181"})
        self.assertEqual(errors, ["Referencias S inválidas: Rango S descendente: S181–S177"])


if __name__ == "__main__":
    unittest.main()
