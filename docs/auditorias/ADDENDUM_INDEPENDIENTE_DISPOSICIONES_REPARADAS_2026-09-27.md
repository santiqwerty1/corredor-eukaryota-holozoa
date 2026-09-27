# Disposiciones residuales: addendum de reinspección independiente

Revisor: `/root/verificacion_fuentes_nuevas`, sin participación en la
implementación ni sus reparaciones. Autor: `/root`. Rama:
`codex/cierre-plan-pendiente`.

Dictamen: **CONFORME EN EL ALCANCE TÉCNICO INSPECCIONADO** para los tres
hashes siguientes. Las seis NC del informe inicial tienen reparación
independientemente comprobada. El informe NO_CONFORME inicial, sus fixtures
y resultados permanecen intactos; no se reemplaza su resultado histórico.

## Versiones y prueba durable

| Objeto reinspeccionado | SHA-256 |
|---|---|
| `scripts/residual_semantic_dispositions.py` | `222a9dd383dc904a08ccb881fd8122abd9b337e24a062e0b5c84cc32b3a593d4` |
| `scripts/remediate_trace_residuals.py` | `85dfdc2db6e85ee2d4344321e4bfae7059a6f46a490a1d5b9f767e4a244d71c4` |
| `scripts/build_atomic_cell_claims.py` | `7a24993ff2411e0bcc1f534633b6e5c5d5a00b9bff3e2ad820700993b1632cd9` |
| Fixture nominal propia de reinspección | `1003fb945081f85820cf2fe0221d82436bfbff3e102706481627cdaf44d29543` |
| Fixture integral propia de reinspección | `981cb993dfb2ed8165f5ed77722edf43bbd877d21b1de464c219e71915227306` |
| `reinspeccion_disposiciones_reparadas_2026-09-27.json` | `2e4a50fa9a84717603104b44a97b4b4224d0528048be3c30ba05d45187e15705` |

Registro nominal de ejecución propia: **2026-09-27T02:03:53Z**; integración
completa propia: **2026-09-27T02:04:01Z**. Finalización de tests/huellas observada
a **2026-09-27T02:05:17Z**. Son tiempos UTC reales de esta ejecución.

El informe inicial preservado
`REVISION_DISPOSICIONES_SEMANTICAS_INICIAL_2026-09-27.md` conserva SHA
`74a252bb91914ea5a5f8b0edf0db3c2c87b94b87fdf1a6a9fe50f9a4cd3ed615`.

## Reparaciones comprobadas por el revisor

| Incidencia inicial | Comprobación independiente posterior |
|---|---|
| NC-DR-01: alias de autor/autorrevisión y placeholders | Se rechazan identidad exacta, mayúsculas, espacios, variantes Unicode NFKC, `NO_ASIGNADO` y `pendiente`. La declaración de independencia incorrecta tampoco basta. |
| NC-DR-02: interiores de rangos S/C omitidos | Se rechaza S01–S03 sin S02 y C-9000–C-9002 sin C-9001. S1 no se admite como clave canónica aunque figure igual en el archivo; `Fig. S02` no se interpreta como una segunda fuente. |
| NC-DR-03: catálogo C externo por symlink | La lectura del catálogo aplica el control de rutas y rechaza el CSV enlazado fuera de la raíz. |
| NC-DR-04: fuente cambiada después de validar disposición | El remediador revalida las disposiciones al final y rechaza el artefacto ya obsoleto, sin devolver los seis deltas. |
| NC-DR-05: corrección cambiada después de validar disposición | El constructor atómico revalida las disposiciones y sus entradas al terminar; rechaza la corrección posterior no enlazada al dictamen. |
| NC-DR-06: BN del roll-up heredada | Las C generadas por disposición usan exclusivamente las C del valor nuevo y no heredan BN de la metadata. C-2708 ya no recibe BN-111. |

La implementación fija además `identidad_fila` dentro de la propuesta firmada:
primera columna y, cuando integran el sujeto, taxón/sistema y magnitud. La
reinspección añade un adversario propio que cambia el sujeto en las mismas
coordenadas: se rechaza. El helper vuelve a comprobar esa identidad al final.

