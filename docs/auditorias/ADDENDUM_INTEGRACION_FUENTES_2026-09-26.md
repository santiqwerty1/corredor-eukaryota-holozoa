# Addendum independiente: integración de ocho artefactos

Inspección finalizada: 2026-09-26T21:51:56Z; revisor /root/verificacion_fuentes_nuevas.

CONFORME para las ocho copias y las tres filas de acceso S548/S549/S557.
Se comparó cada copia byte a byte con su origen temporal y su SHA declarado;
los tres suplementos S548 coinciden además con miembros del ZIP oficial y con
los nombres de media enlazados por el JATS de PNAS. Los dos corrigenda S559
fueron consultados de nuevo en Europe PMC: respuestas idénticas; sus PMCID/DOI
y enlace al artículo corregido PMC6436528 confirman la asociación documental.

El inventario actual contiene 442 archivos y tiene SHA-256
`69704030a52076437e131fde0a1b886605b3ed8efc6a8fcf272660df3e4503cd`. Al retirar del cálculo únicamente las ocho altas
nominales vuelve a tener 434 archivos y huella
`a08bc1a1584b2a31a0da0d84efd1de350abf318b9a2cfa7e0a94e0f34cb0f043`, idéntica a la observada antes de la integración. Esto
comprueba que el conjunto anterior no fue sobrescrito ni reducido.

Los PDF preprint de S548 y S549 siguen presentes con sus SHA completos anteriores;
sus prefijos coinciden con exports/acceso_fuentes.csv en HEAD. Git no versiona
fuentes/, por lo que no se usa HEAD como una prueba inexistente de bytes PDF.
En el export actual, los DOI, nombres de fichero, URLs oficiales/institucional,
fechas de recuperación de hoy y SHA completos de las tres altas concuerdan.
No se atribuye a la integración la fecha original de descarga de los preprints.
Los recuentos de usos y las categorías generales de acceso presentes en el
export no se recalculan ni se adjudican como parte de este cotejo de identidad.

El JSON acompañante `evidencia_revision_integracion_fuentes_2026-09-26.json` conserva los ocho objetos
nominales, sus localizadores, las filas export actual/HEAD y los hashes.
Su SHA-256 es `744d667dfabfb0053f73e0075eecafd3c36a0dbe93c17cfc70687b4bf6bcd739`.
Esta revisión no amplía dictámenes científicos, no retoca consultas originales
ni registra fechas en los CSV cronológicos. No modifiqué fuentes/ ni corpus.
