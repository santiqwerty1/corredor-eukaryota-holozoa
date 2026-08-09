#!/usr/bin/env python3
"""Comprueba la trazabilidad entre el maestro pre-migración y el corpus canónico.

Las tablas con ``source_start_line == 0`` nacieron después de la migración y no
pueden compararse fila a fila con el maestro v5. Las tablas heredadas sí deben
conservar su posición y cabecera de origen. El contenido canónico puede cambiar
después por correcciones bibliográficas, ampliaciones y renumeración global; su
integridad actual se comprueba en ``validate.py`` y ``audit_semantics.py``.
"""

from __future__ import annotations

import re
import sys
import hashlib
from pathlib import Path

from corpus_io import ROOT, load_index, read_csv


ARCHIVED_MASTER = "archive/maestro_provisional_v5_pre_migracion.md"
ARCHIVED_MASTER_SHA256 = (
    "24c5495d85641d03a24c084a51a9b0b5887edf60d6698f94f19775c09c28cfe3"
)


def split_markdown_row(line: str) -> list[str]:
    source = line.strip()
    if source.startswith("|"):
        source = source[1:]
    if source.endswith("|"):
        source = source[:-1]

    cells: list[str] = []
    buffer: list[str] = []
    escaped = False
    in_code = False
    for char in source:
        if escaped:
            buffer.append(char)
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == "`":
            in_code = not in_code
            buffer.append(char)
        elif char == "|" and not in_code:
            cells.append("".join(buffer).strip())
            buffer = []
        else:
            buffer.append(char)
    if escaped:
        buffer.append("\\")
    cells.append("".join(buffer).strip())
    return cells


def is_separator(line: str) -> bool:
    if not line.strip().startswith("|"):
        return False
    cells = split_markdown_row(line)
    return bool(cells) and all(
        re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells
    )


def clean_header(value: str) -> str:
    return value.replace("`", "").strip()


def canonicalize_claim_ids(value: str) -> str:
    pattern = re.compile(r"\bC-(\d{3,4})\b")

    def replace(match: re.Match[str]) -> str:
        number = int(match.group(1))
        return f"C-{number:03d}" if number < 1000 else f"C-{number}"

    return pattern.sub(replace, value)


def parse_tables(lines: list[str]) -> list[dict]:
    tables: list[dict] = []
    for index, line in enumerate(lines):
        if (
            line.strip().startswith("|")
            and index + 1 < len(lines)
            and is_separator(lines[index + 1])
        ):
            end = index + 2
            while end < len(lines) and lines[end].strip().startswith("|"):
                end += 1
            tables.append({
                "start": index + 1,
                "end": end,
                "header": [clean_header(v) for v in split_markdown_row(line)],
                "rows": [
                    [canonicalize_claim_ids(v) for v in split_markdown_row(lines[pos])]
                    for pos in range(index + 2, end)
                ],
            })
    return tables


def main() -> int:
    index = load_index()
    errors: list[str] = []
    if index.get("source_master") != ARCHIVED_MASTER:
        errors.append(
            "table_index.json no apunta al maestro archivado inmutable: "
            f"{index.get('source_master')!r}"
        )
    source = ROOT / ARCHIVED_MASTER
    if not source.exists():
        errors.append(f"Falta el maestro archivado: {ARCHIVED_MASTER}")
        source_bytes = b""
    else:
        source_bytes = source.read_bytes()
        actual_sha256 = hashlib.sha256(source_bytes).hexdigest()
        if actual_sha256 != ARCHIVED_MASTER_SHA256:
            errors.append(
                "El maestro archivado cambió: "
                f"{actual_sha256} != {ARCHIVED_MASTER_SHA256}"
            )
    if errors:
        print("AUDITORÍA DE MIGRACIÓN FALLIDA")
        for error in errors:
            print(f"- {error}")
        return 1
    parsed = parse_tables(source.read_text(encoding="utf-8").splitlines())
    legacy_entries = sorted(
        (entry for entry in index["tables"] if entry["source_start_line"] > 0),
        key=lambda entry: entry["source_start_line"],
    )
    native_entries = [
        entry for entry in index["tables"] if entry["source_start_line"] == 0
    ]

    errors = []
    if len(parsed) != len(legacy_entries):
        errors.append(
            f"Cantidad de tablas heredadas: {len(parsed)} != {len(legacy_entries)}"
        )

    for position, (original, entry) in enumerate(
        zip(parsed, legacy_entries), start=1
    ):
        header, rows = read_csv(ROOT / entry["csv_path"])
        if not header or not original["header"]:
            errors.append(f"Tabla {position} / {entry['id']}: cabecera vacía")
        if not rows:
            errors.append(f"Tabla {position} / {entry['id']}: CSV canónico vacío")
        if entry["source_start_line"] != original["start"]:
            errors.append(f"Tabla {position} / {entry['id']}: línea inicial distinta")
        if entry["source_end_line"] != original["end"]:
            errors.append(f"Tabla {position} / {entry['id']}: línea final distinta")

    if errors:
        print("AUDITORÍA DE MIGRACIÓN FALLIDA")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "AUDITORÍA DE MIGRACIÓN CORRECTA: "
        f"{len(legacy_entries)} tablas heredadas trazadas y "
        f"{len(native_entries)} tablas canónicas posteriores."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
