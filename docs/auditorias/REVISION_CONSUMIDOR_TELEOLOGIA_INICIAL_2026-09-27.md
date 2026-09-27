# Revisión independiente del consumidor de contextos: NO_CONFORME

Fecha real de las pruebas: `2026-09-27T02:29:35Z`. Revisor: `/root/verificacion_fuentes_nuevas`. Rama: `codex/cierre-plan-pendiente`.

El revisor redactó el ledger lingüístico externo, pero no implementó este consumidor ni su integración. Este dictamen es técnico; no es una segunda lectura independiente de sus propias adjudicaciones lingüísticas, ni una firma científica o global.

## Versión inspeccionada y prueba preservada

- `scripts/check_teleology_contexts.py`: SHA256 `dcd4c81135e014909891a3ab066a05c718522ab5e42941c08a032451fd5faceb`.
- `scripts/audit_requirement_controls.py`: SHA256 `a92c9b4a04e23f5a8320d52e0c0b5c47fb99bc8aeb4a8f2a7cd0847c7d0e206a`.
- `tests/test_check_teleology_contexts.py`: SHA256 `5b90a1b1f9e210ffaf3601dd1e7fea6d3b9e2b2acc8d04ab14869ad874bde6db`.
- `tests/test_audit_requirement_controls.py`: SHA256 `f8a8a62f875b4ea30b343334ad412b6641402cf106dabc5122df4dedc9c732ff`.
- Ledger v2 consumido, sin modificarlo: SHA256 `30b0de4813c5c30c54d751f89ab86d359e1c884b3ff9078c0ca74bcb2c2bb029`.
- Fixture propia: `fixtures/revision_consumidor_teleologia_independiente_20260927.py`, SHA256 `cbfe431a1abbaed2fa1f6bffef1ff3f046678d191651a746e184f79e164bd759`.

Resultados nominales íntegros en `revision_consumidor_teleologia_inicial_2026-09-27.json`: **61 casos, 57 PASS y 4 FAIL**. La fixture crea expedientes y contextos ficticios únicamente en directorios temporales. No altera firmas reales, corpus, fuentes ni implementación. No importa las fábricas de expedientes de los tests del autor.

Para atravesar el primer fallo y explorar las demás ramas, los adversarios internos usan explícitamente `version: 1`, la única versión admitida por este código. Esto es una configuración diagnóstica ficticia, no un cambio al ledger v2 real ni una aprobación de esa versión. Dos pruebas separadas contrastan la exigencia contractual de v2.

## NC-CTX-01 — P2: contrato de versión incompatible

`validate_review` exige exactamente `version == 1`; el expediente acordado y preservado declara `version: 2`. El corpus vivo cuenta correctamente 74 candidatas y 95 ocurrencias, pero devuelve `versión de esquema desconocida`.

Las pruebas `schema_v2_current_must_accept` y `schema_v1_not_current_must_reject` fallan: se rechaza la versión vigente y se acepta una versión distinta. Es un bloqueo espurio, no un bypass del censo real. Debe corregirse el consumidor para el contrato vigente; no modificar la evidencia independiente para ajustarla al error del consumidor.

## NC-CTX-02 — P1: contexto cambiado durante la relectura final del expediente

`check_context_reviews` valida el JSON, relee las rutas de contexto y finalmente relee el ledger. La prueba `race_context_during_final_ledger_read` modifica un archivo contextual durante esa segunda lectura del ledger, cuando el bucle de contexto ya terminó. El consumidor retorna sin errores aunque el contexto vivo ya no corresponde al snapshot validado.

La mutación ocurre dentro de la operación de comprobación, antes de su retorno, no después de finalizar una revisión estable. Se requiere una ligadura de vigencia que alcance también el punto de consumo del resultado. Ningún número finito de relecturas sustituye una transacción universal del sistema de archivos; el contrato debe ser explícito sobre sus límites y no atribuir un hash vivo posterior a una revisión de bytes previos.

## NC-CTX-03 — P1: artefacto con CERO_FALLOS y huella nueva no revisada

La prueba `integration_changed_context_before_artifact` ejecuta realmente `check_teleology_candidates`, modifica después una ruta contextual y llama `artifact_row`. El resultado sigue siendo `CERO_FALLOS`; `scope_text` calcula entonces una huella sobre los nuevos bytes, sin revalidar su correspondencia con el ledger. Se materializa así un resultado anterior ligado al contexto posterior no adjudicado.

La fixture usa el mismo algoritmo de huella de alcance de `Corpus.scoped_digest` y llama la integración y `artifact_row` de producción. No basta corregir solamente la relectura local: la materialización debe conservar o comprobar el snapshot que efectivamente sustentó el resultado y fallar si las dependencias cambiaron.

## Reproducción de los fallos teleológicos anteriores

Se probaron de nuevo los dos textos originales por la integración real, con expedientes ficticios que sí alcanzan las ramas posteriores a la versión:

- NC-TEL-01: «La identidad es superior a 70 %; este linaje es primitivo.» Se rechaza tanto con censo nominal vacío como con dictamen exclusivamente para la primera ocurrencia cuantitativa.
- NC-TEL-02: «Hay un criterio; este linaje es más evolucionado.» Se rechaza por ausencia de candidato adjudicado, aunque la ruta de la fixture coincide con la antigua exención de nomenclatura.

En esta implementación quedan corregidas las dos exenciones de línea reproducidas en NC-TEL-01/02: no reaparecen por «criterio», porcentaje o ruta. Se conserva el informe histórico NO_CONFORME y sus resultados originales; la corrección mecánica observada no implica aprobar el consumidor completo, que permanece NO_CONFORME por las NC-CTX anteriores.

## Cobertura conforme observada y límites

Los adversarios restantes verifican rechazo de candidato faltante/extra/duplicado, ocurrencia faltante, offsets y literal alterados, hashes/texto obsoletos, campos adicionales, tipos incorrectos, conflicto de autoría, identidad discordante, declaración ausente, UTC inválido o desordenado, claves JSON duplicadas, rutas fuera del ámbito, enlaces simbólicos de archivo o directorio y cambio de contexto sin modificar las candidatas. Las mutaciones de ledger o contexto inmediatamente después de `validate_review` se rechazan; las dos ventanas finales descritas no.

No se aprueban R-0001–R-0007, los 210 controles pendientes, censos científicos C/S, segundas revisiones ni `make verify`. Tampoco se afirma que el léxico detecte toda forma imaginable de teleología. Una reparación requiere nueva evidencia y reinspección, manteniendo intactos estos hallazgos.
