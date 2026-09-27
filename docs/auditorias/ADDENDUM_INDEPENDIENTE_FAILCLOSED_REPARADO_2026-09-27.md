# Addendum independiente: reparaciones fail-closed reinspeccionadas

Revisor: `/root/verificacion_fuentes_nuevas`, sin participación en la
implementación ni sus reparaciones. Autores: `/root/inspeccion_relojes` y
`/root`. Rama: `codex/cierre-plan-pendiente`.

Dictamen: **CONFORME EN EL ALCANCE TÉCNICO INSPECCIONADO**, para las versiones
exactas abajo. Las incidencias iniciales y **NC-FC-20260927-01/02** tienen
reparación independientemente comprobada. Se conservan ambos informes
NO_CONFORME y sus reproducciones: no se reescribe el resultado histórico.
Este addendum no acredita el cierre global de la investigación.

Reejecución independiente tras recibir la versión estable:
2026-09-27T01:47:16Z. Ampliación final propia: **2026-09-27T01:49:03Z**.
Finalización de tests y huellas observada a 2026-09-27T01:49:30Z. Son horas UTC
del reloj real de la ejecución, no fechas rellenadas desde el corte histórico.

## Versiones y evidencia

| Objeto | SHA-256 |
|---|---|
| `scripts/build_audit_deliverables.py` | `1bba155d719359d0d1009b8329bd061890725c88cf64a597418c2077c063596f` |
| `scripts/audit_chronology.py` | `7d977bae7c206eb61f20bae52035a133f31983fc05ae58c3f890f96b5ec7dba0` |
| `tests/test_build_audit_closure.py` | `84a1c1bbe1fbf46b2d2b01b05d13b4cbcfbe14928a493596d1b182e30c5080f4` |
| Fixture propia original `fixtures/revision_failclosed_independiente_20260926.py` | `b94fc19fd17b4533ecfdbaa04fc229dea9c0d4b76229b4589c6f87cad36c37b9` |
| Primera ampliación propia `fixtures/reinspeccion_failclosed_independiente_20260927.py` | `def926033bd47cb00d0546126537758388590212c0c1b0ea5f0b350c143a8467` |
| Ampliación final propia `fixtures/reinspeccion_delta_final_failclosed_20260927.py` | `e873fe8dbac0eccc3c0c1e2eac1e0836284e47bd31c616182e7cccc218354ea7` |
| Resultado nominal completo `reinspeccion_failclosed_reparaciones_finales_2026-09-27.json` | `872e44423d56434b64d3d3d26faa105bcd1b9eb435c96493e56d7ef7268ef7aa` |

Huellas comprobadas de antecedentes preservados:

- `REVISION_FAILCLOSED_INICIAL_2026-09-26.md`:
  `c5b6935939787cdd4e7cb5d31f9e278b25e3bf18ae90be770732863827dbba27`.
- `REINSPECCION_FAILCLOSED_INDEPENDIENTE_2026-09-27.md`:
  `144b17006978dfc2d069b8c33277d006c99daec2c2126a8d16500b9082b7fa4a`.
- Su JSON con los dos fallos sobre `01bdd7…`:
  `e28e4cf3a56a21e3c3d2a2e491e39b4025049e434a508864354a32d85cc73e84`.

## Reparación NC-FC-20260927-01

La importación de segundas revisiones rechaza los pares resultado/estado
incompatibles. Una fila pendiente válida conserva texto pero no importa
`estado_cierre`. Además, Markdown, JSON y el contador de `main` usan
`valid_closed_review` en vez de tratar cualquier cadena CERRADO como una firma.
No se cambió un resultado previo para hacerlo aprobar.

Comprobaciones independientes:

- El adversario anterior de las 483 filas PENDIENTE/CERRADO ahora se rechaza.
- Se rechazan separadamente PENDIENTE/CERRADO, NO_CONFORME/CERRADO,
  CONFORME/ABIERTO y FALLO_CORREGIDO/ABIERTO.
