# Lectura primaria independiente de S10: C-028–C-036

Dictamen del lote: **NO_CONFORME**. Emisión real: 2026-09-27T03:44:57Z. Revisor: `/root/verificacion_fuentes_nuevas`. Rama observada: `codex/cierre-plan-pendiente`.

Esta lectura precede a la propuesta de corrección del autor. No redacté ni modifiqué los objetos científicos examinados. Mi comprobación anterior de tres localizadores de C-031 no constituía aprobación de toda su ciencia. Se leyeron C01, el protocolo del censo semántico y el handoff antes del cotejo. No hay firma de censo, segunda revisión global, aprobación de BN, resolución de los 210 controles ni aprobación de `make verify`.

## Alcance y evidencia

Se examinaron las nueve C, once filas F, las seis filas Williams 2020 de la tabla y sus 54 celdas, las tres oraciones del párrafo de prosa L51 y la referencia agregada L55. El CSV compañero contiene 30 dictámenes nominales: 28 NO_CONFORME y dos CONFORME limitados a F filas 13 y 14; el JSON conserva los objetos exactos, huellas, evidencia por pasaje y dictamen de cada celda. Un NO_CONFORME integral no significa que todos los componentes sean falsos: por ejemplo, AU 0.036 y el localizador P10 de C-031 son transcripción correcta de esa posición publicada.

Los once archivos de entrada y los siete artefactos temporales/visuales se releían al emitir: no cambiaron respecto de la captura de 03:34:59Z. Esta estabilidad no protege cambios posteriores. Las huellas de C usan columnas canónicas unidas por U+001F y LF; F/tabla usan JSON de fila ordenado por clave, compacto y LF; prosa/celdas, texto exacto más LF. Los algoritmos y objetos se conservan en el JSON.

Fuentes primarias leídas:

- XML S10: SHA256 `7e6d524b255fe17298149e1f0295b5350413ae68b5f6242f44f3014101cb5c98`.
- PDF S10: SHA256 `6591a788679345020c30c61533273fa385e72d19f1297d6115f85ec3d3455768`, 34 páginas. La portada identifica una versión de autor aceptada/peer-reviewed version, no la versión editorial final. DOI 10.1038/s41559-019-1040-x; referencia de revista 2020, aunque el XML indica publicación electrónica en 2019.
- Suplemento EMS84653: SHA256 `dfe47e4d3e8a1fb086db29ae6f423cf92d55037ef411f77bc4fa84cb4d01d6c5`, 10.820.718 bytes, 43 páginas. Root lo recuperó mediante Europe PMC; yo lo leí y cotejé independientemente. Sigue en `/tmp/s10-figuras-cierre-20260927.pBwbOd/EMS84653-supplement-Supplementary_information.pdf`: su integración durable está pendiente y no se fingió como incorporación a `fuentes/`.

Inspección visual efectiva: Fig. 1 (PDF p32), Fig. 3 completa (p34) y detalle de Fig. 3b; ST2 (SI p3) y ST11 (SI p12–13). Se renderizaron las figuras a 170 dpi y las tablas SI a 145 dpi; el detalle de Fig. 3b corresponde al recorte x=1300, y=1180, W=1377, H=1150 de la página 34 a 170 dpi. Las seis imágenes y sus hashes están en el JSON. No se dedujeron los nodos únicamente del OCR.

## Hallazgos científicos que impiden el cierre actual

| Objeto | Defecto nominal y evidencia |
|---|---|
| C-028 | Los 35 genes corresponden a la concatenación reanalizada de Da Cunha; el conjunto original previo tenía 36 (P6/P8). ST11 explicita 35 genes/81 taxones. «Matriz original» es ambiguo y Methods/tabla 1 no localizan correctamente esta cifra. |
| C-029 | P8 expresa ambas log-verosimilitudes como aproximaciones: ≈−684701.2 y ≈−684716.1. ST2 distingue valores exactos por programa y restricciones. La tabla 1 del artículo no es esta tabla. |
| C-030 | P8 publica AU 0.771/0.229 para 2D/3D; ST2 publica 0.767/0.233. ST11 conserva 0.229 para 3D. No se declara esta discrepancia; tampoco corresponde el localizador tabla 1. AU no es PP ni probabilidad de que una topología sea verdadera. |
| C-031 | P10 sí publica AU 0.036 y rechazo de 3D bajo LG+C60+G4+F, a P<0.05. ST11 p12 imprime 0.0036 para esa combinación. No hay fundamento aquí para elegir uno, llamar errata al otro o atribuir su solución al corrigendum. |
| C-032 | Fig. 1 y ST11 asignan PP 1 al agrupamiento Eukaryota + Asgard muestreados en 35/81 bajo CAT+GTR+G4. No es soporte máximo de todas las ramas del árbol. |
| C-033 | PP 0.98 corresponde a Eukaryota + Heimdallarchaeota en 35/81, con SR4 y CAT+GTR+G4 (P11/ST11). «CAT» y «árbol de dos dominios» omiten modelo completo y nodo. |
| C-034 | 21/125 y 43/92 son matrices distintas y ST11 declara que 43/92 es un subconjunto del muestreo ampliado. «Mismo muestreo» y «muestreo común 125» no representan sus denominadores efectivos. P30 menciona 92 e incluye bacterias: se conserva esa discrepancia textual, sin reconstruir 125−33. |
| C-035 | En la prosa se aplica a la matriz de 43 proteínas; Fig. 3b SR4 agrupa Eukaryota + LC3 dentro del conjunto Heimdall, no como hermana del conjunto completo excluyente. El triple `grupo_hermano_de` no concuerda con ese análisis. Fig. 3a (21/SR4) es otro resultado y no puede prestarse al de 43. |
| C-036 | Fig. 3b, P19 y ST11 asignan PP 0.95 a Eukaryota + MAG LC3, no a LC3 aislado. |

