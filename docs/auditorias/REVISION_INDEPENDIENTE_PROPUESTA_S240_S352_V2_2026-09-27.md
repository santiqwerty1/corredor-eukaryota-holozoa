# Reinspección independiente S240/S352 — propuesta v2

Revisor: `/root/revision_residuales/candidatos_editoriales`, distinto del autor `/root/inspeccion_relojes`. Rama comprobada: `codex/cierre-plan-pendiente`. Propuesta inmutable: `PROPUESTA_AUTOR_6_CELDAS_S240_S352_V2_2026-09-27.json`, SHA256 `96d36be9adeed056a5c5f6da54321101b2dc25e7ae1bc28cb9258dae0b3e8bfa`.

Captura propia de objetos/pasajes: 2026-09-27T03:16:51Z. Cuatro expedientes de disposición: 03:20:10Z. CSV nominal: 03:22:59Z. Cobertura de 44 componentes: 03:24:30Z. No se modificaron canon, propuestas, fuentes, inventario ni firmas globales; los rechazos v1 se conservan.

## Resultado

**El paquete completo sigue NO_CONFORME.** Se han leído los 40 registros nuevos, dos correcciones, dos filas conservadas y los derivados propuestos; no se heredan conformidades de v1. Se emiten cuatro revisiones prospectivas de disposición conformes, ligadas a objetos exactos, no a una integración ya realizada.

| Disposición | Componentes | Resultado |
| --- | ---: | --- |
| C2708, comparación nuclear | 3 | Conforme prospectiva; C1037/C2839 y fuentes exactas |
| C2709, EGT y captación propuesta | 4 | Conforme prospectiva; hipótesis no convertidas en demostración |
| C2468, Hedgehog de Monosiga | 8 | Componentes primarios sustentados; sin firma por representación del bloque pendiente |
| C2469, Hedgehog de Capsaspora | 8 | Conforme prospectiva; ausencia de anotación y ortología incierta separadas |
| C2474, familias 7TM de Monosiga | 10 | No conforme: Motivo equivocado de C2876/C2877 |
| C2475, familias 7TM de Capsaspora | 11 | Conforme prospectiva; seis de ocho y familias nominales cotejadas |

Los cuatro JSON conformes cubren 26 componentes. El inventario independiente cubre los 44: 42 componentes científicos acotados tienen soporte; dos conservan NC de trazabilidad porque la fila C completa justifica el resultado con otra familia. Los ocho componentes de C2468 no quedan falsificados por el bloqueo editorial: su disposición no depende por hash de C1581, sino de C2843–C2849. Retener la firma del bloque no es inventar una carencia de fuente.

## C1581: conflicto real de representación

La fila canónica y la conservada en v2 coinciden, SHA de objeto `9bdb1a21bbf293aed15a0e5a71b4bc62ac893567a672da0f7a356d3fd3f0ce16`. Dictamen: **NO_CONFORME**.

- Reúne receptores y ligandos en Capsaspora y Monosiga: cuatro combinaciones que pueden diferir. Incumple el mandato de una proposición por fila (R0343 y prueba de atomicidad de §16).
- `S352 §Signalling pathways` no es el epígrafe del artículo. El pasaje está en Results → Gene repertoire of Capsaspora, cuarto párrafo hijo directo. R0356 exige localizador real; conservar un error previo no lo vuelve localizador válido.
- Conserva `Fuerza=alta`, `Resolución=resuelta` y `Vigencia=vigente`. Describirla como histórica en una explicación no cambia esos campos ni establece que todo el objeto haya pasado revisión.
- El texto de S352 efectivamente contiene la negación general. Fig.4, leída visualmente con la leyenda completa, representa Patched, Dispatched, Hedge y Hog en gris/punteado para Monosiga; no son por ello demostraciones de función receptora ni un ligando completo. La posición textual debe preservarse y atribuirse junto a la información que limita su lectura.

R0378 dice literalmente que la fila cuestionada se conserva intacta. El protocolo de censo no ofrece excepción a atomicidad/localización para filas así conservadas. No es posible aprobar simultáneamente esta fila canónica compuesta e intacta y afirmar que cada fila es atómica. Corregir el epígrafe es una reparación editorial comprobable, no retirar la posición científica; pero no resuelve por sí sola la atomicidad ni autoriza silenciosamente una excepción a «intacta».

