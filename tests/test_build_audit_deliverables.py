from __future__ import annotations

import unittest

from scripts import build_audit_deliverables as builder
from scripts import audit_full


class SourceEditorialStatusTests(unittest.TestCase):
    def test_final_editorial_status_preserves_verified_correction(self) -> None:
        row = {
            "notas de calidad": (
                "Metadatos verificados. La corrección de 2011, "
                "https://doi.org/10.1083/jcb.2010111521952c, sustituyó la "
                "figura 3; las conclusiones no cambiaron."
            ),
        }
        status = builder.final_editorial_status(row)
        self.assertIn("corrección de 2011", status)
        self.assertIn("10.1083/jcb.2010111521952c", status)

    def test_final_editorial_status_does_not_invent_a_search(self) -> None:
        status = builder.final_editorial_status({
            "notas de calidad": "Identidad y pasaje verificados.",
        })
        self.assertIn("no documenta una búsqueda negativa ni su fecha", status)
        self.assertNotIn("2026-08-08", status)
        self.assertIn("no sustituye", status)


class ReconstructedInputTests(unittest.TestCase):
    def test_reconstructed_inputs_reproduce_frozen_aggregates(self) -> None:
        inputs = builder.load_and_validate_reconstructed(
            builder.ROOT / builder.DEFAULT_RECONSTRUCTED_INPUTS
        )
        self.assertEqual(len(inputs["claims"]), 1840)
        self.assertEqual(len(inputs["sources"]), 525)
        self.assertEqual(len(inputs["requirements"]), 483)
        self.assertEqual(len(inputs["searches"]), 165)

    def test_second_review_accepts_declared_later_dates_not_a_fixed_day(self) -> None:
        self.assertTrue(builder.valid_review_date("2026-08-13"))
        self.assertTrue(builder.valid_review_date("2026-09-26T20:00:00Z"))
        self.assertTrue(builder.valid_review_date("2026-08-14"))
        self.assertFalse(builder.valid_review_date("2026-08-08"))
        self.assertFalse(builder.valid_review_date("2026-09-31"))
        self.assertFalse(builder.valid_review_date("20260813"))
        self.assertFalse(builder.valid_review_date("2026-08-13", ("2026-09-26",)))


class VerifiedControlResultTests(unittest.TestCase):
    def test_automated_and_manual_evidence_are_explicitly_accepted(self) -> None:
        self.assertEqual(
            builder.VERIFIED_CONTROL_RESULTS,
            {"CERO_FALLOS", "CONFORME_REVISION_MANUAL"},
        )

    def test_pending_or_failed_results_are_never_accepted(self) -> None:
        for result in ("", "PENDIENTE", "NO_CONFORME"):
            self.assertNotIn(result, builder.VERIFIED_CONTROL_RESULTS)


class RequirementSecondReviewContractTests(unittest.TestCase):
    def test_builder_and_auditor_share_the_full_census_type(self) -> None:
        self.assertEqual(
            builder.REQUIREMENT_REVIEW_TYPE,
            audit_full.REQUIREMENT_REVIEW_TYPE,
        )
        self.assertEqual(
            builder.REQUIREMENT_REVIEW_TYPE,
            "CENSO_REQUISITO_100_PCT",
        )


if __name__ == "__main__":
    unittest.main()
