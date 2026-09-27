# Propuesta independiente de alcance integral para controles manuales

Autor de la propuesta: `Codex /root/revision_residuales/candidatos_editoriales`.
Inventario observado: 2026-09-26T22:07:00Z. Rama: `codex/cierre-plan-pendiente`.
Este documento no implementa el cambio, no firma requisitos y no aprueba
contenido científico. La única escritura de esta intervención es esta propuesta.

## Resultado y método

El defecto no se limita a los ocho candidatos editoriales señalados antes:
**77 de los 210 controles manuales ligan únicamente `data/table_index.json`**.
Otros 81 ligan entre dos y siete archivos. Solo los cinco controles de formato
ya ampliados ligan el conjunto completo de entradas y salidas editoriales.

Se leyeron el encargo, el handoff, el contrato de cronología y las funciones de
alcance, renderizado y ensamblado pertinentes. Se cargó `Corpus` y se ejecutó
`evaluate` en memoria sobre las filas `CONTROL_ESTRUCTURAL` de disposiciones;
se seleccionaron los resultados con `automated == False` y se agruparon las
rutas de `manual_scope_paths`. No se materializaron controles ni se cambiaron
estados. La ejecución nominal confirma 210 manuales, 62 conjuntos de rutas
distintos y 179 slugs; el slug genérico `LITERAL_PROMPT_COMPLETO` reúne 32 IDs.
Los resultados agregados de los auditores invocados por `evaluate` no se usan
como aprobación del literal.

## Inventario de cobertura actual

| Archivos ligados por control | Controles | Familia estructural observada |
| ---: | ---: | --- |
| 1 | 77 | Solo índice, sin contenido narrativo ni tabular ligado |
| 2 | 16 | Índice y un destino tabular o registro C |
| 3 | 39 | Índice y dos destinos específicos |
| 4 | 15 | Índice y tres destinos específicos |
| 5 | 3 | Índice y cuatro destinos específicos |
| 6 | 2 | Índice y cinco destinos específicos |
| 7 | 6 | Índice y seis destinos; incluye cinco controles de cobertura de apéndices |
| 11 | 1 | R-0329: índice, C de sección 15 y nueve CSV BN |
| 18 | 7 | Índice, 16 registros C y apéndice A |
| 24 | 10 | Índice, 16 registros C y siete apéndices; R-0008–R-0017 |
| 27 | 3 | Índice y 26 plantillas; R-0026, R-0028, R-0029 |
| 43 | 20 | Índice, 16 registros C y 26 plantillas |
| 98 | 6 | Índice y 97 CSV; R-0022–R-0025, R-0338, R-0401 |
| 127 | 4 | Base editorial integral; R-0398, R-0400, R-0404, R-0448 |
| 128 | 1 | Base integral y registro Q; R-0399 |
| **Total** | **210** | **182 sin ninguna plantilla ligada; 205 sin los informes ligados** |

La agrupación por sección del literal muestra que el defecto atraviesa
familias editoriales y científicas; no autoriza reclasificar las últimas:

| Familia de literales | Manuales |
| --- | ---: |
| §0, restricciones y registros | 17 |
| §1, alcance | 15 |
| §§2–6, origen, filogenia, fósiles y tiempo | 26 |
| §§7–13, ambiente, ecología, asociación, costes, sexo y magnitudes | 37 |
| §14, nombres y nomenclatura | 22 |
| §15, terreno probatorio y búsquedas | 6 |
| §16, afirmaciones, atribución y evidencia | 39 |
| §17, apéndices | 30 |
| §18, formato y entrega | 18 |

Los 77 IDs que actualmente ligan solo el índice son:

