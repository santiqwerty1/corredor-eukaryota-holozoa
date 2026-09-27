# BN-134: segundo checkpoint de lectura, no cierre

Revisor: `/root/inspeccion_relojes`. Captura: **2026-09-27T04:20:41Z**. Rama comprobada: `codex/cierre-plan-pendiente`. El JSON homónimo contiene la captura viva de las 19 filas, BN-134, fuentes y C nominales, junto con 92 localizadores y huellas de pasajes/artefactos. Las huellas de fila usan JSON canónico compacto ordenado, UTF-8, más LF.

Se preserva el checkpoint anterior `CHECKPOINT_BN134_19_ASOCIACIONES_2026-09-27.json`, SHA `d71bb592fc7d459ea622412ac2f7e1c6172d21648f100cc333310e9afdcb0ff8`. La tabla43 y BN-134 mantienen sus huellas anteriores. No se han modificado canónicos, fuentes, disposiciones ni firmas.

## Cobertura efectiva

Hay lectura parcial delimitada acumulada para diez asociaciones: Lenisia, ANME–SRB, Pelomyxa, ciliados, Angomonas, dinotomos, Kareniaceae, Tremblaya/Moranella, Buchnera y Wolbachia. Cada campo exigido por §9 tiene una anotación explícita en el JSON; anotación de hueco no equivale a revisión científica completa. Ocho filas —Paulinella, UCYN-A, Hatena, Rhopalodia/Epithemia, Mesodinium, Dinophysis, Elysia/Plakobranchus y nucleomorfos— siguen inventariadas y pendientes de esta relectura. Perkinsela queda excluida de dictamen independiente por autoría de propuestas que aún no están integradas.

El literal pide cada caso, antigüedad y comparación genómica, **no un método homogéneo ni un cociente nuevo calculado por el compilador**. No corresponde invalidar una comparación publicada sólo por no presentar ese cociente. Tampoco corresponde convertir una comparación mitocondrial o plastidial en tamaño nuclear completo.

## Hallazgos útiles para reparación posterior

- S210 publica ensamblaje provisional de Arcobacter de 3 Mb y una asociación facultativa bajo condiciones experimentales explícitas. El primer dato sólo cubre parte de la comparación genómica; el segundo es un candidato positivo para el campo de estado. No resuelve antigüedad, transmisión, EGT ni importación.
- La negativa categórica de transmisión hereditaria conjunta en ANME–SRB no se deriva de su geometría extracelular. S226 permite cultivo separado de HotSeep-1 y S227 desacopla actividad usando un aceptor artificial; ninguno demuestra reversibilidad natural universal.
- S233 distingue tres socios de P. schiedti SKADARSKE, sus ensamblajes y sus efectos experimentales. Dependencia de metanogénesis no significa obligación de todos los socios ni de todo Pelomyxa. La comparación con R. bromii no acredita por sí sola vida libre.
- Los resultados de ciliados exigen separar linajes y modalidad inferida. S235 cita reducción en dos simbiontes y falta de reducción significativa en otro; sus referencias genómicas primarias aún requieren cotejo antes de restaurar cifras.
- Se conservan los hallazgos S237/S239 y S263 del primer checkpoint: comparación publicada con A. xylosoxidans, anillo ETP9 externo distinto de importación, cromosoma de Buchnera distinto del total con plásmidos y edad de establecimiento atribuida a otra referencia. No se vuelven a fechar como una nueva aprobación.
- S301 publica contigs mitocondriales de 35,505/39,686 bp, sin cerrar extremos. Los 34,242/34,742 de la tabla viva no son el tamaño total. La fuente sí contiene comparandos mitocondriales de diatomeas de vida libre. No cubre el genoma nuclear del endosimbionte.
- S302 distingue posibles EGT y predicciones de localización de demostraciones experimentales de importación. El transcriptoma mixto de dinotomos impide adjudicar automáticamente todos los candidatos al núcleo hospedador.
- S303 contiene discrepancias internas: 30 tRNA en prosa frente a 29 en Table1, y 110 proteínas del comparando en discusión frente a 113 en tabla. Se conservan sin armonizar. El ensamblaje plastidial de 142,981 bp no es un genoma nuclear.
- S268 fecha divergencias de cepas usadas para inferir introducción en lepidópteros, no una edad universal de captura de Wolbachia. La coincidencia genómica candidata requiere excluir contaminación; no se adjudica como EGT probado.

## Identidad y acceso: no equivalencias silenciosas

El archivo llamado S226 es una tesis de 2015 que contiene un manuscrito aceptado del artículo Nature, no su PDF publicado. S261 contiene realmente **Bublitz et al. 2019, Peptidoglycan Production by an Insect-Bacterial Mosaic**, no el **Husnik et al. 2013** catalogado. El S262 local es un preprint de marzo de 2016, no la versión PNAS citada. El JSON identifica pasajes, archivos y límites; no se cambia el catálogo ni se hace equivalencia de versiones.

La lectura del documento Bublitz local identifica MurF dentro de Moranella, pero los autores conservan formalmente la posibilidad de transporte de mRNA seguido de traducción allí. No se atribuye este resultado a S261 ni se da el mecanismo por resuelto. La [copia publicada de Husnik 2013](https://www.filiphusnik.com/sites/default/files/13_husnik_cell.pdf) se leyó parcialmente por el lector web; no se obtuvo copia local ni se declara revisión integral.

Se recuperó sólo en `/tmp` una [copia de autor de S227](https://researchmap.jp/simplyshawn/published_papers/15198252/attachment_file.pdf), SHA `b633fd65d10d3bf6ec297925dc604b82fee2c1c5610aef80e7efafac5f5abee5`; sus páginas extremas contienen también texto de artículos vecinos, expresamente excluido. No se integró al inventario de fuentes.

La pista primaria [Nakabachi et al. 2014 sobre RlpA4](https://www.sciencedirect.com/science/article/pii/S0960982214007544) requiere lectura completa de métodos y suplemento: sólo se consultó parcialmente una leyenda indexada. No permite todavía una disposición, pero impide tratar la búsqueda incompleta como prueba de inexistencia de importación.

## Estado que se conserva

**BN-134 y sus controles asociados siguen abiertos.** No se aprueba ninguna fila completa ni el catálogo. Los positivos parciales requieren propuestas y revisiones nominales nuevas. Las 408 consultas residuales históricas no se alteran ni se reinterpretan como coincidencias retrospectivas. Faltan la lectura de las ocho filas pendientes, las primarias de varias fechas y comparaciones, y la resolución editorial explícita de las versiones/identidades señaladas.
