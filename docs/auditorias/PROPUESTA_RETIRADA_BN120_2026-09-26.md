# Propuesta de retirada activa de BN-120, preservando su historia

Inspección del contrato y simulaciones de solo lectura: 2026-09-26T22:41:06Z.
Autor: `/root/verificacion_fuentes_nuevas`. Rama:
`codex/cierre-plan-pendiente`. No se ejecutó la retirada, no se regeneraron
derivados y no se modificó corpus, código, fuentes ni registros de fechas.

## Conclusión

La retirada de BN-120 del catálogo **activo** es compatible con las anclas
históricas existentes: no forma parte de las 106 BN originales ni de las 68
activas congeladas. No hay que cambiar `build_negative_history`, su exigencia
de 106 filas ni AF600/AF603/AF604. Debe preservarse separadamente su historia
posterior al corte, pues el builder Q no conserva eventos retirados de ese
grupo.

La solución mínima es un archivo histórico explícito y verificable, fuera de
las tablas BN activas, con la fila completa BN, la fila Q-0181 previa, sus
huellas, la fecha antigua declarada pero no acreditada, las pruebas reales del
26-09 y la causa nominal de retirada con C-2821/C-2822. No mantener una BN
negativa artificial por la identidad no demostrada entre anotaciones.

## Hechos del contrato comprobados

| Componente | Comportamiento y consecuencia |
| --- | --- |
| `build_audit_deliverables.load_negative_rows` | Solo carga tablas del índice con categoría `negative`. El archivo histórico nuevo debe quedar fuera de esa categoría. |
| `build_negative_history`, líneas 1726–1786 | Exige 106 filas y preserva las 68 activas originales. BN-120 no pertenece a ese conjunto. Simulación: su salida y los deltas son idénticos al quitar únicamente BN-120. |
| `build_search_matrix`, líneas 1820–1957 | Q-0001…Q-0165 están congeladas. Las altas posteriores se reconstruyen desde las BN activas y se numeran consecutivamente; una BN posterior retirada deja de producir Q viva. |
| `audit_full.audit_searches` | Exige secuencia Q continua, las 165 huellas originales, una Q por alta BN activa y fechas ligadas a su huella. No admite inventar una Q postcorte `RETIRADA` para BN-120: AF617 exige P1 a una BN posterior ausente de las 106 históricas. |
| `audit_chronology.load_search_dates` | Valida el registro por identidad+huella, fecha, evidencia y localizador; no exige que cada versión histórica siga activa. Por tanto puede conservarse la reinspección de BN-120 después de retirarla. |
| `validate`, referencias internas | Toda BN mencionada en C, apéndices, tablas indexadas o plantillas debe existir activa. La historia de BN-120 no puede dejarse como referencia viva en C-1990, table-53 ni una nota añadida a esas plantillas. |
| Magnitudes/MREQ | MREQ-0044 debe pasar a `VALOR_PUBLICADO` con C terminales reales, sin BN residual. El literal R-0266 no exige que las cifras de fuentes distintas sean la misma anotación. |
| `remediate_trace_residuals` | El control exacto de cuentas cambia de 499/487/12 a 498/486/12 por esta única retirada. Los 410 residuales, 408 BN v3, dos positivos nominales, duplicados y consultas permanecen intactos. |

La fila temporal de BN-120 debe conservarse literalmente:
REINSPECCION `2026-09-26T22:07:15Z`, huella BN
`93f842a7e278911b6160bac9149fd5bbd7b7f6c9395bd707ba147b3cf16c5248`,
evidencia `docs/auditorias/reinspeccion_bn_fuentes_2026-09-26.csv`, SHA
`52c9cff24e1361d1aab1cca7fa08df22ce81a64a331ba37239dbed89b9594fdb`, fila CSV 5.
Ese evento encontró Ensembl, no es todavía el cotejo posterior de los SI de
S434. La inspección S434 tiene su propia evidencia de `22:25:54Z` en
`evidencia_propuesta_bn120_s434_2026-09-26.json`. No intercambiar sus resultados
ni adjudicar ambas observaciones a la fecha original.

## Riesgo Q demostrado en memoria

El CSV Q todavía presente al inspeccionar tiene SHA-256
`31a4ecf4665bd1a7b96f2cf8e3171d01802dda865441b878c9f7a9e3c60cba94`.
Su Q-0181 corresponde a BN-120 y declara 2026-08-13. Esta fecha no cuenta con
prueba de ejecución original y no debe convertirse en fecha acreditada.
La huella de la fila completa Q-0181 es
`fbfd8a456662ce31de0c0f9065d3f84f45d43abc0b2b6ef875b2887823e6d74a`.

