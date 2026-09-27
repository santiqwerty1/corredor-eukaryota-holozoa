# Entrega autoral: reparación de segmentación NC-DEN02

Autor: `/root/verificacion_fuentes_nuevas`. Rama: `codex/cierre-plan-pendiente`. **Pendiente de revisión independiente**: este autor diagnosticó el defecto original y ahora implementó el cambio; sus pruebas no constituyen aprobación independiente de la reparación.

## Alcance implementado

Se modificó únicamente `scripts/build_content_trace.py`, se añadió un módulo de tests dedicado y se escribieron artefactos propios de diagnóstico/propuesta. No se cambió `audit_requirement_controls.py`, el corpus, las fuentes, los ledgers ni las firmas. No se regeneró la matriz de trazabilidad persistente ni se corrigió prosa automáticamente.

Las citas pospuestas como `. [C-001]` pertenecen a la oración precedente y dejan de fusionarla con la siguiente. Se conservan grupos múltiples, grupos anidados, citas sin espacio intermedio, abreviaturas bibliográficas/taxonómicas ya reconocidas, URLs y decimales. Se separa también una oración que empieza por minúscula. Se preserva `[SIN FUENTE]` como prefijo de la siguiente oración, sin absorberlo como una cita de la anterior.

No se añadieron rutas ni frases exentas del deber de llevar C. La semejanza léxica continúa siendo sólo sugerencia y las celdas siguen requiriendo sus correspondencias explícitas. Las comprobaciones previas de traza, tombstone, fragmentos espurios, manifiesto, consistencia de contenido y ausencia de C siguen activas.

## Spans y ambigüedades

`sentence_spans(text)` devuelve offsets Unicode `[inicio, fin)` exactos sobre el texto recibido, sin sustituir signos ni normalizarlo. `split_sentences` recorta ese texto por esos spans. No se alteran las diez columnas de la matriz persistente ni se presentan como offsets de archivo los de un párrafo previamente normalizado por `narrative_blocks`.

Las formas explícitamente encerradas en cursiva de dos componentes, como `*S. rosetta*` y `*D. discoideum*`, conservan el punto de la inicial dentro del token. No se generaliza a cualquier inicial seguida de minúscula, porque eso escondería `modelo B. este segundo resultado…`.

Para iniciales sin tal delimitación se añadió diagnóstico `AMBIGUA_INICIAL_EPITETO`: conserva la lectura con corte y la lectura como abreviatura, sus offsets y el bloque exacto con SHA256. No decide cuál es correcta ni llama a esos cortes infracciones científicas. `main` bloquea explícitamente la construcción si hay fronteras de este tipo no adjudicadas. No existe aquí un consumidor que apruebe spans nominales; se propone por separado y queda pendiente.

## Pruebas autorales

- `python3 -m unittest tests.test_content_trace_sentence_boundaries`: 26 tests, 0.039 s, OK.
- `python3 -m unittest discover -s tests`: 315 tests, 36.036 s, OK en esta ejecución. La cifra incluye otros módulos presentes en el repositorio vivo y no fija una población futura.
- `git diff --check` de los archivos propios: sin errores.

Los tests cubren el defecto original y la prohibición de prestar C a la siguiente oración; minúsculas; cita anterior/posterior al punto; citas consecutivas y anidadas; `[SIN FUENTE]`; abreviaturas; números decimales; URLs y enlaces Markdown; comillas/paréntesis; preguntas/exclamaciones; offsets Unicode; invariante de conservación de texto; y pipeline narrativo que sigue rechazando una nueva oración sin C. Los diagnósticos de inicial muestran ambas lecturas, sin aprobar ninguna automáticamente.

## Censo vivo calculado en memoria

Ejecución real: `2026-09-27T02:52:27Z`. Se comparó la función histórica de segmentación, conservada explícitamente en la fixture, con la nueva sobre el mismo snapshot de entradas. Se leyó la traza persistente para fijar su huella; no se escribió.

- Narrativa/aristas: 1824 segmentos anteriores → 2129 nuevos.
- Celdas: 2664, sin cambio en esta comparación.
- Total provisional: 4488 → 4793.
- 224 bloques con distinta segmentación/localización/contenido.
- 42 segmentos expuestos sin C propia; el estado formal impide construir la traza.
- 1 bloque con 3 fronteras ambiguas: `docs/secciones/010-09-9-asociacion-el-catalogo-de-desenlaces.md:L381`, en las iniciales de B. floridanus/B. pennsylvanicus.
- Manifiesto de celdas sin errores en la comprobación en memoria. Entradas capturadas idénticas antes/después. Matriz persistente intacta.

**42 no significa 42 infracciones científicas adjudicadas.** Entre esos segmentos están los tres cortes provisionales ambiguos, rótulos como `**Ficha de montaje H22.**` y `- **Eukaryota.**`, y oraciones completas anteriormente cubiertas sólo por la C del párrafo. Todos se conservan en la evidencia nominal; requieren revisión y disposición separadas. No se añadió una exención general para rótulos ni se propagó a ellos una C por proximidad.

El caso original de prosa 014:L165 se divide ahora en dos unidades. Ambas llevan C-1664, pero la primera continúa sin S/localizador propio: **NC-DEN01 sigue abierta**. Arreglar fronteras no demuestra densidad de fuente ni repara la atomicidad científica de C-1664.

Los números anteriores son observaciones, no objetivos que deban mantenerse artificialmente. Una adjudicación de spans o una reparación de contenido puede cambiarlos y debe originar un censo nuevo.

## Artefactos y huellas de entrega

- `scripts/build_content_trace.py`: `a1d865203b93016ac979ce54aa405c0e907d926ab9aa064046383d1d00f3d6f6`.
- `tests/test_content_trace_sentence_boundaries.py`: `f84aa2b911bf375226698ffb511bada20a01bba36df5d94954e3b44bc9881419`.
- `fixtures/censo_autoral_segmentacion_20260927.py`: `37bd454ca861a6a981f1b3f1ac96de4564d654b7f39e0972dd4b5a83445c4e6c`.
- `censo_autoral_segmentacion_2026-09-27.json`: `c916c87bbe703fe22fe73f586f85c2ecb252571153421f1ab4f8ba1a13dc4061`.

El JSON contiene las huellas completas de las entradas antes/después, los 42 textos expuestos con localizador, las tres ambigüedades con lecturas alternativas y los hashes/IDs antes/después de los 224 bloques. La fixture sólo construye payloads en memoria: no llama al modo de escritura del builder.

El constructor previo inspeccionado en el diagnóstico tenía SHA256 `665322eef3aa0ffe640173e9463e4b9e3a45687c0af2b26c5270f7764ebb0f54`. Los diagnósticos originales y los expedientes finales de teleología permanecen intactos.

## Integración pendiente

`PROPUESTA_CONTRATO_CENSO_ORACIONES_DENSIDAD_2026-09-27.md` describe —sin implementar ni rellenar firmas— el censo nominal prospectivo de fronteras y densidad, su consumidor exacto, la independencia y la ligadura a contexto/versiones. No cambia silenciosamente el esquema de la traza existente.

Faltan revisión independiente del código entregado; adjudicación de los candidatos de segmentación y de las fronteras ambiguas; correcciones textuales autorizadas con evidencia; puerta adicional de densidad NC-DEN01; y después regeneración y verificación aislada. Esta entrega no certifica R-0393/R-0394, §16, censo científico ni `make verify`.
