# Protocolo de censo semántico integral de afirmaciones

## Objetivo y congelación

El censo cubre el 100 % de las C canónicas vivas y decide, una por una, si la
afirmación está sostenida por el pasaje recuperado que declara `Fuente`. Puede
cerrar R-0008/R-0009 y alimentar la segunda revisión `AFIRMACION`, pero no es
una firma global por sí solo.

Antes de adjudicar se congelan las rutas y SHA-256 de `data/afirmaciones`, los
artefactos de `fuentes/`, todos los apéndices, tablas, búsquedas negativas y
secciones que pueden ser objeto de una glosa, el Apéndice A, la matriz de
fuentes y el inventario de acceso. Si cambia una fila C, una fuente, un
localizador, una BN, una tabla o una dependencia, su dictamen y los de sus
síntesis descendientes quedan obsoletos.

## Unidad probatoria

La unidad exterior es una C. La unidad probatoria es cada proposición atómica
de `Afirmación`, incluidos:

1. sujeto y circunscripción taxonómica;
2. predicado y dirección;
3. objeto o resultado;
4. cifra, signo, unidad, denominador e incertidumbre;
5. organismo, muestra, condición, método y comparación;
6. alcance temporal, espacial y taxonómico;
7. modalidad y fuerza;
8. atribución, límites y excepciones.

Una C solo es `CONFORME` si todos los componentes están cubiertos. Una verdad
general o una coincidencia parcial no repara objeto, método o alcance.

## Evidencia y localizadores

Para cada S se resuelve el artefacto local por el inventario de acceso. Tener
archivo, DOI, URL o clave no equivale a verificación semántica.

- PDF: página PDF e impresa si difiere, sección/figura/tabla y bloque.
- JATS: sección, figura/tabla o XPath estable al párrafo/celda.
- HTML/texto: sección y ordinal de párrafo, tabla o figura.
- Suplemento: archivo, hoja/tabla, fila y columna.
- `tesis general`: solo si la C expresa realmente la tesis y esta se localiza
  en resumen, resultados principales o conclusión.

Se conserva un fragmento de control de hasta 25 palabras, SHA-256 del pasaje
normalizado y del artefacto. La normalización solo une blancos y guiones de fin
de línea. `sin localizar`, una clave sola o una búsqueda léxica son candidatos,
nunca prueba. Si el pasaje no aparece, no se infiere desde memoria, título u
otra fuente.

## Reglas por atribución

### `expresa`

Todos los componentes deben aparecer en las fuentes declaradas. Varias fuentes
pueden cubrir componentes distintos, con matriz explícita. Una contradicción
no resuelta impide conformidad.

### `sintesis(...)`

Todas las dependencias necesarias deben existir y ser `CONFORME`. La conclusión
no puede añadir sujeto, objeto, cifra, causalidad, ancestralidad, universalidad
o fuerza modal. Una dependencia `NO_VERIFICABLE` produce `NO_VERIFICABLE`; una
dependencia `NO_CONFORME`, omitida o insuficiente produce `NO_CONFORME`.

### `glosa`

Una glosa estructural se coteja contra el artefacto que describe. Una glosa que
afirma un hecho científico, cifra, taxón o relación necesita evidencia semántica;
`n/a` no la vuelve editorial.

### BN

Una BN solo prueba la consulta, universo y resultado registrados. Puede sostener
`no se localizó X en Y`, nunca `X no existe`, `el taxón carece de X` ni una
alternativa positiva. Una BN incompleta no se rellena desde memoria.

## Dictámenes

- `CONFORME`: todos los componentes, cifras, unidades, negaciones, dirección,
  alcance, modalidad y atribución coinciden; el localizador es reproducible.
- `NO_CONFORME`: contradicción, inversión, objeto/cifra/unidad incorrectos,
  generalización, causalidad o fuerza no publicadas, fuente circular, síntesis
  no derivable, ausencia convertida en hecho o `expresa` que es inferencia.
- `NO_VERIFICABLE`: solo cuando el corpus congelado no permite decidir por
  artefacto ausente/corrupto/incompleto, imagen ilegible o pasaje no identificable.
  No suaviza una contradicción ni aprueba plausibilidad.

## Ejecución e independencia

1. Construir inventario determinista y grafo de dependencias.
2. Revisar primero `expresa`, luego glosas/BN y finalmente síntesis topológicas.
3. La búsqueda textual solo propone pasajes; un revisor lee el contexto.
4. Registrar también fallos, consultas, secciones y motivo exacto.
5. Exigir 100 % de C una vez, huellas vigentes, componentes cubiertos,
   localizadores, dependencias cerradas y cero aprobaciones automáticas.
6. Congelar la primera revisión y entregarla a un revisor distinto.
7. La segunda revisión repite el cotejo sin leer primero el dictamen.
8. Toda discrepancia queda abierta hasta resolución con pasajes concretos;
   nunca se resuelve por mayoría ni declaración del autor.

## Salidas

La primera revisión se guarda en
`data/auditoria/censo_semantico_afirmaciones_v1.csv` con los campos que exige
`scripts/check_semantic_claim_census.py`: componentes y matrices como JSON
canónico, artefactos/pasajes con huellas, dictamen, motivo, limitaciones,
revisor, fecha y versión de protocolo.

El JSON tiene un contrato cerrado. `componentes_atomicos`,
`fuentes_declaradas` y `artefactos_verificados` son listas sin duplicados;
`fuentes_declaradas` reproduce en orden las claves S/BN de `Fuente`;
`sha256_artefactos` es el mapa exacto ruta→huella del inventario congelado;
`dependencias_y_huellas` es el mapa exacto C→huella de `sintesis(...)`; y
`matriz_cobertura_componentes` contiene exactamente una entrada no vacía por
componente. Cada evidencia de la matriz empieza por una fuente, dependencia o
ruta declarada, seguida opcionalmente por `:` o `#` y su localizador. En una
`expresa` conforme, cada fuente declarada tiene un artefacto nominal local; un
archivo `.url`, disponibilidad o metadato no sustituyen el texto probatorio.
La versión es `1` y `fecha_utc` es un instante UTC del 13 de agosto de 2026.

La revisión independiente se guarda en
`data/auditoria/segunda_revision_afirmaciones_v1.csv`: fija la huella completa
del censo primario, reinspecciona localizadores/pasajes, registra evidencia,
discrepancia, resolución e independencia.

La segunda revisión usa versión `1`, una o más huellas SHA-256 de pasaje
separadas por `;`, instante UTC del mismo cierre y la declaración literal
`REVISION_INDEPENDIENTE_SIN_PARTICIPACION_EN_CENSO_PRIMARIO`. Con
`discrepancia=NO`, la resolución literal es `NO_APLICA`; una discrepancia real
permanece abierta y bloquea el cierre.

## Antirregresiones y cierre

- Ninguna puntuación léxica, acceso, artefacto, DOI o clave puede aprobar.
- Una C no hereda el dictamen de otra; párrafos no transfieren evidencia.
- Una BN nunca se promueve a evidencia positiva.
- Las filas cambiadas invalidan dictámenes por huella.
- El control falla ante C nueva, cambiada, omitida, duplicada, auto-revisada,
  aprobada sin evidencia, discrepancia o residual.

R-0008/R-0009 solo cierran con 100 % de C doblemente revisadas, cero
`NO_CONFORME`, cero `NO_VERIFICABLE` científicos, cero discrepancias abiertas y
huellas exactas de corpus, fuentes, pasajes y ambas revisiones.
