#!/usr/bin/env python3
"""Construye y verifica la trazabilidad final por oración, arista y celda.

La unidad de mapeo es deliberadamente estrecha: una oración no hereda las C
de su párrafo ni de un árbol posterior, y una celda no hereda todas las C de
su fila. Las celdas sustantivas de tablas ``summary`` y ``node`` se fijan por
ruta, fila, columna y SHA-256 de su valor normalizado. Salvo una C escrita en
la propia celda, su correspondencia procede únicamente del manifiesto
canónico ``data/auditoria/mapeo_celdas_afirmaciones.csv``. La puntuación
léxica puede producir sugerencias de diagnóstico, pero nunca aprueba una
celda ni la marca como revisada.

Una unidad sin correspondencia queda como ``SIN_TRAZABILIDAD`` y hace fallar
la construcción; nunca se rellena con una referencia de contexto genérica.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "auditorias" / "matriz_trazabilidad_contenido_2026-08-08.csv"
CELL_MANIFEST = ROOT / "data" / "auditoria" / "mapeo_celdas_afirmaciones.csv"
CLAIM = re.compile(r"\bC-\d{3,5}\b")
RANGE = re.compile(r"\bC-(\d{3,5})\s*(?:-|–)\s*C-(\d{3,5})\b")
SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿¡“«`])")
ABBREVIATION = re.compile(
    r"\b(?:figs?|suppl|pp?|spp?|cf)\.|\bet\s+al\.", re.IGNORECASE,
)
SPURIOUS_SENTENCE_START = re.compile(
    r"^(?:S\d{1,3}\b|figs?\.?\b|suppl\.?\b|pp?\.\s)", re.IGNORECASE,
)
SCIENTIFIC_TEMPLATES = re.compile(r"^(?:00[1-9]|01[0-6]|025)-.*\.md$")
EDITORIAL_PREFIXES = (
    "Las filas siguientes documentan el alcance del encargo",
    "Fuente o fuentes principales:",
    "Fuente principal:",
    "El árbol siguiente es una vista parcial",
    "Las ramas eucariotas externas no se despliegan",
)
EMPTY_VALUES = {"", "n/a", "—", "-"}
METADATA_COLUMNS = re.compile(
    r"^(?:#(?: de la fila del registro.*)?|n[.º°o]*|"
    r"fila(?:s)?(?: y fuentes?| por celda)?|"
    r"fuente(?:s)?(?: y localizador)?|clave|"
    r"referencias?|citas?|marca|id(?:entificador)?|afirmaciones?|"
    r"secciones? con material integrado)$",
    re.IGNORECASE,
)
IDENTITY_COLUMNS = {
    "caso", "modelo a", "modelo b", "pregunta", "nodo", "taxon",
    "taxón", "entidad", "organismo", "hipotesis", "hipótesis", "nombre",
    "termino", "término", "código", "codigo",
}
STOPWORDS = {
    "a", "al", "ante", "bajo", "con", "contra", "como", "de", "del",
    "desde", "durante", "e", "el", "ella", "en", "entre", "es", "esta",
    "este", "estos", "ha", "hacia", "hasta", "la", "las", "lo", "los",
    "más", "menos", "ni", "no", "o", "para", "pero", "por", "que",
    "se", "según", "sin", "sobre", "su", "sus", "un", "una", "uno",
    "y", "ya", "the", "of", "and", "in", "to", "from", "with",
}
HEADER = [
    "id_segmento", "tipo", "ruta", "localizador", "columna", "contenido",
    "sha256_contenido", "afirmaciones", "metodo_mapeo", "estado_revision",
]
CELL_MANIFEST_HEADER = [
    "csv_path", "fila", "columna", "contenido_sha256", "contenido",
    "afirmaciones", "base_semantica", "estado_revision",
    "nota_adjudicacion",
]


@dataclass(frozen=True)
class Segment:
    kind: str
    path: str
    locator: str
    column: str
    content: str
    claims: tuple[str, ...]
    method: str
    content_sha256: str = ""


@dataclass(frozen=True)
class TableCell:
    path: str
    row_number: int
    column: str
    raw_content: str
    contextual_content: str
    own_refs: tuple[str, ...]

    @property
    def content_sha256(self) -> str:
        return hashlib.sha256((self.raw_content + "\n").encode("utf-8")).hexdigest()

    @property
    def manifest_key(self) -> tuple[str, int, str, str]:
        return self.path, self.row_number, self.column, self.content_sha256


def canonical_claim(number: int) -> str:
    return f"C-{number:03d}" if number < 1000 else f"C-{number}"


def claim_refs(text: str) -> tuple[str, ...]:
    refs: list[str] = []
    occupied: list[tuple[int, int]] = []
    for match in RANGE.finditer(text):
        start, end = map(int, match.groups())
        if start <= end:
            refs.extend(canonical_claim(number) for number in range(start, end + 1))
        occupied.append(match.span())
    for match in CLAIM.finditer(text):
        if not any(start <= match.start() < end for start, end in occupied):
            refs.append(match.group(0))
    return tuple(dict.fromkeys(refs))


def normalized_content(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def lexical_tokens(text: str) -> tuple[str, ...]:
    folded = "".join(
        character for character in unicodedata.normalize("NFKD", text.casefold())
        if not unicodedata.combining(character)
    )
    raw_tokens = re.findall(r"[a-z0-9]+(?:[.,][0-9]+)?", folded)
    tokens: list[str] = []
    for token in raw_tokens:
        if len(token) <= 1 or token in STOPWORDS:
            continue
        if token.isalpha() and len(token) > 5 and token.endswith("es"):
            token = token[:-2]
        elif token.isalpha() and len(token) > 4 and token.endswith("s"):
            token = token[:-1]
        tokens.append(token)
    return tuple(tokens)


def editorial_sentence(text: str) -> bool:
    stripped = normalized_content(text).strip(" -*_`[]()")
    if not stripped:
        return True
    if any(stripped.startswith(prefix) for prefix in EDITORIAL_PREFIXES):
        return True
    if re.fullmatch(r"\d+[.)]?", stripped):
        return True
    if re.fullmatch(
        r"S\d{1,3}(?:\s*[–-]\s*S?\d{1,3})?(?:\s+[^;\]]+)?"
        r"(?:\s*[;,]\s*S\d{1,3}(?:\s+[^;\]]+)?) *\]?",
        stripped,
    ):
        return True
    lowered = stripped.casefold()
    if stripped.startswith("C-"):
        # Línea de referencias/localizadores desnudos, no proposición.
        return True
    if lowered.startswith((
        "registro de afirmaciones", "tabla ", "árbol de trabajo", "arbol de trabajo",
        "a continuación", "a continuacion", "véase ", "vease ", "nota editorial",
        "estas definiciones son", "el esquema representa", "solo se conservan esas",
        "en esta sección se conserva", "en esta seccion se conserva",
        "williams et al. hicieron una comparación", "williams et al. hicieron una comparacion",
        "la tabla resume resultados", "los modelos sitio-homogéneos",
        "relaciones y cifras registradas:", "relaciones registradas:",
        "esquema separado del modelo;", "esquema separado del modelo:",
    )) and not claim_refs(stripped):
        return True
    if lowered.startswith((
        "relaciones y cifras registradas:", "relaciones registradas:",
        "esquema separado del modelo;", "esquema separado del modelo:",
    )):
        return True
    return False


def editorial_edge(text: str) -> bool:
    """Excluye rótulos/notas de los bloques ASCII sin fingir una arista."""
    lowered = normalized_content(text).strip(" []").casefold()
    return lowered.startswith((
        "raíz del árbol celular", "raiz del arbol celular",
        "├─ ⋯ ramas externas", "└─ ⋯ ramas externas", "ramas externas",
        "orden de las ramas", "[orden de las ramas",
    )) or "no representado; véase" in lowered or "no representado; vease" in lowered


def claim_catalog() -> tuple[dict[str, str], dict[str, tuple[str, ...]]]:
    texts: dict[str, str] = {}
    tokens: dict[str, tuple[str, ...]] = {}
    for path in sorted((ROOT / "data" / "afirmaciones").glob("*.csv")):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                key = row["#"]
                text = " | ".join(
                    row[field] for field in (
                        "Afirmación", "Sujeto", "Predicado", "Objeto",
                        "Fuente", "Motivo", "Resolución",
                    )
                )
                texts[key] = text
                tokens[key] = lexical_tokens(text)
    return texts, tokens


def lexical_score(
    content: str,
    key: str,
    claim_texts: dict[str, str],
    claim_token_map: dict[str, tuple[str, ...]],
    document_frequency: Counter[str],
) -> float:
    query = set(lexical_tokens(content))
    candidate = set(claim_token_map[key])
    shared = query & candidate
    if not shared:
        return 0.0
    # La suma en coma flotante debe recorrer un orden estable. Iterar el set
    # directamente hacía que empates casi exactos pudieran cambiar de C entre
    # procesos con distinto PYTHONHASHSEED.
    weighted = sum(
        1.0 / max(1, document_frequency[token]) ** 0.5
        for token in sorted(shared)
    )
    numbers = set(re.findall(r"\d+(?:[.,]\d+)?", content))
    claim_numbers = set(re.findall(r"\d+(?:[.,]\d+)?", claim_texts[key]))
    if numbers:
        weighted += 2.0 * len(numbers & claim_numbers)
    return weighted / max(1.0, len(query) ** 0.5)


def best_claims(
    content: str,
    candidates: tuple[str, ...],
    claim_texts: dict[str, str],
    claim_token_map: dict[str, tuple[str, ...]],
    document_frequency: Counter[str],
) -> tuple[str, ...]:
    ranked = sorted(
        (
            (
                lexical_score(
                    content, key, claim_texts, claim_token_map,
                    document_frequency,
                ),
                key,
            )
            for key in candidates if key in claim_texts
        ),
        reverse=True,
    )
    top = ranked[0][0] if ranked else 0.0
    return tuple(
        key for value_score, key in ranked[:5]
        if value_score > 0 and value_score >= top * 0.95
    )[:3]


def split_sentences(text: str) -> list[str]:
    """Segmenta sin cortar abreviaturas bibliográficas o taxonómicas."""
    protected_dot = "\ue000"
    protected = ABBREVIATION.sub(
        lambda match: match.group(0).replace(".", protected_dot), text,
    )
    return [
        piece.replace(protected_dot, ".").strip()
        for piece in SENTENCE_BOUNDARY.split(protected)
        if piece.strip()
    ]


def narrative_blocks(path: Path) -> list[tuple[int, int, str, str]]:
    """Devuelve (inicio, fin, clase, texto) para párrafos y aristas."""
    blocks: list[tuple[int, int, str, str]] = []
    paragraph: list[str] = []
    start = 0
    in_code = False

    def flush(end: int) -> None:
        nonlocal paragraph, start
        if paragraph:
            blocks.append((start, end, "prosa", normalized_content(" ".join(paragraph))))
            paragraph = []

    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        text = raw.strip()
        if text.startswith("```"):
            flush(line_number - 1)
            in_code = not in_code
            continue
        if in_code:
            if text:
                blocks.append((line_number, line_number, "arista", text))
            continue
        if (
            not text
            or text.startswith(("#", "<!--", "---", "|", ">"))
        ):
            flush(line_number - 1)
            continue
        if not paragraph:
            start = line_number
        paragraph.append(text)
    flush(len(path.read_text(encoding="utf-8").splitlines()))
    return blocks


def narrative_segments() -> list[Segment]:
    claim_texts, claim_token_map = claim_catalog()
    document_frequency = Counter(
        token for tokens in claim_token_map.values() for token in set(tokens)
    )
    segments: list[Segment] = []
    for path in sorted((ROOT / "docs" / "secciones").glob("*.md")):
        if not SCIENTIFIC_TEMPLATES.fullmatch(path.name):
            continue
        relative = path.relative_to(ROOT).as_posix()
        section = path.name[:3]
        section_path = ROOT / "data" / "afirmaciones" / f"{section}.csv"
        section_candidates: tuple[str, ...] = ()
        if section_path.exists():
            with section_path.open(encoding="utf-8-sig", newline="") as handle:
                section_candidates = tuple(row["#"] for row in csv.DictReader(handle))
        for start, end, kind, block in narrative_blocks(path):
            if any(block.startswith(prefix) for prefix in EDITORIAL_PREFIXES):
                continue
            if kind == "arista":
                pieces = [block]
            else:
                pieces = split_sentences(block)
            for ordinal, piece in enumerate(pieces, 1):
                if kind == "prosa" and editorial_sentence(piece):
                    continue
                if kind == "arista" and editorial_edge(piece):
                    # Rótulo/nota de alcance del diagrama, no una arista ni
                    # una proposición científica que deba fingir una C propia.
                    continue
                own_refs = claim_refs(piece)
                if own_refs:
                    refs = own_refs
                    method = "cita_en_segmento"
                elif kind == "prosa":
                    # La semejanza léxica se calcula sólo como diagnóstico.
                    # No se promueve a correspondencia, no se serializa como
                    # C y nunca recibe estado REVISADA.
                    block_refs = claim_refs(block)
                    suggestions = best_claims(
                        piece, block_refs, claim_texts, claim_token_map,
                        document_frequency,
                    )
                    if not suggestions:
                        suggestions = best_claims(
                            piece, section_candidates, claim_texts,
                            claim_token_map, document_frequency,
                        )
                    refs = ()
                    method = "sugerencia_no_revisada" if suggestions else "SIN_TRAZABILIDAD"
                else:
                    refs = ()
                    method = "SIN_TRAZABILIDAD"
                locator = f"L{start}" if start == end else f"L{start}-L{end}"
                if len(pieces) > 1:
                    locator += f"; oración {ordinal}"
                segments.append(Segment(kind, relative, locator, "n/a", piece, refs, method))
    return segments


def table_cells() -> list[TableCell]:
    """Inventaría todas las celdas sustantivas de tablas summary/node.

    La primera columna y las columnas de identidad se usan solamente para
    contextualizar el valor. Las columnas de metadatos/citas se excluyen. El
    hash canónico se calcula sobre el valor de celda normalizado, no sobre el
    contexto de fila.
    """
    index = json.loads((ROOT / "data" / "table_index.json").read_text(encoding="utf-8"))
    cells: list[TableCell] = []
    for entry in index["tables"]:
        if entry["category"] not in {"summary", "node"}:
            continue
        relative = entry["csv_path"]
        with (ROOT / relative).open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader)
            for row_number, row in enumerate(reader, 2):
                identity_parts = []
                for column_number, value in enumerate(row):
                    column = normalized_content(header[column_number]).casefold()
                    if column_number == 0 or column in IDENTITY_COLUMNS:
                        content = normalized_content(value)
                        if content.casefold() not in EMPTY_VALUES and not claim_refs(content):
                            identity_parts.append(f"{header[column_number]}={content}")
                identity = " | ".join(identity_parts)
                for column_number, value in enumerate(row):
                    column = normalized_content(header[column_number])
                    column_key = column.casefold()
                    if METADATA_COLUMNS.fullmatch(column_key):
                        continue
                    if column_number == 0 or column_key in IDENTITY_COLUMNS:
                        continue
                    raw_content = normalized_content(value)
                    content = (
                        f"{identity} | {column}={raw_content}" if identity
                        else f"{column}={raw_content}"
                    )
                    if raw_content.casefold() in EMPTY_VALUES:
                        continue
                    cells.append(TableCell(
                        relative, row_number, column, raw_content, content,
                        claim_refs(raw_content),
                    ))
    return cells


def load_cell_manifest() -> tuple[
    dict[tuple[str, int, str, str], dict[str, str]], list[str]
]:
    entries: dict[tuple[str, int, str, str], dict[str, str]] = {}
    errors: list[str] = []
    if not CELL_MANIFEST.exists():
        return entries, [
            f"Falta manifiesto canónico: {CELL_MANIFEST.relative_to(ROOT)}"
        ]
    with CELL_MANIFEST.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != CELL_MANIFEST_HEADER:
            errors.append(
                "Encabezado inesperado en manifiesto de celdas: "
                f"{reader.fieldnames!r}; esperado {CELL_MANIFEST_HEADER!r}"
            )
            return entries, errors
        for line_number, row in enumerate(reader, 2):
            try:
                row_number = int(row["fila"])
            except ValueError:
                errors.append(f"Manifiesto línea {line_number}: fila no entera")
                continue
            key = (
                row["csv_path"], row_number, row["columna"],
                row["contenido_sha256"],
            )
            if key in entries:
                errors.append(
                    f"Manifiesto línea {line_number}: clave duplicada {key!r}"
                )
                continue
            entries[key] = row
    return entries, errors


def cell_manifest_errors(
    cells: list[TableCell],
    manifest: dict[tuple[str, int, str, str], dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    claim_keys = set(claim_catalog()[0])
    inventory_keys = {cell.manifest_key for cell in cells}
    if len(inventory_keys) != len(cells):
        errors.append("El inventario produjo claves de celda duplicadas")
    for cell in cells:
        entry = manifest.get(cell.manifest_key)
        location = f"{cell.path}:fila {cell.row_number}:{cell.column}"
        if entry is None:
            errors.append(
                f"Celda ausente del manifiesto: {location} "
                f"sha256={cell.content_sha256}"
            )
            continue
        if entry["contenido"] != cell.raw_content:
            errors.append(f"Contenido no coincide con el manifiesto: {location}")
        refs = claim_refs(entry["afirmaciones"])
        unknown = sorted(set(refs) - claim_keys)
        if unknown:
            errors.append(
                f"C inexistente en manifiesto: {location}: {', '.join(unknown)}"
            )
        status = entry["estado_revision"]
        if status not in {"REVISADA", "SIN_TRAZABILIDAD"}:
            errors.append(f"Estado inválido en manifiesto: {location}: {status!r}")
        if status == "REVISADA" and not refs:
            errors.append(f"Celda REVISADA sin C: {location}")
        if status == "SIN_TRAZABILIDAD" and refs:
            errors.append(f"Celda SIN_TRAZABILIDAD con C: {location}")
        if cell.own_refs:
            if not set(cell.own_refs).issubset(refs):
                errors.append(
                    f"La C escrita en la celda falta en el manifiesto: "
                    f"{location}; celda={cell.own_refs!r}, manifiesto={refs!r}"
                )
            allowed_bases = {
                "cita_en_celda", "cita_en_celda+manifiesto_explicito",
            }
            if entry["base_semantica"] not in allowed_bases:
                errors.append(
                    f"Celda con C explícita sin base cita_en_celda: {location}"
                )
        elif status == "REVISADA" and entry["base_semantica"] in {
            "", "n/a", "cita_en_celda", "sugerencia_lexica",
        }:
            errors.append(
                f"Mapeo explícito sin base semántica válida: {location}"
            )
        if not entry["nota_adjudicacion"].strip():
            errors.append(f"Adjudicación sin nota: {location}")
    stale = sorted(set(manifest) - inventory_keys)
    for path, row_number, column, digest in stale:
        errors.append(
            "Entrada obsoleta/no inventariada en manifiesto: "
            f"{path}:fila {row_number}:{column} sha256={digest}"
        )
    return errors


def table_segments(
    cells: list[TableCell] | None = None,
    manifest: dict[tuple[str, int, str, str], dict[str, str]] | None = None,
) -> list[Segment]:
    cells = table_cells() if cells is None else cells
    if manifest is None:
        manifest, _ = load_cell_manifest()
    segments: list[Segment] = []
    for cell in cells:
        entry = manifest.get(cell.manifest_key)
        refs: tuple[str, ...] = ()
        method = "SIN_TRAZABILIDAD"
        if entry is not None and entry["estado_revision"] == "REVISADA":
            refs = claim_refs(entry["afirmaciones"])
            if refs:
                method = (
                    "cita_en_celda"
                    if cell.own_refs and refs == cell.own_refs
                    else "cita_en_celda_y_manifiesto_explicito"
                    if cell.own_refs
                    else "manifiesto_explicito_celda"
                )
        segments.append(Segment(
            "celda", cell.path, f"fila {cell.row_number}", cell.column,
            cell.contextual_content, refs, method, cell.content_sha256,
        ))
    return segments


def rows(segments: list[Segment] | None = None) -> list[list[str]]:
    segments = (
        narrative_segments() + table_segments()
        if segments is None else segments
    )
    result: list[list[str]] = []
    for number, segment in enumerate(segments, 1):
        result.append([
            f"TC-{number:05d}", segment.kind, segment.path, segment.locator,
            segment.column, segment.content,
            # La matriz serializa el contexto canónico completo de la celda
            # (identidad de fila + columna + valor), no solo el valor aislado
            # que usa el manifiesto para detectar ediciones. La huella debe
            # corresponder exactamente al campo ``contenido`` serializado.
            hashlib.sha256(
                (segment.content + "\n").encode("utf-8")
            ).hexdigest(),
            "; ".join(segment.claims) if segment.claims else "n/a",
            segment.method if segment.claims else "SIN_TRAZABILIDAD",
            "REVISADA" if segment.claims else "SIN_TRAZABILIDAD",
        ])
    return result


def csv_bytes(segments: list[Segment] | None = None) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, quoting=csv.QUOTE_ALL, lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows(segments))
    return buffer.getvalue().encode("utf-8")


def validate_payload(payload: bytes) -> list[str]:
    errors: list[str] = []
    decoded = payload.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))
    seen_claims: set[str] = set()
    missing = []
    for row in reader:
        refs = claim_refs(row["afirmaciones"])
        seen_claims.update(refs)
        if "lexic" in row["metodo_mapeo"].casefold():
            errors.append(
                "Un método léxico fue serializado como prueba: "
                f"{row['ruta']}:{row['localizador']}"
            )
        if "C-681" in refs:
            errors.append(
                "El tombstone registral C-681 no puede sostener segmentos: "
                f"{row['ruta']}:{row['localizador']}"
            )
        if not refs:
            missing.append(f"{row['ruta']}:{row['localizador']}:{row['tipo']}")
        if row["tipo"] == "prosa":
            content = row["contenido"].strip()
            if SPURIOUS_SENTENCE_START.match(content):
                errors.append(
                    "Fragmento espurio por abreviatura al inicio: "
                    f"{row['ruta']}:{row['localizador']}: {content[:80]!r}"
                )
            if content.count("]") > content.count("["):
                errors.append(
                    "Fragmento espurio de corchete: "
                    f"{row['ruta']}:{row['localizador']}: {content[:80]!r}"
                )
    if missing:
        errors.append(
            f"{len(missing)} segmentos sustantivos carecen de C: "
            + "; ".join(missing[:20])
        )
    return errors


def internal_invariant_errors() -> list[str]:
    """Pruebas pequeñas que protegen bugs confirmados por revisión."""
    errors: list[str] = []
    sample_texts = {"C-001": "alpha", "C-002": "alpha"}
    sample_tokens = {key: lexical_tokens(value) for key, value in sample_texts.items()}
    ranked = best_claims(
        "alpha", ("C-001", "C-002"), sample_texts, sample_tokens,
        Counter({"alpha": 2}),
    )
    if ranked != ("C-002", "C-001") or len(ranked) != len(set(ranked)):
        errors.append(
            f"best_claims produjo orden/duplicados inesperados: {ranked!r}"
        )
    sample = (
        "Resultado [S12 fig. 3; S13 suppl. p. 4]. Después. "
        "Smith et al. 2020 informó otro resultado. Buchnera sp. APS. Fin."
    )
    pieces = split_sentences(sample)
    expected = [
        "Resultado [S12 fig. 3; S13 suppl. p. 4].",
        "Después.",
        "Smith et al. 2020 informó otro resultado.",
        "Buchnera sp. APS.",
        "Fin.",
    ]
    if pieces != expected:
        errors.append(f"Segmentación de abreviaturas inesperada: {pieces!r}")
    if any(
        SPURIOUS_SENTENCE_START.match(piece)
        or piece.count("]") > piece.count("[")
        for piece in pieces
    ):
        errors.append(f"La prueba de segmentación dejó un fragmento espurio: {pieces!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    cells = table_cells()
    manifest, errors = load_cell_manifest()
    errors.extend(cell_manifest_errors(cells, manifest))
    errors.extend(internal_invariant_errors())
    segments = narrative_segments() + table_segments(cells, manifest)
    payload = csv_bytes(segments)
    errors.extend(validate_payload(payload))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != payload:
            print(f"Trazabilidad de contenido desactualizada: {OUTPUT.relative_to(ROOT)}", file=sys.stderr)
            return 1
        print(f"Trazabilidad exacta: {len(segments)} segmentos.")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(payload)
    print(f"Trazabilidad escrita: {OUTPUT.relative_to(ROOT)} ({len(segments)} segmentos).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
