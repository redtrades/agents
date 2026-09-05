#!/usr/bin/env python3

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from src.adapters.implementer.opencode import execute


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def make_repo(root: Path) -> tuple[Path, str]:
    repo = root / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.name", "fixture")
    git(repo, "config", "user.email", "fixture@example.invalid")
    (repo / "owned.txt").write_text("base\n", encoding="utf-8")
    git(repo, "add", "owned.txt")
    git(repo, "commit", "-qm", "base")
    return repo, git(repo, "rev-parse", "HEAD")


def packet(repo: Path, base: str) -> dict:
    return {
        "schema": "agent-platform.phase-request/v1",
        "phase": "implement",
        "issue": {"number": 203, "url": "https://github.com/redtrades/agent-platform/issues/203"},
        "run_id": "gate-c-opencode-implementer-01",
        "cwd": str(repo),
        "input_revision": base,
        "owned_paths": ["owned.txt"],
        "objective": "Make the bounded fixture change.",
        "acceptance_criteria": ["owned.txt is committed exactly once"],
        "author_family": "opencode",
    }


def fake_child(root: Path, body: str) -> str:
    path = root / "fake_opencode.py"
    header = textwrap.dedent(f"""
        import json
        from pathlib import Path
        import subprocess
        import sys

        argv = sys.argv[1:]
        assert argv[:10] == [
            'run', '--pure', '--format', 'json', '--agent', 'build',
            '--model', 'freellmapi/auto:notrain', '--dir', {json.dumps(str(root / 'repo'))},
        ]
        prompt = json.loads(argv[10])
        assert prompt['request']['cwd'] == {json.dumps(str(root / 'repo'))}
        assert prompt['constraints']['owned_paths'] == ['owned.txt']

        def emit(result):
            print(json.dumps({{'type': 'step_start', 'part': {{'type': 'step-start'}}}}))
            print(json.dumps({{'type': 'text', 'part': {{'type': 'text', 'text': json.dumps(result)}}}}))
            print(json.dumps({{'type': 'step_finish', 'part': {{'type': 'step-finish', 'reason': 'stop'}}}}))
    """)
    path.write_text(header + textwrap.dedent(body), encoding="utf-8")
    return json.dumps([sys.executable, str(path), "run", "--pure", "--format", "json", "--agent", "build",
                       "--model", "freellmapi/auto:notrain", "--dir", str(root / "repo")])


