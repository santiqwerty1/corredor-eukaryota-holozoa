# Revisión independiente acotada del supervisor — 2026-09-26

Revisor: agente `/root/aislamiento_verify/revision_supervisor`, distinto del
autor del parche `/root/aislamiento_verify`. Rama inspeccionada:
`codex/cierre-plan-pendiente`. El revisor examinó el diseño, señaló el caso de
`SIGCHLD` heredado y reensayó la implementación posterior; no escribió ni
modificó el código productivo ni sus pruebas del repositorio.

## Dictamen y alcance

**CONFORME en los casos de infraestructura enumerados abajo y solamente sobre
las huellas registradas.** Las reproducciones de `MAKEFILES`, `PYTHONPATH` y
descendientes tardíos del auditor anterior pasan ahora. El supervisor también
superó seis pruebas adversariales propias. No quedan hallazgos accionables
en este alcance examinado.

Este documento no modifica ni sustituye
`revision_infraestructura_2026-09-26.md`: sus INF-01–INF-03 describen otra
versión del código. Registra evidencia posterior independiente, no reescribe
su resultado histórico. No cierra el censo semántico, controles científicos,
segundas revisiones globales, ni el objetivo completo. No se ejecutó
`make verify` sobre el corpus vivo: todas las recetas de esta revisión
pertenecen a fixtures mínimos temporales bajo `/tmp`.

## Huellas examinadas

| Archivo | SHA-256 |
|---|---|
| `scripts/check_isolated_verify.py` | `4064b6ddcde9090a7e762bff40d396662ea46820215fa2185c88b3f8a9d745e9` |
| `tests/test_check_isolated_verify.py` | `59a20f4f5847724052de673c94203d0fd3773e4fc7595c690199fbf2a372298f` |
| `/tmp/revision_aislamiento_20260926.py` | `18638e9e8e3f5e98da2ffdca8bee9112b65fea926ee29de4fc7f46dd0d067a60` |

Un cambio de estas huellas exige volver a examinar el alcance afectado.

