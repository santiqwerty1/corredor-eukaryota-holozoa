# Fuentes sin texto completo

De las **30** fuentes del apéndice A se obtuvieron **24** por vía de acceso abierto. Las **6** restantes están aquí, con la razón de cada una.

Generado por `scripts/fetch_oa.py` el 2026-08-10. Para regenerarlo sin volver a descargar nada:

```bash
python3 scripts/fetch_oa.py --mailto tu@correo --solo-listado
```

> Ninguna de estas fuentes se ha retirado del corpus ni se ha marcado como dudosa: no haber podido descargar el PDF no dice nada sobre la afirmación que sostiene. Esta lista es un encargo pendiente, no un defecto del corpus.

## Sin versión de acceso abierto · 2

Ningún catálogo declara una versión abierta. Vía habitual: préstamo interbibliotecario, acceso institucional, o escribir a quien firma la correspondencia — muchos autores envían su propio PDF si se les pide.

| Clave | Año | Autores | Título | Publicación | DOI |
|---|---|---|---|---|---|
| `S09` | 2013 | Williams et al. | An archaeal origin of eukaryotes supports only two primary domains of life | Nature | [10.1038/nature12779](https://doi.org/10.1038/nature12779) |
| `S27` | 2026 | Appler et al. | Oxygen metabolism in descendants of the archaeal-eukaryotic ancestor | Nature | [10.1038/s41586-026-10128-z](https://doi.org/10.1038/s41586-026-10128-z) |

## El enlace no devolvió un PDF · 2

La respuesta fue una página web, no un artículo: el enlace lleva a la ficha del trabajo y el PDF está detrás de otro clic. Abre el DOI y busca el enlace de descarga en la propia página.

| Clave | Año | Autores | Título | Publicación | DOI |
|---|---|---|---|---|---|
| `S22` | 2015 | Spang et al. | Complex archaea that bridge the gap between prokaryotes and eukaryotes | Nature | [10.1038/nature14447](https://doi.org/10.1038/nature14447) |
| `S24` | 2021 | Liu et al. | Expanded diversity of Asgard archaea and their relationships with eukaryotes | Nature | [10.1038/s41586-021-03494-3](https://doi.org/10.1038/s41586-021-03494-3) |

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
