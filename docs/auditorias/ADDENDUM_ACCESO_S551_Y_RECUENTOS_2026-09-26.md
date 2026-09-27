# Addendum independiente: S551 y recuentos del índice de acceso

Revisión finalizada: 2026-09-26T22:04:26Z. Revisor: /root/verificacion_fuentes_nuevas.

CONFORME para el delta bibliográfico de S551 y la integración mecánica de los
recuentos en las 524 filas del índice. No es una aprobación de apoyo científico
ni una nueva clasificación del acceso o identidad del resto de fuentes.

## S551

La fila de acceso identifica ahora 1964 y la URL institucional con #ndbcontent,
en correspondencia con A y la evidencia nominal Uschmann/NDB 6:605 ya revisada.
Frente a HEAD solo cambian año, URL y nota explicativa. Se conserva el nombre
histórico «S551 [2026, consulta] Goldfuß Georg August.pdf», obtenido_el
2026-08-10 y el estado de identidad anterior; no se atribuye una nueva descarga.
Los bytes del PDF coinciden con la primera inspección independiente: SHA-256
`93bddae4824bddfe29fe136faa1916ff8c5a659da717d95955e4a953e8ae08db`. Esta revisión comprueba transcripción, no repite esa verificación
bibliográfica ni se presenta como una segunda aprobación de mi propio dictamen.

## Utilidad y censo de recuentos

El delta en fetch_oa.py sustituye la extracción de claves aisladas por
expand_source_refs y conserva la deduplicación por afirmación. Se revisó la
importación tanto como módulo como script (--help, sin consultas ni descarga).
Se ejecutaron las tres pruebas nuevas y otras seis de rangos: 9/9 correctas.

Se cotejaron las 2.820 filas del export con todas las filas canónicas; coinciden
íntegramente. El recuento independiente enumera expresamente los conjuntos de
C-840, C-969, C-1630 y C-1646, los cuatro casos vivos que contienen rangos S de
dos/tres dígitos o etiquetas suplementarias de esa longitud. Para las demás
filas toma claves literales, deduplicadas por afirmación. Así no reutiliza el
helper bajo prueba para calcular esos resultados esperados.

Coinciden las dos columnas de las 524 filas: 3.130 relaciones afirmación–fuente,
513 fuentes con alguna cita y 1.513 afirmaciones con una sola clave. El cambio
recupera interiores de rangos; además excluye las figuras S62–S63 de C-840,
dejando S27 como única clave de esa afirmación. Dos llamadas consecutivas dieron
el mismo resultado y no alteraron archivos. La conformidad es del cómputo de
referencias, no del valor científico o del significado de cada cita textual.

No se atribuyen a esta corrección todos los cambios del índice frente a HEAD:
el corpus también ha cambiado. La evidencia separa el efecto del regex antiguo
y el nuevo sobre el mismo export vivo y conserva las filas nominales cotejadas.

## Evidencia y preservación

- CSV nominal: docs/auditorias/revision_recuentos_acceso_2026-09-26.csv; SHA-256 `dd6adeb05eab4afc8c984eeb9bdb43b6a7997c4e60cecf50b2f4d3d1ab776629`.
- Evidencia: docs/auditorias/evidencia_addendum_acceso_s551_impacto_2026-09-26.json; SHA-256 `71f8c35d13617a044820b3494388062193b1541025a6d1fc933b3036c8f6782b`.
- Export inspeccionado: SHA-256 `bda2508d0aa38cb87b260175b99af1047eedbd832ef2014ccbc999554b038f86`.
- Inventario fuentes/: 442 archivos; SHA-256 `69704030a52076437e131fde0a1b886605b3ed8efc6a8fcf272660df3e4503cd`, idéntico al
  inventario de la integración de ocho copias. No se han cambiado esos archivos.

La evidencia y el informe previos de ocho copias permanecen intactos. S545 y
los metadatos S548/S549/S557 no se vuelven a adjudicar en este addendum. Tampoco
se editan corpus, índice, código, registros temporales ni firmas anteriores.
Esta evidencia es una revisión del estado y hashes aquí observados, no del
resultado futuro de una regeneración o de make verify.
