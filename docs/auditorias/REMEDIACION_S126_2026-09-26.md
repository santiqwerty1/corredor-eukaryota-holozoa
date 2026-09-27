# Remediación acotada de los intervalos de S126

## Estado y alcance

Este documento registra una corrección y su procedencia; no constituye una
aprobación independiente del corpus ni sustituye los censos pendientes.
Se conservan los identificadores de las 18 afirmaciones corregidas. Las filas
C-2814–C-2816 documentan la clasificación de Nutomonas, el límite de la búsqueda
de una edad de corona de Breviatea y la composición del muestreo temporal.
C-2817 registra el resultado acotado de BN-025 sobre la corona de Apusomonadida;
se añadió al detectar que esa parte de la celda de edad carecía de una C propia.

## Artefacto recuperado

- Fuente: S126, Liu et al. (2024), *A taxon-rich and genome-scale phylogeny of
  Opisthokonta*.
- Suplemento editorial S1 Data, enlazado por el artículo y por el XML JATS:
  <https://journals.plos.org/plosbiology/article/file?type=supplementary&id=10.1371/journal.pbio.3002794.s020>.
- Recuperación: 2026-09-26. Archivo local:
  `fuentes/S126 [2024] A taxon-rich and genome-scale phylogeny of Opisthokonta - S1 Data.pdf`.
- Tamaño: 3228855 bytes; 21 páginas.
- SHA-256: `e01f0f62c208834b8b67be8fe43692397b39607cbd25d0229beaf82b4d0b5889`.

Los archivos de `fuentes/` no se versionan, conforme a `.gitignore`. El enlace,
el tamaño y la huella permiten recuperar y verificar este suplemento sin
depender de un archivo temporal de la sesión.

## Disposición de la evidencia

1. Los intervalos se transcriben de los rótulos numéricos de los árboles de
   S1 Data, p. 21. Se conservan los decimales impresos y la unidad de 100
   millones de años indicada en la leyenda de Fig. 3. No se recalcula desde
   Table S7, no se convierte a Ma ni se redondea.
2. C-541 utiliza directamente la fila Obazoa de Table 2: los extremos publicados
   son 1,077.05 y 1,334.8, en millones de años antes del presente. Se conserva
   la denominación de los autores, junto a la advertencia de composición.
3. Las leyendas de p. 5 identifican los árboles temporales como 73/74 y sus
   restricciones de raíz como 1.5/1.9 mil millones de años. Los paneles de
   p. 21 están rotulados 72/73. Los localizadores dicen izquierdo/derecho y
   no ocultan esta discrepancia editorial.
4. El nodo Pygsuia biforma–Nutomonas longa no se presenta como corona de
   Breviatea. S01, Table 2, entrada Ancyromonadida, incluye Nutomonas; el propio
   S126 S1 Data, p. 6, lo rotula Ancyromonadida. BN-557 conserva el resultado
   negativo limitado a los artefactos inspeccionados, no a toda la literatura.
5. C-525/C-526 describen la raíz del muestreo de S126, que incluye Nutomonas;
   no se usan como una fecha de corona de Amorphea. La estimación de S548
   permanece separada en la tabla de Amorphea.
6. No se utiliza el recorrido postorder de los árboles de S545 como una
   numeración nodal publicada. Las cifras anteriores convertidas o asociadas
   mediante esa reconstrucción quedan sustituidas por las transcripciones
   localizadas; no se presentan como datos literales del suplemento.

## Archivos complementarios de S545

Los archivos siguientes ya estaban disponibles localmente. El 2026-09-26 se
contrastaron sus tamaños y MD5 con los metadatos públicos de la versión 1:
<https://api.figshare.com/v2/articles/23301824/versions/1>.
Esta comprobación acredita identidad de archivo, no apoyo semántico.

| Archivo del depósito | Bytes | MD5 publicado y comprobado | SHA-256 local |
|---|---:|---|---|
| Phylogenetic_Analysis.tar.gz | 86768013 | 0b80e73e37a377fa682109d901c57ca2 | e016a6f84bd83f481c1c2d6964669970eed719d8b927be7e60efcfc537d43145 |
| scripts.tar.gz | 24864 | e0cdc6fac7ccb6e7a24ed39d97e05094 | bb54e7e2872f11160f8f2b2a8db64b2e06824b2063d35bb0cc1bd31e4f8e170e |

Las URL de descarga verificadas son
<https://ndownloader.figshare.com/files/41076344> y
<https://ndownloader.figshare.com/files/48306592>, respectivamente.
No se conoce la fecha original de descarga y no se inventa en el inventario.

## Revisión independiente del lote

El agente revisor `/root/inspeccion_relojes` no ha editado las afirmaciones.
Sus registros independientes conservan el orden de hallazgo y reinspección:

- `revision_lote_s126_2026-09-26.csv`: cotejo de las 18 C corregidas y las
  tres C añadidas inicialmente; también registra dos hallazgos derivados.
- `cierre_derivados_lote_s126_2026-09-26.csv`: reinspección de esos dos
  hallazgos, ya corregidos, y del formato de F para C-541.
- `addendum_c2817_lote_s126_2026-09-26.csv`: cotejo de la nueva C-2817
  contra BN-025 y el suplemento inspeccionado.
- `revision_mapeo_lote_s126_2026-09-26.csv`: adjudicación del vínculo a C
  de las 18 celdas de edad/método alteradas en nueve tablas. El cotejo de
  Amorphea frente a C-787/C-788/C-789/C-791 no se presenta como una nueva
  revisión científica primaria de S548.

Estos registros contienen huellas de las filas, celdas y artefactos examinados.
Cierran exclusivamente sus hallazgos nominales; no cierran controles globales,
el censo semántico integral ni la segunda revisión completa del corpus.
