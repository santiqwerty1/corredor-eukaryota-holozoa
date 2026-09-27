# Revisión independiente de la remediación residual — 2026-09-26

## Alcance y dictamen

Revisor: agente `/root/revision_residuales`, distinto del autor del cambio
(`/root/contrato_censo`). Revisión finalizada el 2026-09-26T21:10:47Z, sobre la
rama `codex/cierre-plan-pendiente`, comparando con el commit `0f15536`.

**CONFORME, exclusivamente para el cambio de caché de coocurrencia literal,
la actualización explícita de recuentos y los controles añadidos en
`scripts/remediate_trace_residuals.py`.** No se detectó debilitamiento de la
consulta histórica ni reducción de su universo. Este dictamen no aprueba las
408 búsquedas como investigación científica suficiente, no revisa sus
afirmaciones individualmente, no cierra segundas revisiones del corpus y no
declara que `make verify` pase.

El revisor no modificó código, datos científicos, manifiestos de celdas ni
constructores. Los adversarios se ejecutaron sobre directorios temporales o
parches de lectura en memoria; ninguno escribió en el corpus vivo.

## Identificación de los objetos revisados

| Objeto | SHA-256 |
|---|---|
| `scripts/remediate_trace_residuals.py` | `d1e8d0a273fc5a24de14fe1b564211f1a9356d22d3b741a6de60f67245df19a4` |
| `tests/test_remediate_trace_residuals.py` | `e0c6efaf8ad08106cdeed989919fe21e671d69dbd943b8a377352d7aa209b4d8` |
| `data/auditoria/residuales_trazabilidad_no_conformes_v3.csv` | `8a33be0a189a42fe8a6c4b14ae5e36aa8df9da89aa312c045c6fd99de3c3f355` |
| Registro de BN de raíz/corredor, `15_3_15-3-raiz-eucariota-y-corredor-filogenetico.csv` | `d64e1ddadfb8b4f7b6c01d6b1068bb47d2bdce210cad32c03974f11597cc9105` |
| `scripts/validate.py`, usado para el adversario de referencias | `c5c3af9390158f374edbc78ec90f6379a18a6a88242b8068fc7492b0c2cbf131` |

El inventario real de fuentes tuvo **434 artefactos**, con huella
`a08bc1a1584b2a31a0da0d84efd1de350abf318b9a2cfa7e0a94e0f34cb0f043`, calculada
mediante la función histórica sin modificar. El programa independiente
temporal `/tmp/revision_residuales_20260926.py` tuvo SHA-256
`537e6ea568ef7e15a709cbbef3cbe2a7ee7f80bdd5fc0c66d9f7b0d121baae02`.
El archivo temporal no forma parte del contrato permanente; abajo se conservan
el método, los resultados y comandos de reproducción de los contrastes centrales.

## Comprobaciones realizadas

1. Lectura completa del diff y del constructor. Comparación de AST contra
   `0f15536`: `normalized`, `source_snapshot`, `nominal_query`,
   `nominal_components`, `bn_row` y `gap_value` son idénticas.
2. `python3 -m unittest tests.test_remediate_trace_residuals -v`:
   **10 pruebas, 10 aprobadas**, salida 0, 1,035 s en esta ejecución.
3. Adversario independiente de caché: **47.280 comparaciones** contra
   `sum(all(c in t for c in components) for t in texts)`, sobre 16 corpus.
   Se probaron listas vacías, textos vacíos, textos duplicados, componentes
   repetidos, órdenes de consulta mezclados, subcadenas solapadas, NUL,
   Unicode compuesto/descompuesto, `ß`, `İ` y caracteres fuera del BMP.
   Semilla fija `927621`; vocabulario de 14 componentes; productos de
   longitudes 0–3. **Cero diferencias**.
4. Adversario de inventario: PDF binario, `tar.gz` binario, XML, archivo
   oculto, archivo vacío y `.url` se incluyen, con bytes, normalización y
   huellas esperados. Un subdirectorio se omite como ya ocurría antes.
   No hay selección nueva por extensión ni exclusión de PDF o archivos tar.
5. Contraste completo de las **410 consultas reales**, no una muestra:
   cada consulta tuvo sus tres componentes; los recuentos anterior y nuevo
   coincidieron en todas. **408 consultas devolvieron 0**; las únicas
   positivas fueron **C-2472: 3** y **C-2489: 5**. El ensayo completo terminó
   con salida 0 en 291,294 s; incluye lectura del inventario y ejecución de
   ambos algoritmos, por lo que no es una medición comparativa de velocidad.
6. Registro vivo: **498 BN únicas**, **486** con `NO LOCALIZADO EN ESTA
   SESIÓN` y **12** con `LA LITERATURA DECLARA QUE NO SE SABE`. Las 408
   claves marcadas v3 coinciden exactamente con las derivadas de las 410
   filas nominales, exceptuando los dos positivos. **BN-557 aparece una
   sola vez y no pertenece a las 408 v3**.

### Justificación de equivalencia de la caché

Para cada componente, `checked` recoge los índices ya inspeccionados y
`matches` exactamente los inspeccionados que contienen la subcadena. Antes
de intersectar se inspecciona todo índice de `common` todavía no comprobado.
Por ello, después de cada componente, `common` es exactamente el conjunto de
artefactos que satisface la conjunción recorrida. Los aciertos y los fallos
parciales quedan correctamente reutilizados en consultas posteriores. Las
repeticiones y permutaciones no cambian el resultado; con cero componentes
se conserva la semántica de `all([])`. Los textos reales son cadenas
inmutables y el índice conserva una tupla del inventario de esa ejecución.

