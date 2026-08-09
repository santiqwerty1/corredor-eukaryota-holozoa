# Guía de los datos

## 1. Convenciones de serialización

- Codificación: UTF-8.
- Separador: coma.
- Todos los campos se escriben entre comillas.
- Final de línea: `LF`.
- Los identificadores se tratan como texto.
- No se permiten celdas vacías.
- Los campos pueden conservar Markdown en línea cuando es necesario para regenerar el informe.
- Las cifras se conservan como texto para no perder intervalos, signos, incertidumbres ni unidades originales.

## 2. Fuente de verdad

Los archivos de `data/` son canónicos. Los archivos de `exports/` son derivados y se regeneran con `python3 scripts/render.py`.

### 2.1. Afirmaciones

Cada archivo de `data/afirmaciones/` contiene exactamente:

```text
# · Afirmación · Sujeto · Predicado · Objeto · Atribución · Fuente · Aceptación · Fuerza · Motivo · Resolución · Vigencia
```

El número del archivo identifica la sección. No se añade una columna `sección`, porque el encargo fija el orden exacto de columnas.

### 2.2. Apéndices

- `A_fuentes.csv`
- `B_entidades.csv`
- `C_eventos.csv`
- `D_fechas.csv`
- `E_hipotesis.csv`
- `F_magnitudes.csv`
- `G_material_no_encajado.csv`
- `H_recuento_control.csv`

Las columnas proceden del encargo original. `H_recuento_control.csv` se actualiza automáticamente para los recuentos derivados.

### 2.3. Búsquedas negativas

Los bloques originales conservan su esquema en `data/busquedas_negativas/`.  
`exports/busquedas_negativas.csv` ofrece además una vista normalizada con:

```text
clave · sección · estado · hueco · términos exactos o motivo · resultado o motivo · filas relacionadas
```

La auditoría del 2026-08-08 conserva la disposición y la evidencia de las 106
claves presentes antes de la revisión, incluidas las que luego fueron resueltas,
fusionadas o retiradas por alcance. La síntesis está en la
[revisión de búsquedas negativas](docs/auditorias/REVISION-BUSQUEDAS-NEGATIVAS-2026-08-08.md)
y el detalle fila por fila en su
[matriz CSV](docs/auditorias/revision_busquedas_negativas_2026-08-08.csv). La
[matriz de trazabilidad del contenido](docs/auditorias/matriz_trazabilidad_contenido_2026-08-08.csv)
y el
[mapa de claves](docs/auditorias/mapa_claves_inicial_final_2026-08-08.csv)
completan los entregables reproducibles de cierre.

### 2.4. Tablas de síntesis

Cada tabla narrativa tiene su propio CSV en `data/tablas/`. El índice `data/table_index.json` registra:

- identificador del marcador;
- ruta del CSV;
- contexto jerárquico;
- número de filas y columnas;
- líneas de procedencia en el maestro v5;
- política de renderizado en la versión de lectura.

## 3. Identificadores

La migración normalizó `C-0001…C-0999` a `C-001…C-999`. Desde `C-1000`, el identificador se conserva sin relleno adicional.

- Afirmaciones: `C-001…`
- Fuentes: `S01…`
- Eventos: `E01…`
- Hipótesis: `H01…`
- Búsquedas negativas: `BN-001…`

Al insertar filas en una sección intermedia, ejecutar `python3 scripts/renumber.py`.

## 4. Valores cerrados

### Atribución

- `expresa`
- `sintesis(C-...)`
- `glosa`

### Aceptación

- `consenso amplio`
- `aceptación mayoritaria`
- `aceptación mixta`
- `posición minoritaria`
- `no evaluado`

### Fuerza

- `alta`
- `media`
- `baja`
- `desconocida`

### Resolución

- `resuelta`
- `parcialmente resuelta`
- `sin resolver`
- `información insuficiente`

### Vigencia

- `vigente`
- `histórica`
- `superada`
- `rechazada`

### Estado de huecos

- `LA LITERATURA DECLARA QUE NO SE SABE`
- `NO LOCALIZADO EN ESTA SESIÓN`
- `NO BUSCADO`

## 5. Regeneración y control

```bash
python3 scripts/render.py
make verify
```

`make verify` ejecuta la puerta determinista completa sin modificar archivos;
`make check` es un alias. Incluye la reconstrucción histórica de las tablas
heredadas, la auditoría científica integral, el linaje de todas las tablas y las
pruebas de mutación. La misma orden repite la puerta en una copia aislada y
comprueba la identidad de dos renderizados consecutivos.

La validación comprueba, entre otras cosas:

- secuencia y unicidad de afirmaciones;
- referencias internas;
- vocabularios cerrados;
- celdas vacías;
- dimensiones de tablas;
- duplicados bibliográficos;
- dependencias de síntesis;
- sincronización de informes, exportaciones y manifest.
- densidad mínima de dos fuentes resueltas por subapartado científico de nivel 2;
- localizadores, referencias cruzadas, magnitudes y marcadores de cierre final.
