#!/usr/bin/env python3
"""Utilidades compartidas del corpus Eukaryota → Holozoa.

Solo usa la biblioteca estándar para que la validación funcione igual en local y CI.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "data" / "table_index.json"
ORDER_PATH = ROOT / "docs" / "order.txt"

CLAIM_COLUMNS = [
    "#", "Afirmación", "Sujeto", "Predicado", "Objeto", "Atribución",
    "Fuente", "Aceptación", "Fuerza", "Motivo", "Resolución", "Vigencia",
]

LINK_CATEGORIES = {"claims", "appendix", "negative"}
SOURCE_RANGE = re.compile(r"\bS(\d{2,3})\s*(?:-|–)\s*S(\d{2,3})\b")
SOURCE_REF = re.compile(r"\bS\d{2,3}\b")


def _supplementary_source_context(value: str, start: int) -> bool:
    prefix = value[max(0, start - 48):start].casefold()
    return bool(re.search(
        r"(?:\bfig(?:s|ures?|uras?)?\.?|\btable|\btabla|"
        r"\bsuppl(?:ementary)?\.?(?:\s+data)?|\bsupplementary(?:\s+data)?|"
        r"\bvideo)\s*$",
        prefix,
    ))


def expand_source_refs(value: str) -> list[str]:
    """Resuelve S bibliográficas y excluye etiquetas de figuras/tablas Sxx."""
    refs: list[str] = []
    occupied: list[tuple[int, int]] = []
    for match in SOURCE_RANGE.finditer(value):
        start, end = map(int, match.groups())
        if start > end:
            raise ValueError(f"Rango S descendente: {match.group(0)}")
        occupied.append(match.span())
        if _supplementary_source_context(value, match.start()):
            continue
        refs.extend(f"S{number:02d}" for number in range(start, end + 1))
    for match in SOURCE_REF.finditer(value):
        if (
            not any(start <= match.start() < end for start, end in occupied)
            and not _supplementary_source_context(value, match.start())
        ):
            refs.append(match.group(0))
    return list(dict.fromkeys(refs))


def load_index() -> dict:
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def save_index(index: dict) -> None:
    INDEX_PATH.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def read_csv(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise ValueError(f"CSV vacío: {path.relative_to(ROOT)}")
    return rows[0], rows[1:]


def write_csv(path: Path, header: Iterable[str], rows: Iterable[Iterable[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writerow(list(header))
        for row in rows:
            writer.writerow([value if value != "" else "n/a" for value in row])


def csv_text(header: Iterable[str], rows: Iterable[Iterable[str]]) -> str:
    """Serializa un CSV canónico sin tocar el sistema de archivos."""
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, quoting=csv.QUOTE_ALL, lineterminator="\n")
    writer.writerow(list(header))
    for row in rows:
        writer.writerow([value if value != "" else "n/a" for value in row])
    return buffer.getvalue()


def escape_markdown_cell(value: str) -> str:
    return value.replace("|", r"\|").replace("\r\n", "<br>").replace("\n", "<br>")


def markdown_table(header: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(escape_markdown_cell(v) for v in header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    lines.extend(
        "| " + " | ".join(escape_markdown_cell(v) for v in row) + " |"
        for row in rows
    )
    return "\n".join(lines)


def section_template_paths() -> list[Path]:
    paths = []
    for raw in ORDER_PATH.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if raw:
            paths.append(ROOT / raw)
    return paths


def table_map(index: dict | None = None) -> dict[str, dict]:
    index = index or load_index()
    return {entry["id"]: entry for entry in index["tables"]}


def refresh_index_metadata(index: dict | None = None) -> dict:
    index = index or load_index()
    for entry in index["tables"]:
        header, rows = read_csv(ROOT / entry["csv_path"])
        entry["columns"] = header
        entry["column_count"] = len(header)
        entry["row_count"] = len(rows)
    return index


def render_placeholder(entry: dict, mode: str) -> str:
    header, rows = read_csv(ROOT / entry["csv_path"])
    if mode == "full" or entry["readable_policy"] == "inline":
        return markdown_table(header, rows)

    relative = "../" + entry["csv_path"]
    category_labels = {
        "claims": "Registro de afirmaciones",
        "appendix": "Apéndice procesable",
        "negative": "Búsquedas negativas",
    }
    label = category_labels.get(entry["category"], "Datos procesables")
    return (
        f"> **{label}:** [{entry['csv_path']}]({relative}) "
        f"({len(rows)} filas; {len(header)} columnas). "
        "La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV."
    )


def render_report(mode: str) -> str:
    if mode not in {"full", "readable"}:
        raise ValueError("mode debe ser 'full' o 'readable'")
    index = refresh_index_metadata()
    entries = table_map(index)
    placeholder_re = re.compile(r"<!-- TABLE:([a-z0-9-]+) -->")
    chunks: list[str] = []

    for path in section_template_paths():
        text = path.read_text(encoding="utf-8")

        def replace(match: re.Match[str]) -> str:
            table_id = match.group(1)
            if table_id not in entries:
                raise KeyError(f"Marcador sin entrada: {table_id}")
            return render_placeholder(entries[table_id], mode)

        chunks.append(placeholder_re.sub(replace, text).rstrip())

    return "\n\n".join(chunks).rstrip() + "\n"


def write_reports() -> None:
    (ROOT / "docs" / "informe.md").write_text(
        render_report("readable"), encoding="utf-8"
    )
    (ROOT / "docs" / "informe_completo_autocontenido.md").write_text(
        render_report("full"), encoding="utf-8"
    )


def claim_entries(index: dict | None = None) -> list[dict]:
    index = index or load_index()
    entries = [e for e in index["tables"] if e["category"] == "claims"]
    return sorted(entries, key=lambda e: int(e["section"]))


def negative_entries(index: dict | None = None) -> list[dict]:
    index = index or load_index()
    entries = [e for e in index["tables"] if e["category"] == "negative"]
    return sorted(entries, key=lambda e: e["id"])


def node_entries(index: dict | None = None) -> list[dict]:
    index = index or load_index()
    return [e for e in index["tables"] if e["category"] == "node"]


def combined_export_payloads(
    index: dict | None = None,
) -> dict[str, tuple[list[str], list[list[str]]]]:
    """Construye en memoria el contenido exacto de todas las exportaciones."""
    index = refresh_index_metadata(index)
    payloads: dict[str, tuple[list[str], list[list[str]]]] = {}

    all_claims: list[list[str]] = []
    for entry in claim_entries(index):
        header, rows = read_csv(ROOT / entry["csv_path"])
        if header != CLAIM_COLUMNS:
            raise ValueError(f"Cabecera de afirmaciones inválida: {entry['csv_path']}")
        all_claims.extend(rows)
    payloads["exports/afirmaciones.csv"] = (CLAIM_COLUMNS, all_claims)

    negative_header = [
        "clave", "sección", "estado", "hueco",
        "términos exactos o motivo", "resultado o motivo", "filas relacionadas",
    ]
    normalized_negative: list[list[str]] = []
    for entry in negative_entries(index):
        header, rows = read_csv(ROOT / entry["csv_path"])
        lookup = {name.lower(): i for i, name in enumerate(header)}
        for row in rows:
            def get_by(predicates: tuple[str, ...], default: str = "n/a") -> str:
                for name, pos in lookup.items():
                    if any(token in name for token in predicates):
                        return row[pos]
                return default

            normalized_negative.append([
                get_by(("clave",)),
                entry["heading_path"][-1] if entry["heading_path"] else entry["section"],
                get_by(("estado", "etiqueta")),
                get_by(("hueco", "elemento")),
                get_by(("términos", "terminos", "fundamento")),
                get_by(("resultado", "consecuencia", "motivo")),
                get_by(("filas",)),
            ])
    payloads["exports/busquedas_negativas.csv"] = (
        negative_header, normalized_negative,
    )

    nodes = node_entries(index)
    if nodes:
        node_header, _ = read_csv(ROOT / nodes[0]["csv_path"])
        node_rows: list[list[str]] = []
        for entry in nodes:
            header, rows = read_csv(ROOT / entry["csv_path"])
            if header != node_header:
                raise ValueError(f"Esquema nodal incompatible: {entry['csv_path']}")
            node_rows.extend(rows)
        payloads["exports/tablas_nodales.csv"] = (node_header, node_rows)

    catalog_header = [
        "table_id", "categoría", "sección", "título", "ruta CSV",
        "filas", "columnas", "política en informe de lectura",
        "línea inicial en maestro v5", "línea final en maestro v5",
    ]
    catalog_rows = [
        [
            e["id"], e["category"], str(e["section"]), e["title"], e["csv_path"],
            str(e["row_count"]), str(e["column_count"]), e["readable_policy"],
            str(e["source_start_line"]), str(e["source_end_line"]),
        ]
        for e in index["tables"]
    ]
    payloads["exports/catalogo_tablas.csv"] = (catalog_header, catalog_rows)
    return payloads


def write_combined_exports() -> None:
    for relative, (header, rows) in combined_export_payloads().items():
        write_csv(ROOT / relative, header, rows)



def control_csv_payload(
    index: dict | None = None,
) -> tuple[Path, list[str], list[list[str]]]:
    """Calcula el apéndice H esperado sin escribirlo."""
    index = refresh_index_metadata(index or load_index())
    claims: list[list[str]] = []
    for entry in claim_entries(index):
        header, rows = read_csv(ROOT / entry["csv_path"])
        claims.extend(rows)

    # El corte inicial de soporte único queda congelado en las notas de A.
    # Se cuenta por afirmación (una C con una sola S), no por frecuencia de uso
    # de la fuente (una S citada en una sola C), que es una propiedad distinta.
    source_entry = next(
        entry for entry in index["tables"] if entry["id"] == "appendix-a"
    )
    source_header, source_rows = read_csv(ROOT / source_entry["csv_path"])
    notes_index = source_header.index("notas de calidad")
    support_marker = re.compile(
        r"\[SOPORTE ÚNICO\] En el corte inicial es la única fuente citada por "
        r"(\d+) afirmaci(?:ón|ones);",
        flags=re.IGNORECASE,
    )
    initial_support_counts = [
        int(match.group(1))
        for row in source_rows
        if (match := support_marker.search(row[notes_index]))
    ]

    claim_id_pos = CLAIM_COLUMNS.index("#")
    attribution_pos = CLAIM_COLUMNS.index("Atribución")
    source_pos = CLAIM_COLUMNS.index("Fuente")
    claim_ids = {row[claim_id_pos] for row in claims}
    source_ids = {row[0] for row in source_rows}
    per_source_claims: dict[str, set[str]] = {}
    current_single_source_claims = 0
    current_sole_support_sources: set[str] = set()
    for row in claims:
        cited = set(expand_source_refs(row[source_pos]))
        for source in cited:
            per_source_claims.setdefault(source, set()).add(row[claim_id_pos])
        if len(cited) == 1:
            current_single_source_claims += 1
            current_sole_support_sources.update(cited)

    event_entry = next(e for e in index["tables"] if e["id"] == "appendix-c")
    _, event_rows = read_csv(ROOT / event_entry["csv_path"])
    event_ids = {row[0] for row in event_rows}
    hypothesis_entry = next(e for e in index["tables"] if e["id"] == "appendix-e")
    _, hypothesis_rows = read_csv(ROOT / hypothesis_entry["csv_path"])
    hypothesis_ids = {row[0] for row in hypothesis_rows}
    negative_ids: set[str] = set()
    for entry in negative_entries(index):
        _, rows = read_csv(ROOT / entry["csv_path"])
        negative_ids.update(row[0] for row in rows)

    reference_text = "\n".join(
        [path.read_text(encoding="utf-8") for path in section_template_paths()]
        + [
            (ROOT / entry["csv_path"]).read_text(encoding="utf-8")
            for entry in index["tables"]
        ]
    )
    undefined_counts = {
        "referencias `C-…` indefinidas": len(
            set(re.findall(r"\bC-\d{3,5}\b", reference_text)) - claim_ids
        ),
        "referencias `S…` indefinidas": len(
            set(expand_source_refs(reference_text)) - source_ids
        ),
        "referencias `E…` indefinidas": len(
            set(re.findall(r"\bE\d{2,3}\b", reference_text)) - event_ids
        ),
        "referencias `H…` indefinidas": len(
            set(re.findall(r"\bH\d{2,3}\b", reference_text)) - hypothesis_ids
        ),
        "referencias `BN-…` indefinidas": len(
            set(re.findall(r"\bBN-\d{3}\b", reference_text)) - negative_ids
        ),
    }

    claim_position = {row[claim_id_pos]: pos for pos, row in enumerate(claims)}
    synthesis_later = 0
    for pos, row in enumerate(claims):
        attribution = row[attribution_pos]
        if not attribution.startswith("sintesis("):
            continue
        for ref in re.findall(r"\bC-\d{3,5}\b", attribution):
            if ref in claim_position and claim_position[ref] >= pos:
                synthesis_later += 1

    template_text = "\n".join(
        path.read_text(encoding="utf-8") for path in section_template_paths()
    )
    sin_fuente = len(re.findall(r"(?m)^\[SIN FUENTE\]", template_text))

    sin_cifra = 0
    for entry in index["tables"]:
        # H contiene el rótulo de este control: contarlo a sí mismo introduciría
        # una celda espuria y volvería no idempotente la regeneración.
        if entry["id"] == "appendix-h":
            continue
        header, rows = read_csv(ROOT / entry["csv_path"])
        for row in rows:
            sin_cifra += sum(
                cell.count("SIN CIFRA PUBLICADA LOCALIZADA") for cell in row
            )

    counts = {
        "número total de fuentes distintas": next(
            e["row_count"] for e in index["tables"] if e["id"] == "appendix-a"
        ),
        "número de oraciones marcadas `[SIN FUENTE]`": sin_fuente,
        "número de filas del registro": len(claims),
        "número inicial de afirmaciones que dependían de una sola fuente": sum(
            initial_support_counts
        ),
        "número de fuentes que eran soporte único de al menos una afirmación en el corte inicial": len(
            initial_support_counts
        ),
        "número actual de afirmaciones que dependen de una sola fuente": current_single_source_claims,
        "número actual de fuentes que son soporte único de al menos una afirmación": len(
            current_sole_support_sources
        ),
        "número actual de fuentes citadas en una sola C": sum(
            len(claim_refs) == 1 for claim_refs in per_source_claims.values()
        ),
        "número actual de fuentes sin uso en una C": len(source_ids - set(per_source_claims)),
        "número de celdas con `SIN CIFRA PUBLICADA LOCALIZADA`": sin_cifra,
        "número de entidades consolidadas": next(
            e["row_count"] for e in index["tables"] if e["id"] == "appendix-b"
        ),
        "número de eventos consolidados": next(
            e["row_count"] for e in index["tables"] if e["id"] == "appendix-c"
        ),
        "número de hipótesis consolidadas": next(
            e["row_count"] for e in index["tables"] if e["id"] == "appendix-e"
        ),
        "número de fechas consolidadas": next(
            e["row_count"] for e in index["tables"] if e["id"] == "appendix-d"
        ),
        "número de magnitudes consolidadas": next(
            e["row_count"] for e in index["tables"] if e["id"] == "appendix-f"
        ),
        "número de búsquedas negativas": sum(
            e["row_count"] for e in negative_entries(index)
        ),
        "síntesis que dependen de una fila posterior": synthesis_later,
    }
    counts.update(undefined_counts)

    h_entry = next(e for e in index["tables"] if e["id"] == "appendix-h")
    h_path = ROOT / h_entry["csv_path"]
    header, rows = read_csv(h_path)
    legacy_controls = {
        "número de afirmaciones que dependen de una sola fuente",
    }
    updated = []
    seen = set()
    for row in rows:
        key = row[0]
        if key in legacy_controls:
            continue
        if key in counts:
            row = [key, str(counts[key])]
            seen.add(key)
        updated.append(row)
    for key, value in counts.items():
        if key not in seen:
            updated.append([key, str(value)])
    return h_path, header, updated


def refresh_control_csv() -> None:
    """Actualiza el apéndice H con recuentos derivados del estado canónico."""
    h_path, header, updated = control_csv_payload()
    write_csv(h_path, header, updated)

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tracked_files() -> list[Path]:
    """Devuelve el conjunto canónico, independiente de basura local oculta."""
    canonical_roots = (
        ROOT / ".github",
        ROOT / "archive",
        ROOT / "data",
        ROOT / "docs",
        ROOT / "exports",
        ROOT / "scripts",
        ROOT / "tests",
    )
    canonical_top_level = (
        ".gitignore", "CONTRIBUTING.md", "Makefile", "README.md",
        "README_DATOS.md", "VERSION",
    )
    paths: list[Path] = []
    for root in canonical_roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                paths.append(path)
    for name in canonical_top_level:
        path = ROOT / name
        if path.exists():
            paths.append(path)
    return sorted(paths, key=lambda p: p.relative_to(ROOT).as_posix())


def build_manifest() -> dict:
    index = refresh_index_metadata()
    source_path = ROOT / index["source_master"]
    source_sha = sha256(source_path)
    counts = {
        "tablas": len(index["tables"]),
        "afirmaciones": sum(e["row_count"] for e in claim_entries(index)),
        "fuentes": next(e["row_count"] for e in index["tables"] if e["id"] == "appendix-a"),
        "entidades": next(e["row_count"] for e in index["tables"] if e["id"] == "appendix-b"),
        "eventos": next(e["row_count"] for e in index["tables"] if e["id"] == "appendix-c"),
        "fechas": next(e["row_count"] for e in index["tables"] if e["id"] == "appendix-d"),
        "hipótesis": next(e["row_count"] for e in index["tables"] if e["id"] == "appendix-e"),
        "magnitudes": next(e["row_count"] for e in index["tables"] if e["id"] == "appendix-f"),
        "búsquedas_negativas": sum(e["row_count"] for e in negative_entries(index)),
    }
    files = []
    for path in tracked_files():
        rel = path.relative_to(ROOT).as_posix()
        files.append({
            "path": rel,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    return {
        "schema_version": 1,
        "corpus": "Corredor Eukaryota → Holozoa",
        "estado": "encargo completo; huecos científicos etiquetados",
        "fecha_de_corte_bibliografico": "2026-08-08",
        "source_master": index["source_master"],
        "source_master_sha256": source_sha,
        "claim_id_format": "C-001…C-999; C-1000 en adelante",
        "counts": counts,
        "files": files,
    }


def write_manifest() -> None:
    manifest = build_manifest()
    (ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
