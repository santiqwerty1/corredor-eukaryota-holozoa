# Revisión independiente acotada de infraestructura — 2026-09-26

Revisor: agente `/root/estado_revisiones`, distinto de los agentes autores
`contrato_censo` y `aislamiento_verify`. Rama inspeccionada:
`codex/cierre-plan-pendiente`. Se revisaron los cambios de código, sus pruebas
y el contrato documental, sin adjudicar afirmaciones científicas ni controles
manuales de requisitos. No se ejecutó `make verify` sobre el corpus vivo.
Los comandos `make verify` de esta revisión se limitaron a fixtures mínimos
temporales que no contienen el corpus.

## Dictamen

- UTC y catálogos: sin hallazgos accionables en el alcance revisado. La fecha
  explícita, las comprobaciones de calendario y la cronología sustituyen el día
  fijo sin depender del reloj. El Apéndice A sigue congelado una sola vez.
- Aislamiento: **NO CONFORME**. Hay dos vías P1 de contaminación de entorno
  reproducidas que permiten anunciar éxito sin ejecutar comprobaciones reales.
  Se reprodujo además una limitación de supervisión de procesos descendientes.
- Este informe no cierra el censo semántico, la segunda revisión global ni
  ningún control científico. Un cambio de huella requiere reinspección; las
  aprobaciones de infraestructura no se transfieren al contenido del corpus.

## Huellas del estado revisado

| Archivo | SHA-256 |
|---|---|
| `scripts/check_semantic_claim_census.py` | `598dacc8ea3c0d1d3be06763ebc0734988a50c2fc9105095a66274e5c3dc3350` |
| `tests/test_check_semantic_claim_census.py` | `5a98f24c0078b8808942e86999e5cee7cad8b4f3e27dc58cc1ea1ddc4b09b509` |
| `docs/auditorias/protocolo_censo_semantico_2026-08-13.md` | `d312f22b287f94eac3a402af049977f69d56842c2d1638930d77df6ce3f32e15` |
| `scripts/check_isolated_verify.py` | `d03588da522230046eb38cfa11c1fa93be32583b9a6dd94d2c008e37ca764bd0` |
| `tests/test_check_isolated_verify.py` | `84cbe663dc01b9ba360e4aab8c014eccd488c138eb9ee76a27848359e3cd1b9d` |

## Pruebas realizadas