class OpenCodeImplementerTests(unittest.TestCase):
    def test_success_reconciles_exact_one_commit_and_owned_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            command = fake_child(root, """
                cwd = Path(prompt['request']['cwd'])
                (cwd / 'owned.txt').write_text('changed\\n')
                subprocess.run(['git', '-C', str(cwd), 'add', 'owned.txt'], check=True)
                subprocess.run(['git', '-C', str(cwd), 'commit', '-qm', 'change'], check=True)
                candidate = subprocess.run(['git', '-C', str(cwd), 'rev-parse', 'HEAD'], check=True, capture_output=True, text=True).stdout.strip()
                emit({'schema': 'agent-platform.child-implementer-result/v1', 'status': 'success',
                      'candidate_revision': candidate, 'changed_paths': ['owned.txt'],
                      'commit_count': 1, 'attempts': []})
            """)
            result = execute(packet(repo, base), {"AGENT_PLATFORM_OPENCODE_COMMAND": command})
            self.assertEqual(result["status"], "success", result)
            self.assertEqual(result["actor_family"], "opencode")
            self.assertEqual(result["candidate_revision"], git(repo, "rev-parse", "HEAD"))
            self.assertEqual(result["changed_paths"], ["owned.txt"])
            self.assertEqual(result["commit_count"], 1)

    def test_missing_binding_malformed_telemetry_and_nonzero_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            result = execute(packet(repo, base), {})
            self.assertEqual(result["failure"]["code"], "missing-binding")

            malformed = fake_child(root, "print('not-json')")
            result = execute(packet(repo, base), {"AGENT_PLATFORM_OPENCODE_COMMAND": malformed})
            self.assertEqual(result["failure"]["code"], "malformed-child-output")

            telemetry_only = fake_child(root, "print(json.dumps({'type': 'step_finish', 'part': {'type': 'step-finish'}}))")
            result = execute(packet(repo, base), {"AGENT_PLATFORM_OPENCODE_COMMAND": telemetry_only})
            self.assertEqual(result["failure"]["code"], "malformed-child-output")

            failed = fake_child(root, "raise SystemExit(23)")
            result = execute(packet(repo, base), {"AGENT_PLATFORM_OPENCODE_COMMAND": failed})
            self.assertEqual(result["failure"]["code"], "child-failed")

    def test_unowned_change_and_dirty_workspace_are_denied(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            unowned = fake_child(root, """
                cwd = Path(prompt['request']['cwd'])
                (cwd / 'outside.txt').write_text('bad\\n')
                subprocess.run(['git', '-C', str(cwd), 'add', 'outside.txt'], check=True)
                subprocess.run(['git', '-C', str(cwd), 'commit', '-qm', 'bad'], check=True)
                candidate = subprocess.run(['git', '-C', str(cwd), 'rev-parse', 'HEAD'], check=True, capture_output=True, text=True).stdout.strip()
                emit({'schema': 'agent-platform.child-implementer-result/v1', 'status': 'success',
                      'candidate_revision': candidate, 'changed_paths': ['outside.txt'],
                      'commit_count': 1, 'attempts': []})
            """)
            result = execute(packet(repo, base), {"AGENT_PLATFORM_OPENCODE_COMMAND": unowned})
            self.assertEqual(result["failure"]["code"], "forbidden-effect")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            dirty = fake_child(root, """
                cwd = Path(prompt['request']['cwd'])
                (cwd / 'owned.txt').write_text('dirty\\n')
                emit({'schema': 'agent-platform.child-implementer-result/v1', 'status': 'success',
                      'candidate_revision': prompt['request']['input_revision'], 'changed_paths': ['owned.txt'],
                      'commit_count': 0, 'attempts': []})
            """)
            result = execute(packet(repo, base), {"AGENT_PLATFORM_OPENCODE_COMMAND": dirty})
            self.assertEqual(result["failure"]["code"], "forbidden-effect")

    def test_wrong_subject_and_multiple_commits_are_denied(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, _ = make_repo(root)
            result = execute(packet(repo, "f" * 40), {
                "AGENT_PLATFORM_OPENCODE_COMMAND": json.dumps([sys.executable, "missing.py"]),
            })
            self.assertEqual(result["failure"]["code"], "subject-mismatch")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            multiple = fake_child(root, """
                cwd = Path(prompt['request']['cwd'])
                for value in ('one', 'two'):
                    (cwd / 'owned.txt').write_text(value + '\\n')
                    subprocess.run(['git', '-C', str(cwd), 'add', 'owned.txt'], check=True)
                    subprocess.run(['git', '-C', str(cwd), 'commit', '-qm', value], check=True)
                candidate = subprocess.run(['git', '-C', str(cwd), 'rev-parse', 'HEAD'], check=True, capture_output=True, text=True).stdout.strip()
                emit({'schema': 'agent-platform.child-implementer-result/v1', 'status': 'success',
                      'candidate_revision': candidate, 'changed_paths': ['owned.txt'],
                      'commit_count': 1, 'attempts': []})
            """)
            result = execute(packet(repo, base), {"AGENT_PLATFORM_OPENCODE_COMMAND": multiple})
            self.assertEqual(result["failure"]["code"], "forbidden-effect")

    def test_environment_leak_is_denied_and_redacted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            leaked = fake_child(root, """
                emit({'schema': 'agent-platform.child-implementer-result/v1', 'status': 'success',
                      'candidate_revision': prompt['request']['input_revision'], 'changed_paths': [],
                      'commit_count': 0, 'attempts': [__import__('os').environ['FIXTURE_SECRET_TOKEN']]})
            """)
            result = execute(packet(repo, base), {
                "AGENT_PLATFORM_OPENCODE_COMMAND": leaked,
                "FIXTURE_SECRET_TOKEN": "never-return-this-value",
            })
            self.assertEqual(result["failure"]["code"], "credential-leak")
            self.assertNotIn("never-return-this-value", json.dumps(result))


if __name__ == "__main__":
    unittest.main()
