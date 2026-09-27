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
import string
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
ABBREVIATION = re.compile(
    r"\b(?:figs?|suppl|pp?|spp?|cf)\.|\bet\s+al\.", re.IGNORECASE,
)
URL_TOKEN = re.compile(r"https?://[^\s<>\[\]«»\"“”]+", re.IGNORECASE)
CITATION_START = re.compile(r"\[\s*(?:C-\d{3,5}|S\d{2,3}|BN-\d{3})\b")
ITALIC_INITIAL_TERM = re.compile(
    r"(?<![\w*_])(?:\*[A-Z]\.\s+[a-z][a-z-]+\*|_[A-Z]\.\s+[a-z][a-z-]+_)(?![\w*_])"
)
AMBIGUOUS_INITIAL = re.compile(r"(?<![^\W_])[A-Z]\.(?=\s+[a-záéíóúñ][a-záéíóúñ-]+)")
TERMINALS = ".!?…"
TERMINAL_CLOSERS = '\"\u201d\u00bb\u2019\u203a\')]}*_`'
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
EDITORIAL_SENTENCES = frozenset({
    # Reglas contractuales del encargo: describen cómo se construye y lee el
    # corpus, no sostienen una proposición científica sobre sus objetos.
    "No se inventan nombres, fechas, taxones, relaciones ni cifras.",
    "Una cifra se transcribe únicamente cuando una fuente recuperada en esta "
    "sesión la publica con su unidad, denominador y localizador; no se estima, "
    "interpola, redondea ni sustituye por un «orden de magnitud razonable».",
    "Si la magnitud pedida no tiene un valor publicado localizado, la respuesta "
    "literal es **«no hay valor publicado»**, seguida del alcance de la búsqueda "
    "y de la razón por la cual las fuentes recuperadas no proporcionan esa magnitud.",
    "Un hueco declarado y reproducible es un resultado utilizable; una cifra "
    "plausible sin fuente no lo es.",
    "Solo se citan trabajos recuperados en la sesión y enlazados en el Apéndice A.",
    "No se cita de memoria ni se reconstruye un DOI: cuando el DOI no pudo "
    "resolverse contra el recurso recuperado, se consigna **«DOI no verificado»** "
    "y se conserva la URL efectivamente recuperada.",
    "Un trabajo relevante conocido pero no recuperado no entra en la bibliografía; "
    "se registra, si corresponde, como **«trabajo conocido no recuperado»** dentro "
    "de un hueco reproducible.",
    "Entre una referencia que no resuelve y un hueco declarado se conserva el hueco.",
    "Estas reglas son contractuales, no prueba retroactiva de que cada recuperación "
    "se haya ejecutado: la evidencia de recuperación debe seguir resolviendo a una "
    "fuente, un pasaje y un localizador concretos.",
    "En los apéndices, `n/a` significa exclusivamente **no aplicable**.",
    "Cuando el campo sí aplica pero la fuente recuperada no aporta el dato, se "
    "escribe literalmente **«no consta en la fuente recuperada»**; expresiones como "
    "«duración no localizada», «origen no localizado» o «sin unidad publicada» no "
    "sustituyen esa fórmula.",
    "La distinción impide convertir una ausencia de evidencia en un valor o en una inferencia.",
    "En su primera glosa se conservan juntos el término español y el inglés: "
    "atracción de ramas largas (*long-branch attraction*), reloj molecular relajado "
    "bayesiano (*Bayesian relaxed molecular clock*) y transferencia génica "
    "endosimbiótica (*endosymbiotic gene transfer*, EGT).",
    "Las menciones posteriores pueden usar la forma ya definida sin volver a traducirla.",
    # Notas editoriales de alcance, referencias cruzadas y estructura del corpus.
    "La comparación nominal conservada para Alphaproteobacteria no debe confundirse "
    "con una monografía interna del clado.",
    "Ese componente queda declarado como hueco, no se rellena extrapolando desde "
    "Iodidimonadales. [BN-114]",
    "Los falsadores nominales de H18–H21 se conservan exclusivamente en el Apéndice E.",
    "Los falsadores de H12–H22 no se reproducen en este capítulo: su registro "
    "nominal y versionado está exclusivamente en el Apéndice E.",
    "Cada fila de la tabla distingue el material observado de su adjudicación al "
    "nodo y de la incertidumbre corona–tallo.",
    "El censo termina exactamente en Metazoa, que es el extremo solicitado del "
    "corredor Eukaryota → Holozoa → Metazoa.",
    "Las diecinueve fichas siguientes están ordenadas desde asociaciones externas "
    "hasta dependencias heredadas o anidadas.",
    "Cada párrafo empieza por el mecanismo y remite a una sola fila de la tabla; "
    "los campos científicos completos no se duplican en dos redacciones.",
    "Los pares que el encargo escribió con barra o con ≈ se tratan aquí como "
    "conjeturas de trabajo, no como datos.",
    "La barra no crea sinonimia: la tabla 57 clasifica cada par como sinonimia "
    "aproximada, preferencia de autor o conflicto real de contenido.",
})
EMPTY_VALUES = {"", "n/a", "—", "-"}
METADATA_COLUMNS = re.compile(
    r"^(?:#(?: de la fila del registro.*)?|n[.º°o]*|"
    r"fila(?:s)?(?: y fuentes?| por celda)?|"
    r"filas y fuente local|evidencia o hueco|"
    r"fuente(?:s)?(?: y localizador)?|clave|"
    r"referencias?|citas?|marca|id(?:entificador)?|afirmaciones?|"
    r"id_vista|id_afirmacion_canonica|ruta_canonica|sha256_fila_canonica|"
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
    normalized = normalized_content(text)
    if normalized in EDITORIAL_SENTENCES:
        return True
    stripped = normalized.strip(" -*_`[]()")
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


def inline_link_end(text: str, start: int) -> int | None:
    """Fin de destino/título inline nominal; no parser Markdown general.

    CommonMark 0.31.2 §6.3: un paréntesis balanceado con prosa arbitraria
    no basta. Destino desnudo, destino angular y título tienen delimitadores
    diferentes. Una forma que no se reconoce queda inválida, no protegida.
    """
    if start >= len(text) or text[start] != "(":
        return None

    def escaped(offset: int) -> bool:
        return (text[offset] == "\\" and offset + 1 < len(text)
                and text[offset + 1] in string.punctuation)

    def whitespace_end(offset: int) -> int | None:
        line_endings = 0
        while offset < len(text) and text[offset] in " \t\r\n":
            if text[offset] in "\r\n":
                line_endings += 1
                if text[offset:offset + 2] == "\r\n":
                    offset += 1
            offset += 1
        return offset if line_endings <= 1 else None

    def destination_end(offset: int) -> int | None:
        if offset >= len(text):
            return None
        if text[offset] == "<":
            cursor = offset + 1
            while cursor < len(text):
                if escaped(cursor):
                    cursor += 2
                    continue
                if text[cursor] == ">":
                    return cursor + 1
                if text[cursor] in "<\r\n":
                    return None
                cursor += 1
            return None
        cursor, depth = offset, 0
        while cursor < len(text):
            character = text[cursor]
            if escaped(cursor):
                cursor += 2
                continue
            if ord(character) <= 32 or ord(character) == 127:
                break
            if character == "(":
                depth += 1
            elif character == ")":
                if depth == 0:
                    break
                depth -= 1
            cursor += 1
        return cursor if cursor > offset and depth == 0 else None

    def title_end(offset: int) -> int | None:
        if offset >= len(text) or text[offset] not in "\"'(":
            return None
        opening = text[offset]
        closing = ")" if opening == "(" else opening
        cursor = offset + 1
        while cursor < len(text):
            if escaped(cursor):
                cursor += 2
                continue
            if text[cursor] == closing:
                title_lines = text[offset + 1:cursor].replace("\r\n", "\n").replace("\r", "\n")
                if re.search(r"\n[ \t]*\n", title_lines):
                    return None
                return cursor + 1
            if opening == "(" and text[cursor] == "(":
                return None
            cursor += 1
        return None

    def close_after(offset: int) -> int | None:
        end = whitespace_end(offset)
        return end + 1 if end is not None and end < len(text) and text[end] == ")" else None

    beginning = whitespace_end(start + 1)
    if beginning is None or beginning >= len(text):
        return None
    if text[beginning] == ")":
        return beginning + 1
    destination = destination_end(beginning)
    if destination is not None:
        closed = close_after(destination)
        if closed is not None:
            return closed
        title_start = whitespace_end(destination)
        if title_start is not None and title_start > destination:
            title = title_end(title_start)
            if title is not None:
                return close_after(title)
    # Título sin destino, cuando no se pudo leer como destino completo.
    title = title_end(beginning)
    return close_after(title) if title is not None else None


def citation_end(text: str, start: int) -> int | None:
    """Fin excluido de una cita nominal entre corchetes, incluidos anidados.

    No consume cualquier corchete: [SIN FUENTE] o prosa entre corchetes no
    son citas pospuestas y no deben trasladarse a la oración precedente.
    """
    if not CITATION_START.match(text, start):
        return None
    depth = 0
    for offset in range(start, len(text)):
        if text[offset] == "[":
            depth += 1
        elif text[offset] == "]":
            depth -= 1
            if depth == 0:
                end = offset + 1
                if end < len(text) and text[end] == "(":
                    return inline_link_end(text, end)
                return end
    return None


def sentence_masks(text: str) -> tuple[set[int], set[int]]:
    """Puntuación léxica protegida; no clasifica proposiciones como editoriales."""
    abbreviations = {
        offset for match in ABBREVIATION.finditer(text)
        for offset in range(match.start(), match.end()) if text[offset] == "."
    }
    protected: set[int] = set()
    for match in ITALIC_INITIAL_TERM.finditer(text):
        # Token de dos componentes explícitamente encerrado en cursiva, como
        # *S. rosetta*. No extender a «modelo B. este…» sin ese delimitador.
        protected.update(offset for offset in range(match.start(), match.end()) if text[offset] == ".")
    for match in URL_TOKEN.finditer(text):
        # El signo terminal de prosa no es parte de la URL. Sus puntos
        # interiores (dominio/ruta), decimales y query permanecen intactos.
        # Retirar también los cierres externos: «https://example.org.’»
        # no debe proteger el punto por llevar una comilla o formato detrás.
        # Sólo se recorta el sufijo; apóstrofos, guiones bajos y otros signos
        # interiores de ruta/query siguen protegidos, sin reescribir la URL.
        token = match.group().rstrip(TERMINALS + TERMINAL_CLOSERS + ",;:")
        protected.update(range(match.start(), match.start() + len(token)))
    for offset, character in enumerate(text):
        if character == "[":
            end = citation_end(text, offset)
            if end is not None:
                protected.update(range(offset, end))
    return abbreviations, protected


def sentence_spans(text: str) -> list[tuple[int, int]]:
    """Offsets Unicode [inicio, fin) sobre el texto recibido, sin reescribirlo.

    Una cita después del punto se adjunta solo a la oración precedente.
    La siguiente oración se separa también si empieza por minúscula. Los
    spans no son offsets del fichero cuando el llamador normalizó el párrafo;
    no cambian el esquema persistente de la matriz de trazabilidad. Una inicial
    sin delimitador puede ser abreviatura o fin: se conserva el corte provisional
    y sentence_boundary_diagnostics exige su adjudicación, nunca lo aprueba.
    """
    abbreviations, protected = sentence_masks(text)

    spans: list[tuple[int, int]] = []
    start = 0
    offset = 0
    while offset < len(text):
        if text[offset] not in TERMINALS or offset in protected:
            offset += 1
            continue
        end = offset + 1
        while end < len(text) and text[end] in TERMINALS + TERMINAL_CLOSERS:
            end += 1
        had_citation = False
        while True:
            candidate = end
            while candidate < len(text) and text[candidate].isspace():
                candidate += 1
            citation = citation_end(text, candidate)
            if citation is None:
                break
            had_citation = True
            end = citation
            # También admite «Resultado. [C-001]. Siguiente…» sin dejar un
            # segmento de puntuación que oculte la siguiente proposición.
            while end < len(text) and text[end] in TERMINALS + TERMINAL_CLOSERS:
                end += 1
        if offset in abbreviations and not had_citation:
            offset += 1
            continue
        if end < len(text) and not text[end].isspace() and not had_citation:
            offset += 1
            continue
        while start < end and text[start].isspace():
            start += 1
        if start < end:
            spans.append((start, end))
        start = end
        offset = end
    while start < len(text) and text[start].isspace():
        start += 1
    end = len(text)
    while end > start and text[end - 1].isspace():
        end -= 1
    if start < end:
        spans.append((start, end))
    return spans


def split_sentences(text: str) -> list[str]:
    """Conserva citas/abreviaturas y no presta C entre oraciones."""
    return [text[start:end] for start, end in sentence_spans(text)]


def sentence_boundary_diagnostics(text: str) -> list[dict[str, object]]:
    """Conserva lecturas de inicial o abreviatura terminal, sin adjudicarlas."""
    _, protected = sentence_masks(text)
    spans = sentence_spans(text)
    diagnostics: list[dict[str, object]] = []
    for match in AMBIGUOUS_INITIAL.finditer(text):
        punctuation = match.end() - 1
        if punctuation in protected:
            continue
        for index, (start, end) in enumerate(spans[:-1]):
            if start <= punctuation < end and end == punctuation + 1:
                following = spans[index + 1]
                diagnostics.append({
                    "razon": "AMBIGUA_INICIAL_EPITETO",
                    "offset_punto": punctuation,
                    "literal": text[match.start():following[1]],
                    "lectura_corte": [(start, end), following],
                    "lectura_abreviatura": [(start, following[1])],
                })
                break
    # Una abreviatura seguida de otro contenido separado puede terminar una
    # oración. No elegir por mayúscula, formato, número ni C en el resto.
    # Se preserva la segmentación provisional y ambas lecturas; main bloquea.
    for match in ABBREVIATION.finditer(text):
        punctuation = match.end() - 1
        if punctuation in protected:
            continue
        following_start = match.end()
        while following_start < len(text) and text[following_start] in TERMINAL_CLOSERS:
            following_start += 1
        cut_end = following_start
        while following_start < len(text) and text[following_start].isspace():
            following_start += 1
        if following_start == cut_end or following_start == len(text):
            continue
        for start, end in spans:
            if start <= punctuation < following_start < end:
                diagnostics.append({
                    "razon": "AMBIGUA_ABREVIATURA_TERMINAL",
                    "offset_punto": punctuation,
                    "literal": text[match.start():end],
                    "lectura_corte": [(start, cut_end), (following_start, end)],
                    "lectura_abreviatura": [(start, end)],
                })
                break
    return diagnostics


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


def narrative_ambiguities() -> list[dict[str, object]]:
    """Diagnóstico nominal de fronteras pendientes, sin nueva exención de C."""
    result: list[dict[str, object]] = []
    for path in sorted((ROOT / "docs" / "secciones").glob("*.md")):
        if not SCIENTIFIC_TEMPLATES.fullmatch(path.name):
            continue
        for start, end, kind, block in narrative_blocks(path):
            if kind != "prosa":
                continue
            diagnostics = sentence_boundary_diagnostics(block)
            if diagnostics:
                result.append({
                    "ruta": path.relative_to(ROOT).as_posix(),
                    "localizador": f"L{start}" if start == end else f"L{start}-L{end}",
                    "texto": block,
                    "sha256_texto_lf": hashlib.sha256((block + "\n").encode()).hexdigest(),
                    "base_offsets": "Unicode del bloque normalizado, no del archivo",
                    "fronteras": diagnostics,
                })
    return result


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
        if (
            status == "SIN_TRAZABILIDAD"
            and entry["base_semantica"] != "BN_literal_o_límite_sin_C"
        ):
            errors.append(
                f"Celda SIN_TRAZABILIDAD sin base BN/límite explícita: {location}"
            )
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
            for match in CITATION_START.finditer(content):
                if citation_end(content, match.start()) is None:
                    errors.append(
                        "Cita nominal o enlace sin cierre o con sintaxis inválida: "
                        f"{row['ruta']}:{row['localizador']}: offset {match.start()}"
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
    if not all(editorial_sentence(text) for text in EDITORIAL_SENTENCES):
        errors.append("Una oración editorial contractual dejó de ser reconocida")
    scientific_mutations = (
        "No se observaron taxones ni relaciones en el experimento.",
        "Cada fila de la tabla demuestra una relación filogenética.",
        "La barra no crea monofilia en el clado publicado.",
        "La reducción secundaria de la cadena respiratoria mitocondrial bajo "
        "anaerobiosis es el mecanismo que ilustra Blastocystis.",
    )
    misclassified = tuple(
        text for text in scientific_mutations if editorial_sentence(text)
    )
    if misclassified:
        errors.append(
            "Oraciones científicas clasificadas como editoriales: "
            f"{misclassified!r}"
        )
    unreviewed_cell = Segment(
        "celda", "data/tablas/prueba.csv", "fila 3", "valor",
        "valor no localizado", (), "SIN_TRAZABILIDAD",
    )
    scientific_prose = Segment(
        "prosa", "docs/secciones/prueba.md", "L1", "n/a",
        "Una afirmación científica sin C.", (),
        "manifiesto_explicito_limite_sin_C",
    )
    for sample_segment in (unreviewed_cell, scientific_prose):
        if not validate_payload(csv_bytes([sample_segment])):
            errors.append(
                "La traza aceptó un segmento sin C: "
                f"{sample_segment.kind}:{sample_segment.locator}"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    cells = table_cells()
    manifest, errors = load_cell_manifest()
    errors.extend(cell_manifest_errors(cells, manifest))
    errors.extend(internal_invariant_errors())
    for ambiguity in narrative_ambiguities():
        errors.append(
            "Frontera de oración ambigua, requiere adjudicación de spans: "
            f"{ambiguity['ruta']}:{ambiguity['localizador']} "
            f"({len(ambiguity['fronteras'])} fronteras)"
        )
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
