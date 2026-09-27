# Integración de recuentos y tiempo de pérdida génica para R-0212

Autor: `/root`. Rama: `codex/cierre-plan-pendiente`. Fecha UTC: 2026-09-27.
**Integración de autor; no sustituye revisión científica independiente.**
Las revisiones se han reactivado después de que el usuario informase de cuota
disponible. Los dictámenes previos y los posteriores se conservan separados.

## Evidencia primaria y límites

El literal de `docs/C01-PROMPT-INVESTIGACION.md:151` pide trayectorias,
recuentos, tiempo y forma de curva. No exige una tasa idéntica entre linajes.
Se recuperó el PDF editorial íntegro de
[Forni et al. (2026), S512](https://doi.org/10.1016/j.ympev.2026.108532)
en el repositorio KIT y el HTML íntegro de
[Degnan, Lazarus y Wernegreen (2005), S562](https://pmc.ncbi.nlm.nih.gov/articles/PMC1182215/).
El segundo artefacto es HTML, no PDF ni JATS: los intentos de obtener esos
formatos no dieron un documento válido y no se incorporaron como tales.

S562, Results, *Differential gene loss, yet complete stability of genome
architecture within Blochmannia*, empareja explícitamente dos recuentos con
el intervalo de divergencia tomado de Degnan et al. (2004):

| Registro | Linaje | Recuento | Tiempo transcurrido |
| --- | --- | --- | --- |
| C-2833 | B. floridanus | 25 ORF perdidos o inactivados | 16–20 Myr |
| C-2834 | B. pennsylvanicus | 4 ORF perdidos o inactivados | 16–20 Myr |

Son inferencias desde inventarios genómicos bajo un supuesto ancestral, no
un experimento longitudinal. No se transformó la inactivación en eliminación
física de ADN ni se calculó una tasa propia. Las pérdidas paralelas pueden
subestimar los recuentos. El penúltimo párrafo de Discussion dice que los
datos no distinguen los puntos de aceleración o pérdida de genes concretos
en B. floridanus: C-2835 conserva esa limitación explícita. Los dos recuentos
acumulados no definen una curva continua fechada.

S512 ofrece una forma bifásica comparativa, conservada en C-1088. Su eje
cuenta ramas respecto de la transición, no años. Methods, *Inference of gene
families duplication, transfer, and loss*, define los parámetros DTL como
probabilidades no normalizadas por rama (C-1120). Results publica medianas
de 0,592 ± 0,21 en ramas de establecimiento y 0,185 ± 0,123 en las tres ramas
anteriores y posteriores (C-2836/C-2837). El ± es desviación estándar, no
intervalo de confianza. Estos parámetros no son genes/Myr ni la frecuencia
por familia calculada mediante otra fórmula. No se unieron los trabajos
para fabricar una serie temporal única.

Se consultaron además Clayton (2012), Oakeson (2014), Delmotte (2006),
Bourguignon (2020) y S264 como pistas y controles. No se incorporaron cifras
de ellos a estas nuevas C. En particular, la pareja porcentajes/28.000 años
de Clayton depende de una tasa prestada de Buchnera; no se la atribuyó a
Oakeson ni se presentó como duración directamente medida de la asociación.

## Integración e historia

C-1088 conserva su proposición con localizador preciso y límite del eje.
C-1120 sustituye la afirmación de falta de tasa universal por la definición
publicada del parámetro. C-2833–C-2837 se añadieron al final de `15.csv`, sin
renumerar claves existentes; se añadieron seis filas F y cinco entidades B.
Los dos predicados nuevos se definieron inmediatamente en la sección 0.
La prosa conserva la separación entre recuentos, cronología y resolución.

MREQ-0034 enlaza exclusivamente los recuentos y tiempos de C-2833/C-2834,
no los parámetros DTL. El primer intento fue rechazado porque el objeto no
expresaba nominalmente ambas dimensiones; se hicieron explícitos «número
de genes perdidos o inactivados» y «tiempo transcurrido», sin modificar el
validador. R-0212 documenta cobertura con los límites de C-2835; no acredita
conformidad de un control manual ni segunda revisión.

BN-144 se retiró del registro activo. `retirada_bn144_2026-09-27.json`
conserva su fila, Q, las dos C anteriores, R, MREQ y las huellas de las 495 BN
previas; SHA-256:
`fd4d62981bf165f2b0246b5738853e1a8c7af2d184c4f12655fa420defac6673`.
La fecha declarada de la consulta original sigue sin quedar acreditada por
esta integración; tampoco se transforma su reinspección anterior en una
aprobación científica. BN-043 se conserva íntegra como registro histórico
activo de la consulta distinta sobre una tasa universal; ya no se usa como
una condición añadida de R-0212 ni para sostener C-1120.

El contrato nominal pasa de 495/483/12 a 494/482/12; sigue exigiendo las 408
consultas residuales y los dos positivos. Se añadió rechazo de reintroducir
BN-144, incluso si se compensa eliminando otra fila. No se redujo la población
de consultas residuales ni se promovió ningún NO_CONFORME.

`integracion_s512_s562_2026-09-27.json` documenta el inventario 448→450,
conservando todos los archivos anteriores. El corte intermedio tiene SHA-256
`170c7d69a86dbc8361aed5214e5e2c1452b5fee54c382b4cfb3cd61f02960647`.
Durante la revisión independiente se detectó que el antiguo PDF de S296 era
un preprint, no la versión PNAS citada. Se conservó intacto y se añadió el HTML
final correcto; el delta separado está en
`integracion_s296_version_final_2026-09-27.json`. Inventario resultante: 451
archivos, SHA-256
`62fe8db317f35c6679f79343610a8ebd1e1069944c66769b477742860e2791bc`.
`fuentes/` sigue ignorada por Git; no se forzó su alta.

La actualización de acceso conserva las filas anteriores en
`actualizacion_acceso_s296_s512_s562_2026-09-27.json`: 288 textos obtenidos
y 239 restantes de 527 fuentes. La nueva fecha describe la recuperación
actual, no autentica la descarga histórica ni aprueba apoyo científico.

## Hallazgos independientes posteriores sobre HGT

La instantánea del revisor
`evidencia_revision_independiente_s560_hgt_r0212_2026-09-27.json` conserva
las filas que rechazó por atomicidad, aceptación no acreditada y el modo
de fallo atribuido a S296. No se reescribió para sustituir el rechazo.
`correccion_hgt_tras_revision_2026-09-27.json` conserva las versiones previas
y corregidas del autor:

- C-1186 expresa solo la hipótesis de barrera; C-2838 conserva por separado
  la interpretación de Ku y Martin sobre rareza/importancia evolutiva.
- C-2832 expresa solo la media aproximada; la cautela de los autores queda
  en Motivo y en la prosa.
- C-1197 restringe el falso positivo a contaminación no detectada, sin llamar
  a cobertura/binning causas ni atribuir coensamblaje quimérico al pasaje.
- C-1197/C-1198 no afirman consenso amplio sin acreditación; las dimensiones
  de aceptación y fuerza se mantienen distintas.
- C-1196 conserva su proposición y añade localizador de la versión PNAS final.

Esas correcciones se remitieron al revisor para reinspección con huellas
nuevas. `REINSPECCION_INDEPENDIENTE_DELTA_HGT_2026-09-27.md` y su CSV
nominal dictaminan conformes las seis C de ese delta; conservan por separado
los cuatro rechazos iniciales. El revisor participó en búsquedas/propuestas
anteriores: es independiente de esta implementación, no un segundo
investigador ajeno a todas las búsquedas. No se extiende su dictamen a todo
el censo ni a las revisiones globales. Los tests del autor no se presentan
como su dictamen.

## Verificación

Pasada sobre 2838 C, 527 S, 494 BN y 451 artefactos de fuentes, observada
antes de las correcciones de infraestructura posteriores:

- 236 pruebas unitarias pasan. Validación estructural, auditoría semántica,
  migración, procedencia de las 2838 C y censo de 620 F pasan; esos controles
  mecánicos no adjudican apoyo científico nominal.
- QA tabular externa: 97 CSV, 63627 celdas, cero diferencias. Evidencia:
  `qa_tabular_externa_2026-09-27_corpus2838.json`, SHA-256
  `8cfe215b6f339beb0a940c5d48e178339d7172aedd91389793570916bd6dd591`.
- Las 410 consultas históricas fueron comparadas entre búsqueda literal e
  índice: las 408 negativas conservan cero coincidencias; C-2472 y C-2489
  conservan tres y cinco. No son una revisión científica independiente.
  Evidencia: `evidencia_reinspeccion_autor_bn_v3_2026-09-27_inventario451.csv`,
  SHA-256 `04c0f903bf5669ac54d12f461a5f7f9796c816e525dd3319a9d372971b20307e`.
- La cronología tiene 2065 filas, sin errores; las 1657 previas son prefijo
  idéntico. Las nuevas fechas describen ejecuciones reales entre 01:26:53Z
  y 01:30:13Z, no acreditan retrospectivamente las fechas declaradas antiguas.
- Linaje de 97 tablas, trazabilidad de 4488 segmentos y censo de 76 requisitos
  de magnitud pasan. Dos renderizados en copias aisladas producen nueve
  salidas idénticas. Esto verifica el renderizador, no toda la puerta aislada.
- `make verify` termina con código 2 en el censo semántico: congelación
  obsoleta/sin UTC válida y matrices nominales primera/segunda incompletas.
  No se hizo pasar la puerta mediante firmas automáticas ni rebajas.

La instantánea `integridad_delta_r0212_s296_2026-09-27.json` conserva las
huellas y límites de esta pasada. La revisión de infraestructura posterior
detectó además dos casos adversarios pendientes; sus rechazos se conservan
en `REINSPECCION_FAILCLOSED_INDEPENDIENTE_2026-09-27.md` y no se contradicen
con el éxito de los tests anteriores.
Este informe no declara completo el plan ni adjudica el censo semántico,
los 210 controles manuales o las segundas revisiones globales pendientes.
