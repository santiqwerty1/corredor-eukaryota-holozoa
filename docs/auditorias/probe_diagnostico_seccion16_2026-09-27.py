#!/usr/bin/env python3
"""Diagnóstico read-only §16: patrones generan candidatos, jamás dictámenes."""
import argparse, collections, csv, hashlib, io, json, pathlib, re
from datetime import datetime, timezone
ROOT=pathlib.Path(__file__).resolve().parents[2]
def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def rowsha(row,header):
 s=io.StringIO(newline="")
 w=csv.DictWriter(s,fieldnames=header,quoting=csv.QUOTE_ALL,lineterminator="\n")
 w.writerow(row)
 return sha_bytes(s.getvalue().encode())
PATTERNS={
 "modalidad":r"\b(sugier\w*|sugiri\w*|apoy\w*|demostr\w*|compatible|consistente|probablemente|posiblemente|podr[ií]a\w*|propus\w*|propon\w*|interpret\w*|hip[oó]tesis)\b",
 "negacion":r"\b(no|sin|carec\w*|ausen\w*|ning[uú]n\w*|nunca|ni)\b",
 "restriccion":r"\b(solo|s[oó]lo|bajo|entre|al menos|en estos|en estas|muestread\w*|analizad\w*|condiciones|excepto)\b",
 "conjuncion":r"\b(y|ni|pero|mientras|adem[aá]s)\b|;",
 "contradiccion":r"\b(refut\w*|rechaz\w*|contrad\w*|cuestion\w*|debilit\w*|reinterpre\w*|contaminaci[oó]n)\b",
}
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--inventory",action="store_true")
 ap.add_argument("--claims",nargs="*")
 args=ap.parse_args()
 rows=[]; files=[]
 for path in sorted((ROOT/"data/afirmaciones").glob("*.csv")):
  files.append({"ruta":str(path.relative_to(ROOT)),"sha256":sha_bytes(path.read_bytes())})
  with path.open(encoding="utf-8-sig",newline="") as f:
   rd=csv.DictReader(f)
   for n,r in enumerate(rd,start=2):
    flags=[k for k,p in PATTERNS.items() if re.search(p,r["Afirmación"],re.I)]
    rows.append({"id":r["#"],"ruta":str(path.relative_to(ROOT)),"fila_csv":n,"sha256_fila_csv":rowsha(r,rd.fieldnames),"fila":r,"candidatos":flags,"contiene_marca_comillas":any(c in " ".join(r.values()) for c in ['"',"“","”","«","»"]),"metacelda_literal":r["Predicado"]=="tiene_valor_literal_de_campo*","clave_S_declarada":bool(re.search(r"\bS\d+\b",r["Fuente"]))})
 req=[]
 dispositions={r["id_requisito"]:r for r in csv.DictReader((ROOT/"data/auditoria/requisitos_disposiciones.csv").open())}
 for r in csv.DictReader((ROOT/"docs/auditorias/matriz_requisitos_2026-08-08.csv").open()):
  if r["seccion_prompt"]=="16":
   d=dispositions[r["id_requisito"]]
   req.append({k:r[k] for k in ["id_requisito","ancla","requisito_literal","estado_final"]}|{k:d[k] for k in ["tipo","estado_disposicion","control_o_rollup","artefacto_control"]})
 summary={"utc_observacion":datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),"advertencia":"Patrones son candidatos, no fallos ni revisiones; comillas no prueban idioma/original ni correspondencia; negación editorial no es ausencia biológica.","total_C":len(rows),"archivos_C":files,"atribucion":dict(collections.Counter(r["fila"]["Atribución"].split("(")[0] for r in rows)),"aceptacion":dict(collections.Counter(r["fila"]["Aceptación"] for r in rows)),"cuestionado_por":[{k:r[k] for k in ["id","ruta","fila_csv","sha256_fila_csv"]} for r in rows if r["fila"]["Predicado"]=="cuestionado_por"],"candidatos":{},"requisitos":req,"contratos_ausentes":[p for p in ["data/auditoria/censo_semantico_afirmaciones_v1.csv","data/auditoria/segunda_revision_afirmaciones_v1.csv","docs/auditorias/revision_manual_requisitos_2026-08-08.csv"] if not (ROOT/p).exists()]}
 for k in PATTERNS:
  selected=[r for r in rows if k in r["candidatos"]]
  summary["candidatos"][k]={"total":len(selected),"metaceldas":sum(r["metacelda_literal"] for r in selected),"con_S_no_metacelda":sum(r["clave_S_declarada"] and not r["metacelda_literal"] for r in selected),"con_S_no_metacelda_sin_marca_comillas":sum(r["clave_S_declarada"] and not r["metacelda_literal"] and not r["contiene_marca_comillas"] for r in selected)}
 if args.inventory:
  summary["inventario_candidatos"]={k:[r["id"] for r in rows if k in r["candidatos"]] for k in PATTERNS}
  summary["reglas_candidatos"]=PATTERNS
  summary["aceptacion_consenso_ids"]=[r["id"] for r in rows if r["fila"]["Aceptación"]=="consenso amplio"]
 elif args.claims:
  summary={"claims":[r for r in rows if r["id"] in args.claims]}
 print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
