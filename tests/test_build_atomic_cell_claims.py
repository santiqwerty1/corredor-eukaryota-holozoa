from __future__ import annotations

import csv
import io
import unittest

from scripts import build_atomic_cell_claims as module


class AtomicCellClaimTests(unittest.TestCase):
    def test_live_targets_are_one_to_one_and_literal(self) -> None:
        claims_payload, manifest_payload, ids = module.build()
        claims = list(csv.DictReader(io.StringIO(claims_payload.decode("utf-8"))))
        manifest = list(csv.DictReader(io.StringIO(manifest_payload.decode("utf-8"))))
        original_targets = [
            row for path in module.TARGET_FILES for row in module._read(path)[1]
        ]
        targets = module._apply_corrections(original_targets)
        by_id = {row["#"]: row for row in claims}
        mapped = {
            (row["csv_path"], row["fila"], row["columna"], row["contenido_sha256"]): row
            for row in manifest
        }

        self.assertEqual(len(ids), 816)
        self.assertEqual(len(ids), len(set(ids)))
        for target in targets:
            claim = by_id[target["claim_id"]]
            self.assertIn(f"«{target['contenido']}»", claim["Afirmación"])
            self.assertIn(target["contenido"], claim["Objeto"])
            self.assertNotEqual(claim["Fuente"], "")
            key = (
                target["csv_path"], target["fila"], target["columna"],
                target["contenido_sha256"],
            )
            entry = mapped[key]
            self.assertIn(target["claim_id"], entry["afirmaciones"])
            self.assertEqual(entry["estado_revision"], "REVISADA")

    def test_semantic_corrections_preserve_original_review_evidence(self) -> None:
        original = [
            row for path in module.TARGET_FILES for row in module._read(path)[1]
        ]
        effective = module._apply_corrections(original)
        old_by_id = {row["claim_id"]: row for row in original}
        new_by_id = {row["claim_id"]: row for row in effective}
        changed = [
            claim_id for claim_id in old_by_id
            if old_by_id[claim_id]["contenido_sha256"]
            != new_by_id[claim_id]["contenido_sha256"]
        ]
        self.assertEqual(len(changed), 15)
        self.assertIn("C-2783", changed)
        previous_corrections = [key for key in changed if key != "C-2783"]
        self.assertEqual(len(previous_corrections), 14)
        self.assertEqual(set(previous_corrections), {
            "C-2009", "C-2020", "C-2031", "C-2042", "C-2053", "C-2075",
            "C-2141", "C-2152", "C-2163", "C-2174", "C-2185", "C-2196",
            "C-2207", "C-2218",
        })
        for claim_id in previous_corrections:
            self.assertEqual(
                old_by_id[claim_id]["contenido"],
                "criterio discriminatorio, no parentesco filogenético",
            )
            self.assertEqual(
                new_by_id[claim_id]["contenido"],
                "criterio discriminatorio de cercanía a protomitocondrias",
            )
        old_method = old_by_id["C-2783"]
        new_method = new_by_id["C-2783"]
        self.assertEqual(old_method["contenido_sha256"], "c45abf5233e7693dc57c32122466526f24b989defe1fce4dacda02312fbffbd2")
        self.assertEqual(
            old_method["contenido"],
            "ensamblaje de referencia y reconstrucción comparativa; los dos huecos cuantitativos se conservan sin inferir valores ni mezclar versiones",
        )
        self.assertEqual(new_method["_contenido_previo"], old_method["contenido"])
        self.assertEqual(new_method["_contenido_previo_sha256"], old_method["contenido_sha256"])
        self.assertEqual(
            new_method["contenido"],
            "tamaño: ensamblaje de referencia de S446; intrones: reconstrucción comparativa de S434; las métricas se atribuyen por separado a sus fuentes",
        )
        self.assertEqual(new_method["contenido_sha256"], "49f9189e50893de2092acf3b00eee251c912efad6481e0c2205cffaff2a3068d")

    def test_sphaeroforma_method_does_not_inherit_later_cell_claims(self) -> None:
        claims_payload, _, _ = module.build()
        by_id = {
            row["#"]: row
            for row in csv.DictReader(io.StringIO(claims_payload.decode("utf-8")))
        }
        method = by_id["C-2783"]
        self.assertEqual(method["Atribución"], "sintesis(C-1565, C-1566)")
        self.assertEqual(method["Fuente"], "n/a; dependencias canónicas C-1565; C-1566")
        self.assertNotIn("C-2821", str(method))
        self.assertNotIn("C-2822", str(method))
        self.assertEqual(by_id["C-2821"]["Atribución"], "expresa")
        self.assertEqual(by_id["C-2822"]["Atribución"], "expresa")

    def test_source_fragments_do_not_promote_claim_references(self) -> None:
        self.assertEqual(
            module._source_fragments("C-001; S49 tabla 2; BN-114; texto"),
            ["S49 tabla 2", "BN-114"],
        )

    def test_new_custom_predicate_requires_complete_definition(self) -> None:
        valid = (
            "`tiene_valor_literal_de_campo*` relaciona un estudio, matriz, taxón o sistema "
            "con el nombre y el contenido literales de una sola celda tabular. "
            "Ejemplo: C-1996"
        )
        module._validate_predicate_definition(valid)
        with self.assertRaisesRegex(RuntimeError, "Definición prospectiva incompleta"):
            module._validate_predicate_definition(
                "`tiene_valor_literal_de_campo*` sin relación ni ejemplo"
            )

    def synthetic_target(self, content="PP = 1 para el nodo X [C-032]"):
        # Ficción de test; no registra dictámenes para objetos reales.
        return {
            "csv_path": "data/tablas/ficticia.csv", "fila": "2",
            "columna": "soporte", "claim_id": "C-2606",
            "contenido": content, "afirmaciones_previas": "C-029; C-1983",
            "_contenido_previo": "soporte previo rechazado",
        }

    def synthetic_row(self):
        return {
            "estudio": "Ficción de test", "soporte": "dato",
            "filas y fuentes": "C-028; C-033; S01 p. 1; BN-115",
        }

    def synthetic_catalog(self):
        return {key: {"Fuerza": "alta"} for key in (
            "C-028", "C-029", "C-030", "C-031", "C-032", "C-033", "C-1983",
        )}

    def test_corrected_own_refs_do_not_inherit_previous_or_row_references(self):
        target = self.synthetic_target()
        before = dict(target)
        claim = module._generated_claim(target, self.synthetic_row(), self.synthetic_catalog())
        self.assertEqual(claim["Atribución"], "sintesis(C-032)")
        self.assertEqual(claim["Fuente"], "n/a; dependencias canónicas C-032")
        self.assertNotIn("BN-115", str(claim))
        self.assertNotIn("C-1983", str(claim))
        self.assertEqual(target, before)

    def test_corrected_ranges_keep_every_own_dependency_and_strength(self):
        target = self.synthetic_target("Valores publicados [C-029–C-032]")
        catalog = self.synthetic_catalog()
        catalog["C-031"]["Fuerza"] = "baja"
        claim = module._generated_claim(target, self.synthetic_row(), catalog)
        self.assertEqual(claim["Atribución"], "sintesis(C-029, C-030, C-031, C-032)")
        self.assertEqual(claim["Fuerza"], "baja")

    def test_corrected_local_gap_is_kept_but_row_gap_is_not_inherited(self):
        claim = module._generated_claim(
            self.synthetic_target("Dato [C-032]; límite de búsqueda [BN-010]"),
            self.synthetic_row(), self.synthetic_catalog(),
        )
        self.assertIn("BN-010 términos exactos y resultado", claim["Fuente"])
        self.assertNotIn("BN-115", claim["Fuente"])

    def test_correction_without_own_refs_does_not_invent_new_dependencies(self):
        claim = module._generated_claim(
            self.synthetic_target("Valor sin C escrita"),
            self.synthetic_row(), self.synthetic_catalog(),
        )
        self.assertEqual(claim["Atribución"], "sintesis(C-029, C-1983, C-028, C-033)")
        self.assertIn("BN-115", claim["Fuente"])

    def test_unmodified_target_retains_historical_candidate_scope(self):
        target = self.synthetic_target()
        del target["_contenido_previo"]
        claim = module._generated_claim(target, self.synthetic_row(), self.synthetic_catalog())
        self.assertEqual(claim["Atribución"], "sintesis(C-032, C-029, C-1983, C-028, C-033)")
        self.assertIn("BN-115", claim["Fuente"])

    def test_residual_exact_support_path_is_unchanged(self):
        target = self.synthetic_target()
        del target["_contenido_previo"]
        target["_disposicion_semantica"] = True
        claim = module._generated_claim(target, self.synthetic_row(), self.synthetic_catalog())
        self.assertEqual(claim["Atribución"], "sintesis(C-032)")
        self.assertEqual(claim["Fuente"], "n/a; dependencias canónicas C-032")

    def test_corrected_missing_dependency_still_blocks(self):
        with self.assertRaisesRegex(RuntimeError, "dependencia inexistente C-999"):
            module._generated_claim(
                self.synthetic_target("Dato [C-999]"),
                self.synthetic_row(), self.synthetic_catalog(),
            )

    def test_corrected_self_citation_is_not_removed_silently(self):
        for text in ("Dato [C-2606]", "Dato [C-032; C-2606]"):
            with self.subTest(text=text), self.assertRaisesRegex(RuntimeError, "autocita"):
                module._generated_claim(
                    self.synthetic_target(text), self.synthetic_row(), self.synthetic_catalog(),
                )

    def test_corrected_reversed_range_cannot_fall_back_to_row_references(self):
        with self.assertRaisesRegex(RuntimeError, "rango C invertido"):
            module._generated_claim(
                self.synthetic_target("Dato [C-032–C-029]"),
                self.synthetic_row(), self.synthetic_catalog(),
            )


if __name__ == "__main__":
    unittest.main()
