import csv
import json
import tempfile
import unittest
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
        })
        return row, expected, {"C-001": expected}, {artifact: digest}

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
            "version": "1", "fecha_congelacion": "2026-08-13",
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
                patch.object(module, "freeze_payload", return_value=freeze),
            ):
                errors = module.validate()
            self.assertTrue(any("auto-revisión" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
