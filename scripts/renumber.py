#!/usr/bin/env python3
"""Renumera C-… según el orden canónico de las secciones.

Úsalo después de insertar afirmaciones en una sección intermedia, por ejemplo la 13.
Actualiza todos los CSV canónicos y las plantillas narrativas; luego regenera salidas.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

from corpus_io import (
    CLAIM_COLUMNS,
    ROOT,
    claim_entries,
    load_index,
    read_csv,
    section_template_paths,
)


def canonical_claim_id(number: int) -> str:
    return f"C-{number:03d}" if number < 1000 else f"C-{number}"


def atomic_write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent,
    )
    try:
        mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def csv_bytes(header: list[str], rows: list[list[str]]) -> bytes:
    import io

    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, quoting=csv.QUOTE_ALL, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(
        [[value if value != "" else "n/a" for value in row] for row in rows]
    )
    return buffer.getvalue().encode("utf-8")


CLAIM_TOKEN = re.compile(r"\bC-\d{3,5}\b")
CLAIM_REFERENCE = re.compile(
    r"\bC-(\d{3,5})(?:\s*(?:-|–)\s*C-(\d{3,5}))?\b"
)


def replace_claim_references(value: str, mapping: dict[str, str]) -> str:
    """Mapea claves y rangos preservando exactamente los miembros originales."""

    def substitute(match: re.Match[str]) -> str:
        start = int(match.group(1))
        end_text = match.group(2)
        if end_text is None:
            key = canonical_claim_id(start)
            return mapping.get(key, key)
        end = int(end_text)
        if start > end:
            raise ValueError(f"Rango C descendente inválido: {match.group(0)}")
        old_range = [canonical_claim_id(number) for number in range(start, end + 1)]
        missing = [key for key in old_range if key not in mapping]
        if missing:
            raise ValueError(
                f"Rango C contiene claves inexistentes: {match.group(0)} -> {missing[:20]}"
            )
        mapped = [mapping[key] for key in old_range]
        chunks: list[tuple[str, str]] = []
        chunk_start = chunk_end = mapped[0]
        for claim_id in mapped[1:]:
            if int(claim_id.split("-")[1]) == int(chunk_end.split("-")[1]) + 1:
                chunk_end = claim_id
            else:
                chunks.append((chunk_start, chunk_end))
                chunk_start = chunk_end = claim_id
        chunks.append((chunk_start, chunk_end))
        return ", ".join(
            first if first == last else f"{first}–{last}"
            for first, last in chunks
        )

    return CLAIM_REFERENCE.sub(substitute, value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--map-output",
        type=Path,
        help=(
            "Escribe el mapa completo clave_pre_renumeracion→clave_final. "
            "La ruta relativa se resuelve desde la raíz del repositorio."
        ),
    )
    args = parser.parse_args()

    index = load_index()
    ordered_rows: list[list[str]] = []
    for entry in claim_entries(index):
        header, rows = read_csv(ROOT / entry["csv_path"])
        if header != CLAIM_COLUMNS:
            raise ValueError(f"Cabecera inválida: {entry['csv_path']}")
        ordered_rows.extend(rows)

    old_ids = [row[0] for row in ordered_rows]
    malformed = sorted({claim_id for claim_id in old_ids if not CLAIM_TOKEN.fullmatch(claim_id)})
    if malformed:
        raise ValueError(f"Claves C mal formadas antes de renumerar: {malformed[:20]}")
    if len(old_ids) != len(set(old_ids)):
        duplicates = sorted(
            {claim_id for claim_id in old_ids if old_ids.count(claim_id) > 1}
        )
        raise ValueError(f"Claves C duplicadas antes de renumerar: {duplicates[:20]}")
    mapping = {
        old_id: canonical_claim_id(position)
        for position, old_id in enumerate(old_ids, start=1)
    }
    if len(set(mapping.values())) != len(mapping):
        raise ValueError("La renumeración produciría claves C duplicadas")
    changed = {old: new for old, new in mapping.items() if old != new}
    print(f"Afirmaciones: {len(mapping)}; identificadores que cambian: {len(changed)}")
    if args.dry_run:
        for old, new in list(changed.items())[:20]:
            print(f"{old} -> {new}")
        return 0

    def replace(value: str) -> str:
        return replace_claim_references(value, mapping)

    # Precalcula todas las escrituras y rechaza referencias indefinidas antes
    # de tocar el workspace.
    updates: dict[Path, bytes] = {}
    references: set[str] = set()
    for entry in index["tables"]:
        path = ROOT / entry["csv_path"]
        header, rows = read_csv(path)
        references.update(CLAIM_TOKEN.findall(path.read_text(encoding="utf-8")))
        updated = [[replace(cell) for cell in row] for row in rows]
        updates[path] = csv_bytes(header, updated)

    for path in section_template_paths():
        current = path.read_text(encoding="utf-8")
        references.update(CLAIM_TOKEN.findall(current))
        updates[path] = replace(current).encode("utf-8")

    # Entregables de auditoría con referencias C fuera de las plantillas. El
    # prompt, el maestro archivado y los ejemplos de formato de README/MIGRATION
    # son anclas o documentación literal y se excluyen deliberadamente.
    additional_paths: list[Path] = []
    audit_dir = ROOT / "docs" / "auditorias"
    if audit_dir.exists():
        additional_paths.extend(
            path for path in audit_dir.rglob("*")
            if path.is_file() and path.suffix in {".csv", ".json", ".md"}
        )
    for path in additional_paths:
        if not path.exists() or path in updates:
            continue
        current = path.read_text(encoding="utf-8")
        references.update(CLAIM_TOKEN.findall(current))
        updates[path] = replace(current).encode("utf-8")

    undefined = sorted(references - set(mapping))
    if undefined:
        raise ValueError(
            f"Referencias C indefinidas antes de renumerar: {undefined[:20]}"
        )

    map_path: Path | None = None
    if args.map_output:
        map_path = args.map_output
        if not map_path.is_absolute():
            map_path = ROOT / map_path
        map_rows = [
            [old, new, "sí" if old != new else "no"]
            for old, new in mapping.items()
        ]
        updates[map_path] = csv_bytes(
            ["clave_pre_renumeracion", "clave_final", "cambio"], map_rows,
        )

    generated = [
        ROOT / "data" / "table_index.json",
        ROOT / "docs" / "informe.md",
        ROOT / "docs" / "informe_completo_autocontenido.md",
        ROOT / "exports" / "afirmaciones.csv",
        ROOT / "exports" / "busquedas_negativas.csv",
        ROOT / "exports" / "tablas_nodales.csv",
        ROOT / "exports" / "catalogo_tablas.csv",
        ROOT / "manifest.json",
    ]
    rollback_paths = set(updates) | set(generated)
    before = {
        path: path.read_bytes() if path.exists() else None
        for path in rollback_paths
    }

    try:
        for path, content in updates.items():
            atomic_write_bytes(path, content)
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "render.py")],
            check=True,
            cwd=ROOT,
        )
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate.py")],
            check=True,
            cwd=ROOT,
        )
    except BaseException:
        for path, content in before.items():
            if content is None:
                try:
                    path.unlink()
                except FileNotFoundError:
                    pass
            else:
                atomic_write_bytes(path, content)
        print("Renumeración revertida íntegramente tras un fallo.", file=sys.stderr)
        raise

    if map_path is not None:
        try:
            label = map_path.relative_to(ROOT)
        except ValueError:
            label = map_path
        print(f"Mapa de claves: {label}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
