"""Adversarios independientes: solo fixtures temporales, no firmas reales."""
import csv
import hashlib
import io
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, '/home/santi/code/corredor-eukaryota-holozoa')
from scripts import build_audit_deliverables as b

RESULTS = []
def j(v): return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(root, name, content):
    p=root/name; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(content.encode() if isinstance(content,str) else content); return p
def csvwrite(root,name,header,rows):
    out=io.StringIO(newline=''); w=csv.DictWriter(out,fieldnames=header,quoting=csv.QUOTE_ALL,lineterminator='\n')
    w.writeheader();w.writerows(rows);return write(root,name,out.getvalue())
def record(name,fn):
    try:
        detail=fn(); RESULTS.append({'case':name,'result':'PASS','detail':detail})
    except Exception as exc:
        RESULTS.append({'case':name,'result':'FAIL','detail':f'{type(exc).__name__}: {exc}'})
def insist(value,detail):
    if not value: raise AssertionError(detail)
def rejects(fn):
    try: fn()
    except b.BuildError: return
    raise AssertionError('El constructor no rechazó el adversario')

def nominal(root,key='C-001',sha='a'*64,axis='etiquetas'):
    p=write(root,'docs/prueba.txt','Prueba artificial nominal; no es un dictamen científico real.\n')
    return dict(zip(b.NOMINAL_REVIEW_COLUMNS,[
        '1','AFIRMACION' if key.startswith('C-') else 'FUENTE',key,sha,axis,'CONFORME',
        'Autor artificial','Auditor artificial',b.NOMINAL_INDEPENDENCE,
        '2026-09-26T09:00:00Z','2026-09-26T10:00:00Z',j({'docs/prueba.txt':digest(p)}),
        'docs/prueba.txt',digest(p),'párrafo 1','Alcance nominal de prueba artificial completo.',
        'Dictamen nominal artificial del objeto y del eje exactamente identificados.',
        'Solo prueba de infraestructura; no aprueba el corpus.'
    ]))
def nominalwrite(root,rows):return csvwrite(root,b.NOMINAL_REVIEWS,b.NOMINAL_REVIEW_COLUMNS,rows)

def fixture(root):
    claim=dict.fromkeys(b.CLAIM_COLUMNS,'Fixture artificial')
    claim.update({'#':'C-001','Afirmación':'Organismo presenta carácter observado.', 'Sujeto':'Organismo',
                  'Predicado':'presenta','Objeto':'carácter observado','Atribución':'expresa',
                  'Fuente':'S01 Results, párrafo 1','Aceptación':'no evaluado'})
    csvwrite(root,'data/afirmaciones/00.csv',b.CLAIM_COLUMNS,[claim])
    write(root,'data/table_index.json',j({'tables':[{'category':'claims','section':'00','csv_path':'data/afirmaciones/00.csv'}]}))
    write(root,'data/table_lineage.csv','fixture\n')
    for path in ['data/apendices/A_fuentes.csv',str(b.SOURCE_MATRIX_PATH),'exports/acceso_fuentes.csv']:
        write(root,path,'fixture\n')
    write(root,'docs/auditorias/protocolo_censo_semantico_2026-08-13.md','Protocolo artificial explícito.\n')
    article=write(root,'fuentes/S01.xml','<article>Organismo presenta carácter observado.</article>')
    nominalwrite(root,[nominal(root,sha=b.claim_fingerprint(claim),axis=a) for a in b.EXTRA_CLAIM_AXES])
    m=b.semantic_census_module(root)
    write(root,m.FREEZE.relative_to(root),j(m.freeze_payload('2026-09-26T11:00:00Z')))
    item=m.claim_inventory()['C-001']
    primary=dict.fromkeys(m.PRIMARY_HEADER,'NO_APLICA')
    primary.update({'version_censo':'1','id_afirmacion':'C-001','ruta_canonica':item['ruta'],
        'sha256_fila':item['sha256_fila'],'atribucion':'expresa','componentes_atomicos':j(['componente']),
        'fuentes_declaradas':j(['S01']),'artefactos_verificados':j(['fuentes/S01.xml']),
        'sha256_artefactos':j({'fuentes/S01.xml':digest(article)}),'localizador_declarado':claim['Fuente'],
        'localizador_verificado':claim['Fuente'],'fragmento_control':'Organismo presenta carácter observado.',
        'sha256_pasaje':'c'*64,'matriz_cobertura_componentes':j({'componente':['S01:Results, párrafo 1']}),
        'dependencias_y_huellas':'{}','resultado':'CONFORME','motivo_dictamen':'Cotejo artificial nominal de todos los componentes de esta fixture.',
        'revisor':'Auditor primario artificial','fecha_utc':'2026-09-26T12:00:00Z','version_protocolo':digest(m.PROTOCOL)})
    csvwrite(root,m.PRIMARY.relative_to(root),m.PRIMARY_HEADER,[primary])
    secondary=dict(zip(m.SECONDARY_HEADER,['1','C-001',item['sha256_fila'],digest(m.PRIMARY),'CONFORME',
        claim['Fuente'],'c'*64,'Reinspección nominal artificial del componente y su pasaje; prueba de infraestructura.',
        'NO','NO_APLICA','Auditor secundario artificial',m.INDEPENDENCE_DECLARATION,'2026-09-26T13:00:00Z']))
    csvwrite(root,m.SECONDARY.relative_to(root),m.SECONDARY_HEADER,[secondary])
    insist(m.validate()==[],str(m.validate()))
    return claim,m,primary,secondary

