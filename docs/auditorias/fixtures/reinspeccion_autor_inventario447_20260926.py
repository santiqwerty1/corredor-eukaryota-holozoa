"""Reejecución de autor para inventario 447; no adjudica revisiones.

Adaptación por /root del programa independiente de inventario 442,
SHA original 2ce262be2fcdde90fe75073e96d2443f78f9a73ceff290c1e6d35757131c37d1.
Solo emite evidencia nueva de ejecución real; no reescribe dictámenes anteriores.
Conserva la ruta absoluta del experimento: no es un verificador aislado general.
"""
from __future__ import annotations
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/santi/code/corredor-eukaryota-holozoa')
sys.path.insert(0, str(ROOT))
from scripts import remediate_trace_residuals as m

EXPECTED_SCRIPT='91b70d4fa98036b2ebac634c822e133cb4ed9780393b3446f9a0004b0a5c67a3'
EXPECTED_CENSUS='8a33be0a189a42fe8a6c4b14ae5e36aa8df9da89aa312c045c6fd99de3c3f355'
EXPECTED_SOURCES='eb65a6efc4b262af7edb4488ea907c29f7dba2c4e4f61fd76472b653aa547f93'
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def fingerprint(row):
    return hashlib.sha256((json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
def utc():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

assert sha(ROOT/'scripts/remediate_trace_residuals.py')==EXPECTED_SCRIPT
assert sha(m.RESIDUALS)==EXPECTED_CENSUS
_,residuals=m.read_csv(m.RESIDUALS)
assert len(residuals)==410
bn_records={}
bn_file_hashes={}
for path in sorted((ROOT/'data/busquedas_negativas').glob('*.csv')):
    bn_file_hashes[path]=sha(path)
    _,rows=m.read_csv(path)
    for row in rows:
        assert row['clave'] not in bn_records
        bn_records[row['clave']]=(path,row)
old_evidence=ROOT/'docs/auditorias/evidencia_reinspeccion_bn_v3_2026-09-26.csv'
assert sha(old_evidence)=='980c5c51189f44f5bbb694006d9ecea6a6df919ce78e473a202fde9207f082b1'
integration_path=ROOT/'docs/auditorias/integracion_s434_s560_2026-09-26.json'
assert sha(integration_path)=='807aa4e8cf6e01a620243f159585c2a1c554e53e1cc2a3460c520012a675f215'
integration=json.loads(integration_path.read_text())
assert len(integration['archivos'])==5
assert all(sha(ROOT/r['ruta_local'])==r['sha256'] for r in integration['archivos'])
assert (len(bn_records),sum('NO LOCALIZADO EN ESTA SESIÓN' in r.values() for _,r in bn_records.values()),sum('LA LITERATURA DECLARA QUE NO SE SABE' in r.values() for _,r in bn_records.values()))==(497,485,12)
previous_442=ROOT/'docs/auditorias/evidencia_reinspeccion_bn_v3_2026-09-26_inventario442.csv'
assert sha(previous_442)=='e9c1e5370a9f1a3e6450929d1ef212a01ff9deca29c80ebcbb290266af6f1036'
started=utc()
print(json.dumps({'started':started,'mode':'author differential literal + cache; not independent review','inventory_expected':447}),flush=True)
texts,inventory,count=m.source_snapshot()
assert inventory==EXPECTED_SOURCES and count==447
index=m.ExactCooccurrenceIndex(texts)
output=[]
positives=[]
for offset,residual in enumerate(residuals):
    query=m.nominal_query(residual)
    components=m.nominal_components(query)
    assert len(components)==3
    literal_hits=sum(all(component in text for component in components) for text in texts)
    hits=index.count(components)
    assert hits==literal_hits, (residual['claim_id'],literal_hits,hits)
    if (offset+1)%50==0:
        print(json.dumps({'completed_queries':offset+1,'observed_utc':utc()}),flush=True)
    observed=utc()
    if residual['claim_id'] in m.POSITIVE_CLAIMS:
        assert hits>0
        positives.append((residual['claim_id'],hits))
        continue
    bn=f'BN-{147+offset:03d}'
    assert hits==0
    path,record=bn_records[bn]
    literal=' '.join(record.values())
    assert query in literal and inventory in literal and '(447 artefactos)' in literal
    assert m.GENERATED_MARKER in literal
    output.append({
        'clave_bn':bn,
        'huella_fila_bn_sha256':fingerprint(record),
        'clase_fecha':'REINSPECCION',
        'fecha_ejecucion':observed,
        'revisor_ejecutor':'/root (autor; no revisión independiente)',
        'claim_id_residual':residual['claim_id'],
        'csv_bn':str(path.relative_to(ROOT)),
        'csv_celda':residual['csv_path'],
        'fila_celda':residual['fila'],
        'columna_celda':residual['columna'],
        'consulta_exacta':query,
        'coincidencias_artefactos':str(hits),
        'artefactos_censados':str(count),
        'huella_inventario_fuentes_sha256':inventory,
        'huella_censo_residual_sha256':EXPECTED_CENSUS,
        'huella_script_consulta_sha256':EXPECTED_SCRIPT,
        'metodo':'Comprobación por el autor de sum(all(component in text for component in componentes) for text in textos) con ExactCooccurrenceIndex.count; componentes de nominal_query y corpus de source_snapshot. Coinciden ambos; resultado literal, no ausencia científica ni adjudicación de revisión.',
    })
assert len(output)==408 and len({row['clave_bn'] for row in output})==408
assert not {'BN-557','BN-558'} & {row['clave_bn'] for row in output}
assert {key for key,_ in positives}==m.POSITIVE_CLAIMS
assert sha(ROOT/'scripts/remediate_trace_residuals.py')==EXPECTED_SCRIPT
assert sha(m.RESIDUALS)==EXPECTED_CENSUS
assert all(sha(path)==value for path,value in bn_file_hashes.items())
# Verify that source bytes stayed unchanged after the full differential run.
records=[]
for path in sorted((ROOT/'fuentes').iterdir()):
    if path.is_file():
        digest=hashlib.sha256()
        length=0
        with path.open('rb') as stream:
            for chunk in iter(lambda:stream.read(1024*1024),b''):
                digest.update(chunk)
                length+=len(chunk)
        records.append((path.name,digest.hexdigest(),str(length)))
assert len(records)==447
assert hashlib.sha256(('\n'.join('\0'.join(row) for row in records)+'\n').encode()).hexdigest()==inventory
assert sha(old_evidence)=='980c5c51189f44f5bbb694006d9ecea6a6df919ce78e473a202fde9207f082b1'
assert sha(previous_442)=='e9c1e5370a9f1a3e6450929d1ef212a01ff9deca29c80ebcbb290266af6f1036'
destination=ROOT/'docs/auditorias/evidencia_reinspeccion_autor_bn_v3_2026-09-26_inventario447.csv'
assert not destination.exists(), 'No sobrescribir evidencia anterior'
with destination.open('w',encoding='utf-8',newline='') as handle:
    writer=csv.DictWriter(handle,fieldnames=list(output[0]),quoting=csv.QUOTE_ALL,lineterminator='\n')
    writer.writeheader()
    writer.writerows(output)
print(json.dumps({'artifact':str(destination.relative_to(ROOT)),'sha256':sha(destination),'rows':len(output),'positive_results':positives,'started':started,'finished':utc(),'first_execution':output[0]['fecha_ejecucion'],'last_execution':output[-1]['fecha_ejecucion']},ensure_ascii=False),flush=True)
