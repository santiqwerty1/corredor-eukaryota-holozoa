# Diagnóstico independiente nominal: BN-134, BN-135, BN-140 y BN-142

Revisor: `/root/inspeccion_relojes`. Rama observada: `codex/cierre-plan-pendiente`.
Captura de objetos vivos: **2026-09-27T01:32:36Z**. Esta es una observación
nueva, no una fecha reconstruida para búsquedas antiguas.

Dictamen del lote: **NO_CONFORME para declarar completados los cuatro objetos**.
Hay datos positivos recuperables, cobertura parcial y campos todavía sin
verificar. No se declara falsa toda afirmación existente ni ausencia biológica.
No se firma el censo, ningún control manual, las segundas revisiones globales ni
el cierre de los 210 controles. Tampoco se revisa aquí la infraestructura
fail-closed: este revisor participó en su implementación y no es independiente
para aprobarla.

## Independencia y método

El revisor no redactó las cuatro BN ni las tablas 43, 51, 54 y 58. Sus trabajos
anteriores de mapeo y revisión afectaron a otras tablas, no a estas cuatro.
No ha modificado aquí C, BN, fuentes, tablas, manifiestos ni registros canónicos.
Las descargas nuevas permanecen en `/tmp/revision_4bn_20260927/`.

Se leyeron los literales pertinentes del encargo original, el handoff y la
revisión independiente anterior de las ocho BN. Se cotejaron los objetos vivos
y pasajes primarios concretos. La extracción de XML utilizó los párrafos de
JATS y las celdas de tablas, no coincidencias brutas en una línea XML completa.
La extracción de PDF utilizó `pdftotext`; De Bary, página física 11, también se
inspeccionó visualmente. Las búsquedas web y los resúmenes se distinguen abajo
de las fuentes completas. No se vuelve a ejecutar ciegamente una cadena de
comandos contenida en una BN.

`evidencia_diagnostico_4bn_2026-09-27.json` conserva los textos y hashes vivos
de cada fila examinada, de cada fila de las cuatro tablas, de C seleccionadas,
de los requisitos/magnitudes y de los artefactos leídos. La huella de fila es
SHA-256 de JSON UTF-8, claves ordenadas, separadores compactos `,` y `:`,
`ensure_ascii=False`, seguido de LF. La inclusión mecánica de una fila en ese
inventario **no es un dictamen científico favorable sobre sus celdas**.

| BN | SHA-256 de fila viva |
|---|---|
| BN-134 | `93ab398640e379c6605447e71dbf09b8f52f2155cad3fc227b9bb4a0a455c857` |
| BN-135 | `585b3def9bbfab66a7515125b71dadc9e8dc44e8fb993145107be8b8dee372ec` |
| BN-140 | `06cd62c28c94dad1c075735ab8b9c292141ae66ffe48afaf0fd198e02ba2d574` |
| BN-142 | `be377b6eda20acef30e97c8af9576985d012c921cb4ad77f9a47697b73a183c4` |

La revisión anterior `REVISION_8BN_INTEGRACION_C1163_2026-09-26.md` mantiene
su alcance: reprodujo consultas, no aprobó su interpretación científica.
BN-134 tenía 11354 coincidencias con `Ma` poco discriminante; BN-135 terminó
con exit 2 y S213/S445 ausentes; BN-140 y BN-142 tenían 731 y 286 coincidencias,
respectivamente. Ninguno de esos recuentos demuestra cobertura por caso,
familia/linaje o término. No se reescriben esos dictámenes ni sus fechas.

## BN-134 / MREQ-0032 / R-0200: cada asociación y cada campo

El literal de §9 requiere por caso hospedador, simbionte, aportes de ambos,
antigüedad estimada del inicio, transmisión, tamaño del genoma comparado con
parientes de vida libre, EGT, importación de proteínas y dependencia o
reversibilidad. **No pide un método homogéneo entre casos ni una razón numérica
calculada por el compilador.** BN-134 añade ambos filtros; MREQ-0032 también
usa «razón genómica». No deben excluir una comparación publicada con tamaños
y unidades, aunque no haya una razón explícita. Cada cifra necesita su propio
organismo, objeto, método, fuente y límite.

