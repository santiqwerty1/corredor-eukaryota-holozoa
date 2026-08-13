# Checkpoint de migración a Codex — 2026-08-13

## Objetivo que continúa

Implementar íntegramente el plan definido por `docs/C01-PROMPT-INVESTIGACION.md` sin reducir el alcance, debilitar validadores ni autoaprobar revisiones independientes.

## Política prospectiva añadida el 2026-08-13

Estas reglas rigen **todo contenido nuevo a partir de este checkpoint**. No ordenan modificar retroactivamente lo ya entregado; esa normalización pertenece a una pasada de cierre posterior.

### Localizadores: apartado y precisión complementaria

- Citar siempre un apartado recuperable del texto (`resumen`, `resultados`, `discusión`, un encabezado nominal o un puntero semántico verificable).
- Añadir línea, página, figura o tabla cuando aporte precisión, pero nunca usar esos punteros como sustituto del apartado.
- Forma correcta: `S56 discusión, líneas 318–321`.
- Formas insuficientes para contenido nuevo: `S56 líneas 318–321` y `S56` sin localizador.
- Si la evidencia reside exclusivamente en una figura o tabla, declarar que requiere inspección humana. Si el texto también formula la proposición, citar además el apartado textual.
- Motivo operativo: el corpus descargado conserva XML JATS, que suele preservar apartados pero no la maquetación impresa. En la medición recibida, los apartados resolvieron automáticamente el 89 % de los pasajes y los punteros semánticos el 78 %, frente a 0 % para línea, página, figura/tabla aisladas o clave desnuda.

### Accesibilidad como desempate científico

- A igualdad de calidad y pertinencia científica, preferir la fuente con texto completo accesible.
- Si una fuente cerrada es científicamente mejor, conservarla: la accesibilidad no autoriza a degradar calidad.
- Cuando una afirmación dependa de una única fuente cerrada, buscar una segunda fuente accesible equivalente que la corrobore, sin sustituir la primaria mejor.
- Línea base recibida para la pasada de cierre: 237/523 fuentes sin texto completo accesible; 501/1.813 afirmaciones sin ninguna fuente consultable; 409 de ellas dependen de una sola fuente cerrada.

### Predicados personalizados

- Al introducir cualquier predicado nuevo terminado en `*`, añadir inmediatamente una definición que incluya: nombre, relación que expresa y un ejemplo de la afirmación que lo usa.
- No acumular definiciones para una reparación posterior. La línea base comunicada es de 308 predicados personalizados ya existentes.

### Invariantes que no cambian

- `NO LOCALIZADO EN ESTA SESIÓN` es un resultado negativo etiquetado, no una tarea pendiente; no rellenarlo ni convertirlo en evidencia positiva.
- Mantener `Aceptación = no evaluado` cuando no pueda identificarse quién discrepa.
- Mantener las dos capas: prosa legible y registro estructurado.

## Estado del checkpoint

- Rama: `main`.
- Base anterior al checkpoint: `5d11f46`.
- Corpus canónico validado: 1.952 afirmaciones, 523 fuentes, 1.500 entidades, 109 eventos, 215 fechas, 81 hipótesis, 562 magnitudes, 68 búsquedas negativas y 92 tablas.
- Trazabilidad exacta: 3.209 segmentos.
- Se corrigieron 319 filas de afirmaciones. Los cambios se limitaron a `Fuente`, salvo C-1943 y C-1945, que pasaron de `glosa` a síntesis con dependencias previas, y C-1903, cuya glosa quedó con fuente `n/a`.
- Se añadieron marcadores reproducibles de soporte/uso a S02, S03, S04, S395, S507, S511, S515, S519 y S549.
- Los derivados ordinarios (`docs/informe_completo_autocontenido.md`, `exports/afirmaciones.csv`, `data/apendices/H_recuento_control.csv` y `manifest.json`) se regeneraron.
- AF202 y AF203 quedaron en cero en `audit_full.py`.

## Puertas verdes

Ejecutar desde la raíz del repositorio:

```bash
python3 scripts/render.py --check
python3 scripts/validate.py
python3 scripts/audit_migration.py
python3 scripts/build_table_lineage.py --check
python3 scripts/build_content_trace.py --check
python3 scripts/audit_semantics.py
python3 -m unittest discover -s tests -q
python3 scripts/check_render_idempotence.py
git diff --check
```

En este checkpoint pasan las nueve puertas. La suite contiene 58 pruebas.

La clasificación nominal de controles también se ejecuta sin fallos automáticos:

