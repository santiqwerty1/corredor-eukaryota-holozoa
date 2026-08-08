#!/usr/bin/env python3
"""Valida estructura, referencias, vocabularios y salidas generadas."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

from corpus_io import (
    CLAIM_COLUMNS,
    ROOT,
    build_manifest,
    claim_entries,
    load_index,
    negative_entries,
    read_csv,
    refresh_index_metadata,
    render_report,
    section_template_paths,
)

ALLOWED = {
    "Atribución": {"expresa", "glosa"},
    "Aceptación": {
        "consenso amplio", "aceptación mayoritaria", "aceptación mixta",
        "posición minoritaria", "no evaluado",
    },
    "Fuerza": {"alta", "media", "baja", "desconocida"},
    "Resolución": {
        "resuelta", "parcialmente resuelta", "sin resolver",
        "información insuficiente",
    },
    "Vigencia": {"vigente", "histórica", "superada", "rechazada"},
}

SOURCE_TYPES = {
    "investigación primaria", "revisión", "base de datos taxonómica",
    "preprint", "capítulo o libro", "tesis", "divulgación o blog", "otro",
}


def read_all_text(paths: list[Path]) -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def canonical_claim_id(number: int) -> str:
    return f"C-{number:03d}" if number < 1000 else f"C-{number}"


def main() -> int:
    errors: list[str] = []
    index = refresh_index_metadata(load_index())
    entries = index["tables"]

    ids = [e["id"] for e in entries]
    if len(ids) != len(set(ids)):
        errors.append("Hay table_id duplicados.")
    csv_paths = [e["csv_path"] for e in entries]
    if len(csv_paths) != len(set(csv_paths)):
        errors.append("Hay rutas CSV canónicas duplicadas.")

    placeholders_text = read_all_text(section_template_paths())
    placeholders = re.findall(r"<!-- TABLE:([a-z0-9-]+) -->", placeholders_text)
    if set(placeholders) != set(ids):
        errors.append(
            "Los marcadores de tablas no coinciden con table_index.json: "
            f"faltan={sorted(set(ids)-set(placeholders))}, "
            f"sobran={sorted(set(placeholders)-set(ids))}"
        )
    if len(placeholders) != len(set(placeholders)):
        errors.append("Hay marcadores TABLE duplicados en las plantillas.")

    # CSV: existencia, esquema, dimensiones y ausencia de vacíos.
    for entry in entries:
        path = ROOT / entry["csv_path"]
        if not path.exists():
            errors.append(f"Falta {entry['csv_path']}")
            continue
        header, rows = read_csv(path)
        if len(header) != entry["column_count"]:
            errors.append(f"Columnas desactualizadas en {entry['csv_path']}")
        if len(rows) != entry["row_count"]:
            errors.append(f"Filas desactualizadas en {entry['csv_path']}")
        for rno, row in enumerate(rows, start=2):
            if len(row) != len(header):
                errors.append(
                    f"Fila irregular {entry['csv_path']}:{rno}: "
                    f"{len(row)} != {len(header)}"
                )
            for cno, value in enumerate(row, start=1):
                if value == "":
                    errors.append(
                        f"Celda vacía {entry['csv_path']}:{rno}:{cno}; usa n/a."
                    )

    # Afirmaciones.
    claims: list[list[str]] = []
    for entry in claim_entries(index):
        header, rows = read_csv(ROOT / entry["csv_path"])
        if header != CLAIM_COLUMNS:
            errors.append(f"Cabecera de afirmaciones inválida: {entry['csv_path']}")
        claims.extend(rows)

    claim_ids = [row[0] for row in claims]
    if len(claim_ids) != len(set(claim_ids)):
        errors.append("Hay identificadores C duplicados.")
    expected_claim_ids = [
        canonical_claim_id(number) for number in range(1, len(claim_ids) + 1)
    ]
    if claim_ids != expected_claim_ids:
        for pos, (actual, expected) in enumerate(
            zip(claim_ids, expected_claim_ids), start=1
        ):
            if actual != expected:
                errors.append(
                    f"Secuencia C rota en posición {pos}: {actual} != {expected}"
                )
                break
        if len(claim_ids) != len(expected_claim_ids):
            errors.append("Longitud inesperada de la secuencia C.")

    claim_id_set = set(claim_ids)
    claim_num = {cid: int(cid.split("-")[1]) for cid in claim_ids}
    col = {name: pos for pos, name in enumerate(CLAIM_COLUMNS)}
    synthesis_re = re.compile(r"^sintesis\((.+)\)$")
    claim_ref_re = re.compile(r"\bC-\d{3,4}\b")
    for row in claims:
        cid = row[col["#"]]
        attribution = row[col["Atribución"]]
        if attribution not in ALLOWED["Atribución"]:
            match = synthesis_re.fullmatch(attribution)
            if not match:
                errors.append(f"Atribución inválida en {cid}: {attribution}")
            else:
                refs = claim_ref_re.findall(match.group(1))
                if not refs:
                    errors.append(f"Síntesis sin filas de origen en {cid}: {attribution}")
                for ref in refs:
                    if ref not in claim_id_set:
                        errors.append(f"{cid} sintetiza una fila inexistente: {ref}")
                    elif claim_num[ref] >= claim_num[cid]:
                        errors.append(
                            f"{cid} sintetiza una fila no anterior: {ref}"
                        )
        for name in ("Aceptación", "Fuerza", "Resolución", "Vigencia"):
            value = row[col[name]]
            if value not in ALLOWED[name]:
                errors.append(f"{name} inválida en {cid}: {value}")
        if not row[col["Motivo"]].strip():
            errors.append(f"Motivo vacío en {cid}")

    # Claves de apéndices y búsquedas.
    appendix_paths = {
        e["id"]: ROOT / e["csv_path"]
        for e in entries if e["category"] == "appendix"
    }
    source_header, source_rows = read_csv(appendix_paths["appendix-a"])
    source_ids = {row[0] for row in source_rows}
    event_ids = {row[0] for row in read_csv(appendix_paths["appendix-c"])[1]}
    hypothesis_ids = {row[0] for row in read_csv(appendix_paths["appendix-e"])[1]}

    negative_ids: set[str] = set()
    for entry in negative_entries(index):
        header, rows = read_csv(ROOT / entry["csv_path"])
        key_pos = header.index("clave")
        for row in rows:
            key = row[key_pos]
            if key in negative_ids:
                errors.append(f"Clave BN duplicada: {key}")
            negative_ids.add(key)

    # Tipos de fuente y duplicados bibliográficos.
    type_pos = source_header.index("tipo")
    title_pos = source_header.index("título")
    locator_pos = next(
        i for i, name in enumerate(source_header)
        if name.startswith("DOI en forma")
    )
    for row in source_rows:
        if row[type_pos] not in SOURCE_TYPES:
            errors.append(f"Tipo de fuente inválido en {row[0]}: {row[type_pos]}")
    for label, pos in (("título", title_pos), ("DOI/URL", locator_pos)):
        seen: dict[str, str] = {}
        for row in source_rows:
            value = row[pos].strip()
            if not value or value == "n/a" or value == "DOI no verificado":
                continue
            key = value.casefold()
            if key in seen:
                errors.append(
                    f"{label} bibliográfico duplicado: {seen[key]} y {row[0]}"
                )
            seen[key] = row[0]

    # Referencias internas en plantillas y CSV canónicos.
    reference_paths = section_template_paths() + [
        ROOT / entry["csv_path"] for entry in entries
    ]
    corpus_text = read_all_text(reference_paths)
    reference_specs = [
        (r"\bC-\d{3,4}\b", claim_id_set, "C"),
        (r"\bS\d{2,3}\b", source_ids, "S"),
        (r"\bE\d{2,3}\b", event_ids, "E"),
        (r"\bH\d{2,3}\b", hypothesis_ids, "H"),
        (r"\bBN-\d{3}\b", negative_ids, "BN"),
    ]
    for pattern, valid, label in reference_specs:
        found = set(re.findall(pattern, corpus_text))
        undefined = sorted(found - valid)
        if undefined:
            errors.append(f"Referencias {label} indefinidas: {undefined[:20]}")

    # Salidas generadas.
    expected_reports = {
        ROOT / "docs" / "informe.md": render_report("readable"),
        ROOT / "docs" / "informe_completo_autocontenido.md": render_report("full"),
    }
    for path, expected in expected_reports.items():
        if not path.exists() or path.read_text(encoding="utf-8") != expected:
            errors.append(f"Salida generada desactualizada: {path.relative_to(ROOT)}")

    expected_manifest = json.dumps(
        build_manifest(), ensure_ascii=False, indent=2
    ) + "\n"
    manifest_path = ROOT / "manifest.json"
    if not manifest_path.exists() or manifest_path.read_text(encoding="utf-8") != expected_manifest:
        errors.append("manifest.json desactualizado.")

    for required in (
        ROOT / "exports" / "afirmaciones.csv",
        ROOT / "exports" / "busquedas_negativas.csv",
        ROOT / "exports" / "tablas_nodales.csv",
        ROOT / "exports" / "catalogo_tablas.csv",
    ):
        if not required.exists():
            errors.append(f"Falta exportación combinada: {required.relative_to(ROOT)}")

    if errors:
        print(f"VALIDACIÓN FALLIDA: {len(errors)} problema(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("VALIDACIÓN CORRECTA")
    print(f"- afirmaciones: {len(claim_ids)}")
    print(f"- fuentes: {len(source_ids)}")
    print(f"- entidades: {len(read_csv(appendix_paths['appendix-b'])[1])}")
    print(f"- eventos: {len(event_ids)}")
    print(f"- fechas: {len(read_csv(appendix_paths['appendix-d'])[1])}")
    print(f"- hipótesis: {len(hypothesis_ids)}")
    print(f"- magnitudes: {len(read_csv(appendix_paths['appendix-f'])[1])}")
    print(f"- búsquedas negativas: {len(negative_ids)}")
    print(f"- tablas canónicas: {len(entries)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
