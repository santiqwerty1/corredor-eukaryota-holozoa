"""Adversarios independientes. Sólo escribe fixtures generadas en /tmp.

No crea firmas reales ni muta canónicos. Los dictámenes técnicos se registran
por separado después de inspeccionar estas observaciones.
"""
from __future__ import annotations
import copy
import csv
import hashlib
import io
import json
import tempfile
from contextlib import ExitStack
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from scripts import build_atomic_cell_claims as atomic
from scripts import remediate_trace_residuals as rem

LIVE = atomic.ROOT
def sha(raw): return hashlib.sha256(raw).hexdigest()
def rows(raw): return list(csv.DictReader(io.StringIO(raw.decode())))
def csvfile(path, header, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(atomic._csv_bytes(header, data))
def record(key, strength='alta'):
    return dict(zip(atomic.CLAIM_HEADER,[key,'Proposición FICTICIA '+key,'Ficción','posee_rasgo','Fixture',
      'expresa','S01 apartado ficticio','no evaluado',strength,'Fixture técnica sin validez científica','resuelta','vigente']))

class Fixture:
    def __init__(self, root):
        self.root=root
        self.ids=[f'C-{i}' for i in range(1996,2570)]+[f'C-{i}' for i in range(2572,2814)]
        self.paths={
          'TARGET_FILES':(root/'target1.csv',root/'target2.csv'),
          'CORRECTIONS':root/'corrections.csv','CLAIMS':root/'data/afirmaciones/15.csv',
          'MANIFEST':root/'manifest.csv','PREDICATE_DEFINITION':root/'predicate.md'}
        self.targets=[]; self.table_rows=[]; self.manifest=[]; self.corrected={}
        table='data/tablas/ficticia.csv'
        self.table_path=root/table
        self.special_path=root/'data/tablas/table-06-ficticia.csv'
        self.special_rows=[{'estudio':'FICTICIO tabla06','dato':'viejo [C-029]','filas y fuentes':'C-028; BN-115'} for _ in range(40)]
        for i,key in enumerate(self.ids):
            path=table; number=i+2
            if key=='C-2009':path=self.special_path.relative_to(root).as_posix();number=5
            if key=='C-2029':path=self.special_path.relative_to(root).as_posix();number=25
            value='viejo [C-029]'
            self.table_rows.append({'estudio':'FICTICIO '+key,'dato':value,'filas y fuentes':'C-028; BN-115'})
            t=dict(zip(atomic.TARGET_HEADER,[path,str(number),'dato',atomic._digest(value),value,
              'C-029; C-1983',key,'RECHAZO_FICTICIO','fixture sin dictamen científico real']))
            self.targets.append(t)
            self.manifest.append(dict(zip(atomic.MANIFEST_HEADER,[path,str(number),'dato',atomic._digest(value),
              value,'C-029','fixture','NO_CONFORME','historia FICTICIA para test'])))
        self.supports=[record(f'C-{i:03d}','baja' if i==32 else 'alta') for i in range(28,34)]+[record('C-1983')]
        self.support_path=root/'data/afirmaciones/00.csv'
        self.residual_path=root/'residuals.csv'
        self.registry=root/'data/auditoria/disposiciones_residuales_semanticas_v1.json'
        self.reset()
    def reset(self):
        self.corrected={}
        csvfile(self.paths['TARGET_FILES'][0],atomic.TARGET_HEADER,self.targets[:574])
        csvfile(self.paths['TARGET_FILES'][1],atomic.TARGET_HEADER,self.targets[574:])
        csvfile(self.paths['CORRECTIONS'],atomic.CORRECTION_HEADER,[])
        csvfile(self.paths['CLAIMS'],atomic.CLAIM_HEADER,[])
        csvfile(self.support_path,atomic.CLAIM_HEADER,self.supports)
        csvfile(self.paths['MANIFEST'],atomic.MANIFEST_HEADER,self.manifest)
        csvfile(self.table_path,['estudio','dato','filas y fuentes'],self.table_rows)
        csvfile(self.special_path,['estudio','dato','filas y fuentes'],self.special_rows)
        self.paths['PREDICATE_DEFINITION'].write_text('`tiene_valor_literal_de_campo*` relaciona un estudio, matriz, taxón o sistema con el nombre y el contenido literales de una sola celda tabular. Ejemplo: C-1996\n')
        csvfile(self.residual_path,rem.RESIDUAL_HEADER,[])
        self.registry.parent.mkdir(parents=True,exist_ok=True)
        self.registry.write_text('{"version":1,"disposiciones":[]}\n')
    def correction(self, key, value):
        target=next(x for x in self.targets if x['claim_id']==key)
        correction={k:target[k] for k in ['csv_path','fila','columna','claim_id']}
        correction.update(contenido_previo=target['contenido'],contenido_previo_sha256=target['contenido_sha256'],
          contenido_corregido=value,contenido_corregido_sha256=atomic._digest(value),
          autor_correccion='AUTOR_FICTICIO_TEST_INDEPENDIENTE',evidencia_correccion='fixture de autor, no aprobación')
        self.corrected[key]=correction
        csvfile(self.paths['CORRECTIONS'],atomic.CORRECTION_HEADER,list(self.corrected.values()))
        tablepath=self.root/target['csv_path']; data=rows(tablepath.read_bytes());data[int(target['fila'])-2]['dato']=value
        csvfile(tablepath,['estudio','dato','filas y fuentes'],data)
    def context(self):
        stack=ExitStack()
        stack.enter_context(patch.object(atomic,'ROOT',self.root))
        for k,v in self.paths.items():stack.enter_context(patch.object(atomic,k,v))
        for k,v in {'ROOT':self.root,'TARGETS':self.paths['TARGET_FILES'],'CORRECTIONS':self.paths['CORRECTIONS'],'RESIDUALS':self.residual_path}.items():
            stack.enter_context(patch.object(rem,k,v))
        return stack
    def run(self, key='C-2606'):
        with self.context(): a,m,ids=atomic.build()
        c=next(x for x in rows(a) if x['#']==key)
        entry=next(x for x in rows(m) if x['csv_path']==next(t['csv_path'] for t in self.targets if t['claim_id']==key) and x['fila']==next(t['fila'] for t in self.targets if t['claim_id']==key))
        return {'claim':c,'manifest':entry,'claims_sha256':sha(a),'manifest_sha256':sha(m),'count':len(ids)}

def main():
    selected=[LIVE/'scripts/build_atomic_cell_claims.py',LIVE/'tests/test_build_atomic_cell_claims.py',
      *atomic.TARGET_FILES,atomic.CORRECTIONS,atomic.CLAIMS,atomic.MANIFEST]
    before={str(p.relative_to(LIVE)):sha(p.read_bytes()) for p in selected}
    out={'rol':'PRUEBAS_FICTICIAS_INDEPENDIENTES_NO_REVISION_CIENTIFICA',
      'revisor':'/root/revision_residuales/candidatos_editoriales',
      'utc_inicio':datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
      'huellas_antes':before,'casos':[]}
    with tempfile.TemporaryDirectory(prefix='revision-celda-explicita-') as directory:
        f=Fixture(Path(directory))
        def case(name,setup=None, key='C-2606', wrapper=None):
            f.reset()
            if setup:setup()
            history={str(p.name):sha(p.read_bytes()) for p in f.paths['TARGET_FILES']}
            try:
                if wrapper:
                    with wrapper():result=f.run(key)
                else:result=f.run(key)
                obs={'resultado':'ACEPTADO','salida':result}
            except Exception as error:obs={'resultado':'RECHAZADO','clase':type(error).__name__,'error':str(error)}
            obs.update(caso=name,historia_objetivos_intacta=history=={str(p.name):sha(p.read_bytes()) for p in f.paths['TARGET_FILES']})
            out['casos'].append(obs)
        case('correccion_explicita_generica',lambda:f.correction('C-2606','nuevo [C-032]'))
        case('rango_ascendente_incluye_interiores',lambda:f.correction('C-2606','nuevo [C-029–C-032; C-032]'))
        case('BN_local_conservada_fila_excluida',lambda:f.correction('C-2606','nuevo [C-032]; límite [BN-010]'))
        case('correccion_sin_C_conserva_candidatos',lambda:f.correction('C-2606','nuevo sin referencia'))
        case('objetivo_no_corregido_conserva_candidatos')
        for key in ['C-2009','C-2029','C-2472','C-2489']:
            case('rama_directa_'+key,lambda key=key:f.correction(key,'NUEVO FICTICIO [C-032]'),key)
        for label,value in [('autocita','nuevo [C-2606]'),('autocita_en_rango','nuevo [C-2605–C-2607]'),
          ('rango_inverso','nuevo [C-032–C-029]'),('rango_inverso_mixto','nuevo [C-032–C-029; C-033]'),
          ('dependencia_ausente','nuevo [C-999]')]:
            case(label,lambda value=value:f.correction('C-2606',value))
        def invalid_correction(field,value):
            f.correction('C-2606','nuevo [C-032]');f.corrected['C-2606'][field]=value
            csvfile(f.paths['CORRECTIONS'],atomic.CORRECTION_HEADER,list(f.corrected.values()))
        case('hash_previo_invalido',lambda:invalid_correction('contenido_previo_sha256','0'*64))
        case('evidencia_autoral_vacia',lambda:invalid_correction('evidencia_correccion',''))
        case('correccion_huerfana',lambda:invalid_correction('claim_id','C-9999'))
        def residual_without_review():
            f.correction('C-2708','nuevo [C-032]')
            t=next(x for x in f.targets if x['claim_id']=='C-2708')
            r={k:'' for k in rem.RESIDUAL_HEADER};r.update({k:v for k,v in t.items() if k in r})
            r['contenido_anterior']='rechazo FICTICIO';r['contenido_sha256']=atomic._digest(r['contenido_anterior'])
            csvfile(f.residual_path,rem.RESIDUAL_HEADER,[r])
        case('residual_con_C_sin_disposicion',residual_without_review,'C-2708')
        def mutation(which):
            original=atomic._generated_claim;done=False
            def mutate(*args,**kwargs):
                nonlocal done
                result=original(*args,**kwargs)
                if not done:
                    done=True
                    p=f.support_path if which.startswith('support') else f.table_path
                    if which=='support_semantic':
                        data=rows(p.read_bytes())
                        next(x for x in data if x['#']=='C-032')['Fuerza']='desconocida'
                        csvfile(p,atomic.CLAIM_HEADER,data)
                    else:
                        p.write_bytes(p.read_bytes()+b'\n')
                return result
            return patch.object(atomic,'_generated_claim',side_effect=mutate)
        case('mutacion_tabla_durante_build',lambda:f.correction('C-2606','nuevo [C-032]'),wrapper=lambda:mutation('table'))
        case('mutacion_Csoporte_fuera_15_durante_build',lambda:f.correction('C-2606','nuevo [C-032]'),wrapper=lambda:mutation('support'))
        case('mutacion_semantica_Fuerza_C032_fuera_15_durante_build',lambda:f.correction('C-2606','nuevo [C-032]'),wrapper=lambda:mutation('support_semantic'))
        f.reset();f.correction('C-2606','nuevo [C-032]');r1=f.run();r2=f.run()
        out['determinismo_fixture_dos_builds']=r1==r2
    out['huellas_despues']={str(p.relative_to(LIVE)):sha(p.read_bytes()) for p in selected}
    out['canon_historia_codigo_tests_intactos']=out['huellas_despues']==before
    out['utc_fin']=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
