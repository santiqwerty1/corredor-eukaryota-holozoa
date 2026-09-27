# Revisión independiente nominal: S560, HGT y R-0212

Revisor: `/root/revision_residuales/candidatos_editoriales`. Rama comprobada:
`codex/cierre-plan-pendiente`. Inicio real: 2026-09-27T01:14:00Z.
Instantánea principal: 2026-09-27T01:23:19.227672Z.
Dictámenes emitidos: 2026-09-27T01:28:46Z.

## Resultado de esta versión

De las **24 afirmaciones nominales** examinadas (23 del encargo inicial y
C-1197 añadida por el autor durante la revisión), **20 son CONFORME y cuatro
NO_CONFORME**. Las cuatro NC pertenecen exclusivamente a las huellas archivadas:
C-1186, C-1197, C-1198 y C-2832. No se sustituyen por el resultado de un parche
posterior.

También se cotejaron **26 filas F**, la identidad documental limitada de
**S560/S561/S512/S562** y el fundamento de **cuatro retiradas BN**.
El antiguo PDF local rotulado S296 tiene un **NO_CONFORME de identidad de
artefacto**, distinto de la identidad correcta de la referencia bibliográfica A.
Los 59 dictámenes están en
`dictamenes_independientes_s560_hgt_r0212_2026-09-27.csv`.

Esta revisión no usa tests del autor como evidencia científica. No crea firmas
en censos ni adjudica los 210 controles, ninguna segunda revisión global o
`make verify`. No edité canónicos. Participé anteriormente en búsquedas y
propuestas para S560/HGT y en la revisión de ocho BN: soy independiente de la
implementación del parche, **no un segundo investigador independiente de mis
propias búsquedas**. Esa limitación acompaña cada dictamen.

## No conformidades y reparación necesaria

| Objeto | Hallazgo nominal | Reparación |
|---|---|---|
| C-1186 | Barrera natural y rareza/importancia evolutiva son dos proposiciones publicadas separables; la terna representa solo la primera. | Separarlas conservando ambas y sus localizadores. |
| C-2832 | La media aproximada y la exigencia de contrastarla con más datos son proposiciones separables. La cifra sí está publicada. | Mantener el núcleo cuantitativo; conservar la cautela en Motivo/prosa o fila propia. |
| C-1198 | Los casos y controles apoyan la síntesis no binaria, pero no acreditan nominalmente su etiqueta de aceptación «consenso amplio». | Justificar la etiqueta o dejarla no evaluada; no deducir consenso de la fuerza. |
| C-1197 | Objeto atribuye ensamblaje quimérico. S296 final indica que la ausencia de afinidad metazoa sugiere que esos contigs no son coensamblajes quiméricos. Binning/cobertura son controles diagnósticos, no causas demostradas del error. | Restringir a contaminación no detectada y distinguir diagnóstico de mecanismo; justificar aceptación. |

La regla aplicada a las dos filas compuestas es el literal del prompt L254,
no una preferencia editorial nueva. Una cifra con su denominador, intervalo o
condición de medición sigue siendo una única proposición cuantificada:
no se exige fragmentar C-1163, C-2830, C-2833 o C-2834.

C-1197 quedó fijada antes de su modificación en
`evidencia_revision_independiente_c1197_s296_2026-09-27.json`.
La ausencia de acreditación de consenso **no demuestra que no exista consenso**.

## Cotejo primario

### Genes mitocondriales, C-1163/C-2824

Se releyeron íntegros en el JATS local S560 los apartados s2a y s3a.
Results publica 4459 genes nucleares inferidos dentro de 427186 genes de
30 genomas, distribuidos en 394 familias. Methods incluye selección BLASTP,
agrupación MCL, filogenias, representación mínima de eucariotas y
alfaproteobacterias, y separación de parálogos. Las C distinguen esas unidades
de episodios de transferencia y de un inventario exhaustivo de LECA.
El literal R-0209 no exige un total ancestral único; retirar BN-132 tiene
fundamento positivo. Esta revisión no adjudica el resto del mandato
(dirección, TOM/TIM y selección de genes transferidos).

### HGT, C-1185–C-1188/C-1198–C-1199/C-2825–C-2832

S290 local, Sec2/Sec3/Sec5/Sec8/Sec9: se cotejaron definiciones HIC y
clado-hermano, referencia a singleton, umbral ≥70, excepciones endosimbióticas
y porcentajes 3,1–5,1, <1,0 y 0,3. Son clados, no genes ni tasas anuales.
S561 local, s2-2/s2-3/s2-4/s2-9/s4-5/s4-6: 96/9075 OG, 641 secuencias,
629/641 colocalizaciones y cinco OG con alguna identidad individual >70.
Ningún promedio OG supera70; los filtros excluyen candidatos EGT y reconocen
posibles falsos negativos. La colocalización no acredita por sí sola un
mecanismo o dirección de transferencia.

