from __future__ import annotations

import csv
import io
import tempfile
import unittest
from pathlib import Path

from scripts import build_magnitude_census as builder


CLAIM_HEADER = [
    "#", "Afirmación", "Sujeto", "Predicado", "Objeto", "Atribución",
    "Fuente", "Aceptación", "Fuerza", "Motivo", "Resolución", "Vigencia",
]
F_HEADER = [
    "magnitud", "valor tal como lo publica la fuente", "unidad original",
    "organismo, nodo o intervalo al que se aplica", "método o proxy",
    "incertidumbre publicada", "observado o inferido", "fuente con localizador", "#",
]


class MagnitudeCensusTests(unittest.TestCase):
    def _root(
        self,
        magnitude_rows: list[list[str]],
        appendix_sources: tuple[str, ...] = ("S01",),
    ) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "data/afirmaciones").mkdir(parents=True)
        (root / "data/apendices").mkdir(parents=True)
        claims = [
            ["C-001", "dato", "s", "tiene_valor_medido", "o", "expresa", "S01 Results", "no evaluado", "alta", "m", "resuelta", "vigente"],
            ["C-002", "síntesis", "s", "tiene_valor_medido", "o", "sintesis(C-001)", "S01 Results", "no evaluado", "alta", "m", "resuelta", "vigente"],
            ["C-003", "recuento", "s", "tiene_valor_medido", "o", "glosa", "n/a", "no evaluado", "alta", "m", "resuelta", "vigente"],
        ]
        with (root / "data/afirmaciones/00.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(CLAIM_HEADER)
            writer.writerows(claims)
        with (root / "data/apendices/F_magnitudes.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(F_HEADER)
            writer.writerows(magnitude_rows)
        with (root / "data/apendices/A_fuentes.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["clave"])
            writer.writerows([[source] for source in appendix_sources])
        return root

    @staticmethod
    def _row(value: str, uncertainty: str, source: str, claim: str) -> list[str]:
        return ["magnitud", value, "unidad", "objeto", "método", uncertainty, "observado", source, claim]

    def test_classifies_qualitative_synthesis_and_rollup_without_calling_them_published(self) -> None:
        root = self._root([
            self._row("en minutos", "sin cifra numérica más precisa", "S01 Results", "C-001"),
            self._row("10–20", "rango compilado", "S01 Results", "C-002"),
            self._row("78", "recuento vivo", "registro canónico", "C-003"),
        ])
        rows = list(csv.DictReader(io.StringIO(builder.build(root).decode("utf-8"))))
        self.assertEqual(
            [row["resultado"] for row in rows],
            [
                "ESCALA_CUALITATIVA_SIN_CIFRA_COPIADA_DE_F",
                "CONTENIDO_COPIADO_DE_F_CON_C_SINTESIS",
                "CONTENIDO_COPIADO_DE_F_CON_C_GLOSA",
            ],
        )
        self.assertNotIn("PUBLICADO", " ".join(row["resultado"] for row in rows))

    def test_source_absent_from_appendix_a_is_fatal(self) -> None:
        root = self._root([
            self._row("1", "n/a", "S02 Results", "C-001"),
        ])
        with self.assertRaisesRegex(RuntimeError, "ausentes de A.*S02"):
            builder.build(root)

    def test_nonempty_direct_cell_is_only_described_as_copied(self) -> None:
        root = self._root([
            self._row("1", "n/a", "S01 Results", "C-001"),
        ])
        rows = list(csv.DictReader(io.StringIO(builder.build(root).decode("utf-8"))))
        self.assertEqual(rows[0]["resultado"], "CONTENIDO_COPIADO_DE_F")
        self.assertIn("sin cotejo semántico ni bibliográfico", rows[0]["razon_clasificacion"])


if __name__ == "__main__":
    unittest.main()