La tabla 43 representa 19 asociaciones/grupos, pero representar una fila no
completa sus campos. Tiene 9 huecos de aportes, 9 de transmisión, 15 de genoma,
17 de EGT/importación y 11 de dependencia/reversibilidad. La columna de edad
no usa el marcador de trazabilidad, pero mayoritariamente dice NO LOCALIZADA;
eso no se cuenta como una edad. Hospedador y socio están nombrados en las 19.

Inventario completo del estado capturado. `T` significa texto sustantivo
existente, **no aprobado científicamente en este lote**; `H` es hueco explícito;
`NL` es edad no localizada. EGT e importación se separan aunque la tabla viva
los una. `parcial` significa que falta el comparando de vida libre.

| CSV | Caso | Hosp./socio | Aportes | Edad de inicio | Trans. | Genoma vs libre | EGT | Import. | Estado |
|---|---|---|---|---|---|---|---|---|---|
| 2 | Lenisia–Arcobacter | T | T | NL | T | H | H | H | H |
| 3 | ANME–SRB | T | T | NL | T | H | H | H | H |
| 4 | Pelomyxa–metanógenos | T | T | NL | H | H | H | H | H |
| 5 | ciliados–metanógenos | T | H | múltiples orígenes, sin fecha común | T | H | H | H | H |
| 6 | Angomonas–Kinetoplastibacterium | T | T | NL | H | parcial | T | T | H |
| 7 | Paramoeba–Perkinsela | T | H | NL | H | H | H | H | T |
| 8 | Paulinella–cromatóforo | T | T | 90–140 Ma | T | T, comparando no nominal | T | T | H |
| 9 | B. bigelowii–UCYN-A | T | T | inferencia de asociación ya establecida; ≈91 es divergencia A1/A2 | H | H | H | H | H |
| 10 | Hatena–Nephroselmis | T | H | NL | T | H | H | H | T |
| 11 | Rhopalodia/Epithemia | T | H | ≈12 Ma, subconjunto muestreado | H | H | H | H | H |
| 12 | Mesodinium–criptófita | T | H | NL | T | H | H | H | T |
| 13 | Dinophysis–plastos | T | T | NL | T | H | H | H | H |
| 14 | Elysia/Plakobranchus | T | T | NL | T | H | H | H | T |
| 15 | criptófitos/cloraracniófitos–nucleomorfo | T | H | NL; dos adquisiciones | H | H | H | H | H |
| 16 | dinotomos–diatomea | T | T | NL | H | parcial; mitogenomas | H | H | T con límite |
| 17 | kareniáceos–plasto haptófito | T | H | NL | H | parcial; plastoma | H | H | H |
| 18 | Tremblaya/Moranella | T | T | NL por reemplazo | H | H | H | H | T |
| 19 | áfido–Buchnera | T | H | 80–150 Ma son divergencia de cepas, no captura | T | H | H | H | T |
| 20 | hospedadores–Wolbachia | T | H | NL para origen único | T | H | H | H | T dependiente del caso |

El nombre de un hospedador o la palabra «vertical» tampoco sustituye la
comprobación de la especie, condición y evidencia. Los agrupamientos amplios
(ciliados, Wolbachia, dos tipos de nucleomorfo) requieren límites por linaje;
no se debe inventar una fecha de origen común para fenómenos independientes.

### Datos positivos efectivamente cotejados

