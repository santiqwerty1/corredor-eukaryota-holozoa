# Corredor Eukaryota → Holozoa

Corpus de investigación en español sobre el corredor evolutivo comprendido entre el tallo de Eukaryota y el nodo que reúne coanoflagelados y animales, con énfasis en ecología, mecanismos, magnitudes y procedencia probatoria.

**Fecha de corte bibliográfico actual:** 8 de agosto de 2026.

**Versión del corpus:** `0.6.0-research-audit`.

**Estado:** encargo completo. Los huecos científicos permanecen identificados con las etiquetas probatorias exigidas.

## Arquitectura

El repositorio separa deliberadamente las dos capas del corpus:

- `docs/secciones/`: narrativa editable, dividida por secciones y con marcadores de tabla.
- `data/`: CSV canónicos. Los registros y apéndices se editan aquí.
- `docs/informe.md`: versión de lectura; mantiene tablas de síntesis y enlaza los registros grandes.
- `docs/informe_completo_autocontenido.md`: versión generada que reincorpora todas las tablas Markdown exigidas por el encargo.
- `exports/`: CSV combinados para análisis, importación o auditoría.
- `scripts/`: renderizado, validación y renumeración.
- `docs/auditorias/`: entregables reproducibles de revisión y trazabilidad.
- `archive/`: instantánea previa a la migración; no es fuente de verdad.

Los CSV permiten procesar el corpus sin extraer tablas de un archivo Markdown de más de un megabyte. La versión autocontenida conserva el formato literal solicitado en el encargo.

## Archivos principales

| ruta | función |
| --- | --- |
| `docs/C01-PROMPT-INVESTIGACION.md` | encargo original |
| `docs/informe.md` | informe legible |
| `docs/informe_completo_autocontenido.md` | informe completo generado |
| `data/afirmaciones/` | registros por sección con las 12 columnas obligatorias |
| `data/apendices/` | apéndices A–H |
| `data/busquedas_negativas/` | búsquedas negativas por bloque |
| `data/tablas/` | tablas de síntesis y tablas nodales |
| `exports/afirmaciones.csv` | registro global combinado |
| `exports/busquedas_negativas.csv` | búsquedas negativas normalizadas |
| `exports/tablas_nodales.csv` | tablas nodales consolidadas |
| `manifest.json` | inventario, recuentos y SHA-256 |
| `data/table_index.json` | relación entre marcadores Markdown y CSV |
| [`docs/auditorias/`](docs/auditorias/) | matrices e informe de la auditoría de cierre |

## Flujo de edición

1. Modificar la prosa en `docs/secciones/`.
2. Modificar filas en el CSV canónico correspondiente.
3. Regenerar:
   ```bash
   python3 scripts/render.py
   ```
4. Validar:
   ```bash
   python3 scripts/validate.py
   ```
5. Cuando se inserten afirmaciones en una sección intermedia:
   ```bash
   python3 scripts/renumber.py
   ```

También están disponibles:

```bash
make render
make validate
make verify
make check
```

`make verify` es la puerta única usada en local, CI y antes de publicar: comprueba
renderizado, exportaciones, estructura, reconstrucción histórica, reglas
semánticas, matrices de la auditoría científica, linaje de tablas, anclas y
pruebas de mutación. También repite la puerta en una copia aislada y exige dos
renderizados consecutivos idénticos. `make check` es un alias de esa misma puerta.

## Reglas importantes

- No editar manualmente `docs/informe.md`, `docs/informe_completo_autocontenido.md`, `exports/` ni `manifest.json`.
- No dejar celdas vacías; usar `n/a`, `sin localizar` o el marcador requerido.
- Conservar valores, unidades e incertidumbres tal como aparecen en la fuente.
- No promediar estudios discordantes.
- Toda afirmación narrativa sustantiva debe tener una fila en `data/afirmaciones/`.
- Los identificadores `C-…`, `S…`, `E…`, `H…` y `BN-…` se validan en CI.

## Publicación inicial sugerida

Repositorio privado recomendado:

```text
santiqwerty1/corredor-eukaryota-holozoa
```

Desde una copia local con GitHub CLI autenticada:

```bash
./scripts/publish_github.sh
```

El script valida el corpus, crea el repositorio privado si no existe y publica `main`.

## Estado y límites científicos

El cierre y los recuentos están en [`docs/STATUS.md`](docs/STATUS.md). Los
entregables reproducibles están en [`docs/auditorias/`](docs/auditorias/) y las
instrucciones de publicación en
[`docs/GITHUB_SETUP.md`](docs/GITHUB_SETUP.md). Los huecos que la literatura o
la búsqueda no permiten resolver son resultados explícitos del corpus, no fases
de redacción pendientes.
