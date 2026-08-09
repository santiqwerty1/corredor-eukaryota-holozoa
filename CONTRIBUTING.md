# Contribución al corpus

## Principio general

La unidad de trabajo es una afirmación con evidencia. La narrativa explica; los CSV registran.

## Antes de editar

1. Leer `docs/C01-PROMPT-INVESTIGACION.md`.
2. Leer `README_DATOS.md`.
3. Verificar el estado en `docs/STATUS.md`.

## Añadir o modificar una afirmación

1. Editar el CSV de `data/afirmaciones/` correspondiente a la sección.
2. Mantener las doce columnas exactas.
3. Añadir o actualizar la prosa en `docs/secciones/`.
4. Añadir la fuente, entidad, evento, fecha, hipótesis o magnitud a su apéndice cuando corresponda.
5. Ejecutar:
   ```bash
   python3 scripts/renumber.py
   ```
   si cambió el orden global.
6. Regenerar y ejecutar la puerta de calidad completa:
   ```bash
   python3 scripts/render.py
   make verify
   ```

## Fuentes

- No reconstruir DOI.
- Conservar localizadores exactos.
- Marcar preprints y recursos secundarios.
- No declarar consenso amplio sobre una fuente no revisada.
- No reemplazar un hueco por una estimación propia.

## Pull requests

Cada PR debe indicar:

- secciones afectadas;
- afirmaciones nuevas, modificadas o retiradas;
- fuentes añadidas;
- búsquedas negativas cerradas o creadas;
- resultados de validación;
- si hubo renumeración global.

No mezclar una ampliación científica grande con una refactorización masiva de esquemas, salvo que sea imprescindible para preservar coherencia.
