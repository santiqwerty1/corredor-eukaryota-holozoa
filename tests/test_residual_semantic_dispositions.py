"""Fixtures ficticias: no son dictámenes ni firmas sobre el corpus real."""
from __future__ import annotations

import copy
import csv
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import residual_semantic_dispositions as module


class ResidualSemanticDispositionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.registry = self.root / module.REGISTRY
        self.registry.parent.mkdir(parents=True)
        self.author_path = self.root / "docs/author.md"
        self.author_path.parent.mkdir()
        self.author_path.write_text("Propuesta ficticia; no corpus científico.\n")
        self.source_path = self.root / "fuentes/S01 [2000] Fiction.xml"
        self.source_path.parent.mkdir()
        self.source_path.write_text("<article><p>Fixture value 42.</p></article>")
        self.claim_path = self.root / "data/afirmaciones/15.csv"
        self.claim_path.parent.mkdir(parents=True)
        self.claim = {"#": "C-9000", "Afirmación": "Fixture value 42.",
                      "Atribución": "expresa", "Fuente": "S01 Results, paragraph 1"}
        self.write_claim()
        self.residual = {
            "claim_id": "C-2708", "csv_path": "data/tablas/09/table.csv",
            "fila": "7", "columna": "campo", "contenido_anterior": "valor rechazado",
            "contenido_sha256": module.cell_hash("valor rechazado"),
            "resultado": "NO_CONFORME",
        }
        self.target = {
            key: self.residual[key] for key in ("claim_id", "csv_path", "fila", "columna")
        } | {"contenido": "hueco previo", "contenido_sha256": module.cell_hash("hueco previo")}
        self.correction = {
            key: self.residual[key] for key in ("claim_id", "csv_path", "fila", "columna")
        } | {
            "contenido_previo": self.target["contenido"],
            "contenido_previo_sha256": self.target["contenido_sha256"],
            "contenido_corregido": "Fixture value 42 [C-9000]",
            "contenido_corregido_sha256": module.cell_hash("Fixture value 42 [C-9000]"),
            "autor_correccion": "fictional-author", "evidencia_correccion": "docs/author.md",
        }
        self.record = {key: self.residual[key] for key in ("claim_id", "csv_path", "fila", "columna")} | {
            "identidad_fila": {"identidad": "fixture system"},
            "bn": "BN-147", "sha256_residual": module.row_hash(self.residual),
            "contenido_previo": self.target["contenido"], "sha256_previo": self.target["contenido_sha256"],
            "contenido_nuevo": self.correction["contenido_corregido"],
            "sha256_nuevo": self.correction["contenido_corregido_sha256"],
            "autor": "fictional-author", "fecha_utc": "2026-09-27T01:00:00Z",
            "componentes": ["fixture value and unit"], "limites_pendientes": "Fictional fixture only.",
            "afirmaciones_soporte": {"C-9000": module.row_hash(self.claim)},
            "artefactos_soporte": {self.source_path.relative_to(self.root).as_posix(): self.sha(self.source_path)},
            "evidencia_autor": {"ruta": "docs/author.md", "sha256": self.sha(self.author_path)},
        }
        self.table_path = self.root / self.residual["csv_path"]
        self.table_path.parent.mkdir(parents=True)
        self.table_path.write_text("identidad,campo\n" + "fixture system,hueco previo\n" * 6)
        self.review = {
            "version": 1, "claim_id": "C-2708", "disposicion_sha256": "",
            "revisor": "fictional-reviewer", "fecha_utc": "2026-09-27T01:00:01Z",
            "dictamen": "CONFORME", "independencia": module.DECLARATION,
            "cobertura": {"fixture value and unit": [0]},
            "pasajes": [{
                "artefacto": self.source_path.relative_to(self.root).as_posix(),
                "sha256_artefacto": self.sha(self.source_path),
                "localizador": "Results, paragraph 1", "fragmento_control": "Fixture value 42.",
                "sha256_pasaje": hashlib.sha256(b"Fixture value 42.").hexdigest(),
            }], "limitaciones": "No scientific approval; fixture only.",
        }
        self.write_state()

    @staticmethod
    def sha(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def write_claim(self) -> None:
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=list(self.claim), lineterminator="\n")
        writer.writeheader()
        writer.writerow(self.claim)
        self.claim_path.write_text(stream.getvalue())

    def write_state(self, *, bind_proposal: bool = True) -> None:
        if bind_proposal:
            self.review["disposicion_sha256"] = module.proposal_hash(self.record)
        path = self.root / "docs/review.json"
        path.write_text(json.dumps(self.review, ensure_ascii=False) + "\n")
        self.record["revision_independiente"] = {"ruta": "docs/review.json", "sha256": self.sha(path)}
        self.registry.write_text(json.dumps({"version": 1, "disposiciones": [self.record]}, ensure_ascii=False))

    def load(self) -> dict:
        return module.load(self.root, [self.residual], [self.target], [self.correction],
                           start_bn=147, positive_claims={"C-2472", "C-2489"})

    def test_valid_delta_preserves_all_historical_inputs(self) -> None:
        before = copy.deepcopy((self.residual, self.target, self.correction))
        self.assertEqual(set(self.load()), {"C-2708"})
        self.assertEqual(before, (self.residual, self.target, self.correction))
        self.assertEqual(self.residual["resultado"], "NO_CONFORME")

    def test_missing_registry_or_revision_does_not_fall_back_to_approval(self) -> None:
        self.registry.unlink()
        with self.assertRaisesRegex(RuntimeError, "archivo ausente"):
            self.load()
        self.write_state()
        (self.root / "docs/review.json").unlink()
        with self.assertRaisesRegex(RuntimeError, "archivo ausente"):
            self.load()

    def test_corrected_residual_cannot_be_omitted_from_registry(self) -> None:
        self.registry.write_text('{"version":1,"disposiciones":[]}')
        with self.assertRaisesRegex(RuntimeError, "sin disposición revisada"):
            self.load()

    def test_duplicate_unknown_and_boolean_version_are_rejected(self) -> None:
        for raw in (
            '{"version":1,"version":1,"disposiciones":[]}',
            '{"version":true,"disposiciones":[]}',
            '{"version":1,"disposiciones":[],"approve":true}',
            json.dumps({"version": 1, "disposiciones": [self.record, self.record]}),
        ):
            with self.subTest(raw=raw):
                self.registry.write_text(raw)
                with self.assertRaises(RuntimeError):
                    self.load()

    def test_no_disposition_can_promote_a_literal_positive(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "positivo literal"):
            module.load(self.root, [self.residual], [self.target], [self.correction],
                        start_bn=147, positive_claims={"C-2708"})

    def test_all_nominal_identities_and_history_are_bound(self) -> None:
        for field, value in (
            ("fila", "8"), ("columna", "other"), ("bn", "BN-148"),
            ("sha256_residual", "0" * 64), ("contenido_previo", "other"),
            ("sha256_previo", "0" * 64), ("sha256_nuevo", "0" * 64),
            ("autor", "other-author"), ("contenido_nuevo", "different [C-9000]"),
        ):
            with self.subTest(field=field):
                original = self.record[field]
                self.record[field] = value
                self.write_state()
                with self.assertRaises(RuntimeError):
                    self.load()
                self.record[field] = original
        self.write_state()

    def test_self_review_old_date_and_nonconformity_rejected(self) -> None:
        for field, value in (
            ("revisor", "fictional-author"), ("fecha_utc", "2026-09-27T00:59:59Z"),
            ("fecha_utc", "2026-02-30T01:00:00Z"), ("fecha_utc", "2026-09-27"),
            ("dictamen", "PENDIENTE"), ("dictamen", "NO_CONFORME"),
            ("independencia", "self-certification"),
        ):
            with self.subTest(field=field):
                original = self.review[field]
                self.review[field] = value
                self.write_state()
                with self.assertRaises(RuntimeError):
                    self.load()
                self.review[field] = original

    def test_review_is_bound_to_exact_proposal(self) -> None:
        self.record["limites_pendientes"] = "Altered after adjudication."
        self.write_state(bind_proposal=False)
        with self.assertRaisesRegex(RuntimeError, "no ligada"):
            self.load()

    def test_review_and_source_files_cannot_change(self) -> None:
        for path in (self.source_path, self.author_path, self.root / "docs/review.json"):
            with self.subTest(path=path):
                original = path.read_bytes()
                path.write_bytes(original + b"\n")
                with self.assertRaisesRegex(RuntimeError, "artefacto obsoleto"):
                    self.load()
                path.write_bytes(original)

    def test_claim_change_invalidates_disposition(self) -> None:
        self.claim["Afirmación"] = "Changed value 43."
        self.write_claim()
        with self.assertRaisesRegex(RuntimeError, "C soporte ausente/obsoleta"):
            self.load()

    def test_synthesis_and_bn_cannot_be_direct_scientific_support(self) -> None:
        for field, value in (("Atribución", "sintesis(C-0001)"), ("Fuente", "BN-001")):
            with self.subTest(field=field):
                original = self.claim[field]
                self.claim[field] = value
                self.write_claim()
                self.record["afirmaciones_soporte"] = {"C-9000": module.row_hash(self.claim)}
                self.write_state()
                with self.assertRaises(RuntimeError):
                    self.load()
                self.claim[field] = original

    def test_missing_or_unrelated_source_is_rejected(self) -> None:
        self.claim["Fuente"] = "S02 Results"
        self.write_claim()
        self.record["afirmaciones_soporte"] = {"C-9000": module.row_hash(self.claim)}
        self.write_state()
        with self.assertRaisesRegex(RuntimeError, "no coinciden nominalmente"):
            self.load()

    def test_partial_components_or_non_nominal_passage_are_rejected(self) -> None:
        for field, value in (
            ("cobertura", {}), ("cobertura", {"fixture value and unit": []}),
            ("cobertura", {"fixture value and unit": [1]}),
            ("cobertura", {"fixture value and unit": [True]}),
            ("pasajes", []),
        ):
            with self.subTest(field=field):
                original = self.review[field]
                self.review[field] = value
                self.write_state()
                with self.assertRaises(RuntimeError):
                    self.load()
                self.review[field] = original

    def test_local_paths_cannot_escape_or_use_symlinks(self) -> None:
        reference = self.record["evidencia_autor"]
        for relative in ("../outside", "/tmp/outside", "docs/../docs/author.md", "docs//author.md"):
            with self.subTest(relative=relative):
                self.record["evidencia_autor"] = {"ruta": relative, "sha256": reference["sha256"]}
                self.write_state()
                with self.assertRaisesRegex(RuntimeError, "ruta no canónica"):
                    self.load()
        self.record["evidencia_autor"] = reference
        original = self.author_path.read_bytes()
        destination = self.root / "other.md"
        destination.write_bytes(original)
        self.author_path.unlink()
        self.author_path.symlink_to(destination)
        self.write_state()
        with self.assertRaisesRegex(RuntimeError, "symlink"):
            self.load()

    def test_source_mutation_after_first_read_is_detected_by_recheck(self) -> None:
        original = module._artifact
        calls = 0

        def changed(root: Path, reference: dict) -> bytes:
            nonlocal calls
            raw = original(root, reference)
            calls += 1
            if calls == 1:
                self.source_path.write_bytes(self.source_path.read_bytes() + b" ")
            return raw

        with patch.object(module, "_artifact", side_effect=changed):
            with self.assertRaisesRegex(RuntimeError, "artefacto obsoleto"):
                self.load()

    def test_claim_mutation_after_first_catalog_is_detected_by_recheck(self) -> None:
        original = module._claim_catalog
        calls = 0

        def changed(root: Path) -> dict:
            nonlocal calls
            catalog = original(root)
            calls += 1
            if calls == 1:
                self.claim["Afirmación"] = "Mutation after first read."
                self.write_claim()
            return catalog

        with patch.object(module, "_claim_catalog", side_effect=changed):
            with self.assertRaisesRegex(RuntimeError, "modificada durante"):
                self.load()

    def test_identity_aliases_and_placeholders_cannot_sign(self) -> None:
        for identity in (" fictional-author ", "FICTIONAL-AUTHOR", "ｆｉｃｔｉｏｎａｌ-author",
                         "NO_ASIGNADO", "pendiente", "n/a", "sin revisor"):
            with self.subTest(identity=identity):
                self.review["revisor"] = identity
                self.write_state()
                with self.assertRaises(RuntimeError):
                    self.load()

    def test_source_ranges_require_interior_but_not_supplementary_labels(self) -> None:
        self.claim["Fuente"] = "S01–S03 Results"
        self.write_claim()
        self.record["afirmaciones_soporte"] = {"C-9000": module.row_hash(self.claim)}
        self.write_state()
        with self.assertRaisesRegex(RuntimeError, "no coinciden nominalmente"):
            self.load()
        self.claim["Fuente"] = "S01 Results; supplementary fig. S03"
        self.write_claim()
        self.record["afirmaciones_soporte"] = {"C-9000": module.row_hash(self.claim)}
        self.write_state()
        self.assertEqual(set(self.load()), {"C-2708"})

    def test_source_noncanonical_alias_and_descending_range_rejected(self) -> None:
        for source in ("S1 Results", "S001 Results", "S03–S01 Results"):
            with self.subTest(source=source):
                self.claim["Fuente"] = source
                self.write_claim()
                self.record["afirmaciones_soporte"] = {"C-9000": module.row_hash(self.claim)}
                self.write_state()
                with self.assertRaises(RuntimeError):
                    self.load()

    def test_claim_csv_symlink_is_not_a_local_catalog(self) -> None:
        destination = self.root / "other.csv"
        destination.write_bytes(self.claim_path.read_bytes())
        self.claim_path.unlink()
        self.claim_path.symlink_to(destination)
        with self.assertRaisesRegex(RuntimeError, "symlink"):
            self.load()

    def test_same_cell_coordinates_in_a_different_taxon_invalidate_review(self) -> None:
        self.table_path.write_text(self.table_path.read_text().replace("fixture system", "different taxon"))
        with self.assertRaisesRegex(RuntimeError, "identidad taxonómica"):
            self.load()

    def test_claim_range_cannot_omit_interior_support(self) -> None:
        self.correction["contenido_corregido"] = "Fixture [C-9000–C-9002]"
        self.correction["contenido_corregido_sha256"] = module.cell_hash(self.correction["contenido_corregido"])
        self.record["contenido_nuevo"] = self.correction["contenido_corregido"]
        self.record["sha256_nuevo"] = self.correction["contenido_corregido_sha256"]
        self.record["afirmaciones_soporte"]["C-9002"] = "1" * 64
        self.write_state()
        with self.assertRaisesRegex(RuntimeError, "soportes no nominales"):
            self.load()


if __name__ == "__main__":
    unittest.main()
