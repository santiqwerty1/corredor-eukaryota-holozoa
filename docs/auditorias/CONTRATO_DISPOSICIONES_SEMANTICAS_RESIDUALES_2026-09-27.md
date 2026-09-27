# Sustituciones prospectivas de celdas residuales

Propuesta e implementación de autor: `/root`, rama
`codex/cierre-plan-pendiente`. Observación UTC: 2026-09-27T01:53:38Z.
**Pendiente de revisión técnica independiente; no es un dictamen científico.**
Al escribir este informe, el registro real está vacío y no se ha sustituido
ninguna de las celdas mediante el mecanismo nuevo.

## Qué se conserva

El censo histórico tiene 410 filas rechazadas. Su búsqueda literal conserva
408 consultas negativas y dos positivos nominales (C-2472/C-2489). La búsqueda
literal no es una revisión semántica: una oración española puede no aparecer
en un artículo inglés que sí contenga un dato pertinente.

No se cambian esas 410 filas, sus resultados, su numeración BN ni las dos C
de `POSITIVE_CLAIMS`. Tampoco se reescriben las evidencias y UTC de ejecuciones
anteriores. Una fuente nueva no vuelve exitosa una consulta histórica que
tuvo cero coincidencias. Si una ejecución futura encuentra una coincidencia
literal en una de las 408 consultas, el remediador sigue fallando; este contrato
no autoriza reclasificarla silenciosamente.

Las 408 BN continúan registrando consultas negativas exactas, no ausencia
biológica ni necesariamente un hueco vigente en la celda. Los recuentos de
consultas activas no son recuentos de campos científicamente sin resolver.
Una sustitución no transforma una BN en soporte positivo; la celda nueva
cita C expresas y primarias por separado. Los objetivos atómicos conservan
el hueco autoral anterior; el rechazo independiente original está conservado
en el censo residual y sus informes, no se declara aprobado retrospectivamente.

## Qué habilita una sustitución

`data/auditoria/correcciones_celdas_semanticas_v1.csv` ya documenta deltas
autorales no residuales. Para una C del censo residual, una fila de corrección
no basta: debe tener además una disposición en
`data/auditoria/disposiciones_residuales_semanticas_v1.json`.

El contrato cerrado exige identidad exacta `(csv_path, fila, columna, C, BN)`,
huella JSON de la fila residual histórica completa, texto y SHA-256 del hueco
previo y del texto nuevo, autor, UTC real, componentes y límites. La fila
corregida se enlaza literalmente con la corrección autoral y su informe.
El campo `limites_pendientes` debe explicar también cuando no hay ningún
componente pendiente dentro de la proposición nueva; no se deja vacío.

Las C de soporte se declaran explícitamente en el texto nuevo y se fijan con
huella de fila completa. En esta versión sólo se admiten C `expresa` con
primarias nominales: no se admite una BN como dato ni una síntesis cuyo grafo
de dependencias no esté fijado. Cada S declarada tiene un artefacto local
PDF/XML/HTML/TXT y viceversa. Se fijan sus bytes; un archivo `.url` no vale.
La identidad nominal y los hashes no sustituyen el cotejo del contenido.

Un revisor distinto del autor produce un JSON separado, ligado al SHA-256 de
la propuesta completa salvo el propio enlace al dictamen. Debe declarar
`REVISION_INDEPENDIENTE_SIN_PARTICIPACION_EN_CORRECCION`, identificar su
revisión y su UTC, y adjudicar `CONFORME` la propuesta exacta. Cada componente
tiene cobertura explícita en pasajes; cada pasaje conserva artefacto, huella,
localizador, fragmento de control de hasta 25 palabras y SHA-256 del pasaje
normalizado. No se generan esos dictámenes desde un conteo ni un test.

El contrato de independencia requiere un revisor realmente ajeno a la
corrección; la desigualdad de dos cadenas no acredita por sí sola identidades
distintas. Del mismo modo, la cobertura JSON no prueba semántica: eso lo
acredita la lectura nominal del revisor y sus evidencias. El validador comprueba
ligaduras y rechaza firmas ausentes, negativas, anteriores o obsoletas; no
emite dictámenes científicos por su cuenta.

## Materialización y límites

El remediador conserva el texto histórico de los objetivos y las consultas,
pero escribe el texto nuevo de una disposición válida en la tabla y su mapa.
El constructor atómico aplica el delta separado y conserva la C de celda como
síntesis de las C explícitas nuevas, sin heredar las dependencias de la celda
rechazada ni todas las referencias bibliográficas de su fila. Los controles
globales y el censo semántico continúan exigiendo sus revisiones propias.

