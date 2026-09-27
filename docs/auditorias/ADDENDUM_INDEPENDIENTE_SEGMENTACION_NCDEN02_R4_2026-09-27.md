# Reinspección independiente R4: reparación técnica acotada conforme

Revisor: `/root/inspeccion_relojes`; implementación: `/root/verificacion_fuentes_nuevas`. El revisor no participó en el código ni en sus reparaciones. Rama: `codex/cierre-plan-pendiente`. Ejecución adversaria propia: 2026-09-27T03:57:22Z–03:57:28Z. Emisión: 2026-09-27T03:59:02Z, tras suite completa y comprobación final de huellas.

**CONFORME_REPARACION_TECNICA_ACOTADA_VERSION_R4.** Los defectos nominales reproducidos en las versiones inicial, R2 y R3 ya no se reproducen sobre esta versión. Las tres NC anteriores se conservan intactas y continúan identificando correctamente sus versiones rechazadas. Esta conformidad no adjudica el censo de oraciones ni cierra NC-DEN01, los controles globales o `make verify`.

## Objetos fijados

- `scripts/build_content_trace.py`: SHA256 `f6f808cf1102901616ca8e77984f4c4e5db11493d902169b0e35ca334f1f3854`.
- `tests/test_content_trace_sentence_boundaries.py`: `9d1a9545f7f2bd39e436de7c9d451eec4fc3551a65f65a354c015d43f5264296`.
- Fixture propia nueva `fixtures/reinspeccion_independiente_segmentacion_ncden02_r4_20260927.py`: `d2df5fb1aca319580204e404d36e8b117d66b5db9a59d1989c6fcd042cadafa6`.
- Evidencia `EVIDENCIA_INDEPENDIENTE_SEGMENTACION_NCDEN02_R4_2026-09-27.json`: `18ad00fe94f49360a824e6fb40542d462a062957e652134ba142272aa583e67d`.

Se leyó la entrega autoral R4 completa y el delta vivo. El cambio productivo recorta del sufijo de la máscara URL los signos terminales y cierres consumidos por el segmentador; no agrega exenciones, firmas, exclusiones editoriales ni modifica validadores de C/celdas. Se cotejó la interacción con el reconocimiento de citas y enlaces, los spans y los diagnósticos de abreviaturas. Las ejecuciones descritas aquí son del revisor, no las reejecuciones del autor.

## Regresiones y adversarios nuevos

| Ejecución propia | Checks | Pipelines reales |
| --- | ---: | ---: |
| Fixture inicial intacta | 63/63 | 9/9 |
| Fixture R2 intacta | 21/21 | 8/8 |
| Fixture R3 intacta | 40/40 | 27/27 |
| Fixture nueva R4 | 20/20 | 60/60 |

La nueva fixture combina cierres anidados, taxón en cursiva, URI con paréntesis/apóstrofos/decimales y fragmentos, URL codificada, dos URLs en una oración, autolink angular con punto literal, cita enlazada con ruta que contiene espacios, citas pospuestas múltiples, inicios numéricos/minúsculos y el marcador `[SIN FUENTE]`. Se conservaron los offsets Unicode exactos sobre el texto de entrada, incluida separación NBSP+tab; los segmentos son slices exactos y no desaparece contenido no blanco.

Cada caso nuevo se ejecuta en tres variantes: C propia en ambas oraciones, C retirada sólo de la primera y C retirada sólo de la segunda. Los veinte positivos producen exactamente dos segmentos con referencias propias. Las cuarenta variantes con una C retirada fallan sin escribir el CSV. Se usan el `main` real y sus comprobaciones, redirigiendo únicamente rutas y argv a temporales. No se sustituye ningún resultado del validador.

Las seis variantes URL+cierre de R3 ahora exponen correctamente la oración sin C y bloquean. Los casos previos de cierres tras cita, elipsis Unicode, iniciales/abreviaturas ambiguas y citas/enlaces incompletos siguen resolviéndose o bloqueándose según el contrato. La gramática nominal de enlaces ya no protege prosa desnuda como destino o título. No se convierte una referencia presente en prueba de fidelidad científica.

Se reejecutaron también las 46 pruebas focalizadas vivas (0.354 s) y las 335 de la suite completa (25.796 s): todas pasan. `git diff --check` del código y tests devuelve 0. Los resultados mecánicos se limitan a lo ensayado; no prueban un parser Markdown universal ni eliminan toda posible ambigüedad lingüística.

## Determinismo, aislamiento e idempotencia observados

Tres procesos propios con `PYTHONHASHSEED=2,29,977` producen el mismo SHA de spans/diagnósticos del nuevo conjunto: `ef03eff9ebe4363b06fdab77e7002f223a631afae006125cdd4358a1f7411982`. Las 60 ejecuciones temporales conservan sus entradas y el artefacto no cambia entre escritura y `--check`; los casos rechazados no escriben. Los hashes de todas las entradas relevantes, código, fixtures y traza canónica permanecieron iguales antes/después de la inspección y después de la suite.

Dos construcciones del censo vivo exclusivamente en memoria produjeron el mismo SHA `169f0b302ab4ebcec88865e4de6aee63c376964eeb7bb943405738aec234052d`. No se ejecutó el `main` sobre producción, no se escribió la traza canónica ni se regeneraron derivados. Esto verifica aislamiento e idempotencia para estas ejecuciones, no la verificación aislada integral solicitada por el usuario.

## Pendiente que esta revisión no cierra

El censo provisional conserva 4793 segmentos: 2129 narrativos/aristas y 2664 celdas. Hay 42 unidades sin C y 186 bloques con 192 fronteras pendientes (189 abreviaturas terminales posibles, tres iniciales). El manifiesto no arroja errores; la puerta mantiene el fallo de las 42 unidades. No se adjudicó ninguna frontera ni se declaró científicamente errónea una unidad sólo por estar expuesta.

Faltan el consumidor de adjudicaciones/densidad conforme al contrato prospectivo, las lecturas independientes nominales y los derivados finales correspondientes. NC-DEN01 sigue abierta. Este informe no aprueba ciencia, localizadores, corpus, R0393/R0394, censo semántico, segundas revisiones ni controles manuales. Los tres rechazos precedentes conservan sus SHA `694d4ce…930f`, `b74fd82…f4f9` y `d6ce641…ee35`; sus huellas completas están en la evidencia nueva.