Se llamaron en memoria los builders con las entradas congeladas y la fila
viva, y después con una copia del diccionario activo sin BN-120:

- 499 BN, 487 no localizadas, 12 ausencias declaradas → 498/486/12.
- Historia original de 106 BN y sus deltas: exactamente iguales.
- Q calculadas en ese momento: 607 → 606; las primeras 165, idénticas.
- Antes de la retirada virtual, el builder ya asigna Q-0181 a BN-118 y
  Q-0182 a BN-120, debido a las reinspecciones históricas incorporadas.
- Después de la retirada virtual no queda Q viva de BN-120, y Q-0182 pasa a
  BN-121. No se debe presentar ese renumerado derivado como continuidad de
  identidad del Q-0181 antiguo.

Las cuentas de Q describen esta observación, no son nuevas constantes: otras
reinspecciones en curso pueden añadir eventos. La identidad duradera del
antecedente debe ser la pareja **versión/SHA del registro + Q-0181**, además
de la huella de fila, y no Q-0181 sin contexto. No hay referencias a Q-0181 ni
BN-120 en el manifiesto `requisitos_disposiciones.csv` inspeccionado.

## Antecedente Q-0181 que debe preservarse íntegro

La siguiente copia nominal es evidencia de lectura anterior al parche,
no una nueva ejecución ni declaración de vigencia:

```json
{
  "id_busqueda": "Q-0181",
  "fecha": "2026-08-13",
  "bloque": "alta de control manual BN-120",
  "clave_bn": "BN-120",
  "prioridad": "P1",
  "objetivo": "Número agregado de genes publicados y densidad o promedio numérico de intrones para Sphaeroforma arctica JP610 en una misma versión de anotación",
  "consulta_exacta": "\"Sphaeroforma arctica genome genes introns 121.6 Mb\"; \"Sphaeroforma arctica gene count intron density\"; \"Sphaeroforma arctica JP610 genome annotation genes\"",
  "servicio": "corpus vivo; consulta exacta reproducible declarada en la fila BN",
  "fuentes_evaluadas": "BN-120: no se incorporó una fuente positiva; el resultado negativo enumera lo recuperado y lo que falta.",
  "resultado": "La consulta del 13 de agosto de 2026 recuperó páginas de genes individuales de NCBI, el método de anotación genómica de S. arctica y la comparación de intrones de S434, pero no una cifra agregada estable de genes ni una densidad o promedio numérico de intrones atribuible a la misma versión del ensamblaje de 121.6 Mb. El hueco se conserva; no se estima una cifra contando identificadores parciales ni se mezcla una versión actual de RefSeq con la reconstrucción comparativa de S434.",
  "accion_inicial": "NO_APLICA: alta posterior al inventario Q congelado.",
  "cambio_realizado": "ALTA_CANONICA_DOCUMENTADA",
  "desencadenante": "Nueva evidencia primaria que responda al hueco literal o amplíe el censo indicado.",
  "evidencia_final": "BN-120; sha256_fila_bn=93f842a7e278911b6160bac9149fd5bbd7b7f6c9395bd707ba147b3cf16c5248; no se convierte el resultado negativo en una inferencia positiva.",
  "estado_registro": "HUECO_CIENTIFICO_ETIQUETADO",
  "huella_inicial_sha256": "NO_APLICA"
}
```

## Plan concreto, sin relajar contratos

1. **Antes de regenerar**, crear por ejemplo
   `docs/auditorias/retirada_bn120_2026-09-26.json`. Contenido mínimo:
   ruta/cabecera/fila completa de la BN previa y su SHA; fila Q anterior
   completa y su SHA; SHA del CSV Q de origen; fecha original declarada y
   calificación `NO_ACREDITADA`; evento de reinspección del 26-09 con clase,
   instante, evidencia/SHA/localizador; evento de cotejo S434 separado;
   motivo de retirada; C finales y huellas posteriores a su aplicación;
   instante real de la retirada; autor y estado de revisión independiente
   inicialmente pendiente. No inventar ese instante ahora. La fila completa
   BN también está conservada en el JSON de propuesta científica.
2. **Aplicar la corrección científica** ya acordada: C-2821/C-2822, F,
   table-53, prosa y C-2783 mínimo. MREQ-0044 pasa a valor publicado, con C
   terminales; R-0266 incorpora las nuevas C en su alcance, sin autoaprobarlo.
   C-1990 conserva solo BN-121/BN-122 y dos magnitudes. Su dependencia
   C-2784 exige nueva revisión del alcance/huella aunque su ciencia no cambie.
