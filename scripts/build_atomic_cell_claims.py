#!/usr/bin/env python3
"""Materializa afirmaciones atómicas para celdas rechazadas en segunda revisión.

El archivo de objetivos es evidencia versionada del dictamen independiente: cada
fila fija ruta, fila, columna, contenido y huella. El constructor no descubre ni
aprueba celdas por semejanza. Solo puede escribir una C nueva para una fila ya
rechazada, y aborta si el contenido vivo, el manifiesto o la secuencia de IDs no
coinciden exactamente.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET_FILES = (
    ROOT / "data/auditoria/celdas_no_conformes_trazabilidad_v1.csv",
    ROOT / "data/auditoria/celdas_no_conformes_trazabilidad_v2.csv",
)
CORRECTIONS = ROOT / "data/auditoria/correcciones_celdas_semanticas_v1.csv"
CLAIMS = ROOT / "data/afirmaciones/15.csv"
MANIFEST = ROOT / "data/auditoria/mapeo_celdas_afirmaciones.csv"
PREDICATE_DEFINITION = (
    ROOT / "docs/secciones/001-00-0-convenciones-probatorias-y-taxonomicas.md"
)

TARGET_HEADER = [
    "csv_path", "fila", "columna", "contenido_sha256", "contenido",
    "afirmaciones_previas", "claim_id", "revisor_origen", "evidencia_dictamen",
]
CORRECTION_HEADER = [
    "csv_path", "fila", "columna", "claim_id",
    "contenido_previo_sha256", "contenido_previo",
    "contenido_corregido_sha256", "contenido_corregido",
    "autor_correccion", "evidencia_correccion",
]
CLAIM_HEADER = [
    "#", "Afirmación", "Sujeto", "Predicado", "Objeto", "Atribución",
    "Fuente", "Aceptación", "Fuerza", "Motivo", "Resolución", "Vigencia",
]
MANIFEST_HEADER = [
    "csv_path", "fila", "columna", "contenido_sha256", "contenido",
    "afirmaciones", "base_semantica", "estado_revision", "nota_adjudicacion",
]
CLAIM = re.compile(r"\bC-\d{3,5}\b")
CLAIM_RANGE = re.compile(r"\bC-(\d{3,5})\s*(?:-|–)\s*C-(\d{3,5})\b")
SOURCE = re.compile(r"\bS\d{1,4}\b")
GAP = re.compile(r"\bBN-\d{3}\b")
GENERATED_MARKER = "Afirmación atómica de celda; cierre de trazabilidad v1:"


def _validate_predicate_definition(text: str) -> None:
    """Exige la declaración prospectiva completa del predicado introducido."""
    required = (
        "`tiene_valor_literal_de_campo*`",
        "relaciona un estudio, matriz, taxón o sistema",
        "nombre y el contenido literales de una sola celda tabular",
        "Ejemplo: C-1996",
    )
    missing = [fragment for fragment in required if fragment not in text]
    if missing:
        raise RuntimeError(
            "Definición prospectiva incompleta de tiene_valor_literal_de_campo*: "
            + repr(missing)
        )


def _read(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise RuntimeError(f"CSV sin cabecera: {path}")
        return reader.fieldnames, list(reader)


def _csv_bytes(header: list[str], rows: list[dict[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        buffer, fieldnames=header, quoting=csv.QUOTE_ALL, lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def _claim_refs(text: str) -> list[str]:
    refs: list[str] = []
    occupied: list[tuple[int, int]] = []
    for match in CLAIM_RANGE.finditer(text):
        start, end = map(int, match.groups())
        if start <= end:
            refs.extend(f"C-{number:03d}" if number < 1000 else f"C-{number}"
                        for number in range(start, end + 1))
        occupied.append(match.span())
    for match in CLAIM.finditer(text):
        if not any(start <= match.start() < end for start, end in occupied):
            refs.append(match.group())
    return list(dict.fromkeys(refs))


def _digest(value: str) -> str:
    return hashlib.sha256((value + "\n").encode("utf-8")).hexdigest()


def _live_tables() -> dict[tuple[str, int, str], tuple[str, dict[str, str]]]:
    result: dict[tuple[str, int, str], tuple[str, dict[str, str]]] = {}
    paths = set()
    targets = [row for path in TARGET_FILES for row in _read(path)[1]]
    for target in targets:
        paths.add(target["csv_path"])
    for relative in sorted(paths):
        with (ROOT / relative).open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise RuntimeError(f"Tabla sin cabecera: {relative}")
            for row_number, row in enumerate(reader, 2):
                for column, value in row.items():
                    normalized = re.sub(r"\s+", " ", value).strip()
                    result[(relative, row_number, column)] = (normalized, row)
    return result


def _claim_catalog() -> tuple[dict[str, dict[str, str]], dict[str, Path]]:
    rows: dict[str, dict[str, str]] = {}
    paths: dict[str, Path] = {}
    for path in sorted((ROOT / "data/afirmaciones").glob("*.csv")):
        header, found = _read(path)
        if header != CLAIM_HEADER:
            raise RuntimeError(f"Cabecera de C inesperada: {path}: {header!r}")
        for row in found:
            claim_id = row["#"]
            if claim_id in rows:
                raise RuntimeError(f"C duplicada: {claim_id}")
            rows[claim_id] = row
            paths[claim_id] = path
    return rows, paths


def _apply_corrections(
    targets: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Aplica un delta autoral sin reescribir el dictamen independiente.

    Los archivos TARGET_FILES conservan literalmente la celda que rechazó el
    revisor. Cada corrección debe enlazar esa huella previa con una única huella
    nueva y con la misma C atómica; así el historial no se sustituye ni se
    presenta una edición de autor como nueva decisión del revisor.
    """
    header, rows = _read(CORRECTIONS)
    if header != CORRECTION_HEADER:
        raise RuntimeError(f"Cabecera inesperada en {CORRECTIONS}: {header!r}")
    indexed: dict[tuple[str, int, str, str], dict[str, str]] = {}
    for row in rows:
        key = (
            row["csv_path"], int(row["fila"]), row["columna"], row["claim_id"],
        )
        if key in indexed:
            raise RuntimeError(f"Corrección de celda duplicada: {key!r}")
        if not row["autor_correccion"].strip() or not row["evidencia_correccion"].strip():
            raise RuntimeError(f"Corrección sin autor/evidencia: {key!r}")
        corrected = re.sub(r"\s+", " ", row["contenido_corregido"]).strip()
        if corrected != row["contenido_corregido"]:
            raise RuntimeError(f"Corrección no normalizada: {key!r}")
        if _digest(corrected) != row["contenido_corregido_sha256"]:
            raise RuntimeError(f"Huella corregida inválida: {key!r}")
        indexed[key] = row

    effective: list[dict[str, str]] = []
    used: set[tuple[str, int, str, str]] = set()
    for target in targets:
        key = (
            target["csv_path"], int(target["fila"]), target["columna"],
            target["claim_id"],
        )
        correction = indexed.get(key)
        if correction is None:
            effective.append(target)
            continue
        if (
            correction["contenido_previo"] != target["contenido"]
            or correction["contenido_previo_sha256"] != target["contenido_sha256"]
        ):
            raise RuntimeError(
                f"La corrección no enlaza el dictamen original exacto: {key!r}"
            )
        amended = dict(target)
        amended["_contenido_previo"] = target["contenido"]
        amended["_contenido_previo_sha256"] = target["contenido_sha256"]
        amended["contenido"] = correction["contenido_corregido"]
        amended["contenido_sha256"] = correction["contenido_corregido_sha256"]
        effective.append(amended)
        used.add(key)
    orphaned = sorted(set(indexed) - used)
    if orphaned:
        raise RuntimeError(f"Correcciones sin objetivo original: {orphaned[:5]!r}")
    return effective


