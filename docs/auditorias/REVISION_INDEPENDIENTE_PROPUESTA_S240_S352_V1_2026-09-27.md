# Revisión independiente de propuesta S240/S352 v1

Dictamen del paquete: **NO_CONFORME**. No autoriza integrar la propuesta, disponer las seis celdas, retirar búsquedas históricas, firmar controles manuales ni cerrar el plan.

Revisor: /root/revision_residuales/candidatos_editoriales. Rama comprobada: codex/cierre-plan-pendiente. Informe emitido: 2026-09-27T02:17:01Z. Dictámenes nominales fijados: 2026-09-27T02:15:10Z.

## Identidad, independencia y trazabilidad

No redacté ni implementé las C/F/B/celdas/prosa propuestas. Leí las primarias locales y sus contextos, incluida inspección visual propia de Fig. 4; no utilicé tests del autor como revisión científica. Las observaciones del integrador se comprobaron contra el mandato y las fuentes antes de incorporarlas. No se modificaron canon, propuesta, código ni ledger de firmas.

Objeto final: docs/auditorias/PROPUESTA_AUTOR_6_CELDAS_S240_S352_2026-09-27.json, SHA256 **20bc4ed7cd09c556044b8f5f99c93337b8a5519d66420b2b8f84ab62165065ca**. Reconfirmado durante la emisión.

La lectura comenzó a las 01:58:41Z, cuando el autor aún preparaba metadatos. El borrador visto tenía SHA256 3fc812472be6573c6fe372e65abe932b859491a8cf31544e9db7fa9edef21b1d. No guardé entonces sus bytes; el autor recuperó después su snapshot exacto en PROPUESTA_AUTOR_6_CELDAS_S240_S352_BORRADOR_2026-09-27.json. No se presenta esa recuperación como captura independiente anterior.

A las 02:03:50.489734Z comprobé ambos hashes y la igualdad profunda de C_altas, C_correcciones, celdas, F_altas, F_correcciones y B_altas. La versión final añade metadatos, huellas y prosa; la prosa añadida se revisó por separado. Los dictámenes de este informe son sobre la versión final, no una fecha retrospectiva del borrador.

Artefactos propios:

- evidencia_revision_independiente_propuesta_s240_s352_v1_2026-09-27.json, capturada 02:07:50.475550Z, SHA256 a6fee5895bd00c1b8b98f7c03ee566ce7b402e74fdfd2b9bbe2ca7fba5babd60: identidad de fuentes, comprobación independiente de seis pasajes, contextos, Fig. 4 y 39 objetos exactos.
- dictamenes_independientes_propuesta_s240_s352_v1_2026-09-27.csv: 39 objetos de contenido más paquete y destinos. 13 CONFORME limitados (3 F y 10 B), 28 NO_CONFORME. Toda fila lleva hash, UTC y habilita_integracion=NO/habilita_cierre_global=NO. No se debe heredar ninguna conformidad a una versión nueva.
- Los hashes de fila siguen la normalización declarada en el expediente de evidencia; los de texto son UTF-8 con LF final. El hash del paquete liga también las rutas y metadatos no contenidos en la fila.

## Lectura primaria efectivamente realizada

S240: XML local f48e9fa6e660c47322028ce349c68cc77429c9a45e18269023ab033a00068ad7; PDF local 91ea1ace12663e38718521f7688f1fa625448b93f4621295f739560bb1170561. Leí Abstract; secciones de Results and Discussion Sec3–Sec6; métodos Sec9, Sec11, Sec14–Sec16, y parte de Sec12; Table 1 y leyendas Fig. 1/Fig. 4. No afirmo haber leído íntegro todo el suplemento de S240 ni la parte truncada de Sec12. Los pasajes Par7/10/14/16 y Table1 se reextrajeron del XML: texto y hashes coinciden con la propuesta.

S352: XML local 7c62b5db6668fc64d252e5e0621fbb0831be592eda21d90895594c6eb8e23f6c; PDF local 4aa789fa55f7df7872eca7df96b7536408ceb5e4a4af315eb1cf98bb158f857d. Leí The genome of Capsaspora, los cinco párrafos de Gene repertoire of Capsaspora, Discussion y métodos Gene family analysis, Genome sequencing and assembly y Gene prediction. El localizador real del párrafo discutido es Results → Gene repertoire of Capsaspora, cuarto párrafo; no un epígrafe inventado de Signalling pathways.

