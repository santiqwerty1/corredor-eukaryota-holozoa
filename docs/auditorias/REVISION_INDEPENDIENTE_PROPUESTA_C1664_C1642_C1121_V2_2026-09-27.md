# Reinspección independiente de C1664/C1642/C1121 — v2

Revisor: `/root/revision_residuales/candidatos_editoriales`. Captura propia: 2026-09-27T02:50:37Z. Dictámenes: 2026-09-27T02:52:10Z. Rama comprobada: `codex/cierre-plan-pendiente`.

Propuesta exacta: `PROPUESTA_REPARACION_C1664_C1642_C1121_V2_2026-09-27.json`, SHA256 `9cf84c0123fdcaf9fc25f37f5ad7990891c828c086900c4722ceb0b37075fdbc`. No se modificaron propuesta, canónicos ni firmas. La revisión v1 y sus rechazos permanecen intactos. Las conclusiones siguientes provienen de una nueva lectura de los objetos y pasajes, no de heredar dictámenes v1.

## Resultado

El paquete v2 sigue **NO_CONFORME** por dos defectos nominales. El CSV contiene 31 dictámenes: 26 conformidades de objetos dentro del alcance leído, dos conformidades sólo del delta editorial y tres NC (dos defectos y el paquete). Ninguna de estas filas aprueba el corpus, los 210 controles o el cierre de §16.

1. **F_altas[2], umbral >0.5**: P60 de S513 declara una regla de clasificación de nodos, no una estimación del valor del corte. La fila propuesta lo llama correctamente «umbral operacional», pero lo etiqueta `inferido`. Son las probabilidades/estados nodales y los orígenes los que se infieren; no ese umbral elegido. Debe representarse como parámetro metodológico declarado sin atribuirle una estimación empírica. Este dictamen no exige cambiar vocabularios ni retirar el valor de la documentación.
2. **Completitud de B**: las seis altas propuestas son correctas individualmente, pero no incluyen BPMM, MR-BPMM, MCMCglmm ni mapas estocásticos de caracteres/SCM. Los métodos aparecen nominalmente en las C/F propuestas; §17 B exige registrar métodos. Las búsquedas por siglas y variantes de nombres en etiquetas/sinónimos del B vivo tampoco recuperaron entidades correspondientes. Es un faltante nominal, no una declaración de exhaustividad sobre todas las entidades del corpus.

Estos defectos no convierten en falsas las correcciones científicas conformes y no obligan a paralizar otros componentes independientes. S517 todavía reside en `/tmp`; aprobar su lectura no afirma que ya esté integrado en `fuentes/`, ni sustituye el censo de acceso/procedencia o la regeneración de derivados.

## Lectura primaria y objetos conformes

**S517**: copia de autores, 5 páginas, DOI 10.1098/rsbl.2016.0324, título y autores leídos en p.1. SHA256 `61955ee69452e0303df9d90382515529529cefeb3513141d485f926711d5a247`. Releídos Methods y Results completos de p.2. C1664 y F de 223 preservan la definición: Animalia en ambos papeles consumidor y presa/huésped, único individuo huésped durante al menos una fase vital. El mínimo de orígenes procede de reconstrucción bibliográfica/filogenética; no es un censo de transferencias ni una frecuencia pan-eucariota. C2879 y F de 15 registran presencia por filo, no otro número de orígenes. Abstract y segundo párrafo de Results dicen 15; un párrafo posterior del análisis de diversidad dice nueve de 14 filos. Se conserva esta diferencia interna, sin armonizarla ni transferir el denominador del análisis de diversidad al recuento de orígenes. No se replicaron datos de Dryad ni se adjudicaron todas las figuras. La metadata autoral «figura3» es imprecisa: no se empleó como evidencia.