def _source_fragments(text: str) -> list[str]:
    """Conserva fragmentos S/BN con sus localizadores escritos, sin C auxiliares."""
    pieces = []
    for piece in re.split(r"\s*;\s*", text):
        if SOURCE.search(piece) or GAP.search(piece):
            pieces.append(piece.strip())
    return pieces


def _identity(row: dict[str, str], column: str) -> str:
    first_column = next(iter(row))
    parts = [f"{first_column} «{row[first_column].strip()}»"]
    for name in ("taxón o sistema", "magnitud"):
        if name in row and name != column and name != first_column:
            parts.append(f"{name} «{row[name].strip()}»")
    return ", ".join(parts)


def _generated_claim(
    target: dict[str, str], row: dict[str, str],
    catalog: dict[str, dict[str, str]],
) -> dict[str, str]:
    path = target["csv_path"]
    row_number = int(target["fila"])
    column = target["columna"]
    value = target["contenido"]
    metadata = " ; ".join(
        field for name, field in row.items()
        if name.casefold() in {
            "fila", "filas", "filas y fuentes", "filas y fuente local", "#",
            "evidencia o hueco",
        }
    )
    # La columna bibliográfica puede listar toda la fila. No se permite que una
    # C de una celda herede ese roll-up: conserva exclusivamente la C que el
    # dictamen cotejó para esta celda y cualquier C escrita en el propio valor.
    dependency_text = value + "; " + target["afirmaciones_previas"]
    if int(target["claim_id"].split("-")[1]) >= 2572:
        # El segundo dictamen señaló sobre todo celdas compuestas a las que el
        # manifiesto había asignado una sola C. En ese lote se declaran todas
        # las C bibliográficas de la fila como dependencias candidatas; la C
        # resultante es una síntesis explícita que la rerevisión debe cotejar,
        # no una herencia silenciosa del contexto.
        dependency_text += "; " + metadata
    dependencies = _claim_refs(dependency_text)
    dependencies = [item for item in dependencies if item != target["claim_id"]]

    direct_source: list[str] = []
    if target["claim_id"] == "C-2472":
        direct_source = [
            "S435 §Introduction; párrafo que comienza ‘Although close to 1000 genomes’"
        ]
        attribution = "expresa"
    elif target["claim_id"] == "C-2489":
        direct_source = [
            "S435 §Introduction; párrafo que comienza ‘Nonetheless, M. brevicollis’"
        ]
        attribution = "expresa"
    elif "table-06-" in path and 5 <= row_number <= 24:
        direct_source = [
            "S49 Results and Discussion §Discriminatory criteria to evaluate "
            "which alphaproteobacteria may be close to protomitochondria; "
            "tabla 2 [requiere inspección humana]"
        ]
        attribution = "expresa"
    elif "table-06-" in path and 25 <= row_number <= 38:
        direct_source = [
            "S49 Results and Discussion §Other metabolic systems and traits "
            "analyzed in this work and their characteristics; tabla 3 "
            "[requiere inspección humana]"
        ]
        attribution = "expresa"
    else:
        for dependency in dependencies:
            if dependency not in catalog:
                raise RuntimeError(
                    f"{target['claim_id']}: dependencia inexistente {dependency}"
                )
        attribution = (
            f"sintesis({', '.join(dependencies)})" if dependencies else "glosa"
        )
    gaps = list(dict.fromkeys(GAP.findall(value) + GAP.findall(metadata)))
    if direct_source:
        direct_source.extend(gaps)
        sources = "; ".join(dict.fromkeys(direct_source))
    elif dependencies:
        sources = "n/a; dependencias canónicas " + "; ".join(dependencies)
        if gaps:
            sources += "; " + "; ".join(gaps) + " términos exactos y resultado"
    else:
        sources = "; ".join(
            f"{gap} términos exactos y resultado" for gap in gaps
        )
    if not sources:
        raise RuntimeError(
            f"{target['claim_id']}: no se pudo derivar fuente/localizador"
        )

    identity = _identity(row, column)
    insufficient = re.search(
        r"\b(?:no consta|no localiz|no censad|no resuelt|sin cifra|sin edad)\b",
        value, re.IGNORECASE,
    ) is not None
    strength_order = {"desconocida": 0, "baja": 1, "media": 2, "alta": 3}
    strength = "alta"
    if dependencies:
        strength = min(
            (catalog[item]["Fuerza"] for item in dependencies),
            key=lambda value: strength_order[value],
        )
    return {
        "#": target["claim_id"],
        "Afirmación": (
            f"Para {identity}, el campo «{column}» tiene el valor literal "
            f"«{value}»."
        ),
        "Sujeto": identity,
        "Predicado": "tiene_valor_literal_de_campo*",
        "Objeto": f"{column}: {value}",
        "Atribución": attribution,
        "Fuente": sources,
        "Aceptación": "no evaluado",
        "Fuerza": strength,
        "Motivo": (
            f"{GENERATED_MARKER} {path}:fila {row_number}:{column}. "
            "La proposición conserva una sola celda, su identidad de fila y su "
            "modalidad; no hereda valores de otra celda ni convierte un hueco en ausencia."
        ),
        "Resolución": "información insuficiente" if insufficient else "resuelta",
        "Vigencia": "vigente",
    }


