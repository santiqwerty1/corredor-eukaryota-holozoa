# Revisión independiente nominal de ocho BN y de C-1163/E98

Revisor: `/root/revision_residuales/candidatos_editoriales`.
Estado: revisión científica abierta; no firma de censo ni cierre de requisitos.
Rama observada: `codex/cierre-plan-pendiente`.

## Evidencia de ejecución e integridad

La reinspección independiente preservada en
`evidencia_revision_independiente_8bn_integracion_2026-09-26.json`
comenzó el 2026-09-26T22:54:32Z y terminó el 2026-09-26T22:54:36Z.
SHA-256: `bf0701492203d7ca2c4731c6a728f059867c2ac4afeb2408faad2e27421b3f7e`.
El CSV `revision_independiente_8bn_integracion_2026-09-26.csv` separa los
dictámenes de reproducción, cobertura y resultado científico por clave.

Se inspeccionaron los logs originales del ejecutor root, sin modificarlos:

- `evidencia_local_bn_integracion_2026-09-26.json`, SHA-256
  `601474f82434f243c005c69fba147025a0dc7e6f653520b8f69be8eb7a118694`.
- `evidencia_web_bn_integracion_2026-09-26.json`, SHA-256
  `8e0ec02cf32e603ab287e44f9adf1dc81738c6dd439a9ece2a12acf2e7037cd9`.

Las diez consultas locales reprodujeron sus códigos de salida, stderr y
multiconjuntos completos de líneas. El orden de salida de rg puede variar.
Coincidieron las filas vivas de las ocho BN, ambas fórmulas de huella
(la anterior no canónica conservada y la canónica corregida), las salidas
originales de `/tmp/bn-integracion-20260926-ft3hgv9a/` y los 447 archivos
distintos de entrada. Los 441 archivos de fuentes visibles para rg coinciden
con el inventario del log; `fuentes/.resolucion.json` queda excluido.

Esto prueba consistencia y reproducción en esta reinspección. No certifica
independientemente el instante original, la lectura íntegra de cada fuente,
exhaustividad bibliográfica ni apoyo científico. Los cuatro términos web
coinciden con las filas congeladas y conservan 26, 35, 26 y 14 resultados
de metadatos; no se reejecutaron aquí como supuesto testigo retrospectivo.

## Hallazgos nominales

| Clave | Ejecución observada | Límite o defecto |
|---|---|---|
| BN-132 | argv corregido; 127 líneas; exit 0 | No se ejecutó literalmente la cadena inválida. rg no extrae S282 PDF. C-1163 convierte falta de recuento localizado en imposibilidad universal. |
| BN-133 | argv corregido; 7 líneas; exit 2 | `fuentes/S291*` ausente. No acredita lectura de S291 ni ausencia de cifras rivales. |
| BN-134 | argv corregido; 11354 líneas; exit 0 | Patrón `Ma` poco discriminante; no adjudica todos los casos ni documenta método homogéneo. |
| BN-135 | 52 líneas; exit 2 | S213 y S445 ausentes; no se verifican los tres artículos declarados. |
| BN-140 | 731 líneas; exit 0 | Coincidencias no equivalen a revisión completa familia por linaje. |
| BN-142 | 286 líneas; exit 0 | No determina introducción histórica de cada término. |
| BN-144 | Dos consultas: 4 y 2 líneas; exit 0 | El propio registro no es prueba primaria del par genes perdidos y tiempo. |
| BN-146 | Dos consultas: 1 y 23 líneas; exit 0 | La primera recupera solo muestreo, no el filtro que declara la fila. |

En S290 XML el texto contiene `≥70\u00a0%`: entre 70 y % hay NBSP,
no el espacio ASCII del patrón. La única línea de la primera consulta
es el muestreo de 30.358 secuencias, 1.035.375 homólogos y 2.585 árboles.
No es una frecuencia sustantiva de HGT. Tampoco convierte la cifra histórica
del tardígrado, posteriormente cuestionada, en evidencia vigente general.

