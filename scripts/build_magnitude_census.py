#!/usr/bin/env python3
"""Copia y clasifica estructuralmente F sin certificar publicación ni pasajes."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import re
from pathlib import Path

try:
    from corpus_io import expand_source_refs
except ModuleNotFoundError:  # importación como módulo desde la raíz del repositorio
    from scripts.corpus_io import expand_source_refs


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("data/apendices/F_magnitudes.csv")
OUTPUT = Path("data/auditoria/magnitudes_requeridas_v1.csv")
HEADER = [
    "version_esquema", "fila_f", "magnitud_requerida", "resultado",
    "contenido_copiado_de_f", "razon_clasificacion", "unidad_original",
    "objeto", "metodo_o_proxy", "incertidumbre_publicada",
    "observado_o_inferido", "fuente_y_localizador", "afirmaciones",
    "tipos_de_afirmacion", "sha256_fila_f",
]
GAP_MARKERS = (
    "no hay valor publicado", "no localizado", "no consta en la fuente",
    "sin valor publicado", "n/a",
)
CLAIM = re.compile(r"\bC-(\d{3,5})\b")


def digest(header: list[str], row: dict[str, str]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=header, quoting=csv.QUOTE_ALL,
                            lineterminator="\n")
    writer.writerow(row)
    return hashlib.sha256(stream.getvalue().encode("utf-8")).hexdigest()


def canonical_claim_id(number: str) -> str:
    value = int(number)
    return f"C-{value:03d}" if value < 1000 else f"C-{value}"


def claim_type(attribution: str) -> str:
    if attribution.startswith("sintesis"):
        return "sintesis"
    if attribution.startswith("expresa"):
        return "expresa"
    if attribution == "glosa":
        return "glosa"
    return "otro"


def classify(row: dict[str, str], types: set[str]) -> tuple[str, str]:
    value = row["valor tal como lo publica la fuente"].strip()
    lower = value.casefold()
    uncertainty = row["incertidumbre publicada"].casefold()
    if "sin cifra numérica" in uncertainty:
        return (
            "ESCALA_CUALITATIVA_SIN_CIFRA_COPIADA_DE_F",
            "F declara una escala cualitativa y que no localiza una cifra numérica más precisa",
        )
    if any(marker in lower for marker in GAP_MARKERS):
        return (
            "MARCADOR_DE_HUECO_COPIADO_DE_F",
            "la celda de F contiene literalmente un marcador de ausencia; no se infiere inexistencia bibliográfica",
        )
    if "sintesis" in types:
        return (
            "CONTENIDO_COPIADO_DE_F_CON_C_SINTESIS",
            "al menos una C enlazada declara atribución sintesis; el censo no presenta la celda como transcripción primaria",
        )
    if "glosa" in types:
        return (
            "CONTENIDO_COPIADO_DE_F_CON_C_GLOSA",
            "al menos una C enlazada es glosa; el censo trata la celda como recuento o contenido editorial",
        )
    return (
        "CONTENIDO_COPIADO_DE_F",
        "celda no vacía copiada literalmente de F sin cotejo semántico ni bibliográfico",
    )


def build(root: Path) -> bytes:
    path = root / SOURCE
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise RuntimeError("Apéndice F sin cabecera")
        source_header = reader.fieldnames
        rows = list(reader)
    claims: dict[str, dict[str, str]] = {}
    for claim_path in sorted((root / "data/afirmaciones").glob("*.csv")):
        with claim_path.open(encoding="utf-8-sig", newline="") as handle:
            for claim_row in csv.DictReader(handle):
                claim_id = claim_row["#"]
                if claim_id in claims:
                    raise RuntimeError(f"Afirmación duplicada: {claim_id}")
                claims[claim_id] = claim_row
    with (root / "data/apendices/A_fuentes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        appendix_sources = {row["clave"] for row in csv.DictReader(handle)}
    output: list[dict[str, str]] = []
    for number, row in enumerate(rows, 2):
        value = row["valor tal como lo publica la fuente"].strip()
        if not value:
            raise RuntimeError(f"F fila {number}: valor vacío; debe ser valor o hueco")
        claim_ids = sorted({
            canonical_claim_id(item) for item in CLAIM.findall(row["#"])
        })
        missing_claims = sorted(set(claim_ids) - claims.keys())
        if not claim_ids:
            raise RuntimeError(f"F fila {number}: sin C enlazada")
        if missing_claims:
            raise RuntimeError(f"F fila {number}: C inexistentes {missing_claims}")
        sources = set(expand_source_refs(row["fuente con localizador"]))
        missing_sources = sorted(sources - appendix_sources)
        if missing_sources:
            raise RuntimeError(
                f"F fila {number}: fuentes bibliográficas ausentes de A {missing_sources}"
            )
        types = {claim_type(claims[claim_id]["Atribución"]) for claim_id in claim_ids}
        result, reason = classify(row, types)
        output.append({
            "version_esquema": "1",
            "fila_f": str(number),
            "magnitud_requerida": row["magnitud"],
            "resultado": result,
            "contenido_copiado_de_f": value,
            "razon_clasificacion": reason,
            "unidad_original": row["unidad original"],
            "objeto": row["organismo, nodo o intervalo al que se aplica"],
            "metodo_o_proxy": row["método o proxy"],
            "incertidumbre_publicada": row["incertidumbre publicada"],
            "observado_o_inferido": row["observado o inferido"],
            "fuente_y_localizador": row["fuente con localizador"],
            "afirmaciones": row["#"],
            "tipos_de_afirmacion": "; ".join(sorted(types)),
            "sha256_fila_f": digest(source_header, row),
        })
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=HEADER, quoting=csv.QUOTE_ALL,
                            lineterminator="\n")
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
        print(f"MAGNITUDES CENSADAS: {payload.count(bytes([10])) - 1} filas")
        return 0
    if not path.exists() or path.read_bytes() != payload:
        print(f"CENSO DE MAGNITUDES DESACTUALIZADO: {OUTPUT}")
        return 1
    print(f"MAGNITUDES CLASIFICADAS: {payload.count(bytes([10])) - 1} filas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
