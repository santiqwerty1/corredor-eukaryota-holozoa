# Reparación de autor: estados de segunda revisión y catálogo A vivo

Autor/coautor: `/root/inspeccion_relojes`. Rama:
`codex/cierre-plan-pendiente`. Observación final de resultados:
**2026-09-27T01:47:14Z**.

Este documento es un informe de implementación y ensayo del autor, **no una
revisión independiente**. Conserva el NO_CONFORME de
`REINSPECCION_FAILCLOSED_INDEPENDIENTE_2026-09-27.md` y su JSON. No cambia
ninguna firma científica, control manual, matriz canónica ni fuente.

## Defectos reproducidos y cambios

El revisor independiente había demostrado dos fallos sobre el builder
`01bdd7e1ce15019b0ba701c81ccb4b51cbf0e1ab0b100a347edfc0424d35f6f5`:

1. Filas `PENDIENTE/CERRADO` importaban el cierre y, con 483 entradas
   artificiales, el informe declaraba CERRADA.
2. La identidad bibliográfica S podía cambiar en A después de cargarla; el
   resultado conservaba CERRADO con la huella anterior si el expediente
   nominal no dependía de A.

Se añadieron primero pruebas de regresión al fichero de tests del autor.
Antes del parche, el módulo ejecutó 23 métodos de test con **14 fallos de
aserción** (incluidos subcasos adversarios). Después se modificó únicamente
`scripts/build_audit_deliverables.py`:

- Se rechazan antes de importar cualquier firma todos los pares distintos de
  `PENDIENTE/ABIERTO`, `NO_CONFORME/ABIERTO`, `CONFORME/CERRADO` y
  `FALLO_CORREGIDO/CERRADO`. Un par permitido no es una firma válida por sí
  solo: siguen exigidos identidad independiente, fecha, huella y expediente.
- El camino que conserva notas de una fila pendiente ya no copia
  `estado_cierre`; conserva el estado abierto generado.
- Informe, JSON y puerta `--require-complete-review` cuentan como cerradas
  sólo las filas que satisfacen `valid_closed_review`, no una etiqueta aislada
  CERRADO. Esto protege también la llamada directa al generador de informe.
- La matriz S fija la SHA del catálogo A antes de cargar sus filas, rechaza
  claves duplicadas y, después de enlazar los dictámenes nominales, relee A
  y compara tanto filas como SHA de bytes. La SHA se obtiene **después** de
  la relectura final para detectar la mutación inyectada justo al devolver
  las filas. Ausencia o cambio de A abortan con BuildError, sin devolver cierre.

No se alteraron validadores AF, el censo semántico, contratos de independencia,
cronología, fixtures del revisor ni `POSITIVE_CLAIMS`. No se ejecutó la
regeneración canónica de matrices.

## Ensayos observados

| Comando | Resultado |
|---|---|
| `python3 -m unittest tests.test_build_audit_closure tests.test_audit_chronology` | 35 tests, OK |
| `python3 -m unittest discover -s tests` | 242 tests, OK; 23.314 s |
| `python3 docs/auditorias/fixtures/reinspeccion_failclosed_independiente_20260927.py` | 32/32 originales y 22/22 adicionales; UTC emitida 2026-09-27T01:46:34Z |
| `git diff --check -- scripts/build_audit_deliverables.py tests/test_build_audit_closure.py` | exit 0 |

La tercera fila es **reejecución por el autor** de una fixture escrita por el
revisor. Su campo interno `scope` describe el propósito de la fixture, pero no
convierte esta ejecución en una firma independiente. No se sobrescribió su
JSON histórico de 20/22 adicionales. El revisor recibió las nuevas huellas
para ejecutar y dictaminar de nuevo por su cuenta.

Los tests nuevos cubren seis pares de estados incompatibles, preservación de
notas pendientes sin cierre, 483 etiquetas cerradas con resultado pendiente,
mutación del título, retirada, alta, duplicado y borrado de A durante la
construcción, duplicados inicialmente presentes y cambio posterior a su
segunda lectura. Se ejecutan sobre directorios temporales y firmas
artificiales. Las pruebas existentes de determinismo, raíz aislada,
preparación exclusiva de matriz S y obsolescencia siguen pasando.

## Huellas finales y preservadas

| Artefacto | SHA-256 |
|---|---|
| `scripts/build_audit_deliverables.py` final | `1bba155d719359d0d1009b8329bd061890725c88cf64a597418c2077c063596f` |
| `tests/test_build_audit_closure.py` final | `84a1c1bbe1fbf46b2d2b01b05d13b4cbcfbe14928a493596d1b182e30c5080f4` |
| `scripts/audit_chronology.py`, no editado | `7d977bae7c206eb61f20bae52035a133f31983fc05ae58c3f890f96b5ec7dba0` |
| Fixture independiente 20260927, no editada | `def926033bd47cb00d0546126537758388590212c0c1b0ea5f0b350c143a8467` |
| JSON independiente 2026-09-27, no editado | `e28e4cf3a56a21e3c3d2a2e491e39b4025049e434a508864354a32d85cc73e84` |

## Límites

Estas comprobaciones rechazan los cambios observados entre la captura y las
relecturas finales. No son un bloqueo transaccional del sistema de archivos
ni garantizan que otro proceso no escriba después de la última comprobación.
La ejecución aislada del cierre integral sigue siendo un requisito aparte.
No se ha ejecutado aquí `make verify` ni se afirma cerrada ninguna revisión
científica o el objetivo completo del usuario.
