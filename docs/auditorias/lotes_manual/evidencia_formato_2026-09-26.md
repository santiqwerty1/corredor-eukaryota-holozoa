# Revisión independiente de cinco controles editoriales

Revisor: `Codex /root/revision_manual_formato`. Fecha: 2026-09-26.
Comprobación final de evidencia: 2026-09-26T21:12:02Z.
Rama inspeccionada: `codex/cierre-plan-pendiente`.

El revisor no escribió ni corrigió el corpus, sus controles o sus derivados.
Solo produjo los archivos de evidencia de este lote. Los cinco dictámenes
se refieren a R-0398, R-0399, R-0400, R-0404 y R-0448; no son una aprobación
científica, una segunda revisión del conjunto ni un cierre de `make verify`.

## Alcance real y método

Se leyó el encargo literal completo, incluido el contexto de las secciones
16–18, y el contrato de adjudicación manual del auditor. La evidencia se
obtuvo del documento autocontenido regenerado, las 26 plantillas ordenadas,
las 97 tablas CSV, el informe de lectura y los catálogos locales de claves.
El inventario adjunto contiene 129 rutas con SHA-256; incluye además el
encargo, el orden documental, el índice y el registro Q de búsquedas.

`probe_formato_2026-09-26.py` es una inspección de solo lectura escrita por
este revisor: reconstruye en memoria la salida tabular desde CSV y plantillas,
sin importar `render.py` ni funciones del validador del proyecto. Compara
la salida completa, cuenta las tablas y comprueba todas sus cardinalidades.
La salida persistida está en `evidencia_formato_2026-09-26.json`.

La igualdad exacta del ensamblado independiente cubre las 11.706 líneas de
la salida autocontenida: 97 marcadores, 97 tablas, ninguna omitida o duplicada.
Se inspeccionaron manualmente los 315 encabezados, los 22 bloques de árboles
y esquemas y las cabeceras de los ocho apéndices. Esa igualdad no es una
prueba de verdad científica de sus celdas.

## Dictámenes de contenido

### R-0398 — CONFORME

Los ocho apéndices están incluidos como tablas Markdown completas, una
aparición de cada tabla, con orden y cardinalidad conservados:

| Apéndice | Filas | Columnas | Línea de cabecera en el autocontenido |
| --- | ---: | ---: | ---: |
| A | 524 | 9 | 8515 |
| B | 1501 | 5 | 9046 |
| C | 108 | 8 | 10554 |
| D | 216 | 10 | 10669 |
| E | 82 | 8 | 10892 |
| F | 590 | 9 | 10981 |
| G | 23 | 5 | 11578 |
| H | 25 | 2 | 11606 |

La octava columna de C, `desenlace`, está expresamente solicitada después de
la enumeración inicial de siete columnas: no es una columna añadida por
el autor. A, B, D, E y F coinciden con sus columnas literales. G incorpora
material, estado/afirmación, fuente/localizador, sección propuesta y C; H
expresa el recuento como pares control/valor, sin introducir columnas ajenas.
El prompt no fija una enumeración nominal de columnas para G y H.

El informe de lectura enlaza tablas procesables; no se tomó ese enlace
como sustituto de la tabla: se inspeccionó la versión autocontenida que
efectivamente reproduce todos los datos.

### R-0399 — CONFORME tras reinspección de FORM-01

El censo de claves en la salida completa resuelve 2817 C, 524 S, 108 E,
82 H y 498 BN distintas a sus catálogos locales. Las cinco Q citadas
son Q-0171–Q-0175, existentes en el registro local de búsquedas; los 56
identificadores V19 corresponden a vistas locales, no a nuevas C.

Se distinguieron claves documentales de nombres o identificadores de la
literatura: Q-1, ANME-1, K-12, APU-30, RIF-1 y componentes de DOI no son
nuevas claves bibliográficas ni del pipeline. Las marcas [F] y [H] en los
árboles tampoco se confundieron con claves de hipótesis H01, H02, etc.
La referencia C01-PROMPT-INVESTIGACION del apéndice G identifica el propio
encargo local y no una fuente científica ajena al catálogo.

