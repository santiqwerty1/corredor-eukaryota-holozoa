#!/usr/bin/env python3
"""Construye la vista atómica de las C citadas por la sección 19."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SECTION = Path("docs/secciones/025-19-19-respuestas-a-las-seis-preguntas-de-cierre.md")
SUMMARY = Path("data/tablas/19/table-77-19-respuestas-a-las-seis-preguntas-de-cierre.csv")
OUTPUT = Path("data/tablas/19/claims-19.csv")
CLAIM = re.compile(r"\bC-(\d{3,5})\b")
RANGE = re.compile(r"\bC-(\d{3,5})\s*[–-]\s*C-(\d{3,5})\b")
HEADER = [
    "id_vista", "id_afirmacion_canonica", "proposicion",
    "ruta_canonica", "sha256_fila_canonica",
]


def serialized(header: list[str], row: dict[str, str]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=header, quoting=csv.QUOTE_ALL, lineterminator="\n",
    )
    writer.writerow(row)
    return stream.getvalue().encode("utf-8")


def cid(number: int) -> str:
    return f"C-{number:03d}" if number < 1000 else f"C-{number}"


def build(root: Path) -> bytes:
    text = (root / SECTION).read_text(encoding="utf-8")
    text += "\n" + (root / SUMMARY).read_text(encoding="utf-8")
    wanted = {match.group(0) for match in CLAIM.finditer(text)}
    for match in RANGE.finditer(text):
        start, end = map(int, match.groups())
        wanted.update(cid(number) for number in range(start, end + 1))
    claims: dict[str, tuple[str, dict[str, str], list[str]]] = {}
    for path in sorted((root / "data/afirmaciones").glob("*.csv")):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise RuntimeError(f"Afirmaciones sin cabecera: {path}")
            relative = path.relative_to(root).as_posix()
            claims.update(
                (row["#"], (relative, row, reader.fieldnames))
                for row in reader if row["#"] in wanted
            )
    missing = sorted(wanted - claims.keys())
    if missing:
        raise RuntimeError(f"C citadas por sección 19 inexistentes: {missing}")
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=HEADER, quoting=csv.QUOTE_ALL,
                            lineterminator="\n")
    writer.writeheader()
    for number, claim_id in enumerate(sorted(claims, key=lambda key: int(key[2:])), 1):
        relative, row, claim_header = claims[claim_id]
        writer.writerow({
            "id_vista": f"V19-{number:03d}",
            "id_afirmacion_canonica": claim_id,
            "proposicion": row["Afirmación"],
            "ruta_canonica": relative,
            "sha256_fila_canonica": hashlib.sha256(
                serialized(claim_header, row)
            ).hexdigest(),
        })
    return stream.getvalue().encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    payload = build(root)
    path = root / OUTPUT
    if args.write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        print(f"REGISTRO 19 GENERADO: {payload.count(bytes([10])) - 1} proposiciones")
        return 0
    if not path.exists() or path.read_bytes() != payload:
        print(f"REGISTRO 19 DESACTUALIZADO: {OUTPUT}")
        return 1
    print(f"REGISTRO 19 ATÓMICO: {payload.count(bytes([10])) - 1} proposiciones")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