## Adversarios de integridad y límites observados

| Mutación en fixture | Resultado observado |
|---|---|
| Repetir un `claim_id` residual manteniendo 410 filas | Rechazo: `C residual duplicada` |
| Repetir una clave BN no-v3, sin variar recuentos | Rechazo: `El registro activo contiene claves BN duplicadas` |
| Eliminar BN-557 sin sustituirla | Rechazo por recuentos 497/485/12 |
| Sustituir uno de los dos positivos nominales por otra C | Rechazo: deben conservarse los dos pasajes positivos nominales |
| Añadir dos filas duplicadas marcadas explícitamente como generadas v3 | Se regeneran; salida canónica de 498 claves únicas |
| Renombrar BN-557 a BN-558 conservando cantidades | El constructor acepta; el validador general rechaza la referencia BN-557 indefinida |

La canonicalización de entradas generadas v3 repetidas ya existía en
`0f15536`: el constructor elimina filas con su marcador y las reconstruye
desde el censo nominal. No es un rechazo de toda entrada duplicada; es una
regeneración que impide conservar duplicados en la salida. Las filas no-v3,
incluida BN-557, se preservan y no se regeneran como v3.

El constructor no impone una identidad científica concreta a cada BN ajena
a v3. Para verificar que esta separación no ocultaba el caso ensayado, se
ejecutó `validate.main()` dos veces, alterando solamente en memoria el valor
de la columna `clave` de BN-557 a BN-558 en los registros leídos. No se
alteraron C-2815 ni las demás referencias. Resultado exacto:

```text
baseline exit=1
VALIDACIÓN FALLIDA: 1 problema(s)
- manifest.json desactualizado.

BN557_renamed_only_in_registry exit=1
VALIDACIÓN FALLIDA: 2 problema(s)
- Referencias BN indefinidas: ['BN-557']
- manifest.json desactualizado.
```

Por tanto, el cambio no recibió una aprobación ficticia por confiar en ese
otro validador: su rechazo específico fue comprobado. El manifiesto estaba
desactualizado durante la prueba y se conserva ese fallo en este registro.

La búsqueda histórica sobre bytes decodificados de PDF/tar comprimidos no
equivale a extraer e inspeccionar el contenido científico de esos documentos.
Conservarlos en el universo demuestra no exclusión, no lectura semántica de
todos ellos. Cero coincidencias sigue siendo un resultado literal acotado,
nunca evidencia de ausencia biológica. Tampoco se ejecutó aquí una
evaluación de rendimiento repetida o aislada ni el `make verify` global.

## Reproducción del contraste real principal

Desde la raíz del repositorio, sin escritura en los datos:

```bash
python3 -m unittest tests.test_remediate_trace_residuals -v
python3 - <<'PY'
from scripts import remediate_trace_residuals as m
texts, digest, count = m.source_snapshot()
_, rows = m.read_csv(m.RESIDUALS)
index = m.ExactCooccurrenceIndex(texts)
positives = []
for row in rows:
    components = m.nominal_components(m.nominal_query(row))
    assert len(components) == 3
    old = sum(all(component in text for component in components) for text in texts)
    assert index.count(components) == old, row['claim_id']
    if old:
        positives.append((row['claim_id'], old))
assert len(rows) == 410
assert {claim for claim, _ in positives} == m.POSITIVE_CLAIMS
print(count, digest, len(rows), positives)
PY
```

Esta conformidad queda vinculada a las huellas anteriores. Cambios posteriores
en el algoritmo o su contrato requieren nueva revisión; no deben reutilizar
este dictamen como cierre de otro alcance.

## Addendum: ejecución nominal durable de las 408 BN v3

Tras la comparación diferencial anterior, el mismo revisor ejecutó nuevamente
las 410 consultas reales con `ExactCooccurrenceIndex`, sobre el mismo código,
censo y universo de 434 artefactos identificados arriba. La ejecución empezó
el **2026-09-26T21:19:59Z** y terminó el **2026-09-26T21:21:43Z**. Se observaron
otra vez los dos positivos esperados y **408 resultados literales iguales a
cero**; BN-557 no pertenece a este lote.

Se conserva el registro nominal en
`docs/auditorias/evidencia_reinspeccion_bn_v3_2026-09-26.csv`, de 408 filas,
SHA-256 `980c5c51189f44f5bbb694006d9ecea6a6df919ce78e473a202fde9207f082b1`.
Cada fila registra BN, huella de su fila canónica completa, C residual, celda
de origen, consulta exacta, resultado, cantidad/huella de artefactos, huellas
de código y censo, método y **el instante UTC observado para esa consulta**.
Los instantes van de 2026-09-26T21:20:54Z a 2026-09-26T21:21:43Z.

Antes de escribir el registro se comprobó que cada BN describía literalmente
esa consulta, el inventario de fuentes y los 434 artefactos; también que los
CSV BN, el censo residual y el código no habían cambiado durante la ejecución.
La huella de fila usa JSON con claves ordenadas, `ensure_ascii=False`,
separadores `,`/`:` y LF final, igual que `row_fingerprint` del contrato temporal.

Esta evidencia permite ligar una fecha de **REINSPECCION** a esas versiones
concretas, no recuperar la fecha original desconocida. No adjudica las
revisiones científicas pendientes ni convierte cero coincidencias en ausencia
biológica. No se escribió el registro canónico `fechas_ejecuciones_bn.csv`
durante esta actuación: su integración es una operación posterior separada.
