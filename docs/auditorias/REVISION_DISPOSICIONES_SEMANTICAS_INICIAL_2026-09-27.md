# Revisión técnica independiente inicial de disposiciones residuales

Revisor: `/root/verificacion_fuentes_nuevas`, no autor de la implementación.
Autor de los tres módulos: `/root`. Rama: `codex/cierre-plan-pendiente`.
Dictamen de la versión inicial: **NO_CONFORME**. Registro real vacío; las
pruebas usan exclusivamente datos inventados en directorios temporales.

## Versiones y evidencia preservada

| Objeto inicial | SHA-256 |
|---|---|
| `scripts/residual_semantic_dispositions.py` | `06e18f3aaf43f6053a51599cf819dac520f36a429ff077acca9ee76a2ec99e5b` |
| `scripts/remediate_trace_residuals.py` | `c8f2484cffba87c47369187c0818ae8e01efd6999b86546cca988aa2583c437c` |
| `scripts/build_atomic_cell_claims.py` | `d075c18d6538f04b5849bb3a43cad01bf9a02d0b5598f5d0e184044eb86d2778` |
| Fixture nominal propia inicial | `30d09fe5fb7c01d4b512badaf8622acd6c90f8b8ccc425480ef5546aba8c3755` |
| Fixture integral propia, corregido su error de autorreferencia | `23f6561f1bdc25e0d2ed8ce3184a4f143c4d0bd7e25592671d021cd47f9288a9` |

Pruebas nominales: `revision_disposiciones_adversarios_inicial_2026-09-27.json`,
UTC real **2026-09-27T01:56:17Z**, SHA
`36dc55fcc94d34832694ae6f1cb162a6e962c8bbdf86471e64acdce862014486`.
Integración: `integracion_disposiciones_independiente_2026-09-27.json`, UTC
**2026-09-27T01:59:32Z**, SHA
`5abb1403a3f6e5886be317333a7537aa156cd7a490d28569c3c542382b1b6062`.
El desacople adicional de rango C está preservado en
`disposiciones_rango_c_adversario_inicial_2026-09-27.json` con SHA del módulo
inicial observado. No se atribuye retrospectivamente una hora exacta no
registrada a esta última prueba.

## Hallazgos que requieren reparación

1. **NC-DR-01, P1, independencia nominal eludible.** `load()` compara
   `review['revisor'] == record['autor']` sin normalización y solo exige texto.
   Frente a `Autor-Ensayo`, acepta ` autor-ensayo ` y `AUTOR-ENSAYO`; también
   acepta `NO_ASIGNADO` y `pendiente` como revisor. Una declaración exacta de
   independencia no vuelve distintas estas identidades. La corrección debe
   rechazar identidades no asignadas y normalizar antes de comparar. Ni
   siquiera esa normalización demostrará por sí sola independencia real.
2. **NC-DR-02, P1, rangos nominales incompletos.** El regex de S acepta
   `S01–S03` con artefactos únicamente S01/S03: falta S02. El regex de C admite
   `[C-9000–C-9002]` con soporte y revisión únicamente C-9000/C-9002, mientras
   el constructor atómico expande además C-9001. Las referencias del
   expediente y las que se materializan no representan el mismo conjunto.
   Deben aplicarse los parsers canónicos, respetando también el contexto de
   figuras/tablas suplementarias.
3. **NC-DR-03, P1, catálogo C fuera de raíz.** `_claim_catalog` sigue un
   symlink de `data/afirmaciones/15.csv` hacia un archivo fuera del corpus
   temporal, aunque las rutas de los artefactos sí lo rechazan. El cotejo de
   filas acepta el apoyo externo. La exclusión de rutas enlazadas/externas
   debe cubrir igualmente el catálogo canónico de C.
4. **NC-DR-04, P1, fuente caducada al aplicar el delta.** En la integración
   de seis disposiciones válidas, se modifica su artefacto justo después de
   `semantic_dispositions()` y antes de `source_snapshot()` dentro del
   remediador. `build()` devuelve las seis sustituciones pese a que su
   expediente ya no fija los bytes actuales. Revalidar dentro de `load()` no
   cubre todo el intervalo de materialización del llamador.
5. **NC-DR-05, P1, corrección no firmada materializada.** Tras la validación
   real de disposiciones, se modifica la corrección autoral y la celda viva a
   `CAMBIO POSTERIOR NO REVISADO [C-9000]`; el manifiesto se fija a la versión
   histórica que el builder permite. `build_atomic_cell_claims.build()` lee
   de nuevo la corrección y genera esa C distinta sin invalidar el dictamen
   anterior. El constructor debe fijar/revalidar el expediente y sus entradas
   durante todo su enlace, no solo marcar una clave C como dispuesta.
6. **NC-DR-06, P2, BN de otra parte de la fila heredada.** En la integración,
   C-2708 recibe `sintesis(C-9000)` correctamente, pero su Fuente añade
   `BN-111 términos exactos y resultado`, extraída de la metadata histórica
   del roll-up. La celda nueva no la cita. La historia BN debe conservarse
   fuera del apoyo positivo nuevo. El autor había advertido esta posibilidad;
   la prueba independiente la reproduce, sin atribuirse su descubrimiento.

## Integración realmente ejecutada

Se copia `data/` y `docs/` a un directorio temporal y se rebajan las rutas de
ambos builders a esa raíz. No se copian ni cambian las fuentes reales. Una
biblioteca explícitamente artificial conserva las dos consultas positivas y
un documento ficticio sustenta seis propuestas de prueba. Se usan las celdas
C-2708/C-2712/C-2794/C-2797/C-2798/C-2801, con C-9000–C-9005 temporales.

Los builders completos pasan, antes de la aserción de BN heredada, los
controles propios de 410 residuales, las dos claves positivas inalteradas,
408 consultas con términos/resultados idénticos, bytes BN idénticos al
baseline temporal del mismo inventario, objetivos históricos preservados,
816 C generadas, dependencias C nuevas exclusivas e idempotencia de ambas
salidas. La integración no se marca PASS porque sigue fallando la Fuente de
C-2708. Las dos carreras se ejecutan aparte con fixtures íntegras previas.

También se ejecutaron los tests del autor: **34 tests focalizados, OK**. No
neutralizan las NC independientes.

## Correcciones del propio revisor, no defectos de producción

El JSON nominal inicial tiene 9 PASS y 7 FAIL. Uno de esos FAIL corresponde a
una expectativa **incorrecta del revisor**: pretendía aceptar S1 como alias de
S01. El contrato vivo `corpus_io` exige dos o tres cifras y no declara ese
alias. Se retira como hallazgo contra producción; el rechazo observado es
correcto. Se conserva el JSON sin maquillarlo y la reinspección usa la
expectativa corregida: rechazar S no canónica también cuando el artefacto
lleve esa misma clave no canónica.

La primera fixture integral mencionaba su propia C en la descripción nueva;
el rechazo por circularidad fue correcto. Se conserva
`integracion_disposiciones_fixture_inicial_invalida_2026-09-27.json`. Ninguna
de sus tres entradas acredita una carrera ni un defecto de producción. Solo
se corrigió la fixture propia antes de obtener la corrida válida de 01:59:32Z.

## Límite

Estos son defectos de ligadura/materialización, no dictámenes científicos.
No se alteraron corpus, fuentes, pruebas previas, firmas reales, validadores
ni los tres scripts revisados. No se han aprobado disposiciones reales ni
fuentes por metadatos, ni el censo o el plan global. Cada reparación posterior
requiere hashes nuevos y reinspección independiente separada; este dictamen
inicial debe permanecer intacto.