#### FORM-01 — hallazgo previo NO_CONFORME conservado

Durante la primera inspección, la fila BN-117 contenía en `filas relacionadas`
`C-757–C-792; S139–S142; S177–S181; S548`. El intervalo S177–S181 incluía
S180, que no estaba en A. La salida de entonces lo reproducía en la línea
7142 y H indicaba una referencia S indefinida. No se adjudicó conformidad
en ese estado ni se corrigió la fila desde esta revisión.

El autor cambió únicamente ese componente a `S177–S179; S181` y regeneró
la salida. La reinspección separada verificó la fila completa, la expansión
de todos sus rangos, el catálogo A y el documento regenerado. S180 continúa
ausente de A, como dispone la fila S180 de
`data/auditoria/entradas_congeladas_reconstruidas/fuentes_retiradas.csv`;
no se resucitó ni se reasignó su clave. El censo independiente de la nueva
salida devuelve cero claves S indefinidas y H informa cero.

Huellas de la versión reinspeccionada:

- BN, archivo `15_4_15-4-registro-material-tiempo-ambiente-y-ecologia.csv`:
  `99f1ae02a824ebaaa7fdb34b44cd6fe7da405136bde8a8a378c1e85348b82fd1`.
- Autocontenido:
  `96c2ef9fa355658bace71766e3b7626d6c437812bf76cef0ff6e0c95bce59f02`.
- H:
  `778c1fa76468368dd1923826a7c00fd111119f298702984e4348f4215da955c7`.

No se conserva aquí una huella del archivo anterior a esa corrección:
el hallazgo previo está documentado por el contenido literal observado,
su ubicación y la comunicación al autor, no por una falsa congelación previa.

### R-0400 — CONFORME

El barrido literal completo de ambos informes no encuentra identificadores
con prefijos `CLAIM-`, `SRC-`, `ENTITY-`, `EVENT-` ni `HYP-`. Para este
mandato lexical cerrado, el barrido completo sí es una prueba nominal:
se acompañó del censo positivo de las claves realmente emitidas descrito
en R-0399. No se promovió la simple existencia de un archivo a conformidad.

### R-0404 — CONFORME

Se inspeccionó la partición completa por encabezados y por tablas: A es la
única tabla con autores, año, título, publicación, DOI/URL y demás campos
bibliográficos, y aparece una sola vez. Los otros siete apéndices cumplen
funciones distintas y las citas en prosa, árboles y celdas remiten a S.

La única línea con URL fuera del intervalo de A es C-1715, línea 6689:
conserva las consultas GET a RegNum en el campo Fuente, junto a S384.
Su lectura muestra un localizador de una afirmación, no una segunda
bibliografía. D menciona títulos en las filas de fechas de publicación;
esas filas contienen el dato temporal y su S, no otro catálogo de fuentes.
La expresión «Genomas de referencia» del encabezado 12.7 tampoco designa
una bibliografía. No se contaron como bibliografías adicionales los
inventarios operativos de acceso externos al documento solicitado.

### R-0448 — CONFORME editorial, con límite explícito

El documento entregable es Markdown: encabezados, listas, énfasis, tablas
de barras y bloques cercados. Los 22 bloques están cerrados y los 315
encabezados son títulos en español con nombres técnicos o taxonómicos.
Se leyeron todos esos encabezados y bloques, el preámbulo, las cabeceras
tabulares, los apartados A–H y 19 inspeccionados arriba, y 69 pasajes de
prosa distribuidos por todas las plantillas que tienen prosa.

Como selección adicional de lectura, se recorrieron todas las líneas de
las plantillas y todas las 2817 proposiciones C buscando candidatos
lingüísticos atípicos. Se leyeron los nueve pasajes y las quince C devueltos
por ese filtro: son frases españolas; los falsos positivos incluyen la
preposición «a», nombres latinos y citas literales. El JSON conserva
los textos, no solo un recuento. Este filtro no es un clasificador de
idioma validado ni produjo por sí solo el dictamen.

La revisión distingue el español de la voz narrativa de los títulos de
fuentes, citas literales, taxones, localizadores ingleses y términos
originales que el propio encargo obliga a conservar. El texto leído muestra
sintaxis española y esa distinción es coherente en los registros examinados.

