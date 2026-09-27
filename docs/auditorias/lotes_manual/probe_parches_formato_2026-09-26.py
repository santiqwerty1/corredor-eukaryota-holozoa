import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
import validate
import audit_requirement_controls as controls

class IndependentEditorialPatchTests(unittest.TestCase):
    def test_bn117_original_fixture_fails_on_missing_interior(self):
        # La estructura nominal es la fila real; solo se cambia su último campo
        # en memoria y se escribe un fixture temporal, no el corpus.
        path = ROOT / 'data/busquedas_negativas/15_4_15-4-registro-material-tiempo-ambiente-y-ecologia.csv'
        with path.open(newline='') as handle:
            reader = csv.DictReader(handle)
            row = next(r for r in reader if r['clave'] == 'BN-117')
            header = reader.fieldnames
        row['filas relacionadas'] = 'C-757–C-792; S139–S142; S177–S181; S548'
        valid = {'S139', 'S140', 'S141', 'S142', 'S177', 'S178', 'S179', 'S181', 'S548'}
        with tempfile.TemporaryDirectory(prefix='formato-bn117-') as directory:
            fixture = Path(directory) / 'BN-117.csv'
            with fixture.open('w', newline='') as handle:
                writer = csv.DictWriter(handle, header)
                writer.writeheader(); writer.writerow(row)
            self.assertEqual(validate.source_reference_errors(fixture.read_text(), valid),
                             ["Referencias S indefinidas: ['S180']"])
            row['filas relacionadas'] = 'C-757–C-792; S139–S142; S177–S179; S181; S548'
            with fixture.open('w', newline='') as handle:
                writer = csv.DictWriter(handle, header)
                writer.writeheader(); writer.writerow(row)
            self.assertEqual(validate.source_reference_errors(fixture.read_text(), valid), [])

    def test_ranges_expand_all_interior_keys_and_whitespace(self):
        for text in ('S177-S181', 'S177 – S181', 'S177\n–\nS181'):
            with self.subTest(text=text):
                self.assertEqual(validate.source_reference_errors(text, {'S177', 'S181'}),
                                 ["Referencias S indefinidas: ['S178', 'S179', 'S180']"])

    def test_preserves_literal_check_in_supplementary_context(self):
        self.assertEqual(validate.source_reference_errors('S01 fig. S62–S64', {'S01'}),
                         ["Referencias S indefinidas: ['S62', 'S64']"])

    def test_missing_literal_after_invalid_range_is_not_lost(self):
        errors = validate.source_reference_errors('S181–S177; S555', {'S177', 'S181'})
        self.assertEqual(len(errors), 2)
        self.assertIn('S555', errors[1])

    def test_range_after_descending_range_is_not_silently_skipped(self):
        self.assertTrue(validate.source_reference_errors('S181–S177; S200–S202', {'S177','S181','S200','S202'}))

    def test_short_form_reinspection_rejects_missing_interiors(self):
        # Reinspección posterior a FORM-03. El comportamiento anterior que
        # aceptaba este rango se conserva en el informe histórico adjunto.
        self.assertEqual(validate.source_reference_errors('S177–181', {'S177','S181'}),
                         ["Referencias S indefinidas: ['S178', 'S179', 'S180']"])
        self.assertEqual(validate.source_reference_errors('S177–179; S181', {'S177','S178','S179','S181'}), [])
        self.assertEqual(validate.source_reference_errors('S177–179; S181', {'S177','S179','S181'}),
                         ["Referencias S indefinidas: ['S178']"])

    def test_short_forms_do_not_reinterpret_supplements(self):
        self.assertEqual(validate.source_reference_errors('S01 figs. S62–64', {'S01','S62'}), [])
        self.assertEqual(validate.source_reference_errors('S01 tabla S62–64; S177–179', {'S01','S62','S177','S179'}),
                         ["Referencias S indefinidas: ['S178']"])

    def test_short_descending_range_and_leading_zero(self):
        self.assertTrue(validate.source_reference_errors('S181–177', {'S177','S181'}))
        self.assertEqual(validate.source_reference_errors('S08–10', {'S08','S10'}),
                         ["Referencias S indefinidas: ['S09']"])

    def test_live_scope_exact_and_not_automatically_promoted(self):
        corpus = controls.Corpus(ROOT)
        rows = controls.read_csv(ROOT / controls.MANIFEST)[1]
        expected_common = {ROOT / 'data/table_index.json', ROOT / 'docs/order.txt',
                           ROOT / 'docs/informe.md', ROOT / 'docs/informe_completo_autocontenido.md'}
        expected_common.update(corpus.section_paths)
        expected_common.update(ROOT / row['csv_path'] for row in corpus.index['tables'])
        for row in rows:
            rid = row['id_requisito']
            if rid not in {'R-0398','R-0399','R-0400','R-0404','R-0448'}:
                continue
            result = controls.evaluate(corpus, row)
            expected = set(expected_common)
            if rid == 'R-0399':
                expected.add(ROOT / 'docs/auditorias/registro_busquedas_2026-08-08.csv')
            paths = controls.manual_scope_paths(corpus, result)
            self.assertEqual(set(paths), expected)
            self.assertFalse(result.automated)
            self.assertTrue(any('PENDIENTE_AUTOMATIZACION_NOMINAL' in error for error in result.errors))
            canonical = ''.join(p.relative_to(ROOT).as_posix() + '\x1f' + hashlib.sha256(p.read_bytes()).hexdigest() + '\n' for p in sorted(expected))
            self.assertEqual(corpus.scoped_digest(paths), hashlib.sha256(canonical.encode()).hexdigest())

    def test_full_independent_editorial_inventory_stays_live(self):
        evidence = json.loads((ROOT / 'docs/auditorias/lotes_manual/evidencia_formato_2026-09-26.json').read_text())
        for relative, digest in evidence['inventario_sha256'].items():
            with self.subTest(path=relative):
                self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), digest)

    def test_scope_retains_prior_targets(self):
        with tempfile.TemporaryDirectory(prefix='formato-scope-') as directory:
            root = Path(directory)
            extra = root / 'extra-original.csv'
            corpus = SimpleNamespace(root=root, section_paths=[], index={'tables': []})
            result = controls.Result('R-0398','formato',{extra})
            self.assertIn(extra, controls.manual_scope_paths(corpus, result))

if __name__ == '__main__':
    unittest.main(verbosity=2)
