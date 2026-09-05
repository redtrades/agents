"""Contract tests for the Claude-family local implementer adapter."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from src.adapters.implementer.claude import execute


def git(*args: str, cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True,
    )
    return result.stdout.strip()


def make_repo(root: Path) -> tuple[Path, str]:
    repo = root / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    git("config", "user.name", "fake-test", cwd=repo)
    git("config", "user.email", "fake-test@example.invalid", cwd=repo)
    (repo / "README.md").write_text("base\n", encoding="utf-8")
    git("add", "README.md", cwd=repo)
    git("commit", "-m", "base", cwd=repo)
    return repo, git("rev-parse", "HEAD", cwd=repo)


def fake_child(root: Path, body: str) -> str:
    script = root / "fake-child.py"
    script.write_text(body, encoding="utf-8")
    return json.dumps([sys.executable, str(script)])


def packet(repo: Path, base: str, **overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "schema": "agent-platform.phase-request/v1",
        "phase": "implement",
        "issue": {"number": 9, "url": "https://github.com/redtrades/agent-platform/issues/9"},
        "run_id": "claude-run-1",
        "cwd": str(repo),
        "input_revision": base,
        "owned_paths": ["owned.txt"],
        "objective": "Make the admitted smallest change.",
        "acceptance_criteria": ["The fake child returns a typed result."],
        "author_family": "claude",
    }
    value.update(overrides)
    return value


class ClaudeImplementerTests(unittest.TestCase):
    def test_module_entrypoint_emits_json_and_nonzero_on_fail_closed_result(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            request = json.dumps(packet(repo, base))
            child_env = {
                **dict(__import__("os").environ),
                "AGENT_PLATFORM_CLAUDE_COMMAND": json.dumps([sys.executable, "missing.py"]),
                "AGENT_PLATFORM_CLAUDE_CREDENTIAL_REF": "secret://claude-test",
            }
            process = subprocess.run(
                [sys.executable, "-m", "src.adapters.implementer"],
                cwd=REPOSITORY_ROOT,
                input=request,
                capture_output=True,
                text=True,
                env=child_env,
            )
            self.assertNotEqual(process.returncode, 0)
            result = json.loads(process.stdout)
            self.assertEqual(result["schema"], "agent-platform.phase-result/v1")
            self.assertEqual(result["failure"]["code"], "child-failed")

    def test_runs_in_supplied_cwd_and_returns_one_commit_phase_result(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            command = fake_child(root, """
import json
from pathlib import Path
import subprocess
Path('owned.txt').write_text('implemented\\n', encoding='utf-8')
subprocess.run(['git', 'add', 'owned.txt'], check=True)
subprocess.run(['git', 'commit', '-m', 'implement'], check=True, capture_output=True)
candidate = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
print(json.dumps({'schema': 'agent-platform.child-implementer-result/v1', 'status': 'success',
                  'candidate_revision': candidate, 'changed_paths': ['owned.txt'],
                  'commit_count': 1, 'attempts': []}))
""")

            result = execute(packet(repo, base), {
                "AGENT_PLATFORM_CLAUDE_COMMAND": command,
                "AGENT_PLATFORM_CLAUDE_CREDENTIAL_REF": "secret://claude-test",
            })

            self.assertEqual(result["schema"], "agent-platform.phase-result/v1")
            self.assertEqual(result["phase"], "implement")
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["run_id"], "claude-run-1")
            self.assertEqual(result["input_revision"], base)
            self.assertEqual(result["candidate_revision"], git("rev-parse", "HEAD", cwd=repo))
            self.assertEqual(result["changed_paths"], ["owned.txt"])
            self.assertEqual(result["commit_count"], 1)
            self.assertNotIn("secret://claude-test", json.dumps(result))

    def test_missing_exact_command_or_credential_binding_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            repo, base = make_repo(Path(directory))
            for env in (
                {"AGENT_PLATFORM_CLAUDE_CREDENTIAL_REF": "secret://claude-test"},
                {"AGENT_PLATFORM_CLAUDE_COMMAND": json.dumps([sys.executable, "missing.py"])},
            ):
                result = execute(packet(repo, base), env)
                self.assertEqual(result["status"], "fail")
                self.assertEqual(result["failure"]["code"], "missing-binding")

    def test_malformed_child_output_is_not_forwarded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            command = fake_child(root, "print('not-json credential=should-not-escape')")
            result = execute(packet(repo, base), {
                "AGENT_PLATFORM_CLAUDE_COMMAND": command,
                "AGENT_PLATFORM_CLAUDE_CREDENTIAL_REF": "secret://claude-test",
            })
            self.assertEqual(result["status"], "fail")
            self.assertEqual(result["failure"]["code"], "malformed-child-output")
            self.assertNotIn("should-not-escape", json.dumps(result))

    def test_rejects_write_attempt_and_paths_outside_owned_scope(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            command = fake_child(root, """
import json
print(json.dumps({'schema': 'agent-platform.child-implementer-result/v1', 'status': 'success',
                  'candidate_revision': '2' * 40, 'changed_paths': ['../escape.txt'],
                  'commit_count': 0, 'attempts': ['git_push']}))
""")
            result = execute(packet(repo, base), {
                "AGENT_PLATFORM_CLAUDE_COMMAND": command,
                "AGENT_PLATFORM_CLAUDE_CREDENTIAL_REF": "secret://claude-test",
            })
            self.assertEqual(result["status"], "fail")
            self.assertEqual(result["failure"]["code"], "forbidden-effect")


if __name__ == "__main__":
    unittest.main()
