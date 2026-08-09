#!/usr/bin/env python3
"""Puerta determinista de la auditoría científica integral.

La puerta comprueba cobertura, linaje, trazabilidad y cierre editorial. No
consulta la red ni pretende inferir si un artículo dice algo: esa equivalencia
queda acreditada en las matrices revisadas y protegida por huellas SHA-256.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CUTOFF = "2026-08-08"
PROMPT_PATH = "docs/C01-PROMPT-INVESTIGACION.md"
PROMPT_SHA256 = "5245393c50c7a1620ef81f42cdfd92c5632b9218a153a0e0ad2d560a3314ffb3"
ARCHIVE_PATH = "archive/maestro_provisional_v5_pre_migracion.md"
ARCHIVE_SHA256 = "24c5495d85641d03a24c084a51a9b0b5887edf60d6698f94f19775c09c28cfe3"
BASELINE_CLAIM_COUNT = 1840
BASELINE_SOURCE_COUNT = 525
BASELINE_BN_COUNT = 106
BASELINE_ACTIVE_BN_COUNT = 68
BASELINE_CLAIM_KEYSET_SHA256 = "7a1e34cf64103790fc5d7a2de4cc8572f2ce47bc6bc5f0ac5d0457487bd9295e"
BASELINE_SOURCE_KEYSET_SHA256 = "060c5da88ab35dbbf0c7e075d5b4a4859e60671f24f61f32f7e43705d7c9001a"
BASELINE_BN_KEYSET_SHA256 = "92b08c8b7d79974f4a832f67658f17872b34671832c1d7efbff9d5463167b1d2"
BASELINE_ACTIVE_BN_KEYSET_SHA256 = "7bc85b6dccd5ab2528fd671c6bf49277c4739b69f59fbf293a5e68ed2e36147d"
BASELINE_CLAIM_AUDIT_SHA256 = "35cb63c30c32a8eeb86f053226f7b49f7da8bb5d7ebd9706f8008d0399cdffd2"
BASELINE_SOURCE_AUDIT_SHA256 = "35debf215af3681c63535060f9cc3ff07b4b17283c7bb50f2852394ba3973c5c"
BASELINE_REQUIREMENT_AUDIT_SHA256 = "506b24d365410826099f6f5cff433bbf865f4eacb880c43b9ea2acdba0217680"
BASELINE_SEARCH_AUDIT_SHA256 = "29d14eaac34cc7ba8e56150c7eb8a48ab6a1812993351aa1d39a20fd7b13964a"
BASELINE_CLAIM_SUMMARY_SHA256 = "f1f8b1961bbf1fb141408a3023f937d37c53ed6ebb6df390cfcde68fe338cfbb"
BASELINE_CLAIM_CORPUS_SHA256 = "ed8685528ddd5051f333327fb649f5e2657e36c95190cad08b0a805fcc7fd579"
BASELINE_SOURCE_CORPUS_SHA256 = "a1d29920d13d1c308c01797c9f3e6c59322ec628eb312f05973b9a66b71f5cf2"
FROZEN_FINDINGS_MANIFEST_SHA256 = "2d2c2537edbe86f3f19a548b5d6bcbfddca8107cd25c7a674f1c1c68c3bd0661"
SNAPSHOT_HEAD = "a3ce4e6685a4e287a5fbd478d4657e475e10de3c"
SNAPSHOT_EXTERNAL_PATH = "/tmp/corredor-eukaryota-auditoria-20260808/"

CLAIM_MATRIX = "docs/auditorias/matriz_afirmaciones_2026-08-08.csv"
SOURCE_MATRIX = "docs/auditorias/matriz_fuentes_2026-08-08.csv"
REQUIREMENT_MATRIX = "docs/auditorias/matriz_requisitos_2026-08-08.csv"
SEARCH_MATRIX = "docs/auditorias/registro_busquedas_2026-08-08.csv"
REPRO_JSON = "docs/auditorias/auditoria_reproducible_2026-08-08.json"
NEGATIVE_HISTORY = "docs/auditorias/revision_busquedas_negativas_2026-08-08.csv"
TABLE_LINEAGE = "data/table_lineage.csv"
KEY_MAP = "docs/auditorias/mapa_claves_inicial_final_2026-08-08.csv"
AUDIT_REPORT = "docs/auditorias/AUDITORIA-COMPLETA-2026-08-08.md"
SECOND_REVIEW = "docs/auditorias/segunda_revision_2026-08-08.csv"
CONTENT_TRACE = "docs/auditorias/matriz_trazabilidad_contenido_2026-08-08.csv"

CLAIM_MATRIX_COLUMNS = [
    "clave_inicial", "seccion_inicial", "claves_finales", "resultado",
    "estado_inicial", "atomicidad", "equivalencia_spo", "soporte",
    "localizador", "fidelidad_epistemica", "etiquetas",
    "trazabilidad_apendices", "severidad_inicial", "accion_inicial",
    "accion_final", "evidencia_auditoria_inicial", "evidencia_final",
    "estado_hallazgo", "huella_inicial_sha256",
    "huella_corpus_inicial_sha256", "huella_final_sha256",
]
SOURCE_MATRIX_COLUMNS = [
    "clave_inicial", "clave_final", "metadatos_iniciales",
    "metadatos_finales", "identidad_bibliografica", "tipo_inicial",
    "tipo_final", "estado_editorial", "acceso", "doi_url_inicial",
    "doi_url_final", "uso_inicial", "uso_final", "soporte_unico_inicial",
    "soporte_unico_final", "correcciones_retractaciones",
    "veredicto_inicial", "veredicto", "severidad_inicial",
    "accion_inicial", "accion_final", "evidencia_auditoria_inicial",
    "evidencia_final", "estado_hallazgo", "fecha_verificacion",
    "huella_inicial_sha256", "huella_corpus_inicial_sha256",
    "huella_final_sha256",
]
REQUIREMENT_MATRIX_COLUMNS = [
    "id_requisito", "seccion_prompt", "ancla", "requisito_literal",
    "estado_inicial", "estado_final", "afirmaciones_iniciales",
    "afirmaciones", "tablas_iniciales", "tablas", "fuentes_iniciales",
    "fuentes", "busqueda_negativa_inicial", "busqueda_negativa",
    "accion_inicial", "accion", "evidencia_inicial", "evidencia",
    "huella_inicial_sha256",
]
SEARCH_MATRIX_COLUMNS = [
    "id_busqueda", "fecha", "bloque", "clave_bn", "prioridad",
    "objetivo", "consulta_exacta", "servicio", "fuentes_evaluadas",
    "resultado", "accion_inicial", "cambio_realizado", "desencadenante",
    "evidencia_final", "estado_registro", "huella_inicial_sha256",
]
SECOND_REVIEW_COLUMNS = [
    "id_revision", "estrato", "clave_matriz", "tipo_revision",
    "seleccion", "resultado", "revisor_independiente",
    "declaracion_independencia", "fecha", "evidencia", "accion",
    "estado_cierre", "huella_objeto_sha256",
]
CONTENT_TRACE_COLUMNS = [
    "id_segmento", "tipo", "ruta", "localizador", "columna", "contenido",
    "sha256_contenido", "afirmaciones", "metodo_mapeo", "estado_revision",
]

FINAL_QUESTIONS = [
    "1. ¿Qué hace estable una asociación inicialmente conflictiva?",
    "2. ¿Cómo cambian los costos y beneficios con el ambiente?",
    "3. ¿Cuándo una dependencia se vuelve heredable?",
    "4. ¿Qué distingue divergencia, transferencia e integración?",
    "5. ¿Cómo puede la misma evidencia apoyar reconstrucciones diferentes?",
    "6. ¿Qué rasgos están observados y cuáles inferidos?",
]
HEX_SHA256 = re.compile(r"[0-9a-f]{64}")
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
EDITORIAL_PLACEHOLDER = re.compile(
    r"(?:\[(?:PROVISIONAL|PENDIENTE|TODO|TBD)\]|"
    r"\b(?:TODO|TBD|PENDIENTE_DE_COMPLETAR|POR_COMPLETAR)\b)"
)

CLAIM_COLUMNS = [
    "#", "Afirmación", "Sujeto", "Predicado", "Objeto", "Atribución",
    "Fuente", "Aceptación", "Fuerza", "Motivo", "Resolución", "Vigencia",
]
CLOSED_PREDICATES = {
    "miembro_de", "grupo_hermano_de", "desciende_de", "diverge_de",
    "grupo_corona_de", "linaje_troncal_de", "posee_rasgo", "adquiere_rasgo",
    "pierde_rasgo", "converge_con", "depreda_a", "es_huesped_de",
    "compite_con", "endosimbiosis_con", "transfiere_gen_a",
    "sinonimo_propuesto_de", "clasificado_como_por", "tiene_edad_estimada",
    "tiene_valor_medido", "propuesto_por", "respaldado_por",
    "cuestionado_por", "incompatible_con",
}
CUSTOM_PREDICATE = re.compile(r"^[a-z0-9_áéíóúñ]+\*$")
CLAIM_REF = re.compile(r"\bC-\d{3,5}\b")
SOURCE_REF = re.compile(r"\bS\d{2,3}\b")
BN_REF = re.compile(r"\bBN-\d{3}\b")
LOCATOR = re.compile(
    r"§|\bp\.?\s*\d|\bpp\.?|fig(?:ura)?\.?|table|tabla|result|resultado|"
    r"abstract|resumen|discussion|discusi[oó]n|supp|supl|m[eé]todo|method|"
    r"l[ií]nea|caption|conclusi[oó]n|t[ií]tulo|extended data|"
    r"\barts?\.|\bFAQ\b|registro|database|metadatos|"
    r"introducci[oó]n|cap[ií]tulo|protocolo|ecuaci[oó]n|appendix|"
    r"ap[eé]ndice|box|recuadro",
    re.IGNORECASE,
)
PROHIBITED_DERIVATIONS = re.compile(
    r"punto medio derivado|punto medio aritm[eé]tico derivado|"
    r"amplitud (?:calculada|derivada)|promedio propio|promedio calculado por "
    r"esta auditor[ií]a|conversi[oó]n propia|calculad[oa] a partir de los "
    r"extremos|valor intermedio construido|resta aritm[eé]tica entre extremos|"
    r"complemento calculado",
    re.IGNORECASE,
)


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    path: str
    row: int
    key: str
    message: str


class AuditContext:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def path(self, relative: str) -> Path:
        return self.root / relative


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def natural_key(value: str) -> tuple[str, int]:
    match = re.fullmatch(r"([^0-9]*)(\d+)", value)
    return (match.group(1), int(match.group(2))) if match else (value, -1)


def keyset_sha256(values: set[str] | list[str]) -> str:
    data = "".join(f"{value}\n" for value in sorted(set(values), key=natural_key))
    return sha256_bytes(data.encode("utf-8"))


def canonical_row_fingerprint(row: dict[str, str]) -> str:
    """Huella de una fila congelada con serialización inequívoca."""
    payload = json.dumps(
        row, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ) + "\n"
    return sha256_bytes(payload.encode("utf-8"))


def aggregate_keyed_fingerprints(items: list[tuple[str, str]]) -> str:
    """Ancla orden, identidad y contenido de un inventario de huellas."""
    payload = "".join(f"{key}\x1f{fingerprint}\n" for key, fingerprint in items)
    return sha256_bytes(payload.encode("utf-8"))


def valid_iso_date(value: str) -> bool:
    if not ISO_DATE.fullmatch(value):
        return False
    try:
        parsed = dt.date.fromisoformat(value)
    except ValueError:
        return False
    return parsed <= dt.date.fromisoformat(CUTOFF)


def canonical_prefixed_id(prefix: str, number: int) -> str:
    if prefix == "C-":
        return f"C-{number:03d}" if number < 1000 else f"C-{number}"
    if prefix == "S":
        return f"S{number:02d}" if number < 100 else f"S{number}"
    if prefix == "BN-":
        return f"BN-{number:03d}"
    raise ValueError(prefix)


def supplementary_source_context(text: str, start: int) -> bool:
    prefix = text[max(0, start - 48):start].casefold()
    return bool(re.search(
        r"(?:\bfig(?:s|ures?|uras?)?\.?|\btable|\btabla|"
        r"\bsuppl(?:ementary)?\.?(?:\s+data)?|\bsupplementary(?:\s+data)?|"
        r"\bvideo)\s*$",
        prefix,
    ))


def expanded_refs(text: str, prefix: str) -> list[str]:
    """Expande rangos C/S/BN y conserva el orden de primera aparición."""
    escaped = re.escape(prefix)
    range_re = re.compile(
        rf"\b{escaped}(\d{{2,5}})\s*(?:-|\u2013)\s*{escaped}(\d{{2,5}})\b"
    )
    single_re = re.compile(rf"\b{escaped}\d{{2,5}}\b")
    refs: list[tuple[int, int, str]] = []
    occupied: list[tuple[int, int]] = []
    for match in range_re.finditer(text):
        start, end = map(int, match.groups())
        if (
            start <= end
            and end - start <= 10000
            and not (prefix == "S" and supplementary_source_context(text, match.start()))
        ):
            refs.extend(
                (match.start(), ordinal, canonical_prefixed_id(prefix, number))
                for ordinal, number in enumerate(range(start, end + 1))
            )
        occupied.append(match.span())
    for match in single_re.finditer(text):
        if (
            not any(start <= match.start() < end for start, end in occupied)
            and not (prefix == "S" and supplementary_source_context(text, match.start()))
        ):
            number = int(re.search(r"\d+", match.group(0)).group(0))
            refs.append((match.start(), 0, canonical_prefixed_id(prefix, number)))
    return list(dict.fromkeys(value for _, _, value in sorted(refs)))


def deterministic_sample(keys: set[str], stratum: str) -> set[str]:
    """Muestra reproducible del 15 %, estratificada y sin elección editorial."""
    count = math.ceil(len(keys) * 0.15)
    ranked = sorted(
        keys,
        key=lambda key: (
            sha256_bytes(
                f"research-audit-2026-08-08\x1f{stratum}\x1f{key}".encode("utf-8")
            ),
            key,
        ),
    )
    return set(ranked[:count])


def read_dicts(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def add(
    findings: list[Finding], code: str, path: str, message: str,
    row: int = 0, key: str = "n/a",
) -> None:
    findings.append(Finding(code, path, row, key, message))


def load_index(ctx: AuditContext) -> dict:
    return json.loads(ctx.path("data/table_index.json").read_text(encoding="utf-8"))


def load_claims(ctx: AuditContext) -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    rows: list[dict[str, str]] = []
    for entry in sorted(
        (e for e in load_index(ctx)["tables"] if e["category"] == "claims"),
        key=lambda e: int(e["section"]),
    ):
        header, part = read_dicts(ctx.path(entry["csv_path"]))
        if header != CLAIM_COLUMNS:
            raise ValueError(f"Cabecera de afirmaciones inválida: {entry['csv_path']}")
        rows.extend(part)
    return rows, {row["#"]: row for row in rows}


def load_sources(ctx: AuditContext) -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    _, rows = read_dicts(ctx.path("data/apendices/A_fuentes.csv"))
    return rows, {row["clave"]: row for row in rows}


def claim_fingerprint(row: dict[str, str]) -> str:
    payload = "\x1f".join(row[column] for column in CLAIM_COLUMNS) + "\n"
    return sha256_bytes(payload.encode("utf-8"))


def claim_bundle_fingerprint(
    claim_ids: list[str], current: dict[str, dict[str, str]],
) -> str:
    payload = "".join(
        f"{claim_id}\x1f{claim_fingerprint(current[claim_id])}\n"
        for claim_id in claim_ids
    )
    return sha256_bytes(payload.encode("utf-8"))


def source_fingerprint(row: dict[str, str]) -> str:
    return canonical_row_fingerprint(row)


def audit_anchors(ctx: AuditContext, findings: list[Finding]) -> None:
    for relative, expected, code in (
        (PROMPT_PATH, PROMPT_SHA256, "AF001"),
        (ARCHIVE_PATH, ARCHIVE_SHA256, "AF002"),
    ):
        path = ctx.path(relative)
        if not path.exists():
            add(findings, code, relative, "Falta el archivo anclado")
        elif sha256_file(path) != expected:
            add(findings, code, relative, f"SHA-256 distinto del ancla {expected}")
    version = ctx.path("VERSION")
    if not version.exists() or version.read_text(encoding="utf-8") != "0.6.0-research-audit\n":
        add(findings, "AF003", "VERSION", "VERSION debe ser 0.6.0-research-audit")


def audit_index(ctx: AuditContext, findings: list[Finding]) -> None:
    index = load_index(ctx)
    ids: list[str] = []
    paths: list[str] = []
    for entry in index["tables"]:
        ids.append(entry["id"])
        paths.append(entry["csv_path"])
        path = ctx.path(entry["csv_path"])
        if not path.exists():
            add(findings, "AF701", entry["csv_path"], "CSV indexado ausente", key=entry["id"])
            continue
        header, rows = read_dicts(path)
        if header != entry["columns"]:
            add(findings, "AF702", entry["csv_path"], "Columnas del índice obsoletas", key=entry["id"])
        if len(rows) != entry["row_count"] or len(header) != entry["column_count"]:
            add(findings, "AF703", entry["csv_path"], "Dimensiones del índice obsoletas", key=entry["id"])
    if len(ids) != len(set(ids)):
        add(findings, "AF704", "data/table_index.json", "table_id duplicado")
    if len(paths) != len(set(paths)):
        add(findings, "AF705", "data/table_index.json", "Ruta CSV duplicada")
    templates = []
    for raw in ctx.path("docs/order.txt").read_text(encoding="utf-8").splitlines():
        if raw.strip():
            templates.append(ctx.path(raw.strip()).read_text(encoding="utf-8"))
    placeholders = re.findall(r"<!-- TABLE:([a-z0-9-]+) -->", "\n".join(templates))
    if Counter(placeholders) != Counter(ids):
        add(findings, "AF706", "docs/order.txt", "Marcadores TABLE e índice no coinciden uno a uno")


def audit_claims(ctx: AuditContext, findings: list[Finding]) -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    try:
        rows, by_id = load_claims(ctx)
    except ValueError as error:
        add(findings, "AF101", "data/afirmaciones", str(error))
        return [], {}
    ids = [row["#"] for row in rows]
    if len(ids) != len(set(ids)):
        add(findings, "AF102", "data/afirmaciones", "Claves C duplicadas")
    expected = [f"C-{n:03d}" if n < 1000 else f"C-{n}" for n in range(1, len(rows) + 1)]
    if ids != expected:
        add(findings, "AF103", "data/afirmaciones", "La secuencia C final no es continua y canónica")

    position = {cid: index for index, cid in enumerate(ids)}
    for index, row in enumerate(rows, start=2):
        cid = row["#"]
        predicate = row["Predicado"]
        if predicate in CLOSED_PREDICATES:
            pass
        elif predicate.endswith("*") and predicate[:-1] in CLOSED_PREDICATES:
            add(findings, "AF111", "data/afirmaciones", "Predicado cerrado marcado indebidamente con *", index, cid)
        elif not CUSTOM_PREDICATE.fullmatch(predicate):
            add(findings, "AF110", "data/afirmaciones", "Predicado personalizado sin * o con sintaxis inválida", index, cid)

        if predicate == "cuestionado_por":
            refs = CLAIM_REF.findall(f"{row['Sujeto']} {row['Objeto']}")
            if len(refs) != 1:
                add(findings, "AF120", "data/afirmaciones", "cuestionado_por requiere exactamente una C destino", index, cid)
            elif refs[0] not in by_id or position[refs[0]] >= position[cid]:
                add(findings, "AF121", "data/afirmaciones", "Destino cuestionado inexistente o no anterior", index, cid)
            if row["Aceptación"] == "consenso amplio":
                add(findings, "AF122", "data/afirmaciones", "Una contraafirmación no puede ser consenso amplio sin justificación específica", index, cid)

        attribution = row["Atribución"]
        if attribution.startswith("sintesis("):
            refs = parse_synthesis_refs(attribution)
            if refs is None or not refs:
                add(findings, "AF130", "data/afirmaciones", "Síntesis con sintaxis o dependencias inválidas", index, cid)
            else:
                for ref in refs:
                    if ref not in by_id or position[ref] >= position[cid]:
                        add(findings, "AF131", "data/afirmaciones", f"Dependencia de síntesis inexistente o no anterior: {ref}", index, cid)
        elif attribution not in {"expresa", "glosa"}:
            add(findings, "AF132", "data/afirmaciones", "Atribución fuera del vocabulario", index, cid)

        if attribution == "expresa":
            source_text = row["Fuente"]
            sources = expanded_refs(source_text, "S")
            if not sources:
                add(findings, "AF200", "data/afirmaciones", "Afirmación expresa sin fuente S", index, cid)
            else:
                for source in sources:
                    clauses = [
                        clause.strip()
                        for clause in source_text.split(";")
                        if source in expanded_refs(clause, "S")
                    ]
                    if not clauses or not any(
                        LOCATOR.search(clause)
                        or "sin localizar" in clause.casefold()
                        for clause in clauses
                    ):
                        add(findings, "AF202", "data/afirmaciones", f"Fuente sin localizador propio: {source}", index, cid)
        elif attribution == "glosa" and expanded_refs(row["Fuente"], "S"):
            add(
                findings, "AF203", "data/afirmaciones",
                "Glosa conserva fuente bibliográfica S", index, cid,
            )

        if row["Aceptación"] != "no evaluado" and not expanded_refs(row["Fuente"], "S"):
            add(findings, "AF210", "data/afirmaciones", "Aceptación evaluada sin fuente", index, cid)
        if not row["Motivo"].strip() or row["Motivo"] == "n/a":
            add(findings, "AF211", "data/afirmaciones", "Motivo de fuerza ausente", index, cid)
        if PROHIBITED_DERIVATIONS.search(" ".join(row.values())):
            add(findings, "AF400", "data/afirmaciones", "La fila conserva una cifra derivada prohibida", index, cid)
    return rows, by_id


def audit_claim_bidirectionality(
    ctx: AuditContext, findings: list[Finding], claim_ids: set[str],
) -> None:
    referenced: set[str] = set()
    index = load_index(ctx)
    for entry in index["tables"]:
        if entry["category"] == "claims":
            continue
        referenced.update(
            CLAIM_REF.findall(ctx.path(entry["csv_path"]).read_text(encoding="utf-8"))
        )
    for raw in ctx.path("docs/order.txt").read_text(encoding="utf-8").splitlines():
        if raw.strip():
            referenced.update(
                CLAIM_REF.findall(ctx.path(raw.strip()).read_text(encoding="utf-8"))
            )
    missing = sorted(claim_ids - referenced, key=natural_key)
    for claim_id in missing:
        add(
            findings, "AF140", "data/afirmaciones",
            "C final no aparece en narrativa, tabla ni apéndice fuera del registro",
            key=claim_id,
        )


def is_auditable_tombstone(row: dict[str, str]) -> bool:
    """Distingue una clave registral retirada de una afirmación histórica superada."""
    return (
        row["Vigencia"] == "superada"
        and "tombstone auditable" in row["Motivo"].casefold()
    )


def parse_synthesis_refs(value: str) -> list[str] | None:
    match = re.fullmatch(r"sintesis\(([^()]*)\)", value)
    if not match:
        return None
    refs: list[str] = []
    for part in [part.strip() for part in match.group(1).split(",")]:
        range_match = re.fullmatch(r"C-(\d{3,5})\s*(?:-|–)\s*C-(\d{3,5})", part)
        if range_match:
            start, end = map(int, range_match.groups())
            if start > end:
                return None
            refs.extend(f"C-{n:03d}" if n < 1000 else f"C-{n}" for n in range(start, end + 1))
        elif CLAIM_REF.fullmatch(part):
            refs.append(part)
        else:
            return None
    return refs if len(refs) == len(set(refs)) else None


def audit_sources(
    ctx: AuditContext, findings: list[Finding], claims: list[dict[str, str]],
) -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    rows, by_id = load_sources(ctx)
    ids = [row["clave"] for row in rows]
    if len(ids) != len(set(ids)):
        add(findings, "AF220", "data/apendices/A_fuentes.csv", "Claves S duplicadas")
    doi_seen: dict[str, str] = {}
    for index, row in enumerate(rows, 2):
        raw = row["DOI en forma https://doi.org/10.xxxx/... o URL resoluble si no hay DOI"].strip()
        normalized = raw.casefold()
        if normalized in doi_seen:
            add(findings, "AF221", "data/apendices/A_fuentes.csv", f"DOI/URL duplicado con {doi_seen[normalized]}", index, row["clave"])
        doi_seen[normalized] = row["clave"]
        if row["tipo"] not in {"investigación primaria", "revisión", "base de datos taxonómica", "preprint", "capítulo o libro", "tesis", "divulgación o blog", "otro"}:
            add(findings, "AF222", "data/apendices/A_fuentes.csv", "Tipo de fuente fuera del vocabulario", index, row["clave"])
    used: defaultdict[str, set[str]] = defaultdict(set)
    sole_support: defaultdict[str, set[str]] = defaultdict(set)
    for claim in claims:
        claim_sources = set(expanded_refs(claim["Fuente"], "S"))
        for source in claim_sources:
            used[source].add(claim["#"])
            if source not in by_id:
                add(findings, "AF223", "data/afirmaciones", f"Fuente inexistente: {source}", key=claim["#"])
        if len(claim_sources) == 1:
            sole_support[next(iter(claim_sources))].add(claim["#"])
    for source, claim_ids in sole_support.items():
        notes = by_id.get(source, {}).get("notas de calidad", "").casefold()
        if source in by_id and not re.search(r"\[soporte único(?: actual)?\]", notes):
            add(
                findings, "AF224", "data/apendices/A_fuentes.csv",
                f"Soporte único no declarado para {len(claim_ids)} C",
                key=source,
            )
    for source, claim_ids in used.items():
        if source not in by_id or len(claim_ids) != 1:
            continue
        expected = f"[USO EN UNA SOLA C] {next(iter(claim_ids))}."
        if expected not in by_id[source]["notas de calidad"]:
            add(
                findings, "AF227", "data/apendices/A_fuentes.csv",
                "Fuente usada en una sola C sin marcador exacto de uso",
                key=source,
            )
    referenced_anywhere = set(used)
    index = load_index(ctx)
    for entry in index["tables"]:
        if entry["id"] == "appendix-a":
            continue
        referenced_anywhere.update(
            expanded_refs(ctx.path(entry["csv_path"]).read_text(encoding="utf-8"), "S")
        )
    for raw in ctx.path("docs/order.txt").read_text(encoding="utf-8").splitlines():
        if raw.strip():
            referenced_anywhere.update(
                expanded_refs(ctx.path(raw.strip()).read_text(encoding="utf-8"), "S")
            )
    for source in sorted(set(by_id) - referenced_anywhere, key=natural_key):
        add(findings, "AF226", "data/apendices/A_fuentes.csv", "Fuente sin uso en el corpus canónico final", key=source)
    preprints = {row["clave"] for row in rows if row["tipo"] == "preprint"}
    for claim in claims:
        cited = set(expanded_refs(claim["Fuente"], "S"))
        if claim["Aceptación"] == "consenso amplio" and cited and cited <= preprints:
            add(findings, "AF225", "data/afirmaciones", "Consenso amplio sostenido solo por preprint", key=claim["#"])
    return rows, by_id


def audit_matrices(
    ctx: AuditContext, findings: list[Finding], claims: list[dict[str, str]],
    sources: list[dict[str, str]],
) -> None:
    current_claims = {row["#"]: row for row in claims}
    current_source_rows = {row["clave"]: row for row in sources}
    current_sources = set(current_source_rows)
    key_mapping: dict[str, str] = {}
    key_map_path = ctx.path(KEY_MAP)
    if key_map_path.exists():
        _, key_rows = read_dicts(key_map_path)
        key_mapping = {
            row["clave_pre_renumeracion"]: row["clave_final"]
            for row in key_rows
            if "clave_pre_renumeracion" in row and "clave_final" in row
        }
    path = ctx.path(CLAIM_MATRIX)
    if not path.exists():
        add(findings, "AF500", CLAIM_MATRIX, "Falta la matriz final de afirmaciones")
    else:
        header, rows = read_dicts(path)
        if header != CLAIM_MATRIX_COLUMNS:
            add(findings, "AF501", CLAIM_MATRIX, "Cabecera distinta del contrato exacto")
        else:
            matrix_keys = [row["clave_inicial"] for row in rows]
            if len(matrix_keys) != len(set(matrix_keys)):
                add(findings, "AF501", CLAIM_MATRIX, "clave_inicial duplicada en la matriz")
            baseline_rows = [row for row in rows if re.fullmatch(r"C-\d{3,4}", row["clave_inicial"])]
            initial = [row["clave_inicial"] for row in baseline_rows]
            if len(initial) != BASELINE_CLAIM_COUNT or len(initial) != len(set(initial)) or keyset_sha256(initial) != BASELINE_CLAIM_KEYSET_SHA256:
                add(findings, "AF502", CLAIM_MATRIX, "La matriz no cubre exactamente las 1.840 C iniciales")
            initial_audit_items = [
                (row["clave_inicial"], row["huella_inicial_sha256"])
                for row in baseline_rows
            ]
            if (
                any(not HEX_SHA256.fullmatch(value) for _, value in initial_audit_items)
                or aggregate_keyed_fingerprints(initial_audit_items)
                != BASELINE_CLAIM_AUDIT_SHA256
            ):
                add(findings, "AF550", CLAIM_MATRIX, "Huellas del inventario C inicial no coinciden con el congelado")
            initial_corpus_items = [
                (row["clave_inicial"], row["huella_corpus_inicial_sha256"])
                for row in baseline_rows
            ]
            if (
                any(not HEX_SHA256.fullmatch(value) for _, value in initial_corpus_items)
                or aggregate_keyed_fingerprints(initial_corpus_items)
                != BASELINE_CLAIM_CORPUS_SHA256
            ):
                add(findings, "AF551", CLAIM_MATRIX, "Huellas del corpus C inicial no coinciden con la instantánea")
            summary_items: list[tuple[str, str]] = []
            for row in baseline_rows:
                frozen_summary = {
                    "clave_inicial": row["clave_inicial"],
                    "seccion": row["seccion_inicial"],
                    "resultado": row["estado_inicial"],
                    "severidad": row["severidad_inicial"],
                    "accion": row["accion_inicial"],
                    "evidencia_auditoria": row["evidencia_auditoria_inicial"],
                }
                summary_items.append(
                    (row["clave_inicial"], canonical_row_fingerprint(frozen_summary))
                )
            if aggregate_keyed_fingerprints(summary_items) != BASELINE_CLAIM_SUMMARY_SHA256:
                add(findings, "AF552", CLAIM_MATRIX, "Estado/severidad/acción/evidencia C iniciales fueron reescritos")
            covered: Counter[str] = Counter()
            for index, row in enumerate(rows, 2):
                finals = expanded_refs(row["claves_finales"], "C-")
                covered.update(finals)
                for column in CLAIM_MATRIX_COLUMNS:
                    if not row[column].strip():
                        add(findings, "AF501", CLAIM_MATRIX, f"Celda obligatoria vacía: {column}", index, row["clave_inicial"])
                if row["resultado"] not in {"CONFORME", "CORREGIDA", "RETIRADA", "FUSIONADA", "NUEVA"}:
                    add(findings, "AF503", CLAIM_MATRIX, "Resultado final inválido", index, row["clave_inicial"])
                if row["estado_hallazgo"] not in {"CERRADO", "HUECO_CIENTIFICO_ETIQUETADO"}:
                    add(findings, "AF504", CLAIM_MATRIX, "Hallazgo no cerrado", index, row["clave_inicial"])
                for axis in ("atomicidad", "equivalencia_spo", "soporte", "localizador", "fidelidad_epistemica", "etiquetas", "trazabilidad_apendices"):
                    if row[axis] not in {"CONFORME", "NO_APLICA"}:
                        add(findings, "AF505", CLAIM_MATRIX, f"Eje final abierto: {axis}", index, row["clave_inicial"])
                if finals and all(final in current_claims for final in finals):
                    expected_fingerprint = (
                        claim_fingerprint(current_claims[finals[0]])
                        if len(finals) == 1
                        else claim_bundle_fingerprint(finals, current_claims)
                    )
                    if row["huella_final_sha256"] != expected_fingerprint:
                        add(findings, "AF506", CLAIM_MATRIX, "Huella de C final desactualizada", index, row["clave_inicial"])
                elif finals:
                    add(findings, "AF508", CLAIM_MATRIX, "La matriz apunta a una C final inexistente", index, row["clave_inicial"])
                elif row["resultado"] != "RETIRADA":
                    add(findings, "AF509", CLAIM_MATRIX, "Fila sin destino final que no está retirada", index, row["clave_inicial"])
                is_baseline = re.fullmatch(r"C-\d{3,4}", row["clave_inicial"]) is not None
                if is_baseline:
                    mapped_primary = key_mapping.get(row["clave_inicial"])
                    if mapped_primary is not None and mapped_primary not in finals:
                        add(findings, "AF518", CLAIM_MATRIX, "Destino primario contradice el mapa de renumeración", index, row["clave_inicial"])
                    if mapped_primary is None and row["resultado"] != "RETIRADA":
                        add(findings, "AF519", CLAIM_MATRIX, "C inicial ausente del mapa sin disposición RETIRADA", index, row["clave_inicial"])
                elif row["clave_inicial"].startswith("NUEVA:"):
                    pre_key = row["clave_inicial"].removeprefix("NUEVA:")
                    if row["resultado"] != "NUEVA":
                        add(findings, "AF553", CLAIM_MATRIX, "Fila nueva sin resultado NUEVA", index, row["clave_inicial"])
                    if row["huella_inicial_sha256"] not in {"n/a", "NO_APLICA"} or row["huella_corpus_inicial_sha256"] not in {"n/a", "NO_APLICA"}:
                        add(findings, "AF554", CLAIM_MATRIX, "Fila nueva simula una huella inicial", index, row["clave_inicial"])
                    if key_mapping.get(pre_key) not in finals:
                        add(findings, "AF555", CLAIM_MATRIX, "Fila nueva no coincide con su clave pre-renumeración", index, row["clave_inicial"])
                else:
                    add(findings, "AF556", CLAIM_MATRIX, "Sintaxis de clave inicial inválida", index, row["clave_inicial"])
            if covered != Counter({claim_id: 1 for claim_id in current_claims}):
                add(findings, "AF507", CLAIM_MATRIX, "La matriz no cubre cada C final exactamente una vez")

    path = ctx.path(SOURCE_MATRIX)
    if not path.exists():
        add(findings, "AF510", SOURCE_MATRIX, "Falta la matriz final de fuentes")
    else:
        header, rows = read_dicts(path)
        if header != SOURCE_MATRIX_COLUMNS:
            add(findings, "AF511", SOURCE_MATRIX, "Cabecera distinta del contrato exacto")
        else:
            matrix_keys = [row["clave_inicial"] for row in rows]
            if len(matrix_keys) != len(set(matrix_keys)):
                add(findings, "AF511", SOURCE_MATRIX, "clave_inicial duplicada en la matriz")
            baseline_rows = [row for row in rows if re.fullmatch(r"S\d{2,3}", row["clave_inicial"])]
            initial = [row["clave_inicial"] for row in baseline_rows]
            if len(initial) != BASELINE_SOURCE_COUNT or len(initial) != len(set(initial)) or keyset_sha256(initial) != BASELINE_SOURCE_KEYSET_SHA256:
                add(findings, "AF512", SOURCE_MATRIX, "La matriz no cubre exactamente las 525 S iniciales")
            audit_items: list[tuple[str, str]] = []
            corpus_items: list[tuple[str, str]] = []
            for row in baseline_rows:
                frozen = {
                    "clave_inicial": row["clave_inicial"],
                    "clave_final": row["clave_inicial"],
                    "metadata": row["metadatos_iniciales"],
                    "identidad_bibliografica": row["identidad_bibliografica"],
                    "tipo": row["tipo_inicial"],
                    "estado_editorial": row["estado_editorial"],
                    "acceso": row["acceso"],
                    "doi_url": row["doi_url_inicial"],
                    "uso": row["uso_inicial"],
                    "soporte_unico": row["soporte_unico_inicial"],
                    "veredicto": row["veredicto_inicial"],
                    "severidad": row["severidad_inicial"],
                    "accion": row["accion_inicial"],
                    "fecha_verificacion": row["fecha_verificacion"],
                    "evidencia_auditoria": row["evidencia_auditoria_inicial"],
                }
                expected = canonical_row_fingerprint(frozen)
                if row["huella_inicial_sha256"] != expected:
                    add(findings, "AF557", SOURCE_MATRIX, "Huella de auditoría S inicial no reproduce su fila", key=row["clave_inicial"])
                audit_items.append((row["clave_inicial"], row["huella_inicial_sha256"]))
                corpus_items.append((row["clave_inicial"], row["huella_corpus_inicial_sha256"]))
            if aggregate_keyed_fingerprints(audit_items) != BASELINE_SOURCE_AUDIT_SHA256:
                add(findings, "AF558", SOURCE_MATRIX, "Inventario S inicial distinto del congelado")
            if (
                any(not HEX_SHA256.fullmatch(value) for _, value in corpus_items)
                or aggregate_keyed_fingerprints(corpus_items) != BASELINE_SOURCE_CORPUS_SHA256
            ):
                add(findings, "AF559", SOURCE_MATRIX, "Huellas del corpus S inicial no coinciden con la instantánea")
            covered: Counter[str] = Counter()
            for index, row in enumerate(rows, 2):
                if row["veredicto"] not in {
                    "CONFORME", "CORREGIDA", "RETIRADA", "FUSIONADA", "NUEVA",
                }:
                    add(findings, "AF517", SOURCE_MATRIX, "Veredicto final inválido", index, row["clave_inicial"])
                if re.fullmatch(r"S\d{2,3}", row["clave_final"]):
                    covered[row["clave_final"]] += 1
                    if row["clave_final"] in current_sources:
                        current = current_source_rows[row["clave_final"]]
                        if row["huella_final_sha256"] != source_fingerprint(current):
                            add(findings, "AF516", SOURCE_MATRIX, "Huella de S final desactualizada", index, row["clave_inicial"])
                        if row["tipo_final"] != current["tipo"]:
                            add(findings, "AF560", SOURCE_MATRIX, "Tipo final no coincide con A", index, row["clave_inicial"])
                        doi_column = "DOI en forma https://doi.org/10.xxxx/... o URL resoluble si no hay DOI"
                        if row["doi_url_final"] != current[doi_column]:
                            add(findings, "AF561", SOURCE_MATRIX, "DOI/URL final no coincide con A", index, row["clave_inicial"])
                    else:
                        add(findings, "AF515", SOURCE_MATRIX, "La matriz apunta a una S final inexistente", index, row["clave_inicial"])
                elif row["clave_final"] not in {"n/a", "NO_APLICA"}:
                    add(findings, "AF515", SOURCE_MATRIX, "Sintaxis de clave final inválida", index, row["clave_inicial"])
                if row["estado_hallazgo"] not in {"CERRADO", "HUECO_CIENTIFICO_ETIQUETADO"}:
                    add(findings, "AF513", SOURCE_MATRIX, "Hallazgo bibliográfico no cerrado", index, row["clave_inicial"])
                if not valid_iso_date(row["fecha_verificacion"]):
                    add(findings, "AF514", SOURCE_MATRIX, "Fecha inválida o posterior al corte", index, row["clave_inicial"])
                for column in SOURCE_MATRIX_COLUMNS:
                    if not row[column].strip():
                        add(findings, "AF511", SOURCE_MATRIX, f"Celda obligatoria vacía: {column}", index, row["clave_inicial"])
                is_baseline = re.fullmatch(r"S\d{2,3}", row["clave_inicial"]) is not None
                if not is_baseline:
                    if not row["clave_inicial"].startswith("NUEVA:S"):
                        add(findings, "AF562", SOURCE_MATRIX, "Sintaxis de fuente inicial inválida", index, row["clave_inicial"])
                    if row["veredicto"] != "NUEVA":
                        add(findings, "AF563", SOURCE_MATRIX, "Fuente nueva sin veredicto NUEVA", index, row["clave_inicial"])
                    if row["huella_inicial_sha256"] not in {"n/a", "NO_APLICA"} or row["huella_corpus_inicial_sha256"] not in {"n/a", "NO_APLICA"}:
                        add(findings, "AF564", SOURCE_MATRIX, "Fuente nueva simula una huella inicial", index, row["clave_inicial"])
            if covered != Counter({source_id: 1 for source_id in current_sources}):
                add(findings, "AF515", SOURCE_MATRIX, "La matriz no cubre cada S final exactamente una vez")


def normalize_markdown_literal(value: str) -> str:
    value = re.sub(r"[`*_#>]", "", value)
    value = re.sub(r"(?m)^\s*[-+]\s+", "", value)
    return re.sub(r"\s+", " ", value).strip()


def audit_requirements(
    ctx: AuditContext, findings: list[Finding], claim_ids: set[str],
    source_ids: set[str],
) -> None:
    path = ctx.path(REQUIREMENT_MATRIX)
    if not path.exists():
        add(findings, "AF520", REQUIREMENT_MATRIX, "Falta la matriz final de requisitos")
        return
    header, rows = read_dicts(path)
    if header != REQUIREMENT_MATRIX_COLUMNS:
        add(findings, "AF521", REQUIREMENT_MATRIX, "Cabecera distinta del contrato exacto")
        return
    ids = [row["id_requisito"] for row in rows]
    expected = [f"R-{n:04d}" for n in range(1, 484)]
    if ids != expected or len(ids) != len(set(ids)):
        add(findings, "AF522", REQUIREMENT_MATRIX, "Deben existir exactamente R-0001…R-0483")
    prompt_lines = ctx.path(PROMPT_PATH).read_text(encoding="utf-8").splitlines()
    prompt = normalize_markdown_literal("\n".join(prompt_lines))
    allowed = {"CUMPLE", "CUMPLE_MEDIANTE_HUECO_ETIQUETADO", "NO_APLICA_JUSTIFICADO"}
    initial_items: list[tuple[str, str]] = []
    literal_pairs: list[tuple[str, str]] = []
    table_ids = {entry["id"] for entry in load_index(ctx)["tables"]}
    bn_ids: set[str] = set()
    history_path = ctx.path(NEGATIVE_HISTORY)
    if history_path.exists():
        _, history_rows = read_dicts(history_path)
        bn_ids.update(row.get("clave_original", "") for row in history_rows)
    for entry in load_index(ctx)["tables"]:
        if entry["category"] == "negative":
            _, negative_rows = read_dicts(ctx.path(entry["csv_path"]))
            bn_ids.update(row.get("clave", "") for row in negative_rows)
    bn_ids.discard("")
    for index, row in enumerate(rows, 2):
        key = row["id_requisito"]
        for column in REQUIREMENT_MATRIX_COLUMNS:
            if not row[column].strip():
                add(findings, "AF521", REQUIREMENT_MATRIX, f"Celda obligatoria vacía: {column}", index, key)
        frozen = {
            "seccion_prompt": row["seccion_prompt"],
            "requisito_literal": row["requisito_literal"],
            "estado_inicial": row["estado_inicial"],
            "estado_final": "PENDIENTE",
            "afirmaciones": row["afirmaciones_iniciales"],
            "tablas": row["tablas_iniciales"],
            "fuentes": row["fuentes_iniciales"],
            "busqueda_negativa": row["busqueda_negativa_inicial"],
            "accion": row["accion_inicial"],
            "evidencia": row["evidencia_inicial"],
        }
        expected_fingerprint = canonical_row_fingerprint(frozen)
        if row["huella_inicial_sha256"] != expected_fingerprint:
            add(findings, "AF570", REQUIREMENT_MATRIX, "Huella inicial no reproduce el requisito congelado", index, key)
        initial_items.append((key, row["huella_inicial_sha256"]))
        literal_pairs.append((row["seccion_prompt"], row["requisito_literal"]))
        if normalize_markdown_literal(row["requisito_literal"]) not in prompt:
            add(findings, "AF523", REQUIREMENT_MATRIX, "El requisito no es fragmento literal del prompt", index, key)
        anchor = re.fullmatch(r"L(\d+)(?:-L(\d+))?", row["ancla"])
        if not anchor:
            add(findings, "AF571", REQUIREMENT_MATRIX, "Ancla de línea inválida", index, key)
        else:
            start = int(anchor.group(1))
            end = int(anchor.group(2) or start)
            anchored = normalize_markdown_literal(
                "\n".join(prompt_lines[max(0, start - 1):end])
            )
            if start < 1 or end < start or end > len(prompt_lines) or normalize_markdown_literal(row["requisito_literal"]) not in anchored:
                add(findings, "AF572", REQUIREMENT_MATRIX, "El ancla no contiene el requisito literal", index, key)
        if row["estado_final"] not in allowed:
            add(findings, "AF524", REQUIREMENT_MATRIX, "Estado final pendiente o inválido", index, key)
        final_refs = {
            "afirmaciones": (expanded_refs(row["afirmaciones"], "C-"), claim_ids),
            "fuentes": (expanded_refs(row["fuentes"], "S"), source_ids),
            "busqueda_negativa": (expanded_refs(row["busqueda_negativa"], "BN-"), bn_ids),
        }
        for column, (refs, valid) in final_refs.items():
            value = row[column].strip()
            if value not in {"n/a", "NO_APLICA"} and not refs:
                add(findings, "AF573", REQUIREMENT_MATRIX, f"{column} no contiene claves parseables", index, key)
            invalid = sorted(set(refs) - valid, key=natural_key)
            if invalid:
                add(findings, "AF574", REQUIREMENT_MATRIX, f"{column} contiene claves inválidas: {invalid[:10]}", index, key)
        table_refs = re.findall(r"\b(?:table|appendix|negative|node)-[a-z0-9-]+\b", row["tablas"])
        if row["tablas"].strip() not in {"n/a", "NO_APLICA"} and not table_refs:
            add(findings, "AF575", REQUIREMENT_MATRIX, "Campo tablas sin table_id parseable", index, key)
        invalid_tables = sorted(set(table_refs) - table_ids)
        if invalid_tables:
            add(findings, "AF576", REQUIREMENT_MATRIX, f"table_id inválido: {invalid_tables[:10]}", index, key)
        no_keyed_destination = all(
            row[column].strip() in {"n/a", "NO_APLICA"}
            for column in ("afirmaciones", "tablas", "fuentes", "busqueda_negativa")
        )
        explicit_non_keyed_evidence = any(
            marker in row["evidencia"]
            for marker in (
                "control estructural verificable",
                "hueco explícito:",
            )
        )
        if (
            no_keyed_destination
            and row["estado_final"] != "NO_APLICA_JUSTIFICADO"
            and not explicit_non_keyed_evidence
        ):
            add(findings, "AF577", REQUIREMENT_MATRIX, "Requisito sin destino trazable, control estructural o hueco explícito", index, key)
    if len(literal_pairs) != len(set(literal_pairs)):
        add(findings, "AF578", REQUIREMENT_MATRIX, "Requisito literal duplicado dentro de una sección")
    if Counter(row["seccion_prompt"] for row in rows).keys() != {str(number) for number in range(19)}:
        add(findings, "AF579", REQUIREMENT_MATRIX, "Las secciones 0–18 no están cubiertas exactamente como inventario")
    if aggregate_keyed_fingerprints(initial_items) != BASELINE_REQUIREMENT_AUDIT_SHA256:
        add(findings, "AF580", REQUIREMENT_MATRIX, "Inventario de 483 requisitos distinto del congelado")


def audit_appendices(
    ctx: AuditContext, findings: list[Finding], claims: list[dict[str, str]],
    source_ids: set[str],
) -> None:
    claim_ids = {row["#"] for row in claims}
    _, entities = read_dicts(ctx.path("data/apendices/B_entidades.csv"))
    labels = [row["etiqueta preferida"].strip().casefold() for row in entities]
    if len(labels) != len(set(labels)):
        add(findings, "AF410", "data/apendices/B_entidades.csv", "Etiquetas preferidas duplicadas")
    for index, row in enumerate(entities, 2):
        if row["# de la fila del registro donde aparece por primera vez"] not in claim_ids:
            add(findings, "AF411", "data/apendices/B_entidades.csv", "Primera C inexistente", index, row["etiqueta preferida"])

    _, events = read_dicts(ctx.path("data/apendices/C_eventos.csv"))
    event_types = {"endosimbiosis", "transferencia horizontal", "transferencia génica endosimbiótica", "divergencia", "radiación", "extinción", "adquisición de rasgo", "pérdida de rasgo", "reducción genómica", "depredación", "competencia", "relación huésped-patógeno", "asociación no heredable"}
    outcomes = {"transitoria", "dependencia", "integración heredable", "degradación", "pérdida", "no determinado"}
    roles = {"hospedador", "endosimbionte", "simbionte extracelular", "donante", "receptor", "población parental", "linaje resultante", "depredador", "presa", "huésped", "parásito", "competidor"}
    for index, row in enumerate(events, 2):
        if row["tipo"] not in event_types:
            add(findings, "AF420", "data/apendices/C_eventos.csv", "Tipo de evento fuera del vocabulario", index, row["clave"])
        if row["desenlace"] not in outcomes:
            add(findings, "AF421", "data/apendices/C_eventos.csv", "Desenlace fuera del vocabulario", index, row["clave"])
        found_roles = re.findall(r"\(([^()]*)\)", row["participantes con su papel"])
        if not found_roles or any(role not in roles for role in found_roles):
            add(findings, "AF422", "data/apendices/C_eventos.csv", "Participante sin papel cerrado", index, row["clave"])
        for ref in CLAIM_REF.findall(row["# de las filas que lo sostienen"]):
            if ref not in claim_ids:
                add(findings, "AF423", "data/apendices/C_eventos.csv", f"C inexistente: {ref}", index, row["clave"])
        for ref in expanded_refs(row["qué fuente lo describe como evento"], "S"):
            if ref not in source_ids:
                add(findings, "AF424", "data/apendices/C_eventos.csv", f"S inexistente: {ref}", index, row["clave"])

    _, hypotheses = read_dicts(ctx.path("data/apendices/E_hipotesis.csv"))
    hypothesis_ids = {row["clave"] for row in hypotheses}
    if len(hypothesis_ids) != len(hypotheses):
        add(findings, "AF440", "data/apendices/E_hipotesis.csv", "Claves H duplicadas")
    for index, row in enumerate(hypotheses, 2):
        key = row["clave"]
        refs = expanded_refs(row["# de las filas que la componen"], "C-")
        if not refs or any(ref not in claim_ids for ref in refs):
            add(findings, "AF441", "data/apendices/E_hipotesis.csv", "Hipótesis sin C finales válidas", index, key)
        support = expanded_refs(row["fuentes a favor"], "S")
        opposition = expanded_refs(row["fuentes en contra"], "S")
        if not support or any(ref not in source_ids for ref in support):
            add(findings, "AF442", "data/apendices/E_hipotesis.csv", "Hipótesis sin apoyo S válido", index, key)
        explicit_negative = re.search(
            r"no se localiz|ninguna fuente|sin fuente|ausencia de (?:apoyo|oposici[oó]n)",
            row["fuentes en contra"], re.IGNORECASE,
        )
        if (not opposition and not explicit_negative) or any(
            ref not in source_ids for ref in opposition
        ):
            add(findings, "AF443", "data/apendices/E_hipotesis.csv", "Oposición ausente, inválida o no declarada como hueco", index, key)
        incompatible = re.findall(r"\bH\d{2,3}\b", row["con qué otras hipótesis es incompatible y en qué punto exacto"])
        incompatibility_text = row["con qué otras hipótesis es incompatible y en qué punto exacto"].strip()
        if incompatibility_text in {"", "n/a"} or any(ref not in hypothesis_ids for ref in incompatible):
            add(findings, "AF444", "data/apendices/E_hipotesis.csv", "Incompatibilidad H inválida o sin punto documentado", index, key)
        if row["qué observación la falsaría"].strip() in {"", "n/a"}:
            add(findings, "AF445", "data/apendices/E_hipotesis.csv", "Criterio de falsación ausente", index, key)

    known_bn: set[str] = set()
    for entry in load_index(ctx)["tables"]:
        if entry["category"] == "negative":
            _, part = read_dicts(ctx.path(entry["csv_path"]))
            known_bn.update(row.get("clave", "") for row in part)
    if ctx.path(NEGATIVE_HISTORY).exists():
        _, history_rows = read_dicts(ctx.path(NEGATIVE_HISTORY))
        known_bn.update(row.get("clave_original", "") for row in history_rows)
    known_bn.discard("")

    _, unmatched = read_dicts(ctx.path("data/apendices/G_material_no_encajado.csv"))
    for index, row in enumerate(unmatched, 2):
        key = row["material"]
        refs = expanded_refs(row["#"], "C-")
        source_refs = expanded_refs(row["fuente y localizador"], "S")
        bn_refs = expanded_refs(row["fuente y localizador"], "BN-")
        prompt_scope = (
            row["#"].strip() == "n/a"
            and "C01-PROMPT-INVESTIGACION" in row["fuente y localizador"]
        )
        if not refs and not prompt_scope:
            add(findings, "AF446", "data/apendices/G_material_no_encajado.csv", "Material G sin C ni excepción de alcance", index, key)
        if any(ref not in claim_ids for ref in refs):
            add(findings, "AF447", "data/apendices/G_material_no_encajado.csv", "Material G apunta a C inexistente", index, key)
        if any(ref not in source_ids for ref in source_refs):
            add(findings, "AF448", "data/apendices/G_material_no_encajado.csv", "Material G apunta a S inexistente", index, key)
        if any(ref not in known_bn for ref in bn_refs):
            add(findings, "AF452", "data/apendices/G_material_no_encajado.csv", "Material G apunta a BN inexistente", index, key)
        if not source_refs and not bn_refs and not prompt_scope:
            add(findings, "AF449", "data/apendices/G_material_no_encajado.csv", "Material G carece de fuente S, BN o ancla del encargo", index, key)

    appendix_refs: dict[str, set[str]] = {}
    for relative, ref_column in (("data/apendices/D_fechas.csv", "# de la fila que la sostiene"), ("data/apendices/F_magnitudes.csv", "#")):
        _, rows = read_dicts(ctx.path(relative))
        all_refs: set[str] = set()
        seen_payloads: set[tuple[str, ...]] = set()
        for index, row in enumerate(rows, 2):
            refs = expanded_refs(row[ref_column], "C-")
            all_refs.update(refs)
            if not refs or any(ref not in claim_ids for ref in refs):
                add(findings, "AF430", relative, "Fila D/F sin C final válida", index)
            if PROHIBITED_DERIVATIONS.search(" ".join(row.values())):
                add(findings, "AF431", relative, "Fila D/F conserva una derivación propia", index)
            payload = tuple(row.values())
            if payload in seen_payloads:
                add(findings, "AF434", relative, "Fila D/F exactamente duplicada", index)
            seen_payloads.add(payload)
            for column, value in row.items():
                if column not in {"incertidumbre tal como la da la fuente", "incertidumbre publicada"} and value.strip() in {"", "n/a"}:
                    add(findings, "AF435", relative, f"Campo sustantivo ausente: {column}", index)
            if row["observado o inferido"] not in {"observado", "inferido"}:
                add(findings, "AF436", relative, "observado o inferido fuera del vocabulario", index)
            source_text = row["fuente con localizador"]
            source_refs = expanded_refs(source_text, "S")
            internal_control = relative.endswith("F_magnitudes.csv") and row["magnitud"] in {
                "búsquedas negativas activas",
                "búsquedas con ausencia declarada",
                "búsquedas sin resultado localizado",
                "búsquedas activas no buscadas",
            }
            if internal_control:
                if source_text != "registro canónico" or row["método o proxy"] != "recuento de CSV" or row["unidad original"] != "filas":
                    add(findings, "AF437", relative, "Excepción interna F no es recomputable ni está rotulada canónicamente", index)
            elif not source_refs:
                add(findings, "AF438", relative, "Magnitud/fecha científica sin fuente S", index)
            if "sin localizar" in source_text.casefold():
                add(findings, "AF439", relative, "Fuente D/F conserva 'sin localizar'", index)
            for source in source_refs:
                clauses = [
                    clause.strip() for clause in source_text.split(";")
                    if source in expanded_refs(clause, "S")
                ]
                if source not in source_ids or not clauses or not any(LOCATOR.search(clause) for clause in clauses):
                    add(findings, "AF450", relative, f"Fuente D/F inexistente o sin localizador propio: {source}", index)
        appendix_refs[relative] = all_refs

    negative_rows: list[dict[str, str]] = []
    for entry in load_index(ctx)["tables"]:
        if entry["category"] == "negative":
            _, part = read_dicts(ctx.path(entry["csv_path"]))
            negative_rows.extend(part)
    state_counts: Counter[str] = Counter()
    for row in negative_rows:
        state = row.get("estado") or row.get("etiqueta") or ""
        state_counts[state] += 1
    internal_expected = {
        "búsquedas negativas activas": len(negative_rows),
        "búsquedas con ausencia declarada": state_counts["LA LITERATURA DECLARA QUE NO SE SABE"],
        "búsquedas sin resultado localizado": state_counts["NO LOCALIZADO EN ESTA SESIÓN"],
        "búsquedas activas no buscadas": sum(
            count for state, count in state_counts.items()
            if state not in {"LA LITERATURA DECLARA QUE NO SE SABE", "NO LOCALIZADO EN ESTA SESIÓN"}
        ),
    }
    _, magnitude_rows = read_dicts(ctx.path("data/apendices/F_magnitudes.csv"))
    internal_rows = [row for row in magnitude_rows if row["magnitud"] in internal_expected]
    actual_internal = Counter(
        (row["magnitud"], row["valor tal como lo publica la fuente"])
        for row in internal_rows
    )
    expected_internal = Counter(
        {(key, str(value)): 1 for key, value in internal_expected.items()}
    )
    if actual_internal != expected_internal:
        add(findings, "AF451", "data/apendices/F_magnitudes.csv", "Controles BN internos ausentes, duplicados o desactualizados")
    for claim in claims:
        if (
            claim["Predicado"] == "tiene_edad_estimada"
            and claim["#"] not in appendix_refs["data/apendices/D_fechas.csv"]
        ):
            add(findings, "AF432", "data/apendices/D_fechas.csv", "C de edad aplicable ausente de D", key=claim["#"])
        if (
            claim["Predicado"] == "tiene_valor_medido"
            and claim["#"] not in appendix_refs["data/apendices/F_magnitudes.csv"]
        ):
            add(findings, "AF433", "data/apendices/F_magnitudes.csv", "C de magnitud aplicable ausente de F", key=claim["#"])


def audit_negative_history(ctx: AuditContext, findings: list[Finding]) -> None:
    canonical: set[str] = set()
    for entry in load_index(ctx)["tables"]:
        if entry["category"] == "negative":
            _, rows = read_dicts(ctx.path(entry["csv_path"]))
            canonical.update(row["clave"] for row in rows)
    if len(canonical) != BASELINE_ACTIVE_BN_COUNT or keyset_sha256(canonical) != BASELINE_ACTIVE_BN_KEYSET_SHA256:
        add(findings, "AF600", "data/busquedas_negativas", "El conjunto activo no coincide con las 68 BN congeladas")
    path = ctx.path(NEGATIVE_HISTORY)
    if not path.exists():
        add(findings, "AF601", NEGATIVE_HISTORY, "Falta la historia de 106 BN")
        return
    header, rows = read_dicts(path)
    required = {
        "clave_original", "prioridad_final", "desencadenante",
        "delta_auditoria_2026_08_08",
    }
    if not required <= set(header):
        add(findings, "AF602", NEGATIVE_HISTORY, "Faltan prioridad/desencadenante/delta de auditoría")
        return
    ids = [row["clave_original"] for row in rows]
    if len(ids) != BASELINE_BN_COUNT or len(ids) != len(set(ids)) or keyset_sha256(ids) != BASELINE_BN_KEYSET_SHA256:
        add(findings, "AF603", NEGATIVE_HISTORY, "La historia no conserva exactamente 106 BN")
    active_rows = [row for row in rows if row["clave_original"] in canonical]
    counts = Counter(row["prioridad_final"] for row in active_rows)
    if counts != Counter({"P0": 22, "P1": 23, "P2": 23}):
        add(findings, "AF604", NEGATIVE_HISTORY, f"Prioridades activas incorrectas: {dict(counts)}")
    for index, row in enumerate(rows, 2):
        for column in required:
            if not row[column].strip():
                add(findings, "AF602", NEGATIVE_HISTORY, f"Celda obligatoria vacía: {column}", index, row.get("clave_original", "n/a"))
        expected_priority = (
            row["prioridad_final"] in {"P0", "P1", "P2"}
            if row["clave_original"] in canonical
            else row["prioridad_final"] == "RETIRADA"
        )
        if not expected_priority:
            add(findings, "AF605", NEGATIVE_HISTORY, "Prioridad incompatible con disposición activa/histórica", index, row["clave_original"])
        if row["prioridad_final"] == "P2" and row["desencadenante"] == "n/a":
            add(findings, "AF606", NEGATIVE_HISTORY, "BN P2 sin desencadenante literal", index, row["clave_original"])


def audit_searches(ctx: AuditContext, findings: list[Finding]) -> None:
    path = ctx.path(SEARCH_MATRIX)
    if not path.exists():
        add(findings, "AF610", SEARCH_MATRIX, "Falta el registro final de búsquedas")
        return
    header, rows = read_dicts(path)
    if header != SEARCH_MATRIX_COLUMNS:
        add(findings, "AF611", SEARCH_MATRIX, "Cabecera distinta del contrato exacto")
        return
    expected_ids = [f"Q-{number:04d}" for number in range(1, len(rows) + 1)]
    if [row["id_busqueda"] for row in rows] != expected_ids:
        add(findings, "AF618", SEARCH_MATRIX, "Las claves Q no son continuas, únicas y ordenadas")
    baseline_rows = rows[:165]
    if len(baseline_rows) != 165 or [row["id_busqueda"] for row in baseline_rows] != [f"Q-{number:04d}" for number in range(1, 166)]:
        add(findings, "AF619", SEARCH_MATRIX, "Falta el ancla exacta Q-0001…Q-0165")
    initial_items: list[tuple[str, str]] = []
    for index, row in enumerate(baseline_rows, 2):
        frozen = {
            "fecha": row["fecha"],
            "bloque": row["bloque"],
            "objetivo": row["objetivo"],
            "consulta_exacta": row["consulta_exacta"],
            "servicio": row["servicio"],
            "resultado": row["resultado"],
            "fuentes_evaluadas": row["fuentes_evaluadas"],
            "accion": row["accion_inicial"],
        }
        expected_fingerprint = canonical_row_fingerprint(frozen)
        if row["huella_inicial_sha256"] != expected_fingerprint:
            add(findings, "AF620", SEARCH_MATRIX, "Huella Q inicial no reproduce la fila congelada", index, row["id_busqueda"])
        initial_items.append((row["id_busqueda"], row["huella_inicial_sha256"]))
    if aggregate_keyed_fingerprints(initial_items) != BASELINE_SEARCH_AUDIT_SHA256:
        add(findings, "AF621", SEARCH_MATRIX, "Inventario Q-0001…Q-0165 distinto del congelado")
    baseline_bn_rows = baseline_rows[:106]
    ids = [row["clave_bn"] for row in baseline_bn_rows]
    if len(ids) != BASELINE_BN_COUNT or len(ids) != len(set(ids)) or keyset_sha256(ids) != BASELINE_BN_KEYSET_SHA256:
        add(findings, "AF612", SEARCH_MATRIX, "El registro no contiene exactamente las 106 BN")
    history_priorities: dict[str, str] = {}
    history_path = ctx.path(NEGATIVE_HISTORY)
    if history_path.exists():
        _, history_rows = read_dicts(history_path)
        history_priorities = {
            row["clave_original"]: row.get("prioridad_final", "")
            for row in history_rows
        }
    allowed_priorities = {"P0", "P1", "P2", "RETIRADA", "NO_APLICA"}
    allowed_states = {"CERRADO", "HUECO_CIENTIFICO_ETIQUETADO"}
    for index, row in enumerate(rows, 2):
        key = row["id_busqueda"]
        for column in SEARCH_MATRIX_COLUMNS:
            if not row[column].strip():
                add(findings, "AF611", SEARCH_MATRIX, f"Celda obligatoria vacía: {column}", index, key)
        if not valid_iso_date(row["fecha"]):
            add(findings, "AF613", SEARCH_MATRIX, "Fecha inválida o posterior al corte", index, key)
        if row["prioridad"] not in allowed_priorities:
            add(findings, "AF622", SEARCH_MATRIX, "Prioridad fuera del vocabulario", index, key)
        if row["estado_registro"] not in allowed_states:
            add(findings, "AF623", SEARCH_MATRIX, "Registro de búsqueda no cerrado", index, key)
        if row["prioridad"] in {"P0", "P1"} and any(row[field] == "n/a" for field in ("consulta_exacta", "servicio", "fuentes_evaluadas", "resultado")):
            add(findings, "AF614", SEARCH_MATRIX, "Búsqueda P0/P1 incompleta", index, key)
        if row["prioridad"] == "P2" and row["desencadenante"] == "n/a":
            add(findings, "AF615", SEARCH_MATRIX, "P2 sin desencadenante", index, key)
        if BN_REF.fullmatch(row["clave_bn"]) and history_priorities:
            if row["prioridad"] != history_priorities.get(row["clave_bn"]):
                add(findings, "AF617", SEARCH_MATRIX, "Prioridad distinta de la historia BN", index, key)
        if not BN_REF.fullmatch(row["clave_bn"]) and row["clave_bn"] != "n/a":
            add(findings, "AF624", SEARCH_MATRIX, "clave_bn fuera del vocabulario", index, key)
        if index > 166:
            if row["huella_inicial_sha256"] not in {"n/a", "NO_APLICA"}:
                add(findings, "AF625", SEARCH_MATRIX, "Búsqueda nueva simula pertenecer al inventario congelado", index, key)
            for column in (
                "consulta_exacta", "servicio", "fuentes_evaluadas", "resultado",
                "cambio_realizado", "evidencia_final",
            ):
                if row[column].strip() in {"", "n/a", "NO_APLICA"}:
                    add(findings, "AF627", SEARCH_MATRIX, f"Búsqueda nueva incompleta: {column}", index, key)
    systematic = [row["bloque"] for row in baseline_rows if row["bloque"].startswith("actualización sección ")]
    if Counter(systematic) != Counter(f"actualización sección {number}" for number in range(19)):
        add(findings, "AF626", SEARCH_MATRIX, "Las actualizaciones sistemáticas 0–18 no aparecen exactamente una vez")
    seeds = [row for row in baseline_rows if row["bloque"] == "semilla obligatoria"]
    seed_dois = (
        "10.1038/s41586-026-10533-4",
        "10.1073/pnas.2600283123",
        "10.1103/vzxt-rpf8",
    )
    for doi in seed_dois:
        matching = [row for row in seeds if doi in " ".join(row.values())]
        if len(matching) != 1:
            add(findings, "AF616", SEARCH_MATRIX, f"Semilla obligatoria ausente o duplicada: {doi}")


def audit_lineage(ctx: AuditContext, findings: list[Finding]) -> None:
    path = ctx.path(TABLE_LINEAGE)
    if not path.exists():
        add(findings, "AF050", TABLE_LINEAGE, "Falta el linaje de tablas")
        return
    header, rows = read_dicts(path)
    required = {"table_id", "origen", "source_master_sha256", "source_table_ordinal", "source_start_line", "source_end_line", "source_header_sha256", "canonical_path", "transformaciones_documentadas"}
    if not required <= set(header):
        add(findings, "AF051", TABLE_LINEAGE, "Cabecera de linaje incompleta")
        return
    index_ids = {entry["id"] for entry in load_index(ctx)["tables"]}
    lineage_ids = [row["table_id"] for row in rows]
    if len(lineage_ids) != len(set(lineage_ids)) or set(lineage_ids) != index_ids:
        add(findings, "AF052", TABLE_LINEAGE, "Linaje e índice no coinciden uno a uno")
    for index, row in enumerate(rows, 2):
        for column in required:
            if not row[column].strip():
                add(findings, "AF051", TABLE_LINEAGE, f"Celda obligatoria vacía: {column}", index, row["table_id"])
        if row["origen"] == "maestro_v5" and row["source_master_sha256"] != ARCHIVE_SHA256:
            add(findings, "AF053", TABLE_LINEAGE, "Ancla del maestro incorrecta", index, row["table_id"])


def audit_key_map(
    ctx: AuditContext, findings: list[Finding], claim_ids: set[str],
) -> None:
    path = ctx.path(KEY_MAP)
    if not path.exists():
        add(findings, "AF540", KEY_MAP, "Falta el mapa final de claves")
        return
    header, rows = read_dicts(path)
    required = {"clave_pre_renumeracion", "clave_final", "cambio"}
    if not required <= set(header):
        add(findings, "AF541", KEY_MAP, "Cabecera del mapa incompleta")
        return
    before = [row["clave_pre_renumeracion"] for row in rows]
    after = [row["clave_final"] for row in rows]
    if len(before) != len(set(before)):
        add(findings, "AF542", KEY_MAP, "Clave pre-renumeración duplicada")
    if Counter(after) != Counter({claim_id: 1 for claim_id in claim_ids}):
        add(findings, "AF543", KEY_MAP, "El mapa no cubre cada C final exactamente una vez")
    baseline = [key for key in before if re.fullmatch(r"C-(?:\d{3}|1[0-7]\d{2}|18[0-3]\d|1840)", key)]
    if len(baseline) != BASELINE_CLAIM_COUNT or keyset_sha256(baseline) != BASELINE_CLAIM_KEYSET_SHA256:
        add(findings, "AF544", KEY_MAP, "El mapa no conserva las 1.840 C iniciales")
    for index, row in enumerate(rows, 2):
        if not all(row[column].strip() for column in required):
            add(findings, "AF541", KEY_MAP, "Celda obligatoria vacía", index, row.get("clave_pre_renumeracion", "n/a"))
        expected_change = "sí" if row["clave_pre_renumeracion"] != row["clave_final"] else "no"
        if row["cambio"] != expected_change:
            add(findings, "AF545", KEY_MAP, "Indicador de cambio incorrecto", index, row["clave_pre_renumeracion"])


def audit_final_answers(ctx: AuditContext, findings: list[Finding]) -> None:
    table = ctx.path("data/tablas/19/table-77-19-respuestas-a-las-seis-preguntas-de-cierre.csv")
    if not table.exists():
        add(findings, "AF700", str(table.relative_to(ctx.root)), "Falta la tabla de seis respuestas")
        return
    _, rows = read_dicts(table)
    if len(rows) != 6:
        add(findings, "AF710", str(table.relative_to(ctx.root)), "La tabla final debe contener seis respuestas")
    questions = [row.get("pregunta", "") for row in rows]
    if questions != FINAL_QUESTIONS:
        add(findings, "AF713", str(table.relative_to(ctx.root)), "Las seis preguntas no reproducen literalmente el encargo y su orden")
    for index, row in enumerate(rows, 2):
        text = " ".join(row.values())
        if not CLAIM_REF.search(text) or not expanded_refs(text, "S"):
            add(findings, "AF711", str(table.relative_to(ctx.root)), "Respuesta final sin C y S", index)
        if EDITORIAL_PLACEHOLDER.search(text):
            add(findings, "AF712", str(table.relative_to(ctx.root)), "Respuesta final conserva marcador provisional", index)


def audit_report(ctx: AuditContext, findings: list[Finding]) -> None:
    path = ctx.path(AUDIT_REPORT)
    if not path.exists():
        add(findings, "AF070", AUDIT_REPORT, "Falta el informe principal de auditoría")
        return
    text = path.read_text(encoding="utf-8")
    normalized = normalize_markdown_literal(text).casefold()
    required_headings = (
        "## metodología",
        "## veredicto",
        "## hallazgos por severidad",
        "## correcciones",
        "## límites restantes",
    )
    for heading in required_headings:
        if heading not in text.casefold():
            add(findings, "AF071", AUDIT_REPORT, f"Falta el epígrafe obligatorio {heading}")
    required_literals = (
        CUTOFF,
        PROMPT_SHA256,
        FROZEN_FINDINGS_MANIFEST_SHA256,
        "P0 abiertos: 0",
        "P1 abiertos: 0",
        Path(SECOND_REVIEW).name,
        "make verify",
    )
    for literal in required_literals:
        haystack = normalized if literal.startswith(("P0 ", "P1 ")) else text.casefold()
        if literal.casefold() not in haystack:
            add(findings, "AF072", AUDIT_REPORT, f"El informe no documenta: {literal}")


def audit_content_trace(
    ctx: AuditContext, findings: list[Finding], claim_ids: set[str],
) -> list[dict[str, str]]:
    path = ctx.path(CONTENT_TRACE)
    if not path.exists():
        add(findings, "AF730", CONTENT_TRACE, "Falta la matriz de trazabilidad por segmento")
        return []
    header, rows = read_dicts(path)
    if header != CONTENT_TRACE_COLUMNS:
        add(findings, "AF731", CONTENT_TRACE, "Cabecera distinta del contrato exacto")
        return []
    expected_ids = [f"TC-{number:05d}" for number in range(1, len(rows) + 1)]
    if [row["id_segmento"] for row in rows] != expected_ids:
        add(findings, "AF732", CONTENT_TRACE, "Claves TC discontinuas, duplicadas o desordenadas")
    referenced_claims: set[str] = set()
    for index, row in enumerate(rows, 2):
        key = row["id_segmento"]
        if row["tipo"] not in {"prosa", "arista", "celda"}:
            add(findings, "AF733", CONTENT_TRACE, "Tipo de segmento fuera del vocabulario", index, key)
        expected_content_hash = sha256_bytes((row["contenido"] + "\n").encode("utf-8"))
        if row["sha256_contenido"] != expected_content_hash:
            add(findings, "AF734", CONTENT_TRACE, "Huella de contenido desactualizada", index, key)
        refs = expanded_refs(row["afirmaciones"], "C-")
        referenced_claims.update(refs)
        if not refs or any(ref not in claim_ids for ref in refs):
            add(findings, "AF735", CONTENT_TRACE, "Segmento sin C finales válidas", index, key)
        if row["metodo_mapeo"] == "SIN_TRAZABILIDAD" or row["estado_revision"] != "REVISADA":
            add(findings, "AF736", CONTENT_TRACE, "Segmento no trazado o no revisado", index, key)
        if "lexic" in row["metodo_mapeo"].casefold():
            add(
                findings, "AF739", CONTENT_TRACE,
                "Una correspondencia léxica puede sugerir candidatos, pero no acreditar la revisión",
                index, key,
            )
        if not ctx.path(row["ruta"]).is_file():
            add(findings, "AF737", CONTENT_TRACE, "Ruta del segmento inexistente", index, key)
    missing_claims = sorted(claim_ids - referenced_claims, key=natural_key)
    for claim_id in missing_claims:
        add(
            findings, "AF738", CONTENT_TRACE,
            "C final vigente ausente de la trazabilidad segmentada",
            key=claim_id,
        )
    return rows


def review_object_fingerprint(
    stratum: str, row: dict[str, str],
) -> str:
    if stratum == "AFIRMACION" and HEX_SHA256.fullmatch(row.get("huella_final_sha256", "")):
        return row["huella_final_sha256"]
    if stratum == "FUENTE" and HEX_SHA256.fullmatch(row.get("huella_final_sha256", "")):
        return row["huella_final_sha256"]
    return canonical_row_fingerprint(row)


def audit_second_review(ctx: AuditContext, findings: list[Finding]) -> None:
    path = ctx.path(SECOND_REVIEW)
    if not path.exists():
        add(findings, "AF740", SECOND_REVIEW, "Falta la segunda revisión independiente")
        return
    dependencies = (CLAIM_MATRIX, SOURCE_MATRIX, REQUIREMENT_MATRIX, CONTENT_TRACE)
    if any(not ctx.path(relative).exists() for relative in dependencies):
        add(findings, "AF741", SECOND_REVIEW, "No puede validar la segunda revisión sin sus cuatro matrices objeto")
        return
    claim_header, claim_rows = read_dicts(ctx.path(CLAIM_MATRIX))
    source_header, source_rows = read_dicts(ctx.path(SOURCE_MATRIX))
    requirement_header, requirement_rows = read_dicts(ctx.path(REQUIREMENT_MATRIX))
    trace_header, trace_rows = read_dicts(ctx.path(CONTENT_TRACE))
    if (
        claim_header != CLAIM_MATRIX_COLUMNS
        or source_header != SOURCE_MATRIX_COLUMNS
        or requirement_header != REQUIREMENT_MATRIX_COLUMNS
        or trace_header != CONTENT_TRACE_COLUMNS
    ):
        add(findings, "AF741", SECOND_REVIEW, "Las matrices objeto no cumplen sus cabeceras exactas")
        return

    correction: dict[str, dict[str, str]] = {"AFIRMACION": {}, "FUENTE": {}}
    conforming: dict[str, dict[str, str]] = {
        "AFIRMACION": {}, "FUENTE": {}, "REQUISITO": {},
        "TRAZABILIDAD_PROSA": {}, "TRAZABILIDAD_ARISTA": {},
        "TRAZABILIDAD_CELDA": {},
    }
    for row in claim_rows:
        if re.fullmatch(r"C-\d{3,4}", row["clave_inicial"]):
            if row["severidad_inicial"] in {"P0", "P1"}:
                correction["AFIRMACION"][row["clave_inicial"]] = row
            if row["estado_inicial"] == "CONFORME":
                conforming["AFIRMACION"][row["clave_inicial"]] = row
    for row in source_rows:
        if re.fullmatch(r"S\d{2,3}", row["clave_inicial"]):
            if row["severidad_inicial"] in {"P0", "P1"}:
                correction["FUENTE"][row["clave_inicial"]] = row
            if row["veredicto_inicial"] == "CONFORME":
                conforming["FUENTE"][row["clave_inicial"]] = row
    # La revisión de requisitos no se limita a los que ya parecían conformes
    # en el corte inicial: una disposición PARCIAL/FALTA también puede haber
    # sido remediada incorrectamente. Los 483 mandatos forman el estrato
    # completo y cualquier fallo observado obliga a expandirlo al 100 %.
    for row in requirement_rows:
        conforming["REQUISITO"][row["id_requisito"]] = row
    trace_strata = {
        "prosa": "TRAZABILIDAD_PROSA",
        "arista": "TRAZABILIDAD_ARISTA",
        "celda": "TRAZABILIDAD_CELDA",
    }
    for row in trace_rows:
        stratum = trace_strata.get(row["tipo"])
        if stratum and row["estado_revision"] == "REVISADA":
            conforming[stratum][row["id_segmento"]] = row

    header, rows = read_dicts(path)
    if header != SECOND_REVIEW_COLUMNS:
        add(findings, "AF742", SECOND_REVIEW, "Cabecera distinta del contrato exacto")
        return
    expected_ids = [f"REV-{number:05d}" for number in range(1, len(rows) + 1)]
    if [row["id_revision"] for row in rows] != expected_ids:
        add(findings, "AF743", SECOND_REVIEW, "Claves REV discontinuas, duplicadas o desordenadas")

    reviewed_correction: defaultdict[str, Counter[str]] = defaultdict(Counter)
    reviewed_conforming: defaultdict[str, Counter[str]] = defaultdict(Counter)
    conforming_selection: defaultdict[str, dict[str, str]] = defaultdict(dict)
    failures: set[str] = set()
    for index, row in enumerate(rows, 2):
        key = row["clave_matriz"]
        stratum = row["estrato"]
        if row["tipo_revision"] == "CORRECCION_P0_P1":
            population = correction.get(stratum, {})
            reviewed_correction[stratum][key] += 1
            if row["seleccion"] != "CENSO_100_PCT":
                add(findings, "AF744", SECOND_REVIEW, "Corrección P0/P1 no marcada como censo", index, key)
        elif row["tipo_revision"] == "MUESTRA_CONFORME_15":
            population = conforming.get(stratum, {})
            reviewed_conforming[stratum][key] += 1
            conforming_selection[stratum][key] = row["seleccion"]
            if row["seleccion"] not in {"MUESTRA_ESTRATIFICADA_15_PCT", "EXPANSION_100_PCT"}:
                add(findings, "AF745", SECOND_REVIEW, "Selección de muestra fuera del vocabulario", index, key)
        else:
            population = {}
            add(findings, "AF746", SECOND_REVIEW, "Tipo de revisión fuera del vocabulario", index, key)
        if key not in population:
            add(findings, "AF747", SECOND_REVIEW, "Clave ajena al estrato/población declarados", index, key)
            object_row: dict[str, str] | None = None
        else:
            object_row = population[key]
        result = row["resultado"]
        if result not in {"CONFORME", "FALLO_CORREGIDO", "NO_CONFORME"}:
            add(findings, "AF748", SECOND_REVIEW, "Resultado de segunda revisión fuera del vocabulario", index, key)
        elif result in {"FALLO_CORREGIDO", "NO_CONFORME"}:
            failures.add(stratum)
            if row["accion"].strip() in {"", "n/a", "NO_APLICA"}:
                add(findings, "AF759", SECOND_REVIEW, "Fallo sin acción de remediación", index, key)
            if result == "NO_CONFORME":
                add(
                    findings, "AF761", SECOND_REVIEW,
                    "Fallo independiente abierto pendiente de remediación",
                    index, key,
                )
        if row["revisor_independiente"] in {"", "n/a", "NO_ASIGNADO"}:
            add(findings, "AF749", SECOND_REVIEW, "Revisor independiente no identificado", index, key)
        if row["declaracion_independencia"] != "INDEPENDIENTE_DEL_AUTOR_DE_LA_CORRECCION":
            add(findings, "AF750", SECOND_REVIEW, "Declaración de independencia ausente", index, key)
        if not valid_iso_date(row["fecha"]):
            add(findings, "AF751", SECOND_REVIEW, "Fecha de revisión inválida", index, key)
        expected_closure = "ABIERTO" if result == "NO_CONFORME" else "CERRADO"
        if row["estado_cierre"] != expected_closure:
            add(
                findings, "AF752", SECOND_REVIEW,
                f"Estado de cierre incompatible con {result or 'resultado vacío'}",
                index, key,
            )
        if row["evidencia"].strip() in {"", "n/a"} or row["accion"].strip() == "":
            add(findings, "AF753", SECOND_REVIEW, "Evidencia/acción de revisión ausente", index, key)
        if object_row is not None:
            expected = review_object_fingerprint(stratum, object_row)
            if row["huella_objeto_sha256"] != expected:
                add(findings, "AF754", SECOND_REVIEW, "Huella del objeto revisado desactualizada", index, key)

    for stratum, population in correction.items():
        if reviewed_correction[stratum] != Counter({key: 1 for key in population}):
            add(findings, "AF755", SECOND_REVIEW, f"Censo P0/P1 incompleto o duplicado: {stratum}")
    for stratum, population in conforming.items():
        expected_sample = deterministic_sample(set(population), stratum)
        actual_counter = reviewed_conforming[stratum]
        actual = set(actual_counter)
        if any(count != 1 for count in actual_counter.values()):
            add(findings, "AF756", SECOND_REVIEW, f"Muestra con claves duplicadas: {stratum}")
        if stratum in failures:
            if actual != set(population):
                add(findings, "AF757", SECOND_REVIEW, f"Fallo sin expansión al 100 % del estrato: {stratum}")
            for key in actual:
                expected_selection = (
                    "MUESTRA_ESTRATIFICADA_15_PCT"
                    if key in expected_sample else "EXPANSION_100_PCT"
                )
                if conforming_selection[stratum].get(key) != expected_selection:
                    add(findings, "AF760", SECOND_REVIEW, f"Etiquetado de muestra/expansión incorrecto: {stratum}", key=key)
        elif actual != expected_sample:
            add(findings, "AF758", SECOND_REVIEW, f"Muestra determinista del 15 % incorrecta: {stratum}")
        elif any(
            conforming_selection[stratum].get(key) != "MUESTRA_ESTRATIFICADA_15_PCT"
            for key in actual
        ):
            add(findings, "AF760", SECOND_REVIEW, f"Muestra sin etiqueta estratificada correcta: {stratum}")


def audit_repro_json(ctx: AuditContext, findings: list[Finding]) -> None:
    path = ctx.path(REPRO_JSON)
    if not path.exists():
        add(findings, "AF060", REPRO_JSON, "Falta el JSON reproducible")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        add(findings, "AF061", REPRO_JSON, f"JSON inválido: {error}")
        return
    if data.get("audit_id") != "research-audit-2026-08-08" or data.get("cutoff") != CUTOFF:
        add(findings, "AF062", REPRO_JSON, "Identidad o corte incorrectos")
    anchors = data.get("anchors", {})
    if anchors.get("prompt", {}).get("sha256") != PROMPT_SHA256 or anchors.get("archived_master", {}).get("sha256") != ARCHIVE_SHA256:
        add(findings, "AF063", REPRO_JSON, "Anclas reproducibles incorrectas")
    versions = data.get("versions", {})
    if not all(versions.get(key) for key in ("python", "git", "make", "platform")):
        add(findings, "AF065", REPRO_JSON, "Versiones de entorno incompletas")
    before = data.get("counts", {}).get("before", {})
    expected_before = {
        "claims": 1840,
        "sources": 525,
        "entities": 1536,
        "events": 111,
        "dates": 282,
        "hypotheses": 81,
        "magnitudes": 556,
        "negative_active": 68,
        "negative_historical": 106,
        "tables": 90,
    }
    if before != expected_before:
        add(findings, "AF066", REPRO_JSON, "Recuentos iniciales incorrectos")
    index = load_index(ctx)
    claims, _ = load_claims(ctx)
    sources, _ = load_sources(ctx)
    appendices = {
        entry["id"]: len(read_dicts(ctx.path(entry["csv_path"]))[1])
        for entry in index["tables"] if entry["category"] == "appendix"
    }
    active_bn = sum(
        len(read_dicts(ctx.path(entry["csv_path"]))[1])
        for entry in index["tables"] if entry["category"] == "negative"
    )
    expected_after = {
        "claims": len(claims),
        "sources": len(sources),
        "entities": appendices["appendix-b"],
        "events": appendices["appendix-c"],
        "dates": appendices["appendix-d"],
        "hypotheses": appendices["appendix-e"],
        "magnitudes": appendices["appendix-f"],
        "negative_active": active_bn,
        "negative_historical": 106,
        "tables": len(index["tables"]),
    }
    if data.get("counts", {}).get("after") != expected_after:
        add(findings, "AF067", REPRO_JSON, "Recuentos finales desactualizados")
    command_rows = data.get("commands", [])
    command_names = {
        row.get("name") for row in command_rows if isinstance(row, dict)
    }
    required_commands = {
        "make verify (workspace)",
        "python3 scripts/audit_migration.py",
        "git diff --check",
        "make verify (isolated copy)",
        "double render idempotence",
    }
    for name in required_commands:
        if name not in command_names:
            add(findings, "AF068", REPRO_JSON, f"Comando reproducible no documentado: {name}")
    for row in command_rows:
        if isinstance(row, dict) and set(row) & {"status", "result", "exit_code", "passed", "success"}:
            add(findings, "AF073", REPRO_JSON, "El JSON no puede autoatestiguar resultados de comandos")
    snapshot = data.get("snapshot", {})
    if (
        snapshot.get("external_path", "").rstrip("/")
        != SNAPSHOT_EXTERNAL_PATH.rstrip("/")
        or snapshot.get("frozen_findings_manifest_sha256")
        != FROZEN_FINDINGS_MANIFEST_SHA256
        or snapshot.get("head") != SNAPSHOT_HEAD
    ):
        add(findings, "AF069", REPRO_JSON, "Identidad exacta de la instantánea externa incorrecta")
    expected_frozen = {
        "claims_audit_rows_sha256": BASELINE_CLAIM_AUDIT_SHA256,
        "sources_audit_rows_sha256": BASELINE_SOURCE_AUDIT_SHA256,
        "requirements_audit_rows_sha256": BASELINE_REQUIREMENT_AUDIT_SHA256,
        "searches_audit_rows_sha256": BASELINE_SEARCH_AUDIT_SHA256,
        "claims_corpus_rows_sha256": BASELINE_CLAIM_CORPUS_SHA256,
        "sources_corpus_rows_sha256": BASELINE_SOURCE_CORPUS_SHA256,
    }
    if data.get("frozen_aggregates") != expected_frozen:
        add(findings, "AF074", REPRO_JSON, "Agregados congelados ausentes o incorrectos")
    for relative in (
        CLAIM_MATRIX, SOURCE_MATRIX, REQUIREMENT_MATRIX, SEARCH_MATRIX,
        NEGATIVE_HISTORY, TABLE_LINEAGE, KEY_MAP, AUDIT_REPORT,
        SECOND_REVIEW, CONTENT_TRACE,
    ):
        if not ctx.path(relative).exists():
            add(findings, "AF064", REPRO_JSON, f"Artefacto reproducible ausente: {relative}")
            continue
        recorded = data.get("artifacts", {}).get(relative, {}).get("sha256")
        if recorded != sha256_file(ctx.path(relative)):
            add(findings, "AF064", REPRO_JSON, f"Hash de artefacto desactualizado: {relative}")


def run(ctx: AuditContext) -> list[Finding]:
    findings: list[Finding] = []
    audit_anchors(ctx, findings)
    audit_index(ctx, findings)
    claims, _ = audit_claims(ctx, findings)
    # Una C explícitamente marcada como tombstone conserva linaje, pero no
    # finge presencia sustantiva. En cambio, una proposición histórica con
    # Vigencia=superada (p. ej. una clasificación abandonada) sí se traza.
    audit_claim_bidirectionality(
        ctx,
        findings,
        {row["#"] for row in claims if not is_auditable_tombstone(row)},
    )
    sources, _ = audit_sources(ctx, findings, claims)
    audit_matrices(ctx, findings, claims, sources)
    audit_requirements(
        ctx, findings, {row["#"] for row in claims},
        {row["clave"] for row in sources},
    )
    audit_appendices(ctx, findings, claims, {row["clave"] for row in sources})
    audit_negative_history(ctx, findings)
    audit_searches(ctx, findings)
    audit_lineage(ctx, findings)
    audit_key_map(ctx, findings, {row["#"] for row in claims})
    audit_final_answers(ctx, findings)
    audit_report(ctx, findings)
    audit_content_trace(
        ctx, findings,
        {row["#"] for row in claims if not is_auditable_tombstone(row)},
    )
    audit_second_review(ctx, findings)
    audit_repro_json(ctx, findings)
    for relative in (
        "data/afirmaciones", "data/apendices/D_fechas.csv",
        "data/apendices/F_magnitudes.csv", "data/tablas", "docs/secciones",
    ):
        path = ctx.path(relative)
        paths = path.rglob("*") if path.is_dir() else [path]
        for item in paths:
            if item.is_file() and item.suffix in {".csv", ".md"}:
                text = item.read_text(encoding="utf-8")
                if PROHIBITED_DERIVATIONS.search(text):
                    add(findings, "AF401", str(item.relative_to(ctx.root)), "Permanece lenguaje de derivación prohibida")
    return sorted(set(findings))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    findings = run(AuditContext(args.root))
    payload = {
        "audit_id": "research-audit-2026-08-08",
        "cutoff": CUTOFF,
        "finding_count": len(findings),
        "findings": [asdict(finding) for finding in findings],
    }
    if args.json:
        args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if findings:
        print(f"AUDITORÍA INTEGRAL FALLIDA: {len(findings)} hallazgo(s)")
        for finding in findings:
            where = f"{finding.path}:{finding.row}" if finding.row else finding.path
            print(f"- {finding.code} {where} [{finding.key}]: {finding.message}")
        return 1
    print("AUDITORÍA INTEGRAL CORRECTA: matrices, linaje, fuentes, C, D/F, BN y anclas cerrados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
