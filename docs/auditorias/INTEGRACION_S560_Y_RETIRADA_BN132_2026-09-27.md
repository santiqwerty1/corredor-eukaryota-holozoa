# Integración de S560 y retirada activa de BN-132

Autor: `/root`. Rama: `codex/cierre-plan-pendiente`. Trabajo iniciado el
2026-09-26 y continuado el 2026-09-27 UTC. **Pendiente de revisión independiente
de integración**: los agentes revisores permanecen interrumpidos por cuota.
La propuesta independiente previa sobre el artículo no inspeccionó este parche.

## Corrección científica implementada

El literal R-0209 pide «cuántos genes», no un total ancestral único exacto.
Se elimina de C-1163 la afirmación universal no acreditada de que no existe
un recuento único directo. La fuente primaria incorporada como S560 es Wang y
Wu (2014), *Phylogenomic Reconstruction Indicates Mitochondrial Ancestor Was
an Energy Parasite*, PLOS ONE 9(10):e110685,
[DOI y texto editorial](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0110685).
La identidad se cotejó con el JATS PMC4198247.1; Frank Voncken es editor,
no coautor.

C-1163 recoge 4459 genes nucleares de origen mitocondrial inferido en una
muestra de 427186 genes de 30 genomas eucariotas. C-2824 separa las 394 familias
producidas por el análisis. Se conserva el carácter computacional del resultado,
su muestra y el procedimiento que separa parálogos. No se equiparan genes,
familias, episodios ancestrales de transferencia e inventario completo de LECA.
Localizadores: Results and Discussion, Identifying mitochondria-derived nuclear
genes, primer párrafo; Materials and Methods, Identification of
mitochondria-derived nuclear genes.

Se añadieron cuatro filas F al final, sin desplazar las magnitudes anteriores:
genes y familias inferidos, y dos recuentos del muestreo. El predicado nuevo
`tiene_recuento_inferido*` queda definido con relación y ejemplos en la sección 0.
Se actualizaron prosa 9, R-0209 y MREQ-0033. La disposición de cobertura no es
un dictamen científico: dirección, TOM/TIM y los nuevos números siguen sujetos
al cotejo independiente integral. Una primera regeneración rechazó correctamente
una explicación puesta en `razon_hueco` de un resultado positivo; se dejó vacío
ese campo y los límites permanecen en C, prosa y esta evidencia. No se cambió
el validador.

En B se sustituyeron dos etiquetas que ya no describían C-1163:

- `no existe recuento único directo` → `genes nucleares de origen mitocondrial inferido en Wang y Wu`, C-1163.
- `número total de EGT mitocondrial ancestral` → `familias de genes de origen mitocondrial inferido en Wang y Wu`, C-2824.

Ambas nuevas filas son `magnitud o conjunto de datos`; se retira la clasificación
errónea del número como orgánulo. El número de filas B se mantiene en 1503.

## Historia y evidencia preservadas

`retirada_bn132_2026-09-26.json` conserva la BN y Q completas, la C-1163 anterior,
la disposición anterior de R-0209, las huellas de las 498 BN activas antes de
retirar una, y las filas positivas nuevas. SHA-256:
`5a19054d2831607ee30a570eb23b117204ab9e9a195bae4b01818971668d5cd4`.
Q-0186 solo identifica la fila de ese archivo y huella históricos; no es una
identidad estable para generaciones posteriores. No se acredita retrospectivamente
la fecha original ni la consulta con comillas defectuosas. Las reinspecciones
anteriores y sus límites permanecen intactos. El Q derivado todavía requiere
regeneración dentro del expediente completo de cierre.

`integracion_s434_s560_2026-09-26.json` fija las cinco altas locales: JATS de S560,
tres suplementos XLSX de S434 y su XML eLife v3. SHA-256:
`807aa4e8cf6e01a620243f159585c2a1c554e53e1cc2a3460c520012a675f215`.
Los 442 archivos previos conservaron nombre, tamaño y contenido. Inventario final:
447 archivos, SHA-256
`eb65a6efc4b262af7edb4488ea907c29f7dba2c4e4f61fd76472b653aa547f93`.
No se sobreescribieron originales ni se forzó su inclusión en Git.

