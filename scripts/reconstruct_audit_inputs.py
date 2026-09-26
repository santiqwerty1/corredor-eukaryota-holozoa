#!/usr/bin/env python3
"""Reconstruye los insumos históricos de la auditoría desde evidencia versionada.

La instantánea externa usada durante la auditoría original no forma parte del
repositorio. Este programa no intenta recrear información ausente: conserva los
campos iniciales todavía presentes en las matrices, liga cada fila a su huella
original ya publicada y obtiene el corpus inicial del commit Git documentado.
Los insumos resultantes son versionados y el modo ``--check`` impide que una
regeneración use silenciosamente una reconstrucción distinta.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
BASELINE_COMMIT = "a3ce4e6685a4e287a5fbd478d4657e475e10de3c"
EVIDENCE_COMMIT = "af7e799e2d096a48f24afd31d7745e19cebf374d"
OUTPUT_DIR = Path("data/auditoria/entradas_congeladas_reconstruidas")

CLAIM_FIELDS = [
    "clave_inicial", "seccion", "resultado", "severidad", "accion",
    "evidencia_auditoria", "huella_fila_original_sha256",
    "huella_corpus_inicial_sha256",
]
SOURCE_FIELDS = [
    "clave_inicial", "clave_final", "metadata", "identidad_bibliografica",
    "tipo", "estado_editorial", "acceso", "doi_url", "uso",
    "soporte_unico", "veredicto", "severidad", "accion",
    "fecha_verificacion", "evidencia_auditoria",
    "huella_fila_original_sha256", "huella_corpus_inicial_sha256",
]
REQUIREMENT_FIELDS = [
    "seccion_prompt", "requisito_literal", "estado_inicial", "estado_final",
    "afirmaciones", "tablas", "fuentes", "busqueda_negativa", "accion",
    "evidencia", "huella_fila_original_sha256",
]
SEARCH_FIELDS = [
    "fecha", "bloque", "objetivo", "consulta_exacta", "servicio",
    "resultado", "fuentes_evaluadas", "accion",
    "huella_fila_original_sha256",
]
NEGATIVE_HISTORY_FIELDS = [
    "clave_original", "bloque_original", "disposición_final",
    "resultado_documentado", "evidencia_principal", "destino_canónico",
    "prioridad_base", "desencadenante_base",
    "huella_fila_original_sha256", "delta_preservado",
]
ORIGIN_FIELDS = ["clave_temporal", "origen"]
REMOVED_SOURCE_FIELDS = ["clave", "motivo", "destino_documental"]


class ReconstructionError(RuntimeError):
    """Inconsistencia entre los anclajes versionados."""


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_bytes(fields: Sequence[str], rows: Sequence[dict[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        buffer, fieldnames=list(fields), quoting=csv.QUOTE_ALL,
        lineterminator="\n", extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def git_file(relative: str, commit: str = BASELINE_COMMIT) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{commit}:{relative}"], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if completed.returncode:
        raise ReconstructionError(
            f"No se pudo leer {relative} en {commit}: "
            f"{completed.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return completed.stdout


def git_csv(relative: str) -> list[dict[str, str]]:
    text = git_file(relative).decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text, newline="")))


def expand_claims(value: str) -> list[str]:
    result: list[str] = []
    if value == "n/a":
        return result
    for chunk in value.split("; "):
        match = re.fullmatch(r"C-(\d+)–C-(\d+)", chunk)
        if match:
            start, end = map(int, match.groups())
            result.extend(
                f"C-{number:03d}" if number < 1000 else f"C-{number}"
                for number in range(start, end + 1)
            )
        else:
            result.append(chunk)
    return result


def reconstructed_payloads() -> dict[Path, bytes]:
    output = ROOT / OUTPUT_DIR
    claim_matrix = read_csv(
        ROOT / "docs/auditorias/matriz_afirmaciones_2026-08-08.csv"
    )
    source_matrix = read_csv(
        ROOT / "docs/auditorias/matriz_fuentes_2026-08-08.csv"
    )
    requirement_matrix = read_csv(
        ROOT / "docs/auditorias/matriz_requisitos_2026-08-08.csv"
    )
    search_matrix = read_csv(
        ROOT / "docs/auditorias/registro_busquedas_2026-08-08.csv"
    )
    negative_history = read_csv(
        ROOT / "docs/auditorias/revision_busquedas_negativas_2026-08-08.csv"
    )

    claims = [{
        "clave_inicial": row["clave_inicial"],
        "seccion": row["seccion_inicial"],
        "resultado": row["estado_inicial"],
        "severidad": row["severidad_inicial"],
        "accion": row["accion_inicial"],
        "evidencia_auditoria": row["evidencia_auditoria_inicial"],
        "huella_fila_original_sha256": row["huella_inicial_sha256"],
        "huella_corpus_inicial_sha256": row["huella_corpus_inicial_sha256"],
    } for row in claim_matrix if not row["clave_inicial"].startswith("NUEVA:")]
    sources = [{
        "clave_inicial": row["clave_inicial"],
        "clave_final": row["clave_inicial"],
        "metadata": row["metadatos_iniciales"],
        "identidad_bibliografica": row["identidad_bibliografica"],
        "tipo": row["tipo_inicial"],
        "estado_editorial": row["estado_editorial"].removeprefix("INICIAL: ").split(
            " | FINAL", 1
        )[0],
        "acceso": row["acceso"],
        "doi_url": row["doi_url_inicial"],
        "uso": row["uso_inicial"],
        "soporte_unico": row["soporte_unico_inicial"],
        "veredicto": row["veredicto_inicial"],
        "severidad": row["severidad_inicial"],
        "accion": row["accion_inicial"],
        "fecha_verificacion": row["fecha_verificacion"],
        "evidencia_auditoria": row["evidencia_auditoria_inicial"],
        "huella_fila_original_sha256": row["huella_inicial_sha256"],
        "huella_corpus_inicial_sha256": row["huella_corpus_inicial_sha256"],
    } for row in source_matrix if not row["clave_inicial"].startswith("NUEVA:")]
    requirements = [{
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
        "huella_fila_original_sha256": row["huella_inicial_sha256"],
    } for row in requirement_matrix]
    searches = [{
        "fecha": row["fecha"],
        "bloque": row["bloque"],
        "objetivo": row["objetivo"],
        "consulta_exacta": row["consulta_exacta"],
        "servicio": row["servicio"],
        "resultado": row["resultado"],
        "fuentes_evaluadas": row["fuentes_evaluadas"],
        "accion": row["accion_inicial"],
        "huella_fila_original_sha256": row["huella_inicial_sha256"],
    } for row in search_matrix[:165]]
    history = [{
        **{field: row[field] for field in NEGATIVE_HISTORY_FIELDS[:6]},
        "prioridad_base": row["prioridad_final"],
        "desencadenante_base": row["desencadenante"],
        "huella_fila_original_sha256": row["huella_inicial_sha256"],
        "delta_preservado": row["delta_auditoria_2026_08_08"],
    } for row in negative_history]

    ownership: dict[str, str] = {}
    for row in claim_matrix:
        owner = row["clave_inicial"]
        for claim in expand_claims(row["claves_finales"]):
            if claim in ownership:
                raise ReconstructionError(f"Destino final duplicado en matriz: {claim}")
            ownership[claim] = owner
    origins: list[dict[str, str]] = []
    for row in read_csv(
        ROOT / "docs/auditorias/mapa_claves_inicial_final_2026-08-08.csv"
    ):
        temporary = row["clave_pre_renumeracion"]
        if int(temporary.split("-")[1]) <= 1840 or temporary.startswith("C-99"):
            continue
        if (
            temporary == row["clave_final"]
            and int(temporary.split("-")[1]) >= 1953
        ):
            # Alta prospectiva posterior a la matriz histórica que estamos
            # reconstruyendo; no pertenece al manifiesto temporal congelado.
            continue
        owner = ownership[row["clave_final"]]
        origin = "NUEVA" if owner.startswith("NUEVA:") else owner
        origins.append({"clave_temporal": temporary, "origen": origin})

    baseline_sources = git_csv("data/apendices/A_fuentes.csv")
    current_ids = {
        row["clave"] for row in read_csv(ROOT / "data/apendices/A_fuentes.csv")
    }
    matrix_by_id = {row["clave_inicial"]: row for row in source_matrix}
    removed: list[dict[str, str]] = []
    for source in baseline_sources:
        key = source["clave"]
        if key in current_ids:
            continue
        action = matrix_by_id[key]["accion_final"]
        match = re.fullmatch(r"RETIRADA: (.*) Destino: (.*)", action)
        if match:
            motive, destination = match.groups()
        else:
            motive = (
                "Sin referencia final en afirmaciones ni en el catálogo A vivo; "
                "la retirada no equivale a desestimación científica."
            )
            destination = (
                "Permanece en el commit inicial, el maestro histórico y la "
                "matriz inicial→final; no se reasigna la clave."
            )
        removed.append({
            "clave": key, "motivo": motive,
            "destino_documental": destination,
        })

    metadata = {
        "metodo": "reconstruccion_desde_git_y_huellas_versionadas",
        "commit_evidencia_versionada": EVIDENCE_COMMIT,
        "commit_pre_auditoria": BASELINE_COMMIT,
        "limitacion": (
            "Las filas C conservan los campos iniciales aún publicados y la "
            "huella completa original; los campos no publicados no se infieren."
        ),
        "conteos": {
            "afirmaciones": len(claims), "fuentes": len(sources),
            "requisitos": len(requirements), "busquedas": len(searches),
            "historia_bn": len(history), "origenes_temporales": len(origins),
            "fuentes_retiradas": len(removed),
        },
    }
    payloads = {
        output / "afirmaciones_iniciales.csv": csv_bytes(CLAIM_FIELDS, claims),
        output / "fuentes_iniciales.csv": csv_bytes(SOURCE_FIELDS, sources),
        output / "requisitos_iniciales.csv": csv_bytes(
            REQUIREMENT_FIELDS, requirements
        ),
        output / "busquedas_iniciales.csv": csv_bytes(SEARCH_FIELDS, searches),
        output / "historia_bn_inicial.csv": csv_bytes(
            NEGATIVE_HISTORY_FIELDS, history
        ),
        output / "origenes_afirmaciones_temporales.csv": csv_bytes(
            ORIGIN_FIELDS, origins
        ),
        output / "fuentes_retiradas.csv": csv_bytes(
            REMOVED_SOURCE_FIELDS, removed
        ),
        output / "delta_apendices_base.csv": git_file(
            "docs/auditorias/delta_apendices_2026-08-08.csv", EVIDENCE_COMMIT
        ),
        output / "proveniencia.json": (
            json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8"),
    }
    return payloads


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        payloads = reconstructed_payloads()
    except (OSError, KeyError, ValueError, ReconstructionError) as error:
        print(f"RECONSTRUCCIÓN FALLIDA: {error}", file=sys.stderr)
        return 1
    mismatches = []
    for path, payload in payloads.items():
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        elif not path.exists() or path.read_bytes() != payload:
            mismatches.append(path.relative_to(ROOT).as_posix())
    if mismatches:
        print("INSUMOS RECONSTRUIDOS DESACTUALIZADOS: " + ", ".join(mismatches))
        return 1
    print(
        "INSUMOS HISTÓRICOS RECONSTRUIDOS: "
        f"archivos={len(payloads)}; modo={'escritura' if args.write else 'check'}; "
        f"commit_evidencia={EVIDENCE_COMMIT}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