- Se llama directamente a los generadores Markdown y JSON con una fila
  artificial que dice CERRADO pero está PENDIENTE, NO_CONFORME o CONFORME sin
  identidad/fecha/evidencia válidas. Ambos derivados siguen indicando abierto.
  Esta prueba no depende de que el importador ya haya rechazado esas filas.

## Reparación NC-FC-20260927-02

S fija la SHA del CSV A antes de leer sus filas. Al terminar, vuelve a leer las
filas y calcula la SHA de los bytes después de esa relectura; ambas deben
coincidir con lo fijado. El catálogo con claves duplicadas se rechaza antes de
adjudicar una versión. El control no introduce ninguna dependencia del censo C
en la preparación S.

Comprobaciones independientes:

- El cambio de título después de la primera lectura ya no devuelve cierre.
- Se cambia el título inmediatamente después de obtener las filas de la
  segunda lectura; el hash posterior lo detecta.
- Se cambia solo LF a CRLF después de la segunda lectura, comprobando que las
  celdas leídas son idénticas; se detecta la diferencia de bytes.
- Se borra A tras la segunda lectura y se prueban claves A duplicadas al
  empezar; ambos casos se rechazan.
- Control negativo solo en memoria: para el adversario posterior a la
  segunda lectura se fija artificialmente la SHA de A a la anterior, sin
  desactivar la comparación de filas. Reaparece CERRADO. Esto demuestra que
  la nueva prueba ejercita el hash final y no solo la relectura de celdas.

## Resultado completo de la reinspección

| Grupo ejecutado por el revisor | Resultado |
|---|---|
| Adversarios originales, intactos | 32/32 PASS |
| Primera ampliación, intacta, antes 20/22 | 22/22 PASS |
| Ampliación final independiente | 12/12 PASS |
| Tests focalizados builder/cierre/cronología | 42/42, OK, 2.095 s |
| Suite completa | 242/242, OK, 23.696 s |

Se inspeccionaron **66 resultados nominales** propios, no solo el exitcode.
Las pruebas positivas/negativas de fechas, duplicados globales, inventario
semántico vigente, artefactos nominales C/S, ciclos lógicos/resueltos,
obsolescencia histórica, dependencias y fijación del expediente global siguen
pasando tras el último delta. Se confirma la lectura íntegra del verificador
semántico por el adaptador y la separación entre cinco ejes semánticos, dos
ejes C adicionales y cuatro ejes S. Atribuciones, notas, fechas o falta de una
alerta no sustituyen los dictámenes nominales de la versión exacta.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 docs/auditorias/fixtures/reinspeccion_delta_final_failclosed_20260927.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_build_audit_closure tests.test_build_audit_deliverables tests.test_audit_chronology -q
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -q
```

El primer comando contiene por composición la ejecución de las dos fixtures
previas, conserva sus resultados individuales y añade los doce últimos. Todo
ocurre en directorios temporales; las firmas de prueba se declaran artificiales.

## Límites y no transferencia de aprobación

No se atribuye una garantía de atomicidad del sistema de archivos frente a
cualquier escritor posterior, ni exhaustividad universal de los adversarios.
La ejecución final debe realizarse sobre un estado estable y aislado. El JSON
probatorio incluye UTC y diagnósticos temporales; no se presenta su archivo
de ejecución como un derivado de bytes necesariamente idénticos entre corridas.

Este dictamen técnico no demuestra apoyo científico de ninguna fuente,
autenticidad externa de las fechas, identidad real de los revisores ni
independencia humana por el mero texto de una declaración. No se firman C/S,
censos, revisiones globales reales, controles manuales ni los 210 controles.
No se declara que `make verify` global haya pasado, ni que los derivados finales
estén regenerados o que el plan esté cerrado. No se modificó producción,
validadores, corpus, matriz ni firmas reales durante esta revisión.
