from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import renumber  # noqa: E402


class RenumberReferenceTests(unittest.TestCase):
    def test_range_preserves_members_across_inserted_final_key(self) -> None:
        mapping = {
            "C-001": "C-001",
            "C-002": "C-003",
            "C-003": "C-004",
        }
        self.assertEqual(
            renumber.replace_claim_references("sintesis(C-001–C-003)", mapping),
            "sintesis(C-001, C-003–C-004)",
        )

    def test_single_reference_is_not_remapped_twice(self) -> None:
        mapping = {"C-002": "C-003", "C-003": "C-004"}
        self.assertEqual(
            renumber.replace_claim_references("véase C-002", mapping),
            "véase C-003",
        )

    def test_range_with_missing_member_fails_before_writing(self) -> None:
        with self.assertRaises(ValueError):
            renumber.replace_claim_references(
                "C-001–C-003", {"C-001": "C-001", "C-003": "C-004"},
            )

    def test_atomic_write_preserves_existing_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "datos.csv"
            path.write_bytes(b"antes")
            path.chmod(0o664)
            original_mode = path.stat().st_mode & 0o777
            with mock.patch.object(
                renumber.os, "fchmod", wraps=renumber.os.fchmod,
            ) as mocked_fchmod:
                renumber.atomic_write_bytes(path, "después".encode("utf-8"))
            self.assertEqual(path.read_bytes(), "después".encode("utf-8"))
            mocked_fchmod.assert_called_once()
            self.assertEqual(mocked_fchmod.call_args.args[1], original_mode)
            self.assertEqual(path.stat().st_mode & 0o777, original_mode)


if __name__ == "__main__":
    unittest.main()
