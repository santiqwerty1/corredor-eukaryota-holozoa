#!/usr/bin/env python3
"""Inspección editorial independiente de solo lectura; no adjudica requisitos."""
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INDEX = json.loads((ROOT / 'data/table_index.json').read_text())
ENTRIES = {row['id']: row for row in INDEX['tables']}
ORDER = [line.strip() for line in (ROOT / 'docs/order.txt').read_text().splitlines() if line.strip()]
TABLES = {}
for key, row in ENTRIES.items():
    with (ROOT / row['csv_path']).open(encoding='utf-8-sig', newline='') as handle:
        TABLES[key] = list(csv.reader(handle))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def cell(text):
    return text.replace('|', r'\|').replace('\r\n', '<br>').replace('\n', '<br>')

def table(rows):
    return '\n'.join(['| ' + ' | '.join(cell(value) for value in rows[0]) + ' |',
                      '| ' + ' | '.join('---' for _ in rows[0]) + ' |'] +
                     ['| ' + ' | '.join(cell(value) for value in row) + ' |' for row in rows[1:]])

placeholder = re.compile(r'<!-- TABLE:([a-z0-9-]+) -->')
seen_placeholders = []
def expand(match):
    key = match.group(1)
    seen_placeholders.append(key)
    return table(TABLES[key])

assembled = '\n\n'.join(placeholder.sub(expand, (ROOT / path).read_text()).rstrip() for path in ORDER).rstrip() + '\n'
full_path = ROOT / 'docs/informe_completo_autocontenido.md'
full = full_path.read_text()
lines = full.splitlines()
fences = []
fence_start = None
blocks = []
table_start = None
for number, line in enumerate(lines, 1):
    if line.startswith('```'):
        if fence_start is None:
            fence_start = number
        else:
            fences.append([fence_start, number])
            fence_start = None
    if fence_start is None and line.startswith('|'):
        if table_start is None:
            table_start = number
    elif table_start is not None:
        blocks.append([table_start, number - 1])
        table_start = None
if table_start is not None:
    blocks.append([table_start, len(lines)])

expected_headers = {
    'appendix-a': 'clave · autores · año · título · publicación o repositorio · DOI en forma https://doi.org/10.xxxx/... o URL resoluble si no hay DOI · tipo · notas de calidad · fecha de consulta',
    'appendix-b': 'etiqueta preferida · tipo · sinónimos y grafías alternativas · marcas (⚠, ≈, †, [F], [H]) como atributos de la fila · # de la fila del registro donde aparece por primera vez',
    'appendix-c': 'clave · tipo · participantes con su papel · entidad resultante si la hay · intervalo temporal · # de las filas que lo sostienen · qué fuente lo describe como evento · desenlace',
    'appendix-d': 'a qué se aplica · límite más antiguo · límite más reciente · unidad explícita · incertidumbre tal como la da la fuente · tipo · método y calibración · observado o inferido · fuente con localizador · # de la fila que la sostiene',
    'appendix-e': 'clave · qué sostiene en una frase · supuestos que da por buenos · # de las filas que la componen · fuentes a favor · fuentes en contra · con qué otras hipótesis es incompatible y en qué punto exacto · qué observación la falsaría',
    'appendix-f': 'magnitud · valor tal como lo publica la fuente · unidad original · organismo, nodo o intervalo al que se aplica · método o proxy · incertidumbre publicada · observado o inferido · fuente con localizador · #',
    'appendix-g': 'material · afirmación o estado · fuente y localizador · sección propuesta · #',
    'appendix-h': 'control · valor',
}
appendices = {}
for key, header in expected_headers.items():
    rows = TABLES[key]
    rendered = table(rows)
    start = full.find(rendered)
    appendices[key] = {
        'filas': len(rows) - 1,
        'columnas': len(rows[0]),
        'cabecera': rows[0],
        'cabecera_esperada_coincide': rows[0] == header.split(' · '),
        'apariciones_tabla_completa': full.count(rendered),
        'linea_cabecera': full[:start].count('\n') + 1 if start >= 0 else None,
        'todas_filas_cardinalidad_exacta': all(len(row) == len(rows[0]) for row in rows),
    }

known = {
    'C': {r[0] for key, rows in TABLES.items() if ENTRIES[key]['category'] == 'claims' for r in rows[1:]},
    'S': {r[0] for r in TABLES['appendix-a'][1:]},
    'E': {r[0] for r in TABLES['appendix-c'][1:]},
    'H': {r[0] for r in TABLES['appendix-e'][1:]},
    'BN': {r[0] for key, rows in TABLES.items() if ENTRIES[key]['category'] == 'negative' for r in rows[1:]},
    'V19': {r[0] for r in TABLES['claims-19'][1:]},
}
qpath = ROOT / 'docs/auditorias/registro_busquedas_2026-08-08.csv'
with qpath.open(encoding='utf-8-sig', newline='') as handle:
    qrows = list(csv.reader(handle))
known['Q'] = {r[0] for r in qrows[1:]}
patterns = {'C': r'\bC-\d{3,5}\b', 'E': r'\bE\d{2,3}\b', 'H': r'\bH\d{2,3}\b',
            'BN': r'\bBN-\d{3}\b', 'V19': r'\bV19-\d{3}\b', 'Q': r'\bQ-\d{4}\b'}
references = {}
for group, pattern in patterns.items():
    values = set(re.findall(pattern, full))
    references[group] = {'catalogadas': len(known[group]), 'usadas_distintas': len(values), 'no_definidas': sorted(values - known[group])}

