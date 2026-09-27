# Reinspección independiente de la adenda S240/S352 v2

Revisor: `/root/revision_residuales/candidatos_editoriales`. Autor de la propuesta: `/root/inspeccion_relojes`. Rama comprobada: `codex/cierre-plan-pendiente`. Captura nueva: **2026-09-27T04:10:23Z**. Adjudicación: **2026-09-27T04:12:43Z**. El revisor no redactó ni integró los objetos propuestos. Sólo escribió sus artefactos de auditoría; no modificó canónicos, fuentes, propuestas, validadores ni firmas globales.

## Resultado delimitado

Son conformes en su alcance exacto las nuevas C2852, C2876 y C2877. Se emite una revisión independiente nueva de la disposición C2474, con sus diez componentes, nueve C de soporte, tres artefactos y cinco pasajes. No es aprobación del paquete completo ni ejecución de la integración.

De las dieciséis altas B, once son conformes editorialmente y **cinco siguen NO_CONFORME**: Gapfiller, Image, ICORN, REAPR y HMMER. C1581 y C2851 continúan NO_CONFORME; el bloque Hedgehog y C2468 no quedan firmados. Las cuatro revisiones anteriores de disposiciones no se reescriben ni se vuelven a fechar.

## Identidad y cronología verificadas

| Objeto | SHA-256 |
| --- | --- |
| Propuesta autoral de adenda | `cf00495ba91d037d07c2f8b8ac1b950d58d0c4441b28e05e73a4336333894c58` |
| Evidencia autoral | `81d3c8f760eb1e2a97663ea93f06c47cfadb9100511f6dea2bb6529992db35a2` |
| Informe autoral | `8b98736767864a37f03e30fa0a6ff961edb4f5d17a572768d714112c1527cf69` |
| Propuesta v2 base inmutable | `96d36be9adeed056a5c5f6da54321101b2dc25e7ae1bc28cb9258dae0b3e8bfa` |
| Consumidor `scripts/residual_semantic_dispositions.py` | `222a9dd383dc904a08ccb881fd8122abd9b337e24a062e0b5c84cc32b3a593d4` |

La evidencia autoral declara 03:29:46Z y la adenda queda fijada a 03:32:23Z, ambas anteriores a esta lectura y adjudicación. Los `antes` de las tres C y de los dos objetos de prosa coinciden con v2. En C2876/77 cambia exclusivamente Motivo. C2474 conserva contenido, componentes, identidad, límites y artefactos; sólo cambian fecha, evidencia autoral y las dos huellas de soporte reparadas. No se confunde el hash completo de disposición `460070882ee339ef42a75fae24bbdbfe499acdf108c4bdfa39ff55772a7b1c5e` con el que exige el consumidor al excluir `revision_independiente`: **`677f853560fc329aa845378334a7e30ce424180fb9d6798d2ab7d51a41b1ebfc`**.

## Lectura sustantiva nueva

Se releen del artefacto primario S352 los párrafos completos de Results → Gene repertoire of Capsaspora (cuarto párrafo directo), Methods → Gene family analysis, Supplementary Information Note 5 pp.94–96, y se reinspeccionan visualmente Fig.4 p.6 y Fig.S26 pp.43–44 con sus leyendas. Se releen S563 DNA Preparation and Sequencing y Genome Assembly, y S240 Phylogenomics y Par16 para métodos y anclas B. La captura automática reextrae otros pasajes previos, pero su coincidencia no equivale a adjudicarlos otra vez: el inventario de lectura nueva está explícito en la evidencia independiente.

En la columna Monosiga de Fig.S26 hay puntos para Glutamate PF00003, Adhesion/Secretin PF00002, cAMP PF05462 y GPR108-like PF06814; no los hay para Rhodopsin PF00001, Frizzled PF01534, ITR-like PF10192 u OA1-like PF02101. La leyenda identifica los puntos con presencia de gen. Note 5 p.94 dice expresamente que ITR-like y OA1-like están ausentes en Monosiga. Los métodos explican inferencia por homología, no comprobación funcional. Fig.4 es coherente: ITR/OA1 azules, GluR/Secretin/GPR108 rojos y Rhodopsin/Frizzled punteados blancos.

Por ello C2876/77, con los nuevos Motivos nominales, quedan conformes. Se conserva el alcance del genoma analizado y la falta de identificación; no se infiere ausencia universal de GPCR ni falta de toda señalización. C2861 y su componente de celda conservan **una posición textual sobre ligandos**, no una conclusión obtenida de la ausencia de receptores.

C2852 nueva es una glosa documental legítima: C2847 y C2848 describen partes/dominios; C2849 los sitúa en proteínas diferentes. Ninguna de esas tres formulaciones identifica documentalmente un ligando Hedgehog completo. La glosa no decide existencia, inexistencia o función biológica. Elimina el antiguo blanco inventado —leer C1581 como ausencia de cualquier componente semejante— sin ocultar una refutación real: los dominios separados no refutan por sí solos falta de ligando completo. La tensión distinta Patched/receptores permanece en C2850 y C2851; esta última sigue bloqueada por C1581. El predicado nuevo se define inmediatamente en Motivo y en la prosa propuesta de convenciones.

## Cinco B no conformes: primera aparición real

