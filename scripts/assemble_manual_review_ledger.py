#!/usr/bin/env python3
"""Ensambla el ledger canónico a partir de dictámenes humanos independientes.

El programa no decide ni promueve resultados: exige exactamente un dictamen
``CONFORME`` por cada control manual, conserva literalmente prueba, evidencia,
localizadores y revisor, y deja que el validador canónico recalcule literales,
alcances y huellas sobre el repositorio vivo.
"""

from __future__ import annotations

import argparse
import csv
import io
import os
import tempfile
from collections import defaultdict
from pathlib import Path

try:  # ejecución como módulo en tests
    from scripts import audit_requirement_controls as controls
except ImportError:  # ejecución directa: python3 scripts/...
    import audit_requirement_controls as controls


REVIEW_COLUMNS = [
    "id_requisito",
    "resultado",
    "prueba_nominal",
    "evidencia",
    "localizadores_evidencia",
    "revisor",
]


def read_reviews(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames not in (
            REVIEW_COLUMNS,
            controls.MANUAL_LEDGER_HEADER,
        ):
            raise RuntimeError(
                f"{path}: cabecera inválida; esperada {REVIEW_COLUMNS} o "
                f"{controls.MANUAL_LEDGER_HEADER}"
            )
        rows = [
            {column: row[column] for column in REVIEW_COLUMNS}
            for row in reader
        ]
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise RuntimeError(f"{path}: fila con cardinalidad inválida")
    return rows


def csv_payload(rows: list[dict[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        buffer,
        fieldnames=controls.MANUAL_LEDGER_HEADER,
        lineterminator="\n",
        quoting=csv.QUOTE_ALL,
    )
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", dir=path.parent,
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def select_final_reviews(
    review_paths: list[Path],
) -> tuple[dict[str, dict[str, str]], list[str]]:
    """Selecciona el último dictamen sin ocultar una reapertura.

    Los ficheros se pasan en orden cronológico. Una repetición solo es válida
    mientras todos los dictámenes anteriores estén abiertos: así se pueden
    conservar primera revisión, corrección y rerevisión, pero nunca sustituir
    silenciosamente un ``CONFORME`` ya cerrado.
    """
    history: dict[str, list[tuple[Path, dict[str, str]]]] = defaultdict(list)
    for path in review_paths:
        for row in read_reviews(path):
            history[row["id_requisito"]].append((path, row))

    errors: list[str] = []
    selected: dict[str, dict[str, str]] = {}
    for requirement_id, entries in history.items():
        for path, row in entries[:-1]:
            if row["resultado"] == "CONFORME":
                errors.append(
                    f"{requirement_id}: un CONFORME previo de {path} fue "
                    "sustituido por otro dictamen"
                )
        selected[requirement_id] = entries[-1][1]
    return selected, errors


def assemble(root: Path, review_paths: list[Path]) -> bytes:
    corpus = controls.Corpus(root)
    _, dispositions = controls.load_control_rows(root)
    results = {
        row["id_requisito"]: controls.evaluate(corpus, row)
        for row in dispositions
        if row["tipo"] == "CONTROL_ESTRUCTURAL"
    }
    expected = {
        requirement_id
        for requirement_id, result in results.items()
        if not result.automated
    }
    literals = controls.load_requirement_literals(root)
    by_id, history_errors = select_final_reviews(review_paths)
    missing = sorted(expected - set(by_id))
    unexpected = sorted(set(by_id) - expected)
    if history_errors or missing or unexpected:
        raise RuntimeError(
            "cobertura de dictámenes inválida: "
            f"historial={history_errors}; faltantes={missing}; "
            f"inesperados={unexpected}"
        )

    output: list[dict[str, str]] = []
    errors: list[str] = []
    for requirement_id in sorted(expected, key=controls.natural):
        review = by_id[requirement_id]
        if review["resultado"] != "CONFORME":
            errors.append(
                f"{requirement_id}: dictamen abierto {review['resultado']}"
            )
            continue
        template = controls.manual_template_row(
            corpus, results[requirement_id], literals[requirement_id],
        )
        template.update({
            "prueba_nominal": review["prueba_nominal"],
            "resultado": review["resultado"],
            "evidencia": review["evidencia"],
            "localizadores_evidencia": review["localizadores_evidencia"],
            "revisor": review["revisor"],
            "declaracion_independencia": controls.INDEPENDENCE_DECLARATION,
            "fecha_revision": controls.REVIEW_CLOSURE_DATE.isoformat(),
        })
        row_errors = controls.validate_manual_review(
            corpus,
            results[requirement_id],
            literals[requirement_id],
            template,
        )
        errors.extend(row_errors)
        output.append(template)
    if errors:
        raise RuntimeError(
            f"dictámenes no cerrados o inválidos ({len(errors)}):\n- "
            + "\n- ".join(errors)
        )
    return csv_payload(output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--review", type=Path, action="append", required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=controls.MANUAL_LEDGER,
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    reviews = [path.resolve() for path in args.review]
    payload = assemble(root, reviews)
    destination = (
        args.output if args.output.is_absolute() else root / args.output
    )
    if args.check:
        if not destination.exists() or destination.read_bytes() != payload:
            print(f"LEDGER MANUAL DESACTUALIZADO: {destination}")
            return 1
        print(
            f"LEDGER MANUAL REPRODUCIBLE: filas={payload.count(bytes([10])) - 1}; "
            f"destino={destination}"
        )
        return 0
    atomic_write(destination, payload)
    print(
        f"LEDGER MANUAL ENSAMBLADO: filas={payload.count(bytes([10])) - 1}; "
        f"destino={destination}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
