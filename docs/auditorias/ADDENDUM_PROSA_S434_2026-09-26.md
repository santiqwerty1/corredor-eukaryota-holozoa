# Addendum de prosa S434: separación de dos oraciones

Revisor: `/root/verificacion_fuentes_nuevas`.
Observación: 2026-09-26T22:49:37Z. No edité la prosa canónica.

**CONFORME para esta división de párrafos y sus citas locales.** Conserva el
dictamen anterior sobre el contenido científico; no reescribe su evidencia.

En `docs/secciones/013-12-12-multicelularidad-y-el-repertorio-preanimal.md`,
el párrafo anterior `PROSA12:2` de
`evidencia_cotejo_parche_s434_2026-09-26.json` se convirtió en dos:

- L211, comienza «Su análisis probabilístico de intrones con Malin».
  SHA JSON de `{"parrafo": texto_completo}`:
  `2ea1ed735a34c97008746b9d8b74560bbeae8fd2edca7a3bff171c22e7a7a1fc`.
- L213, comienza «Es una estimación del modelo comparativo».
  SHA JSON del mismo formato:
  `c1d4bf7cbc23ecaa4c806f8f32d327356b9a81f6988b5266c99f088ce64add71`.

Se comprobó mediante aserción que concatenar los dos textos, retirar solo
las citas entre corchetes y colapsar blancos reproduce exactamente la prosa
científica anterior. Ambos párrafos citan C-2822 y S434 con los mismos
localizadores. Se conserva la densidad modelada y la advertencia de que no es
un promedio observado sobre todos los genes. No cambiaron C, F ni tabla por
este ajuste.

SHA del archivo completo observado:
`78a806f8868d18191775e0a8a36ddb4cc0b281fb7ec11a84d0c4a73308276749`.
Las huellas JSON usan claves ordenadas, UTF-8, separadores compactos y LF.
Un cambio futuro de texto necesita otro cotejo; no se traslada esta conformidad
a un archivo posterior ni al cierre global de trazabilidad.