def build() -> tuple[bytes, bytes, list[str]]:
    _validate_predicate_definition(PREDICATE_DEFINITION.read_text(encoding="utf-8"))
    targets: list[dict[str, str]] = []
    for path in TARGET_FILES:
        target_header, found = _read(path)
        if target_header != TARGET_HEADER:
            raise RuntimeError(f"Cabecera inesperada en {path}: {target_header!r}")
        targets.extend(found)
    if len(targets) != 816:
        raise RuntimeError(f"Se esperaban 816 celdas rechazadas; hay {len(targets)}")
    targets = _apply_corrections(targets)

    live = _live_tables()
    catalog, claim_paths = _claim_catalog()
    manifest_header, manifest_rows = _read(MANIFEST)
    if manifest_header != MANIFEST_HEADER:
        raise RuntimeError(f"Cabecera inesperada en {MANIFEST}: {manifest_header!r}")
    manifest_index = {
        (row["csv_path"], int(row["fila"]), row["columna"], row["contenido_sha256"]): row
        for row in manifest_rows
    }

    target_ids = [row["claim_id"] for row in targets]
    if len(target_ids) != len(set(target_ids)):
        raise RuntimeError("IDs duplicadas en objetivos atómicos")
    expected_ids = (
        [f"C-{number}" for number in range(1996, 2570)]
        + [f"C-{number}" for number in range(2572, 2814)]
    )
    if target_ids != expected_ids:
        raise RuntimeError(
            "La secuencia C atómica no es exactamente C-1996..C-2569 y C-2572..C-2813"
        )

    generated: list[dict[str, str]] = []
    target_keys: set[tuple[str, int, str, str]] = set()
    for target in targets:
        key3 = (target["csv_path"], int(target["fila"]), target["columna"])
        if key3 not in live:
            raise RuntimeError(f"Celda objetivo ausente: {key3!r}")
        value, table_row = live[key3]
        if value != target["contenido"] or _digest(value) != target["contenido_sha256"]:
            raise RuntimeError(f"Celda objetivo cambió desde la revisión: {key3!r}")
        key4 = key3 + (target["contenido_sha256"],)
        if key4 in target_keys:
            raise RuntimeError(f"Celda objetivo duplicada: {key4!r}")
        target_keys.add(key4)
        manifest_key = key4
        if manifest_key not in manifest_index and target.get("_contenido_previo_sha256"):
            manifest_key = key3 + (target["_contenido_previo_sha256"],)
        if manifest_key not in manifest_index:
            raise RuntimeError(f"Celda objetivo sin manifiesto exacto: {key4!r}")
        generated.append(_generated_claim(target, table_row, catalog))

    claim_header, claim_rows = _read(CLAIMS)
    if claim_header != CLAIM_HEADER:
        raise RuntimeError(f"Cabecera inesperada en {CLAIMS}: {claim_header!r}")
    preserved = [row for row in claim_rows if GENERATED_MARKER not in row["Motivo"]]
    collisions = sorted(set(target_ids) & {row["#"] for row in preserved})
    if collisions:
        raise RuntimeError(f"IDs atómicas colisionan con C ajenas: {collisions[:10]}")
    if any(path != CLAIMS for claim_id, path in claim_paths.items() if claim_id in target_ids):
        raise RuntimeError("Una C atómica existe fuera de data/afirmaciones/15.csv")

    by_identity = {
        (row["csv_path"], int(row["fila"]), row["columna"]): row
        for row in targets
    }
    new_manifest: list[dict[str, str]] = []
    for row in manifest_rows:
        identity = (row["csv_path"], int(row["fila"]), row["columna"])
        target = by_identity.get(identity)
        if target is not None:
            allowed_hashes = {
                target["contenido_sha256"],
                target.get("_contenido_previo_sha256", target["contenido_sha256"]),
            }
            if row["contenido_sha256"] not in allowed_hashes:
                raise RuntimeError(
                    f"Manifiesto no enlaza la versión previa ni corregida: {identity!r}"
                )
            row = dict(row)
            row["contenido_sha256"] = target["contenido_sha256"]
            row["contenido"] = target["contenido"]
            own_refs = _claim_refs(target["contenido"])
            row["afirmaciones"] = "; ".join(
                dict.fromkeys(own_refs + [target["claim_id"]])
            )
            row["base_semantica"] = (
                "cita_en_celda+manifiesto_explicito"
                if own_refs else "cotejo_literal_C_atomica_por_celda"
            )
            row["estado_revision"] = "REVISADA"
            row["nota_adjudicacion"] = (
                "Corrección de autor posterior al dictamen independiente: la C "
                "atómica reproduce solo esta celda; pendiente rerevisión ajena."
            )
        new_manifest.append(row)
    complete_claims = preserved + generated
    complete_claims.sort(key=lambda row: int(row["#"].split("-")[1]))
    return (
        _csv_bytes(CLAIM_HEADER, complete_claims),
        _csv_bytes(MANIFEST_HEADER, new_manifest),
        target_ids,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    claims_payload, manifest_payload, target_ids = build()
    if args.write:
        CLAIMS.write_bytes(claims_payload)
        MANIFEST.write_bytes(manifest_payload)
        print(f"Afirmaciones atómicas escritas: {len(target_ids)} ({target_ids[0]}..{target_ids[-1]}).")
        return 0
    errors = []
    if CLAIMS.read_bytes() != claims_payload:
        errors.append(f"C atómicas desactualizadas: {CLAIMS.relative_to(ROOT)}")
    if MANIFEST.read_bytes() != manifest_payload:
        errors.append(f"Mapeo atómico desactualizado: {MANIFEST.relative_to(ROOT)}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Afirmaciones atómicas exactas: {len(target_ids)} ({target_ids[0]}..{target_ids[-1]}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
