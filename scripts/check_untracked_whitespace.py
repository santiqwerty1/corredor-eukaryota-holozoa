#!/usr/bin/env python3
"""Aplica a archivos nuevos la parte relevante de ``git diff --check``."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".csv", ".json", ".md", ".py", ".txt", ".yml", ".yaml"}


def main() -> int:
    result = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=ROOT, check=True, capture_output=True,
    )
    errors: list[str] = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        relative = raw.decode("utf-8", errors="surrogateescape")
        path = ROOT / relative
        if path.suffix.casefold() not in TEXT_SUFFIXES and path.name not in {"Makefile", "VERSION"}:
            continue
        try:
            lines = path.read_bytes().splitlines(keepends=True)
        except OSError as error:
            errors.append(f"{relative}: no se pudo leer: {error}")
            continue
        for number, line in enumerate(lines, 1):
            body = line.rstrip(b"\r\n")
            if body.endswith((b" ", b"\t")):
                errors.append(f"{relative}:{number}: whitespace al final")
            if (
                body.startswith(b"<<<<<<< ")
                or body == b"======="
                or body.startswith(b">>>>>>> ")
            ):
                errors.append(f"{relative}:{number}: marcador de conflicto")
    if errors:
        print(f"CONTROL DE ARCHIVOS NUEVOS FALLIDO: {len(errors)} problema(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("CONTROL DE ARCHIVOS NUEVOS CORRECTO: sin whitespace ni conflictos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
