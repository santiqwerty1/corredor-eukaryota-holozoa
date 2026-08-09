# Migración de Markdown a CSV

## Alcance

La migración parte de:

```text
archive/maestro_provisional_v5_pre_migracion.md
```

SHA-256 de la instantánea original:

```text
24c5495d85641d03a24c084a51a9b0b5887edf60d6698f94f19775c09c28cfe3
```

El contenido científico no se reinterpretó durante la extracción. Las tablas se identificaron por sintaxis Markdown, se trasladaron a CSV y se sustituyeron en las plantillas por marcadores `<!-- TABLE:... -->`.

## Cambios estructurales

- 78 tablas extraídas.
- Registros de afirmaciones separados por sección.
- Apéndices A–H separados.
- Búsquedas negativas separadas por bloque.
- Tablas de síntesis conservadas como CSV individuales.
- Informes legible y autocontenido generados desde una única capa canónica.
- Secciones narrativas divididas en archivos pequeños para facilitar revisión y diffs.

## Cambio de identificadores

La integración previa usaba cuatro dígitos con cero inicial para las primeras 999 afirmaciones:

```text
C-0001 … C-0999
```

El repositorio normalizó esas claves al formato solicitado:

```text
C-001 … C-999
```

`C-1000` y posteriores permanecen sin cambios. Todas las referencias narrativas, celdas y apéndices fueron actualizadas mediante un mapa determinista.

## Qué no cambia

- El contenido proposicional de las filas.
- El orden de las afirmaciones.
- Las claves `S…`, `E…`, `H…` y `BN-…`.
- Los valores, unidades, intervalos y localizadores.
- La clasificación epistemológica de las afirmaciones.
- Los huecos declarados.

## Fuente de verdad posterior

Después de la migración:

- la prosa se edita en `docs/secciones/`;
- las tablas se editan en `data/`;
- los informes y `exports/` se regeneran;
- la instantánea de `archive/` queda solo para auditoría histórica.

## Verificación histórica

La auditoría de migración reconstruye la instantánea v5 para comprobar la
procedencia y posición de las 78 tablas heredadas. No exige igualdad de contenido
después de las correcciones bibliográficas, ampliaciones y renumeraciones; las 13
tablas creadas después de la migración se cuentan y se validan como tablas nativas.

```bash
python3 scripts/audit_migration.py
```

Para el corpus científico actual, la comprobación operativa es:

```bash
make verify
```

El informe autocontenido no se compara byte a byte con el original porque el renderizador normaliza el espaciado de tablas y el formato de los identificadores. La validación compara filas, columnas, referencias y contenido canónico.
