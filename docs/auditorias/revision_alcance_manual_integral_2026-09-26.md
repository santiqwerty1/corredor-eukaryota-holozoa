# Revisión independiente de la ligadura integral de controles manuales

Revisor: `Codex /root/revision_residuales/candidatos_editoriales`.
Comprobación final de código y pruebas: 2026-09-26T22:23:23Z.
Rama inspeccionada: `codex/cierre-plan-pendiente`.

## Dictamen y límites

**CONFORME para la implementación de infraestructura identificada por las
huellas finales de este informe**, después de corregir dos hallazgos
adversariales. No es un dictamen sobre ninguno de los 210 requisitos, una
aprobación científica, una segunda revisión de sus objetos ni el cierre de
`make verify`.

El revisor escribió la propuesta estructural antecedente, pero no implementó
`manual_scope_paths`, sus guardas ni las correcciones de producción. Los
defectos se comunicaron al autor y este los corrigió; la reinspección ejecutó
adversarios propios. No se cambió corpus, controles, ledger ni firmas desde
esta revisión. Las escrituras de prueba se limitaron a fixtures y copias
temporales; este informe es la evidencia documental nueva.

## Delta realmente inspeccionado

Se cotejó el diff y la versión viva con la propuesta
`propuesta_alcance_manual_integral_2026-09-26.md`, además del contrato temporal
y las dependencias del renderizador. El cambio convierte la base especial
de cinco controles editoriales en una base integral para todos los manuales,
conserva destinos específicos y excluye dependencias circulares conocidas.

Como control de que no se relajaron validadores laterales, se sustituyó
**solo la función `manual_scope_paths`** en una cadena en memoria por su texto
anterior a esta implementación. El archivo reconstruido da exactamente el
SHA-256 anterior `d7b0bff89c439633d73706d3039e7bd0372708e9c511c0a5413620e9510c131a`.
Por tanto, respecto de ese checkpoint, el resto del auditor permanece
byte a byte igual: clasificación, promociones, validación del literal,
evidencia nominal, independencia, fechas y ligaduras no se rebajaron aquí.
El diff contra HEAD contiene cambios temporales anteriores y no se confundió
ese baseline distinto con el alcance de esta revisión.

## Hallazgos y reinspecciones conservados

### ALCANCE-01: consumidor de firmas incluido por referencia explícita

La primera implementación no añadía auditorías indiscriminadamente, pero
aceptaba que `docs/order.txt` nombrase el propio
`docs/auditorias/revision_manual_requisitos_2026-08-08.csv`.
Un fixture independiente devolvió `ledger_from_order_in_scope=True` para
R-0090. El mismo problema podía entrar por un destino de índice o extra.
La firma pasaba a formar parte del objeto firmado: escribirla cambiaba
su propia huella. No se emitió conformidad de esa versión.

No se conserva una huella de aquella primera versión de código: el hallazgo
se documenta por la consulta ejecutada y el comportamiento observado, no por
una congelación retrospectiva inventada. La corrección del autor añadió
rechazo explícito de `manifest.json`, disposiciones y el árbol de auditorías,
con la excepción nominal de Q para R-0399. Se comprobó el rechazo, no una
omisión silenciosa de esos destinos.

### ALCANCE-02: redirección de la propia identidad canónica

La primera corrección, SHA-256
`5d3e5e93ec8817ad9c2c119ab470eb70515f28301495afaf19f9e8a661585edb`,
comparaba rutas resueltas con identidades canónicas sin resolver. Los
adversarios independientes reprodujeron cuatro fallos:

1. `manifest.json` como enlace interno a `data/consumer-payload.txt`.
2. `data/auditoria/requisitos_disposiciones.csv` enlazado a un archivo interno.
3. El directorio `docs/auditorias` redirigido dentro del repositorio, ocultando
   el ledger al control por prefijo.
4. Q enlazado a `data/q-payload.txt`, que podía entrar desde el orden de R-0090
   aunque su excepción pertenece únicamente a R-0399.

La ejecución de 17 pruebas devolvió cuatro fallos de subcasos, mientras los
otros comportamientos comprobados pasaban. Se comunicaron antes de firmar.
El autor reforzó las guardas con identidad lógica normalizada y resuelta,
destinos de consumidores canónicos y el directorio de auditorías también
resuelto. Q solo se admite para R-0399 cuando ambas identidades coinciden
con su ruta nominal, sin redirección. Los cuatro adversarios anteriores
rechazan ahora la entrada y la batería completa pasa.

No se detectó ninguno de esos ciclos en el corpus vivo: fueron defectos
reproducidos en fixtures, no atribuciones de manipulación al usuario.

## Censo vivo de los 210 manuales

El censo propio reconstruyó la base desde índice, glob y orden leídos del
repositorio, y comparó conjuntos completos, no solo cardinalidades:

| Comprobación | Resultado |
| --- | --- |
| Controles manuales | 210 |
| Controles automatizados | 42, sin reclasificación inducida |
| Alcances de 127 archivos | 209 |
| Alcance R-0399 | 128 archivos, añade Q |
| Promociones provocadas por calcular el alcance | 0 |
| Archivos vigilados antes/después del censo | 131, ninguno cambió |
| Destinos específicos perdidos | 0 |

La base es de 97 CSV, 26 plantillas, índice, orden y ambos informes. No se
codifican esas cifras como límite: las altas de tablas y plantillas cambian
el conjunto. El censo comprobó que cada resultado conservó exactamente su
estado y sus pruebas después de calcular el alcance.

