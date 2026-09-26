from __future__ import annotations

import csv
import io
import tempfile
import unittest
from pathlib import Path

from scripts import build_claim_provenance as builder


CLAIM_HEADER = [
    "#", "Afirmación", "Sujeto", "Predicado", "Objeto", "Atribución",
    "Fuente", "Aceptación", "Fuerza", "Motivo", "Resolución", "Vigencia",
]


class ClaimProvenanceTests(unittest.TestCase):
    def _root(self, claims: list[list[str]], appendix_sources: tuple[str, ...] = ("S01",)) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "data/afirmaciones").mkdir(parents=True)
        (root / "data/apendices").mkdir(parents=True)
        (root / "docs/auditorias").mkdir(parents=True)
        (root / "fuentes").mkdir()
        with (root / "data/afirmaciones/00.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(CLAIM_HEADER)
            writer.writerows(claims)
        with (root / "data/apendices/A_fuentes.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["clave"])
            writer.writerows([[source] for source in appendix_sources])
        with (root / "docs/auditorias/matriz_fuentes_2026-08-08.csv").open(
            "w", encoding="utf-8", newline="",
        ) as handle:
            writer = csv.writer(handle)
            writer.writerow(["clave_final", "acceso"])
            writer.writerow(["S01", "METADATOS; PASAJE NO COTEJADO"])
        return root

    @staticmethod
    def _claim(cid: str, **changes: str) -> list[str]:
        row = dict.fromkeys(CLAIM_HEADER, "n/a")
        row.update({
            "#": cid,
            "Afirmación": "Afirmación de control",
            "Sujeto": "sujeto",
            "Predicado": "posee_rasgo",
            "Objeto": "objeto",
            "Atribución": "glosa",
            "Aceptación": "no evaluado",
            "Fuerza": "alta",
            "Motivo": "Control estructural de prueba.",
            "Resolución": "resuelta",
            "Vigencia": "vigente",
        })
        row.update(changes)
        return [row[column] for column in CLAIM_HEADER]

    def test_dependencies_are_collected_from_every_claim_field(self) -> None:
        references = self._claim(
            "C-002",
            Afirmación="Remite a C-001.",
            Sujeto="sujeto de C-003",
            Objeto="objeto de C-004",
            Atribución="sintesis(C-005)",
            Fuente="S01 Results; C-006",
            Motivo="Separado de C-007.",
        )
        claims = [self._claim(f"C-{number:03d}") for number in (1, 3, 4, 5, 6, 7)]
        root = self._root([*claims, references])
        rows = list(csv.DictReader(io.StringIO(builder.build(root).decode("utf-8"))))
        row = next(item for item in rows if item["id_afirmacion"] == "C-002")
        self.assertEqual(
            row["dependencias_declaradas"],
            "C-001; C-003; C-004; C-005; C-006; C-007",
        )

    def test_source_absent_from_appendix_a_is_fatal(self) -> None:
        root = self._root([
            self._claim("C-001", Atribución="expresa", Fuente="S02 Results"),
        ])
        with self.assertRaisesRegex(RuntimeError, "ausentes de A.*S02"):
            builder.build(root)

    def test_access_or_artifact_census_never_claims_semantic_verification(self) -> None:
        root = self._root([
            self._claim("C-001", Atribución="expresa", Fuente="S01 Results"),
        ])
        rows = list(csv.DictReader(io.StringIO(builder.build(root).decode("utf-8"))))
        self.assertIn("no sustituye cotejo semántico", rows[0]["alcance_del_censo"])


if __name__ == "__main__":
    unittest.main()
