# Comprobación final de artefactos nominales: hallazgo y reparación del autor

Autor y ejecutor: `/root`, rama `codex/cierre-plan-pendiente`.
Registro posterior a `ADDENDUM_AUTOR_FAILCLOSED_2026-09-26.md`.
**Pendiente de reinspección independiente**: este addendum no sustituye el
dictamen inicial NO CONFORME ni atribuye al revisor independiente el hallazgo
posterior descrito aquí.

## Variante reproducida

A las 2026-09-27T00:12:11Z ya se había observado una fixture que, después del
`validate()` real del censo, cambiaba `docs/prueba_nominal.txt`. El constructor
de huella `61bf0be9e4b0d9f9f643be8b614905e064353efdf9568588e245c050357a992a`
devolvía `CERRADO`. El archivo había sustentado dos ejes nominales; no pertenecía
al inventario semántico y el registro nominal conservaba la huella antigua.
Por tanto, rehashear exclusivamente el inventario del censo no detectaba
esa modificación. La prueba se hizo en un directorio temporal, no sobre un
censo real ni sobre sus firmas.

## Reparación

`assert_nominal_reviews_current()` vuelve a cargar las revisiones nominales,
lo que revalida los archivos que declaran y sus SHA. Compara tanto el conjunto
vigente como las anotaciones históricas/obsoletas; cualquier diferencia aborta
la construcción. Se invoca antes de devolver la evidencia C y la matriz S.
En C se conserva además la comprobación final del inventario y de los censos.
No se omite un eje, se sustituye una prueba ni se modifica una firma.

Las regresiones cubren cambios de la prueba nominal al terminar la validación
y durante el enlace C, además de su modificación durante la construcción S.
El control negativo desactiva solo en memoria esta nueva comprobación:
los dos métodos de prueba producen **tres fallos esperados y cero errores**.
Esto acredita que los tests ejercitan la protección añadida; no altera el
código de producción ni los datos reales.

## Versiones y resultados

| Objeto | SHA-256 |
|---|---|
| `scripts/build_audit_deliverables.py` | `01bdd7e1ce15019b0ba701c81ccb4b51cbf0e1ab0b100a347edfc0424d35f6f5` |
| `tests/test_build_audit_closure.py` | `a503e8a1d1e00a9ec5f120171e04224cbf5c7a9d61ec7671cba50071580a99c3` |
| `reejecucion_autor_failclosed_2026-09-27.json` | `53626b869d5e83be662058db3c27831fba4d351b66a395bbf123f55bf58f497a` |

Resultados observados antes de materializar este addendum:

- 36 pruebas focalizadas conformes.
- Suite completa: **222 pruebas, cero fallos**.
- Reejecución por el autor de los adversarios de autoría independiente
  preservados: **32/32 conformes**. No es una revisión independiente posterior.

Comandos positivos:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_build_audit_closure tests.test_build_audit_deliverables tests.test_audit_chronology -q
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -q
PYTHONDONTWRITEBYTECODE=1 python3 docs/auditorias/fixtures/revision_failclosed_independiente_20260926.py
```

El control negativo usa `unittest.mock.patch.object` sobre
`assert_nominal_reviews_current`, con `return_value=None`, y ejecuta
`ClaimClosureTests.test_change_during_validation_or_linking_never_closes` y
`SourceClosureTests.test_source_closure_rejects_nominal_document_changed_during_build`.
Los tres fallos corresponden exclusivamente al documento nominal modificado
en validación C, enlace C y construcción S.

## Derivado de densidad y alcance no acreditado

El primer `make verify` del corpus ampliado se detuvo en
`data/auditoria/densidad_referencia.csv`: seguía contando 524 fuentes.
Se ejecutó el generador existente con `--write`; ahora registra 525/34 = 15.44.
Los valores constantes de referencia (34) y umbral (80), el código y sus
comparaciones no cambiaron. SHA del CSV resultante:
`9bfa6754966fa85d7bf3579e06eb732ee696c3a931455c057ad13e496a6906f2`.

La reparación detecta las modificaciones observadas por estas comprobaciones;
no se presenta como garantía de atomicidad del sistema de archivos frente a
escrituras arbitrarias posteriores ni como una auditoría exhaustiva de
concurrencia. Sigue siendo necesaria la revisión ajena y la ejecución final
estable y aislada. No se han creado censos semánticos, firmas nominales ni
aprobaciones científicas o globales a partir de estos tests.
