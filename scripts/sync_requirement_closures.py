#!/usr/bin/env python3
"""Sincroniza las clausuras C→S/Q del manifiesto de requisitos.

Solo estas dos columnas son mecánicas: se calculan recorriendo cada C declarada
y sus dependencias C. El programa no cambia disposiciones, controles, BN,
tablas ni acciones editoriales.
"""

from __future__ import annotations

import argparse
import csv
import io
import os
import re
import sys
import tempfile
from pathlib import Path

try:
    from corpus_io import expand_source_refs
except ModuleNotFoundError:
    from scripts.corpus_io import expand_source_refs


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path("data/auditoria/requisitos_disposiciones.csv")
CLAIM_REF = re.compile(r"\bC-\d{3,5}\b")
CLAIM_RANGE = re.compile(r"\bC-(\d{3,5})\s*(?:-|–)\s*C-(\d{3,5})\b")
SEARCH_REF = re.compile(r"\bQ-\d{4}\b")


def natural(value: str) -> tuple[str, int, str]:
    match = re.fullmatch(r"([^0-9]*)(\d+)(.*)", value)
    return (value, -1, "") if not match else (
        match.group(1), int(match.group(2)), match.group(3),
    )


def expand_claim_refs(value: str) -> list[str]:
    if value == "n/a":
        return []
    refs: list[str] = []
    occupied: list[tuple[int, int]] = []
    for match in CLAIM_RANGE.finditer(value):
        start, end = map(int, match.groups())
        if start > end:
            raise ValueError(f"Rango C descendente: {match.group(0)}")
        refs.extend(
            f"C-{number:03d}" if number < 1000 else f"C-{number}"
            for number in range(start, end + 1)
        )
        occupied.append(match.span())
    refs.extend(
        match.group(0) for match in CLAIM_REF.finditer(value)
        if not any(start <= match.start() < end for start, end in occupied)
    )
    return list(dict.fromkeys(refs))


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def claims(root: Path) -> dict[str, dict[str, str]]:
    index = __import__("json").loads(
        (root / "data/table_index.json").read_text(encoding="utf-8")
    )
    result: dict[str, dict[str, str]] = {}
    for entry in index["tables"]:
        if entry["category"] != "claims":
            continue
        _, rows = read_csv(root / entry["csv_path"])
        result.update({row["#"]: row for row in rows})
    return result


def closure(initial: list[str], corpus: dict[str, dict[str, str]]) -> tuple[list[str], list[str]]:
    sources: set[str] = set()
    searches: set[str] = set()
    pending = list(initial)
    visited: set[str] = set()
    while pending:
        claim = pending.pop()
        if claim in visited:
            continue
        if claim not in corpus:
            raise ValueError(f"C inexistente en manifiesto: {claim}")
        visited.add(claim)
        field = corpus[claim]["Fuente"]
        sources.update(expand_source_refs(field))
        searches.update(SEARCH_REF.findall(field))
        pending.extend(expand_claim_refs(field))
    return sorted(sources, key=natural), sorted(searches, key=natural)


def payload(root: Path) -> tuple[bytes, int]:
    header, rows = read_csv(root / MANIFEST)
    corpus = claims(root)
    changed = 0
    for row in rows:
        sources, searches = closure(
            expand_claim_refs(row["afirmaciones_exactas"]), corpus
        )
        expected_sources = "; ".join(sources) if sources else "n/a"
        expected_searches = "; ".join(searches) if searches else "n/a"
        if (
            row["fuentes_exactas"] != expected_sources
            or row["busquedas_ejecutadas_exactas"] != expected_searches
        ):
            changed += 1
            row["fuentes_exactas"] = expected_sources
            row["busquedas_ejecutadas_exactas"] = expected_searches
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        buffer, fieldnames=header, quoting=csv.QUOTE_ALL, lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8"), changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected, changed = payload(ROOT)
    path = ROOT / MANIFEST
    if args.check:
        if path.read_bytes() != expected:
            print(f"CLAUSURAS R DESACTUALIZADAS: filas={changed}")
            return 1
    else:
        descriptor, temporary = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=path.parent,
        )
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(expected)
            os.replace(temporary, path)
        except BaseException:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
            raise
    print(
        f"CLAUSURAS R SINCRONIZADAS: filas_cambiadas={changed}; "
        f"modo={'check' if args.check else 'escritura'}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
