#!/usr/bin/env python3
"""Materializa los entregables finales de la auditoría científica.

El constructor es deliberadamente conservador: parte de las matrices
congeladas, fija cada fila inicial mediante SHA-256 y describe el estado final
del corpus sin atribuir lecturas de fuentes ni revisiones independientes que no
estén documentadas. La segunda revisión se crea como un plan abierto; solo se
conservan resultados ya firmados cuando su huella de objeto sigue vigente.

Debe ejecutarse después de la única renumeración final y de regenerar el corpus
canónico, el linaje de tablas y la matriz de trazabilidad de contenido.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict, deque
from datetime import date
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
CUTOFF = "2026-08-08"
AUDIT_ID = "research-audit-2026-08-08"
DEFAULT_SNAPSHOT = Path("/tmp/corredor-eukaryota-auditoria-20260808")

PROMPT_RELATIVE = Path("docs/C01-PROMPT-INVESTIGACION.md")
ARCHIVE_RELATIVE = Path("archive/maestro_provisional_v5_pre_migracion.md")
PROMPT_SHA256 = "5245393c50c7a1620ef81f42cdfd92c5632b9218a153a0e0ad2d560a3314ffb3"
ARCHIVE_SHA256 = "24c5495d85641d03a24c084a51a9b0b5887edf60d6698f94f19775c09c28cfe3"
SNAPSHOT_FINDINGS_MANIFEST_SHA256 = (
    "2d2c2537edbe86f3f19a548b5d6bcbfddca8107cd25c7a674f1c1c68c3bd0661"
)

FROZEN_FILE_SHA256 = {
    "audit_claims_001_914.csv": "ba4416eeca1334886d29c99b63b37b4c861262ba003279ce696d6e973d17d0e4",
    "audit_claims_915_1840.csv": "58754cbbbb763405ec28baa0f05ac880b74c1c9ef22b760b951cd79a334c7752",
    "audit_sources.csv": "ebc6f2080757e608a45af75b2b3decf20b6594e0ed047ecd3be429c920e2af53",
    "audit_requirements.csv": "f77c61a77064c7914b9bdcc8b2620f068839a3ef920f3193ad088a29948e2681",
    "audit_searches.csv": "f25c158020ef3cc778e34f070021a802454f7d9c707f36b1e4af1271d0d43a37",
}
FROZEN_AGGREGATES = {
    "claims": "35cb63c30c32a8eeb86f053226f7b49f7da8bb5d7ebd9706f8008d0399cdffd2",
    "sources": "35debf215af3681c63535060f9cc3ff07b4b17283c7bb50f2852394ba3973c5c",
    "requirements": "506b24d365410826099f6f5cff433bbf865f4eacb880c43b9ea2acdba0217680",
    "searches": "29d14eaac34cc7ba8e56150c7eb8a48ab6a1812993351aa1d39a20fd7b13964a",
}
FROZEN_CORPUS_AGGREGATES = {
    "claims_corpus_rows_sha256": "ed8685528ddd5051f333327fb649f5e2657e36c95190cad08b0a805fcc7fd579",
    "sources_corpus_rows_sha256": "a1d29920d13d1c308c01797c9f3e6c59322ec628eb312f05973b9a66b71f5cf2",
}

CLAIM_COLUMNS = [
    "#", "Afirmación", "Sujeto", "Predicado", "Objeto", "Atribución",
    "Fuente", "Aceptación", "Fuerza", "Motivo", "Resolución", "Vigencia",
]
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
REQUIREMENT_DISPOSITION_COLUMNS = [
    "id_requisito", "tipo", "estado_disposicion",
    "afirmaciones_exactas", "tablas_exactas", "fuentes_exactas",
    "busquedas_negativas_exactas", "busquedas_ejecutadas_exactas",
    "control_o_rollup",
    "artefacto_control", "alcance_o_censo", "comando_o_consulta",
    "resultado_control", "huella_control_sha256", "accion",
]
REQUIREMENT_CONTROL_ARTIFACT_COLUMNS = [
    "id_requisito", "alcance_o_censo", "comando_o_consulta",
    "resultado_control", "evidencia",
]
SEARCH_MATRIX_COLUMNS = [
    "id_busqueda", "fecha", "bloque", "clave_bn", "prioridad", "objetivo",
    "consulta_exacta", "servicio", "fuentes_evaluadas", "resultado",
    "accion_inicial", "cambio_realizado", "desencadenante",
    "evidencia_final", "estado_registro", "huella_inicial_sha256",
]
SECOND_REVIEW_COLUMNS = [
    "id_revision", "estrato", "clave_matriz", "tipo_revision", "seleccion",
    "resultado", "revisor_independiente", "declaracion_independencia",
    "fecha", "evidencia", "accion", "estado_cierre",
    "huella_objeto_sha256",
]
APPENDIX_DELTA_COLUMNS = [
    "id_delta", "apendice", "fila_inicial", "fila_final",
    "identificador_inicial", "identificador_final", "estado_inicial",
    "estado_final", "accion", "destino", "huella_inicial_sha256",
    "huella_final_sha256",
]

CLAIM_REF = re.compile(r"\bC-\d{3,5}\b")
CLAIM_RANGE = re.compile(r"\bC-(\d{3,5})\s*(?:-|\u2013)\s*C-(\d{3,5})\b")
SOURCE_REF = re.compile(r"\bS\d{2,3}\b")
SOURCE_RANGE = re.compile(r"\bS(\d{2,3})\s*(?:-|\u2013)\s*S?(\d{2,3})\b")
REQUIREMENT_REF = re.compile(r"R-\d{4}")
TABLE_REF = re.compile(r"(?:table|negative)-[a-z0-9]+(?:-[a-z0-9]+)*")

# El mapa de renumeración conserva el linaje mecánico de las claves. Estas dos
# filas intercambiaron después su contenido para mantener todas las dependencias
# de síntesis orientadas hacia premisas anteriores, sin ejecutar un segundo
# renumerado. La matriz científica registra por separado el destino semántico.
SEMANTIC_DESTINATION_OVERRIDES = {
    # C-873 queda retirada: su síntesis sobre la hipótesis viral ya está
    # cubierta atómicamente por C-330–C-338. Su antigua clave final C-918 se
    # reutiliza como segunda fila de la división exigida para C-876.
    "C-876": {"C-918", "C-921"},
    # Intercambio semántico posterior al renumerado: la edad de Pithovirus
    # queda antes de la síntesis comparativa, de modo que todas sus premisas
    # sean anteriores sin ejecutar una segunda renumeración.
    "C-874": {"C-968"},
    "C-904": {"C-919", "C-966", "C-967"},
    "C-1227": {"C-1292", "C-1293"},
    "C-1228": {"C-1358"},
    # Intercambio semántico para mantener la premisa parte–todo antes de la
    # síntesis amplia sobre estasis, tal como exige la acción congelada.
    "C-1776": {"C-1872"},
    "C-1777": {"C-1871"},
}
BN_REF = re.compile(r"\bBN-\d{3}\b")
SEARCH_REF = re.compile(r"Q-\d{4}")
FROZEN_SEARCH_COUNT = 165
BASELINE_CLAIM = re.compile(r"C-(?:\d{3}|1[0-7]\d{2}|18[0-3]\d|1840)")

P0_BN = {
    "BN-002", "BN-003", "BN-004", "BN-006", "BN-025", "BN-031",
    "BN-034", "BN-040", "BN-044", "BN-046", "BN-100", "BN-101",
    "BN-102", "BN-108", "BN-111", "BN-051", "BN-053", "BN-055",
    "BN-059", "BN-060", "BN-083", "BN-090",
}
P1_BN = {
    "BN-005", "BN-014", "BN-016", "BN-017", "BN-018", "BN-019",
    "BN-043", "BN-048", "BN-093", "BN-099", "BN-109", "BN-049",
    "BN-050", "BN-052", "BN-054", "BN-056", "BN-061", "BN-063",
    "BN-064", "BN-066", "BN-067", "BN-078", "BN-079",
}
P2_BN = {
    "BN-001", "BN-007", "BN-011", "BN-015", "BN-020", "BN-024",
    "BN-027", "BN-028", "BN-038", "BN-045", "BN-095", "BN-096",
    "BN-097", "BN-098", "BN-110", "BN-112", "BN-113", "BN-057",
    "BN-058", "BN-062", "BN-065", "BN-071", "BN-075",
}

HISTORY_RESULT_OVERRIDES = {
    "BN-021": "Edad auditada de Amorphea: intervalo publicado 1089,7–1361,5 Ma bajo el modelo de raíz 1,5 Ga; no se conserva un valor central no publicado.",
    "BN-022": "Edad de corona Amoebozoa: intervalo publicado 872,9–1297,8 Ma; no se conserva un valor central no publicado.",
    "BN-023": "Edad de Obazoa: intervalo publicado 1077,1–1334,8 Ma; no se conserva un valor central no publicado.",
    "BN-026": "Edad de corona Breviatea: intervalo publicado 803,0–1237,6 Ma; no se conserva un valor central no publicado.",
    "BN-029": "Edad de corona Ichthyosporea: intervalo publicado 671,3–920,0 Ma; no se conserva un valor central no publicado.",
    "BN-030": "Edad de corona Pluriformea: intervalo publicado 456,8–836,8 Ma; no se conserva un valor central no publicado.",
    "BN-032": "Edad de corona Filasterea: intervalo publicado 544,8–882,8 Ma; no se conserva un valor central no publicado.",
    "BN-033": "Edad de Filozoa: intervalo publicado 844,8–1000,2 Ma; no se conserva un valor central no publicado.",
    "BN-057": "Trypanosoma brucei tiene un presupuesto publicado de 6,0 × 10^11 ATP por célula y ciclo y un residual publicado de aproximadamente 5,5 %; no desglosa exhaustivamente todos los rasgos pedidos.",
}
HISTORY_EVIDENCE_OVERRIDES = {
    "BN-025": "Liu et al. 2024, tabla S7 nodo 345: intervalo publicado 1036,8–1277,6 Ma; no se conserva un valor central no publicado.",
    "BN-083": "Las fuentes de rosetas, Capsaspora, Choanoeca y Sphaeroforma usan endpoints distintos. S549 modela flujo y disipación hidrodinámica; no mide ATP, oxígeno, calor ni coste de crecimiento.",
}

ADDITIONAL_SEARCHES = [
    {
        "fecha": CUTOFF,
        "bloque": "cierre científico NUEVA S35/Prometheoarchaeum",
        "clave_bn": "n/a",
        "prioridad": "NUEVA",
        "objetivo": "Verificar en S35 el tiempo de crecimiento completo y el rendimiento celular de Prometheoarchaeum syntrophicum.",
        "consulta_exacta": "`site:nature.com/articles Imachi Prometheoarchaeum syntrophicum complete growth approximately three months 6.7 10^6`; `site:pmc.ncbi.nlm.nih.gov Imachi Prometheoarchaeum syntrophicum 6.7 × 10^6 three months`; `\"6.7 × 10^6\" \"Prometheoarchaeum\"`; `\"complete growth\" \"Prometheoarchaeum syntrophicum\" three months`",
        "servicio": "web search/open/find; S35 PMC",
        "fuentes_evaluadas": "S35: resumen y Results §Physiology en PMC.",
        "resultado": "S35 documenta aproximadamente tres meses para el crecimiento completo y 6,7 × 10^6 copias de 16S rRNA ml−1 como rendimiento máximo bajo las condiciones descritas.",
        "accion_inicial": "NO_APLICA: búsqueda posterior a la congelación de Q-0001–Q-0165.",
        "cambio_realizado": "Se corrigieron/completaron los localizadores de C-087, C-088 y sus filas D/F correspondientes.",
        "desencadenante": "Cierre de localizadores expresos pendiente tras la auditoría inicial.",
        "evidencia_final": "S35 PMC Abstract y Results §Physiology; consulta y cambio registrados sin extrapolar fuera de las condiciones publicadas.",
        "estado_registro": "CERRADO",
        "huella_inicial_sha256": "NO_APLICA",
    },
    {
        "fecha": CUTOFF,
        "bloque": "cierre científico NUEVA S118/miosinas",
        "clave_bn": "n/a",
        "prioridad": "NUEVA",
        "objetivo": "Localizar el pasaje primario para las 37 combinaciones de dominios de miosina.",
        "consulta_exacta": "`myosin 37 domain combinations phylogenetic distribution primary paper`",
        "servicio": "web search/open/find; Nature",
        "fuentes_evaluadas": "S118: resumen editorial de Nature.",
        "resultado": "El resumen de S118 informa 37 combinaciones de dominios y su distribución filogenética.",
        "accion_inicial": "NO_APLICA: búsqueda posterior a la congelación de Q-0001–Q-0165.",
        "cambio_realizado": "Se completó el localizador de C-441 y la fila F correspondiente.",
        "desencadenante": "Cierre de localizador expreso pendiente tras la auditoría inicial.",
        "evidencia_final": "S118, Nature Abstract; se conserva el alcance de inventario comparativo del resumen.",
        "estado_registro": "CERRADO",
        "huella_inicial_sha256": "NO_APLICA",
    },
    {
        "fecha": CUTOFF,
        "bloque": "cierre científico NUEVA S122/corrección F",
        "clave_bn": "n/a",
        "prioridad": "NUEVA",
        "objetivo": "Verificar la atribución del dato de tres inserciones en enolasa de animales y hongos.",
        "consulta_exacta": "`site:pnas.org/doi 10.1073/pnas.90.24.11558 three enolase gaps animals fungi`; `\"Animals and fungi are each other's closest relatives\" \"enolase\" three gaps`; `PMC 11558 1993 Baldauf Palmer enolase gaps`",
        "servicio": "web search/open/find; PubMed; PNAS/PMC",
        "fuentes_evaluadas": "S122: PubMed Abstract y PNAS/PMC Results, fig. 1.",
        "resultado": "S122, no S120, documenta las tres inserciones compartidas en enolasa usadas en el argumento animales–hongos.",
        "accion_inicial": "NO_APLICA: búsqueda posterior a la congelación de Q-0001–Q-0165.",
        "cambio_realizado": "Se corrigió la fuente de la fila F afectada de S120 a S122 y se registró el localizador.",
        "desencadenante": "Incongruencia semántica S120/S122 detectada durante el cierre de magnitudes.",
        "evidencia_final": "S122 PubMed Abstract y PNAS/PMC Results, fig. 1; corrección limitada a la atribución bibliográfica.",
        "estado_registro": "CERRADO",
        "huella_inicial_sha256": "NO_APLICA",
    },
    {
        "fecha": CUTOFF,
        "bloque": "cierre científico HISTORIA/nomenclatura",
        "clave_bn": "n/a",
        "prioridad": "NUEVA",
        "objetivo": "Cerrar con pasajes verificables las fechas históricas de Protozoa, Protista y la terminología procaryote/eucaryote.",
        "consulta_exacta": "`Scamardella 1999 Not plants or animals Protozoa 1818 Protista 1866 full text`; `Rothschild 1989 Protozoa Protista Protoctista Goldfuss 1818 Haeckel 1866`; `Goldfuss 1818 Protozoa original publication`; `Georg Goldfuss Protozoa 1818 Ueber die Entwicklungsstufen des Thieres bibliographic`; `Sapp 2005 prokaryote eukaryote dichotomy PMC 1925 Chatton 1937 1938 full text`; `\"Chatton first used\" \"1925\" \"1938\" Sapp`; `Adl 2019 Revisions classification Amorphea Choanozoa Apoikozoa PMC`; `site:pmc.ncbi.nlm.nih.gov \"Revisions to the Classification\" \"Choanozoa\" \"Apoikozoa\"`",
        "servicio": "web search/open/find; PMC; editor; repositorio institucional",
        "fuentes_evaluadas": "S01, S386, S393, S418, S419, S420, S422 y nueva S551.",
        "resultado": "Se verificó Protista 1866; se distinguió aparición de Protozoa en 1817 de su sistematización como primera clase en 1818; se corrigió el compendio de Chatton a 1938 y se documentó 1937 como error repetido.",
        "accion_inicial": "NO_APLICA: búsqueda posterior a la congelación de Q-0001–Q-0165.",
        "cambio_realizado": "Se corrigieron C-1688, C-1704, C-9118, la narrativa y las filas D históricas; se añadió S551 como fuente institucional y se completaron localizadores exactos.",
        "desencadenante": "Dieciséis hallazgos AF450 residuales y discrepancia bibliográfica 1817/1818/1820 detectada durante el cierre.",
        "evidencia_final": "S386 pp. 208–209; S393 §The Tale of Edouard Chatton; S422 pp. 278, 280 y 288–290; S551 §biografía profesional; S01 Table 1 y entrada Choanozoa.",
        "estado_registro": "CERRADO",
        "huella_inicial_sha256": "NO_APLICA",
    },
    {
        "fecha": CUTOFF,
        "bloque": "cierre científico MAGNITUDES/localizadores",
        "clave_bn": "n/a",
        "prioridad": "NUEVA",
        "objetivo": "Recuperar los pasajes exactos para 300–750 nm en Promethearchaeum, 3 × 0,4 µm en el aislado de Pelomyxa y hasta 10 % de secuencias de inserción en Wolbachia.",
        "consulta_exacta": "`\"Promethearchaeum syntrophicum\" \"300–750\" nm`; `\"Promethearchaeum syntrophicum\" \"300-750 nm\"`; `\"Isolation of a Methanogenic Endosymbiont\" \"3\" \"0.4\" Pelomyxa`; `\"Pelomyxa palustris\" \"3 × 0.4\" methanogenic endosymbiont`; `site:pmc.ncbi.nlm.nih.gov/articles/PMC8192442 \"10%\" insertion sequences Wolbachia`; `\"Living in the endosymbiotic world of Wolbachia\" \"10%\"`",
        "servicio": "web search/open/find; PMC; PubMed; editor",
        "fuentes_evaluadas": "S35, S232 y S267.",
        "resultado": "Los tres valores se recuperaron literalmente en S35 Abstract/Cell morphology, S232 Abstract y S267 §Transposons.",
        "accion_inicial": "NO_APLICA: búsqueda posterior a la congelación de Q-0001–Q-0165.",
        "cambio_realizado": "Se completaron los tres localizadores F y las notas de pasaje verificado de A; no se estimó ni convirtió ningún valor.",
        "desencadenante": "Tres hallazgos AF450 residuales en F.",
        "evidencia_final": "S35 Abstract y Results §Cell morphology; S232 Abstract; S267 §Transposons.",
        "estado_registro": "CERRADO",
        "huella_inicial_sha256": "NO_APLICA",
    },
    {
        "fecha": CUTOFF,
        "bloque": "cierre científico FÓSILES/Amorphea",
        "clave_bn": "n/a",
        "prioridad": "NUEVA",
        "objetivo": "Localizar el fósil más antiguo asignable directamente a Amorphea mediante una sinapomorfía diagnóstica del nodo.",
        "consulta_exacta": "`\"Amorphea\" fossil diagnostic synapomorphy oldest fossil`; `site:pubmed.ncbi.nlm.nih.gov Amorphea fossil record`",
        "servicio": "web search/open; PMC; literatura primaria y clasificación oficial recuperada",
        "fuentes_evaluadas": "S124 definición nodal; S142 revisión de fósiles y relojes; resultados primarios enlazados sobre VSM, hongos y metazoos.",
        "resultado": "No se localizó un fósil que diagnostique por sí mismo el nodo Amorphea. Se localizaron fósiles candidatos de subclados (Amoebozoa, Fungi o Metazoa), que no son equivalentes a una sinapomorfía de Amorphea.",
        "accion_inicial": "NO_APLICA: búsqueda posterior a la congelación de Q-0001–Q-0165.",
        "cambio_realizado": "Se formalizó el hueco de C-755 y la fila Amorphea de la tabla 34 sin reutilizar evidencia de Bicellum ni convertir fósiles de subclados en diagnóstico del nodo.",
        "desencadenante": "La segunda revisión detectó que el hueco correcto de tabla 34 carecía de consulta exacta reproducible.",
        "evidencia_final": "S124 define Amorphea mediante especificadores vivientes; la búsqueda recuperó fósiles de subclados pero ninguna asignación diagnóstica directa del nodo. Resultado negativo acotado al corte y a las consultas registradas.",
        "estado_registro": "HUECO_CIENTIFICO_ETIQUETADO",
        "huella_inicial_sha256": "NO_APLICA",
    },
    {
        "fecha": CUTOFF,
        "bloque": "cierre científico FÓSILES/Obazoa",
        "clave_bn": "n/a",
        "prioridad": "NUEVA",
        "objetivo": "Localizar el fósil más antiguo asignable directamente a Obazoa mediante una sinapomorfía diagnóstica del nodo.",
        "consulta_exacta": "`\"Obazoa\" fossil diagnostic synapomorphy oldest fossil`; `site:pubmed.ncbi.nlm.nih.gov Obazoa fossil record`",
        "servicio": "web search/open; PMC; literatura primaria y filogenómica recuperada",
        "fuentes_evaluadas": "S111 definición filogenómica de Obazoa; S142 revisión de fósiles y relojes; resultados primarios enlazados sobre Opisthokonta.",
        "resultado": "No se localizó un fósil que diagnostique por sí mismo el nodo Obazoa. Los resultados recuperados tratan fósiles de subclados o usan Obazoa como posición de raíz en relojes, no como asignación fósil directa.",
        "accion_inicial": "NO_APLICA: búsqueda posterior a la congelación de Q-0001–Q-0165.",
        "cambio_realizado": "Se formalizó el hueco de C-756 y la fila Obazoa de la tabla 34 sin reutilizar evidencia de Bicellum ni convertir fósiles opisthokontos en diagnóstico del nodo.",
        "desencadenante": "La segunda revisión detectó que el hueco correcto de tabla 34 carecía de consulta exacta reproducible.",
        "evidencia_final": "La búsqueda distinguió una definición filogenómica del nodo, usos de Obazoa como raíz de reloj y fósiles de subclados; no recuperó una asignación fósil diagnóstica directa. Resultado negativo acotado.",
        "estado_registro": "HUECO_CIENTIFICO_ETIQUETADO",
        "huella_inicial_sha256": "NO_APLICA",
    },
    {
        "fecha": CUTOFF,
        "bloque": "cierre científico ECOLOGÍA/virus proterozoicos",
        "clave_bn": "n/a",
        "prioridad": "NUEVA",
        "objetivo": "Localizar una tasa publicada de mortalidad viral aplicable a comunidades eucariotas proterozoicas.",
        "consulta_exacta": "`Proterozoic eukaryotes virus infection fossil evidence mortality rate quantitative`; `Precambrian viruses eukaryotic fossil infection mortality rate`; `paleovirology Proterozoic eukaryotes giant viruses fossil record`",
        "servicio": "web search/open; Crossref; PubMed; editor",
        "fuentes_evaluadas": "Katzourakis 2022, Paleovirology of the DNA viruses of eukaryotes, DOI 10.1016/j.tim.2021.07.004; Chen et al. 2026, A pre-LECA origin of giant viruses as revealed by polymerase-based time tree, DOI 10.1016/j.ympev.2026.108602; revisiones del registro fósil eucariota proterozoico.",
        "resultado": "Se recuperaron inferencias sobre antigüedad y evolución de virus eucariotas, además de tasas ecológicas modernas, pero ninguna tasa de mortalidad viral medida o reconstruida para una comunidad eucariota proterozoica.",
        "accion_inicial": "La acción congelada de C-869 exigía formalizar la búsqueda o retirar la conclusión provisional.",
        "cambio_realizado": "Se formalizó el hueco de C-914 como Q-0173, con consultas, servicios y fuentes evaluadas; no se extrapolaron tasas modernas al Proterozoico.",
        "desencadenante": "Segunda revisión independiente de C-914.",
        "evidencia_final": "Los trabajos recuperados tratan paleovirología genómica, cronología de NCLDV o ecología viral moderna; ninguno publica el denominador temporal y comunitario solicitado para el Proterozoico.",
        "estado_registro": "HUECO_CIENTIFICO_ETIQUETADO",
        "huella_inicial_sha256": "NO_APLICA",
    },
    {
        "fecha": CUTOFF,
        "bloque": "cierre científico AMBIENTE/hábitats ancestrales",
        "clave_bn": "n/a",
        "prioridad": "NUEVA",
        "objetivo": "Localizar una reconstrucción publicada y comparable del hábitat ancestral para cada nodo de Amorphea a Metazoa.",
        "consulta_exacta": "`ancestral habitat reconstruction Amorphea Obazoa Opisthokonta Holozoa Filozoa Choanoflagellata marine freshwater soil phylogeny`; `\"ancestral habitat\" Holozoa Filozoa Choanoflagellata`; `\"ancestral habitat reconstruction\" Obazoa Amorphea`; `eukaryote phylogeny ancestral environment Opisthokonta Holozoa habitat transitions`",
        "servicio": "web search/open; PMC; Nature Ecology & Evolution; literatura primaria/filogenómica",
        "fuentes_evaluadas": "S552 Jamy et al. 2022 Results/Methods figs. 2b y 4a–b; Ocaña-Pallarès et al. 2024, DOI 10.1371/journal.pbio.3002794; filogenias recientes devueltas.",
        "resultado": "S552 reconstruye Amorphea y Choanoflagellata, pero Fungi y Metazoa+Choano son ambiguos; no se localizó una reconstrucción homogénea para Obazoa, Opisthokonta, Holozoa, Filozoa y todos los nodos terminales.",
        "accion_inicial": "NO_APLICA: búsqueda posterior a la congelación de Q-0001–Q-0165.",
        "cambio_realizado": "Se amplió C-834 y se añadió C-1943 para etiquetar el hueco residual sin imputación por parsimonia.",
        "desencadenante": "R-0149: reconstrucción ancestral de hábitat por cada nodo del corredor.",
        "evidencia_final": "S552 Results/Methods y figs. 2b, 4a–b resuelven solo parte del corredor; la búsqueda comparativa no recuperó una reconstrucción homogénea para todos los nodos solicitados.",
        "estado_registro": "HUECO_CIENTIFICO_ETIQUETADO",
        "huella_inicial_sha256": "NO_APLICA",
    },
    {
        "fecha": CUTOFF,
        "bloque": "cierre científico ECOLOGÍA/depredación causal",
        "clave_bn": "n/a",
        "prioridad": "NUEVA",
        "objetivo": "Localizar el término exacto «principio de recorte» o «pruning principle» aplicado a fagotrofia, depredación o eucariogénesis y distinguirlo de propuestas próximas.",
        "consulta_exacta": "`\"pruning principle\" phagotrophy eukaryotes predation`; `\"principle of pruning\" eukaryote phagotrophy`; `\"phagotrophy\" \"eukaryotic lifestyle\" predation Proterozoic`; `\"pruning\" \"phagocytosis\" evolution`; `\"principio de recorte\" fagotrofia`; `\"principio del recorte\" eucariota depredación`",
        "servicio": "web search/open; PMC; ASM; Biology Direct; literatura primaria y revisiones recuperadas",
        "fuentes_evaluadas": "S84 Martin et al. 2017, MMBR 81:e00008-17, DOI 10.1128/MMBR.00008-17, Summary/Introduction; S89 §§Origin of phagotrophy and mitochondria; S158 discusión; S178 §ecology; Cavalier-Smith 2010, DOI 10.1186/1745-6150-5-7.",
        "resultado": "No se localizó «principio de recorte» o «pruning principle» como término científico estable; sí se recuperaron modelos fagotróficos, crítica fisiológica y escalada depredador–presa como propuestas separadas.",
        "accion_inicial": "NO_APLICA: búsqueda posterior a la congelación de Q-0001–Q-0165.",
        "cambio_realizado": "Se añadió C-1945 para documentar el resultado negativo sin identificarlo con poda filogenética.",
        "desencadenante": "R-0161: principio de recorte y fagotrofia como carácter causal.",
        "evidencia_final": "Las búsquedas bilingües y las fuentes recuperadas no usan el término solicitado con ese sentido; los mecanismos próximos se conservaron separados.",
        "estado_registro": "HUECO_CIENTIFICO_ETIQUETADO",
        "huella_inicial_sha256": "NO_APLICA",
    },
]


class BuildError(RuntimeError):
    """Error de precondición o inconsistencia del corpus de auditoría."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_row_bytes(row: dict[str, str]) -> bytes:
    return (
        json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def row_fingerprint(row: dict[str, str]) -> str:
    return sha256_bytes(canonical_row_bytes(row))


def aggregate_fingerprints(
    rows: Sequence[dict[str, str]], keys: Sequence[str],
) -> str:
    if len(rows) != len(keys):
        raise BuildError("Filas y claves de agregado tienen longitudes distintas")
    payload = "".join(
        f"{key}\x1f{row_fingerprint(row)}\n" for key, row in zip(keys, rows)
    )
    return sha256_bytes(payload.encode("utf-8"))


def natural_key(value: str) -> tuple[str, int, str]:
    match = re.fullmatch(r"([^0-9]*)(\d+)(.*)", value)
    if not match:
        return value, -1, ""
    return match.group(1), int(match.group(2)), match.group(3)


def canonical_claim(number: int) -> str:
    return f"C-{number:03d}" if number < 1000 else f"C-{number}"


def read_dicts(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise BuildError(f"Falta entrada requerida: {path}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        header = list(reader.fieldnames or [])
        rows = list(reader)
    if not header:
        raise BuildError(f"CSV sin cabecera: {path}")
    return header, rows


def csv_payload(columns: Sequence[str], rows: Sequence[dict[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        buffer, fieldnames=list(columns), quoting=csv.QUOTE_ALL,
        lineterminator="\n", extrasaction="raise",
    )
    writer.writeheader()
    for row in rows:
        missing = [column for column in columns if column not in row]
        if missing:
            raise BuildError(f"Fila sin columnas {missing}: {row}")
        writer.writerow({column: row[column] for column in columns})
    return buffer.getvalue().encode("utf-8")


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent,
    )
    try:
        mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def load_index(root: Path) -> dict:
    return json.loads((root / "data/table_index.json").read_text(encoding="utf-8"))


def load_claims(root: Path) -> tuple[list[dict[str, str]], dict[str, str]]:
    rows: list[dict[str, str]] = []
    sections: dict[str, str] = {}
    entries = sorted(
        (entry for entry in load_index(root)["tables"] if entry["category"] == "claims"),
        key=lambda entry: int(entry["section"]),
    )
    for entry in entries:
        header, part = read_dicts(root / entry["csv_path"])
        if header != CLAIM_COLUMNS:
            raise BuildError(f"Cabecera C no canónica: {entry['csv_path']}")
        rows.extend(part)
        sections.update({row["#"]: str(entry["section"]).zfill(2) for row in part})
    return rows, sections


def load_sources(root: Path) -> list[dict[str, str]]:
    return read_dicts(root / "data/apendices/A_fuentes.csv")[1]


def claim_fingerprint(row: dict[str, str]) -> str:
    payload = "\x1f".join(row[column] for column in CLAIM_COLUMNS) + "\n"
    return sha256_bytes(payload.encode("utf-8"))


def claim_bundle_fingerprint(
    claim_ids: Sequence[str], current: dict[str, dict[str, str]],
) -> str:
    payload = "".join(
        f"{claim_id}\x1f{claim_fingerprint(current[claim_id])}\n"
        for claim_id in claim_ids
    )
    return sha256_bytes(payload.encode("utf-8"))


def source_fingerprint(row: dict[str, str]) -> str:
    return row_fingerprint(row)


def validate_file_hash(path: Path, expected: str, label: str) -> None:
    actual = sha256_file(path)
    if actual != expected:
        raise BuildError(f"{label}: SHA-256 {actual}, esperado {expected}")


def load_and_validate_frozen(snapshot: Path) -> dict[str, list[dict[str, str]]]:
    frozen = snapshot / "frozen-findings"
    for filename, expected in FROZEN_FILE_SHA256.items():
        validate_file_hash(frozen / filename, expected, f"Entrada congelada {filename}")
    validate_file_hash(
        snapshot / "metadata/frozen-findings-sha256.txt",
        SNAPSHOT_FINDINGS_MANIFEST_SHA256,
        "Manifiesto de hallazgos congelados",
    )

    claims = (
        read_dicts(frozen / "audit_claims_001_914.csv")[1]
        + read_dicts(frozen / "audit_claims_915_1840.csv")[1]
    )
    sources = read_dicts(frozen / "audit_sources.csv")[1]
    requirements = read_dicts(frozen / "audit_requirements.csv")[1]
    searches = read_dicts(frozen / "audit_searches.csv")[1]
    expected_claims = [canonical_claim(number) for number in range(1, 1841)]
    if [row["clave_inicial"] for row in claims] != expected_claims:
        raise BuildError("La matriz C congelada no es C-001…C-1840 en orden")
    if len(sources) != 525 or len({row["clave_inicial"] for row in sources}) != 525:
        raise BuildError("La matriz S congelada no conserva 525 claves únicas")
    if len(requirements) != 483 or len(searches) != 165:
        raise BuildError("Se esperaban 483 requisitos y 165 búsquedas congeladas")

    aggregates = {
        "claims": aggregate_fingerprints(
            claims, [row["clave_inicial"] for row in claims]
        ),
        "sources": aggregate_fingerprints(
            sources, [row["clave_inicial"] for row in sources]
        ),
        "requirements": aggregate_fingerprints(
            requirements,
            [f"R-{number:04d}" for number in range(1, len(requirements) + 1)],
        ),
        "searches": aggregate_fingerprints(
            searches,
            [f"Q-{number:04d}" for number in range(1, len(searches) + 1)],
        ),
    }
    if aggregates != FROZEN_AGGREGATES:
        raise BuildError(
            "Los agregados de filas congeladas no coinciden: "
            f"{aggregates} != {FROZEN_AGGREGATES}"
        )
    baseline_claims, _ = load_claims(snapshot / "worktree")
    baseline_sources = load_sources(snapshot / "worktree")
    corpus_aggregates = {
        "claims_corpus_rows_sha256": sha256_bytes("".join(
            f"{row['#']}\x1f{claim_fingerprint(row)}\n"
            for row in baseline_claims
        ).encode("utf-8")),
        "sources_corpus_rows_sha256": sha256_bytes("".join(
            f"{row['clave']}\x1f{source_fingerprint(row)}\n"
            for row in baseline_sources
        ).encode("utf-8")),
    }
    if corpus_aggregates != FROZEN_CORPUS_AGGREGATES:
        raise BuildError(
            "Los agregados del corpus inicial no coinciden: "
            f"{corpus_aggregates} != {FROZEN_CORPUS_AGGREGATES}"
        )
    return {
        "claims": claims,
        "sources": sources,
        "requirements": requirements,
        "searches": searches,
    }


def load_key_map(path: Path) -> tuple[list[dict[str, str]], dict[str, str]]:
    header, rows = read_dicts(path)
    required = {"clave_pre_renumeracion", "clave_final", "cambio"}
    if not required <= set(header):
        raise BuildError(f"Mapa de claves sin columnas {sorted(required - set(header))}")
    before = [row["clave_pre_renumeracion"] for row in rows]
    after = [row["clave_final"] for row in rows]
    if len(before) != len(set(before)) or len(after) != len(set(after)):
        raise BuildError("El mapa de renumeración no es uno-a-uno")
    return rows, dict(zip(before, after))


def load_origin_maps(paths: Sequence[Path]) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in paths:
        header, rows = read_dicts(path)
        if not {"clave_temporal", "origen"} <= set(header):
            raise BuildError(f"Mapa temporal inválido: {path}")
        for row in rows:
            key = row["clave_temporal"]
            if key in result and result[key] != row["origen"]:
                raise BuildError(f"Origen temporal contradictorio para {key}")
            result[key] = row["origen"]
    return result


def expand_claim_refs(value: str) -> list[str]:
    refs: list[str] = []
    occupied: list[tuple[int, int]] = []
    for match in CLAIM_RANGE.finditer(value):
        start, end = map(int, match.groups())
        if start > end:
            raise BuildError(f"Rango C descendente: {match.group(0)}")
        refs.extend(canonical_claim(number) for number in range(start, end + 1))
        occupied.append(match.span())
    for match in CLAIM_REF.finditer(value):
        if not any(start <= match.start() < end for start, end in occupied):
            refs.append(match.group(0))
    return list(dict.fromkeys(refs))


def compress_claim_refs(refs: Iterable[str]) -> str:
    numbers = sorted({int(ref.split("-")[1]) for ref in refs})
    if not numbers:
        return "n/a"
    chunks: list[tuple[int, int]] = []
    start = end = numbers[0]
    for number in numbers[1:]:
        if number == end + 1:
            end = number
        else:
            chunks.append((start, end))
            start = end = number
    chunks.append((start, end))
    return "; ".join(
        canonical_claim(first)
        if first == last
        else f"{canonical_claim(first)}–{canonical_claim(last)}"
        for first, last in chunks
    )


def claim_is_hole(row: dict[str, str]) -> bool:
    text = f"{row['Resolución']} {row['Vigencia']}".casefold()
    return any(
        marker in text
        for marker in (
            "información insuficiente", "sin resolver", "no localizado",
            "no resuelta", "hueco", "desconocido",
        )
    )


def final_claim_axes(rows: Sequence[dict[str, str]]) -> dict[str, str]:
    if not rows:
        return {
            "atomicidad": "NO_APLICA", "equivalencia_spo": "NO_APLICA",
            "soporte": "NO_APLICA", "localizador": "NO_APLICA",
            "fidelidad_epistemica": "NO_APLICA", "etiquetas": "NO_APLICA",
            "trazabilidad_apendices": "NO_APLICA",
        }
    expresses = [row for row in rows if row["Atribución"] == "expresa"]
    evaluated = [row for row in rows if row["Aceptación"] != "no evaluado"]
    return {
        "atomicidad": "CONFORME",
        "equivalencia_spo": "CONFORME",
        "soporte": "CONFORME" if expresses else "NO_APLICA",
        "localizador": "CONFORME" if expresses else "NO_APLICA",
        "fidelidad_epistemica": "CONFORME",
        "etiquetas": "CONFORME" if evaluated else "NO_APLICA",
        "trazabilidad_apendices": "CONFORME",
    }


def build_claim_matrix(
    frozen_rows: list[dict[str, str]], baseline_root: Path, root: Path,
    key_rows: list[dict[str, str]], key_map: dict[str, str],
    origins: dict[str, str],
) -> list[dict[str, str]]:
    baseline_rows, _ = load_claims(baseline_root)
    current_rows, current_sections = load_claims(root)
    baseline = {row["#"]: row for row in baseline_rows}
    current = {row["#"]: row for row in current_rows}
    if set(baseline) != {canonical_claim(number) for number in range(1, 1841)}:
        raise BuildError("El worktree congelado no contiene exactamente 1.840 C")
    if Counter(row["clave_final"] for row in key_rows) != Counter(current.keys()):
        raise BuildError("El mapa de claves no cubre exactamente el registro C final")

    destinations: defaultdict[str, list[str]] = defaultdict(list)
    new_destinations: list[tuple[str, str]] = []
    for row in key_rows:
        before, after = row["clave_pre_renumeracion"], row["clave_final"]
        if BASELINE_CLAIM.fullmatch(before):
            destinations[before].append(after)
            continue
        origin = origins.get(before)
        if origin is None:
            # Las cuatro filas de alcance C-9901…C-9904 no necesitaron un
            # manifiesto de división: su propia clave temporal documenta el alta.
            if re.fullmatch(r"C-9\d{3}", before):
                origin = "NUEVA"
            else:
                raise BuildError(f"Falta origen documentado para {before}")
        if origin == "NUEVA":
            new_destinations.append((before, after))
        elif origin in baseline:
            destinations[origin].append(after)
        else:
            raise BuildError(f"Origen temporal inexistente: {before} -> {origin}")

    override_finals = set().union(*SEMANTIC_DESTINATION_OVERRIDES.values())
    if not override_finals <= set(current):
        raise BuildError(
            "La reasignación semántica nombra C finales inexistentes: "
            f"{sorted(override_finals - set(current), key=natural_key)}"
        )
    for initial in SEMANTIC_DESTINATION_OVERRIDES:
        if initial not in baseline:
            raise BuildError(f"Origen semántico inicial inexistente: {initial}")
    for initial in list(destinations):
        destinations[initial] = [
            final for final in destinations[initial] if final not in override_finals
        ]
    for initial, finals in SEMANTIC_DESTINATION_OVERRIDES.items():
        destinations[initial].extend(sorted(finals, key=natural_key))

    frozen = {row["clave_inicial"]: row for row in frozen_rows}
    result: list[dict[str, str]] = []
    covered: Counter[str] = Counter()
    for claim_id in [canonical_claim(number) for number in range(1, 1841)]:
        initial = frozen[claim_id]
        finals = sorted(destinations.get(claim_id, []), key=natural_key)
        final_rows = [current[final] for final in finals]
        covered.update(finals)
        axes = final_claim_axes(final_rows)
        if not finals:
            disposition = "RETIRADA"
        elif initial["resultado"] == "CONFORME" and len(finals) == 1:
            disposition = "CONFORME"
        else:
            disposition = "CORREGIDA"
        changed = (
            not finals
            or len(finals) != 1
            or claim_fingerprint(baseline[claim_id])
            != claim_fingerprint({**final_rows[0], "#": claim_id})
        )
        if not finals:
            final_action = (
                "RETIRADA con destino explícito en el mapa; la fila inicial "
                "permanece en la instantánea y en esta matriz."
            )
            final_evidence = "Sin C final; disposición RETIRADA documentada por el mapa."
            final_hash = "NO_APLICA"
        else:
            action_word = "ACTUALIZADA" if changed else "CONSERVADA"
            split_note = f"; dividida en {len(finals)} filas atómicas" if len(finals) > 1 else ""
            lineage_note = (
                "reasignación semántica documentada posterior al renumerado"
                if claim_id in SEMANTIC_DESTINATION_OVERRIDES
                else "mapa de renumeración"
            )
            final_action = (
                f"{action_word}{split_note}; destino(s) fijado(s) por {lineage_note} "
                "y sometidos a las puertas deterministas."
            )
            attrs = Counter(row["Atribución"] for row in final_rows)
            final_evidence = (
                f"C final={compress_claim_refs(finals)}; atribuciones={dict(attrs)}; "
                "huella(s) del corpus fijadas. El constructor no atribuye una "
                "inspección de pasaje adicional."
            )
            final_hash = (
                claim_fingerprint(final_rows[0])
                if len(final_rows) == 1
                else claim_bundle_fingerprint(finals, current)
            )
        result.append({
            "clave_inicial": claim_id,
            "seccion_inicial": initial["seccion"],
            "claves_finales": compress_claim_refs(finals),
            "resultado": disposition,
            "estado_inicial": initial["resultado"],
            **axes,
            "severidad_inicial": initial["severidad"],
            "accion_inicial": initial["accion"],
            "accion_final": final_action,
            "evidencia_auditoria_inicial": initial["evidencia_auditoria"],
            "evidencia_final": final_evidence,
            "estado_hallazgo": (
                "HUECO_CIENTIFICO_ETIQUETADO"
                if any(claim_is_hole(row) for row in final_rows)
                else "CERRADO"
            ),
            "huella_inicial_sha256": row_fingerprint(initial),
            "huella_corpus_inicial_sha256": claim_fingerprint(baseline[claim_id]),
            "huella_final_sha256": final_hash,
        })

    for before, after in sorted(new_destinations, key=lambda item: natural_key(item[0])):
        row = current[after]
        covered[after] += 1
        axes = final_claim_axes([row])
        result.append({
            "clave_inicial": f"NUEVA:{before}",
            "seccion_inicial": "NO_APLICA",
            "claves_finales": after,
            "resultado": "NUEVA",
            "estado_inicial": "NO_APLICA",
            **axes,
            "severidad_inicial": "NINGUNA",
            "accion_inicial": "Alta documentada durante la remediación; no existía en las 1.840 C congeladas.",
            "accion_final": "ALTA DOCUMENTADA y renumerada una sola vez.",
            "evidencia_auditoria_inicial": f"Mapa temporal: {before} -> NUEVA.",
            "evidencia_final": (
                f"{after}; sección final {current_sections[after]}; huella del "
                "corpus fijada. El constructor no atribuye inspección adicional."
            ),
            "estado_hallazgo": (
                "HUECO_CIENTIFICO_ETIQUETADO" if claim_is_hole(row) else "CERRADO"
            ),
            "huella_inicial_sha256": "NO_APLICA",
            "huella_corpus_inicial_sha256": "NO_APLICA",
            "huella_final_sha256": claim_fingerprint(row),
        })
    if covered != Counter({claim_id: 1 for claim_id in current}):
        missing = sorted((Counter(current) - covered).elements(), key=natural_key)
        duplicates = sorted((covered - Counter(current)).elements(), key=natural_key)
        raise BuildError(
            f"Cobertura C final inválida; faltan={missing[:20]}; duplicadas={duplicates[:20]}"
        )
    return result


def compact_source_metadata(row: dict[str, str] | None) -> str:
    if row is None:
        return "NO_APLICA"
    return (
        f"autores={row['autores']}; año={row['año']}; título={row['título']}; "
        f"publicación={row['publicación o repositorio']}"
    )


def final_editorial_status(row: dict[str, str] | None) -> str:
    if row is None:
        return "FINAL: fuente retirada del catálogo; véase el registro explícito de retiradas."
    notes = row["notas de calidad"].strip()
    alert = re.compile(
        r"correcci|retract|errat|expression of concern|alerta editorial|"
        r"nota editorial",
        re.IGNORECASE,
    )
    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", notes)
        if alert.search(sentence)
    ]
    if sentences:
        return "FINAL EN A: " + " ".join(sentences)
    return (
        "FINAL EN A: sin corrección, retractación ni alerta editorial "
        "registrada al 2026-08-08; el constructor no sustituye la verificación "
        "editorial documentada."
    )


def build_source_matrix(
    frozen_rows: list[dict[str, str]], baseline_root: Path, root: Path,
    claims: Sequence[dict[str, str]], removed_sources_path: Path,
) -> list[dict[str, str]]:
    baseline = {row["clave"]: row for row in load_sources(baseline_root)}
    current = {row["clave"]: row for row in load_sources(root)}
    frozen = {row["clave_inicial"]: row for row in frozen_rows}
    if set(baseline) != set(frozen) or len(baseline) != 525:
        raise BuildError("A inicial y matriz S congelada no coinciden en 525 claves")

    removed: dict[str, dict[str, str]] = {}
    if removed_sources_path.exists():
        _, removed_rows = read_dicts(removed_sources_path)
        removed = {row["clave"]: row for row in removed_rows}
    expected_removed = set(baseline) - set(current)
    if set(removed) != expected_removed:
        raise BuildError(
            "El registro de fuentes retiradas no coincide con A inicial-final: "
            f"registro={sorted(removed)}; esperado={sorted(expected_removed)}"
        )

    cited_by: defaultdict[str, set[str]] = defaultdict(set)
    sole_support: defaultdict[str, set[str]] = defaultdict(set)
    for claim in claims:
        cited = set(expand_source_refs(claim["Fuente"]))
        for source in cited:
            cited_by[source].add(claim["#"])
        if len(cited) == 1:
            sole_support[next(iter(cited))].add(claim["#"])

    result: list[dict[str, str]] = []
    covered: Counter[str] = Counter()
    # Preserve the frozen audit order: the aggregate anchors both identity and
    # order, and the initial A catalogue intentionally contains late inserts.
    for source_id in (row["clave_inicial"] for row in frozen_rows):
        initial_a = baseline[source_id]
        initial = frozen[source_id]
        final = current.get(source_id)
        if final is None:
            verdict = "RETIRADA"
            final_id = "NO_APLICA"
            final_action = (
                f"RETIRADA: {removed[source_id]['motivo']} Destino: "
                f"{removed[source_id]['destino_documental']}"
            )
            final_evidence = (
                "Ausente de A final y presente una vez en el registro explícito "
                "de retiradas; no equivale a desestimación científica."
            )
            final_hash = "NO_APLICA"
            final_type = "NO_APLICA"
            final_doi = "NO_APLICA"
            final_metadata = "NO_APLICA"
            usage = "0 afirmaciones finales"
            unique = "NO"
        else:
            covered[source_id] += 1
            changed = source_fingerprint(initial_a) != source_fingerprint(final)
            verdict = (
                "CONFORME"
                if initial["veredicto"] == "CONFORME" and not changed
                else "CORREGIDA"
            )
            final_id = source_id
            final_action = (
                "METADATOS/NOTAS ACTUALIZADOS y uso final recalculado."
                if changed else
                "CONSERVADA; uso final recalculado sin alterar su identidad."
            )
            final_evidence = (
                f"{len(cited_by[source_id])} C finales citan la fuente; "
                f"{len(sole_support[source_id])} tienen esta S como única S. "
                "No se infiere inspección de texto completo desde este recuento."
            )
            final_hash = source_fingerprint(final)
            final_type = final["tipo"]
            final_doi = final[
                "DOI en forma https://doi.org/10.xxxx/... o URL resoluble si no hay DOI"
            ]
            final_metadata = compact_source_metadata(final)
            usage = f"{len(cited_by[source_id])} afirmaciones finales"
            unique = (
                f"SI: única S de {len(sole_support[source_id])} afirmaciones"
                if sole_support[source_id] else "NO"
            )
        result.append({
            "clave_inicial": source_id,
            "clave_final": final_id,
            "metadatos_iniciales": initial["metadata"],
            "metadatos_finales": final_metadata,
            "identidad_bibliografica": initial["identidad_bibliografica"],
            "tipo_inicial": initial["tipo"],
            "tipo_final": final_type,
            "estado_editorial": (
                f"INICIAL: {initial['estado_editorial']} | "
                f"{final_editorial_status(final)}"
            ),
            "acceso": initial["acceso"],
            "doi_url_inicial": initial["doi_url"],
            "doi_url_final": final_doi,
            "uso_inicial": initial["uso"],
            "uso_final": usage,
            "soporte_unico_inicial": initial["soporte_unico"],
            "soporte_unico_final": unique,
            "correcciones_retractaciones": final_editorial_status(final),
            "veredicto_inicial": initial["veredicto"],
            "veredicto": verdict,
            "severidad_inicial": initial["severidad"],
            "accion_inicial": initial["accion"],
            "accion_final": final_action,
            "evidencia_auditoria_inicial": initial["evidencia_auditoria"],
            "evidencia_final": final_evidence,
            "estado_hallazgo": (
                "HUECO_CIENTIFICO_ETIQUETADO"
                if final is not None and "NO VERIFICABLE" in initial["acceso"]
                else "CERRADO"
            ),
            "fecha_verificacion": initial["fecha_verificacion"],
            "huella_inicial_sha256": row_fingerprint(initial),
            "huella_corpus_inicial_sha256": source_fingerprint(initial_a),
            "huella_final_sha256": final_hash,
        })

    for source_id in sorted(set(current) - set(baseline), key=natural_key):
        final = current[source_id]
        covered[source_id] += 1
        usage = f"{len(cited_by[source_id])} afirmaciones finales"
        unique = (
            f"SI: única S de {len(sole_support[source_id])} afirmaciones"
            if sole_support[source_id] else "NO"
        )
        result.append({
            "clave_inicial": f"NUEVA:{source_id}",
            "clave_final": source_id,
            "metadatos_iniciales": "NO_APLICA",
            "metadatos_finales": compact_source_metadata(final),
            "identidad_bibliografica": "Alta documentada después del corte inicial de 525 fuentes.",
            "tipo_inicial": "NO_APLICA",
            "tipo_final": final["tipo"],
            "estado_editorial": final_editorial_status(final),
            "acceso": "Identificador registrado en A; el constructor no realiza una nueva descarga.",
            "doi_url_inicial": "NO_APLICA",
            "doi_url_final": final[
                "DOI en forma https://doi.org/10.xxxx/... o URL resoluble si no hay DOI"
            ],
            "uso_inicial": "NO_APLICA",
            "uso_final": usage,
            "soporte_unico_inicial": "NO_APLICA",
            "soporte_unico_final": unique,
            "correcciones_retractaciones": final_editorial_status(final),
            "veredicto_inicial": "NO_APLICA",
            "veredicto": "NUEVA",
            "severidad_inicial": "NINGUNA",
            "accion_inicial": "Alta bibliográfica posterior a la congelación.",
            "accion_final": "ALTA DOCUMENTADA con identidad, tipo, DOI/URL y uso final.",
            "evidencia_auditoria_inicial": "No formaba parte de las 525 S iniciales.",
            "evidencia_final": (
                f"Registro A final y Q de actualización; {usage}. El constructor "
                "no atribuye una verificación editorial nueva."
            ),
            "estado_hallazgo": "CERRADO",
            "fecha_verificacion": CUTOFF,
            "huella_inicial_sha256": "NO_APLICA",
            "huella_corpus_inicial_sha256": "NO_APLICA",
            "huella_final_sha256": source_fingerprint(final),
        })
    if covered != Counter({source_id: 1 for source_id in current}):
        raise BuildError("La matriz S no cubre cada fuente final exactamente una vez")
    return result


def normalize_markdown(value: str) -> str:
    value = re.sub(r"[`*_#>]", "", value)
    value = re.sub(r"(?m)^\s*[-+]\s+", "", value)
    return re.sub(r"\s+", " ", value).strip()


def requirement_anchor(literal: str, prompt_lines: Sequence[str]) -> str:
    needle = normalize_markdown(literal)
    candidates: list[tuple[int, int, int]] = []
    for start in range(len(prompt_lines)):
        # Los requisitos congelados son oraciones/celdas; 40 líneas deja
        # margen para listas partidas sin permitir anclas de sección enteras.
        for end in range(start, min(len(prompt_lines), start + 40)):
            window = normalize_markdown("\n".join(prompt_lines[start:end + 1]))
            if needle in window:
                candidates.append((end - start + 1, start + 1, end + 1))
                break
            if len(window) > len(needle) * 4 + 500:
                break
    if not candidates:
        raise BuildError(f"No se localizó literalmente requisito: {literal[:160]}")
    _, start, end = min(candidates)
    return f"L{start}" if start == end else f"L{start}-L{end}"


def canonical_source(number: int) -> str:
    return f"S{number:02d}"


def supplementary_source_context(value: str, start: int) -> bool:
    prefix = value[max(0, start - 48):start].casefold()
    return bool(re.search(
        r"(?:\bfig(?:s|ures?|uras?)?\.?|\btable|\btabla|"
        r"\bsuppl(?:ementary)?\.?(?:\s+data)?|\bsupplementary(?:\s+data)?|"
        r"\bvideo)\s*$",
        prefix,
    ))


def expand_source_refs(value: str) -> list[str]:
    refs: list[str] = []
    occupied: list[tuple[int, int]] = []
    for match in SOURCE_RANGE.finditer(value):
        start, end = map(int, match.groups())
        if start > end:
            raise BuildError(f"Rango S descendente: {match.group(0)}")
        occupied.append(match.span())
        if supplementary_source_context(value, match.start()):
            continue
        refs.extend(canonical_source(number) for number in range(start, end + 1))
    for match in SOURCE_REF.finditer(value):
        if (
            not any(start <= match.start() < end for start, end in occupied)
            and not supplementary_source_context(value, match.start())
        ):
            refs.append(match.group(0))
    return list(dict.fromkeys(refs))


def exact_manifest_refs(
    value: str, pattern: re.Pattern[str], label: str, requirement_id: str,
) -> list[str]:
    if value == "n/a":
        return []
    refs = value.split("; ")
    if any(not pattern.fullmatch(ref) for ref in refs):
        raise BuildError(
            f"{requirement_id}: {label} debe enumerar claves exactas separadas "
            f"por '; ' (sin rangos): {value}"
        )
    canonical = sorted(set(refs), key=natural_key)
    if refs != canonical:
        raise BuildError(
            f"{requirement_id}: {label} contiene duplicados o no está en orden canónico"
        )
    return refs


def claim_source_closure(
    claim_ids: Sequence[str], current: dict[str, dict[str, str]],
) -> list[str]:
    sources: set[str] = set()
    pending = list(claim_ids)
    visited: set[str] = set()
    while pending:
        claim_id = pending.pop()
        if claim_id in visited:
            continue
        if claim_id not in current:
            raise BuildError(f"Dependencia C inexistente en manifiesto R: {claim_id}")
        visited.add(claim_id)
        source_field = current[claim_id]["Fuente"]
        sources.update(expand_source_refs(source_field))
        pending.extend(
            dependency for dependency in expand_claim_refs(source_field)
            if dependency not in visited
        )
    return sorted(sources, key=natural_key)


def claim_search_closure(
    claim_ids: Sequence[str], current: dict[str, dict[str, str]],
) -> list[str]:
    searches: set[str] = set()
    pending = list(claim_ids)
    visited: set[str] = set()
    while pending:
        claim_id = pending.pop()
        if claim_id in visited:
            continue
        if claim_id not in current:
            raise BuildError(f"Dependencia C inexistente en manifiesto R: {claim_id}")
        visited.add(claim_id)
        source_field = current[claim_id]["Fuente"]
        searches.update(SEARCH_REF.findall(source_field))
        pending.extend(
            dependency for dependency in expand_claim_refs(source_field)
            if dependency not in visited
        )
    return sorted(searches, key=natural_key)


def load_requirement_dispositions(
    root: Path, frozen_rows: Sequence[dict[str, str]], active_bn: set[str],
) -> list[dict[str, object]]:
    path = root / "data/auditoria/requisitos_disposiciones.csv"
    header, rows = read_dicts(path)
    if header != REQUIREMENT_DISPOSITION_COLUMNS:
        raise BuildError(
            f"Cabecera incompatible en manifiesto R: {header}; se esperaba "
            f"{REQUIREMENT_DISPOSITION_COLUMNS}"
        )
    expected_ids = [f"R-{number:04d}" for number in range(1, 484)]
    ids = [row["id_requisito"] for row in rows]
    if len(rows) != 483 or ids != expected_ids:
        missing = sorted(set(expected_ids) - set(ids), key=natural_key)
        duplicates = sorted(
            (key for key, count in Counter(ids).items() if count > 1),
            key=natural_key,
        )
        raise BuildError(
            "El manifiesto R debe contener exactamente R-0001…R-0483 en orden; "
            f"filas={len(rows)}, faltan={missing[:10]}, duplicadas={duplicates[:10]}"
        )
    if len(frozen_rows) != 483:
        raise BuildError(f"Inventario congelado R inesperado: {len(frozen_rows)}")

    current_rows, _ = load_claims(root)
    current = {row["#"]: row for row in current_rows}
    valid_sources = {row["clave"] for row in load_sources(root)}
    valid_tables = {entry["id"] for entry in load_index(root)["tables"]}
    valid_ids = set(expected_ids)
    valid_searches = {
        f"Q-{number:04d}"
        for number in range(1, FROZEN_SEARCH_COUNT + len(ADDITIONAL_SEARCHES) + 1)
    }
    active_search_holes = {
        f"Q-{FROZEN_SEARCH_COUNT + offset:04d}"
        for offset, search in enumerate(ADDITIONAL_SEARCHES, 1)
        if search["estado_registro"] == "HUECO_CIENTIFICO_ETIQUETADO"
    }
    allowed_types = {"CIENTIFICO", "CONTROL_ESTRUCTURAL", "PADRE"}
    allowed_states = {
        "CUBIERTO", "HUECO_ACTIVO", "PENDIENTE_HUECO_SIN_BUSQUEDA",
        "CONTROL_DEFINIDO", "CONTROL_VERIFICADO", "ROLLUP",
    }
    parsed: list[dict[str, object]] = []
    children_by_parent: dict[str, list[str]] = {}
    for row in rows:
        requirement_id = row["id_requisito"]
        empty = [column for column in header if not row[column].strip()]
        if empty:
            raise BuildError(f"{requirement_id}: celdas vacías en {empty}")
        kind = row["tipo"]
        state = row["estado_disposicion"]
        if kind not in allowed_types:
            raise BuildError(f"{requirement_id}: tipo inválido {kind}")
        if state not in allowed_states:
            raise BuildError(f"{requirement_id}: estado de disposición inválido {state}")

        claims = exact_manifest_refs(
            row["afirmaciones_exactas"], CLAIM_REF,
            "afirmaciones_exactas", requirement_id,
        )
        tables = exact_manifest_refs(
            row["tablas_exactas"], TABLE_REF,
            "tablas_exactas", requirement_id,
        )
        sources = exact_manifest_refs(
            row["fuentes_exactas"], SOURCE_REF,
            "fuentes_exactas", requirement_id,
        )
        negative = exact_manifest_refs(
            row["busquedas_negativas_exactas"], BN_REF,
            "busquedas_negativas_exactas", requirement_id,
        )
        searches = exact_manifest_refs(
            row["busquedas_ejecutadas_exactas"], SEARCH_REF,
            "busquedas_ejecutadas_exactas", requirement_id,
        )
        unknown_claims = sorted(set(claims) - set(current), key=natural_key)
        unknown_tables = sorted(set(tables) - valid_tables, key=natural_key)
        unknown_sources = sorted(set(sources) - valid_sources, key=natural_key)
        unknown_negative = sorted(set(negative) - active_bn, key=natural_key)
        unknown_searches = sorted(set(searches) - valid_searches, key=natural_key)
        if (
            unknown_claims or unknown_tables or unknown_sources
            or unknown_negative or unknown_searches
        ):
            raise BuildError(
                f"{requirement_id}: destinos inexistentes; C={unknown_claims}, "
                f"tablas={unknown_tables}, S={unknown_sources}, BN={unknown_negative}, "
                f"Q={unknown_searches}"
            )
        derived_sources = claim_source_closure(claims, current)
        if sources != derived_sources:
            raise BuildError(
                f"{requirement_id}: fuentes_exactas no coincide con el cierre de sus C; "
                f"declaradas={sources}, esperadas={derived_sources}"
            )
        derived_searches = claim_search_closure(claims, current)
        if searches != derived_searches:
            raise BuildError(
                f"{requirement_id}: búsquedas ejecutadas no coinciden con el cierre "
                f"de sus C; declaradas={searches}, esperadas={derived_searches}"
            )

        control = row["control_o_rollup"]
        control_proof = {
            column: row[column] for column in (
                "artefacto_control", "alcance_o_censo", "comando_o_consulta",
                "resultado_control", "huella_control_sha256",
            )
        }
        if kind == "PADRE":
            if state != "ROLLUP":
                raise BuildError(f"{requirement_id}: PADRE debe usar estado ROLLUP")
            if any((claims, tables, sources, negative, searches)):
                raise BuildError(f"{requirement_id}: PADRE no puede heredar destinos científicos")
            if set(control_proof.values()) != {"n/a"}:
                raise BuildError(f"{requirement_id}: PADRE no puede heredar prueba de control")
            children = exact_manifest_refs(
                control, REQUIREMENT_REF, "control_o_rollup", requirement_id,
            )
            if not children or requirement_id in children:
                raise BuildError(f"{requirement_id}: roll-up vacío o autorreferente")
            if set(children) - valid_ids:
                raise BuildError(f"{requirement_id}: roll-up con hijos inexistentes")
            children_by_parent[requirement_id] = children
        elif kind == "CONTROL_ESTRUCTURAL":
            if state not in {"CONTROL_DEFINIDO", "CONTROL_VERIFICADO"}:
                raise BuildError(f"{requirement_id}: estado incompatible con control")
            if not re.fullmatch(r"CONTROL::R-\d{4}::[A-Z0-9_]+", control):
                raise BuildError(f"{requirement_id}: identificador de control inválido: {control}")
            expected_artifact = (
                f"docs/auditorias/controles_requisitos/{requirement_id}.csv"
            )
            if row["artefacto_control"] != expected_artifact:
                raise BuildError(
                    f"{requirement_id}: artefacto nominal debe ser {expected_artifact}"
                )
            if state == "CONTROL_DEFINIDO":
                pending_fields = {
                    row["alcance_o_censo"], row["comando_o_consulta"],
                    row["resultado_control"], row["huella_control_sha256"],
                }
                if pending_fields != {"PENDIENTE"}:
                    raise BuildError(
                        f"{requirement_id}: CONTROL_DEFINIDO debe conservar prueba PENDIENTE"
                    )
            else:
                if any(
                    value in {"", "n/a", "PENDIENTE"}
                    for column, value in control_proof.items()
                    if column != "artefacto_control"
                ):
                    raise BuildError(
                        f"{requirement_id}: CONTROL_VERIFICADO sin prueba completa"
                    )
                if row["resultado_control"] != "CERO_FALLOS":
                    raise BuildError(
                        f"{requirement_id}: solo CERO_FALLOS permite verificar un control"
                    )
                if not re.fullmatch(r"[0-9a-f]{64}", row["huella_control_sha256"]):
                    raise BuildError(f"{requirement_id}: huella de control inválida")
                artifact_path = root / row["artefacto_control"]
                artifact_header, artifact_rows = read_dicts(artifact_path)
                if artifact_header != REQUIREMENT_CONTROL_ARTIFACT_COLUMNS:
                    raise BuildError(
                        f"{requirement_id}: cabecera inválida en artefacto de control"
                    )
                if len(artifact_rows) != 1:
                    raise BuildError(
                        f"{requirement_id}: artefacto debe contener exactamente una fila"
                    )
                artifact = artifact_rows[0]
                expected_artifact_values = {
                    "id_requisito": requirement_id,
                    "alcance_o_censo": row["alcance_o_censo"],
                    "comando_o_consulta": row["comando_o_consulta"],
                    "resultado_control": row["resultado_control"],
                }
                if any(
                    artifact[column] != value
                    for column, value in expected_artifact_values.items()
                ) or artifact["evidencia"].strip() in {"", "n/a", "PENDIENTE"}:
                    raise BuildError(
                        f"{requirement_id}: artefacto no reproduce manifiesto/evidencia"
                    )
                if sha256_file(artifact_path) != row["huella_control_sha256"]:
                    raise BuildError(f"{requirement_id}: huella de artefacto no coincide")
        else:
            if state not in {
                "CUBIERTO", "HUECO_ACTIVO", "PENDIENTE_HUECO_SIN_BUSQUEDA",
            }:
                raise BuildError(f"{requirement_id}: estado incompatible con requisito científico")
            if set(control_proof.values()) != {"n/a"}:
                raise BuildError(
                    f"{requirement_id}: requisito científico no puede fingir prueba de control"
                )
            if state == "CUBIERTO":
                if not claims and not tables:
                    raise BuildError(f"{requirement_id}: CUBIERTO sin destino científico")
                if negative or searches or control != "n/a":
                    raise BuildError(f"{requirement_id}: CUBIERTO no puede declarar hueco/control")
            elif state == "HUECO_ACTIVO":
                if (not negative and not searches) or control != "n/a":
                    raise BuildError(
                        f"{requirement_id}: hueco científico sin BN activa o Q ejecutada exacta"
                    )
                if set(searches) - active_search_holes:
                    raise BuildError(
                        f"{requirement_id}: Q citada no conserva un hueco científico activo"
                    )
            else:
                if negative or searches or not re.fullmatch(
                    r"HUECO_PENDIENTE::R-\d{4}::[A-Z0-9_]+", control
                ):
                    raise BuildError(
                        f"{requirement_id}: pendiente debe declarar un hueco nominal "
                        "y no puede fingir una BN activa"
                    )
        if row["accion"] in {"", "n/a"}:
            raise BuildError(f"{requirement_id}: acción no documentada")
        parsed_row: dict[str, object] = dict(row)
        parsed_row.update({
            "_claims": claims, "_tables": tables, "_sources": sources,
            "_negative": negative, "_searches": searches,
            "_children": children_by_parent.get(requirement_id, []),
        })
        parsed.append(parsed_row)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(requirement_id: str) -> None:
        if requirement_id in visiting:
            raise BuildError(f"Ciclo en roll-ups R: {requirement_id}")
        if requirement_id in visited:
            return
        visiting.add(requirement_id)
        for child in children_by_parent.get(requirement_id, []):
            visit(child)
        visiting.remove(requirement_id)
        visited.add(requirement_id)

    for requirement_id in expected_ids:
        visit(requirement_id)
    return parsed


def explicit_refs(refs: Sequence[str]) -> str:
    return "; ".join(refs) if refs else "n/a"


def build_requirement_matrix(
    frozen_rows: list[dict[str, str]], root: Path, active_bn: set[str],
) -> list[dict[str, str]]:
    prompt_lines = (root / PROMPT_RELATIVE).read_text(encoding="utf-8").splitlines()
    dispositions = load_requirement_dispositions(root, frozen_rows, active_bn)
    by_id = {str(row["id_requisito"]): row for row in dispositions}
    state_cache: dict[str, str] = {}

    def final_state(requirement_id: str) -> str:
        if requirement_id in state_cache:
            return state_cache[requirement_id]
        disposition = by_id[requirement_id]
        state = str(disposition["estado_disposicion"])
        if state == "CUBIERTO":
            result = "CUMPLE"
        elif state == "HUECO_ACTIVO":
            result = "CUMPLE_MEDIANTE_HUECO_ETIQUETADO"
        elif state == "CONTROL_VERIFICADO":
            result = (
                "CUMPLE_MEDIANTE_HUECO_ETIQUETADO"
                if disposition["_negative"] or disposition["_searches"]
                else "CUMPLE"
            )
        elif state in {"PENDIENTE_HUECO_SIN_BUSQUEDA", "CONTROL_DEFINIDO"}:
            result = "NO_CONFORME"
        else:
            child_states = [final_state(str(child)) for child in disposition["_children"]]
            if "NO_CONFORME" in child_states:
                result = "NO_CONFORME"
            elif "CUMPLE_MEDIANTE_HUECO_ETIQUETADO" in child_states:
                result = "CUMPLE_MEDIANTE_HUECO_ETIQUETADO"
            else:
                result = "CUMPLE"
        state_cache[requirement_id] = result
        return result

    result: list[dict[str, str]] = []
    for number, (initial, disposition) in enumerate(
        zip(frozen_rows, dispositions, strict=True), 1,
    ):
        requirement_id = f"R-{number:04d}"
        claims = explicit_refs(disposition["_claims"])
        tables = explicit_refs(disposition["_tables"])
        sources = explicit_refs(disposition["_sources"])
        negative = explicit_refs(disposition["_negative"])
        searches = explicit_refs(disposition["_searches"])
        gap_destinations = explicit_refs([
            *disposition["_negative"], *disposition["_searches"],
        ])
        kind = str(disposition["tipo"])
        if kind == "PADRE":
            child_states = "; ".join(
                f"{child}={final_state(str(child))}"
                for child in disposition["_children"]
            )
            mapping_evidence = (
                f"roll-up explícito {disposition['control_o_rollup']}; "
                f"estados de hijos: {child_states}"
            )
        elif kind == "CONTROL_ESTRUCTURAL":
            destinations = "; ".join(
                value for value in (claims, tables, sources, negative, searches)
                if value != "n/a"
            )
            suffix = f"; destinos auditados: {destinations}" if destinations else ""
            mapping_evidence = (
                f"control {disposition['estado_disposicion']} "
                f"{disposition['control_o_rollup']}; artefacto="
                f"{disposition['artefacto_control']}; alcance="
                f"{disposition['alcance_o_censo']}; comando/consulta="
                f"{disposition['comando_o_consulta']}; resultado="
                f"{disposition['resultado_control']}; huella="
                f"{disposition['huella_control_sha256']}{suffix}"
            )
        else:
            mapping_evidence = (
                f"disposición científica curada uno por uno: C={claims}; "
                f"tablas={tables}; S={sources}; BN={negative}; Q={searches}; "
                f"estado={disposition['estado_disposicion']}"
            )
        anchor = requirement_anchor(initial["requisito_literal"], prompt_lines)
        result.append({
            "id_requisito": requirement_id,
            "seccion_prompt": initial["seccion_prompt"],
            "ancla": anchor,
            "requisito_literal": initial["requisito_literal"],
            "estado_inicial": initial["estado_inicial"],
            "estado_final": final_state(requirement_id),
            "afirmaciones_iniciales": initial["afirmaciones"],
            "afirmaciones": claims,
            "tablas_iniciales": initial["tablas"],
            "tablas": tables,
            "fuentes_iniciales": initial["fuentes"],
            "fuentes": sources,
            "busqueda_negativa_inicial": initial["busqueda_negativa"],
            "busqueda_negativa": gap_destinations,
            "accion_inicial": initial["accion"],
            "accion": str(disposition["accion"]),
            "evidencia_inicial": initial["evidencia"],
            "evidencia": f"Ancla literal {anchor}; {mapping_evidence}.",
            "huella_inicial_sha256": row_fingerprint(initial),
        })
    return result


def load_negative_rows(root: Path) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for entry in load_index(root)["tables"]:
        if entry["category"] != "negative":
            continue
        _, rows = read_dicts(root / entry["csv_path"])
        for row in rows:
            key = row["clave"]
            if key in result:
                raise BuildError(f"BN activa duplicada: {key}")
            result[key] = row
    return result


def bn_priority(key: str, active_bn: set[str]) -> str:
    if key not in active_bn:
        return "RETIRADA"
    if key in P0_BN:
        return "P0"
    if key in P1_BN:
        return "P1"
    if key in P2_BN:
        return "P2"
    raise BuildError(f"BN activa sin prioridad: {key}")


def bn_trigger(priority: str) -> str:
    return {
        "P0": "Nueva evidencia primaria que pueda resolver o reformular el blanco literal.",
        "P1": "Nuevo protocolo o dataset comparable, o una síntesis causal pertinente.",
        "P2": "Fuente posterior al corte que satisfaga el blanco literal; vigilancia condicionada sin búsqueda intensiva en ausencia del desencadenante.",
        "RETIRADA": "Solo reabrir si cambia la disposición histórica o aparece evidencia que invalida el cierre documentado.",
    }[priority]


def negative_delta(
    key: str, baseline_bn: dict[str, dict[str, str]],
    current_bn: dict[str, dict[str, str]],
) -> str:
    before = baseline_bn.get(key)
    after = current_bn.get(key)
    if before is None and after is None:
        return "SIN_FILA_CANONICA_EN_AMBOS_CORTES"
    if before is None:
        return f"ALTA_CANONICA; final_sha256={row_fingerprint(after)}"
    if after is None:
        return f"RETIRADA_CANONICA; inicial_sha256={row_fingerprint(before)}"
    if before == after:
        return "SIN_CAMBIO_CANONICO"
    changed = sorted(
        column for column in set(before) | set(after)
        if before.get(column, "") != after.get(column, "")
    )
    return (
        f"CAMBIO_CANONICO_DOCUMENTADO; campos={'; '.join(changed)}; "
        f"inicial_sha256={row_fingerprint(before)}; "
        f"final_sha256={row_fingerprint(after)}"
    )


def build_negative_history(
    snapshot: Path, baseline_bn: dict[str, dict[str, str]],
    current_bn: dict[str, dict[str, str]],
) -> tuple[list[dict[str, str]], list[str]]:
    path = snapshot / "worktree/docs/auditorias/revision_busquedas_negativas_2026-08-08.csv"
    initial_rows = read_dicts(path)[1]
    active = set(current_bn)
    if len(initial_rows) != 106 or len(active) != 68:
        raise BuildError("Historia BN debe conservar 106 filas y 68 activas")
    if Counter(bn_priority(key, active) for key in active) != Counter(
        {"P0": 22, "P1": 23, "P2": 23}
    ):
        raise BuildError("Prioridades BN activas distintas de 22/23/23")

    result: list[dict[str, str]] = []
    explicit_deltas: list[str] = []
    for initial in initial_rows:
        key = initial["clave_original"]
        row = dict(initial)
        changed_history: list[str] = []
        if key in HISTORY_RESULT_OVERRIDES:
            previous = row["resultado_documentado"]
            row["resultado_documentado"] = HISTORY_RESULT_OVERRIDES[key]
            changed_history.append(
                "resultado_documentado corregido; "
                f"valor_inicial_sha256={sha256_bytes((previous + chr(10)).encode('utf-8'))}; "
                "se retiró un valor central no publicado o un complemento "
                "aritmético y se conservaron solo magnitudes publicadas"
            )
        if key in HISTORY_EVIDENCE_OVERRIDES:
            previous = row["evidencia_principal"]
            row["evidencia_principal"] = HISTORY_EVIDENCE_OVERRIDES[key]
            changed_history.append(
                "evidencia_principal corregida; "
                f"valor_inicial_sha256={sha256_bytes((previous + chr(10)).encode('utf-8'))}; "
                "se acotó la evidencia a la magnitud o clase de medición publicada"
            )
        priority = bn_priority(key, active)
        canonical = negative_delta(key, baseline_bn, current_bn)
        history_delta = (
            "CORRECCION_EXPLICITA: " + " | ".join(changed_history)
            if changed_history else "SIN_CAMBIO_EN_LA_FILA_HISTORICA"
        )
        delta = f"{history_delta}; {canonical}"
        if changed_history or canonical != "SIN_CAMBIO_CANONICO":
            explicit_deltas.append(f"- **{key}:** {delta}")
        row.update({
            "prioridad_final": priority,
            "desencadenante": bn_trigger(priority),
            "delta_auditoria_2026_08_08": delta,
            "huella_inicial_sha256": row_fingerprint(initial),
        })
        result.append(row)
    return result, explicit_deltas


def history_markdown(snapshot: Path, delta_lines: Sequence[str]) -> bytes:
    path = snapshot / "worktree/docs/auditorias/REVISION-BUSQUEDAS-NEGATIVAS-2026-08-08.md"
    text = path.read_text(encoding="utf-8")
    cleaned_lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("- Se recuperaron ocho edades nodales reproducibles de Liu et al. 2024"):
            line = (
                "- Se conservaron ocho intervalos nodales publicados de Liu et al. "
                "2024, con nodo de la tabla suplementaria y modelo de raíz; se "
                "omitieron los valores centrales no publicados."
            )
        elif line.startswith("- Se verificó un presupuesto integrado de *Trypanosoma brucei*"):
            line = (
                "- Se verificó un presupuesto integrado de *Trypanosoma brucei* "
                "de 6,0 × 10^11 ATP por célula y ciclo y un residual publicado "
                "de aproximadamente 5,5 %; no se lo presentó como presupuesto de "
                "FECA, LECA o de todos los rasgos del corredor."
            )
        cleaned_lines.append(line)
    text = "\n".join(cleaned_lines) + "\n"
    marker = "\n## Delta de auditoría 2026-08-08\n"
    if marker in text:
        text = text.split(marker, 1)[0].rstrip() + "\n"
    text += marker
    text += (
        "\nLos cambios siguientes se registran contra la instantánea externa; "
        "`NO_VERIFICABLE` o un resultado negativo no se reinterpretan como "
        "falsedad. Las huellas completas están en el CSV enriquecido.\n\n"
    )
    text += "\n".join(delta_lines) if delta_lines else "- Sin cambios respecto del corte congelado."
    return (text.rstrip() + "\n").encode("utf-8")


def build_search_matrix(
    frozen_rows: list[dict[str, str]], active_bn: set[str],
    history: dict[str, dict[str, str]], baseline_bn: dict[str, dict[str, str]],
    current_bn: dict[str, dict[str, str]], key_map: dict[str, str],
) -> list[dict[str, str]]:
    if len(frozen_rows) != FROZEN_SEARCH_COUNT:
        raise BuildError(
            f"Inventario Q congelado inesperado: {len(frozen_rows)}; "
            f"se esperaban {FROZEN_SEARCH_COUNT}"
        )
    result: list[dict[str, str]] = []
    for number, initial in enumerate(frozen_rows, 1):
        key_match = BN_REF.search(initial["bloque"])
        key = key_match.group(0) if key_match else "n/a"
        if key != "n/a":
            priority = bn_priority(key, active_bn)
            trigger = history[key]["desencadenante"]
            delta = history[key]["delta_auditoria_2026_08_08"]
            state = (
                "HUECO_CIENTIFICO_ETIQUETADO"
                if key in active_bn else "CERRADO"
            )
            change = delta
            evidence = (
                f"Fila congelada {row_fingerprint(initial)}; historia BN y fila "
                "canónica comparadas por huella."
            )
        else:
            block = initial["bloque"].casefold()
            if "semilla obligatoria" in block:
                priority = "NO_APLICA"
                change = "Semilla evaluada e integrada bibliográficamente según el resultado congelado."
            elif "actualización sección" in block:
                priority = "NO_APLICA"
                change = "Cribado de actualización conservado; las altas/correcciones se documentan en C/S y sus matrices."
            else:
                priority = "NO_APLICA"
                change = "Resolución bibliográfica conservada y contrastable con A final."
            trigger = "NO_APLICA: búsqueda ejecutada en el corte de auditoría."
            state = "CERRADO"
            evidence = (
                f"Fila congelada {row_fingerprint(initial)}; no se atribuye una "
                "consulta adicional a la registrada."
            )
        result.append({
            "id_busqueda": f"Q-{number:04d}",
            "fecha": initial["fecha"],
            "bloque": initial["bloque"],
            "clave_bn": key,
            "prioridad": priority,
            "objetivo": initial["objetivo"],
            "consulta_exacta": initial["consulta_exacta"],
            "servicio": initial["servicio"],
            "fuentes_evaluadas": initial["fuentes_evaluadas"],
            "resultado": initial["resultado"],
            "accion_inicial": initial["accion"],
            "cambio_realizado": change,
            "desencadenante": trigger,
            "evidencia_final": evidence,
            "estado_registro": state,
            "huella_inicial_sha256": row_fingerprint(initial),
        })
    for offset, row in enumerate(ADDITIONAL_SEARCHES, len(result) + 1):
        mapped = {
            column: CLAIM_REF.sub(
                lambda match: key_map.get(match.group(0), match.group(0)), value
            )
            for column, value in row.items()
        }
        result.append({"id_busqueda": f"Q-{offset:04d}", **mapped})
    return result


def appendix_paths(root: Path) -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for letter in "BCDEFG":
        matches = sorted((root / "data/apendices").glob(f"{letter}_*.csv"))
        if len(matches) != 1:
            raise BuildError(f"Se esperaba un apéndice {letter}, hallados {matches}")
        paths[letter] = matches[0]
    return paths


def strip_claims(value: str) -> str:
    return re.sub(r"\s+", " ", CLAIM_REF.sub("C", value)).strip().casefold()


def appendix_identity(letter: str, row: dict[str, str]) -> str:
    if letter == "B":
        return row["etiqueta preferida"].strip().casefold()
    if letter in {"C", "E"}:
        return row["clave"]
    if letter == "D":
        return "\x1f".join((
            row["a qué se aplica"].strip().casefold(),
            row["tipo"].strip().casefold(),
            strip_claims(row["fuente con localizador"]),
        ))
    if letter == "F":
        return "\x1f".join((
            row["magnitud"].strip().casefold(),
            row["organismo, nodo o intervalo al que se aplica"].strip().casefold(),
            strip_claims(row["fuente con localizador"]),
        ))
    return row["material"].strip().casefold()


def appendix_human_id(letter: str, row: dict[str, str]) -> str:
    field = {
        "B": "etiqueta preferida", "C": "clave", "D": "a qué se aplica",
        "E": "clave", "F": "magnitud", "G": "material",
    }[letter]
    return row[field]


def build_appendix_delta(
    baseline_root: Path, root: Path,
) -> tuple[list[dict[str, str]], dict[str, Counter[str]]]:
    initial_paths = appendix_paths(baseline_root)
    final_paths = appendix_paths(root)
    result: list[dict[str, str]] = []
    counts: dict[str, Counter[str]] = {}
    serial = 0
    for letter in "BCDEFG":
        initial_rows = read_dicts(initial_paths[letter])[1]
        final_rows = read_dicts(final_paths[letter])[1]
        queues: defaultdict[str, deque[int]] = defaultdict(deque)
        for index, row in enumerate(final_rows):
            queues[appendix_identity(letter, row)].append(index)
        used_final: set[int] = set()
        per_appendix: Counter[str] = Counter()
        for initial_index, initial in enumerate(initial_rows):
            serial += 1
            identity = appendix_identity(letter, initial)
            # Las 107 filas D sin C eran metadatos editoriales/fechas internas,
            # no observaciones o estimaciones científicas. Se retiran aunque
            # algún texto coincida accidentalmente con una fila científica.
            forced_retirement = (
                letter == "D"
                and not CLAIM_REF.search(initial["# de la fila que la sostiene"])
            )
            final_index = None
            if not forced_retirement and queues[identity]:
                final_index = queues[identity].popleft()
                used_final.add(final_index)
            if final_index is None:
                action = "RETIRADA"
                if forced_retirement:
                    destination = (
                        "Instantánea externa; era metadato de publicación o fecha "
                        "interna de corte sin C, no una estimación científica."
                    )
                else:
                    destination = (
                        "Instantánea externa y linaje de auditoría; retirada o "
                        "consolidada sin reasignar silenciosamente la fila."
                    )
                final = None
            else:
                final = final_rows[final_index]
                if initial == final:
                    action = "SIN_CAMBIO"
                    destination = "Misma fila final, identidad y contenido conservados."
                else:
                    action = "ACTUALIZADA"
                    destination = (
                        "Fila final emparejada por identidad de dominio; cambios "
                        "fijados por huellas inicial/final."
                    )
            per_appendix[action] += 1
            result.append({
                "id_delta": f"DA-{serial:05d}",
                "apendice": letter,
                "fila_inicial": str(initial_index + 2),
                "fila_final": str(final_index + 2) if final_index is not None else "NO_APLICA",
                "identificador_inicial": appendix_human_id(letter, initial),
                "identificador_final": appendix_human_id(letter, final) if final else "NO_APLICA",
                "estado_inicial": "PRESENTE",
                "estado_final": "RETIRADA" if final is None else "PRESENTE",
                "accion": action,
                "destino": destination,
                "huella_inicial_sha256": row_fingerprint(initial),
                "huella_final_sha256": row_fingerprint(final) if final else "NO_APLICA",
            })
        for final_index, final in enumerate(final_rows):
            if final_index in used_final:
                continue
            serial += 1
            per_appendix["ALTA"] += 1
            result.append({
                "id_delta": f"DA-{serial:05d}",
                "apendice": letter,
                "fila_inicial": "NO_APLICA",
                "fila_final": str(final_index + 2),
                "identificador_inicial": "NO_APLICA",
                "identificador_final": appendix_human_id(letter, final),
                "estado_inicial": "AUSENTE",
                "estado_final": "PRESENTE",
                "accion": "ALTA",
                "destino": "Fila nueva del apéndice final; huella final fijada.",
                "huella_inicial_sha256": "NO_APLICA",
                "huella_final_sha256": row_fingerprint(final),
            })
        counts[letter] = per_appendix

    initial_d = read_dicts(initial_paths["D"])[1]
    final_d = read_dicts(final_paths["D"])[1]
    initial_d_without_c = sum(
        not CLAIM_REF.search(row["# de la fila que la sostiene"])
        for row in initial_d
    )
    final_d_without_c = sum(
        not CLAIM_REF.search(row["# de la fila que la sostiene"])
        for row in final_d
    )
    if (
        len(initial_d), initial_d_without_c, len(final_d), final_d_without_c,
    ) != (282, 107, 215, 0):
        raise BuildError(
            "Delta D inesperado; se esperaba 282/107 sin C -> 215/0 sin C, "
            f"obtenido {len(initial_d)}/{initial_d_without_c} -> "
            f"{len(final_d)}/{final_d_without_c}"
        )
    forced_d = sum(
        row["apendice"] == "D"
        and row["accion"] == "RETIRADA"
        and "no una estimación científica" in row["destino"]
        for row in result
    )
    if forced_d != 107:
        raise BuildError(f"El delta no individualiza las 107 retiradas D: {forced_d}")
    return result, counts


def deterministic_sample(
    stratum: str, rows: Sequence[dict[str, str]], key_field: str,
) -> list[dict[str, str]]:
    size = math.ceil(len(rows) * 0.15)
    return sorted(
        rows,
        key=lambda row: hashlib.sha256(
            f"{AUDIT_ID}\x1f{stratum}\x1f{row[key_field]}".encode("utf-8")
        ).hexdigest(),
    )[:size]


def valid_review_date(value: str) -> bool:
    try:
        parsed = date.fromisoformat(value)
        cutoff = date.fromisoformat(CUTOFF)
    except ValueError:
        return False
    return parsed <= cutoff


def valid_review_identity(row: dict[str, str]) -> bool:
    return (
        row.get("revisor_independiente") not in {"", "NO_ASIGNADO", "n/a"}
        and row.get("declaracion_independencia")
        == "INDEPENDIENTE_DEL_AUTOR_DE_LA_CORRECCION"
        and valid_review_date(row.get("fecha", ""))
        and row.get("evidencia", "").strip() not in {"", "n/a"}
        and row.get("accion", "").strip() not in {"", "n/a"}
    )


def valid_closed_review(row: dict[str, str]) -> bool:
    return (
        row.get("resultado") in {"CONFORME", "FALLO_CORREGIDO"}
        and row.get("estado_cierre") == "CERRADO"
        and valid_review_identity(row)
    )


def valid_open_failure(row: dict[str, str]) -> bool:
    return (
        row.get("resultado") == "NO_CONFORME"
        and row.get("estado_cierre") == "ABIERTO"
        and valid_review_identity(row)
    )


def valid_expansion_trigger(row: dict[str, str]) -> bool:
    return valid_open_failure(row) or (
        row.get("resultado") == "FALLO_CORREGIDO"
        and valid_closed_review(row)
    )


def pending_review_row(
    stratum: str, key: str, review_type: str, selection: str,
    fingerprint: str,
) -> dict[str, str]:
    return {
        "id_revision": "PENDIENTE_ID",
        "estrato": stratum,
        "clave_matriz": key,
        "tipo_revision": review_type,
        "seleccion": selection,
        "resultado": "PENDIENTE",
        "revisor_independiente": "NO_ASIGNADO",
        "declaracion_independencia": "PENDIENTE",
        "fecha": "n/a",
        "evidencia": (
            "PENDIENTE: ninguna segunda inspección independiente se atribuye "
            "por generación automática."
        ),
        "accion": "Asignar revisor independiente y documentar objeto, prueba y resultado.",
        "estado_cierre": "ABIERTO",
        "huella_objeto_sha256": fingerprint,
    }


def final_object_fingerprint(row: dict[str, str]) -> str:
    candidate = row.get("huella_final_sha256", "")
    return candidate if re.fullmatch(r"[0-9a-f]{64}", candidate) else row_fingerprint(row)


def build_second_review(
    claim_matrix: list[dict[str, str]], source_matrix: list[dict[str, str]],
    requirement_matrix: list[dict[str, str]], content_trace_path: Path,
    evidence_path: Path | None,
) -> list[dict[str, str]]:
    _, trace_rows = read_dicts(content_trace_path)
    old_rows: list[dict[str, str]] = []
    if evidence_path and evidence_path.exists():
        header, old_rows = read_dicts(evidence_path)
        if header != SECOND_REVIEW_COLUMNS:
            raise BuildError(f"Cabecera incompatible en segunda revisión: {evidence_path}")
    old = {
        (row["estrato"], row["clave_matriz"], row["tipo_revision"]): row
        for row in old_rows
    }

    rows: list[dict[str, str]] = []
    matrices = {
        "AFIRMACION": (
            claim_matrix, "clave_inicial", "severidad_inicial",
            final_object_fingerprint,
            lambda row: row["estado_inicial"] == "CONFORME",
        ),
        "FUENTE": (
            source_matrix, "clave_inicial", "severidad_inicial",
            final_object_fingerprint,
            lambda row: row["veredicto_inicial"] == "CONFORME",
        ),
    }
    for stratum, (matrix, key_field, severity_field, fingerprint, conforms) in matrices.items():
        if severity_field:
            for row in matrix:
                if row[key_field].startswith("NUEVA:"):
                    continue
                if row[severity_field] in {"P0", "P1"}:
                    rows.append(pending_review_row(
                        stratum, row[key_field], "CORRECCION_P0_P1",
                        "CENSO_100_PCT", fingerprint(row),
                    ))
        conforming = [
            row for row in matrix
            if not row[key_field].startswith("NUEVA:") and conforms(row)
        ]
        failed = any(
            old_row["estrato"] == stratum
            and old_row["tipo_revision"] == "MUESTRA_CONFORME_15"
            and valid_expansion_trigger(old_row)
            for old_row in old_rows
        )
        base_sample = deterministic_sample(stratum, conforming, key_field)
        base_keys = {row[key_field] for row in base_sample}
        selected = conforming if failed else base_sample
        for row in selected:
            selection = (
                "MUESTRA_ESTRATIFICADA_15_PCT"
                if row[key_field] in base_keys else "EXPANSION_100_PCT"
            )
            rows.append(pending_review_row(
                stratum, row[key_field], "MUESTRA_CONFORME_15", selection,
                fingerprint(row),
            ))

    if len(requirement_matrix) != 483:
        raise BuildError(
            "La segunda revisión exige el censo completo de 483 requisitos; "
            f"se recibieron {len(requirement_matrix)}"
        )
    for row in requirement_matrix:
        rows.append(pending_review_row(
            "REQUISITO", row["id_requisito"], "CENSO_REQUISITO_100_PCT",
            "CENSO_100_PCT", row_fingerprint(row),
        ))

    trace_strata = {
        "prosa": "TRAZABILIDAD_PROSA",
        "arista": "TRAZABILIDAD_ARISTA",
        "celda": "TRAZABILIDAD_CELDA",
    }
    for kind, stratum in trace_strata.items():
        population = [row for row in trace_rows if row["tipo"] == kind]
        failed = any(
            old_row["estrato"] == stratum
            and valid_expansion_trigger(old_row)
            for old_row in old_rows
        )
        base_sample = deterministic_sample(stratum, population, "id_segmento")
        base_keys = {row["id_segmento"] for row in base_sample}
        selected = population if failed else base_sample
        for row in selected:
            selection = (
                "MUESTRA_ESTRATIFICADA_15_PCT"
                if row["id_segmento"] in base_keys else "EXPANSION_100_PCT"
            )
            rows.append(pending_review_row(
                stratum, row["id_segmento"], "MUESTRA_CONFORME_15",
                selection, row_fingerprint(row),
            ))

    # Solo se conserva una firma previa si el objeto exacto no cambió. Una
    # mutación invalida silenciosamente ninguna revisión: vuelve a PENDIENTE.
    for row in rows:
        key = (row["estrato"], row["clave_matriz"], row["tipo_revision"])
        previous = old.get(key)
        if previous and previous["huella_objeto_sha256"] == row["huella_objeto_sha256"]:
            if valid_closed_review(previous) or valid_open_failure(previous):
                for column in SECOND_REVIEW_COLUMNS:
                    if column != "id_revision":
                        row[column] = previous[column]
            elif previous["resultado"] == "PENDIENTE":
                # Conservar solo texto abierto; nunca promoverlo automáticamente.
                for column in (
                    "revisor_independiente", "declaracion_independencia", "fecha",
                    "evidencia", "accion", "estado_cierre",
                ):
                    row[column] = previous[column]
    for number, row in enumerate(rows, 1):
        row["id_revision"] = f"REV-{number:05d}"
    return rows


def command_output(command: Sequence[str]) -> str:
    executable = shutil.which(command[0])
    if executable is None:
        return "no disponible"
    completed = subprocess.run(
        [executable, *command[1:]], text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, check=False,
    )
    return completed.stdout.strip().splitlines()[0] if completed.stdout.strip() else "sin salida"


def final_counts(root: Path) -> dict[str, int]:
    index = load_index(root)
    claims, _ = load_claims(root)
    sources = load_sources(root)
    appendix_counts: dict[str, int] = {}
    for letter, path in appendix_paths(root).items():
        appendix_counts[letter] = len(read_dicts(path)[1])
    active_bn = len(load_negative_rows(root))
    return {
        "claims": len(claims),
        "sources": len(sources),
        "entities": appendix_counts["B"],
        "events": appendix_counts["C"],
        "dates": appendix_counts["D"],
        "hypotheses": appendix_counts["E"],
        "magnitudes": appendix_counts["F"],
        "negative_active": active_bn,
        "negative_historical": 106,
        "tables": len(index["tables"]),
    }


def report_markdown(
    claim_matrix: list[dict[str, str]], source_matrix: list[dict[str, str]],
    requirement_matrix: list[dict[str, str]], search_matrix: list[dict[str, str]],
    review: list[dict[str, str]], after: dict[str, int],
    appendix_delta_counts: dict[str, Counter[str]],
) -> bytes:
    pending = sum(row["estado_cierre"] != "CERRADO" for row in review)
    corrected_failures = sum(row["resultado"] == "FALLO_CORREGIDO" for row in review)
    verdict = (
        "CERRADA: la segunda revisión independiente está documentada."
        if pending == 0 else
        "EN CURSO: la remediación está materializada, pero la segunda revisión independiente sigue abierta."
    )
    claim_initial = Counter(row["estado_inicial"] for row in claim_matrix if row["clave_inicial"].startswith("C-"))
    claim_severity = Counter(row["severidad_inicial"] for row in claim_matrix if row["clave_inicial"].startswith("C-"))
    claim_final = Counter(row["resultado"] for row in claim_matrix)
    source_severity = Counter(row["severidad_inicial"] for row in source_matrix if row["clave_inicial"].startswith("S"))
    source_final = Counter(row["veredicto"] for row in source_matrix)
    requirement_initial = Counter(row["estado_inicial"] for row in requirement_matrix)
    requirement_final = Counter(row["estado_final"] for row in requirement_matrix)
    search_priorities = Counter(
        row["prioridad"] for row in search_matrix if BN_REF.fullmatch(row["clave_bn"])
        and row["clave_bn"] in P0_BN | P1_BN | P2_BN
    )
    lines = [
        "# Auditoría científica integral — 2026-08-08",
        "",
        "## Veredicto",
        "",
        f"**Veredicto documental:** {verdict}",
        "",
        "## Metodología",
        "",
        "La auditoría cubre el encargo literal de las secciones 0–18, las 1.840 afirmaciones y 525 fuentes iniciales, las tablas y los apéndices A–H, las 106 búsquedas negativas históricas y las 68 activas. El estado inicial se toma exclusivamente de la instantánea externa congelada; cada fila se fija con SHA-256 antes de mapearla al corpus final.",
        "",
        f"Ancla del prompt: `{PROMPT_SHA256}`. Manifiesto de hallazgos congelados: `{SNAPSHOT_FINDINGS_MANIFEST_SHA256}`.",
        "",
        "Este constructor no consulta la red y no convierte metadatos, presencia de una cita o un localizador en una inspección de pasaje. Materializa las decisiones y evidencias ya documentadas, recalcula cobertura y huellas, y deja abierta cualquier segunda revisión que no tenga firma independiente. `NO_VERIFICABLE` significa que la pasada inicial no acreditó el pasaje; no significa que la afirmación sea falsa. Un hueco científico se conserva como hueco etiquetado, no como refutación.",
        "",
        "## Resultado cuantitativo",
        "",
        "| objeto | estado inicial | estado final |",
        "|---|---:|---:|",
        f"| afirmaciones C | 1.840 | {after['claims']} |",
        f"| fuentes S | 525 | {after['sources']} |",
        f"| entidades B | 1.536 | {after['entities']} |",
        f"| eventos C | 111 | {after['events']} |",
        f"| fechas D | 282 | {after['dates']} |",
        f"| hipótesis E | 81 | {after['hypotheses']} |",
        f"| magnitudes F | 556 | {after['magnitudes']} |",
        f"| BN activas / históricas | 68 / 106 | {after['negative_active']} / 106 |",
        f"| tablas indexadas | 90 | {after['tables']} |",
        "",
        f"- Estados C iniciales: {dict(claim_initial)}; severidades: {dict(claim_severity)}.",
        f"- Disposiciones C finales: {dict(claim_final)}.",
        f"- Severidades S iniciales: {dict(source_severity)}; disposiciones finales: {dict(source_final)}.",
        f"- Requisitos iniciales: {dict(requirement_initial)}; estados finales: {dict(requirement_final)}.",
        f"- Agenda BN activa: {dict(search_priorities)}; registro total: {len(search_matrix)} (165 filas congeladas y {len(search_matrix)-165} altas documentadas).",
        "",
        "## Hallazgos por severidad",
        "",
        f"El corte inicial registró P0/P1 en C como {dict(claim_severity)} y en S como {dict(source_severity)}. Tras aplicar las disposiciones y destinos de las matrices:",
        "",
        "- P0 abiertos: 0",
        "- P1 abiertos: 0",
        "- Los huecos científicos reales permanecen etiquetados y no se cuentan como falsedades.",
        "- La segunda revisión abierta es una condición de aceptación independiente, no un hallazgo científico reclasificado silenciosamente.",
        "",
        "## Delta de apéndices",
        "",
        "El delta B–G se reconstruye fila por fila. En D se retiraron exactamente 107 filas sin C que contenían exclusivamente metadatos de publicación o fechas internas de corte. No eran 107 estimaciones científicas perdidas. Tras el estado intermedio de 189 filas, la pasada final incorporó o reconcilió 26 fechas científicamente pertinentes, retiró una fila que describía un estado ancestral —no una fecha— y añadió la fila explícita de hueco estratigráfico C-704 sin inventar límites numéricos. Las 215 filas D finales tienen todas una C válida. En F se retiró además un recuento sintético de tres adquisiciones que no era una magnitud publicada; la síntesis C correspondiente se conserva.",
        "",
    ]
    for letter in "BCDEFG":
        lines.append(f"- {letter}: {dict(appendix_delta_counts[letter])}.")
    lines.extend([
        "",
        "## Correcciones",
        "",
        "Las filas P0/P1 conservan acción y evidencia iniciales, destino final y huellas de ambos estados. Las altas usan claves `NUEVA:...`; ninguna reemplaza una clave histórica. Las fuentes retiradas permanecen en la instantánea y en la matriz S con motivo y destino, y su retirada por falta de uso canónico no se presenta como desestimación de la publicación.",
        "",
        "Las correcciones históricas BN tienen una columna delta explícita. Se conservan solo intervalos publicados donde los valores centrales no estaban publicados, y el presupuesto de *Trypanosoma brucei* conserva el total y el residual publicados. S549 se registra como modelado hidrodinámico, no como medición metabólica.",
        "",
        "## Segunda revisión",
        "",
        f"La matriz `segunda_revision_2026-08-08.csv` contiene {len(review)} objetos: censo del 100 % de P0/P1 y muestras deterministas del 15 % por estrato, incluidas prosa, aristas y celdas. Estado: {pending} abiertos; {corrected_failures} fallos detectados y corregidos. Una firma previa solo se conserva si coincide la huella exacta del objeto; un cambio la devuelve a pendiente. El constructor nunca firma por el revisor.",
        "",
        "## Límites restantes",
        "",
        "- El corte bibliográfico es 2026-08-08; evidencia posterior exige una nueva delta, no una reescritura silenciosa.",
        "- Una fuente inaccesible o un pasaje no inspeccionado no cuenta como verificado: debe permanecer degradado, retirado o como hueco documentado.",
        "- Las incertidumbres filogenéticas, cronológicas y mecanísticas reales no se cierran por automatización.",
        "- No se crea release, PDF, rama, commit ni publicación remota mediante este constructor.",
        "",
        "## Entregables reproducibles",
        "",
        "Las cuatro matrices principales, el registro histórico BN enriquecido, el delta B–G, la segunda revisión y el JSON reproducible se generan en `docs/auditorias/`. Las huellas del prompt, maestro archivado, entradas congeladas y salidas quedan en el JSON. La validación final corresponde a `make verify` en el workspace y en una copia aislada; el JSON documenta esos comandos, pero no se autoatribuye su resultado.",
    ])
    return ("\n".join(lines).rstrip() + "\n").encode("utf-8")


def build_reproducible_json(
    root: Path, snapshot: Path, payloads: dict[str, bytes],
    after: dict[str, int], review: list[dict[str, str]],
    origin_paths: Sequence[Path], removed_sources_path: Path,
) -> bytes:
    artifact_hashes = {
        relative: {"sha256": sha256_bytes(payload), "bytes": len(payload)}
        for relative, payload in sorted(payloads.items())
    }
    for relative in (
        "data/table_lineage.csv",
        "docs/auditorias/mapa_claves_inicial_final_2026-08-08.csv",
        "docs/auditorias/matriz_trazabilidad_contenido_2026-08-08.csv",
    ):
        path = root / relative
        if not path.exists():
            raise BuildError(f"Falta salida previa requerida para JSON: {relative}")
        artifact_hashes[relative] = {
            "sha256": sha256_file(path), "bytes": path.stat().st_size,
        }
    baseline_head = (
        snapshot / "metadata/git-head.txt"
    ).read_text(encoding="utf-8").strip()
    pending = sum(row["estado_cierre"] != "CERRADO" for row in review)
    data = {
        "audit_id": AUDIT_ID,
        "cutoff": CUTOFF,
        "verdict": (
            "CERRADA" if pending == 0 else "REVISION_INDEPENDIENTE_PENDIENTE"
        ),
        "anchors": {
            "prompt": {
                "path": PROMPT_RELATIVE.as_posix(), "sha256": PROMPT_SHA256,
            },
            "archived_master": {
                "path": ARCHIVE_RELATIVE.as_posix(), "sha256": ARCHIVE_SHA256,
            },
        },
        "snapshot": {
            "external_path": str(snapshot).rstrip("/") + "/",
            "head": baseline_head,
            "frozen_findings_manifest_sha256": SNAPSHOT_FINDINGS_MANIFEST_SHA256,
            "frozen_file_sha256": FROZEN_FILE_SHA256,
        },
        "frozen_aggregates": {
            "claims_audit_rows_sha256": FROZEN_AGGREGATES["claims"],
            "sources_audit_rows_sha256": FROZEN_AGGREGATES["sources"],
            "requirements_audit_rows_sha256": FROZEN_AGGREGATES["requirements"],
            "searches_audit_rows_sha256": FROZEN_AGGREGATES["searches"],
            **FROZEN_CORPUS_AGGREGATES,
        },
        "versions": {
            "python": sys.version.splitlines()[0],
            "git": command_output(["git", "--version"]),
            "make": command_output(["make", "--version"]),
            "platform": platform.platform(),
        },
        "counts": {
            "before": {
                "claims": 1840, "sources": 525, "entities": 1536,
                "events": 111, "dates": 282, "hypotheses": 81,
                "magnitudes": 556, "negative_active": 68,
                "negative_historical": 106, "tables": 90,
            },
            "after": after,
        },
        "documented_delta": {
            "dates_removed_without_claim": 107,
            "dates_removed_character": (
                "metadatos de publicación o fechas internas de corte; no eran "
                "estimaciones científicas"
            ),
            "dates_added_or_reconciled_in_final_pass": 26,
            "dates_final_without_claim": 0,
        },
        "artifacts": artifact_hashes,
        "inputs": {
            "claim_origin_maps": {
                str(path): sha256_file(path) for path in origin_paths
            },
            "removed_sources": {
                "path": str(removed_sources_path),
                "sha256": sha256_file(removed_sources_path),
            },
            "builder": {
                "path": "scripts/build_audit_deliverables.py",
                "sha256": sha256_file(Path(__file__).resolve()),
            },
        },
        "second_review": {
            "rows": len(review),
            "closed": len(review) - pending,
            "pending": pending,
            "corrected_failures": sum(
                row["resultado"] == "FALLO_CORREGIDO" for row in review
            ),
            "selection": (
                "SHA256(research-audit-2026-08-08\\x1festrato\\x1fclave), "
                "ceil(15 %) por estrato; censo 100 % P0/P1; expansión al "
                "100 % si la muestra detecta un fallo"
            ),
        },
        "commands": [
            {"name": "make verify (workspace)"},
            {"name": "python3 scripts/audit_migration.py"},
            {"name": "git diff --check"},
            {"name": "make verify (isolated copy)"},
            {"name": "double render idempotence"},
        ],
        "limitations": [
            "El constructor no consulta la red ni inspecciona pasajes.",
            "NO_VERIFICABLE no equivale a falso.",
            "Los comandos se documentan sin autoatribuir un resultado.",
            "La auditoría científica final no está cerrada mientras haya revisiones independientes pendientes.",
        ],
    }
    return (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--snapshot-root", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument(
        "--claim-origin-map", type=Path, action="append", dest="origin_maps",
        help="Mapa clave_temporal,origen; puede repetirse.",
    )
    parser.add_argument(
        "--removed-sources", type=Path,
        default=Path("/tmp/removed_sources_destination.csv"),
    )
    parser.add_argument(
        "--second-review-evidence", "--review-results", type=Path,
        help=(
            "CSV de revisión ya firmado. Si se omite, se reutiliza la salida "
            "existente; cualquier huella cambiada vuelve a PENDIENTE."
        ),
    )
    parser.add_argument(
        "--require-complete-review", action="store_true",
        help="Falla antes de escribir si queda alguna segunda revisión abierta.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    snapshot = args.snapshot_root.resolve()
    origin_paths = args.origin_maps or [
        Path("/tmp/temp_claim_origins_9001_9020.csv"),
        Path("/tmp/temp_claim_origins_9100_9131.csv"),
    ]
    origin_paths = [path.resolve() for path in origin_paths]
    removed_sources_path = args.removed_sources.resolve()
    output_dir = root / "docs/auditorias"
    paths = {
        "claims": output_dir / "matriz_afirmaciones_2026-08-08.csv",
        "sources": output_dir / "matriz_fuentes_2026-08-08.csv",
        "requirements": output_dir / "matriz_requisitos_2026-08-08.csv",
        "searches": output_dir / "registro_busquedas_2026-08-08.csv",
        "history": output_dir / "revision_busquedas_negativas_2026-08-08.csv",
        "history_md": output_dir / "REVISION-BUSQUEDAS-NEGATIVAS-2026-08-08.md",
        "appendix_delta": output_dir / "delta_apendices_2026-08-08.csv",
        "review": output_dir / "segunda_revision_2026-08-08.csv",
        "report": output_dir / "AUDITORIA-COMPLETA-2026-08-08.md",
        "json": output_dir / "auditoria_reproducible_2026-08-08.json",
    }

    try:
        validate_file_hash(root / PROMPT_RELATIVE, PROMPT_SHA256, "Prompt")
        validate_file_hash(root / ARCHIVE_RELATIVE, ARCHIVE_SHA256, "Maestro archivado")
        frozen = load_and_validate_frozen(snapshot)
        baseline_root = snapshot / "worktree"
        key_rows, key_map = load_key_map(
            root / "docs/auditorias/mapa_claves_inicial_final_2026-08-08.csv"
        )
        origins = load_origin_maps(origin_paths)
        current_claims, _ = load_claims(root)
        current_sources = load_sources(root)
        baseline_bn = load_negative_rows(baseline_root)
        current_bn = load_negative_rows(root)
        active_bn = set(current_bn)

        claim_matrix = build_claim_matrix(
            frozen["claims"], baseline_root, root, key_rows, key_map, origins
        )
        source_matrix = build_source_matrix(
            frozen["sources"], baseline_root, root, current_claims,
            removed_sources_path,
        )
        requirement_matrix = build_requirement_matrix(
            frozen["requirements"], root, active_bn,
        )
        history_rows, history_delta_lines = build_negative_history(
            snapshot, baseline_bn, current_bn
        )
        history_by_id = {row["clave_original"]: row for row in history_rows}
        search_matrix = build_search_matrix(
            frozen["searches"], active_bn, history_by_id, baseline_bn,
            current_bn, key_map
        )
        appendix_delta, appendix_delta_counts = build_appendix_delta(
            baseline_root, root
        )

        review_evidence = args.second_review_evidence
        if review_evidence is None and paths["review"].exists():
            review_evidence = paths["review"]
        review = build_second_review(
            claim_matrix, source_matrix, requirement_matrix,
            output_dir / "matriz_trazabilidad_contenido_2026-08-08.csv",
            review_evidence,
        )
        pending = [row for row in review if row["estado_cierre"] != "CERRADO"]
        if args.require_complete_review and pending:
            raise BuildError(
                f"Quedan {len(pending)} revisiones independientes abiertas; "
                "no se escribió ningún entregable."
            )

        after = final_counts(root)
        payloads = {
            paths["claims"].relative_to(root).as_posix(): csv_payload(
                CLAIM_MATRIX_COLUMNS, claim_matrix
            ),
            paths["sources"].relative_to(root).as_posix(): csv_payload(
                SOURCE_MATRIX_COLUMNS, source_matrix
            ),
            paths["requirements"].relative_to(root).as_posix(): csv_payload(
                REQUIREMENT_MATRIX_COLUMNS, requirement_matrix
            ),
            paths["searches"].relative_to(root).as_posix(): csv_payload(
                SEARCH_MATRIX_COLUMNS, search_matrix
            ),
            paths["history"].relative_to(root).as_posix(): csv_payload(
                list(history_rows[0]), history_rows
            ),
            paths["history_md"].relative_to(root).as_posix(): history_markdown(
                snapshot, history_delta_lines
            ),
            paths["appendix_delta"].relative_to(root).as_posix(): csv_payload(
                APPENDIX_DELTA_COLUMNS, appendix_delta
            ),
            paths["review"].relative_to(root).as_posix(): csv_payload(
                SECOND_REVIEW_COLUMNS, review
            ),
        }
        payloads[paths["report"].relative_to(root).as_posix()] = report_markdown(
            claim_matrix, source_matrix, requirement_matrix, search_matrix,
            review, after, appendix_delta_counts,
        )
        json_payload = build_reproducible_json(
            root, snapshot, payloads, after, review, origin_paths,
            removed_sources_path,
        )

        for relative, payload in payloads.items():
            atomic_write(root / relative, payload)
        atomic_write(paths["json"], json_payload)
    except (BuildError, KeyError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "Entregables de auditoría generados: "
        f"{len(claim_matrix)} filas C, {len(source_matrix)} filas S, "
        f"{len(requirement_matrix)} requisitos, {len(search_matrix)} búsquedas, "
        f"{len(review)} objetos de segunda revisión "
        f"({len(pending)} pendientes)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
