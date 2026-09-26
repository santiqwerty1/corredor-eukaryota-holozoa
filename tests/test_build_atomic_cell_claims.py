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
        self.assertEqual(len(changed), 14)
        for claim_id in changed:
            self.assertEqual(
                old_by_id[claim_id]["contenido"],
                "criterio discriminatorio, no parentesco filogenético",
            )
            self.assertEqual(
                new_by_id[claim_id]["contenido"],
                "criterio discriminatorio de cercanía a protomitocondrias",
            )

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


if __name__ == "__main__":
    unittest.main()
