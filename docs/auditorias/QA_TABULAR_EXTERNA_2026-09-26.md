# QA tabular externa — 2026-09-26

Resultado: las **97 tablas canónicas**, incluidas cabeceras y todas sus
**63.013 celdas**, coinciden exactamente entre el lector CSV canónico de Python
y la importación independiente mediante `Workbook.fromCSV` de
`@oai/artifact-tool` **2.8.59**. Cero diferencias de dimensiones o contenido.
No se convirtieron cadenas en números o fechas ni se reescribieron tablas.

Se utilizó el runtime empaquetado de Codex, bundle `26.909.12148`, con Node
`v24.19.0`. El primer intento dentro del sandbox volvió a producir
`WSL ERROR: UtilBindVsockAnyPort:309: socket failed 1`; el reintento autorizado
fuera de ese sandbox permitió ejecutar el mismo runtime. No se instalaron
bibliotecas ni se modificaron dependencias empaquetadas.

El resultado ya estaba disponible al observar el reloj a
`2026-09-26T21:10:37Z`; no se reconstruye una hora exacta de inicio ausente.

## Evidencia y alcance

- `qa_tabular_externa_2026-09-26.json`: las 97 rutas, SHA-256 de cada CSV,
  dimensiones esperadas y observadas, y huellas de cada matriz completa.
- SHA-256 del JSON: `3893a94d2ce4155844345d6348740da27c30d2aaa36b28e90ed4aed74258444a`.
- `scripts/check_external_csv_qa.mjs`: ejecutor sin escrituras en el corpus.

La comparación de matrices usa JSON UTF-8 sin espacios separadores y sin
escapar caracteres Unicode. Cada valor debe conservarse como cadena; una
conversión automática cambia la huella y hace fallar la comprobación.

Esta prueba cierra el reintento de interoperabilidad y lectura tabular externa
descrito en el handoff. **No acredita apoyo científico, revisiones manuales,
ni la ejecución completa de `make verify`.** Sus resultados solo corresponden
a las huellas registradas; cualquier tabla cambiada debe reinspeccionarse.

## Reproducción

Preparar un JSON de expectativas con el índice vivo y `csv.reader`. Una fila
por tabla contiene `path`, `sha256_csv`, `rows` (incluida cabecera), `columns`
y `sha256_matrix`. La matriz incluye cabecera y celdas, serializadas con
`json.dumps(matrix, ensure_ascii=False, separators=(',', ':'))` antes de SHA-256.

Ejecutar el script con cuatro argumentos posicionales contando el propio
script: ruta al módulo `artifact_tool.mjs` del runtime empaquetado, raíz del
repositorio y ruta al JSON de expectativas. Usar las rutas nativas del sistema
en el que corre Node; en Windows pueden leerse archivos WSL por UNC.
Guardar stdout como diagnóstico JSON y exigir código de salida cero y
`failures = 0`. El ejecutor verifica primero que cada CSV conserva la huella
usada al preparar las expectativas; no acepta comparar versiones diferentes.