La tabla 1 del artículo trata distancias de cuartetos en 3199 árboles de genes. No respalda las cifras de log-verosimilitud/AU que se le atribuyen. Cinco de las seis filas Williams 2020 apuntan a S09, obra de 2013 distinta (A y R5 del XML lo identifican); la excepción es la fila C-031/P10. No se ha revisado científicamente S09 entero a partir de esa identificación bibliográfica.

### Atomicidad solicitada

C-029 falla la prueba de §16: la log-verosimilitud de 2D podría estar bien transcrita y la de 3D mal. C-030 falla de igual modo para sus dos valores AU. C-034 agrega tres dimensiones separables: 21 genes, 43 genes y 125 genomas; denominarlo «vector de diseño» no impide que una parte sea verdadera y otra falsa. Deben separarse sin perder modelos, unidades ni denominadores.

C-031 sí es una prueba condicional atómica: modelo, estadístico y rechazo no son tres afirmaciones separadas. Puede conservarse como posición publicada de P10, con una atribución inequívoca y un enlace nominal visible a la posición discrepante de ST11. Eso requiere cotejar la propuesta y su contexto efectivos. El dictamen actual NO_CONFORME no ordena sustituir 0.036 ni declara falso P10; impide dar conformidad integral mientras se oculta una discrepancia encontrada.

### Nodos y denominadores comprobados

| Matriz | Modelo/recodificación | Nodo concreto | PP |
|---|---|---|---|
| 35 genes / 81 taxones | CAT+GTR+G4, original | Eukaryota + Asgard muestreados | 1 |
| 35 / 81 | CAT+GTR+G4, SR4 | Eukaryota + Heimdallarchaeota | 0.98 |
| 21 / 125 | CAT+GTR+G4, original | Eukaryota + Heimdallarchaeota | 0.81 |
| 21 / 125 | CAT+GTR+G4, SR4 | Eukaryota + Heimdallarchaeota | 0.79 |
| 43 / 92 | CAT+GTR+G4, original o SR4 | Eukaryota + Heimdallarchaeota | 1 |
| 43 / 92 | CAT+GTR+G4, SR4 | Eukaryota + Heimdallarchaeota MAG LC3 | 0.95 |

Son resultados nominales de ST11, con cotejo de las figuras pertinentes, no cálculos a partir de recuentos ni un soporte intercambiable entre matrices. Fig. 3b es formalmente no enraizada al carecer de grupo externo bacteriano; su leyenda lo dice. El término publicado es Heimdallarchaeota: este informe no demuestra por sí mismo equivalencia de circunscripción con cada uso moderno de Heimdallarchaeia.

## Límites conservados

La corrección de 2020 consignada en A sobre cuartetos/ASTRAL no fue reexaminada aquí como fuente primaria ni se extiende a los valores AU. Los AAM locales conservan la tabla de cuartetos anterior a esa corrección. La disponibilidad de acceso no acredita soporte científico.

No se completaron intervalos de incertidumbre ausentes ni posiciones alineadas mediante cálculo. Las búsquedas literales de dimensiones/positions en XML y suplemento no localizaron un recuento de longitud de alineamiento; el caso de «positions» en SI p36 trata raíces. Esta consulta limitada no equivale a demostrar que el dato nunca se publicó y no cierra ninguna BN. Tampoco se convierte el hallazgo positivo de 81 taxones/modelos en modificación retroactiva de resultados históricos.

Las celdas que remiten a BN conservan NO_VERIFICABLE para ese componente fuera de alcance, aunque exista evidencia positiva nueva que pueda alimentar una propuesta posterior. No se aprueban estudios posteriores usando solamente S10. Todas las discrepancias, requisitos de integración y propuestas de separación siguen abiertos hasta cotejo del parche concreto por un revisor independiente.

Archivos compañeros: `lectura_primaria_independiente_s10_c028_c036_2026-09-27.json` y `.csv`. No se modificaron corpus, fuentes, inventario, ledger científico ni firmas.
