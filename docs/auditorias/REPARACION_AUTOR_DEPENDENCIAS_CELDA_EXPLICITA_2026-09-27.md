# Dependencias de una celda corregida con C explícitas

Autor: `/root`. Observación UTC: 2026-09-27T04:16:10Z. Estado: reparación
autoral pendiente de revisión técnica independiente. Rama
`codex/cierre-plan-pendiente`. No integra ninguna corrección científica.

## Defecto y alcance

La revisión independiente del lote S10 detectó diez C atómicas no residuales
cuya representación prospectiva heredaba referencias anteriores y de toda la
fila. C2606 retenía C1983 y BN115 pese a describir ahora el alcance positivo de
una PP. La generación mecánica no prueba que esas dependencias sostengan la
celda. La propuesta S10 v2 y sus errores se conservan, sin retocar sus hashes.

El constructor ya distingue las disposiciones residuales aprobadas. Esta
reparación añade un caso delimitado: cuando existe una corrección autoral
ligada al objetivo previo y su valor nuevo escribe C explícitas, la síntesis
usa exclusivamente esas C. No incorpora las candidatas del objetivo rechazado
ni la bibliografía general de fila. Conserva una BN escrita en la celda nueva,
pero no añade una BN tomada sólo de la fila. Rechaza autocitas y rangos C
invertidos en las correcciones; una C de apoyo ausente sigue bloqueando.

No se cambian el registro de disposiciones residuales, el contrato de revisión
ajena, los objetivos históricos ni las correcciones existentes. Las quince
correcciones actuales no escriben C propias y conservan su comportamiento.
Los objetivos no corregidos tampoco cambian. Sus referencias candidatas no
reciben por ello aprobación científica: quedan sujetos al censo integral.

Una corrección con C escritas no se declara conforme por esta regla. El
constructor sólo materializa su atribución como síntesis. Su significado,
cobertura, fuentes, estados y dependencias siguen necesitando las revisiones
nominales correspondientes. Para las celdas residuales sigue siendo obligatoria
la disposición independiente exacta, sin posibilidad de eludirla añadiendo C.
Las diez celdas S10 aún necesitan propuestas nuevas con soportes propios y
revisión; esta edición de código no las modifica ni las aprueba.

## Versión entregada y pruebas del autor

- `scripts/build_atomic_cell_claims.py`: SHA256
  `6a357a08f93918254f25b2381cb6c9e18fa520838bd33a3d56f37a74e51ba5e9`.
- `tests/test_build_atomic_cell_claims.py`: SHA256
  `4ea9e78be209811100d32d02e887f91f1a19a14a22a7900e5378705a41b6de27`.

Las 49 pruebas de constructor atómico, disposiciones y remediador pasaron en
7.018 s. Nueve pruebas nuevas comprueban referencias propias, cobertura de
rangos y fuerza mínima, conservación de BN propia, invariancia del caso sin
referencias propias y de objetivos sin corregir, camino residual previo,
dependencia inexistente, autocita y rango inverso. Son fixtures ficticias,
no firmas de datos reales. La verificación del constructor vivo y la suite
global se ejecutan por separado; ningún resultado de autor sustituye la
reinspección adversaria ni el cierre de `make verify`.

No se regeneraron canon, mapeo ni derivados con `--write`. La reparación
requiere revisión independiente antes de utilizarse para materializar el lote.
