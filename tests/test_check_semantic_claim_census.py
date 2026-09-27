import csv
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from scripts import check_semantic_claim_census as module


class SemanticClaimCensusTests(unittest.TestCase):
    def write_csv(self, path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle, fieldnames=header, quoting=csv.QUOTE_ALL,
                lineterminator="\n",
            )
            writer.writeheader()
            writer.writerows(rows)

    def test_load_csv_rejects_empty_evidence_field(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "primary.csv"
            row = {name: "x" for name in module.PRIMARY_HEADER}
            row["fragmento_control"] = ""
            self.write_csv(path, module.PRIMARY_HEADER, [row])
            _, errors = module.load_csv(path, module.PRIMARY_HEADER)
            self.assertTrue(any("fragmento_control" in error for error in errors))

    def test_canonical_json_rejects_noncanonical_serialization(self) -> None:
        errors: list[str] = []
        module.canonical_json('{"b": 1, "a": 2}', "campo", "C-001", errors)
        self.assertTrue(any("JSON canónico" in error for error in errors))

    def valid_primary(self) -> tuple[dict[str, str], dict[str, str], dict[str, dict[str, str]], dict[str, str]]:
        artifact = "fuentes/S01 [2019] fuente.xml"
        digest = "b" * 64
        expected = {
            "ruta": "data/afirmaciones/00.csv", "sha256_fila": "a" * 64,
            "atribucion": "expresa", "fuente": "S01 sección Results",
        }
        row = {name: "NO_APLICA" for name in module.PRIMARY_HEADER}
        row.update({
            "version_censo": "1", "id_afirmacion": "C-001",
            "ruta_canonica": expected["ruta"], "sha256_fila": expected["sha256_fila"],
            "atribucion": expected["atribucion"],
            "componentes_atomicos": '["proposición"]',
            "fuentes_declaradas": '["S01"]',
            "artefactos_verificados": json.dumps([artifact], ensure_ascii=False, separators=(",", ":")),
            "sha256_artefactos": json.dumps({artifact: digest}, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
            "localizador_declarado": expected["fuente"],
            "localizador_verificado": "S01 Results, párrafo 2",
            "fragmento_control": "fragmento nominal verificado",
            "sha256_pasaje": "c" * 64,
            "matriz_cobertura_componentes": '{"proposición":["S01:Results, párrafo 2"]}',
            "dependencias_y_huellas": "{}", "resultado": "CONFORME",
            "motivo_dictamen": "Todos los componentes coinciden con el pasaje nominal.",
            "revisor": "Revisor-E", "fecha_utc": "2026-08-13T12:00:00Z",
            "version_protocolo": "p",
        })
        return row, expected, {"C-001": expected}, {artifact: digest}

    def valid_secondary(self, key: str = "C-001") -> dict[str, str]:
        return {
            "version_revision": "1", "id_afirmacion": key,
            "sha256_fila": "a" * 64, "sha256_censo_primario": "",
            "resultado_independiente": "CONFORME",
            "localizadores_reinspeccionados": "S01 Results, párrafo 2",
            "sha256_pasajes_reinspeccionados": "c" * 64,
            "evidencia_dictamen": "Cotejo independiente de todos los componentes con el pasaje nominal.",
            "discrepancia": "NO", "resolucion_discrepancia": "NO_APLICA",
            "revisor_independiente": "Revisor-F",
            "declaracion_independencia": module.INDEPENDENCE_DECLARATION,
            "fecha_utc": "2026-08-13T13:00:00Z",
        }

    def validate_fixture(
        self, primary: list[dict[str, str]], secondary: list[dict[str, str]],
        frozen_at: object = "2026-08-13T11:00:00Z",
    ) -> list[str]:
        _, expected, _, catalog = self.valid_primary()
        inventory = {
            "version": "1", "version_protocolo": "p",
            "afirmaciones": {row["id_afirmacion"]: expected.copy() for row in primary},
            "archivos_control": {}, "artefactos_fuente": catalog,
            "artefactos_revision": {},
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            freeze_path, primary_path, secondary_path = (
                root / "freeze.json", root / "primary.csv", root / "secondary.csv",
            )
            freeze_path.write_text(
                json.dumps({**inventory, "fecha_congelacion": frozen_at}), encoding="utf-8",
            )
            self.write_csv(primary_path, module.PRIMARY_HEADER, primary)
            secondary = [dict(row, sha256_censo_primario=module.sha(primary_path)) for row in secondary]
            self.write_csv(secondary_path, module.SECONDARY_HEADER, secondary)
            with (
                patch.object(module, "ROOT", root),
                patch.object(module, "FREEZE", freeze_path),
                patch.object(module, "PRIMARY", primary_path),
                patch.object(module, "SECONDARY", secondary_path),
                patch.object(module, "inventory_payload", return_value=inventory),
            ):
                return module.validate()

    def test_later_real_review_dates_are_valid_without_backdating(self) -> None:
        primary, _, _, _ = self.valid_primary()
        secondary = self.valid_secondary()
        primary["fecha_utc"] = "2026-09-26T12:00:00Z"
        secondary["fecha_utc"] = "2026-09-27T12:00:00Z"
        self.assertEqual(self.validate_fixture([primary], [secondary]), [])

    def test_timestamps_reject_invalid_calendar_dates_and_noncanonical_utc(self) -> None:
        for value in (
            None, 2026, "2026-08-13", "2026-02-29T12:00:00Z",
            "2026-09-31T12:00:00Z", "2026-13-01T12:00:00Z",
            "2026-09-26T24:00:00Z", "2026-09-26T12:00:60Z",
            "2026-09-26T12:00:00+00:00", "2026-09-26T12:00:00.0Z",
            "0000-01-01T00:00:00Z", " 2026-09-26T12:00:00Z",
        ):
            with self.subTest(value=value):
                self.assertIsNone(module.parse_utc_timestamp(value))
        self.assertIsNotNone(module.parse_utc_timestamp("2028-02-29T12:00:00Z"))

    def test_validator_rejects_legacy_or_invalid_freeze_dates(self) -> None:
        primary, _, _, _ = self.valid_primary()
        for value in (None, "2026-08-13", "2026-02-30T11:00:00Z"):
            with self.subTest(value=value):
                errors = self.validate_fixture([primary], [self.valid_secondary()], value)
                self.assertTrue(any("fecha_congelacion" in error for error in errors))

    def test_primary_cannot_predate_freeze(self) -> None:
        primary, _, _, _ = self.valid_primary()
        primary["fecha_utc"] = "2026-08-13T10:59:59Z"
        errors = self.validate_fixture([primary], [self.valid_secondary()])
        self.assertTrue(any("primera revisión anterior a la congelación" in error for error in errors))

    def test_secondary_cannot_predate_freeze_or_primary(self) -> None:
        primary, _, _, _ = self.valid_primary()
        secondary = self.valid_secondary()
        secondary["fecha_utc"] = "2026-08-13T10:59:59Z"
        errors = self.validate_fixture([primary], [secondary])
        self.assertTrue(any("segunda revisión anterior a la congelación" in error for error in errors))
        self.assertTrue(any("anterior al cierre del censo primario completo" in error for error in errors))

    def test_secondary_must_follow_all_of_the_primary_census(self) -> None:
        first, _, _, _ = self.valid_primary()
        later = dict(first, id_afirmacion="C-002", fecha_utc="2026-08-13T14:00:00Z")
        second_later = self.valid_secondary("C-002")
        second_later["fecha_utc"] = "2026-08-13T15:00:00Z"
        errors = self.validate_fixture([first, later], [self.valid_secondary(), second_later])
        self.assertEqual(len(errors), 1)
        self.assertIn("C-001: segunda revisión anterior al cierre del censo primario completo", errors[0])

    def test_validator_rejects_invalid_secondary_calendar_date(self) -> None:
        primary, _, _, _ = self.valid_primary()
        secondary = self.valid_secondary()
        secondary["fecha_utc"] = "2026-02-30T13:00:00Z"
        errors = self.validate_fixture([primary], [secondary])
        self.assertTrue(any("fecha_utc independiente no es un instante UTC válido" in error for error in errors))

    def test_validation_does_not_consult_the_current_clock(self) -> None:
        class NoClock(datetime):
            @classmethod
            def now(cls, tz=None):
                raise AssertionError("verify no debe depender del reloj")

            @classmethod
            def utcnow(cls):
                raise AssertionError("verify no debe depender del reloj")

        primary, _, _, _ = self.valid_primary()
        with patch.object(module, "datetime", NoClock):
            self.assertEqual(self.validate_fixture([primary], [self.valid_secondary()]), [])

    def test_freeze_payload_is_deterministic_and_requires_valid_explicit_timestamp(self) -> None:
        with patch.object(module, "inventory_payload", return_value={"version": "1"}):
            first = module.freeze_payload("2026-09-26T12:00:00Z")
            self.assertEqual(first, module.freeze_payload("2026-09-26T12:00:00Z"))
            self.assertEqual(first["fecha_congelacion"], "2026-09-26T12:00:00Z")
            with self.assertRaises(ValueError):
                module.freeze_payload("2026-08-13")

    def test_write_freeze_requires_timestamp_and_does_not_mutate_on_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            freeze_path = Path(directory) / "freeze.json"
            freeze_path.write_bytes(b"conservar")
            for args in (
                ["--write-freeze"],
                ["--write-freeze", "--fecha-congelacion-utc", "2026-02-30T12:00:00Z"],
                ["--fecha-congelacion-utc", "2026-09-26T12:00:00Z"],
            ):
                with self.subTest(args=args), patch.object(module, "FREEZE", freeze_path):
                    with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
                        module.main(args)
                    self.assertEqual(raised.exception.code, 2)
                    self.assertEqual(freeze_path.read_bytes(), b"conservar")

    def test_review_catalog_excludes_but_does_not_drop_control_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            appendix = root / "data/apendices"
            appendix.mkdir(parents=True)
            source = appendix / "A_fuentes.csv"
            other = appendix / "B_entidades.csv"
            source.write_text("fuentes", encoding="utf-8")
            other.write_text("entidades", encoding="utf-8")
            with patch.object(module, "ROOT", root):
                reviews = module.review_artifacts()
                self.assertNotIn("data/apendices/A_fuentes.csv", reviews)
                self.assertEqual(reviews, {"data/apendices/B_entidades.csv": module.sha(other)})
                errors: list[str] = []
                catalog = module.artifact_catalog({
                    "archivos_control": {"data/apendices/A_fuentes.csv": module.sha(source)},
                    "artefactos_fuente": {}, "artefactos_revision": reviews,
                }, errors)
                self.assertEqual(errors, [])
                self.assertEqual(catalog["data/apendices/A_fuentes.csv"], module.sha(source))

    def test_duplicate_catalog_entries_still_fail(self) -> None:
        duplicate = {"data/apendices/A_fuentes.csv": "a" * 64}
        errors: list[str] = []
        module.artifact_catalog({
            "archivos_control": duplicate, "artefactos_fuente": {},
            "artefactos_revision": duplicate,
        }, errors)
        self.assertTrue(any("rutas duplicadas" in error for error in errors))

    def test_primary_evidence_accepts_exact_frozen_artifact_and_coverage(self) -> None:
        row, expected, claims, catalog = self.valid_primary()
        errors: list[str] = []
        module.validate_primary_evidence(row, expected, claims, catalog, errors)
        self.assertEqual(errors, [])

    def test_primary_evidence_rejects_fabricated_hash_and_coverage(self) -> None:
        row, expected, claims, catalog = self.valid_primary()
        artifact = next(iter(catalog))
        row["sha256_artefactos"] = json.dumps(
            {artifact: "d" * 64}, sort_keys=True, separators=(",", ":"),
        )
        row["matriz_cobertura_componentes"] = '{"proposición":["S999:pasaje"]}'
        errors: list[str] = []
        module.validate_primary_evidence(row, expected, claims, catalog, errors)
        self.assertTrue(any("no coincide con artefactos congelados" in error for error in errors))
        self.assertTrue(any("evidencia no declarada" in error for error in errors))

    def test_primary_evidence_rejects_missing_synthesis_dependency_hash(self) -> None:
        row, expected, claims, catalog = self.valid_primary()
        expected["atribucion"] = "sintesis(C-002)"
        row["atribucion"] = expected["atribucion"]
        claims["C-002"] = {
            "ruta": "data/afirmaciones/00.csv", "sha256_fila": "e" * 64,
            "atribucion": "glosa", "fuente": "n/a",
        }
        errors: list[str] = []
        module.validate_primary_evidence(row, expected, claims, catalog, errors)
        self.assertTrue(any("dependencias_y_huellas" in error for error in errors))

    def test_url_stub_is_not_a_semantic_source_artifact(self) -> None:
        self.assertFalse(module.source_artifact_matches("S01", "fuentes/S01 fuente.url"))

    def test_declared_refs_expand_ranges_and_ignore_supplementary_labels(self) -> None:
        self.assertEqual(
            module.declared_source_refs(
                "S27 Results; figs. S62–S63; S531–S533; BN-001–BN-003"
            ),
            ["S27", "S531", "S532", "S533", "BN-001", "BN-002", "BN-003"],
        )
        self.assertEqual(
            module.declared_claim_dependencies("sintesis(C-358–C-360, C-427)"),
            ["C-358", "C-359", "C-360", "C-427"],
        )

    def test_validator_rejects_self_review(self) -> None:
        claim = {
            "ruta": "data/afirmaciones/00.csv",
            "sha256_fila": "a" * 64,
            "atribucion": "glosa",
            "fuente": "n/a",
        }
        freeze = {
            "version": "1", "fecha_congelacion": "2026-08-13T11:00:00Z",
            "version_protocolo": "p", "afirmaciones": {"C-001": claim},
            "archivos_control": {}, "artefactos_fuente": {},
            "artefactos_revision": {},
        }
        primary = {name: "x" for name in module.PRIMARY_HEADER}
        primary.update({
            "id_afirmacion": "C-001", "ruta_canonica": claim["ruta"],
            "sha256_fila": claim["sha256_fila"], "atribucion": "glosa",
            "componentes_atomicos": "[]", "fuentes_declaradas": "[]",
            "artefactos_verificados": "[]", "sha256_artefactos": "{}",
            "matriz_cobertura_componentes": "{}",
            "dependencias_y_huellas": "{}", "resultado": "CONFORME",
            "revisor": "mismo", "version_protocolo": "p",
        })
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            freeze_path = root / "freeze.json"
            primary_path = root / "primary.csv"
            secondary_path = root / "secondary.csv"
            freeze_path.write_text(__import__("json").dumps(freeze), encoding="utf-8")
            self.write_csv(primary_path, module.PRIMARY_HEADER, [primary])
            secondary = {name: "x" for name in module.SECONDARY_HEADER}
            secondary.update({
                "id_afirmacion": "C-001", "sha256_fila": claim["sha256_fila"],
                "sha256_censo_primario": module.sha(primary_path),
                "resultado_independiente": "CONFORME", "discrepancia": "NO",
                "revisor_independiente": "mismo",
                "declaracion_independencia": "revisión independiente",
            })
            self.write_csv(secondary_path, module.SECONDARY_HEADER, [secondary])
            with (
                patch.object(module, "FREEZE", freeze_path),
                patch.object(module, "PRIMARY", primary_path),
                patch.object(module, "SECONDARY", secondary_path),
                patch.object(module, "inventory_payload", return_value={
                    name: value for name, value in freeze.items() if name != "fecha_congelacion"
                }),
            ):
                errors = module.validate()
            self.assertTrue(any("auto-revisión" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
