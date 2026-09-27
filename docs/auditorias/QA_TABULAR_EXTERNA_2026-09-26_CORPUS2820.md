# Repetición de QA tabular externa — corpus de 2820 C

La ejecución con el runtime empaquetado de Codex y `@oai/artifact-tool` 2.8.59
terminó con código cero: **97 CSV, 63.072 celdas y cero discrepancias** frente
a `csv.reader`. Se incluyen las cabeceras y se comparan todas las cadenas,
sin convertir números o fechas ni reescribir tablas. Las 97 huellas seguían
vigentes al comprobar el resultado y consultar el reloj a
`2026-09-26T22:01:42Z`; no se inventa una hora exacta de inicio.

La evidencia nominal es `qa_tabular_externa_2026-09-26_corpus2820.json`,
SHA-256 `bb8d1b72539e5c64267e8d89d89217385b19cbd842c741fccea43b7bde72fcac`.
Contiene ruta, huella del CSV, dimensiones y huellas de las matrices completas
esperadas y observadas. El ejecutor es `scripts/check_external_csv_qa.mjs`;
se siguió el procedimiento de `QA_TABULAR_EXTERNA_2026-09-26.md` con un nuevo
JSON de expectativas preparado desde el índice y los CSV vivos. Se usó el
mismo bundle 26.909.12148 y Node v24.19.0, mediante el reintento autorizado
fuera del sandbox que impide la interoperabilidad WSL/Windows. No se instaló
ni modificó ninguna dependencia.

La prueba anterior de 63.013 celdas se conserva como historia de otra versión.
Esta repetición incluye las correcciones de S548, las glosas de BN y C-2820.
Una alteración posterior de un CSV invalida únicamente la correspondencia de
esa versión con esta evidencia: deberá repetirse la comprobación pertinente.

El dictamen es de interoperabilidad y fidelidad tabular. No aprueba contenido
científico, censos semánticos, requisitos manuales, segundas revisiones ni
la ejecución completa de `make verify`.
