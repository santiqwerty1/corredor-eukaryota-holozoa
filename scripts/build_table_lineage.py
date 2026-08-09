#!/usr/bin/env python3
"""Regenera el linaje auditable de todas las tablas canónicas."""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys

from audit_migration import (
    ARCHIVED_MASTER,
    ARCHIVED_MASTER_SHA256,
    parse_tables,
)
from corpus_io import ROOT, csv_text, load_index, read_csv


HEADER = [
    "table_id",
    "origen",
    "source_master_sha256",
    "source_table_ordinal",
    "source_start_line",
    "source_end_line",
    "source_header_sha256",
    "canonical_path",
    "transformaciones_documentadas",
]


def header_sha256(header: list[str]) -> str:
    payload = "\x1f".join(header) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_rows() -> tuple[list[list[str]], int]:
    archive = ROOT / ARCHIVED_MASTER
    actual = hashlib.sha256(archive.read_bytes()).hexdigest()
    if actual != ARCHIVED_MASTER_SHA256:
        raise ValueError(
            f"El maestro archivado cambió: {actual} != {ARCHIVED_MASTER_SHA256}"
        )
    parsed = parse_tables(archive.read_text(encoding="utf-8").splitlines())
    by_start = {
        table["start"]: (ordinal, table)
        for ordinal, table in enumerate(parsed, start=1)
    }

    rows: list[list[str]] = []
    for entry in load_index()["tables"]:
        start = int(entry["source_start_line"])
        if start > 0:
            if start not in by_start:
                raise ValueError(
                    f"{entry['id']} no coincide con una tabla del maestro en línea {start}"
                )
            ordinal, source_table = by_start[start]
            canonical_header, _ = read_csv(ROOT / entry["csv_path"])
            transformation = (
                "Migración Markdown→CSV; correcciones bibliográficas, "
                "científicas y de claves registradas como delta en la "
                "auditoría 2026-08-08; no se exige igualdad byte a byte."
            )
            if canonical_header != source_table["header"]:
                transformation += (
                    " Cambio de cabecera documentado: "
                    + " | ".join(source_table["header"])
                    + " → "
                    + " | ".join(canonical_header)
                    + "."
                )
            rows.append([
                entry["id"],
                "maestro_v5",
                ARCHIVED_MASTER_SHA256,
                str(ordinal),
                str(start),
                str(entry["source_end_line"]),
                header_sha256(source_table["header"]),
                entry["csv_path"],
                transformation,
            ])
        else:
            rows.append([
                entry["id"],
                "canónica_posterior",
                "n/a",
                "n/a",
                "0",
                "0",
                "n/a",
                entry["csv_path"],
                (
                    "Tabla creada después del maestro v5; procedencia trazada "
                    "por sus C/S y por las matrices de auditoría 2026-08-08."
                ),
            ])

    return rows, len(parsed)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", action="store_true",
        help="No escribe; falla si el linaje canónico no coincide con el esperado.",
    )
    args = parser.parse_args()
    rows, inherited_count = build_rows()
    output = ROOT / "data" / "table_lineage.csv"
    expected = csv_text(HEADER, rows)
    if args.check:
        if not output.exists() or output.read_text(encoding="utf-8") != expected:
            print("Linaje de tablas desactualizado; ejecuta scripts/build_table_lineage.py")
            return 1
        print(
            f"Linaje actualizado: {len(rows)} tablas "
            f"({inherited_count} heredadas; {len(rows) - inherited_count} posteriores)."
        )
        return 0
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writerow(HEADER)
        writer.writerows(rows)
    print(
        f"Linaje regenerado: {len(rows)} tablas "
        f"({inherited_count} heredadas; {len(rows) - inherited_count} posteriores)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