El contrato de BN cambia nominalmente de 498/486/12 a 497/485/12; sigue exigiendo
410 residuales, 408 consultas negativas y los dos positivos nominados. Ahora
rechaza la reintroducción tanto de BN-120 como de BN-132, incluso si se compensa
retirando otra BN. Las pruebas preservan ambas historias y las unidades de S560.

Tras regenerar por el nuevo inventario, las 408 filas v3 cambian exclusivamente
la cantidad y huella del inventario; las otras 89 filas activas siguen idénticas.
Esto se comprobó recuperando las huellas anteriores, no suponiéndolo a partir
de los recuentos. Evidencia: `integridad_delta_s560_bn132_2026-09-27.json`.

## Ejecuciones y límites

- Suite completa final de esta integración: **221 pruebas, cero fallos**.
- Validación: **2824 C, 525 S, 1503 B, 108 eventos, 216 fechas, 82 hipótesis,
  600 magnitudes, 497 BN y 97 tablas**. Auditoría semántica automatizada correcta.
- Claves C, procedencia, censos de magnitudes, linaje, trazabilidad y derivados
  ordinarios regenerados; trazabilidad: **4475 segmentos**.
- Reinspección literal por el autor: **410/410** resultados iguales entre búsqueda
  directa e índice; **408 ceros**, C-2472 = 3 y C-2489 = 5. Se ejecutó realmente
  entre **2026-09-27T00:00:32Z y 2026-09-27T00:06:31Z**. El nombre fechado 26
  del archivo no se usa como fecha de ejecución.
- Evidencia nueva de consultas:
  `evidencia_reinspeccion_autor_bn_v3_2026-09-26_inventario447.csv`, SHA-256
  `98781bb0c54d32d99deae6a6b333234d7b1775a2c2896b09a1911c4cbaa614e3`.
- Cronología: 841 → 1249 filas; las 841 primeras siguen byte por byte idénticas,
  con SHA del prefijo `3576e5d5e8ba0bf95d58a9eda0ee9c830791e19b6b56f8709fb663b190edd059`.
  Cero errores de carga. Son registros de ejecución del autor, no firmas ajenas.
- QA externa: **97 CSV, 63201 celdas y cero diferencias** mediante
  `@oai/artifact-tool` 2.8.59 y Node v24.19.0 del bundle 26.909.12148. El primer
  intento fue bloqueado por WSL; el reintento autorizado fuera del sandbox pasó.
  No se instalaron dependencias. Las 97 huellas volvieron a comprobarse después.
  Evidencia: `qa_tabular_externa_2026-09-27_corpus2824.json`, SHA-256
  `e071a7d7df2ebed75d9acf4fc678326c5efb583331fcd5bfad01e1aded2d9917`.

El listado de acceso también se regeneró. Tres archivos disponibles se
contaban como ausentes por la etiqueta heredada `descargada` en vez de
`descargado`: S129, S381 y S559. Se comprobaron archivo, huella prefijada y
formato antes de cambiar solo la etiqueta, conservando las fechas históricas.
La evidencia `normalizacion_etiqueta_acceso_2026-09-27.json` retiene ambas filas
y los SHA completos observados. El listado registra ahora 285 obtenidas y
240 restantes de 525; esa clasificación de acceso no adjudica soporte científico.

No se crearon censos, firmas nominales ni aprobaciones globales. Siguen ausentes
las dos revisiones de las 2824 C y obsoleta la congelación; los 210 controles
manuales no están adjudicados. La nueva matriz S y la congelación deben prepararse
cuando el corpus y los expedientes se estabilicen. Esta integración no certifica
`make verify` completo, determinismo global ni verificación aislada del cierre.