source_hits = set()
missing_source_lines = []
for number, line in enumerate(lines, 1):
    found = set()
    for match in re.finditer(r'\bS(\d{2,3})(?:\s*[–-]\s*S(\d{2,3}))?\b', line):
        context = line[max(0, match.start() - 50):match.start()].lower()
        if re.search(r'(?:\bfig(?:s|ures?|uras?)?\.?|\btable|\btabla|\bsuppl(?:ementary)?\.?|\bvideo)\s*$', context):
            continue
        first = int(match.group(1)); last = int(match.group(2) or match.group(1))
        found.update(f'S{x:02d}' for x in range(first, last + 1))
    source_hits.update(found)
    missing = sorted(found - known['S'])
    if missing:
        missing_source_lines.append({'linea': number, 'claves': missing, 'texto': line})
references['S'] = {'catalogadas': len(known['S']), 'usadas_distintas': len(source_hits), 'no_definidas': sorted(source_hits - known['S'])}

headings = [{'linea': number, 'texto': line} for number, line in enumerate(lines, 1) if re.match(r'^#{1,6} ', line)]
a_start = next(x['linea'] for x in headings if x['texto'].startswith('# 17.A.'))
a_end = next(x['linea'] for x in headings if x['texto'].startswith('# 17.B.')) - 1
urls_outside_a = [{'linea': n, 'texto': line} for n, line in enumerate(lines, 1) if re.search(r'https?://', line) and not a_start <= n <= a_end]

# Este filtro solo selecciona texto que hay que leer: sus conteos no son un
# detector de idioma validado y nunca producen un dictamen de conformidad.
spanish = set('el la los las un una unos unas de del al en que y o no se con por para como entre desde hasta sobre son es era fue fueron tiene tienen había hay está están estas estos este esta su sus cuya cuyo según cuando donde mediante dentro fuera tanto cada sólo solo más menos porque puede pueden pero sin también así dicho dicha estos esas ese tras ni les lo le'.split())
english = set('the and of a an to in with by from is are was were has have had as for not or on that this these those be at into between within without can could may would should their it its they we our whereas which who than under all some most none during first new many other both only also such'.split())
def triage(value):
    stripped = re.sub(r'\[[^]]*\]|«[^»]*»|“[^”]*”|"[^"]*"|`[^`]*`|\([^)]*\)', ' ', value)
    words = re.findall(r'[A-Za-záéíóúñü]+', stripped.lower())
    es = sum(word in spanish for word in words)
    en = sum(word in english for word in words)
    return es, en, len(words)

language_candidates = []
language_samples = []
for path in ORDER:
    prose = []
    inside = False
    for number, line in enumerate((ROOT / path).read_text().splitlines(), 1):
        if line.startswith('```'):
            inside = not inside
            continue
        if not line.strip() or line.startswith(('<!--', '|')):
            continue
        es, en, length = triage(line)
        if length >= 7 and (en >= es or es == 0):
            language_candidates.append({'ruta': path, 'linea': number, 'es': es, 'en': en, 'texto': line})
        if not inside and not line.startswith(('#', '---', '- `')):
            prose.append({'ruta': path, 'linea': number, 'texto': line})
    by_line = {row['linea']: row for row in prose[:2] + prose[-2:]}
    language_samples.extend(by_line.values())
claim_candidates = []
for key, rows in TABLES.items():
    if ENTRIES[key]['category'] != 'claims':
        continue
    for row in rows[1:]:
        value = row[rows[0].index('Afirmación')]
        es, en, _ = triage(value)
        if en >= es or es == 0:
            claim_candidates.append({'clave': row[0], 'es': es, 'en': en, 'texto': value})

paths = {ROOT / p for p in ORDER} | {ROOT / row['csv_path'] for row in ENTRIES.values()}
paths |= {ROOT / p for p in ['docs/order.txt', 'data/table_index.json', 'docs/informe.md', 'docs/informe_completo_autocontenido.md', 'docs/C01-PROMPT-INVESTIGACION.md', 'docs/auditorias/registro_busquedas_2026-08-08.csv']}
inventory = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(paths)}
output = {
    'alcance': 'Inspección editorial; no verifica apoyo científico, calidad bibliográfica ni cumplimiento global.',
    'inventario_sha256': inventory,
    'salida_igual_a_ensamblado_independiente_de_todas_las_plantillas_y_csv': full == assembled,
    'lineas_markdown': len(lines),
    'plantillas': len(ORDER), 'tablas_indice': len(ENTRIES),
    'marcadores_plantillas': len(seen_placeholders), 'bloques_tabla_salida': len(blocks),
    'identificadores_tabla_omitidos': sorted(set(ENTRIES) - set(seen_placeholders)),
    'identificadores_tabla_repetidos': sorted(k for k, v in Counter(seen_placeholders).items() if v != 1),
    'tablas_con_cardinalidad_incorrecta': [key for key, rows in TABLES.items() if not all(len(r) == len(rows[0]) for r in rows)],
    'apendices': appendices,
    'referencias': references,
    'referencias_s_ausentes_lineas': missing_source_lines,
    'prefijos_prohibidos_en_documento': re.findall(r'\b(?:CLAIM|SRC|ENTITY|EVENT|HYP)-\w*', full),
    'prefijos_prohibidos_en_informe_lectura': re.findall(r'\b(?:CLAIM|SRC|ENTITY|EVENT|HYP)-\w*', (ROOT / 'docs/informe.md').read_text()),
    'encabezados': headings,
    'bloques_cercados': fences,
    'bloque_cercado_sin_cerrar': fence_start,
    'urls_fuera_de_a': urls_outside_a,
    'seleccion_lectura_idioma_no_es_dictamen': {
        'candidatos_plantillas': language_candidates,
        'candidatos_afirmaciones': claim_candidates,
        'muestras_prosa_por_plantilla': language_samples,
    },
}
print(json.dumps(output, ensure_ascii=False, indent=2))

