# Fuentes sin texto completo

De las **12** fuentes del apéndice A se obtuvieron **0** por vía de acceso abierto. Las **12** restantes están aquí, con la razón de cada una.

Generado por `scripts/fetch_oa.py` el 2026-08-10. Para regenerarlo sin volver a descargar nada:

```bash
python3 scripts/fetch_oa.py --mailto tu@correo --solo-listado
```

> Ninguna de estas fuentes se ha retirado del corpus ni se ha marcado como dudosa: no haber podido descargar el PDF no dice nada sobre la afirmación que sostiene. Esta lista es un encargo pendiente, no un defecto del corpus.

## Sin versión de acceso abierto · 1

Ningún catálogo declara una versión abierta. Vía habitual: préstamo interbibliotecario, acceso institucional, o escribir a quien firma la correspondencia — muchos autores envían su propio PDF si se les pide.

| Clave | Año | Autores | Título | Publicación | DOI |
|---|---|---|---|---|---|
| `S09` | 2013 | Williams et al. | An archaeal origin of eukaryotes supports only two primary domains of life | Nature | [10.1038/nature12779](https://doi.org/10.1038/nature12779) |

## Declarada abierta, pero sin PDF enlazado · 1

El catálogo la marca como abierta y no da la dirección del fichero. El DOI suele llevar a la versión legible.

| Clave | Año | Autores | Título | Publicación | DOI |
|---|---|---|---|---|---|
| `S06` | 1990 | Woese, Kandler y Wheelis | Towards a natural system of organisms: proposal for the domains Archaea, Bac | Proceedings of the National Academ | [10.1073/pnas.87.12.4576](https://doi.org/10.1073/pnas.87.12.4576) |

## No identificable automáticamente · 1

O no declara DOI —sólo una URL—, o ningún catálogo abierto reconoce ese DOI. Hay que ir a mano por la referencia.

| Clave | Año | Autores | Título | Publicación | DOI |
|---|---|---|---|---|---|
| `S02` | 2026 | International Commission on Stratigrap | International Chronostratigraphic Chart, version 2026/06 | International Commission on Strati | https://stratigraphy.org/chart/ |

## no intentado · 9

- `S01` Revisions to the Classification, Nomenclature, and Diversity of Eukaryotes
- `S03` EukProt: a database of genome-scale predicted proteins across the diversity of e
- `S04` The Protist Ribosomal Reference database (PR2): a catalog of unicellular eukaryo
- `S05` UniEuk: Time to Speak a Common Language in Protistology!
- `S07` Eocytes: a new ribosome structure indicates a kingdom with a close relationship 
- `S08` The archaebacterial origin of eukaryotes
- `S10` Phylogenomics provides robust support for a two-domains tree of life
- `S11` Lokiarchaea are close relatives of Euryarchaeota, not bridging the gap between p
- `S12` Asgard archaea are the closest prokaryotic relatives of eukaryotes

## Cómo conseguirlas

1. **Prueba el DOI en el navegador.** Buena parte de las bloqueadas por el editor se abren sin más: el rechazo era al cliente automático, no a ti.
2. **Préstamo interbibliotecario.** Si tienes afiliación, es la vía normal y suele tardar días.
3. **Escribe a quien firma la correspondencia.** Funciona más de lo que parece; los autores pueden compartir su manuscrito aceptado.
4. **Busca el manuscrito del autor.** Muchas revistas permiten depositarlo en un repositorio institucional aunque la versión publicada sea de pago.

Cuando consigas alguna, déjala en `fuentes_pdf/` con el mismo nombre que usa el script —`CLAVE [AÑO] Título.pdf`— y la próxima ejecución la dará por obtenida en vez de volver a intentarlo.
