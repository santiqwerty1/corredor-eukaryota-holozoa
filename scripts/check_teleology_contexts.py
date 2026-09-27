#!/usr/bin/env python3
"""Cotejo exacto de adjudicaciones independientes, no clasificador semántico.

Ninguna palabra, ruta o porcentaje exonera otra ocurrencia. Los dictámenes
son evidencia nominal externa al consumidor y caducan si cambia su contexto.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path


REVIEW_PATH = Path("docs/auditorias/censo_contextos_teleologia_v2_contexto_2026-09-27.json")
INDEPENDENCE = "REVISION_INDEPENDIENTE_DE_CONTEXTOS_SIN_AUTORIA_DEL_TEXTO"
PATTERN = re.compile(
    r"\b(superior|inferior|primitiv[oa]s?|avanzad[oa]s?|más evolucionad[oa]s?|"
    r"intento fallido|paso obligatorio|fósil viviente|eslabón perdido|"
    r"eucariota primitivo|organismo simple|versi[oó]n antigua|"
    r"versi[oó]n detenida)\b|apareci[oó] para|"
    r"todavía no hab[ií]a desarrollado", re.IGNORECASE,
)
POSITIVE = {
    "USO_CUANTITATIVO", "CITA_ATRIBUCION_HISTORICA",
    "CRITICA_TERMINOLOGICA", "USO_TECNICO_NO_TELEOLOGICO",
}
NEGATIVE = {"TELEOLOGICO", "NO_VERIFICABLE", "NO_VERIFICABLE_POR_INDEPENDENCIA"}
TOP_FIELDS = {
    "version", "alcance", "revisor", "declaracion_independencia",
    "fecha_revision_utc", "algoritmo_huella", "candidatos", "huellas_rutas",
    "fecha_snapshot_utc",
}
ENTRY_FIELDS = {
    "ruta", "linea", "localizador_logico", "texto", "sha256_texto", "revisor",
    "declaracion_independencia", "fecha_revision_utc", "conflicto_autoria",
    "ocurrencias",
}
OCCURRENCE_FIELDS = {
    "inicio", "fin", "literal", "celda_o_clausula", "dictamen", "motivo",
}


class ContextReviewError(ValueError):
    pass


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContextReviewError(message)


def exact_fields(value: object, fields: set[str], label: str) -> None:
    require(isinstance(value, dict) and set(value) == fields,
            f"{label}: esquema cerrado inválido")


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and value.strip().casefold() not in {
        "n/a", "na", "pendiente", "desconocido", "sin revisar", "tbd", "-", "—",
    }


def utc(value: object) -> datetime:
    require(isinstance(value, str) and bool(re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z", value)),
        "fecha de revisión sin UTC exacto")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContextReviewError("fecha de revisión imposible") from exc


def safe_file(root: Path, path: Path) -> Path:
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise ContextReviewError(f"ruta fuera del corpus: {path}") from exc
    require(bool(relative.parts) and not any(p in {"..", "."} for p in relative.parts),
            f"ruta no canónica: {path}")
    cursor = root
    for component in relative.parts:
        cursor /= component
        require(not cursor.is_symlink(), f"enlace no permitido: {path}")
    require(path.is_file(), f"archivo ausente: {relative.as_posix()}")
    return path


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, f"clave JSON duplicada: {key}")
        result[key] = value
    return result


def collect(root: Path, paths: list[Path]) -> tuple[dict, dict]:
    """Censo léxico íntegro y bytes del contexto; no emite aprobaciones."""
    candidates, snapshots = {}, {}
    for path in sorted(set(paths)):
        payload = safe_file(root, path).read_bytes()
        relative = path.relative_to(root).as_posix()
        snapshots[relative] = payload
        for number, line in enumerate(payload.decode("utf-8").splitlines(), 1):
            occurrences = list(PATTERN.finditer(line))
            if occurrences:
                candidates[(relative, number)] = (line, occurrences)
    return candidates, snapshots


def validate_review(document: object, candidates: dict, snapshots: dict) -> None:
    exact_fields(document, TOP_FIELDS, "revisión")
    require(type(document["version"]) is int and document["version"] == 2,
            "versión de esquema desconocida")
    require(document["algoritmo_huella"] == "SHA256(UTF8(texto+LF))",
            "algoritmo de huella desconocido")
    require(nonempty(document["alcance"]), "falta alcance de revisión")
    require(nonempty(document["revisor"]), "falta identidad de revisor")
    require(document["declaracion_independencia"] == INDEPENDENCE,
            "falta declaración independiente")
    timestamp = utc(document["fecha_revision_utc"])
    require(utc(document["fecha_snapshot_utc"]) >= timestamp,
            "snapshot de contexto anterior a la adjudicación")
    expected_hashes = {path: digest(payload) for path, payload in snapshots.items()}
    require(document["huellas_rutas"] == expected_hashes,
            "alcance o contexto vivo diferente del revisado")
    require(isinstance(document["candidatos"], list), "candidatos no es una lista")
    seen = set()
    for entry in document["candidatos"]:
        exact_fields(entry, ENTRY_FIELDS, "candidato")
        require(isinstance(entry["ruta"], str) and type(entry["linea"]) is int,
                "ruta/línea inválidas")
        key = (entry["ruta"], entry["linea"])
        require(key in candidates and key not in seen, f"candidato ajeno o duplicado: {key}")
        seen.add(key)
        text, occurrences = candidates[key]
        require(entry["texto"] == text and entry["sha256_texto"] == digest((text + "\n").encode()),
                f"texto/huella de candidato obsoletos: {key}")
        require(nonempty(entry["localizador_logico"]), f"sin localizador nominal: {key}")
        require(entry["revisor"] == document["revisor"] and
                entry["declaracion_independencia"] == INDEPENDENCE and
                entry["conflicto_autoria"] == "NO", f"independencia no acreditada: {key}")
        require(utc(entry["fecha_revision_utc"]) <= timestamp,
                f"dictamen posterior a su expediente: {key}")
        reviewed = entry["ocurrencias"]
        require(isinstance(reviewed, list) and len(reviewed) == len(occurrences),
                f"censo de ocurrencias incompleto: {key}")
        for decision, occurrence in zip(reviewed, occurrences):
            exact_fields(decision, OCCURRENCE_FIELDS, "ocurrencia")
            require(type(decision["inicio"]) is int and type(decision["fin"]) is int and
                    (decision["inicio"], decision["fin"], decision["literal"]) ==
                    (occurrence.start(), occurrence.end(), occurrence.group()),
                    f"ocurrencia ajena, duplicada o desordenada: {key}")
            require(nonempty(decision["celda_o_clausula"]) and nonempty(decision["motivo"]),
                    f"dictamen sin fundamento nominal: {key}")
            verdict = decision["dictamen"]
            require(isinstance(verdict, str) and verdict in POSITIVE | NEGATIVE,
                    f"dictamen desconocido: {key}")
            require(verdict in POSITIVE, f"dictamen no conforme: {key}: {verdict}")
    require(seen == set(candidates), "faltan candidatos nominales por revisar")


def stat_signature(path: Path) -> tuple[int, ...]:
    stat = path.stat()
    return stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns


def check_context_reviews(
    root: Path, paths: list[Path], *, verified_hashes: dict[Path, str] | None = None,
) -> tuple[int, int, list[str]]:
    candidates, snapshots = {}, {}
    if verified_hashes is not None:
        verified_hashes.clear()
    try:
        signatures = {path: stat_signature(safe_file(root, path)) for path in set(paths)}
        candidates, snapshots = collect(root, paths)
        review_path = safe_file(root, root / REVIEW_PATH)
        signatures[review_path] = stat_signature(review_path)
        review_bytes = review_path.read_bytes()
        document = json.loads(review_bytes, object_pairs_hook=unique_object)
        validate_review(document, candidates, snapshots)
        # No admitir un resultado sobre archivos cambiados durante el cotejo.
        for relative, payload in snapshots.items():
            require(safe_file(root, root / relative).read_bytes() == payload,
                    f"contexto cambió durante la revisión: {relative}")
        require(safe_file(root, review_path).read_bytes() == review_bytes,
                "expediente cambió durante la revisión")
        # La lectura final de un archivo no puede invalidar silenciosamente
        # otro ya releído. Las firmas stat son guardas de carrera, nunca parte
        # de los derivados deterministas (no serializar inode/mtime).
        for path, signature in signatures.items():
            require(stat_signature(safe_file(root, path)) == signature,
                    f"insumo cambió durante el cotejo final: {path.relative_to(root)}")
        if verified_hashes is not None:
            verified_hashes.update({root / path: digest(payload) for path, payload in snapshots.items()})
            verified_hashes[review_path] = digest(review_bytes)
    except (ContextReviewError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        return len(candidates), sum(len(item[1]) for item in candidates.values()), [str(exc)]
    return len(candidates), sum(len(item[1]) for item in candidates.values()), []