Se leyó literalmente §17B: la última columna pide la fila del registro **donde aparece por primera vez**. El registro definido en §16 es el de afirmaciones C. No basta que una fila F tenga una referencia a esa C. La adenda explica honestamente sus anclas indirectas en metadata, pero esa explicación no cambia el significado de la columna B canónica.

| B | Ancla propuesta | Hallazgo reproducible | Reparación posible, no implementada |
| --- | --- | --- | --- |
| Gapfiller | C2839 | No aparece en ninguna C viva + propuesta; sí en método de F→C2839 | Añadir mención real al Motivo C2839, respaldada por S563 Genome Assembly |
| Image | C2839 | Igual; S563 lo nombra como herramienta de cierre de huecos | Igual |
| ICORN | C2839 | Igual; S563 lo nombra para corrección de bases | Igual |
| REAPR | C2839 | Igual; S563 lo nombra para partición de scaffolds | Igual |
| HMMER | C2864 | C2864 no lo nombra; primera mención literal prospectiva C2865 Motivo | Anclar B a C2865, sin ampliar C2864 |

Las búsquedas sólo localizaron candidatos; las filas C y F se cotejaron completas para adjudicar esta diferencia. Las once B conformes son Illumina HiSeq, SGA, Velvet, SSPACE, RAxML, PhyloBayes, BLASTP, FastTree, crio-SEM, LG+G+F y el concepto documental nuevo de C2852. FastTree aparece en C2824 Motivo y crio-SEM en C1040; no se les inventa una primera mención posterior. No es un censo global de B. Una futura modificación de C2839 exigirá nuevo hash y reinspección de sus dependencias, incluida cualquier disposición que lo fije; no puede conservar firmas por arrastre.

## C2474: conformidad prospectiva, no operacional

El expediente nuevo `revision_independiente_disposicion_c2474_adenda_s240_s352_v2_2026-09-27.json` cubre nominalmente los diez componentes. Se comprobaron por separado el contrato cerrado, independencia, UTC posterior, hash sin revisión, nueve soportes exactos, cobertura completa y uso de los tres artefactos. Estas comprobaciones son estructurales; el dictamen procede de la lectura anterior y la inspección visual, no del resultado del script.

La suplementaria se leyó en `/tmp/S352-supplement-preparacion-v2-20260927.pdf`, SHA `d0f556e6436a6bb67ac99f65f645fbd0995491e27ebce0eaef9585050c388c23`. Su destino declarado en `fuentes/` **todavía no existe**. Tampoco están integradas las nuevas C. No se ejecutó ni se afirma que pase `load()` operacional: deberán integrarse bytes y filas idénticos, así como la corrección y referencias autorales correspondientes. La revisión no retira la historia de BN334 ni convierte su cero literal en prueba científica.

## Bloqueos que no se levantan

C1581 canónica sigue exactamente con hash `9bdb1a21bbf293aed15a0e5a71b4bc62ac893567a672da0f7a356d3fd3f0ce16`: dos organismos, receptores y ligandos, localizador inexistente y estados sin reparar. No consta autorización del usuario para resolver la tensión conservación/atomicidad mediante archivo histórico íntegro y descomposición canónica. C2851 sigue con hash `266cd67714b6dc63d80e3e9bbb7c6d113a70e36e6288c1809c170d01100ec313`. La adenda no autoriza excepciones.

La prosa Hedgehog sustituye correctamente el falso enlace C2852 por la glosa y cambia «histórica» por «previa», pero su objeto completo sigue pendiente. La anotación autoral de conservación, con `habilita_cierre=NO`, es correcta como anotación, no como aprobación de la fila. El defecto de dependencia C2876/77 queda reparado para la prosa GPCR y su lista de referencias, sin adjudicar por arrastre C1582/C1583 ni todo el roll-up.

## Evidencia propia y preservación

| Archivo nuevo | SHA-256 |
| --- | --- |
| `evidencia_independiente_adenda_s240_s352_v2_2026-09-27.json` | `326a4e11de368e65fae40f01f10d9a39d4dbf96e4eb0bd706660761045aafe3b` |
| `dictamenes_independientes_adenda_s240_s352_v2_2026-09-27.csv` | `c5a527cd3601a3afcf2409bd1e7a54276e0225f84a36314463411e0834cbab14` |
| `revision_independiente_disposicion_c2474_adenda_s240_s352_v2_2026-09-27.json` | `91e4655b0b3966b5a58de80b8506d6c4f93c3fb4b44b2461a77d149f8eec15b2` |

El CSV nuevo contiene 35 adjudicaciones delimitadas: 10 conformes de alcance, 14 editoriales limitadas, 7 NO_CONFORME (cinco B y dos C), 1 pendiente de dependencia, 1 disposición prospectiva conforme y 2 dependencias reparadas sin cierre global. Cada objeto lleva hash y UTC real. `probe_revision_adenda_s240_s352_2026-09-27.py` es una captura de sólo lectura y no emite aprobaciones científicas.

Los informes y CSV anteriores, incluidos los rechazos de v1/v2, quedan intactos. Ni esta adenda ni las cinco disposiciones prospectivamente revisadas en conjunto cierran el censo científico, los 210 controles manuales, sus segundas revisiones, el resto del plan o `make verify`.
