import contextlib
import io
import os
import signal
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import check_isolated_verify as module


class IsolatedVerifyTests(unittest.TestCase):
    def make_workspace(self, root: Path) -> None:
        (root / ".git/objects/info").mkdir(parents=True)
        for relative in (
            "README.md", "archive/original.md", "index.html", "support.js",
            ".github/workflows/check.yml", ".git/HEAD", ".git/index",
            "data/input.csv", "exports/derived.csv",
        ):
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("original\n", encoding="utf-8")

    def run_main(self, root: Path, verify=None):
        stdout, stderr = io.StringIO(), io.StringIO()
        with (
            patch.object(module, "ROOT", root),
            patch.object(module, "run_verify", side_effect=verify)
            if verify is not None else contextlib.nullcontext(),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            status = module.main()
        return status, stdout.getvalue(), stderr.getvalue()

    def write_makefile(self, root: Path, recipe: str, variables: str = "") -> None:
        (root / "Makefile").write_text(
            variables + ".PHONY: verify\nverify:\n\t@" + recipe + "\n",
            encoding="utf-8",
        )

    def test_complete_inventory_detects_previously_omitted_domains(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.make_workspace(root)
            before = module.workspace_digest(root)
            for relative in (
                "README.md", "archive/original.md", "index.html", "support.js",
                ".github/workflows/check.yml", ".git/HEAD", ".git/index",
            ):
                with self.subTest(relative=relative):
                    target = root / relative
                    target.write_text("mutated\n", encoding="utf-8")
                    after = module.workspace_digest(root)
                    self.assertNotEqual(before[relative], after[relative])
                    target.write_text("original\n", encoding="utf-8")
            self.assertEqual(before, module.workspace_digest(root))

    def test_inventory_detects_additions_deletions_modes_and_empty_directories(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.make_workspace(root)
            before = module.workspace_digest(root)
            (root / "new-domain").mkdir()
            self.assertIn("new-domain", module.workspace_digest(root))
            (root / "README.md").chmod(0o700)
            self.assertNotEqual(before["README.md"], module.workspace_digest(root)["README.md"])
            (root / "README.md").unlink()
            self.assertNotIn("README.md", module.workspace_digest(root))

    def test_only_execution_caches_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.make_workspace(root)
            before = module.workspace_digest(root)
            (root / "__pycache__").mkdir()
            (root / "__pycache__/cache.pyc").write_bytes(b"cache")
            (root / ".coverage").write_bytes(b"timing")
            self.assertEqual(before, module.workspace_digest(root))
            (root / "unexpected-output.tmp").write_bytes(b"output")
            self.assertNotEqual(before, module.workspace_digest(root))

    def test_symlinks_are_inventoried_without_following_targets(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.make_workspace(root)
            (root / "linked-dir").symlink_to("archive", target_is_directory=True)
            inventory = module.workspace_digest(root)
            self.assertTrue(inventory["linked-dir"].startswith("symlink:"))
            self.assertNotIn("linked-dir/original.md", inventory)

    def test_copy_preserves_internal_links_and_does_not_share_file_inodes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root, copy = Path(raw) / "source", Path(raw) / "copy"
            self.make_workspace(root)
            (root / "linked-file").symlink_to("README.md")
            module.copy_workspace(root, copy)
            self.assertEqual(module.workspace_digest(root), module.workspace_digest(copy))
            self.assertTrue((copy / "linked-file").is_symlink())
            (copy / "linked-file").write_text("mutated", encoding="utf-8")
            self.assertEqual((root / "README.md").read_text(), "original\n")

    def test_copy_rejects_absolute_and_escaping_links(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "source"
            self.make_workspace(root)
            for destination in (str(root / "README.md"), "../../external"):
                with self.subTest(destination=destination):
                    link = root / "escape"
                    link.symlink_to(destination)
                    with self.assertRaisesRegex(module.IsolationError, "escaparía"):
                        module.copy_workspace(root, Path(raw) / "copy")
                    link.unlink()

    def test_copy_rejects_linked_worktree_git_file(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "source"
            root.mkdir()
            (root / ".git").write_text("gitdir: /external/worktrees/checkout\n")
            with self.assertRaisesRegex(module.IsolationError, "autocontenido"):
                module.copy_workspace(root, Path(raw) / "copy")

    def test_copy_rejects_recursive_destination_inside_parent(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.make_workspace(root)
            with self.assertRaisesRegex(module.IsolationError, "dentro del checkout padre"):
                module.copy_workspace(root, root / "recursive-copy")
            self.assertFalse((root / "recursive-copy").exists())

    def test_inventory_does_not_silently_skip_unreadable_directories(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            with patch.object(module.os, "scandir", side_effect=PermissionError("unreadable")):
                with self.assertRaises(PermissionError):
                    module.workspace_digest(root)

    def test_copy_rejects_external_git_object_stores(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "source"
            self.make_workspace(root)
            for relative in ("commondir", "objects/info/alternates", "objects/info/http-alternates"):
                with self.subTest(relative=relative):
                    target = root / ".git" / relative
                    target.write_text("/external/objects\n")
                    with self.assertRaisesRegex(module.IsolationError, "Referencia Git externa"):
                        module.copy_workspace(root, Path(raw) / "copy")
                    target.unlink()

    def test_copy_rejects_git_configuration_includes_without_reading_them(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "source"
            self.make_workspace(root)
            for name, header in (("config", "include"), ("config.worktree", 'includeIf "gitdir:/other/"')):
                with self.subTest(name=name):
                    config = root / ".git" / name
                    config.write_text(f"[{header}]\n path = /external/missing-config\n")
                    with self.assertRaisesRegex(module.IsolationError, "Includes Git no materializados"):
                        module.copy_workspace(root, Path(raw) / "copy")
                    config.unlink()

    def test_git_config_symlink_is_rejected_before_reading_external_content(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "source"
            self.make_workspace(root)
            external = Path(raw) / "external-config"
            external.write_text("[core]\n bare = false\n")
            (root / ".git/config").symlink_to(external)
            with patch.object(module.subprocess, "run") as command:
                with self.assertRaisesRegex(module.IsolationError, "escaparía"):
                    module.copy_workspace(root, Path(raw) / "copy")
                command.assert_not_called()

    def test_environment_cannot_redirect_git_or_skip_make_recipes(self) -> None:
        with patch.dict(os.environ, {
            "GIT_DIR": "/parent/.git", "GIT_WORK_TREE": "/parent",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES": "/parent/.git/objects",
            "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "core.worktree",
            "GIT_CONFIG_VALUE_0": "/parent", "MAKEFLAGS": "n",
            "MAKELEVEL": "4", "MFLAGS": "-n", "MAKEOVERRIDES": "PYTHON=false",
            "MAKEFILES": "/external.mk", "MAKE": "/bin/true", "PYTHON": "/bin/true",
            "PYTHONPATH": "/outside", "PYTHONHOME": "/outside", "BASH_ENV": "/outside.sh",
            "LD_PRELOAD": "/outside.so", "PATH": "/outside/bin",
        }):
            environment = module.verify_environment(Path("/isolated"), "777")
        self.assertEqual(environment["GIT_DIR"], "/isolated/.git")
        self.assertEqual(environment["GIT_WORK_TREE"], "/isolated")
        self.assertEqual(environment["GIT_COMMON_DIR"], "/isolated/.git")
        self.assertEqual(environment["GIT_CONFIG_KEY_0"], "core.fsmonitor")
        self.assertEqual(environment["GIT_OPTIONAL_LOCKS"], "0")
        self.assertEqual(environment["PYTHONHASHSEED"], "777")
        self.assertNotIn("GIT_ALTERNATE_OBJECT_DIRECTORIES", environment)
        self.assertNotIn("MAKEFLAGS", environment)
        self.assertNotIn("MAKELEVEL", environment)
        self.assertNotIn("MFLAGS", environment)
        self.assertNotIn("MAKEOVERRIDES", environment)
        for variable in (
            "MAKEFILES", "MAKE", "PYTHON", "PYTHONPATH", "PYTHONHOME", "BASH_ENV", "LD_PRELOAD",
        ):
            self.assertNotIn(variable, environment)
        self.assertEqual(environment["PATH"], os.defpath)
        self.assertEqual(environment["PYTHONNOUSERSITE"], "1")

    def test_external_makefiles_cannot_skip_a_failing_recipe(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "source"
            self.make_workspace(root)
            self.write_makefile(root, "false")
            external = Path(raw) / "external.mk"
            external.write_text("override SHELL := /bin/true\n")
            with patch.dict(os.environ, {"MAKEFILES": str(external)}):
                status, stdout, stderr = self.run_main(root)
            self.assertEqual(status, 1, (stdout, stderr))
            self.assertIn("falló", stderr)

    def test_external_pythonpath_cannot_skip_python_execution(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "source"
            self.make_workspace(root)
            self.write_makefile(root, 'python3 -c "raise SystemExit(1)"')
            external = Path(raw) / "python-injection"
            external.mkdir()
            (external / "sitecustomize.py").write_text("import os\nos._exit(0)\n")
            with patch.dict(os.environ, {"PYTHONPATH": str(external)}):
                status, stdout, stderr = self.run_main(root)
            self.assertEqual(status, 1, (stdout, stderr))
            self.assertIn("falló", stderr)

    def test_inherited_python_and_make_variables_cannot_skip_commands(self) -> None:
        for variable in ("PYTHON", "MAKE"):
            with self.subTest(variable=variable), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "source"
                self.make_workspace(root)
                if variable == "PYTHON":
                    self.write_makefile(root, '$(PYTHON) -c "raise SystemExit(1)"', "PYTHON ?= python3\n")
                else:
                    self.write_makefile(root, "$(MAKE) failure")
                    with (root / "Makefile").open("a") as handle:
                        handle.write("failure:\n\t@false\n")
                with patch.dict(os.environ, {variable: "/bin/true"}):
                    status, stdout, stderr = self.run_main(root)
                self.assertEqual(status, 1, (stdout, stderr))
                self.assertIn("falló", stderr)

    def test_inherited_path_cannot_select_a_fake_make(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "source"
            self.make_workspace(root)
            self.write_makefile(root, "false")
            external = Path(raw) / "bin"
            external.mkdir()
            fake = external / "make"
            fake.write_text("#!/bin/sh\nexit 0\n")
            fake.chmod(0o755)
            with patch.dict(os.environ, {"PATH": str(external)}):
                status, stdout, stderr = self.run_main(root)
            self.assertEqual(status, 1, (stdout, stderr))
            self.assertIn("falló", stderr)

    def test_detached_recipe_is_reaped_before_parent_hashes(self) -> None:
        for fail_make in (False, True):
            with self.subTest(fail_make=fail_make), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "source"
                self.make_workspace(root)
                self.write_makefile(
                    root, "{ sleep 0.15; echo late-change > " + str(root / "README.md")
                    + "; } >/dev/null 2>&1 &" + ("\n\t@false" if fail_make else ""),
                )
                status, stdout, stderr = self.run_main(root)
                self.assertEqual(status, 1, (stdout, stderr))
                self.assertEqual((root / "README.md").read_text(), "late-change\n")
                self.assertIn("mutó el checkout padre: README.md", stderr)

    def test_setsid_double_fork_and_late_fork_remain_supervised(self) -> None:
        for late_fork in (False, True):
            with self.subTest(late_fork=late_fork), tempfile.TemporaryDirectory() as raw:
                root = Path(raw) / "source"
                self.make_workspace(root)
                self.write_makefile(root, "python3 detached.py >/dev/null 2>&1")
                (root / "detached.py").write_text(
                    "import os, time\nfrom pathlib import Path\n"
                    "if os.fork(): os._exit(0)\n"
                    "os.setsid()\n"
                    + ("time.sleep(0.15)\n" if late_fork else "")
                    + "if os.fork(): os._exit(0)\n"
                    "time.sleep(0.15)\n"
                    f"Path({str(root / 'README.md')!r}).write_text('late-change\\n')\n",
                )
                status, stdout, stderr = self.run_main(root)
                self.assertEqual(status, 1, (stdout, stderr))
                self.assertEqual((root / "README.md").read_text(), "late-change\n")
                self.assertIn("mutó el checkout padre: README.md", stderr)

    def test_failed_detached_descendant_is_not_lost_after_successful_make(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "source"
            self.make_workspace(root)
            self.write_makefile(root, "{ sleep 0.15; exit 23; } >/dev/null 2>&1 &")
            status, stdout, stderr = self.run_main(root)
            self.assertEqual(status, 1, (stdout, stderr))
            self.assertIn("descendiente desacoplado", stderr)

    def test_real_successful_gate_and_finished_descendants_can_pass(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "source"
            self.make_workspace(root)
            self.write_makefile(root, "{ sleep 0.05; true; } >/dev/null 2>&1 &")
            before = module.workspace_digest(root)
            status, stdout, stderr = self.run_main(root)
            self.assertEqual(status, 0, (stdout, stderr))
            self.assertEqual(before, module.workspace_digest(root))
            self.assertIn("todos los descendientes terminaron", stdout)

    def test_ignored_sigchld_is_rejected_instead_of_losing_exit_status(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "source"
            self.make_workspace(root)
            self.write_makefile(root, "false")
            with patch.object(module.signal, "getsignal", return_value=signal.SIG_IGN):
                status, stdout, stderr = self.run_main(root)
            self.assertEqual(status, 1, (stdout, stderr))
            self.assertIn("SIGCHLD", stderr)

    def test_missing_subreaper_fails_closed_without_launching_make(self) -> None:
        with (
            patch.object(module, "enable_subreaper", side_effect=module.IsolationError("no subreaper")),
            patch.object(module.subprocess, "Popen") as child,
        ):
            with self.assertRaisesRegex(module.IsolationError, "no subreaper"):
                module.supervise_verify(Path("/unused"), "1")
            child.assert_not_called()

    def test_normalization_preserves_test_count_status_and_all_other_messages(self) -> None:
        baseline = "Ran 107 tests in 0.123s\n\nOK\nCenso: 2813\n"
        self.assertEqual(
            module.canonical_output(baseline),
            module.canonical_output(baseline.replace("0.123s", "9.999s")),
        )
        for changed in (
            baseline.replace("107", "108"), baseline.replace("OK", "FAILED"),
            baseline.replace("2813", "2812"), baseline.replace("tests", "test"),
            baseline + "/tmp/new-path\n", baseline.replace("0.123s", "0.12s"),
            baseline.replace("0.123s", "unknown"),
        ):
            with self.subTest(changed=changed):
                self.assertNotEqual(module.canonical_output(baseline), module.canonical_output(changed))
        self.assertEqual(module.canonical_output("prefix Ran 1 test in 0.123s\n"),
                         "prefix Ran 1 test in 0.123s\n")

    def test_success_checks_both_seeds_and_parent_without_mutation(self) -> None:
        seeds = []
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.make_workspace(root)
            before = module.workspace_digest(root)

            def verify(copy, seed):
                self.assertNotEqual(copy, root)
                self.assertEqual(module.workspace_digest(copy), before)
                seeds.append(seed)
                return 0, f"Ran 107 tests in {'0.123' if seed == '1' else '0.456'}s\n\nOK\n"

            status, stdout, stderr = self.run_main(root, verify)
            self.assertEqual(status, 0, stderr)
            self.assertEqual(seeds, ["1", "777"])
            self.assertEqual(before, module.workspace_digest(root))
            self.assertIn("tiempo diagnóstico", stdout)

    def test_mutations_outside_old_subset_fail_even_if_command_succeeds(self) -> None:
        for relative in ("README.md", "archive/original.md", ".git/HEAD", "exports/derived.csv"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                self.make_workspace(root)

                def verify(copy, seed):
                    (copy / relative).write_text("mutated\n")
                    return 0, "OK\n"

                status, stdout, stderr = self.run_main(root, verify)
                self.assertEqual(status, 1)
                self.assertIn(relative, stderr)
                self.assertEqual((root / relative).read_text(), "original\n")
                self.assertNotIn("reproducida dos veces", stdout)

    def test_mutation_only_in_second_seed_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.make_workspace(root)

            def verify(copy, seed):
                if seed == "777":
                    (copy / "README.md").write_text("mutated\n")
                return 0, "OK\n"

            status, _, stderr = self.run_main(root, verify)
            self.assertEqual(status, 1)
            self.assertIn("PYTHONHASHSEED=777", stderr)

    def test_parent_mutation_is_rejected_even_when_child_is_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.make_workspace(root)

            def verify(copy, seed):
                (root / "README.md").write_text("mutated\n")
                return 0, "OK\n"

            status, _, stderr = self.run_main(root, verify)
            self.assertEqual(status, 1)
            self.assertIn("mutó el checkout padre: README.md", stderr)

    def test_failure_and_exception_do_not_skip_parent_check(self) -> None:
        for exception in (False, True):
            with self.subTest(exception=exception), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                self.make_workspace(root)

                def verify(copy, seed):
                    (root / ".git/HEAD").write_text("mutated\n")
                    if exception:
                        raise OSError("cannot run make")
                    (copy / "README.md").write_text("also mutated\n")
                    return 1, "failure evidence\n"

                status, _, stderr = self.run_main(root, verify)
                self.assertEqual(status, 1)
                self.assertIn("mutó el checkout padre: .git/HEAD", stderr)
                if not exception:
                    self.assertIn("mutó el checkout con PYTHONHASHSEED=1: README.md", stderr)
                    self.assertIn("failure evidence", stderr)

    def test_different_success_output_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.make_workspace(root)
            status, _, stderr = self.run_main(root, lambda copy, seed: (0, f"value {seed}\n"))
            self.assertEqual(status, 1)
            self.assertIn("La salida", stderr)

    def test_real_git_reads_in_copy_do_not_refresh_index_or_touch_parent(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root, copy = Path(raw) / "source", Path(raw) / "copy"
            root.mkdir()
            # Esta suite también se ejecuta dentro de la puerta hija: no usar
            # su GIT_DIR/GIT_INDEX_FILE para preparar el fixture temporal.
            fixture_environment = module.verify_environment(root, "1")
            subprocess.run(
                ["git", "init", "-q", str(root)], env=fixture_environment, check=True,
            )
            (root / "README.md").write_text("content\n")
            subprocess.run(
                ["git", "add", "README.md"], cwd=root, env=fixture_environment, check=True,
            )
            before = module.workspace_digest(root)
            module.copy_workspace(root, copy)
            child_before = module.workspace_digest(copy)
            for arguments in (["diff", "--check"], ["ls-files", "--others", "--exclude-standard", "-z"]):
                subprocess.run(
                    ["git", *arguments], cwd=copy,
                    env=module.verify_environment(copy, "1"), check=True,
                    capture_output=True,
                )
            self.assertEqual(before, module.workspace_digest(root))
            self.assertEqual(child_before, module.workspace_digest(copy))
            (copy / "README.md").write_text("content with trailing whitespace  \n")
            invalid = subprocess.run(
                ["git", "diff", "--check"], cwd=copy,
                env=module.verify_environment(copy, "1"), capture_output=True,
            )
            self.assertNotEqual(invalid.returncode, 0)
            self.assertIn(b"trailing whitespace", invalid.stdout)


if __name__ == "__main__":
    unittest.main()
