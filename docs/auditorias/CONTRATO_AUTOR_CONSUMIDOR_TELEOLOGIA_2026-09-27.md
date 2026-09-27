# Cotejo nominal del lenguaje: contrato del consumidor

Autor de la implementación: /root. Registro: 2026-09-27T02:36:16Z.
Rama: codex/cierre-plan-pendiente. Este informe no es una revisión independiente.

## Cambio y límites

El consumidor sustituye todas las exenciones por ruta, palabra contextual,
comparativo o porcentaje de `check_teleology_candidates`. El patrón de
candidatos y su universo canónico permanecen: 123 rutas, 74 líneas y 95
ocurrencias en el corte revisado. No se convierte una regla léxica en
aprobación científica ni se certifica la ausencia de expresiones no capturadas
por el patrón. La lectura nominal del revisor se mantiene en expedientes
separados, no generados por este programa.

`check_teleology_contexts.py` exige el esquema cerrado v2 del expediente
`censo_contextos_teleologia_v2_contexto_2026-09-27.json`: cada línea, posición
Unicode, literal, huella, dictamen, motivo, localizador, revisor, declaración
de independencia y conflicto de autoría. Exige cobertura exacta sin
duplicados, faltantes ni sobrantes. Los resultados negativos o no verificables
bloquean. También se ligan los bytes completos de las 123 rutas, incluidas
las que no contienen candidatos: un encabezado conservado no puede heredar
el contexto de un cuerpo modificado.

Las fechas exigen UTC y calendario válidos; snapshot posterior o igual a la
adjudicación y decisiones anteriores o iguales a su expediente. No se
consulta el reloj de ejecución. La autenticidad de lectura, independencia
y fechas procede de la evidencia del revisor, no de su validación sintáctica.

Se rechazan enlaces y escapes de rutas. Se releen los insumos y comprueban
firmas del sistema de archivos para detectar cambios durante el cotejo;
inode y tiempos del sistema **no se serializan**. El resultado conserva los
SHA de los bytes revisados. Al formar el artefacto del control, compara de
nuevo esos SHA con los bytes vivos y registra NO_CONFORME si cambiaron;
nunca vincula un dictamen antiguo a una huella nueva como si fuera revisada.

Estas guardas no constituyen un sistema transaccional del filesystem ni
prometen impedir escrituras posteriores al chequeo. El aislamiento de la
verificación final sigue siendo necesario y no queda aprobado aquí.

## Historia de fallos y correcciones

La reparación anterior de seis usos cuantitativos era limitada. La revisión
independiente descubrió NC-TEL-01/02: una comparación o palabra crítica
presente en otra parte de la línea podía ocultar una frase teleológica.
El nuevo consumidor exige dictamen exacto para cada ocurrencia y no conserva
ninguna de esas excepciones globales.

La primera versión del consumidor fue rechazada independientemente:

- Exigía versión 1 aunque el expediente contextual usa versión 2.
- Un cambio durante la última lectura del ledger podía afectar un contexto
  ya releído sin detectarse.
- La materialización podía asociar el resultado anterior a un hash recalculado
  de contenido nuevo.

Se preservan el informe inicial, sus 61 casos (57 satisfactorios y cuatro
fallidos) y sus versiones identificadas. Las reparaciones exigen v2 sin
fallback, comprueban las firmas finales y transportan las huellas aprobadas
hasta la materialización. Los tests sintéticos están identificados como
fixtures: no generan ni firman revisiones del corpus de producción.

## Reinspección recibida

`ADDENDUM_INDEPENDIENTE_CONSUMIDOR_TELEOLOGIA_REPARADO_2026-09-27.md`
(SHA256 f7db16ecce1777d2db66cba6ca972496ffa9630a8d52fd9fa82df3b003690717)
registra 75/75 adversarios propios, 45 tests focalizados y 288 de la suite.
La conformidad recibida es técnica y acotada: el revisor redactó el ledger
lingüístico, pero no implementó el consumidor. No equivale a firma de los
controles R, de las fuentes, de las C ni del cierre global.

Huellas de la versión reinspeccionada:

| Archivo | SHA256 |
| --- | --- |
| scripts/check_teleology_contexts.py | 4aedf83d64ec851d90db80fbc998a7f2f2f17a04ef1c23213e344cbce0b13429 |
| scripts/audit_requirement_controls.py | 1b275f110e46c7b7423d218e2f8a513b9670fe415a13e8750c26c3132ce97262 |
| tests/test_check_teleology_contexts.py | 7b80c4fff451f363967364b99ce6e917bd20945b765c373b82fae6f157954f44 |
| tests/test_audit_requirement_controls.py | 10d332e9333dc122951dfe445e8f20bfd5e193d3434210a0ec39352b7d0987a2 |

El contexto lingüístico quedará obsoleto ante futuras correcciones canónicas.
No actualizar automáticamente sus huellas ni reusar fechas para eludir la
reinspección del delta. Las propuestas científicas aún no integradas no
forman parte de la conformidad de este expediente.
