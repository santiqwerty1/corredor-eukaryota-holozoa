"""Regresiones de representación y conservación; no revisión científica."""
from __future__ import annotations

import csv
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class HGTQuantificationRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.claims = {
            row["#"]: row
            for path in sorted((ROOT / "data/afirmaciones").glob("*.csv"))
            for row in rows(str(path.relative_to(ROOT)))
        }

    def test_preserves_retired_searches_without_crediting_original_dates(self) -> None:
        history = json.loads((ROOT / "docs/auditorias/retirada_bn133_bn146_2026-09-27.json").read_text())
        expected = {
            "BN-133": "85a2e205c015b9226a699a26d0efa16856deb323d8358ef2e0bc02217a6e45eb",
            "BN-146": "e5c4f0ced6cce3940a1c56e567566040fe0c549bd5658343fede7d3220306e02",
        }
        self.assertEqual(len(history["bn_previas"]), 2)
        self.assertEqual(len(history["q_previas"]), 2)
        self.assertEqual(len(history["huellas_bn_activas_antes"]), 497)
        for record in history["bn_previas"] + history["q_previas"]:
            payload = (json.dumps(record["fila"], ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
            digest = hashlib.sha256(payload).hexdigest()
            self.assertEqual(digest, record["huella_fila_json_sha256"])
            self.assertEqual(set(record["cabecera"]), set(record["fila"]))
            if record["ruta"].startswith("data/busquedas_negativas/"):
                self.assertEqual(digest, expected[record["fila"]["clave"]])
        self.assertTrue(history["acreditacion_fecha_original"].startswith("NO_ACREDITADA:"))
        self.assertTrue(history["estado_revision_independiente"].startswith("PENDIENTE;"))

    def test_requirements_have_published_values_not_an_added_common_denominator(self) -> None:
        spec = {r["id_magnitud"]: r for r in rows("data/auditoria/especificacion_magnitudes_por_requisito_v1.csv")}
        for key in ("MREQ-0035", "MREQ-0036"):
            record = spec[key]
            self.assertEqual(record["id_requisito"], "R-0220")
            self.assertEqual(record["desenlace"], "VALOR_PUBLICADO")
            self.assertEqual(record["registro_hueco"], "")
            self.assertEqual(record["razon_hueco"], "")
            self.assertIn("C-2828", record["afirmaciones_terminales"])
            self.assertIn("C-2832", record["afirmaciones_terminales"])
            self.assertNotIn("mismo denominador", record["magnitud_solicitada"])
        self.assertIn("C-2825", spec["MREQ-0035"]["afirmaciones_terminales"])
        self.assertIn("C-2827", spec["MREQ-0035"]["afirmaciones_terminales"])

    def test_s290_clades_are_not_gene_or_temporal_rates(self) -> None:
        magnitudes = rows("data/apendices/F_magnitudes.csv")
        for key, value in (("C-2825", "3.1–5.1"), ("C-2826", "<1.0"), ("C-2827", "0.3")):
            selected = [r for r in magnitudes if r["#"] == key]
            self.assertEqual(len(selected), 1)
            self.assertEqual(selected[0]["unidad original"], "% de clados")
            self.assertEqual(selected[0]["valor tal como lo publica la fuente"], value)
            self.assertIn("clados", self.claims[key]["Objeto"])
        self.assertIn("sin origen plastidial", self.claims["C-2827"]["Objeto"])

    def test_rival_counts_and_contamination_control_keep_their_denominators(self) -> None:
        self.assertEqual(self.claims["C-2828"]["Objeto"], "96 de 9075 grupos de ortólogos (1,06 %) en 13 genomas")
        self.assertEqual(self.claims["C-2829"]["Objeto"], "641 secuencias candidatas")
        self.assertEqual(self.claims["C-2830"]["Objeto"], "629 de 641 candidatos (98,12 %)")
        self.assertIn("no 641 eventos", self.claims["C-2829"]["Motivo"])
        self.assertIn("no debe atribuirse a todos", self.claims["C-2830"]["Motivo"])

    def test_identity_exceptions_remain_individual_not_group_means(self) -> None:
        record = self.claims["C-2831"]
        self.assertIn("5 de 96", record["Objeto"])
        self.assertIn("individual >70 %", record["Objeto"])
        self.assertIn("Ningún grupo", record["Motivo"])
        self.assertIn("identidad media", record["Motivo"])

    def test_review_summary_is_approximate_and_not_full_text_access(self) -> None:
        record = self.claims["C-2832"]
        self.assertIn("aproximadamente", record["Objeto"])
        self.assertIn("Highlights, cuarto punto", record["Fuente"])
        self.assertIn("sin afirmar acceso al cuerpo completo", record["Motivo"])
        for key in ("C-1185", "C-1186", "C-1187"):
            self.assertEqual(self.claims[key]["Predicado"], "propuesto_por")
            self.assertIn(self.claims[key]["Objeto"], ("Ku y Martin", "Van Etten y Bhattacharya"))
        for n in range(2825, 2833):
            self.assertEqual(self.claims[f"C-{n}"]["Aceptación"], "no evaluado")

    def test_independent_review_corrections_preserve_atomicity_and_caveats(self) -> None:
        self.assertNotIn("y consideraron", self.claims["C-1186"]["Afirmación"])
        self.assertIn("demasiado raras", self.claims["C-2838"]["Afirmación"])
        self.assertEqual(self.claims["C-2838"]["Objeto"], "Ku y Martin")
        self.assertIn("Sec8", self.claims["C-2838"]["Fuente"])
        self.assertNotIn("advirtieron", self.claims["C-2832"]["Afirmación"])
        self.assertIn("más datos y un procedimiento estandarizado", self.claims["C-2832"]["Motivo"])

    def test_tardigrade_error_is_contamination_not_a_claim_of_chimeric_assembly(self) -> None:
        record = self.claims["C-1197"]
        self.assertEqual(record["Objeto"], "contaminación no detectada en los datos ensamblados")
        self.assertNotIn("binning", record["Afirmación"])
        self.assertNotIn("quimérico", record["Objeto"])
        self.assertIn("no acredita ensamblaje quimérico", record["Motivo"])
        for key in ("C-1197", "C-1198"):
            self.assertEqual(self.claims[key]["Aceptación"], "no evaluado")
        self.assertIn("versión PNAS final, PMC4983863", self.claims["C-1196"]["Fuente"])

    def test_negative_hgt_statement_keeps_original_phrase_in_canonical_row(self) -> None:
        record = self.claims["C-1196"]
        self.assertIn("«Evidence for extensive fHGT is absent»", record["Fuente"])
        self.assertIn("Claims of Extensive Functional Horizontal Gene Transfer", record["Fuente"])
        self.assertIn("párrafo final", record["Fuente"])
        self.assertEqual(record["Predicado"], "cuestionado_por")
        self.assertEqual(record["Sujeto"], "afirmación C-1195")


if __name__ == "__main__":
    unittest.main()
