# Revisión independiente de S549 publicado y límites de BN-083

Finalización: 2026-09-26T21:39:46Z. Revisor: agente independiente /root/verificacion_fuentes_nuevas.

## Fuente realmente inspeccionada

Se cotejaron la página pública de APS y la versión publicada de
Physical Review Fluids 11, 063102, de 18-06-2026, DOI
https://doi.org/10.1103/vzxt-rpf8. No se usó una supuesta equivalencia con el
PDF arXiv preexistente.

- Resumen editorial: https://journals.aps.org/prfluids/abstract/10.1103/vzxt-rpf8
  (Abstract). La lectura web fue posible; curl a esa página devolvió 403.
- PDF publicado recuperado del endpoint oficial
  https://harvest.aps.org/v2/journals/articles/10.1103/vzxt-rpf8/fulltext
  a `/tmp/verificacion-fuentes-nuevas-2026-09-26/S549-aps-published.pdf`; 1.953.995 bytes, 12 páginas;
  SHA-256 `2bfd54bd40f0a39f967bfdd7ad69bfa94c8109286e031f82eb8ab7125aed731b`.
- Texto extraído mediante pdftotext -layout:
  `/tmp/verificacion-fuentes-nuevas-2026-09-26/S549-aps-published.txt`;
  SHA-256 `48e1f5f9fb43329e063893dd2e9cfa1a947159eaf7d71080b8d4b87dc8ce2708`.
- Se leyeron resumen, §§I–V, Appendix y sus tablas I–II. Los localizadores
  impresos son 063102-1 a 063102-11; las referencias concluyen en 063102-12.
  La inspección no recalcula las ecuaciones ni valida los resultados del modelo.
- Huella A S549 inspeccionada: `097ed000f73c2b1da41fd1d90ddfcfeb5dd625525d89c3b5a5c811e94d54f540`.

## C-1612

CONFORME. El resumen publicado declara máximos de flujo efectivo y disipación
en crestas del espacio de radio/separación microvillar; identifica un modelo
reducido que omite longitud finita. Basta para la redacción actual, que no
publica una cifra ni convierte el resultado en medida celular. §III y figura 3
(063102-7) confirman el significado: potencia efectiva por área construida
como caída de presión por velocidad y flujo construido con superficie por
velocidad. La prosa de §12.2 que reproduce C-1612 conserva ese alcance.

## C-1613

CONFORME como distinción entre magnitud modelada y presupuesto metabólico
celular medido. El resumen basta para identificar el modelo hidrodinámico,
pero no bastaría, por su silencio, para negar toda otra medición en el artículo.
Por eso se inspeccionaron también §II A–B, §III, §IV y Appendix/Table II:
las entradas son geometría y cinemática extraídas de literatura y las salidas
son físicas del flujo. No se publica un presupuesto de ATP, consumo de O₂,
calorimetría o crecimiento por roseta ni comparación metabólica de las tres
rutas. La potencia disipativa puede tener significado térmico físico; esto no
la convierte en una medición calorimétrica de gasto celular. La prosa no afirma
que el flujo carezca de costo físico, sino que no es el presupuesto pedido.

## C-1495 y el ámbito documental de BN-083

CONFORME en correspondencia semántica y documental acotada, no en certificación
de una nueva búsqueda. C-1495 dice no se localizó, no que ninguna publicación
pueda existir. BN-083 lleva NO LOCALIZADO EN ESTA SESIÓN y §15.4/C-1935 explica
que esa etiqueta no significa inexistencia universal. La Q histórica Q-0052
(2026-08-08) documenta cribado de metadatos/título-resumen en OpenAlex, Crossref
y Europe PMC, 72 registros y dos candidatos sin pasaje inspeccionado, sin
resolución positiva aceptada. Esa limitación queda expresa y no se transforma
en una afirmación de ausencia global. La lectura publicada de S549 confirma
que ese candidato no aporta el presupuesto metabólico por roseta.

El resumen APS solo no demostraría el resultado de la búsqueda BN-083. La
conformidad de C-1495 aquí es su ajuste al resultado de búsqueda documentado,
apoyado por la verificación independiente de por qué S549 no lo resuelve;
no acredita la ejecución original ni elimina los candidatos pendientes.

## BN-083: límite de esta revisión

La fila viva tiene huella `bc5344939f2920e9feabf408f6dd43d22f229e9e38a50d14b76d3d09bea175ce`. Su blanco cubre rosetas,
matriz extracelular, láminas, celularización y comparación clonal/agregativa/
cenocítica; ningún párrafo de S549 se usa para declarar resueltos todos esos
blancos. Su motivo sobre la insuficiencia de S549 es CONFORME contra el PDF.

La fila viva contiene 13 términos frente a los 11 del registro congelado;
los dos añadidos buscan collar/disipación/Iqbal. No hay una fila BN-083 en
data/auditoria/fechas_ejecuciones_bn.csv en esta inspección. No es posible
certificar con lo inspeccionado cuándo se ejecutaron esas dos consultas:
NO_VERIFICABLE para ese subobjeto de cronología/ejecución, no una declaración
de que la búsqueda jamás ocurrió. No se ejecutó ni fechó una búsqueda nueva
de toda BN-083. El resultado histórico y la semántica cauta se conservan.

## Prosa y trazabilidad

Se comprobaron los párrafos de §12.2 correspondientes a C-1495, C-1612 y
C-1613 y la oración de §12.12 que distingue el modelo S549 de la unidad
metabólica. La oración adyacente de C-1603 sigue refiriendo al blanco maestro
documentado y no se convierte en una nueva búsqueda aprobada. No se revisan
aquí todos los presupuestos de matriz, láminas o celularización por especie.
El Apéndice G conserva la misma distinción de clases de magnitud.

## Límites e independencia

No se editó corpus, fuentes/, A, BN ni registros de revisión. Los dos archivos
descargados/extraídos permanecen en /tmp para integración coordinada. Las filas
del CSV registran huellas del corpus examinado, sin actualizar firmas viejas
ni convertir esta revisión en el cierre global de controles o búsquedas.
