from __future__ import annotations

import csv
import io
import unittest

from scripts import sync_claim_key_map as module


class ClaimKeyMapTests(unittest.TestCase):
    def test_live_map_is_one_to_one_and_marks_prospective_additions(self) -> None:
        rows = list(csv.DictReader(io.StringIO(module.payload().decode("utf-8"))))
        before = [row["clave_pre_renumeracion"] for row in rows]
        after = [row["clave_final"] for row in rows]
        self.assertEqual(len(before), len(set(before)))
        self.assertEqual(len(after), len(set(after)))
        self.assertEqual(set(after), set(module.claim_ids()))
        additions = [
            row for row in rows
            if int(row["clave_final"].split("-")[1]) >= module.PROSPECTIVE_START
        ]
        self.assertTrue(additions)
        self.assertTrue(all(row["clave_pre_renumeracion"] == row["clave_final"] for row in additions))
        self.assertTrue(all(row["cambio"] == "no" for row in additions))


if __name__ == "__main__":
    unittest.main()
