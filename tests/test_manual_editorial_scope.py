"""Todas las firmas manuales fijan el entregable íntegro inspeccionado."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from scripts import audit_requirement_controls as controls


class ManualEditorialScopeTests(unittest.TestCase):
    def fixture(self, root):
        relative_paths = [
            "data/table_index.json", "data/apendices/A_fuentes.csv",
            "data/tablas/nodo.csv", "docs/secciones/001.md", "docs/order.txt",
            "docs/informe.md", "docs/informe_completo_autocontenido.md",
            "docs/auditorias/registro_busquedas_2026-08-08.csv",
        ]
        for relative in relative_paths:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(relative + "\n", encoding="utf-8")
        (root / "docs/order.txt").write_text("docs/secciones/001.md\n", encoding="utf-8")
        corpus = SimpleNamespace(
            root=root, section_paths=[root / "docs/secciones/001.md"],
            index={"tables": [{"csv_path": "data/apendices/A_fuentes.csv"},
                              {"csv_path": "data/tablas/nodo.csv"}]},
        )
        return corpus, relative_paths

    def test_each_manual_family_binds_inputs_and_reports(self):
        with TemporaryDirectory() as raw:
            root = Path(raw)
            corpus, relative_paths = self.fixture(root)
            for rid in ("R-0090", "R-0052", "R-0338", "R-0398", "R-0399", "R-0400", "R-0404", "R-0448"):
                with self.subTest(rid=rid):
                    result = controls.Result(rid, "editorial", {root / "data/table_index.json"})
                    paths = controls.manual_scope_paths(corpus, result)
                    expected = relative_paths if rid == "R-0399" else relative_paths[:-1]
                    self.assertEqual(set(paths), {root / value for value in expected})
                    self.assertFalse(result.automated)
                    self.assertEqual(result.checks, [])

    def test_every_artifact_change_invalidates_each_manual_family(self):
        with TemporaryDirectory() as raw:
            root = Path(raw)
            corpus, _ = self.fixture(root)
            for rid in ("R-0090", "R-0052", "R-0338", "R-0398", "R-0399", "R-0400", "R-0404", "R-0448"):
                result = controls.Result(rid, "manual", {root / "data/table_index.json"})
                paths = controls.manual_scope_paths(corpus, result)
                initial = controls.Corpus.scoped_digest(corpus, paths)
                for path in paths:
                    with self.subTest(rid=rid, path=path.name):
                        before = path.read_bytes()
                        path.write_bytes(before + b"cambio\n")
                        self.assertNotEqual(controls.Corpus.scoped_digest(corpus, paths), initial)
                        path.write_bytes(before)

    def test_unrelated_manual_scope_does_not_lose_paths(self):
        with TemporaryDirectory() as raw:
            root = Path(raw)
            corpus, relative_paths = self.fixture(root)
            keep = root / "docs/insumo-especifico.md"
            keep.write_text("insumo nominal\n", encoding="utf-8")
            auditor = root / "scripts/audit_requirement_controls.py"
            result = controls.Result("R-0052", "otro", {keep, auditor})
            expected = {root / value for value in relative_paths[:-1]} | {keep}
            self.assertEqual(set(controls.manual_scope_paths(corpus, result)), expected)

    def test_new_table_and_unordered_template_extend_scope_dynamically(self):
        with TemporaryDirectory() as raw:
            root = Path(raw)
            corpus, _ = self.fixture(root)
            result = controls.Result("R-0090", "manual")
            initial = controls.manual_scope_paths(corpus, result)
            new_csv = root / "data/tablas/nueva.csv"
            new_csv.write_text("nuevo\n", encoding="utf-8")
            corpus.index["tables"].append({"csv_path": "data/tablas/nueva.csv"})
            new_template = root / "docs/secciones/002.md"
            new_template.write_text("nueva\n", encoding="utf-8")
            current = controls.manual_scope_paths(corpus, result)
            self.assertEqual(set(current), set(initial) | {new_csv, new_template})
            corpus.index["tables"].pop()
            self.assertNotIn(new_csv, controls.manual_scope_paths(corpus, result))

    def test_ordered_template_outside_glob_is_bound(self):
        with TemporaryDirectory() as raw:
            root = Path(raw)
            corpus, _ = self.fixture(root)
            template = root / "docs/otra.md"
            template.write_text("otra\n", encoding="utf-8")
            (root / "docs/order.txt").write_text("docs/otra.md\n", encoding="utf-8")
            paths = controls.manual_scope_paths(corpus, controls.Result("R-0090", "manual"))
            self.assertIn(template, paths)
            self.assertIn(root / "docs/secciones/001.md", paths)

    def test_missing_input_is_not_silently_omitted(self):
        with TemporaryDirectory() as raw:
            root = Path(raw)
            corpus, _ = self.fixture(root)
            (root / "docs/informe.md").unlink()
            with self.assertRaisesRegex(RuntimeError, "ausente o no regular"):
                controls.manual_scope_paths(corpus, controls.Result("R-0090", "manual"))

    def test_order_cannot_escape_repository_directly_or_through_symlink(self):
        with TemporaryDirectory() as raw, TemporaryDirectory() as external:
            root = Path(raw)
            corpus, _ = self.fixture(root)
            outside = Path(external) / "fuera.md"
            outside.write_text("fuera\n", encoding="utf-8")
            link = root / "docs/enlace.md"
            link.symlink_to(outside)
            for value in (str(outside), "../" + Path(external).name + "/fuera.md", "docs/enlace.md"):
                with self.subTest(value=value):
                    (root / "docs/order.txt").write_text(value + "\n", encoding="utf-8")
                    with self.assertRaisesRegex(RuntimeError, "fuera del repositorio"):
                        controls.manual_scope_paths(corpus, controls.Result("R-0090", "manual"))

    def test_ledger_and_unrelated_audits_do_not_enter_base_or_digest(self):
        with TemporaryDirectory() as raw:
            root = Path(raw)
            corpus, _ = self.fixture(root)
            result = controls.Result("R-0090", "manual")
            initial_paths = controls.manual_scope_paths(corpus, result)
            initial_digest = controls.Corpus.scoped_digest(corpus, initial_paths)
            for relative in (str(controls.MANUAL_LEDGER), "manifest.json", "docs/auditorias/otra.md"):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("firma o derivado\n", encoding="utf-8")
            paths = controls.manual_scope_paths(corpus, result)
            self.assertEqual(paths, initial_paths)
            self.assertEqual(controls.Corpus.scoped_digest(corpus, paths), initial_digest)

    def test_signature_consumers_are_rejected_from_order_index_and_extras(self):
        for origin in ("order", "index", "extra", "symlink"):
            for relative in (str(controls.MANUAL_LEDGER), "manifest.json", str(controls.MANIFEST),
                             "docs/auditorias/controles_requisitos/R-0090.csv",
                             "docs/auditorias/lotes_manual/firmas.csv"):
                with self.subTest(origin=origin, relative=relative), TemporaryDirectory() as raw:
                    root = Path(raw)
                    corpus, _ = self.fixture(root)
                    target = root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("firma\n", encoding="utf-8")
                    result = controls.Result("R-0090", "manual")
                    if origin == "order":
                        (root / "docs/order.txt").write_text(relative + "\n", encoding="utf-8")
                    elif origin == "index":
                        corpus.index["tables"].append({"csv_path": relative})
                    elif origin == "extra":
                        result.scope_paths.add(target)
                    else:
                        link = root / "docs/secciones/firma.md"
                        link.symlink_to(target)
                    with self.assertRaisesRegex(RuntimeError, "circular o de auditoría no autorizada"):
                        controls.manual_scope_paths(corpus, result)

    def test_search_register_exception_is_nominal_not_global(self):
        with TemporaryDirectory() as raw:
            root = Path(raw)
            corpus, _ = self.fixture(root)
            register = root / "docs/auditorias/registro_busquedas_2026-08-08.csv"
            result = controls.Result("R-0090", "manual", {register})
            with self.assertRaisesRegex(RuntimeError, "auditoría no autorizada"):
                controls.manual_scope_paths(corpus, result)
            result.requirement_id = "R-0399"
            self.assertIn(register, controls.manual_scope_paths(corpus, result))

    def test_canonical_consumer_aliases_are_rejected_even_inside_repository(self):
        for canonical in ("manifest.json", str(controls.MANIFEST)):
            for via in ("canonical", "resolved"):
                with self.subTest(canonical=canonical, via=via), TemporaryDirectory() as raw:
                    root = Path(raw)
                    corpus, _ = self.fixture(root)
                    consumer = root / canonical
                    consumer.parent.mkdir(parents=True, exist_ok=True)
                    target = root / "data/consumidor-enlazado.csv"
                    target.write_text("firma\n", encoding="utf-8")
                    consumer.symlink_to(target)
                    reference = canonical if via == "canonical" else str(target.relative_to(root))
                    (root / "docs/order.txt").write_text(reference + "\n", encoding="utf-8")
                    with self.assertRaisesRegex(RuntimeError, "circular o de auditoría"):
                        controls.manual_scope_paths(corpus, controls.Result("R-0090", "manual"))

    def test_redirected_audit_directory_and_search_register_do_not_bypass_guard(self):
        for redirect_directory in (True, False):
            with self.subTest(directory=redirect_directory), TemporaryDirectory() as raw:
                root = Path(raw)
                corpus, _ = self.fixture(root)
                audits = root / "docs/auditorias"
                register = audits / "registro_busquedas_2026-08-08.csv"
                register.unlink()
                destination = root / "data/firmas"
                destination.mkdir()
                target = destination / register.name
                target.write_text("firma\n", encoding="utf-8")
                if redirect_directory:
                    audits.rmdir()
                    audits.symlink_to(destination, target_is_directory=True)
                else:
                    register.symlink_to(target)
                with self.assertRaisesRegex(RuntimeError, "circular o de auditoría"):
                    controls.manual_scope_paths(corpus, controls.Result("R-0399", "claves"))


if __name__ == "__main__":
    unittest.main()
