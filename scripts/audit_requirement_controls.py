#!/usr/bin/env python3
"""Ejecuta y materializa los controles estructurales nominales R-XXXX.

Cada control consulta el corpus canónico vivo.  El programa no acepta una
declaración de cumplimiento como entrada: reconstruye el censo de C, tablas,
apéndices, búsquedas negativas y narrativa, aplica invariantes deterministas y
solo escribe ``CERO_FALLOS`` cuando la lista de infracciones calculada está
vacía. La existencia o el contenido no vacío de los destinos nunca bastan:
cada promoción requiere además una familia nominal enumerada en
``AUTOMATION_FAMILY_BY_*``. Los mandatos sin prueba suficiente permanecen
``CONTROL_DEFINIDO`` y se publican como ``PENDIENTE_AUTOMATIZACION_NOMINAL``,
salvo que un ledger independiente aporte una revisión nominal completa ligada
por huella al literal y al alcance vivo. Una mera atestación ``CUMPLE`` nunca
promueve un control.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable, Sequence

try:
    from corpus_io import expand_source_refs
except ModuleNotFoundError:  # Importación como ``scripts.audit_...`` en tests.
    from scripts.corpus_io import expand_source_refs


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path("data/auditoria/requisitos_disposiciones.csv")
ARTIFACT_DIR = Path("docs/auditorias/controles_requisitos")
REQUIREMENT_MATRIX = Path("docs/auditorias/matriz_requisitos_2026-08-08.csv")
MANUAL_LEDGER = Path(
    "docs/auditorias/revision_manual_requisitos_2026-08-08.csv"
)
CUTOFF_DATE = date(2026, 8, 8)
ARTIFACT_HEADER = [
    "id_requisito", "alcance_o_censo", "comando_o_consulta",
    "resultado_control", "evidencia",
]
MANUAL_LEDGER_HEADER = [
    "id_requisito", "requisito_literal", "huella_literal_sha256",
    "rutas_censadas", "huella_alcance_sha256", "prueba_nominal",
    "resultado", "evidencia", "localizadores_evidencia", "revisor",
    "declaracion_independencia", "fecha_revision",
]
MANUAL_RESULTS = {"CONFORME", "NO_CONFORME"}
INDEPENDENCE_DECLARATION = "REVISOR_DISTINTO_DEL_AUTOR_DEL_CONTROL"
CLAIM_HEADER = [
    "#", "Afirmación", "Sujeto", "Predicado", "Objeto", "Atribución",
    "Fuente", "Aceptación", "Fuerza", "Motivo", "Resolución", "Vigencia",
]
SOURCE_HEADER = [
    "clave", "autores", "año", "título", "publicación o repositorio",
    "DOI en forma https://doi.org/10.xxxx/... o URL resoluble si no hay DOI",
    "tipo", "notas de calidad", "fecha de consulta",
]
ENTITY_HEADER = [
    "etiqueta preferida", "tipo", "sinónimos y grafías alternativas",
    "marcas (⚠, ≈, †, [F], [H]) como atributos de la fila",
    "# de la fila del registro donde aparece por primera vez",
]
EVENT_HEADER = [
    "clave", "tipo", "participantes con su papel",
    "entidad resultante si la hay", "intervalo temporal",
    "# de las filas que lo sostienen", "qué fuente lo describe como evento",
    "desenlace",
]
DATE_HEADER = [
    "a qué se aplica", "límite más antiguo", "límite más reciente",
    "unidad explícita", "incertidumbre tal como la da la fuente", "tipo",
    "método y calibración", "observado o inferido", "fuente con localizador",
    "# de la fila que la sostiene",
]
HYPOTHESIS_HEADER = [
    "clave", "qué sostiene en una frase", "supuestos que da por buenos",
    "# de las filas que la componen", "fuentes a favor", "fuentes en contra",
    "con qué otras hipótesis es incompatible y en qué punto exacto",
    "qué observación la falsaría",
]
MAGNITUDE_HEADER = [
    "magnitud", "valor tal como lo publica la fuente", "unidad original",
    "organismo, nodo o intervalo al que se aplica", "método o proxy",
    "incertidumbre publicada", "observado o inferido",
    "fuente con localizador", "#",
]
MATERIAL_HEADER = [
    "material", "afirmación o estado", "fuente y localizador",
    "sección propuesta", "#",
]

SOURCE_TYPES = {
    "investigación primaria", "revisión", "base de datos taxonómica",
    "preprint", "capítulo o libro", "tesis", "divulgación o blog", "otro",
}
ATTRIBUTIONS = {"expresa", "glosa"}
ACCEPTANCE = {
    "consenso amplio", "aceptación mayoritaria", "aceptación mixta",
    "posición minoritaria", "no evaluado",
}
STRENGTH = {"alta", "media", "baja", "desconocida"}
RESOLUTION = {
    "resuelta", "parcialmente resuelta", "sin resolver",
    "información insuficiente",
}
VALIDITY = {"vigente", "histórica", "superada", "rechazada"}
EVENT_TYPES = {
    "endosimbiosis", "transferencia horizontal",
    "transferencia génica endosimbiótica", "divergencia", "radiación",
    "extinción", "adquisición de rasgo", "pérdida de rasgo",
    "reducción genómica", "depredación", "competencia",
    "relación huésped-patógeno", "asociación no heredable",
}
EVENT_ROLES = {
    "hospedador", "endosimbionte", "simbionte extracelular", "donante",
    "receptor", "población parental", "linaje resultante", "depredador",
    "presa", "huésped", "parásito", "competidor",
}
OUTCOMES = {
    "transitoria", "dependencia", "integración heredable", "degradación",
    "pérdida", "no determinado",
}
DATE_TYPES = {
    "edad de ocurrencia", "rango observado", "rango inferido de linaje",
    "estimación de divergencia", "intervalo de evento", "evidencia de rasgo",
    "publicación",
}
OBSERVED = {"observado", "inferido"}
CLAIM_REF = re.compile(r"\bC-\d{3,5}\b")
BN_REF = re.compile(r"\bBN-\d{3}\b")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def csv_bytes(header: Sequence[str], rows: Sequence[dict[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        buffer, fieldnames=list(header), quoting=csv.QUOTE_ALL,
        lineterminator="\n", extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent,
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def split_refs(value: str) -> list[str]:
    return [] if value == "n/a" else value.split("; ")


def natural(value: str) -> tuple[str, int, str]:
    match = re.fullmatch(r"([^0-9]*)(\d+)(.*)", value)
    return (value, -1, "") if not match else (
        match.group(1), int(match.group(2)), match.group(3),
    )


@dataclass
class Result:
    requirement_id: str
    slug: str
    scope_paths: set[Path] = field(default_factory=set)
    checks: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metrics: Counter[str] = field(default_factory=Counter)
    witnesses: list[str] = field(default_factory=list)
    automation_families: set[str] = field(default_factory=set)

    def check(self, condition: bool, label: str, error: str) -> None:
        self.checks.append(label)
        if not condition:
            self.errors.append(error)

    def metric(self, name: str, value: int) -> None:
        self.metrics[name] = value

    def automate(self, family: str) -> None:
        """Declara la familia nominal que acredita este mandato concreto."""
        self.automation_families.add(family)

    @property
    def automated(self) -> bool:
        return bool(self.automation_families)


@dataclass(frozen=True)
class ManualReview:
    """Adjudicación humana vinculada al literal y al censo vivo exactos."""

    requirement_id: str
    row: dict[str, str]

    @property
    def conforms(self) -> bool:
        return self.row["resultado"] == "CONFORME"


class Corpus:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.index_path = root / "data/table_index.json"
        self.index = json.loads(self.index_path.read_text(encoding="utf-8"))
        self.entries = {entry["id"]: entry for entry in self.index["tables"]}
        self.table_rows: dict[str, tuple[list[str], list[dict[str, str]]]] = {}
        self.claims: dict[str, dict[str, str]] = {}
        self.claim_paths: dict[str, Path] = {}
        self.bn: dict[str, dict[str, str]] = {}
        self.bn_paths: dict[str, Path] = {}
        for entry in self.index["tables"]:
            path = root / entry["csv_path"]
            header, rows = read_csv(path)
            self.table_rows[entry["id"]] = (header, rows)
            if entry["category"] == "claims":
                for row in rows:
                    self.claims[row["#"]] = row
                    self.claim_paths[row["#"]] = path
            elif entry["category"] == "negative":
                for row in rows:
                    self.bn[row["clave"]] = row
                    self.bn_paths[row["clave"]] = path
        self.appendix_paths = {
            "A": root / "data/apendices/A_fuentes.csv",
            "B": root / "data/apendices/B_entidades.csv",
            "C": root / "data/apendices/C_eventos.csv",
            "D": root / "data/apendices/D_fechas.csv",
            "E": root / "data/apendices/E_hipotesis.csv",
            "F": root / "data/apendices/F_magnitudes.csv",
            "G": root / "data/apendices/G_material_no_encajado.csv",
            "H": root / "data/apendices/H_recuento_control.csv",
        }
        self.appendices = {
            letter: read_csv(path) for letter, path in self.appendix_paths.items()
        }
        self.sources = {row["clave"]: row for row in self.appendices["A"][1]}
        self.section_paths = sorted((root / "docs/secciones").glob("*.md"))
        self.section_text = {
            path: path.read_text(encoding="utf-8") for path in self.section_paths
        }
        self.semantic_result: tuple[int, str] | None = None
        self.content_trace_result: tuple[int, str] | None = None

    def semantic_audit(self) -> tuple[int, str]:
        if self.semantic_result is None:
            completed = subprocess.run(
                [sys.executable, "scripts/audit_semantics.py"], cwd=self.root,
                text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                check=False,
            )
            self.semantic_result = (completed.returncode, completed.stdout.strip())
        return self.semantic_result

    def content_trace_audit(self) -> tuple[int, str]:
        if self.content_trace_result is None:
            completed = subprocess.run(
                [sys.executable, "scripts/build_content_trace.py", "--check"],
                cwd=self.root, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, check=False,
            )
            self.content_trace_result = (
                completed.returncode, completed.stdout.strip(),
            )
        return self.content_trace_result

    def scoped_digest(self, paths: Iterable[Path]) -> str:
        records = []
        for path in sorted(set(paths)):
            relative = path.relative_to(self.root).as_posix()
            records.append(f"{relative}\x1f{sha256_file(path)}\n")
        return sha256_bytes("".join(records).encode("utf-8"))


def load_requirement_literals(root: Path) -> dict[str, str]:
    """Carga el literal auditado; el ledger nunca puede redefinir el mandato."""
    header, rows = read_csv(root / REQUIREMENT_MATRIX)
    required = {"id_requisito", "requisito_literal"}
    if not required.issubset(header):
        raise RuntimeError(
            f"{REQUIREMENT_MATRIX} carece de columnas {sorted(required - set(header))}"
        )
    literals: dict[str, str] = {}
    duplicates = []
    for row in rows:
        rid = row["id_requisito"]
        if rid in literals:
            duplicates.append(rid)
        literals[rid] = row["requisito_literal"]
    if duplicates:
        raise RuntimeError(
            f"requisitos duplicados en matriz: {sorted(set(duplicates))}"
        )
    return literals


def manual_scope_paths(corpus: Corpus, result: Result) -> list[Path]:
    """Separa el corpus revisado del código que valida el ledger.

    El literal tiene su propia huella y el ledger queda ligado a todos los
    destinos científicos calculados por ``evaluate``. Cambiar el auditor no
    invalida una lectura humana; cambiar cualquier fichero censado sí.
    """
    excluded = {
        corpus.root / "scripts/audit_requirement_controls.py",
        corpus.root / "scripts/corpus_io.py",
    }
    return sorted(set(result.scope_paths) - excluded)


def serialize_manual_scope(corpus: Corpus, paths: Iterable[Path]) -> str:
    return ";".join(
        path.relative_to(corpus.root).as_posix() for path in sorted(set(paths))
    )


def manual_template_row(
    corpus: Corpus, result: Result, literal: str,
) -> dict[str, str]:
    paths = manual_scope_paths(corpus, result)
    return {
        "id_requisito": result.requirement_id,
        "requisito_literal": literal,
        "huella_literal_sha256": sha256_bytes(literal.encode("utf-8")),
        "rutas_censadas": serialize_manual_scope(corpus, paths),
        "huella_alcance_sha256": corpus.scoped_digest(paths),
        "prueba_nominal": "PENDIENTE_REVISION",
        "resultado": "PENDIENTE",
        "evidencia": "PENDIENTE_REVISION",
        "localizadores_evidencia": "PENDIENTE_REVISION",
        "revisor": "PENDIENTE_REVISION",
        "declaracion_independencia": "PENDIENTE_REVISION",
        "fecha_revision": "PENDIENTE_REVISION",
    }


def locator_resolves(corpus: Corpus, locator: str) -> bool:
    """Resuelve claves canónicas o una ruta relativa con ancla/fila opcional."""
    locator = locator.strip()
    if re.fullmatch(r"C-\d{3,5}", locator):
        return locator in corpus.claims
    if re.fullmatch(r"S\d+", locator):
        return locator in corpus.sources
    if re.fullmatch(r"BN-\d{3}", locator):
        return locator in corpus.bn
    if locator in corpus.entries:
        return True
    path_text = locator.split("#", 1)[0]
    path_text = re.sub(r":(?:L)?\d+(?::.*)?$", "", path_text)
    if not path_text or Path(path_text).is_absolute():
        return False
    candidate = (corpus.root / path_text).resolve()
    try:
        candidate.relative_to(corpus.root.resolve())
    except ValueError:
        return False
    return candidate.is_file() and candidate != (corpus.root / MANUAL_LEDGER).resolve()


def validate_manual_review(
    corpus: Corpus, result: Result, literal: str, row: dict[str, str],
) -> list[str]:
    """Valida una adjudicación; una palabra como «CUMPLE» nunca basta."""
    rid = result.requirement_id
    errors = []
    expected_paths = manual_scope_paths(corpus, result)
    expected_scope = serialize_manual_scope(corpus, expected_paths)
    expected_digest = corpus.scoped_digest(expected_paths)
    expected_literal_digest = sha256_bytes(literal.encode("utf-8"))
    if row["id_requisito"] != rid:
        errors.append(f"{rid}: id interno no coincide")
    if row["requisito_literal"] != literal:
        errors.append(f"{rid}: literal no coincide con la matriz de requisitos")
    if row["huella_literal_sha256"] != expected_literal_digest:
        errors.append(f"{rid}: huella del literal desactualizada")
    if row["rutas_censadas"] != expected_scope:
        errors.append(f"{rid}: rutas censadas no coinciden con el alcance live")
    if row["huella_alcance_sha256"] != expected_digest:
        errors.append(f"{rid}: huella del alcance live desactualizada")

    nominal = row["prueba_nominal"].strip()
    generic = {"", "OK", "CUMPLE", "CONFORME", "REVISADO", "N/A", "PENDIENTE_REVISION"}
    if nominal.upper() in generic or len(nominal) < 40:
        errors.append(f"{rid}: falta describir una prueba nominal manual sustantiva")
    if row["resultado"] not in MANUAL_RESULTS:
        errors.append(f"{rid}: resultado manual fuera de {sorted(MANUAL_RESULTS)}")
    evidence = row["evidencia"].strip()
    if evidence.upper() in generic or len(evidence) < 30:
        errors.append(f"{rid}: evidencia manual vacía, genérica o insuficiente")
    locators = [
        value.strip() for value in row["localizadores_evidencia"].split(";")
        if value.strip()
    ]
    if not locators or any(not locator_resolves(corpus, value) for value in locators):
        errors.append(f"{rid}: localizador de evidencia ausente o no resoluble")
    reviewer = row["revisor"].strip()
    if len(reviewer) < 3 or reviewer.upper() in generic:
        errors.append(f"{rid}: revisor no identificado")
    if row["declaracion_independencia"] != INDEPENDENCE_DECLARATION:
        errors.append(f"{rid}: independencia no declarada con el valor canónico")
    try:
        reviewed = date.fromisoformat(row["fecha_revision"])
    except ValueError:
        errors.append(f"{rid}: fecha de revisión no es ISO YYYY-MM-DD")
    else:
        if reviewed > CUTOFF_DATE:
            errors.append(f"{rid}: fecha de revisión posterior al corte {CUTOFF_DATE}")
    return errors


def load_manual_reviews(
    corpus: Corpus,
    results: dict[str, Result],
    *,
    require_ledger: bool = False,
) -> tuple[dict[str, ManualReview], list[str]]:
    """Carga un ledger completo: cero filas parciales y cero autoatestaciones."""
    path = corpus.root / MANUAL_LEDGER
    if not path.exists():
        message = f"falta ledger manual: {MANUAL_LEDGER}"
        return ({}, [message] if require_ledger else [])
    header, rows = read_csv(path)
    if header != MANUAL_LEDGER_HEADER:
        return {}, [
            f"ledger manual con cabecera distinta; esperada {MANUAL_LEDGER_HEADER}"
        ]
    malformed = [
        index for index, row in enumerate(rows, 2)
        if None in row or any(value is None for value in row.values())
    ]
    if malformed:
        return {}, [
            f"ledger manual con filas de cardinalidad inválida: {malformed}"
        ]
    expected = {
        rid for rid, result in results.items() if not result.automated
    }
    seen = Counter(row["id_requisito"] for row in rows)
    errors = [
        f"{rid}: aparece {count} veces en ledger manual"
        for rid, count in sorted(seen.items()) if count != 1
    ]
    actual = set(seen)
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing:
        errors.append(f"ledger manual incompleto; faltan {missing}")
    if unexpected:
        errors.append(f"ledger manual contiene controles no pendientes: {unexpected}")
    literals = load_requirement_literals(corpus.root)
    reviews: dict[str, ManualReview] = {}
    for row in rows:
        rid = row["id_requisito"]
        if rid not in expected or seen[rid] != 1:
            continue
        if rid not in literals:
            errors.append(f"{rid}: no aparece en matriz de requisitos")
            continue
        row_errors = validate_manual_review(
            corpus, results[rid], literals[rid], row,
        )
        errors.extend(row_errors)
        if not row_errors:
            reviews[rid] = ManualReview(rid, row)
    if errors:
        return {}, errors
    return reviews, []


def add_targets(corpus: Corpus, row: dict[str, str], result: Result) -> None:
    claims = split_refs(row["afirmaciones_exactas"])
    tables = split_refs(row["tablas_exactas"])
    negatives = split_refs(row["busquedas_negativas_exactas"])
    result.metric("C_objetivo", len(claims))
    result.metric("tablas_objetivo", len(tables))
    result.metric("BN_objetivo", len(negatives))
    for claim_id in claims:
        result.check(
            claim_id in corpus.claims, f"existe {claim_id}",
            f"afirmación objetivo inexistente: {claim_id}",
        )
        if claim_id not in corpus.claims:
            continue
        claim = corpus.claims[claim_id]
        result.scope_paths.add(corpus.claim_paths[claim_id])
        result.check(
            all(claim[column].strip() for column in CLAIM_HEADER),
            f"{claim_id} sin celdas vacías", f"{claim_id} contiene celdas vacías",
        )
        cited = expand_source_refs(claim["Fuente"])
        result.check(
            all(source in corpus.sources for source in cited),
            f"{claim_id} cita S existentes",
            f"{claim_id} cita una fuente inexistente",
        )
    for table_id in tables:
        result.check(
            table_id in corpus.entries, f"existe {table_id}",
            f"tabla objetivo inexistente: {table_id}",
        )
        if table_id not in corpus.entries:
            continue
        path = corpus.root / corpus.entries[table_id]["csv_path"]
        result.scope_paths.add(path)
        header, rows = corpus.table_rows[table_id]
        result.check(bool(header), f"{table_id} tiene cabecera", f"{table_id} sin cabecera")
        result.check(bool(rows), f"{table_id} tiene filas", f"{table_id} sin filas")
        result.check(
            all(all(value.strip() for value in item.values()) for item in rows),
            f"{table_id} sin celdas vacías", f"{table_id} contiene celdas vacías",
        )
    for bn_id in negatives:
        result.check(
            bn_id in corpus.bn, f"existe {bn_id}",
            f"búsqueda negativa objetivo inexistente: {bn_id}",
        )
        if bn_id in corpus.bn:
            result.scope_paths.add(corpus.bn_paths[bn_id])


def check_header(corpus: Corpus, result: Result, letter: str, expected: list[str]) -> None:
    header, rows = corpus.appendices[letter]
    result.scope_paths.add(corpus.appendix_paths[letter])
    result.metric(f"filas_{letter}", len(rows))
    result.check(header == expected, f"cabecera {letter} exacta", f"cabecera {letter} distinta")


def check_enum(
    corpus: Corpus, result: Result, letter: str, column: str, allowed: set[str],
) -> None:
    rows = corpus.appendices[letter][1]
    result.scope_paths.add(corpus.appendix_paths[letter])
    invalid = sorted({row[column] for row in rows} - allowed)
    result.metric(f"valores_{column}", len(rows))
    result.check(not invalid, f"enum {column}", f"valores fuera del enum: {invalid}")


def check_all_machine_cells(corpus: Corpus, result: Result) -> None:
    paths = []
    empty = []
    row_count = 0
    for entry in corpus.index["tables"]:
        path = corpus.root / entry["csv_path"]
        header, rows = corpus.table_rows[entry["id"]]
        paths.append(path)
        row_count += len(rows)
        for row_number, row in enumerate(rows, 2):
            for column in header:
                if not row[column].strip():
                    empty.append(f"{entry['csv_path']}:{row_number}:{column}")
    for path in corpus.appendix_paths.values():
        header, rows = read_csv(path)
        paths.append(path)
        row_count += len(rows)
        for row_number, row in enumerate(rows, 2):
            for column in header:
                if not row[column].strip():
                    empty.append(f"{path.relative_to(corpus.root)}:{row_number}:{column}")
    result.scope_paths.update(paths)
    result.metric("filas_maquinables", row_count)
    result.check(not empty, "censo de celdas vacías", f"celdas vacías: {empty[:20]}")


def check_claim_schema(corpus: Corpus, result: Result) -> None:
    paths = set(corpus.claim_paths.values())
    result.scope_paths.update(paths)
    ordered = sorted(corpus.claims, key=natural)
    expected = [f"C-{number:03d}" if number < 1000 else f"C-{number}" for number in range(1, len(ordered) + 1)]
    bad_headers = [
        path.relative_to(corpus.root).as_posix() for path in paths
        if read_csv(path)[0] != CLAIM_HEADER
    ]
    result.metric("afirmaciones", len(ordered))
    result.check(not bad_headers, "cabeceras C exactas", f"cabeceras C distintas: {bad_headers}")
    result.check(ordered == expected, "C global correlativo", "secuencia C no es global y correlativa")
    invalid_attribution = sorted({
        row["Atribución"] for row in corpus.claims.values()
        if row["Atribución"] not in ATTRIBUTIONS
        and not (
            re.fullmatch(r"sintesis\(.+\)", row["Atribución"])
            and CLAIM_REF.search(row["Atribución"])
        )
    })
    result.check(
        not invalid_attribution, "enum C/Atribución",
        f"C/Atribución fuera de enum o síntesis sin orígenes: {invalid_attribution}",
    )
    for column, allowed in (
        ("Aceptación", ACCEPTANCE),
        ("Fuerza", STRENGTH), ("Resolución", RESOLUTION),
        ("Vigencia", VALIDITY),
    ):
        invalid = sorted({row[column] for row in corpus.claims.values()} - allowed)
        result.check(not invalid, f"enum C/{column}", f"C/{column} fuera de enum: {invalid}")
    no_motive = [
        row["#"] for row in corpus.claims.values()
        if row["Motivo"].strip().casefold() in {"", "n/a", "—", "sin motivo"}
        or "\n" in row["Motivo"].strip()
    ]
    result.check(not no_motive, "Motivo obligatorio", f"C sin Motivo: {no_motive[:20]}")
    weak_motive = [
        row["#"] for row in corpus.claims.values()
        if len(row["Motivo"].strip()) < 20
        or "\n" in row["Motivo"].strip()
    ]
    result.check(
        not weak_motive, "Motivo sustantivo de una línea",
        f"C con Motivo vacío/trivial o multilínea: {weak_motive[:20]}",
    )


def check_refs(corpus: Corpus, result: Result) -> None:
    bad_sources = []
    bad_claims = []
    for row in corpus.claims.values():
        bad_sources.extend(
            f"{row['#']}->{source}" for source in expand_source_refs(row["Fuente"])
            if source not in corpus.sources
        )
        bad_claims.extend(
            f"{row['#']}->{claim}" for claim in CLAIM_REF.findall(row["Fuente"])
            if claim not in corpus.claims
        )
    result.scope_paths.update(corpus.claim_paths.values())
    result.scope_paths.add(corpus.appendix_paths["A"])
    result.metric(
        "referencias_S",
        sum(len(expand_source_refs(row["Fuente"])) for row in corpus.claims.values()),
    )
    result.check(not bad_sources, "referencias S resolubles", f"S inexistentes: {bad_sources[:20]}")
    result.check(not bad_claims, "dependencias C resolubles", f"C inexistentes: {bad_claims[:20]}")


def check_semantics(corpus: Corpus, result: Result) -> None:
    code, output = corpus.semantic_audit()
    result.scope_paths.update(corpus.section_paths)
    result.scope_paths.update(corpus.claim_paths.values())
    result.metric("secciones_markdown", len(corpus.section_paths))
    result.check(code == 0, "audit_semantics.py", output or "auditoría semántica sin salida")
    result.witnesses.append(output.splitlines()[-1] if output else "sin salida")


def check_content_trace(corpus: Corpus, result: Result) -> None:
    """Verifica la puerta exacta por oración, arista y celda sustantiva."""
    code, output = corpus.content_trace_audit()
    result.scope_paths.update(corpus.section_paths)
    result.scope_paths.update(corpus.claim_paths.values())
    result.scope_paths.add(corpus.root / "scripts/build_content_trace.py")
    result.scope_paths.add(
        corpus.root / "data/auditoria/mapeo_celdas_afirmaciones.csv"
    )
    result.scope_paths.add(
        corpus.root
        / "docs/auditorias/matriz_trazabilidad_contenido_2026-08-08.csv"
    )
    result.metric("segmentos_trazabilidad", 0)
    match = re.search(r"(\d+) segmentos", output)
    if match:
        result.metric("segmentos_trazabilidad", int(match.group(1)))
    result.check(
        code == 0, "build_content_trace.py --check",
        output or "puerta de trazabilidad sin salida",
    )
    result.witnesses.append(output.splitlines()[-1] if output else "sin salida")


def check_h_counts(corpus: Corpus, result: Result) -> None:
    """Recalcula las cinco magnitudes obligatorias de H desde el corpus vivo."""
    header, rows = corpus.appendices["H"]
    result.scope_paths.add(corpus.appendix_paths["H"])
    controls = [row["control"] for row in rows]
    duplicate = sorted(
        key for key, count in Counter(controls).items() if count != 1
    )
    by_control = {row["control"]: row["valor"] for row in rows}

    section_text = "\n".join(corpus.section_text.values())
    single_source = sum(
        len(set(expand_source_refs(row["Fuente"]))) == 1
        for row in corpus.claims.values()
    )
    sin_cifra = 0
    for entry in corpus.index["tables"]:
        if entry["id"] == "appendix-h":
            continue
        _, table_rows = corpus.table_rows[entry["id"]]
        sin_cifra += sum(
            cell.count("SIN CIFRA PUBLICADA LOCALIZADA")
            for row in table_rows for cell in row.values()
        )
    expected = {
        "número total de fuentes distintas": len(corpus.sources),
        "número de oraciones marcadas `[SIN FUENTE]`": len(re.findall(
            r"(?m)^\[SIN FUENTE\]", section_text,
        )),
        "número de filas del registro": len(corpus.claims),
        "número actual de afirmaciones que dependen de una sola fuente": single_source,
        "número de celdas con `SIN CIFRA PUBLICADA LOCALIZADA`": sin_cifra,
    }
    missing = sorted(set(expected) - set(by_control))
    non_integer = sorted(
        key for key in expected
        if key in by_control and not re.fullmatch(r"\d+", by_control[key])
    )
    mismatches = sorted(
        f"{key}:registrado={by_control[key]},esperado={value}"
        for key, value in expected.items()
        if key in by_control and by_control[key].isdigit()
        and int(by_control[key]) != value
    )
    result.metric("controles_H_obligatorios", len(expected))
    result.check(header == ["control", "valor"], "cabecera H exacta", "cabecera H distinta")
    result.check(not duplicate, "controles H únicos", f"controles H duplicados: {duplicate}")
    result.check(not missing, "cinco controles H presentes", f"controles H ausentes: {missing}")
    result.check(not non_integer, "valores H enteros", f"valores H no enteros: {non_integer}")
    result.check(not mismatches, "valores H reproducibles", f"recuentos H desactualizados: {mismatches}")


def check_final_questions(
    corpus: Corpus, manifest_row: dict[str, str], result: Result,
) -> None:
    """Prueba las seis respuestas, sus destinos y sus referencias resolubles."""
    table_ids = split_refs(manifest_row["tablas_exactas"])
    result.metric("tablas_cierre", len(table_ids))
    result.check(
        len(table_ids) == 1 and table_ids[0] in corpus.table_rows,
        "una tabla de cierre resoluble",
        f"tablas de cierre inválidas: {table_ids}",
    )
    if len(table_ids) != 1 or table_ids[0] not in corpus.table_rows:
        return
    table_id = table_ids[0]
    path = corpus.root / corpus.entries[table_id]["csv_path"]
    result.scope_paths.add(path)
    header, rows = corpus.table_rows[table_id]
    expected_header = [
        "pregunta", "secciones con material integrado",
        "respuesta breve con citas",
    ]
    result.metric("preguntas_cierre", len(rows))
    result.check(header == expected_header, "cabecera cierre exacta", "cabecera cierre distinta")
    result.check(len(rows) == 6, "seis preguntas de cierre", f"cierre contiene {len(rows)} preguntas")
    numbering = [row["pregunta"].lstrip().split(".", 1)[0] for row in rows]
    result.check(numbering == [str(number) for number in range(1, 7)], "preguntas 1-6", f"numeración: {numbering}")
    empty_destinations = [
        number for number, row in enumerate(rows, 1)
        if not row["secciones con material integrado"].strip()
    ]
    result.check(
        not empty_destinations, "destino por pregunta",
        f"preguntas sin secciones de destino: {empty_destinations}",
    )
    bad_answers = []
    for number, row in enumerate(rows, 1):
        answer = row["respuesta breve con citas"]
        claims = CLAIM_REF.findall(answer)
        sources = expand_source_refs(answer)
        explicit_gap = "literatura no" in answer.casefold()
        if (
            not claims
            or any(claim not in corpus.claims for claim in claims)
            or (not sources and not explicit_gap)
            or any(source not in corpus.sources for source in sources)
        ):
            bad_answers.append(number)
    result.check(
        not bad_answers, "respuesta con C y S resolubles o hueco explícito",
        f"respuestas sin cierre trazable: {bad_answers}",
    )


def check_teleology_candidates(corpus: Corpus, result: Result) -> None:
    """Censa usos potenciales y admite solo contextos críticos/comparativos.

    El veredicto no depende de la mera coincidencia: cada candidato se clasifica
    por contexto estructural. Se permiten la sección terminológica 14.6, su
    tabla de reemplazos, y comparativos mensurables (``superior/inferior a``).
    """
    pattern = re.compile(
        r"\b(superior|inferior|primitiv[oa]s?|avanzad[oa]s?|más evolucionad[oa]s?|"
        r"intento fallido|paso obligatorio|fósil viviente|eslabón perdido|"
        r"eucariota primitivo|organismo simple|versi[oó]n antigua|"
        r"versi[oó]n detenida)\b|apareci[oó] para|"
        r"todavía no hab[ií]a desarrollado",
        re.IGNORECASE,
    )
    candidates = []
    violations = []
    paths = [*corpus.section_paths, *sorted(set(corpus.claim_paths.values()))]
    paths += [corpus.root / entry["csv_path"] for entry in corpus.index["tables"]]
    paths += list(corpus.appendix_paths.values())
    for path in sorted(set(paths)):
        result.scope_paths.add(path)
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not pattern.search(line):
                continue
            relative = path.relative_to(corpus.root).as_posix()
            candidates.append(f"{relative}:{line_number}")
            critical_context = (
                "14-nombres-y-nomenclatura" in relative
                or "table-58-14-8-3" in relative
                or "B_entidades.csv" in relative
                or any(token in line.casefold() for token in (
                    "sustitu", "término", "metáfora", "uso legítimo", "no significa",
                    "puede inducir error", "puede ocultar", "confunde", "representa la evolución",
                    "métrica", "criterio", "terminolog", "históric",
                    "límite superior", "límite inferior", "fosforito superior",
                    "nodo superior",
                ))
            )
            quantitative_comparison = bool(re.search(
                r"\b(?:superior(?:es)?|inferior(?:es)?)\s+a\b|\borden superior\b|"
                r"observación directa.*superior a inventario", line, re.IGNORECASE,
            ))
            molecular_targeting = "destinad" in line.casefold() and "mitocond" in line.casefold()
            if not (critical_context or quantitative_comparison or molecular_targeting):
                violations.append(f"{relative}:{line_number}")
    result.metric("candidatos_teleologia", len(candidates))
    result.check(
        not violations, "clasificación contextual de candidatos teleológicos",
        f"candidatos no clasificados: {violations[:30]}",
    )
    result.witnesses.append(f"candidatos clasificados={len(candidates)}")


def check_teleology_policy_details(
    corpus: Corpus, result: Result, requirement_id: str,
) -> None:
    """Materializa los submandatos positivos que el censo léxico no prueba."""
    text = "\n".join(corpus.section_text.values())
    if requirement_id == "R-0004":
        living = [
            row for row in corpus.claims.values()
            if "linajes vivientes hermanos" in row["Sujeto"].casefold()
            and "ninguno de los dos es el ancestro del otro" in row["Afirmación"].casefold()
            and "mismo tiempo transcurrido" in row["Motivo"].casefold()
        ]
        result.metric("anclas_linajes_vivientes", len(living))
        result.check(
            bool(living), "linajes vivientes no son ancestros detenidos",
            "falta una fila que explicite contemporaneidad, ancestro común y tiempo "
            "transcurrido para linajes vivientes",
        )
    elif requirement_id == "R-0006":
        node_ids = [
            table_id for table_id in corpus.table_rows
            if re.fullmatch(r"table-(?:1[6-9]|2[0-9]|3[0-2])-.*", table_id)
        ]
        missing_sister = []
        for table_id in node_ids:
            header, rows = corpus.table_rows[table_id]
            column = "qué linaje queda fuera (grupo hermano)"
            if column not in header or any(
                row[column].strip().casefold() in {"", "n/a", "—", "-"}
                for row in rows
            ):
                missing_sister.append(table_id)
        disclaimer = bool(re.search(
            r"corredor.{0,120}(?:no (?:es|implica)|sin).{0,80}"
            r"(?:direcci[oó]n|orientaci[oó]n|progreso)|"
            r"no.{0,80}(?:orientad[oa]|dirigid[oa]).{0,80}Holozoa",
            text, re.IGNORECASE | re.DOTALL,
        ))
        result.metric("tablas_nodales_con_hermana", len(node_ids) - len(missing_sister))
        result.check(
            bool(node_ids) and not missing_sister,
            "rama hermana por nodo del corredor",
            f"tablas nodales sin hermana explícita: {missing_sister}",
        )
        result.check(
            disclaimer, "corredor declarado no direccional",
            "falta declarar explícitamente que el corredor es alcance de muestreo, "
            "no dirección u orientación hacia Holozoa",
        )


def check_game_boundary(
    corpus: Corpus, result: Result, requirement_id: str,
) -> None:
    text = "\n".join(corpus.section_text.values())
    result.scope_paths.update(corpus.section_paths)
    proposal = re.compile(
        r"\b(?:propon(?:go|emos|er)|diseñ(?:o|amos|ar)|defin(?:o|imos|ir)|"
        r"asign(?:o|amos|ar))\b.{0,60}\b(?:variables?|mec[aá]nicas?|reglas?|"
        r"par[aá]metros?|escalas?|puntos?|turnos?)\b.{0,60}"
        r"\b(?:juego|jugable|simulaci[oó]n)\b|\b(?:variable|par[aá]metro|"
        r"escala|regla|mec[aá]nica)s? (?:del|para el) juego\b",
        re.IGNORECASE | re.DOTALL,
    )
    hits = [match.group(0)[:160] for match in proposal.finditer(text)]
    result.metric("propuestas_jugables", len(hits))
    result.check(
        not hits, "sin diseño jugable anticipado",
        f"propuestas de diseño localizadas: {hits[:10]}",
    )


def check_narrative_requirements(corpus: Corpus, result: Result) -> None:
    text = "\n".join(corpus.section_text.values())
    result.scope_paths.update(corpus.section_paths)
    required = {
        "fecha de corte": "Fecha de corte bibliográfico",
        "corredor terminal": "Choanozoa",
        "coanoflagelados": "Salpingoeca rosetta",
        "comparandos": "Monocercomonoides",
        "Asgard": "Prometheoarchaeum",
        "alfaproteobacterias": "alfaproteobacter",
        "Doushantuo": "Doushantuo",
        "autoridad Adl": "Adl et al.",
        "ICS": "ICS",
        "recursos de secuencia": "EukProt",
    }
    missing = [label for label, token in required.items() if token.casefold() not in text.casefold()]
    result.metric("hitos_editoriales", len(required))
    result.check(not missing, "hitos narrativos exigidos", f"hitos ausentes: {missing}")


def check_source_catalog(corpus: Corpus, result: Result) -> None:
    check_header(corpus, result, "A", SOURCE_HEADER)
    check_enum(corpus, result, "A", "tipo", SOURCE_TYPES)
    rows = corpus.appendices["A"][1]
    duplicate = [key for key, count in Counter(row["clave"] for row in rows).items() if count != 1]
    naked = [row["clave"] for row in rows if not row["autores"] or not row["año"] or not row["título"]]
    bad_url = [row["clave"] for row in rows if not row[SOURCE_HEADER[5]].startswith(("https://", "http://", "DOI no verificado"))]
    result.metric("fuentes", len(rows))
    result.check(not duplicate, "claves S únicas", f"S duplicadas: {duplicate}")
    result.check(not naked, "sin URL desnuda", f"fuentes sin identidad: {naked[:20]}")
    result.check(not bad_url, "DOI/URL resoluble", f"DOI/URL inválido: {bad_url[:20]}")


def check_appendix_refs(corpus: Corpus, result: Result) -> None:
    bad = []
    for letter in "BCDEFG":
        path = corpus.appendix_paths[letter]
        result.scope_paths.add(path)
        for row_number, row in enumerate(corpus.appendices[letter][1], 2):
            for claim in CLAIM_REF.findall(" ".join(row.values())):
                if claim not in corpus.claims:
                    bad.append(f"{letter}:{row_number}->{claim}")
    result.metric("filas_apendices_B_G", sum(len(corpus.appendices[x][1]) for x in "BCDEFG"))
    result.check(not bad, "referencias C de B-G", f"C inexistentes en apéndices: {bad[:20]}")


AUTOMATION_FAMILY_BY_ID = {
    **{
        f"R-{number:04d}": "TELEOLOGIA_CONTEXTO"
        for number in range(1, 8)
    },
    "R-0018": "SIN_DISENO_DE_JUEGO",
    "R-0019": "SIN_DISENO_DE_JUEGO",
    "R-0021": "SIN_DISENO_DE_JUEGO",
}

AUTOMATION_FAMILY_BY_SLUG = {
    "11_COLUMNAS_ORDEN_EXACTO": "ESQUEMA_AFIRMACIONES",
    "ID_C_GLOBAL_CORRELATIVO_NO_REINICIADO": "ESQUEMA_AFIRMACIONES",
    "ATRIBUCION_UNO_DE_TRES_VALORES": "ESQUEMA_AFIRMACIONES",
    "ACEPTACION_ENUM_5": "ESQUEMA_AFIRMACIONES",
    "FUERZA_ENUM_4": "ESQUEMA_AFIRMACIONES",
    "MOTIVO_FUERZA_OBLIGATORIO": "ESQUEMA_AFIRMACIONES",
    "SIN_MOTIVO_FUERZA_INVALIDA": "ESQUEMA_AFIRMACIONES",
    "RESOLUCION_ENUM_4": "ESQUEMA_AFIRMACIONES",
    "VIGENCIA_ENUM_4": "ESQUEMA_AFIRMACIONES",
    "ESQUEMA_FUENTES_9_COLUMNAS": "CATALOGO_FUENTES",
    "TIPO_FUENTE_ENUM_8": "CATALOGO_FUENTES",
    "SIN_URL_DESNUDA": "CATALOGO_FUENTES",
    "ESQUEMA_ENTIDADES_5_COLUMNAS": "ESQUEMA_APENDICE_B",
    "ESQUEMA_EVENTOS_7_COLUMNAS": "ESQUEMA_APENDICE_C",
    "TIPO_EVENTO_ENUM_CERRADO": "ENUM_EVENTOS",
    "ROL_PARTICIPANTE_ENUM_CERRADO": "ENUM_EVENTOS",
    "PAPEL_OBLIGATORIO_DIRECCION_EVENTO": "ENUM_EVENTOS",
    "COLUMNA_DESENLACE_ENUM_6": "ENUM_EVENTOS",
    "ESQUEMA_CRONOLOGIA_COLUMNAS_EXACTAS": "ESQUEMA_APENDICE_D",
    "ESQUEMA_HIPOTESIS_COLUMNAS_EXACTAS": "ESQUEMA_APENDICE_E",
    "ESQUEMA_CIFRAS_9_COLUMNAS": "ESQUEMA_APENDICE_F",
    "SIN_CAMPOS_EN_BLANCO": "CENSO_CELDAS_MAQUINABLES",
    "NINGUNA_AFIRMACION_SOLO_NARRATIVA": "TRAZABILIDAD_CONTENIDO_EXACTA",
    "PROSA_A_REGISTRO_COBERTURA_100": "TRAZABILIDAD_CONTENIDO_EXACTA",
    "ARISTA_ARBOL_A_FILA_REGISTRO_100": "TRAZABILIDAD_CONTENIDO_EXACTA",
    "ORACION_CIENTIFICA_CON_C": "TRAZABILIDAD_CONTENIDO_EXACTA",
    "VISTA_RESUMEN_SUBCONJUNTO_REGISTRO": "TRAZABILIDAD_CONTENIDO_EXACTA",
    "FUENTES_DISTINTAS_GT_80": "RECUENTO_FUENTES",
    "TABLA_POR_NODO_Y_RAMA_SCHEMA": "ESQUEMA_TABLAS_NODALES",
    "RECUENTO_FINAL_5_MAGNITUDES": "RECUENTOS_H_REPRODUCIBLES",
    "APARTADO_FINAL_6_PREGUNTAS_REFERENCIAS_O_NO_RESPUESTA": "CIERRE_SEIS_PREGUNTAS",
    "PALABRAS_SECCIONES5_13_GE_EUCARIOGENESIS_MAS_NOMENCLATURA": "REPARTO_PALABRAS",
}


def check_specific(corpus: Corpus, manifest_row: dict[str, str], result: Result) -> None:
    rid, slug = result.requirement_id, result.slug

    # Restricciones globales cuya prueba necesita el corpus completo.
    if rid in {f"R-{number:04d}" for number in range(1, 8)}:
        check_teleology_candidates(corpus, result)
        check_teleology_policy_details(corpus, result, rid)
    if rid in {"R-0008", "R-0009", "R-0010", "R-0011", "R-0012", "R-0013", "R-0014", "R-0015", "R-0016", "R-0017"}:
        check_refs(corpus, result)
        check_source_catalog(corpus, result)
        check_appendix_refs(corpus, result)
    if rid in {"R-0018", "R-0019", "R-0021"}:
        forbidden = re.compile(r"\b(puntos de experiencia|regla de juego|mecánica jugable propuesta|turnos de juego)\b", re.IGNORECASE)
        hits = []
        for path, text in corpus.section_text.items():
            result.scope_paths.add(path)
            hits.extend(f"{path.relative_to(corpus.root)}:{m.start()}" for m in forbidden.finditer(text))
        result.metric("candidatos_diseno_juego", len(hits))
        result.check(not hits, "censo de diseño de juego", f"propuestas de juego: {hits[:20]}")
        check_game_boundary(corpus, result, rid)
    if rid in {"R-0022", "R-0023", "R-0024", "R-0025"}:
        check_claim_schema(corpus, result)
        check_all_machine_cells(corpus, result)
    if rid in {"R-0026", "R-0028", "R-0029"}:
        check_narrative_requirements(corpus, result)
    if rid in {f"R-{number:04d}" for number in range(31, 48)}:
        check_narrative_requirements(corpus, result)
        check_semantics(corpus, result)

    # Esquemas y enumeraciones de la capa de registro/apéndices.
    if any(token in slug for token in ("11_COLUMNAS", "ID_C_GLOBAL", "ATRIBUCION_", "ACEPTACION_ENUM", "FUERZA_ENUM", "RESOLUCION_ENUM", "VIGENCIA_ENUM", "MOTIVO_FUERZA")):
        check_claim_schema(corpus, result)
    if slug == "ESQUEMA_FUENTES_9_COLUMNAS" or "TIPO_FUENTE_ENUM" in slug or "SIN_URL_DESNUDA" in slug:
        check_source_catalog(corpus, result)
    if slug == "ESQUEMA_ENTIDADES_5_COLUMNAS":
        check_header(corpus, result, "B", ENTITY_HEADER)
    if slug == "ESQUEMA_EVENTOS_7_COLUMNAS":
        check_header(corpus, result, "C", EVENT_HEADER)
    if slug == "TIPO_EVENTO_ENUM_CERRADO":
        check_enum(corpus, result, "C", "tipo", EVENT_TYPES)
    if slug == "COLUMNA_DESENLACE_ENUM_6":
        check_enum(corpus, result, "C", "desenlace", OUTCOMES)
    if slug in {"ROL_PARTICIPANTE_ENUM_CERRADO", "PAPEL_OBLIGATORIO_DIRECCION_EVENTO"}:
        rows = corpus.appendices["C"][1]
        corpus_path = corpus.appendix_paths["C"]
        result.scope_paths.add(corpus_path)
        bad = []
        for row in rows:
            participants = [part.strip() for part in row["participantes con su papel"].split(";")]
            for participant in participants:
                if not any(re.search(rf"\b{re.escape(role)}\b", participant, re.IGNORECASE) for role in EVENT_ROLES):
                    bad.append(f"{row['clave']}:{participant}")
        result.metric("participantes_evento", sum(len(row["participantes con su papel"].split(";")) for row in rows))
        result.check(not bad, "papel por participante", f"participantes sin papel cerrado: {bad[:20]}")
    if slug == "ESQUEMA_CRONOLOGIA_COLUMNAS_EXACTAS":
        check_header(corpus, result, "D", DATE_HEADER)
    if slug == "ESQUEMA_HIPOTESIS_COLUMNAS_EXACTAS":
        check_header(corpus, result, "E", HYPOTHESIS_HEADER)
    if slug == "ESQUEMA_CIFRAS_9_COLUMNAS":
        check_header(corpus, result, "F", MAGNITUDE_HEADER)
    if slug in {"TABLAS_MARKDOWN_COLUMNAS_ORDEN_SIN_EXTRAS", "NA_EN_CAMPO_NO_APLICA", "SIN_CAMPOS_EN_BLANCO", "REGISTRO_MAQUINABLE"}:
        check_all_machine_cells(corpus, result)

    # Reglas referenciales y de cobertura ya expresadas por auditorías vivas.
    semantic_slugs = (
        "NINGUNA_AFIRMACION_SOLO_NARRATIVA", "PROSA_A_REGISTRO_COBERTURA_100",
        "ARISTA_ARBOL_A_FILA_REGISTRO_100", "ORACION_CIENTIFICA_CON_C",
        "H2_MINIMO_DOS_FUENTES", "VISTA_RESUMEN_SUBCONJUNTO_REGISTRO",
        "LOCALIZADOR_OBLIGATORIO", "FUENTE_CLAVE_Y_LOCALIZADOR",
        "SIN_LOCALIZADOR_SOLO_TESIS", "LOCALIZADOR_ATOMICIDAD_PASAJE",
    )
    if any(token in slug for token in semantic_slugs):
        check_semantics(corpus, result)
    trace_slugs = (
        "NINGUNA_AFIRMACION_SOLO_NARRATIVA",
        "PROSA_A_REGISTRO_COBERTURA_100",
        "ARISTA_ARBOL_A_FILA_REGISTRO_100",
        "ORACION_CIENTIFICA_CON_C",
        "VISTA_RESUMEN_SUBCONJUNTO_REGISTRO",
    )
    if any(token in slug for token in trace_slugs):
        check_content_trace(corpus, result)
    if any(token in slug for token in ("SOLO_CLAVES_LOCALES", "PREFIJOS_EXTERNOS_PROHIBIDOS", "CRONOLOGIA_UNA_FILA", "CIFRAS_CONSOLIDADAS", "ENTIDAD_UNA_FILA", "EVENTO_UNA_FILA", "HIPOTESIS_NOMBRADA")):
        check_appendix_refs(corpus, result)
    if any(token in slug for token in ("ACEPTACION_CON_FUENTE", "CONSENSO_NO_SOSTENIDO", "NO_ATRIBUIR_GLOSA", "SINTESIS_CON_FILAS", "CUESTIONADO_POR", "CONSERVAR_FILA", "CONTRAEVIDENCIA")):
        check_refs(corpus, result)
        check_claim_schema(corpus, result)

    # Controles cuantitativos de cierre.
    if slug == "FUENTES_DISTINTAS_GT_80":
        result.scope_paths.add(corpus.appendix_paths["A"])
        result.metric("fuentes_distintas", len(corpus.sources))
        result.check(len(corpus.sources) > 80, "fuentes > 80", f"solo {len(corpus.sources)} fuentes")
    if slug == "H2_MINIMO_DOS_FUENTES":
        check_semantics(corpus, result)
    if slug == "TABLA_POR_NODO_Y_RAMA_SCHEMA":
        table_ids = split_refs(manifest_row["tablas_exactas"])
        expected = [
            "nodo", "qué linajes quedan dentro", "qué linaje queda fuera (grupo hermano)",
            "caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente",
            "caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente",
            "tipo de evidencia que sostiene el nodo", "soporte cuantitativo transcrito literalmente",
            "edad estimada con intervalo", "método de la estimación",
            "# de la fila del registro que sostiene cada celda sustantiva",
        ]
        bad = [table_id for table_id in table_ids if corpus.table_rows.get(table_id, ([], []))[0] != expected]
        result.metric("tablas_nodales", len(table_ids))
        result.check(len(table_ids) == 17, "17 tablas nodales", f"se esperaban 17, hay {len(table_ids)}")
        result.check(not bad, "esquema nodal exacto", f"tablas nodales con esquema distinto: {bad}")
    if slug == "RECUENTO_FINAL_5_MAGNITUDES":
        check_h_counts(corpus, result)
    if slug == "APARTADO_FINAL_6_PREGUNTAS_REFERENCIAS_O_NO_RESPUESTA":
        check_final_questions(corpus, manifest_row, result)
    if slug == "PALABRAS_SECCIONES5_13_GE_EUCARIOGENESIS_MAS_NOMENCLATURA":
        word_counts = {}
        for path, text in corpus.section_text.items():
            match = re.search(r"^# (\d+)\.", text, re.MULTILINE)
            if match:
                word_counts[int(match.group(1))] = len(re.findall(r"\b\w+\b", text))
                result.scope_paths.add(path)
        left = sum(word_counts.get(n, 0) for n in range(5, 14))
        right = word_counts.get(3, 0) + word_counts.get(14, 0)
        result.metric("palabras_secciones_5_13", left)
        result.metric("palabras_secciones_3_14", right)
        result.check(left >= right, "reparto de palabras", f"5-13={left} < 3+14={right}")

    family = (
        AUTOMATION_FAMILY_BY_ID.get(rid)
        or AUTOMATION_FAMILY_BY_SLUG.get(slug)
    )
    if family:
        result.automate(family)


def evaluate(corpus: Corpus, row: dict[str, str]) -> Result:
    rid = row["id_requisito"]
    slug = row["control_o_rollup"].split("::")[-1]
    result = Result(rid, slug)
    result.scope_paths.add(corpus.index_path)
    if isinstance(getattr(corpus, "root", None), Path):
        result.scope_paths.update({
            corpus.root / "scripts/audit_requirement_controls.py",
            corpus.root / "scripts/corpus_io.py",
        })
    add_targets(corpus, row, result)
    target_checks = len(result.checks)
    check_specific(corpus, row, result)
    nominal_checks = len(result.checks) - target_checks
    if result.automated and nominal_checks <= 0:
        result.automation_families.clear()
        result.errors.append(
            "configuración inválida: familia automatizada sin ninguna prueba "
            "nominal adicional a existencia/no-vacío"
        )
    if not result.automated:
        result.check(
            False,
            "control nominal específico implementado",
            "PENDIENTE_AUTOMATIZACION_NOMINAL: existencia/no-vacío, referencias "
            "genéricas o una puerta agregada no acreditan este mandato literal",
        )
    result.metric("pruebas", len(result.checks))
    result.metric("pruebas_nominales", max(0, nominal_checks))
    result.metric("fallos", len(result.errors))
    return result


def scope_text(corpus: Corpus, result: Result) -> str:
    digest = corpus.scoped_digest(result.scope_paths)
    metrics = ",".join(f"{key}={value}" for key, value in sorted(result.metrics.items()))
    return (
        f"corpus_live; control={result.slug}; clasificacion="
        f"{'AUTOMATIZADO' if result.automated else 'PENDIENTE'}; familias="
        f"{','.join(sorted(result.automation_families)) or 'n/a'}; "
        f"ficheros={len(result.scope_paths)}; "
        f"{metrics}; sha256_censo={digest}"
    )


def evidence_text(corpus: Corpus, result: Result) -> str:
    checks_hash = sha256_bytes("\n".join(result.checks).encode("utf-8"))
    locations = ";".join(
        path.relative_to(corpus.root).as_posix()
        for path in sorted(result.scope_paths)
    )
    if len(locations) > 1800:
        locations = locations[:1800] + "…"
    details = (
        "ninguna infracción" if not result.errors
        else " | ".join(result.errors[:20])
    )
    witnesses = " | ".join(result.witnesses[:5]) or "censo estructural nominal"
    return (
        f"clasificacion={'AUTOMATIZADO' if result.automated else 'PENDIENTE'}; "
        f"familias={','.join(sorted(result.automation_families)) or 'n/a'}; "
        f"pruebas={len(result.checks)}; fallos={len(result.errors)}; "
        f"sha256_pruebas={checks_hash}; testigo={witnesses}; detalle={details}; "
        f"localizadores={locations}"
    )


def artifact_row(corpus: Corpus, result: Result) -> dict[str, str]:
    command = (
        "python3 scripts/audit_requirement_controls.py --root . "
        f"--requirement {result.requirement_id}"
    )
    return {
        "id_requisito": result.requirement_id,
        "alcance_o_censo": scope_text(corpus, result),
        "comando_o_consulta": command,
        "resultado_control": "CERO_FALLOS" if not result.errors else "NO_CONFORME",
        "evidencia": evidence_text(corpus, result),
    }


def manual_artifact_row(
    corpus: Corpus, result: Result, review: ManualReview,
) -> dict[str, str]:
    row = review.row
    paths = manual_scope_paths(corpus, result)
    ledger_sha = sha256_file(corpus.root / MANUAL_LEDGER)
    outcome = "CONFORME_REVISION_MANUAL" if review.conforms else "NO_CONFORME"
    return {
        "id_requisito": result.requirement_id,
        "alcance_o_censo": (
            f"corpus_live; control={result.slug}; "
            "clasificacion=REVISION_MANUAL_INDEPENDIENTE; "
            f"ficheros={len(paths)}; sha256_censo={row['huella_alcance_sha256']}"
        ),
        "comando_o_consulta": (
            "python3 scripts/audit_requirement_controls.py --root . "
            "--verify-manual-ledger"
        ),
        "resultado_control": outcome,
        "evidencia": (
            f"prueba_nominal={row['prueba_nominal']}; resultado={row['resultado']}; "
            f"evidencia={row['evidencia']}; "
            f"localizadores={row['localizadores_evidencia']}; "
            f"revisor={row['revisor']}; "
            f"independencia={row['declaracion_independencia']}; "
            f"fecha={row['fecha_revision']}; "
            f"sha256_literal={row['huella_literal_sha256']}; "
            f"sha256_ledger={ledger_sha}"
        ),
    }


def load_control_rows(root: Path) -> tuple[list[str], list[dict[str, str]]]:
    header, rows = read_csv(root / MANIFEST)
    controls = [row for row in rows if row["tipo"] == "CONTROL_ESTRUCTURAL"]
    if len(controls) != 252:
        raise RuntimeError(f"se esperaban 252 controles estructurales, hay {len(controls)}")
    return header, rows


def materialize(root: Path) -> int:
    corpus = Corpus(root)
    header, rows = load_control_rows(root)
    results = {row["id_requisito"]: evaluate(corpus, row) for row in rows if row["tipo"] == "CONTROL_ESTRUCTURAL"}
    reviews, ledger_errors = load_manual_reviews(corpus, results)
    if ledger_errors:
        print(f"LEDGER MANUAL INVÁLIDO: {len(ledger_errors)}")
        for error in ledger_errors:
            print(f"- {error}")
        return 1
    artifacts: dict[str, bytes] = {}
    for rid, result in results.items():
        artifact = (
            manual_artifact_row(corpus, result, reviews[rid])
            if rid in reviews else artifact_row(corpus, result)
        )
        artifacts[rid] = csv_bytes(ARTIFACT_HEADER, [artifact])
    for row in rows:
        if row["tipo"] != "CONTROL_ESTRUCTURAL":
            continue
        rid = row["id_requisito"]
        result = results[rid]
        review = reviews.get(rid)
        artifact = (
            manual_artifact_row(corpus, result, review)
            if review else artifact_row(corpus, result)
        )
        artifact_path = root / ARTIFACT_DIR / f"{rid}.csv"
        verified = (result.automated and not result.errors) or bool(
            review and review.conforms
        )
        if not verified:
            row["estado_disposicion"] = "CONTROL_DEFINIDO"
            row["alcance_o_censo"] = "PENDIENTE"
            row["comando_o_consulta"] = "PENDIENTE"
            row["resultado_control"] = "PENDIENTE"
            row["huella_control_sha256"] = "PENDIENTE"
            if review:
                row["accion"] = (
                    "Resolver hallazgo de revisión manual independiente: "
                    + review.row["evidencia"]
                )
            elif not result.automated:
                row["accion"] = (
                    "Pendiente de prueba nominal automatizada o revisión manual "
                    "independiente; conservar CONTROL_DEFINIDO."
                )
            else:
                row["accion"] = "Corregir control automatizado: " + " | ".join(
                    result.errors[:8]
                )
        else:
            row["estado_disposicion"] = "CONTROL_VERIFICADO"
            row["alcance_o_censo"] = artifact["alcance_o_censo"]
            row["comando_o_consulta"] = artifact["comando_o_consulta"]
            row["resultado_control"] = artifact["resultado_control"]
            row["huella_control_sha256"] = sha256_bytes(artifacts[rid])
            if review:
                row["accion"] = (
                    f"Control {rid} adjudicado por revisión manual independiente "
                    f"de {review.row['revisor']} el {review.row['fecha_revision']}; "
                    "literal y alcance live verificados por huella."
                )
            else:
                row["accion"] = (
                    f"Control nominal {rid} ejecutado sobre corpus live; "
                    f"{len(result.checks)} pruebas deterministas, cero fallos."
                )
        atomic_write(artifact_path, artifacts[rid])
    atomic_write(root / MANIFEST, csv_bytes(header, rows))
    automated = [result for result in results.values() if result.automated]
    pending = [result for result in results.values() if not result.automated]
    failed = [result for result in automated if result.errors]
    manual_nonconforming = [review for review in reviews.values() if not review.conforms]
    print(
        f"CONTROLES MATERIALIZADOS: total={len(results)}; "
        f"automatizados={len(automated)}; pendientes={len(pending)}; "
        f"verificados={len(automated)-len(failed)}; "
        f"automatizados_no_conformes={len(failed)}; "
        f"revisados_manualmente={len(reviews)}; "
        f"manuales_no_conformes={len(manual_nonconforming)}"
    )
    for result in failed:
        print(f"- {result.requirement_id}: {' | '.join(result.errors[:5])}")
    for review in manual_nonconforming:
        print(f"- {review.requirement_id}: {review.row['evidencia']}")
    return 1 if failed or manual_nonconforming else 0


def verify_artifacts(root: Path) -> int:
    corpus = Corpus(root)
    _, rows = load_control_rows(root)
    control_rows = [row for row in rows if row["tipo"] == "CONTROL_ESTRUCTURAL"]
    results = {
        row["id_requisito"]: evaluate(corpus, row) for row in control_rows
    }
    reviews, ledger_errors = load_manual_reviews(corpus, results)
    errors = list(ledger_errors)
    for row in rows:
        if row["tipo"] != "CONTROL_ESTRUCTURAL":
            continue
        rid = row["id_requisito"]
        result = results[rid]
        review = reviews.get(rid)
        artifact = (
            manual_artifact_row(corpus, result, review)
            if review else artifact_row(corpus, result)
        )
        expected = csv_bytes(ARTIFACT_HEADER, [artifact])
        path = root / ARTIFACT_DIR / f"{row['id_requisito']}.csv"
        if not path.exists() or path.read_bytes() != expected:
            errors.append(f"{row['id_requisito']}: artefacto no reproduce el censo live")
        verified = (result.automated and not result.errors) or bool(
            review and review.conforms
        )
        if verified:
            if row["estado_disposicion"] != "CONTROL_VERIFICADO":
                errors.append(f"{row['id_requisito']}: cero fallos sin promoción")
            elif any(row[column] != artifact[column] for column in (
                "alcance_o_censo", "comando_o_consulta", "resultado_control",
            )):
                errors.append(f"{row['id_requisito']}: manifiesto no reproduce artefacto")
            elif row["huella_control_sha256"] != sha256_bytes(expected):
                errors.append(f"{row['id_requisito']}: SHA de artefacto desactualizado")
        elif row["estado_disposicion"] != "CONTROL_DEFINIDO":
            errors.append(f"{row['id_requisito']}: control fallido promovido")
        elif {
            row["alcance_o_censo"], row["comando_o_consulta"],
            row["resultado_control"], row["huella_control_sha256"],
        } != {"PENDIENTE"}:
            errors.append(
                f"{row['id_requisito']}: CONTROL_DEFINIDO conserva una "
                "atestación parcial o residual"
            )
    if errors:
        print(f"VERIFICACIÓN DE CONTROLES FALLIDA: {len(errors)}")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "VERIFICACIÓN DE CONTROLES CORRECTA: cobertura=252/252; censos, "
        f"artefactos, manifiesto y SHA reproducibles; revisiones_manuales={len(reviews)}."
    )
    return 0


def write_manual_template(root: Path, output: Path) -> int:
    corpus = Corpus(root)
    _, rows = load_control_rows(root)
    results = {
        row["id_requisito"]: evaluate(corpus, row)
        for row in rows if row["tipo"] == "CONTROL_ESTRUCTURAL"
    }
    literals = load_requirement_literals(root)
    pending = sorted(
        (result for result in results.values() if not result.automated),
        key=lambda result: natural(result.requirement_id),
    )
    template = [
        manual_template_row(corpus, result, literals[result.requirement_id])
        for result in pending
    ]
    destination = output if output.is_absolute() else root / output
    if destination.exists():
        print(f"PLANTILLA MANUAL NO ESCRITA: el destino ya existe: {destination}")
        return 1
    payload = csv_bytes(MANUAL_LEDGER_HEADER, template)
    atomic_write(destination, payload)
    print(
        f"PLANTILLA MANUAL ESCRITA: filas={len(template)}; "
        f"sha256={sha256_bytes(payload)}; destino={destination}"
    )
    return 0


def verify_manual_ledger(root: Path) -> int:
    corpus = Corpus(root)
    _, rows = load_control_rows(root)
    results = {
        row["id_requisito"]: evaluate(corpus, row)
        for row in rows if row["tipo"] == "CONTROL_ESTRUCTURAL"
    }
    reviews, errors = load_manual_reviews(
        corpus, results, require_ledger=True,
    )
    if errors:
        print(f"VERIFICACIÓN DEL LEDGER MANUAL FALLIDA: {len(errors)}")
        for error in errors:
            print(f"- {error}")
        return 1
    conforming = sum(review.conforms for review in reviews.values())
    print(
        f"LEDGER MANUAL CORRECTO: cobertura={len(reviews)}/{len(reviews)}; "
        f"conformes={conforming}; no_conformes={len(reviews)-conforming}; "
        "literales, rutas, alcance, evidencia, independencia y fechas verificados."
    )
    return 0


def print_classification(root: Path) -> int:
    corpus = Corpus(root)
    _, rows = load_control_rows(root)
    results = [
        evaluate(corpus, row) for row in rows
        if row["tipo"] == "CONTROL_ESTRUCTURAL"
    ]
    automated = sorted(
        result.requirement_id for result in results if result.automated
    )
    pending = sorted(
        result.requirement_id for result in results if not result.automated
    )
    automated_failures = {
        result.requirement_id: result.errors
        for result in results if result.automated and result.errors
    }
    families: defaultdict[str, list[str]] = defaultdict(list)
    for result in results:
        for family in sorted(result.automation_families):
            families[family].append(result.requirement_id)
    reviews, ledger_errors = load_manual_reviews(
        corpus, {result.requirement_id: result for result in results},
    )
    print(json.dumps({
        "total": len(results),
        "automatizados": automated,
        "pendientes": pending,
        "automatizados_con_fallos": automated_failures,
        "familias": dict(sorted(families.items())),
        "revision_manual": {
            "adjudicados": len(reviews),
            "conformes": sum(review.conforms for review in reviews.values()),
            "no_conformes": sum(
                not review.conforms for review in reviews.values()
            ),
            "errores_ledger": ledger_errors,
        },
        "recuentos": {
            "automatizados": len(automated),
            "pendientes": len(pending),
            "automatizados_con_fallos": len(automated_failures),
        },
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if automated_failures or ledger_errors else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--requirement")
    parser.add_argument("--materialize", action="store_true")
    parser.add_argument("--verify-artifacts", action="store_true")
    parser.add_argument("--verify-manual-ledger", action="store_true")
    parser.add_argument("--write-manual-template", type=Path)
    parser.add_argument("--classification", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if args.materialize:
        return materialize(root)
    if args.verify_artifacts:
        return verify_artifacts(root)
    if args.verify_manual_ledger:
        return verify_manual_ledger(root)
    if args.write_manual_template:
        return write_manual_template(root, args.write_manual_template)
    if args.classification:
        return print_classification(root)
    if not args.requirement:
        raise SystemExit(
            "use --requirement R-XXXX, --materialize, --verify-artifacts "
            "--verify-manual-ledger, --write-manual-template RUTA o "
            "--classification"
        )
    corpus = Corpus(root)
    _, rows = load_control_rows(root)
    by_id = {row["id_requisito"]: row for row in rows if row["tipo"] == "CONTROL_ESTRUCTURAL"}
    if args.requirement not in by_id:
        raise SystemExit(f"control inexistente: {args.requirement}")
    result = evaluate(corpus, by_id[args.requirement])
    print(json.dumps({
        **artifact_row(corpus, result),
        "fallos": result.errors,
        "pruebas": result.checks,
        "clasificacion": "AUTOMATIZADO" if result.automated else "PENDIENTE",
        "familias_automatizacion": sorted(result.automation_families),
    }, ensure_ascii=False, sort_keys=True))
    return 1 if result.errors else 0


if __name__ == "__main__":
    sys.exit(main())
