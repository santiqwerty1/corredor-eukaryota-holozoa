"""Regresiones de representación e historia; no adjudicación científica."""
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


class GeneLossQuantificationRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.claims = {
            row["#"]: row
            for path in sorted((ROOT / "data/afirmaciones").glob("*.csv"))
            for row in rows(str(path.relative_to(ROOT)))
        }

    def test_retired_bn_history_and_q_identity_are_preserved(self) -> None:
        history = json.loads((ROOT / "docs/auditorias/retirada_bn144_2026-09-27.json").read_text())
        self.assertEqual(len(history["huellas_bn_activas_antes"]), 495)
        self.assertEqual(len(history["bn_previas"]), 1)
        self.assertEqual(len(history["q_previas"]), 1)
        self.assertTrue(history["acreditacion_fecha_original"].startswith("NO_ACREDITADA:"))
        self.assertTrue(history["estado_revision_independiente"].startswith("PENDIENTE;"))
        for record in history["bn_previas"] + history["q_previas"]:
            payload = (json.dumps(record["fila"], ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
            self.assertEqual(hashlib.sha256(payload).hexdigest(), record["huella_fila_json_sha256"])
            self.assertEqual(set(record["cabecera"]), set(record["fila"]))
        self.assertEqual(history["bn_previas"][0]["huella_fila_json_sha256"], "49d875db6a79dc9b507dc35177b6fbdaca27044c2ac484529f318f2d5a029b58")

    def test_number_and_time_are_paired_without_removing_inactivation(self) -> None:
        for key, number in (("C-2833", "25"), ("C-2834", "4")):
            claim = self.claims[key]
            self.assertIn(f"{number} ORF", claim["Objeto"])
            self.assertIn("perdidos o inactivados", claim["Objeto"])
            self.assertIn("tiempo transcurrido: 16–20 millones de años", claim["Objeto"])
            self.assertIn("S562 Results, Differential gene loss", claim["Fuente"])
            magnitudes = [r for r in rows("data/apendices/F_magnitudes.csv") if r["#"] == key]
            self.assertEqual({(r["valor tal como lo publica la fuente"], r["unidad original"]) for r in magnitudes}, {(number, "ORF"), ("16–20", "Myr")})

    def test_temporal_limit_is_authors_statement_not_search_inference(self) -> None:
        record = self.claims["C-2835"]
        self.assertEqual(record["Atribución"], "expresa")
        self.assertIn("no distinguen", record["Afirmación"])
        self.assertIn("discusión (Discussion)", record["Fuente"])
        self.assertIn("no un resultado negativo inferido", record["Motivo"])
        self.assertIn("no determinan una curva temporal continua", record["Motivo"])

    def test_dtl_is_not_a_calendar_rate_or_family_frequency(self) -> None:
        self.assertIn("probabilidades no normalizadas", self.claims["C-1120"]["Objeto"])
        for key, value in (("C-2836", "0.592 ± 0.21"), ("C-2837", "0.185 ± 0.123")):
            selected = [r for r in rows("data/apendices/F_magnitudes.csv") if r["#"] == key]
            self.assertEqual(len(selected), 1)
            self.assertEqual(selected[0]["valor tal como lo publica la fuente"], value)
            self.assertEqual(selected[0]["unidad original"], "probabilidad no normalizada por rama")
            self.assertIn("no intervalo de confianza", selected[0]["incertidumbre publicada"])
            self.assertIn("frecuencia por familia", self.claims[key]["Motivo"])

    def test_magnitude_contract_links_counts_not_dtl_parameters(self) -> None:
        record = next(r for r in rows("data/auditoria/especificacion_magnitudes_por_requisito_v1.csv") if r["id_magnitud"] == "MREQ-0034")
        self.assertEqual(record["desenlace"], "VALOR_PUBLICADO")
        self.assertEqual(record["afirmaciones_terminales"], "C-2833; C-2834")
        self.assertEqual(record["registro_hueco"], "")
        self.assertEqual(record["razon_hueco"], "")
        self.assertEqual(record["transformacion_editorial"], "NINGUNA")
        for n in range(2833, 2838):
            self.assertEqual(self.claims[f"C-{n}"]["Aceptación"], "no evaluado")
            self.assertEqual(self.claims[f"C-{n}"]["Resolución"], "sin resolver")

    def test_source_manifest_does_not_mislabel_html_as_pdf(self) -> None:
        integration = json.loads((ROOT / "docs/auditorias/integracion_s512_s562_2026-09-27.json").read_text())
        self.assertEqual(integration["inventario_previo"]["cantidad"], 448)
        self.assertEqual(integration["inventario_final"]["cantidad"], 450)
        source = next(r for r in integration["archivos"] if "/S562 " in r["ruta_local"])
        self.assertTrue(source["ruta_local"].endswith(".html"))
        self.assertIn("no PDF ni JATS", source["contenido"])
        self.assertEqual(source["sha256"], "618ba43000d3c0495c0531d477ecaa2992006fa4e0369c09efb4272c0d5166e7")


if __name__ == "__main__":
    unittest.main()
