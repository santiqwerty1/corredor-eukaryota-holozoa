# Addendum independiente R2: NC-DEN02 permanece no conforme

Dictamen: **NO_CONFORME** para scripts/build_content_trace.py SHA256 `df72e57c7cfa7b0c9d3d6dd1d1457b3b5226af91c395841762a7326347422f8d`. Se conserva el rechazo inicial sin reescribirlo.

Revisor: /root/inspeccion_relojes, sin participación en la implementación de /root/verificacion_fuentes_nuevas. Emisión: 2026-09-27T03:19:16Z. Rama: codex/cierre-plan-pendiente. No se alteraron implementación, contrato, prosa, canon, matriz persistente ni firmas.

## Ensayos propios

Reejecuté mi fixture inicial sobre el hash nuevo: 63/63 comprobaciones y 9/9 escenarios de main pasan ahora. No uso la reejecución autoral como aprobación.

La fixture nueva añade 21 casos (16 pasan y cinco fallan) y ocho escenarios de main (tres pasan y cinco fallan). Ejecutada realmente entre 2026-09-27T03:17:32Z y 2026-09-27T03:17:32Z. Código y entradas fijadas conservaron sus huellas. main se ejecutó en directorios temporales; sólo se sustituyeron rutas/argv, nunca validadores.

Reejecuté además las 36 pruebas dedicadas del autor: pasan. No ejecuté aquí la suite global ni make verify.

Objetos propios:

- Fixture: docs/auditorias/fixtures/reinspeccion_independiente_segmentacion_ncden02_20260927.py, SHA256 `c08afdffe443406a19f1256fea89c9e47c890092fb23c2418b8f526a42e10239`.
- Evidencia completa: docs/auditorias/EVIDENCIA_INDEPENDIENTE_SEGMENTACION_NCDEN02_R2_2026-09-27.json, SHA256 `ca25152de3ca352cdeb9871aac30a95b16078d2aae1bee660381680e95ebf536`.
- Tests del autor observados: `85fb7aeb4418b4602fb50a44ebca0787031fa054800de074840894737c8d3921`.
- Informe inicial intacto: `694d4cebae68bf0f6cd96a92993e137cdba6d203cca6e3c1f90e562ab8fe930f`.

## Nuevos hallazgos

### R2-01 — Cualquier paréntesis balanceado se convierte en supuesto enlace y oculta prosa

`Se observó. [C-001](La proteína actúa. Otra cambia.)`

citation_end consume todo el paréntesis como destino Markdown, aunque contiene prosa con espacios sin una sintaxis válida de destino/título. El resultado es una sola unidad con C-001; validate_payload no da errores, main escribe la traza y --check devuelve 0. Lo mismo ocurre con las variantes `[C-001](https://example.org La proteína actúa. Otra cambia.)` y `[C-001](<> La proteína actúa. Otra cambia.)`.

Es una aceptación indebida concreta, no una falta hipotética de cobertura lingüística. La nueva protección de enlaces pasa a ocultar puntos y proposiciones que siguen sin C propia. El conteo equilibrado de paréntesis no basta para reconocer la gramática de enlace.

El contraste normativo se hizo contra la sección 6.3 de [CommonMark 0.31.2](https://spec.commonmark.org/0.31.2/#links): el destino desnudo no admite espacios ASCII y el título opcional necesita delimitadores propios. No se exige implementar todo CommonMark: se exige no aprobar como enlace cualquier prosa entre paréntesis.

### R2-02 — Los títulos entre comillas y destinos angulares se balancean como si fueran destinos desnudos

Ejemplo válido de enlace: `Dato. [C-001](https://example.org "Figura (a") Otro. [C-002]`.

El paréntesis dentro del título entre comillas no necesita pareja. La implementación lo cuenta como anidamiento del enlace y termina dejando `Dato.` sin su cita. main rechaza pese a que las dos oraciones tienen su C. Se reproduce con título entre comillas simples y con destino angular `[C-001](<https://example.org/a(b>)`.

Son rechazos conservadores, no autopromoción; se distinguen de R2-01. La especificación citada delimita de manera diferente los títulos entre comillas y los destinos angulares. La lectura de cada variante debe conservar esa identidad o declarar un bloqueo nominal explícito, no llamarla un enlace truncado inexistente.

### R2-03 — Comilla curva simple de cierre asignada a la oración siguiente

`‘Dato. [C-001]’ Otro dato. [C-002]` se divide en `‘Dato. [C-001]` y `’ Otro dato. [C-002]`; también ocurre con cierre anidado. Los offsets reconstruyen literalmente esas cadenas, pero sitúan el cierre de la primera unidad dentro de la segunda.

No se prestan C entre oraciones en esta variante. El defecto afecta la frontera nominal exacta y es distinto del bloqueo por prosa enmascarada como enlace.

## Avances y límites observados

Los defectos iniciales de cierres poscita, elipsis Unicode, abreviaturas terminales, cursiva con guion bajo y cita sin cierre están reparados en los escenarios fijados inicialmente. Los casos nuevos también confirman comportamiento correcto para cierres seguidos de punto, varias citas enlazadas, enlaces relativos, URLs con paréntesis equilibrados/escapados y varias fronteras ambiguas; estas últimas bloquean sin adjudicarse automáticamente.

La generación independiente en memoria a las 2026-09-27T03:18:46Z produjo 4793 segmentos: 2129 narrativos/aristas y 2664 celdas. Siguen 42 unidades narrativas sin C. El diagnóstico conservador detecta 186 bloques con 192 fronteras: 189 abreviaturas terminales posibles y 3 iniciales. Dos ejecuciones dan bytes iguales y las entradas antes/después coinciden. La traza persistente no se escribió.

No se aprueban esas 42 unidades ni ninguna de las 192 fronteras. El aumento de diagnósticos no es un censo de errores científicos: mantiene alternativas para adjudicación futura. La determinación reproducible del texto tampoco acredita soporte primario.

## Condición de siguiente inspección

Se requiere corregir la identificación nominal de enlaces y sus delimitadores sin convertir prosa arbitraria en evidencia, y fijar un hash nuevo para reinspección. El autor puede mantener los diagnósticos fail-closed cuando no pueda resolver una forma; no debe prestar C, eliminar contenido ni introducir exenciones de rutas.

NC-DEN01 permanece abierto y separado. Este addendum no habilita censos científicos, controles manuales, firma global o cierre del plan.
