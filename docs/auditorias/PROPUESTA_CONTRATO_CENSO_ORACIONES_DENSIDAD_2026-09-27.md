# Propuesta de contrato: spans nominales y densidad por oración

Estado: **PROPUESTO, NO IMPLEMENTADO, SIN FIRMAS**. Autor: `/root/verificacion_fuentes_nuevas`. Esta propuesta acompaña la reparación autoral de NC-DEN02; no cierra NC-DEN01 ni R-0393/R-0394 y no autoriza rellenar un ledger con dictámenes automáticos.

## Dos objetos distintos

1. **Frontera de oración**: dónde empieza y termina la unidad. El segmentador formal proporciona candidatos y diagnósticos, no resuelve toda ambigüedad lingüística. Una inicial sin delimitación, como `B. floridanus`, puede parecer un final de oración. Deben conservarse el corte y la lectura como abreviatura hasta una adjudicación nominal independiente.
2. **Densidad y soporte**: si la oración contiene uno de los siete objetos del literal R-0393 y qué fuente/localizador la acompaña. Un límite de oración correcto, una C existente o una S resoluble no prueban que el pasaje respalde la proposición.

Los dos objetos deben poder fallar por separado. Resolver una frontera no aprueba ciencia; añadir una cita no resuelve una C compuesta.

## Alcance y coordenadas propuestas

El censo futuro debe inventariar toda la prosa del entregable vivo, incluidas unidades finalmente declaradas no aplicables con motivo nominal. Debe enumerar sus archivos y fijar SHA256 de bytes, índice/orden de entrada y versión del segmentador. La ausencia de un disparador regex no basta para excluir una oración sobre parentesco, carácter o mecanismo.

Cada bloque debe conservar:

- Ruta, localizador de archivo, texto completo y SHA256(UTF8(texto + LF)).
- Base explícita de offsets: puntos de código Unicode, inicio incluido y fin excluido; nunca bytes confundidos con caracteres.
- Si se usan bloques normalizados, texto normalizado y mapa reversible a las posiciones originales. Mientras ese mapa no exista, los offsets del bloque se etiquetan expresamente como offsets del bloque, no del archivo.
- Todos los spans candidatos, grupos de cita pospuestos ligados a la oración precedente, frontera elegida y motivo de la adjudicación. Candidatos ambiguos o modificados no se aprueban por proximidad o semejanza.

La API autoral `sentence_spans` expone offsets exactos sobre el texto que recibe. La matriz de traza vigente no cambia de columnas y sólo conserva ruta/líneas/ordinal de oración. Por tanto, un censo nominal futuro no debe fingir que esa matriz ya contiene offsets de archivo ni cambiar su esquema silenciosamente.

## Expediente nominal mínimo

Una revisión de frontera propuesta incluirá: identidad del bloque; todas las huellas anteriores; offsets alternativos; elección exacta; razón concreta; autor del texto, revisor distinto, declaración de independencia, UTC real, dictamen y evidencia contextual. La revisión debe ser posterior a la versión que leyó. Una edición no hereda el dictamen por recalcular su hash.

Una revisión de densidad propuesta incluirá por oración:

- Texto exacto, spans y huellas de bloque/contexto; C correspondientes y sus huellas.
- Categorías aplicables: fecha, cifra, taxón atribuido, parentesco, carácter diagnóstico, mecanismo o atribución de hipótesis. `NO_APLICA` requiere motivo leído, no una lista de rutas exentas.
- Cada cita que aparece dentro de la oración o en su grupo pospuesto propio: clave S canónica, identidad/versiones de la fuente, fragmento de cita en prosa y localizador declarado; sus offsets permiten comprobar que no proceden de la oración vecina.
- Distinción explícita entre `LOCALIZADOR_DECLARADO`, `SIN_LOCALIZAR_HONESTO` y `[SIN FUENTE]`. La marca honesta autorizada por el encargo no se convierte en pasaje recuperado ni requiere inventarlo. La salida sin fuente debe conservar la oración y su explicación en la misma línea, además de la C exigida por el registro.
- Evidencia primaria/versionada cuando se dictamine que un localizador realmente sostiene cada componente científico. Existencia del DOI, palabra «resultados» o acceso al PDF no bastan.
- Autor/revisor distintos, independencia, UTC, dictamen y límites. Para la segunda revisión del censo se exige otra lectura independiente de la versión final, no la ejecución del consumidor.

La excepción de tesis general no cubre una cifra concreta con clave S desnuda. El circuito debe respetar la admisión explícita de imprecisión honesta, sin confundirla con localización exacta y sin expandir esta tarea a la pasada aplazada de todas las marcas «sin localizar».

## Consumidor prospectivo, aún no implementado

La puerta futura deberá validar esquema cerrado, tipos, calendario/orden UTC, identidad nominal e independencia; población exacta de bloques y oraciones; ausencia de duplicados; offsets y literales coincidentes; cobertura sin solapamientos indebidos ni texto omitido; fuentes/C resolubles; huellas actuales; evidencias locales existentes y no circulares. Debe conservar motivos negativos o ambigüedades como bloqueos, no eliminarlos al construir el censo.

Para utilizar una frontera adjudicada, exigirá correspondencia exacta con el bloque, las alternativas y el dictamen independiente vigente. No tomará una lista de rangos como permiso genérico para fusionar cualquier texto ni prestará C entre spans. Ante archivo nuevo, edición, cambio de contexto, cita desplazada, revisor en conflicto o prueba ausente, fallará de forma cerrada.

La materialización debe ligar el resultado a los bytes realmente revisados y comprobar su vigencia antes de emitir el artefacto; no combinar un resultado viejo con una huella nueva. No usar manifest, controles derivados o el propio censo agregado como fuente circular de aprobación. Inode/mtime, si se emplean para carreras, no se serializan como evidencia determinista. La ejecución final necesita entradas aisladas: no se promete inmunidad a escrituras posteriores al último chequeo.

## Integración mínima posterior

1. Revisión independiente del segmentador y sus nuevos diagnósticos; adjudicación nominal de las fronteras ambiguas, sin cambiar prosa para evitar el caso.
2. Inventario y adjudicación independiente de unidades sin C o rótulos expuestos; reparar contenido sólo con autorización y evidencia, sin nuevas exenciones de rutas/prefijos.
3. Diseñar/revisar el consumidor de spans y densidad conforme a este contrato; mantener todas las puertas C, de celdas y de semántica actuales.
4. Sólo con los expedientes reales adecuados, integrarlo como prueba adicional para R-0393/R-0394. Derivar estados mediante los builders estrictos, no editar una clasificación manualmente para conseguir un verde.
5. Regenerar traza/derivados y ejecutar verificación aislada, determinista e idempotente. Este documento no demuestra ninguno de esos pasos futuros.