```text
R-0090 R-0091 R-0115 R-0126 R-0130 R-0225 R-0243 R-0263
R-0288 R-0289 R-0290 R-0291 R-0292 R-0295 R-0307 R-0308 R-0319
R-0336 R-0343 R-0344 R-0345 R-0349 R-0350 R-0351 R-0352 R-0360
R-0363 R-0368 R-0370 R-0371 R-0373 R-0374 R-0376 R-0380 R-0381
R-0382 R-0383 R-0384 R-0387 R-0388 R-0389 R-0390 R-0391 R-0394
R-0396 R-0397 R-0407 R-0408 R-0409 R-0415 R-0416 R-0417 R-0423
R-0424 R-0425 R-0426 R-0430 R-0432 R-0433 R-0434 R-0437 R-0440
R-0441 R-0443 R-0444 R-0449 R-0451 R-0459 R-0460 R-0461 R-0462
R-0463 R-0466 R-0469 R-0471 R-0474 R-0475
```

## Contrato recomendado

Adoptar para **todos los manuales**, sin promover su resultado, la unión de:

1. Todos los destinos específicos que `evaluate` ya aporta, conservando las
   exclusiones existentes del código del auditor y de `corpus_io.py`.
2. Todos los CSV declarados por `data/table_index.json`: hoy 97, distribuidos
   en 16 registros C, ocho apéndices, nueve BN y 64 tablas restantes.
3. Todas las plantillas de `docs/secciones/*.md` y las plantillas efectivamente
   referidas por `docs/order.txt`. Hoy ambos conjuntos coinciden: 26 archivos.
4. `data/table_index.json`, `docs/order.txt`, `docs/informe.md` y
   `docs/informe_completo_autocontenido.md`.
5. La excepción nominal ya existente de R-0399:
   `docs/auditorias/registro_busquedas_2026-08-08.csv`, porque el censo de claves
   de ese requisito incluye Q citadas en el documento.

La base tiene **127 rutas, no 126**: además de los 97 CSV, 26 plantillas,
orden y dos informes, incluye el propio índice. R-0399 mantiene 128.
No fijar esos números en el algoritmo: son el inventario de esta versión;
nuevas tablas, plantillas o cambios de orden deben alterar el alcance.
Resolver rutas dentro del repositorio, rechazar archivos ausentes y evitar
que una referencia de orden fuera del glob quede sin ligar. No omitir archivos
por inexistencia ni sustituir la unión por una lista que pierda destinos.

En los 210 alcances observados, **el único destino fuera de la base propuesta
es Q para R-0399**. No hay otro archivo de `docs/auditorias/` ni código auxiliar
que sea necesario rescatar del alcance manual actual. Si una familia adquiere
después un insumo específico adicional, deberá conservarlo mediante una
adición nominal y demostrar que no consume el dictamen que está ligando.

La huella del literal sigue separada. La base integral no reemplaza la lectura
del prompt en contexto ni la política prospectiva del handoff; el texto
atomizado de la matriz puede estar cortado por su segmentación. No incluir la
matriz completa para solucionar esto: incorpora estados/evidencias derivados
de controles y produciría una dependencia problemática. La eventual ligadura
del prompt/handoff como contexto normativo sería una ampliación explícita,
distinta de la base de entregables propuesta, no un motivo para retocar firmas.

## Circularidad y límites reales

- **No se observa un ciclo directo en los dos informes o H.**
  `corpus_io.render_report` consume índice, orden, plantillas y CSV;
  `control_csv_payload` calcula H desde ese corpus. Ninguno lee el ledger
  manual, los artefactos de controles ni la matriz de segunda revisión.
  H contiene recuentos del corpus, no resultados de firmas manuales. Que sea
  derivado no lo vuelve circular por sí solo.
- **Excluir `manifest.json` y el conjunto indiscriminado de auditorías.**
  El manifiesto registra archivos de `docs/`, incluidas las propias revisiones;
  ligarlo a una firma haría que añadirla cambiase su objeto firmado. Tampoco
  añadir el ledger, sus lotes/evidencias de firma, `controles_requisitos/`,
  `requisitos_disposiciones.csv`, las matrices de requisitos/segunda revisión
  o el informe reproducible que consumen resultados de revisión. La consulta
  del literal no equivale a ligar toda la matriz donde aparece.
