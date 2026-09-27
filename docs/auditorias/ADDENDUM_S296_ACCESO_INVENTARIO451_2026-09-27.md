# Addendum independiente: S296, acceso e inventario 451

Revisor: `/root/verificacion_fuentes_nuevas`; autor de cambios: `/root`.
UTC final: 2026-09-27T01:31:58Z. Rama: `codex/cierre-plan-pendiente`.
No se modificaron corpus, fuentes, A, export ni firmas.

## S296: discrepancia preservada y versión correcta

El PDF anterior, SHA `1b6271c98a3515b26f8b8be56b2a3567d611253c17274df35861127bad2d54fe`,
es el preprint bioRxiv 10.1101/033464 de diciembre de 2015, versión interna009,
36 páginas y título distinto. **NO COINCIDE** con la publicación PNAS2016
identificada en A. Se conserva la discrepancia nominal en el CSV; no se
sobrescribe ni renombra el documento histórico.

El nuevo HTML completo PMC4983863, SHA
`386809ac25942beaf0f8351ff6c3e2f3dc9de7b11b07210bc75908a915eb2136`,
sí coincide en título, diez autores, DOI10.1073/pnas.1600338113 y
PNAS113(18):5053–5058. Se cotejaron la cabecera y estructura íntegra del HTML,
el depósito DOI y los registros oficiales. Fecha online:24-03-2016;
edición impresa:03-05-2016. [PubMed](https://pubmed.ncbi.nlm.nih.gov/27035985/).

La descarga propia adicional de PMC devolvió un desafío, no el artículo;
no se usa para certificar igualdad de archivos. El HTML local se inspeccionó
como documento completo, no se aprobó por el nombre del archivo. Las
relaciones de comentario y preprint observadas no son corrigenda; tampoco
su presencia o la falta de alertas prueba una revisión editorial universal.
No se presume equivalencia científica entre preprint y versión publicada.

## Preservación y acceso

Inventario451 observado:
`62fe8db317f35c6679f79343610a8ebd1e1069944c66769b477742860e2791bc`.
Al excluir únicamente el HTML nuevo del cálculo se recuperan450archivos y
`170c7d69a86dbc8361aed5214e5e2c1452b5fee54c382b4cfb3cd61f02960647`.
El corte450 ya está ligado independientemente a448→447→442. No se
sobrescribieron archivos anteriores, incluido el PDF preprint.

Se inspeccionaron las filas de acceso S296/S512/S560/S561/S562: DOI, nombre,
formato real, URL, SHA completa y fecha de recuperación son compatibles
con los artefactos observados. `url_pdf` es un nombre de columna heredado:
S296/S562 se declaran expresamente HTML y S560/S561 JATS, no PDF.
Restaurar las dos filas previas S296/S512 y excluir la alta S562 del CSV
inicial inspeccionado reconstruye exactamente el SHA previo de526filas.

Se conservó además un hallazgo real de vigencia: a01:26:48UTC los recuentos
coincidían; al incorporarse C-2838, el mismo CSV dejó S290=7/6 mientras el
corpus pasó a8/7. La evidencia inicial conserva este **NO_CONFORME**.
Tras la corrección de autor, a01:31:58UTC la reinspección encontró cero
diferencias en las527filas. Restaurar solo esas dos celdas S290 reproduce
la SHA completa anterior: no se modificó otra celda del export.

CSV final inspeccionado:
`8dc16c54c1e44e6b126efec71517c6756246233d0c1c4dd1176d914bc1229959`.
527claves únicas;288obtenidas y239restantes según los estados de acceso;
LF sin CR. Son cuentas de obtención y citas, no527identidades aprobadas.

## Evidencia y límites

- `addendum_identidad_s296_2026-09-27.csv`: dos artefactos nominales, con
  NO_CONFORME de la antigua versión y CONFORME acotado del HTML publicado.
- `evidencia_s296_acceso_inventario451_2026-09-27.json`: conserva el primer
  estado y su discrepancia de recuentos; SHA
  `ac2d039a82776be083d62ceb5f43d1e6b45cbadd428bf6ed0afe5c9e61c52794`.
- `reinspeccion_acceso_s290_inventario451_2026-09-27.json`: nueva evidencia
  de los recuentos corregidos, sin alterar la anterior.

Dictamen final de este subalcance: conformes identidad/acceso del HTML final,
integridad451→450 y vigencia de los recuentos corregidos. La identidad del
antiguo PDF como PNAS2016 sigue NO_CONFORME y se conserva como historia.
No se adjudica apoyo científico ni estado editorial integral; no se crean
censos o firmas nominales de cierre ni se declara cerrado el plan.
