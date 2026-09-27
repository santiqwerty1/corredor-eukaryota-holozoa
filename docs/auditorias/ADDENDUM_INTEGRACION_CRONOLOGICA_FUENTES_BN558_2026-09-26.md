# Addendum: revisión independiente de integración cronológica

Revisión finalizada: 2026-09-26T21:57:55Z. Revisor de integración: /root/verificacion_fuentes_nuevas.

CONFORME para las 13 ligaduras VERIFICACION_FUENTE de S547–S559 y la ligadura
REINSPECCION de BN-558. Esta conformidad comprueba la integración del registro,
no constituye una nueva aprobación científica ni segunda revisión global.

## Estado exacto inspeccionado

- data/auditoria/fechas_objetos_revision.csv: 13 filas;
  SHA-256 `e1624c83c7e6975d090ebb15b2f931dcb1b78d2d96c820a346ae8957a3d07f94`.
- data/auditoria/fechas_ejecuciones_bn.csv: 409 filas en esta observación;
  SHA-256 `54d573667af92fe76bc2b473ec3a9ab43519e4ce9b59893b4dcd7d13fbecbd4c`. Solo BN-558 se revisa nominalmente aquí.
- Evidencia S548 y BN-558:
  docs/auditorias/confirmacion_final_s548_2026-09-26.csv;
  SHA-256 `571551cea1c97534e87e9af85035adda4cf285c6ec25f0440d1cd3508f871f6b`.
- CSV de dictamen por objeto: revision_integracion_cronologica_fuentes_bn558_2026-09-26.csv;
  SHA-256 `0051cf090b50d8feb16bd6d5d1bbd674adb532ddc1c9ba09f9fd24aa32c630a3`.

## Comprobaciones nominales

Para cada S se recomputó source_fingerprint de la fila A viva, se verificó
el SHA del CSV probatorio, se buscó la fila nominal exacta y se comparó
literalmente su fecha con la copiada al registro. Las doce filas ordinarias
apuntan a la fila CSV/clave correctas y a dictámenes CONFORME de identidad;
S551/S559 usan su addendum posterior, sin reutilizar los NO_CONFORME originales.
Las fechas históricas de consulta de las trece S siguen idénticas a HEAD.

S548 usa el registro A-S548 de su confirmación posterior, con la huella
canónica JSON `233871dc64f3916d4ab38519893b6df351a14dd81c5d0cf5ff2716226184d2e0`
y UTC 2026-09-26T21:49:34Z. No reutiliza la huella A anterior de la primera
verificación de identidad. La evidencia conserva también su propia huella de
fila CSV con QUOTE_ALL; se comprobaron ambos algoritmos por separado y no se
confunden la huella de bytes CSV y la canónica del registro temporal.

BN-558 usa la fila nominal BN-558 de esa misma confirmación, con huella
canónica JSON `d16f1b092bf754e97876e987201d909daa27f14a823d9d0c8fd7ba2684ab6ec4`
y UTC 2026-09-26T21:49:34Z. La evidencia declara reinspección del universo
nominal y el registro conserva REINSPECCION, no EJECUCION_ORIGINAL.
Se comprobó la coincidencia literal de la fecha y las dos serializaciones de
la fila; no se volvió a juzgar el resultado científico de esa búsqueda.

Los cargadores estructurales devolvieron 13/0 errores y 409/0 errores. Esto
solo describe su validez estructural y ligadura de archivos, no la vigencia
científica de todos sus objetos. Los archivos permanecieron iguales desde el
inicio hasta el final de esta inspección.

## Historia y límites que permanecen

Las otras 408 filas del registro BN documentan la observación anterior del
inventario de 434 artefactos. No se certifican aquí como vigentes para el
inventario ampliado de 442 ni se anticipa la revisión en curso de sus nuevas
huellas. Una futura adición de 408 registros nuevos queda fuera del hash de
archivo completo observado arriba y fuera de este dictamen.

BN-083 no está integrado como reinspección integral: las dos consultas
adicionales realizadas son evidencia parcial 2/13 y conservan su alcance.
Los dictámenes anteriores de identidad y sus addenda permanecen intactos.
No modifiqué los registros ni sus fechas, el corpus, las fuentes o las firmas
científicas. Soy autor de parte de la evidencia bibliográfica previa, pero no
de la integración revisada; aquí solo cotejo la transcripción/ligadura contra
esa evidencia y el corpus vivo, sin presentarla como otra revisión científica
independiente de mis propios dictámenes.
