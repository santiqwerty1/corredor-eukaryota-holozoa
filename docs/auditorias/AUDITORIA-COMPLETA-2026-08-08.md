# Auditoría científica integral — 2026-08-08

## Veredicto

**Veredicto documental:** EN CURSO: la remediación está materializada, pero la segunda revisión independiente sigue abierta.

## Metodología

La auditoría cubre el encargo literal de las secciones 0–18, las 1.840 afirmaciones y 525 fuentes iniciales, las tablas y los apéndices A–H, las 106 búsquedas negativas históricas y las 68 activas. El estado inicial se toma exclusivamente de la instantánea externa congelada; cada fila se fija con SHA-256 antes de mapearla al corpus final.

Ancla del prompt: `5245393c50c7a1620ef81f42cdfd92c5632b9218a153a0e0ad2d560a3314ffb3`. Manifiesto de hallazgos congelados: `2d2c2537edbe86f3f19a548b5d6bcbfddca8107cd25c7a674f1c1c68c3bd0661`.

Este constructor no consulta la red y no convierte metadatos, presencia de una cita o un localizador en una inspección de pasaje. Materializa las decisiones y evidencias ya documentadas, recalcula cobertura y huellas, y deja abierta cualquier segunda revisión que no tenga firma independiente. `NO_VERIFICABLE` significa que la pasada inicial no acreditó el pasaje; no significa que la afirmación sea falsa. Un hueco científico se conserva como hueco etiquetado, no como refutación.

## Resultado cuantitativo

| objeto | estado inicial | estado final |
|---|---:|---:|
| afirmaciones C | 1.840 | 1937 |
| fuentes S | 525 | 517 |
| entidades B | 1.536 | 1491 |
| eventos C | 111 | 109 |
| fechas D | 282 | 212 |
| hipótesis E | 81 | 81 |
| magnitudes F | 556 | 553 |
| BN activas / históricas | 68 / 106 | 68 / 106 |
| tablas indexadas | 90 | 91 |

- Estados C iniciales: {'CORREGIR': 1076, 'CONFORME': 65, 'NO_VERIFICABLE': 699}; severidades: {'P1': 1157, 'NINGUNA': 566, 'P0': 117}.
- Disposiciones C finales: {'CORREGIDA': 1775, 'CONFORME': 65, 'NUEVA': 19}.
- Severidades S iniciales: {'P2': 371, 'P1': 34, 'P0': 18, 'NINGUNA': 102}; disposiciones finales: {'CORREGIDA': 464, 'CONFORME': 48, 'RETIRADA': 13, 'NUEVA': 5}.
- Requisitos iniciales: {'NO_VERIFICABLE': 128, 'INCUMPLE': 10, 'PARCIAL': 205, 'CUMPLE': 140}; estados finales: {'CUMPLE': 235, 'NO_APLICA_JUSTIFICADO': 133, 'CUMPLE_MEDIANTE_HUECO_ETIQUETADO': 115}.
- Agenda BN activa: {'P2': 23, 'P0': 22, 'P1': 23}; registro total: 170 (165 filas congeladas y 5 altas documentadas).

## Hallazgos por severidad

El corte inicial registró P0/P1 en C como {'P1': 1157, 'NINGUNA': 566, 'P0': 117} y en S como {'P2': 371, 'P1': 34, 'P0': 18, 'NINGUNA': 102}. Tras aplicar las disposiciones y destinos de las matrices:

- P0 abiertos: 0
- P1 abiertos: 0
- Los huecos científicos reales permanecen etiquetados y no se cuentan como falsedades.
- La segunda revisión abierta es una condición de aceptación independiente, no un hallazgo científico reclasificado silenciosamente.

## Delta de apéndices

El delta B–G se reconstruye fila por fila. En D se retiraron exactamente 107 filas sin C que contenían exclusivamente metadatos de publicación o fechas internas de corte. No eran 107 estimaciones científicas perdidas. Tras el estado intermedio de 189 filas, la pasada final incorporó o reconcilió 24 fechas científicamente pertinentes y retiró una fila que describía un estado ancestral, no una fecha. Las 212 filas D finales tienen todas una C válida. En F se retiró además un recuento sintético de tres adquisiciones que no era una magnitud publicada; la síntesis C correspondiente se conserva.

- B: {'SIN_CAMBIO': 4, 'ACTUALIZADA': 1485, 'RETIRADA': 47, 'ALTA': 2}.
- C: {'ACTUALIZADA': 109, 'RETIRADA': 2}.
- D: {'SIN_CAMBIO': 5, 'ACTUALIZADA': 137, 'RETIRADA': 140, 'ALTA': 70}.
- E: {'ACTUALIZADA': 81}.
- F: {'SIN_CAMBIO': 1, 'ACTUALIZADA': 505, 'RETIRADA': 50, 'ALTA': 47}.
- G: {'ACTUALIZADA': 22, 'SIN_CAMBIO': 1, 'RETIRADA': 1}.

## Correcciones

Las filas P0/P1 conservan acción y evidencia iniciales, destino final y huellas de ambos estados. Las altas usan claves `NUEVA:...`; ninguna reemplaza una clave histórica. Las fuentes retiradas permanecen en la instantánea y en la matriz S con motivo y destino, y su retirada por falta de uso canónico no se presenta como desestimación de la publicación.

Las correcciones históricas BN tienen una columna delta explícita. Se conservan solo intervalos publicados donde los valores centrales no estaban publicados, y el presupuesto de *Trypanosoma brucei* conserva el total y el residual publicados. S549 se registra como modelado hidrodinámico, no como medición metabólica.

## Segunda revisión

La matriz `segunda_revision_2026-08-08.csv` contiene 2060 objetos: censo del 100 % de P0/P1 y muestras deterministas del 15 % por estrato, incluidas prosa, aristas y celdas. Estado: 2060 abiertos; 0 fallos detectados y corregidos. Una firma previa solo se conserva si coincide la huella exacta del objeto; un cambio la devuelve a pendiente. El constructor nunca firma por el revisor.

## Límites restantes

- El corte bibliográfico es 2026-08-08; evidencia posterior exige una nueva delta, no una reescritura silenciosa.
- Una fuente inaccesible o un pasaje no inspeccionado no cuenta como verificado: debe permanecer degradado, retirado o como hueco documentado.
- Las incertidumbres filogenéticas, cronológicas y mecanísticas reales no se cierran por automatización.
- No se crea release, PDF, rama, commit ni publicación remota mediante este constructor.

## Entregables reproducibles

Las cuatro matrices principales, el registro histórico BN enriquecido, el delta B–G, la segunda revisión y el JSON reproducible se generan en `docs/auditorias/`. Las huellas del prompt, maestro archivado, entradas congeladas y salidas quedan en el JSON. La validación final corresponde a `make verify` en el workspace y en una copia aislada; el JSON documenta esos comandos, pero no se autoatribuye su resultado.
