#!/usr/bin/env python3
"""Auditorías semánticas que complementan la validación estructural."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from corpus_io import (
    ROOT,
    claim_entries,
    load_index,
    negative_entries,
    read_csv,
    table_map,
)


CLAIM_REF = re.compile(r"\bC-\d{3,5}\b")
SOURCE_REF = re.compile(r"\bS\d{2,3}\b")
TABLE_REF = re.compile(r"<!-- TABLE:([a-z0-9-]+) -->")
ATTRIBUTION_TAG = re.compile(
    r"\[([^\]\n]*?);\s*(expresa|glosa|s[ií]ntesis)\]",
    re.IGNORECASE,
)
H2 = re.compile(r"^## (.+)$", re.MULTILINE)
NUMBER = re.compile(r"\d")
LOCATOR = re.compile(
    r"resumen|m[eé]tod|result|discusi[oó]n|fig|tabla|§|p\.|pp\.|"
    r"l[ií]nea|introducci[oó]n|t[ií]tulo|material|supp|extended|nota|"
    r"conclusi[oó]n|tesis|cap[ií]tulo|descripci[oó]n|fisiolog[ií]a|revisi[oó]n",
    re.IGNORECASE,
)


def claim_rows() -> tuple[dict[str, dict[str, str]], list[dict[str, str]]]:
    index = load_index()
    ordered: list[dict[str, str]] = []
    for entry in claim_entries(index):
        path = ROOT / entry["csv_path"]
        with path.open(encoding="utf-8", newline="") as handle:
            ordered.extend(csv.DictReader(handle))
    return {row["#"]: row for row in ordered}, ordered


def appendix_refs(path: Path, column: str) -> set[str]:
    refs: set[str] = set()
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            refs.update(CLAIM_REF.findall(row[column]))
    return refs


def audit_narrative(errors: list[str]) -> None:
    allowed_prefixes = (
        "Williams et al. hicieron una comparación cuantitativa adicional.",
        "Fuente o fuentes principales:",
        "El árbol siguiente es una vista parcial del corredor.",
    )
    # Rótulos de alcance del diagrama, no aristas ni proposiciones científicas.
    # Las aristas reales del bloque siguen obligadas a llevar una referencia C.
    allowed_code_labels = {
        "raíz del árbol celular no especificada",
    }
    for path in sorted((ROOT / "docs" / "secciones").glob("*.md")):
        if path.name.startswith((
            "000-", "001-", "002-", "017-", "018-", "019-", "020-",
            "021-", "022-", "023-", "024-", "025-",
        )):
            continue
        in_code = False
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            text = raw.strip()
            if text.startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                if text and "C-" not in text and text not in allowed_code_labels:
                    errors.append(
                        f"Línea de árbol/esquema sin fila C en "
                        f"{path.relative_to(ROOT)}:{line_no}"
                    )
                continue
            if (
                not text or text.startswith((
                    "#", "<!--", "---", "|", ">",
                ))
            ):
                continue
            if "C-" not in text and not text.startswith(allowed_prefixes):
                errors.append(
                    f"Prosa sin fila C en {path.relative_to(ROOT)}:{line_no}"
                )


def expanded_claim_refs(text: str) -> list[str]:
    refs: list[str] = []
    occupied: list[tuple[int, int]] = []
    for match in re.finditer(r"C-(\d{3,5})\s*[–-]\s*C-(\d{3,5})", text):
        start, end = map(int, match.groups())
        if start > end:
            continue
        refs.extend(
            f"C-{number:03d}" if number < 1000 else f"C-{number}"
            for number in range(start, end + 1)
        )
        occupied.append(match.span())
    for match in CLAIM_REF.finditer(text):
        if not any(start <= match.start() < end for start, end in occupied):
            refs.append(match.group(0))
    return list(dict.fromkeys(refs))


def attribution_category(attribution: str) -> str:
    """Reduce el valor canónico de C a una de las tres categorías narrativas."""

    if attribution.startswith("sintesis("):
        return "síntesis"
    return attribution


def audit_narrative_attribution_labels(
    errors: list[str], by_id: dict[str, dict[str, str]],
) -> None:
    for path in sorted((ROOT / "docs" / "secciones").glob("*.md")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for match in ATTRIBUTION_TAG.finditer(line):
                first_field = match.group(1).split(";", 1)[0]
                refs = expanded_claim_refs(first_field)
                if not refs:
                    continue
                unknown = [ref for ref in refs if ref not in by_id]
                if unknown:
                    errors.append(
                        f"Rótulo de atribución con C inexistente en "
                        f"{path.relative_to(ROOT)}:{line_no}: {', '.join(unknown)}"
                    )
                    continue
                actual = {
                    attribution_category(by_id[ref]["Atribución"])
                    for ref in refs
                }
                raw_expected = match.group(2).casefold()
                if raw_expected == "sintesis":
                    errors.append(
                        f"Rótulo narrativo no canónico 'sintesis' en "
                        f"{path.relative_to(ROOT)}:{line_no}; use 'síntesis'"
                    )
                expected = "síntesis" if raw_expected == "sintesis" else raw_expected
                if actual != {expected}:
                    errors.append(
                        f"Rótulo narrativo {expected!r} no coincide con C en "
                        f"{path.relative_to(ROOT)}:{line_no}: "
                        f"{', '.join(refs)} -> {sorted(actual)}"
                    )


def audit_cross_references(
    errors: list[str], by_id: dict[str, dict[str, str]], ordered: list[dict[str, str]]
) -> None:
    position = {row["#"]: index for index, row in enumerate(ordered)}
    for row in ordered:
        fields = f"{row['Sujeto']} {row['Objeto']}"
        for match in re.finditer(r"afirmación (C-\d{3,5})", fields, re.IGNORECASE):
            ref = match.group(1)
            if ref not in by_id:
                errors.append(f"{row['#']} nombra una afirmación inexistente: {ref}")
            elif position[ref] >= position[row["#"]]:
                errors.append(f"{row['#']} nombra una afirmación no anterior: {ref}")


def audit_quantitative_appendices(
    errors: list[str], ordered: list[dict[str, str]]
) -> None:
    date_refs = appendix_refs(
        ROOT / "data" / "apendices" / "D_fechas.csv",
        "# de la fila que la sostiene",
    )
    magnitude_refs = appendix_refs(
        ROOT / "data" / "apendices" / "F_magnitudes.csv", "#"
    )
    for row in ordered:
        if row["Objeto"].startswith(("NO ", "LA LITERATURA")):
            continue
        if (
            row["Predicado"] == "tiene_edad_estimada"
            and NUMBER.search(row["Objeto"])
            and row["#"] not in date_refs
        ):
            errors.append(f"Fecha cuantitativa sin apéndice D: {row['#']}")
        if (
            row["Predicado"] == "tiene_valor_medido"
            and NUMBER.search(row["Objeto"])
            and row["#"] not in magnitude_refs | date_refs
        ):
            errors.append(f"Magnitud cuantitativa sin apéndice D/F: {row['#']}")


def audit_all_localizers(errors: list[str], ordered: list[dict[str, str]]) -> None:
    for row in ordered:
        if row["Atribución"] != "expresa":
            continue
        source_text = row["Fuente"]
        for source in dict.fromkeys(SOURCE_REF.findall(source_text)):
            clauses = [
                clause.strip()
                for clause in source_text.split(";")
                if source in SOURCE_REF.findall(clause)
            ]
            if not clauses or not any(
                LOCATOR.search(clause) or "sin localizar" in clause.casefold()
                for clause in clauses
            ):
                errors.append(
                    f"Afirmación expresa sin localizador o marca honesta para "
                    f"{source}: {row['#']}"
                )


def audit_glosa_source_contract(
    errors: list[str], ordered: list[dict[str, str]],
) -> None:
    """Una glosa no puede simular respaldo bibliográfico mediante una S."""

    for row in ordered:
        if row["Atribución"] == "glosa" and SOURCE_REF.search(row["Fuente"]):
            errors.append(
                f"Glosa con fuente bibliográfica S: {row['#']} ({row['Fuente']})"
            )


def audit_summary_rows(
    errors: list[str], by_id: dict[str, dict[str, str]],
) -> None:
    """Cada fila sustantiva de tabla se vincula a una o más C existentes."""
    for entry in load_index()["tables"]:
        if entry["category"] not in {"summary", "node"}:
            continue
        header, rows = read_csv(ROOT / entry["csv_path"])
        for row_no, row in enumerate(rows, start=2):
            refs = CLAIM_REF.findall(" ".join(row))
            if not refs:
                errors.append(
                    f"Fila de tabla sin C en {entry['csv_path']}:{row_no}"
                )
            for ref in refs:
                if ref not in by_id:
                    errors.append(
                        f"Fila de tabla con C inexistente en "
                        f"{entry['csv_path']}:{row_no}: {ref}"
                    )


def resolved_sources(
    text: str,
    by_id: dict[str, dict[str, str]],
    tables: dict[str, dict],
) -> set[str]:
    """Resuelve fuentes directas, filas C citadas y tablas insertadas."""

    sources = set(SOURCE_REF.findall(text))
    claim_queue = list(CLAIM_REF.findall(text))
    for table_id in TABLE_REF.findall(text):
        entry = tables[table_id]
        table_text = (ROOT / entry["csv_path"]).read_text(encoding="utf-8")
        sources.update(SOURCE_REF.findall(table_text))
        claim_queue.extend(CLAIM_REF.findall(table_text))

    seen_claims: set[str] = set()
    while claim_queue:
        claim_id = claim_queue.pop()
        if claim_id in seen_claims or claim_id not in by_id:
            continue
        seen_claims.add(claim_id)
        claim_text = " ".join(by_id[claim_id].values())
        sources.update(SOURCE_REF.findall(claim_text))
        claim_queue.extend(CLAIM_REF.findall(claim_text))
    return sources


def audit_h2_source_density(
    errors: list[str], by_id: dict[str, dict[str, str]]
) -> None:
    """Aplica la regla del encargo: cada H2 científico usa al menos dos fuentes."""

    tables = table_map()
    for path in sorted((ROOT / "docs" / "secciones").glob("*.md")):
        top = re.search(r"^# (\d+)\.", path.read_text(encoding="utf-8"), re.MULTILINE)
        if not top or not 2 <= int(top.group(1)) <= 15:
            continue
        text = path.read_text(encoding="utf-8")
        headings = list(H2.finditer(text))
        for index, heading in enumerate(headings):
            title = heading.group(1)
            if "Registro de afirmaciones" in title:
                continue
            end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            sources = resolved_sources(text[heading.start():end], by_id, tables)
            if len(sources) < 2:
                errors.append(
                    f"H2 sostenido por menos de dos fuentes en "
                    f"{path.relative_to(ROOT)}: {title} ({', '.join(sorted(sources)) or '0'})"
                )


def audit_negative_counts(
    errors: list[str], by_id: dict[str, dict[str, str]]
) -> None:
    index = load_index()
    counts: Counter[str] = Counter()
    total = 0
    for entry in negative_entries(index):
        header, rows = read_csv(ROOT / entry["csv_path"])
        names = [name.casefold() for name in header]
        state_pos = next(
            pos for pos, name in enumerate(names) if name in {"estado", "etiqueta"}
        )
        for row in rows:
            counts[row[state_pos]] += 1
            total += 1
    expected = {
        "registro canónico de búsquedas negativas": total,
        "búsquedas negativas con ausencia declarada": counts[
            "LA LITERATURA DECLARA QUE NO SE SABE"
        ],
        "búsquedas negativas sin resultado localizado": counts[
            "NO LOCALIZADO EN ESTA SESIÓN"
        ],
        "búsquedas negativas no buscadas": counts["NO BUSCADO"],
    }
    by_subject: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for row in by_id.values():
        by_subject[row["Sujeto"]].append(row)
    for subject, value in expected.items():
        if not any(str(value) in row["Objeto"] for row in by_subject.get(subject, [])):
            errors.append(
                f"Recuento de búsquedas desactualizado para {subject}: esperado {value}"
            )


def audit_final_markers(errors: list[str]) -> None:
    checks = {
        ROOT / "docs" / "secciones" / "000-preambulo.md": (
            "Documento maestro provisional", "siguen pendientes",
        ),
        ROOT / "docs" / "secciones" / "002-01-1-alcance-del-corpus.md": (
            "permanece pendiente", "no constituye todavía",
        ),
        ROOT / "docs" / "secciones" / "025-19-19-respuestas-a-las-seis-preguntas-de-cierre.md": (
            "Mapa provisional", "estado provisional",
        ),
        ROOT / "data" / "tablas" / "19" / "table-77-19-respuestas-a-las-seis-preguntas-de-cierre.csv": (
            "estado provisional", "faltan tasas evolutivas de 13",
        ),
        ROOT / "README.md": (
            "Estado:** provisional", "secciones 13 y 15 final siguen pendientes",
        ),
        ROOT / "manifest.json": (
            "provisional; faltan las secciones 13 y 15 final",
        ),
    }
    for path, phrases in checks.items():
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase in text:
                errors.append(f"Marcador provisional en {path.relative_to(ROOT)}: {phrase}")


def main() -> int:
    errors: list[str] = []
    by_id, ordered = claim_rows()
    audit_narrative(errors)
    audit_narrative_attribution_labels(errors, by_id)
    audit_cross_references(errors, by_id, ordered)
    audit_quantitative_appendices(errors, ordered)
    audit_all_localizers(errors, ordered)
    audit_glosa_source_contract(errors, ordered)
    audit_summary_rows(errors, by_id)
    audit_h2_source_density(errors, by_id)
    audit_negative_counts(errors, by_id)
    audit_final_markers(errors)

    if errors:
        print(f"AUDITORÍA SEMÁNTICA FALLIDA: {len(errors)} problema(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "AUDITORÍA SEMÁNTICA CORRECTA: narrativa registrada, referencias "
        "anteriores, magnitudes trazadas, densidad H2, contrato de atribución, "
        "localizadores honestos y cierre final."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
