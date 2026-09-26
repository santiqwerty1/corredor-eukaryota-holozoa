#!/usr/bin/env python3
"""Construye un censo versionado de procedencia sin afirmar cotejo semántico."""

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
OUTPUT = Path("data/auditoria/procedencia_afirmaciones_v1.csv")
DEPENDENCY = re.compile(r"\bC-(\d{3,5})\b")
HEADER = [
    "version_esquema", "id_afirmacion", "ruta_canonica", "sha256_fila",
    "atribucion", "fuente_y_localizador_declarados", "fuentes_declaradas",
    "dependencias_declaradas", "artefactos_locales", "estado_acceso_registrado",
    "alcance_del_censo",
]


def serialized(header: list[str], row: dict[str, str]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=header, quoting=csv.QUOTE_ALL,
                            lineterminator="\n")
    writer.writerow(row)
    return stream.getvalue().encode("utf-8")


def canonical_claim_id(number: str) -> str:
    value = int(number)
    return f"C-{value:03d}" if value < 1000 else f"C-{value}"


def declared_dependencies(row: dict[str, str], header: list[str]) -> list[str]:
    """Censa referencias inter-C en toda la fila, no solo en Atribución."""
    current = row["#"]
    dependencies = {
        canonical_claim_id(number)
        for field in header
        if field != "#"
        for number in DEPENDENCY.findall(row.get(field, ""))
    }
    dependencies.discard(current)
    return sorted(dependencies)


def build(root: Path) -> bytes:
    matrix_path = root / "docs/auditorias/matriz_fuentes_2026-08-08.csv"
    access: dict[str, str] = {}
    with matrix_path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            access[row["clave_final"]] = row["acceso"]
    appendix_path = root / "data/apendices/A_fuentes.csv"
    with appendix_path.open(encoding="utf-8-sig", newline="") as handle:
        appendix_sources = {row["clave"] for row in csv.DictReader(handle)}
    local_by_source: dict[str, list[str]] = {}
    for path in sorted((root / "fuentes").glob("S*")):
        match = re.match(r"S(\d{1,4})(?:\s|$)", path.name)
        if match:
            key = f"S{int(match.group(1)):02d}"
            local_by_source.setdefault(key, []).append(path.relative_to(root).as_posix())

    claims: list[tuple[str, dict[str, str], list[str]]] = []
    ids: set[str] = set()
    for path in sorted((root / "data/afirmaciones").glob("*.csv")):
        relative = path.relative_to(root).as_posix()
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise RuntimeError(f"Sin cabecera: {relative}")
            for row in reader:
                claim_id = row["#"]
                if claim_id in ids:
                    raise RuntimeError(f"Afirmación duplicada: {claim_id}")
                ids.add(claim_id)
                claims.append((relative, row, reader.fieldnames))

    output: list[dict[str, str]] = []
    for relative, row, header in claims:
        declared = sorted(set(expand_source_refs(row["Fuente"])))
        dependencies = declared_dependencies(row, header)
        missing_dependencies = sorted(set(dependencies) - ids)
        if missing_dependencies:
            raise RuntimeError(f"{row['#']}: dependencias inexistentes {missing_dependencies}")
        missing_sources = sorted(set(declared) - appendix_sources)
        if missing_sources:
            raise RuntimeError(
                f"{row['#']}: fuentes bibliográficas ausentes de A {missing_sources}"
            )
        artifacts = sorted({p for key in declared for p in local_by_source.get(key, [])})
        states = [
            f"{key}: {access[key]}"
            if key in access
            else f"{key}: REGISTRADA EN A; SIN ESTADO EN MATRIZ DE ACCESO"
            for key in declared
        ]
        if row["Atribución"].startswith("expresa"):
            scope = (
                "PROCEDENCIA_DECLARADA; artefacto/acceso censado; "
                "el censo no sustituye cotejo semántico del pasaje"
            )
        elif row["Atribución"].startswith("sintesis"):
            scope = "SINTESIS_CON_DEPENDENCIAS_EXISTENTES; no implica verificación primaria nueva"
        else:
            scope = "GLOSA_DECLARADA; propiedad editorial, no afirmación atribuida a fuente primaria"
        output.append({
            "version_esquema": "1",
            "id_afirmacion": row["#"],
            "ruta_canonica": relative,
            "sha256_fila": hashlib.sha256(serialized(header, row)).hexdigest(),
            "atribucion": row["Atribución"],
            "fuente_y_localizador_declarados": row["Fuente"],
            "fuentes_declaradas": "; ".join(declared) if declared else "n/a",
            "dependencias_declaradas": "; ".join(dependencies) if dependencies else "n/a",
            "artefactos_locales": "; ".join(artifacts) if artifacts else "NO HAY ARTEFACTO LOCAL VERSIONADO",
            "estado_acceso_registrado": "; ".join(states) if states else "n/a",
            "alcance_del_censo": scope,
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
        print(f"PROCEDENCIA CENSADA: {payload.count(bytes([10])) - 1} afirmaciones")
        return 0
    if not path.exists() or path.read_bytes() != payload:
        print(f"CENSO DE PROCEDENCIA DESACTUALIZADO: {OUTPUT}")
        return 1
    print(f"PROCEDENCIA VERIFICABLE: {payload.count(bytes([10])) - 1} afirmaciones")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
