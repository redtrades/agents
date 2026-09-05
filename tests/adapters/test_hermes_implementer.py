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

from src.adapters.implementer.hermes import execute


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
        "issue": {"number": 199, "url": "https://github.com/redtrades/agent-platform/issues/199"},
        "run_id": "gate-c-hermes-implementer-01",
        "cwd": str(repo),
        "input_revision": base,
        "owned_paths": ["owned.txt"],
        "objective": "Make the bounded fixture change.",
        "acceptance_criteria": ["owned.txt is committed exactly once"],
        "author_family": "hermes",
    }


def fake_child(root: Path, body: str) -> str:
    path = root / "fake_hermes.py"
    header = textwrap.dedent(f"""
        import json
        from pathlib import Path
        import subprocess
        import sys

        argv = sys.argv[1:]
        assert argv[:8] == [
            '--in', {json.dumps(str(root / 'repo'))},
            '--provider', 'gate_c_local',
            '--model', 'Qwen3.8-Flash-Next-AD-3.84bpw-IQ4_XS-M64',
            '--toolsets', 'terminal,file',
        ]
        assert argv[8] == '--ignore-rules'
        assert argv[9] == '-z'
        prompt = json.loads(argv[10])
        assert prompt['request']['cwd'] == {json.dumps(str(root / 'repo'))}
        assert prompt['constraints']['owned_paths'] == ['owned.txt']
    """)
    path.write_text(header + textwrap.dedent(body), encoding="utf-8")
    return json.dumps([
        sys.executable, str(path),
        "--in", str(root / "repo"),
        "--provider", "gate_c_local",
        "--model", "Qwen3.8-Flash-Next-AD-3.84bpw-IQ4_XS-M64",
        "--toolsets", "terminal,file",
        "--ignore-rules",
    ])


class HermesImplementerTests(unittest.TestCase):
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
                print(json.dumps({'schema': 'agent-platform.child-implementer-result/v1', 'status': 'success',
                                  'candidate_revision': candidate, 'changed_paths': ['owned.txt'],
                                  'commit_count': 1, 'attempts': []}))
            """)
            result = execute(packet(repo, base), {"AGENT_PLATFORM_HERMES_COMMAND": command})
            self.assertEqual(result["status"], "success", result)
            self.assertEqual(result["actor_family"], "hermes")
            self.assertEqual(result["candidate_revision"], git(repo, "rev-parse", "HEAD"))
            self.assertEqual(result["changed_paths"], ["owned.txt"])
            self.assertEqual(result["commit_count"], 1)

    def test_malformed_and_nonzero_child_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            malformed = fake_child(root, "print('not-json')")
            result = execute(packet(repo, base), {"AGENT_PLATFORM_HERMES_COMMAND": malformed})
            self.assertEqual(result["failure"]["code"], "malformed-child-output")

            failed = fake_child(root, "raise SystemExit(23)")
            result = execute(packet(repo, base), {"AGENT_PLATFORM_HERMES_COMMAND": failed})
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
                print(json.dumps({'schema': 'agent-platform.child-implementer-result/v1', 'status': 'success',
                                  'candidate_revision': candidate, 'changed_paths': ['outside.txt'],
                                  'commit_count': 1, 'attempts': []}))
            """)
            result = execute(packet(repo, base), {"AGENT_PLATFORM_HERMES_COMMAND": unowned})
            self.assertEqual(result["failure"]["code"], "forbidden-effect")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            dirty = fake_child(root, """
                cwd = Path(prompt['request']['cwd'])
                (cwd / 'owned.txt').write_text('dirty\\n')
                print(json.dumps({'schema': 'agent-platform.child-implementer-result/v1', 'status': 'success',
                                  'candidate_revision': prompt['request']['input_revision'],
                                  'changed_paths': ['owned.txt'], 'commit_count': 0, 'attempts': []}))
            """)
            result = execute(packet(repo, base), {"AGENT_PLATFORM_HERMES_COMMAND": dirty})
            self.assertEqual(result["failure"]["code"], "forbidden-effect")

    def test_subject_mismatch_and_multi_commit_are_denied(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            wrong = packet(repo, "f" * 40)
            result = execute(wrong, {"AGENT_PLATFORM_HERMES_COMMAND": json.dumps([sys.executable, "missing.py"])})
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
                print(json.dumps({'schema': 'agent-platform.child-implementer-result/v1', 'status': 'success',
                                  'candidate_revision': candidate, 'changed_paths': ['owned.txt'],
                                  'commit_count': 2, 'attempts': []}))
            """)
            result = execute(packet(repo, base), {"AGENT_PLATFORM_HERMES_COMMAND": multiple})
            self.assertIn(result["failure"]["code"], {"malformed-child-output", "forbidden-effect"})

    def test_environment_leak_is_denied_and_redacted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, base = make_repo(root)
            leaked = fake_child(root, """
                print(json.dumps({'schema': 'agent-platform.child-implementer-result/v1', 'status': 'success',
                                  'candidate_revision': prompt['request']['input_revision'], 'changed_paths': [],
                                  'commit_count': 0, 'attempts': [__import__('os').environ['FIXTURE_SECRET_TOKEN']]}))
            """)
            result = execute(packet(repo, base), {
                "AGENT_PLATFORM_HERMES_COMMAND": leaked,
                "FIXTURE_SECRET_TOKEN": "never-return-this-value",
            })
            self.assertEqual(result["failure"]["code"], "credential-leak")
            self.assertNotIn("never-return-this-value", json.dumps(result))


if __name__ == "__main__":
    unittest.main()
