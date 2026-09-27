# Entrega autoral R4: URL seguida de cierre de cita o formato

Autor: `/root/verificacion_fuentes_nuevas`. Fecha real de emisión: 2026-09-27T03:51:20Z. Rama: `codex/cierre-plan-pendiente`. **Pendiente de revisión independiente; no cierra NC-DEN02.**

Se conserva intacto el rechazo R3 de `ee13ebaafe7b6322975be9dcee846c59575e925126733be5dc2f7f23764e625a`: informe independiente SHA256 `d6ce641fb1eebcba6737939be88732543f0a56b94cba92b3b7468d2d8e7bee35`; evidencia `7cd23c70aacbdc17e9d3b039213ac69869509ca699834b9dfcb3c3f2e99d651e`. También se conservaron sus fixtures y todos los rechazos previos.

## Reparación limitada

El sufijo de una URL podía incluir un cierre `’`, `›`, apóstrofo ASCII, asterisco, guion bajo o acento grave. El recorte anterior no retiraba esos cierres, por lo que protegía indebidamente el punto terminal precedente y fusionaba la oración siguiente.

`sentence_masks` ahora recorta del extremo de ese token el mismo conjunto de signos terminales y cierres que consume `sentence_spans`. No se cambia el interior de la URL: dominio, ruta, consulta, decimales y apóstrofos/marcadores interiores siguen protegidos. No se reescriben los textos ni se comprueba que las URLs resuelvan. El cambio productivo consiste en una expresión de recorte y su explicación; no altera las restantes comprobaciones de C, el esquema persistente, las exclusiones editoriales ni las reglas de ambigüedad.

## Pruebas realizadas por el autor

- 46 tests focalizados: OK, 0.401 s. Cuatro tests nuevos cubren nueve envoltorios × cuatro terminadores × dos separadores (72 variantes con conservación de offsets), citas pospuestas múltiples, cinco URLs con puntuación interior y 18 pipelines `main`/`--check` aislados. Se comprueba tanto que la primera oración no herede la C de la segunda como el caso inverso; los positivos tienen C propia en ambas.
- Suite completa: 335 tests, OK, 27.082 s.
- Reejecución autoral, de 03:50:53Z a 03:50:59Z, de las fixtures independientes intactas: inicial 63/63 comprobaciones y 9/9 pipelines; R2 21/21 y 8/8; R3 40/40 y 27/27. Se inspeccionan los resultados nominales, no sólo exitcode. Las identidades estáticas de las fixtures se separan del ejecutor real en el JSON: estas corridas no son aprobación independiente.
- Tres semillas `PYTHONHASHSEED` (1, 17, 981) producen la misma huella del conjunto sintético. Las entradas antes/después permanecieron idénticas.
- `git diff --check` de los archivos propios: sin errores.

## Censo en memoria, sin regeneración

Dos materializaciones sucesivas dieron exactamente el mismo payload provisional `169f0b302ab4ebcec88865e4de6aee63c376964eeb7bb943405738aec234052d`, igual al registrado por el censo R3. No se tomó 4793 como objetivo: resultaron 2129 segmentos narrativos/aristas y 2664 celdas, 42 segmentos sin C y 186 bloques con 192 fronteras ambiguas (189 abreviaturas, tres iniciales). El manifiesto no mostró errores. Estas fronteras no se adjudicaron ni se reinterpretaron como infracciones científicas.

La traza persistente conserva SHA256 `525e1d5efb16c6b1be6e1cf5e2bed53d025d87cd4c2d9b06ab75a75d5c12fe0d`. Ningún artefacto de producción se regeneró; los pipelines sólo escribieron temporales. Los textos/spans nominales históricos continúan en el censo R3, ligado por huella y sin reconstruir su fecha.

NC-DEN01 sigue abierta. Esta entrega no aprueba ciencia, densidad por oración, R0393/R0394, censos, segundas revisiones ni `make verify`. La ausencia de variantes problemáticas en el texto vivo no exime el fallo sintético; el revisor debe repetir su propia evaluación sobre esta nueva versión.

## Huellas de la entrega

- `scripts/build_content_trace.py`: `f6f808cf1102901616ca8e77984f4c4e5db11493d902169b0e35ca334f1f3854`.
- `tests/test_content_trace_sentence_boundaries.py`: `9d1a9545f7f2bd39e436de7c9d451eec4fc3551a65f65a354c015d43f5264296`.
- `fixtures/reejecucion_autoral_segmentacion_r4_20260927.py`: `3622c27f3e3519882f6ef624ba654ba3ac1f8340e17d6d6e8d3a993d40bb11f4`.
- `pruebas_autorales_segmentacion_r4_2026-09-27.json`: `06f3ff107974728d25f92bc72178d41ca212be8bd3748deb64001a80b1224448`.
