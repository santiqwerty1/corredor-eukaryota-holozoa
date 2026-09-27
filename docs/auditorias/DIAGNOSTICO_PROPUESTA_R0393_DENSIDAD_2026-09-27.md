# R-0393: diagnóstico independiente y propuesta contractual

**Dictamen: la automatización actual no demuestra el literal completo de R-0393.** Hay dos defectos reproducidos: el control confunde presencia de C con localizador de fuente por oración, y el segmentador puede fusionar oraciones cuando la cita sigue al punto. No se modificaron implementación, corpus, registros de revisión, clasificaciones ni derivados de auditoría.

Revisor: `/root/verificacion_fuentes_nuevas`. Rama: `codex/cierre-plan-pendiente`. UTC real de la reproducción: `2026-09-27T02:39:12Z`.

## Encargo y puerta observada

Se leyeron íntegramente §16 del encargo y `DIAGNOSTICO_INDEPENDIENTE_SECCION16_2026-09-27.md`, y las funciones pertinentes del auditor de requisitos, auditor semántico y constructor de trazabilidad.

R-0393 exige localizador de fuente en cada oración de prosa que contenga fecha, cifra, taxón atribuido a autor, parentesco, carácter diagnóstico, mecanismo propuesto o atribución de hipótesis. R-0394 prescribe, para la oración sin fuente, conservarla precedida de `[SIN FUENTE]` y explicar en esa misma línea por qué se incluye. Son requisitos distintos de que exista una fila C.

La fila R-0393 usa el slug `ORACION_CIENTIFICA_CON_C` y la familia `TRAZABILIDAD_CONTENIDO_EXACTA`. Ejecuta únicamente `audit_semantics.py` y `build_content_trace.py --check`. Con el caso vivo aún presente, la invocación real de `python3 scripts/audit_requirement_controls.py --root . --requirement R-0393` terminó en **exit 0, AUTOMATIZADO, CERO_FALLOS**, 2 pruebas, 4488 segmentos. La salida completa se conserva en la evidencia JSON.

Ese resultado contrasta con el literal, no con una preferencia nueva del revisor. No se propone borrarlo del historial ni cambiar un enum para ocultar el defecto.

## NC-DEN-01 — P1: C no equivale a fuente/localizador de la oración

En `docs/secciones/014-13-13-escalas-tasas-y-recuentos.md:165`, la primera oración informa los recuentos 223/15 y 16/89 y termina con `[C-1664]`. Las S y sus localizadores aparecen en la oración posterior. La primera no los lleva ni está precedida de `[SIN FUENTE]`.

La fixture separa además correctamente dos oraciones con citas anteriores al punto:

> Se midieron 223 orígenes [C-001]. Otro análisis informó 16 casos [C-001; S01 p. 1].

El constructor produce dos segmentos y su `--check` acepta ambos. Por tanto, el incumplimiento no depende exclusivamente del error de segmentación: aun segmentando bien, `validate_payload` exige C pero no S/localizador dentro de esa misma oración. También acepta la cifra con `[C-001; S01]` o con `[C-001; método propio]`.

`audit_narrative` del auditor semántico examina líneas con C, no la densidad de fuente por oración. `audit_all_localizers` comprueba las celdas Fuente de filas con atribución expresa y sus S; no los localizadores de la prosa. La densidad H2 comprueba dos fuentes por apartado, una obligación diferente. Ninguna de estas comprobaciones convierte una C resoluble en un localizador escrito en la oración.

## NC-DEN-02 — P1: cita pospuesta hace desaparecer una frontera de oración

El patrón `SENTENCE_BOUNDARY` exige una mayúscula o algunos signos inmediatamente después del espacio que sigue a punto/interrogación/exclamación. En `. [C-1664] Parasitismo…`, lo siguiente es `[`, de modo que no corta; después de `]` tampoco existe un punto.

La reproducción viva de L165 devuelve **un único segmento `L165` con `cita_en_segmento`**, aunque el texto tiene dos oraciones. La fixture más pequeña lo confirma:

> Se midieron 223 orígenes. [C-001; S01 p. 1] Otro análisis informó 16 casos.

El segundo enunciado no tiene C ni fuente propios, pero queda dentro del segmento que contiene la C de la primera oración; build y `--check` terminan en 0. Esto contradice la promesa de no heredar C del párrafo. Debe repararse manteniendo esa promesa, no declarando que el párrafo pasa a ser la unidad contractual.

## Prueba propia y huellas

Fixture: `fixtures/diagnostico_r0393_independiente_20260927.py`, SHA256 `bc7548ad44a047d28c5daa1bb87330734ea9ef49b8952738b36c7a2af1223837`.

Resultado: `evidencia_diagnostico_r0393_2026-09-27.json`, SHA256 `3fb87f24dbce7b880e5361ca77a098ef0959867a56f9007094733efe9f4fe25a`.

Hay **10/10 reproducciones conformes a la conducta observada**, no 10 aprobaciones del producto: seis muestran aceptación de formulaciones que incumplen densidad o registro; otros controlan localizador presente, marca honesta, rechazo de ausencia de C y abreviaturas. Cada caso contiene adjudicación manual explícita, texto exacto, número gramatical esperado, segmentación real, segmentos, resultado de construcción y de `--check`. Se ejecutan las funciones de producción sobre un corpus mínimo ficticio en un directorio temporal; no se parchea la lógica de validación. El auditor narrativo también se ejecuta sobre esas líneas.

Versiones inspeccionadas:

- `scripts/audit_requirement_controls.py`: `1b275f110e46c7b7423d218e2f8a513b9670fe415a13e8750c26c3132ce97262`.
- `scripts/build_content_trace.py`: `665322eef3aa0ffe640173e9463e4b9e3a45687c0af2b26c5270f7764ebb0f54`.
- `scripts/audit_semantics.py`: `c8640f86a7f69f130f670948c11fcb1869afa5ae184c46e4d8adf7f889a154eb`.
- Prosa 014: `a25a781a6b02463eb6d6acf0c257080b6ef218afdfb6025dbd003592927deac9`.

Las ocho entradas expresamente censadas en `hashes_before/after` no cambiaron durante la fixture. Esto no es un snapshot exhaustivo de todo el repositorio: el autor comunicó una edición concurrente de C-1196 en 09.csv, ajena a las reproducciones aisladas y al texto L165. La salida viva conserva exactamente la huella de alcance que calculó aquella ejecución; no se promueve a una certificación global estable.

## Reparación propuesta, sin implementación

### 1. Conservar y reparar la traza C

Mantener todas las comprobaciones actuales de C por oración/arista/celda, correspondencia explícita de celdas, ausencia de sugerencias léxicas convertidas en revisiones, identidad del contenido, orden de dependencias y consistencia del derivado. No aceptar `[SIN FUENTE]` como exención de registrar la afirmación.

Corregir la segmentación con spans de texto y reglas explícitas para grupos de cita pospuestos: una cita inmediatamente después del signo terminal pertenece a la oración anterior, pero no arrastra a la siguiente. Preservar abreviaturas bibliográficas/taxonómicas, números decimales, URLs, corchetes y comillas. Registrar offsets y texto exacto; no usar un número de línea como sustituto de una oración. Los casos ambiguos deben quedar nominalmente pendientes, no fusionarse silenciosamente y aprobarse.

Las pruebas mínimas deben incluir los dos ejemplos anteriores; cita antes/después del punto; dos citas consecutivas; segunda oración sin C; segunda sin S; abreviaturas `et al.`, `fig.`, `p.`; decimales; preguntas/exclamaciones; mayúsculas/lowercase reales y delimitadores anidados. Regenerar luego la traza con el builder estricto y atender los fallos nuevos; no preservar el número 4488 como objetivo.

### 2. Añadir una puerta de densidad separada y acumulativa

Sobre un inventario exhaustivo y estable de oraciones de prosa, comprobar por oración aplicable:

- Presencia local de clave S canónica, resoluble a A, y localizador asociado a esa S en la misma oración. Una C, una BN, una S situada en la oración contigua o la palabra «método» fuera de una cita no sustituyen el requisito.
- Si corresponde la salida honesta sin fuente, verificar prefijo literal `[SIN FUENTE]` y explicación sustantiva en la misma línea, con enlace a la C registrada; conservar la oración. Esto se liga nominalmente con R-0394, sin hacer desaparecer el incumplimiento original por reclasificarlo.
- La excepción de tesis general no justifica una cifra sin localizador. La política explícita del encargo admite `Sxx (sin localizar)` como marca honesta: conservar esa categoría y distinguirla de un pasaje efectivamente ubicado. Esta reparación no debe transformar la tarea aplazada de localizar todas las imprecisiones en un nuevo bloqueo universal ni inventar localizadores.

El parser puede comprobar estructura, presencia, ubicación, identidades, hashes y cobertura. No puede concluir que cualquier palabra «resultados» es un localizador correcto ni que la fuente sostiene todas las cifras de la oración. Las rutas o frases editoriales no deben constituir una exención abierta de contexto.

### 3. Evidencia nominal independiente necesaria

Para el cierre íntegro hace falta un censo nominal de las oraciones de prosa, no solamente las que disparen un regex numérico. Por cada unidad: ruta/offsets/texto/hash y contexto; categoría o categorías del literal de R-0393 presentes o no aplicabilidad motivada; C correspondiente; S/localizador o marca honesta; alcance de lo sostenido por cada cita; dictamen, motivo, autor/revisor distintos, declaración de independencia y UTC real. Las oraciones con mecanismo, parentesco o atribución sin cifras requieren lectura, no un resultado negativo del regex.

La suficiencia y correspondencia del pasaje para cada componente científico se revisa contra fuente/versiones/artefactos concretos, ligada al censo semántico; no se hereda del mero hecho de que una S exista en A. Las afirmaciones compuestas, como C-1664, siguen necesitando su reparación científica independiente: añadir una cita a la prosa no resuelve esa atomicidad.

Todo el inventario, incluidos los casos declarados no aplicables y su contexto, debe quedar ligado a hashes de las entradas vivas. Un cambio obliga a reevaluar la vigencia; no copiar nuevas huellas sobre un dictamen viejo. El consumidor debe exigir población completa, unicidad, dictámenes vigentes y detección de cambios al materializar, sin alimentarse de su propio resultado agregado.

### 4. Clasificación derivada del contrato completo, no parche de estado

Conservar las dos pruebas actuales como evidencia estructural parcial. La condición que justifique R-0393 debe incorporar las comprobaciones de densidad y la evidencia nominal que cubra la aplicabilidad semántica completa. Sólo después de implementar y revisar ese contrato deben regenerarse estados/artefactos desde sus builders. No basta renombrar el slug, desactivar una familia, marcar manualmente CONTROL_DEFINIDO ni rellenar una fila de revisión manual con «todos pasan».

Se requiere reinspección independiente del código nuevo y revisión posterior de las reparaciones textuales; no autoaprobar el ledger al construirlo. R-0392 continúa siendo el roll-up de R-0393 y R-0394, no una vía alternativa para eludirlos.

## Límites y preservación

No se hizo un censo nuevo de todas las infracciones de densidad ni se declara que sólo exista L165. Tampoco se verificaron aquí las fuentes S513/S517 ni los recuentos científicos de C-1664. Los resultados prueban el defecto del control y de su segmentador, no la falsedad científica del texto.

Se dejaron intactos el código y los expedientes finales de teleología: consumidor SHA `4aedf83d64ec851d90db80fbc998a7f2f2f17a04ef1c23213e344cbce0b13429`, ledger v2 SHA `30b0de4813c5c30c54d751f89ab86d359e1c884b3ff9078c0ca74bcb2c2bb029`. La edición posterior de 09.csv caduca legítimamente su ligadura contextual; este diagnóstico no la renueva. No se firma R-0393, §16, censo C/S ni cierre global.