def path_case(name,mode):
    with tempfile.TemporaryDirectory() as raw:
        root=Path(raw);row=nominal(root);target=root/name;target.parent.mkdir(parents=True,exist_ok=True)
        if mode=='logical':target.symlink_to(root/'docs/prueba.txt');rel=name
        else:
            write(root,name,'Derivado circular artificial')
            if mode=='resolved':
                (root/'alias.txt').symlink_to(target);rel='alias.txt'
            elif mode=='parent':
                (root/'alias_dir').symlink_to(target.parent,target_is_directory=True);rel='alias_dir/'+target.name
            else:rel=name
        row['evidencia_local']=rel;row['huella_evidencia_sha256']=digest(root/rel)
        nominalwrite(root,[row]);rejects(lambda:b.load_nominal_reviews(root))
        return 'Se rechaza, sin transformar circularidad en historia obsoleta.'

def stale_and_cycle():
    with tempfile.TemporaryDirectory() as raw:
        root=Path(raw);row=nominal(root);write(root,'manifest.json','{}')
        row['artefactos_inspeccionados']=j({'aaa-ausente.txt':'a'*64,'manifest.json':digest(root/'manifest.json')})
        nominalwrite(root,[row]);rejects(lambda:b.load_nominal_reviews(root))
        return 'La ausencia anterior no oculta el ciclo posterior.'
def nominal_history():
    with tempfile.TemporaryDirectory() as raw:
        root=Path(raw);old=nominal(root);p=nominalwrite(root,[old]);before=p.read_bytes()
        write(root,'docs/prueba.txt','Nueva versión artificial de la prueba.\n')
        hist=b.load_nominal_reviews(root);insist(not hist and len(hist.obsolete)==1,'Firma obsoleta presta resultado')
        insist(p.read_bytes()==before,'Reescritura de firma histórica')
        new={**old,'fecha_revision_utc':'2026-09-26T14:00:00Z','huella_evidencia_sha256':digest(root/'docs/prueba.txt')}
        new['artefactos_inspeccionados']=j({'docs/prueba.txt':new['huella_evidencia_sha256']})
        nominalwrite(root,[old,new]);current=b.load_nominal_reviews(root)
        insist(len(current)==1 and len(current.obsolete)==1,'Historia/reinspección no separadas')
        nominalwrite(root,[new,{**new,'resultado':'NO_CONFORME'}]);rejects(lambda:b.load_nominal_reviews(root))
        return 'Historia intacta, reinspección nueva elegible, duplicado vigente rechazado.'

def census_case(mode):
    with tempfile.TemporaryDirectory() as raw:
        root=Path(raw);claim,m,pri,sec=fixture(root)
        if mode=='valid':
            first=b.load_claim_review_evidence(root);second=b.load_claim_review_evidence(root)
            insist(first==second,'Resultado no determinista')
            insist(b.claim_closure(b.final_claim_axes([claim],first))=='CERRADO','No admite fixture íntegra')
            return 'Dos lecturas idénticas, censo real validate() íntegro y dos ejes nominales.'
        if mode=='primary_duplicate':csvwrite(root,m.PRIMARY.relative_to(root),m.PRIMARY_HEADER,[pri,pri]);sec['sha256_censo_primario']=digest(m.PRIMARY)
        elif mode=='secondary_duplicate':csvwrite(root,m.SECONDARY.relative_to(root),m.SECONDARY_HEADER,[sec,sec])
        elif mode=='source_stale':write(root,'fuentes/S01.xml','Otra versión de la fuente')
        elif mode=='control_stale':write(root,b.SOURCE_MATRIX_PATH,'Otra versión de la matriz S')
        elif mode=='dependency':pri['dependencias_y_huellas']=j({'C-999':'b'*64});csvwrite(root,m.PRIMARY.relative_to(root),m.PRIMARY_HEADER,[pri]);sec['sha256_censo_primario']=digest(m.PRIMARY)
        elif mode=='negative':
            pri['resultado']='NO_CONFORME';sec['resultado_independiente']='NO_CONFORME'
            csvwrite(root,m.PRIMARY.relative_to(root),m.PRIMARY_HEADER,[pri]);sec['sha256_censo_primario']=digest(m.PRIMARY)
        elif mode=='missing_secondary':m.SECONDARY.unlink()
        if mode in {'primary_duplicate','dependency','negative'}:csvwrite(root,m.SECONDARY.relative_to(root),m.SECONDARY_HEADER,[sec])
        ev=b.load_claim_review_evidence(root)
        insist(ev.errors and b.claim_closure(b.final_claim_axes([claim],ev))=='ABIERTO','Cierre indebido: '+str(ev))
        return 'Permanece abierto: '+str(ev.errors)[:500]