```bash
python3 scripts/audit_requirement_controls.py --root . --classification
```

Resultado: 42 controles automatizados, 0 automatizados con fallos y 210 pendientes de revisión manual.

## Puertas deliberadamente abiertas

### 1. Controles de requisitos

- Falta `docs/auditorias/revision_manual_requisitos_2026-08-08.csv`.
- Los 210 controles manuales siguen sin adjudicación independiente.
- `python3 scripts/audit_requirement_controls.py --root . --verify-artifacts` devuelve 294 incidencias porque los 252 artefactos de control y 36 vínculos del manifiesto no se han rematerializado contra el corpus vivo; R-0446 además informa cero fallos sin promoción.
- No rematerializar ni promover controles antes de resolver los requisitos sustantivos: la automatización no puede sustituir la revisión nominal del literal.

### 2. Matrices y segunda revisión

`python3 scripts/audit_full.py --json /tmp/audit_full_checkpoint.json` devuelve 12.574 hallazgos. El desglose actual es:

| Código | Conteo | Significado operativo |
|---|---:|---|
| AF748–AF752 | 2.060 cada uno | las 2.060 filas de segunda revisión siguen pendientes, sin revisor, independencia, fecha ni cierre |
| AF506 | 1.501 | huellas de afirmaciones desactualizadas |
| AF754 | 441 | huellas de objetos de segunda revisión desactualizadas |
| AF747 | 244 | población/estrato de segunda revisión obsoleto |
| AF516 | 39 | huellas de fuentes desactualizadas |
| AF574 | 33 | R-0288–R-0320 todavía arrastran S420 |
| AF758 | 4 | muestras deterministas obsoletas |
| AF064 | 3 | hashes del JSON reproducible obsoletos |
| AF561 | 3 | DOI/URL finales no sincronizados con A |
| AF515, AF560 | 2 cada uno | cobertura/tipo de matriz de fuentes obsoletos |
| AF067, AF507 | 1 cada uno | recuentos/cobertura de matrices obsoletos |

No quedan AF202, AF203, AF224 ni AF227.

### 3. Inconsistencia S420

S420 ya no existe en `data/apendices/A_fuentes.csv`, pero permanece en la matriz de fuentes y en R-0288–R-0320. Resolver una sola disposición canónica: restaurar S420 con uso válido o retirar/reemplazar todas sus referencias. No corregir únicamente la matriz.

### 4. QA tabular externa

El parser CSV canónico, los auditores y las pruebas pasan. El intento adicional con `@oai/artifact-tool` no pudo iniciarse en este entorno por `WSL ERROR: UtilBindVsockAnyPort: socket failed 1`. Reintentar desde el runtime de Codex; no instalar una biblioteca alternativa ni modificar las dependencias empaquetadas.

### 5. Insumos congelados que ya no están en `/tmp`

Los valores predeterminados de `scripts/build_audit_deliverables.py` apuntan a cuatro rutas ausentes en este checkpoint:

- `/tmp/corredor-eukaryota-auditoria-20260808`
- `/tmp/temp_claim_origins_9001_9020.csv`
- `/tmp/temp_claim_origins_9100_9131.csv`
- `/tmp/removed_sources_destination.csv`

El commit congelado `a3ce4e6685a4e287a5fbd478d4657e475e10de3c` sí existe en Git. Las huellas esperadas y la procedencia de esos insumos están registradas en `docs/auditorias/auditoria_reproducible_2026-08-08.json`. Reconstruirlos desde Git/evidencia auditable o pasar rutas equivalentes explícitas; no omitirlos ni inventarlos para conseguir una salida verde.

## Orden recomendado para continuar

1. Leer completo `docs/C01-PROMPT-INVESTIGACION.md` y derivar una lista de evidencia por requisito.
2. Auditar y remediar los 210 controles manuales, manteniendo `NO_CONFORME` cuando falte prueba nominal.
3. Resolver S420 y cualquier otro hallazgo sustantivo descubierto por esos controles.
4. Estabilizar el corpus canónico y ejecutar de nuevo las puertas verdes.
5. Reconstruir y validar los cuatro insumos congelados antes de invocar `build_audit_deliverables.py`.
6. Regenerar matrices, artefactos de controles, informe reproducible, exportaciones y manifiesto con los builders del repositorio.
7. Encargar la segunda revisión a agentes distintos de quienes hicieron las correcciones; cubrir la población y las expansiones exigidas, con huellas live.
8. Ejecutar `make verify`, comprobar determinismo/idempotencia en copia aislada, revisar el diff y solo entonces hacer el commit/push final.
