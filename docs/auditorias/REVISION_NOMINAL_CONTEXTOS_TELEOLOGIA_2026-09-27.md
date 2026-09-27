# Revisión independiente nominal de contextos teleológicos

Revisor: `/root/verificacion_fuentes_nuevas`. Rama observada: `codex/cierre-plan-pendiente`.

Dictamen limitado: las 95 ocurrencias de las 74 líneas candidatas fueron leídas y adjudicadas individualmente. No se identificó una afirmación teleológica afirmativa en esas ocurrencias y contextos. Esto no acredita ciencia, fuentes, fechas bibliográficas, ausencia universal de teleología fuera del léxico buscado, los controles R-0001–R-0007 ni el cierre global.

## Evidencia nominal y contexto

La adjudicación se fijó a las `2026-09-27T02:18:27Z` en `censo_contextos_teleologia_v1_2026-09-27.json`, SHA256 `b206dc433fba33bb51642ef543ab6027aad9cf571e0271d43d0b46736bb2ab8d`. Se conserva sin modificaciones.

La versión consumible `censo_contextos_teleologia_v2_contexto_2026-09-27.json`, SHA256 `30b0de4813c5c30c54d751f89ab86d359e1c884b3ff9078c0ca74bcb2c2bb029`, añade las huellas SHA256 de bytes de las 123 rutas del ámbito y la fecha real del snapshot `2026-09-27T02:23:36Z`. Todas las rutas están incluidas, también las que no contienen candidatos. Las capturas antes y después del cotejo fueron iguales, y las 74 líneas/95 ocurrencias siguieron coincidiendo exactamente con v1. Los motivos y la fecha original de adjudicación se preservan.

El snapshot fija el contexto del que depende la interpretación —por ejemplo, el cuerpo crítico de un apartado cuyo encabezado nombra «organismo simple»—, pero no declara una lectura científica exhaustiva de las 123 rutas. Un cambio de esos bytes obliga a reexaminar la vigencia del expediente; no autoriza copiar las huellas nuevas sin revisión.

## Método y resultados

El inventario fue mecánico; no adjudicó. Se leyeron todas las líneas completas, las celdas CSV correspondientes y el contexto pertinente. Para los encabezados terminológicos se leyó el cuerpo de cada apartado. Para «corredor superior» se cotejaron las afirmaciones C-1716/C-1718 y la tabla de códigos, distinguiendo inclusión taxonómica de progreso evolutivo. La comparación C-1462 se interpretó por su sujeto —resolución de evidencia—, sin afirmar aquí la corrección científica de esa comparación.

Cada una de las 95 ocurrencias tiene offsets Unicode de Python (fin excluido), literal, celda o cláusula, dictamen y motivo propios. El texto completo de cada línea queda ligado por SHA256 de UTF-8(texto + LF). La distribución resultante es:

- 24 usos cuantitativos: umbrales, rangos o comparaciones de magnitudes explícitas.
- 12 usos técnicos no teleológicos: inclusión taxonómica, unidades o límites estratigráficos y comparación de clases de evidencia.
- 49 críticas terminológicas: palabras nombradas para cuestionar su uso, delimitarlo o proponer un reemplazo.
- 10 citas o atribuciones históricas: términos como objetos de discusión o búsquedas de acuñación; la adjudicación no valida la fecha o atribución histórica buscada.

No hay una exención por ruta, por título de sección, por presencia de «criterio» ni por otra palabra de la línea. El contexto de cada ocurrencia consta explícitamente. La clasificación positiva no se obtuvo aplicando reglas automáticas a estas categorías.

## Independencia

La declaración por entrada es `REVISION_INDEPENDIENTE_DE_CONTEXTOS_SIN_AUTORIA_DEL_TEXTO`; `conflicto_autoria` es `NO` en las 74 entradas. Se revisó el historial de participación propio: las inspecciones previas de identidad bibliográfica y de fuentes no supusieron redactar estas líneas. Las propuestas anteriores sobre S434/C-2783 no aparecen entre las candidatas actuales. El revisor no editó aquí el corpus ni el detector.

## Límites y no conformidades que no se cierran

Las NC-TEL-01 y NC-TEL-02 del informe `NO_CONFORMIDADES_CONTROL_TELEOLOGICO_2026-09-27.md` siguen siendo hallazgos reales del detector inspeccionado allí. Este ledger no repara ni aprueba su consumidor. No se cierra ninguna de esas NC por obtener 95 adjudicaciones positivas: la reparación del código requiere pruebas adversarias y revisión técnica independientes.

Tampoco se firma ningún control global, censo semántico C/S, segunda revisión científica, disposición científica ni resultado de `make verify`. Los hechos numéricos e históricos usados como contexto no se verifican científicamente en este trabajo.

## Utilidades reproducibles

- `fixtures/inventario_teleologia_20260927.py`, SHA256 `7e85c49c3a288f49957616d22ad5773060473cbaea9475d80199a0ef0ac7ad57`: extracción de texto, offsets y contexto, sin dictamen.
- `fixtures/snapshot_contexto_teleologia_20260927.py`, SHA256 `b8d94bdebdd710ffa0686d9e5da5f34e4a72c3ca51d7434b54c6cd2bdf29ed4a`: cotejo de las adjudicaciones ya fijadas contra el corpus y doble captura de las 123 huellas; tampoco genera dictámenes.

Estas utilidades comprueban identidad textual y población, no sustituyen la lectura nominal ni constituyen evidencia científica automática.
