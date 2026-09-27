"""Deltas semánticos prospectivos; nunca convierten consultas BN en evidencia.

Una disposición enlaza el rechazo histórico, el hueco autoral, una corrección
explícita y una revisión ajena de esa propuesta exacta. Las C científicas de
soporte siguen necesitando el censo global y sus dos revisiones. Este módulo
comprueba ligaduras, no deduce conformidad a partir de palabras o hashes.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path, PurePosixPath

try:
    from .corpus_io import expand_source_refs, _supplementary_source_context
    from .sync_requirement_closures import expand_claim_refs
except ImportError:
    from corpus_io import expand_source_refs, _supplementary_source_context
    from sync_requirement_closures import expand_claim_refs


REGISTRY = "data/auditoria/disposiciones_residuales_semanticas_v1.json"
DECLARATION = "REVISION_INDEPENDIENTE_SIN_PARTICIPACION_EN_CORRECCION"
FIELDS = {
    "claim_id", "csv_path", "fila", "columna", "bn", "sha256_residual",
    "contenido_previo", "sha256_previo", "contenido_nuevo", "sha256_nuevo",
    "autor", "fecha_utc", "componentes", "limites_pendientes",
    "afirmaciones_soporte", "artefactos_soporte", "evidencia_autor",
    "revision_independiente", "identidad_fila",
}
REVIEW_FIELDS = {
    "version", "claim_id", "disposicion_sha256", "revisor", "fecha_utc",
    "dictamen", "independencia", "cobertura", "pasajes", "limitaciones",
}


def row_hash(value: object) -> str:
    return hashlib.sha256((json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ) + "\n").encode()).hexdigest()


def cell_hash(value: str) -> str:
    return hashlib.sha256((value + "\n").encode()).hexdigest()


def proposal_hash(record: dict) -> str:
    return row_hash({key: value for key, value in record.items()
                     if key != "revision_independiente"})


def _fail(message: str) -> None:
    raise RuntimeError("Disposición semántica residual: " + message)


def _keys(value: object, expected: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != expected:
        _fail(f"contrato cerrado inválido en {label}")


def _text(value: object, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        _fail(f"texto vacío/inválido en {label}")


def _identity(value: object, label: str) -> str:
    _text(value, label)
    normalized = " ".join(unicodedata.normalize("NFKC", value).casefold().split())
    placeholder = normalized.replace("_", " ").replace("-", " ")
    if (not any(char.isalnum() for char in normalized)
            or placeholder in {"n/a", "na", "none", "null", "autor", "revisor"}
            or re.search(r"\b(?:no asignado|pendiente|pending|unknown|tbd|sin revisor|sin autor)\b", placeholder)):
        _fail(f"identidad no asignada en {label}")
    return normalized


def _sha(value: object, label: str) -> None:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        _fail(f"SHA-256 inválido en {label}")


def _utc(value: object) -> datetime:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", value):
        _fail("UTC inválida")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as error:
        raise RuntimeError("Disposición semántica residual: UTC imposible") from error


def _path(root: Path, relative: str) -> Path:
    _text(relative, "ruta")
    pure = PurePosixPath(relative)
    if (pure.is_absolute() or ".." in pure.parts or "\\" in relative
            or pure.as_posix() != relative):
        _fail(f"ruta no canónica: {relative!r}")
    path = root / relative
    if any(part.is_symlink() for part in (path, *path.parents) if part != root.parent):
        _fail(f"symlink no permitido: {relative}")
    if not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
        _fail(f"archivo ausente/fuera de raíz: {relative}")
    return path


def _artifact(root: Path, reference: dict) -> bytes:
    _keys(reference, {"ruta", "sha256"}, "artefacto")
    _sha(reference["sha256"], "artefacto")
    raw = _path(root, reference["ruta"]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != reference["sha256"]:
        _fail(f"artefacto obsoleto: {reference['ruta']}")
    return raw


def _object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            _fail(f"clave JSON duplicada: {key}")
        result[key] = value
    return result


def _json(raw: bytes) -> object:
    try:
        return json.loads(raw, object_pairs_hook=_object)
    except (ValueError, UnicodeError) as error:
        raise RuntimeError("Disposición semántica residual: JSON inválido") from error


def _claim_catalog(root: Path) -> dict[str, dict[str, str]]:
    catalog = {}
    for path in sorted((root / "data/afirmaciones").glob("*.csv")):
        path = _path(root, path.relative_to(root).as_posix())
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                key = row["#"]
                if key in catalog:
                    _fail(f"C duplicada: {key}")
                catalog[key] = row
    return catalog


def _row_identity(root: Path, record: dict) -> dict[str, str]:
    path = _path(root, record["csv_path"])
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
            _fail("cabecera tabular vacía/duplicada")
        rows = list(reader)
        first = reader.fieldnames[0]
    try:
        number = int(record["fila"])
    except (TypeError, ValueError) as error:
        raise RuntimeError("Disposición semántica residual: número de fila inválido") from error
    if not 2 <= number <= len(rows) + 1 or record["columna"] == first:
        _fail("fila inexistente/corrección de identidad no admitida")
    row = rows[number - 2]
    names = [first] + [name for name in ("taxón o sistema", "magnitud")
                      if name in row and name not in {first, record["columna"]}]
    return {name: row[name].strip() for name in names}


def _sources(value: str) -> set[str]:
    for match in re.finditer(r"\bS\d+\b", value):
        if _supplementary_source_context(value, match.start()):
            continue
        key = match.group()
        if not re.fullmatch(r"S\d{2,3}", key) or key != f"S{int(key[1:]):02d}":
            _fail(f"clave S no canónica: {key}")
    try:
        return set(expand_source_refs(value))
    except ValueError as error:
        raise RuntimeError("Disposición semántica residual: rango S inválido") from error


def load(
    root: Path, residuals: list[dict[str, str]],
    targets: list[dict[str, str]], corrections: list[dict[str, str]],
    *, start_bn: int, positive_claims: set[str],
) -> dict[str, dict]:
    """Devuelve sólo deltas completos y revisados, o falla sin escribir nada."""
    registry_path = _path(root, REGISTRY)
    registry_raw = registry_path.read_bytes()
    registry = _json(registry_raw)
    _keys(registry, {"version", "disposiciones"}, "registro")
    if type(registry["version"]) is not int or registry["version"] != 1:
        _fail("versión desconocida")
    if not isinstance(registry["disposiciones"], list):
        _fail("disposiciones debe ser lista")
    by_residual = {row["claim_id"]: (index, row) for index, row in enumerate(residuals)}
    by_target = {row["claim_id"]: row for row in targets}
    by_correction = {row["claim_id"]: row for row in corrections}
    if (len(by_residual) != len(residuals) or len(by_target) != len(targets)
            or len(by_correction) != len(corrections)):
        _fail("identidad C duplicada en entradas")
    required = set(by_residual) & set(by_correction)
    records = {}
    catalog = _claim_catalog(root) if registry["disposiciones"] else {}
    read_references: list[dict] = []
    for record in registry["disposiciones"]:
        _keys(record, FIELDS, "disposición")
        key = record["claim_id"]
        _text(key, "claim_id")
        if key in records or key not in required or key in positive_claims:
            _fail(f"disposición duplicada/huérfana/positivo literal: {key}")
        index, residual = by_residual[key]
        target, correction = by_target.get(key), by_correction[key]
        if target is None:
            _fail(f"sin objetivo histórico: {key}")
        identity = ("csv_path", "fila", "columna", "claim_id")
        if any(record[field] != residual[field] or record[field] != target[field]
               or record[field] != correction[field] for field in identity):
            _fail(f"identidad nominal distinta: {key}")
        if record["bn"] != f"BN-{start_bn + index:03d}":
            _fail(f"BN distinta: {key}")
        if record["sha256_residual"] != row_hash(residual):
            _fail(f"rechazo original distinto: {key}")
        if residual["contenido_sha256"] != cell_hash(residual["contenido_anterior"]):
            _fail(f"hash del rechazo inválido: {key}")
        for new, content_key, hash_key in (
            (False, "contenido_previo", "sha256_previo"),
            (True, "contenido_nuevo", "sha256_nuevo"),
        ):
            content = record[content_key]
            _text(content, content_key)
            if content != " ".join(content.split()) or cell_hash(content) != record[hash_key]:
                _fail(f"contenido/huella no canónicos: {key}")
            prefix = "corregido" if new else "previo"
            if (content != correction[f"contenido_{prefix}"]
                    or record[hash_key] != correction[f"contenido_{prefix}_sha256"]):
                _fail(f"corrección no enlazada: {key}")
        if (record["contenido_previo"] != target["contenido"]
                or record["sha256_previo"] != target["contenido_sha256"]
                or record["contenido_nuevo"] == record["contenido_previo"]):
            _fail(f"objetivo previo distinto/delta vacío: {key}")
        author_identity = _identity(record["autor"], "autor")
        if record["autor"] != correction["autor_correccion"]:
            _fail(f"autor distinto: {key}")
        author_time = _utc(record["fecha_utc"])
        if record["identidad_fila"] != _row_identity(root, record):
            _fail(f"identidad taxonómica/de fila distinta: {key}")
        _text(record["limites_pendientes"], "límites")
        components = record["componentes"]
        if (not isinstance(components, list) or not components
                or any(not isinstance(item, str) or not item.strip() for item in components)
                or len(set(components)) != len(components)):
            _fail(f"componentes vacíos/duplicados: {key}")
        support = record["afirmaciones_soporte"]
        artifacts = record["artefactos_soporte"]
        if not isinstance(support, dict) or not support or not isinstance(artifacts, dict) or not artifacts:
            _fail(f"sin C/artefactos de soporte: {key}")
        try:
            cited = set(expand_claim_refs(record["contenido_nuevo"]))
        except ValueError as error:
            raise RuntimeError("Disposición semántica residual: rango C inválido") from error
        if cited != set(support) or key in cited:
            _fail(f"soportes no nominales/circularidad: {key}")
        declared_sources: set[str] = set()
        for claim, digest in support.items():
            _sha(digest, "C soporte")
            if claim not in catalog or row_hash(catalog[claim]) != digest:
                _fail(f"C soporte ausente/obsoleta: {claim}")
            # Este contrato acotado exige apoyos expresos directos; no omite
            # descendientes de una síntesis al fijar únicamente su fila.
            if catalog[claim].get("Atribución") != "expresa":
                _fail(f"C soporte no es expresa directa: {claim}")
            source_field = catalog[claim].get("Fuente", "")
            sources = _sources(source_field)
            if not sources or re.search(r"\bBN-\d+\b", source_field):
                _fail(f"C soporte sin primaria nominal: {claim}")
            declared_sources.update(sources)
        artifact_sources: set[str] = set()
        for relative, digest in artifacts.items():
            if (not relative.startswith("fuentes/")
                    or Path(relative).suffix.lower() not in {".pdf", ".xml", ".html", ".txt"}):
                _fail(f"artefacto no probatorio: {relative}")
            nominal = re.match(r"(S\d{1,4})\b", Path(relative).name)
            if nominal is None:
                _fail(f"artefacto sin clave fuente: {relative}")
            _sources(nominal.group(1))
            artifact_sources.add(nominal.group(1))
            reference = {"ruta": relative, "sha256": digest}
            _artifact(root, reference)
            read_references.append(reference)
        if artifact_sources != declared_sources:
            _fail(f"fuentes/artefactos no coinciden nominalmente: {key}")
        for field in ("evidencia_autor", "revision_independiente"):
            raw = _artifact(root, record[field])
            read_references.append(record[field])
            if field == "revision_independiente":
                review = _json(raw)
        if record["evidencia_autor"]["ruta"] not in correction["evidencia_correccion"]:
            _fail(f"evidencia autoral no enlazada: {key}")
        _keys(review, REVIEW_FIELDS, "revisión")
        if (type(review["version"]) is not int or review["version"] != 1
                or review["claim_id"] != key
                or review["disposicion_sha256"] != proposal_hash(record)
                or review["dictamen"] != "CONFORME"
                or review["independencia"] != DECLARATION):
            _fail(f"revisión no conforme/no ligada: {key}")
        reviewer_identity = _identity(review["revisor"], "revisor")
        if reviewer_identity == author_identity or _utc(review["fecha_utc"]) < author_time:
            _fail(f"autorrevisión/cronología inválida: {key}")
        _text(review["limitaciones"], "limitaciones de revisión")
        coverage, passages = review["cobertura"], review["pasajes"]
        if not isinstance(coverage, dict) or set(coverage) != set(components):
            _fail(f"cobertura nominal incompleta: {key}")
        if not isinstance(passages, list) or not passages:
            _fail(f"sin pasajes: {key}")
        for passage in passages:
            _keys(passage, {"artefacto", "sha256_artefacto", "localizador",
                           "fragmento_control", "sha256_pasaje"}, "pasaje")
            if (passage["artefacto"] not in artifacts
                    or passage["sha256_artefacto"] != artifacts[passage["artefacto"]]):
                _fail(f"pasaje fuera del inventario: {key}")
            _text(passage["localizador"], "localizador")
            _text(passage["fragmento_control"], "fragmento")
            if len(passage["fragmento_control"].split()) > 25:
                _fail(f"fragmento excede 25 palabras: {key}")
            _sha(passage["sha256_pasaje"], "pasaje")
        used = set()
        for refs in coverage.values():
            if (not isinstance(refs, list) or not refs
                    or any(type(item) is not int or not 0 <= item < len(passages) for item in refs)
                    or len(set(refs)) != len(refs)):
                _fail(f"referencias de cobertura inválidas: {key}")
            used.update(refs)
        if used != set(range(len(passages))):
            _fail(f"pasajes no adjudicados: {key}")
        if {item["artefacto"] for item in passages} != set(artifacts):
            _fail(f"artefactos sin pasaje: {key}")
        records[key] = record
    if set(records) != required:
        _fail("correcciones residuales sin disposición revisada: " + repr(sorted(required - set(records))))
    # Relectura final: un artefacto o C que cambia durante la validación no
    # puede seguir ligado a un dictamen anterior. No se consulta el reloj.
    if _path(root, REGISTRY).read_bytes() != registry_raw:
        _fail("registro modificado durante la validación")
    for reference in read_references:
        _artifact(root, reference)
    if records:
        current_catalog = _claim_catalog(root)
        for record in records.values():
            if record["identidad_fila"] != _row_identity(root, record):
                _fail("identidad de fila modificada durante la validación")
            for claim, digest in record["afirmaciones_soporte"].items():
                if claim not in current_catalog or row_hash(current_catalog[claim]) != digest:
                    _fail(f"C soporte modificada durante la validación: {claim}")
    return records
