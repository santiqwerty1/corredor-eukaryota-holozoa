"""Captura read-only de deltas; los resultados no son dictámenes científicos."""
import csv
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUD = ROOT / 'docs/auditorias'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def rh(value): return sha((json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))+'\n').encode())
def ch(value): return sha((value+'\n').encode())
def read(name): return json.loads((AUD/name).read_text())
def rows(path):
    with path.open(newline='') as f: return list(csv.DictReader(f))

name = 'PROPUESTA_AUTOR_ADENDA_S240_S352_V2_2026-09-27.json'
a = read(name)
b = read('PROPUESTA_AUTOR_6_CELDAS_S240_S352_V2_2026-09-27.json')
old = read('evidencia_independiente_s240_s352_v2_2026-09-27.json')
fresh = json.loads(subprocess.check_output([sys.executable, str(AUD/'probe_revision_s240_s352_v2_2026-09-27.py')], text=True))
out = {'revisor':'/root/revision_residuales/candidatos_editoriales',
       'fecha_captura_utc':datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
       'rol':'CAPTURA_INDEPENDIENTE_NO_ADJUDICACION_AUTOMATICA',
       'propuesta':{'ruta':str((AUD/name).relative_to(ROOT)), 'sha256':sha((AUD/name).read_bytes())},
       'artefactos':[], 'C':[], 'B':[], 'prosa':[], 'checks':{},
       'pasajes_reextraidos':fresh['pasajes'], 'fuentes_releidas':fresh['fuentes'],
       'imagenes_reinspeccionadas':fresh['imagenes_inspeccionadas']}
for path in [a['base_inmutable']['ruta'],a['evidencia_autor']['ruta'],
             'docs/auditorias/INFORME_AUTOR_ADENDA_S240_S352_V2_2026-09-27.md',
             'scripts/residual_semantic_dispositions.py','docs/C01-PROMPT-INVESTIGACION.md']:
    out['artefactos'].append({'ruta':path,'sha256':sha((ROOT/path).read_bytes())})
out['checks']['pasajes_iguales_a_captura_previa']={k:old['pasajes'][k]==v for k,v in fresh['pasajes'].items()}
out['checks']['base_fija']=sha((ROOT/a['base_inmutable']['ruta']).read_bytes())==a['base_inmutable']['sha256']
out['checks']['evidencia_autor_fija']=sha((ROOT/a['evidencia_autor']['ruta']).read_bytes())==a['evidencia_autor']['sha256']
base_c={x['fila']['#']:x['fila'] for x in b['C_altas']+b['C_conservadas']}
prospective={r['#']:r for path in sorted((ROOT/'data/afirmaciones').glob('*.csv')) for r in rows(path)}
out['C1581_viva']={'fila':prospective['C-1581'],'sha256':rh(prospective['C-1581'])}
prospective.update(base_c)
prospective.update({x['despues']['#']:x['despues'] for x in b['C_correcciones']})
for x in a['C_reemplazos']:
    ident=x['despues']['#']; prospect=prospective[ident]
    item={'id':ident,'antes':x['antes'],'despues':x['despues'],
          'sha256_antes':rh(x['antes']),'sha256_despues':rh(x['despues']),
          'antes_igual_base':prospect==x['antes'],
          'huellas_correctas':rh(x['antes'])==x['sha256_antes'] and rh(x['despues'])==x['sha256_despues'],
          'campos_cambiados':[k for k in x['antes'] if x['antes'][k]!=x['despues'][k]]}
    out['C'].append(item); prospective[ident]=x['despues']
out['contexto_documental']=[{'fila':base_c[k],'sha256':rh(base_c[k])} for k in ['C-2847','C-2848','C-2849','C-2851']]
bf=rows(ROOT/'data/apendices/B_entidades.csv')
for x in a['B_altas_adicionales']:
    row=x['fila']; term=row['etiqueta preferida']; pattern=r'(?<![A-Za-z])'+re.escape(term)+r'(?![A-Za-z])'
    hits=[]
    for key,r in sorted(prospective.items(), key=lambda kv:int(kv[0].split('-')[1])):
        fields={k:v for k,v in r.items() if re.search(pattern,v,re.I)}
        if fields:hits.append({'id':key,'campos':fields,'sha256':rh(r)})
    anchor=row['# de la fila del registro donde aparece por primera vez']
    out['B'].append({'fila':row,'sha256_fila':rh(row),'hash_correcto':rh(row)==x['sha256_fila'],
      'tipo_ancla_autor':x['tipo_ancla'],'apariciones_C':hits,
      'ancla_contiene_termino':any(y['id']==anchor for y in hits),
      'primera_C_literal':hits[0]['id'] if hits else None,
      'existentes_B':[r for r in bf if re.search(pattern,r['etiqueta preferida'],re.I)],
      'anclas_F_autor_cotejadas':[{'fila':y['fila'],'sha256':rh(y['fila']),
          'igual_F_base':y['fila'] in [z['fila'] for z in b['F_altas']]} for y in x.get('evidencia_ancla',{}).get('menciones_F',[])]})
for x in a['prosa_reemplazos_de_objeto']:
    out['prosa'].append({'indice_base':x['indice_base'],'antes_igual_base':x['antes']==b['prosa_cambios'][x['indice_base']],
      'sha256_texto_despues':ch(x['despues']['despues']), 'despues':x['despues'],
      'hash_correcto':ch(x['despues']['despues'])==x['despues']['sha256_despues']})
d=a['disposicion_C2474_reemplazo']['despues']; d0=next(x for x in b['disposiciones_registro_propuestas'] if x['claim_id']=='C-2474')
out['disposicion']={'valor':d,'sha256_sin_revision':rh({k:v for k,v in d.items() if k!='revision_independiente'}),
 'antes_igual_base':a['disposicion_C2474_reemplazo']['antes']==d0,
 'campos_cambiados':[k for k in d0 if d0[k]!=d[k]],
 'C_soporte_correctas':{k:rh(prospective[k])==v for k,v in d['afirmaciones_soporte'].items()},
 'fuentes_destino_presentes':{k:(ROOT/k).exists() for k in d['artefactos_soporte']}}
out['checks']['sin_cambio_contenido_componentes_C2474']=all(d[k]==d0[k] for k in ['contenido_nuevo','sha256_nuevo','componentes','limites_pendientes','artefactos_soporte','identidad_fila'])
out['checks']['huella_contenido_correcta_C2474']=ch(d['contenido_nuevo'])==d['sha256_nuevo']
out['checks']['C1581_inalterada']=out['C1581_viva']['sha256']==a['metadatos_conservacion']['sha256_fila_intacta']
print(json.dumps(out,ensure_ascii=False,indent=2))
