# Identidades estables y sucesiones de afirmaciones

Autorización del usuario recibida el 2026-09-27, durante el cierre de
`codex/cierre-plan-pendiente`. Este contrato documenta la transición solicitada;
no es un dictamen científico ni una aprobación de las sustitutas.

## Numeración

En este cierre se conservan las claves C canónicas publicadas. No se ejecutará
una renumeración global para insertar, corregir o descomponer afirmaciones.
Las nuevas proposiciones reciben números nuevos al final de la secuencia;
una clave retirada nunca se reutiliza. Los IDs reservados en propuestas aún
no integradas no deben tratarse como filas canónicas presentes.

El contenido de una fila sí puede cambiar tras auditoría. Por eso una clave
estable no equivale a una versión inmutable: un consumidor debe fijar commit
y comparar la fila completa, además de leer sus sucesiones.

`scripts/renumber.py` sigue existiendo como herramienta de migración. Su uso
fuera de esta política requeriría una decisión explícita y una migración
coordinada, mapa completo antes/después, actualización de todos los consumidores
y nueva revisión de las ligaduras afectadas. No es una operación prevista para
este cierre. Actualmente no actualiza de forma general `data/auditoria/` y sí
reescribe archivos de `docs/auditorias/`; ejecutarlo sobre expedientes firmados
invalidaría sus huellas y podría alterar evidencia histórica. No debe usarse
como reparación automática de una partición.

## CSV de sucesiones

Ruta: `data/auditoria/sucesiones_afirmaciones.csv`. UTF-8, CSV con comillas,
salto LF y exactamente estas cuatro columnas:

- `fila_retirada`: C que deja de representar la proposición científica compuesta.
- `filas_sustitutas`: C explícitas, separadas por punto y coma y espacio; sin rangos.
- `motivo`: razón de la partición y referencia al expediente que conserva el original.
- `fecha`: instante UTC de inscripción de la sucesión en este registro, con formato
  `YYYY-MM-DDTHH:MM:SSZ`. Una inscripción retrospectiva se identifica en `motivo`;
  nunca se inventa la fecha de una edición histórica.

Se registran sucesiones materializadas, no propuestas ni autorizaciones futuras.
La primera entrada registra el caso preexistente C-681. C-1581 no se incorpora
hasta que su transición esté efectivamente aplicada. Si una sustituta se divide
después, se añade su propia sucesión; no se reescribe la transición anterior.
No se admiten autocitas, ciclos ni destinos ausentes del registro canónico.

## Materialización autorizada

1. Conservar la fila original íntegra, sus claves, procedencia y huella en un
   expediente de auditoría antes de modificar su representación activa.
2. Mantener el ID original como fila de registro: `Atribución=glosa`,
   `Predicado=tiene_estado*`, `Vigencia=superada`, con las sustitutas nombradas.
3. Incorporar una fila nueva por proposición atómica, sin perder ninguna posición
   científica, limitación de alcance o contraevidencia.
4. Revisar nominalmente los consumidores de la clave antigua: síntesis, tablas,
   entidades, mapeos, controles, material no encajado y demás datos de auditoría.
   Una sustitución textual indiscriminada no demuestra la pertinencia del enlace.
5. Registrar la sucesión y someter original, sustitutas, relaciones y derivados
   a las revisiones independientes exigidas. La autorización editorial no las aprueba.

Para C-1581 se conserva además la formulación literal de S352 y sus límites en
cada sustituta, conforme a la autorización específica. El original y sus
contraevidencias no desaparecen del historial.
