# Reinspección independiente fail-closed — 2026-09-27

Revisor: `/root/verificacion_fuentes_nuevas`, ajeno a la implementación y a
sus reparaciones; autores de código: `/root/inspeccion_relojes` y `/root`.
Rama comprobada: `codex/cierre-plan-pendiente`.
Ejecución probatoria ampliada: **2026-09-27T01:41:42Z** (reloj real UTC).
Dictamen de la versión indicada: **NO_CONFORME**.

Se conserva intacto `REVISION_FAILCLOSED_INICIAL_2026-09-26.md` y su resultado
histórico. Esta reinspección acredita que sus adversarios han pasado en una
versión posterior; no reescribe su firma ni adjudica al autor las pruebas del
revisor. Tampoco reutiliza como aprobación independiente la reejecución anterior
del autor.

## Objeto inspeccionado y prueba durable

| Archivo | SHA-256 inspeccionado |
|---|---|
| `scripts/build_audit_deliverables.py` | `01bdd7e1ce15019b0ba701c81ccb4b51cbf0e1ab0b100a347edfc0424d35f6f5` |
| `scripts/audit_chronology.py` | `7d977bae7c206eb61f20bae52035a133f31983fc05ae58c3f890f96b5ec7dba0` |
| `tests/test_build_audit_closure.py` | `a503e8a1d1e00a9ec5f120171e04224cbf5c7a9d61ec7671cba50071580a99c3` |
| Fixture independiente original, `fixtures/revision_failclosed_independiente_20260926.py` | `b94fc19fd17b4533ecfdbaa04fc229dea9c0d4b76229b4589c6f87cad36c37b9` |
| Fixture independiente ampliada, `fixtures/reinspeccion_failclosed_independiente_20260927.py` | `def926033bd47cb00d0546126537758388590212c0c1b0ea5f0b350c143a8467` |

