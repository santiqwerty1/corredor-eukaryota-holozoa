from __future__ import annotations

import unittest

from scripts import corpus_io


class SourceReferenceTests(unittest.TestCase):
    def test_abbreviated_ranges_retain_every_interior_key(self) -> None:
        self.assertEqual(corpus_io.expand_source_refs("S177–181"),
                         ["S177", "S178", "S179", "S180", "S181"])
        self.assertEqual(corpus_io.expand_source_refs("S08-10"), ["S08", "S09", "S10"])
        with self.assertRaisesRegex(ValueError, "Rango S descendente"):
            corpus_io.expand_source_refs("S181–177")

    def test_abbreviated_supplementary_range_is_not_bibliographic(self) -> None:
        self.assertEqual(corpus_io.expand_source_refs("S01 figs. S62–64"), ["S01"])

    def test_ranges_expand_and_supplementary_labels_do_not(self) -> None:
        self.assertEqual(
            corpus_io.expand_source_refs(
                "S08–S10 Results; S27 fig. 2; figs. S62–S63; tabla S8",
            ),
            ["S08", "S09", "S10", "S27"],
        )


if __name__ == "__main__":
    unittest.main()
