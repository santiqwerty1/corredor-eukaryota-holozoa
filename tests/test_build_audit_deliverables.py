from __future__ import annotations

import unittest

from scripts import build_audit_deliverables as builder


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
        self.assertIn("sin corrección, retractación ni alerta", status)
        self.assertIn("no sustituye", status)


if __name__ == "__main__":
    unittest.main()