Los resultados nominales completos, incluidos ambos fallos y todos los PASS,
están en `reinspeccion_failclosed_independiente_2026-09-27.json`. La fixture
ampliada reutiliza únicamente las utilidades de la fixture independiente
original, no las fixtures escritas por los autores del código. Trabaja en
directorios temporales con documentos y firmas declaradamente artificiales.
Su exitcode no resume el resultado: se analizaron las entradas JSON una a una.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 docs/auditorias/fixtures/revision_failclosed_independiente_20260926.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/auditorias/fixtures/reinspeccion_failclosed_independiente_20260927.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_build_audit_closure tests.test_build_audit_deliverables tests.test_audit_chronology -q
```

Resultado independiente: **32/32 adversarios originales**, **20/22 de la
ampliación**, y **36/36 tests focalizados**. El éxito de los tests del autor no
neutraliza los dos fallos independientes de la ampliación.

## Reparaciones anteriores comprobadas

- La fecha global anterior a la segunda semántica ya no conserva CONFORME.
  El expediente transporta el máximo UTC de los censos y los UTC nominales.
  La ampliación comprueba separadamente C y S: 14:59:59 frente a un último eje
  nominal a las 15:00 devuelve PENDIENTE; igualdad exacta admite la fixture;
  día sin hora no demuestra orden dentro del mismo día y queda PENDIENTE.
- Las filas globales duplicadas, incluso contradictorias en cualquiera de los
  dos órdenes, se rechazan antes de construir el diccionario. Ya no opera
  «la última gana».
- El inventario semántico y los hashes de congelación y de los dos censos se
  comprueban antes/después del enlace. Una fuente cambiada inmediatamente
  después del `validate()` real del censo ya no cierra.
- `assert_nominal_reviews_current` vuelve a leer las filas y revalida todos sus
  artefactos. Doce casos propios C/S cambian o borran la prueba, cambian o
  borran el registro nominal, cambian un artefacto adicional que no es el
  documento principal o cambian el destino de un enlace simbólico permitido.
  Todos se rechazan. Los dos controles negativos desactivan únicamente ese
  guard en memoria: reaparece CERRADO. Esto comprueba que se ejercitó la
  protección concreta, sin alterar producción.
- Los adversarios originales vuelven a rechazar ciclos por `manifest`,
  disposiciones, controles y matriz S, por ruta directa, nombre lógico,
  destino resuelto y directorio enlazado; una prueba obsoleta no oculta un
  ciclo posterior. La historia obsoleta se conserva y no presta aprobación;
  una reinspección nueva puede coexistir sin reescribirla. Duplicados de
  censos, dependencia inválida, censo negativo o segunda semántica ausente
  dejan abierta la C.
- Relectura del contrato: C usa una instancia aislada del verificador íntegro
  y su `validate()`, sin reducirlo; los cinco ejes semánticos no aprueban los
  dos ejes nominales restantes. S requiere cuatro ejes actuales independientes
  del censo C. La preparación S precede a la congelación semántica y el modo
  normal exige los bytes S ya preparados. La firma global fija además el
  expediente completo: cambiarlo sin cambiar C invalida la firma.

## NC-FC-20260927-01 — PENDIENTE importa CERRADO (P1)

Localizador en la versión inspeccionada: `build_second_review`, rama
`previous['resultado'] == 'PENDIENTE'` (líneas 2717–2723); contadores y veredicto
en `report_markdown` (líneas 2770–2784), y contador de `main` (línea 3133).
`/root/inspeccion_relojes` había señalado esta posibilidad en un mensaje; el
revisor la reprodujo ahora y no se atribuye el descubrimiento original.

Se crea el censo artificial completo de 483 revisiones R pendientes y solo se
cambia `estado_cierre` a CERRADO en las entradas anteriores. El constructor
copia ese campo por la rama PENDIENTE, sin necesitar identidad de revisor,
fecha o evidencia válidas: devuelve **483/483 PENDIENTE/CERRADO**. El informe
declara **«CERRADA: la segunda revisión independiente está documentada.»**,
porque su contador solo consulta `estado_cierre`.

Es un cierre administrativo espurio, no una revisión científica verdadera.
No se afirma que evada todas las puertas posteriores: otro validador puede
rechazar la contradicción. El constructor, el informe y su propio contador de
pendientes no deben importarla como cierre. Corrección mínima propuesta al
autor: rechazar el estado incoherente o forzar ABIERTO al conservar una fila
PENDIENTE; conservar solamente su texto abierto. Añadir la regresión con todas
las filas para comprobar también el veredicto agregado.

## NC-FC-20260927-02 — matriz S con A ya cambiada (P2)

Localizador: `build_source_matrix`, lectura `current = ... load_sources(root)`
(línea 1293) y retorno después de `assert_nominal_reviews_current` (1515–1516).

Fixture S01 con cuatro dictámenes nominales vigentes, artefactos externos al
CSV A y matriz inicial cerrada. Justo después de leer A, y **antes del retorno
del constructor**, se cambia el título de S01 en el CSV canónico temporal.
Los dictámenes, el documento nominal y su mapa de artefactos no cambian. El
constructor devuelve S01 CERRADO con:

- SHA anterior: `da8fdc2d90db4337857fa31f48d5a30bdc8e8e838083fb8381e30f2396afd339`.
- SHA de A que ya existe al retornar: `4ede6568627b119a126279fbcf350d893e80eb16f0fc6741742c5a8be0e290b6`.

La recarga nominal no comprueba por sí misma la identidad canónica a la que
se enlazó. Es una omisión concreta de relectura de A, no una exigencia de
atomicidad universal del sistema de archivos ni una escritura arbitraria
posterior al último guard. Su alcance probado es el constructor S, usado
también en preparación S; no se declara una evasión global de `make verify`.
La posterior reconstrucción o congelación íntegra puede advertir la diferencia.
Corrección mínima propuesta: fijar y revalidar A en el mismo intervalo de
construcción, conservando la separación acíclica S/C. No exigir que la prueba
de cada fuente incluya el CSV A entero para suplir este control del adaptador.

## Límite del dictamen

La comprobación temporal prueba formato, ligadura y orden declarado, no que
una fecha histórica sea auténtica ni que una etiqueta de revisor identifique
a una persona independiente. Los fixtures no constituyen evidencia editorial
ni científica del corpus vivo. Este informe no firma ninguna C, S, censo,
segunda revisión real, control manual, conjunto de 210 controles ni cierre
global. No se editó la implementación para obtener el resultado. Las dos NC
se comunicaron al autor antes de cualquier reparación posterior; un nuevo
hash requiere reinspección y addendum, sin sustituir este registro.
