"""Read-only capture for the independent v2 review; stdout only."""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
PROPOSAL = ROOT / 'docs/auditorias/PROPUESTA_REPARACION_C1664_C1642_C1121_V2_2026-09-27.json'
def sha(data):
    return hashlib.sha256(data).hexdigest()
def rowsha(row):
    return sha((json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode())
def rows(path):
    with (ROOT / path).open(newline='') as stream:
        return list(csv.DictReader(stream))
p = json.loads(PROPOSAL.read_text())
result = {'fecha_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'revisor': '/root/revision_residuales/candidatos_editoriales', 'propuesta': str(PROPOSAL.relative_to(ROOT)), 'sha256_propuesta': sha(PROPOSAL.read_bytes()), 'normalizacion_objeto': 'JSON UTF-8 ensure_ascii=False, sort_keys=True, separators=(comma,colon), LF final; prosa UTF-8 literal + LF', 'objetos': [], 'fuentes': [], 'pasajes': [], 'bn': []}
def add(name, pointer, obj, path, previous=None, live=None):
    item = {'objeto': name, 'puntero_propuesta': pointer, 'ruta': path, 'propuesto': obj, 'sha256_objeto': sha((obj+'\n').encode()) if isinstance(obj,str) else rowsha(obj)}
    if previous is not None:
        item.update(anterior=previous, coincide_anterior_vivo=previous == live, sha256_anterior=sha((previous+'\n').encode()) if isinstance(previous,str) else rowsha(previous))
    result['objetos'].append(item)
claims = {r['#']: r for path in (ROOT / 'data/afirmaciones').glob('*.csv') for r in rows(str(path.relative_to(ROOT)))}
for i,x in enumerate(p['C_correcciones']):
    add(x['claim_id'],f'/C_correcciones/{i}/propuesta',x['propuesta'],x['ruta'],x['anterior'],claims[x['claim_id']])
for i,x in enumerate(p['C_altas']):
    add(x['fila']['#'],f'/C_altas/{i}/fila',x['fila'],x['ruta'])
    result['objetos'][-1]['id_ausente_del_vivo'] = x['fila']['#'] not in claims
for i,x in enumerate(p['F_sustituciones']):
    old = rows('data/apendices/F_magnitudes.csv')
    for j,obj in enumerate(x['nuevas']):
        add(f'F-S{i+1}-{j+1}',f'/F_sustituciones/{i}/nuevas/{j}',obj,'data/apendices/F_magnitudes.csv',x['anterior'],next((r for r in old if r==x['anterior']),None))
for i,obj in enumerate(p['F_altas']):
    add(f'F-A{i+1}',f'/F_altas/{i}',obj,'data/apendices/F_magnitudes.csv')
for i,x in enumerate(p['tablas_correcciones']):
    add(f'TABLA-{i+1}',f'/tablas_correcciones/{i}/propuesta',x['propuesta'],x['ruta'],x['anterior'],next((r for r in rows(x['ruta']) if r==x['anterior']),None))
for i,x in enumerate(p['prosa']):
    add(f'PROSA-{x["linea"]}',f'/prosa/{i}/propuesta',x['propuesta'],x['ruta'],x['anterior'],(ROOT/x['ruta']).read_text().splitlines()[x['linea']-1])
br = rows('data/apendices/B_entidades.csv')
for i,obj in enumerate(p['B_altas']):
    add(f'B-{i+1}',f'/B_altas/{i}',obj,'data/apendices/B_entidades.csv')
    result['objetos'][-1]['coincidencias_etiqueta_viva'] = sum(r['etiqueta preferida']==obj['etiqueta preferida'] for r in br)
for x in p['artefactos']:
    path = Path(x.get('ruta',x.get('ruta_temporal')))
    if not path.is_absolute(): path = ROOT/path
    result['fuentes'].append({'clave': x['clave'], 'ruta':str(path), 'sha256':sha(path.read_bytes()), 'coincide_propuesta':sha(path.read_bytes())==x['sha256']})
xml = ET.parse(ROOT/p['artefactos'][1]['ruta']).getroot()
for pid in ['P1','P5','P7','P12','P35','P36','P37','P53','P54','P60','P61','P65']:
    node=next(x for x in xml.iter('p') if x.get('id')==pid)
    text=' '.join(''.join(node.itertext()).split())+'\n'
    result['pasajes'].append({'S':'S513','localizador':pid,'normalizacion':'itertext, blancos simples, LF final','sha256':sha(text.encode()),'texto':text})
for path in [Path('/tmp/S517-p2-raw-revision-20260927.txt'), Path('/tmp/S517-revision-independiente-20260927.txt')]:
    result['pasajes'].append({'S':'S517','ruta_extracto':str(path),'sha256':sha(path.read_bytes()),'procedencia':'pdftotext de PDF identificado; no fuente distinta'})
for i,row in enumerate(rows('data/busquedas_negativas/15_5_15-5-asociacion-integracion-y-transferencia.csv'),2):
    if row['clave'] in ['BN-044','BN-111','BN-113']:
        result['bn'].append({'fila_csv':i,'fila':row,'sha256':rowsha(row)})
result['B_vivo_sha256'] = sha((ROOT/'data/apendices/B_entidades.csv').read_bytes())
result['B_metodos_busqueda_literal'] = {term:[r for r in br if term.casefold() in json.dumps(r,ensure_ascii=False).casefold()] for term in ['BPMM','MR-BPMM','MCMCglmm','SCM','bayesian phylogenetic','mapas estocásticos','filogenético mixto']}
print(json.dumps(result,ensure_ascii=False,indent=2))