3. **Retirar únicamente la fila activa BN-120** y todas sus referencias
   vigentes en C-1990, fuentes/# de table-53, especificación de magnitudes y
   mapeos. No borrar sus apariciones en evidencia histórica congelada,
   propuestas, dictámenes anteriores o el archivo de retirada.
4. **Conservar el registro temporal** de su reinspección, con la huella
   antigua. No cambiar clase a EJECUCION_ORIGINAL y no ligar esa fila a otra
   BN. No agregar un evento duplicado con la misma identidad/huella para
   simular el cotejo S434: éste queda como evento distinto en el archivo.
5. **Ajustar la cuenta exacta** `EXPECTED_BN_COUNTS=(498,486,12)` y comentario
   nominal de retirada; no tocar reglas v3 ni excepciones positivas.
   Adaptar el fixture de tests para 88 BN previas + BN-557/558 + 408 v3,
   identificando explícitamente a BN-120 como retirada. No eliminar las
   pruebas que rechazan perder BN-557, duplicados, marcas v3 ajenas o un
   censo distinto de 410/408.
6. **Regenerar con los builders estrictos**: remediator actualiza C-1931,
   C-1933, F y prosa de recuento; render actualiza H y exports según su flujo.
   Actualizar linajes, mapeos, procedencia, magnitudes, Q y matrices. Q debe
   dejar de mostrar BN-120 como hueco vigente; no inyectar una Q artificial
   P1 ni alterar `build_negative_history` para conseguirlo. Conservar el
   antecedente como historia explícita externa a Q viva.
7. **Revisar independientemente** el contenido de C y celdas, la retirada y
   la correspondencia exacta entre archivo histórico y antecedente. Las
   firmas previas de controles se invalidan al cambiar corpus/derivados:
   no recalcularles la huella ni trasladar una conformidad antigua.

El archivo histórico no debe convertirse en una tabla del índice, ni se debe
añadir a la narrativa científica una cita BN-120 ya indefinida. Se puede
enlazar desde la documentación de auditoría fuera del corpus indexado. Si se
exige conservar Q-0181 con idéntica identidad **dentro del Q vivo**, hará falta
un contrato de eventos e identidad postcorte y su revisión específica; el
builder actual no ofrece esa garantía. No recomiendo introducir ese cambio
más amplio para una sola retirada.

## Controles y pruebas de aceptación de la implementación

- Archivo histórico: SHA de la fila BN exactamente
  `93f842a7e278911b6160bac9149fd5bbd7b7f6c9395bd707ba147b3cf16c5248`;
  SHA del Q previo exactamente el indicado; fecha original no acreditada;
  prueba del 26-09 intacta; C-2821/C-2822 existentes y con huellas exactas.
- Registro activo: BN-120 ausente, las restantes 498 claves preservadas;
  486 no localizadas, 12 ausencias declaradas y cero NO BUSCADO; las 408 BN
  v3 mantienen identidades y ámbitos, además de BN-557/558 científicas.
- Adversarios nuevos: reintroducir BN-120 activa debe fallar por cuenta;
  retirar otra fila debe fallar; corrupción de una celda o huella histórica
  debe detectarse en la prueba de preservación; ninguna fecha original puede
  obtenerse de la reinspección ni del propio Q derivado.
- `validate` sin BN indefinidas; MREQ-0044 sin hueco residual; C-2783 solo
  sintetiza C-1565/C-1566. F conserva modalidad inferida para la densidad.
- Historia de 106 filas, subconjunto original de 68, distribución 22/23/23 y
  las primeras 165 Q/huellas completamente intactos. Q nueva determinista y
  sin BN-120 negativa actual; historial anterior conservado externamente.
- `load_search_dates` conserva la reinspección aunque su BN ya no sea activa;
  en la observación de este informe cargó 833 versiones y cero errores.
- Controles R-0266 y R-0399 y los afectados por corpus/derivados deben
  regenerarse y revisarse según el contrato, sin usar este informe como
  aprobación científica global.
- Ejecutar tests de remediator, cronología y entregables, `git diff --check`,
  luego `make verify` determinista/idempotente/aislado cuando las nuevas
  revisiones nominales estén realmente disponibles.

La copia de solo lectura y las simulaciones de este informe no certifican una
retirada todavía no aplicada ni constituyen el cierre de esos controles.
