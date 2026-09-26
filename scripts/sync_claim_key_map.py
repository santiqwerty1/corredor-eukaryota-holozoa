#!/usr/bin/env python3
"""Sincroniza en el mapa las altas C prospectivas sin reescribir su linaje."""

from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "docs/auditorias/mapa_claves_inicial_final_2026-08-08.csv"
HEADER = ["clave_pre_renumeracion", "clave_final", "cambio"]
PROSPECTIVE_START = 1953


def claim_ids() -> list[str]:
    result: list[str] = []
    for path in sorted((ROOT / "data/afirmaciones").glob("*.csv")):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            result.extend(row["#"] for row in csv.DictReader(handle))
    return result


def payload() -> bytes:
    with MAP.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != HEADER:
            raise RuntimeError(f"Cabecera inesperada: {reader.fieldnames!r}")
        rows = list(reader)
    rows = [
        row for row in rows
        if not (
            row["clave_pre_renumeracion"] == row["clave_final"]
            and int(row["clave_final"].split("-")[1]) >= PROSPECTIVE_START
        )
    ]
    live = claim_ids()
    existing_final = {row["clave_final"] for row in rows}
    for claim_id in live:
        number = int(claim_id.split("-")[1])
        if number >= PROSPECTIVE_START:
            if claim_id in existing_final:
                raise RuntimeError(f"Alta prospectiva colisiona con el mapa histórico: {claim_id}")
            rows.append({
                "clave_pre_renumeracion": claim_id,
                "clave_final": claim_id,
                # El contrato histórico de esta columna es binario. La condición
                # prospectiva se deduce de la clave >= PROSPECTIVE_START y no se
                # disfraza como una tercera clase de cambio.
                "cambio": "no",
            })
    if {row["clave_final"] for row in rows} != set(live):
        raise RuntimeError("El mapa sincronizado no cubre exactamente las C vivas")
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=HEADER, quoting=csv.QUOTE_ALL, lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    expected = payload()
    if args.write:
        MAP.write_bytes(expected)
        print(f"MAPA C SINCRONIZADO: {len(claim_ids())} claves")
        return 0
    if MAP.read_bytes() != expected:
        print(f"MAPA C DESACTUALIZADO: {MAP.relative_to(ROOT)}")
        return 1
    print(f"MAPA C EXACTO: {len(claim_ids())} claves")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
