# Revisión independiente de seis ocurrencias: teleología

Revisor: `/root/inspeccion_relojes`. Inspección: 2026-09-27T02:05:36Z–2026-09-27T02:07:41Z. No soy autor de estas seis proposiciones ni implementador del cambio contemporáneo del detector.

**Dictamen nominal de redacción: las seis ocurrencias son no teleológicas.** Esto no confirma las cifras, la fidelidad a las fuentes, las afirmaciones científicas completas ni el cierre de R-0001–R-0007.

| Objeto vivo | Expresión examinada | Razón contextual |
| --- | --- | --- |
| data/afirmaciones/15.csv:929, C-2825 | cuartil superior | El Motivo define un umbral sobre valores de identidad; la Afirmación cuenta clados. Ningún linaje es calificado como superior ni orientado a un fin. |
| data/afirmaciones/15.csv:935, C-2831 | identidad proteica superior al 70 % | La comparación es entre una magnitud individual y un umbral. La fila diferencia individuos y medias de grupo, sin jerarquía evolutiva. |
| data/apendices/F_magnitudes.csv:602, C-2825 | cuartil superior | El método clasifica por identidad clado–grupo hermano; “superior” modifica al cuartil, no al grupo procariota cuantificado. |
| data/apendices/F_magnitudes.csv:603, C-2826 | cuartil superior | Misma función estadística en la magnitud sobre clados eucariotas; no se predica superioridad de los eucariotas. |
| data/apendices/F_magnitudes.csv:604, C-2827 | cuartil superior | El filtro de origen plastidial delimita el denominador; la posición en la distribución no implica avance, propósito o destino de un linaje. |
| docs/secciones/010-09-9-asociacion-el-catalogo-de-desenlaces.md:569 | identidad proteica superior al 70 % | El párrafo atribuye el recuento de candidatos a Rossoni y colaboradores. El contexto mantiene denominadores e identidades individuales separados; no convierte la similitud proteica en progreso. |

Se leyó el literal antiteleológico de `docs/C01-PROMPT-INVESTIGACION.md:11`, las seis líneas completas y dos líneas anteriores/posteriores de cada una. Se descarta la lectura teleológica por el papel semántico de cada expresión en la proposición completa, no por una autorización genérica de la palabra “superior”.

Los textos exactos, contexto, SHA-256 de archivo/línea, coordenadas de las ocurrencias y UTC están preservados en `revision_redaccion_6_ocurrencias_teleologia_2026-09-27.json`, SHA-256 `8d1afd15d9dbc7e60908a17598620b00ffee0df152d954d8374b78afdc5aeb34`. Las tres huellas de archivo se comprobaron sin cambios al finalizar la inspección:

- C15: `e5fa927ad150cec64bb2d49d1d6d32180d2a02f13d97fb324833174a796aceac`.
- F: `04430032764e8e940abe33a9804a1663e9b7086dcab6c6c2feb7a0f1b9969110`.
- Prosa09: `4c3107d34a62d6b64941bd0adb453f841d90e693eb71f5bf7747240252958217`.

## Ejecuciones y límites

La primera ejecución real de `python3 scripts/audit_requirement_controls.py --classification` devolvió exit1 y esos mismos seis candidatos en los siete controles. La segunda, realizada para preservar stdout, ya encontró una modificación concurrente del detector y devolvió exit0; el código leído al final tuvo SHA `0200686fac33c6074c194ee7cfcc440a67e2e57fb96e207b573c6a330463f7ca`. Se conservan ambos hechos; no se inventa una huella retrospectiva del primer código ni se trata la segunda salida como prueba de determinismo del mismo estado.

La decisión lingüística autoriza como máximo una clasificación **por ocurrencia**. No autoriza ignorar la línea entera si contiene otra afirmación teleológica, ni nuevos usos de “superior” con otro sujeto. No se revisó el parche del detector ni se ejecutaron adversarios de ese cambio. Tampoco se consultaron S290/S561 para una segunda revisión científica en este lote. No se modificaron producción, validadores, matrices ni firmas.
