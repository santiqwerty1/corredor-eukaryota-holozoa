# Revisión residual independiente — inventario de 442 artefactos

Revisor: `/root/revision_residuales`, distinto de `/root`, autor del cambio
de recuento y de la integración de fuentes. Rama:
`codex/cierre-plan-pendiente`. Este dictamen complementa, sin reescribir, la
revisión y evidencia anteriores del inventario de 434 artefactos.

**CONFORME para el delta de contrato 499/487/12 y para la nueva ejecución
literal nominal de las 408 BN v3.** No constituye revisión científica de
BN-557, BN-558, las nuevas fuentes o las C-2818/C-2819; no adjudica controles
manuales ni segundas revisiones globales.

## Delta de código, sin debilitamiento

Se cotejó la versión viva con la huella de la versión previamente revisada.
Revertir únicamente el comentario que identifica BN-557/BN-558 como ajenas a
v3 y `EXPECTED_BN_COUNTS = (499, 487, 12)` a `(498, 486, 12)` recupera
exactamente el SHA-256 anterior:
`d1e8d0a273fc5a24de14fe1b564211f1a9356d22d3b741a6de60f67245df19a4`.
Por tanto, no cambiaron el universo, la normalización, las consultas, el
índice, los dos positivos nominales, las 410 filas exigidas, las 408 BN v3
ni los controles de duplicados y coincidencias.

El cotejo análogo de los tests recuperó exactamente su huella anterior
`e0c6efaf8ad08106cdeed989919fe21e671d69dbd943b8a377352d7aa209b4d8` al retirar
el fixture y las aserciones adicionales de BN-558 y revertir las cuentas.
No se eliminó ninguna prueba anterior.

`python3 -m unittest tests.test_remediate_trace_residuals -v` pasó:
**10 pruebas, 10 aprobadas**, salida 0, 1,064 s. Tres adversarios propios
adicionales rechazaron:

- retirar BN-558: recuento inesperado 498/486/12;
- duplicar su clave sin cambiar el total: claves BN duplicadas;
- atribuir falsamente a BN-558 el marcador generado v3: recuento inesperado
  tras la regeneración.

Otro cotejo de fixture confirmó que todos los campos de BN-557 y BN-558 se
preservan literalmente, y que ambas quedan fuera de los 408 probes v3.
Esto prueba preservación mecánica, no validez científica de esas búsquedas.

## Reinspección real, no reutilización de fechas

Después de que finalizara la regeneración del autor, se ejecutaron nuevamente
las **410 consultas** sobre los **442 artefactos** vivos. Para cada consulta
se comparó la expresión literal histórica
`sum(all(component in text for component in components) for text in texts)`
con `ExactCooccurrenceIndex.count(components)`.

- Inicio observado: **2026-09-26T21:48:48Z**.
- Fin observado, incluida comprobación final del inventario:
  **2026-09-26T21:53:20Z**.
- **410/410 recuentos idénticos**; **408 consultas con cero coincidencias**.
- Únicas consultas positivas: **C-2472 = 3**, **C-2489 = 5**.
- Registro BN vivo: **499 claves únicas**, **487** no localizadas y
  **12** con ausencia declarada por la literatura; las 408 claves generadas
  v3 permanecen nominalmente separadas de BN-557/BN-558.

La evidencia nueva de 408 filas está en
`docs/auditorias/evidencia_reinspeccion_bn_v3_2026-09-26_inventario442.csv`.
Cada fila fija BN, huella actual de fila, C/celda residual, consulta exacta,
recuento, método, inventario/código/censo y el instante realmente observado.
Los instantes por consulta abarcan **2026-09-26T21:49:40Z** a
**2026-09-26T21:53:18Z**. La clase es exclusivamente `REINSPECCION`, no
`EJECUCION_ORIGINAL`.

Se verificaron las ocho copias contra el registro de integración y sus SHA.
El inventario completo se calculó al inicio y se volvió a hashear al final;
se mantuvo en 442 artefactos con la misma huella. También se comprobó que
las filas BN, el censo residual y el script permanecieron sin cambios durante
la ejecución. No se omitieron PDF, XML, XLSX, archivos tar ni otros archivos
admitidos por el universo histórico.

## Historial e invalidación preservados

Las 408 nuevas huellas BN son distintas de las de la ejecución de 434
artefactos. El registro temporal antiguo seguía siendo estructuralmente válido
(408 filas, cero errores de carga), pero **no aportaba ninguna ligadura a las
408 versiones regeneradas**. Se comprobó esa falta de coincidencia antes de
terminar la nueva ejecución: las fechas antiguas no se transfirieron por clave.

La evidencia antigua conserva su SHA
`980c5c51189f44f5bbb694006d9ecea6a6df919ce78e473a202fde9207f082b1` y no fue
sobrescrita. Este revisor no modificó `fechas_ejecuciones_bn.csv`, el corpus,
los tests ni las fuentes. La integración de las nuevas fechas debe realizarse
después y cotejarse por identidad **y huella**, manteniendo el historial.

## Huellas de esta revisión

| Objeto | SHA-256 |
|---|---|
| `scripts/remediate_trace_residuals.py` | `43855566ac6b29fd1e9b7dd98da500e07d1c2e4d68a50e2ff8d64d33e6db8b4d` |
| `tests/test_remediate_trace_residuals.py` | `2465199ed356723ccacb70d194b25463fffce35475141f93789de061de6a6b50` |
| Censo residual v3 | `8a33be0a189a42fe8a6c4b14ae5e36aa8df9da89aa312c045c6fd99de3c3f355` |
| Inventario de 442 artefactos | `69704030a52076437e131fde0a1b886605b3ed8efc6a8fcf272660df3e4503cd` |
| `docs/auditorias/integracion_artefactos_fuentes_2026-09-26.json` | `6e2a9120d50b6fa22ab873afc2824ce6cbc3e6fed4461e525cc0b99eff81e048` |
| Evidencia nominal nueva, `evidencia_reinspeccion_bn_v3_2026-09-26_inventario442.csv` | `e9c1e5370a9f1a3e6450929d1ef212a01ff9deca29c80ebcbb290266af6f1036` |
| Programa independiente `/tmp/materializar_reinspeccion_bn_v3_20260926_inventario442.py` | `2ce262be2fcdde90fe75073e96d2443f78f9a73ceff290c1e6d35757131c37d1` |

La consulta conserva la búsqueda literal sobre bytes decodificados y
normalizados del universo histórico. Incluir un archivo comprimido no
significa haber interpretado su contenido científico. Cero coincidencias no
demuestra inexistencia del dato ni ausencia biológica. Una modificación futura
del inventario o de las filas invalidará estas ligaduras para la nueva versión.
No se ejecutó ni se aprobó aquí el cierre global de `make verify`.
