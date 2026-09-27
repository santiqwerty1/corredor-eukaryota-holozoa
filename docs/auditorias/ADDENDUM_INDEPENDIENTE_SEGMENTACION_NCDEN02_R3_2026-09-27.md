# Reinspección independiente R3 de NC-DEN02

Revisor: `/root/inspeccion_relojes`; autor del código: `/root/verificacion_fuentes_nuevas`. Sin participación del revisor en esta implementación. Se excluye su distinta autoría de propuestas científicas. Rama comprobada: `codex/cierre-plan-pendiente`. Ejecución propia: 2026-09-27T03:38:16Z–03:38:22Z; después se completaron la suite y el cotejo de huellas. Se preservan los dictámenes NC inicial y R2.

**Dictamen nuevo: NO_CONFORME**, limitado a segmentación y enlace de citas. Los arreglos anteriores pasan sus regresiones, pero queda una clase nueva que presta C entre oraciones. No se adjudica NC-DEN01, ciencia, densidad, controles globales ni `make verify`.

## Objeto exacto

- `scripts/build_content_trace.py`: SHA256 `ee13ebaafe7b6322975be9dcee846c59575e925126733be5dc2f7f23764e625a`.
- `tests/test_content_trace_sentence_boundaries.py`: `f4af0a0cdd179b40e761c0dcbe56095add09462665173d5db67856e3a9eb81b6`.
- Fixture nueva propia `fixtures/reinspeccion_independiente_segmentacion_ncden02_r3_20260927.py`: `bcd28ef26a623c33d7e573801e6a5fe1d91a48154fdd2eda0d39053f38ab1983`.
- Evidencia `EVIDENCIA_INDEPENDIENTE_SEGMENTACION_NCDEN02_R3_2026-09-27.json`: `7cd23c70aacbdc17e9d3b039213ac69869509ca699834b9dfcb3c3f2e99d651e`.

Se leyeron el delta, la entrega autoral R3 y el contrato prospectivo completo; las 331 pruebas del autor no se toman como aprobación. Se ejecutaron pruebas propias con el `main` real en directorios temporales. Sólo se redirigen raíz, manifiesto, salida y argv: no se reemplazan validadores ni resultados.

## R3-URL-CIERRE-01: una URL absorbe el cierre de oración

Entrada mínima entre comillas curvas pareadas:

```text
‘El dato consta en https://example.org.’ [C-001] Otra proposición sin cita.
```

Esperado: dos segmentos; el segundo sin C hace fallar la construcción. Si la frontera se considerase ambigua, el resultado admisible sería diagnóstico explícito y bloqueo, no una elección silenciosa.

Resultado real: un único segmento con C001, sin errores de payload ni diagnóstico de ambigüedad. `main` escribe el CSV y devuelve 0; la segunda ejecución con `--check` también devuelve 0. La última proposición hereda indebidamente la referencia anterior. No es falta de un localizador S ni prueba insuficiente de una C: el error ocurre antes, en la frontera.

La causa está en la combinación de `URL_TOKEN` y `sentence_masks`: el token incluye `’`, `›`, comilla simple, asterisco, subrayado o backtick, y la limpieza terminal de la máscara no los separa. Por ello protege el punto anterior como parte de la URL. Añadirlos sólo a `TERMINAL_CLOSERS` no basta: el bucle de segmentación nunca llega a examinar ese punto protegido. Se reprodujo la fusión con los seis cierres; los controles paralelos con comillas dobles, guillemets dobles y paréntesis sí separan correctamente y rechazan la oración sin C.

Estos casos sintéticos no establecen que exista hoy la variante en la prosa científica. Un probe separado de bloques narrativos, fuera de grupos de cita, encontró cero URLs con esas secuencias punto+cierre. Ello no sanea el comportamiento del consumidor ni autoriza una exención de datos futuros. La reparación deberá conservar también la puntuación interna legítima de URLs, los spans exactos y la ruta fail-closed.

## Resultados propios

| Grupo | Resultado |
| --- | --- |
| Fixture inicial, reejecutada sin editar | 63/63 checks, 9/9 pipelines |
| Fixture R2, reejecutada sin editar | 21/21 checks, 8/8 pipelines |
| Adversarios nuevos R3 | 34/40 checks; seis fusiones incorrectas |
| Pipelines nuevos R3 | 21/27; seis aceptaciones que debían bloquear |
| Tests focalizados vivos | 42/42, ejecución propia |
| Suite viva | 331/331, 32.735 s, ejecución propia |
| `git diff --check` del código/tests revisados | 0 |

Los casos nuevos incluyen destinos angulares vacíos/con espacios/escapes, destinos relativos y paréntesis, títulos delimitados con puntuación, rechazos de prosa desnuda o títulos incompletos, y tres ambigüedades de abreviatura/inicial. Todos éstos, salvo la clase URL+cierre, funcionan en la versión revisada. La evidencia conserva entradas, cortes esperados/reales, spans, diagnósticos y las salidas reales de los 27 pipelines nuevos. Los resultados completos de las reejecuciones históricas se identifican por SHA de JSON canónico; se registran sus conteos, estabilidad y listas de fallos vacías sin duplicar todo su texto.

## Determinismo, aislamiento y censo

Tres procesos con `PYTHONHASHSEED=1,17,981` produjeron el mismo SHA de spans y diagnósticos: `95dc6643d52d7051726d1ec1d9046d0dd3bf206d7915bf51c37a7020edcabaff`. Esto confirma determinismo para la muestra, no corrección de sus fronteras erróneas. Los pipelines temporales repiten construcción/check y comprueban que sus entradas no cambian.

La inspección independiente en memoria produjo 4793 segmentos provisionales (2129 narrativos/aristas y 2664 celdas), 42 sin C, 186 bloques con 192 fronteras pendientes: 189 posibles abreviaturas terminales y tres iniciales. No se adjudicó ninguna. Dos materializaciones dieron el mismo SHA `169f0b302ab4ebcec88865e4de6aee63c376964eeb7bb943405738aec234052d`; el manifiesto no produjo errores. La puerta conserva el fallo de 42 unidades sin C. La traza persistente y todos los archivos relevantes de entrada permanecieron iguales antes/después de la inspección y después de la suite completa.

No se ejecutó el `main` sobre producción, ni se regeneró una matriz, ni se cambió prosa, canon, fuentes o firmas. La corrección adicional requiere implementación por el autor y nueva reinspección de la versión exacta; las NC preservadas no se convierten en conformidad por recalcular huellas.