**S513**: XML local SHA256 `97c37c51e5148821ade14fbab6cdf1c873aaad82b02bcd6e30d69c3944b8e040`. Releídos P1/P5/P7/P12/P35–37/P53/P54/P60/P61/P65, con texto íntegro y huellas en la captura independiente. P5 explicita 1.850 combinaciones microbio–insecto y 402 familias; P7 los 16 orígenes mínimos y 89 familias. P35–37 aclaran criterios operacionales de dependencia, no verificación experimental de todos los casos. P60/P61 distinguen inferencia BPMM y contraste SCM; no se confunden estados inferidos con observaciones ancestrales. C2883 conserva la negación condicional original: la falta de filogenias de especies impide resolver todos los orígenes dentro de familias mixtas, no demuestra una imposibilidad general.

Para C1121 y sus F, P12 publica correlación filogenética −0.32, intervalo creíble −0.54 a −0.09 y pMCMC 0.006; P53 declara modos posteriores e intervalos del 95 %, y P65 identifica MR-BPMM y la unidad familiar. La lectura conjunta sustenta **intervalo creíble del 95 %**, no un intervalo de confianza frecuentista de las ilustraciones ni una correlación de Pearson. Se conservan cifras originales, unidades, incertidumbre, escala y cautela frente a causalidad universal.

**C1642/BN111 y C2882/BN113**: cotejo del registro vivo, respectivamente filas CSV 10 y 11 de `15_5_15-5-asociacion-integracion-y-transferencia.csv`. Las nuevas glosas describen el resultado registrado, no inexistencia biológica o bibliográfica. No se certifica aquí la ejecución original, la fecha de búsqueda ni la exhaustividad de la literatura.

Las tablas 55d/44 y la prosa de líneas 165/383 reflejan esos objetos con localizadores, sin convertir los recuentos parciales en denominadores universales. La tabla comparativa puede agrupar resultados que ahora tienen proposiciones separadas en C. Las seis altas B son nominalmente correctas y no tienen duplicado literal vivo; ello no subsana la falta de los cuatro métodos.

## Límites y precondiciones comprobados

- Los cuatro objetos C anteriores, las dos F sustituidas, ambas filas de tablas y las tres líneas de prosa coinciden exactamente con el estado vivo leído. Coinciden todos los hashes de filas/pasajes declarados por el autor. La comparación es por objeto, no una aprobación de los archivos completos.
- C2879–C2883 todavía no existen en el canon; su destino es `15.csv`. El máximo vivo es C2838. El integrador debe respetar las reservas del lote precedente y no crear discontinuidades o colisiones; no se ha validado una integración aún inexistente.
- **C1665**: sólo se aprueba el cambio de referencias en Motivo. Su proposición S460, aceptación/fuerza/resolución y localizador siguen fuera de esta revisión.
- **Prosa182**: sólo se aprueba el delta de referencias de los resultados separados. La proposición de multicelularidad no recibe aprobación por arrastre.
- **C1201**: no adjudicada. El uso de C1121 como correlato acotado no prueba una tesis universal de ausencia de predictor; las referencias preexistentes a C1201 no se convierten en aprobación de esa fila.
- No se ejecutaron tests del autor para decidir ciencia, no se firmaron controles globales y no se afirma `make verify` ni aislamiento/idempotencia desde este lote.

## Evidencia reproducible

`evidencia_revision_independiente_c1664_c1642_c1121_v2_2026-09-27.json` contiene 29 objetos propuestos completos, punteros JSON, SHA256 de cada objeto, contraste de anteriores vivos, fuentes/pasajes y registros BN. `dictamenes_independientes_propuesta_c1664_c1642_c1121_v2_2026-09-27.csv` contiene los 31 dictámenes nominales. La captura se obtiene con el probe propio de sólo lectura `probe_revision_c1664_c1642_c1121_v2_2026-09-27.py`; su salida automática no sustituye las adjudicaciones de lectura.

Normalización de objeto JSON: UTF-8, `ensure_ascii=False`, claves ordenadas, separadores compactos y LF final. Prosa: texto literal UTF-8 más LF. Pasajes XML: `itertext`, blancos simples, LF final. Esta normalización no se presenta como el hash canónico CSV de otros contratos.
