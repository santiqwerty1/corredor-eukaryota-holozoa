#!/usr/bin/env python3
"""Renumera C-… según el orden canónico de las secciones.

Úsalo después de insertar afirmaciones en una sección intermedia, por ejemplo la 13.
Actualiza todos los CSV canónicos y las plantillas narrativas; luego regenera salidas.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from corpus_io import (
    CLAIM_COLUMNS,
    ROOT,
    claim_entries,
    load_index,
    read_csv,
    section_template_paths,
    write_csv,
)


def canonical_claim_id(number: int) -> str:
    return f"C-{number:03d}" if number < 1000 else f"C-{number}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    index = load_index()
    ordered_rows: list[list[str]] = []
    entry_rows: list[tuple[dict, list[str], list[list[str]]]] = []
    for entry in claim_entries(index):
        header, rows = read_csv(ROOT / entry["csv_path"])
        if header != CLAIM_COLUMNS:
            raise ValueError(f"Cabecera inválida: {entry['csv_path']}")
        entry_rows.append((entry, header, rows))
        ordered_rows.extend(rows)

    mapping = {
        row[0]: canonical_claim_id(position)
        for position, row in enumerate(ordered_rows, start=1)
    }
    changed = {old: new for old, new in mapping.items() if old != new}
    print(f"Afirmaciones: {len(mapping)}; identificadores que cambian: {len(changed)}")
    if args.dry_run:
        for old, new in list(changed.items())[:20]:
            print(f"{old} -> {new}")
        return 0

    pattern = re.compile(r"\bC-\d{3,5}\b")

    def replace(value: str) -> str:
        return pattern.sub(lambda match: mapping.get(match.group(0), match.group(0)), value)

    # Todos los CSV canónicos, incluidos apéndices, fechas, eventos y tablas.
    for entry in index["tables"]:
        path = ROOT / entry["csv_path"]
        header, rows = read_csv(path)
        updated = [[replace(cell) for cell in row] for row in rows]
        write_csv(path, header, updated)

    # Plantillas narrativas.
    for path in section_template_paths():
        path.write_text(replace(path.read_text(encoding="utf-8")), encoding="utf-8")

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "render.py")],
        check=True,
        cwd=ROOT,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate.py")],
        check=True,
        cwd=ROOT,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