Límite: no se afirma haber leído palabra por palabra las aproximadamente
50.000 palabras de las plantillas más todas las celdas científicas. La
inspección lingüística es estratificada; el censo estructural y de claves
sí es exhaustivo sobre la salida ligada por hash. Este dictamen del idioma
general del documento no acredita traducción técnica correcta, literalidad
epistémica, primera glosa bilingüe, atomicidad ni ninguna otra propiedad
semántica que corresponde a controles separados.

## FORM-02 — ligadura oficial inicialmente insuficiente

Al cerrar este lote, `manual_scope_paths` censa 98 archivos para R-0398,
siete para R-0399/R-0400 y solo `data/table_index.json` para R-0404/R-0448.
No incluye los informes regenerados; en R-0404/R-0448 tampoco liga la prosa.
En R-0399 incluso omite A y el archivo de BN que contenía FORM-01.

Se conservan en el CSV las rutas y huellas exigidas por ese contrato vivo,
sin falsearlas ni editar el validador. El inventario complementario de 129
archivos liga la evidencia editorial real, pero no corrige por sí mismo
la puerta oficial. Los dictámenes de contenido no autorizan promover
automáticamente el ledger global mientras FORM-02 siga abierto. Tras
reforzar el alcance del auditor hay que comprobar de nuevo el inventario
y emitir o actualizar la ligadura mediante una reinspección independiente.

La fecha del lote es la fecha real de revisión, 2026-09-26, no la fecha
histórica usada en nombres de archivos de auditoría. La declaración
canónica de independencia se limita al autor del control y del corpus;
el script de evidencia de este lote es autoría del propio revisor y
no se presenta como una segunda revisión de su propio código.

## Reinspección posterior de FORM-02 — CERRADA

Fecha: 2026-09-26T21:17:19Z. El autor amplió `manual_scope_paths` para estos
cinco requisitos. Se leyó el diff y se comparó el conjunto de rutas resultante
con el inventario editorial levantado de forma independiente antes del
parche. No se ejecutó ninguna rematerialización desde esta revisión.

El alcance oficial contiene ahora los 97 CSV, las 26 plantillas, el orden,
el índice y ambos informes: 127 archivos. R-0399 liga además el registro Q,
128 archivos. El encargo tiene su huella literal separada; su archivo
completo también queda en el inventario complementario. Se comprobó que
los 129 archivos de ese inventario siguen byte-idénticos a la versión
efectivamente revisada y que la ampliación no clasifica los requisitos
como automatizados ni pierde destinos previos.

Las ocho pruebas del autor (cinco sobre rangos S y tres sobre alcance) y
las nueve comprobaciones independientes de `probe_parches_formato_2026-09-26.py`
pasaron. Entre estas últimas están el cálculo independiente del digest,
el conjunto exacto de rutas de cada control, la no promoción automática,
la conservación de destinos preexistentes y la comprobación de las 129
huellas. Después, y no antes, se recalcularon las ligaduras del lote.

- R-0398, R-0400, R-0404 y R-0448:
  `7af6b08e88ab0425111347126be807827258a4e27de293a54ca9278d7258033a`.
- R-0399:
  `5fcf8ca02c099693516ffb8052bf369be495436d1d98410b55526925099e9fb4`.

Las cinco filas finales pasan individualmente `validate_manual_review`
sin errores. Esto valida el contrato del lote; no afirma que el ledger
global de 210 filas exista ni que sus restantes controles estén cerrados.
La copia `revision_formato_2026-09-26_estado_inicial.csv` conserva las cinco
filas y advertencias emitidas antes de reforzar la ligadura, con SHA-256
`905ed2bf0505737f3a77a5a2bc722549e65bf66cc2517188c3f5e1a77aec0740`.
El lote final tiene SHA-256
`8b86a84a416af7e72e337f2cc7a47bad7ef3d5e5d9df60d4ea0839ea6b20b15a`.

## Revisión acotada del parche de rangos S

