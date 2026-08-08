# Corredor Eukaryota → Holozoa — Documento maestro provisional

**Fecha de corte bibliográfico: 8 de agosto de 2026.**

**Estado del corpus:** quinta integración estructural de las Partes 1A, 1B, 1C, 1D, 2, 3, 4, 5 y 6. Están desarrolladas las secciones 0–12 y 14, junto con búsquedas negativas incrementales. La sección 13 y el mapa probatorio completo de la sección 15 siguen pendientes. Metazoa permanece como nombre terminal.

**Arquitectura del repositorio:** los CSV de `data/` son la capa canónica de registros y tablas. Este documento autocontenido se genera desde esos CSV; `docs/informe.md` ofrece una versión de lectura con enlaces a los registros externos.

**Identificadores globales:** 1719 afirmaciones `C-…`, 446 fuentes `S…`, 106 eventos `E…`, 81 hipótesis `H…` y 90 búsquedas negativas numeradas. Las claves locales anteriores quedan sustituidas por las de este archivo.

**Unidad temporal por defecto:** Ma antes del presente. Cuando una fuente publica Ga, se conserva Ga. Los nombres cronoestratigráficos siguen la Tabla Cronoestratigráfica Internacional, versión 2026/06.

**Autoridades adoptadas:** Adl et al. 2019 para clasificación eucariota; EukProt, PR2 y UniEuk para secuencia, muestreo y armonización taxonómica; International Commission on Stratigraphy 2026/06 para tiempo geológico; ICZN, Madrid Code 2025, ICNP 2025 Revision y PhyloCode versión 6 para los ámbitos nomenclaturales correspondientes.

**Criterio de integración bibliográfica:** las fuentes se deduplican por DOI o URL canónica. Una coincidencia de título no prevalece sobre DOI distintos salvo cuando se verificó un metadato erróneo. Las correcciones quedan anotadas en el apéndice A.

**Etiquetas descriptivas cerradas del corpus integrado:**

- `raíz del árbol celular no especificada`
- `linaje hospedador arqueano no identificado`
- `simbionte alfaproteobacteriano ancestral no muestreado`
- `linaje asgard más próximo a Eukaryota no resuelto`
- `linaje alfaproteobacteriano más próximo a la mitocondria no resuelto`
- `población LUCA reconstruida`
- `población LBCA reconstruida`
- `población LACA reconstruida`
- `población FECA nuclear no muestreada`
- `población FMCA no muestreada`
- `población LECA reconstruida`
- `linaje eucariota troncal no muestreado`
- `donante bacteriano premitocondrial no identificado`
- `virus ancestral de Nucleocytoviricota no muestreado`
- `módulo ancestral de curvatura de membrana no muestreado`
- `raíz eucariota no resuelta`
- `población ancestral de Amorphea no muestreada`
- `población ancestral de Obazoa no muestreada`
- `población ancestral de Opisthokonta no muestreada`
- `población ancestral de Holozoa no muestreada`
- `población ancestral de Filozoa no muestreada`
- `población ancestral de Choanozoa sensu stricto no muestreada`
- `organismo perforador del Grupo Chuar no identificado`
- `holozoo fósil de posición interna indeterminada`
- `endosimbionte metanógeno de Pelomyxa palustris no identificado con certeza`
- `cianobacteria ancestral del cromatóforo no muestreada`
- `donante bacteriano de SUF no identificado`
- `linaje hospedador eucariota ancestral de Archaeplastida no muestreado`
- `simbionte cianobacteriano ancestral no muestreado`

Estas etiquetas no son taxones formales. Se conservan literalmente en la prosa y en las tablas.

---

# 0. Convenciones probatorias y taxonómicas

## 0.1. Clases de evidencia

Un genoma ensamblado a partir de metagenomas (*metagenome-assembled genome*, MAG) reconstruye secuencias desde una comunidad y no constituye por sí mismo una observación de la célula, su morfología ni su fisiología en cultivo. [C-006; n/a]

Un cultivo axénico (*axenic culture*) contiene un solo organismo. Un cocultivo (*co-culture*) mantiene dos o más organismos juntos; un cultivo de enriquecimiento (*enrichment culture*) aumenta la proporción de un organismo sin garantizar que sea el único. [C-007; n/a]

En esta parte se distinguen cinco niveles: detección de secuencia; inferencia filogenética; reconstrucción metabólica; caracterización bioquímica de proteína recombinante; y observación en una célula identificada. Una ESP detectada en un MAG no recibe el mismo peso que una red filamentosa observada por criotomografía electrónica (*cryo-electron tomography*). [C-006–C-007; glosa documental]

## 0.2. Grupo corona, grupo tronco y grupo total

*Grupo corona* (*crown group*) designa aquí el último ancestro común de todos los representantes vivientes de un grupo y todos sus descendientes. [C-008; n/a]

*Grupo tronco* (*stem group*) reúne linajes extinguidos más próximos a ese grupo corona que a cualquier grupo corona viviente externo. [C-009; n/a]

*Grupo total* (*total group*) es la suma del grupo corona y su grupo tronco. [C-010; n/a]

Estas definiciones son relacionales. Un fósil no entra en un tallo por ser antiguo, y un linaje viviente no puede convertirse en troncal respecto de otro linaje viviente por conservar una combinación particular de rasgos. [C-008–C-010; glosa documental]

## 0.3. Registro de afirmaciones de la sección 0

---

> **Registro de afirmaciones:** [data/afirmaciones/00.csv](../data/afirmaciones/00.csv) (10 filas; 12 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---


---

# 1. Alcance del corpus integrado provisional

El corredor principal tratado es el tallo de Eukaryota entre FECA y LECA, Eukaryota, Amorphea, Obazoa, Opisthokonta, Holozoa, Filozoa y el nodo que reúne coanoflagelados y animales. Metazoa se mantiene como terminal sin desarrollar su topología interna.

La integración incorpora tratamientos propios de Amoebozoa, Apusomonadida, Breviatea, Holomycota, Ichthyosporea, Pluriformea, Corallochytrea y Filasterea. También incorpora Asgardarchaeota y el componente alfa-proteobacteriano como participantes de la eucariogénesis.

La sección 13 permanece pendiente. Por ello, este archivo no constituye todavía el corpus final solicitado.

## 1.1. Registro de afirmaciones de la sección 1

Esta sección delimita el alcance documental y no introduce afirmaciones científicas adicionales; no genera filas de registro.

# 2. El punto de partida: dos dominios o tres

## 2.1. Tres dominios, eocitos y dos dominios

### 2.1.1. Tres topologías que no deben fundirse

**Árbol de tres dominios** [C-011–C-012; S06 fig. 1]

```text
raíz del árbol celular no especificada
├─ Bacteria
├─ Archaea
└─ Eukaryota
```

En su formulación de 1990, Bacteria, Archaea y Eucarya fueron tratados como tres dominios primarios. [C-011; S06 título; fig. 1] La relación relevante para este documento es la monofilia de Archaea excluyendo a Eukaryota. [C-012; S06 fig. 1]

**Hipótesis del eocito** [C-013–C-015; S07 resumen; fig. 4]

```text
raíz del árbol celular no especificada
├─ Bacteria
└─ Archaea sensu inclusivo
   ├─ otros linajes arqueanos
   └─┬─ eocitos
     └─ Eukaryota
```

Lake et al. distinguieron cuatro patrones ultraestructurales ribosómicos y recuperaron una relación estrecha entre los eocitos termoacidófilos examinados y los eucariotas. [C-013–C-014; S07 resumen; figs. 1–4] La consecuencia cladística es que el uso de Archaea que excluye Eukaryota pasa a ser parafilético. [C-015; S08 fig. 1; S14 tesis general]

**Árbol de dos dominios con Asgardarchaeota** [C-037–C-038; S10 figs. 1–3; S25 fig. 1; S26 fig. 3]

```text
raíz del árbol celular no especificada
├─ Bacteria
└─ Archaea sensu inclusivo
   └─ Asgardarchaeota [F] ⚠
      └─ Eukaryota
```

Las filogenómicas recientes recuperadas sitúan Eukaryota dentro de Archaea y, más concretamente, dentro de Asgardarchaeota. [C-037; S09 tesis general; S10 figs. 1–3; S25 fig. 1; S26 fig. 3] El punto exacto de inserción dentro de Asgardarchaeota sigue sin resolverse. [C-038; S10 fig. 3; S25 fig. 1; S26 fig. 3]

### 2.1.2. Por qué el modelo cambia el árbol

Cox et al. analizaron 53 genes y separaron dos problemas: heterogeneidad composicional entre linajes (*compositional heterogeneity*) y heterogeneidad entre sitios (*site heterogeneity*). [C-016; S08 resumen; Methods] Su matriz combinada de rRNA incluyó 40 taxones y 1.048 caracteres. [C-017; S08 Methods: Ribosomal RNA analyses]

Con GTR homogéneo, esa matriz produjo tres dominios; con NDCH y dos vectores de composición, produjo la topología del eocito. [C-018–C-019; S08 Results; fig. 1] En proteínas se aplicaron modelos CAT y CAT-GTR. [C-020; S08 Methods: Protein analyses] La comparación demuestra que el modelo puede cambiar la topología sin cambiar el problema biológico estudiado. [C-021; S08 Results; Discussion]

Williams et al. hicieron una comparación cuantitativa adicional. La tabla resume resultados sin convertir probabilidad posterior (*posterior probability*, PP), prueba AU y log-verosimilitud a una escala común. Los modelos sitio-homogéneos (*site-homogeneous*) y sitio-heterogéneos (*site-heterogeneous*) se mantienen diferenciados.

| estudio y matriz | modelo o prueba | resultado publicado | soporte transcrito | interpretación limitada | filas |
| --- | --- | --- | --- | --- | --- |
| Williams et al. 2020; matriz original de 35 genes | LG+G4+F | dos dominios tuvo mejor log-verosimilitud que tres dominios | −684701.2 frente a −684716.1 | La diferencia de ajuste no equivale por sí sola a rechazo del árbol alternativo. | C-022–C-023 |
| Williams et al. 2020; misma matriz | prueba AU bajo LG+G4+F | ninguna topología fue rechazada | 0.771 frente a 0.229 | El modelo homogéneo dejó una diferencia no decisiva. | C-024 |
| Williams et al. 2020; misma matriz | LG+C60+G4+F | rechazo de tres dominios | AU = 0.036 | Una mezcla de perfiles cambió el resultado de la prueba. | C-025 |
| Williams et al. 2020 | CAT+GTR+G4 | dos dominios | apoyo posterior máximo | El resultado depende de un modelo sitio-heterogéneo. | C-026 |
| Williams et al. 2020 | CAT con recodificación SR4 | dos dominios | PP = 0.98 | La recodificación de aminoácidos (*amino-acid recoding*) fue una prueba contra sesgo composicional. | C-027 |
| Williams et al. 2020; matrices ampliadas | 21 proteínas universales; 43 arqueano-eucariotas; 125 genomas | Eukaryota dentro de Asgard | máximo para la asociación con Heimdallarchaeia; LC3 PP = 0.95 | La división asgard concreta fue modificada por estudios posteriores. | C-028–C-030 |

[C-022–C-030; S10 tabla 1; figs. 1–3; material suplementario]

### 2.1.3. Una oposición publicada al resultado asgard

Da Cunha et al. separaron 36 proteínas universales en 11 «Woese proteins» y 25 «eocyte proteins», con 3.499 y 4.869 posiciones respectivamente. [C-031–C-032; S11 Results; figs. 1–2] Después de retirar secuencias rápidas, el conjunto de 11 proteínas recuperó monofilia arqueana con bootstrap de 100 %. [C-033; S11 fig. 1]

Los árboles individuales, sin embargo, no distribuyeron el apoyo de manera uniforme: la relación Eukaryota–Lokiarchaeota quedó por debajo de 70 % en la mayoría, con SecY en 84 % y EF2 en 100 %. [C-034; S11 Results; Supplementary figs.] La retirada de una secuencia EF2 alteró esa relación. [C-035; S11 Results; fig. 3]

Spang et al. publicaron una respuesta que cuestionó la selección de proteínas, el tratamiento de los datos y la interpretación, y volvió a recuperar a Asgard como los parientes procariotas más próximos de Eukaryota. [C-036; S12 tesis general; figs. 1–3] El episodio muestra una discrepancia en datos seleccionados y modelado, no dos observaciones celulares incompatibles.

### 2.1.4. Consecuencia nomenclatural

Bajo el árbol de dos dominios, «Archaea» usado para designar solo arqueas sin eucariotas es parafilético. [C-039; S14 tesis general] Fournier y Poole propusieron asumir esa consecuencia en una clasificación cladística. [C-040; S14 tesis general]

La literatura filogenómica, sin embargo, conserva habitualmente los nombres Archaea y Eukaryota mientras representa a Eukaryota dentro de Archaea. [C-041; S10; S25; S26] Esta práctica es convencional: no convierte dos topologías incompatibles en una sola ni resuelve por sí misma qué rango o código debe recibir cada nombre.

### 2.1.5. La posición neomurana

Cavalier-Smith y Chao defendieron en 2020 una variante neomurana que deriva Neomura, es decir, arqueas y eucariotas en su terminología, de bacterias planctobacterianas. [C-042; S13 título; resumen] Se trata como posición minoritaria porque no fue recuperada por las filogenómicas de dos dominios examinadas.

`NO LOCALIZADO EN ESTA SESIÓN`: no se recuperó una defensa primaria independiente posterior a 2020 de esa variante. [C-043; BN-001]

## 2.2. Bacteria, Archaea y la divisoria lipídica

### 2.2.1. Química de membrana

| conjunto celular | estereoisómero del glicerol | cadenas hidrófobas | enlace principal | relación con el problema | filas |
| --- | --- | --- | --- | --- | --- |
| Archaea típica | glicerol-1-fosfato | isoprenoides | éter | Es la química esperable para el linaje hospedador arqueano no identificado por comparación con arqueas actuales. | C-044 |
| Bacteria típica | glicerol-3-fosfato | ácidos grasos | éster | Es la química predominante en bacterias. | C-045 |
| Eukaryota moderno | glicerol-3-fosfato | ácidos grasos | éster | La membrana eucariota se parece en este eje a la bacteriana, no a la arqueana típica. | C-046 |

[C-044–C-046; S15 introducción; fig. 1]

La discordancia entre un hospedador de afinidad arqueana y una membrana eucariota predominantemente bacteriana es la divisoria lipídica (*lipid divide*). [C-047; S15 introducción; Discussion] No es una prohibición química simple: bacterias FCB poseen potencial para sintetizar lípidos éter arqueanos, de modo que las rutas no se distribuyen absolutamente por dominio. [C-048–C-049; S15 Results; Discussion]

### 2.2.2. Membranas heteroquirales experimentales

Caforio et al. diseñaron *Escherichia coli* con hasta aproximadamente 30 % de lípidos de tipo arqueano. [C-050; S16 Results; figs. 2–4] Las células fueron viables durante el experimento. [C-051; S16 Results; figs. 3–5] Esto cuestiona una incompatibilidad absoluta, pero no identifica qué ocurrió en el tallo eucariota. [C-052; S16 Discussion]

Justice et al. obtuvieron una membrana mínima heteroquiral capaz de sostener crecimiento. [C-053; S17 Results; fig. 5] En ese sistema, la heteroquiralidad redujo aptitud, ralentizó crecimiento y elevó permeabilidad y fragilidad hipoosmótica. [C-054; S17 Results; fig. 5] Por tanto, «viable» y «funcionalmente equivalente» no son sinónimos. [C-055; S16 Discussion; S17 Discussion]

### 2.2.3. Soluciones propuestas y estado del problema

| propuesta | montaje mínimo | qué la apoya | qué no resuelve | estado | filas |
| --- | --- | --- | --- | --- | --- |
| reemplazo de la ruta arqueana por genes bacterianos | el linaje hospedador arqueano no identificado adquiere y fija enzimas bacterianas | afinidad bacteriana de rutas eucariotas; abundancia de genes bacterianos | donante, orden, selectividad y geometría de membrana | sin resolver | C-056 |
| intermedio heteroquiral | coexistencia transitoria de ambas quiralidades | viabilidad experimental de membranas mixtas | ocurrencia ancestral, duración y dirección del reemplazo | sin resolver | C-057 |
| hospedador con membrana no estereotípica | el linaje hospedador arqueano no identificado ya poseía mezcla o repertorio distinto | excepciones modernas a la distribución de rutas | composición real del hospedador no muestreado | sin resolver | C-058 |

[C-056–C-058; S15, S16, S17]

No existe una reconstrucción consensuada del orden molecular de la transición. [C-059; S15, S16, S17] Los experimentos acotan lo químicamente posible y algunos costes, pero no seleccionan una historia única.

## 2.3. Naturaleza quimérica del genoma eucariota

Rivera et al. distinguieron una tendencia: genes informacionales con afinidad principalmente arqueana y genes operacionales con afinidad principalmente bacteriana. [C-060; S18 resumen; figs. 1–3] La separación no es universal ni exhaustiva. [C-061; S18 Discussion; S20 Results]

Brueckner y Martin compararon 150 genomas eucariotas con 19.050.992 proteínas de 5.443 bacterias y 212 arqueas. [C-062; S20 Methods; Results] Dentro del subconjunto con afinidad procariótica identificable, atribuyeron 44 % a Archaea y 56 % a Bacteria; al excluir linajes plastidiales, la fracción bacteriana fue 53 %. [C-063–C-064; S20 Results; fig. 2]

Cotton y McInerney encontraron que los genes de afinidad arqueana examinados tendían a ser más esenciales, expresados y conectados que los de afinidad bacteriana. [C-065; S19 Results; figs. 1–3] Un recuento de genes y una medida de importancia funcional responden preguntas distintas. [C-066; S19 Discussion; S20 Discussion]

Un análisis mucho más reciente usó aproximadamente 75 millones de proteínas procarióticas de 47.545 genomas, incluidos 63 asgard, y aproximadamente 30 millones de secuencias de 993 especies eucariotas. [C-067; S21 Methods; Extended Data] Tobiasson et al. atribuyeron a Asgard una contribución dominante a numerosos sistemas funcionales conservados y concentraron la contribución alfa-proteobacteriana reconstruida en energía y ensamblaje Fe–S. [C-068–C-069; S21 Results; figs. 1–4]

Las cifras no son promediables: cambian el universo de genes, el criterio de origen, la unidad funcional y el denominador. [C-070; S19, S20, S21] La frase defendible no es un porcentaje único de «genoma arqueano» o «genoma bacteriano», sino una lista condicionada por método.

## 2.4. Asgardarchaeota como conjunto de actores

### 2.4.1. De Lokiarchaeota a una diversidad mucho mayor

Lokiarchaeota fue descrito desde MAG de sedimentos marinos. [C-071; S22 Methods; fig. 1] Sus ESP iniciales fueron inferidas por secuencia. [C-072; S22 Results; figs. 2–4]

En 2017, Asgard agrupaba Loki-, Thor-, Odin- y Heimdallarchaeota. [C-073; S23 fig. 1] El registro SeqCode consultado contiene 17 clases hijas y registra nombres alternativos o solapados como Wukongarchaeia y Sifarchaeia. [C-074–C-077; S50 lista de children; related names] Esa lista es nomenclatural, no una topología cerrada. [C-077; S50 notas]

Zhang et al. añadieron 223 MAG y propusieron 16 linajes nuevos a partir de 40 muestras y 11.878 MAG reconstruidos. [C-078–C-079; S26 resumen; Methods] Su colección principal reunió 411 genomas asgard y 14 eucariotas; solo dos genomas asgard procedían de linajes cultivados. [C-080–C-081; S26 Methods; fig. 3] La completitud media fue 85.3 % y la contaminación media 3.6 %. [C-082; S26 Results; Supplementary table] El predominio de MAG sigue siendo una propiedad central del terreno probatorio. [C-083; S26 Methods]

### 2.4.2. Divisiones nombradas y clase de evidencia localizada

En S37, la identificación de células afiliadas a Hodarchaeales usó hibridación fluorescente *in situ* amplificada por deposición catalizada del reportero (*catalysed reporter deposition–fluorescence in situ hybridization*, CARD-FISH) y microscopía; no procedió de cultivo. [C-098; S37 Methods]

El término sintrofía (*syntrophy*) se usa aquí para la dependencia documentada de *Promethearchaeum syntrophicum* respecto de socios que consumen H₂ o formiato. [C-084; C-090; S34 Results; S35 fisiología]

| clase o nombre relacionado | marca | evidencia celular localizada | ecología o metabolismo localizado | estado en esta sesión | filas |
| --- | --- | --- | --- | --- | --- |
| Asgardarchaeia | [F] | MAG | `NO LOCALIZADO EN ESTA SESIÓN` | nombre registrado; perfil específico pendiente | C-074–C-077; C-148 |
| Atabeyarchaeia | [F] | MAG | `NO LOCALIZADO EN ESTA SESIÓN` | nombre registrado; perfil específico pendiente | C-074–C-077; C-148 |
| Baldrarchaeia | [F] | MAG | `NO LOCALIZADO EN ESTA SESIÓN` | nombre registrado; perfil específico pendiente | C-074–C-077; C-148 |
| Borrarchaeia | [F] | MAG | `NO LOCALIZADO EN ESTA SESIÓN` | nombre registrado; perfil específico pendiente | C-074–C-077; C-148 |
| Freyarchaeia | [F] | MAG | `NO LOCALIZADO EN ESTA SESIÓN` | nombre registrado; perfil específico pendiente | C-074–C-077; C-148 |
| Heimdallarchaeia | [F] ⚠ | MAG; observación CARD-FISH para Hodarchaeales afiliados | nichos microóxicos; potencial de respiración de O₂, hemo, ROS e hidrogenasas | fisiología inferida; sin aislamiento axénico | C-096–C-098; C-104; C-108–C-109 |
| Hermodarchaeia | [F] | MAG | degradación potencial de alcanos y aromáticos | inferencia genómica | C-107 |
| Hodarchaeia | [F] ⚠ | MAG; células afiliadas observadas por CARD-FISH | temperatura óptima inferida; metabolismo reconstruido | posición hermana de Eukaryota disputada | C-096–C-098; C-111–C-116; C-122 |
| Jordiarchaeia | [F] | MAG | `NO LOCALIZADO EN ESTA SESIÓN` | nombre registrado; perfil específico pendiente | C-074–C-077; C-148 |
| Kariarchaeia | [F] | MAG | `NO LOCALIZADO EN ESTA SESIÓN` | tamaño genómico mediano publicado; perfil específico pendiente | C-074–C-077; C-114; C-148 |
| Lokiarchaeia | [F] | MAG; enriquecimiento de *Lokiarchaeum ossiferum* | sedimentos; fisiología completa no localizada | observación celular directa disponible para un enriquecimiento | C-071–C-072; C-093–C-095 |
| Njordarchaeia | [F] ⚠ | MAG | `NO LOCALIZADO EN ESTA SESIÓN` | algunos MAG cuestionados por quimerismo | C-112; C-114; C-121 |
| Odinarchaeia | [F] | MAG; OdinTubulin recombinante | `NO LOCALIZADO EN ESTA SESIÓN` | función de tubulina nativa no localizada | C-129–C-130 |
| Promethearchaeia | [F] | cocultivo puro de *Promethearchaeum syntrophicum* | catabolismo de aminoácidos y péptidos en sintrofía obligada | única descripción taxonómica cultivada localizada con ese rango | C-084–C-092; C-149 |
| Ranarchaeia | [F] | MAG | `NO LOCALIZADO EN ESTA SESIÓN` | nombre registrado; perfil específico pendiente | C-074–C-077; C-148 |
| Shennonarchaeia | [F] | MAG | `NO LOCALIZADO EN ESTA SESIÓN` | nombre registrado; perfil específico pendiente | C-074–C-077; C-148 |
| Thorarchaeia | [F] | MAG | acetogénesis y reducción de azufre reconstruidas en sedimentos | sin cultivo localizado | C-102 |
| Sifarchaeia | ≈ [F] | dos MAG en la fuente primaria localizada | polisacáridos y metilotrofia anaerobia | relación nomenclatural con la lista principal dependiente de circunscripción | C-076; C-106 |
| Wukongarchaeia | ≈ [F] | MAG | `NO LOCALIZADO EN ESTA SESIÓN` | nombre alternativo o relacionado en el registro consultado | C-076–C-077 |

### 2.4.3. Ecologías y metabolismos documentados

Thorarchaeota fue reconstruido desde sedimentos con rutas de acetogénesis y reducción de azufre. [C-102; S28 resumen; figs. 2–4] Helarchaeota fue propuesto como participante en oxidación anaerobia de hidrocarburos. [C-103; S29 resumen; figs. 2–4]

Heimdallarchaeia de un nicho lacustre iluminado y microóxico presentó potencial de mixotrofia (*mixotrophy*) y rodopsinas. [C-104; S30 resumen; figs. 1–5] Gerdarchaeota y otros Asgard mostraron genes y transcritos asociados con degradación de materia orgánica. [C-105; S31 resumen; figs. 2–5]

Dos MAG de Sifarchaeota codificaron rutas de degradación de polisacáridos y metilotrofia anaerobia. [C-106; S32 resumen; figs. 2–4] Hermodarchaeota fue descrito con potencial de degradación de alcanos y aromáticos; «potencial» conserva la modalidad epistémica del trabajo. [C-107; S33 título; Results]

Appler et al. analizaron 404 MAG, incluidos 136 Heimdallarchaeia nuevos, e identificaron genes para complejo IV, hemo, detoxificación de especies reactivas e hidrogenasas. [C-108–C-109; S27 resumen; Results] En conjunto, Asgard ocupa ambientes anóxicos, microóxicos, iluminados y costeros con oxígeno variable. [C-110; S27, S28, S29, S30, S31, S32, S33] No existe una ecología única que pueda asignarse al clado completo.

## 2.5. Cultivos y observaciones celulares directas

### 2.5.1. *Promethearchaeum syntrophicum*

La publicación inicial usó *Candidatus Prometheoarchaeum syntrophicum*; la descripción taxonómica de 2024 adoptó *Promethearchaeum syntrophicum*. [C-149; S34 título; S35 título] No es una mera variante tipográfica.

El organismo se mantiene en cocultivo puro con un socio consumidor de H₂ o formiato y no en cultivo axénico independiente. [C-084; S35 descripción] Sus células midieron 300–750 nm. [C-085; S35 descripción morfológica] Creció entre 4 °C y 30 °C, con óptimo de 20 °C. [C-086; S35 fisiología]

Un crecimiento completo necesitó aproximadamente tres meses y alcanzó alrededor de 6.7 × 10^6 copias de 16S rRNA ml−1 bajo las condiciones descritas. [C-087–C-088; S35 fisiología; sin localizar] El cromosoma publicado mide 4.32 Mb y posee 31.1 % GC. [C-089; S35 Genome characteristics]

El catabolismo de aminoácidos y péptidos depende de socios que retiran hidrógeno o formiato. [C-090; S34 Results; S35 fisiología] Las protrusiones se observaron por microscopía. [C-091; S34 figs. 2–3] El modelo E3 extrapola desde esas observaciones; el proceso histórico no fue observado. [C-092; S34 Discussion; fig. 5]

### 2.5.2. *Lokiarchaeum ossiferum*

*Lokiarchaeum ossiferum* procede de un enriquecimiento, no de un cultivo axénico. [C-093; S36 Methods] La criotomografía electrónica mostró protrusiones ramificadas y filamentos helicoidales de doble hebra compatibles con actina arqueana. [C-094–C-095; S36 figs. 1–4]

### 2.5.3. Hodarchaeales observados sin cultivo

En sedimentos de Aarhus Bay, células afiliadas a Hodarchaeales representaron 0.1 % de las lecturas relativas de rRNA examinadas. [C-096; S37 resumen; Results] Las células marcadas midieron en promedio 3 µm, con rango de 1.5–5.2 µm. [C-097; S37 resumen; fig. 2] La identificación usó CARD-FISH y microscopía in situ, no cultivo. [C-098; S37 Methods]

### 2.5.4. *Nerearchaeum marumarumayae*

El enriquecimiento de *Nerearchaeum marumarumayae* alcanzó 89 % y permaneció asociado con *Stromatodesulfovibrio nilemahensis*. [C-099–C-100; S38 resumen; fig. 1] El genoma indicó potencial para producir H₂, acetato, formiato y sulfito. [C-101; S38 Results] La fuente no autoriza llamarlo cultivo puro ni convertir todos esos potenciales en flujos medidos.

## 2.6. Posición interna de Eukaryota dentro de Asgard

### 2.6.1. Hipótesis Hodarchaeales–Eukaryota

La matriz NM54 de Eme et al. tuvo 54 proteínas no ribosómicas, 313 taxones arqueanos y 13.513 posiciones. [C-111; S25 Methods] En datos sin filtrar, Eukaryota se asoció con Njordarchaeales; al retirar sitios rápidos, la asociación pasó a Hodarchaeales. [C-112; S25 Results; Extended Data]

Los análisis principales CAT+GTR y recodificados recuperaron Hodarchaeales como grupo hermano de Eukaryota. [C-113; S25 fig. 1] El mismo trabajo publicó tamaños genómicos medianos de 2.4, 2.7, 3.4, 3.7 y 5.1 Mb para Njord-, Kari-, Gerd-, Heimdall- y Hodarchaeales. [C-114; S25 fig. 3]

La reconstrucción ancestral produjo 4.053 familias proteicas para el ancestro de Hodarchaeales y 3.134 para el ancestro asgard considerado. [C-115; S25 Results; fig. 3] La temperatura óptima mediana de Hodarchaeales fue inferida en 36.7 °C. [C-116; S25 Results; fig. 4] Ninguna de esas magnitudes es una medición en un Hodarchaeales cultivado.

### 2.6.2. Hipótesis de origen más profundo fuera de Heimdallarchaeia

La matriz de 97 proteínas de Zhang et al. reunió 97 proteínas, 411 Asgard, 14 eucariotas y 20.067 posiciones. [C-117; S26 Methods; fig. 3] El análisis SR4-CAT+GTR produjo PP = 1; la matriz de 150 proteínas produjo PP = 0.8 y NM57 PP = 1 para posiciones fuera de Heimdallarchaeia. [C-118–C-119; S26 fig. 3; Extended Data]

La topología principal situó Eukaryota dentro de Asgardarchaeota pero como hermana de Heimdallarchaeia, no dentro de ella. [C-120; S26 fig. 3] Además, algunos MAG de Njordarchaeota contenían 22–51 % de fracciones afiliadas a TACK, lo que cuestionó su uso sin depuración. [C-121; S26 Results; Extended Data]

Ambos estudios sostienen dos dominios; discrepan en el nodo interno. [C-122; S25 fig. 1; S26 fig. 3] `linaje asgard más próximo a Eukaryota no resuelto` es, por tanto, la etiqueta correcta en esta fase.

## 2.7. Proteínas de firma eucariota: detección y función

Los genomas asgard codifican homólogos de actina, profilina, gelsolina, ESCRT, ubiquitina, GTPasas pequeñas y tubulina. [C-123; S22, S23, S24] La tabla separa la clase de evidencia, porque una secuencia con buen alineamiento no produce por sí sola un filamento, una vesícula ni un tráfico intracelular.

| sistema | detección por secuencia | caracterización funcional localizada | observación en célula asgard nativa | límite | filas |
| --- | --- | --- | --- | --- | --- |
| actina | sí | estructuras y polimerización caracterizadas en trabajos complementarios | sí, red filamentosa en *L. ossiferum* | la función celular completa de cada paralogo no está resuelta | C-123–C-124 |
| profilina | sí | regulación de actina heteróloga in vitro | no localizada | ensayo recombinante, no fenotipo nativo | C-125 |
| gelsolina/cofilina | sí | unión, corte, tapado, recocido y agrupamiento dependientes de Ca²⁺ según proteína | no localizada | funciones distribuidas entre proteínas recombinantes | C-126 |
| ESCRT-III/Vps4 | sí | ensamblaje, remodelado y desensamblaje bioquímicos | no localizada en esta sesión | función fisiológica concreta no observada en una célula asgard | C-127 |
| ubiquitina–ESCRT-I/II/III | sí | componentes y conjugación caracterizados estructural y bioquímicamente | no localizada | homología de maquinaria no equivale a un endosoma eucariota | C-128 |
| OdinTubulin | sí | protofilamentos, anillos y dinámica in vitro | `NO LOCALIZADO EN ESTA SESIÓN` | Odinarchaeota no cultivado | C-129–C-130 |
| GTPasas pequeñas, roadblock y TRAPPC3 | sí | pliegues, dímeros y propiedades bioquímicas eucariota-semejantes | `NO LOCALIZADO EN ESTA SESIÓN` | no se demostró tráfico vesicular nativo | C-131–C-132 |

La actina de *Lokiarchaeum ossiferum* cuenta con evidencia nativa. [C-124; S36] Profilina, gelsolina, tubulina, ESCRT y GTPasas cuentan con combinaciones distintas de secuencia, estructura y bioquímica recombinante. [C-125–C-132; S39, S40, S41, S42, S43, S44] Colapsar esas clases produciría una certeza que los experimentos no contienen. [C-133; S36; S39, S40, S41, S42, S43, S44]

## 2.8. El simbionte alfa-proteobacteriano

### 2.8.1. Lo ampliamente aceptado

La comparación del genoma de *Rickettsia prowazekii* con sistemas mitocondriales fue una línea histórica de apoyo a la afinidad alfa-proteobacteriana. [C-134; S45 resumen] La ascendencia alfa-proteobacteriana de la mitocondria tiene consenso amplio. [C-135; S45, S46, S47, S48]

La etiqueta `simbionte alfaproteobacteriano ancestral no muestreado` evita identificar al ancestro con una especie o familia viviente. [C-147; n/a]

### 2.8.2. El grupo vivo más próximo no está resuelto

| estudio | muestreo o modelo destacado | topología | qué excluye o no excluye | filas |
| --- | --- | --- | --- | --- |
| Martijn et al. 2018 | doce clados alfa divergentes y un linaje hermano; controles de ramas y composición | mitocondrias hermanas de alfa-proteobacterias muestreadas | no identifica una familia alfa viviente como hermana | C-136–C-137 |
| Fan et al. 2020 | muestreo taxonómico sistemático y retirada de sitios | mitocondrias dentro de Alpha IIb | contradice una posición completamente externa | C-138–C-139 |
| Muñoz-Gómez et al. 2022 | 108 proteínas; MAM60+GFmix | mitocondrias hermanas de alfa-proteobacterias conocidas | contradice Alpha IIb como ubicación estable bajo ese modelo | C-140–C-142 |
| Geiger et al. 2023 | triangulación de rasgos metabólicos | Iodidimonadales como mejor candidato funcional | no demuestra grupo hermano filogenético | C-143–C-144 |

Martijn et al. recuperaron una divergencia anterior a los grupos alfa muestreados. [C-136–C-137; S46 fig. 1] Fan et al. recuperaron inserción dentro de Alpha IIb. [C-138–C-139; S47 figs. 1–4] Muñoz-Gómez et al., con 108 proteínas y MAM60+GFmix, volvieron a recuperar una posición hermana de las alfa-proteobacterias conocidas. [C-140–C-142; S48 resumen; fig. 2]

Geiger et al. identificaron a Iodidimonadales como candidato funcional por combinación metabólica. [C-143; S49 Results] Esa semejanza no es una prueba de hermandad filogenética. [C-144; S49 Discussion]

Los trabajos discrepan sobre una inserción interna o externa respecto de los grupos alfa vivientes muestreados. [C-145; S46, S47, S48] No existe una familia viviente única aceptada como el pariente más próximo. [C-146; S46, S47, S48, S49] La etiqueta estable es `linaje alfaproteobacteriano más próximo a la mitocondria no resuelto`.

## 2.9. Qué no se sabe en esta parte

1. La posición interna exacta de Eukaryota dentro de Asgardarchaeota permanece sin resolver. [C-038; C-122]
2. La composición de membrana del linaje hospedador arqueano no identificado no puede observarse directamente. [C-058–C-059]
3. El orden histórico de reemplazo, mezcla o retención de rutas lipídicas no está resuelto. [C-056–C-059]
4. La mayor parte de las divisiones asgard solo posee MAG, por lo que su morfología y fisiología no están medidas en aislamiento. [C-083; C-148]
5. La función nativa de OdinTubulin y de las GTPasas pequeñas asgard no fue localizada. [C-130; C-132]
6. La familia alfa-proteobacteriana viviente más próxima a la mitocondria no está resuelta. [C-145–C-146]

---

## 2.10. Registro de afirmaciones de la sección 2

> **Registro de afirmaciones:** [data/afirmaciones/02.csv](../data/afirmaciones/02.csv) (139 filas; 12 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---

# 3. Eucariogénesis

## 3.1. Poblaciones ancestrales y extremos del intervalo

### 3.1.1. Etiquetas y alcance

Delaye atribuye a Forterre 1997 la propuesta del acrónimo LUCA. [C-153; S53 §History of LUCA; S54 título y texto]

El primer uso conjunto localizado en esta sesión de LUCA, LBCA, LACA, FECA y LECA aparece en Makarova et al. 2005. [C-154; S51 introducción y fig. 1]

No se localizó en esta sesión una fuente que establezca de forma inequívoca quién acuñó por primera vez cada una de las etiquetas LBCA, LACA y FECA. [C-155; BN-010]

LUCA designa la población ancestral reconstruida situada en el nodo del que divergen Bacteria y Archaea en el árbol celular adoptado por la fuente. [C-156; S55 introducción; fig. 1]

LBCA designa el último ancestro común de las bacterias vivientes incluidas en la reconstrucción. [C-157; S51 fig. 1; S101 título y métodos]

LACA designa el último ancestro común de las arqueas vivientes incluidas en la reconstrucción. [C-158; S51 fig. 1; S58 Methods]

O’Malley et al. distinguen conceptos abstracto, celular, poblacional y consorcial de LECA. [C-159; S52 secciones 2–5]

El concepto poblacional de LECA evita tratar una población ancestral recombinante como una única célula individual. [C-160; S52 §Population concept]

Richards et al. definen FECA como el primer descendiente del lado eucariota del último ancestro común entre Eukaryota y el linaje asgard hermano adoptado. [C-161; S56 líneas 318–321]

La definición de FECA no implica que FECA poseyera ya los rasgos celulares atribuidos a LECA. [C-162; S56 líneas 320–322]

Richards et al. denominan FMCA al primer descendiente del lado mitocondrial del último ancestro común entre el progenitor alfa-proteobacteriano y Eukaryota. [C-163; S56 líneas 319–321]

Si otros linajes aportaron material al tallo eucariota, pueden definirse FECAs adicionales para esos componentes sin convertirlos en taxones formales. [C-164; S56 línea 320]

LECA designa el último ancestro común de todos los eucariotas vivientes. [C-165; S52 tesis general; S56 líneas 309–330]

LECA no designa al primer eucariota. [C-166; S56 líneas 318–330; S57 p. 296]

El intervalo FECA–LECA carece de descendientes vivientes que se separaran en el tallo y hayan sido identificados como tales. [C-167; S56 líneas 321–324; S57 pp. 295–296]

La ausencia de representantes vivos identificados del tallo obliga a reconstruir su historia mediante distribuciones de genes, duplicaciones, pérdidas, estructuras y relojes. [C-168; S56 líneas 322–384; S57 pp. 295–300]

| etiqueta | término original | uso operacional en esta parte | filas |
| --- | --- | --- | --- |
| LUCA | last universal common ancestor | población ancestral del nodo Bacteria–Archaea | C-153; C-156 |
| LBCA | last bacterial common ancestor | último ancestro común de las bacterias vivientes muestreadas | C-157 |
| LACA | last archaeal common ancestor | último ancestro común de las arqueas vivientes bajo la circunscripción adoptada | C-158 |
| FECA | first eukaryotic common ancestor | primer descendiente del lado eucariota tras la divergencia del linaje asgard hermano | C-161–C-162 |
| nFECA | nuclear FECA | extremo nuclear del tallo usado por Kay et al. | C-169–C-170 |
| FMCA / mFECA | first mitochondrial common ancestor / mitochondrial FECA | primer descendiente del lado mitocondrial tras separarse de Alphaproteobacteria | C-163; C-169; C-171 |
| LECA | last eukaryotic common ancestor | último ancestro común de todos los eucariotas vivientes; no el primer eucariota | C-165–C-166 |

### 3.1.2. Modelo mínimo y pluralidad de contribuciones

Richards et al. denominan modelo two+ al consenso mínimo de al menos dos linajes procarióticos contribuyentes acompañado por cambios celulares sustantivos. [C-181; S56 líneas 311–317]

El modelo two+ incluye un componente de ascendencia arqueana, probablemente asgard, y un componente relacionado con Alphaproteobacteria. [C-182; S56 líneas 312–313]

Los modelos de eucariogénesis difieren en qué participante encapsuló a cuál y en el orden de adquisición de la complejidad celular. [C-183; S56 líneas 316–317]

El modelo two+ permite contribuciones adicionales por transferencia horizontal o asociaciones más prolongadas sin asumir que todas originaron orgánulos. [C-184; S56 líneas 313–315; 320; 333]

### 3.1.3. Cronología de los dos tallos en Kay et al. 2026

Kay et al. distinguen un FECA nuclear, nFECA, y un FECA mitocondrial, mFECA, para fechar los dos tallos contribuyentes. [C-169; S58 fig. 1; líneas 91–96]

Kay et al. estimaron nFECA entre 3.05 y 2.79 Ga. [C-170; S58 líneas 91–93; fig. 1]

Kay et al. estimaron mFECA entre 2.37 y 2.13 Ga. [C-171; S58 líneas 91–93; fig. 1]

Kay et al. estimaron la radiación de LECA entre 1.80 y 1.67 Ga. [C-172; S58 líneas 91–93; fig. 1]

Kay et al. estimaron una duración mediana aproximada de 1.1 Gyr para el tallo nuclear entre nFECA y LECA. [C-173; S58 línea 92]

Kay et al. estimaron una duración mediana aproximada de 0.6 Gyr para el tallo mitocondrial entre mFECA y LECA. [C-174; S58 línea 92]

El reloj de Kay et al. utilizó MCMCTree, 18 calibraciones fósiles y restricciones de edad relativa por cross-bracing. [C-175; S58 Methods: species tree dating; Supplementary Note 3]

Kay et al. analizaron 135 árboles génicos fechados, 95 de ascendencia arqueana y 40 de ascendencia bacteriana. [C-176; S58 líneas 94–96; fig. 1c]

En Kay et al., 19 de 40 familias bacterianas no dieron apoyo fuerte a un origen alfa-proteobacteriano. [C-177; S58 línea 95]

En Kay et al., 9 de 95 familias arqueanas no apoyaron un origen asgard. [C-178; S58 línea 95]

Kay et al. declaran que las identidades y edades de nFECA y mFECA cambiarían si se descubrieran genomas más próximos o cambiara la topología. [C-179; S58 línea 91]

El intervalo de 1.80–1.67 Ga para LECA de Kay et al. no constituye una estimación de consenso. [C-180; S58 líneas 187–190]

```text
tallo nuclear:       nFECA 3.05–2.79 Ga ────────────────┐
                                                           ├─ población LECA reconstruida 1.80–1.67 Ga
tallo mitocondrial:  mFECA 2.37–2.13 Ga ────────────────┘
                       adquisición e integración mitocondrial dentro del intervalo mFECA–LECA
```
Relaciones y cifras registradas: C-169–C-180. El esquema representa el marco temporal de S58 y no una cronología de consenso.

## 3.2. Reconstrucción de LECA

### 3.2.1. Qué clase de inferencia es

La reconstrucción de LECA infiere presencia ancestral a partir de distribución taxonómica, ortología, duplicación, pérdida y modelos de estado ancestral; no observa directamente una célula fósil. [C-185; S56 líneas 325–407; S60 tesis general]

La presencia de un rasgo en linajes situados a ambos lados de una raíz eucariota propuesta apoya su presencia en LECA solo si convergencia y transferencia son menos probables que herencia y pérdida. [C-186; n/a; derivación metodológica de S56 y S60]

Richards et al. sostienen que no existía en 2024 un conjunto cuantitativo consensuado que definiera todo el repertorio de familias génicas de LECA. [C-187; S56 líneas 383–384]

Bernabeu et al. construyeron tres conjuntos de 100 proteomas eucariotas cada uno, que abarcaron 185 especies y tuvieron un solapamiento proteico medio de 46%. [C-188; S59 Methods: dataset assembly; Extended Data fig. 1]

Tras filtros de calidad, Bernabeu et al. conservaron 256 proteomas para análisis de ortogrupos. [C-189; S59 Methods: quality filtering]

Bernabeu et al. reconstruyeron un promedio de 12.907 ortogrupos para LECA con el criterio relajado de presencia en tres supergrupos. [C-190; S59 Results: ancestral reconstruction; fig. 1]

Bernabeu et al. reconstruyeron un promedio de 7.751 ortogrupos para LECA con el criterio estricto de presencia en cinco supergrupos. [C-191; S59 Results: ancestral reconstruction; fig. 1]

La consistencia media de los ortogrupos de LECA reconstruidos por Bernabeu et al. fue 79% entre réplicas de muestreo. [C-192; S59 Results: robustness; Extended Data]

Bernabeu et al. estimaron que solo 3% de sus ortogrupos podría explicarse potencialmente por transferencia horizontal entre supergrupos. [C-193; S59 Results: HGT control]

Bernabeu et al. asignaron 5.317 términos KEGG Orthology al proteoma funcional consensuado de LECA. [C-194; S59 Results: functional reconstruction]

### 3.2.2. Núcleo y sistema endomembranoso

Bernabeu et al. describen su reconstrucción como una aproximación automatizada y no como un retrato celular exhaustivo. [C-195; S59 Discussion: limitations]

Neumann et al. analizaron 60 genomas eucariotas para reconstruir el complejo del poro nuclear. [C-196; S61 Methods; tabla 1]

Neumann et al. identificaron representantes de 19 nucleoporinas en todos los supergrupos considerados. [C-197; S61 Results; tabla 2]

La reconstrucción por parsimonia de Neumann et al. atribuyó entre 23 y 26 de 31 nucleoporinas a LECA. [C-198; S61 Results; fig. 4]

La envoltura nuclear y un complejo del poro nuclear complejo se atribuyen a LECA por distribución filogenética profunda y reconstrucción por parsimonia. [C-199; S61 Results; S56 fig. 2]

La presencia de retículo endoplasmático y Golgi en LECA se infiere de la distribución profunda de maquinaria de tráfico, Rabs y SNAREs. [C-200; S60 §Endomembrane system; S65, S66 tesis general]

Elias et al. reconstruyeron hasta 23 Rab GTPasas en LECA. [C-201; S65 Results; fig. 5]

Kloepper et al. analizaron más de 2.000 secuencias SNARE procedentes de 145 especies. [C-202; S66 Abstract; Methods]

Kloepper et al. propusieron que aproximadamente 20 subclases de SNARE estaban presentes en el cenancestro eucariota. [C-203; S66 Results; fig. 6]

La diversidad ancestral de Rabs y SNAREs implica que LECA ya poseía compartimentos de tráfico diferenciados, aunque no determina su morfología exacta. [C-204; S65 Discussion; S66 Discussion]

### 3.2.3. Citoesqueleto, motores y cilio

Actina y tubulina se atribuyen a LECA por su distribución paneucariota, sus paralogías antiguas y la conservación de motores y proteínas asociadas. [C-205; S62 pp. 513–520; S56 fig. 2]

Wickstead et al. reconstruyeron familias de kinesinas anteriores a la diversificación de los eucariotas vivientes. [C-206; S62 §Motor proteins; referencia primaria allí citada]

La presencia de un cilio eucariota con axonema, cuerpo basal y transporte intraflagelar se atribuye a LECA por la distribución de componentes ciliares e IFT. [C-207; S69 Results; S70 tesis general; S71 Results]

van Dam et al. recuperaron un conjunto completo de módulos IFT en la reconstrucción de LECA. [C-208; S71 Results; fig. 4]

van Dam et al. propusieron que IFT-A y BBSome se originaron por duplicación y divergencia desde un sistema semejante a IFT-B. [C-209; S71 Results; fig. 5]

### 3.2.4. Mitocondria, crestas y peroxisoma

La mitocondria de LECA conservaba un genoma propio y maquinaria de importación de proteínas, según la distribución universal de orgánulos mitocondriales derivados. [C-210; S56 fig. 2; S57 pp. 298–301; S60 §Mitochondria]

Muñoz-Gómez et al. propusieron que las crestas mitocondriales son homólogas a membranas intracitoplasmáticas alfa-proteobacterianas. [C-211; S72 Abstract; figs. 1–4]

Muñoz-Gómez et al. identificaron un sistema alphaMICOS restringido filogenéticamente a Alphaproteobacteria. [C-212; S72 Results; fig. 2]

La atribución de crestas a LECA se apoya en la universalidad ancestral de la mitocondria y en la homología propuesta de MICOS. [C-213; S72 Discussion; S56 fig. 2]

Jansen et al. compararon los 37 PEX conocidos en un conjunto representativo de eucariotas. [C-214; S73 Abstract; Methods]

Los componentes centrales de biogénesis peroxisomal presentan distribución profunda compatible con un peroxisoma en LECA. [C-215; S73 Results; S74 Results; S56 fig. 2]

Gabaldón et al. atribuyeron entre 39% y 58% de las proteínas peroxisomales analizadas a origen eucariota. [C-216; S74 Abstract; Results]

Gabaldón et al. atribuyeron entre 13% y 18% de las proteínas peroxisomales analizadas a origen alfa-proteobacteriano. [C-217; S74 Abstract; Results]

Eme et al. reconstruyeron una maquinaria compleja de división celular y mitosis en LECA. [C-218; S63 Results; figs. 2–4]

### 3.2.5. Mitosis, meiosis, intrones y espliceosoma

Eme et al. reconstruyeron componentes del complejo promotor de la anafase y regulación de ciclo celular anteriores a las divergencias eucariotas mayores. [C-219; S64 Results; figs. 2–5]

Bremer et al. 2023 reconstruyeron mitosis cerrada, ortomitosis y husos intranucleares como estado de LECA. [C-220; S75 Abstract; Results; S76 Abstract (corroboración de estado sincitial y mitosis cerrada)]

La reconstrucción de mitosis cerrada no implica que todos los descendientes conservaran ese estado. [C-221; S75 Discussion]

Ramesh et al. identificaron genes meióticos en Giardia y otros eucariotas que habían sido considerados asexuales. [C-222; S77 Results; tabla 1]

La distribución del kit meiótico apoya que meiosis o un proceso homólogo estaba presente en LECA. [C-223; S77 Discussion; S78 tesis general]

La presencia de genes meióticos no demuestra por sí sola el ciclo vital, la ploidía ni la frecuencia de apareamiento de LECA. [C-224; S77 Discussion; S78 Discussion]

Collins y Penny reconstruyeron una organización espliceosomal compleja en LECA. [C-225; S67 Results; Discussion]

Vosseberg et al. estimaron que 20–35% de los intrones de LECA estaban compartidos entre paralogos antiguos. [C-226; S68 Results; fig. 3]

El patrón de intrones compartidos entre paralogos indica que numerosos intrones espliceosomales precedieron a duplicaciones pre-LECA. [C-227; S68 Results; Discussion]

La envoltura nuclear, el poro y el espliceosoma se atribuyen a LECA por líneas de evidencia independientes que convergen, pero su orden de origen dentro del tallo permanece sin resolver. [C-228; S61; S67, S68; S91]

### 3.2.6. Fagocitosis y metabolismo: reconstrucciones incompatibles

Bremer et al. 2022 reconstruyeron a LECA como multinucleado y no fagocítico. [C-229; S79 Abstract; Results]

Bremer et al. 2022 analizaron 1.789 árboles génicos para reconstruir rasgos celulares de LECA. [C-230; S79 Methods; Results]

Bernabeu et al. 2026 reconstruyeron endocitosis, procesamiento de partículas extracelulares, fagosomas y lisosomas en LECA. [C-231; S59 Results: cellular reconstruction; fig. 3]

La reconstrucción no fagocítica de Bremer et al. y la reconstrucción de sistemas fagosomales de Bernabeu et al. son resultados incompatibles en la atribución de fagocitosis funcional a LECA. [C-232; S79; S59]

La presencia de genes anotados en endocitosis no equivale por sí sola a demostrar ingestión de presas completas por LECA. [C-233; n/a; limitación inferencial derivada de S59]

Bernabeu et al. reconstruyeron mitocondrias aerobias, metabolismo de hemo y agrupaciones hierro-azufre en LECA. [C-234; S59 Results: metabolic reconstruction; fig. 3]

Bernabeu et al. no reconstruyeron piruvato:ferredoxina oxidorreductasa, hidrogenasa [FeFe] ni biosíntesis de rodoquinona en su LECA consensuado. [C-235; S59 Results: energy metabolism]

Bernabeu et al. interpretaron su reconstrucción como más compatible con un LECA aerobio que con uno anaerobio productor de hidrógeno. [C-236; S59 Discussion]

La reconstrucción funcional de Bernabeu et al. no elimina la posibilidad de anaerobiosis facultativa o de pérdidas tempranas no recuperables. [C-237; S59 Discussion: limitations; S57 pp. 301–303]

### 3.2.7. Matriz de caracteres y método de inferencia

| carácter atribuido a LECA | método o criterio | resolución y límite | filas |
| --- | --- | --- | --- |
| mitocondria integrada con genoma e importación | distribución universal de orgánulos mitocondriales derivados y comparación de sistemas | presencia en LECA; orden de integración interno no resuelto | C-210 |
| crestas mitocondriales | homología de MICOS/alphaMICOS y universalidad mitocondrial ancestral | forma exacta y cronología de transformación no observadas | C-211–C-213 |
| envoltura nuclear y poro | 60 genomas; distribución de 19 nucleoporinas; parsimonia de 23–26/31 | geometría y orden dentro del tallo no resueltos | C-192–C-195 |
| retículo y Golgi | paralogía y distribución profunda de Rab y SNARE | morfología ancestral exacta no observable | C-196–C-204 |
| actina, tubulina y motores | distribución paneucariota y filogenias de familias | arquitectura celular intermedia no resuelta | C-205–C-206 |
| cilio, cuerpo basal e IFT | distribución de componentes, homología y duplicación de módulos IFT | estado funcional y ciclo de uso no observados | C-207–C-209 |
| peroxisoma | distribución comparada de PEX y origen mosaico del proteoma | contenido metabólico ancestral exacto no resuelto | C-214–C-218 |
| mitosis | filogenómica de maquinaria y reconstrucción de estados | mitosis cerrada ortomítica es una reconstrucción sensible a codificación | C-219–C-221 |
| meiosis o proceso homólogo | inventario de genes meióticos en linajes profundos | no resuelve ploidía, ciclo ni frecuencia de sexo | C-222–C-224 |
| intrones y espliceosoma | distribución de componentes y posiciones de intrones entre paralogos | orden de núcleo, intrones y duplicaciones parcialmente resuelto | C-225–C-228 |
| fagocitosis | estados ancestrales frente a ortogrupos funcionales | S79 y S59 producen inferencias incompatibles | C-229–C-233 |

## 3.3. Orden de los eventos: mitocondria y fagotrofia

Pittis y Gabaldón infirieron una adquisición tardía de la mitocondria a partir de distribuciones de longitudes de ramas de genes de distinta ascendencia procariótica. [C-238; S82 Abstract; Results; fig. 2]

El análisis de Pittis y Gabaldón comparó tiempos relativos de llegada de familias de genes arqueanas, alfa-proteobacterianas y bacterianas no alfa-proteobacterianas. [C-239; S82 Methods; fig. 1]

Martin et al. sostuvieron que la adquisición mitocondrial tardía inferida por Pittis y Gabaldón era un artefacto estadístico y de interpretación. [C-240; S83 título; Results; Discussion]

Vosseberg et al. usaron duplicaciones antiguas de familias génicas para ordenar expansiones funcionales respecto de la adquisición mitocondrial. [C-241; S80 Methods; figs. 1–4]

Vosseberg et al. favorecieron una posición mitocondria-intermedia, con duplicaciones tanto anteriores como posteriores al establecimiento del endosimbionte. [C-242; S80 Results; fig. 4]

Tria et al. analizaron 163.545 duplicaciones en 24.571 árboles génicos de 150 genomas eucariotas. [C-243; S81 Abstract; Methods]

Tria et al. identificaron 713 duplicaciones asignadas al tallo pre-LECA. [C-244; S81 Results; tabla suplementaria]

Tria et al. interpretaron la distribución de duplicaciones como apoyo a una adquisición mitocondrial temprana respecto de gran parte de la complejificación eucariota. [C-245; S81 Discussion]

Kay et al. fecharon duplicaciones asociadas con citoesqueleto, tráfico de membranas, endomembranas, fagocitosis y núcleo antes del límite inferido para la endosimbiosis mitocondrial. [C-246; S58 Results: cellular systems; figs. 3–5]

Kay et al. interpretaron su cronología como incompatible con una versión estricta de mitocondria-primero. [C-247; S58 Discussion; fig. 5]

La discrepancia entre mitocondria-temprana, mitocondria-intermedia y mitocondria-tardía se debe en parte a que los estudios datan familias, duplicaciones o ramas distintas y usan denominadores diferentes para “complejidad”. [C-248; S80, S81, S82, S83; S58]

La precedencia de fagotrofia respecto de la mitocondria no está resuelta. [C-249; S58, S59; S79; S84]

| posición | base inferencial | fuentes | filas |
| --- | --- | --- | --- |
| mitocondria tardía | distribuciones de longitudes de rama por ascendencia | S82 | C-238–C-240 |
| mitocondria intermedia | duplicaciones antiguas ordenadas respecto de la señal mitocondrial | S80 | C-241–C-242 |
| mitocondria temprana | gran conjunto de duplicaciones pre-LECA | S81 | C-243–C-245 |
| complejidad nuclear anterior a mFECA | reloj relajado de especies y duplicaciones | S58 | C-246–C-247 |
| fagotrofia antes de mitocondria | modelo autógeno y cronología de complejidad | S89; S58 | C-275–C-279 |
| mitocondria antes de fagotrofia moderna | modelos H₂, flujo inverso, E3 y reconstrucción no fagocítica | S85; S90, S82; S79 | C-250–C-257; C-281–C-294 |

## 3.4. Modelos rivales de eucariogénesis

### 3.4.1. Hipótesis del hidrógeno

La hipótesis del hidrógeno fue propuesta por Martin y Müller en 1998. [C-250; S85 título y tesis general]

La hipótesis del hidrógeno supone un linaje hospedador arqueano no identificado anaerobio, autotrófico y dependiente de H₂. [C-251; S85 modelo y fig. 1]

La hipótesis del hidrógeno supone un simbionte alfaproteobacteriano ancestral no muestreado facultativamente anaerobio. [C-252; S85 modelo y fig. 1]

En la hipótesis del hidrógeno, el simbionte libera H₂ y CO₂ durante heterotrofia anaerobia y el hospedador consume esos productos. [C-253; S85 modelo metabólico]

La hipótesis del hidrógeno requiere anoxia o condiciones con respiración limitada durante el montaje inicial. [C-254; S85 modelo; Discussion]

La hipótesis del hidrógeno sitúa la asociación metabólica antes de una célula eucariota fagocítica plenamente desarrollada. [C-255; S85 Discussion; S84 §Symbiogenic models]

La presencia universal de orgánulos mitocondriales derivados y la fisiología anaerobia distribuida entre eucariotas son compatibles con la hipótesis del hidrógeno. [C-256; S84 §Hydrogen hypothesis; S85 Discussion]

La ausencia de evidencia de metanogénesis en los asgard más próximos muestreados compromete la identidad metabólica original del hospedador de la hipótesis del hidrógeno. [C-257; S90 Introduction; S57 pp. 302–303]

```text
simbionte alfa facultativo
  heterotrofia anaerobia: H₂ + CO₂  ─────▶  hospedador arqueano metanógeno
  respiración cuando hay aceptores; integración posterior
```
Esquema separado del modelo; todas sus relaciones están registradas en las filas C-250–C-257. Fuente principal: S85.

### 3.4.2. Hipótesis sintrófica original y revisada

Moreira y López-García propusieron la hipótesis sintrófica original en 1998. [C-258; S86 título y modelo]

La hipótesis sintrófica original postuló una arquea metanógena, una delta-proteobacteria fermentativa y una alfa-proteobacteria metanótrofa como participantes. [C-259; S86 modelo; fig. 1]

En la hipótesis sintrófica original, la delta-proteobacteria aporta el citoplasma y la arquea metanógena aporta el núcleo. [C-260; S86 modelo]

López-García y Moreira reformularon la hipótesis sintrófica en 2020 para incorporar Asgardarchaeota. [C-261; S87 título; fig. 1]

La hipótesis sintrófica revisada supone un asgard productor de H₂ dentro o asociado estrechamente con una bacteria sulfatorreductora compleja. [C-262; S87 fig. 1; modelo]

La hipótesis sintrófica revisada incorpora una alfa-proteobacteria facultativamente aerobia y oxidante de sulfuro como progenitor mitocondrial. [C-263; S87 fig. 1; Discussion]

La hipótesis sintrófica revisada sitúa el montaje inicial en tapetes microbianos del Paleoproterozoico con gradientes de oxígeno, sulfuro e hidrógeno. [C-264; S87 fig. 2; §Ecological setting]

La hipótesis sintrófica revisada invierte el hospedador respecto de modelos con hospedador arqueano, al asignar el compartimento envolvente principal a una bacteria sulfatorreductora. [C-265; S87 modelo; S56 líneas 312–317]

La naturaleza quimérica del genoma eucariota y la existencia de consorcios metabólicos modernos son compatibles con sintrofía, pero no identifican el montaje tripartito específico. [C-266; S87 Discussion; S56 líneas 312–316]

```text
Asgard productor de H₂ ⇄ bacteria sulfatorreductora compleja
                       + alfa-proteobacteria oxidante de sulfuro
tapete microbiano con gradientes de O₂, H₂ y sulfuro
```
Esquema separado del modelo; todas sus relaciones están registradas en las filas C-258–C-266. Fuente principal: S86, S87.

### 3.4.3. Modelo *inside-out*

Baum y Baum propusieron el modelo inside-out en 2014. [C-267; S88 título y modelo]

El modelo inside-out supone una célula arqueana que produce protrusiones alrededor de simbiontes alfa-proteobacterianos extracelulares. [C-268; S88 fig. 1; §Model]

En el modelo inside-out, el cuerpo celular arqueano ancestral se vuelve homólogo del núcleo. [C-269; S88 fig. 1; §Nuclear compartment]

En el modelo inside-out, los espacios entre protrusiones fusionadas originan el retículo endoplasmático y el espacio perinuclear. [C-270; S88 fig. 1; §Endomembranes]

En el modelo inside-out, la fusión periférica de protrusiones genera la membrana plasmática eucariota. [C-271; S88 fig. 1]

El modelo inside-out permite una asociación mitocondrial externa inicial y no requiere fagocitosis previa. [C-272; S88 Discussion]

Las protrusiones observadas en asgard cultivados son compatibles con una premisa geométrica de inside-out, pero no demuestran la transición propuesta. [C-273; n/a; comparación documental de S88 con S34]

La continuidad topológica entre membrana nuclear externa, retículo y membrana plasmática predicha por inside-out difiere de una invaginación autógena hacia el interior. [C-274; S88 figs. 1–2; S96 modelo]

```text
cuerpo arqueano ancestral = futuro núcleo
        ╰─ protrusiones rodean ectosimbiontes alfa
             ╰─ fusión periférica = membrana plasmática
espacios interprotrusión = retículo y espacio perinuclear
```
Esquema separado del modelo; todas sus relaciones están registradas en las filas C-267–C-274. Fuente principal: S88.

### 3.4.4. Modelo autógeno fagotrófico

Cavalier-Smith formuló un modelo fagotrófico autógeno en el que citosqueleto, endomembranas, núcleo y fagocitosis preceden a la mitocondria. [C-275; S89 resumen; §§Origin of phagotrophy and mitochondria]

El modelo autógeno fagotrófico supone un protoeucariota capaz de engullir al progenitor mitocondrial. [C-276; S89 modelo; S84 §Autogenous models]

El modelo autógeno fagotrófico no requiere sintrofía de H₂ para iniciar la asociación mitocondrial. [C-277; S84 comparación de modelos]

La cronología de Kay et al. es compatible con partes de un hospedador celularmente complejo antes de la endosimbiosis mitocondrial. [C-278; S58 figs. 3–5]

La reconstrucción no fagocítica de Bremer et al. cuestiona la fagocitosis premitocondrial obligatoria. [C-279; S79 Results]

Las partes neomuranas y varios grupos taxonómicos del modelo de Cavalier-Smith no deben confundirse con la hipótesis más general de fagocitosis antes de mitocondria. [C-280; n/a; distinción documental basada en S89 y S84]

```text
protoeucariota con núcleo + endomembranas + citosqueleto + fagocitosis
        └─ fagocita y retiene progenitor mitocondrial
```
Esquema separado del modelo; todas sus relaciones están registradas en las filas C-275–C-280. Fuente principal: S89; S84.

### 3.4.5. Modelo de flujo inverso

Spang et al. propusieron el modelo de flujo inverso en 2019. [C-281; S90 título y modelo]

El modelo de flujo inverso supone un hospedador asgard organoheterótrofo que libera equivalentes reductores o H₂ hacia un socio bacteriano. [C-282; S90 fig. 5; Discussion]

La dirección del intercambio en flujo inverso es opuesta a la hipótesis del hidrógeno original. [C-283; S90 Discussion; S85 modelo]

El modelo de flujo inverso requiere proximidad física y una relación sintrófica anaerobia antes de la internalización. [C-284; S90 fig. 5; Discussion]

Las reconstrucciones de metabolismo organoheterótrofo en varios asgard respaldan la plausibilidad del flujo inverso. [C-285; S90 Results; fig. 3]

La identidad y fisiología del socio bacteriano del flujo inverso no están resueltas por los genomas asgard. [C-286; S90 Discussion]

```text
hospedador Asgard organoheterótrofo ── equivalentes reductores/H₂ ──▶ socio bacteriano
asociación anaerobia próxima ──▶ integración
```
Esquema separado del modelo; todas sus relaciones están registradas en las filas C-281–C-286. Fuente principal: S90.

### 3.4.6. Modelo E3

Imachi et al. propusieron el modelo de entrelazamiento, engullimiento y endogenización, E3, en 2020. [C-287; S34 Discussion; fig. 6]

E3 parte de una arquea asgard anaerobia, pequeña, de crecimiento lento y dependiente de socios sintróficos. [C-288; S34 Results; Discussion]

En E3, protrusiones del hospedador entrelazan físicamente a un socio bacteriano. [C-289; S34 fig. 6a–b]

En E3, el engullimiento se produce por extensión y fusión de protrusiones, no por una maquinaria fagocítica moderna preexistente. [C-290; S34 fig. 6c–d]

En E3, la endogenización convierte al socio bacteriano en endosimbionte mitocondrial. [C-291; S34 fig. 6e]

Promethearchaeum syntrophicum produjo protrusiones y creció en sintrofía en cultivo de enriquecimiento. [C-292; S34 Results; figs. 2–5]

Imachi et al. no observaron el engullimiento ni la endogenización postulados por E3. [C-293; S34 Discussion; fig. 6 legend]

E3 es compatible con una asociación metabólica previa y con una internalización sin fagocitosis moderna, pero no especifica por sí solo todos los orígenes del núcleo y endomembranas. [C-294; S34 Discussion; S57 pp. 300–303]

```text
Asgard sintrófico con protrusiones
  entrelazamiento ─▶ engullimiento por extensión/fusión ─▶ endogenización
  observado: protrusiones y sintrofía; propuesto: engullimiento y endogenización
```
Esquema separado del modelo; todas sus relaciones están registradas en las filas C-287–C-294. Fuente principal: S34.

### 3.4.7. Comparación del montaje inicial

| clave | modelo | participantes | intercambio y dirección | ambiente | geometría y orden | apoyo | compromiso principal | fila inicial |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H12 | hipótesis del hidrógeno | arquea metanógena; alfa facultativa | H₂ y CO₂: alfa→arquea | anoxia | asociación metabólica antes de fagocitosis | universalidad mitocondrial y anaerobiosis | asgard próximos no metanogénicos | C-250 |
| H13 | hipótesis sintrófica revisada | Asgard; bacteria sulfatorreductora; alfa oxidante de sulfuro | H₂ y compuestos de azufre entre socios | tapete con gradientes | montaje tripartito; hospedador bacteriano | quimerismo y analogías de consorcios | identidad del hospedador y topología discutidas | C-261 |
| H14 | modelo inside-out | cuerpo arqueano; ectosimbiontes alfa | intercambio no fijado por el modelo | no exclusivo | protrusiones y fusión exterior | topología celular y protrusiones compatibles | sin transición observada; oposición a invaginación | C-267 |
| H15 | modelo autógeno fagotrófico | protoeucariota fagotrófico; progenitor mitocondrial | no exige sintrofía inicial | variable | fagocitosis de la bacteria | cronología de complejidad pre-mFECA | reconstrucción no fagocítica de LECA | C-275 |
| H16 | modelo de flujo inverso | Asgard organoheterótrofo; socio bacteriano | equivalentes reductores: arquea→bacteria | anoxia | sintrofía antes de integración | metabolismo asgard reconstruido | socio bacteriano no identificado | C-281 |
| H17 | modelo E3 | Asgard sintrófico; socio bacteriano | metabolitos sintróficos; dirección específica variable | anoxia y proximidad | entrelazar, engullir, endogenizar | cultivo, sintrofía y protrusiones | dos etapas decisivas no observadas | C-287 |

## 3.5. Origen del núcleo como problema separado

El origen del núcleo y el origen de la célula eucariota completa son preguntas parcialmente separables. [C-295; n/a; distinción analítica apoyada por S88, S91, S92, S93, S94, S95, S96]

### 3.5.1. Invasión de intrones

Martin y Koonin propusieron en 2006 la hipótesis de invasión de intrones para la compartimentación núcleo–citosol. [C-296; S91 título y modelo]

La hipótesis de invasión de intrones supone que intrones de grupo II procedentes del endosimbionte bacteriano invadieron genes del hospedador. [C-297; S91 modelo; fig. 1]

La hipótesis de invasión de intrones propone que intrones de grupo II dieron origen a intrones espliceosomales y componentes de su maquinaria. [C-298; S91 modelo; Discussion]

La hipótesis de invasión de intrones supone que el empalme de pre-ARNm era más lento que la traducción. [C-299; S91 modelo cinético]

En la hipótesis de invasión de intrones, la envoltura nuclear separa transcripción y empalme de la traducción y reduce la síntesis de proteínas aberrantes. [C-300; S91 fig. 1; Discussion]

Los intrones compartidos entre paralogos pre-LECA son compatibles con una invasión temprana de intrones, pero no establecen que esa presión originara la envoltura nuclear. [C-301; S68; S91]

La hipótesis de invasión de intrones requiere que la adquisición mitocondrial preceda o coincida con la expansión de intrones que selecciona compartimentación. [C-302; S91 modelo]

Fuente o fuentes principales: S91; S68.

### 3.5.2. Origen viral

Bell propuso en 2001 una hipótesis viral para el origen del núcleo eucariota. [C-303; S92 título y modelo]

La hipótesis viral de Bell supone una infección persistente de un hospedador arqueano por un virus complejo de ADN. [C-304; S92 modelo]

La hipótesis viral atribuye al compartimento viral contribuciones a cromosomas lineales, separación de transcripción y traducción y procesamiento de ARNm. [C-305; S92 Discussion; S94 secciones 2–4]

Takemura propuso en 2001 una variante que vincula el origen nuclear con poxvirus. [C-306; S93 título y modelo]

Bell actualizó en 2020 la hipótesis viral usando comparaciones con virus gigantes de ADN. [C-307; S94 tesis general]

Takemura relacionó en 2020 medusavirus con una actualización de la hipótesis viral del núcleo. [C-308; S95 título; modelo]

Takemura declaró que el mecanismo de origen nuclear permanece desconocido y que la hipótesis viral es controvertida. [C-309; S95 Introduction; Conclusion]

Las semejanzas entre virus gigantes y eucariotas en polimerasas, histonas o procesamiento de ARNm no determinan la dirección de transferencia génica. [C-310; S94 Discussion; S95 Discussion]

No se ha observado un virus que se transforme en un núcleo hereditario ni un núcleo que se origine de novo durante una infección. [C-311; n/a; límite empírico de S92, S93, S94, S95]

Fuente o fuentes principales: S92, S93, S94, S95.

### 3.5.3. Invaginación autógena

Cavalier-Smith propuso en 1975 un origen autógeno de núcleo y endomembranas por invaginación de la membrana plasmática. [C-312; S96 título y modelo]

La hipótesis autógena de invaginación supone que membranas internas rodearon el material genético desde el interior de una célula ancestral. [C-313; S96 modelo]

La continuidad entre envoltura nuclear y retículo endoplasmático es compatible con una derivación común por remodelado de membranas. [C-314; S96; S99 tesis general]

La hipótesis autógena de invaginación no especifica por sí sola el origen de las nucleoporinas ni del espliceosoma. [C-315; n/a; comparación con S61 y S67]

La invaginación interna y la exteriorización inside-out asignan orientaciones topológicas opuestas al origen de la envoltura nuclear. [C-316; S88; S96]

Fuente o fuentes principales: S96.

### 3.5.4. Submodelo nuclear *inside-out*

El submodelo nuclear inside-out deriva la envoltura nuclear de la membrana del cuerpo celular arqueano ancestral y el retículo de espacios entre protrusiones. [C-317; S88 fig. 1; §Nucleus]

El submodelo nuclear inside-out predice que la inserción de poros durante interfase ocurre desde el lado citoplasmático por un mecanismo compatible con crecimiento hacia afuera. [C-318; S88 Predictions]

El submodelo nuclear inside-out es compatible con una contribución viral de genes individuales sin aceptar que el compartimento nuclear completo descienda de un virus. [C-319; S88; S94, S95]

El submodelo nuclear inside-out no requiere que intrones de grupo II sean la causa inicial de la envoltura, aunque puede incorporar una selección posterior por separación de empalme y traducción. [C-320; S88; S91]

Fuente o fuentes principales: S88.

### 3.5.5. Comparación de los modelos nucleares

| clave | modelo | supuesto central | mecanismo | apoyo principal | compromiso | filas |
| --- | --- | --- | --- | --- | --- | --- |
| H18 | invasión de intrones | intrones de grupo II del endosimbionte; empalme lento | separación de empalme y traducción | intrones pre-LECA | causalidad envoltura–intrones no demostrada | C-296–C-302 |
| H19 | origen viral | virus de ADN persistente | compartimento o genes nucleares | homologías con virus gigantes | dirección de HGT y transición no observada | C-303–C-311 |
| H20 | invaginación autógena | membrana ancestral remodelable | invaginación hacia el ADN | continuidad núcleo–retículo | no explica por sí sola poro ni espliceosoma | C-312–C-316 |
| H21 | núcleo inside-out | cuerpo asgard y protrusiones | cuerpo ancestral = núcleo; espacios = retículo | predicciones topológicas | geometría no observada y oposición a invaginación | C-317–C-320 |

## 3.6. Hipótesis del protocoatómero

Devos et al. propusieron la hipótesis del protocoatómero en 2004. [C-321; S97 título; Discussion]

Devos et al. compararon siete proteínas de vesículas recubiertas y del complejo del poro nuclear. [C-322; S97 Results; tabla 1]

Las proteínas comparadas por Devos et al. comparten combinaciones de β-propeller y α-solenoid. [C-323; S97 Results; figs. 1–3]

La hipótesis del protocoatómero propone que COPI, COPII, clatrina y el complejo del poro nuclear divergieron de un módulo ancestral de curvatura de membrana. [C-324; S97 Discussion; S98 tesis general]

Devos et al. consideraron convergencia y divergencia como explicaciones de la arquitectura compartida y favorecieron divergencia. [C-325; S97 Discussion]

La ausencia de similitud de secuencia detectable entre algunos componentes limita la resolución de relaciones internas del protocoatómero. [C-326; S97 Discussion; S98 §Evolution]

van Dam et al. relacionaron módulos IFT y BBSome con una ascendencia coatómero-like. [C-327; S71 título; Results]

La expansión por duplicación y divergencia de módulos de membrana puede explicar diversidad de compartimentos sin requerir un origen independiente para cada cubierta. [C-328; S99 secciones 2–4; S97 Discussion]

La hipótesis del protocoatómero no especifica si la mitocondria se adquirió antes o después de la expansión de endomembranas. [C-329; n/a; alcance de S97, S98, S99]

La hipótesis del protocoatómero es compatible con más de una geometría de origen nuclear porque establece homología molecular sin fijar orientación de membranas. [C-330; S97, S98, S99]

```text
módulo ancestral β-propeller + α-solenoid
      ├─ COPI / COPII
      ├─ clatrina y adaptadores
      ├─ complejo del poro nuclear
      └─ módulos relacionados de IFT / BBSome
```
Relaciones registradas: C-321–C-330. El diagrama expresa una hipótesis de homología y duplicación, no el orden completo de eucariogénesis.

## 3.7. Matriz de compatibilidad

Las categorías son `mutuamente excluyentes`, `parcialmente compatibles` y `compatibles`. La comparación se limita a la parte explícita de cada modelo; no convierte compatibilidad parcial en una síntesis histórica única. [C-400]

| modelo A | modelo B | relación | punto exacto | observación que los distinguiría | fila |
| --- | --- | --- | --- | --- | --- |
| H12 hipótesis del hidrógeno | H13 hipótesis sintrófica revisada | parcialmente compatibles | Comparten sintrofía anaerobia, pero H12 usa hospedador arqueano y flujo alfa→arquea; H13 revisada usa hospedador bacteriano y montaje tripartito. | Una filogenia celular que identificara inequívocamente qué membrana ancestral envolvió a las demás y una reconstrucción metabólica del hospedador distinguirían los montajes. | C-331 |
| H12 hipótesis del hidrógeno | H14 modelo inside-out | parcialmente compatibles | H12 especifica metabolismo; H14 especifica geometría. Chocan solo si H12 exige internalización directa incompatible con ectosimbiosis prolongada. | Homologías de orientación de membranas y evidencia de asociación alfa extracelular anterior a la internalización discriminarían la geometría sin alterar el flujo de H₂. | C-332 |
| H12 hipótesis del hidrógeno | H15 modelo autógeno fagotrófico | mutuamente excluyentes | H12 requiere mitocondria antes de fagocitosis compleja; H15 requiere fagocitosis y núcleo antes de mitocondria. | Una cronología robusta que coloque fagocitosis funcional antes o después de mFECA distinguiría el orden. | C-333 |
| H12 hipótesis del hidrógeno | H16 modelo de flujo inverso | parcialmente compatibles | Ambas usan sintrofía anaerobia y hospedador arqueano, pero postulan direcciones opuestas del flujo reductor. | La reconstrucción segura del metabolismo del hospedador y del simbionte ancestral distinguiría quién producía y quién consumía H₂ o equivalentes reductores. | C-334 |
| H12 hipótesis del hidrógeno | H17 modelo E3 | parcialmente compatibles | H12 aporta el intercambio metabólico; E3 aporta la geometría de internalización. Son compatibles si el socio productor de H₂ es el bacteriano entrelazado. | La identificación del metabolismo del socio entrelazado y del hospedador establecería si E3 puede implementar el flujo de H12. | C-335 |
| H12 hipótesis del hidrógeno | H18 hipótesis de invasión de intrones | compatibles | H12 explica la asociación mitocondrial y H18 una consecuencia nuclear posterior de intrones transferidos por el endosimbionte. | El orden intrones→envoltura puede evaluarse sin cambiar el montaje metabólico de H12. | C-336 |
| H12 hipótesis del hidrógeno | H19 hipótesis viral del núcleo | compatibles | H12 no excluye una contribución viral adicional al núcleo, siempre que el virus no sustituya al hospedador arqueano ni al endosimbionte. | Filogenias de genes nucleares podrían distinguir contribución viral parcial de origen completo del compartimento. | C-337 |
| H12 hipótesis del hidrógeno | H20 hipótesis autógena de invaginación nuclear | compatibles | H12 especifica metabolismo y H20 geometría nuclear autógena; pueden ocurrir en etapas distintas. | El orden relativo de invaginación nuclear e integración mitocondrial distinguiría variantes, no la compatibilidad básica. | C-338 |
| H12 hipótesis del hidrógeno | H21 submodelo nuclear inside-out | parcialmente compatibles | H12 y H21 comparten hospedador arqueano, pero H21 exige una topología exteriorizada que H12 no especifica. | La orientación homóloga de membranas del núcleo, retículo y plasma decidiría si el montaje H12 puede insertarse en H21. | C-339 |
| H12 hipótesis del hidrógeno | H22 hipótesis del protocoatómero | compatibles | H22 explica la ascendencia de maquinaria de membrana y no fija metabolismo ni orden mitocondrial. | La homología del protocoatómero puede probarse independientemente del flujo de H₂. | C-340 |
| H13 hipótesis sintrófica revisada | H14 modelo inside-out | parcialmente compatibles | H13 revisada asigna el hospedador envolvente a una bacteria sulfatorreductora; H14 asigna el cuerpo ancestral al asgard. | La procedencia de membranas nucleares, citoplasmáticas y plasmáticas distinguiría qué participante fue el compartimento envolvente. | C-341 |
| H13 hipótesis sintrófica revisada | H15 modelo autógeno fagotrófico | mutuamente excluyentes | H13 inicia con un consorcio procariótico y no con un protoeucariota fagocítico; H15 requiere fagocitosis premitocondrial. | Una fagocitosis funcional inequívocamente anterior a la asociación tripartita excluiría H13 en su forma estricta. | C-342 |
| H13 hipótesis sintrófica revisada | H16 modelo de flujo inverso | parcialmente compatibles | Ambas usan sintrofía y un asgard que puede producir equivalentes reductores, pero difieren en hospedador y número de socios. | La identidad del compartimento hospedador y la necesidad de una bacteria sulfatorreductora distinguirían los modelos. | C-343 |
| H13 hipótesis sintrófica revisada | H17 modelo E3 | parcialmente compatibles | E3 puede proporcionar un mecanismo de internalización dentro de un consorcio, pero H13 asigna el hospedador principal a una bacteria y E3 a Asgard. | La topología de membranas y el papel celular de la bacteria sulfatorreductora discriminarían la combinación. | C-344 |
| H13 hipótesis sintrófica revisada | H18 hipótesis de invasión de intrones | compatibles | La sintrofía revisada puede preceder a una invasión de intrones desde el progenitor mitocondrial. | El donante de intrones y su fecha relativa pueden evaluarse dentro del montaje H13. | C-345 |
| H13 hipótesis sintrófica revisada | H19 hipótesis viral del núcleo | compatibles | H13 no excluye aportes virales parciales durante o después de la integración. | La dirección de homologías virales no afecta por sí sola el montaje metabólico tripartito. | C-346 |
| H13 hipótesis sintrófica revisada | H20 hipótesis autógena de invaginación nuclear | compatibles | H13 especifica participantes y ecología; H20 puede explicar una invaginación nuclear posterior. | La procedencia bacteriana o arqueana de la membrana que se invagina distinguiría variantes internas. | C-347 |
| H13 hipótesis sintrófica revisada | H21 submodelo nuclear inside-out | mutuamente excluyentes | H13 revisada coloca al asgard dentro de un hospedador bacteriano; H21 requiere que el cuerpo asgard ancestral sea el núcleo y origen topológico central. | Una asignación inequívoca de la membrana nuclear ancestral a Asgard o a la bacteria resolvería el choque. | C-348 |
| H13 hipótesis sintrófica revisada | H22 hipótesis del protocoatómero | compatibles | La homología de coatómeros y poros puede evolucionar dentro de un montaje tripartito. | Las relaciones estructurales de H22 no fijan la identidad del hospedador de H13. | C-349 |
| H14 modelo inside-out | H15 modelo autógeno fagotrófico | parcialmente compatibles | Ambas permiten complejidad premitocondrial, pero H14 internaliza por protrusiones alrededor de ectosimbiontes y H15 por fagocitosis. | Evidencia del mecanismo de internalización y del estado de fagocitosis premitocondrial distinguiría las variantes. | C-350 |
| H14 modelo inside-out | H16 modelo de flujo inverso | compatibles | H16 especifica flujo metabólico arquea→bacteria y H14 puede alojar esa asociación como ectosimbiosis entre protrusiones. | La geometría y el metabolismo son predicciones independientes salvo que el flujo requiera una posición imposible. | C-351 |
| H14 modelo inside-out | H17 modelo E3 | parcialmente compatibles | Ambas usan protrusiones asgard y evitan fagocitosis moderna; H14 deriva citoplasma y retículo de blebs, E3 enfatiza entrelazamiento y engullimiento. | La homología de los espacios interprotrusión y el mecanismo de cierre de membranas distinguirían los modelos. | C-352 |
| H14 modelo inside-out | H18 hipótesis de invasión de intrones | compatibles | La geometría inside-out puede preceder o acompañar una presión posterior de intrones sobre compartimentación. | El orden de intrones y cierre de la envoltura distinguiría la variante causal. | C-353 |
| H14 modelo inside-out | H19 hipótesis viral del núcleo | parcialmente compatibles | Inside-out explica el compartimento celular; una contribución viral genética es compatible, pero un núcleo íntegramente viral sustituiría la homología del cuerpo arqueano. | La procedencia del compartimento frente a genes individuales separaría contribución parcial de origen viral completo. | C-354 |
| H14 modelo inside-out | H20 hipótesis autógena de invaginación nuclear | mutuamente excluyentes | H14 deriva núcleo y retículo por exteriorización; H20 por invaginación interior de la membrana ancestral. | La orientación topológica ancestral de membranas y la inserción de poros distinguirían las geometrías opuestas. | C-355 |
| H14 modelo inside-out | H21 submodelo nuclear inside-out | compatibles | H21 es el componente nuclear explícito de H14. | No requieren una observación distinta para compatibilidad; la evidencia que afecta H14 afecta H21. | C-356 |
| H14 modelo inside-out | H22 hipótesis del protocoatómero | compatibles | H22 aporta una maquinaria ancestral de curvatura que puede operar durante protrusión, fusión y formación de poros. | La homología molecular puede probarse independientemente de la orientación inside-out. | C-357 |
| H15 modelo autógeno fagotrófico | H16 modelo de flujo inverso | mutuamente excluyentes | H15 requiere protoeucariota fagocítico y mitocondria tardía; H16 inicia con sintrofía procariótica antes de fagocitosis. | La cronología de fagocitosis respecto de la asociación mitocondrial distinguiría los montajes estrictos. | C-358 |
| H15 modelo autógeno fagotrófico | H17 modelo E3 | mutuamente excluyentes | H15 internaliza por fagocitosis preexistente; E3 propone engullimiento por protrusiones sin maquinaria fagocítica moderna. | Una reconstrucción funcional de la maquinaria de fagocitosis anterior a la internalización distinguiría los mecanismos. | C-359 |
| H15 modelo autógeno fagotrófico | H18 hipótesis de invasión de intrones | parcialmente compatibles | Pueden combinarse solo si la invasión de intrones y su presión selectiva ocurren después de una mitocondria adquirida tardíamente; chocan si H18 origina el núcleo antes exigido por H15. | Fechar expansión de intrones frente al origen nuclear y a mFECA distinguiría el orden. | C-360 |
| H15 modelo autógeno fagotrófico | H19 hipótesis viral del núcleo | compatibles | Un protoeucariota fagocítico puede recibir aportes virales al núcleo antes o después de la mitocondria. | La contribución viral puede probarse sin decidir el mecanismo de captura mitocondrial. | C-361 |
| H15 modelo autógeno fagotrófico | H20 hipótesis autógena de invaginación nuclear | compatibles | H20 puede originar el núcleo autógeno requerido antes de la fagocitosis mitocondrial de H15. | El orden núcleo→fagocitosis→mitocondria sería la versión combinada. | C-362 |
| H15 modelo autógeno fagotrófico | H21 submodelo nuclear inside-out | mutuamente excluyentes | H15 suele asumir invaginación y fagocitosis de una célula ya interiorizada; H21 requiere topología inside-out y no necesita fagocitosis para la asociación inicial. | La orientación de membranas y el mecanismo de internalización resolverían el conflicto. | C-363 |
| H15 modelo autógeno fagotrófico | H22 hipótesis del protocoatómero | compatibles | La expansión del protocoatómero puede formar la maquinaria endomembranosa y fagocítica previa postulada por H15. | La homología de cubiertas no determina por sí sola cuándo se adquirió la mitocondria. | C-364 |
| H16 modelo de flujo inverso | H17 modelo E3 | compatibles | H16 puede proporcionar el intercambio metabólico inicial y E3 la geometría de entrelazamiento e internalización. | El socio bacteriano de E3 tendría que ser el receptor de equivalentes reductores predicho por H16. | C-365 |
| H16 modelo de flujo inverso | H18 hipótesis de invasión de intrones | compatibles | Una asociación de flujo inverso puede culminar en un endosimbionte que transfiera intrones de grupo II. | La dirección metabólica no altera la predicción intrón→compartimentación. | C-366 |
| H16 modelo de flujo inverso | H19 hipótesis viral del núcleo | compatibles | H16 no excluye una contribución viral adicional al núcleo. | La evidencia viral puede evaluarse de forma separada de la sintrofía. | C-367 |
| H16 modelo de flujo inverso | H20 hipótesis autógena de invaginación nuclear | compatibles | La sintrofía de flujo inverso puede coexistir con una invaginación nuclear autógena en otra etapa. | El orden de ambos procesos distinguiría variantes, no su compatibilidad. | C-368 |
| H16 modelo de flujo inverso | H21 submodelo nuclear inside-out | compatibles | El flujo arquea→bacteria puede ocurrir entre el cuerpo asgard y ectosimbiontes rodeados por protrusiones inside-out. | Reconstrucciones de orientación y metabolismo deberían ser simultáneamente consistentes. | C-369 |
| H16 modelo de flujo inverso | H22 hipótesis del protocoatómero | compatibles | H22 no fija metabolismo ni identidad del socio bacteriano. | La homología de coatómeros puede evaluarse independientemente. | C-370 |
| H17 modelo E3 | H18 hipótesis de invasión de intrones | compatibles | E3 puede producir el endosimbionte que después dona intrones de grupo II. | El orden E3→transferencia de intrones→compartimentación es una combinación explícita comprobable. | C-371 |
| H17 modelo E3 | H19 hipótesis viral del núcleo | compatibles | E3 no excluye aportes virales genéticos o una infección persistente posterior. | La procedencia viral de genes no altera necesariamente el mecanismo de engullimiento. | C-372 |
| H17 modelo E3 | H20 hipótesis autógena de invaginación nuclear | compatibles | E3 trata la internalización mitocondrial y H20 puede tratar por separado la envoltura nuclear. | La cronología de invaginación respecto del engullimiento distingue variantes. | C-373 |
| H17 modelo E3 | H21 submodelo nuclear inside-out | parcialmente compatibles | Comparten protrusiones asgard; E3 propone engullimiento focal de un socio y H21 una exteriorización global que define núcleo y retículo. | La continuidad topológica de protrusiones, retículo y membrana plasmática distinguiría si son etapas del mismo proceso. | C-374 |
| H17 modelo E3 | H22 hipótesis del protocoatómero | compatibles | Un protocoatómero podría mediar curvatura y fusión de membranas durante E3 sin estar especificado por el modelo. | La presencia de esa maquinaria en el tallo debe probarse mediante duplicaciones y homología. | C-375 |
| H18 hipótesis de invasión de intrones | H19 hipótesis viral del núcleo | parcialmente compatibles | Una contribución viral parcial puede coexistir con presión por intrones; son rivales solo cuando cada una se presenta como causa principal y suficiente del compartimento nuclear. | La cronología y procedencia de nucleoporinas, espliceosoma y membranas distinguirían causalidad principal de aporte accesorio. | C-376 |
| H18 hipótesis de invasión de intrones | H20 hipótesis autógena de invaginación nuclear | compatibles | La invaginación puede producir una envoltura cuya fijación sea favorecida por la necesidad de separar empalme y traducción. | El orden y la asociación temporal entre carga de intrones e invaginación distinguirían la combinación. | C-377 |
| H18 hipótesis de invasión de intrones | H21 submodelo nuclear inside-out | compatibles | Inside-out puede originar la geometría y la invasión de intrones aportar una presión selectiva posterior para cerrar o regular la envoltura. | Fechar intrones respecto de la formación topológica de la envoltura discriminaría la secuencia. | C-378 |
| H18 hipótesis de invasión de intrones | H22 hipótesis del protocoatómero | compatibles | La maquinaria protocoatómero puede originar poros y cubiertas mientras los intrones explican una presión funcional. | Homología de complejos y cronología de intrones son líneas independientes. | C-379 |
| H19 hipótesis viral del núcleo | H20 hipótesis autógena de invaginación nuclear | parcialmente compatibles | La invaginación autógena puede recibir genes virales; son incompatibles solo si H19 exige que el compartimento completo descienda del virus. | Distinguir origen de membrana frente a origen de genes resolvería la rivalidad aparente. | C-380 |
| H19 hipótesis viral del núcleo | H21 submodelo nuclear inside-out | parcialmente compatibles | Inside-out puede aceptar aportes virales parciales, pero no un reemplazo del cuerpo arqueano por un compartimento viral ancestral. | La homología topológica del núcleo y la dirección de HGT distinguirían las versiones. | C-381 |
| H19 hipótesis viral del núcleo | H22 hipótesis del protocoatómero | compatibles | Un origen o aporte viral no excluye que poro y coatómeros compartan una arquitectura celular ancestral, salvo que se atribuya también esa maquinaria al virus. | Filogenias y estructuras de nucleoporinas podrían separar aportes virales de paralogía celular. | C-382 |
| H20 hipótesis autógena de invaginación nuclear | H21 submodelo nuclear inside-out | mutuamente excluyentes | H20 invagina hacia dentro; H21 exterioriza protrusiones y conserva el cuerpo arqueano como núcleo. | La orientación topológica ancestral y el mecanismo de inserción de poros distinguen las geometrías. | C-383 |
| H20 hipótesis autógena de invaginación nuclear | H22 hipótesis del protocoatómero | compatibles | El protocoatómero puede proporcionar maquinaria de curvatura a una invaginación autógena. | La homología molecular no fija dirección de curvatura. | C-384 |
| H21 submodelo nuclear inside-out | H22 hipótesis del protocoatómero | compatibles | El protocoatómero puede mediar poros y curvatura dentro de la geometría inside-out. | La combinación exige que la cronología de duplicaciones sea anterior o concomitante a la exteriorización. | C-385 |

## 3.8. Qué no se sabe

La identidad taxonómica exacta del linaje hospedador arqueano no identificado permanece sin resolver. [C-386; S56 líneas 312–324; S57 pp. 295–301]

La identidad taxonómica exacta del simbionte alfaproteobacteriano ancestral no muestreado permanece sin resolver. [C-387; S56 líneas 312–324; S57 pp. 297–300]

No se sabe cuántos linajes adicionales, además de los componentes arqueano y alfa-proteobacteriano, contribuyeron de forma estable a la eucariogénesis. [C-388; S56 líneas 312–315; 320; 333–346]

Sin evidencia de un compartimento o genoma endosimbiótico, no puede distinguirse de forma general una ráfaga de transferencia desde asociaciones transitorias de una integración prolongada. [C-389; S56 línea 333]

No se conoce el orden completo de aparición de núcleo, poro, endomembranas, fagocitosis, mitosis y ciclo sexual dentro del intervalo FECA–LECA. [C-390; S56 líneas 321–330; S57 pp. 295–305; S100 tesis general]

No se ha resuelto si LECA era fagotrófico, aunque poseía sistemas de membrana que algunas reconstrucciones anotan como endocíticos y fagosomales. [C-391; S79; S59]

No existe una duración de consenso para el intervalo FECA–LECA. [C-392; S58 líneas 91–93; S56 líneas 306 y 321–324]

No se conoce si la población LECA tuvo un único ciclo vital dominante o alternó estados celulares ecológicamente distintos. [C-393; S52 §Population and consortium concepts; S56 líneas 325–330]

No se conoce la geometría celular intermedia que conectó membranas procarióticas con envoltura nuclear, retículo, Golgi y membrana plasmática eucariota. [C-394; S57 pp. 299–303; S88; S96]

La homología estructural de coatómeros y poro no determina por sí sola qué geometría celular produjo esos complejos. [C-395; S97, S98, S99]

La presencia de protrusiones en Asgard cultivados no determina si la internalización ancestral siguió inside-out, E3 u otra geometría. [C-396; S88; S34]

La dirección de transferencia entre virus gigantes y eucariotas no está resuelta para varias homologías usadas en hipótesis virales del núcleo. [C-397; S94, S95 Discussion]

La proporción del repertorio de LECA que conserva señal filogenética útil más allá de Eukaryota no está cuantificada de forma consensuada. [C-398; S56 líneas 380–384]

Mejor muestreo de arqueas y bacterias próximas, proteomas eucariotas menos sesgados, modelos heterogéneos y estructuras proteicas pueden cambiar tanto la topología como la cronología del tallo. [C-399; S56 líneas 380–407; S58 línea 91]

Los modelos de esta parte no forman una única lista de alternativas equivalentes porque algunos explican metabolismo, otros geometría, otros origen nuclear y otro homología de maquinaria. [C-400; n/a; matriz de compatibilidad de esta parte]

## 3.9. Registro de afirmaciones

> **Registro de afirmaciones:** [data/afirmaciones/03.csv](../data/afirmaciones/03.csv) (255 filas; 12 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---

# 4. La raíz eucariota y la forma de Amorphea

## 4.1. Por qué la raíz es difícil

La raíz del árbol eucariota identifica el nodo correspondiente a la población LECA reconstruida y condiciona la polaridad de los caracteres eucariotas. [C-405; S102 resumen; S56 tesis general]

No existe un grupo externo celular próximo a Eukaryota que conserve suficientes caracteres homólogos y una distancia evolutiva corta para enraizarlo directamente. [C-406; S102 resumen; S137 §Rooting]

Las divergencias profundas del árbol eucariota acumulan sustituciones múltiples y saturación. [C-407; S102 resumen; S137 §Phylogenomic artefacts]

La atracción de ramas largas puede agrupar linajes de evolución rápida por artefacto. [C-408; S102 resumen; S104 tesis general]

La heterogeneidad composicional y la heterogeneidad de tasas entre sitios pueden cambiar la topología recuperada. [C-409; S102 figs. 1–2; S104 tesis general]

La selección de ortólogos, los datos ausentes y las secuencias atípicas pueden alterar la raíz inferida. [C-410; S104 tesis general; S126 figs. 2 y 5]

Una probabilidad posterior, un bootstrap y una prueba AU no son medidas intercambiables y se transcriben sin convertirlas a una escala común. [C-411; n/a; convención documental]

## 4.2. Hipótesis de raíz que no deben fundirse

### 4.2.1. División histórica unikonta–bikonta

```text
Eukaryota [H] ⚠
├─ Unikonta sensu histórico ⚠
└─ Bikonta sensu histórico ⚠
```

La división histórica unikonta–bikonta situó la raíz entre un conjunto que incluía Amoebozoa y Opisthokonta y otro conjunto de eucariotas ancestrales supuestamente biciliados. [C-412; S116 tesis general; S118 tesis general; S89 clasificación]

La denominación Unikonta suponía un estado ancestral con un solo cinetosoma o sistema flagelar. [C-413; S89 §Unikonta; S138 discusión]

La denominación Bikonta suponía un estado ancestral con dos cinetosomas o sistemas flagelares. [C-414; S116 tesis general; S138 discusión]

La división unikonta–bikonta no coincide exactamente con Amorphea frente a Diaphoretickes ni con Opimoda frente a Diphoda. [C-415; S105 discusión; S124 definición; S137 revisión]

### 4.2.2. Raíz entre Amorphea y Diaphoretickes: una abreviación condicionada

Brown et al. organizaron el árbol eucariota no en dos, sino en tres ensamblajes de orden superior: Amorphea, Diaphoretickes y Excavata. [C-663; S108 Introduction]

Al resumir la propuesta de Derelle et al., Brown et al. escribieron que la raíz quedaba “somewhere between Amorphea and the other two listed lineages”. [C-664; S108 Introduction]

La expresión «raíz entre Amorphea y Diaphoretickes» corresponde por tanto a una abreviación de árboles simplificados, no a una bipartición inequívoca cuando Excavata y los linajes profundos no asignados se representan por separado. [C-665; S108 Introduction; Results; BN-036]

Esta abreviación no es sinónima de la raíz Opimoda–Diphoda: Opimoda contiene más que Amorphea y Diphoda contiene más que Diaphoretickes bajo la circunscripción de Derelle et al. [C-666; S105 fig. 1; S108 Introduction]

### 4.2.3. Raíz Opimoda–Diphoda

```text
Eukaryota [H] ⚠
├─ Opimoda ⚠
└─ Diphoda ⚠
```

Derelle et al. propusieron una raíz entre Opimoda y Diphoda mediante proteínas eucariotas de origen bacteriano. [C-416; S105 título; figs. 1–3]

Opimoda incluyó a Amorphea y linajes profundos asociados según la circunscripción de Derelle et al. [C-417; S105 fig. 1; definición]

Diphoda incluyó a Diaphoretickes y varios linajes excavados según la circunscripción de Derelle et al. [C-418; S105 fig. 1; definición]

El análisis de Derelle et al. recuperó la raíz Opimoda–Diphoda con PP = 0.95 bajo CAT-GTR y PP = 0.97 bajo CAT en los análisis citados. [C-419; S105 resultados; figs. 2–3]

### 4.2.4. Raíz Discoba

```text
Eukaryota [H] ⚠
├─ Discoba ⚠
└─ restantes eucariotas activamente mitocondriados del muestreo
```

He et al. propusieron una raíz con Discoba como rama hermana del resto de los eucariotas activamente mitocondriados incluidos. [C-420; S106 título; fig. 1]

La raíz Discoba de He et al. no prueba la monofilia de una Excavata amplia. [C-421; S106 discusión; S137 revisión]

### 4.2.5. Raíz excavada con divergencias sucesivas

```text
Eukaryota [H] ⚠
├─ linaje excavado 1 del análisis
├─ linaje excavado 2 del análisis
├─ linaje excavado 3 del análisis
├─ linaje excavado 4 del análisis
└─ restantes eucariotas muestreados
```

Al Jewari y Baldauf analizaron 183 proteínas eucariotas de ascendencia arqueana para evaluar la raíz. [C-422; S103 resumen; Methods]

Al Jewari y Baldauf recuperaron cuatro linajes excavados que se separan sucesivamente antes del resto de Eukaryota. [C-423; S103 resumen; figs. 1–3]

La hipótesis de raíz excavada sucesiva no identifica a Excavata como un único clado hermano del resto. [C-424; S103 resumen; fig. 3]

Al Jewari y Baldauf atribuyeron parte del conflicto con otras raíces a secuencias atípicas, mosaicos y sensibilidad a datos ausentes en modelos CAT. [C-425; S104 tesis general; S103 discusión]

### 4.2.6. Raíz Opisthokonta

```text
Eukaryota [H] ⚠
├─ Opisthokonta
└─ restantes eucariotas
```

Cerón-Romero et al. analizaron 2.786 familias génicas de 158 linajes mediante reconciliación de árboles génicos y árbol de especies. [C-426; S107 título; Methods]

Cerón-Romero et al. favorecieron una raíz entre Opisthokonta y todos los demás linajes eucariotas. [C-427; S107 título; resultados]

La raíz Opisthokonta es incompatible en su posición exacta con Opimoda–Diphoda y con raíces excavadas. [C-428; S105; S103; S107]

### 4.2.7. Raíz Opimoda+–Diphoda+ de Williamson et al.

```text
Eukaryota [H] ⚠
├─ Opimoda+ ⚠
└─ Diphoda+ ⚠
```

Williamson et al. analizaron 100 taxones y 93 proteínas relacionadas con la mitocondria. [C-429; S102 Methods; fig. 1]

Williamson et al. incluyeron todos los supergrupos eucariotas reconocidos por su clasificación de trabajo. [C-430; S102 resumen; Supplementary table 7]

Williamson et al. compararon modelos sitio-homogéneos, mezclas de perfiles y modelos sitio-heterogéneos. [C-431; S102 figs. 1–2; Methods]

Williamson et al. aplicaron retirada de sitios rápidos, taxones rápidos y genes divergentes como pruebas de artefacto. [C-432; S102 Methods; Extended Data]

Williamson et al. recuperaron consistentemente una raíz entre Opimoda+ y Diphoda+. [C-433; S102 resumen; figs. 1–2]

Opimoda+ y Diphoda+ amplían o modifican las circunscripciones de Opimoda y Diphoda usadas en 2015. [C-434; S102 fig. 1; S105 definición]

La raíz de Williamson et al. es una inferencia filogenómica y no una observación directa de LECA. [C-435; n/a; clasificación de evidencia basada en S102]

### 4.2.8. Comparación de las raíces

| hipótesis | marcadores | método principal | primera divergencia | relación con las otras | filas |
| --- | --- | --- | --- | --- | --- |
| Unikonta–Bikonta | DHFR–TS, miosinas, caracteres flagelares | caracteres raros y reconstrucción morfológica | Unikonta / Bikonta | histórica; circunscripciones no coinciden con nombres actuales | C-412–C-415; C-437–C-457 |
| Amorphea–Diaphoretickes en esquema simplificado | supergrupos de síntesis | representación resumida de árboles globales | Amorphea / Diaphoretickes solo cuando otros linajes se omiten o asignan a uno de los lados | no define una bipartición única con Excavata y linajes huérfanos; no es sinónimo de Opimoda–Diphoda | C-663–C-666 |
| Opimoda–Diphoda | proteínas de origen bacteriano | concatenación y modelos CAT | Opimoda / Diphoda | incompatible con raíces Discoba, excavada sucesiva y Opisthokonta | C-416–C-419 |
| Discoba | proteínas de ascendencia mitocondrial | filogenia enraizada | Discoba / resto del muestreo | no equivale a Excavata monofilética | C-420–C-421 |
| excavada sucesiva | 183 proteínas de ascendencia arqueana | concatenación y análisis de sensibilidad | cuatro linajes sucesivos / resto | no es una bifurcación Excavata / resto | C-422–C-425 |
| Opisthokonta | 2.786 árboles génicos | reconciliación de genes y especies | Opisthokonta / resto | usa una clase de evidencia distinta de concatenación | C-426–C-428 |
| Opimoda+–Diphoda+ | 93 proteínas relacionadas con mitocondria, 100 taxones | modelos complejos y retirada de sitios/taxones/genes rápidos | Opimoda+ / Diphoda+ | revisión de circunscripciones Opimoda/Diphoda | C-429–C-435 |

No existe una posición de raíz eucariota aceptada como consenso universal. [C-436; S102 resumen; S137 §Rooting]

## 4.3. Caracteres moleculares raros y su peso actual

### 4.3.1. Fusión DHFR–TS

Stechmann y Cavalier-Smith propusieron la fusión DHFR–TS como sinapomorfía derivada de Bikonta. [C-437; S116 tesis general]

DHFR y TS aparecen fusionadas en numerosos eucariotas y separadas en otros. [C-438; S117 fig. 2; Results]

Se han documentado pérdidas de DHFR, TS o del locus fusionado en varios subgrupos. [C-439; S117 Results; fig. 2]

La fisión de genes y la pérdida diferencial hacen que DHFR–TS sea un carácter no fiable para polarizar por sí solo la raíz. [C-440; S117 líneas sobre DHFR–TS; Discussion]

La fusión DHFR–TS conserva valor como carácter histórico local, pero no como prueba decisiva de una raíz unikonta–bikonta. [C-441; S117 Discussion; S120 tesis general]

### 4.3.2. Repertorios de miosina

Richards y Cavalier-Smith clasificaron 37 combinaciones de dominios de miosina en el muestreo disponible en 2005. [C-442; S118 Results; sin localizar]

Richards y Cavalier-Smith atribuyeron tres tipos de miosina a LECA en su reconstrucción. [C-443; S118 Results; S119 introducción]

Sebé-Pedrós et al. incorporaron por primera vez representantes de todos los supergrupos eucariotas principales de su clasificación de trabajo. [C-444; S119 introducción; Methods]

Sebé-Pedrós et al. declararon que no pretendían inferir el árbol eucariota a partir del contenido de miosinas. [C-445; S119 introducción: “We do not aim to infer...”]

Duplicación, pérdida, convergencia, fisión y transferencia horizontal pueden alterar los repertorios de miosina. [C-446; S119 introducción; Discussion]

Los repertorios de miosina tienen peso actual como evidencia de historia de familias génicas, no como polarizador único de la raíz. [C-447; S119 Discussion; S102 introducción]

### 4.3.3. Inserciones y deleciones conservadas

Baldauf y Palmer identificaron cuatro inserciones o deleciones compartidas por animales y hongos frente al muestreo externo de 1993. [C-448; S122 resumen; Results]

Una inserción de 12 aminoácidos en eEF1A fue uno de los caracteres usados para asociar animales y hongos. [C-449; S122 resumen; fig. 1]

Tres hendiduras pequeñas en enolasa fueron usadas como caracteres adicionales de la relación animales–hongos. [C-450; S122 resumen; Results]

Los indels pueden presentar homoplasia, errores de alineamiento y pérdidas secundarias. [C-451; S123 tesis general; S120 Discussion]

Los indels históricos respaldan Opisthokonta, pero no determinan por sí solos la raíz de Eukaryota. [C-452; S122; S123]

### 4.3.4. Posiciones de intrones

Rogozin et al. documentaron conservación de posiciones de intrones entre reinos eucariotas. [C-453; S121 título; Results]

Rogozin et al. documentaron ganancias y pérdidas masivas de intrones específicas de linaje. [C-454; S121 título; Results]

La conservación de intrones puede sostener homología profunda, pero la pérdida diferencial dificulta usarla como marcador de raíz único. [C-455; S121 Discussion; S120 Discussion]

### 4.3.5. Evaluación conjunta

Rogozin et al. analizaron cambios genómicos raros y no recuperaron apoyo para la filogenia unikonta–bikonta. [C-456; S120 título; Results]

Ningún carácter molecular raro localizado en esta sesión resuelve por sí solo la raíz eucariota. [C-457; S117; S119, S120, S121, S122, S123]

## 4.4. Amorphea y los linajes que orbitan su base

### 4.4.1. Amorphea

Adl et al. definieron Amorphea como el clado menos inclusivo que contiene Homo sapiens, Neurospora crassa y Dictyostelium discoideum. [C-458; S124 definición de Amorphea; S01 clasificación]

Amorphea incluye Amoebozoa y Obazoa en la clasificación adoptada. [C-459; S01 clasificación; S108 fig. 1; S109 árbol]

Amoebozoa es el grupo hermano de Obazoa dentro de Amorphea en la topología de trabajo. [C-460; S01 clasificación; S109 árbol; S112 fig. 3]

No se localizó una sinapomorfía morfológica exclusiva publicada para Amorphea. [C-461; NO LOCALIZADO EN ESTA SESIÓN; BN-020]


```text
CRuMs [F] ── grupo hermano de ── Amorphea [F]
                                      ├─ Amoebozoa [F]
                                      └─ Obazoa [F]
```

### 4.4.2. CRuMs

Brown et al. analizaron 351 proteínas, 61 o 64 taxones y 97.002 posiciones de aminoácidos. [C-462; S108 Methods: Data Set Construction]

Brown et al. usaron LG+C60+F+Γ-PMSF y CAT-GTR+Γ como modelos sitio-heterogéneos. [C-463; S108 Methods: Tree Inference]

Brown et al. recuperaron Collodictyonida, Rigifilida y Mantamonas como un clado denominado provisionalmente CRuMs. [C-464; S108 resumen; fig. 1]

Brown et al. recuperaron CRuMs como grupo hermano de Amorphea con soporte máximo. [C-465; S108 Results: fig. 1; líneas sobre maximal support]

Brown et al. declararon que CRuMs era un rótulo provisional y no un taxón formal. [C-466; S108 Discussion: “place-holding moniker”]

### 4.4.3. Ancyromonadida y Malawimonadida

Brown et al. situaron Ancyromonadida fuera de Amorphea y más lejos de Amorphea que CRuMs. [C-467; S108 resumen; Results]

En el análisis de máxima verosimilitud de Brown et al., Ancyromonadida y Malawimonadida formaron un clado con BS = 77 %. [C-468; S108 Results; fig. 1]

Las cadenas bayesianas convergentes de Brown et al. situaron Malawimonadida con CRuMs+Amorphea y excluyeron Ancyromonadida con PP = 1. [C-469; S108 Results; suppl. figs. S2–S3]

Brown et al. trataron las dos posiciones de Ancyromonadida y Malawimonadida como hipótesis candidatas. [C-470; S108 Results: “candidate hypotheses requiring further investigation”]

Torruella et al. 2025 recuperaron una asociación entre Ancyromonadida y Malawimonadida en parte de sus análisis, sin eliminar toda sensibilidad profunda. [C-471; S109 resultados; fig. 2; sin localizar]

## 4.5. Historia nomenclatural: nombres solapados, no una bolsa de sinónimos

### 4.5.1. Unikonta y Amorphea

Cavalier-Smith empleó Unikonta para una agrupación basada en una reconstrucción ancestral uniciliada y caracteres moleculares asociados. [C-472; S89 clasificación; S116, S117, S118]

Unikonta fue abandonado en la clasificación de Adl et al. porque el nombre y su diagnóstico sugerían una ancestralidad flagelar no sostenida. [C-473; S124 introducción y definición de Amorphea]

Amorphea sustituyó a Unikonta mediante una definición filogenética de nodo que no depende de contar cilios. [C-474; S124 definición; S01 clasificación]

### 4.5.2. Podiata

Cavalier-Smith empleó “podiates” para eucariotas con pseudópodos o descendientes de formas pseudopodiales dentro de su sistema. [C-475; S125 clasificación; S145 tesis general]

El uso de Podiata en filogenómicas recientes puede designar Amorphea+CRuMs. [C-476; S109 árbol; S108 relación hermana; sin localizar]

Podiata sensu Cavalier-Smith y Podiata sensu filogenómico reciente son circunscripciones rivales y no sinónimos automáticos. [C-477; S125; S109]

### 4.5.3. Sulcozoa

Cavalier-Smith propuso Sulcozoa para Apusozoa y Varisulca en su clasificación de 2013. [C-478; S125 resumen y clasificación]

Sulcozoa fue concebido como un conjunto que podía ser parafilético respecto de Opisthokonta y Amoebozoa. [C-479; S125 discusión clasificatoria]

Sulcozoa no es un nombre alternativo moderno de Obazoa. [C-480; S125; S111 definición de Obazoa]

### 4.5.4. Varisulca

Varisulca reunió Diphyllatea, Planomonadida, Discocelida, Mantamonadida y Rigifilida en la clasificación de Cavalier-Smith. [C-481; S125 clasificación; sin localizar]

Varisulca no equivale a CRuMs porque incluye linajes distintos y excluye Collodictyonida en la circunscripción citada. [C-482; S125; S108 definición de CRuMs]

### 4.5.5. Estado de Amorphea

Amorphea permanece en uso en Adl et al. 2019. [C-483; S01 clasificación]

La disponibilidad nomenclatural, la aceptación en una clasificación y el soporte filogenético son propiedades distintas. [C-484; n/a; convención documental]

## 4.6. Corredor filogenético y tablas por nodo

El árbol siguiente es una vista parcial del corredor. Las ramas eucariotas externas no se despliegan como catálogo. Dentro de Holozoa, la lista de ramas profundas no representa un orden de divergencia; las tres topologías incompatibles se muestran por separado en 4.7.

```text
Eukaryota [F]  [vista parcial]
├─ ⋯ ramas externas al corredor no desplegadas
└─ Amorphea [F]  [C-656]
   ├─ Amoebozoa [F]
   └─ Obazoa [F]
      ├─ Breviatea [F] ⚠
      └─┬─ Apusomonadida [F] ⚠
        └─ Opisthokonta [F]
           ├─ Holomycota [F]
           └─ Holozoa [F]
              │  [orden de las ramas siguientes no representado; véase 4.7]
              ├─ Pluriformea [F] ⚠
              │  ├─ Corallochytrea [F]
              │  └─ Syssomonas y linajes incluidos según circunscripción
              ├─ Ichthyosporea [F] ⚠
              └─ Filozoa [F]
                 ├─ Filasterea [F]
                 └─ Choanozoa sensu stricto ≈ Apoikozoa [F]
                    ├─ Choanoflagellata [F]
                    └─ Metazoa [F]  [terminal]
```

La inclusión de Amorphea en Eukaryota, la incertidumbre sobre la raíz interna de Holozoa y la circunscripción de Pluriformea están registradas respectivamente en C-656, C-639 y C-646–C-649.

### 4.6.1. Eukaryota

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Eukaryota | todos los eucariotas vivientes y la población LECA reconstruida | linaje asgard más próximo a Eukaryota no resuelto | envoltura nuclear, poro nuclear, endomembranas, citoesqueleto y mitocondria atribuidos a LECA; no constituyen una única sinapomorfía morfológica observada [S56 fig. 2] | paralogías profundas y repertorios celulares reconstruidos; S56 [S56 §§Reconstrucción] | filogenómica comparada y reconstrucción ancestral | n/a para monofilia corona; la posición de la raíz interna está discutida | 1.679–1.866 Ga en S139; 1.958–2.386 Ga en S140; no existe estimación de consenso | relojes relajados con calibraciones y raíces diferentes | C-485, C-486, C-487, C-488, C-489, C-490, C-491, C-492 |

### 4.6.2. Amorphea

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Amorphea | Amoebozoa y Obazoa | CRuMs en S108 y S109 | SIN SINAPOMORFÍA MORFOLÓGICA PUBLICADA LOCALIZADA [BN-020] | definición de nodo y soporte multigénico; no se localizó una fusión exclusiva vigente [S108 Results] | filogenómica concatenada con modelos sitio-heterogéneos | soporte máximo para CRuMs+Amorphea en S108; Amorphea cerca de 100 % durante retirada de sitios rápidos | NO LOCALIZADO EN ESTA SESIÓN | NO LOCALIZADO EN ESTA SESIÓN; BN-021 | C-493, C-494, C-495, C-496, C-497, C-498, C-499, C-500 |

### 4.6.3. Amoebozoa

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Amoebozoa | Discosea y Tevosa, con sus linajes componentes según S112 | Obazoa | formas ameboides aparecen en muchos miembros, pero no son exclusivas ni constantes; SIN SINAPOMORFÍA MORFOLÓGICA PUBLICADA LOCALIZADA para el nodo completo [S112 discusión morfológica] | 325 genes y 63.157 posiciones en S112 [S112 Methods; fig. 3] | filogenómica concatenada bajo ML y Bayes | BPP = 1.0 y MLBS = 99 para el respaldo principal citado en S112 | NO LOCALIZADO EN ESTA SESIÓN | NO LOCALIZADO EN ESTA SESIÓN; BN-022 | C-501, C-502, C-503, C-504, C-505, C-506, C-507, C-508 |

### 4.6.4. Obazoa

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Obazoa | Breviatea, Apusomonadida y Opisthokonta | Amoebozoa | SIN SINAPOMORFÍA MORFOLÓGICA PUBLICADA LOCALIZADA [BN-024] | matriz de 159 proteínas y 43.615 aminoácidos en S111; matrices posteriores amplían muestreo [S111 Methods] | filogenómica concatenada y comparación de modelos | clado fuertemente respaldado en S111; cerca de 100 % durante retirada de sitios rápidos en S108 | NO LOCALIZADO EN ESTA SESIÓN | NO LOCALIZADO EN ESTA SESIÓN; BN-023 | C-509, C-510, C-511, C-512, C-513, C-514, C-515, C-516 |

### 4.6.5. Apusomonadida

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apusomonadida | Thecamonas y otros apusomonádidos muestreados | Opisthokonta en la topología de trabajo de S109 | dorsal theca, dos cinetosomas y raíces microtubulares caracterizan taxones estudiados; exclusividad nodal no demostrada [S113 Results; figs. 2–8] | filogenómica de Obazoa y muestreo ampliado de flagelados [S111; S109] | ultraestructura taxonómica y filogenómica | soporte alto en S109; valor numérico exacto NO LOCALIZADO EN ESTA SESIÓN | NO LOCALIZADO EN ESTA SESIÓN | NO LOCALIZADO EN ESTA SESIÓN; BN-025 | C-517, C-518, C-519, C-520, C-521, C-522, C-523, C-524 |

### 4.6.6. Breviatea

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Breviatea | Breviata, Pygsuia y linajes breviados reconocidos | Apusomonadida+Opisthokonta en la topología de trabajo de S109 | dos cuerpos basales, raíces microtubulares y orgánulo mitocondrial relacionado en Breviata; no son sinapomorfías exclusivas demostradas del nodo [S114 Results] | filogenómica de Obazoa y marcadores posteriores [S111; S109] | filogenómica, genómica y ultraestructura de taxones | soporte de Obazoa alto; orden interno varía entre estudios y valor exacto no localizado | NO LOCALIZADO EN ESTA SESIÓN | NO LOCALIZADO EN ESTA SESIÓN; BN-026 | C-525, C-526, C-527, C-528, C-529, C-530, C-531, C-532 |

### 4.6.7. Opisthokonta

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Opisthokonta | Holomycota y Holozoa | Apusomonadida en la topología de trabajo de S109 | cilio posterior en las células flageladas y crestas mitocondriales planas se propusieron como caracteres; existen pérdidas y estados no flagelados [S137 revisión; S144 discusión] | indels históricos, múltiples matrices filogenómicas y contenido génico [S122; S126] | filogenómica, cambios genómicos raros y ultraestructura comparada | aproximadamente 85 % de ramas internas congruentes en 18 árboles de S126; Opisthokonta como clado no fue el nodo conflictivo principal | 1.083,2 Ma; IC 95 % 978,7–1.187,6 Ma | MCMCTree, reloj relajado no correlacionado, 10 calibraciones fósiles, raíz fijada en 1,5 Ga | C-533, C-534, C-535, C-536, C-537, C-538, C-539, C-540 |

### 4.6.8. Holomycota

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Holomycota | Nucleariida, Fungi y parientes unicelulares próximos | Holozoa | SIN SINAPOMORFÍA MORFOLÓGICA PUBLICADA LOCALIZADA para todo Holomycota [BN-027] | filogenómica y trayectorias de contenido génico; Nucleariida hermana del resto en S126 [S126 Results; S143] | filogenómica de proteínas y genómica comparada | Nucleariida hermana del resto recuperada consistentemente en S126; clado Holomycota estable en matrices principales | 996 Ma; IC 95 % 890,1–1.101,9 Ma | MCMCTree, reloj relajado no correlacionado, 10 calibraciones fósiles, raíz fijada en 1,5 Ga | C-541, C-542, C-543, C-544, C-545, C-546, C-547, C-548 |

### 4.6.9. Holozoa

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Holozoa | Pluriformea, Ichthyosporea y Filozoa; Tunicaraptor con posición interna discutida | Holomycota | SIN SINAPOMORFÍA MORFOLÓGICA PUBLICADA LOCALIZADA para todo Holozoa [BN-028] | fusión ubiquitina–S128 propuesta en S130; filogenómica de múltiples matrices [S130 resumen; S126] | filogenómica concatenada, concordancia génica y caracteres moleculares | monofilia amplia estable; raíz interna produce topologías Pluriformea-sister, Teretosporea-sister e Ichthyosporea-sister | 1.003,8 Ma; IC 95 % 913,8–1.093,9 Ma | MCMCTree, reloj relajado no correlacionado, 10 calibraciones fósiles, raíz fijada en 1,5 Ga | C-549, C-550, C-551, C-552, C-553, C-554, C-555, C-556 |

### 4.6.10. Ichthyosporea

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ichthyosporea | Ichthyophonida, Dermocystida y otros linajes según circunscripción de S133 | variable entre Filozoa, Pluriformea o el resto de Holozoa según matriz | paredes o estadios multinucleados aparecen en varios linajes, pero no son sinapomorfía exclusiva universal; SIN SINAPOMORFÍA MORFOLÓGICA PUBLICADA LOCALIZADA para el nodo completo [S133 revisión] | filogenómica de S128, S129, S130 y síntesis genómica de S133 [S128, S129, S130; S133] | filogenómica y genómica comparada | ninguna de las tres posiciones profundas tiene concordancia génica suficiente para resolver el nodo en S126 | NO LOCALIZADO EN ESTA SESIÓN | NO LOCALIZADO EN ESTA SESIÓN; BN-029 | C-557, C-558, C-559, C-560, C-561, C-562, C-563, C-564 |

### 4.6.11. Pluriformea sensu Hehenberger et al. 2017

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pluriformea sensu Hehenberger et al. 2017 | Syssomonas y Corallochytrium/Corallochytrea en la circunscripción original | variable: resto de Holozoa o Ichthyosporea según matriz | ciclos pluriformes en taxones descritos; SIN SINAPOMORFÍA MORFOLÓGICA PUBLICADA LOCALIZADA para el clado completo [S129 descripción; S132] | 255 genes, 81.495 aminoácidos, 38 taxones en S129 [S129 Methods] | transcriptómica y filogenómica concatenada | Ichthyosporea como rama profunda obtuvo MLBS = 74 % en S129; otras matrices recuperan topologías distintas | NO LOCALIZADO EN ESTA SESIÓN | NO LOCALIZADO EN ESTA SESIÓN; BN-030 | C-565, C-566, C-567, C-568, C-569, C-570, C-571, C-572 |

### 4.6.12. Corallochytrea

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Corallochytrea | Corallochytrium y linajes asignados por secuencia según autor | Syssomonas dentro de Pluriformea sensu S129 | morfología de Corallochytrium no establece una sinapomorfía de un clado multiespecífico; SIN SINAPOMORFÍA MORFOLÓGICA PUBLICADA LOCALIZADA [S129 Discussion] | transcriptoma de Corallochytrium y filogenómica de Pluriformea [S129 Methods] | filogenómica y descripción morfológica de taxones | relación Syssomonas+Corallochytrium fuertemente apoyada en S129; valor exacto no localizado | NO LOCALIZADO EN ESTA SESIÓN | NO LOCALIZADO EN ESTA SESIÓN; BN-031 | C-573, C-574, C-575, C-576, C-577, C-578, C-579, C-580 |

### 4.6.13. Filasterea

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Filasterea | Capsaspora, Ministeria, Pigoraptor y linajes incorporados por clasificaciones posteriores | Choanozoa sensu stricto dentro de Filozoa | filopodios o tentáculos actínicos caracterizan algunos miembros; Pigoraptor y ciclos diversos impiden tratarlos como sinapomorfía universal [S130 descripción; S129; S132] | 78 proteínas en S130 y 255 genes en S129; repertorios de adhesión y señalización [S130 Methods; S129] | filogenómica concatenada y genómica comparada | Filasterea y su relación con Choanozoa recibieron soporte máximo en S130 para el muestreo de 2008 | NO LOCALIZADO EN ESTA SESIÓN | NO LOCALIZADO EN ESTA SESIÓN; BN-032 | C-581, C-582, C-583, C-584, C-585, C-586, C-587, C-588 |

### 4.6.14. Filozoa

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Filozoa | Filasterea y Choanozoa sensu stricto | Ichthyosporea o Pluriformea según la raíz interna de Holozoa adoptada | capacidad de formar filopodios se propuso históricamente; no es exclusiva ni universal; SIN SINAPOMORFÍA MORFOLÓGICA PUBLICADA LOCALIZADA para el nodo [S130 Discussion; S134 revisión] | matriz de 78 proteínas, 30 taxones y 17.482 aminoácidos en S130 [S130 Methods] | filogenómica concatenada y repertorios celulares | soporte máximo en ML y Bayes para la relación Filasterea+(Choanoflagellata+Metazoa) en S130 | NO LOCALIZADO EN ESTA SESIÓN | NO LOCALIZADO EN ESTA SESIÓN; BN-033 | C-589, C-590, C-591, C-592, C-593, C-594, C-595, C-596 |

### 4.6.15. Choanozoa sensu stricto ≈ Apoikozoa

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Choanozoa sensu stricto ≈ Apoikozoa | Choanoflagellata y Metazoa | Filasterea | complejo de collar con cilio apical rodeado de microvellosidades actínicas propuesto para el ancestro; homología y distribución exacta requieren cautela [S134 glosario y discusión] | filogenias multigénicas y genómicas recuperan Choanoflagellata+Metazoa [S130; S136; S147] | filogenómica, genómica y morfología comparada | relación Choanoflagellata+Metazoa con soporte máximo en S130; S136 confirma el nodo con muestreo de coanoflagelados | 761–957 Ma en S142; no existe estimación de consenso | reloj molecular relajado bayesiano con seis calibraciones fósiles | C-597, C-598, C-599, C-600, C-601, C-602, C-603, C-604 |

### 4.6.16. Choanoflagellata

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Choanoflagellata | Craspedida y Acanthoecida en la clasificación de trabajo | Metazoa | célula con un cilio apical rodeado por collar de microvellosidades actínicas en el estado característico [S134 glosario; S136 introducción] | filogenias multigénicas y genomas de coanoflagelados [S136; S147] | morfología, filogenia molecular y genómica | grupo hermano de Metazoa con soporte máximo en S130; S136 recupera la relación en su muestreo | la divergencia Choanoflagellata–Metazoa fue estimada en 761–957 Ma por S142 | reloj molecular relajado bayesiano con seis calibraciones fósiles | C-605, C-606, C-607, C-608, C-609, C-610, C-611, C-612 |

### 4.6.17. Metazoa

| nodo | qué linajes quedan dentro | qué linaje queda fuera (grupo hermano) | caracteres morfológicos o ultraestructurales propuestos como sinapomorfía, con fuente | caracteres moleculares o genómicos propuestos (fusiones génicas, inserciones y deleciones raras, sintenia, dominios proteicos), con fuente | tipo de evidencia que sostiene el nodo | soporte cuantitativo transcrito literalmente | edad estimada con intervalo | método de la estimación | # de la fila del registro que sostiene cada celda sustantiva |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Metazoa | Metazoa se mantiene como terminal y no se desarrolla su topología interna en esta parte | Choanoflagellata | n/a: el encargo limita Metazoa a un terminal y no permite desarrollar caracteres internos [n/a] | filogenómica recupera Metazoa como clado hermano de Choanoflagellata [S130; S136] | filogenómica; la morfología interna queda fuera de alcance | soporte máximo para Choanoflagellata+Metazoa en S130 | NO BUSCADO: origen y divergencias de Metazoa fuera de alcance | NO BUSCADO; BN-035 | C-613, C-614, C-615, C-616, C-617, C-618, C-619, C-620 |

## 4.7. Tres raíces incompatibles dentro de Holozoa unicelular

```text
H32 Pluriformea-sister:      (Pluriformea, (Ichthyosporea, Filozoa))
H33 Teretosporea-sister:     ((Pluriformea, Ichthyosporea), Filozoa)
H34 Ichthyosporea-sister:    (Ichthyosporea, (Pluriformea, Filozoa))
```

Liu et al. reunieron 348 taxones pertenecientes a 33 linajes principales de Opisthokonta. [C-621; S126 Results; S3 table]

La matriz BUSCO de Liu et al. contiene 228 genes. [C-622; S126 tabla 1; Methods]

La matriz OrthoFinder de Liu et al. contiene 440 genes. [C-623; S126 tabla 1; Methods]

La matriz Tikhonenkov_2020 de Liu et al. contiene 201 genes. [C-624; S126 tabla 1; Methods]

Liu et al. generaron 18 árboles mediante tres matrices, dos versiones de taxones y tres esquemas de modelos. [C-625; S126 Methods; fig. 2]

Aproximadamente 85 % de las ramas internas fueron congruentes entre los 18 árboles. [C-626; S126 Results]

Los análisis con el mismo conjunto de ortólogos mostraron 97–98 % de congruencia. [C-627; S126 Results]

Los análisis con conjuntos de ortólogos diferentes mostraron 87–91 % de congruencia. [C-628; S126 Results]

BUSCO y Tikhonenkov_2020 recuperaron Pluriformea como grupo hermano del resto de Holozoa. [C-629; S126 Results; fig. 4]

OrthoFinder recuperó Pluriformea+Ichthyosporea como Teretosporea, hermana de Filozoa. [C-630; S126 Results; fig. 4]

Una ejecución BUSCO bajo GTR+CAT apoyó débilmente Teretosporea-sister con UFB = 23. [C-631; S126 Results; S1 Data]

La hipótesis Ichthyosporea-sister no fue recuperada en los análisis principales de Liu et al. [C-632; S126 Results]

La reducción de la matriz Tikhonenkov_2020 a 60 taxones cambió el resultado a Ichthyosporea-sister. [C-633; S126 fig. 5C; Results]

El aumento del muestreo a 180, 240 y 347 taxones favoreció Pluriformea-sister en los análisis citados. [C-634; S126 fig. 5C; Results]

La hipótesis Teretosporea-sister obtuvo UFB = 98 con OrthoFinder#2 bajo un modelo sitio-homogéneo. [C-635; S126 fig. 5E; Results]

Solo 0,7 % de los loci, 3 de 426, apoyaron Teretosporea-sister en el cálculo de gCF citado. [C-636; S126 fig. 5E; Results]

El 98,6 % de los árboles génicos, 420 de 426, apoyó topologías distintas de las tres candidatas en el análisis citado. [C-637; S126 fig. 5E; Results]

Los apoyos de sitios para las tres topologías fueron 34,04/32,98/32,98. [C-638; S126 fig. 5E; S112 table]

La raíz interna de Holozoa permanece sin resolver porque matrices con alto soporte de concatenación muestran baja concordancia génica y de sitios. [C-639; S126 Results; fig. 5]

## 4.8. Circunscripciones rivales en el extremo del corredor

### 4.8.1. Choanozoa sensu histórico, Choanozoa sensu stricto y Apoikozoa

La Choanozoa histórica de Cavalier-Smith reunió protistas opisthokontos y excluyó animales, por lo que era parafilética respecto de Metazoa. [C-640; S125 clasificación; S130 introducción]

Brunet y King emplearon Choanozoa para el clado Choanoflagellata+Metazoa. [C-641; S134 glosario; definición]

Budd y Jensen propusieron Apoikozoa para el clado Metazoa+Choanoflagellata. [C-642; S135 resumen]

Adl et al. 2019 prefirieron Choanozoa y consideraron inadecuada la etimología de Apoikozoa. [C-643; S01 nota de Choanozoa]

Choanozoa sensu stricto y Apoikozoa tienen la misma circunscripción pretendida en las fuentes citadas, pero no son equivalentes a Choanozoa sensu histórico. [C-644; S01; S134; S135]

### 4.8.2. Pluriformea, Corallochytrea y Corallochytrium

Corallochytrium es un género y Corallochytrea es el nombre de un linaje que lo contiene según la clasificación adoptada. [C-645; S01 clasificación; S129 fig. 1]

Hehenberger et al. definieron Pluriformea para Syssomonas+Corallochytrium en su muestreo. [C-646; S129 resumen; fig. 1]

Pluriformea sensu Hehenberger et al. contiene Corallochytrea y no es sinónimo automático de Corallochytrea. [C-647; S129 fig. 1; S01 clasificación]

Liu et al. emplearon “Pluriformea/Corallochytrea” y después “Pluriformea” como una abreviación operacional de su muestreo. [C-648; S126 Methods; fig. 2; sin localizar]

Pluriformea, Corallochytrea y Corallochytrium deben conservarse como entidades separadas en el corpus. [C-649; n/a; derivación documental de C-645–C-648]

## 4.9. Qué permanece sin resolver

La posición exacta de la raíz eucariota permanece discutida entre raíces Opimoda(+)-Diphoda(+), excavadas y Opisthokonta. [C-650; S102; S103; S104; S105; S106; S107]

La relación exacta de Ancyromonadida y Malawimonadida con CRuMs y Amorphea permanece sensible al método. [C-651; S108; S109; S115]

El orden interno temprano de Obazoa ha cambiado con la incorporación de nuevos taxones. [C-652; S111 árbol; S109 árbol]

La raíz interna de Holozoa unicelular permanece sin resolver. [C-653; S126 fig. 5]

No se localizó una sinapomorfía morfológica publicada exclusiva para varios nodos filogenómicos del corredor. [C-654; BN-020; BN-024; BN-027; BN-028]

Las edades nodales de Opisthokonta, Holomycota y Holozoa citadas proceden de un único marco de reloj y no constituyen consenso. [C-655; S126 Methods; fig. 3]

## 4.10. Registro de afirmaciones de la sección 4

> **Registro de afirmaciones:** [data/afirmaciones/04.csv](../data/afirmaciones/04.csv) (262 filas; 12 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---

# 5. El registro material: fósiles y biomarcadores

## 5.1. Criterios de reconocimiento y límites de los acritarcos

«Acritarco» designa una categoría artificial de microfósiles orgánicos de afinidad biológica incierta y no un clado. [C-667; S152 §2]

La ornamentación compleja, los procesos huecos, las aberturas de excistamiento y una pared multicapa aumentan la probabilidad de afinidad eucariota, pero ningún carácter aislado es universalmente diagnóstico. [C-668; S151 resultados; S152 §2]

El tamaño de una vesícula por sí solo no permite asignarla con seguridad a Eukaryota. [C-669; S152 §2]

La microscopía electrónica de transmisión puede revelar capas de pared y organización submicrométrica no visibles con microscopía óptica. [C-670; S151 métodos y figs. 2–7]

La química orgánica de la pared puede apoyar una afinidad biológica, pero la alteración térmica y la diagénesis limitan su especificidad. [C-671; S151 discusión; S161 métodos]

## 5.2. Roper, Ruyang y otros registros de pared orgánica

La sucesión del Grupo Roper está constreñida por edades U–Pb y Re–Os entre aproximadamente 1492 ± 4 Ma y 1361 ± 21 Ma. [C-672; S150 §Geological setting]

Tappania plana del Grupo Roper presenta procesos ramificados y morfologías que fueron interpretadas como crecimiento eucariota complejo. [C-673; S150 descripción sistemática; S152 fig. 2]

Valeria lophostriata posee estriaciones concéntricas regulares en la pared de la vesícula. [C-674; S150 descripción sistemática; S153 fig. 2]

Las estriaciones de Valeria lophostriata apoyan una afinidad eucariota, pero no resuelven su posición dentro del grupo corona. [C-675; S150 discusión]

Dictyosphaera y Shuiyousphaeridium del Grupo Ruyang presentan ornamentación y organización de pared usadas para proponer afinidad eucariota. [C-676; S151 resultados; S152 §2]

La edad del conjunto Ruyang está acotada de forma más amplia y menos directa que la del Grupo Roper. [C-677; S150 discusión estratigráfica]

Qingshania magnifica procede de la Formación Chuanlinggou, datada en aproximadamente 1.63 Ga. [C-678; S154 resumen y §Geological setting]

Qingshania magnifica forma filamentos uniseriados compuestos por células de hasta 250 µm de diámetro. [C-679; S154 resumen; fig. 2]

Miao y colaboradores interpretaron Qingshania magnifica como un eucariota multicelular, sin asignarlo con seguridad a un grupo corona viviente. [C-680; S154 discusión]

## 5.3. Candidatos antiguos y discutidos

Grypania spiralis fue interpretada como un alga eucariota macroscópica en la Formación de Hierro Negaunee de aproximadamente 2.1 Ga. [C-681; S155 resumen]

La atribución eucariota de Grypania spiralis es cuestionada porque su morfología no aporta una sinapomorfía celular inequívoca. [C-682; S152 §3]

Rafatazmia chitrakootensis fue descrita en la Dolomía Tirohan de la cuenca Vindhyan y se le atribuyó una edad aproximada de 1.6 Ga. [C-683; S156 resumen y §Geological setting]

Bengtson y colaboradores interpretaron Rafatazmia chitrakootensis como una rodófita del grupo corona. [C-684; S156 título; discusión]

La asignación de Rafatazmia chitrakootensis a Rhodophyta corona es cuestionada por la ausencia de caracteres reproductivos inequívocos y por incertidumbres estratigráficas. [C-685; S152 discusión; S178 §fossil record]

## 5.4. Microfósiles con forma de vasija (*vase-shaped microfossils*, VSM) y daño por perforación

Los microfósiles con forma de vasija del Grupo Chuar fueron comparados con amebas testadas modernas y se interpretan habitualmente dentro de Amoebozoa o su grupo total. [C-686; S157 resumen y discusión]

Las unidades portadoras de perforaciones estudiadas por Porter en el Grupo Chuar se sitúan entre 780 y 740 Ma. [C-687; S158 título; §Geological setting]

Porter midió perforaciones circulares de 0.1–3.4 µm en siete especies de microfósiles orgánicos del Grupo Chuar. [C-688; S158 resultados; tabla 1]

La regularidad, distribución taxonómica y semejanza con perforaciones de protistas vampirélidos apoyan una interpretación de depredación por perforación. [C-689; S158 discusión]

La diagénesis, el daño post mortem y la preparación fueron evaluados como explicaciones alternativas para las perforaciones del Grupo Chuar. [C-690; S158 discusión]

Algunos microfósiles con forma de vasija presentan perforaciones aproximadamente semicirculares o circulares de 15–35 µm. [C-691; S158 discusión; material comparativo]

No se ha identificado taxonómicamente al organismo que produjo las perforaciones del Grupo Chuar. [C-692; S158 discusión]

## 5.5. Fósiles con relevancia directa para el corredor

Bangiomorpha pubescens presenta filamentos multicelulares con diferenciación basal y patrones de división comparados con bangiales vivientes. [C-693; S159 descripción; figs. 4–9]

Butterfield interpretó etapas reproductivas diferenciadas de Bangiomorpha pubescens como evidencia de reproducción sexual. [C-694; S159 discusión]

La sucesión que contiene Bangiomorpha pubescens fue datada en aproximadamente 1.047 Ga. [C-695; S160 resumen]

Bangiomorpha pubescens funciona como calibración mínima para divergencias eucariotas solo si se acepta su asignación a Rhodophyta corona. [C-696; S160 discusión; S141 §calibrations]

Ourasphaira giraldae procede de la Formación Grassy Bay y está acotada aproximadamente entre 1010 y 890 Ma. [C-697; S161 resumen; métodos]

Loron y colaboradores interpretaron Ourasphaira giraldae como un hongo sobre la base de morfología, ultraestructura y espectroscopía. [C-698; S161 resumen; figs. 1–3]

La afinidad fúngica de Ourasphaira giraldae no permite asignarla con seguridad a Fungi corona ni fechar por sí sola Opisthokonta corona. [C-699; S161 discusión; S178 §fossil record]

Bicellum brasieri procede de depósitos lacustres de la Formación Diabaig de aproximadamente 1.0 Ga. [C-700; S162 resumen; §Geological setting]

Bicellum brasieri conserva una masa interna de células isodiamétricas rodeada por una capa de células alargadas. [C-701; S162 resultados; figs. 1–3]

Strother y colaboradores consideraron que Bicellum brasieri es más consistente con una afinidad holozoa que con un alga de pared rígida. [C-702; S162 discusión]

Los autores de Bicellum brasieri indicaron que no podían excluir por completo paredes celulares delgadas y flexibles. [C-703; S162 discusión: «cannot entirely rule out thin, flexible cell walls»]

## 5.6. Doushantuo y Weng’an: embriones, quistes y desarrollo holozoo

La Formación Doushantuo fue depositada aproximadamente entre 635 y 551 Ma según dataciones U–Pb de circones en niveles volcánicos. [C-704; S168 resumen]

Una capa tobácea inmediatamente sobre el fosforito superior de Weng’an dio una edad SIMS U–Pb de 609 ± 5 Ma. [C-705; S169 resumen]

Tianzhushania y formas del ciclo Megasphaera fueron interpretadas históricamente como embriones animales por sus divisiones palintómicas. [C-706; S166 introducción; S168 contexto]

Huldtgren y colaboradores reinterpretaron fósiles de Tianzhushania como protistas holozoos enquistantes con núcleos fosilizados y estructuras de germinación. [C-707; S163 título; resultados]

Chen y colaboradores interpretaron estructuras internas de fósiles tipo Megasphaera como diferenciación celular y separación germen–soma. [C-708; S166 resumen; figs. 2–4]

La interpretación de diferenciación germen–soma en fósiles tipo Megasphaera cuestiona una identificación exclusiva como protista unicelular enquistante. [C-709; S166 discusión]

Moczydłowska y colaboradores propusieron afinidades algales para varios acritarcos de Doushantuo, incluido material relacionado con Tianzhushania. [C-710; S167 resumen y discusión]

Caveasphaera muestra una secuencia de desarrollo con redistribución celular que fue comparada con embriología animal. [C-711; S164 resultados; fig. 3]

La posición filogenética de Caveasphaera no está resuelta entre un holozoo no animal y un linaje relacionado con animales. [C-712; S164 discusión]

Helicoforamina fue interpretada como holozoo mediante reconstrucción de etapas de desarrollo, pero su posición dentro de Holozoa permanece indeterminada. [C-713; S165 título; discusión]

## 5.7. Biomarcadores

Los esteranos y hopanos reportados en rocas arcaicas fueron reinterpretados por Rasmussen y colaboradores como contaminantes introducidos después de la litificación. [C-714; S170 resumen; figs. 1–3]

La reinterpretación de los biomarcadores arcaicos retiró ese conjunto como evidencia segura de eucariotas arcaicos. [C-715; S170 discusión]

La biota de protosteroides fue inferida a partir de productos diagenéticos de esteroles ancestrales abundantes en rocas mesoproterozoicas. [C-716; S171 resumen; figs. 1–4]

Brocks y colaboradores interpretaron la biota de protosteroides como eucariotas del grupo tronco ecológicamente abundantes antes del ascenso de esteroles modernos de grupos corona. [C-717; S171 discusión]

El 24-isopropilcolestano fue propuesto como biomarcador de demosponjas del Criogénico. [C-718; S172 resumen]

La presencia de precursores y productos equivalentes en Rhizaria unicelulares cuestiona la especificidad animal del 24-isopropilcolestano. [C-719; S174 resumen]

La genómica comparada de esponjas apoya la capacidad biosintética necesaria para producir esteroles C30, pero no demuestra exclusividad frente a otros eucariotas. [C-720; S173 resultados; fig. 2]

Saccharomyces cerevisiae produjo esteroles en experimentos con 7 nM de O₂ disuelto. [C-721; S176 resumen; resultados]

El umbral de 7 nM de O₂ para una levadura no puede convertirse directamente en un valor único de oxígeno atmosférico proterozoico. [C-722; S176 discusión]

## 5.8. Asignación fósil más antigua localizada por nodo

| nodo | fósil más antiguo localizado | edad | método y clase de evidencia | filas | estado de asignación |
| --- | --- | --- | --- | --- | --- |
| Eukaryota, grupo corona | *Bangiomorpha pubescens*, si se acepta la afinidad rodófita de grupo corona | aprox. 1.047 Ga | U–Pb CA-ID-TIMS sobre circón; interpretación morfológica y filogenética separadas | C-693–C-696 | La asignación depende de la afinidad rodófita; no equivale al origen de Eukaryota. |
| Amorphea | NO LOCALIZADO EN ESTA SESIÓN | n/a | Búsqueda bibliográfica de fósiles diagnósticos | C-703 | No se localizó un fósil con sinapomorfía diagnóstica del nodo. |
| Obazoa | NO LOCALIZADO EN ESTA SESIÓN | n/a | Búsqueda bibliográfica de fósiles diagnósticos | C-703 | No se localizó un fósil con sinapomorfía diagnóstica del nodo. |
| Opisthokonta | *Ourasphaira giraldae* como candidato de afinidad fúngica | 1010–890 Ma | Morfología tridimensional y ultraestructura; edad estratigráfica del Grupo Grassy Bay | C-697–C-699 | La afinidad es candidata; no fija por sí sola la edad del grupo corona de Opisthokonta. |
| Holozoa | *Bicellum brasieri* como posible holozoo; *Helicoforamina* como holozoo de posición interna indeterminada | aprox. 1.0 Ga; 609 ± 5 Ma para Weng’an | Morfología y desarrollo preservado; U–Pb SIMS para Weng’an | C-700–C-703; C-705; C-711 | Ninguno resuelve sin ambigüedad la posición exacta dentro de Holozoa. |
| Filozoa | NO LOCALIZADO EN ESTA SESIÓN | n/a | Búsqueda bibliográfica de caracteres diagnósticos | C-703 | No se localizó un fósil asignable al nodo con confianza. |
| Choanozoa *sensu stricto* ≈ Apoikozoa | NO LOCALIZADO EN ESTA SESIÓN | n/a | Búsqueda bibliográfica de caracteres diagnósticos | C-703 | No se localizó un fósil que discrimine el nodo coanoflagelados+animales. |
| Amoebozoa | VSM del Grupo Chuar, interpretados por comparación con amebas testadas | 780–740 Ma | Morfología comparada; posición total o corona no resuelta uniformemente | C-686–C-692 | La afinidad amoebozoa es más fuerte que la asignación a un subclado corona concreto. |
| Holomycota | *Ourasphaira giraldae* como candidato fúngico | 1010–890 Ma | Morfología y ultraestructura | C-697–C-699 | La identificación como hongo temprano sigue siendo una atribución paleobiológica, no una secuencia genómica. |

## 5.9. Registro de afirmaciones de la sección 5

> **Registro de afirmaciones:** [data/afirmaciones/05.csv](../data/afirmaciones/05.csv) (56 filas; 12 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---

# 6. Tiempo: relojes moleculares y desacuerdo con las rocas

## 6.1. Estimaciones publicadas

Douzery y colaboradores estimaron que las principales divergencias eucariotas consideradas en su estudio ocurrieron entre 950 y 1259 Ma. [C-723; S142 resumen]

Douzery y colaboradores estimaron la divergencia entre animales y coanoflagelados entre 761 y 957 Ma. [C-724; S142 resumen; tabla 1]

El análisis de Douzery y colaboradores utilizó un reloj molecular relajado bayesiano y seis referencias fósiles. [C-725; S142 métodos]

Parfrey y colaboradores estimaron la edad de LECA entre 1679 y 1866 Ma. [C-726; S139 resumen; resultados]

Parfrey y colaboradores ampliaron el muestreo de eucariotas microbianos respecto de estudios anteriores. [C-727; S139 métodos]

Eme y colaboradores obtuvieron estimaciones de LECA que abarcaron 1007–1898 Ma entre sus análisis. [C-728; S141 §Molecular clocks; fig. 3]

Eme y colaboradores estimaron Opisthokonta entre 904 y 1579 Ma. [C-729; S141 fig. 3 y material suplementario]

En los análisis de Eme y colaboradores, el intervalo entre LECA y Opisthokonta varió entre 23 y 334 Ma. [C-730; S141 discusión]

Strassert y colaboradores estimaron la edad de LECA entre 1958 y 2386 Ma. [C-731; S140 resumen; fig. 2]

Strassert y colaboradores exploraron más de un modelo de reloj relajado, distribuciones alternativas de calibración y dos posiciones de raíz. [C-732; S140 métodos; Supplementary Data 1]

La corrección publicada para Strassert y colaboradores no fue tratada en esta sesión como una nueva estimación temporal independiente. [C-733; S140 nota editorial]

Betts y colaboradores integraron información genómica y fósil en una escala temporal común para la evolución temprana de la vida. [C-734; S177 resumen y métodos]

Porter sostuvo que no existen fósiles inequívocos asignables a grupos corona de supergrupos eucariotas antes de aproximadamente 1.05 Ga. [C-735; S178 §3]

La posición de un origen tardío de la diversidad eucariota viviente interpreta muchos fósiles paleoproterozoicos y mesoproterozoicos como grupos troncales o de posición indeterminada. [C-736; S178 discusión; S179 resumen]

Un preprint de 2026 propuso un límite mínimo próximo a 1696 Ma para LECA a partir de dinámica de clados. [C-737; S181 resumen]

No existe una estimación de consenso para la edad de LECA. [C-738; S139 resultados; S141 fig. 3; S140 fig. 2; S178 discusión]

Las estimaciones recuperadas para LECA en esta parte abarcan desde 1007 Ma hasta 2386 Ma. [C-739; S141 fig. 3; S140 fig. 2]

El rango recuperado para LECA tiene una amplitud de 1379 Ma. [C-740; S141 fig. 3; S140 fig. 2]

| estudio | magnitud | intervalo publicado | modelo o enfoque | calibración | filas |
| --- | --- | --- | --- | --- | --- |
| Douzery et al. 2004 | principales divergencias eucariotas | 950–1259 Ma | reloj molecular relajado; proteínas concatenadas | calibraciones fósiles del estudio | C-723–C-726 |
| Douzery et al. 2004 | Choanoflagellata–Metazoa | 761–957 Ma | reloj molecular relajado | calibraciones fósiles del estudio | C-724–C-726 |
| Parfrey et al. 2011 | LECA | 1679–1866 Ma | relojes multigénicos; muestreo ampliado de protistas | calibraciones mínimas y máximas explícitas | C-727–C-729 |
| Eme et al. 2014 | LECA | 1007–1898 Ma | comparación de análisis de reloj | múltiples esquemas de calibración | C-730–C-732 |
| Eme et al. 2014 | Opisthokonta | 904–1579 Ma | comparación de análisis de reloj | múltiples esquemas de calibración | C-731–C-732 |
| Eme et al. 2014 | duración del tallo eucariota en escenarios considerados | 23–334 Ma | diferencia entre edades inferidas de eventos delimitadores | dependiente del escenario y calibración | C-732 |
| Strassert et al. 2021 | LECA | 1958–2386 Ma | reloj relajado con muestreo filogenómico | calibraciones fósiles y priors del estudio | C-733–C-736 |
| Betts et al. 2018 | origen/divergencia temprana de Eukaryota | intervalos dependientes del análisis; conservar fuente | integración de datos genómicos y fósiles | calibraciones probabilísticas | C-737–C-738 |
| Chernikova et al. 2011 | radiación de diversidad eucariota viviente | posición tardía relativa | cambios genómicos raros y reloj | calibraciones del estudio | C-739 |
| Berney y Pawlowski 2006 | diversificación eucariota | cronología recalibrada | reloj molecular y registro continuo de microfósiles | microfósiles seleccionados | C-740 |

## 6.2. El peso de *Bangiomorpha*

Bangiomorpha pubescens ejerce un peso desproporcionado como calibración porque combina una edad radiométrica relativamente precisa con una posible asignación a Rhodophyta corona. [C-741; S160 discusión; S141 §calibrations; S140 métodos]

Mover el nodo asignado a Bangiomorpha o tratarlo como fósil troncal modifica las restricciones mínimas de divergencias profundas. [C-742; S141 §calibration sensitivity; S178 discusión]

## 6.3. Por qué no existe una edad de consenso

Una calibración fósil suele aportar un mínimo para la edad de un nodo, no la fecha exacta de la divergencia. [C-743; S141 §Molecular clock methodology]

Los límites máximos de calibración son más difíciles de justificar porque dependen de ausencia fósil y de modelos de preservación. [C-744; S141 §Molecular clock methodology; S177 métodos]

Los relojes estrictos suponen una tasa única, mientras que los relojes relajados permiten variación de tasa entre ramas. [C-745; S142 métodos; S141 §Molecular clocks]

Los relojes relajados autocorrelacionados y no autocorrelacionados hacen supuestos incompatibles sobre la dependencia de tasas entre ramas adyacentes. [C-746; S141 §Molecular clocks; S140 métodos]

La saturación de sustituciones reduce la información temporal retenida en divergencias proterozoicas profundas. [C-747; S141 discusión]

La heterotaquia puede hacer que un mismo sitio cambie de tasa a través del árbol y sesgar estimaciones si el modelo no la representa. [C-748; S141 discusión; S140 métodos]

La ausencia de un grupo externo cercano a Eukaryota dificulta simultáneamente la raíz y la datación de divergencias profundas. [C-749; S141 discusión; S177 métodos]

La propuesta de conciliación entre fósiles jóvenes y relojes antiguos sostiene que buena parte del registro proterozoico temprano pertenece al grupo tronco y no al grupo corona. [C-750; S171 discusión; S178 §4]

## 6.4. Nodos sin intervalo comparable localizado

Las estimaciones nodales de Amorphea, Obazoa, Holozoa y Filozoa no fueron localizadas con intervalos comparables en una misma matriz durante esta sesión. [C-751; sin localizar]

## 6.5. Registro de afirmaciones de la sección 6

> **Registro de afirmaciones:** [data/afirmaciones/06.csv](../data/afirmaciones/06.csv) (29 filas; 12 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---

# 7. Ambiente

## 7.1. Oxígeno: cronología, proxies y discrepancias cuantitativas

La Gran Oxidación produjo una acumulación persistente de oxígeno atmosférico durante el Paleoproterozoico, aproximadamente entre 2.43 y 2.32 Ga según la síntesis de proxies recuperada. [C-752; S194 fig. 1 y texto principal]

La excursión de Lomagundi–Jatuli se sitúa aproximadamente entre 2.22 y 2.06 Ga en la reconstrucción de Bekker y Holland. [C-753; S195 resumen]

Los carbonatos de la excursión Lomagundi–Jatuli alcanzan valores de δ13C positivos de hasta aproximadamente +15‰ en la compilación citada. [C-754; S195 resultados]

La hipótesis de sobreimpulso de oxígeno durante Lomagundi–Jatuli infiere aumento y recuperación posteriores a partir de ciclos de carbono, azufre, hierro y fósforo. [C-755; S195 discusión]

La caída posterior a Lomagundi–Jatuli está respaldada por una reducción de evaporitas sulfáticas, fosforitas y estados de oxidación de lutitas en las compilaciones recuperadas. [C-756; S195 resultados y discusión]

Planavsky y colaboradores infirieron menos de 0.1% del nivel atmosférico presente de O₂ para partes del Mesoproterozoico mediante isótopos de cromo. [C-757; S182 resumen; fig. 3]

Zhang y colaboradores infirieron 4–8% PAL de O₂ para aproximadamente 1.4 Ga mediante un modelo biogeoquímico de la Formación Xiamaling. [C-758; S183 resumen; resultados]

Liu y colaboradores obtuvieron una mejor estimación de aproximadamente 1–2% PAL de O₂ para la edad media de la Tierra mediante termodinámica de anomalías de cerio. [C-759; S184 resumen; fig. 4]

Canfield y colaboradores interpretaron isótopos de cromo altamente fraccionados como evidencia de niveles de O₂ superiores a 4% PAL en parte del Mesoproterozoico. [C-760; S185 resumen y discusión]

Las estimaciones mesoproterozoicas recuperadas de pO₂, desde <0.1% PAL hasta 4–8% PAL, no deben promediarse. [C-761; S182 resumen; S183 resumen; S184 resumen; S185 resumen]

La discrepancia cuantitativa sobre pO₂ mesoproterozoica es empírica y metodológica, no una diferencia de unidades. [C-762; S182 métodos; S183 métodos; S184 métodos; S185 métodos]

La biosíntesis experimental de esteroles a 7 nM de O₂ muestra que ese proceso puede operar en condiciones microóxicas. [C-763; S176 resultados]

El umbral de esteroles no establece el nivel mínimo de O₂ requerido por fagotrofia, mitosis o eucariogénesis completa. [C-764; S176 discusión]

Mills y colaboradores mostraron que algunas esponjas modernas toleran concentraciones de O₂ muy inferiores a las atmosféricas actuales. [C-765; S199 resumen y resultados]

Los experimentos con esponjas no proporcionan un umbral universal para los eucariotas unicelulares del corredor. [C-766; S199 discusión]

| intervalo u organismo | valor | proxy o método | observado/inferido | fuente | fila |
| --- | --- | --- | --- | --- | --- |
| Mesoproterozoico, partes del intervalo | <0.1% PAL O₂ | isótopos de Cr | inferido | S182 resumen; fig. 3 | C-757 |
| aprox. 1.4 Ga, Formación Xiamaling | 4–8% PAL O₂ | modelo biogeoquímico sedimentario | inferido | S183 resumen; resultados | C-758 |
| edad media de la Tierra | aprox. 1–2% PAL O₂ | termodinámica de anomalías de Ce | inferido | S184 resumen; fig. 4 | C-759 |
| parte del Mesoproterozoico | >4% PAL O₂ | fraccionamiento de isótopos de Cr | inferido | S185 resumen y discusión | C-760 |
| cultivo de *Saccharomyces cerevisiae* | 7 nM O₂ | biosíntesis experimental de esteroles | observado | S176 resultados | C-763 |

## 7.2. Química redox del océano

El modelo clásico de Canfield propuso aguas medias euxínicas durante gran parte del Proterozoico. [C-767; S186 tesis general]

Planavsky y colaboradores encontraron evidencia de condiciones anóxicas ferruginosas extendidas en el océano mesoproterozoico. [C-768; S187 resumen; fig. 3]

La evidencia de condiciones ferruginosas extendidas cuestiona un océano mesoproterozoico globalmente euxínico. [C-769; S187 discusión]

Sperling y colaboradores compilaron aproximadamente 4.700 mediciones de especiación de hierro de lutitas entre 2300 y 360 Ma. [C-770; S188 resumen y métodos]

La compilación de Sperling y colaboradores indicó aguas subsuperficiales mesoproterozoicas predominantemente anóxicas y ferruginosas, con mayor tendencia local a euxinia que en el Neoproterozoico. [C-771; S188 resumen]

No existe una fracción global única y publicada de océano óxico, ferruginoso y euxínico válida para todo el Mesoproterozoico. [C-772; S187 discusión; S188 discusión; S189 discusión]

Reinhard y colaboradores interpretaron datos de molibdeno como evidencia de un reservorio marino pequeño y de estasis redox durante parte del Proterozoico medio. [C-773; S189 resumen; fig. 2]

## 7.3. Metales traza y nutrientes

Anbar y Knoll propusieron que la química redox proterozoica restringió la disponibilidad de Mo, Cu y Zn y, por esa vía, rutas metabólicas dependientes de metales. [C-774; S190 tesis general]

Scott y colaboradores usaron concentraciones e isótopos de molibdeno para proponer una oxigenación escalonada del océano proterozoico. [C-775; S191 resumen; fig. 3]

Planavsky y colaboradores reconstruyeron un reservorio de fosfato marino proterozoico menor que el fanerozoico mediante relaciones P/Fe en rocas ricas en óxidos. [C-776; S192 resumen; fig. 2]

La adsorción de fósforo a óxidos de hierro ha sido propuesta como mecanismo de limitación de productividad en océanos proterozoicos. [C-777; S192 discusión; S193 introducción]

Reinhard y colaboradores propusieron una expansión del reservorio marino de fósforo alrededor de 800–700 Ma. [C-778; S193 resumen; fig. 3]

No se localizó en esta sesión una serie cuantitativa única y comparable para Mo, Fe, Cu, Zn, Ni y Co durante todo el Paleoproterozoico, Mesoproterozoico y Neoproterozoico. [C-779; sin localizar]

## 7.4. «Aburrido millardo» y glaciaciones

El término «aburrido millardo» se ha aplicado aproximadamente al intervalo 1.8–0.8 Ga para describir estabilidad tectónica, climática y biogeoquímica relativa. [C-780; S194 discusión; S189 introducción]

La biota de protosteroides cuestiona que el «aburrido millardo» fuera ecológicamente uniforme o pobre en eucariotas. [C-781; S171 discusión]

La glaciación Sturtiana comenzó alrededor de 717 Ma y terminó alrededor de 659 Ma en la cronología criogénica recuperada. [C-782; S196 resultados; S197 fig. 2]

La terminación de la glaciación Marinoana está datada en 635.2 ± 0.6 Ma en la sucesión de Doushantuo. [C-783; S168 resumen]

El inicio de la glaciación Marinoana está menos constreñido que su final y fue situado en las fuentes recuperadas después de aproximadamente 659 Ma y antes de aproximadamente 639 Ma. [C-784; S198 introducción y resultados]

La Formación Doushantuo comienza inmediatamente después de la deglaciación Marinoana en el registro de South China. [C-785; S168 resumen]

No se localizó una estimación única de temperatura media global para el Mesoproterozoico que sea comparable entre proxies y modelos. [C-786; sin localizar]

## 7.5. Hábitat, estructura espacial y densidad

La hipótesis del hidrógeno requiere un entorno anaerobio porque postula transferencia de H₂ entre un simbionte bacteriano y un hospedador arqueano metanógeno. [C-787; S141 §eukaryogenesis context]

Los experimentos de esteroles y los linajes anaerobios actuales muestran que la presencia de rasgos eucariotas no exige un ambiente uniformemente oxigenado. [C-788; S176 discusión; S210 resumen; S211 resumen]

Lenisia limosa fue cultivada a partir de un ambiente marino anóxico y porta epibiontes Arcobacter asociados con transferencia interespecífica de hidrógeno. [C-789; S210 resumen; fig. 2]

Salpingoeca rosetta alterna formas nadadoras, sésiles y coloniales en cultivo, lo que impide asignar un único microhábitat funcional a toda su vida. [C-790; S200 resultados; fig. 7]

Capsaspora owczarzaki fue aislada originalmente en asociación con el caracol dulceacuícola Biomphalaria glabrata y también puede mantenerse en cultivo axénico. [C-791; S206 introducción y métodos]

No se localizó una reconstrucción ancestral cuantitativa y comparable del hábitat para cada nodo desde Eukaryota hasta Choanozoa sensu stricto. [C-792; sin localizar]

No se localizó una estimación publicada de densidad celular para comunidades proterozoicas atribuibles al corredor. [C-793; sin localizar]

No se localizó en esta sesión una escala única de dispersión geográfica para poblaciones de todos los eucariotas microbianos del corredor. [C-794; sin localizar]

## 7.6. Registro de afirmaciones de la sección 7

> **Registro de afirmaciones:** [data/afirmaciones/07.csv](../data/afirmaciones/07.csv) (43 filas; 12 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---

# 8. Ecología y trofismo

## 8.1. Coanoflagelados: alimentación, colonias, rosetas y señales

Los coanoflagelados generan corrientes con el flagelo y capturan bacterias en un collar de microvellosidades. [C-795; S200 introducción; S147 introducción]

Monosiga brevicollis es un coanoflagelado unicelular bacterívoro cuyo genoma contiene aproximadamente 9.200 genes ricos en intrones. [C-796; S147 resumen]

Salpingoeca rosetta presenta al menos cinco formas celulares o coloniales: tecada, nadadora lenta, nadadora rápida, roseta y cadena. [C-797; S200 resultados; fig. 7]

Las rosetas de Salpingoeca rosetta se forman por divisiones celulares seriadas sin separación completa y no por agregación de células inicialmente independientes. [C-798; S200 resultados; películas suplementarias]

La bacteria Algoriphagus machipongonensis induce el desarrollo de rosetas en Salpingoeca rosetta. [C-799; S201 resumen; fig. 1]

El factor RIF-1 de Algoriphagus machipongonensis es un sulfonolípido activo a concentraciones femtomolares, aproximadamente 10^-15 M. [C-800; S201 resumen; resultados]

Salpingoeca rosetta respondió a RIF-1 a lo largo de un intervalo dinámico de nueve órdenes de magnitud en el estudio publicado. [C-801; S201 resumen]

RIF-2 y lisofosfatidiletanolaminas bacterianas pueden potenciar la inducción de rosetas, mientras que IOR-1 puede inhibirla. [C-802; S202 resumen; figs. 2–4]

La respuesta de roseta depende de la combinación de señales bacterianas y no de un único interruptor químico universal. [C-803; S201 discusión; S202 discusión]

Vibrio fischeri secreta EroS, una liasa de condroitina que induce apareamiento en Salpingoeca rosetta. [C-804; S203 resumen; fig. 1]

La enjambrazón de Salpingoeca rosetta comenzó desde 15 minutos después de la exposición a Vibrio fischeri en el experimento publicado. [C-805; S203 resultados; fig. 1]

Dentro de 30 minutos de exposición a Vibrio fischeri se observaron enjambres de Salpingoeca rosetta. [C-806; S203 fig. 1B]

La fusión celular de parejas de Salpingoeca rosetta dentro de los enjambres ocurre en minutos y es seguida por fusión nuclear. [C-807; S203 fig. 1C–D]

La recombinación observada después de la inducción con Vibrio fischeri respalda que el proceso inducido es sexual y no solo agregativo. [C-808; S203 fig. 1E y resultados]

No se localizó una dosis única de EroS que pueda tratarse como umbral universal fuera de las condiciones experimentales del estudio. [C-809; S203 métodos, sin localizar valor único]

Choanoeca flexa forma láminas celulares que invierten rápida y reversiblemente su curvatura ante transiciones de luz a oscuridad. [C-810; S204 resumen; figs. 1–2]

La inversión de Choanoeca flexa ocurre dentro de aproximadamente 30 s en las condiciones publicadas. [C-811; S204 resultados; fig. 2]

La vía de fotopercepción propuesta para Choanoeca flexa incluye una rodopsina–fosfodiesterasa y cGMP como segundo mensajero. [C-812; S204 resultados; fig. 3]

La inhibición de actina o miosina impidió la inversión de Choanoeca flexa en los ensayos publicados. [C-813; S204 fig. 4T]

## 8.2. Filasterea e Ichthyosporea

Capsaspora owczarzaki alterna estadios filopodial adherente, agregativo y quístico. [C-814; S206 resultados; figs. 2–3]

La agregación de Capsaspora owczarzaki reúne células que crecieron por separado y produce material extracelular cohesivo entre ellas. [C-815; S206 resultados; fig. 3D–F]

En las condiciones publicadas, la agregación de Capsaspora owczarzaki fue inducida durante 4–5 días con agitación a 60 rpm. [C-816; S206 métodos, Cell culture conditions]

El estadio quístico de Capsaspora owczarzaki se obtuvo de cultivos de 14 días en el protocolo publicado. [C-817; S206 métodos, Cell culture conditions]

Los ortólogos del adhesoma de integrinas y genes de señalización aumentaron su expresión durante el estadio agregativo de Capsaspora owczarzaki. [C-818; S206 resultados; análisis de RNA-seq]

La transición de Capsaspora owczarzaki entre estadios es reversible a escala de cultivo sin requerir mutaciones fijadas conocidas. [C-819; S206 resultados y métodos]

Ministeria vibrans presenta un flagelo fino y microvellosidades radiales; el supuesto pedúnculo vibrátil de descripciones previas fue reinterpretado. [C-820; S212 resumen]

El estudio ultraestructural de Ministeria vibrans no observó un pedúnculo separado que hiciera vibrar el cuerpo celular. [C-821; S212 resumen]

Sphaeroforma arctica crece como coenocito y alcanza hasta 128 núcleos antes de la celularización. [C-822; S207 resumen; resultados]

Las divisiones nucleares de Sphaeroforma arctica ocurren sincrónicamente a intervalos regulares de 11–12 h en las condiciones publicadas. [C-823; S207 resultados]

La celularización de Sphaeroforma arctica depende de actomiosina y genera una capa de células polarizadas. [C-824; S208 resumen; figs. 2–6]

La ruta cenocítica de Sphaeroforma arctica separa temporalmente crecimiento nuclear y compartimentación celular. [C-825; S207 discusión; S208 discusión]

Creolimax fragrantissima forma un coenocito multinucleado y libera células ameboides uninucleadas después de la compartimentación. [C-826; S209 resumen y resultados]

La regulación transcripcional y el empalme alternativo difieren entre estadios de Creolimax fragrantissima. [C-827; S209 resultados]

## 8.3. Depredadores holozoos, Obazoa, Holomycota y Amoebozoa

Pigoraptor vietnamica, Pigoraptor chileana y Syssomonas multiformis consumen presas eucariotas grandes. [C-828; S129 resumen; S132 resultados]

Syssomonas multiformis puede formar agregados transitorios y participar en alimentación conjunta sobre una misma presa. [C-829; S132 resultados; figs. 4–6]

Syssomonas multiformis presenta fusiones celulares parciales y estructuras sincitiales transitorias en condiciones de cultivo ricas. [C-830; S132 resultados; discusión]

Tunicaraptor unikontum mide aproximadamente 3–5 µm y depreda otros eucariotas. [C-831; S131 resumen]

Tunicaraptor unikontum emplea una estructura alimentaria transitoria semejante a una boca para capturar presas eucariotas. [C-832; S131 resumen; figs. morfológicas]

La posición de Tunicaraptor unikontum dentro de Holozoa cambia entre análisis y no está resuelta. [C-833; S131 discusión; S129 filogenias]

Lenisia limosa porta epibiontes Arcobacter oxidadores de hidrógeno. [C-834; S210 resumen; fig. 1]

Lenisia limosa produce H₂ mediante una hidrogenasa de fusión dependiente de NADH y Arcobacter consume ese H₂. [C-835; S210 fig. 2; discusión]

La asociación Lenisia–Arcobacter beneficia a ambos socios en las condiciones anóxicas estudiadas. [C-836; S210 resumen; discusión]

Lenisia limosa con Arcobacter es un análogo actual de una asociación sintrófica externa, no evidencia directa de la asociación que participó en eucariogénesis. [C-837; S210 discusión]

Pygsuia biforma usa rodoquinona en un orgánulo relacionado con la mitocondria bajo hipoxia. [C-838; S211 resumen; resultados]

El gen rquA de Pygsuia biforma fue adquirido por transferencia génica horizontal según su filogenia. [C-839; S211 filogenia; discusión]

Fonticula alba forma cuerpos fructíferos por agregación de células previamente independientes. [C-840; S213 resultados y discusión]

La multicelularidad agregativa de Fonticula alba surgió independientemente de la de Capsaspora owczarzaki y Dictyostelium discoideum en la filogenia disponible. [C-841; S206 discusión; S213 filogenia; S215 introducción]

Rozella allomycis es un parásito intracelular de Allomyces. [C-842; S214 introducción y resultados]

Cryptomycota y Microsporidia comparten señales filogenómicas de parentesco y rasgos asociados con parasitismo. [C-843; S214 resumen; filogenias]

La reducción genómica extrema y los mitosomas de Microsporidia son especializaciones secundarias de parásitos obligados. [C-844; S214 discusión]

En quimeras de Dictyostelium discoideum, algunos genotipos contribuyen desproporcionadamente a esporas y explotan la contribución al tallo de otros genotipos. [C-845; S215 resultados]

La vía agregativa crea oportunidades de conflicto porque reúne células con parentesco menor que una colonia clonal derivada de una sola célula. [C-846; S206 discusión; S215 discusión]

| organismo | ecología documentada | alimentación | hospedador o socio | ciclo/forma | aporte al corredor | filas |
| --- | --- | --- | --- | --- | --- | --- |
| *Monosiga brevicollis* | marino; vida libre | bacterivoría por filtración | sin hospedador obligado documentado aquí | unicelular | genoma y aparato alimentario coanoflagelado | C-795–C-796 |
| *Salpingoeca rosetta* | marino; cultivo con bacterias | bacterivoría por filtración | sin hospedador obligado | formas tecada, nadadoras, roseta y cadena; apareamiento inducible | rosetas clonales y señales bacterianas | C-797–C-809 |
| *Choanoeca flexa* | marino; colonias laminares | filtración bacteriana, no cuantificada aquí | sin hospedador obligado | lámina celular reversible | inversión colectiva regulada por luz | C-810–C-813 |
| *Capsaspora owczarzaki* | asociado históricamente con caracol dulceacuícola; cultivo axénico | nutrición no cuantificada en esta parte | *Biomphalaria glabrata* en aislamiento original | filopodial, agregado y quiste | multicelularidad agregativa y expresión diferencial | C-791; C-814–C-819 |
| *Ministeria vibrans* | medio acuático; cultivo descrito | bacterivoría no cuantificada aquí | sin hospedador localizado | célula con microvellosidades y flagelo fino | revisión del supuesto pedúnculo | C-820–C-821 |
| *Sphaeroforma arctica* | ictiospóreo cultivado | osmotrofia inferida en cultivo; tasa no localizada | sin hospedador en el experimento citado | crecimiento cenocítico y celularización | ruta cenocítica multicelular | C-822–C-825 |
| *Creolimax fragrantissima* | ictiospóreo cultivado | nutrición no cuantificada aquí | sin ficha de hospedador completa localizada | coenocito y células ameboides | regulación por estadio | C-826–C-827 |
| *Syssomonas multiformis* | vida libre; cultivo | depredación de eucariotas | sin hospedador obligado | agregados, alimentación conjunta y fusiones parciales | depredación cooperativa transitoria | C-828–C-830 |
| *Pigoraptor vietnamica* y *P. chileana* | vida libre; cultivo | depredación de eucariotas | sin hospedador obligado | células depredadoras | diversidad de holozoos fagotróficos | C-828 |
| *Tunicaraptor unikontum* | vida libre; marino | depredación de eucariotas | sin hospedador obligado | estructura alimentaria transitoria | depredador holozoo de posición discutida | C-831–C-833 |
| *Lenisia limosa* | marino anóxico | metabolismo productor de H₂; asociación sintrófica | epibiontes *Arcobacter* | asociación externa estable en cultivo | análogo actual de sintrofía externa | C-789; C-834–C-837 |
| *Pygsuia biforma* | hipóxico/anóxico | metabolismo de rodoquinona | sin hospedador obligado localizado | orgánulo relacionado con mitocondria | adaptación anaerobia mediante HGT | C-838–C-839 |
| *Fonticula alba* | terrestre/microbiano; detalle ecológico no compilado | alimentación no cuantificada aquí | sin hospedador obligado | agregación y cuerpo fructífero | multicelularidad agregativa independiente | C-840–C-841 |
| *Rozella allomycis* | interior de hongo acuático | parasitismo intracelular | *Allomyces* | ciclo parasítico | parasitismo holomicota | C-842 |
| Microsporidia | intracelular | parasitismo obligado | múltiples animales y protistas según linaje; no desglosado aquí | mitosomas y reducción genómica | especialización secundaria | C-843–C-844 |
| *Dictyostelium discoideum* | suelo | bacterivoría durante crecimiento; socialidad al hambre | sin hospedador | agregación y cuerpo fructífero | conflicto y trampa social | C-845–C-846 |

## 8.4. Depredación observada, hipótesis causal y magnitudes tróficas

Las perforaciones del Grupo Chuar constituyen observación fósil de daño compatible con depredación, pero no identifican al depredador. [C-847; S158 resultados y discusión]

La ornamentación y las paredes resistentes de algunos acritarcos han sido interpretadas como defensas frente a depredadores, pero esa función no puede observarse directamente en el fósil. [C-848; S152 discusión; S158 discusión]

La hipótesis de una escalada depredador–presa proterozoica predice aumento de tamaño, ornamentación y blindaje junto con señales de ataque. [C-849; S158 discusión; S178 §ecology]

La ausencia de covariación temporal entre daño, tamaño y estructuras defensivas debilitaría la hipótesis de escalada depredador–presa. [C-850; S158 discusión]

Hansen y colaboradores encontraron una relación lineal depredador:presa óptima de aproximadamente 3:1 para flagelados distintos de dinoflagelados en su compilación. [C-851; S224 resumen]

La misma compilación informó relaciones lineales óptimas de 1:1 para un dinoflagelado y 8:1 para ciliados. [C-852; S224 resumen]

Las relaciones de tamaño de protistas modernos no permiten estimar sin datos adicionales el tamaño del depredador que perforó microfósiles del Grupo Chuar. [C-853; S158 discusión; S224 discusión]

No se localizaron tasas de ingestión o aclaramiento comparables para todos los apusomonádidos, breviados, filastereos e ictiospóreos solicitados. [C-854; sin localizar]

## 8.5. Virus y elementos móviles

La lisis viral desvía materia celular hacia materia orgánica disuelta y nutrientes reutilizables por microorganismos, proceso denominado bucle viral (viral loop). [C-855; S216 tesis general]

No existe una tasa publicada localizada de mortalidad viral para comunidades eucariotas proterozoicas. [C-856; sin localizar]

Rambo y colaboradores reconstruyeron seis genomas de virus de ADN bicatenario de hasta 117 kb asociados con Lokiarchaeota y Helarchaeota. [C-857; S217 resumen]

La evidencia de virus de Asgard procede de metagenomas y no de partículas aisladas infectando cultivos asgard. [C-858; S217 métodos y discusión]

Medusavirus es un virus gigante de ADN aislado de agua termal que infecta Acanthamoeba castellanii. [C-859; S222 resumen]

Los virus gigantes aportan homologías y maquinarias complejas al debate sobre el origen del núcleo, pero no demuestran que el núcleo descienda de un virus. [C-860; S222 discusión; S223 discusión]

Los tamaños genómicos y morfologías de mimivirus, pandoravirus, medusavirus y pitovirus no fueron compilados con valores auditables en esta sesión. [C-861; sin localizar]

Cohen y colaboradores demostraron que la señalización bacteriana por GMP–AMP cíclico protege frente a infección por fagos. [C-862; S218 resumen]

La relación entre sistemas bacterianos cGAS-like y cGAS–STING eucariota es homóloga a nivel de componentes, pero las vías completas no son idénticas. [C-863; S218 discusión]

Las viperinas procariotas producen nucleótidos antivirales y protegen contra fagos. [C-864; S219 resumen; resultados]

Bernheim y colaboradores interpretaron la viperina eucariota como derivada de una familia bacteriana y arqueana de proteínas antivirales. [C-865; S219 discusión]

La Argonaute de Thermus thermophilus usa guías de ADN para interferir con ADN invasor. [C-866; S220 resumen; resultados]

La homología entre Argonautas procariotas y eucariotas no implica que el sistema completo de ARN de interferencia existiera en procariotas. [C-867; S220 discusión]

La hipótesis de invasión de intrones propone que intrones de grupo II del endosimbionte contribuyeron al origen de intrones espliceosomales y de la compartimentación núcleo–citosol. [C-868; S221 tesis general]

No se localizó en esta sesión una cadena de evidencia única que conecte intrones de grupo II, telomerasa, telómeros y cromosomas lineales como un solo evento. [C-869; sin localizar]

## 8.6. Respuesta reversible y cambio heredable

La formación de rosetas, el apareamiento inducido, la inversión de Choanoeca flexa, la agregación de Capsaspora y la celularización de Sphaeroforma son respuestas del ciclo vital observadas sin selección de nuevas mutaciones. [C-870; S200 resultados; S201 resultados; S203 resultados; S204 resultados; S206 resultados; S208 resultados]

La reversibilidad está demostrada directamente para la inversión lumínica de Choanoeca flexa. [C-871; S204 figs. 1G–H y 2]

La reversibilidad completa tras retirar RIF-1, EroS o las condiciones de agregación no fue localizada con una cinética comparable para todos los casos. [C-872; sin localizar]

No se localizaron costes energéticos directos, en unidades comunes, para rosetas de Salpingoeca, agregados de Capsaspora o coenocitos de Sphaeroforma. [C-873; sin localizar]

Ichthyophonus hoferi, Abeoforma, Pirum, Entamoeba, Pelomyxa y Mastigamoeba no recibieron en esta parte una ficha ecológica completa con fuente primaria localizada. [C-874; sin localizar]

La distribución actual de fagotrofia, osmotrofia y parasitismo dentro de Opisthokonta es compatible con múltiples cambios de modo trófico y no con una escala lineal de complejidad. [C-875; S200 introducción; S129 resumen; S210 resumen; S214 discusión]

## 8.7. Registro de afirmaciones de la sección 8

> **Registro de afirmaciones:** [data/afirmaciones/08.csv](../data/afirmaciones/08.csv) (81 filas; 12 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---

# 9. Asociación: el catálogo de desenlaces

## 9.0. Distinciones operativas

Una endosimbiosis se define por la localización de un organismo dentro de otro y no por que la interacción sea beneficiosa para ambos. [C-876; S230 tesis general; S240 introducción; expresa]

Simbiosis incluye mutualismo, comensalismo y parasitismo en su uso biológico amplio. [C-877; S230 tesis general; S267 introducción; expresa]

Transmisión vertical designa el paso del socio a la descendencia del hospedador. [C-878; S229 definición; expresa]

Transmisión horizontal designa la adquisición del socio desde otros hospedadores o desde el ambiente. [C-879; S229 definición; S268 introducción; expresa]

Transferencia génica endosimbiótica designa el movimiento de ADN desde un endosimbionte u orgánulo hacia el genoma del hospedador. [C-880; S282 tesis general; expresa]

La transferencia génica horizontal no exige que el donante sea un endosimbionte estable. [C-881; S291 introducción; S293 tesis general; sintesis(C-880)]

Dependencia, transmisión, reducción genómica, transferencia de genes e importación de proteínas son dimensiones separables de una asociación. [C-882; S228 resultados; S230 revisión; S246 resultados; sintesis(C-878, C-879, C-880)]

No existe un único umbral universalmente aceptado que transforme toda endosimbiosis en orgánulo. [C-883; S242 discusión; S246 discusión; S282 revisión; expresa]

La tipología de esta sección ordena desenlaces observados sin tratarlos como una secuencia obligatoria. [C-884; n/a; glosa]

## 9.1. Tipología cerrada y numerada de desenlaces

El contacto sin consecuencia detectable es un desenlace operacional basado en una hipótesis nula y rara vez constituye el resultado principal publicado. [C-885; n/a; BN-037; glosa]

No se localizó en esta sesión un caso experimental del corredor publicado específicamente como contacto sin consecuencia. [C-886; BN-037; glosa]

Lenisia limosa fagocita bacterias del género Alteromonas. [C-887; S210 fig. 1 y microscopía; expresa]

Microsporidia son parásitos intracelulares obligados de otros eucariotas. [C-888; S269 resumen; expresa]

Hatena arenicola adquiere temporalmente una célula de Nephroselmis por ingestión. [C-889; S249 resultados; S250 resultados; expresa]

La asociación Lenisia limosa–Arcobacter se mantiene en cultivo pero no tiene transmisión vertical demostrada. [C-890; S210 resultados; S225 resultados; sintesis(C-878, C-879)]

Algunos metanógenos de ciliados anaerobios persisten durante división celular y estadios de quiste. [C-891; S236 resultados; expresa]

Buchnera aphidicola y los áfidos mantienen una dependencia nutricional obligada. [C-892; S266 tesis general; expresa]

Paulinella chromatophora posee genes de origen cromatofórico en el núcleo y dirige proteínas de vuelta al cromatóforo. [C-893; S243 resultados; S244 resultados; expresa]

Los nucleomorfos son núcleos reducidos de algas incorporadas por endosimbiosis secundaria. [C-894; S258 introducción; S259 resumen; expresa]

Monocercomonoides exilis perdió por completo el orgánulo derivado de la mitocondria. [C-895; S275 resumen; S276 resultados; expresa]

No se localizó un caso inequívoco en que un endosimbionte obligado y genómicamente reducido recuperara una existencia libre autónoma. [C-896; BN-038; glosa]

### 9.1.1. Tipología cerrada

| n.º | desenlace | caso documentado | qué mantiene o limita el estado | transmisión o heredabilidad | # |
| --- | --- | --- | --- | --- | --- |
| 1 | contacto sin consecuencia | NO LOCALIZADO EN ESTA SESIÓN | La ausencia de efecto solo puede acotarse al ensayo realizado. | no determinada | C-885–C-886; BN-037 |
| 2 | depredación o consumo | *Lenisia limosa* consume *Alteromonas* | Captura y fagocitosis observadas. | no heredable | C-887 |
| 3 | parasitismo | Microsporidia en hospedadores eucariotas | Dependencia intracelular del parásito y explotación del hospedador. | transmisión variable según especie | C-888 |
| 4 | asociación transitoria facultativa | *Hatena arenicola*–*Nephroselmis* | Readquisición ambiental después de reparto asimétrico. | vertical incompleta y horizontal | C-889; C-966–C-971 |
| 5 | asociación estable no heredable | *Lenisia limosa*–*Arcobacter* | Eliminación de equivalentes reductores y mejora metabólica; herencia no demostrada. | no demostrada | C-890; C-897–C-910 |
| 6 | endosimbiosis con transmisión vertical | metanógenos de ciliados anaerobios | Persistencia durante división y quistes en los taxones estudiados. | vertical y, a escala amplia, mixta | C-891; C-926–C-931 |
| 7 | dependencia mutua obligada | áfidos–*Buchnera aphidicola* | Nutrición complementaria, transmisión materna y pérdida de autonomía. | vertical materna | C-892; C-1000–C-1006 |
| 8 | integración con transferencia al hospedador | *Paulinella chromatophora*–cromatóforo | EGT, compensación por HGT e importación de proteínas. | vertical en el linaje fotosintético | C-893; C-947–C-957 |
| 9 | reducción extrema u orgánulo derivado | nucleomorfos; nitroplasto UCYN-A | Control del hospedador, genomas reducidos o importación proteica. | heredable | C-894; C-958–C-965; C-986–C-991 |
| 10 | degradación o pérdida | *Monocercomonoides exilis* | Sustitución de ISC por SUF y pérdida total del MRO detectable. | pérdida fijada en el linaje | C-895; C-1050–C-1053 |
| 11 | ruptura con recuperación de vida libre | NO LOCALIZADO EN ESTA SESIÓN | Se documentaron reemplazo o pérdida, no recuperación autónoma del mismo simbionte reducido. | n/a | C-896; C-1107; BN-038 |

## 9.2. Asociación externa y sintrofía

Lenisia limosa es un breviado anaerobio cultivado con epibiontes de Arcobacter. [C-897; S210 resumen y resultados; expresa]

Microscopía electrónica mostró células de Arcobacter conectadas a Lenisia limosa por estructuras semejantes a pili. [C-898; S210 fig. 1 y microscopía; expresa]

Hamann y colaboradores interpretaron la asociación como intercambio de hidrógeno desde Lenisia hacia Arcobacter. [C-899; S210 resumen; resultados metabólicos; expresa]

Una hidrogenasa aceptora de NAD(P)H de Lenisia se expresó solamente en presencia de Arcobacter en los experimentos publicados. [C-900; S210 resultados transcriptómicos; expresa]

La ruta fermentativa asociada con Arcobacter fue calculada por los autores como capaz de producir el doble de ATP que la ruta alternativa comparada. [C-901; S210 discusión metabólica; expresa]

Arcobacter puede usar óxido nitroso como aceptor de electrones en el sistema experimental. [C-902; S210 resultados; expresa]

La inhibición del metabolismo de N₂O redujo el crecimiento y la respiración del protista en el sistema experimental. [C-903; S210 resultados; expresa]

Proteínas de Arcobacter anotadas como factores de virulencia bacteriana pueden participar en una asociación mutualista en Lenisia. [C-904; S210 discusión; expresa]

En microcosmos de breviados, el crecimiento se asoció con funciones metabólicas del microbioma más que con una única identidad bacteriana. [C-905; S225 resumen y resultados; expresa]

Arcobacteraceae, Desulfovibrionaceae y Terasakiella fueron identificados como candidatos funcionales en distintos microcosmos de breviados. [C-906; S225 resultados; expresa]

Los intentos de mantener axénicos a los breviados estudiados no tuvieron éxito. [C-907; S225 métodos y discusión; expresa]

El estudio de microcosmos no detectó una señal significativa de codiversificación entre cada breviado y una bacteria concreta. [C-908; S225 discusión; expresa]

El sistema Lenisia–Arcobacter ilustra una asociación externa basada en eliminación de productos reductores. [C-909; S210; S225; sintesis(C-899, C-900, C-901, C-905)]

Lenisia–Arcobacter no constituye una observación de la asociación que originó la mitocondria. [C-910; n/a; síntesis de C-897–C-910; glosa]

Consorcios de arqueas metanotróficas anaerobias y bacterias reductoras de sulfato ocupan zonas de transición metano–sulfato. [C-911; S226 introducción; expresa]

Wegener y colaboradores estudiaron consorcios termófilos ANME-1–HotSeep-1 a 60 °C. [C-912; S226 métodos y resultados; expresa]

La adición de H₂ reprimió la oxidación de metano en el consorcio termófilo estudiado. [C-913; S226 resultados; expresa]

Citocromos multihemo, estructuras tipo pili y conexiones entre células apoyaron transferencia directa de electrones entre ANME y SRB. [C-914; S226 resultados y discusión; expresa]

Aceptores artificiales solubles permitieron oxidación de metano por ANME sin reducción simultánea de sulfato por el socio bacteriano. [C-915; S227 resumen y resultados; expresa]

La dependencia ecológica de un consorcio ANME–SRB no implica incapacidad catabólica absoluta de ANME para transferir electrones a otros aceptores. [C-916; S226; S227; sintesis(C-914, C-915)]

Los consorcios ANME–SRB ilustran que una asociación puede ser estable sin endocitosis ni transmisión hereditaria conjunta. [C-917; S226; S227; sintesis(C-912, C-916)]

## 9.3. Endosimbiontes procariotas y eucariotas en protistas

Pelomyxa palustris es una ameba anaerobia o microaerobia que alberga varios procariotas intracelulares. [C-918; S231 resumen; S233 introducción; expresa]

Un aislamiento de 1988 atribuyó Methanobacterium formicicum a Pelomyxa palustris. [C-919; S232 resumen; expresa]

El aislado atribuido a Pelomyxa midió aproximadamente 3 × 0,4 µm. [C-920; S232 descripción; expresa]

El aislado histórico tuvo tiempos de generación de 10 h con H₂/CO₂ y 12 h con formiato. [C-921; S232 resultados; expresa]

El estudio de 2017 no detectó Methanobacterium formicicum en las Pelomyxa examinadas. [C-922; S231 resumen y resultados; expresa]

Gutiérrez y colaboradores consideraron probable que el aislado histórico fuera un contaminante de vida libre. [C-923; S231 discusión; expresa]

El consorcio de Pelomyxa schiedti usa metanogénesis hidrogenotrófica como proceso central de consumo de H₂. [C-924; S233 resumen y resultados; expresa]

La identidad del metanógeno de Pelomyxa palustris no puede fijarse universalmente a partir del aislamiento de 1988. [C-925; S231; S232; S233; sintesis(C-920, C-923, C-924)]

Un estudio de 2024 examinó metanógenos endosimbióticos en 32 especies de ciliados anaerobios de vida libre. [C-926; S234 resumen; expresa]

Los metanógenos de ciliados anaerobios mostraron asociaciones con identidad del hospedador y hábitat. [C-927; S234 resultados; expresa]

Los metanógenos de ciliados pertenecen a varios linajes de Methanomicrobiales, Methanobacteriales y Methanosarcinales. [C-928; S235 resultados; expresa]

La persistencia a través de división y quistes apoyó transmisión vertical en ciliados estudiados por van Hoek y colaboradores. [C-929; S236 resultados y discusión; expresa]

Los análisis de 2025 recuperaron orígenes múltiples y transmisión mixta de metanógenos en ciliados anaerobios. [C-930; S235 resumen y resultados; expresa]

La transmisión de metanógenos en ciliados no puede describirse como exclusivamente vertical para todo el grupo. [C-931; S235; S236; sintesis(C-929, C-930)]

Angomonas deanei alberga una sola bacteria beta-proteobacteriana por célula. [C-932; S238 resumen; expresa]

La división de Kinetoplastibacterium está sincronizada con el ciclo celular de Angomonas deanei. [C-933; S238 resumen y resultados; expresa]

Los genomas de Kinetoplastibacterium estudiados rondan 0,8 Mb y han perdido genes bacterianos de división. [C-934; S237 resultados; S239 introducción; expresa]

Angomonas aporta proteínas nucleares que forman un anillo semejante a dinamina alrededor del sitio de división bacteriano. [C-935; S238 resultados; expresa]

Una proteína nuclear denominada ETP9 controla la división del endosimbionte de Angomonas deanei. [C-936; S239 resumen y resultados; expresa]

Un gen de ornitina ciclodeaminasa fue transferido desde el endosimbionte al núcleo de Angomonas. [C-937; S238 resumen y discusión; expresa]

La proteína OCD transferida se localiza en el glicosoma y no fue detectada dentro del endosimbionte. [C-938; S238 resultados; expresa]

La transferencia de un gen no implica que su producto regrese al compartimento donante. [C-939; S238; sintesis(C-937, C-938)]

Perkinsela vive como endosimbionte eucariota obligado dentro de Paramoeba. [C-940; S240 resumen e introducción; expresa]

El genoma nuclear de Perkinsela secuenciado mide aproximadamente 9,5 Mb. [C-941; S240 resumen y resultados; expresa]

Perkinsela perdió el flagelo pero conserva transcripción policistrónica, trans-splicing y un orgánulo semejante a glicosoma. [C-942; S240 resumen y resultados; expresa]

Las rutas metabólicas de Perkinsela y Paramoeba son complementarias e interdependientes. [C-943; S240 resultados y discusión; expresa]

Microscopía mostró invaginaciones por las que Perkinsela incorpora material citoplasmático de Paramoeba. [C-944; S240 resumen; fig. 1; expresa]

El genoma mitocondrial de Perkinsela conserva seis genes codificantes de proteínas. [C-945; S241 resumen; expresa]

Perkinsela demuestra que una asociación obligada puede conservar dos núcleos eucariotas y dos linajes mitocondriales distintos. [C-946; S240; S241; sintesis(C-942, C-943, C-945)]

## 9.4. Endosimbiosis en curso o comparativamente recientes

La endosimbiosis fotosintética de Paulinella se estima entre 90 y 140 Ma. [C-947; S245 introducción; expresa]

El cromatóforo de Paulinella chromatophora posee un cromosoma circular de 1,02 Mb. [C-948; S242 resumen; expresa]

El genoma del cromatóforo de Paulinella chromatophora codifica 867 proteínas. [C-949; S242 resumen; expresa]

El genoma del cromatóforo está reducido respecto de cianobacterias de vida libre emparentadas. [C-950; S242 resultados; S245 resultados; expresa]

Nowack y colaboradores estimaron que entre 0,3 % y 0,8 % de los genes nucleares de Paulinella examinados proceden de transferencia endosimbiótica. [C-951; S243 resumen y resultados; expresa]

El mismo estudio comparó esa proporción con 11–14 % de genes de origen plastidial en Archaeplastida. [C-952; S243 discusión; expresa]

Al menos dos genes cromatofóricos transferidos al núcleo fueron identificados inicialmente con productos vinculados a fotosíntesis. [C-953; S243 resultados; expresa]

Proteínas nucleares de Paulinella son importadas masivamente al cromatóforo. [C-954; S243 discusión; S244 resultados; expresa]

Transferencias horizontales desde bacterias distintas del endosimbionte compensan funciones perdidas por el cromatóforo. [C-955; S244 título y resultados; expresa]

La integración funcional de Paulinella combina transferencia endosimbiótica, transferencia horizontal e importación de proteínas. [C-956; S243; S244; sintesis(C-953, C-954, C-955)]

El cromatóforo se transmite con el linaje celular fotosintético de Paulinella y no se readquiere en cada generación desde el ambiente. [C-957; S242 discusión; S245 introducción; expresa]

Braarudosphaera bigelowii alberga al diazótrofo cyanobacteriano UCYN-A. [C-958; S248 resumen y resultados; expresa]

UCYN-A fija N₂ y entrega nitrógeno reducido al hospedador fotosintético. [C-959; S246 resultados; S247 resultados; expresa]

El hospedador suministra carbono y otros metabolitos a UCYN-A. [C-960; S247 resultados; expresa]

La división de UCYN-A está coordinada con el ciclo celular de Braarudosphaera. [C-961; S246 resultados; expresa]

UCYN-A importa proteínas codificadas por el genoma nuclear de Braarudosphaera. [C-962; S246 resumen y resultados; expresa]

Coale y colaboradores denominaron nitroplasto al compartimento UCYN-A integrado en Braarudosphaera. [C-963; S246 título, resumen y discusión; expresa]

La clasificación de UCYN-A como orgánulo no convierte en universales los mismos criterios para todas las endosimbiosis. [C-964; S246 discusión; sintesis(C-883, C-963)]

No se localizó en esta sesión un intervalo filogenético primario auditado para el inicio de la asociación Braarudosphaera–UCYN-A. [C-965; BN-039; glosa]

Hatena arenicola incorpora por fagocitosis una célula de Nephroselmis. [C-966; S249 resultados; S250 resultados; expresa]

El simbionte de Nephroselmis aumenta de tamaño y reorganiza estructuras dentro de Hatena. [C-967; S249 resultados; expresa]

Durante la división de Hatena, solo una célula hija hereda el compartimento de Nephroselmis. [C-968; S249 resultados; S250 resumen; expresa]

La hija sin Nephroselmis conserva un aparato de alimentación y puede capturar otra presa compatible. [C-969; S250 resultados; expresa]

Hatena combina transmisión vertical incompleta con readquisición horizontal. [C-970; S249; S250; sintesis(C-968, C-969)]

No se localizó transferencia génica endosimbiótica demostrada desde Nephroselmis hacia el núcleo de Hatena. [C-971; BN-040; glosa]

Los cuerpos esferoidales de Rhopalodia gibba poseen genes de fijación de nitrógeno de afinidad cianobacteriana. [C-972; S251 resultados; expresa]

El cuerpo esferoidal de Epithemia turgida conserva un genoma cianobacteriano reducido y no fotosintético. [C-973; S252 resumen y resultados; expresa]

Los cuerpos esferoidales muestran que la fijación de nitrógeno puede mantenerse después de perder la fotosíntesis del simbionte. [C-974; S251; S252; sintesis(C-972, C-973)]

No se localizó una tabla primaria homogénea con antigüedad, transmisión, tamaño genómico e importación proteica para Paulinella, UCYN-A, Hatena y cuerpos esferoidales. [C-975; BN-041; glosa]

### 9.4.1. Fichas comparativas por grado de integración

| caso | hospedador | socio | qué aporta | antigüedad estimada | transmisión | genoma o reducción | EGT o importación | estado | filas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| *Lenisia limosa*–*Arcobacter* | *Lenisia limosa* | *Arcobacter* epibionte | Consumo de H₂/equivalentes reductores; N₂O como aceptor. | NO LOCALIZADO EN ESTA SESIÓN | No demostrada | Genoma comparativo no localizado en esta entrega | No EGT ni importación demostradas | asociación externa dependiente del contexto | C-897–C-910 |
| ANME–SRB | arquea ANME | bacteria reductora de sulfato | Transferencia de electrones; acoplamiento de oxidación de metano y reducción de sulfato. | n/a | No hereditaria conjunta | n/a | n/a | consorcio extracelular | C-911–C-917 |
| *Pelomyxa*–metanógenos | *Pelomyxa* | arqueas metanógenas y otros procariotas | Consumo de H₂ mediante metanogénesis hidrogenotrófica. | NO LOCALIZADO EN ESTA SESIÓN | No resuelta para todo el consorcio | No localizado de forma homogénea | No localizado | endosimbiosis metabólica | C-918–C-925 |
| ciliados anaerobios–metanógenos | ciliados anaerobios | arqueas metanógenas | Consumo de H₂ y metanogénesis. | Múltiples orígenes; sin edad absoluta localizada | Vertical, horizontal o mixta según linaje | No localizado de forma homogénea | No localizado | endosimbiosis recurrente | C-926–C-931 |
| *Angomonas deanei*–*Kinetoplastibacterium* | *Angomonas deanei* | *Candidatus Kinetoplastibacterium* | Complementación metabólica y división controlada por proteínas del hospedador. | NO LOCALIZADO EN ESTA SESIÓN | Vertical sincronizada con división celular | aprox. 0,8 Mb | EGT de OCD; ETP9 importada/controla división | dependencia heredable | C-932–C-939 |
| *Paramoeba*–*Perkinsela* | *Paramoeba* | *Perkinsela* | Complementación metabólica; ingestión de citoplasma del hospedador. | NO LOCALIZADO EN ESTA SESIÓN | Vertical presumida por obligacia; modo exacto no localizado | núcleo aprox. 9,5 Mb; mitocondria conserva 6 genes proteicos | Interdependencia metabólica; importación completa no resuelta | endosimbiosis eucariota obligada | C-940–C-946 |
| *Paulinella chromatophora*–cromatóforo | *Paulinella chromatophora* | cianobacteria del linaje del cromatóforo | Fotosíntesis; EGT y compensación de funciones. | 90–140 Ma | Vertical | 1,02 Mb; 867 proteínas | EGT 0,3–0,8 % inicial; importación masiva | integración heredable | C-947–C-957 |
| *Braarudosphaera bigelowii*–UCYN-A | *Braarudosphaera bigelowii* | UCYN-A / nitroplasto | Fijación de N₂ por nitrógeno reducido; carbono desde el hospedador. | NO LOCALIZADO EN ESTA SESIÓN (BN-039) | División coordinada y herencia celular | Genoma reducido; cifra no reunida aquí | Importación de proteínas nucleares | orgánulo fijador de nitrógeno propuesto | C-958–C-965 |
| *Hatena arenicola*–*Nephroselmis* | *Hatena arenicola* | *Nephroselmis* | Fotosíntesis y remodelación del simbionte capturado. | NO LOCALIZADO EN ESTA SESIÓN | Vertical incompleta; readquisición horizontal | NO LOCALIZADO EN ESTA SESIÓN | EGT no localizada (BN-040) | asociación reversible por linaje celular | C-966–C-971 |
| *Rhopalodia*/*Epithemia*–cuerpo esferoidal | diatomeas | cianobacteria no fotosintética | Fijación de nitrógeno. | NO LOCALIZADO EN ESTA SESIÓN | Heredable | Genoma reducido; cifra no consolidada aquí | No consolidado | integración heredable | C-972–C-975 |
| *Mesodinium rubrum*–criptófita | *Mesodinium rubrum* | criptófita ingerida | Plastos, mitocondrias, nucleomorfos y núcleos secuestrados. | n/a | Reposición horizontal | Orgánulos y núcleo retenidos temporalmente | Sin integración heredable demostrada | cleptoplastia compleja | C-976–C-978 |
| *Dinophysis*–plastos criptófitos | *Dinophysis* | plastos obtenidos vía *Mesodinium* | Fotosíntesis temporal. | n/a | Adquisición horizontal repetida | n/a | Sin EGT heredable consolidada aquí | cleptoplastia | C-979–C-981 |
| *Elysia*/*Plakobranchus*–plastos | babosas marinas | plastos de algas | Fotosíntesis temporal. | n/a | Adquisición alimentaria; no hereditaria | n/a | Genomas de hospedador sin HGT nuclear extensa demostrada | cleptoplastia | C-982–C-985 |
| criptófitos/cloraracniófitos–nucleomorfo | célula eucariota secundaria | núcleo de alga roja o verde incorporada | Conserva genes nucleares mínimos del endosimbionte. | NO LOCALIZADO EN ESTA SESIÓN | Heredable | 373 kb/331 genes en *Bigelowiella*; 551 kb en *Guillardia* | Importación y coordinación celular implícitas; detalle fuera de esta ficha | integración heredable secundaria | C-986–C-991 |
| dinotomos–endosimbionte diatomeo | *Durinskia baltica* o *Kryptoperidinium foliaceum* | diatomea terciaria intracelular | Fotosíntesis y compartimentos eucariotas retenidos, incluidas mitocondrias. | NO LOCALIZADO EN ESTA SESIÓN | División coordinada; modo fino no consolidado | mitocondrias endosimbiontes: 34.242/34.742 bp y 58/59 genes | 9 candidatos EGT en dinotomos | endosimbiosis terciaria obligada con núcleo retenido | C-1110–C-1116 |
| kareniáceos–plasto haptófito | *Karlodinium* y parientes | plasto terciario derivado de haptófita | Fotosíntesis; pérdida génica e importación asociada. | NO LOCALIZADO EN ESTA SESIÓN | Heredable | 142.981 bp en *K. veneficum*; 70 proteínas, 30 ARNt, 3 ARNr | 90 candidatos EGT en kareniáceos | integración terciaria heredable | C-1115; C-1117–C-1118 |
| *Tremblaya*–*Moranella*–piojo harinoso | piojo harinoso; *Tremblaya* como hospedador interno | *Tremblaya* y *Moranella* | Rutas metabólicas tripartitas y genes bacterianos en insecto. | NO LOCALIZADO EN ESTA SESIÓN | Vertical del consorcio; reemplazos históricos | 138.927 bp y 538.294 bp | HGT bacteriana al insecto | dependencia anidada con reemplazo | C-993–C-999 |
| áfido–*Buchnera aphidicola* | áfido | *Buchnera aphidicola* | Aminoácidos esenciales. | 80–150 Ma para divergencia de cepas comparadas | Vertical materna | 640.681 bp en APS; rango moderno 412–646 kb | No detallada en esta entrega | dependencia obligada | C-1000–C-1006 |
| hospedadores–*Wolbachia* | artrópodos y nematodos según caso | *Wolbachia* | Manipulación reproductiva o aporte mutualista. | NO LOCALIZADO EN ESTA SESIÓN | Materna y horizontal entre hospedadores | Variable; hasta 10 % de elementos de inserción en algunos genomas | HGT al hospedador no cuantificada aquí | parasitismo, mutualismo facultativo u obligado | C-1007–C-1011 |

## 9.5. Robo temporal de orgánulos, endosimbiosis secundaria y nucleomorfos

Mesodinium rubrum adquiere de criptófitas plastos, mitocondrias, nucleomorfos y núcleos. [C-976; S253 resumen; expresa]

Los núcleos criptófitos secuestrados por Mesodinium cambian en número y tamaño durante hambre y realimentación. [C-977; S253 resultados; expresa]

Mesodinium necesita reponer material criptófito para mantener a largo plazo el sistema fotosintético. [C-978; S253 discusión; expresa]

Dinophysis consume Mesodinium y retiene plastos de origen criptófito. [C-979; S254 introducción; S255 resumen; expresa]

Dinophysis no retiene de forma equivalente todos los componentes celulares que Mesodinium obtiene de su presa. [C-980; S255 resumen y resultados; expresa]

La fotoaclimatación de los plastos retenidos por Dinophysis es más limitada que en el donante fotosintético. [C-981; S255 resultados; expresa]

Elysia chlorotica obtiene plastos al consumir el alga Vaucheria litorea. [C-982; S256 introducción; expresa]

El análisis de ADN de huevos de Elysia chlorotica no encontró evidencia de transferencia extensa de genes fotosintéticos a la línea germinal. [C-983; S256 título y resultados; expresa]

El genoma de Plakobranchus ocellatus no contiene los genes nucleares algales necesarios para explicar la fotosíntesis por transferencia horizontal. [C-984; S257 resumen y resultados; expresa]

La kleptoplastia puede transferir temporalmente una función sin transferir hereditariamente los genes nucleares que la sostienen en el donante. [C-985; S253; S256; S257; sintesis(C-982, C-983, C-984)]

El nucleomorfo de Bigelowiella natans mide aproximadamente 373.000 bp y contiene 331 genes. [C-986; S258 resumen; expresa]

El nucleomorfo de Bigelowiella natans está distribuido en tres cromosomas lineales. [C-987; S258 resultados; expresa]

El nucleomorfo de Guillardia theta mide aproximadamente 551 kb. [C-988; S259 resumen; expresa]

El nucleomorfo de Guillardia theta contiene 17 intrones espliceosomales diminutos y 44 genes solapados. [C-989; S259 resumen; expresa]

Los nucleomorfos de criptófitos y cloraracniófitos tuvieron orígenes independientes en algas rojas y verdes incorporadas. [C-990; S258 introducción; S259 introducción; expresa]

Un nucleomorfo no es una etapa cronológica universal situada entre endosimbionte y orgánulo. [C-991; n/a; síntesis de C-993–C-997; glosa]

No se localizó en esta sesión una ficha completa y homogénea de endosimbiosis terciarias con antigüedad, tamaño de todos los genomas, transmisión y reversibilidad. [C-992; BN-042; glosa]

Durinskia baltica y Kryptoperidinium foliaceum albergan endosimbiontes diatomeos terciarios y son los únicos casos localizados con dos mitocondrias de origen evolutivo distinto en la misma célula. [C-1110; S301 resumen; introducción; expresa]

Las regiones codificantes de los genomas mitocondriales endosimbiontes de Durinskia baltica y Kryptoperidinium foliaceum miden 34.242 bp y 34.742 bp. [C-1111; S301 resultados; tabla 1; expresa]

Los genomas mitocondriales endosimbiontes de Durinskia baltica y Kryptoperidinium foliaceum codifican 58 y 59 genes. [C-1112; S301 resultados; tabla 1; expresa]

Los genomas mitocondriales del hospedador y del endosimbionte en los dos dinotomos conservaron rasgos comparables a sus parientes de vida libre pese a su coexistencia. [C-1113; S301 conclusiones; resultados; expresa]

El endosimbionte diatomeo de los dinotomos conserva núcleo, citosol, ribosomas citosólicos, retículo endoplasmático y mitocondrias. [C-1114; S302 introducción y discusión; expresa]

Burki y colaboradores identificaron nueve candidatos de transferencia génica endosimbiótica en dinotomos y noventa en kareniáceos. [C-1115; S302 resumen; resultados; expresa]

La persistencia estable y obligada del endosimbionte diatomeo no produjo una transferencia génica masiva comparable a la inferida en kareniáceos. [C-1116; S302 resultados y discusión; sintesis(C-1114, C-1115)]

El genoma del plasto terciario de Karlodinium veneficum mide 142.981 bp y codifica 70 proteínas, 30 ARNt y tres ARNr. [C-1117; S303 resultados; tabla 1; expresa]

La filogenia plastidial de Karlodinium veneficum respaldó un origen haptófito con bootstrap de 100 %, pero no resolvió si los plastos de Karlodinium y Karenia derivan de una sola endosimbiosis terciaria o de adquisiciones independientes. [C-1118; S303 fig. 4; discusión; expresa]

## 9.6. Endosimbiosis anidadas, reducción extrema y reemplazo

Cada célula de Tremblaya princeps en Planococcus citri contiene células de Moranella endobia. [C-993; S260 introducción y resultados; expresa]

El genoma de Tremblaya princeps mide 138.927 bp. [C-994; S260 resultados; expresa]

El genoma de Moranella endobia mide 538.294 bp. [C-995; S260 resultados; expresa]

Tremblaya, Moranella y el piojo harinoso completan conjuntamente rutas de aminoácidos esenciales. [C-996; S260 resultados; S261 resultados; expresa]

Genes bacterianos adquiridos por el genoma del insecto completan funciones ausentes en ambos endosimbiontes. [C-997; S261 título y resultados; expresa]

El endosimbionte interno de Tremblaya fue reemplazado repetidamente en distintos linajes de piojos harinosos. [C-998; S262 título y resultados; expresa]

La asociación anidada demuestra que dependencia del sistema no equivale a permanencia de una especie simbionte concreta. [C-999; S261; S262; sintesis(C-996, C-997, C-998)]

El genoma de Buchnera sp. APS contiene un cromosoma de 640.681 bp y dos plásmidos pequeños. [C-1000; S263 resumen; expresa]

Buchnera suministra aminoácidos esenciales que son escasos en la dieta de savia de los áfidos. [C-1001; S263 discusión; S266 tesis general; expresa]

Buchnera se transmite maternalmente dentro de bacteriocitos y no se cultiva de forma autónoma. [C-1002; S266 tesis general; expresa]

Las cepas de Buchnera comparadas por van Ham y colaboradores divergieron hace 80–150 Ma. [C-1003; S264 resumen; expresa]

El ancestro compartido de Buchnera reconstruido por Chong y colaboradores contenía 616 genes codificantes de proteínas y 39 genes de ARN. [C-1004; S265 resumen y resultados; expresa]

Los genomas modernos de Buchnera analizados abarcaron 412–646 kb y 354–587 genes proteicos. [C-1005; S265 resumen; expresa]

Las pérdidas génicas posteriores al ancestro de Buchnera fueron no aleatorias entre loci. [C-1006; S265 resultados; expresa]

Wolbachia puede actuar como parásito reproductivo, mutualista facultativo o mutualista obligado según el hospedador. [C-1007; S267 revisión; expresa]

Wolbachia se transmite habitualmente por vía materna dentro de una especie hospedadora. [C-1008; S267 revisión; expresa]

La filogenia de Wolbachia en lepidópteros muestra transferencia horizontal común entre especies. [C-1009; S268 título y resultados; expresa]

Elementos de inserción pueden ocupar hasta 10 % de algunos genomas de Wolbachia. [C-1010; S267 revisión; expresa]

Wolbachia no representa un único grado estable de integración. [C-1011; S267; S268; sintesis(C-1007, C-1008, C-1009, C-1010)]

## 9.7. Correlatos de dependencia, persistencia y ruptura

La dependencia del hospedador se correlaciona negativamente con el tamaño del genoma simbionte en asociaciones de transmisión vertical. [C-1012; S228 resultados; expresa]

La misma correlación no fue equivalente en simbiontes de transmisión horizontal. [C-1013; S228 resultados; expresa]

Los cuellos de botella de transmisión reducen el tamaño efectivo de las poblaciones simbiontes. [C-1014; S229 revisión; S286 modelo; expresa]

Un tamaño efectivo pequeño aumenta la fijación por deriva de mutaciones ligeramente deletéreas. [C-1015; S230 revisión; S298 introducción; expresa]

La pérdida de recombinación y reparación puede intensificar el trinquete de Muller en endosimbiontes. [C-1016; S298 introducción y discusión; expresa]

Allen y colaboradores encontraron que la velocidad del trinquete puede disminuir por selección en endosimbiontes antiguos. [C-1017; S298 resultados y discusión; expresa]

Endobacterias hereditarias de hongos pueden conservar recombinación y plasticidad genómica durante asociaciones antiguas. [C-1018; S299 título y resultados; expresa]

La transmisión vertical no determina por sí sola una reducción genómica extrema. [C-1019; S228; S299; sintesis(C-1012, C-1018)]

La transmisión horizontal permite reemplazar socios y puede mantener acceso a diversidad ambiental. [C-1020; S229 revisión; S262 resultados; S268 resultados; expresa]

La disponibilidad ambiental de la función aportada por un socio puede reducir el beneficio neto de mantenerlo. [C-1021; S228 discusión; S247 discusión; expresa]

La dependencia puede mantenerse a nivel funcional aunque cambie la identidad taxonómica del socio. [C-1022; S225; S262; sintesis(C-905, C-998, C-1020)]

La reducción genómica puede convertir una asociación contingente en dependencia porque elimina alternativas metabólicas del simbionte. [C-1023; S230 revisión; S260 resultados; S265 resultados; expresa]

No se localizó una trayectoria cuantitativa universal de número de genes perdidos por unidad de tiempo para endosimbiontes. [C-1024; BN-043; glosa]

No se localizó un criterio empírico único que prediga si una asociación concreta se volverá obligada. [C-1025; BN-044; glosa]

### 9.7.1. Correlatos publicados

| condición | desenlace asociado | tipo de apoyo | filas |
| --- | --- | --- | --- |
| transmisión vertical | correlación negativa entre dependencia y tamaño del genoma simbionte | Correlato comparado; no causalidad universal. | C-1012–C-1013 |
| cuello de botella de transmisión | reduce Ne y aumenta deriva | Modelos y datos de transmisión. | C-1014–C-1015 |
| pérdida de recombinación y reparación | puede intensificar el trinquete de Muller | Existen límites por selección y contraejemplos con recombinación. | C-1016–C-1019 |
| transmisión horizontal | permite reemplazo y acceso a socios ambientales | Puede impedir fidelidad estricta y mantener función con otra identidad. | C-1020; C-1022 |
| disponibilidad ambiental de la función | puede reducir beneficio de mantener el socio | Dependiente del ambiente y del balance de costes. | C-1021 |
| reducción genómica | elimina alternativas metabólicas y puede fijar dependencia | Trayectorias y velocidades no universales. | C-1023–C-1025 |

## 9.8. Pérdida y degradación de la mitocondria

Las mitocondrias aerobias conservan fosforilación oxidativa y una cadena respiratoria acoplada a síntesis de ATP. [C-1026; S270 introducción; S281 revisión; expresa]

Las mitocondrias anaerobias y los orgánulos relacionados derivan de mitocondrias y no de orígenes endosimbióticos independientes. [C-1027; S270 introducción; S272 discusión; S281 revisión; expresa]

Nyctotherus ovalis vive en ambientes intestinales anóxicos y posee mitocondrias productoras de hidrógeno. [C-1028; S270 resumen e introducción; expresa]

El orgánulo de Nyctotherus ovalis conserva un genoma propio. [C-1029; S270 resumen y resultados; expresa]

La cadena respiratoria de Nyctotherus ovalis conserva componentes de los complejos I y II. [C-1030; S270 resumen y resultados; expresa]

La mitocondria de Nyctotherus ovalis carece de los componentes genómicos estudiados de los complejos III, IV y V. [C-1031; S270 resumen; expresa]

La cadena de Nyctotherus ovalis usa fumarato como aceptor final en la reconstrucción publicada. [C-1032; S270 resumen y discusión; expresa]

Nyctotherus ovalis alberga metanógenos que consumen el H₂ producido por sus orgánulos. [C-1033; S270 introducción y discusión; expresa]

Nyctotherus ovalis documenta un orgánulo con genoma, cadena respiratoria reducida y metabolismo de hidrógeno. [C-1034; S270; sintesis(C-1028, C-1029, C-1030, C-1031, C-1032, C-1033)]

Trichomonas vaginalis posee hidrogenosomas sin genoma ni maquinaria propia de traducción. [C-1035; S271 resumen; expresa]

Los hidrogenosomas de Trichomonas producen H₂, CO₂ y acetato a partir de piruvato. [C-1036; S271 resumen; expresa]

Los hidrogenosomas de Trichomonas forman ATP por fosforilación a nivel de sustrato y no por fosforilación oxidativa. [C-1037; S271 resumen; expresa]

Todas las proteínas del hidrogenosoma de Trichomonas son codificadas en el núcleo e importadas desde el citosol. [C-1038; S271 resumen y resultados; expresa]

El estudio de S271 había localizado experimentalmente 30 proteínas hidrogenosomales y predijo 226 candidatos con presecuencias N-terminales. [C-1039; S271 resumen; expresa]

Giardia intestinalis posee mitosomas de aproximadamente 50–200 nm. [C-1040; S273 introducción; expresa]

Una célula de Giardia intestinalis contiene aproximadamente 40 mitosomas en las condiciones estudiadas. [C-1041; S273 introducción y resultados; expresa]

Los mitosomas de Giardia no producen ATP. [C-1042; S272 resultados; S273 introducción; expresa]

La función metabólica principal localizada en mitosomas de Giardia es el ensamblaje de agrupaciones hierro-azufre. [C-1043; S272 título y resultados; expresa]

Los mitosomas de Entamoeba histolytica contienen una vía de activación de sulfato. [C-1044; S274 título y resultados; expresa]

Entamoeba histolytica no debe usarse como ejemplo de un mitosoma reducido únicamente al ensamblaje Fe–S. [C-1045; S272; S274; sintesis(C-1043, C-1044)]

Los mitosomas de microsporidios conservan componentes funcionales de ensamblaje de agrupaciones Fe–S. [C-1046; S269 resultados; S297 resultados; expresa]

En Encephalitozoon cuniculi, frataxina, Nfs1 e Isu1 colocalizan con Hsp70 mitocondrial en el mitosoma. [C-1047; S269 resultados; figs. 2–3; expresa]

En Trachipleistophora hominis, parte de Isu1 y frataxina se localiza en el citosol, mientras Nfs1 y Hsp70 permanecen en el mitosoma. [C-1048; S269 resultados; fig. 4; expresa]

Los mitosomas microsporidianos muestran reducción convergente con diferencias internas de localización y función. [C-1049; S269; S297; sintesis(C-1046, C-1047, C-1048)]

Monocercomonoides exilis carece de orgánulo mitocondrial y de las proteínas diagnósticas de ese compartimento. [C-1050; S275 resumen; S276 resultados; expresa]

Monocercomonoides exilis adquirió lateralmente un sistema SUF bacteriano para ensamblaje de Fe–S en el citosol. [C-1051; S275 resultados; S276 resultados; expresa]

Las proteínas SUF de Monocercomonoides pueden madurar una proteína Fe–S en Escherichia coli. [C-1052; S277 resumen y resultados; expresa]

La adquisición de SUF precedió y pudo permitir la pérdida de la función mitocondrial ISC, pero no demuestra por sí sola el orden completo de pérdida del orgánulo. [C-1053; S275 discusión; S276 discusión; S277 discusión; expresa]

Henneguya salminicola perdió el genoma mitocondrial. [C-1054; S278 título y resultados; expresa]

Henneguya salminicola perdió casi todos los genes nucleares examinados para transcripción y replicación del genoma mitocondrial. [C-1055; S278 resumen y resultados; expresa]

Henneguya salminicola conserva estructuras interpretadas como orgánulos relacionados con mitocondrias. [C-1056; S278 resultados y discusión; expresa]

La pérdida de genoma mitocondrial no equivale a pérdida total del compartimento mitocondrial. [C-1057; S275; S278; sintesis(C-1054, C-1055, C-1056)]

El gradiente mitocondrial incluye estados que se originaron independientemente en linajes distintos y no una única serie ancestral observada. [C-1058; S270 discusión; S281 revisión; expresa]

No se localizó una cifra comparable de rendimiento energético para todos los estados del gradiente mitocondrial. [C-1059; BN-045; glosa]

### 9.8.1. Gradiente funcional comparado

La tabla ordena grados de conservación funcional; no representa una única serie ancestral observada. [C-1058; S281; sintesis documental]

| estado | funciones conservadas o perdidas | rendimiento energético localizado | ambiente o asociación | filas |
| --- | --- | --- | --- | --- |
| mitocondria aerobia completa | fosforilación oxidativa y cadena respiratoria | ATP por fosforilación oxidativa; cifra comparativa no reunida | ambientes con aceptores adecuados | C-1026 |
| mitocondria anaerobia productora de H₂ | *Nyctotherus ovalis*: genoma propio, complejos I/II, fumarato, H₂ | NO LOCALIZADO EN ESTA SESIÓN con denominador común | intestino anóxico; metanógenos asociados | C-1028–C-1034; BN-045 |
| hidrogenosoma sin genoma | *Trichomonas vaginalis*: piruvato → H₂, CO₂ y acetato | ATP por fosforilación a nivel de sustrato | ambiente anaerobio del hospedador | C-1035–C-1039 |
| mitosoma con ISC | *Giardia intestinalis*: 50–200 nm, aprox. 40 por célula | no produce ATP | anaerobiosis o microaerobiosis intestinal | C-1040–C-1043 |
| mitosoma con activación de sulfato | *Entamoeba histolytica* | NO LOCALIZADO EN ESTA SESIÓN con denominador común | intestino del hospedador | C-1044–C-1045; BN-045 |
| mitosomas microsporidianos | ISC conservado con distribución interna variable | NO LOCALIZADO EN ESTA SESIÓN con denominador común | parasitismo intracelular obligado | C-1046–C-1049; BN-045 |
| ausencia de MRO | *Monocercomonoides exilis*: SUF citosólico lateral | sin producción organelar; cifra celular comparativa no localizada | intestino anóxico | C-1050–C-1053; BN-045 |
| MRO sin genoma mitocondrial | *Henneguya salminicola* | función energética completa no resuelta | parásito de salmón | C-1054–C-1057 |

## 9.9. Cooperación y conflicto entre genomas

Los genomas mitocondriales eucariotas actuales codifican aproximadamente entre 1 y 70 proteínas según la revisión localizada. [C-1060; S281 revisión; expresa]

La hipótesis CoRR propone que genes mitocondriales se conservan localmente para regulación redox de su expresión. [C-1061; S279 tesis general; expresa]

La hidrofobicidad de productos de membrana dificulta su importación desde el citosol y favorece retención organelar. [C-1062; S280 resultados; S281 revisión; expresa]

La composición GC y la hidrofobicidad explicaron patrones de retención en un análisis de 2.015 genomas mitocondriales. [C-1063; S280 resumen y resultados; expresa]

Los códigos genéticos mitocondriales divergentes pueden obstaculizar transferencias funcionales al núcleo. [C-1064; S281 revisión; expresa]

CoRR, hidrofobicidad y código divergente no son mutuamente excluyentes. [C-1065; S279; S280; S281; sintesis(C-1061, C-1062, C-1063, C-1064)]

La transferencia endosimbiótica movió numerosos genes mitocondriales ancestrales hacia cromosomas nucleares. [C-1066; S282 tesis general; expresa]

No se puede dar un único número de genes transferidos desde la protomitocondria porque pérdidas, duplicaciones y transferencias posteriores borraron parte de la señal. [C-1067; S282 revisión; expresa]

Proteínas nucleares destinadas a mitocondria atraviesan complejos de importación de membrana externa e interna, incluidos TOM y TIM. [C-1068; S283 revisión; expresa]

La importación proteica permite que un gen transferido al núcleo siga sosteniendo una función mitocondrial. [C-1069; S282; S283; sintesis(C-1066, C-1068)]

Un gen mitocondrial egoísta puede aumentar dentro de la célula aunque reduzca la respiración del hospedador. [C-1070; S284 resultados; S285 resultados; expresa]

En levadura, genomas mitocondriales petites hipersupresivos desplazan al mtDNA respiratorio. [C-1071; S285 resultados; expresa]

Algunos cruzamientos con mtDNA hipersupresivo produjeron más de 95 % de colonias respiratoriamente deficientes. [C-1072; S285 resultados; expresa]

La herencia uniparental reduce la competencia directa entre genomas citoplasmáticos de dos progenitores. [C-1073; S300 modelos; expresa]

Los modelos de herencia uniparental no muestran que el control del conflicto sea la única explicación de su origen. [C-1074; S300 discusión; expresa]

Un cuello de botella germinal aumenta la varianza de heteroplasmia entre descendientes. [C-1075; S286 modelo; S287 resultados; expresa]

La mayor varianza entre hospedadores puede mejorar la eficacia de selección purificadora contra mtDNA deletéreo. [C-1076; S286 resultados; S287 discusión; expresa]

Heteroplasmia designa la coexistencia de variantes mitocondriales dentro de una célula u organismo. [C-1077; S287 introducción; expresa]

La hipótesis de la maldición de la madre predice acumulación de variantes mitocondriales que dañan a machos pero son neutras o beneficiosas en hembras. [C-1078; S288 introducción; S289 introducción; expresa]

El panel de Drosophila de Carnegie y colaboradores combinó nueve genomas nucleares con nueve haplotipos mitocondriales, para 81 genotipos. [C-1079; S288 resumen; expresa]

En ocho de nueve fondos nucleares, la varianza mitocondrial del tamaño alar fue mayor en machos que en hembras. [C-1080; S288 resumen y resultados; expresa]

El análisis de aproximadamente 0,5 millones de participantes del UK Biobank no encontró apoyo genómico global para la maldición de la madre en humanos. [C-1081; S289 resumen; expresa]

La maldición de la madre tiene apoyo dependiente de especie, carácter y diseño experimental. [C-1082; S288; S289; sintesis(C-1078, C-1080, C-1081)]

La propuesta de que anisogamia y dos tipos sexuales surgieron para controlar conflicto citoplasmático es una hipótesis, no un hecho histórico observado. [C-1083; S300 discusión; expresa]

Las incompatibilidades mitonucleares aparecen cuando variantes de los dos genomas interactúan con efectos de aptitud dependientes de combinación. [C-1084; S288 resultados; expresa]

El genoma de Salpingoeca rosetta contiene un mínimo de veinte familias completas de elementos transponibles según el cribado publicado. [C-1119; S304 resumen; resultados; expresa]

El inventario de Salpingoeca rosetta incluyó siete familias de transposones de ADN y trece familias de retrotransposones LTR, además de dos candidatos no-LTR sin secuencia completa. [C-1120; S304 resumen; resultados; expresa]

El ensamblaje examinado de Monosiga brevicollis contenía tres familias nuevas de retrotransposones LTR y una ausencia aparente de retrotransposones no-LTR y transposones de ADN. [C-1121; S305 resumen; expresa]

La diversidad de familias de elementos móviles difiere entre los dos coanoflagelados genómicamente examinados. [C-1122; S304; S305; sintesis(C-1119, C-1120, C-1121)]

La herencia estrictamente materna de mitocondrias no es universal en animales porque algunos bivalvos presentan herencia doble uniparental. [C-1123; S306 resumen; introducción; expresa]

En la herencia doble uniparental, las hembras transmiten el mitogenoma F a ambos sexos y los machos transmiten el mitogenoma M a sus hijos varones. [C-1124; S306 introducción; expresa]

La existencia de herencia doble uniparental muestra que la supresión de conflicto mediante herencia materna exclusiva no es un estado universal entre eucariotas. [C-1125; S300; S306; sintesis(C-1074, C-1123, C-1124)]

## 9.10. Transferencia génica horizontal hacia y dentro de eucariotas

Conjugación, transformación y transducción describen mecanismos establecidos de transferencia genética en procariotas. [C-1085; S291 revisión; expresa]

Esos tres rótulos no describen automáticamente el paso final de integración estable en un cromosoma nuclear eucariota. [C-1086; S291; S293; sintesis(C-1085)]

Fagotrofia, endosimbiosis, vectores virales, elementos móviles y etapas celulares vulnerables se han propuesto como rutas de HGT eucariota. [C-1087; S291 revisión; S292 tesis general; S293 tesis general; expresa]

Ku y Martin analizaron 30.358 secuencias eucariotas frente a 1.035.375 homólogos procariotas en 2.585 árboles génicos. [C-1088; S290 resumen y métodos; expresa]

La regla del 70 % de Ku y Martin trata identidades procariota-eucariota superiores a 70 % como señal probable de contaminación o error en muchos ensamblajes. [C-1089; S290 título y resultados; expresa]

Ku y Martin defendieron una barrera natural que hace rara la transferencia continua desde procariotas hacia eucariotas. [C-1090; S290 discusión; expresa]

Van Etten y Bhattacharya sostuvieron que la cuestión principal es cuánto HGT eucariota existe y no si existe. [C-1091; S291 título y discusión; expresa]

La atribución de origen bacteriano a un gen eucariota requiere filogenia, contexto genómico, cobertura, composición y exclusión de contaminación. [C-1092; S290 métodos; S291 discusión; expresa]

La hipótesis “eres lo que comes” propone un trinquete en el que genes de presas bacterianas sustituyen genes nucleares eucariotas. [C-1093; S292 resumen; expresa]

El modelo de enlace débil propone que células germinales, embriones, tejidos dañados o etapas unicelulares vulnerables facilitan HGT. [C-1094; S293 tesis general; expresa]

El gen rquA participa en biosíntesis de rodoquinona en Pygsuia biforma. [C-1095; S211 resultados; expresa]

rquA fue transferido al menos dos veces desde bacterias hacia eucariotas y después entre linajes de protistas según la reconstrucción publicada. [C-1096; S211 resumen y resultados; expresa]

Pygsuia posee además un sistema SUF adquirido lateralmente en su orgánulo relacionado con mitocondrias. [C-1097; S294 título y resultados; expresa]

Monocercomonoides y Pygsuia muestran adquisiciones independientes de sistemas bacterianos vinculados a metabolismo anaerobio o Fe–S. [C-1098; S275; S277; S211; S294; sintesis(C-1051, C-1052, C-1095, C-1097)]

Boothby y colaboradores afirmaron que aproximadamente una sexta parte de los genes de un borrador de genoma de tardígrado procedía de HGT. [C-1099; S295 título, resumen y discusión; expresa]

Koutsovoulos y colaboradores no recuperaron evidencia de HGT extensa al reensamblar el genoma con controles de contaminación. [C-1100; S296 título y resultados; expresa]

El episodio de los tardígrados muestra que contaminación, binning y cobertura pueden simular transferencia horizontal masiva. [C-1101; S295; S296; sintesis(C-1099, C-1100)]

La existencia de casos falsos positivos no refuta los casos de HGT apoyados por filogenia, función y contexto genómico. [C-1102; S291; S211; S296; sintesis(C-1092, C-1095, C-1096, C-1100)]

La controversia sobre HGT eucariota es en parte una disputa sobre denominador, filtros y unidad de recuento. [C-1103; S290; S291; sintesis(C-1088, C-1089, C-1090, C-1091, C-1092)]

## 9.11. Qué no se sabe

No se conoce la secuencia celular exacta que convirtió la asociación alfa-proteobacteriana ancestral en una mitocondria heredable. [C-1104; S281 revisión; S282 revisión; expresa]

No se conoce un criterio universal que prediga el punto de no retorno de una endosimbiosis. [C-1105; S228; S230; S246; sintesis(C-883, C-1025)]

No se sabe cuántas asociaciones transitorias desaparecieron sin dejar genomas, fósiles o descendientes muestreables. [C-1106; n/a; derivación de S230 y S282; glosa]

No se localizó un caso de recuperación completa de vida libre por el mismo endosimbionte obligado y reducido. [C-1107; BN-038; glosa]

No se localizó una medida comparable del coste neto para el hospedador en todas las asociaciones tratadas. [C-1108; BN-046; glosa]

No se buscó una auditoría nominal de cada especie simbionte bajo ICNP, ICN o ICZN. [C-1109; BN-047; glosa]

No se localizó una estimación homogénea de la fracción genómica ocupada por elementos móviles para todos los linajes del corredor. [C-1126; BN-048; glosa]

## 9.12. Registro de afirmaciones de la sección 9

> **Registro de afirmaciones:** [data/afirmaciones/09.csv](../data/afirmaciones/09.csv) (251 filas; 12 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

# 10. Rasgos con costo

## 10.0. Alcance, denominadores y clases de coste

Un coste absoluto de un rasgo puede expresarse como ATP equivalente invertido en su construcción u operación. [C-1127; S307 pp. 82–83]

Un coste relativo divide el coste absoluto del rasgo por el presupuesto energético celular usado como denominador. [C-1128; S307 pp. 83, 95]

El coste de construcción y el coste de operación son magnitudes distintas. [C-1129; S307 pp. 82, 90; S324 tabla 1]

El coste de oportunidad contabiliza la energía que se habría obtenido al oxidar un precursor incorporado a biomasa. [C-1130; S307 p. 82]

El coste energético basal no determina por sí solo el efecto neto de aptitud de un rasgo. [C-1131; S307 pp. 82–83]

La misma cifra absoluta produce costes relativos distintos en células con presupuestos distintos. [C-1132; S307 pp. 83, 86–89]

Los valores medidos o modelados en organismos actuales no constituyen mediciones del coste del rasgo durante el tallo eucariota. [C-1133; S307 pp. 81–82, 94–95]

La revisión cuantitativa de 2025 declara que la mayoría de los escenarios sobre núcleo, endomembranas, fagocitosis y otros rasgos carecen de balance neto cuantitativo. [C-1134; S307 p. 82]

El coste de un rasgo puede cambiar si se añade al presupuesto total o sustituye inversión en componentes preexistentes. [C-1135; S307 fig. 1 y pp. 84–85]

No existe una conversión universal entre ATP invertido y coeficiente de selección para todos los organismos y regímenes de crecimiento. [C-1136; S307 pp. 83, 95]

## 10.1. Tabla consolidada de rasgos con coste

La tabla siguiente conserva los encabezados exigidos y no convierte ni promedia unidades. [C-1137; C-1138]

| rasgo | qué habilita | dependencias previas que exige | cifra de coste publicada | unidad exacta | organismo, condición experimental o modelo del que procede | si es medida o estimada por los autores | fuente y localizador | compensación documentada |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| núcleo y envoltura nuclear, sistema completo | compartimentación núcleo-citosol y transporte selectivo | membranas, cromatina, poros, transporte y regulación | SIN CIFRA PUBLICADA LOCALIZADA | SIN CIFRA PUBLICADA LOCALIZADA | FECA/LECA reconstruidos | no localizada | BN-049; C-1146 | Separación espacial y control de intercambio; beneficio histórico neto no cuantificado |
| membrana de macronúcleo | envoltura de un núcleo somático ciliado | área nuclear y biosíntesis de membrana | 6.8 × 10^9 Vcell^0.54 | ATP | ciliados; modelo morfométrico | estimada por los autores | S307 pp. 90–91; C-1139 | compartimentación; no incluye coste de contenido nuclear |
| membrana de micronúcleo | envoltura de un núcleo germinal ciliado | área nuclear y biosíntesis de membrana | 1.5 × 10^9 Vcell^0.41 | ATP | ciliados; modelo morfométrico | estimada por los autores | S307 pp. 90–91; C-1140 | compartimentación; no incluye coste de contenido nuclear |
| complejo del poro nuclear | transporte selectivo núcleo-citosol | nucleoporinas y ensamblaje de poro | 1.3 × 10^7 | ATP por poro | levadura; masa molecular y composición | estimada por los autores | S307 p. 91; C-1143 | transporte selectivo |
| sistema endomembranoso completo | secreción, importación, tráfico y compartimentación | membranas, coatómeros, GTPasas, SNARE, motores y gradientes | SIN CIFRA PUBLICADA LOCALIZADA | SIN CIFRA PUBLICADA LOCALIZADA | FECA/LECA reconstruidos | no localizada | BN-050; C-1156 | tráfico y especialización; balance ancestral no cuantificado |
| vesícula durante construcción | transporte de carga y membrana | lípidos, clatrina, actina y proteínas auxiliares | 1.67 × 10^7 | ATP por vesícula | vesícula de 50 nm; 140 s | estimada por los autores | S307 tabla 1; C-1147 | transporte; cifra no incluye red completa |
| retículo endoplasmático + Golgi, membranas | síntesis, importación, procesamiento y secreción | membranas y maquinaria de tráfico | 1.1 | % del presupuesto celular | Ostreococcus tauri | estimada por los autores | S307 tabla 1; C-1151 | capacidad secretora y de membrana |
| retículo endoplasmático + Golgi, membranas | síntesis, importación, procesamiento y secreción | membranas y maquinaria de tráfico | 21 | % del presupuesto celular | célula pancreática de Sus scrofa | estimada por los autores | S307 tabla 1; C-1154 | gran capacidad secretora; comparando especializado |
| citoesqueleto de actina y tubulina, sistema completo | forma, transporte, motilidad, división y fagocitosis | polímeros, nucleótidos, motores y reguladores | SIN CIFRA PUBLICADA LOCALIZADA | SIN CIFRA PUBLICADA LOCALIZADA | FECA/LECA reconstruidos | no localizada | C-1166 | Las cifras disponibles miden subconjuntos actuales |
| microtúbulos corticales | forma y organización cortical | tubulina, GTP y nucleación | 5.0 × 10^10 | ATP | célula idealizada de Ochromonas | estimada por los autores | S307 tabla 1; C-1159 | mantenimiento de arquitectura celular |
| actina + tubulina totales | forma, transporte y división | proteínas, ATP/GTP y reguladores | 0.1%; 1.4 × 10^9 | % del presupuesto; ATP | Saccharomyces cerevisiae | estimada por los autores | S307 tabla 1; C-1160 | funciones múltiples; no separa recambio |
| fagocitosis, evento completo | captura de partículas y presas | actina, membrana, ATP local, tráfico y digestión | SIN CIFRA PUBLICADA LOCALIZADA | SIN CIFRA PUBLICADA LOCALIZADA | holozoos unicelulares o comparandos inmediatos | no localizada | BN-051; C-1171 | adquisición de alimento; coste neto no cuantificado |
| peroxisoma completo | oxidaciones, detoxificación y rutas lipídicas | membrana, importación PEX, ATPasas y enzimas | SIN CIFRA PUBLICADA LOCALIZADA | SIN CIFRA PUBLICADA LOCALIZADA | eucariotas actuales y LECA reconstruido | no localizada | BN-052; C-1174 | compartimentación metabólica |
| mitosis abierta | segregación cromosómica con acceso citoplasmático | huso, motores, control y reconstrucción nuclear | SIN CIFRA PUBLICADA LOCALIZADA | SIN CIFRA PUBLICADA LOCALIZADA | protistas y otros eucariotas | no localizada | BN-053; C-1181 | segregación; coste comparativo no localizado |
| mitosis cerrada | segregación manteniendo compartimento nuclear | huso intranuclear, motores y control | SIN CIFRA PUBLICADA LOCALIZADA | SIN CIFRA PUBLICADA LOCALIZADA | protistas y hongos | no localizada | BN-053; C-1181 | segregación en ciclos multinucleados |
| mitocondria y fosforilación oxidativa, sistema completo | síntesis de ATP y metabolismo integrado | membranas, complejos respiratorios, genomas, importación y sustratos | SIN CIFRA PUBLICADA LOCALIZADA | SIN CIFRA PUBLICADA LOCALIZADA | simbionte integrado ancestral | no localizada | BN-054; C-1188 | beneficio energético dependiente de ambiente y sustrato |
| membranas mitocondriales | superficie bioenergética y compartimentación | lípidos y proteínas de membrana | 4–17 | % del presupuesto celular | ciliados | estimada por los autores | S307 tabla 1; C-1182–C-1185 | superficie para metabolismo; no incluye orgánulo completo |
| cilio/flagelo eucariota | natación, corrientes y señalización | axonema, motores, membrana, IFT y ATP | 6.15 × 10^10 | ATP por célula | dos flagelos de Chlamydomonas | estimada por los autores | S324 tabla 1; C-1189 | natación; beneficio depende del ambiente |
| operación de cilio/flagelo eucariota | batido y propulsión | dineínas y ATP | 9.7 × 10^5 | ATP s^-1 flagelo^-1 | Chlamydomonas | estimada por los autores | S324 tabla 1; C-1191 | movimiento y adquisición de recursos |
| adhesión celular, sistema completo | contacto, agregación y transmisión de fuerzas | receptores, ligandos, citoesqueleto y señalización | SIN CIFRA PUBLICADA LOCALIZADA | SIN CIFRA PUBLICADA LOCALIZADA | coanoflagelados y filastereos | no localizada | BN-055; C-1198 | persistencia de contacto; beneficio cuantitativo no localizado |
| señalización celular, sistema completo | detección y coordinación de respuestas | receptores, nucleótidos, enzimas y proteínas efectoras | SIN CIFRA PUBLICADA LOCALIZADA | SIN CIFRA PUBLICADA LOCALIZADA | linajes del corredor | no localizada | BN-056; C-1203 | precisión y plasticidad; coste total no localizado |

La tabla de costes conserva la unidad y el denominador originales de cada fuente. [C-1137; n/a]

Cuando no se localizó una cifra para el rasgo completo, la tabla usa el marcador SIN CIFRA PUBLICADA LOCALIZADA. [C-1138; n/a]

## 10.2. Núcleo y envoltura nuclear

El coste modelado de la membrana de un macronúcleo de ciliado escala como 6.8 × 10^9 Vcell^0.54 ATP. [C-1139; S307 pp. 90–91]

El coste modelado de la membrana de un micronúcleo de ciliado escala como 1.5 × 10^9 Vcell^0.41 ATP. [C-1140; S307 pp. 90–91]

Para otros eucariotas, el coste modelado de la membrana nuclear escala como 7.8 × 10^9 Vcell^0.48 ATP. [C-1141; S307 pp. 90–91]

En un ciliado de 10^5 µm³, el volumen nuclear usado como proxy dio costes relativos de 2.5% para el macronúcleo y 0.032% para el micronúcleo. [C-1142; S307 p. 91]

Un complejo del poro nuclear de levadura fue estimado en 1.3 × 10^7 ATP de construcción. [C-1143; S307 p. 91]

Un complejo del poro nuclear de vertebrado fue estimado en 2.9 × 10^7 ATP de construcción. [C-1144; S307 p. 91]

El coste conjunto estimado de poros nucleares escala como 7.0 × 10^8 Vnuc^0.78 ATP. [C-1145; S307 p. 91]

No se localizó una cifra publicada para el coste total de construir y operar un núcleo ancestral completo. [C-1146; BN-049]

## 10.3. Endomembranas y tráfico vesicular

Una vesícula de 50 nm fue estimada en 1.67 × 10^7 ATP durante su construcción. [C-1147; S307 tabla 1]

La misma vesícula de 50 nm fue estimada en 9.6 × 10^6 ATP una vez en el citoplasma. [C-1148; S307 tabla 1]

El coste de membrana pura fue estimado en 1.25 × 10^9 ATP µm^-2. [C-1149; S307 tabla 1]

El coste de membrana con 40% de proteína por área fue estimado en 1.45 × 10^9 ATP µm^-2. [C-1150; S307 tabla 1]

La membrana de retículo endoplasmático y Golgi representa 1.1% del presupuesto celular estimado en Ostreococcus tauri. [C-1151; S307 tabla 1]

La membrana de retículo endoplasmático y Golgi representa 1.1% del presupuesto celular estimado en Saccharomyces cerevisiae. [C-1152; S307 tabla 1]

La membrana de retículo endoplasmático y Golgi representa 3.0% del presupuesto celular estimado en Dunaliella salina. [C-1153; S307 tabla 1]

La membrana de retículo endoplasmático y Golgi representa 21% del presupuesto celular estimado en una célula pancreática de Sus scrofa. [C-1154; S307 tabla 1]

En los cuatro eucariotas modelados por Lynch y Marinov, las membranas internas representan proporciones diferentes del coste total de membranas. [C-1155; S312 tabla 1; S313]

No se localizó una cifra publicada para el coste total del sistema endomembranoso ancestral con todos sus componentes luminales, motores y regulación. [C-1156; BN-050]

Un preprint de 2024 modeló que un proto-retículo con translocasas Sec podía aportar beneficio neto bajo sus parámetros. [C-1157; S342 resultados; S307 pp. 93–94]

El mismo preprint no encontró beneficio de pinocitosis de moléculas pequeñas en los rangos de parámetros considerados. [C-1158; S342 resultados; S307 pp. 93–94]

## 10.4. Citoesqueleto y fagocitosis

Los microtúbulos corticales de una célula idealizada de Ochromonas fueron estimados en 5.0 × 10^10 ATP de construcción. [C-1159; S307 tabla 1]

Actina y tubulina totales representan 0.1% y 1.4 × 10^9 ATP del presupuesto de Saccharomyces cerevisiae. [C-1160; S307 tabla 1]

Actina y tubulina totales representan 0.4% y 1.1 × 10^10 ATP del presupuesto de Schizosaccharomyces pombe. [C-1161; S307 tabla 1]

Actina y tubulina totales representan 5.7% del presupuesto celular estimado en fibroblastos de ratón. [C-1162; S307 tabla 1]

Actina y tubulina totales representan 0.6% del presupuesto celular estimado en células HeLa. [C-1163; S307 tabla 1]

La polimerización de actina está acoplada a unión e hidrólisis de ATP. [C-1164; S326 tesis general]

La dinámica de microtúbulos está acoplada a unión e hidrólisis de GTP en tubulina. [C-1165; S327 tesis general]

Los costes de nucleótidos por subunidad no equivalen al coste total del citoesqueleto porque abundancia, recambio y motores varían. [C-1166; S307 tabla 1; S326; S327]

CK-B suministra ATP local a estructuras de actina durante fagocitosis mediada por complemento. [C-1167; S328 resultados]

La inhibición de CK-B redujo la formación global de F-actina a 73 ± 9% del control en el sistema estudiado. [C-1168; S328 resultados]

Durante fagocitosis, el contenido de ATP de neutrófilos humanos cayó rápidamente hasta 0.8 fmol por célula en el experimento de Borregaard y Herlin. [C-1169; S329 resultados]

La caída de contenido de ATP a 0.8 fmol por célula no es una medida del coste total por partícula ingerida. [C-1170; S329 métodos y discusión]

No se localizó una cifra publicada de ATP por evento de fagocitosis para un holozoo unicelular o un comparando inmediato del corredor. [C-1171; BN-051]

## 10.5. Peroxisomas y mitosis

La importación y reciclado de receptores peroxisomales utiliza las ATPasas AAA+ PEX1 y PEX6. [C-1172; S330 tesis general; S331 resultados; S332 estructura]

Pex1/Pex6 puede desplegar sustratos mediante enhebrado procesivo dependiente de ATP. [C-1173; S331 resultados]

No se localizó una cifra publicada para el coste total de construir, importar proteínas y mantener un peroxisoma completo. [C-1174; BN-052]

La mitosis abierta desensambla ampliamente la envoltura nuclear durante la segregación cromosómica. [C-1175; S333 revisión]

La mitosis cerrada conserva la envoltura nuclear durante la segregación cromosómica. [C-1176; S333 revisión]

Las mitosis semiabiertas o parcialmente abiertas comprenden estados intermedios de permeabilización o desensamblaje nuclear. [C-1177; S333 revisión]

En el muestreo de holozoos de Shah y colaboradores, ciclos multinucleados se asociaron con mitosis cerrada y ciclos predominantemente mononucleados con mitosis abierta. [C-1178; S334 resultados y fig. 4]

Corallochytrium limacisporum presentó mitosis abierta en el estudio comparado. [C-1179; S334 resultados]

La reconstrucción de una mitosis ancestral cerrada u ortomítica permanece dependiente del muestreo y de la codificación de caracteres. [C-1180; S75 resultados y discusión; S334 discusión]

No se localizó una cifra publicada que compare el coste energético total de mitosis abierta, cerrada y semiabierta en protistas. [C-1181; BN-053]

## 10.6. Mitocondria, cilio, adhesión y señalización

La membrana mitocondrial representa 1.9% del presupuesto celular estimado en Dunaliella salina. [C-1182; S307 tabla 1]

La membrana mitocondrial representa entre 4% y 17% del presupuesto celular estimado en ciliados. [C-1183; S307 tabla 1]

La membrana mitocondrial representa 6.7% del presupuesto celular estimado en una célula pancreática de Sus scrofa. [C-1184; S307 tabla 1]

La membrana mitocondrial representa 7.9% del presupuesto celular estimado en Ostreococcus tauri. [C-1185; S307 tabla 1]

El área total de membrana mitocondrial fue modelada como aproximadamente 3.0 Vcell^0.99 en el conjunto de Lynch y Marinov. [C-1186; S312 resultados; S313]

El coste de membranas mitocondriales no incluye por sí solo síntesis, recambio y operación de complejos respiratorios, metabolitos y transporte. [C-1187; S307 tabla 1; S312]

No se localizó una cifra única publicada para el coste total de una mitocondria ancestral integrada y su fosforilación oxidativa. [C-1188; BN-054]

La construcción de los dos flagelos de Chlamydomonas fue estimada en 6.15 × 10^10 ATP por célula. [C-1189; S324 tabla 1]

La construcción de los flagelos de Chlamydomonas representó 1.4% del presupuesto de su ciclo celular en el modelo. [C-1190; S324 tabla 1]

La operación de cada flagelo de Chlamydomonas fue estimada en 9.7 × 10^5 ATP s^-1. [C-1191; S324 tabla 1]

La operación de los flagelos de Chlamydomonas representó 1.2% del presupuesto de su ciclo celular en el modelo. [C-1192; S324 tabla 1]

El coste total modelado de construcción y operación de flagelos de Chlamydomonas fue 2.6% del presupuesto del ciclo. [C-1193; S324 tabla 1]

En una encuesta de 200 especies, la construcción de flagelos se situó en la mayoría entre 0.1% y 40% del presupuesto celular. [C-1194; S307 p. 90; S324 resultados]

Los modelos de beneficio de natación dependen de distribución de recursos, tamaño celular y velocidad. [C-1195; S324 resultados; S307 pp. 92–93]

El fortalecimiento de adhesión mediada por integrinas aumentó aproximadamente siete veces bajo una fuerza constante de 200 nN en el sistema de Gallant y colaboradores. [C-1196; S336 resultados]

La fuerza de 200 nN es una carga mecánica aplicada y no una cifra de ATP consumido por adhesión. [C-1197; S336 métodos]

No se localizó una cifra publicada para el coste total de adhesión celular en un coanoflagelado o filastereo. [C-1198; BN-055]

La señalización por proteínas G consume GTP en el ciclo de activación y desactivación de Gα. [C-1199; S337 tesis general]

La precisión de sistemas de detección celular está restringida conjuntamente por tiempo, número de proteínas y disipación energética en modelos de asignación de recursos. [C-1200; S338 resumen y modelo]

La calorimetría de embriones de pez cebra detectó oscilaciones de calor asociadas al ciclo celular y a señalización fosforilativa. [C-1201; S339 resultados]

Las oscilaciones de calor embrionarias no proporcionan el coste total de una red de señalización en un protista ancestral. [C-1202; S339 métodos y discusión]

No se localizó una cifra publicada para el coste total de señalización de una célula del corredor. [C-1203; BN-056]

## 10.7. Posición de la precondición energética mitocondrial

Lane y Martin propusieron que la endosimbiosis mitocondrial permitió una expansión aproximada de 200000 veces en el número de genes expresados. [C-1204; S308 resumen]

En el cálculo de Lane y Martin, una bacteria ampliada hipotética dispondría de 0.0005 fW por gen. [C-1205; S308 p. 931]

El valor de 0.0005 fW por gen era 230000 veces menor que el del protozoo comparado en el cálculo. [C-1206; S308 p. 931]

Lane y Martin expresaron la diferencia como aproximadamente 200000 veces más energía por gen eucariota. [C-1207; S308 pp. 929, 931]

Lane y Martin atribuyeron entre 10^5 y 10^6 veces más potencia por gen al hospedador con mitocondrias en su formulación. [C-1208; S308 p. 931]

El denominador de energía por gen de Lane y Martin divide la potencia total disponible por el número de genes. [C-1209; S308 sección Energy per gene expressed]

La hipótesis predice que un procariota sin genomas bioenergéticos localizados no puede sostener una expansión eucariota del repertorio expresado bajo los supuestos del modelo. [C-1210; S308 conclusión]

La hipótesis no identifica la respiración aerobia por sí sola como la ventaja relevante. [C-1211; S308 pp. 929–930]

Lane y Martin sostuvieron que los genomas mitocondriales permiten control local sobre membranas bioenergéticas extensas. [C-1212; S308 pp. 930–933]

La comparación de Lane y Martin normaliza por gen y no por volumen celular ni por coste marginal de añadir un gen. [C-1213; S308 sección Energy per gene expressed; S311]

## 10.8. Posición contraria, réplicas y reanálisis

Lynch y Marinov calcularon por separado los costes de replicación, transcripción y traducción de genes. [C-1214; S309 métodos]

Lynch y Marinov concluyeron que la carga relativa de un gen generalmente disminuye al aumentar el tamaño celular. [C-1215; S309 resultados]

Lynch y Marinov sostuvieron que no existe una barrera energética general que impida complejidad genómica procariótica. [C-1216; S309 discusión; S311]

La posición de Lynch y Marinov usa como objeto principal el coste incremental de replicar y expresar un gen dentro del presupuesto de la célula. [C-1217; S309 métodos; S311]

Lynch y Marinov objetaron que potencia metabólica total dividida por número de genes no mide el coste incremental de un gen. [C-1218; S311 texto principal]

Lane y Martin respondieron que el coste marginal actual no resuelve la capacidad histórica de ampliar y expresar repertorios proteicos. [C-1219; S310 texto principal]

Las dos posiciones comparan magnitudes empíricas diferentes además de interpretar de forma distinta la causalidad histórica. [C-1220; S308, S309, S310, S311]

Gerlitz y colaboradores informaron que más de la mitad de 80 valores rastreados no estaban presentes en las fuentes citadas de las que supuestamente procedían. [C-1221; S314 resultados]

La crítica de procedencia de datos no demuestra por sí sola que la hipótesis energética o su negación sea correcta. [C-1222; S314 discusión; S315]

La corrección de eLife de 2018 modificó el registro del análisis de membranas y debe citarse junto con el artículo de 2017. [C-1223; S313 texto editorial]

Schavemaker y Muñoz-Gómez concluyeron que demanda energética y provisión por membranas bioenergéticas escalan con el tamaño celular sin un salto universal único. [C-1224; S316 resultados y discusión]

Schavemaker y Muñoz-Gómez no descartaron funciones energéticas importantes de las mitocondrias en células grandes. [C-1225; S316 discusión]

Chiyomaru y Takemoto no recuperaron una frontera energética simple que separase universalmente complejidad genómica procariótica y eucariota. [C-1226; S317 resultados y discusión]

No existe una resolución de consenso de la controversia sobre si la mitocondria fue precondición energética de la complejidad genómica. [C-1227; S308, S309, S310, S311, S312, S313, S314, S315, S316, S317, S318; S344]

## 10.9. Barrera de deriva y tamaño efectivo de población

La hipótesis de barrera de deriva propone que la eficacia de selección sobre efectos pequeños depende del tamaño efectivo de población. [C-1228; S320 tesis general; S321 resumen]

Como aproximación, efectos de aptitud menores que 1/Ne pueden ser efectivamente invisibles a la selección. [C-1229; S307 p. 91; S319 pp. 1401–1403]

Lynch y Conery estimaron Ne generalmente mayor que 10^8 para procariotas en su muestreo. [C-1230; S319 p. 1401 y fig. 1]

Lynch y Conery estimaron Ne frecuentemente entre 10^7 y 10^8 para eucariotas unicelulares en su muestreo. [C-1231; S319 pp. 1401–1402 y fig. 1]

Lynch y Conery estimaron Ne entre 10^5 y 10^6 para invertebrados en su muestreo. [C-1232; S319 pp. 1401–1402]

Lynch y Conery estimaron Ne entre 10^4 y 10^5 para vertebrados en su muestreo. [C-1233; S319 pp. 1401–1402]

Las estimaciones de 2003 usaron diversidad en sitios silenciosos y una tasa mutacional media asumida de aproximadamente 2.3 × 10^-10 por sitio y división celular. [C-1234; S319 p. 1401]

La relación de equilibrio usada para diploides fue aproximadamente 4Neμ para diversidad neutral. [C-1235; S319 p. 1401]

La hipótesis de peligro mutacional atribuye la acumulación de intrones, regiones intergénicas y elementos móviles ligeramente deletéreos a selección purificadora debilitada. [C-1236; S319 tesis general; S320]

Lynch y Conery estimaron umbrales críticos de Ne cercanos a 7 × 10^7 para retrotransposones y 2 × 10^7 para transposones de ADN bajo su modelo. [C-1237; S319 material principal y suplementario]

La hipótesis de barrera de deriva no requiere que toda expansión génica, intrónica o intergénica sea ventajosa. [C-1238; S320 tesis general]

El estudio de Lewin y Eyre-Walker estimó Ne de largo plazo para 120 especies eucariotas usando diversidad nucleotídica y tasas de mutación directas. [C-1239; S322 resumen]

Las estimaciones de Ne de Lewin y Eyre-Walker variaron casi cuatro órdenes de magnitud. [C-1240; S322 resumen]

Lewin y Eyre-Walker no encontraron aumento de tamaño genómico asociado con Ne pequeño tras controlar la no independencia filogenética. [C-1241; S322 resumen]

Marino y colaboradores analizaron 807 especies animales para probar relaciones entre proxies de Ne, transposones y tamaño genómico. [C-1242; S323 resumen y métodos]

Marino y colaboradores no encontraron apoyo para que la deriva sea el determinante predominante del tamaño genómico y contenido de transposones a largo plazo en animales. [C-1243; S323 resumen y discusión]

Los resultados negativos en animales y en 120 eucariotas cuestionan una relación global simple sin refutar todos los mecanismos de deriva en linajes concretos. [C-1244; S322; S323]

No existe un valor único de Ne para procariotas, protistas unicelulares o eucariotas multicelulares. [C-1245; S319; S322]

## 10.10. Adaptación, compensación y productos no adaptativos

La natación puede compensar el coste flagelar cuando aumenta suficientemente la adquisición de recursos en un ambiente concreto. [C-1246; S324 modelos coste-beneficio; S307 pp. 92–93]

La fagocitosis proporciona adquisición de partículas, pero no se localizó un balance energético neto comparable para los holozoos unicelulares estudiados. [C-1247; S328; BN-051]

La fosforilación oxidativa proporciona síntesis de ATP acoplada a gradientes electroquímicos, pero ese beneficio no demuestra que la adquisición mitocondrial fuera seleccionada inicialmente por complejidad genómica. [C-1248; S308; S309; S316]

La adhesión puede aumentar resistencia mecánica y persistencia de contacto, pero no se localizó su balance ATP-beneficio en los linajes del corredor. [C-1249; S336; BN-055]

Los intrones espliceosomales, regiones intergénicas redundantes y algunos elementos móviles se han propuesto como productos parcialmente no adaptativos de deriva y sesgo mutacional. [C-1250; S319; S320]

La expansión de familias génicas puede originarse por duplicación inicialmente neutra o levemente deletérea antes de adquirir funciones posteriores. [C-1251; S319; S320; S340]

El coste relativo estimado de duplicar el gen mediano de Saccharomyces cerevisiae fue 4.68 × 10^-5. [C-1252; S340 resultados; S307 p. 90]

En Saccharomyces cerevisiae, cambios superiores a 10% en ARNm y 2% en proteína para un gen de expresión mediana fueron estimados como visibles a la selección. [C-1253; S340 resultados; S307 p. 91]

Que un rasgo tenga beneficio actual no demuestra que cada etapa de su origen tuviera beneficio neto. [C-1254; S320 tesis general; S307 pp. 94–95]

Que una modificación pueda fijarse por deriva no demuestra que sea selectivamente neutra en todos los ambientes. [C-1255; S319, S320, S321, S322, S323]

## 10.11. Qué permanece sin cuantificar

No se conoce la relación cuantitativa exacta entre coste energético relativo y efecto de aptitud para los rasgos del corredor. [C-1256; S307 Future Issues 1]

Los rasgos celulares se adquieren mediante estados intermedios cuyos tamaños mutacionales fenotípicos rara vez están cuantificados. [C-1257; S307 Future Issues 3]

No se localizó una tabla experimental que mida en un mismo protista los costes totales de núcleo, endomembranas, citoesqueleto, fagocitosis, peroxisomas, mitosis, mitocondria, cilio, adhesión y señalización. [C-1258; BN-057]

No puede sumarse sin corrección cada porcentaje de la tabla porque algunos son fracciones del presupuesto total y otros fracciones del coste de membranas o costes absolutos. [C-1259; S307; S312]

No se localizó una reconstrucción cuantitativa del presupuesto energético de FECA o LECA que descomponga todos los rasgos pedidos. [C-1260; BN-058]

La discrepancia energética combina datos incompletos, extrapolación a ancestros no observados y elecciones distintas de denominador. [C-1261; S308, S309, S310, S311, S312, S313, S314, S315, S316, S317, S318; S344]

## 10.12. Registro de afirmaciones de la sección 10

> **Registro de afirmaciones:** [data/afirmaciones/10.csv](../data/afirmaciones/10.csv) (135 filas; 12 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

# 11. Sexo, meiosis y ciclo vital

**Fecha de corte bibliográfico: 8 de agosto de 2026.**

**Cobertura de esta entrega:** reconstrucción de la sexualidad de LECA; distinción entre sexo, meiosis y recombinación; origen y mantenimiento de meiosis; costes; tipos de apareamiento; ciclos de ploidía; anisogamia; sexo críptico y parasexualidad; fósil de *Bangiomorpha*; apareamiento bacteriano inducido en *Salpingoeca rosetta*.

**Regla probatoria:** presencia de un gen, expresión de un gen, recombinación poblacional, fusión celular, cariogamia y meiosis observada se registran como clases de evidencia diferentes.


---

## 11.1. Definiciones operativas y componentes desacoplables

La recombinación genética puede ocurrir sin meiosis y sin fusión entre individuos. [C-1262; S357 §Definitions; S360 introducción]

La meiosis es un programa de división y recombinación que reduce la ploidía, pero no equivale por sí sola al ciclo sexual completo. [C-1263; S357 §Meiosis; S358 introducción]

El sexo eucariota, en sentido celular, combina material genético de núcleos distintos y puede incluir singamia, cariogamia y meiosis en momentos separados. [C-1264; S357 figs. 1–2; S78 tesis general]

Plasmogamia designa la fusión de citoplasmas y cariogamia la fusión de núcleos. [C-1265; S357 §Cell-cell fusion and karyogamy]

Singamia se usa para la fusión de células sexuales y puede abarcar plasmogamia y cariogamia según el autor y el ciclo. [C-1266; S357 §Definitions]

Un tipo de apareamiento define compatibilidad de fusión y no implica necesariamente anisogamia, cromosomas sexuales ni dos sexos. [C-1267; S357 §Mating types; S365 resultados; S375 introducción]

Un ciclo haplonte tiene crecimiento mitótico predominantemente haploide y una fase diploide restringida al cigoto. [C-1268; S357 fig. 1]

Un ciclo diplonte tiene crecimiento mitótico predominantemente diploide y produce células haploides mediante meiosis. [C-1269; S357 fig. 1]

Un ciclo haplodiplonte incluye crecimiento mitótico tanto haploide como diploide. [C-1270; S357 fig. 1]

La parasexualidad permite recombinación y cambios de ploidía sin la secuencia canónica de meiosis. [C-1271; S360 §§1–2; S369 resultados]

---

## 11.2. ¿Era sexual LECA? Inventarios, observaciones y límites

SPO11 inicia roturas de doble cadena programadas en muchas meiosis eucariotas. [C-1272; S346 tabla 1; S358 §Recombination]

DMC1 es una recombinasa derivada de la familia RecA/Rad51 y favorece intercambio entre cromosomas homólogos durante meiosis. [C-1273; S346 tabla 1; S357 §Meiosis]

MSH4 y MSH5 forman un complejo asociado con estabilización de intermediarios de recombinación y entrecruzamientos meióticos. [C-1274; S346 tabla 1; S358 §Crossovers]

HOP1 participa en ejes cromosómicos y recombinación meiótica en los sistemas donde ha sido caracterizado. [C-1275; S346 tabla 1; S358 §§Chromosome axes]

MND1 coopera con HOP2 en la búsqueda de homología y la invasión de cadena mediada por recombinasas. [C-1276; S346 tabla 1; S358 §Recombination]

REC8 es una cohesina meiótica asociada con cohesión de cromátidas y segregación reduccional. [C-1277; S346 tabla 1; S358 §Cohesins]

Ramesh y colaboradores identificaron en Giardia un conjunto de genes meióticos que incluía cinco genes considerados específicos de meiosis. [C-1278; S77 resumen y tabla 1]

Malik y colaboradores localizaron en Trichomonas vaginalis 27 de los 29 genes meióticos examinados. [C-1279; S346 resumen; tabla 2]

Trichomonas vaginalis conservaba ocho de nueve genes que el estudio clasificó como específicos de meiosis. [C-1280; S346 resumen]

No se había observado meiosis en Trichomonas vaginalis en el estudio que publicó su inventario de genes. [C-1281; S346 resumen y discusión]

Carr y colaboradores localizaron 18 genes meióticos conservados en los coanoflagelados examinados. [C-1282; S348 resultados y tabla 1]

La presencia de genes meióticos en Monosiga brevicollis precedió a la observación experimental de sexo en Salpingoeca rosetta. [C-1283; S348; S349; S203]

El genoma de Capsaspora owczarzaki contiene un repertorio amplio de homólogos relacionados con sexo y meiosis. [C-1284; S352 suplemento y discusión]

No se ha documentado directamente un ciclo sexual de Capsaspora owczarzaki en las fuentes recuperadas para esta sección. [C-1285; BN-059]

Los inventarios de Amoebozoa recuperan genes meióticos en linajes sin sexo observado. [C-1286; S353 resultados; S354 resultados]

La presencia de un homólogo llamado meiótico no demuestra que su función actual esté restringida a meiosis. [C-1287; S355 resultados y discusión]

La ausencia aparente de un gen meiótico individual no demuestra ausencia de meiosis. [C-1288; S346 tabla 2; S347 discusión; S358 revisión]

La conservación distribuida de la maquinaria de recombinación, cohesión y reducción de ploidía favorece una meiosis presente en LECA. [C-1289; S77, S346, S347, S348; S353, S354, S355, S356, S78, S357, S358]

La inferencia de un LECA sexual no identifica su ciclo de ploidía, frecuencia de apareamiento ni señales ambientales. [C-1290; S78, S357, S358]

La afirmación “todos los eucariotas son sexuales salvo prueba en contrario” es una propuesta metodológica, no una observación exhaustiva de todas las especies. [C-1291; S356 título y tesis general; S355 contraargumento]

La conclusión de que el sexo es ancestral en Eukaryota tiene mayor apoyo que la conclusión de que cada especie eucariota viviente practica sexo actualmente. [C-1292; S355, S356, S78, S357, S358]

---

## 11.3. Origen de la meiosis

La meiosis comparte huso, cromosomas, cohesión y segregación con la mitosis y se interpreta como derivada de una división mitótica ancestral. [C-1293; S359 tesis general; S357 §Meiosis]

Wilkins y Holliday distinguieron cuatro innovaciones respecto de mitosis: apareamiento de homólogos, recombinación entre no hermanas, supresión de separación de hermanas en meiosis I y ausencia de replicación antes de meiosis II. [C-1294; S359 resumen y tabla 1]

Las recombinasas eucariotas RAD51 y DMC1 pertenecen a la familia de RecA bacteriana. [C-1295; S357 §Recombination; S359 discusión]

La recombinación homóloga bacteriana proporciona antecedentes moleculares para reparación y búsqueda de homología, pero no contiene por sí sola el programa meiótico eucariota. [C-1296; S357; S359]

La hipótesis de reparación propone que recombinación y fusión entre genomas permitieron reparar daño usando una copia homóloga. [C-1297; S357 §Origins; S359 discusión]

La hipótesis de restauración y reducción de ploidía interpreta la meiosis como solución a ciclos de fusión que duplicaban el número cromosómico. [C-1298; S357 §Ploidy cycles; S359 discusión]

La hipótesis de control de apareamiento entre homólogos propone que el emparejamiento y los entrecruzamientos redujeron errores de segregación en genomas diploides. [C-1299; S359 modelo]

El modelo de transición desde transferencia lateral a sexo meiótico propone que la expansión genómica redujo la eficacia de reemplazar genomas completos mediante transferencia de fragmentos. [C-1300; S371 modelo y resultados]

Las hipótesis sobre el origen de la meiosis no son equivalentes a las hipótesis sobre su mantenimiento posterior. [C-1301; S361 introducción; S357 conclusión]

No existe una ordenación de consenso para la adquisición ancestral de fusión celular, cariogamia, recombinación meiótica y división reduccional. [C-1302; S357 conclusión; S359 discusión; S360 revisión]

---

## 11.4. Hipótesis sobre el mantenimiento del sexo

La hipótesis de purga de mutaciones propone que recombinación y segregación facilitan separar alelos deletéreos y eliminarlos. [C-1303; S361 §§deleterious mutations; S363 tesis general]

El trinquete de Muller describe acumulación irreversible de mutaciones deletéreas en poblaciones asexuales finitas sin recombinación. [C-1304; S361 §Muller ratchet]

La hipótesis Fisher–Muller propone que recombinación reúne mutaciones beneficiosas surgidas en fondos genéticos distintos. [C-1305; S361 §beneficial mutations]

La hipótesis de la Reina Roja propone que recombinación genera genotipos que cambian frente a antagonistas coevolutivos. [C-1306; S361 §Red Queen]

La hipótesis de ambientes variables propone que recombinación puede aumentar la diversidad de descendencia bajo cambios temporales o espaciales. [C-1307; S361 §environmental variation]

La reparación de daño puede contribuir al mantenimiento del sexo además de haber sido propuesta como función original. [C-1308; S357; S361]

Ninguna hipótesis de mantenimiento explica por sí sola la distribución completa de frecuencias sexuales, ciclos de ploidía y tasas de recombinación eucariotas. [C-1309; S361; S362]

---

## 11.5. Costes del sexo en microorganismos eucariotas

El coste doble clásico compara una hembra sexual que invierte en descendientes de ambos sexos con una hembra asexual que produce únicamente descendientes reproductivos equivalentes. [C-1310; S362 introducción; S363 modelo]

El coste doble de producir machos no se aplica sin modificación a organismos isógamos sin una clase que aporte poco citoplasma al cigoto. [C-1311; S362 §§cost classification; S357 §Isogamy]

La búsqueda de pareja puede imponer tiempo, mortalidad y pérdida de oportunidades de crecimiento. [C-1312; S362 tabla y discusión]

La fusión celular y nuclear exige reconocimiento, contacto, remodelado de membrana y coordinación de núcleos. [C-1313; S203 figs. 1–2; S357 §Cell fusion]

La meiosis consume tiempo y recursos y puede producir segregación no equilibrada o roturas no reparadas. [C-1314; S358 §§Recombination and segregation; S362 discusión]

La recombinación puede romper combinaciones de alelos favorables además de generar combinaciones nuevas. [C-1315; S361 §costs of recombination]

Los cambios de ploidía alteran relación entre volumen, dosis génica, enmascaramiento de mutaciones y eficacia de selección. [C-1316; S357 §Ploidy; S361 discusión]

No se localizó una medición integrada del coste energético de un episodio sexual completo en un coanoflagelado, filastereo o ictiospóreo. [C-1317; BN-060]

No se localizó un valor publicado del coste de encontrar pareja para Salpingoeca rosetta en condiciones naturales. [C-1318; BN-061]

---

## 11.6. Tipos de apareamiento, ciclos de ploidía y anisogamia

Salpingoeca rosetta alterna estados haploides y diploides en cultivo. [C-1319; S349 resumen y fig. 1]

En el estudio de 2013, la limitación de nutrientes coincidió con la transición de cultivos haploides de Salpingoeca rosetta hacia diploidía. [C-1320; S349 resumen; resultados]

El apareamiento observado en Salpingoeca rosetta fue anisógamo porque fusionó células flageladas de tamaños distintos. [C-1321; S349 resumen; fig. 2]

La anisogamia de Salpingoeca rosetta no establece por sí sola sexos masculino y femenino homólogos a los de animales. [C-1322; S349; S357]

El modelo clásico de anisogamia combina un presupuesto finito de material gamético con un compromiso entre número de gametos y tamaño de cada gameto. [C-1323; S364 ecuaciones 2.1 y discusión]

En el modelo de selección disruptiva, estrategias de gametos pequeños y grandes pueden desplazar a tamaños intermedios bajo determinadas funciones de supervivencia y encuentro. [C-1324; S364 resultados]

La teoría de anisogamia explica una divergencia de tamaños gaméticos, pero no identifica el estado ancestral de Salpingoeca rosetta ni de LECA. [C-1325; S349; S364]

Dictyostelium discoideum posee tres tipos de apareamiento determinados por variantes de un locus. [C-1326; S365 resumen y resultados]

En Dictyostelium discoideum, células haploides compatibles se fusionan y forman un cigoto que participa en el desarrollo del macrocisto. [C-1327; S366 resultados; S367 fig. 1]

El cigoto de Dictyostelium discoideum atrae y consume células vecinas durante la formación del macrocisto. [C-1328; S367 fig. 1 y §Life cycle]

La germinación de macrocistos de Dictyostelium discoideum y la recuperación rutinaria de progenie haploide han sido difíciles en laboratorio. [C-1329; S367 introducción]

La existencia de tres tipos de apareamiento en Dictyostelium discoideum demuestra que tipos de apareamiento no tienen que limitarse a dos. [C-1330; S365]

---

## 11.7. Sexo críptico, parasexualidad y criterios de detección

El sexo críptico puede inferirse por decaimiento del desequilibrio de ligamiento con distancia, genotipos recombinantes y estimaciones poblacionales de recombinación. [C-1331; S367 resumen; S370 métodos]

Las firmas poblacionales de recombinación no identifican por sí solas meiosis canónica, parasexualidad o transferencia genética ocasional. [C-1332; S347 discusión; S360 revisión; S370 discusión]

Flowers y colaboradores resecuenciaron 137 fragmentos génicos de cepas silvestres norteamericanas de Dictyostelium discoideum. [C-1333; S367 resumen y métodos]

Dictyostelium discoideum mostró decaimiento rápido del desequilibrio de ligamiento y genotipos recombinantes pese a que el sexo rara vez se observa en laboratorio. [C-1334; S367 resumen y resultados]

Marshall y Berbee infirieron sexo críptico y una fase vegetativa haploide en Pseudoperkinsus tapetis mediante genética de poblaciones. [C-1335; S370 resumen y resultados]

El caso de Pseudoperkinsus tapetis documenta sexo inferido en Ichthyosporea sin observación completa de apareamiento y meiosis. [C-1336; S370]

Durante el enquistamiento de Giardia intestinalis, los dos núcleos intercambian material genético mediante un proceso denominado diplomixis. [C-1337; S368 resultados; S369 resultados]

La diplomixis de Giardia utiliza homólogos de SPO11, HOP1 y DMC1 en recombinación homóloga sin la secuencia completa de meiosis canónica. [C-1338; S346 §Results; S368; S369]

Giardia intestinalis muestra que genes asociados con meiosis pueden integrarse en un proceso parasexual derivado. [C-1339; S346; S368; S369]

La recombinación poblacional detectada en Giardia no demuestra que su ciclo incluya meiosis canónica. [C-1340; S374 resultados; S369 título y discusión]

El inventario genómico de un organismo putativamente asexual debe combinarse con expresión, función, citología y genética de poblaciones para evaluar sexo. [C-1341; S347; S353, S354, S355, S356; S360]

No se localizó observación completa de singamia, cariogamia y meiosis en Sphaeroforma arctica, Creolimax fragrantissima, Abeoforma o Pirum. [C-1342; BN-062]

La fusión celular inducida por inanición y la expresión de genes asociados con meiosis fueron observadas en el amoebozoario Fisculla terrestris. [C-1343; S372 resumen y resultados]

Fisculla terrestris ilustra que una señal ambiental puede coordinar fusión y un programa molecular relacionado con meiosis fuera del corredor principal. [C-1344; S372]

El genoma de Ministeria vibrans contenía todos los componentes clave de meiosis y singamia buscados por Li y colaboradores excepto REC8. [C-1372; S376 Extended Data fig. 10k]

Durante la agregación de Ministeria vibrans se expresaron diferencialmente genes asociados con meiosis y singamia, incluidos PCH2, MSH4, MSH5, SPO11, HOP2, MND1, GEX1 y HAP2. [C-1373; S376 fig. 6e; Extended Data fig. 10j–k]

Aproximadamente 10 % de las células teñidas de Ministeria vibrans mostraron ambas marcas en condiciones de agregación, frente a menos de 2 % sin agregación, con P = 0.0017. [C-1374; S376 fig. 6f]

Li y colaboradores observaron una fusión clara de dos células de Ministeria vibrans tras revisar aproximadamente 216 células durante aproximadamente 2.7 horas por célula. [C-1375; S376 fig. 6g; Supplementary Video 5]

Los autores calificaron como «not conclusive» la evidencia de meiosis y apareamiento en agregados de Ministeria vibrans y solicitaron investigación adicional. [C-1376; S376 discusión, párrafos sobre fig. 6]

Ministeria vibrans aporta observación directa de fusión celular y una firma transcriptómica compatible con apareamiento, pero no una meiosis completa observada. [C-1377; S376 fig. 6e–g; Extended Data fig. 10j–o]

---

## 11.8. Evidencia fósil de sexo

Bangiomorpha pubescens conserva filamentos diferenciados y estructuras interpretadas como esporas o gametos especializados. [C-1345; S159 descripción y figs. 4–9]

Butterfield interpretó la diferenciación de Bangiomorpha pubescens como evidencia de reproducción sexual. [C-1346; S159 resumen y discusión]

La meiosis no está observada directamente en Bangiomorpha pubescens. [C-1347; S159]

La primera aparición de Bangiomorpha pubescens fue revisada a 1.047 +0.013/−0.017 Ga. [C-1348; S160 resumen y resultados]

Bangiomorpha pubescens aporta evidencia fósil de diferenciación compatible con sexo, no una observación del origen del sexo en LECA. [C-1349; S78, S357, S358; S159; S160]

---

## 11.9. Apareamiento inducido por señales externas en coanoflagelados

Vibrio fischeri induce apareamiento en Salpingoeca rosetta mediante la proteína EroS. [C-1350; S203 resumen y resultados; S350 comentario]

EroS es una condroitin liasa bacteriana que degrada condroitín sulfato producido por Salpingoeca rosetta. [C-1351; S203 resumen; figs. 3–5]

Salpingoeca rosetta forma enjambres dentro de los 30 minutos posteriores a exposición a Vibrio fischeri. [C-1352; S203 fig. 1A–B]

La fusión de una pareja de Salpingoeca rosetta ocurre en minutos una vez establecida la orientación basal. [C-1353; S203 fig. 1C]

Después de la plasmogamia, los núcleos de Salpingoeca rosetta convergen y se fusionan para producir una célula diploide. [C-1354; S203 fig. 1D]

El apareamiento entre cepas genéticamente distintas de Salpingoeca rosetta produjo descendencia recombinante. [C-1355; S203 fig. 1E y resultados]

EroS y otras condroitin liasas indujeron apareamiento a concentraciones consideradas ambientalmente relevantes por los autores. [C-1356; S203 resumen y fig. 6]

En experimentos posteriores se usaron concentraciones de EroS de aproximadamente 0.2–1 μg/ml, equivalentes a aproximadamente 2–8 nM. [C-1357; S351 métodos]

Una actividad de 0.05 U/ml de EroS fue usada en ensayos de señales bacterianas combinadas. [C-1358; S351 métodos]

La inducción de apareamiento por EroS demuestra regulación ambiental de la entrada al comportamiento sexual, pero no demuestra reversión de células ya fusionadas. [C-1359; S203]

No se localizó un tiempo cuantificado de retorno a una población no apareante después de retirar EroS. [C-1360; BN-063]

Las señales de limitación nutricional y EroS representan dos condiciones experimentales distintas asociadas con sexo en Salpingoeca rosetta. [C-1361; S349; S203]

No está resuelto cómo se integran fisiológicamente la limitación nutricional y la señal EroS en Salpingoeca rosetta. [C-1362; BN-064]

---

## 11.10. Estado de resolución

La evidencia más directa de sexo en el corredor procede de Salpingoeca rosetta, donde se observaron plasmogamia, cariogamia, diploidía y recombinación. [C-1363; S349; S203]

La evidencia de capacidad sexual en Capsaspora y varios Amoebozoa es principalmente genómica y no tiene la misma resolución que la observación en Salpingoeca rosetta. [C-1364; S349; S203; S352, S353, S354, S355]

Giardia demuestra que recombinación, cariogamia parcial e intercambio nuclear pueden ocurrir sin meiosis canónica. [C-1365; S368; S369]

La reconstrucción de LECA sexual es una inferencia filogenética y funcional, no una observación fósil ni celular del ancestro. [C-1366; S77, S346, S347, S348; S353, S354, S355, S356, S78, S357, S358; S159]

No se conoce la frecuencia de sexo en LECA ni en el tallo eucariota. [C-1367; S357 conclusión; S78 discusión]

No se conoce si LECA era isógamo, anisógamo o presentaba más de un modo de apareamiento. [C-1368; S357 conclusión; S364 discusión]

No se conoce qué señal ambiental activaba el ciclo sexual de LECA. [C-1369; BN-065]

La presencia de sexo en un linaje no implica que sea frecuente, obligado o dominante en su ciclo vital. [C-1370; S78; S357; S367; S370]

Meiosis, sexo y recombinación deben codificarse como rasgos separados en el corpus. [C-1371; S357; S360]

---

## 11.11. Vista comparativa de clases de evidencia

| organismo o nodo | evidencia | clase | conclusión limitada | filas |
| --- | --- | --- | --- | --- |
| LECA | distribución de módulos meióticos | reconstrucción ancestral | meiosis/sexo ancestral probable | C-1289–C-1291 |
| *Salpingoeca rosetta* | ploidía, plasmogamia, cariogamia, recombinación | observación experimental | ciclo sexual demostrado | C-1316–C-1320; C-1347–C-1357 |
| *Capsaspora owczarzaki* | inventario genómico | capacidad inferida | ciclo no observado en fuentes recuperadas | C-1284–C-1285 |
| Amoebozoa diversos | genes y transcriptos | capacidad inferida; contraejemplos funcionales | resolución variable | C-1286–C-1288 |
| *Dictyostelium discoideum* | fusión, macrocistos y genética de poblaciones | observación parcial + inferencia poblacional | sexo documentado, frecuencia silvestre inferida | C-1324–C-1332 |
| *Giardia intestinalis* | intercambio nuclear, genes y población | observación de diplomixis + inferencia | parasexualidad sin meiosis canónica | C-1334–C-1339 |
| *Pseudoperkinsus tapetis* | genética de poblaciones | inferencia indirecta | sexo críptico | C-1331–C-1332 |
| † *Bangiomorpha pubescens* | morfología diferenciada | inferencia paleobiológica | sexo compatible; meiosis no observada | C-1345–C-1349 |

---

## 11.12. Registro de afirmaciones de la sección 11

> **Registro de afirmaciones:** [data/afirmaciones/11.csv](../data/afirmaciones/11.csv) (116 filas; 12 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---

# 12. Multicelularidad y el repertorio preanimal

**Fecha de corte bibliográfico: 8 de agosto de 2026.**

**Cobertura de esta entrega:** rutas clonal, cenocítica y agregativa; parentesco y conflicto; evolución experimental; métricas genómicas de ocho holozoos y un obazoo; repertorios preanimales de adhesión, matriz, señalización y regulación; hipótesis de transición temporal a espacial.

**Regla probatoria:** se distinguen morfología observada, respuesta reversible, homología de dominio, presencia de un gen, función bioquímica, despliegue transcripcional y reconstrucción ancestral. Ninguna de esas clases sustituye automáticamente a las otras.

**Distribución del esfuerzo:** Metazoa se conserva como terminal comparativo. No se desarrolla su topología ni diversificación interna.

---

## 12.1. Rutas celulares y definiciones operativas

La multicelularidad clonal se forma mediante divisiones celulares sucesivas sin separación completa de las células hijas. [C-1378; S134 §Routes to multicellularity; S443 §Clonal development]

La multicelularidad agregativa se forma cuando células que crecieron de manera independiente se adhieren y organizan en un colectivo. [C-1379; S206 resultados; S134 §Routes to multicellularity]

Un cenocito contiene varios núcleos dentro de un citoplasma continuo. [C-1380; S207 introducción; S133 §Development]

La celularización subdivide un cenocito mediante membranas y produce unidades celulares separadas. [C-1381; S208 resumen y fig. 1]

Las rutas clonal, agregativa y cenocítica describen mecanismos de formación y no niveles de complejidad ni etapas obligatorias. [C-1382; S134 tesis general; S445 discusión]

Choanoeca flexa puede combinar crecimiento clonal y agregación en una misma lámina celular. [C-1383; S424 resumen; figs. 1–2]

La coexistencia de clonación y agregación en Choanoeca flexa refuta que ambos mecanismos sean universalmente excluyentes. [C-1384; S424 resumen y discusión]

Una ruta clonal suele elevar la relación genética entre células, pero no elimina mutación somática ni conflicto intraclonal. [C-1385; S443 §§Relatedness and conflict; S433 discusión]

Una ruta agregativa admite quimeras de genotipos distintos cuando el reconocimiento de parentesco es incompleto. [C-1386; S215 resultados; S431 resultados; S424 fig. 6]

### 12.1.1. Vista comparativa de rutas

| ruta | unidad inicial | mecanismo de ensamblaje | relación genética esperada | ejemplos documentados en esta entrega | señal o condición localizada | # |
| --- | --- | --- | --- | --- | --- | --- |
| clonal | una célula fundadora | división sin separación completa | alta al inicio, con mutación posterior posible | rosetas de *S. rosetta*; levadura snowflake | RIF modula entrada al programa en *S. rosetta*; sedimentación selecciona snowflake | C-1378; C-1385; C-1387–C-1390; C-1443–C-1446 |
| agregativa | células que crecieron por separado | adhesión, reorientación y posible matriz | variable; admite quimerismo | *Capsaspora*, *Ministeria*, *Fonticula*, *Dictyostelium* | lípidos, calcio, bacterias, alimento o inanición según linaje | C-1379; C-1386; C-1419–C-1442 |
| cenocítica con celularización | una célula multinucleada | división nuclear sin citocinesis seguida de membranación | alta dentro del cenocito inicial | *Sphaeroforma*, *Creolimax* | relación núcleo-citoplasma en *Sphaeroforma* | C-1380–C-1381; C-1403–C-1415 |
| clonal-agregativa | una célula o células independientes | combinación de división y agregación | depende de contribución clonal y reconocimiento | *Choanoeca flexa* | salinidad, desecación y rehidratación | C-1383–C-1384; C-1392–C-1402 |

## 12.2. Vía clonal y combinación clonal-agregativa en coanoflagelados

Las rosetas de Salpingoeca rosetta se forman por divisiones seriadas de una célula fundadora y no por agregación de células libres. [C-1387; S200 resultados; fig. 4]

Las células de las rosetas de Salpingoeca rosetta permanecen conectadas por puentes intercelulares y matriz extracelular. [C-1388; S200 figs. 4–6]

La actividad inductora de rosetas de Algoriphagus machipongonensis incluye el sulfonolípido RIF-1. [C-1389; S201 resumen; resultados de purificación]

La inducción bacteriana de rosetas modifica la probabilidad de entrar en un programa clonal y no agrega directamente las células. [C-1390; S200; S201 discusión]

No se localizó un presupuesto energético por roseta de Salpingoeca rosetta expresado en ATP, consumo de oxígeno o tasa de crecimiento equivalente. [C-1391; BN-077]

Choanoeca flexa forma láminas de células polarizadas conectadas mediante contactos entre collares. [C-1392; S204 figs. 1–3; S424 fig. 1]

Las láminas de Choanoeca flexa invierten su curvatura en respuesta a transiciones de luz a oscuridad. [C-1393; S204 resumen; figs. 2–4]

Las divisiones clonales de Choanoeca flexa ocurrieron aproximadamente cada 8–10 h en las condiciones publicadas. [C-1394; S424 fig. 1e–f; §C. flexa sheets can form clonally]

Las células disociadas de Choanoeca flexa comenzaron a agregarse en minutos. [C-1395; S424 fig. 2c–d; §C. flexa sheets can form by aggregation]

Los agregados de Choanoeca flexa maduraron en láminas polarizadas dentro de 24 h. [C-1396; S424 fig. 2d–g]

A las 24 h las láminas agregativas de Choanoeca flexa promediaron alrededor de 50 células y algunas alcanzaron aproximadamente 120. [C-1397; S424 fig. 2g; texto de resultados]

La aphidicolina a 17 µg ml−1 no abolió la agregación de Choanoeca flexa. [C-1398; S424 fig. 2i]

En dos campañas de campo las láminas activas de Choanoeca flexa no se observaron por encima de 94 ppt de salinidad. [C-1399; S424 fig. 3e; resultados de campo]

Las pozas con láminas de Choanoeca flexa tuvieron una salinidad media de 62.1 ± 24.8 ppt y las pozas sin láminas 146.3 ± 95.7 ppt. [C-1400; S424 fig. 3e; resultados]

La evaporación experimental durante cuatro días indujo disociación de láminas de Choanoeca flexa y la rehidratación restauró multicelularidad mediante división y agregación. [C-1401; S424 figs. 4a–e]

Las cepas de Choanoeca flexa de pozas distintas mostraron reconocimiento que restringió la agregación entre ellas. [C-1402; S424 resumen; fig. 6]

## 12.3. Vía cenocítica con celularización

Sphaeroforma arctica crece como un cenocito antes de dividir su citoplasma en células hijas. [C-1403; S207 resumen; S208 resumen]

Los ciclos nucleares de Sphaeroforma arctica duraron aproximadamente 11–12 h en las condiciones de cultivo publicadas. [C-1404; S207 fig. 1 y resultados]

El número de núcleos y el tamaño celular de Sphaeroforma arctica pueden desacoplarse experimentalmente. [C-1405; S207 resumen; figs. 2–4]

Sphaeroforma arctica puede alcanzar 128 núcleos antes de la celularización en el ciclo descrito. [C-1406; S208 introducción; fig. 1]

La celularización de Sphaeroforma arctica depende de invaginaciones coordinadas de membrana asociadas con una red de actomiosina. [C-1407; S208 resumen; figs. 2–5]

La celularización de Sphaeroforma arctica produce transitoriamente una capa de células polarizadas con organización comparable a un epitelio. [C-1408; S208 título; figs. 4–6]

La relación núcleo-citoplasma actúa como disparador de celularización en Sphaeroforma arctica bajo las manipulaciones publicadas. [C-1409; S425 resumen; figs. 2–5]

El disparo por relación núcleo-citoplasma en Sphaeroforma arctica no establece que el mismo mecanismo iniciara la multicelularidad animal. [C-1410; S425 discusión; S133 §Evolutionary implications]

Creolimax fragrantissima alterna una fase ameboide proliferativa con crecimiento cenocítico y liberación de células hijas. [C-1411; S209 figs. 1–2; S426 fig. 1]

El genoma publicado de Creolimax fragrantissima abarca aproximadamente 45 Mb en 82 scaffolds. [C-1412; S209 tabla 1]

La anotación publicada de Creolimax fragrantissima contiene 8,695 genes y un promedio de 6.5 intrones por gen. [C-1413; S209 tabla 1]

La expresión génica de Creolimax fragrantissima cambia ampliamente entre fases ameboide y cenocítica. [C-1414; S209 resultados; figs. 3–5]

La celularización de Sphaeroforma y el desarrollo cenocítico de Creolimax representan una ruta distinta de la agregación de células previamente independientes. [C-1415; S208; S209; S133 tabla comparativa]

En Corallochytrium se ha descrito desarrollo mediante divisiones tipo clivaje y una arquitectura genómica muy pobre en intrones. [C-1416; S434 figs. 2 y 5; S129 suplemento]

El genoma publicado de Corallochytrium limacisporum tiene 24.1 Mb y 7,535 genes predichos. [C-1417; S434 tabla de genomas y datos fuente]

La densidad publicada para Corallochytrium fue 0.0 intrones por kbp de secuencia codificante en el conjunto analizado. [C-1418; S434 fig. 5 y datos fuente]

## 12.4. Vía agregativa en Filasterea, Holomycota y Amoebozoa

Capsaspora owczarzaki presenta estadios filopodial, agregativo y quístico en las condiciones de cultivo estudiadas. [C-1419; S206 figs. 2–3]

Los agregados de Capsaspora owczarzaki se forman por unión de células independientes y no por división clonal. [C-1420; S206 fig. 4]

Las células de los agregados de Capsaspora owczarzaki están separadas por material extracelular cohesivo. [C-1421; S206 fig. 3D–F]

La agregación de Capsaspora owczarzaki puede inducirse mediante calcio y una fracción sérica o lipoproteica de masa superior a 30 kDa. [C-1422; S427 resultados; figs. 1–4]

La quelación de calcio con EGTA reduce la agregación inducida de Capsaspora owczarzaki. [C-1423; S427 fig. 3]

Lípidos zwitteriónicos diacilados internalizados por endocitosis inducen retracción de filopodios y agregación en Capsaspora owczarzaki. [C-1424; S428 resumen; figs. 1–5]

La retracción de filopodios de Capsaspora owczarzaki comienza en segundos tras la exposición a los lípidos activos. [C-1425; S428 resultados de imagen temporal]

Ministeria vibrans es un bacterívoro marino de vida libre que forma agregados grandes en cultivo monoxénico con Thalassospira lucentensis. [C-1426; S376 resumen; figs. 2–3]

Thalassospira representó 63% de las lecturas bacterianas únicas en el cultivo xenico original de Ministeria vibrans analizado. [C-1427; S376 Extended Data fig. 2; resultados]

Los agregados de Ministeria vibrans alcanzaron decenas de células dentro de 24 h y después cientos de células. [C-1428; S376 fig. 3a–b]

La aphidicolina no impidió que Ministeria vibrans formara agregados. [C-1429; S376 fig. 3c; Extended Data fig. 3]

El estudio de Ministeria vibrans propuso beneficios de alimentación y apareamiento para la agregación, pero no estableció que ambos expliquen su origen evolutivo. [C-1430; S376 resumen; discusión]

Fonticula alba agrega amebas y forma estructuras fructíferas en su ciclo. [C-1431; S213 resultados; S429 introducción]

Fonticula alba forma un colectivo multicelular dinámico que invade y consume parches bacterianos. [C-1432; S429 resumen; figs. 1–6]

Dictyostelium discoideum agrega células haploides independientes durante inanición y produce un cuerpo fructífero con esporas y tallo. [C-1433; S215 introducción; S430 resumen]

Las rutas agregativas de Capsaspora, Fonticula y Dictyostelium se encuentran en ramas separadas del entorno de Opisthokonta y Amoebozoa. [C-1434; S206 fig. 1; S213 filogenia; S445 revisión]

## 12.5. Parentesco, conflicto y mecanismos antitramposo

En quimeras de Dictyostelium discoideum algunos genotipos aumentan su representación entre las esporas a costa de otros. [C-1435; S215 resultados]

La formación del tallo de Dictyostelium discoideum implica muerte de las células que lo componen y beneficia la dispersión de esporas. [C-1436; S215 introducción y discusión]

La evolución experimental a baja relación genética en Dictyostelium discoideum favoreció tramposos que deterioraron el desarrollo multicelular. [C-1437; S430 resumen; resultados]

La evolución experimental a alta relación genética mantuvo el desarrollo multicelular de Dictyostelium discoideum. [C-1438; S430 resumen; resultados]

El reconocimiento de parentesco mediante sistemas de adhesión reduce la incorporación de tramposos a agregados de Dictyostelium discoideum. [C-1439; S431 resumen; resultados]

La vía clonal reduce el quimerismo al derivar el colectivo de una célula, mientras que la vía agregativa requiere mecanismos adicionales para limitar mezcla y conflicto. [C-1440; S430; S431; S443 discusión]

No se localizaron experimentos que identifiquen tramposos genéticos y mecanismos de castigo en Capsaspora owczarzaki. [C-1441; BN-078]

No se localizaron experimentos que identifiquen tramposos genéticos y mecanismos de castigo en Ministeria vibrans. [C-1442; BN-079]

## 12.6. Evolución experimental de multicelularidad en levadura

La selección repetida por sedimentación produjo levaduras snowflake multicelulares en todas las poblaciones replicadas del experimento de Ratcliff y colaboradores dentro de 60 transferencias diarias. [C-1443; S432 resumen; resultados]

Las levaduras snowflake se desarrollaron clonalmente por separación incompleta de células hijas. [C-1444; S432 figs. 1–2]

El fenotipo snowflake tuvo una ventaja de aptitud de 34% sobre células individuales en el ensayo de sedimentación publicado. [C-1445; S432 resultados; fig. 2]

La apoptosis de células dentro de agregados snowflake favoreció la producción de propágulos más pequeños en el experimento inicial. [C-1446; S432 resultados; figs. 3–4]

El experimento prolongado de Bozdag y colaboradores aplicó 600 rondas de selección a cinco poblaciones anaerobias de levadura snowflake. [C-1447; S433 resumen; fig. 1]

Las poblaciones anaerobias evolucionadas se hicieron aproximadamente 2 × 10^4 veces mayores y alcanzaron escala milimétrica. [C-1448; S433 resumen; fig. 1]

Las poblaciones anaerobias evolucionadas se hicieron aproximadamente 10^4 veces más resistentes mecánicamente. [C-1449; S433 resumen; fig. 3]

La elongación celular y el entrelazamiento de ramas contribuyeron al aumento de tamaño y tenacidad en levadura snowflake. [C-1450; S433 resumen; figs. 2–3]

Las poblaciones sometidas a competencia por oxígeno aumentaron solo alrededor de seis veces su tamaño en el mismo programa experimental. [C-1451; S433 resumen]

Los experimentos con levadura documentan compensaciones entre reproducción de propágulos, tamaño, difusión y resistencia mecánica, pero no reconstruyen directamente el ancestro de Holozoa. [C-1452; S432 discusión; S433 discusión]

### 12.6.1. Costes y compensaciones cuantificados o no localizados

| sistema | beneficio o compensación observada | cifra de coste publicada localizada | unidad | condición | fuente | # |
| --- | --- | --- | --- | --- | --- | --- |
| roseta de *Salpingoeca rosetta* | filtración y organización clonal; el beneficio neto no se cuantifica aquí | SIN CIFRA PUBLICADA LOCALIZADA | SIN CIFRA PUBLICADA LOCALIZADA | cultivo con señal bacteriana | S200–S201; BN-077 | C-1387–C-1391 |
| lámina de *Choanoeca flexa* | alternancia entre alimentación, natación, persistencia y reconstitución | SIN CIFRA PUBLICADA LOCALIZADA | SIN CIFRA PUBLICADA LOCALIZADA | gradiente de salinidad y luz | S204–S424; BN-085 | C-1392–C-1402 |
| celularización de *Sphaeroforma arctica* | producción coordinada de células hijas | SIN CIFRA PUBLICADA LOCALIZADA | SIN CIFRA PUBLICADA LOCALIZADA | cultivo sincronizado | S207–S425; BN-086 | C-1403–C-1410 |
| agregación de *Capsaspora owczarzaki* | respuesta rápida y colectiva a lípidos y calcio | SIN CIFRA PUBLICADA LOCALIZADA | SIN CIFRA PUBLICADA LOCALIZADA | lípidos, fracción sérica y calcio | S206–S428 | C-1419–C-1425 |
| agregación de *Ministeria vibrans* | alimentación mejorada y apareamiento plausible | SIN CIFRA PUBLICADA LOCALIZADA | SIN CIFRA PUBLICADA LOCALIZADA | cultivo monoxénico | S376; BN-090 | C-1426–C-1430 |
| levadura snowflake inicial | selección por sedimentación | 34 | % de ventaja de aptitud | ensayo de sedimentación | S432 | C-1445 |
| levadura snowflake prolongada | tamaño y tenacidad frente a difusión y reproducción | aproximadamente 2 × 10^4 en tamaño; aproximadamente 10^4 en tenacidad | veces respecto del ancestro | tratamiento anaerobio, 600 rondas | S433 | C-1447–C-1451 |

## 12.7. Genomas de referencia y arquitectura génica

El genoma publicado de Monosiga brevicollis tiene aproximadamente 41.6 Mb y alrededor de 9,200 genes. [C-1453; S147 §Gene structure; tabla 1]

Los genes de Monosiga brevicollis tienen un promedio publicado de 6.6 intrones y los intrones promedian 174 bp. [C-1454; S147 tabla 1]

El ensamblaje publicado de Salpingoeca rosetta tiene aproximadamente 55 Mb, 154 scaffolds y N50 de 1.52 Mb. [C-1455; S205 tabla 1]

La anotación publicada de Salpingoeca rosetta contiene 11,629 genes con apoyo transcriptómico para 98% de los modelos. [C-1456; S205 tabla 1; métodos]

El genoma publicado de Capsaspora owczarzaki abarca 28 Mb en 84 scaffolds y contiene 8,657 genes codificantes. [C-1457; S352 tabla 1; resultados]

Los genes de Capsaspora owczarzaki tienen un promedio publicado de 3.8 intrones y una longitud media de intrón de 166 bp. [C-1458; S352 tabla 1]

La anotación utilizada en el estudio de Ministeria vibrans contenía 12,127 genes antes de filtrados transcriptómicos. [C-1459; S376 métodos y Extended Data]

No se localizó en esta sesión un tamaño de genoma nuclear y una densidad de intrones de Ministeria vibrans publicados en la misma versión que el análisis de agregación. [C-1460; BN-080]

El ensamblaje de referencia de Sphaeroforma arctica JP610 registra 121.6 Mb. [C-1461; S446 Assembly statistics]

El linaje ichthyofónido ancestral y sus descendientes muestran densidades de intrones elevadas frente a Corallochytrium en la reconstrucción comparativa publicada. [C-1462; S434 figs. 5–6]

El registro de ensamblaje GCA_000142905.1 confirma que existe un genoma de Thecamonas trahens disponible para comparación. [C-1463; S442 registro de ensamblaje]

No se localizaron en esta sesión cifras auditables y homogéneas de tamaño, número de genes y densidad de intrones para Thecamonas trahens. [C-1464; BN-081]

### 12.7.1. Tabla comparativa de genomas

| organismo | tamaño del genoma publicado | genes publicados | densidad o promedio de intrones | versión o método | fuente | # |
| --- | --- | --- | --- | --- | --- | --- |
| *Monosiga brevicollis* | aproximadamente 41.6 Mb | aproximadamente 9,200 | 6.6 intrones por gen; 174 bp de longitud media | ensamblaje y anotación 2008 | S147 | C-1453–C-1454 |
| *Salpingoeca rosetta* | aproximadamente 55 Mb; 154 scaffolds; N50 1.52 Mb | 11,629; 98% con apoyo transcriptómico | NO LOCALIZADO EN ESTA SESIÓN en unidad homogénea | ensamblaje y RNA-seq 2013 | S205; BN-087 | C-1455–C-1456 |
| *Capsaspora owczarzaki* | 28 Mb; 84 scaffolds | 8,657 | 3.8 intrones por gen; 166 bp de longitud media | ensamblaje y anotación 2013 | S352 | C-1457–C-1458 |
| *Ministeria vibrans* | NO LOCALIZADO EN ESTA SESIÓN | 12,127 antes de filtros | NO LOCALIZADO EN ESTA SESIÓN | anotación usada por el estudio 2026 | S376; BN-080 | C-1459–C-1460 |
| *Sphaeroforma arctica* | 121.6 Mb | NO LOCALIZADO EN ESTA SESIÓN en una versión auditada aquí | intrón-rico cualitativamente; cifra por gen NO LOCALIZADA | ensamblaje GCF_001186125.1 y genómica comparada | S446; S434 | C-1461–C-1462 |
| *Creolimax fragrantissima* | aproximadamente 45 Mb; 82 scaffolds | 8,695 | 6.5 intrones por gen | ensamblaje y anotación 2015 | S209 | C-1412–C-1414 |
| *Corallochytrium limacisporum* | 24.1 Mb | 7,535 | 0.0 intrones por kbp de CDS en el conjunto publicado | genómica comparada 2017 | S434 | C-1416–C-1418 |
| *Thecamonas trahens* | NO LOCALIZADO EN ESTA SESIÓN | NO LOCALIZADO EN ESTA SESIÓN | NO LOCALIZADO EN ESTA SESIÓN | ensamblaje GCA_000142905.1 disponible | S442; BN-081 | C-1463–C-1464 |

## 12.8. Adhesión y matriz extracelular antes de Metazoa

Monosiga brevicollis posee 23 genes con dominios de cadherina en la anotación publicada. [C-1465; S147 §Cadherins; Supplementary Notes]

Monosiga brevicollis posee 17 genes con dominios similares al dominio extracelular de integrina alfa, pero el estudio no localizó una integrina beta canónica. [C-1466; S147 §Integrin-related domains]

El genoma de Monosiga brevicollis contiene cinco genes con dominios de colágeno y dos proteínas con repeticiones Gly-X-Y extensas. [C-1467; S147 §Extracellular matrix proteins]

Capsaspora owczarzaki conserva integrina alfa, integrina beta y componentes citoplasmáticos del adhesoma. [C-1468; S436 resultados; fig. 1]

Los componentes del adhesoma de Capsaspora owczarzaki se regulan durante su ciclo vital y varios aumentan durante agregación. [C-1469; S206 transcriptómica; S441 figs. 2–4]

La distribución de integrinas entre holozoos unicelulares es parcheada y no sigue una simple secuencia de adición acumulativa hacia Metazoa. [C-1470; S435 resultados; S436 discusión]

La presencia de dominios de cadherina, integrina o colágeno en un unicelular no demuestra que cumplan la misma función tisular que en animales. [C-1471; S147 discusión; S352 discusión; S134 §Co-option]

No se localizó una medición comparable del coste energético de producir matriz extracelular en los ocho holozoos genómicos solicitados. [C-1472; BN-082]

## 12.9. Señalización preanimal

Monosiga brevicollis posee aproximadamente 120 tirosina quinasas, 30 tirosina fosfatasas y 80 proteínas con dominios SH2 en el inventario publicado. [C-1473; S147 §Tyrosine kinase signaling]

La señalización por fosfotirosina estaba diversificada antes de Metazoa, pero sus redes preanimales no son idénticas a las redes animales. [C-1474; S147; S352; S440 discusión]

La quinasa Src de Capsaspora posee regulación y especificidad distintas de Src animales reconstruidas en ensayos bioquímicos. [C-1475; S440 resultados; figs. 2–5]

El muestreo de 19 transcriptomas choanoflagelados reveló componentes de Notch y Delta en distribuciones mosaico. [C-1476; S435 fig. 2 y suplementos]

La presencia separada de componentes de Notch o Hedgehog en holozoos unicelulares no equivale a una vía animal completa. [C-1477; S147 discusión; S352 fig. 2; S435 suplementos]

Los receptores acoplados a proteína G y otras familias de señalización tienen historias anteriores a Metazoa y expansiones y pérdidas posteriores. [C-1478; S352 resultados; S434 figs. 2–4; S435]

Los 235 dominios que Suga y colaboradores clasificaron como innovaciones del tallo metazoano incluyen ligandos y componentes extracelulares ausentes en los unicelulares comparados. [C-1479; S352 fig. 2; resultados]

## 12.10. Regulación transcripcional preanimal

Capsaspora owczarzaki posee dos genes Runx con dominios Runt conservados, pero carece de CBFβ y del motivo WRPY en esos genes. [C-1480; S437 §Runx; fig. 1]

Capsaspora owczarzaki posee tres genes T-box en el inventario publicado. [C-1481; S437 §T-box; S438 resultados]

Uno de los T-box de Capsaspora fue clasificado dentro de Brachyury con soporte bootstrap de 50% en el análisis inicial. [C-1482; S437 fig. 2]

Los análisis posteriores respaldaron que Brachyury es la clase más antigua de la familia T-box y que su función de unión a ADN precede a Metazoa. [C-1483; S438 resumen; resultados]

Homólogos de Myc y Max están presentes en Monosiga brevicollis y Capsaspora owczarzaki. [C-1484; S439 resumen; fig. 1]

Myc y Max de Monosiga brevicollis heterodimerizan y se unen a secuencias E-box canónicas y no canónicas. [C-1485; S439 resumen; resultados bioquímicos]

Los genomas unicelulares holozoos contienen familias de homeodominio, pero su distribución y arquitectura difieren entre linajes. [C-1486; S437 resultados; suplementos]

Los dominios p53/p63/p73 y Runx fueron inferidos como presentes antes de Metazoa en la comparación de Capsaspora, choanoflagelados y animales. [C-1487; S352 fig. 2; S437]

La presencia de un factor de transcripción preanimal no demuestra que regulase tipos celulares coexistentes. [C-1488; S441 discusión; S134 §Temporal-to-spatial]

### 12.10.1. Repertorio funcional localizado

| familia o sistema | presencia preanimal localizada | ausencia, discontinuidad o límite | interpretación permitida | # |
| --- | --- | --- | --- | --- |
| integrinas y adhesoma | integrinas alfa y beta con adaptadores en *Capsaspora*; dominios alfa en *Monosiga* | *Monosiga* carece de beta canónica en el estudio; distribución mosaico en otros holozoos | adhesión mediada por integrinas tiene componentes preanimales, no una red idéntica en todos los linajes | C-1466; C-1468–C-1471 |
| cadherinas | 23 genes con dominios de cadherina en *Monosiga* | función intercelular animal no demostrada para todos | homología de dominio anterior a Metazoa | C-1465; C-1471 |
| matriz y colágeno | dominios de colágeno y repeticiones Gly-X-Y en *Monosiga* | fibrillas y matriz animal completa no demostradas | repertorio molecular parcial | C-1467; C-1471–C-1472 |
| fosfotirosina | expansión de TK, PTP y SH2 en *Monosiga*; Src funcional en *Capsaspora* | redes y regulación difieren de animales | sistema preanimal diversificado y reconfigurado | C-1473–C-1475 |
| Notch y Delta | componentes en distribuciones mosaico entre choanoflagelados | vía completa no inferible de componentes separados | cooptación y pérdidas son alternativas | C-1476–C-1477 |
| Hedgehog | componentes parciales en comparaciones holozoas | vía canónica animal completa no localizada fuera de Metazoa | no equiparar pieza con vía | C-1477 |
| GPCR y otras señales | familias antiguas con expansiones y pérdidas | números y ligandos no son homogéneos entre especies | historia mosaico | C-1478–C-1479 |
| Brachyury/T-box | tres T-box en *Capsaspora*; uno asociado inicialmente con Brachyury | bootstrap inicial 50%; función ancestral de desarrollo no observada | origen premetazoano del factor, no del mesodermo | C-1481–C-1483 |
| Runx | dos Runx en *Capsaspora* | sin CBFβ y sin motivo WRPY | arquitectura preanimal distinta | C-1480; C-1487 |
| p53/p63/p73 | dominio inferido antes de Metazoa | función de control tisular no demostrada | homología de repertorio | C-1487–C-1488 |
| Myc–Max | presentes en *Monosiga* y *Capsaspora*; función bioquímica demostrada en *Monosiga* | interfaces divergentes respecto de humanos | regulación de crecimiento anterior a Metazoa | C-1484–C-1485 |
| homeodominios | familias localizadas en *Capsaspora* y otros holozoos | distribución y arquitecturas parcheadas | repertorio ancestral con pérdidas | C-1486–C-1488 |

## 12.11. Hipótesis de transición temporal a espacial

Capsaspora owczarzaki despliega programas transcriptómicos distintos en los estadios filopodial, agregativo y quístico. [C-1489; S206 resultados; S441 figs. 1–4]

La accesibilidad de cromatina y las modificaciones de histonas de Capsaspora owczarzaki cambian entre estadios. [C-1490; S441 resumen; figs. 2–5]

Los genes asociados con adhesión y señalización animal se expresan diferencialmente durante el ciclo de Capsaspora owczarzaki. [C-1491; S206; S441 resultados]

La hipótesis de transición de regulación temporal a espacial propone que programas usados en fases sucesivas de un unicelular fueron cooptados para tipos celulares coexistentes. [C-1492; S206 discusión; S441 discusión; S134]

La expresión por estadios de Capsaspora apoya la plausibilidad de la hipótesis temporal-a-espacial, pero no identifica qué programa originó cada tipo celular animal. [C-1493; S206; S441]

Ministeria vibrans reguló 4,884 genes entre estados de agregación en el análisis publicado. [C-1494; S376 transcriptómica; Extended Data]

El estudio de Ministeria vibrans identificó 521 homólogos de genes animales relacionados con multicelularidad, incluidos 68 de adhesión, 400 de señalización y 53 factores de transcripción. [C-1495; S376 fig. 5; Supplementary Data]

De los 521 homólogos de Ministeria vibrans, 332 cambiaron significativamente durante la agregación. [C-1496; S376 fig. 5; resultados]

La regulación de repertorios durante agregación en Capsaspora y Ministeria es compatible con un uso preanimal en ciclos y colectivos, pero no demuestra que la agregación fuese ancestral en Filozoa. [C-1497; S206; S376 discusión]

## 12.12. Qué permanece sin resolver

No se ha establecido si el ancestro común de Filozoa era agregativo, clonal, cenocítico o combinaba más de una capacidad. [C-1498; S376 introducción y discusión; S134]

No se conoce una cifra de coste energético comparable para las rutas clonal, agregativa y cenocítica en organismos del corredor. [C-1499; BN-083]

No se ha demostrado una correspondencia uno a uno entre estadios de Capsaspora y tipos celulares animales. [C-1500; S441 discusión]

La arquitectura del repertorio preanimal se reconstruye con pérdidas, duplicaciones y muestreo incompleto, por lo que una ausencia en una especie no prueba origen posterior. [C-1501; S352; S434; S435 métodos y discusión]

No se localizó un recuento único y no disputado de orígenes independientes para cada subtipo clonal, cenocítico y agregativo definido con los criterios de este corpus. [C-1502; BN-084]

La evidencia experimental muestra que multicelularidad simple puede evolucionar con rapidez bajo selección intensa, mientras que la historia natural del corredor abarca divergencias profundas no reproducidas por esos ensayos. [C-1503; S432; S433; S134 discusión]

---

## 12.13. Registro de afirmaciones de la sección 12

> **Registro de afirmaciones:** [data/afirmaciones/12.csv](../data/afirmaciones/12.csv) (126 filas; 12 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---

---

# 13. Escalas, tasas y recuentos

Esta sección permanece pendiente. El marcador no contiene afirmaciones científicas ni sustituye su investigación.

# 14. Nombres y nomenclatura

## 14.1. Tres propiedades que no deben fundirse

Un nombre nomenclaturalmente disponible o válidamente publicado cumple los requisitos del código que le resulta aplicable. [C-1504; S378 arts. 10–11; S379 Principios y reglas de publicación; S380 reglas de publicación]

La disponibilidad o publicación válida de un nombre no establece que el taxón correspondiente sea monofilético. [C-1505; S378 Preámbulo; S379 Preámbulo; S380 Principios]

La aceptación de un taxón por una clasificación o base de datos es una decisión curatorial o comunitaria dependiente de versión. [C-1506; S01 introducción y clasificación; S05 tesis general]

El respaldo filogenético de un clado depende de datos, muestreo, modelo y pruebas de artefacto. [C-1507; S137 §§Phylogenomics and artefacts; S126 Methods]

Un nombre puede estar disponible y no ser aceptado por una clasificación vigente. [C-1508; S378 arts. 10–11; S01 clasificación]

Una clasificación puede usar un rótulo informal que no haya sido establecido bajo ningún código. [C-1509; S01 introducción; S05 tesis general]

Un clado puede recibir soporte filogenético antes de disponer de un nombre establecido bajo PhyloCode. [C-1510; S381 arts. 7–9; S382 §§Establishment and registration]

En este corpus, nombre disponible, taxón aceptado y clado respaldado se registran como propiedades independientes. [C-1511; n/a; convención documental]


## 14.2. Códigos aplicables

### 14.2.1. ICZN: nombres zoológicos

El ICZN regula la nomenclatura de animales bajo su ámbito. [C-1512; S378 Preámbulo; art. 1]

El ICZN no decide qué hipótesis filogenética o circunscripción taxonómica es correcta. [C-1513; S378 Preámbulo]

Bajo el ICZN, un nombre disponible debe satisfacer requisitos de publicación y formación aplicables. [C-1514; S378 arts. 10–11]

Bajo el ICZN, la prioridad participa en la selección del nombre válido entre nombres disponibles, con las excepciones previstas por el código. [C-1515; S378 art. 23; FAQ]

La validez nomenclatural bajo ICZN no equivale a verdad biológica del taxón. [C-1516; S378 Preámbulo; art. 23]

Metazoa y Animalia pueden funcionar como nombres de alto nivel en zoología sin que el ICZN resuelva por sí mismo su definición filogenética. [C-1517; S378 arts. 1 y 11.4; S381 art. 3]


### 14.2.2. ICN: Madrid Code

El Madrid Code es la decimoctava edición del ICN. [C-1518; S379 portada y prefacio]

El Madrid Code fue publicado el 21 de julio de 2025 y sustituyó al Shenzhen Code. [C-1519; S379 sitio oficial ICN]

El ICN regula nombres de organismos tratados tradicionalmente como algas, hongos y plantas dentro de su ámbito. [C-1520; S379 título; Preámbulo]

La aplicación histórica del ICN a un organismo no demuestra que ese organismo pertenezca a Archaeplastida o Fungi. [C-1521; S379 Preámbulo; S405; S406]

El nombre de un oomiceto puede estar gobernado por el ICN aunque Oomycota sea un linaje de Stramenopiles. [C-1522; S379 Preámbulo; S405 título y síntesis]


### 14.2.3. ICNP: nombres procarióticos

La revisión 2025 del ICNP fue publicada en 2026. [C-1523; S380 metadatos bibliográficos]

El ICNP regula la nomenclatura de procariotas dentro de su ámbito. [C-1524; S380 título; General Considerations]

El uso de procariota en el nombre del ICNP es una delimitación nomenclatural y no convierte a “Prokaryota” en un clado. [C-1525; S380 título; S392 tesis general; S393 discusión]

Los nombres de Asgardarchaeota y de alfa-proteobacterias se evalúan bajo códigos procarióticos o sistemas complementarios, no bajo el ICZN. [C-1526; S380 General Considerations]


### 14.2.4. PhyloCode y RegNum

PhyloCode versión 6 fue ratificado en 2019 y publicado en 2020. [C-1527; S381 portada y prefacio]

PhyloCode regula nombres de clados definidos filogenéticamente. [C-1528; S381 preámbulo; arts. 1–3 y 9]

PhyloCode no asigna rangos obligatorios a los clados. [C-1529; S381 art. 3]

PhyloCode puede operar concurrentemente con ICZN, ICN e ICNP. [C-1530; S381 preámbulo; art. 21; S382 §§Relationship to rank-based codes]

El establecimiento de un nombre bajo PhyloCode requiere una definición filogenética y el cumplimiento de requisitos de publicación y registro. [C-1531; S381 arts. 4, 7–9; S382 §§Establishment and registration]

RegNum es el registro oficial asociado con PhyloCode. [C-1532; S381 art. 8; S384 portada]

La ausencia de un resultado en una búsqueda de RegNum no demuestra por sí sola que ningún autor haya usado el nombre en la literatura. [C-1533; n/a; regla probatoria del corpus]


### 14.2.5. Phylonyms y definiciones formales localizadas

Phylonyms contiene definiciones filogenéticas iniciales asociadas con PhyloCode. [C-1534; S383 introducción]

Phylonyms no pretende contener todos los nombres de clados existentes. [C-1535; S383 introducción]

Phylonyms establece Eukarya con el número de registro 42. [C-1536; S383 entrada Eukarya, Registration 42]

Phylonyms establece Amorphea con el número de registro 8. [C-1537; S383 entrada Amorphea, Registration 8]

Phylonyms establece Opisthokonta con el número de registro 72. [C-1538; S383 entrada Opisthokonta, Registration 72]

No se localizaron en esta sesión entradas separadas de Phylonyms o RegNum para Holozoa, Filozoa, Choanozoa, Apoikozoa, Obazoa, Pluriformea o Corallochytrea. [C-1539; BN-069]


## 14.3. Rangos y marcado del corpus

Adl et al. 2019 usa una jerarquía de clados de alto nivel sin imponer una secuencia uniforme de rangos linneanos. [C-1540; S01 introducción; esquema de clasificación]

En este corpus, Eukaryota, Amorphea, Obazoa, Opisthokonta, Holozoa, Filozoa y Choanozoa sensu stricto se tratan como clados sin rango uniforme. [C-1541; n/a; convención documental basada en S01 y S381]

Los nombres de género y especie conservan el código de rangos aplicable según el tratamiento nomenclatural del organismo. [C-1542; S378; S379; S380]

Fungi puede recibir rango de reino en sistemas clasificados, pero ese rango no es una sinapomorfía. [C-1543; S387; S388; S389]

Animalia o Metazoa puede recibir rango de reino en sistemas clasificados, pero el rango no determina su relación con Choanoflagellata. [C-1544; S387; S388; S130]

La marca ⚠ identifica posición, contenido o validez discutidos. [C-1545; n/a; convención documental]

La marca ≈ identifica equivalencia condicionada por la definición o circunscripción adoptada. [C-1546; n/a; convención documental]

La marca [F] identifica un clado recuperado principalmente por filogenómica sin sinapomorfía morfológica publicada localizada. [C-1547; n/a; convención documental]

La marca [H] identifica una composición dependiente de la hipótesis topológica adoptada. [C-1548; n/a; convención documental]

La marca † se reserva para taxones con registro fósil propio. [C-1549; n/a; convención documental]

Una población ancestral reconstruida no recibe la marca †. [C-1550; n/a; convención documental]


## 14.4. Grupo corona, grupo tronco y grupo total

Grupo corona designa el último ancestro común de los representantes vivientes especificados y todos sus descendientes. [C-1551; S385 §§Crown clades; S135 §Terminology]

Grupo total incluye el grupo corona y todos los linajes extinguidos más próximos a esa corona que a cualquier corona viviente externa especificada. [C-1552; S385 §§Total clades; S135 §Terminology]

Grupo tronco es el grupo total menos el grupo corona. [C-1553; S385 §§Stem groups; S135 §Terminology]

Un fósil no pertenece a un grupo tronco solo por ser antiguo. [C-1554; S385 §§Stem and total clades]

Un linaje viviente no es miembro del grupo tronco de su linaje hermano viviente bajo la definición extante de corona y total. [C-1555; S385 §§Stem groups; S412 tesis general]

Eukaryota se usa en este corpus para el grupo corona de todos los eucariotas vivientes. [C-1556; n/a; convención documental coherente con S01 y S383 entrada Eukarya]

El tallo de Eukaryota entre FECA y LECA es una etiqueta histórica reconstruida y no equivale automáticamente al grupo tronco paleontológico definido respecto de una corona externa. [C-1557; S385 §§Stem groups; Parte 1B definiciones FECA–LECA]

La distinción corona–tallo permite que un fósil eucariota antiguo documente el grupo total sin calibrar necesariamente LECA. [C-1558; S385; S135; Parte 2 §5–6]

La conciliación propuesta entre relojes antiguos y fósiles corona más jóvenes depende de distinguir grupo tronco y grupo corona. [C-1559; S135 §Terminology; Parte 2 §6]

La aplicación de corona, tallo y total a Holozoa exige una posición filogenética del fósil que discrimine linajes internos y externos. [C-1560; S385; Parte 2 §5.5–5.8]


## 14.5. Historia y competencia de nombres del corredor

### 14.5.1. Eucarya, Eukarya y Eukaryota

Woese, Kandler y Wheelis usaron Eucarya para uno de sus tres dominios en 1990. [C-1561; S06 título; fig. 1]

Adl et al. 2019 usa Eukaryota como nombre del conjunto eucariota. [C-1562; S01 clasificación]

Phylonyms establece Eukarya mediante una definición filogenética de corona modificada por apomorfía. [C-1563; S383 entrada Eukarya, Definition]

Eucarya, Eukarya y Eukaryota se han aplicado aproximadamente al mismo gran conjunto, pero difieren en grafía, fuente y estatuto nomenclatural. [C-1564; S01; S383 entrada Eukarya; S06]

Este corpus conserva Eukaryota como etiqueta preferida y registra Eukarya sensu Phylonyms como circunscripción relacionada marcada ≈. [C-1565; n/a; convención documental derivada de C-1561–C-1564]


### 14.5.2. Unikonta, Podiata, Sulcozoa, Varisulca y Amorphea

Unikonta fue usado para un conjunto que incluía Amoebozoa y Opisthokonta y se vinculó a una reconstrucción de un aparato flagelar ancestral único. [C-1566; S89 clasificación y discusión]

La oposición Unikonta–Bikonta no coincide exactamente con Amorphea frente a los demás eucariotas. [C-1567; S124 nota de Amorphea; S137 §Root and supergroups]

Adl et al. 2012 introdujo Amorphea para reemplazar Unikonta en su clasificación. [C-1568; S124 clasificación y nota de Amorphea]

Phylonyms define Amorphea como un clado corona mínimo y trata Unikonta como sinónimo aproximado. [C-1569; S383 entrada Amorphea, Synonyms and Definition]

Phylonyms declara para Amorphea que “No non-molecular synapomorphies are known”. [C-1570; S383 entrada Amorphea, Diagnostic apomorphies]

Podiata sensu Cavalier-Smith y Podiata usado para Amorphea+CRuMs no tienen necesariamente la misma circunscripción. [C-1571; S89; S137 §Deep orphan lineages]

Sulcozoa sensu Cavalier-Smith fue concebido como un conjunto que podía ser parafilético respecto de Amoebozoa y Opisthokonta. [C-1572; S125 clasificación y discusión]

Sulcozoa no es un sinónimo moderno de Obazoa. [C-1573; S125; S111 definición de Obazoa]

Varisulca reunió linajes que hoy no constituyen CRuMs bajo la misma circunscripción. [C-1574; S125 clasificación; S137 §Deep orphan lineages]

Amorphea continúa en la clasificación de Adl et al. 2019. [C-1575; S01 clasificación]


### 14.5.3. Opisthokonta, Holomycota y Nucletmycea

Opisthokonta en su concepto moderno reúne Holozoa y Holomycota. [C-1576; S01 clasificación; S126 fig. 2]

Phylonyms establece Opisthokonta como un clado corona mínimo con el número de registro 72. [C-1577; S383 entrada Opisthokonta, Registration 72 and Definition]

El uso de Opisthokonta por Copeland en 1956 tuvo una circunscripción distinta del concepto animal-hongo moderno. [C-1578; S383 entrada Opisthokonta, Nomenclatural history]

La aplicación moderna de Opisthokonta a animales, hongos y parientes fue desarrollada por Cavalier-Smith y consolidada por filogenias posteriores. [C-1579; S383 entrada Opisthokonta, Nomenclatural history; S146]

Holomycota y Nucletmycea compiten como nombres para conjuntos ampliamente solapados del lado fúngico de Opisthokonta. [C-1580; S01 clasificación y notas; S383 entrada Opisthokonta, Composition]


### 14.5.4. Obazoa, Holozoa y Filozoa

Holozoa designa el clado opisthokonto que contiene Metazoa y sus parientes unicelulares más próximos frente a Holomycota. [C-1581; S01 clasificación; S421 tesis general]

La atribución de la primera introducción exacta de Holozoa no quedó verificada en una fuente primaria en esta sesión. [C-1582; BN-070]

Filozoa fue propuesto para Filasterea más Choanoflagellata y Metazoa. [C-1583; S130 resumen; fig. 1]

Holozoa y Filozoa no son sinónimos porque Holozoa incluye ramas externas a Filozoa. [C-1584; S01 clasificación; S130 fig. 1; S126 figs. 2 y 4]

Obazoa fue propuesto para Opisthokonta, Breviatea y Apusomonadida. [C-1585; S111 resumen; fig. 2]

Obazoa no es un rango zoológico establecido por ICZN. [C-1586; S378; S111]


### 14.5.5. Choanozoa sensu stricto y Apoikozoa

La Choanozoa histórica de Cavalier-Smith reunió protistas opisthokontos y excluyó Metazoa. [C-1587; S125 clasificación; S130 introducción]

Brunet y King usaron Choanozoa sensu stricto para Choanoflagellata más Metazoa. [C-1588; S134 glosario y definición]

Budd y Jensen propusieron Apoikozoa para Metazoa más Choanoflagellata. [C-1589; S135 resumen y nomenclatura]

Adl et al. 2019 prefirió Choanozoa sensu stricto para el clado Metazoa+Choanoflagellata. [C-1590; S01 clasificación y nota de Choanozoa]

Choanozoa sensu stricto y Apoikozoa tienen la misma circunscripción pretendida en las fuentes citadas. [C-1591; S01; S135; S134]

Choanozoa sensu stricto y Choanozoa sensu histórico no tienen la misma circunscripción. [C-1592; S125; S134]

La etimología colonial propuesta para Apoikozoa no constituye una sinapomorfía filogenética del clado. [C-1593; S134 discusión terminológica; S01 nota de Choanozoa]

Este corpus usa Choanozoa sensu stricto ≈ Apoikozoa y conserva ambas entidades de nombre por separado. [C-1594; n/a; derivación documental de C-1587–C-1593]


### 14.5.6. Pluriformea, Corallochytrea y Corallochytrium

Corallochytrium es un género. [C-1595; S01 clasificación; S129 fig. 1]

Corallochytrea es un clado que contiene Corallochytrium bajo la clasificación adoptada. [C-1596; S01 clasificación; S129 fig. 1]

Hehenberger et al. propusieron Pluriformea para Syssomonas más Corallochytrium en su muestreo. [C-1597; S129 resumen; fig. 1]

Pluriformea sensu Hehenberger et al. contiene Corallochytrea y no es sinónimo pleno de Corallochytrea. [C-1598; S01; S129 fig. 1]

Liu et al. usaron “Pluriformea/Corallochytrea” como etiqueta operacional de determinadas matrices. [C-1599; S126 Methods; figs. 2 y 4]

Pluriformea, Corallochytrea y Corallochytrium se conservan como entidades separadas en el corpus. [C-1600; n/a; derivación documental de C-1595–C-1599]


## 14.6. Advertencias terminológicas

### 14.6.1. Protista y protista

Haeckel propuso el reino Protista en 1866. [C-1601; S386 historia; S422 historia]

Las circunscripciones históricas de Protista incluyeron conjuntos distintos de microorganismos e incluso bacterias en algunos sistemas. [C-1602; S386; S422]

Protista entendido como todos los eucariotas que no son animales, plantas ni hongos es parafilético. [C-1603; S01 introducción; S137 fig. 1]

Protista no se sustituye por un único clado moderno. [C-1604; S01 clasificación; S137]

“Protista” conserva uso legítimo como rótulo histórico de un reino especificado. [C-1605; S386; S422]

“Protista” o “protista” conserva uso ecológico y organizativo para eucariotas predominantemente microbianos cuando no se presenta como clado. [C-1606; S01 introducción; S05 tesis general]


### 14.6.2. Protozoa y protozoo

Goldfuss introdujo Protozoa en 1818 como una clase de animales. [C-1607; S386 historia; S422 historia]

Protozoa histórico incluyó organismos que ya no se consideran un único linaje eucariota. [C-1608; S386; S422; S01 clasificación]

Protozoo no es sinónimo filogenético de eucariota unicelular. [C-1609; S01; S386]

El reemplazo taxonómico de Protozoa es la identificación del clado específico al que pertenece cada organismo. [C-1610; S01 clasificación]

Protozoo conserva un uso acotado en historia, medicina, parasitología y ecología cuando la categoría funcional se define. [C-1611; S386; S422]


### 14.6.3. Alga y cianobacterias

Alga no designa un único clado. [C-1612; S390 título; resumen; S01 clasificación]

Guiry distribuyó las algas documentadas por AlgaeBase entre cuatro reinos, catorce filos y sesenta y tres clases. [C-1613; S390 título; resumen]

Guiry informó 50.589 especies vivientes y 10.556 especies fósiles en AlgaeBase al 1 de noviembre de 2023. [C-1614; S390 resumen]

Las cianobacterias son Bacteria aunque “algas verdeazules” persista como nombre tradicional. [C-1615; S06 fig. 1; S391 tesis general]

Incluir cianobacterias dentro de “algas” es un uso funcional o histórico, no una afirmación de parentesco eucariota. [C-1616; S391 tesis general; S390 resumen]

Alga conserva uso legítimo en ecología, ficología y descripción de productores fotosintéticos si se identifica la circunscripción. [C-1617; S390; S391]


### 14.6.4. Invertebrado

Lamarck introdujo el uso zoológico de animales sin vértebras y se le atribuye la acuñación de invertebrados alrededor de 1801. [C-1618; S418 historia; S419 perfil institucional]

Invertebrado define animales por ausencia de vértebras. [C-1619; S419 historia; S388 clasificación]

Animalia menos Vertebrata es parafilético respecto de Vertebrata. [C-1620; S388; S137 árbol eucariota como contexto]

Invertebrado no se sustituye por un único clado. [C-1621; S388]

Invertebrado conserva uso práctico en zoología, ecología y conservación si no se presenta como grupo monofilético. [C-1622; n/a; uso disciplinario derivado de S419]


### 14.6.5. Procariota

Chatton introdujo las formas procaryotes y eucaryotes en la primera mitad del siglo XX; la prioridad exacta entre sus publicaciones de 1925 y 1937/1938 requiere distinguir uso y elaboración. [C-1623; S393 historia; S420 historia]

Stanier y van Niel reintrodujeron y difundieron la dicotomía procariota–eucariota en 1962. [C-1624; S393 historia]

Procariota define células por ausencia de un núcleo eucariota y otros rasgos de organización eucariota. [C-1625; S393 discusión conceptual]

Bacteria más Archaea excluyendo Eukaryota no forma un clado bajo un árbol de dos dominios. [C-1626; S392 tesis general; S394 discusión]

Pace propuso abandonar procariota como categoría taxonómica. [C-1627; S392 tesis general]

Procariota conserva uso descriptivo para un grado de organización celular si se aclara que no es un clado. [C-1628; S392; S393; S394]


### 14.6.6. Acritarco

Evitt introdujo acritarch en 1963 para microfósiles orgánicos de afinidad incierta. [C-1629; S395 título y propuesta; S397 historia]

Acritarco es un taxón de forma artificial y no un clado. [C-1630; S395; S396; S397]

Un acritarco cuya afinidad biológica se resuelve puede ser reclasificado fuera de Acritarcha. [C-1631; S397 texto principal]

Acritarco no es sinónimo de eucariota. [C-1632; S396 revisión; Parte 2 §5.1]

Acritarco conserva uso legítimo en paleontología y bioestratigrafía como categoría morfológica explícitamente artificial. [C-1633; S396; S397]


### 14.6.7. Reino

Whittaker propuso un sistema de cinco reinos en 1969. [C-1634; S387 título y esquema]

Cavalier-Smith publicó un sistema revisado de seis reinos en 1998. [C-1635; S389 título y resumen]

Ruggiero et al. propusieron una clasificación de siete reinos en 2015. [C-1636; S388 resumen y tabla de clasificación]

Cinco, seis y siete reinos no son tres recuentos empíricos incompatibles de una magnitud natural única. [C-1637; S387; S388; S389]

El rango reino no tiene una equivalencia filogenética uniforme entre sistemas. [C-1638; S387; S388; S389]

Reino conserva uso legítimo cuando se cita el sistema y la circunscripción adoptados. [C-1639; n/a; derivación documental de C-1634–C-1638]


### 14.6.8. Archezoa

Archezoa agrupó eucariotas interpretados como primitivamente carentes de mitocondria. [C-1640; S398 resumen e historia]

Genes de ascendencia mitocondrial fueron identificados en linajes incluidos en Archezoa. [C-1641; S398 resumen; S399 revisión]

Hidrogenosomas y mitosomas son orgánulos derivados de mitocondrias. [C-1642; S399 título y síntesis]

La hipótesis de que los miembros de Archezoa carecían primitivamente de mitocondria fue refutada. [C-1643; S398; S399]

Los antiguos miembros de Archezoa se sustituyen por sus clados filogenéticos y por descripciones del orgánulo mitocondrial reducido. [C-1644; S01 clasificación; S399]

Archezoa conserva uso legítimo como nombre histórico de una hipótesis refutada. [C-1645; S398; S399]


### 14.6.9. Excavata

Excavata fue propuesto para varios linajes de protistas con caracteres de surco alimentario y aparato flagelar comparables. [C-1646; S400 introducción; S137 §Supergroups]

Hampl et al. analizaron 143 proteínas y 48 taxones al apoyar la monofilia de Excavata. [C-1647; S400 título; Methods]

La monofilia de Excavata fue sensible a muestreo y análisis posteriores. [C-1648; S137 §Excavata and orphan lineages]

Adl et al. 2019 no usa Excavata como un supergrupo monofilético único equivalente a su circunscripción histórica. [C-1649; S01 clasificación; S137]

Excavata se sustituye en afirmaciones filogenéticas por nombres de sus clados componentes y por la topología concreta. [C-1650; S01; S137]

Excavata conserva uso histórico o comparativo cuando se especifica la circunscripción y no se presupone monofilia. [C-1651; n/a; derivación documental de S400, S137]


### 14.6.10. Chromalveolata

La hipótesis Chromalveolata propuso un origen único de plastos secundarios rojos en un ancestro común de varios grandes linajes. [C-1652; S401 título y modelo]

Chromalveolata requería pérdidas secundarias de plastos para explicar numerosos miembros no fotosintéticos. [C-1653; S401 modelo; S403 discusión]

Filogenias nucleares no recuperaron de manera estable la monofilia de los hospedadores chromalveolates. [C-1654; S137; S403]

Pietluch et al. informaron que sus filogenias plastidiales rechazaron consistentemente la monofilia original de plastos Chromalveolata. [C-1655; S404 resumen; Results]

Chromalveolata no se acepta actualmente como un único clado de hospedadores en la clasificación adoptada. [C-1656; S01; S137; S404]

El rechazo de Chromalveolata no implica que todos los plastos complejos rojos tengan orígenes totalmente independientes. [C-1657; S403 discusión; S404 Discussion]

Chromalveolata conserva uso legítimo para nombrar la hipótesis histórica y sus predicciones. [C-1658; S401; S403; S404]


### 14.6.11. Unikonta y Bikonta como advertencia terminológica

Unikonta y Bikonta codificaron reconstrucciones ancestrales de aparatos flagelares además de circunscripciones taxonómicas. [C-1659; S89; S137 §Rooting]

Los nombres Unikonta y Bikonta pueden inducir a atribuir uno o dos flagelos a todos sus miembros vivientes. [C-1660; S137; S412]

Amorphea reemplaza Unikonta en la clasificación ISP adoptada, pero no constituye sinonimia histórica exacta. [C-1661; S124 nota de Amorphea; S01]

Las raíces Opimoda–Diphoda y Opimoda+–Diphoda+ no deben denominarse simplemente Unikonta–Bikonta. [C-1662; S137 §Rooting; Parte 1C §4.2]

Unikonta y Bikonta conservan uso legítimo para describir hipótesis históricas con su circunscripción original. [C-1663; n/a; derivación documental de C-1659–C-1662]


### 14.6.12. Hongo aplicado a oomicetos y mohos mucilaginosos

Los oomicetos fueron llamados hongos por convergencias de crecimiento filamentoso, absorción y reproducción por esporas. [C-1664; S405 introducción y revisión]

Oomycota pertenece a Stramenopiles y no a Fungi. [C-1665; S405 título y filogenia; S01 clasificación]

Los mohos mucilaginosos no constituyen Fungi. [C-1666; S406; S407; S01]

Diversos mohos mucilaginosos pertenecen a Amoebozoa. [C-1667; S406 filogenia; S407 filogenia]

“Hongo” aplicado a oomicetos o mohos mucilaginosos no equivale a pertenencia taxonómica a Fungi. [C-1668; S405, S406, S407]

“Fungus-like” o “semejante a hongo” conserva uso ecológico si se acompaña del clado real. [C-1669; n/a; derivación documental de S405, S406, S407]


### 14.6.13. Flagelo

El flagelo bacteriano es un motor rotatorio extracelular ensamblado con proteínas bacterianas. [C-1670; S408 comparación estructural]

El cilio o flagelo eucariota se basa en microtúbulos, dineínas y membrana celular. [C-1671; S408 comparación estructural]

El flagelo bacteriano y el cilio eucariota no son estructuras homólogas como orgánulos completos. [C-1672; S408 síntesis comparada]

El término flagelo sin calificador mezcla sistemas no homólogos. [C-1673; S408]

Este corpus usa flagelo bacteriano y cilio eucariota, conservando “flagelo eucariota” solo cuando reproduce la terminología de una fuente. [C-1674; n/a; convención documental]


### 14.6.14. Simbiosis y mutualismo

Simbiosis tiene usos históricos amplios que incluyen mutualismo, comensalismo y parasitismo. [C-1675; S409 revisión terminológica]

Simbiosis no es sinónimo necesario de mutualismo. [C-1676; S409 resumen y discusión]

Mutualismo describe una asociación con beneficio neto para ambos participantes bajo las condiciones especificadas. [C-1677; S409 terminología]

Parasitismo puede ser una forma de simbiosis bajo la definición amplia. [C-1678; S409 revisión terminológica]

Toda aparición de simbiosis en este corpus debe especificar efecto, localización, duración y transmisión cuando se conozcan. [C-1679; n/a; convención documental derivada de S409]


### 14.6.15. Endosimbiosis seriada

Sagan formuló en 1967 una teoría de origen endosimbiótico seriado de componentes de la célula eucariota. [C-1680; S410 título y modelo]

El origen bacteriano de mitocondrias es un componente aceptado de la teoría endosimbiótica. [C-1681; S411 síntesis; Parte 1A §2.6]

El origen cianobacteriano de plastos primarios es un componente aceptado de la teoría endosimbiótica. [C-1682; S411 síntesis]

La propuesta de un origen espiroquetal de cilios y cuerpos basales no obtuvo apoyo comparable. [C-1683; S411 evaluación histórica]

Aceptar el origen endosimbiótico de mitocondrias y plastos no implica aceptar todos los componentes de la formulación histórica. [C-1684; S410; S411]

Endosimbiosis seriada conserva uso legítimo si se enumeran los episodios concretos y su estado probatorio. [C-1685; S410; S411]


### 14.6.16. Eucariota primitivo

“Eucariota primitivo” aplicado a un linaje viviente confunde descendencia actual con estado ancestral. [C-1686; S412; S413]

Un linaje viviente puede conservar un estado plesiomórfico para un carácter y ser derivado para otros. [C-1687; S412; S413]

“Plesiomórfico para el carácter X respecto del nodo Y” sustituye a “primitivo” cuando la reconstrucción lo sostiene. [C-1688; S412; S413]

“Eucariota primitivo” conserva uso legítimo únicamente como cita histórica o como término explícitamente criticado. [C-1689; n/a; derivación documental de S412, S413]


### 14.6.17. Organismo simple

La complejidad biológica puede medirse mediante dimensiones distintas, como número de tipos celulares, redes regulatorias, estructura genómica o organización morfológica. [C-1690; S414 capítulos 1–3]

“Organismo simple” sin una métrica explícita no produce una comparación auditable. [C-1691; S414]

Un organismo unicelular no es necesariamente simple en genoma, ciclo vital, regulación o ecología. [C-1692; S414; Parte 2 §8]

“Simple” conserva uso legítimo solo con una variable, método y comparación declarados. [C-1693; S414]


### 14.6.18. Fósil viviente

Living fossil se ha aplicado mediante criterios distintos de estasis morfológica, baja diversidad, larga duración o semejanza con fósiles. [C-1694; S415 revisión; S416 revisión]

Ningún linaje viviente ha dejado de evolucionar desde su divergencia. [C-1695; S415; S416]

“Fósil viviente” puede ocultar diferencias entre estasis de un carácter y estasis del organismo completo. [C-1696; S415 discusión]

“Linaje con estasis morfológica documentada en el carácter X durante el intervalo Y” sustituye una afirmación vaga de fósil viviente. [C-1697; S415; S416]

Fósil viviente conserva uso acotado como rótulo histórico o heurístico si sus criterios se especifican y no significa “sin cambios”. [C-1698; S415; S416]


### 14.6.19. Eslabón perdido

“Eslabón perdido” representa la evolución como una cadena lineal con huecos discretos. [C-1699; S417 tesis general; S423]

Un fósil transicional no tiene que ser ancestro directo de un linaje viviente. [C-1700; S417; S423]

“Fósil transicional” o “miembro del grupo tronco” sustituye a “eslabón perdido” cuando la topología lo permite. [C-1701; S385; S417]

No se localizó en esta sesión una atribución primaria inequívoca de la primera acuñación científica de “missing link”. [C-1702; BN-071]

Eslabón perdido conserva uso legítimo únicamente como objeto de historia cultural o crítica terminológica. [C-1703; n/a; derivación documental de S417]


### 14.6.20. Basal aplicado a un linaje viviente

Basal puede aplicarse comparativamente a un nodo situado más cerca de una raíz que otro nodo en la misma ruta. [C-1704; S412 fig. 1 y texto]

Basal aplicado a un linaje viviente como sinónimo de ancestral es incorrecto. [C-1705; S412 resumen y discusión]

Dos linajes vivientes hermanos tienen la misma duración evolutiva desde su ancestro común. [C-1706; S412; S413]

Un linaje con pocas especies no es por ello más basal que su hermano con muchas especies. [C-1707; S412 fig. 1; S423]

“Rama que diverge primero en el árbol enraizado bajo la hipótesis H” sustituye a “linaje basal”. [C-1708; S412; S413]

Basal conserva uso legítimo para nodos o divergencias comparadas con una referencia especificada. [C-1709; S412]


## 14.7. Integración terminológica y límites

Los términos protista, protozoo, alga, invertebrado, procariota y acritarch no comparten el mismo tipo de problema. [C-1710; S01; S386; S390; S392; S395]

Protista e invertebrado son principalmente agrupaciones residuales parafiléticas en sus usos amplios. [C-1711; S01; S388; S137]

Alga y protozoo son categorías funcionales e históricas con circunscripciones variables y múltiples orígenes. [C-1712; S386; S390]

Acritarco es una categoría paleontológica artificial que puede contener organismos de afinidades distintas. [C-1713; S395, S396, S397]

Procariota combina una descripción celular útil con una lectura taxonómica parafilética bajo dos dominios. [C-1714; S392, S393, S394]

Archezoa y Chromalveolata son hipótesis históricas modificadas o rechazadas por contraevidencia específica. [C-1715; S398, S399, S400, S137, S401, S402, S403, S404]

“Basal”, “primitivo”, “simple”, “fósil viviente” y “eslabón perdido” pueden introducir una lectura escalonada si no se operacionalizan. [C-1716; S412, S413, S414, S415, S416, S417; S423]

El reemplazo preferido es nombrar clado, carácter, interacción, métrica, topología y circunscripción concretos. [C-1717; n/a; síntesis documental de C-1710–C-1716]

No se localizó una autoridad única que resuelva todas las circunscripciones ambiregnales de protistas entre ICZN e ICN. [C-1718; BN-072]

No se buscó el estatuto nomenclatural individual de cada género y especie mencionado en el corpus porque requeriría una auditoría nominal separada. [C-1719; BN-073]

## 14.8. Vistas de resumen

### 14.8.1. Códigos

| código o recurso | ámbito | qué puede establecer | qué no establece | filas |
| --- | --- | --- | --- | --- |
| ICZN | nomenclatura zoológica | disponibilidad y validez de nombres zoológicos | No decide monofilia ni topología | C-1512–C-1517 |
| ICN, Madrid Code | nombres de algas, hongos y plantas según ámbito tradicional | publicación válida, prioridad y tipificación bajo sus reglas | El ámbito histórico no equivale a Archaeplastida o Fungi | C-1518–C-1522 |
| ICNP 2025 Revision | nomenclatura procariótica | nombres de bacterias y arqueas bajo el código | “Procariota” en el título no crea un clado | C-1523–C-1526 |
| PhyloCode v6 | nombres de clados | definiciones filogenéticas, establecimiento y registro | No reemplaza necesariamente los códigos de rangos | C-1527–C-1533 |
| Phylonyms/RegNum | definiciones y registro bajo PhyloCode | entradas establecidas y números de registro | La cobertura no es exhaustiva | C-1534–C-1539 |

### 14.8.2. Nombres rivales o solapados

| nombres | relación | motivo | etiqueta preferida | filas |
| --- | --- | --- | --- | --- |
| Eucarya / Eukarya / Eukaryota | ≈ | Mismo gran referente pretendido con grafías y estatutos diferentes | Eukaryota | C-1561–C-1565 |
| Unikonta / Amorphea | ≈ | Reemplazo clasificatorio con circunscripción y diagnóstico modificados | Amorphea | C-1566–C-1570; C-1575 |
| Podiata | ≈ ⚠ | Circunscripciones de autor no coincidentes | Podiata con autor y definición | C-1571 |
| Sulcozoa / Obazoa | no equivalentes | Contenido histórico parafilético frente a clado filogenómico | Obazoa para el clado | C-1572–C-1573; C-1585–C-1586 |
| Varisulca / CRuMs | no equivalentes | Composición distinta | CRuMs o linajes componentes | C-1574 |
| Holomycota / Nucletmycea | ≈ ⚠ | Clados solapados con preferencias de autor | Nombre con circunscripción | C-1580 |
| Holozoa / Filozoa | no equivalentes | Filozoa está anidado en Holozoa | Ambos como entidades separadas | C-1581–C-1584 |
| Choanozoa histórico / Choanozoa s.s. | no equivalentes | El histórico excluye Metazoa | Choanozoa sensu stricto | C-1587–C-1588; C-1592 |
| Choanozoa s.s. / Apoikozoa | ≈ | Misma circunscripción pretendida, historias y preferencias diferentes | Choanozoa s.s. ≈ Apoikozoa | C-1588–C-1594 |
| Pluriformea / Corallochytrea / Corallochytrium | anidación, no sinonimia plena | Clado amplio, clado contenido y género | Tres entidades | C-1595–C-1600 |

### 14.8.3. Términos problemáticos y reemplazos

| término | estado | reemplazo o uso acotado | filas |
| --- | --- | --- | --- |
| protista / Protista | parafilético o informal | clado específico; “protista” solo como rótulo no cladístico | C-1601–C-1606 |
| protozoo | polifilético/parafilético según uso | clado y modo de alimentación específicos | C-1607–C-1611 |
| alga | funcional y no monofilético | clado fotosintético o función declarada | C-1612–C-1617 |
| invertebrado | categoría negativa parafilética | clado animal concreto | C-1618–C-1622 |
| procariota | grado celular; parafilético como taxón en dos dominios | Bacteria, Archaea o descripción celular explícita | C-1623–C-1628 |
| acritarco | taxón de forma artificial | afinidad biológica si se resuelve; si no, acritarch operacional | C-1629–C-1633 |
| reino | rango dependiente de sistema | sistema y circunscripción citados | C-1634–C-1639 |
| Archezoa | hipótesis refutada | clados específicos y orgánulo relacionado con mitocondria | C-1640–C-1645 |
| Excavata | supergrupo histórico discutido | clados componentes y topología | C-1646–C-1651 |
| Chromalveolata | hipótesis histórica superada en forma original | linajes hospedadores y plastidiales específicos | C-1652–C-1658 |
| Unikonta / Bikonta | nombres históricos con diagnóstico ancestral discutido | Amorphea o topología de raíz explícita | C-1659–C-1663 |
| hongo para oomicetos/mohos mucilaginosos | semejanza convergente | Stramenopiles o Amoebozoa; “fungus-like” acotado | C-1664–C-1669 |
| flagelo | ambigüedad entre sistemas no homólogos | flagelo bacteriano, archaellum o cilio eucariota | C-1670–C-1674 |
| simbiosis | no equivale necesariamente a mutualismo | tipo de interacción, efecto y transmisión | C-1675–C-1679 |
| endosimbiosis seriada | propuesta compuesta | episodios e hipótesis componentes | C-1680–C-1685 |
| eucariota primitivo | lectura ancestralizante | estado plesiomórfico X respecto del nodo Y | C-1686–C-1689 |
| organismo simple | métrica ausente | variable de complejidad explícita | C-1690–C-1693 |
| fósil viviente | criterios múltiples y riesgo de “sin cambios” | estasis del carácter X en intervalo Y | C-1694–C-1698 |
| eslabón perdido | metáfora lineal | fósil transicional o miembro del tallo | C-1699–C-1703 |
| basal aplicado a viviente | confunde terminal y ancestro | rama que diverge primero bajo árbol y raíz especificados | C-1704–C-1709 |

## 14.9. Registro de afirmaciones de la sección 14

> **Registro de afirmaciones:** [data/afirmaciones/14.csv](../data/afirmaciones/14.csv) (216 filas; 12 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---

# 15. Búsquedas negativas y huecos provisionales

Esta sección consolida las búsquedas negativas de las entregas integradas. Todavía no sustituye el mapa probatorio completo exigido para la sección 15 final.

## 15.1. Punto de partida y participantes celulares

La tabla distingue ausencia declarada por la literatura, resultado no localizado en esta sesión y material deliberadamente reservado para otra entrega.

> **Búsquedas negativas:** [data/busquedas_negativas/15_1_15-1-punto-de-partida-y-participantes-celulares.csv](../data/busquedas_negativas/15_1_15-1-punto-de-partida-y-participantes-celulares.csv) (9 filas; 6 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---

## 15.2. Eucariogénesis

La búsqueda de prioridad histórica individual para LBCA, LACA y FECA no produjo una fuente inequívoca en esta sesión. [C-401; BN-010]

No se localizó una medición directa de la duración FECA–LECA independiente de un reloj molecular. [C-402; BN-011]

No se localizó una cifra publicada de coste energético de mantener una envoltura nuclear ancestral específica de FECA o LECA. [C-403; BN-012]

No se buscó en esta parte una cronología fósil completa de cada innovación celular porque corresponde a las secciones 5 y 6 ya tratadas en la Parte 2. [C-404; BN-013]

> **Búsquedas negativas:** [data/busquedas_negativas/15_2_15-2-eucariogenesis.csv](../data/busquedas_negativas/15_2_15-2-eucariogenesis.csv) (10 filas; 6 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

## 15.3. Raíz eucariota y corredor filogenético

> **Búsquedas negativas:** [data/busquedas_negativas/15_3_15-3-raiz-eucariota-y-corredor-filogenetico.csv](../data/busquedas_negativas/15_3_15-3-raiz-eucariota-y-corredor-filogenetico.csv) (17 filas; 4 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---

## 15.4. Registro material, tiempo, ambiente y ecología

| etiqueta | hueco | términos exactos | consecuencia documental |
| --- | --- | --- | --- |
| NO LOCALIZADO EN ESTA SESIÓN | Sinapomorfía morfológica diagnóstica de Amorphea | `Amorphea morphological synapomorphy fossil`; `Amorphea diagnostic morphology` | No se asignó ningún fósil al nodo por un carácter morfológico exclusivo. |
| NO LOCALIZADO EN ESTA SESIÓN | Sinapomorfía morfológica diagnóstica de Obazoa | `Obazoa morphological synapomorphy`; `Obazoa fossil record` | Se mantuvo `SIN SINAPOMORFÍA MORFOLÓGICA PUBLICADA LOCALIZADA` fuera de cualquier inferencia. |
| NO LOCALIZADO EN ESTA SESIÓN | Fósil diagnóstico de Filozoa o Choanozoa sensu stricto | `Filozoa fossil diagnostic`; `choanoflagellate animal common ancestor fossil`; `Apoikozoa fossil` | Las celdas nodales se marcaron como no localizadas. |
| NO LOCALIZADO EN ESTA SESIÓN | Intervalos nodales comparables de Amorphea, Obazoa, Holozoa y Filozoa en una sola matriz de reloj | `Amorphea Obazoa Holozoa Filozoa molecular clock supplementary table`; `holozoan divergence times relaxed clock` | No se produjo una tabla nodal completa ni una interpolación. |
| NO LOCALIZADO EN ESTA SESIÓN | Temperatura media global mesoproterozoica comparable entre proxies | `Mesoproterozoic global mean temperature proxy estimate`; `Mesoproterozoic temperature quantitative reconstruction` | La sección 7 conserva el hueco sin cifra. |
| NO LOCALIZADO EN ESTA SESIÓN | Serie homogénea de Mo, Fe, Cu, Zn, Ni y Co para todo el Proterozoico | `Proterozoic trace metal Mo Fe Cu Zn Ni Co quantitative time series`; `Proterozoic seawater trace metals compilation` | No se ensambló una curva sintética entre proxies incompatibles. |
| NO LOCALIZADO EN ESTA SESIÓN | Fracciones globales únicas de océano óxico, ferruginoso y euxínico | `global fraction oxic ferruginous euxinic Proterozoic ocean`; `Mesoproterozoic ocean redox area fraction` | Se conservaron reconstrucciones cualitativas y compilaciones, sin porcentaje inventado. |
| NO LOCALIZADO EN ESTA SESIÓN | Densidad celular de comunidades proterozoicas atribuibles al corredor | `Proterozoic microbial eukaryote cell density abundance estimate`; `Mesoproterozoic protist abundance cells` | Se declaró ausencia de estimación localizada. |
| NO LOCALIZADO EN ESTA SESIÓN | Escala geográfica única de dispersión de eucariotas microbianos del corredor | `choanoflagellate biogeography distance population structure`; `filasterean dispersal population genetics`; `ichthyosporean biogeography` | Los estudios recuperados fueron específicos de especie y marcador. |
| NO LOCALIZADO EN ESTA SESIÓN | Umbral universal de EroS | `EroS dose threshold Salpingoeca rosetta chondroitinase concentration`; `Vibrio fischeri EroS units mating dose` | Se registraron tiempos de respuesta, no una dosis universal. |
| NO LOCALIZADO EN ESTA SESIÓN | Cinética comparable de reversión al retirar RIF-1, EroS o condiciones de agregación | `Salpingoeca rosetta RIF withdrawal reversibility`; `EroS washout mating reversal`; `Capsaspora aggregate reversal kinetics` | No se equipararon respuestas con protocolos distintos. |
| NO LOCALIZADO EN ESTA SESIÓN | Tasas comparables de ingestión y aclaramiento para todos los linajes solicitados | `Monosiga Salpingoeca clearance rate bacteria`; `apusomonad feeding rate`; `breviate ingestion rate`; `filasterean clearance rate`; `ichthyosporean feeding rate` | Solo se retuvieron relaciones de tamaño y mecanismos observados. |
| NO LOCALIZADO EN ESTA SESIÓN | Costes energéticos directos de rosetas, agregados y coenocitos | `Salpingoeca rosette energetic cost`; `Capsaspora aggregation ATP cost`; `Sphaeroforma coenocyte energetic cost` | No se reemplazó el hueco con analogías bioenergéticas. |
| NO LOCALIZADO EN ESTA SESIÓN | Fichas primarias completas de *Ichthyophonus*, *Abeoforma*, *Pirum*, *Entamoeba*, *Pelomyxa* y *Mastigamoeba* | `Ichthyophonus hoferi life cycle host primary`; `Abeoforma Pirum ecology primary`; `Pelomyxa methanogen endosymbiont primary`; `Mastigamoeba ecology primary` | Quedaron explícitamente pendientes para la siguiente parte ecológica/asociativa. |
| NO LOCALIZADO EN ESTA SESIÓN | Tamaños auditables de mimivirus, pandoravirus, medusavirus y pitovirus en una misma fuente | `mimivirus pandoravirus medusavirus pithovirus genome size comparison primary` | Se evitó compilar valores de fuentes heterogéneas sin localizador común. |
| NO BUSCADO | Glaciación huroniana con cronología y temperatura detalladas | n/a | Se priorizaron el intervalo mesoproterozoico y las glaciaciones criogénicas en esta parte; queda para ampliación ambiental. |
| NO BUSCADO | Excursiones isotópicas de carbono distintas de Lomagundi–Jatuli | n/a | El cierre ambiental completo queda para la integración de la sección 7. |

---

## 15.5. Asociación, integración y transferencia

> **Búsquedas negativas:** [data/busquedas_negativas/15_5_15-5-asociacion-integracion-y-transferencia.csv](../data/busquedas_negativas/15_5_15-5-asociacion-integracion-y-transferencia.csv) (12 filas; 5 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---

## 15.6. Rasgos con costo y controversia energética

> **Búsquedas negativas:** [data/busquedas_negativas/15_6_15-6-rasgos-con-costo-y-controversia-energetica.csv](../data/busquedas_negativas/15_6_15-6-rasgos-con-costo-y-controversia-energetica.csv) (10 filas; 5 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---

## 15.7. Sexo, meiosis y ciclo vital

> **Búsquedas negativas:** [data/busquedas_negativas/15_7_15-7-sexo-meiosis-y-ciclo-vital.csv](../data/busquedas_negativas/15_7_15-7-sexo-meiosis-y-ciclo-vital.csv) (10 filas; 5 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---

## 15.8. Nombres y nomenclatura

> **Búsquedas negativas:** [data/busquedas_negativas/15_8_15-8-nombres-y-nomenclatura.csv](../data/busquedas_negativas/15_8_15-8-nombres-y-nomenclatura.csv) (8 filas; 4 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.


## 15.9. Multicelularidad y repertorio preanimal

> **Búsquedas negativas:** [data/busquedas_negativas/15_9_15-9-multicelularidad-y-repertorio-preanimal.csv](../data/busquedas_negativas/15_9_15-9-multicelularidad-y-repertorio-preanimal.csv) (14 filas; 5 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

---

# Apéndice A. Fuentes



> **Apéndice procesable:** [data/apendices/A_fuentes.csv](../data/apendices/A_fuentes.csv) (446 filas; 9 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

# Apéndice B. Entidades



> **Apéndice procesable:** [data/apendices/B_entidades.csv](../data/apendices/B_entidades.csv) (1518 filas; 5 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

# Apéndice C. Eventos



> **Apéndice procesable:** [data/apendices/C_eventos.csv](../data/apendices/C_eventos.csv) (106 filas; 8 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

# Apéndice D. Fechas



> **Apéndice procesable:** [data/apendices/D_fechas.csv](../data/apendices/D_fechas.csv) (258 filas; 10 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

# Apéndice E. Hipótesis



> **Apéndice procesable:** [data/apendices/E_hipotesis.csv](../data/apendices/E_hipotesis.csv) (81 filas; 8 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

# Apéndice F. Magnitudes



> **Apéndice procesable:** [data/apendices/F_magnitudes.csv](../data/apendices/F_magnitudes.csv) (446 filas; 9 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

# Apéndice G. Material no encajado



> **Apéndice procesable:** [data/apendices/G_material_no_encajado.csv](../data/apendices/G_material_no_encajado.csv) (30 filas; 5 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

# Apéndice H. Recuento de control

> **Apéndice procesable:** [data/apendices/H_recuento_control.csv](../data/apendices/H_recuento_control.csv) (20 filas; 2 columnas). La versión autocontenida reproduce aquí la tabla Markdown generada desde ese CSV.

# 19. Mapa provisional de las seis preguntas de cierre

| pregunta | secciones con material integrado | estado provisional |
| --- | --- | --- |
| 1. ¿Qué hace estable una asociación inicialmente conflictiva? | 3.5–3.7; 8; 9.2; 9.6; 9.7; 9.9; 10.7–10.10; 12.5 | Hay mecanismos, correlatos, parentesco, reconocimiento y límites bioenergéticos citados; no se localizó un criterio universal de estabilidad. |
| 2. ¿Cómo cambian los costos y beneficios con el ambiente? | 7; 8; 9.2; 9.7; 10.0–10.10; 11.4–11.6; 11.9; 12.2; 12.6 | La tabla de 10 conserva denominadores y condiciones; las secciones 11–12 añaden señales, respuestas reversibles y compensaciones experimentales; faltan tasas evolutivas de 13. |
| 3. ¿Cuándo una dependencia se vuelve heredable? | 9.0; 9.1; 9.4–9.7 | Se distinguen transmisión, EGT, importación y reducción; no se localizó un umbral universal. |
| 4. ¿Qué distingue divergencia, transferencia e integración? | 3; 4; 9.0; 9.4; 9.9; 9.10 | Las clases de evento y sus participantes están separadas en el apéndice C. |
| 5. ¿Cómo puede la misma evidencia apoyar reconstrucciones diferentes? | 2–6; 9.7; 9.9; 9.10; 10.7–10.9; 11.2; 11.7; 11.8; 12.7–12.11; 15 | Se documentan dependencias de modelo, denominador, muestreo, contaminación, anotación, homología, función y reconstrucción ancestral. |
| 6. ¿Qué rasgos están observados y cuáles inferidos? | 0; 10.1; 11.2; 11.7; 11.8; 11.11; 12.1–12.12; registros C; apéndices D y F | Cada fila declara fuerza, motivo y resolución; la sección 12 separa morfología, respuesta reversible, homología, presencia génica, función y reconstrucción ancestral. |
