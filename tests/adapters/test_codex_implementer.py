"""Focused contract tests for the Codex implementer seam."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from src.adapters.implementer.codex import AdapterError, _argv_from_env, _prompt, execute


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True,
    ).stdout.strip()


def make_repo(root: Path) -> tuple[Path, str]:
    repo = root / "repo"
    metadata = Path(f"{repo}.git")
    subprocess.run(
        ["git", "init", "-q", f"--separate-git-dir={metadata}", str(repo)],
        check=True, capture_output=True, text=True,
    )
    git(repo, "config", "user.name", "fixture")
    git(repo, "config", "user.email", "fixture@example.invalid")
    (repo / "owned.txt").write_text("base\n", encoding="utf-8")
    git(repo, "add", "owned.txt")
    git(repo, "commit", "-qm", "base")
    return repo, git(repo, "rev-parse", "HEAD")


def packet(repo: Path, base: str, **overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "schema": "agent-platform.phase-request/v1",
        "phase": "implement",
        "issue": {"number": 224, "url": "https://github.com/redtrades/agent-platform/issues/224"},
        "run_id": "codex-phase-seam-224-01",
        "cwd": str(repo),
        "input_revision": base,
        "owned_paths": ["owned.txt"],
        "objective": "Make one bounded fixture change.",
        "acceptance_criteria": ["owned.txt is changed in one commit."],
        "author_family": "other:codex-implementer",
    }
    value.update(overrides)
    return value


def fake_codex(root: Path, body: str) -> str:
    executable = root / "codex"
    repository = (root / "repo").resolve()
    executable.write_text(textwrap.dedent(f"""\
        #!{sys.executable}
        import json
        from pathlib import Path
        import subprocess
        import sys

        argv = sys.argv[1:]
        expected = [
            '-a', 'never', 'exec', '--ignore-user-config', '--ignore-rules',
            '--strict-config', '--ephemeral', '-C', {json.dumps(str(repository))},
            '-s', 'workspace-write', '-',
        ]
        assert argv == expected, argv
        raw_prompt = sys.stdin.read()
        instructions, raw_packet = raw_prompt.rsplit('\\n', 1)
        assert instructions.startswith('Execute the task now.'), instructions
        prompt = json.loads(raw_packet)
        assert Path(prompt['request']['cwd']).resolve() == Path({json.dumps(str(repository))})
        assert prompt['constraints']['owned_paths'] == ['owned.txt']
    """) + textwrap.dedent(body), encoding="utf-8")
    executable.chmod(0o700)
    return json.dumps([str(executable), "-a", "never", "exec", "--ignore-user-config", "--ignore-rules",
                       "--strict-config", "--ephemeral", "-C", str(repository),
                       "-s", "workspace-write", "-"])


def environment(command: str, **extra: str) -> dict[str, str]:
    return {
        "AGENT_PLATFORM_CODEX_COMMAND": command,
        "AGENT_PLATFORM_CODEX_CREDENTIAL_REF": "secret://codex-host-auth",
        **extra,
    }


class CodexImplementerTests(unittest.TestCase):
    def test_prompt_requires_success_for_a_zero_change_result(self):
        with tempfile.TemporaryDirectory() as directory:
            repo, base = make_repo(Path(directory))
            _, raw_packet = _prompt(packet(repo, base)).rsplit("\n", 1)
            prompt = json.loads(raw_packet)
        self.assertEqual(prompt["return_contract"]["status"], "success")

    def test_prompt_declares_the_complete_local_only_execution_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            repo, base = make_repo(Path(directory))
            request = packet(repo, base)
            rendered = _prompt(request)
            instructions, raw_packet = rendered.rsplit("\n", 1)
            prompt = json.loads(raw_packet)

        self.assertTrue(instructions.startswith("Execute the task now."))
        self.assertIn("Do not merely summarize or echo the packet.", instructions)
        self.assertIn("do not access GitHub or the network", instructions)
        self.assertIn("Change only owned paths", instructions)
        self.assertIn("Do not create or alter Git history.", instructions)
        self.assertIn("commit_count 0", instructions)
        self.assertIn("output exactly the required child JSON object", instructions)
        self.assertEqual(prompt["request"], request)
        self.assertNotIn("secret://", rendered)
        self.assertNotIn("AGENT_PLATFORM_CODEX_CREDENTIAL_REF", rendered)

        self.assertEqual(prompt["execution_contract"], {
            "packet": "complete-and-authoritative",
            "action": "execute-now",
            "remote_context": "do-not-access-github-network-or-refetch-issue-or-pr",
            "workspace": "use-only-admitted-local-cwd-and-local-git",
            "changes": "owned-paths-only",
            "commit": "model-must-not-commit; controller-commits-validated-paths",
            "result": "return-exact-child-envelope",
        })

    def test_direct_script_from_external_cwd_reaches_typed_request_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            completed = subprocess.run(
                [sys.executable, str(REPOSITORY_ROOT / "src/adapters/implementer/codex.py")],
                cwd=directory,
                input=json.dumps({"not": "an admitted request"}),
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(completed.returncode, 1, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["schema"], "agent-platform.phase-result/v1")
        self.assertEqual(result["failure"]["code"], "family-conflict")

    def test_controller_derives_success_from_owned_edit_despite_arbitrary_child_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            git(repo, "config", "user.name", "Agent mvp-one-shot")
            git(repo, "config", "user.email", "agent+mvp-one-shot.codex-phase-seam-224-01@agents.invalid")
            command = fake_codex(root, """
                cwd = Path(prompt['request']['cwd'])
                (cwd / 'owned.txt').write_text('changed\\n', encoding='utf-8')
                print('unstructured non-authoritative model text')
            """)
            result = execute(packet(repo, base), environment(command))
            self.assertEqual(result["status"], "success", result)
            self.assertEqual(result["actor_family"], "other:codex-implementer")
            self.assertEqual(result["candidate_revision"], git(repo, "rev-parse", "HEAD"))
            self.assertEqual(result["changed_paths"], ["owned.txt"])
            self.assertEqual(result["commit_count"], 1)
            self.assertEqual(git(repo, "status", "--porcelain=v1", "--untracked-files=all"), "")
            self.assertEqual(git(repo, "log", "-1", "--format=%an <%ae>"),
                             "Agent mvp-one-shot <agent+mvp-one-shot.codex-phase-seam-224-01@agents.invalid>")
            self.assertEqual(git(repo, "log", "-1", "--format=%B"),
                             "mvp: implement issue #224\n\nAgent-Actor: agent/mvp-one-shot\nAgent-Run-ID: codex-phase-seam-224-01")

    def test_command_binding_is_exact_and_shell_free(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, _ = make_repo(root)
            safe = json.loads(fake_codex(root, "print('{}')"))
            self.assertEqual(_argv_from_env(environment(json.dumps(safe)), repo.resolve()), safe)
            for unsafe in (
                ["bash", "-c", "echo unsafe"],
                [*safe[:-3], "danger-full-access", "-"],
                [*safe[:-1], "--config", "unsafe=true", "-"],
            ):
                with self.assertRaises(AdapterError):
                    _argv_from_env(environment(json.dumps(unsafe)), repo.resolve())

    def test_missing_nonzero_and_wrong_head_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            self.assertEqual(execute(packet(repo, base), {})["failure"]["code"], "missing-binding")
            failed = fake_codex(root, "raise SystemExit(23)")
            self.assertEqual(execute(packet(repo, base), environment(failed))["failure"]["code"], "child-failed")
            self.assertEqual(execute(packet(repo, "f" * 40), environment(failed))["failure"]["code"],
                             "subject-mismatch")

    def test_nonzero_child_failure_has_only_safe_typed_diagnostics(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            command = fake_codex(root, """
                print('authentication failed: never-return-this-value', file=sys.stderr)
                raise SystemExit(23)
            """)
            result = execute(packet(repo, base), environment(command, FIXTURE_SECRET_TOKEN="never-return-this-value"))

        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["failure"]["code"], "child-failed")
        self.assertEqual(result["failure"]["diagnostic"]["child_exit_status"], 23)
        self.assertEqual(result["failure"]["diagnostic"]["stderr_category"], "authentication")
        self.assertRegex(result["failure"]["diagnostic"]["stderr_sha256"], r"^[0-9a-f]{64}$")
        self.assertNotIn("never-return-this-value", json.dumps(result))

    def test_zero_exit_child_text_cannot_override_empty_workspace_denial(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            for child_status in ("no_op", "failure"):
                with self.subTest(child_status=child_status):
                    command = fake_codex(root, f"""
                        print(json.dumps({{'schema': 'agent-platform.child-implementer-result/v1', 'status': {child_status!r},
                              'candidate_revision': None, 'changed_paths': [], 'commit_count': 0,
                              'attempts': ['raw-output-marker']}}))
                    """)
                    result = execute(packet(repo, base, objective="prompt-marker"), environment(
                        command, FIXTURE_SECRET_TOKEN="environment-marker",
                    ))

                    self.assertEqual(result["failure"]["code"], "forbidden-effect")
                    rendered = json.dumps(result)
                    self.assertNotIn("raw-output-marker", rendered)
                    self.assertNotIn("prompt-marker", rendered)
                    self.assertNotIn("environment-marker", rendered)

    def test_zero_exit_empty_edit_fails_without_parsing_child_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            command = fake_codex(root, "print('not json and not a success claim')")
            result = execute(packet(repo, base), environment(command))

        self.assertEqual(result["failure"]["code"], "forbidden-effect")
        self.assertIn("empty", result["failure"]["message"])

    def test_child_commit_reset_metadata_drift_is_denied_before_controller_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            command = fake_codex(root, """
                cwd = Path(prompt['request']['cwd'])
                (cwd / 'owned.txt').write_text('bad\\n', encoding='utf-8')
                subprocess.run(['git', '-C', str(cwd), 'add', 'owned.txt'], check=True)
                subprocess.run(['git', '-C', str(cwd), 'commit', '-qm', 'bad'], check=True)
                subprocess.run(['git', '-C', str(cwd), 'reset', '--hard', prompt['request']['input_revision']],
                               check=True, stdout=subprocess.DEVNULL)
                subprocess.run(['git', '-C', str(cwd), 'config', '--local', 'user.name', 'model-drift'], check=True)
                (cwd / 'owned.txt').write_text('after-reset\\n', encoding='utf-8')
                print('this claim is not authoritative')
            """)
            result = execute(packet(repo, base), environment(command))
            self.assertEqual(result["failure"]["code"], "forbidden-effect", result)
            self.assertIn("Git metadata changed", result["failure"]["message"])

    def test_out_of_scope_edits_are_denied_regardless_of_child_output(self):
        cases = (
            ("""
                cwd = Path(prompt['request']['cwd'])
                (cwd / 'outside.txt').write_text('bad\\n', encoding='utf-8')
                print('outside path claim')
            """, "forbidden-effect"),
            ("""
                cwd = Path(prompt['request']['cwd'])
                (cwd / 'owned.txt').write_text('bad\\n', encoding='utf-8')
                (cwd / 'outside.txt').write_text('also-bad\\n', encoding='utf-8')
                print('owned path cannot hide an outside edit')
            """, "forbidden-effect"),
        )
        for body, code in cases:
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                repo, base = make_repo(root)
                result = execute(packet(repo, base), environment(fake_codex(root, body)))
                self.assertEqual(result["failure"]["code"], code, result)

    def test_controller_disables_malicious_local_hooks_when_committing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            git(repo, "config", "user.name", "Agent mvp-one-shot")
            git(repo, "config", "user.email", "agent+mvp-one-shot.codex-phase-seam-224-01@agents.invalid")
            hooks = root / "hooks"
            hooks.mkdir()
            hook = hooks / "pre-commit"
            marker = root / "hook-executed"
            hook.write_text(f"#!/bin/sh\ntouch {marker}\nexit 1\n", encoding="utf-8")
            hook.chmod(0o700)
            git(repo, "config", "core.hooksPath", str(hooks))
            command = fake_codex(root, """
                cwd = Path(prompt['request']['cwd'])
                (cwd / 'owned.txt').write_text('changed\\n', encoding='utf-8')
                print('ordinary output')
            """)
            result = execute(packet(repo, base), environment(command))
            self.assertEqual(result["status"], "success", result)
            self.assertNotEqual(git(repo, "rev-parse", "HEAD"), base)
            self.assertFalse(marker.exists())

    def test_environment_value_leak_is_denied_and_redacted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            command = fake_codex(root, """
                import os
                print(json.dumps({'schema': 'agent-platform.child-implementer-result/v1', 'status': 'success',
                      'candidate_revision': prompt['request']['input_revision'], 'changed_paths': [],
                      'commit_count': 0, 'attempts': [os.environ['FIXTURE_SECRET_TOKEN']]}))
            """)
            result = execute(packet(repo, base), environment(command, FIXTURE_SECRET_TOKEN="never-return-this-value"))
            self.assertEqual(result["failure"]["code"], "credential-leak")
            self.assertNotIn("never-return-this-value", json.dumps(result))

    def test_stderr_runtime_path_does_not_trigger_environment_leak_detection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            git(repo, "config", "user.name", "Agent mvp-one-shot")
            git(repo, "config", "user.email", "agent+mvp-one-shot.codex-phase-seam-224-01@agents.invalid")
            command = fake_codex(root, """
                import os
                cwd = Path(prompt['request']['cwd'])
                print(os.environ['HOME'], file=sys.stderr)
                (cwd / 'owned.txt').write_text('changed\\n', encoding='utf-8')
                print('arbitrary output')
            """)
            result = execute(packet(repo, base), environment(command, HOME="/home/fixture"))
            self.assertEqual(result["status"], "success", result)


if __name__ == "__main__":
    unittest.main()