El parche de `validate.py` añade interiores de rangos mediante la expansión
canónica y conserva el control literal previo. Se verificó con un fixture
CSV temporal de la fila nominal BN-117: la forma anterior falla por S180
y la forma corregida pasa. Se verificaron asimismo rangos con guion,
raya y blancos, varios interiores ausentes, rangos descendentes, claves
literales posteriores y el comportamiento anterior de etiquetas de
suplementos. No se cambió código productivo ni el corpus desde esta revisión.

`python3 scripts/validate.py` devolvió únicamente `manifest.json desactualizado`;
no se presenta ese resultado como validación global verde. Las huellas
del código inspeccionado son:

| Archivo | SHA-256 |
| --- | --- |
| scripts/validate.py | c5c3af9390158f374edbc78ec90f6379a18a6a88242b8068fc7492b0c2cbf131 |
| scripts/audit_requirement_controls.py | d7b0bff89c439633d73706d3039e7bd0372708e9c511c0a5413620e9510c131a |
| tests/test_validate_source_ranges.py | 453fee847f88305128615df101b37e6d10af497f77497fa168f95f625c28696c |
| tests/test_manual_editorial_scope.py | de270c38f009dbfe7bcadcf3f0b81155c20c2a7c19ba86b1c9c2b4a089f892ad |

### FORM-03 — limitación de notación abreviada observada inicialmente

`source_reference_errors('S177–181', {'S177', 'S181'})` devuelve una lista
vacía: la expansión canónica exige repetir S después de la raya. Esto no
es un debilitamiento introducido por el parche ni invalida la prueba de
BN-117, cuyo rango repetía S, pero impide afirmar que se validan todas
las notaciones abreviadas de rangos. La forma `S177–179; S181` también
pasa por control literal, no por haber expandido sus interiores.

La novena serie independiente registra explícitamente este comportamiento
como limitación, no como aprobación. Se buscó esa sintaxis abreviada en
todo el autocontenido mediante `\\bS(\\d{2,3})\\s*[–-]\\s*(\\d{2,3})\\b`:
no hay ocurrencias en la versión editorial revisada. Por tanto, el hallazgo
afecta a una posible entrada futura y no deja claves indefinidas ocultas
bajo esa forma en el lote actual. Fue comunicado al autor y permanece
separado de los cinco dictámenes editoriales y de FORM-02.

### Reinspección de FORM-03 — CERRADA

Fecha: 2026-09-26T21:18:49Z. El autor cambió únicamente el reconocimiento
del segundo prefijo de `SOURCE_RANGE` de `S` a `S?`, conservando la
comprobación de rango descendente y la distinción de contexto suplementario.
Se leyó ese diff y se volvió a probar el contraejemplo, sin editar el
validador desde la revisión.

La nueva versión rechaza `S177–181` cuando faltan S178, S179 y S180;
acepta `S177–179; S181` cuando existen todos sus miembros y rechaza esa
misma forma si falta S178. También rechaza S181–177, conserva el cero
de S08–10 y no convierte `figs. S62–64` en un rango bibliográfico.
Pasaron las nueve pruebas de `test_corpus_io` + `test_validate_source_ranges`
y las once pruebas independientes finales del probe de parches. El caso
del probe que documentaba el comportamiento anterior fue reemplazado por
el contraejemplo con su resultado exigido tras la reparación; la historia
y el resultado anterior permanecen arriba, no se reescribieron como éxito.

Huellas finales añadidas o modificadas por esta reparación:

| Archivo | SHA-256 |
| --- | --- |
| scripts/corpus_io.py | 4d7d35fb8649d41e4c137da16e1991a1a4117d8c46b68aa5d7fc3ae0c462fef7 |
| tests/test_corpus_io.py | 3534f0dcbebda29be8cb9d30a1ea512c21e5a7466a3a26233ddabc31c45221d9 |
| tests/test_validate_source_ranges.py | 49b4ec0531986349f7285df3958aee6ce5296284d16eaa51f72cd9c8750447cc |

El inventario editorial sigue sin cambios y los cinco dictámenes se
mantienen ligados al mismo documento efectivamente inspeccionado. Cerrar
FORM-03 no aprueba otras formas de referencia no ensayadas, ni la evidencia
científica de las fuentes, ni el cierre global.
