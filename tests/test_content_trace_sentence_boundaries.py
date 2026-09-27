"""Regresiones autorales de NC-DEN02; no adjudican soporte científico."""
import contextlib
import csv
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import build_content_trace as trace


class SentenceBoundaryTests(unittest.TestCase):
    def assert_sentences(self, text, expected):
        self.assertEqual(trace.split_sentences(text), expected)
        spans = trace.sentence_spans(text)
        self.assertEqual([text[start:end] for start, end in spans], expected)
        self.assertTrue(all(start < end for start, end in spans))
        self.assertTrue(all(a[1] <= b[0] for a, b in zip(spans, spans[1:])))
        self.assertEqual("".join(text.split()), "".join("".join(expected).split()))

    def test_postposed_citation_stays_with_previous_sentence(self):
        self.assert_sentences("Se midieron 223 orígenes. [C-001] Otro análisis informó 16 casos. [C-002; S01 p. 1]", [
            "Se midieron 223 orígenes. [C-001]", "Otro análisis informó 16 casos. [C-002; S01 p. 1]",
        ])

    def test_postposed_citation_cannot_cover_following_unregistered_sentence(self):
        pieces = trace.split_sentences("Se midieron 223 orígenes. [C-001; S01 p. 1] Otro análisis informó 16 casos.")
        self.assertEqual(len(pieces), 2)
        self.assertEqual(trace.claim_refs(pieces[0]), ("C-001",))
        self.assertEqual(trace.claim_refs(pieces[1]), ())

    def test_lowercase_start_is_also_a_boundary(self):
        self.assert_sentences("Se midió. [C-001] este segundo enunciado no recibe esa C.", [
            "Se midió. [C-001]", "este segundo enunciado no recibe esa C.",
        ])

    def test_adjacent_postposed_citations(self):
        self.assert_sentences("Se midió.[C-001][S01 p. 2] Otro dato. [C-002]", [
            "Se midió.[C-001][S01 p. 2]", "Otro dato. [C-002]",
        ])

    def test_multiple_postposed_citations_with_spaces(self):
        self.assert_sentences("Se midió. [C-001] [S01 p. 2] [BN-001] Otro dato. [C-002]", [
            "Se midió. [C-001] [S01 p. 2] [BN-001]", "Otro dato. [C-002]",
        ])

    def test_terminal_period_after_postposed_citation(self):
        self.assert_sentences("Se midió. [C-001]. Otro dato. [C-002]", [
            "Se midió. [C-001].", "Otro dato. [C-002]",
        ])

    def test_citations_before_terminal_period(self):
        self.assert_sentences("Se midió [C-001; S01 p. 2]. otro dato [C-002].", [
            "Se midió [C-001; S01 p. 2].", "otro dato [C-002].",
        ])

    def test_bibliographic_and_taxonomic_abbreviations(self):
        self.assert_sentences("Smith et al. observaron Buchnera sp. APS [C-001; S01 fig. 3; S02 suppl. p. 4]. Otro dato [C-002].", [
            "Smith et al. observaron Buchnera sp. APS [C-001; S01 fig. 3; S02 suppl. p. 4].", "Otro dato [C-002].",
        ])

    def test_abbreviation_as_terminal_before_postposed_citation(self):
        self.assert_sentences("Lo describieron Smith et al. [C-001] otro análisis [C-002].", [
            "Lo describieron Smith et al. [C-001]", "otro análisis [C-002].",
        ])

    def test_decimal_is_not_sentence_boundary(self):
        self.assert_sentences("Se midió 3.14 y 2,5 [C-001]. Hubo otro dato [C-002].", [
            "Se midió 3.14 y 2,5 [C-001].", "Hubo otro dato [C-002].",
        ])

    def test_italic_initial_term_keeps_abbreviation(self):
        self.assert_sentences("Se observó *S. rosetta* [C-001]. No se extrapola a *D. discoideum*. [C-002]", [
            "Se observó *S. rosetta* [C-001].", "No se extrapola a *D. discoideum*. [C-002]",
        ])

    def test_initial_label_does_not_exempt_lowercase_next_sentence(self):
        self.assert_sentences("Se comparó con el modelo B. este segundo resultado no tiene C.", [
            "Se comparó con el modelo B.", "este segundo resultado no tiene C.",
        ])
        diagnostics = trace.sentence_boundary_diagnostics("Se comparó con el modelo B. este segundo resultado no tiene C.")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0]["razon"], "AMBIGUA_INICIAL_EPITETO")

    def test_plain_genus_initial_has_two_explicit_readings(self):
        text = "Hubo pérdidas en B. floridanus. [C-001]"
        diagnostic, = trace.sentence_boundary_diagnostics(text)
        self.assertEqual(diagnostic["offset_punto"], text.index("B.") + 1)
        self.assertEqual([text[a:b] for a, b in diagnostic["lectura_corte"]], [
            "Hubo pérdidas en B.", "floridanus. [C-001]",
        ])
        self.assertEqual([text[a:b] for a, b in diagnostic["lectura_abreviatura"]], [text])

    def test_italic_initial_and_citation_initial_are_not_ambiguous(self):
        self.assertEqual(trace.sentence_boundary_diagnostics(
            "Hubo pérdidas en *B. floridanus*. [C-001; S01 §B. floridanus]"
        ), [])

    def test_url_internal_punctuation_and_terminal(self):
        self.assert_sentences("Consta en https://example.org/v1.2?a=3.5. [C-001] Otro resultado [C-002].", [
            "Consta en https://example.org/v1.2?a=3.5. [C-001]", "Otro resultado [C-002].",
        ])

    def test_url_terminal_before_quote_or_format_does_not_hide_boundary(self):
        wrappers = (("‘", "’"), ("‹", "›"), ("'", "'"), ("*", "*"),
                    ("_", "_"), ("`", "`"), ("**", "**"), ("__", "__"),
                    ("(‘**", "**’)"))
        for opening, closing in wrappers:
            for punctuation in (".", "?", "!", "…"):
                for separator in (" ", "\n\t"):
                    with self.subTest(opening=opening, punctuation=punctuation, separator=separator):
                        first = opening + "Consta en https://example.org/v1.2" + punctuation + closing
                        second = "otra proposición. [C-002]"
                        text = first + separator + second
                        self.assert_sentences(text, [first, second])
                        self.assertEqual(trace.claim_refs(trace.split_sentences(text)[0]), ())
                        self.assertEqual(trace.sentence_boundary_diagnostics(text), [])

    def test_url_closer_keeps_multiple_postposed_citations_on_previous_sentence(self):
        first = "(‘Consta en https://example.org.’) [C-001] [S01 p. 1]"
        self.assert_sentences(first + " Otro dato sin cita.", [first, "Otro dato sin cita."])
        self.assertEqual(trace.claim_refs(trace.split_sentences(first + " Otro dato sin cita.")[1]), ())

    def test_url_interior_apostrophe_format_and_decimal_are_not_trimmed(self):
        for url in ("https://example.org/O'Reilly/v1.2", "https://example.org/a_b/v1.2",
                    "https://example.org/a*b/v1.2", "https://example.org/a`b/v1.2",
                    "https://example.org/O’Neil?q=a_b&v=3.5"):
            with self.subTest(url=url):
                text = "Consta en " + url + " y se conserva [C-001]. Otro dato. [C-002]"
                self.assert_sentences(text, ["Consta en " + url + " y se conserva [C-001].", "Otro dato. [C-002]"])
                _, protected = trace.sentence_masks(text)
                start = text.index(url)
                self.assertTrue(all(start + i in protected for i, c in enumerate(url) if c == "."))

    def test_real_main_url_closers_require_a_claim_for_each_sentence(self):
        wrappers = (("‘", "’"), ("‹", "›"), ("'", "'"), ("*", "*"), ("_", "_"), ("`", "`"))
        for opening, closing in wrappers:
            for first_has_claim, second_has_claim in ((False, True), (True, False), (True, True)):
                with self.subTest(opening=opening, first=first_has_claim, second=second_has_claim), tempfile.TemporaryDirectory(prefix="author-den02-url-") as temporary:
                    first = opening + "Consta en https://example.org." + closing
                    text = first + (" [C-001]" if first_has_claim else "") + " Otra proposición."
                    text += " [C-002]" if second_has_claim else ""
                    valid = first_has_claim and second_has_claim
                    root = Path(temporary)
                    prose = root / "docs/secciones/003-02-fixture.md"
                    prose.parent.mkdir(parents=True)
                    prose.write_text(text + "\n", encoding="utf-8")
                    claims = root / "data/afirmaciones/03.csv"
                    claims.parent.mkdir(parents=True)
                    with claims.open("w", encoding="utf-8", newline="") as handle:
                        writer = csv.writer(handle)
                        writer.writerow(["#", "Afirmación", "Sujeto", "Predicado", "Objeto", "Fuente", "Motivo", "Resolución"])
                        for key in ("C-001", "C-002"):
                            writer.writerow([key, "Dato ficticio", "fixture", "posee_rasgo", "dato", "S01 p. 1", "Sólo prueba", "resuelta"])
                    (root / "data/table_index.json").write_text('{"tables": []}\n', encoding="utf-8")
                    manifest = root / "data/auditoria/mapeo_celdas_afirmaciones.csv"
                    manifest.parent.mkdir(parents=True)
                    with manifest.open("w", encoding="utf-8", newline="") as handle:
                        csv.writer(handle).writerow(trace.CELL_MANIFEST_HEADER)
                    output = root / "docs/auditorias/fixture.csv"
                    with patch.object(trace, "ROOT", root), patch.object(trace, "CELL_MANIFEST", manifest), patch.object(trace, "OUTPUT", output), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                        with patch.object(sys, "argv", ["build_content_trace.py"]):
                            write_exit = trace.main()
                        payload = output.read_bytes() if output.exists() else None
                        with patch.object(sys, "argv", ["build_content_trace.py", "--check"]):
                            check_exit = trace.main()
                        after = output.read_bytes() if output.exists() else None
                    self.assertEqual(write_exit == check_exit == 0, valid)
                    self.assertEqual(payload is not None, valid)
                    self.assertEqual(payload, after)
                    if valid:
                        self.assertEqual(len(list(csv.DictReader(io.StringIO(payload.decode())))), 2)

    def test_markdown_link_url_does_not_split_inside_link(self):
        self.assert_sentences("Consta en [el sitio](https://example.org/v1.2). [C-001] Otro resultado [C-002].", [
            "Consta en [el sitio](https://example.org/v1.2). [C-001]", "Otro resultado [C-002].",
        ])

    def test_nested_citation_preserves_locator_punctuation(self):
        self.assert_sentences("Se midió. [C-001; S01 fig. 2 (panel [a.])] Otra medida. [C-002]", [
            "Se midió. [C-001; S01 fig. 2 (panel [a.])]", "Otra medida. [C-002]",
        ])

    def test_quoted_terminal_then_citation(self):
        self.assert_sentences("«Se observaron 12 casos.» [C-001] Otro resultado [C-002].", [
            "«Se observaron 12 casos.» [C-001]", "Otro resultado [C-002].",
        ])

    def test_closers_after_postposed_citation_do_not_lend_C(self):
        for opening, closing in (("(", ")"), ("«", "»"), ("“", "”"), ("‘", "’"), ("‹", "›"), ('"', '"'),
                                 ("'", "'"), ("*", "*"), ("**", "**"), ("__", "__"),
                                 ("(**«", "»**)")):
            with self.subTest(opening=opening):
                first = opening + "Se observó. [C-001]" + closing
                self.assert_sentences(first + " Otro resultado carece de C.", [first, "Otro resultado carece de C."])
                self.assertEqual(trace.claim_refs(trace.split_sentences(first + " Otro resultado carece de C.")[1]), ())

    def test_closers_between_multiple_citations(self):
        self.assert_sentences("(Se observó. [C-001]) [S01 p. 1] **Otro resultado**.", [
            "(Se observó. [C-001]) [S01 p. 1]", "**Otro resultado**.",
        ])

    def test_no_space_after_postposed_citation(self):
        for first in ("Se observó. [C-001]", "(Se observó. [C-001])", "Se observó…[C-001]"):
            with self.subTest(first=first):
                self.assert_sentences(first + "otro dato.", [first, "otro dato."])

    def test_linked_postposed_citation_with_nested_or_escaped_parentheses(self):
        for destination in ("https://example.org/v1.2", "https://example.org/(v1.2)",
                            r"https://example.org/v1\)2"):
            with self.subTest(destination=destination):
                first = "Se observó. [C-001](" + destination + ")"
                self.assert_sentences(first + " Otra observación.", [first, "Otra observación."])
                self.assertEqual(trace.citation_end(first, first.index("[")), len(first))

    def test_unicode_ellipsis_terminal_with_and_without_citation(self):
        self.assert_sentences("Se observó… [C-001] otro dato… [C-002] Fin…", [
            "Se observó… [C-001]", "otro dato… [C-002]", "Fin…",
        ])

    def test_underscore_italic_initial_is_not_split_or_diagnosed(self):
        text = "Se observó _B. floridanus_. [C-001] Otro dato. [C-002]"
        self.assert_sentences(text, ["Se observó _B. floridanus_. [C-001]", "Otro dato. [C-002]"])
        self.assertEqual(trace.sentence_boundary_diagnostics(text), [])

    def test_double_emphasis_does_not_silently_protect_plain_initial(self):
        text = "Modelo __B. este resultado__ carece de apoyo. [C-001]"
        self.assertTrue(trace.sentence_boundary_diagnostics(text))

    def test_abbreviation_terminal_retains_two_readings(self):
        for text in (
            "Se analizaron otras spp. El segundo resultado no está registrado. [C-001]",
            "Se analizaron otras spp. el segundo resultado no está registrado. [C-001]",
            "Se analizaron otras spp. **El segundo** resultado no está registrado. [C-001]",
            "(Se analizaron otras spp.) Otro resultado no está registrado. [C-001]",
            "Se analizaron otras spp. [SIN FUENTE] Otro resultado. [C-001]",
            "Se consultó p. 2 resultados más se atribuyeron después. [C-001]",
        ):
            with self.subTest(text=text):
                diagnostic, = trace.sentence_boundary_diagnostics(text)
                self.assertEqual(diagnostic["razon"], "AMBIGUA_ABREVIATURA_TERMINAL")
                self.assertEqual([text[a:b] for a, b in diagnostic["lectura_abreviatura"]], [text])
                before, after = [text[a:b] for a, b in diagnostic["lectura_corte"]]
                self.assertEqual(trace.claim_refs(before), ())
                self.assertEqual(trace.claim_refs(after), ("C-001",))
                self.assertEqual("".join((before + after).split()), "".join(text.split()))

    def test_abbreviations_inside_citation_or_url_remain_unambiguous(self):
        text = "Se observó. [C-001; S01 fig. 3; p. 2] Otro dato https://example.org/spp.test. [C-002]"
        self.assertEqual(trace.sentence_boundary_diagnostics(text), [])

    def test_unclosed_nominal_citation_or_link_is_rejected_by_payload(self):
        for text in ("Se observó [C-001; S01 p. 1 sin cierre.",
                     "Se observó [C-001](https://example.org/sin_cierre.",
                     "Se observó [C-001; panel [a] sin cierre."):
            with self.subTest(text=text), patch.object(trace, "claim_catalog", return_value=({"C-001": "ficticia"}, {})):
                segment = trace.Segment("prosa", "docs/secciones/003-02-fixture.md", "L1", "n/a", text, ("C-001",), "cita_en_segmento")
                errors = trace.validate_payload(trace.csv_bytes([segment]))
                self.assertTrue(any("sin cierre" in error for error in errors), errors)

    def test_inline_link_destination_and_title_valid_forms(self):
        # Sintaxis nominal delimitada, no una comprobación de que la URL resuelva.
        for body in (
            "", "<>", "../article.pdf#sec", "https://example.org/a(b(c(d)))",
            r"https://example.org/a\(b", "<https://example.org/a(b>", "<relative path>",
            'https://example.org "Figura (a"', "https://example.org 'Figura a)'",
            r'https://example.org "Figura \"a\""', "https://example.org (Figura a)",
            r"https://example.org (Figura \(a\))", '"Título sin destino"',
            '  https://example.org \n "Título" \t', "https://example.org\u00a0dato",
        ):
            with self.subTest(body=body):
                first = "Dato. [C-001](" + body + ")"
                self.assertEqual(trace.inline_link_end(first, first.index("](") + 1), len(first))
                self.assert_sentences(first + " Otro dato. [C-002]", [first, "Otro dato. [C-002]"])

    def test_invalid_inline_link_cannot_mask_prose(self):
        for body in (
            "La proteína actúa. Otra cambia.", "https://example.org La proteína actúa. Otra cambia.",
            "<> La proteína actúa. Otra cambia.", "url sin título delimitado",
            "url\tprosa. Otra.", "url\nprosa. Otra.", r"url\ prosa. Otra.",
            'url "título" prosa. Otra.', 'url "título sin cierre',
            "<url<interior>", "<url\nfragmento>", "url\x7f", "url\x0b",
            "url (título (anidado))", "url(a", "url\n\n", '<url>"título"',
        ):
            with self.subTest(body=body):
                text = "Dato. [C-001](" + body + ")"
                self.assertIsNone(trace.citation_end(text, text.index("[")))
                segment = trace.Segment("prosa", "docs/secciones/003-02-fixture.md", "L1", "n/a", text, ("C-001",), "cita_en_segmento")
                self.assertTrue(any("sintaxis inválida" in e for e in trace.validate_payload(trace.csv_bytes([segment]))))

    def test_link_title_newlines_are_not_blank_lines(self):
        for line_end in ("\n", "\r", "\r\n"):
            with self.subTest(line_end=repr(line_end)):
                valid = '[C-001](url "Primera' + line_end + 'segunda' + line_end + 'tercera")'
                self.assertEqual(trace.citation_end(valid, 0), len(valid))
                invalid = '[C-001](url "Primera' + line_end + ' \t' + line_end + 'segunda")'
                self.assertIsNone(trace.citation_end(invalid, 0))

    def test_angle_destination_escape_is_not_an_unescaped_delimiter(self):
        valid = r"[C-001](<https://example.org/a\>b>)"
        self.assertEqual(trace.citation_end(valid, 0), len(valid))
        invalid = r"[C-001](<https://example.org/a\>)"
        self.assertIsNone(trace.citation_end(invalid, 0))

    def test_link_whitespace_newlines_and_crlf_are_bounded(self):
        for separator in (" ", "\t", "\n", "\r", "\r\n", " \r\n\t"):
            with self.subTest(separator=repr(separator)):
                text = '[C-001](' + separator + 'url' + separator + '"título"' + separator + ')'
                self.assertEqual(trace.citation_end(text, 0), len(text))
        self.assertIsNone(trace.citation_end('[C-001](url\r\n\r\n"título")', 0))

    def test_real_main_rejects_false_destinations_and_accepts_delimited_title(self):
        cases = (
            ("Dato. [C-001](La proteína cambia. Otra actúa.)", False),
            ("Dato. [C-001](url Un resultado. Otro resultado.)", False),
            ("Dato. [C-001](<> Un resultado. Otro resultado.)", False),
            ('Dato. [C-001](url "Figura (a") Otro dato. [C-002]', True),
            ("Dato. [C-001](<url(a>) Otro dato. [C-002]", True),
            ("‘Dato. [C-001]’ Otro dato. [C-002]", True),
        )
        for text, valid in cases:
            with self.subTest(text=text), tempfile.TemporaryDirectory(prefix="author-den02-link-") as temporary:
                root = Path(temporary)
                prose = root / "docs/secciones/003-02-fixture.md"
                prose.parent.mkdir(parents=True)
                prose.write_text(text + "\n", encoding="utf-8")
                claims = root / "data/afirmaciones/03.csv"
                claims.parent.mkdir(parents=True)
                with claims.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.writer(handle)
                    writer.writerow(["#", "Afirmación", "Sujeto", "Predicado", "Objeto", "Fuente", "Motivo", "Resolución"])
                    for key in ("C-001", "C-002"):
                        writer.writerow([key, "Dato ficticio", "fixture", "posee_rasgo", "dato", "S01 p. 1", "Sólo prueba", "resuelta"])
                (root / "data/table_index.json").write_text('{"tables": []}\n', encoding="utf-8")
                manifest = root / "data/auditoria/mapeo_celdas_afirmaciones.csv"
                manifest.parent.mkdir(parents=True)
                with manifest.open("w", encoding="utf-8", newline="") as handle:
                    csv.writer(handle).writerow(trace.CELL_MANIFEST_HEADER)
                output = root / "docs/auditorias/fixture.csv"
                with patch.object(trace, "ROOT", root), patch.object(trace, "CELL_MANIFEST", manifest), patch.object(trace, "OUTPUT", output), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    with patch.object(sys, "argv", ["build_content_trace.py"]):
                        first = trace.main()
                    payload = output.read_bytes() if output.exists() else None
                    with patch.object(sys, "argv", ["build_content_trace.py", "--check"]):
                        second = trace.main()
                    after = output.read_bytes() if output.exists() else None
                self.assertEqual(first == second == 0, valid)
                self.assertEqual(payload is not None, valid)
                self.assertEqual(payload, after)
                if valid:
                    self.assertEqual(len(list(csv.DictReader(io.StringIO(payload.decode())))), 2)

    def test_two_sentences_inside_outer_parentheses_do_not_share_claim(self):
        self.assert_sentences("(Se observaron 12 casos. [C-001] Otro resultado [C-002].)", [
            "(Se observaron 12 casos. [C-001]", "Otro resultado [C-002].)",
        ])

    def test_exclamations_questions_and_ellipsis(self):
        self.assert_sentences("¿Hubo cambio? [C-001] ¡Hubo! [C-002] Se discutió... [C-003] otro dato.", [
            "¿Hubo cambio? [C-001]", "¡Hubo! [C-002]", "Se discutió... [C-003]", "otro dato.",
        ])

    def test_sin_fuente_marker_not_attached_to_preceding_sentence(self):
        self.assert_sentences("Primer dato. [C-001] [SIN FUENTE] Otro dato; se conserva para revisar. [C-002]", [
            "Primer dato. [C-001]", "[SIN FUENTE] Otro dato; se conserva para revisar. [C-002]",
        ])

    def test_non_citation_bracket_cannot_lend_claim_backwards(self):
        self.assert_sentences("Primer dato. [Este segundo dato usa C-002]", [
            "Primer dato.", "[Este segundo dato usa C-002]",
        ])

    def test_original_unicode_offsets_and_whitespace_are_preserved(self):
        text = "  Ámbito α. [C-001]\n\tβ segundo. [C-002]  "
        self.assert_sentences(text, ["Ámbito α. [C-001]", "β segundo. [C-002]"])
        self.assertEqual(trace.sentence_spans(text)[0][0], 2)
        self.assertEqual(trace.sentence_spans(text)[1][0], text.index("β"))

    def test_empty_and_non_terminated_input(self):
        self.assert_sentences("  ", [])
        self.assert_sentences(" Texto sin signo terminal [C-001] ", ["Texto sin signo terminal [C-001]"])

    def test_internal_invariants_unchanged(self):
        self.assertEqual(trace.internal_invariant_errors(), [])

    def test_full_narrative_pipeline_fails_on_newly_exposed_sentence_without_C(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "docs/secciones/003-02-fixture.md"
            path.parent.mkdir(parents=True)
            path.write_text("Se midieron 223 orígenes. [C-001; S01 p. 1] Otro análisis informó 16 casos.\n", encoding="utf-8")
            claims = root / "data/afirmaciones/03.csv"
            claims.parent.mkdir(parents=True)
            with claims.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["#", "Afirmación", "Sujeto", "Predicado", "Objeto", "Fuente", "Motivo", "Resolución"])
                writer.writerow(["C-001", "Se midieron 223 orígenes", "fixture", "tiene_valor_medido", "223", "S01 p. 1", "Caso ficticio", "resuelta"])
            with patch.object(trace, "ROOT", root):
                segments = trace.narrative_segments()
                errors = trace.validate_payload(trace.csv_bytes(segments))
            self.assertEqual(len(segments), 2)
            self.assertEqual(segments[0].claims, ("C-001",))
            self.assertEqual(segments[1].claims, ())
            self.assertEqual(segments[1].locator, "L1; oración 2")
            self.assertTrue(any("carecen de C" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
