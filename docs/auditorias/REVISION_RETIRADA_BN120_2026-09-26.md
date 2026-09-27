# Revisión de la retirada activa de BN-120

Revisor: `/root/verificacion_fuentes_nuevas`. Inspección estable posterior al
remediator: 2026-09-26T22:49:37Z. Autor del cambio: `/root`.
No edité el corpus, registro temporal, código ni archivo de retirada.
Participé en la investigación primaria y propuesta anterior; esta revisión
declara ese antecedente y no se presenta como firma del censo global.

**CONFORME para la retirada nominal, preservación histórica y delta del
remediator.** No cierra R-0266, BN-121/122 ni `make verify`. El registro Q en
disco todavía requiere regeneración al momento de esta revisión.

## Preservación comprobada contra el estado vivo

Archivo de autor revisado:
`docs/auditorias/retirada_bn120_2026-09-26.json`, SHA-256
`bdcdbb7e12e3d84ff3b7ac811d44da851b0f1b5a66e506c42b21090b06d895bc`.

- Sus 499 claves/huellas previas se compararon contra todas las filas vivas:
  única baja **BN-120**; ninguna alta y ninguna modificación entre las otras
  **498**. No se confunde la retirada con una búsqueda negativa nueva.
- La fila BN completa reproduce
  `93f842a7e278911b6160bac9149fd5bbd7b7f6c9395bd707ba147b3cf16c5248`.
  Reinsertarla en memoria en su posición original, con cabecera y formato
  QUOTE_ALL/LF, recupera exactamente el SHA del archivo anterior:
  `faa3f504f57e4683d4c9753400135e1e7a0bbadf1e0300c30b2c94d0955f6bfb`.
- Q-0181 completa reproduce
  `fbfd8a456662ce31de0c0f9065d3f84f45d43abc0b2b6ef875b2887823e6d74a`;
  el registro de origen queda identificado por su SHA
  `31a4ecf4665bd1a7b96f2cf8e3171d01802dda865441b878c9f7a9e3c60cba94`.
  Coincide con la copia independiente previa al parche conservada en
  `PROPUESTA_RETIRADA_BN120_2026-09-26.md`.
- La fecha antigua 2026-08-13 se conserva como declaración **NO_ACREDITADA**;
  la reinspección real `2026-09-26T22:07:15Z` queda separada del cotejo de
  suplementos S434 `2026-09-26T22:25:54Z`. Las tres pruebas enlazadas en el
  archivo existen y sus SHA coinciden.
- `load_search_dates` conserva la reinspección BN-120 de la huella retirada,
  clase REINSPECCION y prueba CSV/fila 5 originales; cargó 833 versiones y
  cero errores. No se cambió por una fecha de ejecución original.
- Las dos C positivas completas del archivo coinciden con sus filas vivas:
  C-2821, `636e5a351e081de1a81b5719a3e76f8d3800a9d13427ccddc1a60d47eda20707`;
  C-2822, `a1c93f9a6dffa29487104c46f48a94697402cd2e1b965d10694f9e4913aa238a`.
  Su apoyo primario se cotejó en `cotejo_parche_s434_2026-09-26.csv`, no se
  deduce de la decisión de retirar BN-120.

Los SHA de filas de este informe usan JSON de la fila completa, claves
ordenadas, UTF-8, separadores compactos y LF; no son una firma QUOTE_ALL del
censo semántico ni deben copiarse a otro contrato de huella.

## Delta de código y pruebas

Código revisado: `scripts/remediate_trace_residuals.py`, SHA
`4334b061dce47722c32dc233de6557a8954bbe1e62165083e43870d0d58cfc4d`.
Al revertir **solo en memoria** el comentario nominal BN-120, el cambio de
499/487/12 a 498/486/12, `RETIRED_BN_KEYS` y su comprobación, se obtiene
exactamente el SHA anterior revisado:
`43855566ac6b29fd1e9b7dd98da500e07d1c2e4d68a50e2ff8d64d33e6db8b4d`.
Por tanto, este delta no cambió universo, consultas, normalización, índice,
410 residuales, dos positivos ni identidades de las 408 negativas v3.

La restricción nominal nueva impide reintroducir BN-120 aunque se compense
con otra baja, además de los controles existentes de cuentas/duplicados.
No se añadió estado BN ni excepción de evidencia científica.

Tests revisados: `tests/test_remediate_trace_residuals.py`, SHA
`57228b7d854cc862dd7bf1ee1d5e5aaaae2f7d259b0b5bbdc4ddc618be16797d`.
Ejecuté `python3 -m unittest tests.test_remediate_trace_residuals -v`:
**12 pruebas aprobadas**, salida 0. Incluyen conservación histórica,
reintroducción simple de BN-120, baja de otra BN y reintroducción compensada;
se mantienen rechazo de pérdida de BN-557, control 410/408 y pruebas de
equivalencia de coocurrencia literal. No se ejecutó una nueva campaña de 408
consultas como parte de este cotejo: las filas se preservaron literalmente.

## Recuentos y dependencia de C-1990

El registro vivo tiene **498/486/12**. C-1931/C-1933, sus F y la prosa 15
reflejan esas cuentas después del remediator. Huellas JSON observadas:

- C-1931: `0a745de3f90219efeaf8b1d8c0a3bf7672d93940ae6c005ca0cdf1d2ae853a53`.
- C-1933: `5406545c73ff4815deff2674aa44b064aa1758f35a0f671b081301a3d8653644`.
- C-1990: `68e114ca61ad08c9fea9f85b2519189a02011475f0329cc2173ac6f28e97dad9`.
- C-2784: `e0b620c97f78aba950f63163be3c7a8cf5560b3d70e52dbcbb3c6140804ffa88`.

C-1990 describe ahora dos resultados registrados de BN-121/122, con glosa,
fuerza desconocida y límite explícito de búsqueda. No afirma inexistencia
universal ni conserva el hueco resuelto de Sphaeroforma. C-2784 conserva su
literal de apusomonádidos y propaga la fuerza desconocida de la dependencia.
Esto es conformidad del delta de atribución/preservación, **no** aprobación
científica íntegra de BN-121/122 o de toda C-2784.

## Derivados y límites pendientes

La construcción de Q realizada en memoria da 606 filas, ninguna negativa
vigente de BN-120; las anclas originales de 165 Q y 106 BN no cambian. El Q
en disco conserva aún el registro anterior a la regeneración. No lo certifico
como actualizado. Tampoco se certifican H, exports, matriz de requisitos,
revisiones globales ni los inventarios de fuentes por adelantado.

Después de la escritura del remediator volví a ejecutar, sin mutación:

- `python3 scripts/audit_semantics.py`: salida 0, auditoría correcta.
- `python3 scripts/build_atomic_cell_claims.py`: salida 0, 816 C exactas.
- `git diff --check`: salida 0.

No ejecuté `make verify` completo ni aislado. La integración de los SI de
S434 y la regeneración/cotejo de derivados siguen pendientes fuera de este
dictamen nominal. El archivo de autor queda intacto con su marcador de revisión
pendiente; este informe ajeno registra el resultado sin autoeditar esa firma.
