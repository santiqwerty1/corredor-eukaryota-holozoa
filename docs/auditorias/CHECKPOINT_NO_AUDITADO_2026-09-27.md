# Checkpoint de ensayo: no auditado

Solicitado por el usuario para ensayar la absorción desde el proyecto
eslabón-perdido, cuya base es `af7e799`. Preparado desde el árbol de trabajo de
`codex/cierre-plan-pendiente`, con HEAD previo
`0f155364dc30e6344e1575b10d2c50703afb7ce6`.

Este snapshot no es una publicación auditada, no autoriza ingestión final y
no declara que `make verify` pase. Conserva cambios parciales, propuestas,
rechazos y revisiones pendientes. En particular, el constructor de C atómicas
incluye la reparación autoral 6a357a08 y sus dos no conformidades independientes
todavía sin reparar. Los tests del autor no constituyen conformidad global.

Los revisores confirmaron puntos estables y suspendieron sus escrituras para
capturar el checkpoint. El snapshot Git incluye los archivos versionables del
workspace, no los artefactos ignorados de `fuentes/` ni los archivos temporales
de `/tmp`. Hay propuestas que apuntan a esas evidencias locales; una copia Git
sola no permite reproducir toda la auditoría científica.

Los consumidores de ensayo deben usar `data/afirmaciones/` y los CSV canónicos
con la identidad de este commit. Los informes, exportaciones y manifest pueden
estar desactualizados: se conservan como estaban, sin disimular el estado de
trabajo mediante una regeneración parcial.

Respecto de `af7e799`, `data/afirmaciones/05.csv` no cambia. En
`data/afirmaciones/06.csv` cambian C-785, C-787 y C-789–C-792, sin altas, bajas
ni cambio de sus IDs. El rango vivo de sección 5 es C-694–C-756; sección 6 es
C-757–C-792. El censo integral no ha terminado, por lo que el contenido no
está congelado para la entrega final.

Se incorpora el CSV solicitado de sucesiones con el antecedente ya materializado
C-681. La autorización nueva para C-1581 está documentada, pero su partición aún
no se ha aplicado en este checkpoint. Los IDs canónicos se mantienen estables
en este cierre según `PROTOCOLO_SUCESIONES_AFIRMACIONES.md`.
