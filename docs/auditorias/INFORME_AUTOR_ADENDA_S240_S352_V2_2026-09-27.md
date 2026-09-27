# Adenda autoral a S240/S352 v2: deltas nominales, sin integración

Autor: `/root/inspeccion_relojes`. Rama: `codex/cierre-plan-pendiente`. Fijación: 2026-09-27T03:32:23Z. No es dictamen independiente ni cierre científico.

La propuesta nueva `PROPUESTA_AUTOR_ADENDA_S240_S352_V2_2026-09-27.json` tiene SHA256 `cf00495ba91d037d07c2f8b8ac1b950d58d0c4441b28e05e73a4336333894c58`. Su evidencia `EVIDENCIA_AUTOR_ADENDA_S240_S352_V2_2026-09-27.json` tiene SHA256 `81d3c8f760eb1e2a97663ea93f06c47cfadb9100511f6dea2bb6529992db35a2`. La v2 base `96d36be9adeed056a5c5f6da54321101b2dc25e7ae1bc28cb9258dae0b3e8bfa` permanece intacta, al igual que v1 y sus rechazos.

Se leyó completo el informe independiente v2 y el CSV nominal. Esta adenda propone tres sustituciones C, dieciséis altas B y dos sustituciones de objetos de prosa prospectiva. No toca archivos canónicos, fuentes, matrices ni firmas.

- C2876/C2877: sólo cambia `Motivo`, de Frizzled a ITR-like/OA1-like, respectivamente. Afirmación, fuente, organismos y modalidad no cambian. Nuevas huellas: `c65770c1e3bad199fd1fd17238e3736661ccf3abbbbf8672fa6b0b16054fe595` y `4263ccb0148c80c22ff7128b84c7a3c337143985a459c5010dfbc877d005c066`.
- C2852: se retira el enlace de contraevidencia a un blanco ampliado. La glosa nueva contrasta únicamente lo que documenta C2849, con C2847–48 como contexto: dominios en proteínas distintas no son una identificación documental de ligando completo. No afirma ausencia, existencia ni función del ligando y no refuta C1581. Se adjuntan íntegros y con huellas los tres objetos documentales. Huella nueva: `a151b6cd6bec10aa4f1965abb83d0a6933c7bec628cdc873a6099b7223fb4e5d`. El predicado nuevo queda definido de inmediato en Motivo y prospectivamente en §0; se añade su objeto documental a B. Su condición de glosa no lo exime de revisión.
- B: se proponen quince métodos realmente nombrados: Illumina HiSeq, SGA, Velvet, SSPACE, Gapfiller, Image, ICORN, REAPR, HMMER, RAxML, PhyloBayes, BLASTP, FastTree, crio-SEM y LG+G+F. Las búsquedas con límites de palabra evitan falsos positivos como Asgard/SGA. FastTree se ancla a C2824 y crio-SEM a C1040. Gapfiller/Image/ICORN/REAPR tienen mención literal en F→C2839; HMMER, en F→C2864 antes de su mención en C2865. Estos cinco enlaces se declaran indirectos, no apariciones literales inventadas en C. CAT y TEM ya existen y no se duplican. Es un lote nominal, no un censo global de entidades.

El expediente C2474 conserva celda, componentes, cifras, fuentes y límites: cambian sólo huellas de C2876/77, evidencia autoral y fecha nueva. Su revisión sigue `null`; hash del objeto completo de disposición `460070882ee339ef42a75fae24bbdbfe499acdf108c4bdfa39ff55772a7b1c5e`. Debe reinspeccionarse, no heredar la revisión v2. Las otras cuatro disposiciones prospectivamente conformes conservan exactamente su evidencia y objetos v2; esta adenda no vuelve a firmarlas.

## Pendiente preservado

C1581 permanece byte por byte intacta y NO_CONFORME. C2851 tampoco se modifica y conserva la dependencia no resuelta. La prosa Hedgehog elimina la contraevidencia errónea C2852 y usa «previa», no una Vigencia histórica ficticia, pero el bloque y su roll-up siguen pendientes por C1581/C2851. La anotación autoral de conservación retira C2852 de su lista de contraevidencias sin modificar la fila C1581. La representación definitiva requiere la decisión que coordina raíz; no se integra a partir de esta adenda.

## Comprobaciones autorales

Se comprobaron por script de sólo lectura los hashes anterior/posterior de las tres C, las dieciséis B y ambas prosas; igualdad exacta de los anteriores con v2; diferencia exclusivamente en Motivo para C2876/77; resolución de la evidencia; igualdad del contenido y componentes de C2474; y ausencia de firma independiente. Son comprobaciones mecánicas, no sustituyen la lectura de quien revise el delta. F no se altera: su cambio concurrente de localizadores C031 queda fuera del alcance. Tampoco se modifica el inventario de fuentes ni se adjudican los seis genes mitocondriales de C1041.
