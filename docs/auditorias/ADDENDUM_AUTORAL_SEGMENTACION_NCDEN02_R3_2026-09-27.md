# Entrega autoral R3: destinos y títulos de citas enlazadas

Autor: `/root/verificacion_fuentes_nuevas`. Rama: `codex/cierre-plan-pendiente`. Registro final de pruebas: `2026-09-27T03:25:05Z`. **Pendiente de reinspección independiente**; no es dictamen de conformidad ni cierre de NC-DEN02.

## Rechazo precedente preservado

El revisor fijó NO_CONFORME para `df72e57c7cfa7b0c9d3d6dd1d1457b3b5226af91c395841762a7326347422f8d`. Aunque sus casos iniciales ya pasaban, comprobó aceptación real de prosa indebidamente protegida como destino de enlace, rechazo de destinos/títulos válidos y asignación errónea de una comilla curva al segmento siguiente. Sus tres artefactos permanecen intactos:

- `ADDENDUM_INDEPENDIENTE_SEGMENTACION_NCDEN02_R2_2026-09-27.md`: `b74fd820776c197db516846e1dedb2c888c2024c5a18d5313cca5ff013afd4f9`.
- `EVIDENCIA_INDEPENDIENTE_SEGMENTACION_NCDEN02_R2_2026-09-27.json`: `ca25152de3ca352cdeb9871aac30a95b16078d2aae1bee660381680e95ebf536`.
- `fixtures/reinspeccion_independiente_segmentacion_ncden02_20260927.py`: `c08afdffe443406a19f1256fea89c9e47c890092fb23c2418b8f526a42e10239`.

No se reescribieron tampoco el rechazo inicial, las entregas autorales anteriores ni sus censos.

## Delta

`inline_link_end` reconoce por separado destino desnudo, destino angular y título opcional. Exige los delimitadores correspondientes; un paréntesis equilibrado ya no basta. Distingue escapes de puntuación, espacios/controles ASCII y separadores con como máximo un salto de línea; los títulos no admiten líneas vacías. Los paréntesis literales dentro de títulos entre comillas o destinos angulares no se balancean como los del destino desnudo. La referencia técnica consultada fue [CommonMark 0.31.2, §6.3](https://spec.commonmark.org/0.31.2/#links).

La función se limita a componentes de una cita nominal enlazada: no es un parser completo de Markdown, no resuelve referencias de enlace ni comprueba que un destino exista. Una forma no reconocida no se protege como enlace: queda sujeta al rechazo de cita/enlace incompleto o sintácticamente inválido. Los textos de título y destino tampoco se promueven a evidencia científica.

Se añadieron los cierres `’` y `›` al conjunto consumido tras puntuación/cita. Los demás controles de C, celdas, contenido y ambigüedad siguen activos. No se introdujeron exenciones ni cambios de esquema. El tratamiento sigue operando sobre el texto recibido; el pipeline narrativo conserva su normalización previa, por lo que los spans del censo no son offsets del archivo bruto.

## Pruebas

- 42 pruebas autorales: OK, 0.103 s. Se incluyen seis tests nuevos con múltiples subcasos de destinos/títulos válidos e inválidos, escapes, CR/LF/CRLF, líneas vacías, límites de controles y seis pipelines reales en directorios temporales.
- Suite viva completa: 331 pruebas, OK, 25.299 s.
- `git diff --check -- scripts/build_content_trace.py`: sin errores.
- Reejecución **por el autor** de la fixture R2 intacta a `2026-09-27T03:24:04Z`: 63/63 comprobaciones y 9/9 pipelines iniciales; 21/21 comprobaciones y 8/8 pipelines adicionales. Huellas antes/después estables. No se presenta esa ejecución como aprobación del revisor cuyo nombre está codificado en la fixture: el envoltorio JSON identifica al ejecutor real y separa esos campos estáticos.

## Censo en memoria y pendientes

A `2026-09-27T03:24:22Z` se obtuvieron de nuevo 4793 segmentos provisionales: 2129 narrativos/aristas y 2664 celdas; 42 segmentos expuestos sin C; 186 bloques con 192 fronteras pendientes. Las entradas fueron idénticas antes/después, el manifiesto de celdas no dio errores y la traza persistente quedó intacta. No se forzó ese recuento ni se adjudicaron las ambigüedades. La comparación histórica y los textos/spans nominales quedan en el JSON nuevo.

No se editó canon, fuentes, ledgers, firmas ni `audit_requirement_controls.py`, y no se regeneró producción. Los pipelines de prueba sólo escribieron en temporales.

Faltan reinspección independiente de esta versión, adjudicación nominal de fronteras/candidatos y la puerta acumulativa de densidad. **NC-DEN01 permanece abierta**. Nada de esta entrega aprueba ciencia, localizadores, R0393/R0394, §16, censos, segundas revisiones ni `make verify`.

## Huellas R3

- `scripts/build_content_trace.py`: `ee13ebaafe7b6322975be9dcee846c59575e925126733be5dc2f7f23764e625a`.
- `tests/test_content_trace_sentence_boundaries.py`: `f4af0a0cdd179b40e761c0dcbe56095add09462665173d5db67856e3a9eb81b6`.
- `censo_autoral_segmentacion_r3_2026-09-27.json`: `79f75c6e14630ae2476a9864e50c0cde1ed6f4629a77d8777647f04ba44c4312`.
- `pruebas_autorales_segmentacion_r3_2026-09-27.json`: `cc6b47ffae16bfe93143a40e52ee1c4185f16cae35b3f4f9e6915ba8b4fa5bcc`.
- Fixture autoral reutilizada para el censo, sin editar: `fixtures/censo_autoral_segmentacion_reparada_20260927.py`, `073164b42b08e430a15d6b98c8161f5a1b153dbaff93ad6672a3e248eb92e11d`.
