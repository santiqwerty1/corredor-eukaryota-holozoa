# Reinspección nominal de siete BN: fuentes e índices

Finalizada: 2026-09-26T22:16:46Z. Revisor: /root/verificacion_fuentes_nuevas.

Se ejecutaron realmente los términos vivos de BN-114, BN-115, BN-118,
BN-120, BN-121, BN-130 y BN-131. Todas las fechas son REINSPECCION del 26-09,
no consulta original del 13-08. No se modificó el corpus ni el registro temporal.
Las cinco consultas internas usaron argv revisados manualmente, sin evaluar
comandos del CSV. El inventario de 442 archivos permanece `69704030a52076437e131fde0a1b886605b3ed8efc6a8fcf272660df3e4503cd`.

## Resultado y límites

- BN-114/115/118: búsquedas internas completas en los ámbitos declarados.
  Se conservan 73; 199+3; 177+68 líneas respectivamente. Se cotejaron los
  contextos nominales, no una bibliografía externa exhaustiva. En particular,
  los campos de asociación de H22 no se rellenan con términos generales sobre
  organismos o maquinaria molecular; table-40 conserva sus 26 filas y huecos.
- BN-120: hallazgo que impide reutilizar sin cambios el resultado como vigente.
  [Ensembl oficial](https://protists.ensembl.org/Sphaeroforma_arctica_jp610_gca_001186125/Info/Annotation/)
  publica 18.213 genes codificantes para GCA_001186125.1 (121.631.465 bp,
  database 116.1). No se mezcla con otras anotaciones, no se calcula densidad de
  intrones y no se refuta retroactivamente la búsqueda histórica. El requisito
  conjunto genes+intrones sigue sin quedar resuelto en esta observación.
- BN-121: términos completos ejecutados, pero revisión de candidatos PARCIAL.
  Se distinguen crecimiento/replicación, expresión, difusión y medidas para
  verificar respiración de un coste directo de mantenimiento del fenotipo.
  No se certifica toda la fila ni la cláusula sobre ningún resultado.
  Quedan candidatos/SI no inspeccionados íntegramente y errores de acceso
  explícitos. El PDF local S433 es bioRxiv 2021, no la publicación Nature 2023;
  se abrió PMC10425966, que se identifica como manuscrito de autor ligado a
  la publicación final, sin afirmar identidad de bytes con la versión editorial.
- BN-130/131: los pasajes nominales S112 y S133 son compatibles con un hueco
  acotado, no con inexistencia universal. [El estudio citosquelético de 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5043310/)
  sí propone una candidata potencial para Amoebozoa y requiere más muestreo;
  queda registrada, no descartada por no ser todavía diagnóstico universal.

Los lotes web devuelven 21, 28, 40 y 23 entradas respectivamente, con duplicados
y resultados secundarios/ajenos. BN-121 tuvo dos repeticiones individuales
adicionales (23 y 22 entradas); no se suman como artículos únicos. Se conservan
títulos/URL de todos los resultados recibidos. El buscador combina los lotes:
no se inventan contadores por consulta individual donde no los proporciona.
Los secundarios no sustentan los dictámenes científicos.

## Evidencia durable

- docs/auditorias/reinspeccion_bn_fuentes_2026-09-26.csv: SHA-256 `52c9cff24e1361d1aab1cca7fa08df22ce81a64a331ba37239dbed89b9594fdb`.
- docs/auditorias/evidencia_reinspeccion_bn_fuentes_2026-09-26.json: SHA-256 `acaaead2d678a1445797785edb95523818193a0c98c78cb70192ee84a950b97b`.
- docs/auditorias/evidencia_ejecuciones_internas_bn_fuentes_2026-09-26.json: argv, fechas, universo de archivos y SHA, salida/resumen.
- docs/auditorias/evidencia_ejecuciones_web_bn_fuentes_2026-09-26.json: términos, fechas y resultados nominales.

Las copias nuevas de páginas/JATS permanecen solo en /tmp. Los pasajes locales
mantienen sus rutas y SHA; no se ha cambiado fuentes/ ni el inventario.
Ejecución conforme no significa dictamen científico integral ni habilita a
cerrar automáticamente estas filas. BN-120 y BN-121 llevan límites nominales
que no pueden eliminarse al trasladar fechas o evidencia a otro registro.
