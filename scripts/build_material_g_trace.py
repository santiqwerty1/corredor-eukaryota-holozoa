#!/usr/bin/env python3
"""Censa que cada material de G tenga C vigente y destino narrativo explícito."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("data/apendices/G_material_no_encajado.csv")
OUTPUT = Path("data/auditoria/integracion_material_g.csv")
CLAIM = re.compile(r"\bC-(\d{3,5})\b")
RANGE = re.compile(r"\bC-(\d{3,5})\s*[–-]\s*C-(\d{3,5})\b")
HEADER = [
    "fila_g", "material", "afirmaciones_declaradas", "destinos_narrativos",
    "seccion_propuesta", "sha256_fila_g", "resultado",
]


def canonical(number: int) -> str:
    return f"C-{number:03d}" if number < 1000 else f"C-{number}"


def refs(text: str) -> set[str]:
    found = {match.group(0) for match in CLAIM.finditer(text)}
    for match in RANGE.finditer(text):
        start, end = map(int, match.groups())
        found.update(canonical(number) for number in range(start, end + 1))
    return found


def row_digest(header: list[str], row: dict[str, str]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=header, quoting=csv.QUOTE_ALL, lineterminator="\n",
    )
    writer.writerow(row)
    return hashlib.sha256(stream.getvalue().encode("utf-8")).hexdigest()


def build(root: Path) -> bytes:
    claims: set[str] = set()
    for path in sorted((root / "data/afirmaciones").glob("*.csv")):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            claims.update(row["#"] for row in csv.DictReader(handle))
    narrative: dict[str, set[str]] = {}
    for path in sorted((root / "docs/secciones").glob("*.md")):
        relative = path.relative_to(root).as_posix()
        narrative[relative] = refs(path.read_text(encoding="utf-8"))
    for path in sorted((root / "data/tablas").rglob("*.csv")):
        relative = path.relative_to(root).as_posix()
        narrative[relative] = refs(path.read_text(encoding="utf-8"))
    source_path = root / SOURCE
    with source_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise RuntimeError("Apéndice G sin cabecera")
        source_header = reader.fieldnames
        source_rows = list(reader)
    output: list[dict[str, str]] = []
    for number, row in enumerate(source_rows, 2):
        declared = refs(row["#"])
        if not declared:
            if (
                row["#"].strip().casefold() == "n/a"
                and "C01-PROMPT-INVESTIGACION" in row["fuente y localizador"]
                and row["sección propuesta"].strip()
            ):
                output.append({
                    "fila_g": str(number),
                    "material": row["material"],
                    "afirmaciones_declaradas": "n/a",
                    "destinos_narrativos": "docs/C01-PROMPT-INVESTIGACION.md",
                    "seccion_propuesta": row["sección propuesta"],
                    "sha256_fila_g": row_digest(source_header, row),
                    "resultado": "EXCLUIDO_POR_ALCANCE_EXPLICITO",
                })
                continue
            raise RuntimeError(f"G fila {number}: material sin C ni exclusión explícita")
        if not declared <= claims:
            raise RuntimeError(
                f"G fila {number}: C ausentes o inexistentes: {sorted(declared - claims)}"
            )
        destinations = sorted(
            path for path, cited in narrative.items() if cited & declared
        )
        if not destinations:
            raise RuntimeError(
                f"G fila {number}: material sin destino narrativo con C declarada"
            )
        output.append({
            "fila_g": str(number),
            "material": row["material"],
            "afirmaciones_declaradas": "; ".join(sorted(declared)),
            "destinos_narrativos": "; ".join(destinations),
            "seccion_propuesta": row["sección propuesta"],
            "sha256_fila_g": row_digest(source_header, row),
            "resultado": "INTEGRADO_Y_TRAZADO",
        })
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=HEADER, quoting=csv.QUOTE_ALL, lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(output)
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
        print(f"MATERIAL G INTEGRADO: {payload.count(bytes([10])) - 1} filas")
        return 0
    if not path.exists() or path.read_bytes() != payload:
        print(f"TRAZA G DESACTUALIZADA: {OUTPUT}")
        return 1
    print(f"MATERIAL G TRAZADO: {payload.count(bytes([10])) - 1} filas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
