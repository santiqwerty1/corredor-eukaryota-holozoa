# Fuentes sin texto completo

De las **14** fuentes del apéndice A se obtuvieron **5** por vía de acceso abierto. Las **9** restantes están aquí, con la razón de cada una.

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

## El servidor del editor rechazó la descarga · 3

El catálogo las da por abiertas, pero el servidor responde con un error (casi siempre 403) a un cliente automático. **Suelen abrirse sin problema desde un navegador**: prueba el enlace del DOI directamente.

| Clave | Año | Autores | Título | Publicación | DOI |
|---|---|---|---|---|---|
| `S01` | 2019 | Adl, S. M. et al. | Revisions to the Classification, Nomenclature, and Diversity of Eukaryotes | Journal of Eukaryotic Microbiology | [10.1111/jeu.12691](https://doi.org/10.1111/jeu.12691) |
| `S04` | 2013 | Guillou, L. et al. | The Protist Ribosomal Reference database (PR2): a catalog of unicellular euk | Nucleic Acids Research 41:D597–D60 | [10.1093/nar/gks1160](https://doi.org/10.1093/nar/gks1160) |
| `S05` | 2017 | Berney, C. et al. | UniEuk: Time to Speak a Common Language in Protistology! | Journal of Eukaryotic Microbiology | [10.1111/jeu.12414](https://doi.org/10.1111/jeu.12414) |

## El enlace no devolvió un PDF · 3

La respuesta fue una página web, no un artículo: el enlace lleva a la ficha del trabajo y el PDF está detrás de otro clic. Abre el DOI y busca el enlace de descarga en la propia página.

| Clave | Año | Autores | Título | Publicación | DOI |
|---|---|---|---|---|---|
| `S07` | 1984 | Lake et al. | Eocytes: a new ribosome structure indicates a kingdom with a close relations | Proceedings of the National Academ | [10.1073/pnas.81.12.3786](https://doi.org/10.1073/pnas.81.12.3786) |
| `S08` | 2008 | Cox et al. | The archaebacterial origin of eukaryotes | Proceedings of the National Academ | [10.1073/pnas.0810647105](https://doi.org/10.1073/pnas.0810647105) |
| `S10` | 2020 | Williams et al. | Phylogenomics provides robust support for a two-domains tree of life | Nature Ecology & Evolution | [10.1038/s41559-019-1040-x](https://doi.org/10.1038/s41559-019-1040-x) |

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

## Cómo conseguirlas

1. **Prueba el DOI en el navegador.** Buena parte de las bloqueadas por el editor se abren sin más: el rechazo era al cliente automático, no a ti.
2. **Préstamo interbibliotecario.** Si tienes afiliación, es la vía normal y suele tardar días.
3. **Escribe a quien firma la correspondencia.** Funciona más de lo que parece; los autores pueden compartir su manuscrito aceptado.
4. **Busca el manuscrito del autor.** Muchas revistas permiten depositarlo en un repositorio institucional aunque la versión publicada sea de pago.

Cuando consigas alguna, déjala en `fuentes_pdf/` con el mismo nombre que usa el script —`CLAVE [AÑO] Título.pdf`— y la próxima ejecución la dará por obtenida en vez de volver a intentarlo.
