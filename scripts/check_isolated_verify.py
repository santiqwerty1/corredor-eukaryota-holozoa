#!/usr/bin/env python3
"""Ejecuta la misma puerta ``make verify`` en una copia aislada completa."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
# Solo se excluyen cachés de ejecución, nunca dominios editoriales ni Git.
TRANSIENT_DIRECTORIES = {"__pycache__", ".pytest_cache"}
TRANSIENT_FILES = {".coverage"}
UNITTEST_ELAPSED = re.compile(r"^Ran (\d+) tests? in \d+\.\d{3}s$", re.MULTILINE)


class IsolationError(ValueError):
    """La copia no puede reproducirse sin depender del checkout original."""


def transient(name: str) -> bool:
    return (
        name in TRANSIENT_DIRECTORIES
        or name in TRANSIENT_FILES
        or name.endswith((".pyc", ".pyo"))
    )


def workspace_entries(root: Path):
    """Recorre el checkout completo, sin seguir enlaces ni excluir .git."""
    def raise_error(error: OSError) -> None:
        raise error

    if not root.is_dir():
        raise IsolationError(f"No existe el directorio que se debe inventariar: {root}")
    for current, directories, files in os.walk(root, followlinks=False, onerror=raise_error):
        directories[:] = sorted(name for name in directories if not transient(name))
        yield Path(current)
        for name in directories:
            path = Path(current) / name
            if path.is_symlink():
                yield path
        for name in sorted(files):
            if not transient(name):
                yield Path(current) / name


def workspace_digest(root: Path) -> dict[str, str]:
    """Huella contenido, tipo y permisos, incluidos derivados y metadatos Git.

    No solo se protegen las fuentes canónicas: una puerta de comprobación no
    debe cambiar tampoco outputs existentes, archivos nuevos, README, archive,
    recursos web, configuración ni índice/refs/objetos Git. Se ignoran tiempos
    de acceso/modificación y las cachés de ejecución declaradas arriba.
    """
    result: dict[str, str] = {}
    for path in workspace_entries(root):
        metadata = path.lstat()
        mode = stat.S_IMODE(metadata.st_mode)
        key = path.relative_to(root).as_posix()
        if stat.S_ISLNK(metadata.st_mode):
            result[key] = f"symlink:{mode:o}:{os.readlink(path)}"
        elif stat.S_ISDIR(metadata.st_mode):
            result[key] = f"directory:{mode:o}"
        elif stat.S_ISREG(metadata.st_mode):
            digest = hashlib.sha256()
            with path.open("rb") as handle:
                for block in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(block)
            result[key] = f"file:{mode:o}:{digest.hexdigest()}"
        else:
            raise IsolationError(f"Tipo de archivo no aislable: {key}")
    return result


def check_copy_inputs(root: Path) -> None:
    """Rechaza redirecciones a Git externo y enlaces que escaparían de la copia.

    Una .git de worktree (archivo gitdir), commondir o almacén de objetos con
    alternates exige materialización explícita, no copiar el puntero al padre.
    Los enlaces relativos internos se preservan; nunca se desreferencian.
    """
    git = root / ".git"
    if git.is_symlink() or not git.is_dir():
        raise IsolationError(".git debe ser un directorio Git autocontenido, no un puntero externo")
    for relative in ("commondir", "objects/info/alternates", "objects/info/http-alternates"):
        if (git / relative).exists():
            raise IsolationError(f"Referencia Git externa no aislable: .git/{relative}")
    resolved_root = root.resolve()
    for path in workspace_entries(root):
        if not path.is_symlink():
            continue
        target = os.readlink(path)
        try:
            internal = path.resolve().is_relative_to(resolved_root)
        except (OSError, RuntimeError) as error:
            raise IsolationError(f"Enlace no resoluble: {path.relative_to(root)}") from error
        if os.path.isabs(target) or not internal:
            raise IsolationError(f"Enlace que escaparía de la copia: {path.relative_to(root)}")
    for name in ("config", "config.worktree"):
        config = git / name
        if not config.exists():
            continue
        # Que el propio fichero esté copiado no vuelve internos sus includes.
        # Consultar sin seguirlos permite rechazar esas dependencias externas.
        result = subprocess.run(
            ["git", "config", "--file", str(config), "--no-includes", "--name-only",
             "--get-regexp", r"^(include|includeif\..*)\.path$"],
            cwd=root, env=verify_environment(root, "1"),
            text=True, capture_output=True,
        )
        if result.returncode == 0:
            raise IsolationError(f"Includes Git no materializados en .git/{name}")
        if result.returncode != 1:
            raise IsolationError(f"No se pudo inspeccionar .git/{name}: {result.stderr.strip()}")


def copy_workspace(root: Path, destination: Path) -> None:
    if destination.resolve().is_relative_to(root.resolve()):
        raise IsolationError("La copia temporal no puede estar dentro del checkout padre")
    check_copy_inputs(root)
    shutil.copytree(
        root,
        destination,
        symlinks=True,
        ignore=lambda directory, names: [name for name in names if transient(name)],
    )


def verify_environment(copy: Path, seed: str) -> dict[str, str]:
    # No heredar puntos de inyección capaces de saltarse una receta o hacer
    # que un intérprete termine con 0 sin ejecutar los controles. Se usa la
    # ruta del sistema; el PATH del llamador tampoco selecciona las herramientas.
    environment = {
        key: value for key, value in os.environ.items()
        if not key.startswith(("GIT_", "PYTHON", "MAKE", "LD_"))
        and key not in {
            "GNUMAKEFLAGS", "MFLAGS", "BASH_ENV", "ENV", "SHELL", "SHELLOPTS",
            "BASHOPTS", "CDPATH", "IFS",
        }
    }
    environment.update({
        "PATH": os.defpath,
        "AUDIT_ISOLATED_CHILD": "1",
        "PYTHONHASHSEED": seed,
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONNOUSERSITE": "1",
        "GIT_DIR": str(copy / ".git"),
        "GIT_COMMON_DIR": str(copy / ".git"),
        "GIT_WORK_TREE": str(copy),
        "GIT_INDEX_FILE": str(copy / ".git/index"),
        "GIT_OBJECT_DIRECTORY": str(copy / ".git/objects"),
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        # Un fsmonitor heredado podría ejecutar un proceso del checkout padre.
        "GIT_CONFIG_COUNT": "2",
        "GIT_CONFIG_KEY_0": "core.fsmonitor",
        "GIT_CONFIG_VALUE_0": "false",
        # git diff puede refrescar el índice aun con GIT_OPTIONAL_LOCKS=0;
        # impedir ese caché no cambia el examen de contenido/whitespace.
        "GIT_CONFIG_KEY_1": "diff.autoRefreshIndex",
        "GIT_CONFIG_VALUE_1": "false",
    })
    return environment


def enable_subreaper() -> None:
    """Activa y comprueba la adopción de huérfanos solo en el supervisor.

    Una sesión/grupo de procesos no basta: setsid y doble fork pueden escapar
    de ellos. Linux reparenta sus descendientes al subreaper; ECHILD certifica
    que ya no queda ninguno antes de tomar huellas. No es un sandbox contra
    código hostil ni impide una escritura explícita fuera de la copia.
    """
    if not sys.platform.startswith("linux"):
        raise IsolationError("La supervisión completa de descendientes requiere Linux")
    import ctypes

    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(36, 1, 0, 0, 0) != 0:  # PR_SET_CHILD_SUBREAPER
        raise IsolationError(f"No se pudo activar subreaper: errno={ctypes.get_errno()}")
    active = ctypes.c_int()
    if libc.prctl(37, ctypes.byref(active), 0, 0, 0) != 0 or active.value != 1:
        raise IsolationError("No se pudo verificar PR_GET_CHILD_SUBREAPER")


def supervise_verify(copy: Path, seed: str) -> int:
    """No termina cuando make sale, sino cuando termina todo su árbol."""
    signal.signal(signal.SIGCHLD, signal.SIG_DFL)
    enable_subreaper()
    process = subprocess.Popen(
        ["make", "verify"], cwd=copy, env=verify_environment(copy, seed),
        start_new_session=True,
    )
    status = process.wait()
    descendant_failed = False
    while True:
        try:
            _, child_status = os.waitpid(-1, 0)
        except ChildProcessError:
            break
        except InterruptedError:
            continue
        if os.waitstatus_to_exitcode(child_status) != 0:
            descendant_failed = True
    if descendant_failed:
        print("Un descendiente desacoplado de make terminó con error.", file=sys.stderr)
    return 0 if status == 0 and not descendant_failed else 1


def run_verify(copy: Path, seed: str) -> tuple[int, str]:
    # Con SIGCHLD ignorado, waitpid puede perder el estado real y Popen
    # interpretar ECHILD como retorno 0. No certificar en ese entorno.
    if signal.getsignal(signal.SIGCHLD) != signal.SIG_DFL:
        raise IsolationError("SIGCHLD no tiene disposición predeterminada; no se puede certificar el retorno")
    completed = subprocess.run(
        [sys.executable, "-I", str(Path(__file__).resolve()), "--supervise", str(copy), seed],
        cwd=copy,
        env=verify_environment(copy, seed),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return completed.returncode, completed.stdout


def canonical_output(output: str) -> str:
    """Normaliza solo los milisegundos diagnósticos que imprime unittest.

    Conserva el número de pruebas, OK/FAILED y todo el resto de la salida.
    Las rutas, mensajes y formatos inesperados no se normalizan. La igualdad
    probada es de salida normalizada, no byte a byte del reloj de pared.
    """
    return UNITTEST_ELAPSED.sub(
        lambda match: re.sub(r"\d+\.\d{3}s$", "<elapsed>s", match.group()), output,
    )


def report_changes(before: dict[str, str], after: dict[str, str], message: str) -> bool:
    changed = sorted(
        key for key in set(before) | set(after) if before.get(key) != after.get(key)
    )
    if changed:
        print(message + ": " + ", ".join(changed[:20]), file=sys.stderr)
    return bool(changed)


def verify_copy(copy: Path) -> int:
    before = workspace_digest(copy)
    outputs = []
    for seed in ("1", "777"):
        status, output = run_verify(copy, seed)
        # Una ejecución fallida tampoco puede ocultar que ha mutado la copia.
        mutated = report_changes(
            before, workspace_digest(copy),
            f"La puerta aislada mutó el checkout con PYTHONHASHSEED={seed}",
        )
        if status:
            print(
                f"La puerta completa falló en la copia aislada con PYTHONHASHSEED={seed}.",
                file=sys.stderr,
            )
            print(output, file=sys.stderr, end="")
            return 1
        if mutated:
            return 1
        outputs.append(canonical_output(output))
    if outputs[0] != outputs[1]:
        print(
            "La salida de la puerta aislada cambia entre PYTHONHASHSEED=1 y 777 "
            "(excluido únicamente el tiempo de unittest).",
            file=sys.stderr,
        )
        return 1
    return 0


def main() -> int:
    try:
        parent_before = workspace_digest(ROOT)
    except (OSError, IsolationError) as error:
        print(f"No se pudo inventariar el checkout padre: {error}", file=sys.stderr)
        return 1
    status = 1
    try:
        with tempfile.TemporaryDirectory(prefix="corredor-verify-isolated-") as raw:
            copy = Path(raw) / "repo"
            copy_workspace(ROOT, copy)
            if not report_changes(
                parent_before, workspace_digest(copy), "La copia inicial no reproduce el checkout",
            ):
                status = verify_copy(copy)
    except (OSError, IsolationError) as error:
        print(f"No se pudo ejecutar la puerta aislada: {error}", file=sys.stderr)
    # También se comprueba el padre tras fallos o excepciones de la puerta.
    try:
        if report_changes(
            parent_before, workspace_digest(ROOT), "La puerta aislada mutó el checkout padre",
        ):
            status = 1
    except (OSError, IsolationError) as error:
        print(f"No se pudo comprobar el checkout padre al terminar: {error}", file=sys.stderr)
        status = 1
    if status:
        return status
    print(
        "Puerta completa reproducida dos veces en copia aislada, sin mutaciones del "
        "checkout ni del padre (incluidos derivados y Git), con salidas idénticas "
        "para PYTHONHASHSEED=1 y 777 salvo el tiempo diagnóstico de unittest; "
        "todos los descendientes terminaron antes de comprobar las huellas."
    )
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--supervise":
        try:
            sys.exit(supervise_verify(Path(sys.argv[2]), sys.argv[3]))
        except (OSError, IsolationError) as error:
            print(f"No se pudo supervisar la puerta: {error}", file=sys.stderr)
            sys.exit(1)
    elif len(sys.argv) == 1:
        sys.exit(main())
    else:
        print("Uso: check_isolated_verify.py", file=sys.stderr)
        sys.exit(2)