Inspeccioné visualmente Fig. 4 en la página 6 del PDF, render propio /tmp/S352-fig4-review-20260927.png, SHA256 b7d12beb90dbd75c95c57cb26240c7678129e26c305c21485beafe12384281ab. Reproducción: pdftoppm -f 6 -singlefile -scale-to 1700 -png [PDF S352] [salida]. La extracción textual no sustituye la lectura de colores/trazos de esa figura.

Lectura adicional posterior: el autor recuperó un suplemento editorial que mi intento inicial no había conseguido. Extraje independientemente las páginas 94–96 desde /tmp/S352-supplement-preparacion-v2-20260927.pdf, SHA256 d0f556e6436a6bb67ac99f65f645fbd0995491e27ebce0eaef9585050c388c23, a /tmp/S352-supl94-96-revision-independiente-v1-20260927.txt y las leí antes del dictamen 02:15:10Z. Es una lectura posterior al JSON 02:07:50Z, no incluida retrospectivamente en él. URL editorial comunicada por el recuperador: https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fncomms3325/MediaObjects/41467_2013_BFncomms3325_MOESM833_ESM.pdf. No he integrado ese archivo en fuentes/ ni leído todo el suplemento; tampoco pretendo una inspección propia de Fig. S26.

La consulta auxiliar de Jackson et al. 2016 (DOI 10.1016/j.cub.2015.11.055, https://pmc.ncbi.nlm.nih.gov/articles/PMC4728078/) accedió por resultado de búsqueda a Results/Table1 tras bloqueo recaptcha de la apertura. Identifica 39.9 Mb y ensamblaje en 2402 scaffolds, pero no es lectura íntegra ni alta canónica de esa fuente. No se necesita esta consulta para confirmar el valor de Table1 de S240; sí impide justificar modalidad científica por el simple hecho de observar la tabla.

## Hallazgos nominales

### S1. Texto y Fig. 4 de S352 no permiten ausencia indiferenciada en Monosiga

Afecta C-2842, C-1581, C-2468 y prosa C-1581. El párrafo general atribuye a ambos organismos la falta de receptores y ligandos de varios sistemas. Pero la leyenda codifica en gris componentes presentes en Monosiga, y Fig. 4 muestra Patched/Dispatched grises, además de Hedge y Hog separados. Smoothened/Gli se muestran blancos discontinuos. La figura no demuestra una vía Hedgehog funcional ni convierte un homólogo de Patched en receptor funcional probado; sí impide omitir esos componentes al convertir la generalización narrativa en ausencia genómica indistinta.

Supplementary Note5 pp95–96 distingue explícitamente la carencia en Capsaspora de ligando Hh, Dispatched, Patched y Smoothened; para Monosiga describe las partes Hedge/Hog en dos proteínas. Por tanto no atribuyo a Capsaspora la misma tensión que a Monosiga.

La reparación debe conservar la declaración textual atribuida, separar los hallazgos de dominios/componentes y registrar la contraevidencia con una fila cuestionado_por explícita conforme a §16. No borrar ni suavizar silenciosamente la posición que se conserva. La modalidad funcional y la antigüedad evolutiva no pueden inferirse de la mera presencia de componentes.

### A1. Negaciones científicas compuestas

C-2842–C-2845 unen receptores y ligandos, dos objetos cuya presencia o ausencia puede diferir. C-1581 además une los dos organismos. Incumplen la prueba explícita de atomicidad de docs/C01-PROMPT-INVESTIGACION.md:254; un rótulo sintesis no exime de ella.

La restricción a Rhodopsin en C-2844/C-2845 es científicamente importante y está respaldada por el párrafo y Supplementary Note5 p94. No es ausencia de todos los GPCR: ese suplemento describe seis de ocho familias 7TM en Capsaspora. No se aprueba en este informe ningún nuevo recuento/familia positiva propuesto después de v1.

### Q1. Fragmento original obligatorio ausente en filas epistémicas

El mandato de §16, línea 276, pide el fragmento original entre comillas y localizador dentro de las filas con formulaciones epistémicas, negaciones o restricciones de alcance. No basta que el autor copie el párrafo completo en su JSON de auditoría.

- C-1037 transcribe correctamente una estimación nuclear ~9.5 Mbp, pero debe conservar el fragmento modal original, no solo el token estimated sin comillas. S240 Par7: “was estimated to be”.
- C-1040 mejora la antigua afirmación de captación directa: interpretación morfológica apoyada por datos genómicos. Debe citar “These observations suggest”, Par16.
- C-2840 conserva 8 candidatos entre 3846 alineamientos; falta “likely derived from the endosymbiont”, Par14.
- C-2841 distingue hipótesis de importación demostrada; falta “we speculate”, Par16.
- C-2842–C-2845 y la síntesis negativa C-1581 carecen del fragmento original de las negaciones y alcance atribuidos.

Estos NO_CONFORME formales no significan que ~9.5, 8 o 3846 sean cifras falsas. Separar soporte científico de cumplimiento evita tanto rechazar evidencia real como aprobar filas incompletas.

### M1. Modalidad científica no es observación de una tabla

C-2839 y F_altas/0: el valor 39.9 Mbp y Bodo como comparando de vida libre están respaldados por S240 Table1/Par10, que remiten a ref25. No hay cociente fabricado ni identificación de Bodo como ancestro directo.

Sin embargo, el predicado tiene_valor_medido y el campo F observado necesitan justificación sobre la magnitud y su método. La mera transcripción de un valor publicado no decide observado/inferido; una estimación también puede estar impresa. Hay que identificar qué representa el tamaño/longitud del ensamblaje y cómo se obtuvo, y alinear predicado/F. No se exige declararlo necesariamente inferido sin leer el método ni se rechaza 39.9.

Las otras tres filas F son conformes en su objeto limitado: ~9.5 Mbp como estimación, 8 genes candidatos de origen inferido y 3846 como recuento del conjunto de alineamientos interpretables. Genes, alineamientos y eventos de transferencia no son unidades intercambiables.

### D1. Las seis sustituciones dependen de filas rechazadas

C-2708 conserva comparación nuclear acotada; C-2709 conserva candidato EGT e hipótesis vesicular. En C-2709 no se ha identificado una enzima reintroducida como producto de ninguno de los ocho genes candidatos: EGT y captación hipotética no son por sí solos demostración del mecanismo de retorno.

C-2468 hereda S1. C-2469 tiene soporte acotado a Capsaspora, pero hereda A1/Q1. C-2474/C-2475 preservan explícitamente que otros GPCR/señales no se adjudican, pero heredan A1/Q1. Ninguna de las seis disposiciones está aprobada en v1. Las BN históricas conservan su naturaleza de resultados de consultas: encontrar soporte semántico nuevo no transforma retrospectivamente su ejecución.

### I1. Destinos de las altas no compatibles con orden canónico

La propuesta ubica C-2839–C-2841 en data/afirmaciones/09.csv y C-2842–C-2845 en12.csv. Integrarlas allí antecedería a IDs menores de secciones posteriores; scripts/audit_full.py:422–424 exige secuencia C continua y canónica (AF103). Es defecto de integración del paquete, no razón para negar soporte científico. Debe repararse la ubicación, nunca debilitar el validador.

## Alcance exacto y siguiente paso autorizado

Las diez conformidades B solo reconocen identidad, tipo, marca hipotética y referencia de primera aparición dentro del espacio de IDs de esta propuesta. No acreditan que la entidad posea o carezca de una función. Las tres conformidades F no aprueban sus C vinculadas. El CSV adjudica cada objeto exacto, no una familia genérica.

La próxima propuesta debe ser v2 separada, con huellas nuevas; conservar v1 y su rechazo. Revisión posterior explícita sobre v2 y, si procede, sobre el contrato de disposición ligado a sus bytes. No reutilizar estos dictámenes como firmas de producción.

No se ha realizado aquí un censo científico de las 2838 C vivas, diagnóstico completo de todos los controles §16, revisión de los otros BN abiertos ni aprobación de los 210 controles manuales. No se ha corrido make verify para fingir que equivale a revisión científica. Este informe no declara cierre del plan.

