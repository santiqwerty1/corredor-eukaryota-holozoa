# Revisión independiente de cronología declarada — 2026-09-26

Revisor: `/root/revision_residuales`; autor de la implementación temporal:
`/root/cronologia_cierre`. Rama inspeccionada: `codex/cierre-plan-pendiente`.
Base del diff: `0f15536`. Reinspección final: 2026-09-26T21:21:41Z.

## Dictamen y límites

**CONFORME para los contratos temporales identificados por las huellas de
este informe, después de corregir y reinspeccionar CRONO-01.** El fallo
original se conserva abajo; no se reemplaza por una historia de aprobación
ininterrumpida.

El alcance comprende `audit_chronology.py`, los cambios temporales de
`audit_full.py`, `build_audit_deliverables.py` y
`audit_requirement_controls.py`, la preservación de campos firmados en
`assemble_manual_review_ledger.py` y el contrato documental. No comprende
la ampliación de `manual_scope_paths` ni `tests/test_manual_editorial_scope.py`,
de autoría/revisión separadas. Que el archivo completo de controles figure
con huella no constituye aprobación de ese otro cambio.

No se adjudica aquí ninguna revisión científica ni control manual del corpus,
no se aprueban fechas concretas de otras personas y no se cierra el plan
global. Los fixtures que usan `CONFORME` son datos de prueba temporales, no
firmas del ledger real. No se modificó código productivo, datos científicos
ni registros cronológicos del corpus para ejecutar los adversarios.

## Hallazgo CRONO-01 y reinspección

**Estado inicial: NO_CONFORME.** El primer soporte de reinspecciones de BN
históricas aceptaba una nueva ejecución de BN-025 fechada `2026-08-07`, aunque
la Q congelada de la misma BN estaba fechada `2026-08-08`. La evidencia local,
su SHA y la huella BN eran válidas en el fixture. El constructor generaba la
Q posterior y `audit_searches` no emitía AF613. La fecha coincidía con el
registro, pero faltaba cotejarla con el antecedente histórico conocido.

Reproducción independiente original:

```text
test_historical_reinspection_cannot_precede_original_q ... FAIL
AssertionError: 'AF613' not found in {'AF617'}:
Una reinspección fechada 2026-08-07 se aceptó antes de su Q original de 2026-08-08
```

AF617 provenía de prioridades simplificadas del fixture y no detectaba el
defecto temporal. La evidencia relevante es la ausencia de AF613 y la
aceptación de la Q contradictoria por el constructor.

El autor añadió la cota de la Q original tanto al constructor como al auditor.
**Estado tras reinspección: CORREGIDO.** El mismo adversario ahora obtiene
`BuildError` antes de generar una salida. Además, en otro ensayo independiente
se construyó una Q válida, luego se alteraron conjuntamente su fecha y la del
registro a `2026-08-07`, y se cambió el texto del bloque para intentar eludir
la clasificación. El auditor produjo:

```text
AF613, Q-0176:
Reinspección incompatible con Q original:
fecha anterior a 2026-08-08 o sin precisión para demostrar el orden
```

La comparación se liga a identidad/posición y huella, no a un prefijo textual
del bloque. El arreglo no reescribe las Q históricas.

## Pruebas ejecutadas por este revisor

1. Suite relacionada: **81 pruebas, 81 aprobadas**, salida 0, 12,532 s:

   ```bash
   python3 -m unittest tests.test_audit_chronology tests.test_build_audit_deliverables tests.test_audit_full tests.test_audit_requirement_controls tests.test_assemble_manual_review_ledger
   ```

2. Adversarios independientes en `/tmp/revision_cronologia_20260926.py`:
   **13 pruebas, 13 aprobadas** después de la corrección, salida 0, 1,749 s.
   Huella del programa:
   `6a616fa17c428c3546d4ef1b81db924bcf60f2ee31de269995999c9aa9818789`.
   Comprenden:

   - fechas imposibles, formatos compactos, offsets, horas/segundos fuera
     de rango y tipos no textuales;
   - firma anterior a versión, diferencia de precisión día/instante y
     antecedentes temporales inválidos;
   - ambos CSV ausentes: no se inventan fechas y una BN nueva conserva
     `FECHA_NO_DOCUMENTADA`;
   - otro objeto, estrato o hash no presta su fecha a la versión consultada;
   - dos fechas para una misma identidad/huella: registro rechazado entero;
   - una fila temporal inválida impide prestar las fechas de otras filas;
   - hash de evidencia desactualizado, hash de objeto inválido, localizador
     genérico, cabecera incompleta, campos faltantes y campos sobrantes;
   - evidencia absoluta, externa, symlink hacia fuera del repositorio y
     los cuatro destinos derivados expresamente prohibidos por circularidad;
   - una firma anterior a la versión registrada, a la verificación de fuente
     o al dictamen manual vuelve a `PENDIENTE` en el constructor y provoca
     AF751 en el auditor; una firma de otro hash tampoco se transfiere;
   - formato histórico de seis columnas: solo admite `NO_CONFORME`, sin
     añadir los campos de una firma completa;
   - ensamblado exacto de los doce campos: cambios o vacíos en literal,
     alcance, ambas huellas, independencia y fecha se rechazan. Se parcheó
     `manual_template_row` para lanzar una excepción si el ensamblador
     intentaba recalcular una plantilla: no lo hizo;
   - CRONO-01: la reinspección histórica no puede preceder a su Q original.

