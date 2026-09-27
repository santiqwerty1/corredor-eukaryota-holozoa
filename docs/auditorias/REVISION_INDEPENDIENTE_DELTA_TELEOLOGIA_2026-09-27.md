# Delta cuantitativo del detector teleológico: revisión independiente

Revisor: `/root/verificacion_fuentes_nuevas`; autor del delta: `/root`.
Rama: `codex/cierre-plan-pendiente`.
Dictamen: **CONFORME EN EL ALCANCE DEL DELTA TÉCNICO**. No es conformidad de
los controles R-0001–R-0007 ni una aprobación global del detector o del corpus.

Ejecución propia: **2026-09-27T02:09:12Z**; tests terminados y huellas
comprobadas a **2026-09-27T02:09:40Z**, UTC real.

| Objeto | SHA-256 |
|---|---|
| `scripts/audit_requirement_controls.py` | `0200686fac33c6074c194ee7cfcc440a67e2e57fb96e207b573c6a330463f7ca` |
| `tests/test_audit_requirement_controls.py` | `66ff9f19eb975dc98cc9c397dd6736e50da34e977509f3ea11b8a14d708c1ffb` |
| Fixture propia `fixtures/revision_teleologia_cuantitativa_independiente_20260927.py` | `abd95c6d88c2143ba28ad61312b473302451609ee9613e77842fa5c8de398cc6` |
| Evidencia `revision_teleologia_cuantitativa_independiente_2026-09-27.json` | `0846a0993ac526114959215bcd51014bdcd3994e0adb482dd6db8c5799a963b6` |

## Método y resultado

Se leyó el delta de `check_teleology_candidates`. La rama nueva exige que
**cada ocurrencia** del patrón potencialmente teleológico en una línea quede
contenida en un span cuantitativo permitido: cuartil superior/inferior o
identidad [proteica] superior/inferior a/al una cifra porcentual. No se añade
una ruta, número de línea, clave C ni tabla exenta. No se retira una ocurrencia
de la población antes de clasificarla.

La fixture propia ejecuta el detector real y una ablación únicamente en
memoria que sustituye por falso el uso de `quantified_occurrences` en la
decisión. No modifica producción ni se presenta como una reconstrucción
histórica completa del script. Permite aislar la aportación de esta rama
manteniendo exactamente las otras reglas, rutas y recuentos.

**268/268 casos propios pasan**:

- Ocho líneas exclusivamente cuantitativas, incluidas mayúsculas, decimales
  con punto/coma, porcentajes con/sin espacio y varias ocurrencias permitidas.
- Quince construcciones teleológicas solas.
- Las 240 combinaciones de esas ocho líneas cuantitativas y quince
  construcciones teleológicas, en los dos órdenes: siguen siendo rechazadas.
- Cinco límites adicionales: linaje superior al 70 %, identidad sin porcentaje,
  comparativo no cubierto, cuartil con superior fuera del span y teleología en
  una línea distinta. No se amplía la excepción a estos casos.

En cada caso se comprueban también población y alcance antes/después. La misma
ruta se declara como prosa, C, tabla y apéndice: la deduplicación conserva una
inspección y la población no disminuye para producir el PASS.

En lectura diagnóstica del corpus vivo se mantienen **123 rutas y 74 líneas
candidatas**, iguales con y sin la rama nueva. La ablación da exactamente seis
alertas; el detector con la rama cuantitativa no las da:

| Localizador vivo en la ejecución | Uso cuantitativo |
|---|---|
| `data/afirmaciones/15.csv:929` | Cuartil superior en el motivo de C-2825 |
| `data/afirmaciones/15.csv:935` | Identidad proteica superior al 70 % en C-2831 |
| `data/apendices/F_magnitudes.csv:602` | Cuartil superior del umbral HIC |
| `data/apendices/F_magnitudes.csv:603` | Cuartil superior del umbral HIC |
| `data/apendices/F_magnitudes.csv:604` | Cuartil superior del umbral HIC |
| `docs/secciones/010-09-9-asociacion-el-catalogo-de-desenlaces.md:569` | Identidad proteica superior al 70 % |

Se ejecutaron además **22 tests del módulo, OK en 8.830 s**. No se ejecutó
`make verify` ni se firmó ningún control manual en esta revisión.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 docs/auditorias/fixtures/revision_teleologia_cuantitativa_independiente_20260927.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_audit_requirement_controls -q
```

## Límites preexistentes expresamente comprobados

El resto del detector conserva excepciones de línea completa. Dos casos
propios son aceptados **tanto sin como con la rama nueva**:

- «La identidad es superior a 70 %; este linaje es primitivo.»: actúa el
  `quantitative_comparison` preexistente.
- «Hay un criterio; este linaje es más evolucionado.»: actúa el
  `critical_context` preexistente.

Se preservan ambos resultados en el JSON y se comunicaron al autor. No se
atribuyen al delta nuevo ni se ocultan para declarar infalible al detector.
Demuestran que el detector sigue siendo una heurística de candidatos y no
una prueba exhaustiva de ausencia de teleología. Revisar esas reglas previas
sería una modificación adicional que este revisor no ha implementado ni
aprobado. El dictamen favorable es exclusivamente sobre la excepción
cuantitativa acotada y su no ampliación en los adversarios ejecutados.

Los números científicos y la interpretación de las seis proposiciones
requieren sus cotejos nominales propios; esta inspección de código no los
reemplaza. No se aprueban por ella R-0001–R-0007, los 210 controles, censos,
segundas revisiones reales ni el cierre global del plan.
