# Contrato de cronología declarada del cierre

Este contrato separa el corte bibliográfico y los inventarios históricos de
las fechas reales de nuevas inspecciones. No cambia el corte 2026-08-08, las
fechas de consulta de A ni las 165 búsquedas Q congeladas y sus huellas.
2026-08-13 es el inicio documentado del cierre, no una fecha que el generador
pueda atribuir a una revisión posterior.

## Qué valida y qué no valida

`scripts/audit_chronology.py` acepta únicamente días `YYYY-MM-DD` e instantes
UTC `YYYY-MM-DDTHH:MM:SSZ` con calendario y hora válidos. No consulta el reloj,
la red, mtime ni las fechas de commits. Las firmas de control manual y de
segunda revisión no pueden ser anteriores al inicio del cierre. Permanecen
obligatorios los requisitos existentes de evidencia, independencia, literal,
alcance y huellas del corpus vivo.

Cuando hay un antecedente temporal documentado para la versión exacta, la
firma debe ser igual o posterior. Una firma expresada solo como día no
demuestra posterioridad a una versión horaria del mismo día: en ese caso se
requiere un instante UTC o un día posterior. La segunda revisión de una fuente
también respeta su fecha de verificación registrada; la de un requisito, la
fecha de su dictamen manual si existe.

La coherencia temporal y una huella **no prueban autenticidad**, ejecución real,
independencia ni apoyo científico. Sin reloj externo no se certifica que una
fecha declarada no sea futura: las fechas deben corresponder a observaciones
reales y la evidencia se inspecciona independientemente. La ausencia de un
antecedente de versión no se interpreta como conocimiento de cuándo se creó.

## Fechas de objetos revisados

El registro opcional `data/auditoria/fechas_objetos_revision.csv` tiene esta
cabecera exacta:

```csv
estrato,clave_objeto,huella_objeto_sha256,fecha_version,evidencia_local,huella_evidencia_sha256,localizador_evidencia
```

Una fila declara la fecha observada para una versión exacta; no constituye una
aprobación. Los estratos son `CONTROL_MANUAL`, `AFIRMACION`, `FUENTE`,
`REQUISITO`, `TRAZABILIDAD_PROSA`, `TRAZABILIDAD_ARISTA`,
`TRAZABILIDAD_CELDA` y `VERIFICACION_FUENTE`. En `CONTROL_MANUAL`, la clave es
R-XXXX y la huella es `huella_alcance_sha256`; el literal se valida aparte.
En los seis estratos de segunda revisión, clave y huella son las de la fila
de revisión. `VERIFICACION_FUENTE` usa la clave S y `source_fingerprint` de
la fila canónica A, y registra la fecha de la verificación, no de publicación
ni de consulta bibliográfica.

Para una S nueva, `build_audit_deliverables.py` solo publica la fecha de
verificación si existe este registro con la huella exacta. Sin él publica
`FECHA_NO_DOCUMENTADA` y `audit_full.py` bloquea con AF514. No hereda el corte
bibliográfico ni la fecha de un derivado como prueba de ejecución. Las fechas
de las S del inventario congelado se conservan literalmente para no alterar
su procedencia histórica.

## Ejecuciones de búsquedas BN

`data/auditoria/fechas_ejecuciones_bn.csv` tiene esta cabecera exacta:

```csv
clave_bn,huella_fila_bn_sha256,clase_fecha,fecha_ejecucion,evidencia_local,huella_evidencia_sha256,localizador_evidencia
```

`clase_fecha` solo admite `EJECUCION_ORIGINAL` o `REINSPECCION`. Una reinspección
no acredita la fecha original, aunque repita los términos y obtenga el mismo
resultado. Una reinspección documentada de una BN histórica produce una Q
posterior separada, conservando la prioridad histórica. Las Q históricas no se
reescriben. La reinspección no puede ser anterior a su Q original congelada;
el builder rechaza esa contradicción y el auditor también la detecta. Las
altas BN posteriores toman
la fecha y clase de este registro únicamente si corresponde a su huella viva.
Si no existe evidencia de fecha, el builder publica `FECHA_NO_DOCUMENTADA`
y el auditor bloquea con AF613. La fecha que antes generaba automáticamente
el builder nunca sirve de evidencia para rellenar este registro.

La huella BN es SHA-256 del JSON de la fila completa, con claves ordenadas,
`ensure_ascii=False`, separadores `,` y `:`, y un LF final; es la misma
serialización que `build_audit_deliverables.row_fingerprint`. Cambiar términos,
resultado o cualquier otro campo exige una nueva ligadura explícita; una
ejecución anterior no se transfiere automáticamente a la nueva versión.

## Cómo registrar una observación posterior

1. Ejecutar realmente la inspección o consulta y conservar su alcance, método,
   resultado, objeto/huella e instante observado en un artefacto local durable.
   No inventar una hora para una observación de la que solo se conserva el día.
2. Calcular la huella del objeto y del artefacto de evidencia. Registrar su ruta
   relativa y un localizador nominal en uno de los CSV anteriores. El registro
   debe ser declarado por quien puede documentar la ejecución, no por el
   generador de matrices. No rellenar fechas de filas antiguas por analogía.
3. Mantener `REINSPECCION` cuando eso es lo que se hizo. La fecha de una nueva
   consulta no resuelve la fecha original desconocida.
4. Regenerar los derivados y encargar su revisión independiente. La presencia
   del registro no cierra automáticamente una revisión científica ni manual.

Los registros rechazan cabeceras y cardinalidades inválidas, duplicados de
identidad/huella, fechas imposibles, archivos externos, evidencia inexistente o
con SHA incorrecto y localizadores genéricos. No se permite usar como prueba de
fecha estos registros, el Q derivado o la matriz de fuentes derivada: sería
procedencia circular. Si un registro es inválido, ninguna de sus fechas se
presta a los derivados.

## Ensamblado de dictámenes manuales

`assemble_manual_review_ledger.py` conserva los doce campos firmados. Compara
sus huellas con el corpus vivo y rechaza una firma obsoleta: no recalcula una
huella para volver a firmar un objeto cambiado, no fija la fecha y no declara
independencia por el revisor. El formato histórico de seis columnas solo se
admite para conservar un `NO_CONFORME`, nunca para cerrar. Un `CONFORME` exige
el esquema completo con fecha, literal, alcance, huellas e independencia
declarados por su revisor. El orden de archivos no puede contradecir las fechas
de firma conocidas. Una conformidad anterior no puede sustituirse en silencio.

## Incidencia de alcance separada

La inspección de formato identificó que los alcances firmables de R-0404 y
R-0448 no incluían toda la narrativa y salida pertinentes. El autor principal
implementó un refuerzo nominal de alcance por separado, sujeto a revisión
independiente de formato y no incluido en el dictamen temporal. La corrección
de fechas no considera cerrados esos controles ni transfiere las firmas
anteriores al alcance ampliado.