## C-1163, BN-132 y E98: propuesta, no implementación

S282 se inspeccionó en el PDF local
`fuentes/S282 [2004] Endosymbiotic gene transfer organelle genomes forge eukaryotic chromos.pdf`,
SHA-256 `249c74e98b6c3c7679439db0b1093033a9a33a29e863faf8ed4b57b3aea0107e`.
La extracción independiente `/tmp/S282-revision-independiente-20260926.txt`
coincide con `/tmp/S282-cierre-20260926.txt`, SHA-256
`4938dd635d08010e65da7162f1e6e1937668da9ea9f3406fdf75caf6d800d656`.

- P.127, apartado `Ancient transfers that are shown by genome comparisons`:
  aparece 630, referido al trabajo 65. No es apoyo para la universal actual.
- Pp.132–133, `Endosymbiotic gene transfer: bigger questions`: se comparan
  atribuciones mitocondriales y LGT, con límites de muestreo y filogenias.
- P.133, último párrafo de ese apartado: los autores proponen transferencias
  tempranas antes de importación, y reducción organelar después de evolucionar
  importación. E98 no debe decir que tal orden no consta en esta fuente;
  debe atribuirlo como escenario de los autores, no cronología consensuada.

Propuesta: retirar de C-1163 la atribución expresa de imposibilidad universal;
usar una glosa limitada al resultado de BN-132 o proposiciones nuevas con
primaria directa. BN-132 debe reconocer resultados parciales y distinguirlos
del total de transferencias, sin transformar `NO LOCALIZADO` en inexistencia.
R-0209/MREQ-0033 no queda resuelto por ese cambio documental.

La primaria de Gabaldón y Huynen (2003), DOI `10.1126/science.1085463`,
Science 301:609, se leyó en la copia pública subida por el autor:
https://www.researchgate.net/publication/10633111_Reconstruction_of_the_Proto-Mitochondrial_Metabolism
No hay PDF descargado por este revisor: su descarga devolvió 403.
El resultado son 630 grupos ortólogos reconstruidos y una estimación mínima
del proteoma; no son 630 transferencias nucleares ancestrales.
La continuación de 2005, DOI `10.1093/bioinformatics/bti1124`, p.ii144,
explicita que el conjunto incluye codificación nuclear y mitocondrial.
Se consultó el pasaje indexado del PDF editorial y el resumen editorial;
no se afirma haber descargado y revisado íntegramente ese PDF.

C-1961/S281 cuantifica reducción del repertorio desde miles de genes
codificantes a por lo menos 69 proteínas reconstruidas en LECA. No se debe
interpretar su diferencia como número transferido al núcleo, ni atribuir
al núcleo la recepción de toda pérdida genómica en E98.

## Filtros añadidos frente al encargo

El literal de R-0200 pide antigüedad estimada de cada asociación y tamaño
del genoma del simbionte comparado con parientes de vida libre. No exige
un método homogéneo común a todos los casos. BN-134 sí lo añade a su hueco.
Retirar ese filtro conserva el alcance: registrar cada cifra con método,
organismo, unidad y comparando; no calcular una razón no publicada.

R-0220 pide las posiciones de barrera de HGT y contraria, con las cifras
de cada una y el método de atribución. No exige idéntico denominador.
BN-133 exige el de S290, y BN-146 exige mismo objeto y denominador para el
par. La falta de comparabilidad debe explicarse, no descartar valores
publicados ni sustituirlos por una tasa común inventada. Se mantiene separada
la evidencia de muestreo, el umbral de identidad, el número de candidatos,
la fracción del repertorio analizado y la contaminación detectada.

La búsqueda de primarias y valores parciales está abierta. No se asignan
nuevas claves C/S en esta revisión ni se registra ninguna fecha en los CSV
canónicos de cronología.