SHA-256 de la serialización del mapa completo ID → rutas censadas:
`5f8e3555bfae51bbbfedc2df00dc2f8381f3a3b52fb8f93ca732ebe311789522`.
Serialización: JSON con claves ordenadas, `ensure_ascii=False`, separadores
`,` y `:`, seguido de LF; los valores son la lista de rutas relativas
ordenadas unidas con `;`, como exige el contrato actual.

## Adversarios independientes y pruebas

La batería propia contiene 17 pruebas, con subcasos para:

- Cambiar cada archivo base y observar una huella distinta; contrastar
  además la serialización SHA con una implementación independiente.
- Conservar un insumo específico y las exclusiones de código existentes.
- Añadir/quitar una tabla y una plantilla nueva no ordenada con `Corpus`
  ya creado; añadir una plantilla ordenada fuera del glob, sin perder las
  plantillas anteriores. Las entradas repetidas no duplican el conjunto.
- Suprimir cualquiera de los ocho archivos de un fixture base: todos fallan
  cerrados. Directorios, enlaces rotos y bucles tampoco producen un alcance.
- Introducir rutas externas desde índice, secciones, orden y extras,
  escape `..` o enlace exterior: se rechazan. Un enlace interno lícito liga
  los bytes que se consumen y cambiar los bytes de su destino invalida la huella.
- Intentar introducir siete consumidores desde orden, índice, extras y
  enlaces: 28 combinaciones rechazadas; comprobar las cuatro variantes
  adicionales de ALCANCE-02 y el carácter nominal de Q.
- Cambiar archivos de revisión no ligados sin alterar base ni huella.
- Validar una fila puramente sintética, modificar su fixture y comprobar
  que la huella antigua se rechaza sin reescribir la fila firmada.
- Copiar las entradas editoriales reales a un directorio temporal y ejecutar
  `render_report` en ambos modos y `control_csv_payload` antes/después de
  introducir firmas y derivados de auditoría no ligados. Las dos salidas y
  el contenido de H permanecieron exactamente iguales.

La primera ejecución del fixture de validación de firma carecía de `entries`
en su objeto sintético; se corrigió ese fixture, no el código de producción.
Ese error de montaje no se contabiliza como defecto del repositorio.

Ejecuciones finales:

```text
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/revision_alcance_manual_integral_20260926.py
17 pruebas, 3.126 s, OK

PYTHONDONTWRITEBYTECODE=1 python3 /tmp/censo_alcance_manual_integral_20260926.py
210 manuales; 42 automatizados; 209 × 127 rutas y 1 × 128; exit 0

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_manual_editorial_scope tests.test_audit_requirement_controls tests.test_assemble_manual_review_ledger -q
44 pruebas, 11.451 s, OK

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
201 pruebas, 17.438 s, OK

git diff --check -- scripts/audit_requirement_controls.py tests/test_manual_editorial_scope.py
exit 0
```

## Circularidad y cautelas que permanecen

La inspección de dependencias y el experimento aislado concuerdan: informes
y H no consumen firmas actualmente; ligarlos no introduce por sí solo un
ciclo. El rechazo de auditorías es conservador. Un nuevo insumo científico
en ese árbol requerirá excepción nominal y revisión de dependencias, no
retirar la guarda. Esta comprobación no es un analizador general de todas
las futuras dependencias posibles.

La ampliación invalida firmas cuando cambia cualquier archivo de la base,
aunque el cambio no afecte sustantivamente a su literal. Hay que estabilizar
y regenerar primero; no recalcular huellas ni fechas sobre dictámenes
antiguos. Los hashes no prueban lectura, ejecución auténtica ni apoyo
científico. Esta revisión tampoco convierte los 210 controles en conformes.

## Huellas finales

| Archivo | SHA-256 |
| --- | --- |
| `scripts/audit_requirement_controls.py` | `dd1ce68ca9a9fd29ad2501daed3fffa2951459da2fb07608182c0418b5c1b2e2` |
| `tests/test_manual_editorial_scope.py` | `3c3358dd416639d06b2c2c16c0eadbab6965ec7b8c4bb1fc79b42cc9c4996b7d` |
| `tests/test_audit_requirement_controls.py` | `38de59c78108dfe042a48b0b72645733bdfacdb23b68cd92f13226fe4faf0324` |
| `tests/test_assemble_manual_review_ledger.py` | `1d99972d8aafa2485072e948387fb01d543b8d5a4c435b0ea4f664ff805610ff` |
| `scripts/corpus_io.py` | `4d7d35fb8649d41e4c137da16e1991a1a4117d8c46b68aa5d7fc3ae0c462fef7` |
| `scripts/build_audit_deliverables.py` | `50884b7a6bce0c2bd232848b3c2eca5a7446a55e88da90bc203bbf604df88bd0` |
| `/tmp/revision_alcance_manual_integral_20260926.py` | `4bff404da5f51c052f334b99a7d42a2fa16c71860e3385c0248893aa8d76c21d` |
| `/tmp/censo_alcance_manual_integral_20260926.py` | `2626a569ff5bad8a8ce0d7fc95cebce9572cb3a387bee4f8dcce6458f0b53319` |

Los scripts propios están en rutas temporales; sus huellas y métodos quedan
consignados aquí. No se atribuye persistencia futura a esos archivos ni se
confunde esta revisión de infraestructura con evidencia primaria científica.
