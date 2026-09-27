# Revisión independiente de segmentación NC-DEN02

Dictamen del hash revisado: **NO_CONFORME**. No autoriza cerrar NC-DEN02, regenerar una traza aprobada ni adjudicar candidatos científicos. NC-DEN01 —presencia de fuente/localizador por oración— es otro control y continúa abierto.

Revisor: /root/inspeccion_relojes. Emisión: 2026-09-27T03:03:32Z. Rama: codex/cierre-plan-pendiente. No participé en esta implementación ni en sus tests dedicados; mi propuesta científica S240/S352 no forma parte del dictamen.

## Identidad y reproducción

- scripts/build_content_trace.py: `a1d865203b93016ac979ce54aa405c0e907d926ab9aa064046383d1d00f3d6f6`.
- tests/test_content_trace_sentence_boundaries.py: `f84aa2b911bf375226698ffb511bada20a01bba36df5d94954e3b44bc9881419`.
- Contrato propuesto leído íntegramente: `19c491ed7232c4b6267519a487dc2fe3281d74e3a757ef9dd82efadfd2c48846`.
- Fixture independiente: docs/auditorias/fixtures/revision_independiente_segmentacion_ncden02_20260927.py, SHA256 `7c046b65b22b57ac6d15ebfdb74a3fd0eebd7eb9ef6e26500e39dd24be3ac573`.
- Evidencia: docs/auditorias/EVIDENCIA_INDEPENDIENTE_SEGMENTACION_NCDEN02_2026-09-27.json, SHA256 `da9650f37c22c9fc975b0164171b3f5cd14a27e23a8553163e615356e6411483`.

Ensayo adversario ejecutado realmente entre 2026-09-27T03:02:02Z y 2026-09-27T03:02:02Z. Código, test, contrato, entrega y traza persistente conservaron sus bytes durante el ensayo. Los defectos se atribuyen al comportamiento del hash actual; no afirmo sin un análisis histórico que todos fueron introducidos por este delta.

La fixture imprime JSON. Para reproducir: `python3 docs/auditorias/fixtures/revision_independiente_segmentacion_ncden02_20260927.py`. Contiene 63 comprobaciones propias (49 pasan, 14 fallan) y nueve escenarios adicionales del pipeline/main real (tres pasan, seis fallan). Sólo se sustituyen ROOT, rutas del manifiesto/salida y argv dentro de directorios temporales; no se reemplazan los validadores ni la segmentación.

Reejecuté los 26 tests del autor: pasan. Eso no contradice las reproducciones que no cubren.

## Hallazgos

### IND-DEN02-01 — Cierres posteriores a la cita vuelven a prestar C entre oraciones

Caso mínimo:

`(Se observó. [C-001]) Otro resultado carece de C.`

Esperado: dos unidades, la segunda sin C. Real: una sola unidad que contiene C-001; no hay diagnóstico ambiguo. main escribe la traza temporal con exit 0 y su --check vuelve a dar exit 0; validate_payload devuelve lista vacía. Se reproduce igualmente con comillas angulares, rectas y curvas, comilla simple, cursiva, negrita y cierres anidados.

La causa está en sentence_spans: los cierres se consumen antes de adjuntar citas, pero no después; el cierre que sigue a ] hace que la condición de carácter no blanco descarte el punto como frontera. No es un defecto cosmético de ordinales: una proposición sin C queda dentro de una fila serializada como REVISADA.

Dos variantes de la misma frontera también fallan: `Dato. [C-001](https://example.org) Otro.` y `Dato. [C-001]Otro resultado carece de C.`. El enlace Markdown y la falta de espacio después del grupo no deben autorizar préstamo de evidencia. Si una variante se declara ambigua/no soportada, tiene que bloquearse explícitamente, no producir conformidad por fusión.

### IND-DEN02-02 — La elipsis Unicode se omite como frontera sin diagnóstico

`Dato… [C-001] Otro resultado carece de C.` produce un segmento, ningún diagnóstico y una traza temporal que main escribe y --check acepta. El signo … no está en el conjunto .!?; el caso equivalente con tres puntos ASCII sí se separa. El tratamiento Unicode exacto de offsets no compensa esta pérdida de una frontera.

### IND-DEN02-03 — Una abreviatura al final de oración se protege de manera incondicional

`Se analizaron otras spp. El segundo resultado no está registrado. [C-001]`

