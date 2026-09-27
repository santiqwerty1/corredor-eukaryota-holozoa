# Diagnóstico independiente de §16: candidatos, casos leídos y trabajo pendiente

Fecha UTC: 2026-09-27T02:31:28Z. Rama: codex/cierre-plan-pendiente. Revisor: /root/revision_residuales/candidatos_editoriales.

**Resultado: §16 no está cerrado.** Este expediente diagnostica el corpus vivo; no modifica canon, no firma requisitos, no actualiza huellas de dictámenes históricos y no aprueba el censo completo. La propuesta S240/S352 v1 se revisó en otro expediente: sus filas nuevas no forman parte de las 2838 C de este diagnóstico.

## Alcance completo y cobertura real

Leí íntegro §16 del encargo (líneas 245–283), el handoff, el protocolo de censo semántico integral y el contrato de cronología. Leí también el contrato vigente de disposiciones residuales y las funciones pertinentes de alcance manual, validación de firmas, esquema del censo, procedencia, referencias y densidad narrativa. La ligadura integral de firmas manuales es conservadora: cambiar el entregable invalida la firma; ligar bytes no demuestra haber leído ni entendido el contenido.

El inventario completo de §16 contiene **65 requisitos, R-0333–R-0397**:

- 13 padres/roll-ups, que no se cierran por una declaración independiente de sus hijos.
- 39 controles estructurales con CONTROL_DEFINIDO, pendientes de adjudicación manual sustantiva.
- 13 con CONTROL_VERIFICADO, cuyo alcance automático debe distinguirse del cumplimiento científico del literal.

El CSV inventario_requisitos_seccion16_2026-09-27.csv enumera los 65 literales íntegros, sus estados visibles, familia probatoria, artefactos necesarios y pendiente nominal. No son 65 firmas. Incluye atomicidad, SPO, atribución, localizadores, aceptación, fuerza, resolución/vigencia, contraevidencia, citas originales, topologías/métodos, soporte, densidad y comparación cualitativa: ninguna dimensión se elimina por falta de evidencia.

**Lectura nominal registrada:** 21 filas C completas y dos oraciones/párrafos de prosa adjudicados aparte. Hay 23 entradas: 10 NO_CONFORME (8 C y 2 objetos de prosa), 3 SIN_FALLO_EN_DIMENSION_REVISADA, 1 observación de localizador y 9 PENDIENTE_COTEJO_PRIMARIO. No se llama a las 21 filas una muestra representativa ni se extrapola una tasa de fallos.

Las restantes 2817 C no recibieron aquí lectura nominal completa. De las 21 leídas, nueve se usaron como contexto/dependencia y no se cotejaron primariamente; las otras tampoco equivalen por defecto a revisión científica integral de todos sus componentes. El ámbito global sigue siendo todas las C, toda la narrativa, aristas, tablas y dependencias, con segunda revisión independiente posterior.

## Censo automático de candidatos, no de infracciones

Captura read-only: 2026-09-27T02:25:46Z; 2838 C, 16 archivos canónicos fijados por hash. Distribución: 1776 expresa, 925 sintesis, 137 glosa; 2706 no evaluado y 132 consenso amplio. No hay otra etiqueta de aceptación en este corte.

| Patrón en Afirmación | Candidatos | Metaceldas literales | Con S y no metacelda | Último grupo sin marca de comillas |
| --- | ---: | ---: | ---: | ---: |
| Modalidad | 274 | 19 | 246 | 238 |
| Negación | 1217 | 651 | 461 | 433 |
| Restricción | 296 | 26 | 252 | 243 |
| Conjunción/lista | 1689 | 530 | 1066 | 1014 |
| Rechazo/contraevidencia | 39 | 1 | 37 | 35 |

Las categorías se solapan y no se suman. Comillas no demuestran idioma original, autenticidad ni pertinencia. Ausencia de comillas no demuestra que una glosa editorial necesite una cita inglesa. Una conjunción puede integrar una única prueba condicional. El patrón tampoco es exhaustivo: C-1040, con una elevación modal observada al cotejar S240, no coincide con nuestro patrón de modalidad.

candidatos_diagnostico_seccion16_2026-09-27.json conserva IDs por categoría, reglas exactas, hashes de los 16 archivos y los 65 requisitos. probe_diagnostico_seccion16_2026-09-27.py reproduce el inventario sin escribir canon ni emitir decisiones. El número 433 significa candidatos sin marca, **no 433 incumplimientos adjudicados**.

