# Addendum: normalización LF del índice de acceso

Inspección: 2026-09-26T22:06:34Z. Revisor: /root/verificacion_fuentes_nuevas.

CONFORME para el delta posterior al addendum de S551 y recuentos. No modifica
ni sustituye aquella evidencia: registra los hashes de esta nueva serialización.

Se comprobó que el export vivo no contiene CR. Reintroducir CR antes de cada
LF reproduce exactamente el SHA-256 del export inspeccionado anteriormente
(`bda2508d0aa38cb87b260175b99af1047eedbd832ef2014ccbc999554b038f86`). Además,
las huellas JSON de las 524 filas coinciden una a una con el CSV nominal de
revisión anterior. Por tanto, se preservan todas las celdas y los recuentos.

En scripts/fetch_oa.py, retirar únicamente `lineterminator="\n"` de la llamada
a csv.writer de volcar reproduce el hash previo del script. En el archivo de
pruebas, retirar únicamente el nuevo método de LF reproduce su hash anterior.
Se ejecutó `python3 -m unittest tests.test_fetch_oa_impact -v`: 4/4 pruebas
correctas, incluida la escritura y relectura de Unicode y coma. Se ejecutó
`git diff --check`: salida vacía y código 0.

SHA-256 actuales:

- exports/acceso_fuentes.csv: `d4e7a96054e7a3787afa48b6fd1a116d593716de5048b7fb36f93b983bb9e274`.
- scripts/fetch_oa.py: `64d20a0e787732e90a5aec273c8680a994afcd86bfb60e11a9921dbce54f3e42`.
- tests/test_fetch_oa_impact.py: `270d1d1fddf9b39aba853e09dcfcb69f6fe208197590e458e458cbc626083ecb`.

Solo revisé la serialización y el delta de prueba; no se amplía el dictamen
científico, la identidad de fuentes o el alcance de las revisiones anteriores.
No modifiqué export, script, pruebas ni evidencia previa.