La salida conserva una sola unidad con C-001, sin ambigüedad; main y --check dan 0. La protección de spp. puede ser válida dentro de una frase, pero aquí también elimina un final plausible de oración. La política propuesta exige mantener la incertidumbre sin resolverla por semejanza: no basta detectar únicamente inicial+epíteto. No se pide un parser omnisciente; se pide que esta situación potencialmente fusionada no se certifique sin diagnóstico o adjudicación.

### IND-DEN02-04 — Cursiva Markdown con guiones bajos produce un corte falso y ningún diagnóstico nominal

`Hubo cambios en _B. floridanus_. [C-001] Otro.`

La salida es `Hubo cambios en _B.`, `floridanus_. [C-001]`, `Otro.`; diagnostics está vacío. La misma forma con asteriscos conserva el taxón. ITALIC_INITIAL_TERM sólo reconoce asteriscos y el carácter _ impide además el comienzo que busca AMBIGUOUS_INITIAL.

Este defecto es distinto de los anteriores: expone unidades sin C y por eso tiende a rechazar, no a prestar una C con éxito. Sigue sin satisfacer la segmentación nominal de cursivas y necesita tratamiento/adjudicación explícitos. No convierte el taxón en infracción científica.

### IND-DEN02-05 — Un grupo nominal sin cierre puede serializarse como revisado

`Se observó [C-001; S01 p. 1 sin cierre.`

citation_end no reconoce un grupo completo, pero claim_refs recoge C-001; validate_payload sólo rechaza exceso de cierres, no esta apertura sin cierre. main escribe y --check acepta. Es una limitación conexa de validación del grupo, no una afirmación de que el delta la introdujo. La reparación no puede prometer fail-closed para citas nominales si una forma estructuralmente incompleta conserva aprobación por la regex de C.

## Aspectos que sí se comprobaron

Los spans exactos conservan todas las unidades no blancas de los casos ensayados, respetan orden y límites Unicode y reconstruyen literalmente cada segmento por slicing. Pasan casos propios de cita pospuesta normal, grupos múltiples y anidados, [SIN FUENTE], corchetes no nominales, finales antes de las citas, UTF-8/emoji/acentos combinados/CRLF/NBSP, decimales y notación exponencial, URLs con query, autolinks y enlaces Markdown normales. Las iniciales simples B. floridanus y la cadena de dos iniciales generan alternativas explícitas; la fixture normal con oración sin C y la de inicial pendiente bloquean main sin escribir.

Una fixture positiva con dos C explícitas genera dos segmentos; dos ejecuciones conservan bytes y entradas. Los casos incorrectamente aceptados también son idempotentes: esto demuestra precisamente que determinismo e idempotencia no prueban una segmentación correcta.

## Censo vivo independiente en memoria

A las 2026-09-27T03:02:41Z reproduje 2129 unidades narrativas/aristas y 2664 celdas: 4793 segmentos; 42 unidades narrativas sin C; un bloque con tres fronteras ambiguas. Dos generaciones en memoria coinciden byte a byte. El manifiesto de celdas no presentó errores en esa comprobación.

La evidencia guarda todos los hashes de entradas antes/después, los 42 textos/localizadores y las alternativas. Los inputs permanecieron idénticos durante esa ejecución y la traza persistente quedó en SHA256 `525e1d5efb16c6b1be6e1cf5e2bed53d025d87cd4c2d9b06ab75a75d5c12fe0d`. No se escribió una matriz canónica.

Estos recuentos son observaciones del snapshot, no objetivos de cierre ni adjudicaciones. No revisé el soporte científico de esas 42 unidades, ni adopté como infracción cada corte provisional.

## Contrato y siguiente condición de revisión

El documento leído separa explícitamente fronteras de densidad y propone identidad, contexto, independencia, UTC y huellas. Sigue siendo propuesta, no consumidor implementado. Los hallazgos anteriores muestran que el diagnóstico técnico actual no cubre todas las formas que el propio segmentador puede aprobar erróneamente.

La reparación debe conservar estos rechazos, añadir comportamiento verificable para los casos nominales y recibir una reinspección del nuevo hash. Las alternativas deben seguir siendo alternativas hasta su adjudicación ajena. No se debe arreglar esto propagando C, suprimiendo texto o eximiendo prefijos/rutas.

No se alteraron código, prosa, canon, contrato, CSV de traza ni registros de firmas. Las únicas escrituras fueron esta evidencia/fixture/informe y las fixtures efímeras aisladas. No se declara make verify, cierre de NC-DEN01, densidad, ciencia, controles manuales ni plan integral.