3. Comparación adicional, independiente de los tests del autor: se extrajo
   por AST la función `build_search_matrix` de `0f15536` y se ejecutó con
   los mismos datos congelados que la función nueva. **Las 165 primeras
   filas completas fueron idénticas**, no solo sus fechas. La nueva
   reinspección se agrega como Q separada. También pasó el contraste contra
   el agregado congelado de huellas en la suite relacionada.
4. Ensayo adicional del auditor sobre una Q retrofechada y con bloque
   renombrado: AF613 específico confirmado, como se documentó arriba.
5. Inspección del código: en estos módulos no se usa `now()`, `today()`,
   mtime ni fecha de commit para rellenar fechas. `2026-08-13` se conserva
   como límite inferior declarado de revisiones, no como fecha impuesta
   a todas las firmas. Las nuevas S/BN sin evidencia fechada no heredan
   automáticamente el corte bibliográfico. La suite verifica la conservación
   literal de las fechas de fuentes congeladas y la ausencia de fecha
   inventada para las fuentes nuevas.

## Límites que permanecen explícitos

Los registros son declaraciones locales ligadas a evidencia por SHA. El
validador prueba formato, identidad, integridad y orden respecto de
antecedentes declarados; **no prueba por sí solo autenticidad, independencia,
ejecución material ni contenido científico**. La revisión humana/independiente
de esos extremos sigue siendo necesaria.

La ausencia del registro opcional de fechas de objetos no proporciona una
fecha de creación. En ese caso, el control temporal de firmas solo conoce
el inicio de cierre y los demás antecedentes presentes; no certifica un
orden desconocido. En cambio, las nuevas búsquedas y verificaciones de fuente
sin su evidencia temporal específica se publican como fecha no documentada
y quedan bloqueadas por los auditores correspondientes.

Sin un reloj externo, un calendario coherente puede aceptar una fecha futura
declarada; el adversario `9999-12-31` lo confirma. Esto se documenta como
límite del contrato, no como comprobación de que una inspección ocurrió.
La evidencia circular bloqueada mecánicamente corresponde a los dos registros
de fechas, la matriz Q y la matriz de fuentes; el control no puede detectar
por sí solo que un documento distinto o una copia derive semánticamente de
ellos. Ese examen de procedencia corresponde a la inspección independiente.

No se ejecutó ni se aprobó aquí el `make verify` global. Las firmas antiguas
de seis columnas no se rehabilitan ni se completan con fechas/huellas nuevas
por este dictamen: necesitan una nueva revisión completa si se pretende
cerrarlas.

## Huellas de la versión reinspeccionada

| Archivo | SHA-256 |
|---|---|
| `scripts/audit_chronology.py` | `7d977bae7c206eb61f20bae52035a133f31983fc05ae58c3f890f96b5ec7dba0` |
| `scripts/audit_full.py` | `a8f1fd10327decc65b6640f510484b9e4cf551f9e6258eb84ad2919f8021275f` |
| `scripts/build_audit_deliverables.py` | `50884b7a6bce0c2bd232848b3c2eca5a7446a55e88da90bc203bbf604df88bd0` |
| `scripts/audit_requirement_controls.py` | `d7b0bff89c439633d73706d3039e7bd0372708e9c511c0a5413620e9510c131a` |
| `scripts/assemble_manual_review_ledger.py` | `d1e68c7834411de19c9d3eb3342b781a294112d8936c6107828631fc343bb4f2` |
| `docs/auditorias/CONTRATO_CRONOLOGIA_CIERRE.md` | `e3307c9807f0ed8718b034af8092e2bf030c426f5ebb7012d16e4984797f73a9` |
| `tests/test_audit_chronology.py` | `0348e24730bfc03778cd8262a4253049f07697be89824ad7fc50187505bac1b5` |
| `tests/test_build_audit_deliverables.py` | `608978e4b33b7fe3d0522a152c551624a309abc53a5008266d4bbc6993342339` |
| `tests/test_audit_full.py` | `c842cfabf67c909291c5a40560b2e9abd730adf3b8d99155e44f81cf17abbdc0` |
| `tests/test_audit_requirement_controls.py` | `38de59c78108dfe042a48b0b72645733bdfacdb23b68cd92f13226fe4faf0324` |
| `tests/test_assemble_manual_review_ledger.py` | `1d99972d8aafa2485072e948387fb01d543b8d5a4c435b0ea4f664ff805610ff` |

Las huellas de `audit_full.py`, `build_audit_deliverables.py` y su contrato
corresponden a la reparación de CRONO-01, no a la implementación inicial
defectuosa. Un cambio posterior exige reinspección del alcance afectado.
