# Revisión independiente del adaptador de cierre — estado inicial

UTC real: 2026-09-26T22:58:32Z. Revisor: `/root/verificacion_fuentes_nuevas`;
autor del adaptador: `/root/inspeccion_relojes`. Rama propia compartida:
`codex/cierre-plan-pendiente`. No se editaron código, corpus, censos, fuentes
ni firmas reales. Dictamen de esta versión: **NO CONFORME**.

## Versión y método

Se leyó el código y su contrato nominal, y se ejecutaron los 32 tests del
autor (pasan) y 32 adversarios propios (28 pasan, cuatro fallan; tres causas).
Los adversarios construyen sus propias fixtures, sin importar fixtures ni
tests del autor. Ejecutan `validate()` real en dos censos artificiales y
usan únicamente directorios temporales; sus dictámenes no son científicos.

La evidencia nominal completa está en
`adversarios_failclosed_inicial_2026-09-26.json`.

| Objeto | SHA-256 |
|---|---|
| `scripts/build_audit_deliverables.py` | `fbd536af6ee4eb5b9b492056fce0e93f2a42b78118ac2bb24dcb45977d9f127e` |
| `tests/test_build_audit_closure.py` | `21ba5a8318a76f1bde1e3c19f4d301af651f93a96b60bffa8e8e38cf5aa98737` |
| `tests/test_build_audit_deliverables.py` | `0e25f194fde751b62bb685d7a9386127e7501393ff00938fb26322e5565ae568` |
| `tests/test_audit_chronology.py` | `d862c4d153858c1cb4d8435a5cdbc3a925899f093bae175729236d6dfb734565` |
| `scripts/check_semantic_claim_census.py` | `598dacc8ea3c0d1d3be06763ebc0734988a50c2fc9105095a66274e5c3dc3350` |
| `/tmp/revision_failclosed_independiente_20260926.py` | `b94fc19fd17b4533ecfdbaa04fc229dea9c0d4b76229b4589c6f87cad36c37b9` |

Comandos ejecutados, sin escrituras en los canónicos:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_build_audit_closure tests.test_build_audit_deliverables tests.test_audit_chronology -q
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/revision_failclosed_independiente_20260926.py
```

## Hallazgos abiertos de la versión inspeccionada

### FC-01 — P1 — Una firma global puede preceder al expediente

En la fixture, la congelación es de las 11:00 UTC, la primera revisión
semántica de las 12:00 y la segunda de las 13:00. Una segunda revisión global
fechada 11:30, con SHA canónica y token `expediente_sha256` correctos, se
conserva como CONFORME/CERRADO. La comparación de SHA no establece el orden
temporal. `bounds()` no incorpora los UTC de las revisiones semánticas ni
los de los ejes nominales que integran el expediente. No basta con validar
el orden entre ambas revisiones semánticas: falta este enlace posterior.

### FC-02 — P1 — Dictámenes globales duplicados se resuelven por orden

Dos filas del mismo estrato, objeto y tipo, una NO_CONFORME/ABIERTO y otra
CONFORME/CERRADO, no provocan rechazo. Si la aprobación va última, se
conserva CONFORME; al invertir el orden se conserva NO_CONFORME. El `dict`
de `old_rows` descarta silenciosamente una firma contradictoria. Debe
rechazarse la ambigüedad, no adjudicarla mediante posición en el CSV.

### FC-03 — P2 — Ventana de cambio concurrente de artefactos

La fixture ejecuta el `validate()` real y justo al terminar modifica
`fuentes/S01.xml`, antes del enlace del censo. El adaptador acepta el
expediente y devuelve CERRADO. Se comprueban otra vez las tres huellas de
congelación/primaria/secundaria y la fila C, pero no la vigencia de los
artefactos del inventario después de validar. La prueba no demuestra un
cambio real del corpus: demuestra una ventana reproducible si coinciden
escrituras y cierre. Una nueva comprobación coherente del inventario debe
rechazar ese cambio antes de prestar conformidad.

## Comprobaciones que sí pasan

Se rechazan 16 variantes de ciclos con manifest, disposiciones, controles
y matriz S: rutas directas, symlinks lógicos, symlinks resueltos y enlaces
de directorio padre. Un artefacto ausente anterior no oculta otro circular.
Las firmas nominales obsoletas se conservan intactas y no prestan resultado;
una reinspección nueva puede coexistir, y dos dictámenes nominales vigentes
se rechazan. Los censos duplicados, incompletos, negativos, con dependencia
incorrecta o artefactos/matriz S cambiados antes de validar dejan C abiertas.
Una fixture íntegra es estable en dos lecturas. La firma global con expediente
cambiado se invalida aunque no cambie la C.

Esto no cierra controles científicos, revisiones reales ni el plan. Las
correcciones posteriores requieren addendum con nuevas huellas; este
dictamen y sus fallos se conservan sin reescritura.