def race_artifact():
    with tempfile.TemporaryDirectory() as raw:
        root=Path(raw);claim,m,_,_=fixture(root);real=m.validate
        def changed_after_validation():
            result=real();write(root,'fuentes/S01.xml','Mutación entre validación y enlace, fuente ya no vigente.');return result
        m.validate=changed_after_validation
        with patch.object(b,'semantic_census_module',return_value=m):
            try:ev=b.load_claim_review_evidence(root)
            except b.BuildError:return 'Rechazo del cambio concurrente.'
        insist(b.claim_closure(b.final_claim_axes([claim],ev))!='CERRADO','Aprueba tras mutación de artefacto inmediatamente después de validate()')

def global_case(mode):
    with tempfile.TemporaryDirectory() as raw:
        root=Path(raw);claim,m,_,_=fixture(root)
        ev=b.load_claim_review_evidence(root)
        matrix=[{'clave_inicial':'C-001','estado_inicial':'CORREGIR','severidad_inicial':'P0',
            'huella_final_sha256':b.claim_fingerprint(claim),'estado_hallazgo':'CERRADO','evidencia_final':ev.evidence([claim])}]
        requirements=[{'id_requisito':f'R-{n:04d}'} for n in range(1,484)]
        trace=csvwrite(root,'trace.csv',['tipo','id_segmento'],[])
        rows=b.build_second_review(matrix,[],requirements,trace,None,root=root)
        sig={**rows[0],'resultado':'CONFORME','estado_cierre':'CERRADO','revisor_independiente':'Global artificial',
            'declaracion_independencia':'INDEPENDIENTE_DEL_AUTOR_DE_LA_CORRECCION','fecha':'2026-09-26T14:00:00Z',
            'evidencia':'Revisión artificial con expediente_sha256='+b.row_fingerprint(matrix[0]),'accion':'Sin cambio artificial'}
        if mode=='premature':sig['fecha']='2026-09-26T11:30:00Z'
        inputs=[sig]
        if mode.startswith('duplicate'):
            negative={**sig,'resultado':'NO_CONFORME','estado_cierre':'ABIERTO','evidencia':'Discrepancia artificial abierta'}
            inputs=[negative,sig] if mode=='duplicate_last_approval' else [sig,negative]
        if mode=='changed_dossier':matrix[0]['evidencia_final']+=' Cambio del expediente sin cambiar la C.'
        p=csvwrite(root,'global.csv',b.SECOND_REVIEW_COLUMNS,inputs)
        try:out=b.build_second_review(matrix,[],requirements,trace,p,root=root)[0]
        except b.BuildError:
            insist(mode.startswith('duplicate'),'Rechazo inesperado');return 'Duplicado rechazado.'
        if mode=='valid':insist(out['resultado']=='CONFORME','Firma íntegra no conservada')
        elif mode.startswith('duplicate'):raise AssertionError('Duplicados aceptados; resultado final='+out['resultado'])
        else:insist(out['resultado']=='PENDIENTE','Firma indebidamente conservada='+out['resultado'])
        return 'Resultado='+out['resultado']

for name in ['manifest.json','data/auditoria/requisitos_disposiciones.csv','docs/auditorias/controles_requisitos/R-0001.csv','docs/auditorias/matriz_fuentes_2026-08-08.csv']:
    for mode in ['direct','logical','resolved','parent']:
        record('cycle_'+name+'_'+mode,lambda name=name,mode=mode:path_case(name,mode))
record('stale_cannot_hide_cycle',stale_and_cycle)
record('nominal_history_and_duplicates',nominal_history)
for mode in ['valid','primary_duplicate','secondary_duplicate','source_stale','control_stale','dependency','negative','missing_secondary']:
    record('census_'+mode,lambda mode=mode:census_case(mode))
record('artifact_changed_after_validate',race_artifact)
for mode in ['valid','changed_dossier','premature','duplicate_last_approval','duplicate_last_failure']:
    record('global_'+mode,lambda mode=mode:global_case(mode))
print(json.dumps({'tests':len(RESULTS),'passed':sum(r['result']=='PASS' for r in RESULTS),'results':RESULTS},ensure_ascii=False,indent=2))
