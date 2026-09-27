# Revisión independiente de integración de fechas BN v3

Revisor: `/root/revision_residuales`, independiente de la integración realizada
por `/root`. Comprobación final: **2026-09-26T21:28:22Z**. Rama:
`codex/cierre-plan-pendiente`.

**CONFORME para la copia nominal de las 408 fechas de reinspección.** Este
addendum no modifica ni sustituye los informes anteriores; tampoco aprueba
objetos científicos, búsquedas originales, controles manuales o cierre global.

| Objeto cotejado | SHA-256 |
|---|---|
| `data/auditoria/fechas_ejecuciones_bn.csv` | `f8377b7feead3bd281e0963dae658c265add5d256e89e49c81c1273dd4347114` |
| `docs/auditorias/evidencia_reinspeccion_bn_v3_2026-09-26.csv` | `980c5c51189f44f5bbb694006d9ecea6a6df919ce78e473a202fde9207f082b1` |

Se compararon todas las filas, no una muestra:

- 408 registros, 408 claves únicas y cobertura exacta de las 408 BN v3
  derivadas del censo residual, excluidos los dos pasajes positivos. BN-557
  no fue añadida a este registro.
- Copia literal de clave, huella de fila BN e instante de ejecución; clase
  exclusivamente `REINSPECCION`. Los instantes conservados van de
  `2026-09-26T21:20:54Z` a `2026-09-26T21:21:43Z`.
- Ruta y SHA de evidencia correctos en las 408 filas. Cada localizador
  identifica exactamente su fila CSV, clave BN, C residual y resultado cero
  de la evidencia nominal correspondiente.
- Las 408 huellas de fila coinciden con el JSON canónico de las BN vivas.
  No se añadieron fechas originales, dictámenes científicos ni campos de
  aprobación al contrato de siete columnas.
- `load_search_dates(root)` devolvió **408 filas y cero errores**.
- Se recalculó también el inventario actual de `fuentes/`, leyendo todos
  sus archivos: **434 artefactos**, huella
  `a08bc1a1584b2a31a0da0d84efd1de350abf318b9a2cfa7e0a94e0f34cb0f043`,
  idéntica a la de la ejecución documentada.

La conformidad queda limitada a esas versiones. Una modificación del universo
de `fuentes/` no puede heredar esta prueba: vuelve obsoleta la consulta respecto
del nuevo universo; al regenerarse las filas BN con el nuevo inventario,
cambiarán sus huellas y estas fechas no deben transferirse. Cero errores del
cargador temporal, por sí solo, no demuestra que las fuentes sigan intactas.
Este dictamen no autoriza reconstruir fechas originales desconocidas ni
reinterpretar cero coincidencias literales como ausencia científica.

Esta actuación solo creó el presente addendum; no transformó registros,
evidencia previa, fuentes ni datos científicos.
