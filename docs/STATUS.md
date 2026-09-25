# Estado del encargo

**Fecha de corte bibliográfico:** 8 de agosto de 2026.

**Versión:** `0.6.0-research-audit`.

**Estado a 25 de septiembre de 2026:** encargo original completo; auditoría de
cierre abierta desde el checkpoint del 13 de agosto; encargo de seguimiento sin
empezar. El detalle de cada frente está más abajo.

## Completado

- Secciones 0–15 y cierre de las seis preguntas.
- Sección 13 con escalas, tasas, duraciones y recuentos.
- Remediación investigada de ambiente, ecología, trofismo, asociaciones y gradiente mitocondrial.
- Sección 15 con mapa probatorio, evidencia retirada o reinterpretada, relaciones débiles y 68 búsquedas negativas activas etiquetadas.
- Revisión individual de las 106 búsquedas negativas históricas: 68 continúan activas y 38 fueron retiradas, con disposición y evidencia conservadas en una auditoría reproducible.
- Agenda posterior asignada para las 68 filas activas: 22 P0, 23 P1 y 23 P2, cada grupo con criterios de éxito y detención.
- Registros canónicos y apéndices A–H.
- Renumeración global, exportaciones, versión de lectura y versión autocontenida.
- Validación estructural, auditoría de migración y auditoría semántica.
- Checkpoint del 13 de agosto: 319 filas de afirmaciones corregidas en la columna
  `Fuente`, marcadores de soporte añadidos a nueve fuentes y derivados
  regenerados.

## Resultado canónico

Recuentos leídos de los CSV, que son los que declaran `manifest.json` y
`data/apendices/H_recuento_control.csv`:

- 1.952 afirmaciones.
- 523 fuentes.
- 1.500 entidades.
- 109 eventos.
- 215 fechas.
- 81 hipótesis.
- 562 magnitudes.
- 68 búsquedas negativas activas.
- 106 búsquedas negativas históricas auditadas.
- 92 tablas canónicas: 78 heredadas y 14 posteriores.
- 3.209 segmentos de trazabilidad exacta.

El cierre del 8 de agosto declaraba 1.937 afirmaciones, 517 fuentes, 1.491
entidades, 212 fechas, 553 magnitudes y 91 tablas. La diferencia es trabajo de
la auditoría posterior, no una discrepancia: los derivados se regeneraron desde
los datos.

## Auditoría de cierre: abierta

El estado exacto y el orden recomendado para continuar están en el
[checkpoint del 13 de agosto](auditorias/HANDOFF_CODEX_2026-08-13.md). En
resumen:

| Puerta | Estado |
|---|---|
| renderizado, validación estructural, migración, linaje de tablas, trazabilidad, auditoría semántica y pruebas | pasan |
| `audit_requirement_controls.py --verify-artifacts` | 294 incidencias: 210 controles manuales sin adjudicar y artefactos sin rematerializar |
| `audit_full.py` | 12.574 hallazgos, casi todos segunda revisión pendiente y huellas desactualizadas |
| S420 | retirada del apéndice A pero citada todavía en la matriz de fuentes y en R-0288–R-0320 |

Por eso `make verify` falla y la CI está en rojo desde, como mínimo, el 10 de
agosto: la puerta incluye esas dos auditorías y **no se ha debilitado para que
pase**. Es el estado esperado mientras la auditoría siga abierta.

## Encargo de seguimiento: sin empezar

El proyecto que consume este corpus envió un encargo de seguimiento
(`docs/campaigns/C01-ENCARGO-SEGUIMIENTO.md` en `eslabon-perdido`). Tres de sus
puntos rigen desde el 12 de agosto para todo contenido nuevo y están recogidos
en el checkpoint: localizador con apartado, fuente accesible como desempate y
definición de cada predicado nuevo. El resto sigue pendiente, en particular la
sección nueva sobre sexo, anisogamia y mitocondria y las definiciones de los 308
predicados con asterisco.

Dos puntos de ese encargo ya están resueltos por los datos: el manifiesto y el
apéndice H cuadran con los CSV, y el recuento de afirmaciones de fuente única es
1.195.

## Versión congelada para la ingestión

El 25 de septiembre de 2026 `eslabon-perdido` congeló esta versión, `af7e799`,
como corpus de partida de la Campaña 1. La congelación fija la huella de la capa
canónica —`data/` y `docs/secciones/`—, no la del repositorio entero, así que un
commit que sólo regenere derivados o documentación sigue verificando contra
ella.

Los resultados de auditoría que lleguen después **no se aplican sobre la versión
congelada**: se congelan como versión nueva y se ingieren por diferencia contra
la anterior. Cualquier cambio en `data/` o `docs/secciones/` produce, por tanto,
una versión distinta a ojos del consumidor.

## Evidencia y verificación

- [Revisión de las búsquedas negativas](auditorias/REVISION-BUSQUEDAS-NEGATIVAS-2026-08-08.md).
- [Matriz de disposición de las búsquedas negativas](auditorias/revision_busquedas_negativas_2026-08-08.csv).
- [Matriz de trazabilidad del contenido](auditorias/matriz_trazabilidad_contenido_2026-08-08.csv).
- [Mapa de claves iniciales y finales](auditorias/mapa_claves_inicial_final_2026-08-08.csv).
- [Checkpoint del 13 de agosto](auditorias/HANDOFF_CODEX_2026-08-13.md).

La puerta de calidad reproducible es `make verify`; comprueba el renderizado y
las exportaciones, la estructura, las auditorías, el linaje de tablas y las
pruebas automatizadas, y repite el conjunto en una copia aislada con doble
renderizado idempotente.

Los huecos restantes están declarados como resultados de investigación con una de las tres etiquetas del encargo; no representan fases de redacción pendientes.
