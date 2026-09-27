# Reinspección técnica independiente: CONFORME en el alcance probado

Revisor: `/root/verificacion_fuentes_nuevas`. Rama: `codex/cierre-plan-pendiente`. Pruebas nominales ejecutadas a las `2026-09-27T02:33:45Z`; verificaciones unitarias y comprobación posterior de huellas completadas después, durante esta misma revisión.

El revisor es autor del ledger lingüístico externo, pero no del consumidor ni de estas reparaciones de producción. La independencia declarada aquí es respecto de la implementación técnica: no constituye una segunda revisión independiente del propio ledger, ni una aprobación científica o global.

## Huellas inspeccionadas

- `scripts/check_teleology_contexts.py`: `4aedf83d64ec851d90db80fbc998a7f2f2f17a04ef1c23213e344cbce0b13429`.
- `scripts/audit_requirement_controls.py`: `1b275f110e46c7b7423d218e2f8a513b9670fe415a13e8750c26c3132ce97262`.
- `tests/test_check_teleology_contexts.py`: `7b80c4fff451f363967364b99ce6e917bd20945b765c373b82fae6f157954f44`.
- `tests/test_audit_requirement_controls.py`: `10d332e9333dc122951dfe445e8f20bfd5e193d3434210a0ec39352b7d0987a2`.
- Ledger v2 preservado: `30b0de4813c5c30c54d751f89ab86d359e1c884b3ff9078c0ca74bcb2c2bb029`.
- Fixture independiente nueva `fixtures/reinspeccion_consumidor_teleologia_independiente_20260927.py`: `86042d9a5fbab2feb65c7d06d2cb4c2ef9afa5501f4912b3515d7c5d26084a1d`.
- Resultados `reinspeccion_consumidor_teleologia_reparado_2026-09-27.json`: `9e7cb673b40d4e7aa4901b4cfdc6789944e3a118cc79403057c08a21093fbbf5`.

Las dos huellas de código y las de los ledgers v1/v2 se comprobaron de nuevo al terminar las pruebas, sin cambios. La fixture y los resultados iniciales permanecen intactos; no se transforma el rechazo histórico en una aprobación retroactiva.

## Resultados ejecutados por este revisor

- 75/75 adversarios propios PASS: los 61 casos anteriores adaptados explícitamente al contrato ficticio v2 y 14 casos adicionales de vigencia/materialización. No se alteró el ledger real.
- `python3 -m unittest tests.test_check_teleology_contexts tests.test_audit_requirement_controls`: 45 pruebas, 9.668 s, OK.
- `python3 -m unittest discover -s tests`: 288 pruebas, 24.091 s, OK.
- Invocación diagnóstica del consumidor sobre el corpus vivo: 74 líneas candidatas, 95 ocurrencias, 124 huellas ligadas (123 rutas más ledger), sin errores. Es un cotejo técnico, no una firma de R-0001–R-0007.

## Resolución nominal de las NC

**NC-CTX-01, corregida.** Se admite exactamente la versión 2 y se rechaza la 1. Los dos casos que fallaban antes ahora pasan. El ledger independiente no fue reescrito para satisfacer al consumidor.

**NC-CTX-02, corregida para la carrera reproducida.** La mutación de contexto durante la segunda lectura final del ledger se rechaza mediante la guarda de identidad/estado de archivo. Además se rechazan mutaciones transitorias de contexto o ledger aunque restauren los bytes antes de la relectura, y un reemplazo por symlink con contenido idéntico durante esa lectura final.

**NC-CTX-03, corregida.** Los hashes de los bytes realmente cotejados se transfieren al resultado únicamente al tener éxito. Antes de materializar se comparan esos hashes con las entradas vivas; el cambio de contexto después del chequeo produce `NO_CONFORME`, no `CERO_FALLOS` con una huella ajena a la revisión. También fallan ledger modificado, contexto eliminado, pérdida de ruta revisada del alcance, symlink sobrevenido y modificación de una ruta ya leída al calcular el hash de otra posterior. Los errores aparecen antes de decidir el resultado del artefacto y se actualiza la métrica de fallos.

**NC-TEL-01/02, corrección mecánica reconfirmada.** Se ejecutaron otra vez los dos textos originales. «La identidad es superior a 70 %; este linaje es primitivo.» se rechaza tanto sin dictamen como con dictamen solamente de la ocurrencia cuantitativa. «Hay un criterio; este linaje es más evolucionado.» se rechaza sin adjudicación nominal. La antigua ruta exenta de nomenclatura no evita esos rechazos.

## Cobertura adicional y determinismo observado

La salida opcional de hashes elimina entradas residuales preexistentes, se completa solamente con el snapshot comprobado y queda vacía tras un fallo. Una segunda comprobación fallida también descarta los hashes aprobados de la primera. Se conserva el rechazo de esquema abierto, claves JSON duplicadas, tipos incorrectos, errores de calendario/orden UTC, conflictos de autoría, dictámenes negativos, rutas y candidatos ajenos, omisiones de ocurrencias, cambios de texto/contexto y UTF-8 inválido.

El artefacto ficticio sin cambios es idéntico entre materializaciones consecutivas. Una reescritura estable de los mismos bytes entre el chequeo y la materialización conserva el resultado y los derivados; inode/mtime/ctime se usan como guardas de carrera, no se serializan. Esto comprueba determinismo e idempotencia locales del consumidor, no los de `make verify` global.

## Límite no transaccional y alcance de conformidad

El sistema de archivos no se bloquea transaccionalmente. Estas pruebas acreditan las ventanas nominales reproducidas y las guardas descritas, no inmunidad frente a una modificación arbitraria posterior al último chequeo. Una ejecución final debe realizarse sobre entradas aisladas/estables y validar los derivados al terminar. No se promete detectar cambios posteriores al punto comprobado ni impedir que otro proceso escriba después.

El consumidor no determina semántica mediante regex ni genera dictámenes de aprobación: exige evidencia nominal externa para el censo exacto. La veracidad del juicio, la autenticidad sustantiva de la independencia declarada y la exhaustividad de un léxico no quedan demostradas por pasar estas validaciones estructurales.

Se mantiene íntegro `REVISION_CONSUMIDOR_TELEOLOGIA_INICIAL_2026-09-27.md` (SHA256 `fc41f5f6aea3f8ed962365847ea92b65f9a1f03c2a8d6b7230401819b775fa91`) y su JSON de 57/61 (`0eb184977c09758573534798fb57986e392aad7090986236eed991348a345db8`). Este addendum resuelve las tres NC técnicas para las huellas nuevas indicadas; no firma ciencia, censos C/S, revisiones globales, controles R ni `make verify`.
