# Addendum autoral: reparación posterior al rechazo independiente de NC-DEN02

Autor del parche y de esta entrega: `/root/verificacion_fuentes_nuevas`. Rama: `codex/cierre-plan-pendiente`. Fecha de fijación de pruebas: `2026-09-27T03:14:37Z`. **Pendiente de reinspección independiente.** Este documento no revoca ni reescribe el dictamen NO_CONFORME de la versión anterior.

## Antecedente preservado

La revisión independiente inspeccionó el constructor `a1d865203b93016ac979ce54aa405c0e907d926ab9aa064046383d1d00f3d6f6` y obtuvo 49/63 comprobaciones y 3/9 pipelines conformes. Su informe, evidencia y fixture se conservaron sin editar:

- `REVISION_INDEPENDIENTE_SEGMENTACION_NCDEN02_2026-09-27.md`: `694d4cebae68bf0f6cd96a92993e137cdba6d203cca6e3c1f90e562ab8fe930f`.
- `EVIDENCIA_INDEPENDIENTE_SEGMENTACION_NCDEN02_2026-09-27.json`: `da9650f37c22c9fc975b0164171b3f5cd14a27e23a8553163e615356e6411483`.
- `fixtures/revision_independiente_segmentacion_ncden02_20260927.py`: `7c046b65b22b57ac6d15ebfdb74a3fd0eebd7eb9ef6e26500e39dd24be3ac573`.

También permanecen intactos la entrega autoral inicial, su censo y el diagnóstico original de R0393. Los defectos conexos encontrados por el revisor no se atribuyen retrospectivamente, sin prueba, al primer delta.

## Cambios implementados y límites

1. El segmentador consume cierres de paréntesis, comillas y formato también **después** de cada cita pospuesta. Una cita seguida por un enlace Markdown incluye su destino balanceado, con paréntesis anidados y escapes. La adyacencia `. [C-001]Otro` ya no permite prestar esa C a la segunda oración. Los grupos consecutivos siguen perteneciendo a la oración anterior.
2. La elipsis Unicode `…` se trata como signo terminal, igual que la elipsis ASCII ya contemplada. No se declara con ello resuelta toda ambigüedad lingüística de una elipsis.
3. Una abreviatura protegida que deja contenido posterior separado ya no puede aprobar silenciosamente un bloque fusionado. Se conserva la segmentación provisional y se informa `AMBIGUA_ABREVIATURA_TERMINAL`, con las lecturas de corte y abreviatura y sus spans exactos. Se incluyen casos con cierre, formato, número o `[SIN FUENTE]` posterior: ninguno de esos rasgos permite decidir la lectura ni prestar una C por proximidad. El diagnóstico es conservador, no una adjudicación de que cada punto sea realmente terminal.
4. Las formas inequívocamente delimitadas por cursiva `_B. floridanus_`, además de `*B. floridanus*`, conservan el token. No se extiende esa protección a cualquier inicial seguida de minúscula ni a la negrita: las lecturas ambiguas siguen explícitas.
5. La validación de prosa rechaza una cita nominal o enlace cuyo cierre no se localiza, aunque dentro aparezca una C reconocible. El reconocimiento léxico de la clave no subsana una cita incompleta.

Se mantienen las comprobaciones previas de C, tombstone, fragmentos espurios, correspondencia de celdas y contenido. No se añadieron rutas, frases ni tipos editoriales exentos. El esquema persistente sigue teniendo las mismas diez columnas. Los offsets son Unicode sobre el texto recibido; en el censo proceden de bloques normalizados y **no son offsets de bytes ni del archivo Markdown original**.

`main` bloquea tanto los segmentos sin C como las fronteras no adjudicadas. No existe aún un consumidor de adjudicaciones nominales que autorice esas fronteras. Esta entrega no los fabrica, no modifica la prosa para evitarlos y no trata la ambigüedad como infracción científica.

## Pruebas autorales reales

Ejecución registrada entre `2026-09-27T03:13:57Z` y `2026-09-27T03:14:37Z`:

- Módulo autoral: 36 pruebas, 0.026 s, OK.
- Suite viva completa: 325 pruebas, 36.800 s, OK.
- `git diff --check -- scripts/build_content_trace.py`: sin errores.

Las diez regresiones nuevas añaden cierres posteriores y anidados, cierres entre citas múltiples, adyacencia, enlaces anidados/escapados, elipsis Unicode, cursiva con subrayado, límite de negrita, alternativas de abreviatura terminal y citas/enlaces incompletos. Los casos de cortes, spans y conservación de texto de la entrega inicial siguen ejecutándose.

Reejecuté personalmente la fixture **ajena e intacta** a `2026-09-27T03:13:35Z`: 63/63 comprobaciones y 9/9 pipelines pasan; archivos revisados estables. Esa ejecución es **autoral**, no una segunda aprobación independiente. El JSON envolvente declara al ejecutor real y aparta expresamente los campos estáticos de identidad que emite la fixture original, para que no se confundan con la identidad de quien la reejecutó. El revisor debe ejecutar y juzgar la nueva versión por separado.

## Censo vivo en memoria

Ejecución real: `2026-09-27T03:12:50Z`. Las entradas se fijaron y compararon antes/después. No se escribió la matriz de trazabilidad guardada.

- 1824 segmentos narrativos/aristas históricos frente a 2129 provisionales nuevos; 2664 celdas sin cambio; 4488 frente a 4793 segmentos totales.
- 224 bloques con variación de segmentación/localización/contenido frente a la función histórica.
- 42 segmentos expuestos sin C propia, igual recuento que en la entrega inicial. No son 42 infracciones científicas adjudicadas.
- 186 bloques con 192 fronteras pendientes: 189 `AMBIGUA_ABREVIATURA_TERMINAL` y tres `AMBIGUA_INICIAL_EPITETO`.
- Manifiesto de celdas sin errores; entradas estables; traza persistente intacta.

El aumento de diagnósticos respecto de las tres iniciales anteriores procede del reconocimiento explícito del límite de las abreviaturas protegidas. Incluye usos que una lectura nominal puede resolver como abreviatura; el programa no los exime por `et al.`, `sp.` o `p.` ni decide por la presencia de C en el resto del bloque. Las dos lecturas se conservan para esa adjudicación futura, no para fijar un objetivo de recuento.

La fixture nueva reutiliza el cálculo inicial intacto y elimina únicamente la repetición del literal largo de cada frontera: el bloque completo, los spans y la huella del literal redundante permanecen en el expediente. No se omiten fronteras ni segmentos sin C.

## Huellas de esta entrega

- `scripts/build_content_trace.py`: `df72e57c7cfa7b0c9d3d6dd1d1457b3b5226af91c395841762a7326347422f8d`.
- `tests/test_content_trace_sentence_boundaries.py`: `85fb7aeb4418b4602fb50a44ebca0787031fa054800de074840894737c8d3921`.
- `fixtures/censo_autoral_segmentacion_reparada_20260927.py`: `073164b42b08e430a15d6b98c8161f5a1b153dbaff93ad6672a3e248eb92e11d`.
- `censo_autoral_segmentacion_reparada_2026-09-27.json`: `a52c61cd0abcdec937581ee7cefe003dff9f6409b4e995558a0c29cbaa74adc8`.
- `pruebas_autorales_segmentacion_reparada_2026-09-27.json`: `4a6f711684ab3cee7c80c8412bfbcc3339199e43f1c893ea1df350aa0d68ea58`.

## Pendientes y no aprobación

No se editó el corpus, las fuentes, los censos/firmas reales, `audit_requirement_controls.py` ni los artefactos del revisor. No se regeneraron derivados de producción. Los pipelines de prueba sólo escribieron en directorios temporales.

Faltan reinspección independiente de este código, adjudicación nominal de fronteras y candidatos, y la puerta acumulativa de densidad. **NC-DEN01 sigue abierta**: disponer de C por oración no demuestra disponer de fuente/localizador por oración. La política de localizador honesto no se modifica ni se abre aquí el refinamiento posterior al cierre. Este addendum no aprueba R0393/R0394, §16, ciencia, censos, segundas revisiones ni `make verify`.
