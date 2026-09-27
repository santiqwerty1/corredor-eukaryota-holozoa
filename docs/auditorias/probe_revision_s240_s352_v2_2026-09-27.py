"""Captura independiente de sólo lectura; no produce dictámenes automáticos."""
import csv
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PROPOSAL=ROOT/'docs/auditorias/PROPUESTA_AUTOR_6_CELDAS_S240_S352_V2_2026-09-27.json'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def rh(value): return sha((json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode())
def norm(node): return ' '.join(''.join(node.itertext()).split())
def rows(path):
    with (ROOT/path).open(newline='') as f: return list(csv.DictReader(f))
p=json.loads(PROPOSAL.read_text())
out={'revisor':'/root/revision_residuales/candidatos_editoriales','fecha_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'propuesta':str(PROPOSAL.relative_to(ROOT)),'sha256_propuesta':sha(PROPOSAL.read_bytes()),'objetos':[],'pasajes':{},'fuentes':[],'disposiciones':[],'archivos_base':[]}
def add(name,category,index,value,path,previous=None):
    item={'objeto':name,'categoria':category,'indice':index,'ruta':path,'sha256_objeto':rh(value),'valor':value}
    if previous is not None:
        item['sha256_anterior']=rh(previous)
        item['anterior_presente_vivo']=previous in rows(path)
    out['objetos'].append(item)
for cat in ['C_altas','C_correcciones','C_conservadas','F_altas','F_correcciones','B_altas','B_correcciones','A_altas']:
    for i,x in enumerate(p[cat]):
        value=x.get('fila',x.get('despues'))
        name=value.get('#') if cat.startswith('C_') else f'{cat}-{i+1}'
        add(name,cat,i,value,x['ruta'],x.get('antes'))
        if cat=='C_conservadas':out['objetos'][-1]['conservada_presente_vivo']=value in rows(x['ruta'])
for i,x in enumerate(p['prosa_cambios']):
    add(f'PROSA-{i+1}','prosa_cambios',i,x['despues'],x['ruta'])
    out['objetos'][-1]['sha256_objeto']=sha((x['despues']+'\n').encode())
    out['objetos'][-1]['ocurrencias_antes']= (ROOT/x['ruta']).read_text().count(x['antes'])
for i,x in enumerate(p['metadatos_tablas']):
    add(f'META-{i+1}','metadatos_tablas',i,x['despues'],x['ruta'])
    out['objetos'][-1]['sha256_objeto']=sha((x['despues']+'\n').encode())
    out['objetos'][-1]['anterior_presente_vivo']=rows(x['ruta'])[int(x['fila'])-2][x['columna']]==x['antes']
for d in p['disposiciones_registro_propuestas']:
    out['disposiciones'].append({'claim_id':d['claim_id'],'sha256_disposicion':rh({k:v for k,v in d.items() if k!='revision_independiente'}),'componentes':d['componentes'],'C_soporte':d['afirmaciones_soporte'],'artefactos':d['artefactos_soporte']})
for path,digest in p['huellas_archivos_base'].items():
    actual=sha((ROOT/path).read_bytes());out['archivos_base'].append({'ruta':path,'sha256_propuesta':digest,'sha256_vivo':actual,'coincide':actual==digest})
for x in p['fuentes']:
    path=Path(x.get('ruta',x.get('ruta_temporal')))
    if not path.is_absolute():path=ROOT/path
    out['fuentes'].append({'clave':x['clave'],'ruta_leida':str(path),'sha256':sha(path.read_bytes()),'coincide_autor':sha(path.read_bytes())==x['sha256_archivo']})
source_paths={x['clave']:x['ruta_leida'] for x in out['fuentes'] if x['ruta_leida'].endswith('.xml')}
roots={s:ET.parse(path).getroot() for s,path in source_paths.items()}
def passage(key,source,locator,text):
    text=' '.join(text.split())
    out['pasajes'][key]={'fuente':source,'localizador':locator,'texto_normalizado':text,'sha256_pasaje':sha((text+'\n').encode())}
for pid in ['Par7','Par10','Par14','Par15','Par16']:
    passage('S240_'+pid,'S240',f'JATS p[@id={pid}]',norm(next(x for x in roots['S240'].iter('p') if x.get('id')==pid)))
passage('S240_Methods','S240','Methods, Phylogenomics, JATS sec[@id=Sec14]',norm(next(x for x in roots['S240'].iter('sec') if x.get('id')=='Sec14')))
tab=next(x for x in roots['S240'].iter('table-wrap') if x.get('id')=='Tab1')
passage('S240_Table1','S240','Table1: fila Genome size (Mbp), columnas Perkinsela/Bodo y nota b',norm(tab))
for sid in ['sec2.1','sec4.2','sec4.4']:
    sec=next(x for x in roots['S563'].iter('sec') if x.get('id')==sid)
    passage('S563_'+sid,'S563',f'JATS sec[@id={sid}]/p[1]',norm(sec.find('p')))
for title,key,ordinal in [('Gene repertoire of Capsaspora','S352_GeneRepertoire_p4',4),('Gene family analysis','S352_Methods',1)]:
    sec=next(x for x in roots['S352'].iter('sec') if x.find('title') is not None and norm(x.find('title'))==title)
    passage(key,'S352',f'{title}, párrafo hijo directo {ordinal}',norm(sec.findall('p')[ordinal-1]))
fig=next(x for x in roots['S352'].iter('fig') if x.get('id')=='f4')
passage('S352_Fig4_leyenda','S352','Fig4 pPDF6/impresa6, leyenda completa; símbolos inspeccionados visualmente',norm(fig.find('caption')))
supp='/tmp/S352-supplement-preparacion-v2-20260927.pdf'
pages={pg:subprocess.check_output(['pdftotext','-f',str(pg),'-l',str(pg),'-layout',supp,'-'],text=True) for pg in [43,44,94,95,96]}
specs=[('S352_SI_7TM',94,'C. owczarzaki has a rich repertoire','The origin of the three subunits'),('S352_SI_Hh_inicio',95,'Main players of the canonical Hedgehog',None),('S352_SI_Hh_fin',96,'C-terminal part','Similarly, no receptor'),('S352_SI_Wnt',96,'Similarly, no receptor','The JAK/STAT'),('S352_S26_leyenda',44,'Supplementary Figure S26. Conservation',None)]
for key,pg,start,end in specs:
    text=pages[pg].split(start,1)[1]
    if end:text=text.split(end,1)[0]
    text=start+text
    text=re.sub(r'\s'+str(pg)+r'\s*\f?\s*$','',text)
    passage(key,'S352',f'Supplementary Information pPDF/impresa{pg}; bloque desde {start}',text)
out['imagenes_inspeccionadas']=[{'ruta':path,'sha256':sha(Path(path).read_bytes())} for path in ['/tmp/S352-fig4-review-20260927.png','/tmp/S352-s26-independiente-v2-20260927-043.png','/tmp/S352-s26-independiente-v2-20260927-044.png']]
out['B_metodos_candidates']={term:[r for r in rows('data/apendices/B_entidades.csv') if re.search(r'(?<![A-Za-z])'+re.escape(term)+r'(?![A-Za-z])',json.dumps(r,ensure_ascii=False),re.I)] for term in ['Illumina','SGA','Velvet','SSPACE','Gapfiller','Image','ICORN','REAPR','HMMER','RAxML','PhyloBayes','FastTree','BLASTP','crio-SEM']}
print(json.dumps(out,ensure_ascii=False,indent=2))
