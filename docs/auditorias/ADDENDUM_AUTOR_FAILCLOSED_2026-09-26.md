# Reparación del adaptador de cierre: comprobación del autor

Registro materializado a las 2026-09-26T23:45:00Z por `/root`, en
`codex/cierre-plan-pendiente`. Este documento **no es un dictamen independiente**.
La revisión inicial de `/root/verificacion_fuentes_nuevas` conserva su resultado
NO CONFORME y sus huellas; no se reescribe ni se considera aprobada por estas
pruebas. La revisión independiente del parche permanece PENDIENTE: los agentes
revisores interrumpieron su ejecución por límite de uso.

## Cambios implementados

- FC-01: el expediente C incorpora el instante máximo de todas las filas de
  ambos censos y los instantes de sus ejes nominales. El expediente S incorpora
  los instantes de sus cuatro ejes. La firma global debe ser igual o posterior
  a todos los límites temporales de su expediente, además de fijar su SHA.
- FC-02: se rechazan dos filas globales del mismo estrato, objeto y tipo de
  revisión, incluso idénticas. El orden del CSV no adjudica contradicciones.
- FC-03: se vuelve a comparar el inventario semántico después de validar y
  al terminar el enlace; también se comprueban nuevamente las huellas de la
  congelación y de ambos censos. Un cambio observado aborta la construcción.

Se incorporaron tres pruebas de regresión permanentes: cronología de firmas
globales C/S, duplicados en ambos órdenes y cambios de fuente/censo primario/
censo secundario tanto al salir de la validación como durante el enlace.
Todas usan fixtures temporales; no escriben revisiones científicas reales.

## Evidencia de ejecución por el autor

| Archivo | SHA-256 |
|---|---|
| `scripts/build_audit_deliverables.py` | `61bf0be9e4b0d9f9f643be8b614905e064353efdf9568588e245c050357a992a` |
| `tests/test_build_audit_closure.py` | `fb01901114b73a8a1e8ac54357dd028e4127d993fcc130f3e903eeec2985ea2c` |
| `tests/test_build_atomic_cell_claims.py` | `e0d0dd20edd6c2870bc482ea8333e4094e2d6ba0bd232f37e2e9049f9f36d55d` |
| `fixtures/revision_failclosed_independiente_20260926.py` | `b94fc19fd17b4533ecfdbaa04fc229dea9c0d4b76229b4589c6f87cad36c37b9` |
| `reejecucion_autor_failclosed_2026-09-26.json` | `d7cb53b44086a53e03b3265b5f93def80e02f951298c4fd542ffdab71e69f8fd` |

Comandos observados sobre esas versiones:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_build_audit_closure tests.test_build_audit_deliverables tests.test_audit_chronology -q
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -q
PYTHONDONTWRITEBYTECODE=1 python3 docs/auditorias/fixtures/revision_failclosed_independiente_20260926.py
git diff --check
```

Resultados finales: 35 pruebas focalizadas conformes; 220 pruebas de la suite
conformes; 32/32 adversarios de autoría independiente conformes al reejecutarlos
`/root`; comprobación de espacios sin errores. Una primera ejecución de las
nuevas fixtures falló por modificar un insumo después de congelarlo y por usar
la declaración de independencia de otro contrato; se corrigieron las fixtures,
sin cambiar esas exigencias del código, y se repitió íntegra la suite.

El script de adversarios se conserva byte por byte desde su original en `/tmp`.
Es una evidencia histórica, no una nueva suite escrita por raíz; conserva la
ruta absoluta del repositorio usada por su autor y no certifica ejecución en
una copia aislada. Su salida JSON se inspecciona por `passed == tests`: el script
histórico no convierte un adversario fallido en un código de salida distinto.

## Límites y siguiente revisión

Pasar los adversarios conocidos no acredita ausencia de otros fallos de
concurrencia, ni reemplaza la reinspección independiente del código. Tampoco
aprueba una fuente, afirmación, requisito, matriz o censo real. El censo de
afirmaciones y su segunda revisión siguen ausentes; no se generaron firmas.
`make verify` completo, su idempotencia y su ejecución aislada no quedan
certificados por este addendum. Deben verificarse tras cerrar el corpus y sus
revisiones nominales, conservando el dictamen inicial y añadiendo uno nuevo.
