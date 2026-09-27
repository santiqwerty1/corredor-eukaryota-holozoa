# Evidencia primaria propuesta: S560, Wang y Wu (2014)

Revisor independiente: `/root/revision_residuales/candidatos_editoriales`.
Observación nominal del artefacto: 2026-09-26T22:59:03Z.
Estado: propuesta de alta reservada por raíz; no se certifica integración
en fuentes, fechas canónicas ni censo científico.

## Identidad y acceso

- Autores: Zhang Wang y Martin Wu. Frank Voncken figura como editor, no autor.
- Título: *Phylogenomic Reconstruction Indicates Mitochondrial Ancestor Was an Energy Parasite*.
- PLOS ONE 9(10):e110685; publicación electrónica 2014-10-15.
- DOI: https://doi.org/10.1371/journal.pone.0110685 .
- PMID 25333787; PMCID PMC4198247; versión JATS PMC4198247.1.
- Editorial: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0110685 .
- XML abierto recuperado: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4198247/fullTextXML .
- Artefacto real: `/tmp/Wang-Wu-2014-PMC4198247.xml`, 129891 bytes.
- SHA-256: `0cc3ae6e651cb6841f280570ee4915ba6f2a7528e69f7180004e6612c4015901`.
- Licencia declarada en JATS: CC BY 4.0.

La identidad se cotejó entre JATS, registro PubMed y página editorial. No se
encontró alta canónica previa por título, DOI o pareja de autores en la
inspección de A; raíz confirmó la reserva S560. Este documento no añade S.

## Resultado y localizadores exactos

`body/sec[@id='s2']/sec[@id='s2a']`, primer párrafo de Results and Discussion,
identifica computacionalmente 4459 genes nucleares de procedencia mitocondrial
agrupados en 394 familias, partiendo de 427186 genes de 30 genomas eucariotas.
Son dos unidades diferentes: genes del muestreo y familias reconstruidas.

`body/sec[@id='s3']/sec[@id='s3a']`, Materials and Methods, explica el filtro:
BLASTP inicial contra 2742 genomas; entre los cinco mejores hits debe figurar
una secuencia alfaproteobacteriana o mitocondrial, E≤1e-4; recuperación
posterior de homólogos E≤1e-15; agrupación MCL y árboles FastTree2; partición
con al menos dos eucariotas y dos alfaproteobacterias. Parálogos se separan
y tratan como nuevas familias. No es un conteo de eventos de transferencia.

`table-wrap[@id='pone-0110685-t001']` informa 1613 genomas para la comparación
filogenómica, incluidos 171 alfaproteobacterianos, 67 Rickettsiales y 30
eucariotas. Este total no sustituye los 2742 de la búsqueda inicial.

`s2a`, párrafos segundo y tercero: controles de los autores 278/427186
secuencias (0,07%) con Deinococcus/Thermus y recuperación 46/50 genes de
Reclinomonas (8% no recuperado). Son diagnósticos de ese procedimiento,
no garantía independiente de ausencia de errores ni extrapolación universal.

## Propuesta de corrección y retirada de BN-132

La propuesta de raíz de distinguir C-1163 (4459 genes) y otra C separada
(394 familias) evita mezclar unidades. Deben conservar muestra, método y
atribución a los autores; no traducir 4459 en eventos ancestrales ni 394 en
inventario completo de LECA. Tampoco igualar origen mitocondrial con destino
actual de cada proteína.

Recomiendo retirar prospectivamente BN-132 como hueco activo cuando se
incorporen esos resultados y sus límites, conservando su historia y logs.
El encargo R-0209 pide «cuántos genes», no un único total ancestral exacto.
No se debe fabricar un residual con ese requisito añadido. Que este trabajo
no establezca un total universal es un límite del resultado positivo, no una
declaración de inexistencia en la literatura.

La retirada no constituye aprobación automática de R-0209 entero: la
dirección y TOM/TIM conservan su obligación de soporte independiente. El
cotejo del parche, las huellas de las nuevas filas y los derivados queda
pendiente de la implementación por raíz.