- **Q es una excepción acotada, no una licencia general.**
  `build_search_matrix` usa BN, historia congelada y fechas de ejecuciones;
  no usa conformidades manuales. Su contenido debe estabilizarse antes de
  revisar R-0399. Los registros temporales siguen sujetos a su contrato propio;
  no hay que incluirlos globalmente por analogía ni usarlos como prueba circular.
- **El coste es invalidación global.** Un cambio de una C, BN, apéndice,
  plantilla, orden o salida invalida las 210 ligaduras, aunque la modificación
  sea irrelevante para algún literal. Es conservador y técnicamente coherente,
  pero exige congelar corpus y regenerar antes de adjudicar lotes. No recalcular
  huellas sobre dictámenes anteriores ni atribuirles fechas nuevas. Conservar
  versiones e historial, y encargar reinspección cuando cambie su objeto.
- **No prueba ciencia ni ejecución.** Los 127 archivos protegen la identidad
  del entregable, no autentican recuperación de fuentes, búsquedas o apoyo
  semántico. No es necesario incorporar los 442 archivos de `fuentes/` a todas
  las firmas ni leerlos masivamente para corregir esta infraestructura. Cada
  revisión científica deberá documentar por separado sus artefactos primarios,
  pasajes, huellas y límites; ligar mucho contenido no afirma haberlo leído.
- **La estabilidad sigue siendo comprobable.** Modificar solo una firma o
  una auditoría fuera del alcance no debe cambiar los 127 archivos después de
  renderizar. Si un cambio futuro añade resultados de revisión a H o a las
  plantillas, habrá que volver a analizar esa dependencia antes de mantener
  este contrato.

## Verificación propuesta para la implementación, no ejecutada aquí

Pruebas de mutación para un control antes limitado al índice, uno localizado,
uno de censo C y los cinco de formato: cambio individual de CSV, plantilla,
orden, índice y ambas salidas debe invalidar la huella. Añadir/quitar destinos
y conservar un destino específico fuera de la base deben tener cobertura.
Solo R-0399 debe conservar su adición Q mientras no se justifique otra.
Cambiar el ledger o un artefacto de auditoría no ligado no debe cambiar la
base ni los informes regenerados. Mantener los requisitos de literal,
evidencia nominal, independencia y fecha; no aceptar firmas obsoletas.

Antes de recoger dictámenes: implementar, revisar independientemente el
contrato, estabilizar entradas/Q, regenerar ambos informes y comprobar
idempotencia. Esta propuesta no cuenta como esa revisión de implementación.

## Huellas de la inspección estructural

| Archivo | SHA-256 observado |
| --- | --- |
| `scripts/audit_requirement_controls.py` | `d7b0bff89c439633d73706d3039e7bd0372708e9c511c0a5413620e9510c131a` |
| `scripts/corpus_io.py` | `4d7d35fb8649d41e4c137da16e1991a1a4117d8c46b68aa5d7fc3ae0c462fef7` |
| `scripts/build_audit_deliverables.py` | `50884b7a6bce0c2bd232848b3c2eca5a7446a55e88da90bc203bbf604df88bd0` |
| `docs/auditorias/CONTRATO_CRONOLOGIA_CIERRE.md` | `e3307c9807f0ed8718b034af8092e2bf030c426f5ebb7012d16e4984797f73a9` |
| `data/auditoria/requisitos_disposiciones.csv` | `03b13408627fcefc542e6834ca140909cd1d9ba0199509dd50028ae5c3f7ac26` |
| `docs/auditorias/matriz_requisitos_2026-08-08.csv` | `029ec3ddd98f327fb92bb7c1f4da0a466864ee93c0157fd4c5fa36781b4fc6a5` |
| `docs/order.txt` | `a530b3b2b2385cc2d9b876bce0a8bd8eec22205b7cc487166644806958ddcf6a` |
| `data/table_index.json` | `b1324a18b82d2289d6698a8a2fe86b487b39a70325321bd4c08079b090e76a1b` |

Los recuentos describen esta observación y no se transfieren a versiones
posteriores. No se leyó ni adjudicó el contenido científico de los 210 mandatos.
