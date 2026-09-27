# BN-120: atribución anterior de la celda de método C-2783

Inspección y prueba en memoria: 2026-09-26T22:33:52Z.
Autor: `/root/verificacion_fuentes_nuevas`.
Este addendum corrige la propuesta de enlazar C-2783 con las C nuevas de
genes/densidad: C-2821 y C-2822 son posteriores y no pueden ser dependencias
de esa síntesis. No modifica el corpus ni dicta conformidad del futuro parche.

## Solución mínima propuesta por el autor principal y cotejada aquí

La celda `versión o método` de table-53, fila nominal 6, puede decir:

> tamaño: ensamblaje de referencia de S446; intrones: reconstrucción
> comparativa de S434; las métricas se atribuyen por separado a sus fuentes

Es fiel a C-1565 (registro del tamaño/S446) y C-1566 (reconstrucción comparativa
de intrones/S434). El último segmento describe la organización editorial de
la fila; no afirma equivalencia entre anotaciones. No añade los recuentos ni
el método específico Malin a esas dos C.

Las celdas de genes y densidad llevan **dentro de su propio valor** las C
nuevas, respectivamente C-2821 y C-2822. La primera especifica el conjunto
Broad Institute de S434; la segunda, su modelo Malin de 342 ortólogos/40
genomas y la unidad intrones/kbp codificante. Sus entradas del mapeo deben
apuntar a esas C nuevas, no a C-1990 ni a C-2783.

El campo `#` puede conservar:

```text
C-1565–C-1566; C-2783; las celdas de genes e intrones incluyen sus propias C
```

No incluir ahí otra vez C-2821/C-2822: `_generated_claim` agrega las C de ese
campo como candidatas para el lote >=C-2572. Las referencias locales en las
dos celdas precisas evitan tanto esa herencia incorrecta como una omisión de
atribución. El campo fuente puede mantener sus localizadores S específicos;
no necesita repetir las C nuevas fuera de las celdas.

## Prueba ejecutada sin escritura

Se cargaron el catálogo vivo y la fila table-53, se construyó una copia en
memoria con los tres valores propuestos y se llamó a `_generated_claim` con
objetivo C-2783/columna método y `afirmaciones_previas=C-1565; C-1566`.
No se ejecutó el generador sobre archivos ni se alteraron sus reglas.

Resultado comprobado mediante aserciones:

```text
Atribución = sintesis(C-1565, C-1566)
Fuente = n/a; dependencias canónicas C-1565; C-1566
Sujeto = organismo «*Sphaeroforma arctica*»
Predicado = tiene_valor_literal_de_campo*
Objeto = versión o método: [literal propuesto]
Ausencia de C-2821 y C-2822 en todos los campos generados: comprobada
```

No se probó todavía la cadena completa con la corrección histórica de celda,
las nuevas C y sus mapeos aplicados: corresponde a la revisión del parche real.
Los resultados `resuelta`/`media` del generador son etiquetas mecánicas, no una
firma de revisión independiente ni aprobación del apoyo científico.

## C-1566 no necesita cambiar

Su comparación ya tiene como contexto una reconstrucción publicada. Añadir
Malin/342/40 como calificador de esa reconstrucción podría conservar su único
predicado comparativo, pero ampliaría el detalle afirmado y exigiría nuevo
cotejo y huella. No es necesario para esta solución. Conviene conservar su
SPO y dejar los parámetros en C-2822, donde delimitan la densidad nueva.

La propuesta no introduce excepciones de orden, no transforma C-2783 en una
atribución directa nominal y no altera validadores, enum ni reglas SPO.

## Huellas observadas

SHA-256 de archivos:

- `scripts/build_atomic_cell_claims.py`: `f3d8ff6b7a03552e500dc735a9ca169d628e86cc87799bddb7689bc74002b6aa`.
- `scripts/validate.py`: `c5c3af9390158f374edbc78ec90f6379a18a6a88242b8068fc7492b0c2cbf131`.

SHA-256 de filas completas (JSON ordenado, UTF-8, separadores compactos y LF):

- C-1565: `e501d163d7b39131a574fa7e95696f5598087ec7ad942982cfe67b0ef795c9f9`.
- C-1566: `3915165771ae7282beb44d74233fef9c4bf2025b75315476fd320e16b93d84b4`.
- C-2783, antes del parche: `c59f2f4e6199f6bdd387fce502db7f574546409e237f17549906306d20d8def5`.
