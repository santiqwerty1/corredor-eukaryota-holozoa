from __future__ import annotations

import unittest

from scripts import remediate_trace_residuals as module


class TraceResidualRemediationTests(unittest.TestCase):
    def test_nominal_query_has_three_real_components(self) -> None:
        query = (
            "identidad=«Hedgehog»; campo=«Metazoa»; valor=«presente»"
        )
        self.assertEqual(
            module.nominal_components(query),
            ["hedgehog", "metazoa", "presente"],
        )

    def test_gap_never_promotes_zero_hits_to_scientific_absence(self) -> None:
        value = module.gap_value("BN-147")
        self.assertIn("no se adjudica un valor", value)
        self.assertNotIn("carece", value.casefold())
        self.assertNotIn("ausente", value.casefold())

    def test_known_positive_cells_cannot_be_materialized_as_negative(self) -> None:
        self.assertEqual(module.POSITIVE_CLAIMS, {"C-2472", "C-2489"})


if __name__ == "__main__":
    unittest.main()
