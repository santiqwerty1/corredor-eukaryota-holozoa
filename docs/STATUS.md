# Estado del encargo

**Fecha de cierre:** 8 de agosto de 2026.

**Versión:** `0.6.0-research-audit`.

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

## Resultado canónico

- 1.937 afirmaciones.
- 517 fuentes.
- 1.491 entidades.
- 109 eventos.
- 212 fechas.
- 81 hipótesis.
- 553 magnitudes.
- 68 búsquedas negativas activas.
- 106 búsquedas negativas históricas auditadas.
- 91 tablas canónicas.

## Evidencia y verificación

- [Revisión de las búsquedas negativas](auditorias/REVISION-BUSQUEDAS-NEGATIVAS-2026-08-08.md).
- [Matriz de disposición de las búsquedas negativas](auditorias/revision_busquedas_negativas_2026-08-08.csv).
- [Matriz de trazabilidad del contenido](auditorias/matriz_trazabilidad_contenido_2026-08-08.csv).
- [Mapa de claves iniciales y finales](auditorias/mapa_claves_inicial_final_2026-08-08.csv).

La puerta de calidad reproducible es `make verify`; comprueba el renderizado y
las exportaciones, la estructura, las auditorías, el linaje de tablas y las
pruebas automatizadas, y repite el conjunto en una copia aislada con doble
renderizado idempotente.

Los huecos restantes están declarados como resultados de investigación con una de las tres etiquetas del encargo; no representan fases de redacción pendientes.
