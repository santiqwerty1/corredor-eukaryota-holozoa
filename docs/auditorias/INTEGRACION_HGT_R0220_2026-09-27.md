# Integración de cifras de HGT para R-0220

Autor: `/root`. Rama: `codex/cierre-plan-pendiente`. Fecha UTC: 2026-09-27.
**Revisión independiente de integración pendiente.** Los revisores están
interrumpidos por cuota; esta evidencia de autor no sustituye sus dictámenes.

## Corrección del requisito y evidencia primaria

El literal R-0220, en `docs/C01-PROMPT-INVESTIGACION.md:155`, pide las cifras
de las dos posiciones y el método de atribución. No exige un denominador
idéntico. La revisión independiente anterior de ocho BN ya había señalado
que BN-133 y BN-146 añadían esa restricción y no acreditaban ausencia de
cifras. Se corrige el contenido, no se rebaja el contrato de validación.

Se cotejaron los apartados Results, Deep differences between prokaryotes and
eukaryotes, The 70 % rule y Methods del JATS local de
[Ku y Martin (2016), S290](https://doi.org/10.1186/s12915-016-0315-9).
Se incorporó como S561 el artículo primario de
[Rossoni y colaboradores (2019)](https://doi.org/10.7554/eLife.45017),
*The genomes of polyextremophilic cyanidiales contain 1% horizontally
transferred genes with diverse adaptive functions*. Su JATS PMC6629376.1
se recuperó de Europe PMC y se cotejaron título, DOI y los siete autores.
Los editores del artículo no se incorporaron como coautores.

Los resultados se mantienen separados:

| Registro | Resultado publicado | Unidad y denominador |
|---|---|---|
| C-2825, S290 | 3,1–5,1 % | Clados procariotas HIC no singleton / clados de cada grupo comparado |
| C-2826, S290 | <1,0 % | Clados eucariotas HIC no singleton / todos los clados eucariotas analizados |
| C-2827, S290 | 0,3 % | Clados eucariotas HIC no singleton / clados restantes tras retirar origen plastidial |
| C-2828, S561 | 96 de 9075; 1,06 % | Grupos de ortólogos candidatos a HGT / grupos de los 13 genomas analizados |
| C-2829, S561 | 641 | Secuencias individuales candidatas, no episodios independientes de transferencia |
| C-2830, S561 | 629 de 641; 98,12 % | Candidatos colocalizados con genes nativos en una lectura larga / candidatos examinados |
| C-2831, S561 | 5 de 96; 5,2 % | Grupos candidatos con alguna comparación individual >70 % de identidad / grupos candidatos |
| C-2832, S291 | Aproximadamente 1 % | Contribución media resumida de HGT a inventarios génicos de protistas |

HIC en S290 se calcula a partir de la identidad media entre un clado y su
grupo hermano, usando un umbral específico del grupo derivado del cuartil
superior de identidades de singleton. Sus porcentajes no son porcentajes de
genes transferidos ni tasas por unidad de tiempo. S561 agrupa proteínas,
infiere árboles, inspecciona candidatos y filtra por soporte, muestreo y posible
transferencia endosimbiótica. La colocalización en lecturas largas es un control
adicional de contaminación, no una prueba autónoma de mecanismo o dirección.
Las excepciones de identidad en C-2831 son individuales: ningún grupo excede
el umbral en su identidad media. No se fabrica una tasa común entre trabajos.

El valor de S291 y su cautela sobre más datos y un procedimiento estandarizado
se cotejaron en el cuarto punto de los Highlights públicos de la
[ficha editorial](https://www.sciencedirect.com/science/article/pii/S0168952520302067),
también reproducidos por el
[repositorio de Rutgers](https://scholarship.libraries.rutgers.edu/esploro/outputs/journalArticle/Horizontal-Gene-Transfer-in-Eukaryotes-Not/991031665538804646).
No se afirma acceso al cuerpo completo de S291: la antigua ruta institucional
de su PDF respondió 404 y la ruta PDF del editor respondió 403. La ficha
institucional descargada por curl era un contenedor web, no el texto completo.
La cifra aproximada no se extrapola a un resultado universal o experimental.

## Integración canónica

Se corrigieron las ternas sujeto–predicado–objeto de C-1185, C-1186 y C-1187:
`propuesto_por` termina ahora en los autores, no en otro concepto. C-1186
conserva la interpretación publicada de Ku y Martin, sin convertirla en consenso.
C-1187 se restringe a la postura explícita del resumen de S291. C-1188 describe
el protocolo de S561, no una lista universal de pruebas suficientes. Las
referencias de las síntesis C-1198 y C-1199 incluyen la nueva fuente de C-1188.

C-2825–C-2832 se añadieron al final de `data/afirmaciones/15.csv`, conservando
la secuencia global de claves, y se presentan en la prosa de la sección 9.
Se añadieron catorce filas F y nueve entidades B, y se sustituyeron seis
etiquetas B que ya no describían las ternas corregidas. La regla de C-1185
conserva ahora el umbral ≥70 de The 70 % rule, también en F.
El nuevo predicado `tiene_proporcion_publicada*` quedó definido inmediatamente
en la sección 0, con relación y ejemplos; no significa validación independiente.

MREQ-0035 y MREQ-0036 enlazan valores publicados con unidades y denominadores
explícitos. `registro_hueco` y `razon_hueco` quedan vacíos para los resultados
positivos. R-0220 conserva una disposición de cobertura, con advertencia de que
no adjudica revisión nominal. Una primera ejecución del censo rechazó el texto
porque su contrato exige identificar la frecuencia sustantiva de HGT; C-2832
precisa que es una frecuencia relativa de genes, no una tasa temporal. No se
modificó `build_requirement_magnitude_census.py` para hacerlo pasar.

El validador detectó además la primera ubicación incorrecta de las altas C en
el archivo 09; se movieron al registro final, sin renumerar claves existentes.
La auditoría semántica pidió un localizador reconocible en C-1185; se conservó
el encabezado exacto The 70 % rule y se añadió el nombre de apartado en español.
No se sustituyó el pasaje recuperado por una marca de imprecisión.

## Historia y artefactos preservados

`retirada_bn133_bn146_2026-09-27.json` conserva las dos BN, sus Q completas,
las cuatro C corregidas inicialmente, la disposición R-0220 y las dos
especificaciones MREQ anteriores, además de las huellas de las 497 BN previas.
SHA-256: `5a282cd06c145b050240d6aaef8ed46448309089c8d8445e9c3a728e83447cc1`.
Las propuestas positivas allí guardadas corresponden a la preparación; las
filas finales y sus huellas constan en el registro de integridad del delta.

Q-0187 y Q-0196 solo identifican estas consultas en la versión archivada de
`registro_busquedas_2026-08-08.csv`, SHA-256
`31a4ecf4665bd1a7b96f2cf8e3171d01802dda865441b878c9f7a9e3c60cba94`.
El archivo Q no se ha reescrito. Su fecha original no queda acreditada por
retirar las BN; se conservan las reinspecciones posteriores y sus límites.

El contrato nominal de BN pasa de 497/485/12 a 495/483/12 y rechaza reintroducir
cualquiera de las cuatro retiradas, incluso compensando con la desaparición
de otra fila. Las 408 consultas residuales y los dos positivos siguen exigidos.
Las otras 87 BN permanecen idénticas; las 408 v3 solo cambian el número y SHA
del inventario. No se añadió otra BN con la condición artificial de denominador
idéntico.

`integracion_s561_2026-09-27.json`, SHA-256
`7bb8d9ab71c4cdbe1aa2e8261c165e7c9f9a1d81cd4981f5b5d2671f09236398`,
acredita que se conservaron los 447 archivos anteriores. Se añadió únicamente
el JATS de S561, SHA-256
`ae605a39767da61863afb1c7a017e51689a79a758990392c01d0d5fd1747320a`.
Inventario resultante: 448 archivos, SHA-256
`1373e4658ea749685d9b9fdea95e800ff3bff56ab3d2012ae3b9d47d45d55bb6`.
La respuesta HTML de la ruta PDF de eLife no se integró como PDF. `fuentes/`
sigue ignorada por Git; no se sobreescribieron documentos ni se forzó su alta.

## Comprobaciones realizadas y límites

- Suite: 228 pruebas, cero fallos. Incluye seis regresiones de representación
  y conservación de este lote, no seis revisiones científicas.
- Validación y auditoría semántica automatizadas correctas: 2832 C, 526 S,
  1512 B, 108 eventos, 216 fechas, 82 hipótesis, 614 F, 495 BN y 97 tablas.
- Linaje y trazabilidad regenerados: 4485 segmentos; mapa C, procedencia,
  censos de magnitudes, densidad y derivados ordinarios actualizados.
- Idempotencia del render: dos pasadas en copias aisladas produjeron las nueve
  salidas idénticas. Esto no sustituye la ejecución integral aislada de
  `make verify`, que sigue sin pasar.
- Ejecución diferencial real del autor entre 00:39:30Z y 00:44:43Z del
  2026-09-27: búsqueda literal e índice coinciden en las 410 consultas.
  Las 408 negativas dan cero; C-2472 da 3 y C-2489 da 5. Cero coincidencias
  literales no acredita ausencia científica.
- Evidencia de consultas:
  `evidencia_reinspeccion_autor_bn_v3_2026-09-27_inventario448.csv`, SHA-256
  `379055c23c99120da925a56c178bd78fdef0229338e4e9e93553c2de21b4d6ab`.
- Cronología: 1249 → 1657 filas, conservando byte por byte el prefijo previo,
  SHA-256 `65d8c8e061aa34ed34fe58a612a1d217947f25fe7f5314e24588653306ab42de`.
  Cero errores de carga. Las fechas nuevas pertenecen a ejecuciones de autor,
  no a dictámenes independientes.
- QA externa: 97 CSV, 63467 celdas, cero diferencias; Node v24.19.0 y
  `@oai/artifact-tool` 2.8.59 del bundle 26.909.12148. Tras el fallo de
  interoperabilidad WSL, el reintento autorizado usó el mismo runtime sin
  instalar paquetes. Se volvieron a comprobar las 97 huellas.
  Evidencia: `qa_tabular_externa_2026-09-27_corpus2832.json`, SHA-256
  `6e5d12682b642c0ace34786d97e1c7d24f00dc77c1f3118f0578ec8f5b59acef`.
- Acceso: 286 fuentes obtenidas y 240 restantes de 526. S291 no se cuenta
  como descargada por haber podido consultar su resumen y Highlights.

`integridad_delta_s561_bn133_bn146_2026-09-27.json` fija las comprobaciones,
la cronología, las filas finales de integración y el resultado de `make verify`.
Esta última orden sale con código 2 en `check_semantic_claim_census.py`: la
congelación no tiene un instante UTC válido ni coincide con el corpus, y faltan
las dos matrices de revisión de las 2832 C. Las puertas anteriores pasan.

**El plan no está cerrado.** No se han creado firmas ni aprobaciones para
suplir los 210 controles manuales, las revisiones nominales S/C o las segundas
revisiones globales. La revisión editorial exhaustiva de S561 también sigue
pendiente. Debe estabilizarse y revisarse el corpus antes de preparar la matriz
S, congelar con UTC real y materializar el cierre. No se declara éxito integral,
determinista, idempotente y aislado de `make verify`.
