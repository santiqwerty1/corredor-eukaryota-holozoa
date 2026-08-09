#!/usr/bin/env python3
"""Ejecuta la misma puerta ``make verify`` en una copia aislada completa."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="corredor-verify-isolated-") as raw:
        copy = Path(raw) / "repo"
        shutil.copytree(
            ROOT,
            copy,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".coverage"),
        )
        environment = os.environ.copy()
        environment["AUDIT_ISOLATED_CHILD"] = "1"
        completed = subprocess.run(
            ["make", "verify"],
            cwd=copy,
            env=environment,
            text=True,
        )
        if completed.returncode:
            print(
                "La puerta completa falló en la copia aislada.",
                file=sys.stderr,
            )
            return completed.returncode
    print("Puerta completa reproducida correctamente en una copia aislada.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
