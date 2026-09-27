# Revisión técnica independiente: dependencias explícitas de celda

Revisor: `/root/revision_residuales/candidatos_editoriales`. Autor del cambio: `/root`. Rama comprobada: `codex/cierre-plan-pendiente`. Ejecución independiente: **2026-09-27T04:21:11Z–04:21:13Z**. Dictamen: **NO_CONFORME**, limitado a los dos defectos reproducidos aquí. No es revisión científica de S10 ni cierre del plan.

## Versión fijada

- Código revisado `scripts/build_atomic_cell_claims.py`: `6a357a08f93918254f25b2381cb6c9e18fa520838bd33a3d56f37a74e51ba5e9`.
- Tests del autor `tests/test_build_atomic_cell_claims.py`: `4ea9e78be209811100d32d02e887f91f1a19a14a22a7900e5378705a41b6de27`.
- Snapshot exacto del código: `snapshot_build_atomic_cell_claims_6a357a08_2026-09-27.txt`, mismo hash que el código. Se conserva aunque el autor repare después.
- Evidencia nueva `evidencia_independiente_dependencias_celda_explicita_v1_2026-09-27.json`: `d531a88f970a459019e2f29a4477d740c7c388b403a69488abe0f92878d0ba69`.
- Reproductor propio `probe_independiente_dependencias_celda_explicita_2026-09-27.py`: `156faf23a8404df3afa59908802fe30670216c1102ea17bbe93737cecc702f97`.

El reproductor crea sólo fixtures ficticias en un directorio temporal `/tmp`, con 816 objetivos, catálogo, tablas, correcciones, manifiesto y registro vacío. Ejecuta el `build()` real; sólo redirige sus rutas. No sustituye `_apply_corrections`, el consumidor residual ni la generación por stubs. Las mutaciones controladas de concurrencia ocurren únicamente en esos archivos temporales. No hay dictámenes científicos fingidos ni firmas reales en las fixtures.

## DEP-EXPLICITA-01 — préstamo de fuente en ramas directas (P1)

`exact_dependencies` se calcula, pero las cuatro ramas `direct_source` siguen teniendo prioridad en `_generated_claim` (líneas 276–299 de la versión fijada). Una corrección ligada con contenido `NUEVO FICTICIO [C-032]`, cuya única C de apoyo existe y tiene Fuerza baja, emite:

| Ruta de código probada | Atribución producida | Fuente producida |
| --- | --- | --- |
| table-06 fila 5 / C2009 | expresa | S49 tabla 2 |
| table-06 fila 25 / C2029 | expresa | S49 tabla 3 |
| condición nominal C2472 | expresa | S435, primer localizador fijo |
| condición nominal C2489 | expresa | S435, segundo localizador fijo |

En los cuatro casos la Fuerza sí deriva de C032, pero esa C desaparece de Atribución/Fuente. El resultado mezcla apoyo explícito con una fuente fija ajena al contenido corregido. Las primeras dos ramas son las de las correcciones table-06, cuyo comportamiento sin C propias debe conservarse. Los dos IDs positivos S435 se probaron como ramas aisladas en la fixture: **no se afirma que una corrección de esos positivos sea admisible en el inventario residual vivo**, donde otra puerta la bloquea. Aun así la precedencia interna equivocada queda demostrada también en esas condiciones.

El defecto bloquea la conformidad del mecanismo general, aunque el camino genérico de las diez celdas S10 no use estas excepciones. Reparación propuesta, no implementada por el revisor: dar prioridad al apoyo explícito validado frente a `direct_source`, manteniendo las excepciones anteriores sólo cuando no hay soporte exacto prospectivo. Añadir regresiones para ambas zonas table-06 y las condiciones nominales, sin permitir que las correcciones de positivos evadan su control residual.

## DEP-EXPLICITA-02 — catálogo fuera de 15.csv no fijado durante build (P2)

El conjunto `input_paths` de `build()` (líneas 374–377) sólo fija `CLAIMS`, que es `data/afirmaciones/15.csv`, pero `_claim_catalog()` consume todos los CSV de afirmaciones. La relectura final de disposiciones no protege soportes de correcciones no residuales cuando no hay disposiciones que los fijen.

Reproducción con el pipeline completo: después de obtener el catálogo, la fixture cambia C032 en `data/afirmaciones/00.csv`, de Fuerza `baja` a `desconocida`. `build()` termina aceptado y genera C2606 con Fuerza **baja**, tomada del catálogo antiguo. El mismo resultado se reproduce cambiando sólo los bytes con un LF; la mutación semántica descarta que el hallazgo sea únicamente cosmético. Por contraste, una mutación de la tabla durante el mismo punto del pipeline sí falla con `Entradas cambiaron durante materialización atómica`.

Este defecto pertenece a la cobertura incompleta de la guarda de entradas; no se presenta como una promoción científica deliberada ni como prueba de que ocurrió en el corpus real. Para el contrato determinista y aislado debe fijarse el catálogo completo, incluida su membresía fresca, y comprobar que no cambian, aparecen o desaparecen archivos ni destinos durante la materialización. No basta con añadir únicamente el archivo de un soporte concreto o volver a comprobar sólo las disposiciones.

## Lo que sí resistió los adversarios

El reproductor ejecutó 21 casos con historia de objetivos preservada. El camino genérico corregido usa sólo C explícitas; no arrastra C1983, C028 ni BN115. Los rangos ascendentes incluyen interiores y la fuerza mínima; una BN escrita en la celda nueva se conserva, la de metadata de fila no. La corrección sin C explícita y el objetivo no corregido mantienen su anterior conjunto de candidatos: esta invariancia **no aprueba científicamente** esos candidatos.

Se rechazaron autocita directa y en rango, rango inverso solo y mixto, dependencia ausente, hash previo incorrecto, evidencia autoral vacía y corrección huérfana. Una corrección ficticia residual de C2708 con C explícita y sin disposición se rechazó por `correcciones residuales sin disposición revisada`. No se encontró evasión de esa puerta por añadir C al contenido. Se mantuvo la nota del manifiesto que exige rerevisión ajena; su estado técnico `REVISADA` no se interpreta aquí como aprobación científica.

Dos ejecuciones de la fixture genérica dieron bytes idénticos. Los hashes de código, tests, ambos objetivos históricos, quince correcciones reales, C15 y manifiesto vivos fueron iguales antes y después. Ninguna prueba escribió esos archivos.

## Regresiones y límites

Se ejecutó de nuevo `python3 -m unittest tests.test_build_atomic_cell_claims tests.test_residual_semantic_dispositions tests.test_remediate_trace_residuals`: **49 tests, 6.253 s, OK**. Incluyen las regresiones de revisión residual previa: autoría/UTC, revisión exacta, pasajes/componentes, fuentes, mutaciones, identidad, rangos y confinamiento. Son una regresión complementaria; su éxito no anula los dos defectos de los adversarios propios.

`python3 scripts/build_atomic_cell_claims.py` produjo **816 afirmaciones exactas**, sin `--write`. Esto confirma invariancia del estado vivo actual —incluidas las quince correcciones sin C propias—, no la corrección de todos los caminos futuros ni el cierre de `make verify`.

No se integró ni aprobó ninguna corrección científica S10. No se modificaron canon, implementación, tests del autor, fuentes, disposiciones reales, firmas ni evidencia previa. Una versión reparada requiere reinspección con hash nuevo; este rechazo permanece histórico.