**Decisión necesaria para el cierre global:** autorizar una representación que preserve íntegramente el original en evidencia histórica y descomponga su representación canónica activa, con identidad/procedencia y posiciones/contraevidencias conservadas. Este revisor no ejecuta ni presupone esa autorización. No hace falta esperar esa decisión para leer o corregir otros objetos independientes. Tampoco procede degradar validadores, excluir C1581 del censo o cambiarle los estados sin evidencia por conveniencia de cierre.

## Otros defectos nominales

**C2851** depende de C1581 NC. La tensión contextual receptor/Patched es real, pero la nueva síntesis no sanea el objeto original ni habilita su cierre. **C2852** añade además un blanco más fuerte: interpreta la falta de ligandos como falta de cualquier componente semejante. C1581 no dice eso. La distribución de dominios Hedge/Hog en proteínas distintas no demuestra un ligando Hedgehog completo, como reconoce la propia propuesta. Conservar ambas descripciones y advertir su no equivalencia es válido; dirigir una contraevidencia a una proposición ampliada por el redactor no lo es. C2847–C2849, sobre los dominios, sí tienen soporte. C2850 se limita al contraste contextual de receptor/Patched y no se interpreta como prueba funcional.

**C2876 y C2877**, Motivo: la primera versa sobre ITR-like y la segunda sobre OA1-like, pero ambas justifican su resultado con «La fila Frizzled sin punto…». La prosa afirmativa, la figura y los localizadores sí sostienen sus ausencias nominales. No obstante, la fila completa exige que el Motivo justifique su propio objeto: ambas reciben NC hasta corregir esa copia. Por eso no se firma C2474 aunque sus datos biológicos estén localizados.

**B incompleto:** las 40 altas son nominalmente coherentes, pero faltan métodos explícitos del lote. El probe registra búsquedas precisas para Illumina HiSeq, SGA, Velvet, SSPACE, Gapfiller, Image, ICORN, REAPR, HMMER, RAxML, PhyloBayes, BLASTP, FastTree y crio-SEM. Se distinguieron falsos positivos léxicos (Asgard/SGA, fibroblastos/BLAST) de entidades reales. Comprobación posterior al CSV, 03:23–03:24 UTC: también falta LG+G+F, presente en Motivo C2840 y publicado en S240 Methods; CAT y TEM sí tienen entidades previas. No se presenta esta lista nominal como censo exhaustivo de B. FastTree ya aparece en C2824; la primera aparición de una entidad nueva no debe inventarse. Los nombres sólo presentes en F pueden enlazarse explícitamente a su C de soporte, distinguiendo esa ancla de una supuesta mención literal previa.

Estos defectos afectan asimismo a los deltas de prosa/roll-up que los citan, según cada fila del CSV. No se declaran falsas todas las oraciones que comparten un párrafo ni se transfieren NC a las otras celdas de una tabla.

## Pasajes y límites científicos revisados

**S240/S563.** Se releyeron directamente Par7/Par10/Par14–16, Table1 con nota b y Methods → Phylogenomics de S240. Para S563 se leyeron metadatos y contexto de Results → Comparative Analysis of Kinetoplastid Genomes, DNA Preparation and Sequencing y Genome Assembly. La cifra de Bodo Konstanz, 39.9 Mbp, se conserva como reconstrucción por ensamblaje y comparando de vida libre. Perkinsela ~9.5 Mbp es estimación nuclear, no medición citométrica. No se calcula razón ni se aprueba el dato mitocondrial de C1041.

Los ocho genes de Par14 son candidatos probablemente derivados del endosimbionte entre 3.846 alineamientos con filogenias interpretables. No son ocho eventos observados ni todo el genoma del hospedador. El procedimiento publicado incluye cribado, curación y modelos LG+G+F/CAT; no se adjudican aquí topologías o soportes de cada gen individual fuera de lo expresado en el recuento. Par16 distingue invaginaciones/vesículas observadas, interpretación que «suggest», especulación sobre metabolitos y posibilidad adicional de enzimas. Las C nuevas conservan esa modalidad, el destino vesicular desconocido y la falta de atribución de un retorno dirigido a productos de esos ocho genes. Son mecanismos especulativos sin nombre propio: §17 E no obliga a inventarles una hipótesis con nombre, rivales o falsadores sólo porque contienen lenguaje modal.

