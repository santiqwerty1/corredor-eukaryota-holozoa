# Dos no conformidades del control teleológico completo

Revisor independiente: `/root/verificacion_fuentes_nuevas`.
Versión inspeccionada de `scripts/audit_requirement_controls.py`:
`0200686fac33c6074c194ee7cfcc440a67e2e57fb96e207b573c6a330463f7ca`.
Rama: `codex/cierre-plan-pendiente`. Observación real:
**2026-09-27T02:09:12Z**.

Dictamen del control completo en el alcance de estos adversarios:
**NO_CONFORME**. Ambas incidencias permanecen **ABIERTAS**.

Este expediente es separado de
`REVISION_INDEPENDIENTE_DELTA_TELEOLOGIA_2026-09-27.md`, que declara conforme
solo la rama nueva que corrige seis falsos positivos cuantitativos. La
preexistencia de estos defectos identifica su origen: no reduce su severidad
ni los convierte en meras advertencias prescindibles para el cierre.

## NC-TEL-01 — excepción cuantitativa oculta otra proposición (P1)

Entrada artificial exacta:

> La identidad es superior a 70 %; este linaje es primitivo.

Resultado real de `check_teleology_candidates`: una línea candidata, cero
errores; línea clasificada como aceptada. `quantitative_comparison` reconoce
«superior a» y exime toda la línea, incluida la segunda proposición que
califica el linaje de primitivo. No hay negación ni mención crítica que
sustente esa exención de la proposición teleológica.

Localizador: cálculo de `quantitative_comparison` y condición final OR de
`check_teleology_candidates`, líneas 910–922 en la versión indicada.

## NC-TEL-02 — una palabra de contexto oculta otra proposición (P1)

Entrada artificial exacta:

> Hay un criterio; este linaje es más evolucionado.

Resultado real: una línea candidata, cero errores; línea clasificada como
aceptada. La mera presencia de «criterio» activa `critical_context` para toda
la línea, sin comprobar que esté negando, criticando o contextualizando
adecuadamente la proposición «este linaje es más evolucionado».

Localizador: tokens de `critical_context` y condición final OR de
`check_teleology_candidates`, líneas 896–922 en la versión indicada.

## Evidencia y reproducción

Las dos entradas, la población, el alcance y sus resultados reales están
preservados en `legacy_limitations_not_introduced` del JSON
`revision_teleologia_cuantitativa_independiente_2026-09-27.json`, SHA
`0846a0993ac526114959215bcd51014bdcd3994e0adb482dd6db8c5799a963b6`.
El nombre histórico del campo se conserva, pero este informe adjudica ambos
casos explícitamente como defectos reales del control completo.

La fixture propia que los ejecutó tiene SHA
`abd95c6d88c2143ba28ad61312b473302451609ee9613e77842fa5c8de398cc6`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 docs/auditorias/fixtures/revision_teleologia_cuantitativa_independiente_20260927.py
```

Se ejecutan con el detector real y con la rama nueva desactivada solo en
memoria: ambos aceptan las dos entradas. Esto demuestra que no nacieron del
delta cuantitativo, sin exonerar el control global. Los 268 adversarios
favorables del delta y los 22 tests del proyecto no cubrían su rechazo y no
cierran estas dos no conformidades.

Se requiere una reparación del autor que no permita que un span/cláusula
admitido o un token incidental oculten una proposición teleológica distinta,
con reinspección independiente posterior. No se ha implementado dicha
reparación en esta revisión, ni se aprueba R-0001–R-0007. Cero alertas en el
corpus observado **no equivale a una prueba semántica de ausencia** y no
autoriza el cierre global mientras estas incidencias sigan abiertas.