## Casos con hallazgo nominal

### Atomicidad y atribución: C-1664

data/afirmaciones/13.csv, fila CSV49; SHA de fila 1ed0e3adbf89c0dcf45441964a87b7067bafaa23a585c44f5f0468f121cd51cb.

Reúne al menos 223 orígenes de parasitismo/15 filos, al menos 16 orígenes de simbiosis/89 familias y un resultado negativo de frecuencia pan-eucariota. Son resultados separables con denominadores diferentes. Declara sintesis(C-1121), pero C-1121 trata el correlato de vitaminas B, no contiene ninguno de esos dos recuentos.

Leí S513, Evolutionary origins of obligate symbiosis, p1: respalda el resultado de insectos y explicita límites de resolución a nivel familiar. No se recuperó aquí texto local S517 ni se adjudica falsa la cifra 223. La reparación requiere C atómicas de cada resultado y una glosa de búsqueda distinta; una fuente citada adicional no sustituye la dependencia C que la síntesis exige.

### Modalidad: C-1040

data/afirmaciones/09.csv, fila CSV70. S240 Par16 separa observaciones de invaginaciones/vesículas, interpretación sugerida de endocitosis y especulación sobre captación. La fila viva afirma captación mostrada y usa depreda_a. El contexto no demuestra retorno dirigido de productos de genes EGT. Es un fallo de modalidad/descomposición, no de disponibilidad del artículo. La reparación autoral S240/S352 continúa por su circuito separado.

### Cita original: C-1196 y C-1121

C-1196: data/afirmaciones/09.csv, fila CSV226. La negativa sobre HGT extensa está respaldada por el HTML PNAS final S296 y el vínculo cuestionado_por → C-1195 existe. Falta dentro de la fila el fragmento original negativo exigido por R-0380/R-0383/R-0384.

**Autocorrección del alcance de mi revisión:** mi dictamen científico previo de C-1196 omitió esta exigencia de §16. Este es un hallazgo nuevo sobre la misma formulación, no una falsedad añadida por el autor ni una excusa para reescribir el dictamen anterior. Se preservan ambos expedientes. La propuesta posterior de reparación no se aprueba desde este diagnóstico.

C-1121: mismo CSV, fila151. S513, Nutrient deficiencies and obligate symbiosis p2, restringe el resultado al único componente dietario correlacionado entre nichos. La fila no conserva el fragmento original de esa restricción entre comillas. El hallazgo no convierte correlación en causalidad ni supone haber revisado aquí todos sus tamaños muestrales.

### Negación compuesta y contexto: C-1581

data/afirmaciones/12.csv, fila101. Junta dos organismos y receptores/ligandos. Cita un epígrafe Signalling pathways que no existe en el JATS S352 leído; el pasaje real está en Gene repertoire of Capsaspora p4. La lectura independiente de Fig.4 y, después, Supplementary Note5 pp95–96 obliga a distinguir componentes/dominos de Monosiga frente a ausencia de sistema canónico funcional. La cita inglesa ya presente no elimina atomicidad ni tensión contextual. No se adjudica función de un receptor por el color de un homólogo en una figura.

### BN convertida en afirmación más fuerte: C-1642

data/afirmaciones/13.csv, fila27; fuente única BN-111. BN-111 declara NO LOCALIZADO EN ESTA SESIÓN y anclas parciales no comparables. La C dice No existe una cronología y usa carece_de_cronología_comparable. Restringir los sistemas a los documentados en el corpus no demuestra que la búsqueda haya sido exhaustiva ni que tal cronología no exista. Su Motivo añade una generalización sobre las fuentes sin pasaje propio.

Debe registrar el resultado limitado de BN-111, conservando las anclas parciales. No se propone inventar cifras, una ordenación universal ni una fuente que declare inexistencia.

### Contraevidencia sin la relación exigida: C-426 y C-477

Se censaron las **32** filas con predicado cuestionado_por: todas contienen enlace a una C en sujeto/afirmación/objeto. Eso es un resultado referencial completo de esas 32 filas, no prueba de que estén todas las contraevidencias.

C-426 (03.csv:fila255) declara sensibilidad de C-202/C-208 y su Motivo llama cuestionadas a esas reconstrucciones, pero no existe fila cuestionado_por cuyo objetivo sea C-202 o C-208. C-477 (04.csv:fila48) declara límites de C-475/C-476 y los llama cuestionados, sin esa relación explícita a ninguno. Sus predicados posee_sensibilidad/posee_limitacion y referencias C no cumplen por sí solos R-0377/R-0379.

