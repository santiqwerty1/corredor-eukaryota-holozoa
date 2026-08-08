#!/usr/bin/env python3
"""Comprueba que los CSV conservan las tablas del maestro v5 pre-migración."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from corpus_io import ROOT, load_index, read_csv


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
    source = ROOT / index["source_master"]
    parsed = parse_tables(source.read_text(encoding="utf-8").splitlines())
    entries = sorted(index["tables"], key=lambda entry: entry["source_start_line"])

    errors: list[str] = []
    if len(parsed) != len(entries):
        errors.append(f"Cantidad de tablas: {len(parsed)} != {len(entries)}")

    for position, (original, entry) in enumerate(zip(parsed, entries), start=1):
        header, rows = read_csv(ROOT / entry["csv_path"])
        expected_header = original["header"]
        if entry["category"] == "claims":
            expected_header = [
                "#", "Afirmación", "Sujeto", "Predicado", "Objeto", "Atribución",
                "Fuente", "Aceptación", "Fuerza", "Motivo", "Resolución", "Vigencia",
            ]
        if header != expected_header:
            errors.append(f"Tabla {position} / {entry['id']}: cabecera distinta")
        if entry["id"] == "appendix-h":
            if [row[0] for row in rows] != [row[0] for row in original["rows"]]:
                errors.append(
                    f"Tabla {position} / {entry['id']}: controles distintos"
                )
        elif rows != original["rows"]:
            errors.append(f"Tabla {position} / {entry['id']}: filas distintas")
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
        f"AUDITORÍA DE MIGRACIÓN CORRECTA: "
        f"{len(entries)} tablas y {sum(e['row_count'] for e in entries)} filas."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
