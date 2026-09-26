#!/usr/bin/env python3
"""Materializa la comparación cuantitativa pedida por la referencia de escala."""

from __future__ import annotations

import argparse
import csv
import io
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path("data/auditoria/densidad_referencia.csv")
HEADER = [
    "fuentes_corpus", "fuentes_referencia", "cociente_redondeado_2_decimales",
    "umbral_fuentes", "supera_referencia", "supera_umbral",
]


def payload(root: Path) -> bytes:
    with (root / "data/apendices/A_fuentes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        source_count = sum(1 for _ in csv.DictReader(handle))
    reference = 34
    threshold = 80
    ratio = (Decimal(source_count) / Decimal(reference)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP,
    )
    row = {
        "fuentes_corpus": str(source_count),
        "fuentes_referencia": str(reference),
        "cociente_redondeado_2_decimales": str(ratio),
        "umbral_fuentes": str(threshold),
        "supera_referencia": "SI" if source_count > reference else "NO",
        "supera_umbral": "SI" if source_count > threshold else "NO",
    }
    if row["supera_referencia"] != "SI" or row["supera_umbral"] != "SI":
        raise RuntimeError(f"densidad insuficiente: {row}")
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=HEADER, quoting=csv.QUOTE_ALL, lineterminator="\n",
    )
    writer.writeheader()
    writer.writerow(row)
    return stream.getvalue().encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    expected = payload(root)
    path = root / OUTPUT
    if args.write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(expected)
        print("DENSIDAD DE REFERENCIA MATERIALIZADA")
        return 0
    if not path.exists() or path.read_bytes() != expected:
        print(f"DENSIDAD DE REFERENCIA DESACTUALIZADA: {OUTPUT}")
        return 1
    print("DENSIDAD DE REFERENCIA CORRECTA")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
