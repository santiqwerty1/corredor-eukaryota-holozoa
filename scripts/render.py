#!/usr/bin/env python3
"""Regenera los informes, exportaciones combinadas, índice y manifest."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from corpus_io import (
    ROOT,
    build_manifest,
    load_index,
    refresh_index_metadata,
    refresh_control_csv,
    render_report,
    save_index,
    write_combined_exports,
    write_manifest,
)


def expected_outputs() -> dict[Path, str]:
    return {
        ROOT / "docs" / "informe.md": render_report("readable"),
        ROOT / "docs" / "informe_completo_autocontenido.md": render_report("full"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="No escribe; falla si los informes o el manifest están desactualizados.",
    )
    args = parser.parse_args()

    if not args.check:
        refresh_control_csv()
    index = refresh_index_metadata(load_index())
    if not args.check:
        save_index(index)
        write_combined_exports()
        for path, content in expected_outputs().items():
            path.write_text(content, encoding="utf-8")
        write_manifest()
        print("Informes, exportaciones, índice y manifest regenerados.")
        return 0

    failures: list[str] = []
    for path, content in expected_outputs().items():
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            failures.append(str(path.relative_to(ROOT)))

    current_manifest = ROOT / "manifest.json"
    # El manifest esperado se calcula sin sobrescribir el actual.
    import json

    expected_manifest = json.dumps(
        build_manifest(), ensure_ascii=False, indent=2
    ) + "\n"
    if not current_manifest.exists() or current_manifest.read_text(encoding="utf-8") != expected_manifest:
        failures.append("manifest.json")

    if failures:
        print("Archivos generados desactualizados:")
        for failure in failures:
            print(f"  - {failure}")
        print("Ejecuta: python scripts/render.py")
        return 1

    print("Archivos generados actualizados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
