# Reinspección independiente de v3 y v4 — C1664/C1642/C1121

Revisor: `/root/revision_residuales/candidatos_editoriales`. Captura nueva: 2026-09-27T02:55:07Z. UTC exacta de adjudicación en ambos CSV. Rama: `codex/cierre-plan-pendiente`. No se modificó canon, propuestas ni dictámenes anteriores.

## Resultado acotado

**V3 sigue NO_CONFORME**: repara las cuatro entidades de métodos pero todavía representa el corte operacional >0.5 como magnitud inferida. **V4 es CONFORME como propuesta limitada al lote leído**: corrige ese defecto y conserva el valor como parámetro del método de F de 16 orígenes y de Motivo C2880. No se pierde el valor ni se amplía/relaja AF436. No se afirma que el paquete esté integrado o que las comprobaciones posteriores hayan pasado.

Huellas exactas:

- v2: `9cf84c0123fdcaf9fc25f37f5ad7990891c828c086900c4722ceb0b37075fdbc`.
- v3: `90d4e2b446df1aaa1d53dbe7d1ac4f210d7b1ffe091ecd96c0dc1d61c3632ad3`.
- v4: `f617976321c0cc1d784812d57d7d08ff533c178e65ddea1877cdfe434126b7d4`.

## Comparación y lectura nuevas

Se comparó profundamente el JSON completo, no sólo el número de versión ni los hashes declarados. De v2 a v3 cambian exclusivamente versión, UTC, estado, antecedente y cuatro altas B al final; las seis B anteriores y todos los objetos C/F/tablas/prosa permanecen idénticos. De v3 a v4 cambian exclusivamente versión, UTC, estado, antecedente, una nota de límites y la retirada de F_altas[2]. Las dos F_altas de correlación y pMCMC permanecen intactas. Todos los objetos retenidos conservan exactamente sus hashes comprobados.

Releídos S513 P8/P51/P52/P60/P61 desde XML local SHA `97c37c51e5148821ade14fbab6cdf1c873aaad82b02bcd6e30d69c3944b8e040`: P51 distingue BPMM de respuesta única y MR-BPMM multirrespuesta; P52 identifica MCMCglmm como paquete R; P60 especifica la función predict y el corte; P8/P61 identifican SCM y su aplicación como contraste. Las etiquetas, aliases y enlaces de las cuatro nuevas B son congruentes con los objetos respectivos. No son cuatro apoyos científicos independientes: son entidades metodológicas de la misma fuente.

La clasificación incorrecta de F del umbral se conserva en v2/v3 y en sus NC. En v4, `>0.5` permanece dentro de la misma tabla F, ahora únicamente como parámetro del método del recuento de 16 orígenes; además permanece «mayor que 0.5» en Motivo C2880. P60 separa una probabilidad posterior estimada de la regla adoptada para clasificarla. Esta representación no transforma el corte en una cifra inferida, ni retira la cifra publicada, ni exige un tercer estado del vocabulario del validador.

Los dictámenes nuevos por objeto son una reinspección por identidad demostrada y contraste del delta, no firmas copiadas a archivos arbitrariamente modificados. Su fundamento científico continúa siendo la lectura primaria documentada en la revisión v2, complementada por los nuevos pasajes; no son una segunda fuente científica independiente.

## Límites no promovidos

Se mantienen íntegros los límites de v2: sólo cambio de referencias en Motivo de C1665, sin aprobación S460; sólo referencias nuevas en prosa182, sin aprobación de multicelularidad; C1201 no adjudicada. No se aprueban de modo global §16, B, F, los 210 controles ni el corpus. Las marcas editoriales limitadas de esas dos filas permanecen distintas de las conformidades científicas.

Todavía son actuaciones del integrador, no hechos certificados aquí: incorporación durable y procedencia de S517, conservación de IDs continuos respecto del lote previo reservado, derivados, manifiesto y verificación final. Si cambian objetos sustantivos, esta adjudicación por hash no se extiende al cambio.

## Artefactos

- `evidencia_reinspeccion_c1664_c1642_c1121_v3_v4_2026-09-27.json`: deltas completos, 33 objetos v3/32 objetos v4 con hashes y punteros, cuatro B nuevas y cinco pasajes íntegros/hashes leídos.
- `dictamenes_reinspeccion_c1664_c1642_c1121_v3_2026-09-27.csv`: 35 filas, NC de F del corte y del paquete preservadas.
- `dictamenes_reinspeccion_c1664_c1642_c1121_v4_2026-09-27.csv`: 34 filas, conformidad de la propuesta limitada; dos deltas exclusivamente editoriales no son aprobaciones científicas de sus filas completas.

Los expedientes v1/v2 permanecen intactos. No se utilizaron tests del autor como evidencia científica ni se editaron libros de firmas globales.
