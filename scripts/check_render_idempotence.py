#!/usr/bin/env python3
"""Prueba dos renderizados consecutivos en una copia temporal aislada."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RENDER_OUTPUTS = [
    "data/table_index.json",
    "data/apendices/H_recuento_control.csv",
    "docs/informe.md",
    "docs/informe_completo_autocontenido.md",
    "exports/afirmaciones.csv",
    "exports/busquedas_negativas.csv",
    "exports/tablas_nodales.csv",
    "exports/catalogo_tablas.csv",
    "manifest.json",
]


def digest(root: Path) -> dict[str, str]:
    return {
        relative: hashlib.sha256((root / relative).read_bytes()).hexdigest()
        for relative in RENDER_OUTPUTS
    }


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="corredor-render-idempotence-") as raw:
        copy = Path(raw) / "repo"
        shutil.copytree(
            ROOT,
            copy,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )
        command = [sys.executable, "scripts/render.py"]
        subprocess.run(command, cwd=copy, check=True)
        first = digest(copy)
        subprocess.run(command, cwd=copy, check=True)
        second = digest(copy)
        if first != second:
            changed = [key for key in RENDER_OUTPUTS if first[key] != second[key]]
            print(
                "Render no idempotente; cambiaron en la segunda pasada: "
                + ", ".join(changed),
                file=sys.stderr,
            )
            return 1
    print(
        "Render idempotente: dos pasadas aisladas produjeron "
        f"{len(RENDER_OUTPUTS)} salidas idénticas."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
