from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import audit_semantics  # noqa: E402


class NegativeCountAuditTests(unittest.TestCase):
    def test_count_can_coexist_with_another_claim_for_same_subject(self) -> None:
        claims = {
            "C-001": {
                "Sujeto": "registro canónico de búsquedas negativas",
                "Objeto": "1 fila etiquetada",
            },
            "C-002": {
                "Sujeto": "registro canónico de búsquedas negativas",
                "Objeto": "trazabilidad de consulta",
            },
            "C-003": {
                "Sujeto": "búsquedas negativas con ausencia declarada",
                "Objeto": "1 fila",
            },
            "C-004": {
                "Sujeto": "búsquedas negativas sin resultado localizado",
                "Objeto": "0 filas",
            },
            "C-005": {
                "Sujeto": "búsquedas negativas no buscadas",
                "Objeto": "0 filas",
            },
        }
        with (
            mock.patch.object(audit_semantics, "load_index", return_value={}),
            mock.patch.object(
                audit_semantics, "negative_entries", return_value=[{"csv_path": "negative.csv"}],
            ),
            mock.patch.object(
                audit_semantics,
                "read_csv",
                return_value=(
                    ["clave", "estado"],
                    [["BN-001", "LA LITERATURA DECLARA QUE NO SE SABE"]],
                ),
            ),
        ):
            errors: list[str] = []
            audit_semantics.audit_negative_counts(errors, claims)
        self.assertEqual(errors, [])


class NarrativeAttributionTests(unittest.TestCase):
    def test_explicit_label_must_match_live_claim_attribution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sections = root / "docs/secciones"
            sections.mkdir(parents=True)
            (sections / "010-test.md").write_text(
                "Texto. [C-001; S01 Results; expresa]\n", encoding="utf-8",
            )
            errors: list[str] = []
            with mock.patch.object(audit_semantics, "ROOT", root):
                audit_semantics.audit_narrative_attribution_labels(
                    errors,
                    {"C-001": {"Atribución": "glosa"}},
                )
            self.assertEqual(len(errors), 1)
            self.assertIn("no coincide", errors[0])

    def test_synthesis_label_matches_live_synthesis_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sections = root / "docs/secciones"
            sections.mkdir(parents=True)
            (sections / "010-test.md").write_text(
                "Texto. [C-002; S01 Results; síntesis]\n", encoding="utf-8",
            )
            errors: list[str] = []
            with mock.patch.object(audit_semantics, "ROOT", root):
                audit_semantics.audit_narrative_attribution_labels(
                    errors,
                    {"C-002": {"Atribución": "sintesis(C-001)"}},
                )
            self.assertEqual(errors, [])

    def test_unaccented_synthesis_label_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sections = root / "docs/secciones"
            sections.mkdir(parents=True)
            (sections / "010-test.md").write_text(
                "Texto. [C-002; S01 Results; sintesis]\n", encoding="utf-8",
            )
            errors: list[str] = []
            with mock.patch.object(audit_semantics, "ROOT", root):
                audit_semantics.audit_narrative_attribution_labels(
                    errors,
                    {"C-002": {"Atribución": "sintesis(C-001)"}},
                )
            self.assertEqual(len(errors), 1)
            self.assertIn("no canónico", errors[0])


class AttributionContractTests(unittest.TestCase):
    def test_glosa_cannot_keep_bibliographic_source(self) -> None:
        errors: list[str] = []
        audit_semantics.audit_glosa_source_contract(
            errors,
            [{"#": "C-001", "Atribución": "glosa", "Fuente": "S01 Results"}],
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("Glosa con fuente bibliográfica S", errors[0])

    def test_glosa_may_keep_bounded_operational_reference(self) -> None:
        errors: list[str] = []
        audit_semantics.audit_glosa_source_contract(
            errors,
            [{"#": "C-001", "Atribución": "glosa", "Fuente": "BN-001; Q-0001"}],
        )
        self.assertEqual(errors, [])

    def test_expressa_may_use_honest_unlocated_marker(self) -> None:
        errors: list[str] = []
        audit_semantics.audit_all_localizers(
            errors,
            [{"#": "C-001", "Atribución": "expresa", "Fuente": "S01 sin localizar"}],
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