La postura y media aproximada de S291 se contrastaron en el resumen y
Highlights públicos del [editor](https://www.sciencedirect.com/science/article/pii/S0168952520302067)
y de [Rutgers](https://scholarship.libraries.rutgers.edu/esploro/outputs/journalArticle/Horizontal-Gene-Transfer-in-Eukaryotes-Not/991031665538804646).
La apertura editorial directa dio403; el buscador devolvió el apartado
editorial y Rutgers concordante. No se afirma recuperación de PDF ni lectura
del cuerpo completo de S291. Esto basta para las dos atribuciones públicas
restringidas, no para otras tesis de ese artículo.

Se leyeron las dependencias relevantes de S211 (s2-6 y s3-4/s3-5) para la
síntesis, distinguiendo producción/localización de RQ, escenarios de transferencia
y mecanismo enzimático todavía no resuelto. S296 publicado se pudo cotejar
finalmente en un HTML local añadido por el autor durante esta revisión:
SHA256 `386809ac25942beaf0f8351ff6c3e2f3dc9de7b11b07210bc75908a915eb2136`.
Se leyó completo Results, *Claims of Extensive Functional Horizontal Gene
Transfer into H. dujardini*, y su contexto inmediato; no se sustituyó por el
preprint. El [artículo final](https://pmc.ncbi.nlm.nih.gov/articles/PMC4983863/)
sostiene la ausencia de HGT extensa y el papel de contaminantes, no el
quimerismo atribuido en C-1197.

Las cifras heterogéneas satisfacen la demanda de cifras de ambas posiciones,
sin hacerlas intercambiables: el denominador idéntico exigido por las viejas
BN-133/BN-146 no estaba en R-0220. La legitimidad de retirar esos huecos no
dispensa corregir las NC de las C ni adjudica todo R-0220.

### Trayectorias, C-1088/C-1120/C-2833–C-2837

Se extrajo independientemente el PDF editorial S512 y se leyeron Results
pp.2–3, Discussion p.6 y Methods p.8. La trayectoria bifásica es comparativa;
Fig.2B cuenta ramas. Los valores0,592±0,21 y0,185±0,123 son mediana±desviación
estándar de probabilidades DTL no normalizadas por rama. El segundo grupo
comprende tres ramas antes y tres después. No se convierte DTL en genes/año
ni en la frecuencia por familia calculada mediante otra fórmula.

El HTML completo S562 conserva un resultado diferente: 25 y4 ORF perdidos
**o inactivados**, respectivamente en B. floridanus y B. pennsylvanicus,
durante16–20Myr. Results, *Differential gene loss*, condiciona la reconstrucción
al repertorio ancestral combinado y advierte subestimación por pérdidas
paralelas. La introducción atribuye la divergencia a Degnan et al.2004.
Discussion, penúltimo párrafo, declara no poder fechar pérdidas individuales.
Las C conservan estas restricciones. La pareja número–tiempo es positiva y
justifica retirar BN-144; la prosa no mezcla esas cifras con la curva
comparativa de Enterobacterales. No se ha reconstruido una curva continua
fechada que S562 no ofrece.

## Historia, fechas y huellas

Las cuatro BN están ausentes del conjunto activo, pero sus filas completas
permanecen en los JSON de retirada. Se recalcularon huellas de esas filas;
no se validan retrospectivamente las consultas originales malformadas ni sus
fechas. Q conserva identidad histórica por archivo/huella, no por número
estable entre generaciones.

Se comprobó además la integración de las ocho reinspecciones anteriores:
las ocho filas conservan fecha real22:54:34–36 UTC del26, enlace a nuestro CSV,
dictamen y `habilita_cierre=NO`. Prefijo833:
`9d0175a112981fa7a1c56b8231435e3028c0cd6023b70150c06238aedae11e4d`;
prefijo841:
`3576e5d5e8ba0bf95d58a9eda0ee9c830791e19b6b56f8709fb663b190edd059`.
No se reescribió aquel CSV ni se reemplazaron dictámenes históricos.

La instantánea principal guarda filas completas, fuentes, magnitudes,
disposiciones, hashes originales de documentos y hashes de pasajes JATS.
`comprobaciones_revision_independiente_s560_hgt_r0212_2026-09-27.json`
añade hashes de pasajes HTML S562, cronología y vías de recuperación web.
A01:25:51 UTC no había cambiado ninguna de las23 C desde la instantánea.
Los dictámenes posteriores se emiten sobre **aquellas huellas**, aunque el autor
aplique correcciones mientras se materializa este informe.

Las conformidades F son de valor/unidad/denominador/localizador. Las
conformidades S son de identidad/tipo/disponibilidad del pasaje, **no revisión
editorial exhaustiva ni validación de fechas históricas**. Los derivados,
inventarios posteriores, matriz S completa, dos censos C, congelación y
verificación determinista/idempotente/aislada quedan fuera de este dictamen.