Desde la raíz del repositorio:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_check_semantic_claim_census -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_check_isolated_verify -v
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/revision_contrato_censo_20260926.py
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/revision_aislamiento_20260926.py
```

Resultados sobre las huellas anteriores:

- Suite UTC/catálogos del repositorio: 20 pruebas, todas pasan.
- Suite aislamiento del repositorio: 21 pruebas, todas pasan.
- Auditor adversario UTC/catálogos: 7 pruebas, todas pasan; incluye las 27
  combinaciones de tres instantes alrededor del cambio de año, 18 combinaciones
  de fecha imposible/no canónica y rol, inversión del orden de filas primarias,
  tres pares de catálogos, conservación de A y comparación con semillas 1/777
  y zonas `UTC`/`Pacific/Kiritimati`.
- Auditor adversario de aislamiento: 8 pruebas, 5 pasan y 3 fallan. Los fallos
  corresponden a los dos P1 y a la limitación de descendientes descritos abajo.
- Hardlinks a archivos externos o del padre, incluida `.git/index.lock`, se
  materializan en inodos diferentes. Un symlink interno hacia ese hardlink
  modifica solamente la copia. Un symlink `.git/locks` hacia fuera se rechaza.
- `copytree` conserva los permisos examinados de archivos y directorios aun
  con `umask 077`; la comparación inicial no informa una igualdad falsa.
- Una receta fallida que modifica el padre es detectada. La normalización de
  salida conserva número de pruebas, estado y mensajes; solo ignora el campo
  de tiempo de la línea canónica de `unittest`.

Los auditores temporales tienen las huellas siguientes. Sus rutas en `/tmp`
son auxiliares y no constituyen entregables duraderos; la reproducción mínima
autocontenida de los hallazgos de aislamiento se incluye más abajo.

| Auditor temporal | SHA-256 |
|---|---|
| `/tmp/revision_contrato_censo_20260926.py` | `f0fc0b5ca7b35772f97c3b815a5efb9446ea5c31349a80f83df05d65a1a9eaf5` |
| `/tmp/revision_aislamiento_20260926.py` | `18638e9e8e3f5e98da2ffdca8bee9112b65fea926ee29de4fc7f46dd0d067a60` |

## Hallazgos abiertos

### INF-01 — P1 — `MAKEFILES` permite omitir las recetas

Estado: ABIERTO. `verify_environment()` elimina varias variables de Make,
pero conserva `MAKEFILES`. Un fichero externo incluido por esa variable puede
contener `override SHELL := /bin/true`. En el fixture cuya única receta es
`@false`, ambas ejecuciones devuelven cero y `main()` anuncia verificación
aislada correcta. El padre y la copia no cambian: las huellas no descubren
que la comprobación se omitió. Debe impedirse esa inyección y demostrarse
que la receta deliberadamente fallida vuelve a fallar.

### INF-02 — P1 — `PYTHONPATH` permite ejecutar código externo al checkout

Estado: ABIERTO. El entorno de la puerta conserva `PYTHONPATH`. En un
directorio externo, un `sitecustomize.py` con `import os; os._exit(0)` hace que
`python3 -c "raise SystemExit(1)"` termine con éxito antes de ejecutar su
comprobación. `main()` vuelve a declarar éxito dos veces y no encuentra
mutaciones. La corrección debe cubrir las vías de configuración que introduzcan
código Python externo, sin tratar una cadena de salida estable como prueba de
ejecución. No se exige sustituir el intérprete por otro no solicitado.

### INF-03 — Limitación abierta — descendientes sobreviven a la comparación

Estado: ABIERTO; requiere disposición explícita. Una receta que lanza
`{ sleep 0.5; echo late-change > RUTA_PADRE/README.md; } >/dev/null 2>&1 &`
devuelve antes que el proceso descendiente. `main()` anuncia éxito y, medio
segundo después, cambia el padre. La copia y las comparaciones antes/después
no son un sandbox de procesos. El caso no demuestra que las recetas reales
del proyecto hagan esto; demuestra que el mensaje de inmutabilidad no cubre
descendientes pendientes. Si se pretende esa garantía, hay que supervisar o
rechazar esos procesos antes de anunciar cierre. El auditor esperó a sus
descendientes de prueba antes de retirar el fixture.

## Reproducción mínima autocontenida de INF-01/02/03

Ejecutar este código con Python desde la raíz del repositorio. Solo crea y
modifica fixtures bajo el directorio temporal; nunca modifica el checkout real.
En el estado revisado imprime `0` para los tres casos, cuando no debería
certificarse éxito. En `descendiente`, `late-change` prueba la mutación tardía.

```python
import contextlib
import io
import os
import tempfile
import time
from pathlib import Path
from unittest.mock import patch
from scripts import check_isolated_verify as m

for caso in ("MAKEFILES", "PYTHONPATH", "descendiente"):
    with tempfile.TemporaryDirectory(prefix="revision-infra-") as raw:
        base = Path(raw)
        padre = base / "padre"
        (padre / ".git/objects/info").mkdir(parents=True)
        (padre / "README.md").write_text("original\n")
        env = {}
        receta = "@false"
        if caso == "MAKEFILES":
            externo = base / "externo.mk"
            externo.write_text("override SHELL := /bin/true\n")
            env["MAKEFILES"] = str(externo)
        elif caso == "PYTHONPATH":
            externo = base / "python_externo"
            externo.mkdir()
            (externo / "sitecustomize.py").write_text("import os\nos._exit(0)\n")
            env["PYTHONPATH"] = str(externo)
            receta = '@python3 -c "raise SystemExit(1)"'
        else:
            receta = ("@{ sleep 0.5; echo late-change > "
                       + str(padre / "README.md") + "; } >/dev/null 2>&1 &")
        (padre / "Makefile").write_text(".PHONY: verify\nverify:\n\t" + receta + "\n")
        salida, errores = io.StringIO(), io.StringIO()
        with (patch.object(m, "ROOT", padre), patch.dict(os.environ, env),
              contextlib.redirect_stdout(salida), contextlib.redirect_stderr(errores)):
            resultado = m.main()
        if caso == "descendiente":
            time.sleep(0.8)
        print(caso, resultado, (padre / "README.md").read_text().strip())
        print(salida.getvalue(), errores.getvalue())
```

## Límites del dictamen UTC/catálogos

El verificador comprueba sintaxis, calendario y orden temporal. No autentica
la hora real de trabajo: una serie coherente de instantes futuros puede pasar.
El protocolo revisado declara correctamente esa limitación y exige evidencia
de ejecución e independencia. No se aprobó una fecha futura ni se convirtió
esa aceptación sintáctica en evidencia de que una revisión hubiera ocurrido.
No se revisaron semánticamente pasajes científicos, ni se aprobó una congelación
nueva o las filas ausentes del censo.
