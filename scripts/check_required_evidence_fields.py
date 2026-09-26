#!/usr/bin/env python3
"""Censa los campos obligatorios de topologías y fósiles sin rellenar huecos.

El control no convierte ``no consta`` en evidencia positiva: clasifica cada
campo como dato, hueco explícito o no aplicable, exige el ancla C/S/BN/Q de la
fila y falla ante vacíos o marcadores de hueco sin búsqueda/alcance nominal.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path("data/auditoria/censo_campos_topologias_fosiles.csv")
TABLES = {
    "TOPOLOGIA": (
        Path("data/tablas/02/table-01-2-1-2-por-que-el-modelo-cambia-el-arbol.csv"),
        (
            "matriz", "muestreo taxonómico", "análisis", "modelo",
            "resultado publicado", "soporte cuantitativo tal cual",
        ),
        "estudio", "filas y fuentes",
    ),
    "FOSIL": (
        Path("data/tablas/05/table-34-5-8-asignacion-fosil-mas-antigua-localizada-por-nodo.csv"),
        (
            "qué se observa", "qué se infiere", "método de datación",
            "incertidumbre publicada", "quién discute la atribución",
            "argumento de discusión",
        ),
        "nodo", "filas y fuentes",
    ),
}
HEADER = [
    "tipo", "ruta", "fila_csv", "item", "campo", "valor",
    "clasificacion", "anclas_fila", "sha256_valor",
]
GAPS = (
    "no consta", "no hay valor publicado", "no localizado",
    "no publicada", "sin estadística", "sin estadistica",
)


def classify(value: str) -> str:
    folded = value.casefold().strip()
    if folded == "n/a" or folded.startswith("n/a:"):
        return "NO_APLICA_EXPLICITO"
    if any(marker in folded for marker in GAPS):
        return "HUECO_EXPLICITO"
    return "DATO_DECLARADO"


def build(root: Path) -> bytes:
    result: list[dict[str, str]] = []
    errors: list[str] = []
    for kind, (relative, fields, item_field, anchors_field) in TABLES.items():
        with (root / relative).open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        for row_number, row in enumerate(rows, 2):
            anchors = row[anchors_field]
            if "C-" not in anchors:
                errors.append(f"{relative}:fila {row_number}: sin C de anclaje")
            if kind == "TOPOLOGIA" and "S" not in anchors:
                errors.append(f"{relative}:fila {row_number}: sin fuente S")
            no_fossil = kind == "FOSIL" and "NO LOCALIZADO" in row["fósil más antiguo localizado"]
            for field in fields:
                value = row[field].strip()
                if not value:
                    errors.append(f"{relative}:fila {row_number}:{field}: vacío")
                    continue
                category = classify(value)
                if category == "HUECO_EXPLICITO" and not any(
                    marker in anchors for marker in ("BN-", "Q-", "S")
                ):
                    errors.append(
                        f"{relative}:fila {row_number}:{field}: hueco sin BN/Q/S"
                    )
                if category == "NO_APLICA_EXPLICITO" and kind == "TOPOLOGIA":
                    if not value.casefold().startswith("n/a:"):
                        errors.append(
                            f"{relative}:fila {row_number}:{field}: n/a sin motivo"
                        )
                if category == "NO_APLICA_EXPLICITO" and kind == "FOSIL" and not no_fossil:
                    errors.append(
                        f"{relative}:fila {row_number}:{field}: n/a en ítem fósil positivo"
                    )
                result.append({
                    "tipo": kind,
                    "ruta": relative.as_posix(),
                    "fila_csv": str(row_number),
                    "item": row[item_field],
                    "campo": field,
                    "valor": value,
                    "clasificacion": category,
                    "anclas_fila": anchors,
                    "sha256_valor": hashlib.sha256((value + "\n").encode()).hexdigest(),
                })
    if errors:
        raise RuntimeError("\n".join(errors))
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=HEADER, quoting=csv.QUOTE_ALL, lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(result)
    return stream.getvalue().encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        payload = build(root)
    except RuntimeError as error:
        print(f"CENSO DE CAMPOS FALLIDO:\n{error}")
        return 1
    target = root / OUTPUT
    if args.write:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
    elif not target.exists() or target.read_bytes() != payload:
        print(f"CENSO DE CAMPOS DESACTUALIZADO: {OUTPUT}")
        return 1
    print(f"CAMPOS TOPOLOGÍAS/FÓSILES CENSADOS: {payload.count(bytes([10])) - 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