1. **Angomonas deanei.** S237 JATS, introducción y `Results / Overall Genomic
   Content`, Table 1: identifica *Ca. K. crithidii* como el simbionte de
   *A. deanei* y CKcri en la tabla. Longitud publicada **821,932 bp** frente a
   **7,359,146 bp** de *Achromobacter xylosoxidans*. El párrafo inmediatamente
   posterior describe explícitamente a este último como libre y publica
   **7.36 Mbp**, 6,815 genes y **∼9 veces** los valores endosimbiontes. Son
   alternativas de transcripción de los autores, no conversión propia. No
   generalizar el valor CKcri a todos los Kinetoplastibacterium. La cifra
   tabular exige mantener el aviso de inspección humana que corresponda.
2. **Perkinsela.** S240 JATS, `Endosymbiont and host nuclear genome sequencing`,
   Par7: tamaño nuclear estimado **~9.5 Mbp**, 5,252 genes predichos. `Biology
   of a kinetoplastid endosymbiont`, Par10, califica expresamente a *Bodo
   saltans* como libre; Table 1 compara **9.5** con **39.9 Mbp**. No calcular
   un cociente ni confundir genoma nuclear con el mitocondrial. `Host-endosymbiont
   interactions`, Par14: **8 genes** probablemente derivados del simbionte
   entre **3,846** alineamientos interpretables. Se puede recuperar EGT
   candidato, no importación proteica demostrada: Par16 propone tráfico y
   metabolitos/posibles enzimas como hipótesis. La edad sigue sin cifra en los
   pasajes inspeccionados; Par4 dice que cuándo ocurrió es una incógnita.
3. **Paulinella.** S245 JATS Introduction/Par2 publica el intervalo **90–140
   Mya** atribuido a ref. 6. Par16 publica una estimación propia de **124 Mya**
   tras ampliar el muestreo y advierte que las dataciones moleculares son
   mínimas y podrían ser más antiguas. Son estimaciones distintas con método
   y atribución, no un intervalo que podamos promediar. Par3 nombra al
   comparando libre *Synechococcus* WH 5701. Par4 contiene la expresión inglesa
   ambigua `reduced one-third in size`; no se recomienda convertirla sin
   cotejar las cifras primarias subyacentes. Este lote no vuelve a certificar
   el 1,02 Mb de C-1044/S242, cuyo original no fue leído aquí.
4. **UCYN-A.** S455 JATS, párrafo que comienza `The age of divergence for
   UCYN-A1 and UCYN-A2`: **around 91 Myr ago** corresponde a divergencia de
   los dos linajes. Los autores infieren que la asociación ancestral con un
   hospedador relacionado con Braarudosphaera estaba establecida en el
   Cretácico tardío. C-1061 y la cautela de la tabla distinguen esos objetos;
   no registrar 91 como medida directa de captura.
5. **Buchnera.** S263 PDF física 1 / impresa 81, columna izquierda: el resumen
   publica cromosoma **640,681 bp** más dos plásmidos y una comparación
   **un séptimo del genoma de E. coli**. La identidad de E. coli como pariente
   se explicita, pero esta lectura no verifica adicionalmente el rótulo
   ecológico «vida libre» de la cepa comparada. El párrafo introductorio
   posterior recoge una edad de establecimiento de **200–250 Myr** atribuida
   al análisis filogenético de su ref. 7 (Moran et al., 1993). Esto no es
   C-1099 (80–150 Ma para divergencia de cepas) ni una datación propia de
   Shigenobu et al. Se puede recuperar como estimación expresamente atribuida
   y buscar la ref. 7 antes de adjudicar su método/calibraciones. No se ha
   verificado aquí si trabajos posteriores revisan esa edad.

Las cifras de Rhopalodiaceae (C-1637/S454 y C-1640/S456), los mitogenomas de
dinotomos y plastoma de Karlodinium se inventariaron, **no se aprobaron** sin
leer sus originales en este lote. El tamaño de un compartimento retenido no
responde por sí solo al tamaño del genoma completo del socio. Tampoco basta
el marcador BN-134 agregado para justificar cada otro campo residual.