La comparación de identidades textuales sigue sin demostrar independencia
real de personas; la reparación impide los alias y placeholders reproducidos,
no sustituye la verificación humana del autor y del revisor.

## Adaptación explícita de las fixtures

No se modificaron las fixtures ni los JSON de rechazo iniciales. Se crearon
dos fixtures nuevas para el campo obligatorio `identidad_fila`; cada propuesta
artificial declara su identidad exacta y la incluye en el hash adjudicado.
La fixture nominal crea una tabla artificial completa. La integral extrae
la identidad de cada una de las seis filas en la copia temporal, sin recurrir
al helper de producción para calcular esa expectativa.

Se corrigió expresamente la expectativa errónea del revisor sobre S1/S01,
documentada en el informe inicial. No se oculta aquel FAIL ni se cuenta como
defecto reparado de producción. Las nuevas pruebas comprueban el contrato
canónico real y la exclusión correcta de figuras suplementarias.

## Integración completa y resultados

Se ejecutaron los builders completos sobre una copia temporal de `data/` y
`docs/`, sin editar el repositorio real ni copiar su biblioteca científica.
Seis disposiciones ficticias cambian C-2708, C-2712, C-2794, C-2797, C-2798 y
C-2801, apoyadas en C-9000–C-9005 y un artefacto explícitamente artificial.
La biblioteca temporal reproduce únicamente las dos consultas positivas
históricas y el documento de prueba; no es evidencia científica nueva.

Se comprobó conjuntamente:

- 410 residuales originales y las dos claves `POSITIVE_CLAIMS` intactas.
- 408 consultas negativas con idénticos términos y resultados que el baseline
  temporal del mismo inventario.
- Bytes BN y objetivos históricos idénticos a ese baseline: las disposiciones
  no reescriben la historia ni convierten las consultas en positivos.
- 816 C atómicas, seis síntesis con solo las nuevas dependencias explícitas,
  ninguna BN heredada del roll-up.
- Segunda ejecución de ambos builders con salidas idénticas: idempotencia
  del caso integral de seis deltas.
- Rechazo de las dos carreras de materialización, después de validar fixtures
  íntegras, no por ausencia accidental de un campo obligatorio.

Resultados ejecutados por el revisor:

| Grupo | Resultado |
|---|---|
| Adversarios nominales propios | 20/20 PASS |
| Integración y carreras propias | 3/3 PASS |
| Tests focalizados del proyecto | 40 tests, OK, 6.542 s |
| Suite completa del proyecto | 264 tests, OK, 24.118 s |

```bash
PYTHONDONTWRITEBYTECODE=1 python3 docs/auditorias/fixtures/reinspeccion_disposiciones_independiente_20260927.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/auditorias/fixtures/reinspeccion_integracion_disposiciones_20260927.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_residual_semantic_dispositions tests.test_remediate_trace_residuals tests.test_build_atomic_cell_claims -q
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -q
```

Se interpretaron todos los resultados JSON propios; un exitcode cero no se
tomó como equivalente a PASS. `git diff --check` de las fixtures e informe
inicial propios no mostró errores.

## Alcance no transferible

El registro real seguía vacío en la comprobación final: SHA
`3e8c22675e0d075ccf15897066b8e11dd1209b97c455a6bb13dcbabdd7616ed1`, cero
disposiciones. No se firmó ni materializó una corrección científica real.
El contrato exige después su revisión nominal del texto, componentes,
fuentes y pasajes; hashes y cobertura JSON no la sustituyen. Las C de soporte
siguen sujetas al censo semántico y sus revisiones globales.

No se promete atomicidad frente a cualquier escritura futura o no cooperante,
ni exhaustividad universal de estos adversarios. La materialización final
debe ejecutarse sobre un estado estable. Este dictamen no certifica hechos
de fuentes, censos, segundas revisiones reales, los 210 controles ni
`make verify` global. Solo cierra las incidencias técnicas reproducidas para
los tres hashes indicados; cualquier delta posterior requiere nueva revisión.
