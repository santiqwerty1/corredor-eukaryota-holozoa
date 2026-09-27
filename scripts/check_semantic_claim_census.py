#!/usr/bin/env python3
"""Valida la congelación y las dos revisiones semánticas de todas las C.

El control es deliberadamente mecánico: no genera dictámenes, no promueve
coincidencias léxicas y no interpreta disponibilidad como apoyo. Las decisiones
son artefactos manuales; este script impide omisiones, huellas obsoletas,
auto-revisión, discrepancias abiertas y aprobaciones sin evidencia nominal.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "data/auditoria/congelacion_censo_semantico_v1.json"
PRIMARY = ROOT / "data/auditoria/censo_semantico_afirmaciones_v1.csv"
SECONDARY = ROOT / "data/auditoria/segunda_revision_afirmaciones_v1.csv"
PROTOCOL = ROOT / "docs/auditorias/protocolo_censo_semantico_2026-08-13.md"
RESULTS = {"CONFORME", "NO_CONFORME", "NO_VERIFICABLE"}
HEX64 = re.compile(r"[0-9a-f]{64}")
UTC_TIMESTAMP = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
INDEPENDENCE_DECLARATION = "REVISION_INDEPENDIENTE_SIN_PARTICIPACION_EN_CENSO_PRIMARIO"
PLACEHOLDERS = {"", "n/a", "pendiente", "no verificado", "sin revisar", "x"}

PRIMARY_HEADER = [
    "version_censo", "id_afirmacion", "ruta_canonica", "sha256_fila",
    "atribucion", "componentes_atomicos", "fuentes_declaradas",
    "artefactos_verificados", "sha256_artefactos", "localizador_declarado",
    "localizador_verificado", "fragmento_control", "sha256_pasaje",
    "matriz_cobertura_componentes", "dependencias_y_huellas", "resultado",
    "motivo_dictamen", "limitaciones", "revisor", "fecha_utc",
    "version_protocolo",
]
SECONDARY_HEADER = [
    "version_revision", "id_afirmacion", "sha256_fila",
    "sha256_censo_primario", "resultado_independiente",
    "localizadores_reinspeccionados", "sha256_pasajes_reinspeccionados",
    "evidencia_dictamen", "discrepancia", "resolucion_discrepancia",
    "revisor_independiente", "declaracion_independencia", "fecha_utc",
]


def serialized(header: list[str], row: dict[str, str]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=header, quoting=csv.QUOTE_ALL, lineterminator="\n",
    )
    writer.writerow(row)
    return stream.getvalue().encode("utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def claim_inventory() -> dict[str, dict[str, str]]:
    claims: dict[str, dict[str, str]] = {}
    for path in sorted((ROOT / "data/afirmaciones").glob("*.csv")):
        relative = path.relative_to(ROOT).as_posix()
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise RuntimeError(f"Sin cabecera: {relative}")
            for row in reader:
                key = row["#"]
                if key in claims:
                    raise RuntimeError(f"C duplicada: {key}")
                claims[key] = {
                    "ruta": relative,
                    "sha256_fila": hashlib.sha256(
                        serialized(reader.fieldnames, row)
                    ).hexdigest(),
                    "atribucion": row["Atribución"],
                    "fuente": row["Fuente"],
                }
    return dict(sorted(claims.items()))


def source_artifacts() -> dict[str, str]:
    return {
        path.relative_to(ROOT).as_posix(): sha(path)
        for path in sorted((ROOT / "fuentes").glob("S*"))
        if path.is_file()
    }


def control_paths() -> tuple[Path, ...]:
    return (
        ROOT / "data/apendices/A_fuentes.csv",
        ROOT / "docs/auditorias/matriz_fuentes_2026-08-08.csv",
        ROOT / "exports/acceso_fuentes.csv",
    )


def review_artifacts() -> dict[str, str]:
    """Congela todos los artefactos locales admisibles para glosas y BN.

    No incluye las propias salidas del censo: una revisión no puede usarse a sí
    misma como evidencia. Las filas C ya quedan fijadas por ``afirmaciones``;
    los archivos de control se registran una sola vez en su propio catálogo.
    """
    roots = [
        ROOT / "data/apendices",
        ROOT / "data/tablas",
        ROOT / "data/busquedas_negativas",
        ROOT / "docs/secciones",
    ]
    paths = [path for base in roots for path in base.rglob("*") if path.is_file()]
    paths.extend(
        path for path in (ROOT / "data/auditoria").glob("*.csv")
        if path not in {PRIMARY, SECONDARY}
    )
    paths.extend([ROOT / "data/table_index.json", ROOT / "data/table_lineage.csv"])
    return {
        path.relative_to(ROOT).as_posix(): sha(path)
        for path in sorted(set(paths) - set(control_paths())) if path.exists()
    }


def inventory_payload() -> dict[str, object]:
    """Inventario vivo reproducible, sin inventar una fecha de congelación."""
    protocol_hash = sha(PROTOCOL) if PROTOCOL.exists() else "PROTOCOLO_NO_DISPONIBLE"
    return {
        "version": "1",
        "version_protocolo": protocol_hash,
        "afirmaciones": claim_inventory(),
        "archivos_control": {
            path.relative_to(ROOT).as_posix(): sha(path) for path in control_paths()
        },
        "artefactos_fuente": source_artifacts(),
        "artefactos_revision": review_artifacts(),
    }


def parse_utc_timestamp(value: object) -> datetime | None:
    """Acepta solo instantes UTC canónicos y fechas de calendario reales."""
    if not isinstance(value, str) or not UTC_TIMESTAMP.fullmatch(value):
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def freeze_payload(fecha_congelacion: str) -> dict[str, object]:
    if parse_utc_timestamp(fecha_congelacion) is None:
        raise ValueError("fecha_congelacion debe ser un instante UTC válido YYYY-MM-DDTHH:MM:SSZ")
    return {**inventory_payload(), "fecha_congelacion": fecha_congelacion}


def load_csv(path: Path, header: list[str]) -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    if not path.exists():
        return [], [f"Falta artefacto: {path.relative_to(ROOT)}"]
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != header:
            return [], [
                f"Cabecera inesperada en {path.relative_to(ROOT)}: "
                f"{reader.fieldnames!r}"
            ]
        rows = list(reader)
    for line, row in enumerate(rows, 2):
        empty = [name for name in header if not row[name].strip()]
        if empty:
            errors.append(f"{path.name}:{line}: campos vacíos {empty}")
    return rows, errors


def canonical_json(value: str, field: str, key: str, errors: list[str]) -> object | None:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        errors.append(f"{key}: {field} no es JSON: {exc}")
        return None
    rendered = json.dumps(parsed, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if value != rendered:
        errors.append(f"{key}: {field} no usa JSON canónico")
    return parsed


def canonical_ref(prefix: str, number: int) -> str:
    if prefix == "S":
        return f"S{number:02d}" if number < 100 else f"S{number}"
    if prefix == "C-":
        return f"C-{number:03d}" if number < 1000 else f"C-{number}"
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


def expanded_ref_occurrences(text: str, prefix: str) -> list[tuple[int, int, str]]:
    escaped = re.escape(prefix)
    range_re = re.compile(
        rf"\b{escaped}(\d{{1,5}})\s*(?:-|\u2013)\s*{escaped}(\d{{1,5}})\b"
    )
    single_re = re.compile(rf"\b{escaped}\d{{1,5}}\b")
    refs: list[tuple[int, int, str]] = []
    occupied: list[tuple[int, int]] = []
    for match in range_re.finditer(text):
        start, end = map(int, match.groups())
        if (
            start <= end and end - start <= 10000
            and not (prefix == "S" and supplementary_source_context(text, match.start()))
        ):
            refs.extend(
                (match.start(), ordinal, canonical_ref(prefix, number))
                for ordinal, number in enumerate(range(start, end + 1))
            )
        occupied.append(match.span())
    for match in single_re.finditer(text):
        if any(start <= match.start() < end for start, end in occupied):
            continue
        if prefix == "S" and supplementary_source_context(text, match.start()):
            continue
        number = int(re.search(r"\d+", match.group()).group())
        refs.append((match.start(), 0, canonical_ref(prefix, number)))
    return refs


def declared_source_refs(text: str) -> list[str]:
    occurrences = expanded_ref_occurrences(text, "S")
    occurrences.extend(expanded_ref_occurrences(text, "BN-"))
    return list(dict.fromkeys(value for _, _, value in sorted(occurrences)))


def declared_claim_dependencies(text: str) -> list[str]:
    return list(dict.fromkeys(
        value for _, _, value in sorted(expanded_ref_occurrences(text, "C-"))
    ))


def is_placeholder(value: str) -> bool:
    return value.strip().casefold() in PLACEHOLDERS


def valid_string_list(value: object, field: str, key: str, errors: list[str]) -> list[str] | None:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        errors.append(f"{key}: {field} debe ser una lista JSON de cadenas no vacías")
        return None
    if len(value) != len(set(value)):
        errors.append(f"{key}: {field} contiene duplicados")
    return value


def artifact_catalog(frozen: dict[str, object], errors: list[str]) -> dict[str, str]:
    catalog: dict[str, str] = {}
    for field in ("archivos_control", "artefactos_fuente", "artefactos_revision"):
        block = frozen.get(field)
        if not isinstance(block, dict) or any(
            not isinstance(path, str) or not isinstance(digest, str)
            or not HEX64.fullmatch(digest)
            for path, digest in block.items()
        ):
            errors.append(f"Congelación: {field} no es un mapa ruta→SHA-256 válido")
            continue
        overlap = set(catalog) & set(block)
        if overlap:
            errors.append(f"Congelación: rutas duplicadas entre catálogos: {sorted(overlap)[:5]}")
        catalog.update(block)
    return catalog


def source_artifact_matches(source: str, artifact: str) -> bool:
    name = Path(artifact).name
    if source.startswith("S"):
        return (
            Path(artifact).suffix.casefold() != ".url"
            and bool(re.match(rf"{re.escape(source)}(?!\d)", name))
        )
    if source.startswith("BN-") and artifact.startswith("data/busquedas_negativas/"):
        path = ROOT / artifact
        if not path.exists():
            return False
        with path.open(encoding="utf-8-sig", newline="") as handle:
            return any(source in row.values() for row in csv.DictReader(handle))
    return False


def validate_primary_evidence(
    row: dict[str, str], expected: dict[str, str], claims: dict[str, dict[str, str]],
    catalog: dict[str, str], errors: list[str],
) -> None:
    key = row["id_afirmacion"]
    parsed: dict[str, object | None] = {}
    for field in (
        "componentes_atomicos", "fuentes_declaradas", "artefactos_verificados",
        "sha256_artefactos", "matriz_cobertura_componentes",
        "dependencias_y_huellas",
    ):
        parsed[field] = canonical_json(row[field], field, key, errors)

    components = valid_string_list(
        parsed["componentes_atomicos"], "componentes_atomicos", key, errors,
    )
    sources = valid_string_list(
        parsed["fuentes_declaradas"], "fuentes_declaradas", key, errors,
    )
    artifacts = valid_string_list(
        parsed["artefactos_verificados"], "artefactos_verificados", key, errors,
    )
    hashes = parsed["sha256_artefactos"]
    coverage = parsed["matriz_cobertura_componentes"]
    dependencies = parsed["dependencias_y_huellas"]

    expected_sources = declared_source_refs(expected["fuente"])
    if sources is not None and sources != expected_sources:
        errors.append(
            f"{key}: fuentes_declaradas no reproduce Fuente; "
            f"esperado {expected_sources!r}"
        )
    expected_dependencies = declared_claim_dependencies(expected["atribucion"])
    expected_dependency_hashes = {
        dependency: claims[dependency]["sha256_fila"]
        for dependency in expected_dependencies if dependency in claims
    }
    missing_dependencies = [item for item in expected_dependencies if item not in claims]
    if missing_dependencies:
        errors.append(f"{key}: dependencias inexistentes {missing_dependencies}")
    if dependencies != expected_dependency_hashes:
        errors.append(f"{key}: dependencias_y_huellas no coincide con la atribución viva")

    if artifacts is not None:
        for artifact in artifacts:
            if artifact not in catalog:
                errors.append(f"{key}: artefacto no congelado: {artifact}")
    if not isinstance(hashes, dict) or any(
        not isinstance(path, str) or not isinstance(digest, str)
        for path, digest in hashes.items()
    ):
        errors.append(f"{key}: sha256_artefactos debe ser un objeto ruta→SHA-256")
    elif artifacts is not None:
        expected_hashes = {
            artifact: catalog[artifact] for artifact in artifacts if artifact in catalog
        }
        if hashes != expected_hashes:
            errors.append(f"{key}: sha256_artefactos no coincide con artefactos congelados")

    if components is not None:
        if not components:
            errors.append(f"{key}: no descompone la afirmación en componentes atómicos")
        if not isinstance(coverage, dict) or set(coverage) != set(components):
            errors.append(f"{key}: matriz de cobertura no coincide con los componentes")
        else:
            handles = set((sources or []) + expected_dependencies + (artifacts or []))
            for component, evidence in coverage.items():
                evidence_list = valid_string_list(
                    evidence, f"cobertura[{component}]", key, errors,
                )
                if evidence_list is not None and not evidence_list:
                    errors.append(f"{key}: componente sin evidencia: {component}")
                for token in evidence_list or []:
                    if not any(
                        token == handle or token.startswith(handle + ":")
                        or token.startswith(handle + "#") for handle in handles
                    ):
                        errors.append(
                            f"{key}: cobertura[{component}] usa evidencia no declarada: {token}"
                        )

    if row["localizador_declarado"] != expected["fuente"]:
        errors.append(f"{key}: localizador_declarado no reproduce Fuente")
    if not HEX64.fullmatch(row["sha256_pasaje"]):
        errors.append(f"{key}: sha256_pasaje no es SHA-256")
    if len(row["fragmento_control"].split()) > 25:
        errors.append(f"{key}: fragmento_control supera 25 palabras")
    if len(row["motivo_dictamen"].strip()) < 30:
        errors.append(f"{key}: motivo_dictamen no es evidencia nominal suficiente")
    if is_placeholder(row["revisor"]):
        errors.append(f"{key}: revisor primario no identificado")
    if parse_utc_timestamp(row["fecha_utc"]) is None:
        errors.append(f"{key}: fecha_utc no es un instante UTC válido")
    if row["version_censo"] != "1":
        errors.append(f"{key}: version_censo inválida")

    if row["resultado"] == "CONFORME":
        for field in ("localizador_verificado", "fragmento_control"):
            if is_placeholder(row[field]):
                errors.append(f"{key}: CONFORME con {field} sin verificar")
        if expected["atribucion"].startswith("expresa"):
            if not artifacts:
                errors.append(f"{key}: expresa CONFORME sin artefacto fuente")
            for source in sources or []:
                if not any(source_artifact_matches(source, artifact) for artifact in artifacts or []):
                    errors.append(
                        f"{key}: expresa CONFORME sin artefacto nominal para {source}"
                    )


def validate() -> list[str]:
    errors: list[str] = []
    expected_freeze = inventory_payload()
    frozen: dict[str, object] = {}
    if not FREEZE.exists():
        errors.append(f"Falta congelación: {FREEZE.relative_to(ROOT)}")
    else:
        try:
            loaded = json.loads(FREEZE.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Congelación: JSON inválido: {exc}")
        else:
            if not isinstance(loaded, dict):
                errors.append("Congelación: debe ser un objeto JSON")
            else:
                frozen = loaded
    freeze_time = parse_utc_timestamp(frozen.get("fecha_congelacion"))
    if freeze_time is None:
        errors.append("Congelación: fecha_congelacion debe ser un instante UTC válido")
    else:
        expected_freeze["fecha_congelacion"] = frozen["fecha_congelacion"]
    if frozen != expected_freeze:
        errors.append("La congelación semántica no coincide con el corpus vivo")
    claims = expected_freeze["afirmaciones"]
    assert isinstance(claims, dict)
    catalog = artifact_catalog(expected_freeze, errors)

    primary, primary_errors = load_csv(PRIMARY, PRIMARY_HEADER)
    errors.extend(primary_errors)
    by_claim: dict[str, dict[str, str]] = {}
    primary_times: list[datetime] = []
    for row in primary:
        key = row["id_afirmacion"]
        if key in by_claim:
            errors.append(f"Primera revisión duplicada: {key}")
            continue
        by_claim[key] = row
        expected = claims.get(key)
        if expected is None:
            errors.append(f"Primera revisión contiene C inexistente: {key}")
            continue
        if row["ruta_canonica"] != expected["ruta"]:
            errors.append(f"{key}: ruta canónica incorrecta")
        if row["sha256_fila"] != expected["sha256_fila"]:
            errors.append(f"{key}: huella de fila obsoleta")
        if row["atribucion"] != expected["atribucion"]:
            errors.append(f"{key}: atribución no coincide")
        if row["resultado"] not in RESULTS:
            errors.append(f"{key}: resultado primario inválido")
        validate_primary_evidence(row, expected, claims, catalog, errors)
        primary_time = parse_utc_timestamp(row["fecha_utc"])
        if primary_time is not None:
            primary_times.append(primary_time)
            if freeze_time is not None and primary_time < freeze_time:
                errors.append(f"{key}: primera revisión anterior a la congelación")
        if row["version_protocolo"] != expected_freeze["version_protocolo"]:
            errors.append(f"{key}: versión de protocolo incorrecta")
    missing = sorted(set(claims) - set(by_claim))
    extra = sorted(set(by_claim) - set(claims))
    if missing:
        errors.append(f"Faltan {len(missing)} C en primera revisión: {missing[:10]}")
    if extra:
        errors.append(f"Sobran {len(extra)} C en primera revisión: {extra[:10]}")

    secondary, secondary_errors = load_csv(SECONDARY, SECONDARY_HEADER)
    errors.extend(secondary_errors)
    second_by_claim: dict[str, dict[str, str]] = {}
    primary_hash = sha(PRIMARY) if PRIMARY.exists() else ""
    last_primary_time = max(primary_times, default=None)
    for row in secondary:
        key = row["id_afirmacion"]
        if key in second_by_claim:
            errors.append(f"Segunda revisión duplicada: {key}")
            continue
        second_by_claim[key] = row
        expected = claims.get(key)
        if expected is None:
            errors.append(f"Segunda revisión contiene C inexistente: {key}")
            continue
        if row["sha256_fila"] != expected["sha256_fila"]:
            errors.append(f"{key}: segunda revisión con huella obsoleta")
        if row["sha256_censo_primario"] != primary_hash:
            errors.append(f"{key}: no fija la huella del censo primario completo")
        if row["resultado_independiente"] not in RESULTS:
            errors.append(f"{key}: resultado independiente inválido")
        if key in by_claim and row["revisor_independiente"] == by_claim[key]["revisor"]:
            errors.append(f"{key}: auto-revisión")
        if row["declaracion_independencia"] != INDEPENDENCE_DECLARATION:
            errors.append(f"{key}: declaración de independencia insuficiente")
        if row["version_revision"] != "1":
            errors.append(f"{key}: version_revision inválida")
        if is_placeholder(row["revisor_independiente"]):
            errors.append(f"{key}: revisor independiente no identificado")
        secondary_time = parse_utc_timestamp(row["fecha_utc"])
        if secondary_time is None:
            errors.append(f"{key}: fecha_utc independiente no es un instante UTC válido")
        else:
            if freeze_time is not None and secondary_time < freeze_time:
                errors.append(f"{key}: segunda revisión anterior a la congelación")
            # Cada fila secundaria fija el CSV primario completo, no solo su C.
            if last_primary_time is not None and secondary_time < last_primary_time:
                errors.append(f"{key}: segunda revisión anterior al cierre del censo primario completo")
        passage_hashes = row["sha256_pasajes_reinspeccionados"].split(";")
        if not passage_hashes or any(not HEX64.fullmatch(item) for item in passage_hashes):
            errors.append(f"{key}: huellas de pasajes reinspeccionados inválidas")
        if len(row["evidencia_dictamen"].strip()) < 30:
            errors.append(f"{key}: evidencia independiente insuficiente")
        if row["discrepancia"] not in {"NO", "SI"}:
            errors.append(f"{key}: marca de discrepancia inválida")
        if row["discrepancia"] == "SI":
            errors.append(f"{key}: discrepancia semántica abierta")
        elif row["resolucion_discrepancia"] != "NO_APLICA":
            errors.append(f"{key}: resolución incompatible con discrepancia=NO")
        if key in by_claim and row["resultado_independiente"] != by_claim[key]["resultado"]:
            errors.append(f"{key}: los dictámenes independientes no coinciden")
        if row["resultado_independiente"] == "CONFORME" and any(
            is_placeholder(row[field])
            for field in (
                "localizadores_reinspeccionados",
                "sha256_pasajes_reinspeccionados", "evidencia_dictamen",
            )
        ):
            errors.append(f"{key}: segunda aprobación sin reinspección nominal")
    missing_second = sorted(set(claims) - set(second_by_claim))
    if missing_second:
        errors.append(
            f"Faltan {len(missing_second)} C en segunda revisión: "
            f"{missing_second[:10]}"
        )
    residual_primary = sorted(
        key for key, row in by_claim.items() if row["resultado"] != "CONFORME"
    )
    residual_secondary = sorted(
        key for key, row in second_by_claim.items()
        if row["resultado_independiente"] != "CONFORME"
    )
    if residual_primary:
        errors.append(f"Residuales en primera revisión: {residual_primary}")
    if residual_secondary:
        errors.append(f"Residuales en segunda revisión: {residual_secondary}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-freeze", action="store_true")
    parser.add_argument(
        "--fecha-congelacion-utc",
        help="Instante real de congelación, explícito: YYYY-MM-DDTHH:MM:SSZ",
    )
    args = parser.parse_args(argv)
    if args.write_freeze and parse_utc_timestamp(args.fecha_congelacion_utc) is None:
        parser.error("--write-freeze exige --fecha-congelacion-utc con un instante UTC válido")
    if args.fecha_congelacion_utc is not None and not args.write_freeze:
        parser.error("--fecha-congelacion-utc solo se admite con --write-freeze")
    if args.write_freeze:
        FREEZE.parent.mkdir(parents=True, exist_ok=True)
        FREEZE.write_text(
            json.dumps(freeze_payload(args.fecha_congelacion_utc), ensure_ascii=False, sort_keys=True, indent=2)
            + "\n",
            encoding="utf-8",
        )
        print(f"CONGELACIÓN SEMÁNTICA ESCRITA: {len(claim_inventory())} C")
        return 0
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        return 1
    print(f"CENSO SEMÁNTICO DOBLEMENTE REVISADO: {len(claim_inventory())} C")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
