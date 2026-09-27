# Revisión independiente de fuentes recientes e inventarios

Revisor: `/root/verificacion_fuentes_nuevas`, distinto de `/root`, autor de las
integraciones. Rama: `codex/cierre-plan-pendiente`. Inspección del primer lote:
2026-09-27T01:14:36Z–01:23:13Z. No se modificaron A, artículos, corpus,
cronología ni firmas reales. Las descargas propias quedaron exclusivamente
en `/tmp/revision-fuentes-recientes-20260927.86d6S8/`.

## Resultado acotado

Conformes la identidad bibliográfica, el tipo documental comprobable y el
acceso material de S560, S561, S512 y S562. No se aprueba su apoyo científico
ni una revisión editorial universal. El CSV nominal conserva expresamente
`NO_VERIFICABLE` para el cierre editorial integral: falta de aviso en los
servicios consultados no demuestra inexistencia de avisos.

| Fuente | Resultado documental observado |
|---|---|
| S560 | JATS research-article, dos autores Wang/Wu; Frank Voncken es editor. Nueva recuperación de Europe PMC idéntica byte a byte al local. Título, DOI y fecha coinciden con [PLOS](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0110685). |
| S561 | Siete autores; eLife distingue manuscrito aceptado del 31-05-2019 y versión de registro v2 del 15-07-2019. El cuerpo, título y autores del JATS local coinciden tras normalización con XML editorial v2; `back` no coincide y no se declara igualdad integral. [Versiones editoriales](https://api.elifesciences.org/articles/45017/versions). |
| S512 | PDF editorial de diez páginas y seis autores; DOI, título y volumen 217:108532 coinciden con [KITopen](https://publikationen.bibliothek.kit.edu/1000189992) y depósito DOI. No es un resumen ni un preprint. |
| S562 | HTML íntegro PMC1182215, tres autores, Genome Research 15(8):1023–1033. La nueva respuesta oficial reproduce el texto normalizado de `article`; solo cambian dos tokens web fuera del contenido. No hay PDF/JATS local de esta alta. [Ficha editorial](https://genome.cshlp.org/content/15/8/1023.short). |

La inspección editorial incluyó JATS/cabeceras oficiales, cuatro depósitos
Crossref, cuatro registros Europe PMC y consultas nominales sobre corrección
o retractación. S561 enlaza un comentario y un preprint: no se cuentan como
corrigenda. Los campos de actualización vacíos no se convierten en aprobación.
Los bloqueos 403/429/503 y el alcance de cada consulta constan en la evidencia.
Las fechas de publicación, versión y recuperación se mantienen separadas.

## Integridad de las altas

Se recalcularon SHA, tamaño y nombre de cada archivo y se retiraron únicamente
las altas declaradas del cálculo, sin borrar archivos. La reconstrucción inversa
recupera exactamente estos cuatro cortes:

| Archivos | SHA-256 del inventario |
|---:|---|
| 442 | `69704030a52076437e131fde0a1b886605b3ed8efc6a8fcf272660df3e4503cd` |
| 447 | `eb65a6efc4b262af7edb4488ea907c29f7dba2c4e4f61fd76472b653aa547f93` |
| 448 | `1373e4658ea749685d9b9fdea95e800ff3bff56ab3d2012ae3b9d47d45d55bb6` |
| 450 | `170c7d69a86dbc8361aed5214e5e2c1452b5fee54c382b4cfb3cd61f02960647` |

Las ocho altas son cuatro artefactos S434, un JATS S560, un JATS S561,
un PDF S512 y un HTML S562. Los cuatro S434 conservan exactamente los SHA
de la propuesta y el cotejo anteriores; no se reevalúa aquí su ciencia.
El inventario completo de 450 nombres/SHA/tamaños queda en el JSON durable.
El posterior S296 y el corte 451 se registran separadamente en el addendum,
sin fingir que 450 continúa siendo el inventario final vivo.

## Pendientes anteriores: qué quedó realmente cubierto

- S126: ahora se cotejan explícitamente identidad, ocho autores y tipo con
  JATS/cabecera [PLOS](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3002794).
  Methods and Resources y research-article son compatibles con investigación
  primaria; esta comprobación no adjudica paneles, cifras o notas científicas.
- S548: huella A actual `233871dc64f3916d4ab38519893b6df351a14dd81c5d0cf5ff2716226184d2e0`,
  coincidente con la confirmación final nominal y con su ligadura cronológica
  ya revisada; publicación y preprint permanecen separados. No quedó pendiente
  en mi tarea una identidad bibliográfica, pero no se aprueba toda la fuente.
- S549: A conserva `097ed000f73c2b1da41fd1d90ddfcfeb5dd625525d89c3b5a5c811e94d54f540`;
  el PDF APS publicado permanece con su SHA inspeccionado. La revisión de
  C-1612/C-1613 y las dos consultas posteriores de BN-083 están en sus archivos
  previos; eso no certifica la ejecución integral de las trece consultas BN-083.
- S551: A conserva la huella del addendum que corrigió Uschmann/1964/NDB6:605;
  el nombre histórico del PDF y la fecha de descarga no se cambian.
- S559: original y dos corrigenda conservan sus SHA. El límite de recuperación
  del informe inicial ya fue cubierto por `evidencia_c006_s559_2026-09-26.md`
  y la integración independiente de ocho copias. Releí ambos avisos: financiación
  omitida y nombre/afiliaciones de A. Murat Eren. No se reemplaza el dictamen
  científico de C-006 ni se presume ausencia de otros avisos.

Se conservan todos los dictámenes y NO_CONFORME anteriores. La comparación de
huellas solo comprueba vigencia del objeto identificado; no amplía el alcance
de una firma bibliográfica a las notas científicas o al censo completo.

## Entregables

- `revision_fuentes_recientes_inventario450_2026-09-27.csv`: seis filas nominales,
  incluidas S126 y S559 en los subalcances expresos anteriores.
- `evidencia_fuentes_recientes_inventario450_2026-09-27.json`: metadatos observados,
  nueve huellas A, artefactos, consultas y reconstrucción íntegra del inventario.
  SHA-256 `f63b2adbbffc89eea0c66fc44bcd9664ddd37698eba8233c5e263addd8043252`.
- Auditor temporal propio: `/tmp/revision_fuentes_recientes_20260927.py`,
  SHA-256 `dcc0937cf07c85e4379debf4b0811c6a3bb68b4e625e9b221c795587b0891112`.
  El JSON durable conserva los resultados sin depender de la persistencia de /tmp.

Este lote no crea entradas del ledger nominal de cierre, no aprueba las 527
fuentes ni cierra controles, censos o `make verify`.
