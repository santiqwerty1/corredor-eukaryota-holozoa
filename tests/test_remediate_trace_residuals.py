from __future__ import annotations

import csv
import hashlib
import io
import itertools
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import remediate_trace_residuals as module


class TraceResidualRemediationTests(unittest.TestCase):
    def test_index_matches_original_exact_cooccurrence_for_all_components(self) -> None:
        texts = [
            module.normalized(value)
            for value in ("Alpha beta", "ALPHA\n\tGAMMA", "Straße", "STRASSE", "áβ\x00x", "")
        ]
        index = module.ExactCooccurrenceIndex(texts)
        vocabulary = ["alpha", "beta", "gamma", "strasse", "áβ", "\x00", "x", "", "missing"]
        for length in range(4):
            for components in itertools.product(vocabulary, repeat=length):
                with self.subTest(components=components):
                    expected = sum(all(component in text for component in components) for text in texts)
                    self.assertEqual(index.count(list(components)), expected)
        self.assertEqual(module.ExactCooccurrenceIndex([]).count([]), 0)

    def test_index_does_not_rescan_cached_exact_components(self) -> None:
        calls: list[tuple[str, str]] = []

        class CountingText(str):
            def __contains__(self, component: str) -> bool:
                calls.append((str(self), component))
                return super().__contains__(component)

        index = module.ExactCooccurrenceIndex([
            CountingText("alpha beta gamma"), CountingText("alpha beta"),
        ])
        self.assertEqual(index.count(["alpha", "beta"]), 2)
        self.assertEqual(index.count(["alpha", "beta", "gamma"]), 1)
        self.assertEqual(index.count(["beta", "alpha", "beta"]), 2)
        self.assertEqual(len(calls), 6)
        self.assertEqual(set(index.matches), {"alpha", "beta", "gamma"})

    def test_snapshot_keeps_binary_url_and_hidden_artifacts_with_original_normalization(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources = root / "fuentes"
            sources.mkdir()
            (sources / "directory").mkdir()
            files = {
                "S01.pdf": b"\xffPDF\x00 ALPHA\r\n Beta\x80",
                "S02.url": b"HTTPS://example.test\n",
                ".metadata": "Straße\táβ".encode("utf-8"),
            }
            for name, payload in files.items():
                (sources / name).write_bytes(payload)
            with patch.object(module, "ROOT", root):
                texts, digest, count = module.source_snapshot()
            expected_records = [
                (name, hashlib.sha256(payload).hexdigest(), str(len(payload)))
                for name, payload in sorted(files.items())
            ]
            inventory = "\n".join("\0".join(row) for row in expected_records) + "\n"
            self.assertEqual(count, 3)
            self.assertEqual(digest, hashlib.sha256(inventory.encode()).hexdigest())
            self.assertEqual(texts, [
                " ".join(payload.decode("utf-8", errors="ignore").casefold().split())
                for _, payload in sorted(files.items())
            ])

    def test_index_preserves_short_circuit_and_fills_partial_cache_on_later_queries(self) -> None:
        index = module.ExactCooccurrenceIndex(["alpha common", "beta common", "gamma common"])
        self.assertEqual(index.count(["alpha", "common"]), 1)
        self.assertEqual(index.checked["common"], {0})
        self.assertEqual(index.count(["beta", "common"]), 1)
        self.assertEqual(index.checked["common"], {0, 1})
        self.assertEqual(index.count(["missing", "common"]), 0)
        self.assertEqual(index.checked["common"], {0, 1})
        self.assertEqual(index.count(["common"]), 3)
        self.assertEqual(index.checked["common"], {0, 1, 2})

    def build_fixture(
        self, root: Path, *, include_bn557: bool = True,
        residual_count: int = 410, missing_positive: bool = False,
        restore_bn120: bool = False, restore_bn132: bool = False,
        restore_bn133: bool = False, restore_bn146: bool = False,
        restore_bn144: bool = False,
        omit_other_bn: str | None = None,
    ) -> tuple[dict[Path, bytes], dict[str, tuple[str, int]], dict[str, str]]:
        def write(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(module.csv_bytes(header, rows))

        residual_path = root / "residuals.csv"
        correction_path = root / "corrections.csv"
        from scripts import build_atomic_cell_claims as atomic
        write(correction_path, atomic.CORRECTION_HEADER, [])
        registry_path = root / "data/auditoria/disposiciones_residuales_semanticas_v1.json"
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        registry_path.write_text('{"version":1,"disposiciones":[]}', encoding="utf-8")
        table_path = root / "data/tablas/02/table.csv"
        target_paths = (root / "target1.csv", root / "target2.csv")
        manifest_path = root / "manifest.csv"
        claims_path = root / "claims.csv"
        magnitudes_path = root / "magnitudes.csv"
        narrative_path = root / "narrative.md"
        bn_path = root / "data/busquedas_negativas/15_1_15-1-punto-de-partida-y-participantes-celulares.csv"
        ids = ["C-2472", "C-2489"] + [f"C-{9001 + i}" for i in range(408)]
        if missing_positive:
            ids[0] = "C-9999"
        residuals = []
        for index, claim in enumerate(ids[:residual_count]):
            residuals.append({
                "claim_id": claim, "csv_path": "data/tablas/02/table.csv",
                "fila": str(index + 2), "columna": "campo",
                "contenido_anterior": f"valor-{index}",
                "contenido_sha256": module.digest_cell(f"valor-{index}"),
                "origen_revision": "Revisor independiente de prueba",
                "resultado": "NO_CONFORME", "evidencia": "rechazo nominal",
                "localizadores": "localizador de prueba",
            })
        write(residual_path, module.RESIDUAL_HEADER, residuals)
        write(table_path, ["nodo", "campo"], [
            {"nodo": f"identidad-{index}", "campo": f"valor-{index}"}
            for index in range(len(residuals))
        ])
        target_header = ["claim_id", "contenido", "contenido_sha256", "evidencia_dictamen", "resultado"]
        for target_index, path in enumerate(target_paths):
            write(path, target_header, [{
                "claim_id": row["claim_id"], "contenido": row["contenido_anterior"],
                "contenido_sha256": row["contenido_sha256"],
                "evidencia_dictamen": "NO_CONFORME independiente conservado.",
                "resultado": "NO_CONFORME",
            } for row in residuals] if target_index == 0 else [])
        manifest_header = ["csv_path", "fila", "columna", "contenido", "contenido_sha256", "nota_adjudicacion"]
        write(manifest_path, manifest_header, [{
            "csv_path": row["csv_path"], "fila": row["fila"], "columna": row["columna"],
            "contenido": row["contenido_anterior"], "contenido_sha256": row["contenido_sha256"],
            "nota_adjudicacion": "NO_CONFORME independiente conservado.",
        } for row in residuals])
        bn_header = ["clave", "estado", "hueco", "términos exactos", "resultado"]
        bn_rows = [{
            # Cinco de las 77 negativas previas representan retiradas
            # nominales; el censo v3 sigue fijo en 408.
            "clave": "BN-{:03d}".format({73: 144, 74: 133, 75: 146, 76: 132, 77: 120}.get(index, index)),
            "estado": "NO LOCALIZADO EN ESTA SESIÓN" if index <= 77 else "LA LITERATURA DECLARA QUE NO SE SABE",
            "hueco": "hueco anterior", "términos exactos": "consulta anterior",
            "resultado": "resultado anterior",
        } for index in range(1, 90)]
        bn_rows = [
            row for row in bn_rows
            if (restore_bn120 or row["clave"] != "BN-120")
            and (restore_bn132 or row["clave"] != "BN-132")
            and (restore_bn133 or row["clave"] != "BN-133")
            and (restore_bn146 or row["clave"] != "BN-146")
            and (restore_bn144 or row["clave"] != "BN-144")
            and row["clave"] != omit_other_bn
        ]
        bn557 = {
            "clave": "BN-557", "estado": "NO LOCALIZADO EN ESTA SESIÓN",
            "hueco": "edad de corona de Breviatea con muestreo interno en S126 S1 Data",
            "términos exactos": "Breviatea|Pygsuia|Nutomonas; inspección de S1 Data",
            "resultado": "Resultado científico nominal ajeno a las consultas v3.",
        }
        if include_bn557:
            bn_rows.append(bn557)
        bn_rows.append({
            "clave": "BN-558", "estado": "NO LOCALIZADO EN ESTA SESIÓN",
            "hueco": "cifra nominal de corona de Amorphea en S548 publicado",
            "términos exactos": "Amorphea; JATS y suplementos publicados de S548",
            "resultado": "Resultado científico nominal ajeno a las consultas v3.",
        })
        write(bn_path, bn_header, bn_rows)
        write(claims_path, ["#", "Afirmación", "Objeto", "Motivo"], [
            {"#": key, "Afirmación": "anterior", "Objeto": "anterior", "Motivo": "anterior"}
            for key in ("C-1931", "C-1933")
        ])
        write(magnitudes_path, ["magnitud", "valor tal como lo publica la fuente"], [
            {"magnitud": name, "valor tal como lo publica la fuente": "anterior"}
            for name in ("búsquedas negativas activas", "búsquedas sin resultado localizado")
        ])
        narrative_path.write_text("Prosa sin dictamen", encoding="utf-8")
        with (
            patch.object(module, "ROOT", root),
            patch.object(module, "RESIDUALS", residual_path),
            patch.object(module, "CORRECTIONS", correction_path),
            patch.object(module, "TARGETS", target_paths),
            patch.object(module, "MANIFEST", manifest_path),
            patch.object(module, "CLAIMS", claims_path),
            patch.object(module, "MAGNITUDES", magnitudes_path),
            patch.object(module, "NARRATIVE", narrative_path),
            patch.object(module, "source_snapshot", return_value=(
                ["identidad-0 campo valor-0", "identidad-1 campo valor-1"], "a" * 64, 431,
            )),
        ):
            payloads, probes = module.build()
        return payloads, probes, bn557

    def test_build_preserves_bn557_and_408_generated_negative_queries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads, probes, bn557 = self.build_fixture(root)
            negative_payload = next(value for path, value in payloads.items() if "busquedas_negativas" in path.parts)
            negatives = list(csv.DictReader(io.StringIO(negative_payload.decode())))
            self.assertEqual(len(negatives), 494)
            self.assertNotIn("BN-120", {row["clave"] for row in negatives})
            self.assertNotIn("BN-132", {row["clave"] for row in negatives})
            self.assertNotIn("BN-133", {row["clave"] for row in negatives})
            self.assertNotIn("BN-146", {row["clave"] for row in negatives})
            self.assertNotIn("BN-144", {row["clave"] for row in negatives})
            self.assertEqual(next(row for row in negatives if row["clave"] == "BN-557"), bn557)
            self.assertEqual(sum(module.GENERATED_MARKER in " ".join(row.values()) for row in negatives), 408)
            self.assertEqual(len(probes), 408)
            self.assertNotIn("BN-557", probes)
            self.assertNotIn("BN-558", probes)
            self.assertEqual(
                next(row for row in negatives if row["clave"] == "BN-558")["términos exactos"],
                "Amorphea; JATS y suplementos publicados de S548",
            )
            self.assertTrue(all(count == 0 for _, count in probes.values()))
            claims = list(csv.DictReader(io.StringIO(payloads[root / "claims.csv"].decode())))
            claim = next(row for row in claims if row["#"] == "C-1933")
            self.assertEqual(claim["Afirmación"], "482 búsquedas negativas están marcadas NO LOCALIZADO EN ESTA SESIÓN.")
            self.assertEqual(claim["Objeto"], "482 filas")
            target = list(csv.DictReader(io.StringIO(payloads[root / "target1.csv"].decode())))
            self.assertTrue(all("pendiente de nueva revisión independiente" in row["evidencia_dictamen"] for row in target))
            self.assertTrue(all(row["resultado"] == "NO_CONFORME" for row in target))

    def test_build_rejects_loss_of_bn557(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(RuntimeError, "Recuento BN inesperado"):
                self.build_fixture(Path(directory), include_bn557=False)

    def test_retired_negatives_cannot_return_or_replace_other_negatives(self) -> None:
        for kwargs, error in (
            ({"restore_bn120": True}, "Recuento BN inesperado"),
            ({"omit_other_bn": "BN-001"}, "Recuento BN inesperado"),
            ({"restore_bn120": True, "omit_other_bn": "BN-001"}, "reintroduce BN retiradas"),
            ({"restore_bn132": True}, "Recuento BN inesperado"),
            ({"restore_bn132": True, "omit_other_bn": "BN-001"}, "reintroduce BN retiradas"),
            ({"restore_bn133": True}, "Recuento BN inesperado"),
            ({"restore_bn133": True, "omit_other_bn": "BN-001"}, "reintroduce BN retiradas"),
            ({"restore_bn146": True}, "Recuento BN inesperado"),
            ({"restore_bn146": True, "omit_other_bn": "BN-001"}, "reintroduce BN retiradas"),
            ({"restore_bn144": True}, "Recuento BN inesperado"),
            ({"restore_bn144": True, "omit_other_bn": "BN-001"}, "reintroduce BN retiradas"),
        ):
            with self.subTest(kwargs=kwargs), tempfile.TemporaryDirectory() as directory:
                with self.assertRaisesRegex(RuntimeError, error):
                    self.build_fixture(Path(directory), **kwargs)

    def test_bn120_history_retains_rows_and_does_not_credit_old_date(self) -> None:
        path = Path(__file__).resolve().parents[1] / "docs/auditorias/retirada_bn120_2026-09-26.json"
        history = json.loads(path.read_text(encoding="utf-8"))
        expected = {
            "bn_previa": "93f842a7e278911b6160bac9149fd5bbd7b7f6c9395bd707ba147b3cf16c5248",
            "q_previa": "fbfd8a456662ce31de0c0f9065d3f84f45d43abc0b2b6ef875b2887823e6d74a",
        }
        for key, digest in expected.items():
            record = history[key]
            encoded = (json.dumps(record["fila"], ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
            self.assertEqual(hashlib.sha256(encoded).hexdigest(), digest)
            self.assertEqual(record["huella_fila_json_sha256"], digest)
            self.assertEqual(set(record["cabecera"]), set(record["fila"]))
        self.assertEqual(history["fecha_original_declarada"], "2026-08-13")
        self.assertTrue(history["acreditacion_fecha_original"].startswith("NO_ACREDITADA:"))
        self.assertIn("2026-09-26T22:07:15Z; REINSPECCION", history["reinspeccion_bn"])
        self.assertIn("2026-09-26T22:25:54Z", history["cotejo_s434"])
        self.assertEqual(len(history["huellas_bn_activas_antes"]), 499)
        self.assertEqual(history["huellas_bn_activas_antes"]["BN-120"], expected["bn_previa"])
        self.assertEqual({item["fila"]["#"] for item in history["afirmaciones_positivas"]}, {"C-2821", "C-2822"})

    def test_bn132_retirement_preserves_history_and_distinct_units(self) -> None:
        path = Path(__file__).resolve().parents[1] / "docs/auditorias/retirada_bn132_2026-09-26.json"
        history = json.loads(path.read_text(encoding="utf-8"))
        expected = {
            "bn_previa": "f959d62895a3206acd331bcee7604117d59af36ab607419aa66ff16060ebb2d5",
            "q_previa": "9b2f1d0303bf05b2dbc4c820244995a9fe7d66e30fa59db271f981e8fd8e1453",
            "afirmacion_previa": "c59688ac315b1fad9837a7ec679954c23661f55ba70268976d6bc701f1cad923",
        }
        for key, digest in expected.items():
            record = history[key]
            encoded = (json.dumps(record["fila"], ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
            self.assertEqual(hashlib.sha256(encoded).hexdigest(), digest)
            self.assertEqual(record["huella_fila_json_sha256"], digest)
            self.assertEqual(set(record["cabecera"]), set(record["fila"]))
        self.assertEqual(len(history["huellas_bn_activas_antes"]), 498)
        self.assertNotIn("BN-120", history["huellas_bn_activas_antes"])
        self.assertEqual(history["huellas_bn_activas_antes"]["BN-132"], expected["bn_previa"])
        self.assertEqual(history["fecha_original_declarada"], "2026-08-13")
        self.assertTrue(history["acreditacion_fecha_original"].startswith("NO_ACREDITADA:"))
        self.assertTrue(history["estado_revision_independiente"].startswith("PENDIENTE"))
        positive = {item["fila"]["#"]: item["fila"] for item in history["afirmaciones_positivas"]}
        self.assertEqual(set(positive), {"C-1163", "C-2824"})
        self.assertEqual(positive["C-1163"]["Objeto"], "4459 genes entre 427186 genes de 30 genomas eucariotas")
        self.assertEqual(positive["C-2824"]["Objeto"], "394 familias de genes")
        self.assertEqual(history["fuente_positiva"]["fila"]["clave"], "S560")

    def test_build_still_requires_410_residuals_and_the_two_nominal_positives(self) -> None:
        for kwargs, error in (
            ({"residual_count": 409}, "exactamente 410"),
            ({"missing_positive": True}, "dos pasajes positivos nominales"),
        ):
            with self.subTest(kwargs=kwargs), tempfile.TemporaryDirectory() as directory:
                with self.assertRaisesRegex(RuntimeError, error):
                    self.build_fixture(Path(directory), **kwargs)

    def test_nominal_query_has_three_real_components(self) -> None:
        query = (
            "identidad=«Hedgehog»; campo=«Metazoa»; valor=«presente»"
        )
        self.assertEqual(
            module.nominal_components(query),
            ["hedgehog", "metazoa", "presente"],
        )

    def test_gap_never_promotes_zero_hits_to_scientific_absence(self) -> None:
        value = module.gap_value("BN-147")
        self.assertIn("no se adjudica un valor", value)
        self.assertNotIn("carece", value.casefold())
        self.assertNotIn("ausente", value.casefold())

    def test_known_positive_cells_cannot_be_materialized_as_negative(self) -> None:
        self.assertEqual(module.POSITIVE_CLAIMS, {"C-2472", "C-2489"})


if __name__ == "__main__":
    unittest.main()
