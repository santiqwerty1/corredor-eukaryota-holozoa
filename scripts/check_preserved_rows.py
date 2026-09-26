#!/usr/bin/env python3
"""Prueba que las filas que el encargo ordenó no tocar siguen byte-idénticas."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_COMMIT = "af7e799e2d096a48f24afd31d7745e19cebf374d"
OUTPUT = Path("data/auditoria/conservacion_filas_cuestionadas.csv")
TARGETS = {"data/afirmaciones/02.csv": ("C-018",)}
HEADER = [
    "ruta", "clave", "commit_evidencia", "sha256_fila_evidencia",
    "sha256_fila_viva", "resultado",
]


def row_bytes(header: list[str], row: dict[str, str]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=header, quoting=csv.QUOTE_ALL, lineterminator="\n",
    )
    writer.writerow(row)
    return stream.getvalue().encode("utf-8")


def read_rows(payload: str) -> tuple[list[str], dict[str, dict[str, str]]]:
    reader = csv.DictReader(io.StringIO(payload))
    if reader.fieldnames is None:
        raise RuntimeError("CSV sin cabecera")
    rows = {row["#"]: row for row in reader}
    return reader.fieldnames, rows


def build(root: Path) -> bytes:
    output: list[dict[str, str]] = []
    for relative, keys in TARGETS.items():
        historical = subprocess.run(
            ["git", "show", f"{EVIDENCE_COMMIT}:{relative}"],
            cwd=root, check=True, text=True, stdout=subprocess.PIPE,
        ).stdout
        live = (root / relative).read_text(encoding="utf-8")
        old_header, old_rows = read_rows(historical)
        new_header, new_rows = read_rows(live)
        if old_header != new_header:
            raise RuntimeError(f"{relative}: cabecera viva distinta de evidencia")
        for key in keys:
            if key not in old_rows or key not in new_rows:
                raise RuntimeError(f"{relative}: falta {key}")
            old_hash = hashlib.sha256(
                row_bytes(old_header, old_rows[key])
            ).hexdigest()
            new_hash = hashlib.sha256(
                row_bytes(new_header, new_rows[key])
            ).hexdigest()
            if old_hash != new_hash:
                raise RuntimeError(
                    f"{relative}:{key}: la fila cuestionada cambió"
                )
            output.append({
                "ruta": relative,
                "clave": key,
                "commit_evidencia": EVIDENCE_COMMIT,
                "sha256_fila_evidencia": old_hash,
                "sha256_fila_viva": new_hash,
                "resultado": "IDENTICA_BYTE_A_BYTE",
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
        print(f"FILAS CUESTIONADAS FIJADAS: {payload.count(bytes([10])) - 1}")
        return 0
    if not path.exists() or path.read_bytes() != payload:
        print(f"CONSERVACIÓN DESACTUALIZADA: {OUTPUT}")
        return 1
    print(f"FILAS CUESTIONADAS IDÉNTICAS: {payload.count(bytes([10])) - 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
