from __future__ import annotations

import unittest

from scripts import corpus_io


class SourceReferenceTests(unittest.TestCase):
    def test_ranges_expand_and_supplementary_labels_do_not(self) -> None:
        self.assertEqual(
            corpus_io.expand_source_refs(
                "S08–S10 Results; S27 fig. 2; figs. S62–S63; tabla S8",
            ),
            ["S08", "S09", "S10", "S27"],
        )


if __name__ == "__main__":
    unittest.main()
