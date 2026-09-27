#!/usr/bin/env python3
"""Retira valores no acreditados de celdas rechazadas y fija huecos nominales.

La entrada es el censo versionado de dos rerevisiones independientes. Para cada
NO_CONFORME se repite una consulta literal exacta sobre ``fuentes/``. Solo si la
consulta da cero coincidencias se sustituye el valor anterior por un hueco de
trazabilidad acotado a esa consulta. Cero coincidencias nunca se interpreta como
ausencia biológica ni como prueba de que el dato no exista en la literatura.
Una corrección semántica posterior puede sustituir ese hueco sólo mediante
una disposición nominal con revisión ajena ligada a la propuesta. La consulta
y la BN históricas se conservan; no se añaden positivos literales por esa vía.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "data/auditoria/residuales_trazabilidad_no_conformes_v3.csv"
TARGETS = (
    ROOT / "data/auditoria/celdas_no_conformes_trazabilidad_v1.csv",
    ROOT / "data/auditoria/celdas_no_conformes_trazabilidad_v2.csv",
)
MANIFEST = ROOT / "data/auditoria/mapeo_celdas_afirmaciones.csv"
CORRECTIONS = ROOT / "data/auditoria/correcciones_celdas_semanticas_v1.csv"
CLAIMS = ROOT / "data/afirmaciones/15.csv"
MAGNITUDES = ROOT / "data/apendices/F_magnitudes.csv"
NARRATIVE = ROOT / "docs/secciones/016-15-15-lo-que-no-se-sabe-y-como-lo-sabemos.md"
GENERATED_MARKER = "Cierre nominal de trazabilidad v3"
START_BN = 147
POSITIVE_CLAIMS = {"C-2472", "C-2489"}
EXPECTED_RESIDUALS = 410
EXPECTED_V3_NEGATIVES = 408
# BN-557 y BN-558 son consultas científicas posteriores, ajenas a la remediación v3.
# BN-120 fue retirada al recuperar genes y densidad en S434 (C-2821/C-2822).
# Su fila y Q previa se conservan en docs/auditorias/retirada_bn120_2026-09-26.json.
# BN-132 se retira tras localizar recuentos de genes/familias en S560,
# C-1163/C-2824; historia en retirada_bn132_2026-09-26.json.
# BN-133/BN-146 se retiran al recuperar cifras de ambas posiciones HGT con
# denominadores explícitos (S290/S291/S561, C-2825–C-2832); historia completa
# en retirada_bn133_bn146_2026-09-27.json. Ninguna retirada convierte una BN
# en prueba positiva ni altera las 408 consultas v3.
# BN-144 se retira al recuperar el par recuento–tiempo en S562;
# la ausencia de resolución de pérdidas individuales se conserva en C-2835.
# Historia previa íntegra: retirada_bn144_2026-09-27.json.
EXPECTED_BN_COUNTS = (494, 482, 12)
RETIRED_BN_KEYS = {"BN-120", "BN-132", "BN-133", "BN-144", "BN-146"}

RESIDUAL_HEADER = [
    "claim_id", "csv_path", "fila", "columna", "contenido_anterior",
    "contenido_sha256", "origen_revision", "resultado", "evidencia",
    "localizadores",
]


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise RuntimeError(f"CSV sin cabecera: {path}")
        return reader.fieldnames, list(reader)


def csv_bytes(header: list[str], rows: list[dict[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=header, quoting=csv.QUOTE_ALL, lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def digest_cell(value: str) -> str:
    return hashlib.sha256((value + "\n").encode("utf-8")).hexdigest()


def normalized(value: str) -> str:
    return " ".join(value.casefold().split())


def source_snapshot() -> tuple[list[str], str, int]:
    records: list[tuple[str, str, str]] = []
    texts: list[str] = []
    for path in sorted((ROOT / "fuentes").iterdir()):
        if not path.is_file():
            continue
        payload = path.read_bytes()
        records.append((path.name, hashlib.sha256(payload).hexdigest(), str(len(payload))))
        texts.append(normalized(payload.decode("utf-8", errors="ignore")))
    inventory = "\n".join("\0".join(row) for row in records) + "\n"
    return texts, hashlib.sha256(inventory.encode()).hexdigest(), len(records)


class ExactCooccurrenceIndex:
    """Memoiza pertenencia literal por componente, sin interpretar el texto.

    Los textos y componentes ya tienen exactamente la normalización histórica.
    Cada conjunto contiene los índices de artefactos que contienen la cadena;
    su intersección equivale al ``all(component in text ...)`` original. La
    evaluación es perezosa: solo inspecciona artefactos que superaron los
    componentes anteriores y reutiliza tanto aciertos como fallos. No hay
    tokenización, stemming, coincidencia aproximada ni cambio del universo.
    """

    def __init__(self, texts: list[str]) -> None:
        self.texts = tuple(texts)
        self.matches: dict[str, set[int]] = {}
        self.checked: dict[str, set[int]] = {}

    def count(self, components: list[str]) -> int:
        common = set(range(len(self.texts)))
        for component in components:
            matches = self.matches.setdefault(component, set())
            checked = self.checked.setdefault(component, set())
            pending = common - checked
            matches.update(index for index in pending if component in self.texts[index])
            checked.update(pending)
            common &= matches
            if not common:
                return 0
        # Conserva incluso la semántica de all([]) para consultas sin componentes.
        return len(common)


def negative_path(csv_path: str) -> Path:
    if "/02/" in csv_path:
        name = "15_1_15-1-punto-de-partida-y-participantes-celulares.csv"
    elif any(part in csv_path for part in ("/05/", "/06/", "/07/", "/08/")):
        name = "15_4_15-4-registro-material-tiempo-ambiente-y-ecologia.csv"
    elif "/09/" in csv_path:
        name = "15_5_15-5-asociacion-integracion-y-transferencia.csv"
    elif "/10/" in csv_path:
        name = "15_6_15-6-rasgos-con-costo-y-controversia-energetica.csv"
    elif "/12/" in csv_path:
        name = "15_9_15-9-multicelularidad-y-repertorio-preanimal.csv"
    elif "/14/" in csv_path:
        name = "15_8_15-8-nombres-y-nomenclatura.csv"
    elif "/15/" in csv_path:
        name = "15_3_15-3-raiz-eucariota-y-corredor-filogenetico.csv"
    else:
        raise RuntimeError(f"Sin registro BN de destino para {csv_path}")
    return ROOT / "data/busquedas_negativas" / name


def gap_value(bn: str) -> str:
    return (
        "HUECO DE TRAZABILIDAD: la consulta literal exacta del valor anterior "
        "no produjo coincidencias en los artefactos de fuentes/; no se adjudica "
        f"un valor para este campo [{bn}]"
    )


def nominal_query(residual: dict[str, str]) -> str:
    """Fija la conjunción exacta identidad de fila + campo + valor rechazado."""
    path = ROOT / residual["csv_path"]
    header, rows = read_csv(path)
    index = int(residual["fila"]) - 2
    if not (0 <= index < len(rows)):
        raise RuntimeError(f"Fila residual inexistente: {residual['claim_id']}")
    identity = rows[index][header[0]].strip()
    return (
        f"identidad=«{identity}»; campo=«{residual['columna']}»; "
        f"valor=«{residual['contenido_anterior']}»"
    )


def nominal_components(query: str) -> list[str]:
    return [normalized(value) for value in re.findall(r"=«([^»]+)»", query)]


def bn_row(
    header: list[str], residual: dict[str, str], bn: str,
    source_hash: str, source_count: int,
) -> dict[str, str]:
    locator = f"{residual['csv_path']}:fila {residual['fila']}:{residual['columna']}"
    terms = (
        f"consulta nominal conjunta exacta {residual['_consulta_nominal']}; ámbito fuentes/ "
        f"({source_count} artefactos); sha256_inventario={source_hash}; reproducible: "
        f"python3 scripts/remediate_trace_residuals.py --probe {bn}"
    )
    result = (
        "0 artefactos con coocurrencia literal de los tres componentes exactos "
        "tras normalizar mayúsculas y blancos. "
        "El resultado se limita a esta consulta y no demuestra inexistencia del "
        "dato ni ausencia biológica; por el dictamen independiente se retira el "
        f"valor no acreditado. {GENERATED_MARKER}; objeto nominal {locator}."
    )
    if "/14/" in residual["csv_path"]:
        result += " El objeto pertenece a terminología histórica."
    row = {field: "n/a" for field in header}
    row["clave"] = bn
    for field in ("estado", "etiqueta"):
        if field in row:
            row[field] = "NO LOCALIZADO EN ESTA SESIÓN"
    if "hueco" in row:
        row["hueco"] = (
            f"Pasaje que sostenga conjuntamente el valor anterior del campo "
            f"{residual['columna']} para {locator}"
        )
    terms_field = next((field for field in header if field.startswith("términos")), None)
    result_field = next((field for field in header if field.startswith("resultado")), None)
    if terms_field is None:
        raise RuntimeError(f"Registro BN sin campo de términos: {header!r}")
    row[terms_field] = terms if result_field else f"{terms}; resultado: {result}"
    if result_field:
        row[result_field] = result
    for field in ("filas relacionadas", "filas o fuente"):
        if field in row:
            row[field] = f"{residual['claim_id']}; {locator}"
    return row


def semantic_dispositions(residuals: list[dict[str, str]] | None = None) -> dict[str, dict]:
    try:
        from . import build_atomic_cell_claims as atomic
        from . import residual_semantic_dispositions as dispositions
    except ImportError:
        import build_atomic_cell_claims as atomic
        import residual_semantic_dispositions as dispositions
    snapshots = {path: path.read_bytes() for path in (RESIDUALS, *TARGETS, CORRECTIONS)}
    correction_header, corrections = read_csv(CORRECTIONS)
    if correction_header != atomic.CORRECTION_HEADER:
        raise RuntimeError("Cabecera de correcciones semánticas inesperada")
    targets = [row for path in TARGETS for row in read_csv(path)[1]]
    found = dispositions.load(
        ROOT, residuals if residuals is not None else read_csv(RESIDUALS)[1],
        targets, corrections, start_bn=START_BN, positive_claims=POSITIVE_CLAIMS,
    )
    for key, record in found.items():
        if record["contenido_previo"] != gap_value(record["bn"]):
            raise RuntimeError(f"La disposición no conserva el hueco histórico exacto: {key}")
    if any(path.read_bytes() != raw for path, raw in snapshots.items()):
        raise RuntimeError("Entradas de disposición modificadas durante la validación")
    return found


def build() -> tuple[dict[Path, bytes], dict[str, tuple[str, int]]]:
    header, residuals = read_csv(RESIDUALS)
    if header != RESIDUAL_HEADER or len(residuals) != EXPECTED_RESIDUALS:
        raise RuntimeError("El censo residual debe contener exactamente 410 filas canónicas")
    if any(row["resultado"] != "NO_CONFORME" for row in residuals):
        raise RuntimeError("El censo residual contiene una fila no rechazada")
    ids = [row["claim_id"] for row in residuals]
    if len(ids) != len(set(ids)):
        raise RuntimeError("C residual duplicada")
    if not POSITIVE_CLAIMS.issubset(ids):
        raise RuntimeError("El censo residual debe conservar los dos pasajes positivos nominales")
    if len(ids) - len(POSITIVE_CLAIMS) != EXPECTED_V3_NEGATIVES:
        raise RuntimeError("El censo residual debe conservar exactamente 408 consultas negativas v3")

    dispositions = semantic_dispositions(residuals)
    input_paths = {
        RESIDUALS, CORRECTIONS, *TARGETS, MANIFEST, CLAIMS, MAGNITUDES, NARRATIVE,
        *(ROOT / row["csv_path"] for row in residuals),
        *(ROOT / "data/busquedas_negativas").glob("*.csv"),
    }
    inputs_before = {path: path.read_bytes() for path in input_paths}
    source_texts, source_hash, source_count = source_snapshot()
    cooccurrences = ExactCooccurrenceIndex(source_texts)
    probes: dict[str, tuple[str, int]] = {}
    payloads: dict[Path, bytes] = {}
    assigned: dict[str, str] = {}
    historical: dict[str, str] = {}
    by_table: dict[Path, list[tuple[dict[str, str], str]]] = {}
    for offset, residual in enumerate(residuals):
        bn = f"BN-{START_BN + offset:03d}"
        query = nominal_query(residual)
        residual["_consulta_nominal"] = query
        components = nominal_components(query)
        count = cooccurrences.count(components)
        if residual["claim_id"] not in POSITIVE_CLAIMS:
            probes[bn] = (query, count)
        if count and residual["claim_id"] not in POSITIVE_CLAIMS:
            raise RuntimeError(
                f"{bn}/{residual['claim_id']}: la consulta ya no es negativa ({count})"
            )
        if not count and residual["claim_id"] in POSITIVE_CLAIMS:
            raise RuntimeError(f"{residual['claim_id']}: pasaje positivo dejó de resolver")
        historical_value = (
            residual["contenido_anterior"]
            if residual["claim_id"] in POSITIVE_CLAIMS else gap_value(bn)
        )
        historical[residual["claim_id"]] = historical_value
        disposition = dispositions.get(residual["claim_id"])
        replacement = disposition["contenido_nuevo"] if disposition else historical_value
        assigned[residual["claim_id"]] = replacement
        by_table.setdefault(ROOT / residual["csv_path"], []).append((residual, replacement))

    for path, changes in by_table.items():
        table_header, rows = read_csv(path)
        for residual, replacement in changes:
            index = int(residual["fila"]) - 2
            if not (0 <= index < len(rows)) or residual["columna"] not in table_header:
                raise RuntimeError(f"Celda residual inexistente: {residual['claim_id']}")
            live = " ".join(rows[index][residual["columna"]].split())
            prior_gap = gap_value(f"BN-{START_BN + residuals.index(residual):03d}")
            if live not in {residual["contenido_anterior"], replacement, prior_gap}:
                raise RuntimeError(f"Celda concurrentemente modificada: {residual['claim_id']}")
            rows[index][residual["columna"]] = replacement
        payloads[path] = csv_bytes(table_header, rows)

    for target_path in TARGETS:
        target_header, target_rows = read_csv(target_path)
        for row in target_rows:
            # El objetivo conserva el hueco autoral histórico. La corrección
            # semántica se aplica prospectivamente en su registro separado.
            replacement = historical.get(row["claim_id"])
            if replacement is None:
                continue
            row["contenido"] = replacement
            row["contenido_sha256"] = digest_cell(replacement)
            suffix = (
                " Corrección de autor v3: pasaje positivo nominal localizado; pendiente "
                "de nueva revisión independiente."
                if row["claim_id"] in POSITIVE_CLAIMS else
                " Corrección de autor v3: valor positivo retirado tras rerevisión; "
                "hueco nominal pendiente de nueva revisión independiente."
            )
            if suffix.strip() not in row["evidencia_dictamen"]:
                row["evidencia_dictamen"] += suffix
        payloads[target_path] = csv_bytes(target_header, target_rows)

    manifest_header, manifest_rows = read_csv(MANIFEST)
    lookup = {(row["csv_path"], row["fila"], row["columna"]): row for row in residuals}
    for row in manifest_rows:
        residual = lookup.get((row["csv_path"], row["fila"], row["columna"]))
        if residual is None:
            continue
        replacement = assigned[residual["claim_id"]]
        row["contenido"] = replacement
        row["contenido_sha256"] = digest_cell(replacement)
        row["nota_adjudicacion"] = (
            "Corrección de autor posterior al dictamen independiente: la C "
            "atómica reproduce solo esta celda; pendiente rerevisión ajena."
        )
    payloads[MANIFEST] = csv_bytes(manifest_header, manifest_rows)

    grouped: dict[Path, list[tuple[dict[str, str], str]]] = {}
    for offset, residual in enumerate(residuals):
        if residual["claim_id"] in POSITIVE_CLAIMS:
            continue
        grouped.setdefault(negative_path(residual["csv_path"]), []).append(
            (residual, f"BN-{START_BN + offset:03d}")
        )
    for path, entries in grouped.items():
        bn_header, bn_rows = read_csv(path)
        bn_rows = [row for row in bn_rows if GENERATED_MARKER not in " ".join(row.values())]
        bn_rows.extend(
            bn_row(bn_header, residual, bn, source_hash, source_count)
            for residual, bn in entries
        )
        bn_rows.sort(key=lambda row: int(row["clave"].split("-")[1]))
        payloads[path] = csv_bytes(bn_header, bn_rows)

    active: list[dict[str, str]] = []
    for path in sorted((ROOT / "data/busquedas_negativas").glob("*.csv")):
        raw = payloads.get(path, path.read_bytes())
        active.extend(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    total = len(active)
    unlocated = sum("NO LOCALIZADO EN ESTA SESIÓN" in row.values() for row in active)
    declared = sum("LA LITERATURA DECLARA QUE NO SE SABE" in row.values() for row in active)
    if (total, unlocated, declared) != EXPECTED_BN_COUNTS:
        raise RuntimeError(
            f"Recuento BN inesperado: total={total}, no_localizado={unlocated}, literatura={declared}"
        )
    if len({row["clave"] for row in active}) != total:
        raise RuntimeError("El registro activo contiene claves BN duplicadas")
    retired_active = RETIRED_BN_KEYS & {row["clave"] for row in active}
    if retired_active:
        raise RuntimeError(
            "El registro activo reintroduce BN retiradas por evidencia positiva: "
            + ", ".join(sorted(retired_active))
        )
    expected_v3 = {
        f"BN-{START_BN + offset:03d}"
        for offset, residual in enumerate(residuals)
        if residual["claim_id"] not in POSITIVE_CLAIMS
    }
    actual_v3 = {
        row["clave"] for row in active if GENERATED_MARKER in " ".join(row.values())
    }
    if actual_v3 != expected_v3 or len(actual_v3) != EXPECTED_V3_NEGATIVES:
        raise RuntimeError("Las 408 BN de remediación v3 no coinciden con los residuales nominales")

    claims_header, claim_rows = read_csv(CLAIMS)
    for row in claim_rows:
        if row["#"] == "C-1931":
            row["Afirmación"] = (
                f"El registro canónico contiene {total} búsquedas negativas activas y "
                "cada una porta exactamente una de las dos etiquetas exigidas."
            )
            row["Objeto"] = f"{total} filas etiquetadas"
            row["Motivo"] = (
                "La auditoría conserva las claves originales y sus disposiciones; "
                "408 altas entre BN-147 y BN-556 documentan consultas nominales de la "
                "remediación v3 y "
                "no convierten cero coincidencias literales en ausencia científica."
            )
        elif row["#"] == "C-1933":
            row["Afirmación"] = (
                f"{unlocated} búsquedas negativas están marcadas "
                "NO LOCALIZADO EN ESTA SESIÓN."
            )
            row["Objeto"] = f"{unlocated} filas"
            row["Motivo"] = (
                "Cada alta v3 identifica una celda, la cadena consultada, el ámbito, "
                "la huella del inventario y el resultado limitado de la consulta."
            )
    payloads[CLAIMS] = csv_bytes(claims_header, claim_rows)

    magnitude_header, magnitude_rows = read_csv(MAGNITUDES)
    for row in magnitude_rows:
        if row["magnitud"] == "búsquedas negativas activas":
            row["valor tal como lo publica la fuente"] = str(total)
        elif row["magnitud"] == "búsquedas sin resultado localizado":
            row["valor tal como lo publica la fuente"] = str(unlocated)
    payloads[MAGNITUDES] = csv_bytes(magnitude_header, magnitude_rows)

    narrative = NARRATIVE.read_text(encoding="utf-8")
    narrative = re.sub(
        r"El registro canónico contiene \d+ búsquedas negativas activas y cada una "
        r"porta exactamente una de las (?:dos|tres) etiquetas exigidas\.",
        f"El registro canónico contiene {total} búsquedas negativas activas y cada una "
        "porta exactamente una de las dos etiquetas exigidas.", narrative,
    )
    narrative = re.sub(
        r"Doce filas están marcadas `LA LITERATURA DECLARA QUE NO SE SABE`, \d+ "
        r"están marcadas `NO LOCALIZADO EN ESTA SESIÓN` y ninguna está marcada "
        r"`NO BUSCADO`\.",
        f"Doce filas están marcadas `LA LITERATURA DECLARA QUE NO SE SABE`, "
        f"{unlocated} están marcadas `NO LOCALIZADO EN ESTA SESIÓN` y ninguna está "
        "marcada `NO BUSCADO`.", narrative,
    )
    payloads[NARRATIVE] = narrative.encode("utf-8")
    if semantic_dispositions() != dispositions:
        raise RuntimeError("Disposiciones cambiaron durante la remediación")
    if any(not path.is_file() or path.read_bytes() != raw for path, raw in inputs_before.items()):
        raise RuntimeError("Entradas cambiaron durante la remediación")
    return payloads, probes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--probe")
    args = parser.parse_args()
    payloads, probes = build()
    if args.probe:
        if args.probe not in probes:
            raise SystemExit(f"BN fuera de la remediación: {args.probe}")
        term, count = probes[args.probe]
        print(f"{args.probe}: {count} coincidencias exactas: {term}")
        return 0 if count == 0 else 1
    if args.write:
        for path, payload in payloads.items():
            path.write_bytes(payload)
        print("RESIDUALES REMEDIADOS: 408 consultas negativas y 2 positivos literales; disposiciones semánticas verificadas por separado")
        return 0
    stale = [path.relative_to(ROOT).as_posix() for path, payload in payloads.items()
             if path.read_bytes() != payload]
    if stale:
        raise SystemExit("Remediación de trazabilidad desactualizada: " + "; ".join(stale))
    print("REMEDIACIÓN VERIFICADA: 408 consultas negativas y 2 positivos literales; disposiciones semánticas verificadas por separado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
