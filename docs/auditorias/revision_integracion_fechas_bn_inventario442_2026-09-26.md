# Revisión independiente de integración de fechas BN: inventario 442

Revisor: `/root/revision_residuales`, distinto del autor de la integración,
`/root`. Comprobación terminada: **2026-09-26T22:01:19Z**. Rama:
`codex/cierre-plan-pendiente`.

**CONFORME exclusivamente para la integración de las 408 nuevas ligaduras de
reinspección v3.** Este addendum conserva los dictámenes anteriores y no
reaprueba BN-558, fuentes, afirmaciones científicas, controles manuales ni
segundas revisiones globales.

| Objeto comprobado | SHA-256 |
|---|---|
| `data/auditoria/fechas_ejecuciones_bn.csv` | `d61ca90536e7ba2f80b797569bb90c1169fae1d74d888e132146638b4e7e91af` |
| `docs/auditorias/evidencia_reinspeccion_bn_v3_2026-09-26_inventario442.csv` | `e9c1e5370a9f1a3e6450929d1ef212a01ff9deca29c80ebcbb290266af6f1036` |

Se cotejaron todas las filas, sin muestreo, mediante un programa independiente
de lectura, sin invocar un generador ni modificar el registro:

- El CSV tiene 817 filas y 817 parejas únicas `(clave_bn,
  huella_fila_bn_sha256)`: las 408 anteriores, la fila separada BN-558 y las
  408 nuevas. `load_search_dates(root)` devuelve 817 filas y cero errores.
- El prefijo de bytes completo del registro anterior —cabecera más sus 408
  filas— conserva SHA-256
  `f8377b7feead3bd281e0963dae658c265add5d256e89e49c81c1273dd4347114`.
  Por tanto, no se reemplazaron ni refirmaron esas entradas históricas.
- Las 408 nuevas claves, huellas, clases `REINSPECCION` e instantes son copia
  literal de las 408 filas de la evidencia 442, una por clave. Los instantes
  permanecen entre `2026-09-26T21:49:40Z` y `2026-09-26T21:53:18Z`; no se han
  convertido en fechas originales ni sustituido por la fecha de integración.
- Cada ruta y SHA de evidencia corresponde al artefacto nominal. Cada
  localizador coincide exactamente con su fila CSV, BN, C residual,
  `artefactos_censados=442` y `coincidencias_artefactos=0`.
- Las 408 huellas nuevas coinciden con las filas BN vivas, usando JSON
  canónico de la fila completa, claves ordenadas, `ensure_ascii=False`,
  separadores `,` y `:`, y LF final. Las 408 huellas antiguas son distintas y
  ninguna coincide con su versión viva: quedan como historial, no como prueba
  vigente prestada al inventario nuevo.
- Hay exactamente 409 ligaduras vigentes: las 408 nuevas más BN-558. Las
  pruebas v3 no incluyen BN-557 ni BN-558. La fila temporal BN-558 conserva
  la huella canónica de fila
  `ff4d6fd2f6ccdeffd8046406d5af5de9087f0fcbb56ae9583bbc428880fd6f43`,
  previamente consignada en la revisión independiente de integración
  cronológica de fuentes/BN-558; se comprobó además su enlace a la huella BN
  viva. Aquí se comprueba preservación, no su apoyo científico.
- Se volvieron a leer íntegramente los archivos de `fuentes/`: 442 artefactos,
  inventario SHA-256
  `69704030a52076437e131fde0a1b886605b3ed8efc6a8fcf272660df3e4503cd`,
  igual al de las 408 filas de evidencia. El registro mantuvo su SHA antes y
  después de esta comprobación.
- La evidencia histórica 434 conserva SHA-256
  `980c5c51189f44f5bbb694006d9ecea6a6df919ce78e473a202fde9207f082b1`.
  El esquema sigue siendo el contrato de siete columnas: no se añadieron
  campos de aprobación ni objetos científicos por esta integración.

La comprobación ejecutada fue
`python3 /tmp/revision_integracion_fechas_bn442_20260926.py`, salida 0; huella
del programa revisor:
`31af9e9f83f242105646afce167fa75e7a7fa28f5526e103a44ff34ba625e8c9`.
Los contrastes anteriores describen sus aserciones; el programa temporal no
forma parte del registro ni es prueba sustitutiva de la ejecución de las
consultas. Las consultas y sus resultados siguen acreditados por la evidencia
nominal y el dictamen `revision_residuales_inventario442_2026-09-26.md`.

Esta conformidad es de integración y solo para estas versiones. Otro cambio
de inventario o de fila BN exige una nueva observación y ligadura; no se puede
transferir una fecha pasada. Cero coincidencias literales no equivale a
ausencia científica. La existencia del registro tampoco demuestra cierre
manual o global. Esta actuación solo añade el presente documento; no altera
el corpus, las fuentes, los registros ni los informes anteriores.
