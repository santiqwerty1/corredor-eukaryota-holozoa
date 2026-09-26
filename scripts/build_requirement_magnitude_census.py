#!/usr/bin/env python3
"""Censa magnitudes desde los requisitos literales, nunca desde el apéndice F.

El inventario de alcance y la especificación terminal son entradas versionadas y
revisables. Este programa se limita a comprobarlas contra el prompt vivo, las C
canónicas, el apéndice A y los registros BN/Q ejecutados; no calcula valores.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = Path("docs/auditorias/matriz_requisitos_2026-08-08.csv")
CLASSIFICATION = Path("data/auditoria/clasificacion_literales_cuantitativos_v1.csv")
SPECIFICATION = Path("data/auditoria/especificacion_magnitudes_por_requisito_v1.csv")
SEMANTIC_CONTRACTS = Path("data/auditoria/contratos_semanticos_magnitudes_v1.csv")
OUTPUT = Path("data/auditoria/magnitudes_por_requisito_v1.csv")

CLASS_HEADER = ["id_requisito", "clasificacion", "justificacion_literal"]
SPEC_HEADER = [
    "id_magnitud", "id_requisito", "fragmento_literal", "magnitud_solicitada",
    "desenlace", "afirmaciones_terminales", "registro_hueco", "razon_hueco",
    "transformacion_editorial",
]
CONTRACT_HEADER = ["id_magnitud", "contrato_semantico", "objeto_literal_verificado"]
OUTPUT_HEADER = [
    "version_esquema", "id_magnitud", "id_requisito", "ancla_prompt",
    "requisito_literal", "magnitud_solicitada", "desenlace",
    "valor_o_hueco_terminal", "afirmaciones_terminales", "fuentes_y_localizadores",
    "registro_hueco", "busqueda_ejecutada", "razon_hueco",
    "transformacion_editorial", "sha256_requisito", "sha256_especificacion",
]

ALLOWED_CLASSIFICATIONS = {
    "MAGNITUD_PEDIDA", "REGLA_CUANTITATIVA", "CONTEXTO_NO_MAGNITUD",
}
CLAIM = re.compile(r"\bC-\d{3,5}\b")
SOURCE = re.compile(r"(?:^|[;,])\s*(S\d{2,4})\b")
GAP = re.compile(r"\b(?:BN-\d{3}|Q-\d{4})\b")
NUMBER = re.compile(
    r"(?<![A-Za-zÁÉÍÓÚÜÑáéíóúüñ])(?:[<>≤≥~≈]?\s*[−-]?\d|\d\s*[×^])"
)

# Detector deliberadamente de alta sensibilidad. Toda coincidencia debe quedar
# clasificada en el inventario; añadir un nuevo literal cuantitativo rompe el build.
QUANTITATIVE_PATTERNS = (
    r"\bsoporte cuantitativo\b", r"\bproporciones?\b", r"\bmagnitud\b",
    r"\bcu[aá]nt(?:o|a|os|as)\b", r"\bqu[eé] edad\b", r"\bedad(?:es)?\b",
    r"\btama[nñ]o\b", r"\bduraci[oó]n\b", r"\btasas?\b", r"\bfrecuencia\b",
    r"\bdensidad(?:es)?\b", r"\babundancias?\b", r"\btemperatura\b",
    r"\bprofundidades?\b", r"\bdistancias?\b", r"\brangos?\b",
    r"\bintervalos?\b", r"\bincertidumbres?\b", r"\bmargen de error\b",
    r"\bcifra(?:s)?\b", r"\bporcentajes?\b", r"\bfracci[oó]n\b",
    r"\bn[uú]mero (?:de|total)\b", r"\bvalores? de ne\b", r"\bgeneraciones?\b",
    r"\bord(?:en|enes) de magnitud\b", r"\bgenes conserva\b",
    r"\bvalor(?:es)? publicados?\b", r"\bumbrales?\b", r"\brendimiento energ[eé]tico\b",
    r"\bor[ií]genes?\b", r"\brecuentos?\b", r"\bqu[eé] cuesta\b", r"\bcoste doble\b",
)
QUANTITATIVE = re.compile("|".join(QUANTITATIVE_PATTERNS), re.IGNORECASE)


def _normal(text: str) -> str:
    return "".join(
        char for char in unicodedata.normalize("NFKD", text.casefold())
        if not unicodedata.combining(char)
    )


def _read(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise RuntimeError(f"CSV sin cabecera: {path}")
        return reader.fieldnames, list(reader)


def _require_header(path: Path, actual: list[str], expected: list[str]) -> None:
    if actual != expected:
        raise RuntimeError(f"Cabecera inesperada en {path}: {actual!r}")


def _row_digest(header: list[str], row: dict[str, str]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=header, quoting=csv.QUOTE_ALL,
                            lineterminator="\n")
    writer.writerow(row)
    return hashlib.sha256(stream.getvalue().encode("utf-8")).hexdigest()


def _claim_index(root: Path) -> dict[str, dict[str, str]]:
    index: dict[str, dict[str, str]] = {}
    for path in sorted((root / "data/afirmaciones").glob("*.csv")):
        _, rows = _read(path)
        for row in rows:
            claim_id = row["#"].strip()
            if claim_id in index:
                raise RuntimeError(f"C duplicada: {claim_id}")
            index[claim_id] = row
    return index


def _negative_search_index(root: Path) -> dict[str, dict[str, str]]:
    index: dict[str, dict[str, str]] = {}
    for path in sorted((root / "data/busquedas_negativas").glob("*.csv")):
        _, rows = _read(path)
        for row in rows:
            key = row.get("clave", "").strip()
            if not key:
                continue
            if key in index:
                raise RuntimeError(f"registro negativo duplicado: {key}")
            payload = " ; ".join(value.strip() for value in row.values() if value and value.strip())
            query = " ; ".join(
                value.strip() for field, value in row.items()
                if value and value.strip() and any(token in _normal(field) for token in ("termin", "consulta"))
            )
            result = " ; ".join(
                value.strip() for field, value in row.items()
                if value and value.strip() and any(token in _normal(field) for token in ("resultado", "motivo", "consecuencia"))
            )
            index[key] = {"payload": payload, "query": query, "result": result}
    # Se admiten Q solo si existe un registro versionado y ejecutado con consulta y resultado.
    q_path = root / "data/auditoria/busquedas_ejecutadas.csv"
    if q_path.exists():
        _, rows = _read(q_path)
        for row in rows:
            key = (row.get("clave") or row.get("id") or "").strip()
            if key:
                index[key] = {
                    "payload": " ; ".join(v.strip() for v in row.values() if v.strip()),
                    "query": (row.get("consulta") or row.get("terminos") or "").strip(),
                    "result": (row.get("resultado") or "").strip(),
                }
    return index


def _has_source_localizer(text: str) -> bool:
    if "sin localizar con mayor precisión" in text.casefold():
        return False
    matches = list(SOURCE.finditer(text))
    if not matches:
        return False
    for pos, match in enumerate(matches):
        end = matches[pos + 1].start() if pos + 1 < len(matches) else len(text)
        tail = text[match.end():end].strip(" ,;")
        if len(tail) < 2 or _normal(tail) in {"n/a", "na"}:
            return False
    return True


def _contains(text: str, pattern: str) -> bool:
    return re.search(pattern, _normal(text), re.IGNORECASE) is not None


def _validate_semantic_contract(
    magnitude_id: str,
    contract: str,
    outcome: str,
    claim_rows: list[dict[str, str]],
    search: dict[str, str] | None,
) -> None:
    claim_text = " ; ".join(
        " ; ".join((row["Afirmación"], row["Sujeto"], row["Objeto"], row["Fuente"]))
        for row in claim_rows
    )
    gap_text = search["payload"] if search else ""
    text = claim_text if outcome == "VALOR_PUBLICADO" else gap_text
    if contract == "NIVEL_OXIGENO" and outcome == "VALOR_PUBLICADO":
        for row in claim_rows:
            if not _contains(row["Objeto"], r"(\bo2\b|\bpal\b|\bnm\b|\bum\b|umol)"):
                raise RuntimeError(
                    f"{magnitude_id}: objeto terminal no es una cifra de oxígeno"
                )
            if _contains(row["Objeto"], r"(delta\s*13c|δ13c)"):
                raise RuntimeError(
                    f"{magnitude_id}: δ13C no puede reasignarse como cifra de oxígeno"
                )
        return
    if contract == "LATENCIA_RESPUESTA" and outcome == "VALOR_PUBLICADO":
        required = r"(expuest|inversion|inicio de agregacion|desagregacion|reagregacion)"
        forbidden = r"(metodos|culture conditions|ciclo nuclear|cultivo de 14 dias)"
        for row in claim_rows:
            row_text = " ; ".join((row["Afirmación"], row["Sujeto"], row["Objeto"], row["Fuente"]))
            if not _contains(row_text, required) or _contains(row_text, forbidden):
                raise RuntimeError(
                    f"{magnitude_id}: tiempo de protocolo, cultivo o ciclo no es latencia de respuesta"
                )
        return
    rules: dict[str, tuple[str, str]] = {
        "DISTRIBUCION_FOSIL_DEFENSIVA": (r"(vsm|acritarc|defensiv|distribucion de tamano)", r""),
        "RANGO_TAMANO_CELULAR": (r"(rango.{0,40}celul|tamano celular.{0,80}procariot)", r""),
        "PERDIDA_GENES_NUMERO_TIEMPO": (r"(numero de genes|genes perdidos).{0,100}(tiempo|transcurr)", r"universal"),
        "CIFRA_HGT_SUSTANTIVA": (r"(cifras sustantivas|frecuencia).{0,100}(hgt|transfer)", r"tamano de muestreo"),
        "DURACION_GLACIACION": (r"(duracion).{0,100}(glaciacion|sturt|marino)", r"oae1|oae2"),
        "DURACION_TRANSICION_REDOX": (r"duracion.{0,100}(cambio|transicion).{0,100}redox", r"duracion unica|constante universal"),
        "COSTE_DOBLE_ISOGAMIA": (r"(coste doble|twofold).{0,120}(isogam|protist)", r""),
    }
    if contract not in rules:
        raise RuntimeError(f"{magnitude_id}: contrato semántico desconocido {contract}")
    required, forbidden = rules[contract]
    if not _contains(text, required):
        raise RuntimeError(f"{magnitude_id}: objeto terminal no satisface contrato {contract}")
    if forbidden and _contains(text, forbidden):
        raise RuntimeError(f"{magnitude_id}: emparejamiento no equivalente prohibido por {contract}")


def build(root: Path) -> bytes:
    req_header, req_rows = _read(root / REQUIREMENTS)
    requirements = {row["id_requisito"]: row for row in req_rows}
    detected = {
        row["id_requisito"] for row in req_rows
        if QUANTITATIVE.search(row["requisito_literal"])
    }

    class_header, class_rows = _read(root / CLASSIFICATION)
    _require_header(root / CLASSIFICATION, class_header, CLASS_HEADER)
    classifications: dict[str, str] = {}
    for row in class_rows:
        req_id = row["id_requisito"].strip()
        value = row["clasificacion"].strip()
        if req_id in classifications:
            raise RuntimeError(f"literal cuantitativo clasificado dos veces: {req_id}")
        if req_id not in requirements:
            raise RuntimeError(f"clasificación de requisito inexistente: {req_id}")
        if value not in ALLOWED_CLASSIFICATIONS:
            raise RuntimeError(f"clasificación inválida en {req_id}: {value}")
        if len(row["justificacion_literal"].strip()) < 25:
            raise RuntimeError(f"justificación insuficiente en {req_id}")
        classifications[req_id] = value
    missing = sorted(detected - classifications.keys())
    surplus = sorted(classifications.keys() - detected)
    if missing:
        raise RuntimeError(f"literal cuantitativo sin clasificación/fila: {missing}")
    if surplus:
        raise RuntimeError(f"clasificación sin coincidencia del detector: {surplus}")

    spec_header, spec_rows = _read(root / SPECIFICATION)
    _require_header(root / SPECIFICATION, spec_header, SPEC_HEADER)
    claims = _claim_index(root)
    _, source_rows = _read(root / "data/apendices/A_fuentes.csv")
    source_keys = {row["clave"].strip() for row in source_rows}
    searches = _negative_search_index(root)
    contract_header, contract_rows = _read(root / SEMANTIC_CONTRACTS)
    _require_header(root / SEMANTIC_CONTRACTS, contract_header, CONTRACT_HEADER)
    contracts: dict[str, str] = {}
    for row in contract_rows:
        magnitude_id = row["id_magnitud"].strip()
        if magnitude_id in contracts:
            raise RuntimeError(f"contrato semántico duplicado: {magnitude_id}")
        if len(row["objeto_literal_verificado"].strip()) < 30:
            raise RuntimeError(f"objeto literal insuficiente en contrato {magnitude_id}")
        contracts[magnitude_id] = row["contrato_semantico"].strip()
    output: list[dict[str, str]] = []
    seen_magnitudes: set[str] = set()
    covered_requirements: set[str] = set()
    for row in spec_rows:
        magnitude_id = row["id_magnitud"].strip()
        req_id = row["id_requisito"].strip()
        if magnitude_id in seen_magnitudes:
            raise RuntimeError(f"magnitud duplicada: {magnitude_id}")
        seen_magnitudes.add(magnitude_id)
        if classifications.get(req_id) != "MAGNITUD_PEDIDA":
            raise RuntimeError(f"{magnitude_id}: {req_id} no está clasificado MAGNITUD_PEDIDA")
        literal = requirements[req_id]["requisito_literal"]
        fragment = row["fragmento_literal"].strip()
        if not fragment or _normal(fragment) not in _normal(literal):
            raise RuntimeError(f"{magnitude_id}: fragmento no pertenece al literal {req_id}")
        if len(row["magnitud_solicitada"].strip()) < 12:
            raise RuntimeError(f"{magnitude_id}: magnitud no descrita nominalmente")
        if row["transformacion_editorial"].strip() != "NINGUNA":
            raise RuntimeError(f"{magnitude_id}: transformación editorial prohibida")

        outcome = row["desenlace"].strip()
        claim_ids = CLAIM.findall(row["afirmaciones_terminales"])
        gap_ids = GAP.findall(row["registro_hueco"])
        if outcome == "VALOR_PUBLICADO":
            if not claim_ids or gap_ids or row["razon_hueco"].strip():
                raise RuntimeError(f"{magnitude_id}: valor requiere C y no admite hueco")
            values: list[str] = []
            sources: list[str] = []
            for claim_id in claim_ids:
                if claim_id not in claims:
                    raise RuntimeError(f"{magnitude_id}: C inexistente {claim_id}")
                claim = claims[claim_id]
                exact = claim["Objeto"].strip()
                if not NUMBER.search(exact):
                    raise RuntimeError(f"{magnitude_id}: cifra sin valor literal en {claim_id}")
                source = claim["Fuente"].strip()
                if not _has_source_localizer(source):
                    raise RuntimeError(f"{magnitude_id}: cifra sin fuente/localizador en {claim_id}")
                missing_sources = sorted(set(SOURCE.findall(source)) - source_keys)
                if missing_sources:
                    raise RuntimeError(f"{magnitude_id}: S ausentes de A {missing_sources}")
                values.append(f"{claim_id}: {exact}")
                sources.append(f"{claim_id}: {source}")
            _validate_semantic_contract(
                magnitude_id, contracts[magnitude_id], outcome,
                [claims[claim_id] for claim_id in claim_ids], None,
            ) if magnitude_id in contracts else None
            terminal = " ; ".join(values)
            source_text = " ; ".join(sources)
            search_text = "n/a"
            reason = "n/a"
            gap_text = "n/a"
        elif outcome in {"HUECO_EXPLICITO", "HUECO_TRAZABILIDAD"}:
            if claim_ids or len(gap_ids) != 1:
                raise RuntimeError(f"{magnitude_id}: hueco requiere exactamente un BN/Q y ninguna C")
            gap_id = gap_ids[0]
            search = searches.get(gap_id)
            if not search:
                raise RuntimeError(f"{magnitude_id}: hueco sin búsqueda versionada {gap_id}")
            if len(search["query"]) < 12 or len(search["result"]) < 20:
                raise RuntimeError(f"{magnitude_id}: hueco sin consulta y resultado suficientes {gap_id}")
            reason = row["razon_hueco"].strip()
            if len(reason) < 30:
                raise RuntimeError(f"{magnitude_id}: hueco sin razón específica")
            if outcome == "HUECO_EXPLICITO":
                terminal = "NO HAY VALOR PUBLICADO LOCALIZADO"
                source_text = "n/a"
            else:
                terminal = (
                    "VALOR PUBLICADO LOCALIZADO SIN C CANÓNICA; "
                    "NO SE TRANSFORMA NI SE INCORPORA COMO VALOR TERMINAL ; "
                    + search["result"]
                )
                source_text = f"{gap_id}: {search['result']}"
            search_text = search["payload"]
            gap_text = gap_id
            _validate_semantic_contract(
                magnitude_id, contracts[magnitude_id], outcome, [], search,
            ) if magnitude_id in contracts else None
        else:
            raise RuntimeError(f"{magnitude_id}: desenlace inválido {outcome}")

        covered_requirements.add(req_id)
        output.append({
            "version_esquema": "1",
            "id_magnitud": magnitude_id,
            "id_requisito": req_id,
            "ancla_prompt": requirements[req_id]["ancla"],
            "requisito_literal": literal,
            "magnitud_solicitada": row["magnitud_solicitada"].strip(),
            "desenlace": outcome,
            "valor_o_hueco_terminal": terminal,
            "afirmaciones_terminales": "; ".join(claim_ids) if claim_ids else "n/a",
            "fuentes_y_localizadores": source_text,
            "registro_hueco": gap_text,
            "busqueda_ejecutada": search_text,
            "razon_hueco": reason,
            "transformacion_editorial": "NINGUNA",
            "sha256_requisito": _row_digest(req_header, requirements[req_id]),
            "sha256_especificacion": _row_digest(spec_header, row),
        })
    expected = {key for key, value in classifications.items() if value == "MAGNITUD_PEDIDA"}
    uncovered = sorted(expected - covered_requirements)
    if uncovered:
        raise RuntimeError(f"literal cuantitativo sin fila terminal de magnitud: {uncovered}")
    unknown_contracts = sorted(contracts.keys() - seen_magnitudes)
    if unknown_contracts:
        raise RuntimeError(f"contratos para magnitudes inexistentes: {unknown_contracts}")

    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=OUTPUT_HEADER, quoting=csv.QUOTE_ALL,
                            lineterminator="\n")
    writer.writeheader()
    writer.writerows(output)
    return stream.getvalue().encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    payload = build(root)
    path = root / OUTPUT
    if args.write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        print(f"MAGNITUDES DESDE REQUISITOS: {payload.count(bytes([10])) - 1} filas")
        return 0
    if not path.exists() or path.read_bytes() != payload:
        print(f"CENSO REQUISITO→MAGNITUD DESACTUALIZADO: {OUTPUT}")
        return 1
    print(f"CENSO REQUISITO→MAGNITUD VERIFICADO: {payload.count(bytes([10])) - 1} filas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
