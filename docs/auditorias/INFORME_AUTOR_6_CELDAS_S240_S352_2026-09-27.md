# Propuesta autoral acotada: seis celdas S240/S352

Autor: `/root/inspeccion_relojes`. Rol: **autor de la propuesta, no revisor independiente**. Informe materializado a partir de comprobaciones realizadas hasta 2026-09-27T02:03:31Z. Rama verificada: `codex/cierre-plan-pendiente`.

## Estado y versiones

Esta propuesta no se ha incorporado al corpus y no autoriza cierres, censos, firmas, controles ni disposiciones. Está pendiente del dictamen nominal de `/root/revision_residuales/candidatos_editoriales`. Durante la preparación de las huellas, el revisor empezó por el borrador que ya estaba visible en el espacio compartido; se conserva exactamente esa captura, no se sustituyen sus conclusiones por la versión ampliada.

| Artefacto | SHA-256 | Alcance |
| --- | --- | --- |
| PROPUESTA_AUTOR_6_CELDAS_S240_S352_BORRADOR_2026-09-27.json | 3fc812472be6573c6fe372e65abe932b859491a8cf31544e9db7fa9edef21b1d | Borrador exacto inspeccionado inicialmente por el revisor, conservado desde el snapshot autoral. |
| PROPUESTA_AUTOR_6_CELDAS_S240_S352_2026-09-27.json | 20bc4ed7cd09c556044b8f5f99c93337b8a5519d66420b2b8f84ab62165065ca | Mismas C/F/B y seis textos; añade huellas, UTC de materialización, designación del revisor y tres párrafos propuestos. |

La comparación JSON de las claves comunes da **cero diferencias**. La segunda versión no es una corrección científica del borrador. Ambas quedan inmóviles; cualquier reparación se presentará en versión nueva.

Raíz ya comunicó un **NO_CONFORME contextual preliminar** sobre C-2842: la declaración narrativa general de S352 debe confrontarse con el componente Patched y los dominios Hedge/Hog de Fig. 4. La formulación de ausencia sin excepción, fuerza alta y resolución resuelta de la propuesta no debe incorporarse mientras no se resuelva esa contradicción nominal. Este informe conserva el problema, no lo transforma en una aprobación condicionada.

Además, para la futura v2 raíz ha indicado dos requisitos de integración que **v1 no cumple aún**: todas las altas C deben ir al final de `data/afirmaciones/15.csv`, y los textos de las celdas deben contener las citas explícitas a las C que los sostienen. Se espera el dictamen completo antes de reparar.

## Objetos propuestos

El JSON contiene campos canónicos completos para siete altas C reservadas C-2839–C-2845, tres correcciones C antiguas, seis reemplazos de celdas con las filas C residuales antes/después, tres altas F, una corrección F y diez altas B. No se han añadido esas filas a producción.

| Celda / BN histórica | Componente que propone recuperar | C científicas de la propuesta |
| --- | --- | --- |
| C-2708 / BN-473, table43 fila CSV 7, genoma comparado | Tamaño nuclear estimado de Perkinsela ~9.5 Mbp y comparando libre Bodo saltans 39.9 Mbp; sin cociente propio ni dato mitocondrial | C-1037 corregida, C-2839 |
| C-2709 / BN-474, misma fila, EGT/importación | Ocho candidatos de EGT en 3,846 alineamientos con filogenias interpretables; captación de metabolitos y posiblemente enzimas como hipótesis explícita | C-2840, C-2841 |
| C-2468 / BN-329, table54 fila CSV 7, Monosiga | Declaración nominal de Suga sobre receptores/ligandos Hedgehog, pendiente de resolver contexto Fig. 4 | C-2842 |
| C-2469 / BN-330, misma fila, Capsaspora | Declaración nominal por organismo sobre receptores/ligandos Hedgehog, no todos los componentes de la vía | C-2843 |
| C-2474 / BN-334, table54 fila CSV 8, Monosiga | Declaración nominal limitada a familia Rhodopsin de GPCR; otras familias sin adjudicar | C-2844 |
| C-2475 / BN-335, misma fila, Capsaspora | Misma restricción por organismo y subfamilia; no ausencia global de GPCR | C-2845 |

