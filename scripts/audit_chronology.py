"""Fechas declaradas y ligadas a evidencia, sin reloj ni fechas de relleno.

Estos controles prueban formato, ligadura y orden declarado; no autenticidad
del registro, independencia del revisor ni apoyo científico de una fuente.
"""
from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REVIEW_START = "2026-08-13"
UNKNOWN_DATE = "FECHA_NO_DOCUMENTADA"
OBJECT_DATES = Path("data/auditoria/fechas_objetos_revision.csv")
SEARCH_DATES = Path("data/auditoria/fechas_ejecuciones_bn.csv")
MANUAL_LEDGER = Path("docs/auditorias/revision_manual_requisitos_2026-08-08.csv")
OBJECT_HEADER = [
    "estrato", "clave_objeto", "huella_objeto_sha256", "fecha_version",
    "evidencia_local", "huella_evidencia_sha256", "localizador_evidencia",
]
SEARCH_HEADER = [
    "clave_bn", "huella_fila_bn_sha256", "clase_fecha", "fecha_ejecucion",
    "evidencia_local", "huella_evidencia_sha256", "localizador_evidencia",
]
STRATA = {
    "CONTROL_MANUAL", "AFIRMACION", "FUENTE", "REQUISITO",
    "TRAZABILIDAD_PROSA", "TRAZABILIDAD_ARISTA", "TRAZABILIDAD_CELDA",
    "VERIFICACION_FUENTE",
}
DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
UTC = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
HEX = re.compile(r"[0-9a-f]{64}")


def parse_date(value: str) -> datetime | None:
    """No admite variantes ISO compactas, semanas ISO, offsets ni fechas imposibles."""
    if not isinstance(value, str):
        return None
    try:
        if DATE.fullmatch(value):
            return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        if UTC.fullmatch(value):
            return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        pass
    return None


def temporal_errors(value: str, not_before: tuple[str, ...] = ()) -> list[str]:
    parsed = parse_date(value)
    if parsed is None:
        return ["fecha no es un día ISO YYYY-MM-DD o instante UTC válido"]
    errors = []
    for bound in not_before:
        lower = parse_date(bound)
        if lower is None:
            errors.append(f"antecedente temporal inválido: {bound}")
        elif parsed < lower or (
            DATE.fullmatch(value) and UTC.fullmatch(bound) and parsed.date() == lower.date()
        ):
            errors.append(f"fecha anterior a {bound} o sin precisión para demostrar el orden")
    return errors


def review_date_errors(value: str, not_before: tuple[str, ...] = ()) -> list[str]:
    return temporal_errors(value, (REVIEW_START, *not_before))


@dataclass
class DateRegistry:
    rows: dict[tuple[str, ...], dict[str, str]]
    errors: list[str]

    def object_date(self, stratum: str, key: str, fingerprint: str) -> tuple[str, ...]:
        row = self.rows.get((stratum, key, fingerprint))
        return (row["fecha_version"],) if row else ()


def _load(root: Path, relative: Path, header: list[str], search: bool) -> DateRegistry:
    path = root / relative
    if not path.exists():
        return DateRegistry({}, [])
    errors: list[str] = []
    result: dict[tuple[str, ...], dict[str, str]] = {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != header:
            return DateRegistry({}, [f"{relative}: cabecera temporal incompatible"])
        for line, row in enumerate(reader, 2):
            label = f"{relative}:{line}"
            if None in row or any(not isinstance(row.get(name), str) or not row[name].strip() for name in header):
                errors.append(f"{label}: fila temporal incompleta o cardinalidad inválida")
                continue
            row_errors = []
            fingerprint = row["huella_fila_bn_sha256" if search else "huella_objeto_sha256"]
            value = row["fecha_ejecucion" if search else "fecha_version"]
            key = (row["clave_bn"], fingerprint) if search else (row["estrato"], row["clave_objeto"], fingerprint)
            if key in result:
                row_errors.append("metadato temporal duplicado para objeto y huella")
            if not HEX.fullmatch(fingerprint):
                row_errors.append("huella de objeto inválida")
            row_errors.extend(temporal_errors(value))
            if search:
                if not re.fullmatch(r"BN-[0-9]{3,}", row["clave_bn"]):
                    row_errors.append("clave BN inválida")
                if row["clase_fecha"] not in {"EJECUCION_ORIGINAL", "REINSPECCION"}:
                    row_errors.append("clase de fecha BN inválida")
            elif row["estrato"] not in STRATA:
                row_errors.append("estrato temporal inválido")
            evidence = Path(row["evidencia_local"])
            resolved = (root / evidence).resolve()
            forbidden = {
                (root / OBJECT_DATES).resolve(), (root / SEARCH_DATES).resolve(),
                (root / "docs/auditorias/registro_busquedas_2026-08-08.csv").resolve(),
                (root / "docs/auditorias/matriz_fuentes_2026-08-08.csv").resolve(),
            }
            if evidence.is_absolute() or not resolved.is_relative_to(root.resolve()) or not resolved.is_file() or resolved in forbidden:
                row_errors.append("evidencia local inexistente, externa o circular")
            elif not HEX.fullmatch(row["huella_evidencia_sha256"]) or hashlib.sha256(resolved.read_bytes()).hexdigest() != row["huella_evidencia_sha256"]:
                row_errors.append("huella de evidencia local inválida o desactualizada")
            if row["localizador_evidencia"].strip().casefold() in {"n/a", "pendiente", "sin localizar"}:
                row_errors.append("localizador temporal no declarado")
            errors.extend(f"{label}: {error}" for error in row_errors)
            if not row_errors:
                result[key] = row
    # Un registro estructuralmente inválido nunca presta fechas a otra fila.
    return DateRegistry({} if errors else result, errors)


def load_object_dates(root: Path) -> DateRegistry:
    return _load(root, OBJECT_DATES, OBJECT_HEADER, False)


def load_search_dates(root: Path) -> DateRegistry:
    return _load(root, SEARCH_DATES, SEARCH_HEADER, True)


def manual_review_dates(root: Path) -> tuple[dict[str, str], list[str]]:
    """Antecedentes de segunda revisión; no valida ni aprueba el ledger manual."""
    path = root / MANUAL_LEDGER
    if not path.exists():
        return {}, []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not {"id_requisito", "fecha_revision"}.issubset(reader.fieldnames or []):
            return {}, ["ledger manual sin identidad/fecha para contrastar cronología"]
        dates: dict[str, str] = {}
        errors = []
        for row in reader:
            key, value = row.get("id_requisito"), row.get("fecha_revision")
            if not key or value is None or key in dates:
                errors.append("ledger manual con identidad temporal duplicada o incompleta")
            else:
                dates[key] = value
        return dates, errors
