# Verificación nominal de las trece fuentes nuevas — 2026-09-26

Finalización de la inspección: 2026-09-26T21:27:59Z. Revisor: agente independiente /root/verificacion_fuentes_nuevas.

La diferencia de claves entre A vivo y las 525 filas del inventario inicial es
exactamente S547–S559. Se inspeccionaron documentos locales, metadatos DOI
depositados por los editores y páginas oficiales o institucionales. Esta es
evidencia de una observación posterior, no una asignación retrospectiva de fechas.
No se cambiaron A, fuentes/, el corpus, los ledgers ni los registros cronológicos.

El CSV nominal registra 11 CONFORME y 2 NO_CONFORME. Su conformidad está limitada
a identidad bibliográfica y al tipo documental comprobable, con límites en cada
fila. No firma controles manuales ni segundas revisiones científicas.

## Discrepancias que requieren remediación

- S551: el artículo NDB está firmado por Georg Uschmann y fue publicado en
  Neue Deutsche Biographie 6 (1964), p. 605. A usa la institución como autor y
  el año de consulta como año bibliográfico. La consulta histórica no se altera.
  La página contiene también una biografía ADB de Victor Carus (1879), distinta.
- S559: el editor clasifica el documento como Perspective y el JATS como
  review-article; A lo clasifica como investigación primaria. Su identidad
  nominal, año, DOI y paginación sí coinciden. La página muestra corrigenda
  fechados en 2018; no se afirma haber agotado la revisión editorial.

## Límites de versión y acceso

- S548: A sí identifica la publicación PNAS 2026. El PDF local preexistente
  es un preprint bioRxiv de diciembre de 2025. Se obtuvo el JATS publicado en
  /tmp; su identidad no transfiere automáticamente resultados entre versiones.
  El cotejo científico se encomienda por separado y no se cierra aquí.
- S549: el PDF local es arXiv v1 de mayo de 2026, anterior a la publicación
  APS de junio. Se confirmó la identidad publicada en APS y Crossref, no la
  equivalencia integral entre versiones.
- S557: se obtuvo el PDF editorial desde el sitio institucional de un coautor,
  solo en /tmp. Su título usa el singular concentration, como A.
- S558: se confirmó identidad por Crossref y ficha institucional; no se obtuvo
  texto completo. Article/journal-article no prueba por sí solo un tipo más fino.

## Evidencia y reutilización

`verificacion_fuentes_nuevas_2026-09-26.csv` contiene las 13 huellas de A y los
dictámenes. `evidencia_identidad_fuentes_nuevas_2026-09-26.json` conserva los
campos bibliográficos observados, rutas, localizadores y SHA-256 de los artefactos
inspeccionados. Las respuestas de red originales se conservan temporalmente en
`/tmp/verificacion-fuentes-nuevas-2026-09-26/`; los campos seleccionados sí quedan
versionables en el JSON. No se copiaron artículos completos a la auditoría.

Una fila NO_CONFORME documenta una verificación ejecutada, pero no aprueba su
objeto. Si A se corrige, su huella cambia y se necesita reinspección explícita;
esta evidencia anterior no debe reescribirse para simular una firma posterior.
La integración en registros cronológicos queda a cargo del ensamblado coordinado.