Los números de fila son físicos CSV, contando cabecera: fila 7 equivale a índice de datos 5 y fila 8 a índice 6. Los índices de objetos en el bloque de huellas JSON son base cero.

Las seis BN y sus resultados históricos se mantienen **intactos**. Un soporte semántico nuevo no cambia una consulta literal histórica a resultado positivo ni modifica `POSITIVE_CLAIMS`. La propuesta de reemplazar las C de celda por síntesis de las C científicas requerirá una disposición explícita auditada; no se ha implementado.

## Correcciones antiguas incluidas

- C-1037: sustituir “mide aproximadamente 9,5 Mb” por una atribución explícita de la **estimación publicada ~9.5 Mbp**. F conserva grafía/unidad originales, clasifica el tamaño estimado como inferido y no añade intervalo.
- C-1040: separar lo observado por microscopía —invaginaciones y vesículas— de la interpretación de endocitosis. La captación de enzimas del hospedador queda en C-2841 como hipótesis, no importación dirigida demostrada.
- C-1581: se propone síntesis de las dos C nominales Hedgehog y localizador real de S352; esa síntesis también depende del dictamen sobre C-2842. No puede retenerse como aprobada si una dependencia es rechazada.
- C-1041, seis genes mitocondriales de Perkinsela citando S241, se preserva fuera de alcance. No se restaura en la celda comparativa y **no se declara falsa**; S241 no fue revisada en este lote.

Las tres altas F separan el valor Bodo, el recuento de candidatos y el denominador de alineamientos. No se calculan porcentajes ni cocientes. La clasificación propuesta “observado” para el valor comparativo de Bodo significa valor registrado en la tabla, **no** una medición nueva ni revisión del método de la referencia 25; se señala expresamente esa limitación para la revisión independiente, sin llenar el campo con un método no inspeccionado.

## Fuentes y localizadores leídos

| Fuente local | SHA-256 |
| --- | --- |
| fuentes/S240 [2017] Genome sequencing reveals metabolic and cellular interdependence in an.xml | f48e9fa6e660c47322028ce349c68cc77429c9a45e18269023ab033a00068ad7 |
| fuentes/S352 [2013] The Capsaspora genome reveals a complex unicellular prehistory of anim.xml | 7c62b5db6668fc64d252e5e0621fbb0831be592eda21d90895594c6eb8e23f6c |

S240: Results and Discussion, Endosymbiont and host nuclear genome sequencing (Par7); Biology of a kinetoplastid endosymbiont (Par10 y Table 1, fila Genome size (Mbp), columna Bodo saltans); Host-endosymbiont interactions (Par14 y Par16). S352: Results, Gene repertoire of Capsaspora, cuarto párrafo hijo directo de la sección, con remisión a Fig. 4. El encabezado “Signalling pathways” usado por C-1581 no es ese encabezado JATS.

El JSON preserva los seis pasajes completos normalizados, selectores y SHA de pasaje; incluye también las filas históricas de BN y residuales. El soporte numérico de Bodo depende de una tabla y se marca “requiere inspección humana”. No se han descargado fuentes nuevas para esta propuesta.

## Comprobaciones autorales y límites

Se comprobaron estructura JSON, siete IDs distintos, encabezados canónicos C/F/B, ausencia de duplicación exacta de las diez etiquetas B propuestas, coincidencia de las filas antiguas con el repositorio vivo, localización de las seis celdas y de las seis BN, reproducción de los seis pasajes desde XML y coincidencia de SHA de ambas fuentes. También se verificaron las huellas de los objetos y los tres párrafos antes/después propuestos. Son controles de preparación del autor, **no evidencia de independencia ni dictamen científico**.

Quedan fuera de este lote la reparación de las otras celdas de table54 —incluida la cifra 235 de dominios que no puede convertirse en recuento GPCR—, la clausura de BN-134/BN-140, la antigüedad de otros casos y cualquier aprobación integral de tablas o controles. Antes de integrar se requiere dictamen independiente de la propuesta exacta, v2 para los defectos detectados, nueva revisión nominal y disposición explícita conservadora del historial. Los derivados, manifiestos, recuentos y verificaciones se regenerarán por raíz sólo después de esa secuencia.
