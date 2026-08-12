# Encargo al auditor · verificación contra el texto completo

Hasta ahora la auditoría ha trabajado con lo que el corpus dice de sí mismo.
Ahora hay **texto completo** de buena parte de la bibliografía, así que se puede
verificar contra la fuente en vez de contra el resumen.

---

## Prompt

> El repositorio incluye ahora los PDF de las fuentes en acceso abierto,
> descargados legalmente de los catálogos abiertos (OpenAlex, Unpaywall,
> Europe PMC, arXiv, OpenAIRE). Están en `fuentes/`, fuera del control de
> versiones, con el nombre `CLAVE [AÑO] Título.pdf` —por ejemplo
> `S056 [2024] Reconstructing the last common ancestor.pdf`—, de modo que cada
> fichero se rastrea hasta su fila del apéndice A por la clave.
>
> **Qué hay disponible y qué no**, fuente a fuente:
>
> - `exports/acceso_fuentes.csv` — una fila por fuente: si hay versión abierta,
>   por qué vía llegó, el fichero descargado y, si no se obtuvo, la razón.
> - `docs/FUENTES-SIN-ACCESO.md` — las que faltan, agrupadas por causa.
>
> **Puedes descargar más.** Si necesitas una fuente que no está:
>
> ```bash
> python3 scripts/fetch_oa.py --mailto <correo>
> ```
>
> Reutiliza la resolución cacheada, salta los PDF ya bajados y sólo reintenta lo
> que falta, así que relanzarlo es barato. Con `--core-key <clave>` añade CORE
> (la clave es gratuita en core.ac.uk/services/api). `--solo-listado` regenera el
> documento de faltantes sin tocar la red.
>
> **Lo que este material permite hacer y antes no:**
>
> 1. **Verificar el localizador de cada afirmación.** La columna `Fuente` dice
>    cosas como «S56 líneas 318–321» o «S38 resumen y fig. 5». Con el PDF delante
>    se puede comprobar que el pasaje citado sostiene lo que la afirmación dice, y
>    que lo dice con la fuerza declarada. Prioriza las afirmaciones marcadas
>    `fuerza alta`: son las que más daño hacen si el localizador no sostiene.
> 2. **Cerrar el censo de requisitos con verificación nominal.** Los controles que
>    esperaban lectura manual ya la tienen.
> 3. **Revisar las contraevidencias.** Un artículo suele discutir los resultados
>    que lo contradicen; esas discusiones son la materia prima de las
>    contraevidencias que faltan por registrar.
> 4. **Comprobar fechas y magnitudes de los apéndices D y F** contra el intervalo
>    tal como lo publica la fuente, con su incertidumbre. El corpus exige no
>    promediar: el ancho del intervalo es el dato.
> 5. **Auditar las cuatro fuentes de solidez baja** —3 preprints, 1 divulgación—
>    que el apéndice A clasifica por tipo, según el modo auditoría de §18.2.
>
> **Reglas que no cambian.** No se inventa nada: si el PDF no sostiene la
> afirmación, eso es un hallazgo que se registra, no una afirmación que se
> corrige en silencio. Si una fuente no está disponible, la afirmación **no se
> marca como dudosa por eso**: no haber podido descargar el PDF no dice nada
> sobre lo que la afirmación sostiene. Y el corpus es inmutable para el visor:
> las correcciones entran por el flujo de la auditoría, no editando CSV a mano.
>
> **Dos discrepancias detectadas que conviene resolver de paso:**
>
> - El apéndice H declara **1 196** afirmaciones dependientes de una sola fuente;
>   contando sobre `exports/afirmaciones.csv` con la regla de claves `S\d{2,3}`
>   salen **1 195**. Una fila de diferencia, sin identificar.
> - **10 de las 523 fuentes del apéndice A no las cita ninguna afirmación.**
>   ¿Sobran del apéndice, o falta citarlas?

---

## Estado de la descarga

Tras tres pasadas sobre las 523 fuentes del apéndice A:

| | |
|---|---|
| **Con texto completo o recurso** | **286 (54 %)** |
| PDF | 232 |
| XML JATS (texto completo) | 187 |
| Accesos directos a recursos web | 7 |

**No todo es PDF, y el XML suele ser mejor.** Está estructurado, se busca sin
capa de OCR y permite comprobar un localizador sin abrir nada. Muchas fuentes
tienen ambos: el PDF conserva páginas y figuras —que los localizadores citan—, y
el XML permite buscar dentro del texto.

Cada fichero obtenido lleva su huella `sha256` y su fecha en el informe, y un
veredicto de identidad: **203 comprobadas, 83 sin comprobar, ninguna
discrepancia**. «Sin comprobar» significa que no había metadatos legibles, no
que haya sospecha.

### Lo que falta, por lo que está en juego

Las 237 fuentes sin texto sostienen **1 120 citas, de las cuales 409 no tienen
ninguna otra fuente**. El listado va ordenado por ese impacto, no por clave.

| Motivo | Fuentes |
|---|---|
| sin versión abierta declarada | 121 |
| el servidor rechazó al cliente automático (403) | 80 |
| la respuesta no era un fichero, sino la ficha web | 34 |
| sin DOI o no reconocida por ningún catálogo | 25 |
| declarada abierta sin fichero enlazado | 2 |

El grupo de **403 es fruta madura**: son fuentes que los catálogos dan por
abiertas y cuyo servidor rechaza a los clientes automáticos. **Suelen abrirse
pinchando el DOI en un navegador.** El script no suplanta a un navegador para
evitarlo, así que ese rescate es manual y barato. Las tres que más pesan —S129,
S137 y S84— suman 81 citas entre ellas.

Cuando consigas una fuente por tu cuenta, déjala en `fuentes/` con el mismo
patrón de nombre y la siguiente ejecución la dará por obtenida.

### Los pasajes ya extraídos

`exports/pasajes.csv` recorta, de cada localizador, el fragmento que la propia
afirmación señala: **558 de 2 820 localizadores ya tienen su pasaje delante**, y
la cifra sube conforme llegan más textos. `docs/revision-pasajes.html` los
enfrenta a la afirmación para revisarlos en tandas, y el visor los muestra en la
ficha de cada afirmación y en su propia vista.

El script recorta y presenta; **decidir si el pasaje sostiene la afirmación
sigue siendo tuyo** (§27.12). Un pasaje ausente no es un defecto de la
afirmación: es un localizador que no se pudo resolver, y el informe dice por qué.