Este diagnóstico verifica la omisión respecto de la contraevidencia que el propio canon declara; no pretende haber corroborado científicamente todos esos límites en S56/S58/S120/S123. Deben conservarse las posiciones y cotejarse los pasajes al añadir las relaciones nominales, sin rebajar ni borrar la tesis criticada.

### Prosa más amplia o con cita en otra oración

docs/secciones/004-03-3-eucariogenesis.md:428 dice que no se ha observado un virus convertido en núcleo sin reproducir el límite a los casos examinados de C-338. La referencia C no conserva automáticamente alcance. La glosa n/a y claves S tampoco aportan por sí solas apartado recuperable.

docs/secciones/014-13-13-escalas-tasas-y-recuentos.md:165: la primera oración cuantitativa de C-1664 termina solo con [C-1664]; los S/localizadores están en la oración siguiente. El mandato es por oración. R-0393 aparece verificado automáticamente mediante trazabilidad/referencias; el contraejemplo muestra que esa puerta no prueba el literal completo. No se modificó ni debilitó el validador.

## Controles contra falsos positivos

C-1955 describe el alcance editorial de tabla34: leí sus 17 identidades nodales; acaba en Metazoa sin nodos descendientes. No requiere inventar una frase inglesa ni una fuente científica que certifique una decisión de composición.

C-1965 describe el censo propio de procedencia y declara expresamente que no certifica apoyo semántico. Leí el constructor pertinente y corrí la comprobación read-only: exit0, PROCEDENCIA VERIFICABLE:2838 afirmaciones. Ese resultado no se promueve a revisión de pasajes.

C-2435/tabla40a:fila25:estado de genoma coinciden en una declaración literal de hueco BN-296, no en ausencia del genoma de Entamoeba. No se exige una fuente inglesa para el resultado propio de búsqueda. Resolución=resuelta se refiere al objeto metacelda, no a una cuestión biológica. Este diagnóstico no vuelve a certificar fechas o ejecución original de BN-296.

C-031 combina AU0.036, modelo y rechazo en una prueba condicional: no se divide mecánicamente por contener varios datos. La cita original aparece en S10. Su ordinal párrafo3 no coincide con p5 del apartado correspondiente del JATS local: debe precisarse la versión/localizador, sin declarar falso el resultado ni convertir AU en porcentaje de confianza.

## Evidencia preservada y pendientes

- evidencia_diagnostico_seccion16_2026-09-27.json conserva las 21 filas leídas, sus rutas/números/hashes, siete pasajes con localizador/huella/fragmento, tres BN, seis capturas de prosa y hashes de contratos/código/artefactos.
- dictamenes_diagnostico_seccion16_2026-09-27.csv fija los 23 objetos y UTC real. Son dictámenes diagnósticos por dimensión, nunca firmas de conformidad global.
- inventario_requisitos_seccion16_2026-09-27.csv cubre todos los literales, incluidos los aún no adjudicados.
- candidatos_diagnostico_seccion16_2026-09-27.json y probe_diagnostico_seccion16_2026-09-27.py permiten reproducir selección sin etiquetado científico automático.

Persisten ausentes data/auditoria/censo_semantico_afirmaciones_v1.csv, data/auditoria/segunda_revision_afirmaciones_v1.csv y docs/auditorias/revision_manual_requisitos_2026-08-08.csv. Una colección de revisiones de lotes no los sustituye.

Pendiente global: adjudicar las 132 etiquetas consenso amplio con evidencia sustantiva; resolver literal fuente/tesis y restricciones caso por caso; cotejar todos los componentes de expresas, glosas científicas y síntesis; completar contraevidencias y conservación histórica; revisar métodos/topologías/soportes y cada oración científica. No se deduce que las 132 etiquetas sean falsas ni se exige inventar disidentes cuando el encargo no los exige para consenso amplio.

La priorización siguiente debe partir de los NC nominales y fuentes accesibles, pero mantener un inventario exhaustivo hasta cubrir el resto. Los BN-134/135/140/142 siguen fuera de este sublote para no duplicar su investigación. Cualquier cambio de fila o fuente exige lectura de la versión nueva, no recalcular huellas para heredar dictámenes.