## Evidencia ejecutada por este revisor

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_check_isolated_verify -v
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/revision_aislamiento_20260926.py
```

- Suite del repositorio: **31 pruebas, todas pasan**, reejecutadas por este
  revisor; no se sustituye esta ejecución por el resultado comunicado por el
  autor. Incluye los rechazos de las variables `MAKE`, `PYTHON`, `MAKEFILES`,
  `PYTHONPATH` y selección de un `make` falso mediante `PATH`.
- Auditor independiente anterior: **8 pruebas, todas pasan**, sin modificarlo.
  En la primera inspección de este revisor, antes del parche, el mismo auditor
  produjo cinco éxitos y los tres fallos de `MAKEFILES`, `PYTHONPATH` y
  mutación tardía; ahora las recetas deliberadamente fallidas son rechazadas
  y la mutación tardía se observa antes de terminar la comprobación.
- Ensayo propio reproducible a continuación: **6 pruebas, todas pasan**.
  Comprueba tres generaciones creadas tardíamente, `setsid`, doble `fork`,
  mutación de la copia aun cuando `make` falla, muerte por señal de un
  descendiente, disposición real —no simulada— de `SIGCHLD`, y conservación
  del estado subreaper del proceso llamador.

No se ensayó aquí la suite global de 157 pruebas ni se certifican sus resultados.

## Razón técnica y límites

El supervisor separado activa y comprueba `PR_SET_CHILD_SUBREAPER` antes de
lanzar `make`. Espera primero su retorno y luego los huérfanos adoptados hasta
`ECHILD`. La adopción sigue el parentesco, no la sesión o grupo de procesos;
por eso las pruebas con `setsid` y generaciones posteriores siguen observadas.
Esta interpretación coincide con la documentación de
[PR_SET_CHILD_SUBREAPER](https://www.man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html).

El punto de entrada rechaza una disposición no predeterminada de `SIGCHLD`
antes de recoger el supervisor; este además restablece `SIG_DFL` antes de
lanzar `make`. Esto evita el caso reproducido donde `SIG_IGN` hacía que
`subprocess` interpretara como cero el retorno perdido de un comando fallido.
La pérdida de estados con `SIG_IGN` está documentada en
[wait(2)](https://man7.org/linux/man-pages/man2/wait.2.html).

- Es supervisión y comparación de estados, **no un sandbox de seguridad**.
  Una receta puede escribir mediante una ruta absoluta fuera de la copia;
  las pruebas demuestran detección del cambio del padre, no prevención.
- Las huellas comparan estados iniciales y finales, no registran cada escritura
  intermedia. No prueban ausencia de una escritura posteriormente revertida.
- Se requiere Linux con soporte subreaper. La ausencia de soporte no autoriza
  una alternativa menos estricta: debe fallar antes de lanzar las recetas.
- Un descendiente que no termina mantiene pendiente la comprobación: no hay
  timeout que convierta esa situación en éxito. La gestión de cancelaciones
  o la terminación forzada externa del supervisor no fue certificada aquí.
- Se inspeccionó el filtrado de las vías de entorno citadas y la selección de
  herramientas del sistema; no se certificó un sistema operativo hostil ni
  todas las dependencias posibles del sistema.

## Reproducción autocontenida de los seis ensayos propios

Ejecutar desde la raíz del repositorio. El programa solo crea fixtures bajo
`/tmp`, no altera los archivos del repositorio y usa la implementación viva.
Los retardos coordinan los fixtures; las aserciones usan resultados y estados,
no una cota de tiempo de ejecución.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import contextlib, ctypes, io, signal, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from scripts import check_isolated_verify as m

class ReviewSupervisor(unittest.TestCase):
    def fixture(self, base, code, fail_make=False):
        root = Path(base) / 'source'
        (root / '.git/objects/info').mkdir(parents=True)
        (root / 'README.md').write_text('original\n')
        code = code.replace('PARENT_TARGET', repr(str(root / 'README.md')))
        (root / 'worker.py').write_text(code)
        (root / 'Makefile').write_text(
            '.PHONY: verify\nverify:\n\t@python3 worker.py >/dev/null 2>&1\n'
            + ('\t@false\n' if fail_make else ''))
        return root

    def execute(self, root):
        out, err = io.StringIO(), io.StringIO()
        with patch.object(m, 'ROOT', root), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            result = m.main()
        return result, out.getvalue(), err.getvalue()

    def test_three_generations_after_make_exit_mutate_parent(self):
        code = (
            'import os,time\nfrom pathlib import Path\n'
            'if os.fork(): os._exit(0)\nos.setsid()\n'
            'for generation in range(3):\n'
            '    time.sleep(0.09)\n    if os.fork(): os._exit(0)\n'
            "Path(PARENT_TARGET).write_text('late\\n')\n")
        with tempfile.TemporaryDirectory(prefix='review-supervisor-', dir='/tmp') as raw:
            root = self.fixture(raw, code)
            status, out, err = self.execute(root)
            self.assertEqual(status, 1, (out, err))
            self.assertEqual((root / 'README.md').read_text(), 'late\n')
            self.assertIn('mutó el checkout padre: README.md', err)

    def test_double_fork_mutates_copied_content_even_when_make_failed(self):
        code = (
            'import os,time\nfrom pathlib import Path\n'
            'if os.fork(): os._exit(0)\nos.setsid()\n'
            'if os.fork(): os._exit(0)\ntime.sleep(0.2)\n'
            "Path('README.md').write_text('late\\n')\n")
        with tempfile.TemporaryDirectory(prefix='review-supervisor-', dir='/tmp') as raw:
            root = self.fixture(raw, code, True)
            status, out, err = self.execute(root)
            self.assertEqual(status, 1, (out, err))
            self.assertEqual((root / 'README.md').read_text(), 'original\n')
            self.assertIn('mutó el checkout con PYTHONHASHSEED=1: README.md', err)
            self.assertIn('falló', err)

    def test_detached_child_killed_by_signal_rejected(self):
        code = (
            'import os,time,signal\nif os.fork(): os._exit(0)\n'
            'os.setsid()\ntime.sleep(0.1)\nos.kill(os.getpid(), signal.SIGTERM)\n')
        with tempfile.TemporaryDirectory(prefix='review-supervisor-', dir='/tmp') as raw:
            root = self.fixture(raw, code)
            status, out, err = self.execute(root)
            self.assertEqual(status, 1, (out, err))
            self.assertIn('descendiente desacoplado', err)

    def test_real_sigchld_ignored_is_rejected_before_make(self):
        with tempfile.TemporaryDirectory(prefix='review-supervisor-', dir='/tmp') as raw:
            root = self.fixture(raw, 'raise SystemExit(23)\n')
            previous = signal.signal(signal.SIGCHLD, signal.SIG_IGN)
            try:
                status, out, err = self.execute(root)
            finally:
                signal.signal(signal.SIGCHLD, previous)
            self.assertEqual(status, 1, (out, err))
            self.assertIn('SIGCHLD', err)

    def test_supervisor_entry_resets_real_sigchld(self):
        with tempfile.TemporaryDirectory(prefix='review-supervisor-', dir='/tmp') as raw:
            root = self.fixture(raw, 'raise SystemExit(23)\n')
            source = ('import os,signal,sys;signal.signal(signal.SIGCHLD,signal.SIG_IGN);'
                      'os.execv(sys.executable,[sys.executable,"-I",sys.argv[1],'
                      '"--supervise",sys.argv[2],"1"])')
            done = subprocess.run(
                [sys.executable, '-I', '-c', source, str(Path(m.__file__).resolve()), str(root)],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=10)
            self.assertEqual(done.returncode, 1, done.stdout)
            self.assertIn('Error 23', done.stdout)

    def test_three_generations_success_do_not_change_parent_subreaper(self):
        libc = ctypes.CDLL(None)
        previous = ctypes.c_int()
        self.assertEqual(libc.prctl(37, ctypes.byref(previous), 0, 0, 0), 0)
        code = (
            'import os,time\nif os.fork(): os._exit(0)\nos.setsid()\n'
            'for generation in range(3):\n'
            '    time.sleep(0.03)\n    if os.fork(): os._exit(0)\n')
        with tempfile.TemporaryDirectory(prefix='review-supervisor-', dir='/tmp') as raw:
            root = self.fixture(raw, code)
            status, out, err = self.execute(root)
            self.assertEqual(status, 0, (out, err))
        current = ctypes.c_int()
        self.assertEqual(libc.prctl(37, ctypes.byref(current), 0, 0, 0), 0)
        self.assertEqual(current.value, previous.value)

unittest.main(verbosity=2)
PY
```
