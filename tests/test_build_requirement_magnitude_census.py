from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from scripts import build_requirement_magnitude_census as builder


REQ_HEADER = [
    "id_requisito", "seccion_prompt", "ancla", "requisito_literal",
    "estado_inicial", "estado_final", "afirmaciones_iniciales", "afirmaciones",
    "tablas_iniciales", "tablas", "fuentes_iniciales", "fuentes",
    "busqueda_negativa_inicial", "busqueda_negativa", "accion_inicial", "accion",
    "evidencia_inicial", "evidencia", "huella_inicial_sha256",
]
CLAIM_HEADER = [
    "#", "Afirmación", "Sujeto", "Predicado", "Objeto", "Atribución", "Fuente",
    "Aceptación", "Fuerza", "Motivo", "Resolución", "Vigencia",
]


class RequirementMagnitudeCensusTests(unittest.TestCase):
    def _root(
        self, *, source: str = "S01 tabla 2", gap: str = "BN-001",
        transform: str = "NINGUNA", include_spec: bool = True,
    ) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        for folder in (
            "docs/auditorias", "data/auditoria", "data/afirmaciones",
            "data/apendices", "data/busquedas_negativas",
        ):
            (root / folder).mkdir(parents=True, exist_ok=True)
        requirement = ["R-0001", "x", "L1", "Da la magnitud publicada."] + ["n/a"] * 15
        with (root / builder.REQUIREMENTS).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle); writer.writerow(REQ_HEADER); writer.writerow(requirement)
        with (root / builder.CLASSIFICATION).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle); writer.writerow(builder.CLASS_HEADER)
            writer.writerow(["R-0001", "MAGNITUD_PEDIDA", "El literal solicita expresamente una magnitud publicada concreta."])
        with (root / builder.SPECIFICATION).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle); writer.writerow(builder.SPEC_HEADER)
            if include_spec:
                writer.writerow(["MREQ-0001", "R-0001", "magnitud publicada", "valor de prueba publicado", "VALOR_PUBLICADO", "C-001", "", "", transform])
        with (root / builder.SEMANTIC_CONTRACTS).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle); writer.writerow(builder.CONTRACT_HEADER)
        with (root / "data/afirmaciones/00.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle); writer.writerow(CLAIM_HEADER)
            writer.writerow(["C-001", "La fuente publicó 12 unidades.", "objeto", "tiene_valor_medido", "12 unidades", "expresa", source, "no evaluado", "alta", "dato directo", "resuelta", "vigente"])
        with (root / "data/apendices/A_fuentes.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle); writer.writerow(["clave"]); writer.writerow(["S01"])
        with (root / "data/busquedas_negativas/15.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle); writer.writerow(["clave", "hueco", "términos exactos", "resultado o motivo"])
            writer.writerow([gap, "valor de prueba no localizado", "consulta nominal de valor de prueba", "La consulta no recuperó un valor publicado comparable."])
        return root

    def test_builds_from_requirement_and_claim_not_appendix_f(self) -> None:
        payload = builder.build(self._root()).decode("utf-8")
        self.assertIn("R-0001", payload)
        self.assertIn("C-001: 12 unidades", payload)
        self.assertNotIn("F_magnitudes", payload)

    def test_quantitative_literal_without_terminal_row_is_fatal(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "sin fila terminal"):
            builder.build(self._root(include_spec=False))

    def test_number_without_source_localizer_is_fatal(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "sin fuente/localizador"):
            builder.build(self._root(source="S01"))

    def test_gap_without_versioned_search_is_fatal(self) -> None:
        root = self._root(gap="BN-001")
        with (root / builder.SPECIFICATION).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle); writer.writerow(builder.SPEC_HEADER)
            writer.writerow(["MREQ-0001", "R-0001", "magnitud publicada", "valor de prueba publicado", "HUECO_EXPLICITO", "", "BN-999", "La búsqueda nominal no recuperó una publicación con esa magnitud.", "NINGUNA"])
        with self.assertRaisesRegex(RuntimeError, "hueco sin búsqueda versionada"):
            builder.build(root)

    def test_editorial_transformation_is_fatal(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "transformación editorial prohibida"):
            builder.build(self._root(transform="REDONDEO"))

    def test_hole_description_cannot_approve_itself_as_search_result(self) -> None:
        root = self._root()
        with (root / builder.SPECIFICATION).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle); writer.writerow(builder.SPEC_HEADER)
            writer.writerow(["MREQ-0001", "R-0001", "magnitud publicada", "valor de prueba publicado", "HUECO_EXPLICITO", "", "BN-001", "La búsqueda nominal no recuperó una publicación con esa magnitud.", "NINGUNA"])
        with (root / "data/busquedas_negativas/15.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle); writer.writerow(["clave", "hueco", "términos exactos"])
            writer.writerow(["BN-001", "valor de prueba no localizado", "consulta nominal de valor de prueba"])
        with self.assertRaisesRegex(RuntimeError, "hueco sin consulta y resultado suficientes"):
            builder.build(root)

    @staticmethod
    def _claim(subject: str, obj: str, source: str = "S01 resultados") -> dict[str, str]:
        return {"Afirmación": f"{subject} tiene {obj}", "Sujeto": subject, "Objeto": obj, "Fuente": source}

    def test_semantic_mutant_delta13c_cannot_become_oxygen_level(self) -> None:
        correct = self._claim("atmósfera mesoproterozoica", "4–8% PAL de O₂ inferido")
        mutant = self._claim("excursión Lomagundi", "+15‰ δ13Ccarbonato")
        builder._validate_semantic_contract("MREQ-X", "NIVEL_OXIGENO", "VALOR_PUBLICADO", [correct], None)
        with self.assertRaisesRegex(RuntimeError, "cifra de oxígeno|δ13C"):
            builder._validate_semantic_contract("MREQ-X", "NIVEL_OXIGENO", "VALOR_PUBLICADO", [correct, mutant], None)

    def test_semantic_mutant_culture_time_cannot_become_response_latency(self) -> None:
        correct = self._claim("inicio de agregación de Capsaspora", "aproximadamente 20 min")
        mutant = self._claim("estadio quístico de Capsaspora", "cultivo de 14 días", "S01 métodos, Culture conditions")
        builder._validate_semantic_contract("MREQ-X", "LATENCIA_RESPUESTA", "VALOR_PUBLICADO", [correct], None)
        with self.assertRaisesRegex(RuntimeError, "no es latencia de respuesta"):
            builder._validate_semantic_contract("MREQ-X", "LATENCIA_RESPUESTA", "VALOR_PUBLICADO", [correct, mutant], None)

    def test_semantic_mutants_sampling_and_oae_are_rejected(self) -> None:
        hgt = {"payload": "cifras sustantivas de HGT; tamaño de muestreo de 2.585 árboles"}
        oae = {"payload": "duración de glaciación global calculada desde OAE2"}
        with self.assertRaisesRegex(RuntimeError, "emparejamiento no equivalente"):
            builder._validate_semantic_contract("MREQ-X", "CIFRA_HGT_SUSTANTIVA", "HUECO_EXPLICITO", [], hgt)
        with self.assertRaisesRegex(RuntimeError, "emparejamiento no equivalente"):
            builder._validate_semantic_contract("MREQ-X", "DURACION_GLACIACION", "HUECO_EXPLICITO", [], oae)

    def test_semantic_mutants_perforation_universal_and_gamete_shape_are_rejected(self) -> None:
        perforation = self._claim("perforaciones en acritarcos", "0.1–3.4 µm")
        universal_loss = {"payload": "número de genes perdidos y tiempo; tasa universal de pérdida"}
        universal_redox = {"payload": "duración del cambio redox; constante universal de cuenca"}
        gamete_shape = {"payload": "61% de alargamiento de gameto y 55% de collar"}
        with self.assertRaisesRegex(RuntimeError, "objeto terminal no satisface"):
            builder._validate_semantic_contract("MREQ-X", "RANGO_TAMANO_CELULAR", "VALOR_PUBLICADO", [perforation], None)
        with self.assertRaisesRegex(RuntimeError, "emparejamiento no equivalente"):
            builder._validate_semantic_contract("MREQ-X", "PERDIDA_GENES_NUMERO_TIEMPO", "HUECO_EXPLICITO", [], universal_loss)
        with self.assertRaisesRegex(RuntimeError, "emparejamiento no equivalente"):
            builder._validate_semantic_contract("MREQ-X", "DURACION_TRANSICION_REDOX", "HUECO_EXPLICITO", [], universal_redox)
        with self.assertRaisesRegex(RuntimeError, "objeto terminal no satisface"):
            builder._validate_semantic_contract("MREQ-X", "COSTE_DOBLE_ISOGAMIA", "HUECO_EXPLICITO", [], gamete_shape)


if __name__ == "__main__":
    unittest.main()
