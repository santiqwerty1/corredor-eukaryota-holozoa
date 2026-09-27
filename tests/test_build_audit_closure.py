"""Fixtures probatorias artificiales: nunca crean firmas en el corpus real."""
from __future__ import annotations

import json
import argparse
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import audit_chronology as chronology
from scripts import build_audit_deliverables as b


def write(root: Path, relative: str, data: str | bytes) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data.encode() if isinstance(data, str) else data)
    return path


def json_string(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def claim(key: str = "C-001") -> dict[str, str]:
    return {
        **dict.fromkeys(b.CLAIM_COLUMNS, "Fixture"), "#": key,
        "Afirmación": "Organismo presenta carácter en la muestra.",
        "Sujeto": "Organismo", "Predicado": "presenta", "Objeto": "carácter",
        "Atribución": "expresa", "Fuente": "S01 Results, párrafo 2",
        "Aceptación": "no evaluado",
    }


def nominal(root: Path, key: str, fingerprint: str, axis: str) -> dict[str, str]:
    proof = write(root, "docs/prueba_nominal.txt", "Fixture de prueba independiente, sin aprobación real.")
    return {
        "version_revision": "1", "estrato": "AFIRMACION" if key.startswith("C-") else "FUENTE",
        "clave_objeto": key, "huella_objeto_sha256": fingerprint, "eje": axis,
        "resultado": "CONFORME", "autor_version": "Autor-Fixture",
        "revisor_independiente": "Revisor-Fixture",
        "declaracion_independencia": b.NOMINAL_INDEPENDENCE,
        "fecha_version_utc": "2026-09-26T09:00:00Z", "fecha_revision_utc": "2026-09-26T10:00:00Z",
        "artefactos_inspeccionados": json_string({"docs/prueba_nominal.txt": b.sha256_file(proof)}),
        "evidencia_local": "docs/prueba_nominal.txt", "huella_evidencia_sha256": b.sha256_file(proof),
        "localizador_evidencia": "párrafo 1", "alcance": f"Fixture nominal de {key}, eje {axis}.",
        "dictamen": f"Fixture independiente del eje {axis}, de la versión exacta {key}.",
        "limitaciones": "Solo fixture de test; no constituye revisión científica.",
    }


def write_nominal(root: Path, rows: list[dict[str, str]]) -> None:
    write(root, str(b.NOMINAL_REVIEWS), b.csv_payload(b.NOMINAL_REVIEW_COLUMNS, rows))


def census_fixture(root: Path, extra_axes: bool = False):
    row = claim()
    write(root, "data/afirmaciones/00.csv", b.csv_payload(b.CLAIM_COLUMNS, [row]))
    write(root, "data/table_index.json", json_string({"tables": [{
        "category": "claims", "section": "00", "csv_path": "data/afirmaciones/00.csv",
    }]}))
    write(root, "data/table_lineage.csv", "fixture\n")
    for path in ("data/apendices/A_fuentes.csv", str(b.SOURCE_MATRIX_PATH), "exports/acceso_fuentes.csv"):
        write(root, path, "fixture\n")
    write(root, "docs/auditorias/protocolo_censo_semantico_2026-08-13.md", "Protocolo fixture explícito.\n")
    artifact = "fuentes/S01.xml"
    artifact_path = write(root, artifact, "<article>Organismo presenta carácter en la muestra.</article>")
    if extra_axes:
        write_nominal(root, [nominal(root, row["#"], b.claim_fingerprint(row), axis) for axis in b.EXTRA_CLAIM_AXES])
    module = b.semantic_census_module(root)
    write(root, str(module.FREEZE.relative_to(root)), json_string(module.freeze_payload("2026-09-26T11:00:00Z")))
    expected = module.claim_inventory()[row["#"]]
    primary = dict.fromkeys(module.PRIMARY_HEADER, "NO_APLICA")
    primary.update({
        "version_censo": "1", "id_afirmacion": row["#"], "ruta_canonica": expected["ruta"],
        "sha256_fila": expected["sha256_fila"], "atribucion": row["Atribución"],
        "componentes_atomicos": '["proposición"]', "fuentes_declaradas": '["S01"]',
        "artefactos_verificados": json_string([artifact]),
        "sha256_artefactos": json_string({artifact: b.sha256_file(artifact_path)}),
        "localizador_declarado": row["Fuente"], "localizador_verificado": "S01 Results, párrafo 2",
        "fragmento_control": "Organismo presenta carácter en la muestra.", "sha256_pasaje": "c" * 64,
        "matriz_cobertura_componentes": '{"proposición":["S01:Results, párrafo 2"]}',
        "dependencias_y_huellas": "{}", "resultado": "CONFORME",
        "motivo_dictamen": "Todos los componentes nominales fueron cotejados en esta fixture.",
        "revisor": "Primario-Fixture", "fecha_utc": "2026-09-26T12:00:00Z",
        "version_protocolo": b.sha256_file(module.PROTOCOL),
    })
    write(root, str(module.PRIMARY.relative_to(root)), b.csv_payload(module.PRIMARY_HEADER, [primary]))
    secondary = {
        "version_revision": "1", "id_afirmacion": row["#"], "sha256_fila": expected["sha256_fila"],
        "sha256_censo_primario": b.sha256_file(module.PRIMARY), "resultado_independiente": "CONFORME",
        "localizadores_reinspeccionados": "S01 Results, párrafo 2", "sha256_pasajes_reinspeccionados": "c" * 64,
        "evidencia_dictamen": "Reinspección independiente nominal de todos los componentes de la fixture.",
        "discrepancia": "NO", "resolucion_discrepancia": "NO_APLICA", "revisor_independiente": "Segundo-Fixture",
        "declaracion_independencia": module.INDEPENDENCE_DECLARATION, "fecha_utc": "2026-09-26T13:00:00Z",
    }
    write(root, str(module.SECONDARY.relative_to(root)), b.csv_payload(module.SECONDARY_HEADER, [secondary]))
    return row, module, primary, secondary


class ClaimClosureTests(unittest.TestCase):
    def test_attribution_and_hole_words_never_approve(self):
        for attr in ("expresa", "glosa", "sintesis(C-001)"):
            row = {**claim(), "Atribución": attr, "Resolución": "hueco; información insuficiente"}
            axes = b.final_claim_axes([row])
            self.assertEqual(set(axes.values()), {"PENDIENTE"})
            self.assertEqual(b.claim_closure(axes), "ABIERTO")
        self.assertEqual(set(b.final_claim_axes([{"Atribución": "expresa", "Aceptación": "no evaluado"}]).values()), {"PENDIENTE"})

    def test_full_census_cannot_approve_unreviewed_axes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row, module, _, _ = census_fixture(root)
            self.assertEqual(module.validate(), [])
            evidence = b.load_claim_review_evidence(root)
            self.assertEqual(evidence.errors, ())
            axes = b.final_claim_axes([row], evidence)
            self.assertTrue(all(axes[axis] == "CONFORME" for axis in b.SEMANTIC_AXES))
            self.assertTrue(all(axes[axis] == "PENDIENTE" for axis in b.EXTRA_CLAIM_AXES))
            self.assertEqual(b.claim_closure(axes), "ABIERTO")
            self.assertNotEqual(b.claim_fingerprint(row), module.claim_inventory()[row["#"]]["sha256_fila"])

    def test_complete_nominal_evidence_is_deterministic_and_root_isolated(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row, _, _, _ = census_fixture(root, extra_axes=True)
            first = b.load_claim_review_evidence(root)
            second = b.load_claim_review_evidence(root)
            self.assertEqual(first, second)
            self.assertEqual(b.claim_closure(b.final_claim_axes([row], first)), "CERRADO")
            with tempfile.TemporaryDirectory() as other:
                self.assertTrue(b.load_claim_review_evidence(Path(other)).errors)
            self.assertEqual(first, b.load_claim_review_evidence(root))

    def test_absent_obsolete_discrepant_and_changed_primary_remain_open(self):
        for mutation in ("absent", "claim", "artifact", "discrepancy", "primary", "self_review", "negative"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                row, module, primary, secondary = census_fixture(root)
                if mutation == "absent":
                    module.PRIMARY.unlink()
                elif mutation == "claim":
                    row["Objeto"] = "otro carácter"
                    write(root, "data/afirmaciones/00.csv", b.csv_payload(b.CLAIM_COLUMNS, [row]))
                elif mutation == "artifact":
                    write(root, "fuentes/S01.xml", "versión distinta")
                elif mutation == "primary":
                    primary["motivo_dictamen"] += " Texto posterior a la segunda revisión."
                    write(root, str(module.PRIMARY.relative_to(root)), b.csv_payload(module.PRIMARY_HEADER, [primary]))
                else:
                    if mutation == "discrepancy":
                        secondary["discrepancia"] = "SI"
                    elif mutation == "self_review":
                        secondary["revisor_independiente"] = primary["revisor"]
                    else:
                        secondary["resultado_independiente"] = "NO_CONFORME"
                    write(root, str(module.SECONDARY.relative_to(root)), b.csv_payload(module.SECONDARY_HEADER, [secondary]))
                evidence = b.load_claim_review_evidence(root)
                self.assertTrue(evidence.errors)
                self.assertEqual(b.claim_closure(b.final_claim_axes([row], evidence)), "ABIERTO")

    def test_in_memory_claim_change_does_not_reuse_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row, _, _, _ = census_fixture(root, extra_axes=True)
            evidence = b.load_claim_review_evidence(root)
            row["Fuente"] += "; localizador diferente"
            self.assertEqual(set(b.final_claim_axes([row], evidence).values()), {"PENDIENTE"})

    def test_change_during_validation_or_linking_never_closes(self):
        for phase in ("validation", "linking"):
            for target in ("source", "primary", "secondary", "nominal_document"):
                with self.subTest(phase=phase, target=target), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    row, module, _, _ = census_fixture(root, extra_axes=True)
                    self.assertEqual(module.validate(), [])
                    paths = {
                        "source": root / "fuentes/S01.xml",
                        "primary": module.PRIMARY,
                        "secondary": module.SECONDARY,
                        "nominal_document": root / "docs/prueba_nominal.txt",
                    }
                    def mutate():
                        path = paths[target]
                        path.write_bytes(path.read_bytes() + b"\n")
                    validate = module.validate
                    load_claims = b.load_claims
                    def validate_then_mutate():
                        result = validate()
                        mutate()
                        return result
                    def load_claims_then_mutate(repository):
                        result = load_claims(repository)
                        mutate()
                        return result
                    with mock.patch.object(b, "semantic_census_module", return_value=module):
                        if phase == "validation":
                            with mock.patch.object(module, "validate", side_effect=validate_then_mutate):
                                with self.assertRaises(b.BuildError):
                                    b.load_claim_review_evidence(root)
                        else:
                            with mock.patch.object(b, "load_claims", side_effect=load_claims_then_mutate):
                                with self.assertRaises(b.BuildError):
                                    b.load_claim_review_evidence(root)


class NominalContractTests(unittest.TestCase):
    def test_nominal_contract_rejects_invalid_evidence_identity_and_time(self):
        for mutation in ("same_reviewer", "date_only", "before_version", "scope", "circular", "duplicate"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                row = nominal(root, "S01", "a" * 64, "estado_editorial")
                if mutation == "same_reviewer":
                    row["revisor_independiente"] = row["autor_version"]
                elif mutation == "date_only":
                    row["fecha_revision_utc"] = "2026-09-26"
                elif mutation == "before_version":
                    row["fecha_revision_utc"] = "2026-09-26T08:00:00Z"
                elif mutation == "scope":
                    row["alcance"] = "CONFORME"
                elif mutation == "circular":
                    path = write(root, str(b.SOURCE_MATRIX_PATH), "matriz no independiente")
                    row["evidencia_local"] = str(b.SOURCE_MATRIX_PATH)
                    row["huella_evidencia_sha256"] = b.sha256_file(path)
                write_nominal(root, [row, row] if mutation == "duplicate" else [row])
                with self.assertRaises(b.BuildError):
                    b.load_nominal_reviews(root)

    def test_manifest_controls_and_aliases_are_not_evidence(self):
        forbidden = [
            "manifest.json", "data/auditoria/requisitos_disposiciones.csv",
            "docs/auditorias/controles_requisitos/R-0008.csv", str(b.SOURCE_MATRIX_PATH),
        ]
        for name in forbidden:
            for alias in ("direct", "logical", "resolved"):
                with self.subTest(name=name, alias=alias), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    row = nominal(root, "S01", "a" * 64, "estado_editorial")
                    target = root / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if alias == "logical":
                        target.symlink_to(root / "docs/prueba_nominal.txt")
                        relative = name
                    else:
                        write(root, name, "derivado consumidor")
                        if alias == "resolved":
                            (root / "alias.txt").symlink_to(target)
                            relative = "alias.txt"
                        else:
                            relative = name
                    row["evidencia_local"] = relative
                    row["huella_evidencia_sha256"] = b.sha256_file(root / relative)
                    write_nominal(root, [row])
                    with self.assertRaises(b.BuildError):
                        b.load_nominal_reviews(root)

    def test_historical_signature_survives_artifact_change_and_reinspection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            old = nominal(root, "S01", "a" * 64, "estado_editorial")
            old_bytes = b.csv_payload(b.NOMINAL_REVIEW_COLUMNS, [old])
            write_nominal(root, [old])
            write(root, "docs/prueba_nominal.txt", "Nuevo artefacto compartido.")
            obsolete = b.load_nominal_reviews(root)
            self.assertFalse(obsolete)
            self.assertEqual(len(obsolete.obsolete), 1)
            self.assertEqual((root / b.NOMINAL_REVIEWS).read_bytes(), old_bytes)
            new = {**old, "fecha_revision_utc": "2026-09-26T11:00:00Z"}
            digest = b.sha256_file(root / "docs/prueba_nominal.txt")
            new["huella_evidencia_sha256"] = digest
            new["artefactos_inspeccionados"] = json_string({"docs/prueba_nominal.txt": digest})
            write_nominal(root, [old, new])
            current = b.load_nominal_reviews(root)
            self.assertEqual(len(current), 1)
            self.assertEqual(len(current.obsolete), 1)
            self.assertEqual(next(iter(current.values())), new)
            self.assertEqual(b.read_dicts(root / b.NOMINAL_REVIEWS)[1][0], old)
            with self.assertRaises(b.BuildError):
                write_nominal(root, [new, {**new, "dictamen": new["dictamen"] + " Otro dictamen."}])
                b.load_nominal_reviews(root)


class SourceClosureTests(unittest.TestCase):
    def fixture(self, root):
        source = {
            "clave": "S01", "autores": "Autor", "año": "2026", "título": "Título fixture",
            "publicación o repositorio": "Revista", "tipo": "primaria",
            "DOI en forma https://doi.org/10.xxxx/... o URL resoluble si no hay DOI": "https://doi.org/10.0000/fixture",
            "notas de calidad": "No se infiere ninguna verificación desde esta nota.",
        }
        new = {**source, "clave": "S999"}
        write(root, "data/apendices/A_fuentes.csv", b.csv_payload(list(source), [source, new]))
        frozen = []
        for number in range(1, 526):
            key = f"S{number:02d}"
            frozen.append({
                "clave_inicial": key, "metadata": "histórico", "identidad_bibliografica": "histórica",
                "tipo": "primaria", "estado_editorial": "histórico", "acceso": "NO VERIFICABLE",
                "doi_url": "https://example.org", "uso": "histórico", "soporte_unico": "NO",
                "veredicto": "CONFORME", "severidad": "NINGUNA", "accion": "Conservar",
                "evidencia_auditoria": "histórica", "fecha_verificacion": "2026-08-08",
                "huella_corpus_inicial_sha256": b.source_fingerprint(source) if number == 1 else "a" * 64,
            })
        removed = write(root, "removed.csv", b.csv_payload(["clave", "motivo", "destino_documental"], [
            {"clave": row["clave_inicial"], "motivo": "Fixture retirada", "destino_documental": "Fixture"}
            for row in frozen[1:]
        ]))
        return source, new, frozen, removed

    def test_date_only_and_initial_approval_do_not_close_current_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, new, frozen, removed = self.fixture(root)
            registry = chronology.DateRegistry({("VERIFICACION_FUENTE", "S999", b.source_fingerprint(new)): {"fecha_version": "2026-09-26T10:00:00Z"}}, [])
            with mock.patch.object(b, "load_object_dates", return_value=registry):
                rows = b.build_source_matrix(frozen, root, [], removed)
            live = [row for row in rows if row["clave_final"] in {"S01", "S999"}]
            self.assertEqual({row["estado_hallazgo"] for row in live}, {"ABIERTO"})
            self.assertEqual(live[0]["veredicto"], "PENDIENTE")
            self.assertEqual(live[1]["fecha_verificacion"], "2026-09-26T10:00:00Z")

    def test_source_closure_rejects_nominal_document_changed_during_build(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, _, frozen, removed = self.fixture(root)
            rows = [nominal(root, "S01", b.source_fingerprint(source), axis) for axis in b.SOURCE_REVIEW_AXES]
            write_nominal(root, rows)
            baseline = b.build_source_matrix(frozen, root, [], removed)
            self.assertEqual(next(r for r in baseline if r["clave_final"] == "S01")["estado_hallazgo"], "CERRADO")
            load_sources = b.load_sources
            def load_then_mutate(repository):
                result = load_sources(repository)
                write(root, "docs/prueba_nominal.txt", "Prueba nominal modificada durante la construcción S.")
                return result
            with mock.patch.object(b, "load_sources", side_effect=load_then_mutate):
                with self.assertRaisesRegex(b.BuildError, "expediente nominal"):
                    b.build_source_matrix(frozen, root, [], removed)

    def test_complete_source_review_is_acyclic_and_stale_or_negative_does_not_close(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, _, frozen, removed = self.fixture(root)
            rows = [nominal(root, "S01", b.source_fingerprint(source), axis) for axis in b.SOURCE_REVIEW_AXES]
            write_nominal(root, rows)
            def current():
                return next(row for row in b.build_source_matrix(frozen, root, [], removed) if row["clave_final"] == "S01")
            before = current()
            self.assertEqual(before["estado_hallazgo"], "CERRADO")
            # La matriz S no lee ni siquiera censos corruptos: antecede al censo.
            write(root, "data/auditoria/censo_semantico_afirmaciones_v1.csv", "inválido")
            self.assertEqual(before, current())
            rows[0]["resultado"] = "NO_CONFORME"
            write_nominal(root, rows)
            self.assertEqual(current()["estado_hallazgo"], "ABIERTO")
            rows[0]["resultado"] = "CONFORME"
            write_nominal(root, rows)
            source["notas de calidad"] += " Nueva versión."
            write(root, "data/apendices/A_fuentes.csv", b.csv_payload(list(source), [source]))
            self.assertEqual(current()["estado_hallazgo"], "ABIERTO")
            self.assertIn("HISTORICA_NO_VIGENTE", current()["evidencia_final"])

    def test_source_catalogue_changed_during_build_is_rejected(self):
        for mutation in ("title", "removed", "added", "duplicate", "deleted"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source, new, frozen, removed = self.fixture(root)
                write_nominal(root, [nominal(root, "S01", b.source_fingerprint(source), axis)
                                     for axis in b.SOURCE_REVIEW_AXES])
                load_sources = b.load_sources
                mutated = False

                def load_then_mutate(repository):
                    nonlocal mutated
                    result = load_sources(repository)
                    if not mutated:
                        mutated = True
                        rows = [dict(row) for row in result]
                        if mutation == "title":
                            rows[0]["título"] = "Nueva identidad sin revisión"
                        elif mutation == "removed":
                            rows.pop(0)
                        elif mutation == "added":
                            rows.append({**source, "clave": "S998"})
                        elif mutation == "duplicate":
                            rows.append(dict(source))
                        if mutation == "deleted":
                            (root / "data/apendices/A_fuentes.csv").unlink()
                        else:
                            write(root, "data/apendices/A_fuentes.csv", b.csv_payload(list(source), rows))
                    return result

                with mock.patch.object(b, "load_sources", side_effect=load_then_mutate):
                    with self.assertRaisesRegex(b.BuildError, "catálogo A"):
                        b.build_source_matrix(frozen, root, [], removed)

    def test_source_catalogue_mutation_after_final_read_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, _, frozen, removed = self.fixture(root)
            write_nominal(root, [nominal(root, "S01", b.source_fingerprint(source), axis)
                                 for axis in b.SOURCE_REVIEW_AXES])
            load_sources = b.load_sources
            calls = 0

            def load_then_mutate_on_second_read(repository):
                nonlocal calls
                result = load_sources(repository)
                calls += 1
                if calls == 2:
                    changed = [dict(row) for row in result]
                    changed[0]["título"] = "Cambio posterior a la relectura"
                    write(root, "data/apendices/A_fuentes.csv", b.csv_payload(list(source), changed))
                return result

            with mock.patch.object(b, "load_sources", side_effect=load_then_mutate_on_second_read):
                with self.assertRaisesRegex(b.BuildError, "catálogo A"):
                    b.build_source_matrix(frozen, root, [], removed)
            self.assertEqual(calls, 2)

    def test_duplicate_live_source_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, new, frozen, removed = self.fixture(root)
            write(root, "data/apendices/A_fuentes.csv", b.csv_payload(list(source), [source, source, new]))
            with self.assertRaisesRegex(b.BuildError, "catálogo A.*duplicadas"):
                b.build_source_matrix(frozen, root, [], removed)

    def test_preparation_writes_only_source_matrix_and_never_reads_census(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, _, frozen, removed = self.fixture(root)
            args = argparse.Namespace(
                root=root, reconstructed_inputs=Path("inputs"), origin_maps=None,
                removed_sources=removed, second_review_evidence=None,
                require_complete_review=False, check=False, prepare_source_matrix=True,
            )
            before = {p.relative_to(root) for p in root.rglob("*") if p.is_file()}
            with (
                mock.patch.object(b, "parse_args", return_value=args),
                mock.patch.object(b, "validate_file_hash"),
                mock.patch.object(b.subprocess, "run", return_value=mock.Mock(returncode=0)),
                mock.patch.object(b, "load_and_validate_reconstructed", return_value={"sources": frozen}),
                mock.patch.object(b, "load_claims", return_value=([], {})),
                mock.patch.object(b, "build_claim_matrix", side_effect=AssertionError("No leer C/censo")),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(b.main(), 0)
                prepared = (root / b.SOURCE_MATRIX_PATH).read_bytes()
                self.assertEqual(b.main(), 0)
                self.assertEqual((root / b.SOURCE_MATRIX_PATH).read_bytes(), prepared)
                args.check = True
                self.assertEqual(b.main(), 0)
                write(root, str(b.SOURCE_MATRIX_PATH), "desactualizada")
                args.prepare_source_matrix = False
                self.assertEqual(b.main(), 1)
                self.assertEqual((root / b.SOURCE_MATRIX_PATH).read_text(), "desactualizada")
            after = {p.relative_to(root) for p in root.rglob("*") if p.is_file()}
            self.assertEqual(after - before, {b.SOURCE_MATRIX_PATH})


class GlobalReviewDossierTests(unittest.TestCase):
    def test_incompatible_review_states_are_rejected_before_import(self):
        pairs = (("PENDIENTE", "CERRADO"), ("NO_CONFORME", "CERRADO"),
                 ("CONFORME", "ABIERTO"), ("FALLO_CORREGIDO", "ABIERTO"),
                 ("DESCONOCIDO", "CERRADO"), ("PENDIENTE", "DESCONOCIDO"))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = write(root, "trace.csv", b.csv_payload(["tipo", "id_segmento"], []))
            requirements = [{"id_requisito": f"R-{n:04d}"} for n in range(1, 484)]
            generated = b.build_second_review([], [], requirements, trace, None, root=root)
            for result, state in pairs:
                with self.subTest(result=result, state=state):
                    rows = [{**row, "resultado": result, "estado_cierre": state} for row in generated]
                    path = write(root, "signed.csv", b.csv_payload(b.SECOND_REVIEW_COLUMNS, rows))
                    with self.assertRaisesRegex(b.BuildError, "resultado/estado_cierre incompatibles"):
                        b.build_second_review([], [], requirements, trace, path, root=root)

    def test_pending_review_preserves_notes_but_never_a_closed_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = write(root, "trace.csv", b.csv_payload(["tipo", "id_segmento"], []))
            requirements = [{"id_requisito": f"R-{n:04d}"} for n in range(1, 484)]
            rows = b.build_second_review([], [], requirements, trace, None, root=root)
            rows[0]["evidencia"] = "Nota de trabajo, aún no revisada."
            path = write(root, "signed.csv", b.csv_payload(b.SECOND_REVIEW_COLUMNS, rows))
            result = b.build_second_review([], [], requirements, trace, path, root=root)
            self.assertEqual(result[0]["evidencia"], rows[0]["evidencia"])
            self.assertEqual({(r["resultado"], r["estado_cierre"]) for r in result},
                             {("PENDIENTE", "ABIERTO")})

    def test_report_cannot_trust_closed_label_on_pending_rows(self):
        rows = [{**b.pending_review_row("REQUISITO", f"R-{n:04d}", "fixture", "fixture", "a" * 64),
                 "estado_cierre": "CERRADO"} for n in range(1, 484)]
        after = dict.fromkeys(("claims", "sources", "entities", "events", "dates", "hypotheses",
                               "magnitudes", "negative_active", "tables"), 0)
        report = b.report_markdown([], [], [], [], rows, after, {k: {} for k in "BCDEFG"}).decode()
        self.assertNotIn("CERRADA: la segunda revisión", report)
        self.assertIn("483 segundas revisiones permanecen abiertos", report)

    def test_global_signature_cannot_precede_semantic_or_nominal_dossier(self):
        for stratum in ("AFIRMACION", "FUENTE"):
            with self.subTest(stratum=stratum), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                if stratum == "AFIRMACION":
                    row, _, _, _ = census_fixture(root, extra_axes=True)
                    evidence = b.load_claim_review_evidence(root)
                    self.assertEqual(evidence.errors, ())
                    dossier = {
                        "clave_inicial": row["#"], "estado_inicial": "CORREGIR",
                        "severidad_inicial": "P0", "huella_final_sha256": b.claim_fingerprint(row),
                        "estado_hallazgo": "CERRADO", "evidencia_final": evidence.evidence([row]),
                    }
                    self.assertIn("expediente_no_antes_utc=2026-09-26T13:00:00Z", dossier["evidencia_final"])
                    self.assertIn("expediente_no_antes_utc=2026-09-26T10:00:00Z", dossier["evidencia_final"])
                    claims, sources = [dossier], []
                    dates = (("11:30:00", "PENDIENTE"), ("12:30:00", "PENDIENTE"), ("13:00:00", "CONFORME"))
                else:
                    source, _, frozen, removed = SourceClosureTests().fixture(root)
                    nominal_rows = [nominal(root, "S01", b.source_fingerprint(source), axis) for axis in b.SOURCE_REVIEW_AXES]
                    nominal_rows[-1]["fecha_revision_utc"] = "2026-09-26T14:00:00Z"
                    write_nominal(root, nominal_rows)
                    dossier = next(r for r in b.build_source_matrix(frozen, root, [], removed) if r["clave_final"] == "S01")
                    self.assertEqual(dossier["estado_hallazgo"], "CERRADO")
                    self.assertIn("expediente_no_antes_utc=2026-09-26T14:00:00Z", dossier["evidencia_final"])
                    dossier.update({"severidad_inicial": "P0", "veredicto_inicial": "CORREGIR"})
                    claims, sources = [], [dossier]
                    dates = (("11:30:00", "PENDIENTE"), ("13:30:00", "PENDIENTE"), ("14:00:00", "CONFORME"))
                requirements = [{"id_requisito": f"R-{n:04d}"} for n in range(1, 484)]
                trace = write(root, "trace.csv", b.csv_payload(["tipo", "id_segmento"], []))
                signature = b.build_second_review(claims, sources, requirements, trace, None, root=root)[0]
                signature.update({
                    "resultado": "CONFORME", "estado_cierre": "CERRADO",
                    "revisor_independiente": "Global-Fixture",
                    "declaracion_independencia": "INDEPENDIENTE_DEL_AUTOR_DE_LA_CORRECCION",
                    "evidencia": "Revisión artificial expediente_sha256=" + b.row_fingerprint(dossier),
                    "accion": "Sin cambio artificial",
                })
                for date, expected in dates:
                    signature["fecha"] = f"2026-09-26T{date}Z"
                    path = write(root, "signed.csv", b.csv_payload(b.SECOND_REVIEW_COLUMNS, [signature]))
                    result = b.build_second_review(claims, sources, requirements, trace, path, root=root)[0]
                    self.assertEqual(result["resultado"], expected, (stratum, date))

    def test_global_duplicate_signatures_are_rejected_in_both_orders(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = write(root, "trace.csv", b.csv_payload(["tipo", "id_segmento"], []))
            requirements = [{"id_requisito": f"R-{n:04d}"} for n in range(1, 484)]
            signature = b.build_second_review([], [], requirements, trace, None, root=root)[0]
            positive = {**signature, "resultado": "CONFORME", "estado_cierre": "CERRADO"}
            negative = {**signature, "resultado": "NO_CONFORME", "estado_cierre": "ABIERTO"}
            for rows in ([positive, negative], [negative, positive], [signature, signature]):
                with self.subTest(results=[row["resultado"] for row in rows]):
                    path = write(root, "signed.csv", b.csv_payload(b.SECOND_REVIEW_COLUMNS, rows))
                    with self.assertRaisesRegex(b.BuildError, "duplicada y ambigua"):
                        b.build_second_review([], [], requirements, trace, path, root=root)

    def test_canonical_hash_alone_cannot_preserve_a_global_signature(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = write(root, "trace.csv", b.csv_payload(["tipo", "id_segmento"], []))
            claims = [{
                "clave_inicial": "C-001", "estado_inicial": "CORREGIR", "severidad_inicial": "P0",
                "huella_final_sha256": "a" * 64, "estado_hallazgo": "CERRADO", "evidencia_final": "Expediente inicial",
            }]
            requirements = [{"id_requisito": f"R-{n:04d}"} for n in range(1, 484)]
            rows = b.build_second_review(claims, [], requirements, trace, None, root=root)
            signed = rows[0]
            signed.update({
                "resultado": "CONFORME", "estado_cierre": "CERRADO",
                "revisor_independiente": "Revisor-Fixture",
                "declaracion_independencia": "INDEPENDIENTE_DEL_AUTOR_DE_LA_CORRECCION",
                "fecha": "2026-09-26T20:00:00Z", "evidencia": "Revisión nominal fixture sin token.", "accion": "Sin cambio",
            })
            proof = root / "signed.csv"
            def save_and_build():
                write(root, "signed.csv", b.csv_payload(b.SECOND_REVIEW_COLUMNS, rows))
                return b.build_second_review(claims, [], requirements, trace, proof, root=root)[0]
            self.assertEqual(save_and_build()["resultado"], "PENDIENTE")
            signed["evidencia"] += " expediente_sha256=" + b.row_fingerprint(claims[0])
            self.assertEqual(save_and_build()["resultado"], "CONFORME")
            claims[0]["evidencia_final"] = "Otro expediente con la misma huella canónica"
            self.assertEqual(save_and_build()["resultado"], "PENDIENTE")
            signed["evidencia"] += " expediente_sha256=" + b.row_fingerprint(claims[0])
            claims[0]["estado_hallazgo"] = "ABIERTO"
            signed["evidencia"] += " expediente_sha256=" + b.row_fingerprint(claims[0])
            self.assertEqual(save_and_build()["resultado"], "PENDIENTE")

    def test_report_does_not_close_or_zero_findings_from_empty_second_review(self):
        row = {
            "clave_inicial": "C-001", "estado_inicial": "CORREGIR", "resultado": "CORREGIDA",
            "estado_hallazgo": "ABIERTO", "severidad_inicial": "P0",
        }
        after = dict.fromkeys(("claims", "sources", "entities", "events", "dates", "hypotheses", "magnitudes", "negative_active", "tables"), 1)
        report = b.report_markdown([row], [], [], [], [], after, {k: {} for k in "BCDEFG"}).decode()
        self.assertIn("EN CURSO", report)
        self.assertIn("P0 abiertos: 1", report)


if __name__ == "__main__":
    unittest.main()
