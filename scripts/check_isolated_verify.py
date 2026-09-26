#!/usr/bin/env python3
"""Ejecuta la misma puerta ``make verify`` en una copia aislada completa."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDITED_ROOTS = (
    "Makefile", "data", "docs", "exports", "fuentes", "manifest.json",
    "scripts", "tests",
)


def workspace_digest(root: Path) -> dict[str, str]:
    """Huella todas las entradas que la puerta puede leer o regenerar."""
    result: dict[str, str] = {}
    for relative in AUDITED_ROOTS:
        candidate = root / relative
        paths = [candidate] if candidate.is_file() else candidate.rglob("*")
        for path in paths:
            if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            key = path.relative_to(root).as_posix()
            result[key] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def run_verify(copy: Path, seed: str) -> tuple[int, str]:
    environment = os.environ.copy()
    environment["AUDIT_ISOLATED_CHILD"] = "1"
    environment["PYTHONHASHSEED"] = seed
    completed = subprocess.run(
        ["make", "verify"],
        cwd=copy,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return completed.returncode, completed.stdout


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="corredor-verify-isolated-") as raw:
        copy = Path(raw) / "repo"
        shutil.copytree(
            ROOT,
            copy,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".coverage"),
        )
        before = workspace_digest(copy)
        first_status, first_output = run_verify(copy, "1")
        if first_status:
            print(
                "La puerta completa falló en la copia aislada con PYTHONHASHSEED=1.",
                file=sys.stderr,
            )
            print(first_output, file=sys.stderr, end="")
            return 1
        after_first = workspace_digest(copy)
        if before != after_first:
            changed = sorted(
                key for key in set(before) | set(after_first)
                if before.get(key) != after_first.get(key)
            )
            print(
                "La puerta aislada mutó el corpus: " + ", ".join(changed[:20]),
                file=sys.stderr,
            )
            return 1
        second_status, second_output = run_verify(copy, "777")
        if second_status:
            print(
                "La puerta completa falló en la copia aislada con "
                "PYTHONHASHSEED=777.",
                file=sys.stderr,
            )
            print(second_output, file=sys.stderr, end="")
            return 1
        after_second = workspace_digest(copy)
        if after_first != after_second:
            changed = sorted(
                key for key in set(after_first) | set(after_second)
                if after_first.get(key) != after_second.get(key)
            )
            print(
                "La puerta aislada no es determinista entre semillas: "
                + ", ".join(changed[:20]),
                file=sys.stderr,
            )
            return 1
        if first_output != second_output:
            print(
                "La salida de la puerta aislada cambia entre "
                "PYTHONHASHSEED=1 y 777.",
                file=sys.stderr,
            )
            return 1
    print(
        "Puerta completa reproducida dos veces en copia aislada, sin mutaciones "
        "y con salidas idénticas para PYTHONHASHSEED=1 y 777."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