**S352.** Se leyó el párrafo completo Gene repertoire of Capsaspora p4 y Methods → Gene family analysis. Se reinspeccionó visualmente Fig.4 p6, no sólo su leyenda. En el suplemento se leyeron Note5 pp94–96 y se renderizaron de nuevo Fig.S26 pp43–44 para lectura propia. La leyenda identifica el punto como presencia; en Monosiga están Glutamate, Adhesion/Secretin, cAMP y GPR108-like, y no hay puntos en Rhodopsin, Frizzled, ITR-like u OA1-like. En Capsaspora están las seis familias nominales propuestas y faltan Rhodopsin/Frizzled. El número seis de ocho se publica en p94, no se inventa sumando puntos. Estas anotaciones no demuestran acoplamiento funcional de cada receptor ni justifican negar todos los GPCR.

En Capsaspora, Note5 declara por separado Hh, Dispatched, Patched, Smoothened, Hint/Hog y Hedge no identificados; la ortología de CAOG_06541 respecto de Gli queda explícitamente incierta. No se convierte el símbolo de Gli en Fig.4 en ausencia de todas las proteínas semejantes. La atribución negativa de ligandos Rhodopsin procede del párrafo general, no se infiere desde la ausencia de un receptor. Los métodos de homología/arquitectura/filogenias delimitan el significado de presencia y ausencia.

## Fuentes, cronología y no solapamiento

Los cinco hashes de artefactos leídos coinciden con la propuesta. S563 XML y el suplemento S352 siguen en `/tmp`; los JSON de disposición enlazan sus destinos propuestos y hashes, y declaran expresamente dónde se leyeron. No se afirma que esos destinos ya existan. El consumidor deberá comprobar bytes idénticos, fuentes/C integradas e identidad de la fila al materializar.

La única huella de archivo base divergente es F_magnitudes.csv, por la integración independiente de localizadores de C031 comunicada por raíz. Se verificó sin escribir: sustituir en memoria solamente la fila C031 posterior por la anterior y serializar idénticamente recupera `04430032764e8e940abe33a9804a1663e9b7086dcab6c6c2feb7a0f1b9969110`, exactamente la base v2. F actual es `5cd817e3ddda5dfba34b45e8a0ce7ecd1f1202ab1e2eaa9282a01808a54b3c77`. La F previa de C1037 continúa presente exacta. No se actualizaron retrospectivamente hashes históricos ni se repitió la revisión científica C031.

## Expedientes emitidos

Todos están en `docs/auditorias/`:

- `evidencia_independiente_s240_s352_v2_2026-09-27.json`: 100 objetos, hashes, pasajes propios, contraste de anteriores y artefactos.
- `dictamenes_independientes_propuesta_s240_s352_v2_2026-09-27.csv`: 108 filas; 89 conformidades nominales, una editorial, cuatro disposiciones conformes prospectivas, 12 NC, una disposición pendiente sin firma y C1041 fuera de alcance.
- `cobertura_independiente_44_componentes_s240_s352_v2_2026-09-27.json`: adjudicación nominal de todos los componentes y límites, con dependencias/hashes.
- `revision_independiente_disposicion_c2708_s240_s352_v2_2026-09-27.json`, `...c2709...`, `...c2469...`, `...c2475...`: contrato cerrado del consumidor, independencia, UTC, SHA de disposición excluyendo `revision_independiente`, cobertura y pasajes. No se crearon expedientes conformes para C2468/C2474.
- `pasaje_pdf_fig4_revision_s240_s352_v2_2026-09-27.json`: extracción propia de la leyenda PDF; la lectura de símbolos se respalda adicionalmente por imágenes identificadas en la evidencia.
- `no_solapamiento_F_c031_s240_v2_2026-09-27.json`: reproducción en memoria del archivo base.

Los cuatro expedientes cumplen comprobaciones de claves exactas, hashes de disposición y C soporte, fuentes nominales, cobertura de todos sus componentes/artefactos, fragmentos de hasta 25 palabras y cronología. Esas comprobaciones no son la prueba científica: lo es la lectura nominal descrita. No se ejecutó `load` contra un canon en el que las altas y artefactos futuros todavía no existen. No se aprobaron los 210 controles, el censo semántico completo ni `make verify`.
