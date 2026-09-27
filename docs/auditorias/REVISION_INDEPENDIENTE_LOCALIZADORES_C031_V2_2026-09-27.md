# Revisión independiente: tres localizadores de C-031, F y table-01

Dictamen: **CONFORME exclusivamente para el delta v2 de los tres campos identificados**. No es conformidad integral de C-031, de sus propiedades F ni de las otras filas de la tabla.

Revisor: /root/inspeccion_relojes, distinto del autor /root y sin participación en la corrección propuesta. Cotejo nominal: 2026-09-27T03:08:16Z. No se modificaron propuesta, canon ni fuentes.

Objeto: docs/auditorias/PROPUESTA_LOCALIZADORES_C031_F_TABLA_V2_2026-09-27.json, SHA256 `f5a497ba982f247f4bb3e64310b55f45da5758214cefabc0b803232c4691f375`. Se conserva v1, SHA256 `99166dc75d74faf1c6f53bea8e85ea084d39fa400f59667681c6e58cdf5d3fad`: su padre abreviado «Results» resolvía el subapartado/P10; la observación nominal produjo v2 con el encabezado completo. No se convierte esa abreviación previa en una falta de soporte científico.

## Cotejo primario

Leí el XML local S10, SHA256 `7e6d524b255fe17298149e1f0295b5350413ae68b5f6242f44f3014101cb5c98`, y los nueve párrafos directos P6–P14 del subapartado. La ruta exacta es:

Results and Discussion → Analysis of core genes consistently supports two primary domains, not three → quinto párrafo directo, JATS P10.

P10 identifica el análisis ML bajo LG+C60+G4+F y declara el resultado AU = 0.036 para el árbol 3D, condicionado al modelo y a la alineación de 35 genes. El fragmento original propuesto coincide literalmente. SHA256 del párrafo normalizado: `84cc93e813b02087fee2abec06592f5015abfdd458ee5cacfe67ac6de6faef87`.

También leí T1/Table 1: su objeto son distancias sumadas de cuartetos de superárboles. No es el localizador del resultado AU0.036. No se adjudican aquí sus valores ni su corrección editorial.

El título y DOI internos de S10 corresponden a Phylogenomics provides robust support for a two-domains tree of life, DOI10.1038/s41559-019-1040-x. El registro A distingue S09, Williams2013, de S10, Williams2020. Por tanto, el reemplazo S09→S10 en la fila Williams2020/AU0.036 identifica la fuente efectivamente leída; no se usa sólo semejanza de autores.

## Tres objetos autorizados

| Objeto | Posición CSV observada | Campo único | SHA256 de fila propuesta |
|---|---:|---|---|
| C-031, data/afirmaciones/02.csv | 16 | Fuente | `d602733bd48a4264d736d216d28750994bd6b9e7d6e616a378176c7e0f5d96c0` |
| F, data/apendices/F_magnitudes.csv | 11 | fuente con localizador | `8d9d1c62d5dfec55af5bcece47efc9f3d36d1b9e9e3f500af4758faa4c3d1051` |
| table-01, fila AU0.036/LG+C60+G4+F | 9 | filas y fuentes | `a597c1474b8ec44ec90b02709e7809e138ef150a8ad36ee0cb4e1e890e69a824` |

Los antes coinciden exactamente con las filas vivas; los SHA de archivos base y de filas antes/después se recalcularon y coinciden. No hay diferencias en otros campos. Las huellas completas ligan la identidad del objeto, pero no amplían el alcance de esta revisión a todas sus propiedades.

La celda de muestreo con BN-430 permanece idéntica. La referencia BN-115 se conserva en el metadato de fila. Se capturaron las filas BN y sus hashes para verificar preservación, no para certificar sus consultas ni rellenar el hueco. Las otras cinco filas Williams2020, todavía con S09, están identificadas mediante hash y expresamente fuera de este dictamen.

## Evidencia y límites de integración

- docs/auditorias/REVISION_INDEPENDIENTE_LOCALIZADORES_C031_V2_2026-09-27.json, SHA256 `dc9db3f8504cafca14f26a8c04fe49c89afc81223c14739cab6848b8a71cac29`.
- docs/auditorias/dictamenes_localizadores_c031_v2_2026-09-27.csv, SHA256 `7414e7ef3764b5ecec931be5821a70f4414bbed22ba4857fc77d8bcf130f6713`.

Se puede integrar exactamente el reemplazo de esos tres campos conforme a v2. Toda modificación adicional requiere su propio cotejo. No se certifican toda la ciencia o atomicidad de C-031, los ejes de F, las otras cinco filas, censos científicos, segundas revisiones globales, controles manuales ni make verify. La regeneración posterior no hereda una firma global de estos tres dictámenes.