Cambiar un objeto, C de soporte, fuente, informe o dictamen invalida la ligadura.
Se rechazan rutas no canónicas, escapadas y symlinks. Se releen los artefactos,
las C y el registro al terminar para detectar cambios durante la comprobación;
el llamador también compara las entradas residuales/objetivos/correcciones.
No se consulta la hora del sistema en validación: la comprobación es repetible.

Los 16 tests nuevos usan datos ficticios en directorios temporales; sus
dictámenes inventados sólo ejercitan el contrato y no firman objetos reales.
Pasan además los 13 tests de remediación y los cinco del constructor atómico.
`build_atomic_cell_claims.py` conserva las 816 C atómicas exactas con el
registro vacío. La revisión independiente y la prueba de integración con
disposiciones no vacías están encargadas a otro agente; este informe no
anticipa su resultado ni declara cerrados los controles del plan.

## Reparaciones posteriores a la primera revisión técnica

La primera revisión independiente encontró fallos reales. Sus reproducciones
se conservan en `revision_disposiciones_adversarios_inicial_2026-09-27.json`
y `integracion_disposiciones_independiente_2026-09-27.json`: no se sustituyen
por los resultados de los tests del autor. La expectativa del revisor de
aceptar S1 como alias de S01 fue retirada por él, manteniendo el resultado
original como antecedente; S01 es la forma canónica de esta versión.

Se corrigieron:

- Normalización de identidades para detectar autorrevisión con variantes de
  mayúsculas, blancos o Unicode; rechazo de identidades pendientes/no asignadas.
- Expansión de los interiores de rangos S y C mediante los parsers del corpus;
  las etiquetas de figuras suplementarias no son fuentes bibliográficas.
- Rechazo de symlinks en CSV del catálogo C, no sólo en artefactos probatorios.
- Revalidación de la disposición al final de ambos constructores y comprobación
  de que sus entradas no cambiaron durante la materialización. Validar al
  principio no bastaba si la corrección o su fuente cambiaba después.
- Eliminación de BN heredadas desde el roll-up de la fila para las nuevas
  síntesis de celda. Las consultas históricas quedan fuera de su apoyo positivo.

Se añadió `identidad_fila` al contrato: un mapa exacto de la primera columna
y los campos `taxón o sistema`/`magnitud` cuando forman parte del sujeto.
Las mismas coordenadas de celda en un taxón diferente no pueden conservar la
revisión. Esta versión no admite sustituir la propia primera columna; exige
un tratamiento separado para ese cambio de identidad.

Versión de autor remitida a reinspección (todavía no aprobada aquí):

| Script | SHA-256 |
| --- | --- |
| residual_semantic_dispositions.py | `222a9dd383dc904a08ccb881fd8122abd9b337e24a062e0b5c84cc32b3a593d4` |
| remediate_trace_residuals.py | `85dfdc2db6e85ee2d4344321e4bfae7059a6f46a490a1d5b9f767e4a244d71c4` |
| build_atomic_cell_claims.py | `7a24993ff2411e0bcc1f534633b6e5c5d5a00b9bff3e2ad820700993b1632cd9` |

Los 22 tests específicos del helper pasan. El registro real sigue vacío;
ningún test ha incorporado una firma o disposición científica al corpus.

## Reinspección técnica recibida

`ADDENDUM_INDEPENDIENTE_DISPOSICIONES_REPARADAS_2026-09-27.md`
(SHA-256 `3086d6d76320bb88bf6b41c1267fc1a772b1d614ffe41c35e226b78063ed15fe`)
dictamina conforme el alcance técnico de esos tres hashes: 20 adversarios
nominales propios, tres pruebas integrales propias, 40 tests focalizados y
264 tests del proyecto. La captura final del revisor es 02:05:17Z. El JSON
`reinspeccion_disposiciones_reparadas_2026-09-27.json` conserva SHA-256
`2e4a50fa9a84717603104b44a97b4b4224d0528048be3c30ba05d45187e15705`.

La integración ficticia comprobó seis deltas, las 410/408/2 entradas, consultas
idénticas, BN y objetivos históricos intactos, 816 C atómicas, idempotencia y
rechazo de las carreras. No contiene ni sustituye un dictamen sobre las seis
celdas científicas propuestas de S240/S352. El registro real permanece vacío
hasta contar con propuestas científicas corregidas y sus revisiones exactas.