**Acción propuesta, no ejecutada:** retirar del planteamiento los filtros
ajenos al literal; completar los comparandos y datos positivos nominales
anteriores con C específicas, conservar unidades y objetos, y revisar por
separado todos los restantes campos. No aprobar R-0200 ni MREQ-0032 por
contar 19 filas o por el resultado de `rg`.

## BN-135 / MREQ-0074 / R-0261: tres ejemplos no son tres orígenes probados

§12 nombra tres casos concretos y los llama independientes. No exige que
esos sean los únicos orígenes agregativos de toda la biota. §13 pide recuentos
según la literatura con autor y criterio. BN-135 añade «exactamente» y
«demuestre exhaustivamente»: retirar esa exigencia global no autoriza contar
los ejemplos como una magnitud publicada.

- **Capsaspora:** S206, resultados experimentales de agregación y Discussion,
  párrafo que empieza `The aggregative multicellularity observed`: la
  agregación está observada; la discusión plantea tanto caracteres ancestrales
  como evolución independiente y dice que el muestreo limitado impide
  discriminarlos con fiabilidad. La posición filogenética no resuelve sola
  la reconstrucción del carácter.
- **Fonticula:** [resumen primario de Brown et al. 2009](https://pubmed.ncbi.nlm.nih.gov/19692665/),
  DOI 10.1093/molbev/msp185: sitúa Fonticula junto a Nuclearia, hermano de
  Fungi, y sostiene independencia respecto de las radiaciones multicelulares
  fúngica y animal. No contrasta en ese resumen el origen de Capsaspora.
  El texto completo editorial no fue accesible en esta sesión; el intento
  del espejo no proporcionó el artículo. No se finge lectura integral de S213.
- **Dictyostelium y comparación agregativa:** S445, copia del laboratorio
  de Parfrey, PDF física 7, columna izquierda, Table 1 y discusión; la terna
  comparada allí es **Copromyxa, Fonticula y dictyostelids**, no Capsaspora.
  Su argumento favorece orígenes independientes y mecanismos distintos en
  Amorphea; no convierte esa terna en la terna del encargo. La copia es un
  PDF editorial de nueve páginas con paginación provisional 1–9; citar página
  física y apartado, no inventar equivalencia con la paginación final.
  [Copia primaria leída](https://www.zoology.ubc.ca/~parfrey/parfrey_lab/wp-content/uploads/2017/06/Parfrey_origins_multicellularity_2013.pdf).

C-1538 afirma ramas separadas, pero su predicado `converge_con`, objeto
«orígenes» y motivo apelan a independencia/reconstrucción ancestral. Esa
combinación no queda plenamente respaldada por los pasajes anteriores.
R-0261 consta como CUBIERTO sólo por C-1538: **no acredita íntegramente el
literal de independencia de los tres casos**. La tabla 51 agrega además
Ministeria y un recuento de 12 de otra fuente; no son sustitutos del examen
de la terna. Se mantiene NO_CONFORME para el cierre nominal. Es apropiado
explicar qué independencia sostiene cada autor y dónde sigue abierta;
no fabricar una cifra tres consensuada ni retirar los tres casos del texto.

## BN-140: matriz funcional, no una sola matriz publicada

§12 pide familias y linajes en que aparecen o faltan. Enumera además ocho
organismos para la comparación de genomas. No pide que toda la literatura
utilice un único muestreo ni un mismo método. Esos filtros añadidos por BN-140
y C-1992 no deben bloquear resultados nominales con métodos diferentes.

La tabla 54 tiene 12 familias/sistemas por cinco grupos: 60 celdas de
distribución, **44 huecos explícitos y 16 textos sustantivos**, no 16 positivos
automáticamente verificados. «Otros coanoflagelados» y «otros holozoos» no
dicen qué ocurre en cada taxón. *Thecamonas* no es holozoo y no tiene columna;
Salpingoeca, Ministeria, Sphaeroforma, Creolimax y Corallochytrium tampoco
quedan desagregados aquí. La tabla genómica 53 no reemplaza ese mapa funcional.
No se prescribe artificialmente una misma técnica a todos: sí una asignación
taxón/familia/evidencia suficientemente nominal para responder al literal.

Inventario por fila CSV; `H` lista columnas hoy vacías de adjudicación. M=
Monosiga, C=Capsaspora, OC=otros coanoflagelados, OH=otros holozoos, A=Metazoa.
El resto es texto existente pendiente de cotejo salvo los pasajes explícitos
que siguen.

| CSV | Familia/sistema | H | Incidencia nominal |
|---|---|---|---|
| 2 | integrinas/adhesoma | OC, A | «distribución mosaico» en OH no identifica taxones |
| 3 | cadherinas | C, OC, OH, A | 23 genes M no responde por los demás |
| 4 | ECM/colágeno | C, OC, OH, A | dominio/motivo no demuestra función ni colágeno completo |
| 5 | pTyr/TK/PTP/SH2 | OC, OH, A | conteos y ensayos deben conservar componentes y organismo |
| 6 | Notch/Delta | M, C, OH, A | OC mosaico puede precisarse con S435 |
| 7 | Hedgehog | M, C, OC, OH | S352 ya permite recuperar M y C con límite de anotación |
| 8 | GPCR | M, C, OC, OH | **A=235 dominios es objeto equivocado** |
| 9 | Brachyury | M, C, OC, OH, A | filogenia/afinidad de unión no cubre todas las celdas |
| 10 | Runx | M, OC, OH | separar dos genes Capsaspora de cofactores no localizados |
| 11 | p53/p63/p73 | M, C, OC, A | inferencia ancestral en OH no da presencia en linajes actuales |
| 12 | Myc/Max | OC, OH, A | ensayo bioquímico Monosiga no se extrapola |
| 13 | homeodominio | M, C, OC, A | distribución parcheada sin taxón no completa la columna |

**Correcciones positivamente sustentadas:**

- S352 JATS `The origins of metazoan protein domains`: los **235** son dominios
  innovadores del tallo metazoano en conjunto, entre ellos componentes
  extracelulares. **No son 235 GPCR ni evidencia nominal de esa celda**.
  C-1583 conserva el objeto general; es su adjudicación a la celda GPCR/A
  la que falla.
- S352 JATS `Gene repertoire of Capsaspora`, párrafo que empieza `Our data
  reveal the contrasting evolutionary histories`: ambos genomas estudiados
  carecen de receptores/ligandos anotados de Hedgehog y de la familia
  Rhodopsin de GPCR en ese análisis. Permite restaurar Hedgehog/M y C con
  alcance exacto; para GPCR **sólo la subfamilia Rhodopsin**, no todos los
  receptores GPCR. C-1581 ya recoge Hedgehog, pero su localizador
  `§Signalling pathways` no es el encabezado de ese párrafo en el JATS local;
  el encabezado local verificable es el anterior.
- Ese párrafo S352 publica **92 TK en Capsaspora y 128 en M. brevicollis**.
  Son recuentos/versiones distintos de ~120 de S147; no elegir uno como
  «corrección» sin especificar estudio y método. No se leyó S147 en este lote.
- S435 JATS `Choanozoan-specific gene families: innovation and loss` identifica
  un homólogo claro de Notch en *Mylnosiga fluctuans* y dominios parciales
  en otros cinco coanoflagelados. `Materials and methods / Notch and Delta`
  explica que el criterio es arquitectura de dominios; sus filogenias están
  poco resueltas. No convertir la distribución en función Notch demostrada
  ni tratar un subconjunto de dominios como receptor completo. Los autores
  conservan como alternativa convergencia por barajado de dominios.

**Resultado:** la matriz no está completa. Tampoco se justifica mantener
como no localizada una celda cuyo dato nominal puede recuperarse ahora.
Cada ausencia declarada debe conservar muestra, criterio y versión; los
44 huecos no equivalen a 44 ausencias biológicas. No se adjudica por este
informe el apoyo de S436–S441 no leído ni se cierra BN-140 como control global.

## BN-142: introducción, uso temprano y prioridad son ejes distintos

§14 pide quién introdujo cada término y cuándo, su problema, reemplazo y
uso legítimo con fuente. Autorizar una glosa ante falta de fuente no permite
llamar «acuñación» a cualquier mención fechada. El campo de tabla 58 tiene
12 huecos explícitos, 6 atribuciones nominales existentes y 2 usos tempranos
expresamente limitados. Los seis no han sido todos ratificados por esta
revisión: se inventarían para evitar que queden ocultos detrás de BN-142.

| CSV | Término | Cobertura actual / pendiente |
|---|---|---|
| 2 | Protista | Haeckel 1866; C-1777 remite a S386/S422 históricos, sin primaria original leída aquí |
| 3 | protozoo | Goldfuss 1817/1818, C-1783 distingue impresión/clasificación; preservar distinción; no nueva aprobación |
| 4 | alga | HUECO BN-537; no inventar un acuñador único de todos los sentidos |
| 5 | invertebrado | Lamarck alrededor de 1801; C-1794 atribución de fuerza baja; fecha de título no prueba prioridad |
| 6 | procariota | Chatton 1925 / difusión1962; S393 nominal no leído aquí; no confundir introducción/difusión |
| 7 | acritarco | Evitt1963; identidad editorial S395 localizada, texto de propuesta no recuperado aquí; metadatos no aprobación |
| 8 | reino | HUECO BN-538; distinguir palabra antigua de esquemas de cinco/seis/siete reinos |
| 9 | Archezoa | HUECO BN-539; falta pasaje de propuesta e identificación de versión/circunscripción |
| 10 | Excavata | HUECO BN-540; falta propuesta nominal y circunscripción |
| 11 | Chromalveolata | HUECO BN-541; falta propuesta nominal, no rellenar sólo por fecha del DOI |
| 12 | Unikonta/Bikonta | HUECO BN-542; revisar cada nombre por separado y su circunscripción |
| 13 | hongo para oomicetos/mohos | HUECO BN-543; aplicación histórica de un vocablo no tiene por qué equivaler a acuñación de una hipótesis |
| 14 | flagelo | HUECO BN-544; distinguir introducción de palabra y aplicación a estructuras no homólogas |
| 15 | simbiosis | HUECO BN-545; recuperable uso/definición De Bary1879, no prioridad sobre Frank sin cotejo |
| 16 | endosimbiosis seriada | Sagan1967 documenta propuesta; acuñación literal de la expresión no probada aquí |
| 17 | eucariota primitivo | HUECO BN-546; descriptor no adjudicable a un autor por memoria |
| 18 | organismo simple | HUECO BN-547; distinguir crítica del descriptor de su origen lexical |
| 19 | fósil viviente | HUECO BN-548; recuperable uso Darwin1859p107 y486 |
| 20 | eslabón perdido | uso más antiguo verificado Vestiges1844; la propia celda no afirma prioridad universal; no ratificado aquí |
| 21 | basal aplicado a viviente | uso localizado McDade1990; no equivale a acuñación ni a fecha universal; no ratificado aquí |

### Nuevas primarias históricas leídas

- **De Bary**: [escaneo de Die Erscheinung der Symbiose](https://darwin-online.org.uk/converted/pdf/1879_Bary_Symbiose_A3450.pdf),
  título en páginas físicas 5 y 7, año 1879; prefacio física10/impresa4,
  noviembre1878; física11/impresa5 define Symbiose por convivencia de
  organismos de distinto nombre. Inspección visual de esta última página.
  Física27/impresa21 reúne parasitismo, mutualismo y otras asociaciones como
  casos de una categoría amplia. Acredita uso, definición, autor y fecha de
  publicación, **no prueba que De Bary acuñara primero la palabra**. La
  atribución a Frank1877/symbiotismus apareció en resultados bibliográficos,
  pero su original no se leyó: queda pendiente, no completado por memoria.
- **Darwin**: [primera edición de Origin of Species](https://darwin-online.org.uk/converted/published/1859_Origin_F373/1859_Origin_F373.html),
  capítuloIV, página107, párrafo después de Ornithorhynchus/Lepidosiren, usa
  **living fossils**. CapítuloXIV, p486, vuelve a la expresión. La transcripción
  está identificada como primera edición1859; el contenido fue leído, no sólo
  la portada. Permite una afirmación nominal de uso en1859. C-1870/S415 trata
  pluralidad de criterios, no sustituye esa historia. Este cotejo solo no
  determina la primera ocurrencia de toda lengua/literatura.

Las otras fuentes históricas nombradas en la tabla se mantienen como pistas
o soporte previo, no como lecturas nuevas ficticias. La imposibilidad de
identificar un acuñador único para una locución informal no exonera de
documentar su uso/problema ni de señalar precisamente qué aspecto no se
localizó. BN-142 necesita adjudicación término por término; no basta una
consulta genérica por `coined|introduced`.

## Propuestas de sustitución: evidencia nueva no borra el residual histórico

Ampliación de alcance documental solicitada por root; observación real
**2026-09-27T01:37:34Z**. Se leyó el censo residual v3 y el mapeo vivo, sin
editarlos. Una evidencia semántica nueva no convierte en exitosa la consulta
literal histórica. Deben preservarse sus 410 rechazos/disposiciones de origen,
las 408 consultas negativas, los dos positivos literales existentes y sus
versiones. No se propone añadir estas nuevas fuentes a `POSITIVE_CLAIMS`.

Identificación exacta de las celdas potencialmente afectadas (fila CSV incluye
cabecera), C residual/mapeada y BN. «Completo» se refiere sólo al alcance de la
proposición descrita, nunca a toda la fila de la asociación ni al control.

| Objeto | C actual / BN | Qué permite la fuente | Qué NO permite restaurar o cerrar |
|---|---|---|---|
| tabla43:fila6:genoma del socio comparado con parientes de vida libre | C-1030; **no está en el residual v3** | S237: comparación nominal CKcri821,932bp / A.xylosoxidans7,359,146bp; completo para esas dos longitudes y condición libre | No vuelve a verificar la cláusula de pérdida de genes de división del texto actual; si se conserva necesita su soporte propio |
| tabla43:fila7:genoma del socio comparado con parientes de vida libre | C-2708 / BN-473 | S240: genomas nucleares Perkinsela9.5Mbp / Bodo39.9Mbp, este último libre; completo para comparación nuclear | El residual anterior incluía además seis genes mitocondriales. No se cotejaron aquí; no restaurar automáticamente esa cláusula |
| tabla43:fila7:EGT al núcleo; importación de proteínas de vuelta | C-2709 / BN-474 | S240Par14: ocho EGT candidatos entre3846alineamientos; sólo componente EGT | No afirma ausencia de EGT, ni prueba importación dirigida. Par16 es hipótesis de tráfico; la parte importación requiere límite propio |
| tabla43:fila19:genoma del socio comparado con parientes de vida libre | C-2754 / BN-511 | S263: cromosoma640,681bp, dos plásmidos y comparación publicada un séptimo de E.coli | No respalda aquí el rango moderno412–646kb del residual antiguo ni verifica la ecología libre de la cepa de referencia. Parcial respecto de todo el campo solicitado |
| tabla43:fila19:antigüedad estimada del inicio | C-1099; **no está en el residual v3** | S263 recoge establecimiento200–250Myr atribuido a suref7, separado de divergencia80–150Ma | No es datación propia de S263; falta inspección de ref7/metodología y vigencia frente a revisiones posteriores |
| tabla54:fila7:Monosiga | C-2468 / BN-329 | S352+C-1581: ausencia anotada de receptores/ligandos Hedgehog en el genoma estudiado; completo con ese límite | No ausencia universal en todo Monosiga/Choanoflagellatea ni de cada componente citoplasmático de la vía |
| tabla54:fila7:Capsaspora | C-2469 / BN-330 | Mismo párrafo S352 para Capsaspora; completo con ese límite | Mismas restricciones; no firma de otros linajes |
| tabla54:fila8:Monosiga | C-2474 / BN-334 | S352: receptores/ligandos de **Rhodopsin-family GPCR**, componente de la celda | No ausencia de todo GPCR; la antigua generalidad «familias antiguas» no queda validada |
| tabla54:fila8:Capsaspora | C-2475 / BN-335 | Misma subfamilia de S352; componente de la celda | No ausencia de todo GPCR ni función ensayada |
| tabla54:fila8:Metazoa | C-1583; **no está en el residual v3** | Detecta error de adjudicación:235 son todos los dominios innovadores del estudio | Retirar/reubicar ese dato no suministra aún un nuevo valor de GPCR para Metazoa |
| tabla54:fila6:otros choanoflagelados | C-1580; **no está en el residual v3** | S435 nombra Mylnosiga fluctuans para Notch y el criterio de arquitectura | No completa todos los choanoflagelados ni prueba actividad de Notch/Delta. No cubrir Delta con una afirmación sólo de Notch |
| tabla58:fila15:quién lo introdujo y cuándo | C-2801 / BN-545 | DeBary1879: uso y definición fechados; componente histórico de la celda | No demuestra prioridad universal ni resuelve Frank1877; la negativa literal anterior permanece histórica |
| tabla58:fila19:quién lo introdujo y cuándo | C-2804 / BN-548 | Darwin1859p107/486: uso fechado de living fossils | No prueba sola prioridad lexical universal; falta apoyo historiográfico de la atribución de acuñación si se quiere esa formulación |

No se propone una disposición de producción en este informe. Para habilitar
una sustitución, una disposición nueva y auditada deberá identificar la clave
exacta `(csv_path,fila,columna)`, el residual y hash anteriores, el nuevo texto
y hash, C nuevas o modificadas, fuentes/pasajes y huellas, el componente
resuelto y los límites restantes, autor, revisión independiente y UTC reales.
La relación debe ser **sustitución prospectiva por nueva evidencia**, no
aprobación retrospectiva de la celda rechazada. El validador deberá fallar si
esa disposición falta, está obsoleta o no cubre todos los componentes que el
texto nuevo afirma; ni un resultado de búsqueda ni la fecha sola la suplen.

Las fuentes S237/S240 no bastan para restituir literalmente todos los textos
históricos. El inventario paralelo de esta propuesta conserva las filas de
mapeo y de residuales seleccionadas; no les cambia `NO_CONFORME` ni
`estado_revision`. No se aprueba aquí una implementación de ese contrato.

## Resultado y límites de la entrega

Hay acciones nominales realizables con primarias ya leídas: genomas
Angomonas/Perkinsela y EGT candidata Perkinsela; comparación Buchnera y edad
histórica atribuida; límites precisos de UCYN-A y Paulinella; Hedgehog por
dos genomas y corrección de la celda235/GPCR; uso histórico de Symbiose y
living fossils. Son **propuestas de parche con evidencia**, no implementación
ni aprobación anticipada de sus futuras versiones.

Los cuatro dictámenes generales permanecen NO_CONFORME para cierre de
cobertura. Cambiar la consulta para ajustarla al literal no debe rebajar la
exigencia de evidencia. Cada parche necesita nuevas huellas y una revisión
independiente posterior. No se reescribió el informe histórico S282/C-2823/E98
ni se trasladó su conformidad parcial a estas BN.
