"""Contract tests for the Codex-family read-only reviewer adapter."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from src.adapters.reviewer.codex import AdapterError, _argv_from_env, execute


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
    (repo / "candidate.txt").write_text("candidate\n", encoding="utf-8")
    git("add", "candidate.txt", cwd=repo)
    git("commit", "-m", "candidate", cwd=repo)
    return repo, git("rev-parse", "HEAD", cwd=repo)


def fake_child(root: Path, body: str) -> str:
    script = root / "fake-child.py"
    script.write_text(body, encoding="utf-8")
    return json.dumps([sys.executable, str(script)])


def packet(repo: Path, candidate: str, **overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "schema": "agent-platform.phase-request/v1",
        "phase": "review",
        "issue": {"number": 9, "url": "https://github.com/redtrades/agent-platform/issues/9"},
        "run_id": "codex-run-1",
        "reviewer_run_id": "review-run-1",
        "cwd": str(repo),
        "candidate_sha": candidate,
        "reviewer_family": "codex",
        "author_family": "claude",
        "acceptance_criteria": ["Candidate meets the issue contract."],
    }
    value.update(overrides)
    return value


def env(command: str) -> dict[str, str]:
    return {
        "AGENT_PLATFORM_CODEX_COMMAND": command,
        "AGENT_PLATFORM_CODEX_CREDENTIAL_REF": "secret://codex-test",
    }


class CodexReviewerTests(unittest.TestCase):
    def test_committed_child_result_schema_matches_the_typed_adapter_contract(self):
        schema_path = REPOSITORY_ROOT / "src" / "adapters" / "reviewer" / "child-review-result.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(schema["type"], "object")
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["required"]), {
            "schema", "verdict", "candidate_sha", "reviewer_run_id", "reviewer_family",
            "author_family", "findings", "acceptance_evidence", "attempts",
        })
        self.assertEqual(schema["properties"]["schema"]["const"], "agent-platform.child-review-result/v1")
        self.assertEqual(schema["properties"]["verdict"]["enum"], ["pass", "needs-fix", "reject"])
        self.assertEqual(schema["properties"]["candidate_sha"]["pattern"], "^[0-9a-f]{40}$")
        self.assertFalse(schema["properties"]["findings"]["items"]["additionalProperties"])
        self.assertFalse(schema["properties"]["acceptance_evidence"]["items"]["additionalProperties"])

    def test_module_entrypoint_emits_strict_json(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, candidate = make_repo(root)
            command = fake_child(root, f"""
import json
print(json.dumps({{'schema': 'agent-platform.child-review-result/v1', 'verdict': 'pass',
                  'candidate_sha': '{candidate}', 'reviewer_run_id': 'review-run-1',
                  'reviewer_family': 'codex', 'author_family': 'claude',
                  'findings': [], 'acceptance_evidence': [
                      {{'criterion': 'Candidate meets the issue contract.', 'candidate_sha': '{candidate}'}}],
                  'attempts': []}}))
""")
            process = subprocess.run(
                [sys.executable, "-m", "src.adapters.reviewer"],
                cwd=REPOSITORY_ROOT,
                input=json.dumps(packet(repo, candidate)),
                capture_output=True,
                text=True,
                env={**os.environ, **env(command)},
            )
            self.assertEqual(process.returncode, 0)
            result = json.loads(process.stdout)
            self.assertEqual(result["schema"], "agent-platform.review-result/v1")
            self.assertEqual(result["candidate_sha"], candidate)

    def test_reviews_exact_candidate_with_distinct_families_and_bindings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, candidate = make_repo(root)
            command = fake_child(root, f"""
import json
print(json.dumps({{'schema': 'agent-platform.child-review-result/v1', 'verdict': 'pass',
                  'candidate_sha': '{candidate}', 'reviewer_run_id': 'review-run-1',
                  'reviewer_family': 'codex', 'author_family': 'claude',
                  'findings': [], 'acceptance_evidence': [
                      {{'criterion': 'Candidate meets the issue contract.', 'candidate_sha': '{candidate}'}}],
                  'attempts': []}}))
""")

            result = execute(packet(repo, candidate), env(command))

            self.assertEqual(result, {
                "schema": "agent-platform.review-result/v1",
                "phase": "review",
                "status": "success",
                "issue_number": 9,
                "candidate_sha": candidate,
                "reviewer_run_id": "review-run-1",
                "reviewer_family": "codex",
                "author_family": "claude",
                "verdict": "pass",
                "findings": [],
                "acceptance_evidence": [{"criterion": "Candidate meets the issue contract.", "candidate_sha": candidate}],
                "independence": None,
                "failure": None,
            })

    def test_same_codex_family_requires_distinct_run_and_reports_reduced_independence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, candidate = make_repo(root)
            command = fake_child(root, f"""
import json
print(json.dumps({{'schema': 'agent-platform.child-review-result/v1', 'verdict': 'pass',
                  'candidate_sha': '{candidate}', 'reviewer_run_id': 'review-run-1',
                  'reviewer_family': 'codex', 'author_family': 'other:codex-implementer',
                  'findings': [], 'acceptance_evidence': [
                      {{'criterion': 'Candidate meets the issue contract.', 'candidate_sha': '{candidate}'}}],
                  'attempts': []}}))
""")
            result = execute(packet(repo, candidate, author_family="other:codex-implementer"), env(command))
            self.assertEqual(result["status"], "success", result)
            self.assertEqual(result["independence"], {
                "level": "reduced",
                "distinct_principal": False,
                "reason": "same Codex family with a distinct run and ephemeral context; not distinct-principal proof",
            })
            denied = execute(packet(
                repo, candidate, author_family="other:codex-implementer", reviewer_run_id="codex-run-1",
            ), env(command))
            self.assertEqual(denied["failure"]["code"], "family-conflict")

    def test_requires_exact_bindings_and_rejects_same_family(self):
        with tempfile.TemporaryDirectory() as directory:
            repo, candidate = make_repo(Path(directory))
            command = json.dumps([sys.executable, "missing.py"])
            for overrides in (
                {"reviewer_family": "claude"},
                {"author_family": "codex"},
            ):
                result = execute(packet(repo, candidate, **overrides), env(command))
                self.assertEqual(result["status"], "fail")
                self.assertEqual(result["failure"]["code"], "family-conflict")

    def test_allows_only_the_controller_generated_codex_provider_configuration(self):
        safe = [
            "codex", "exec",
            "-c", 'model_provider="freellmapi"',
            "-c", 'model_providers.freellmapi.name="FreeLLMAPI"',
            "-c", 'model_providers.freellmapi.base_url="http://127.0.0.1:3100/v1"',
            "-c", 'model_providers.freellmapi.wire_api="responses"',
            "-c", 'model_providers.freellmapi.env_key="FREELLMAPI_API_KEY"',
            "-c", "model_providers.freellmapi.requires_openai_auth=false",
            "-",
        ]
        self.assertEqual(_argv_from_env(env(json.dumps(safe))), safe)

        for unsafe in (
            [*safe[:-1], "-c", 'shell_environment_policy.inherit="all"', "-"],
            [
                "codex", "exec",
                "-c", 'model_provider="freellmapi"',
                "-c", 'model_providers.freellmapi.base_url="http://localhost:3100/v1"',
                "-",
            ],
            ["bash", "-c", "echo unsafe"],
        ):
            with self.assertRaises(AdapterError):
                _argv_from_env(env(json.dumps(unsafe)))

    def test_missing_binding_malformed_output_and_candidate_drift_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, candidate = make_repo(root)
            missing = execute(packet(repo, candidate), {"AGENT_PLATFORM_CODEX_COMMAND": "[]"})
            self.assertEqual(missing["failure"]["code"], "missing-binding")

            malformed_command = fake_child(root, "print('malformed secret=must-not-escape')")
            malformed = execute(packet(repo, candidate), env(malformed_command))
            self.assertEqual(malformed["failure"]["code"], "malformed-child-output")
            self.assertNotIn("must-not-escape", json.dumps(malformed))

            drift_command = fake_child(root, """
import json
print(json.dumps({'schema': 'agent-platform.child-review-result/v1', 'verdict': 'pass',
                  'candidate_sha': '1' * 40, 'reviewer_run_id': 'review-run-1',
                  'reviewer_family': 'codex', 'author_family': 'claude',
                  'findings': [], 'acceptance_evidence': [], 'attempts': []}))
""")
            drift = execute(packet(repo, candidate), env(drift_command))
            self.assertEqual(drift["failure"]["code"], "subject-mismatch")

    def test_rejects_child_write_attempt_and_detects_git_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, candidate = make_repo(root)
            command = fake_child(root, """
import json
from pathlib import Path
Path('reviewer-wrote.txt').write_text('bad', encoding='utf-8')
print(json.dumps({'schema': 'agent-platform.child-review-result/v1', 'verdict': 'needs-fix',
                  'candidate_sha': 'CANDIDATE', 'reviewer_run_id': 'review-run-1',
                  'reviewer_family': 'codex', 'author_family': 'claude',
                  'findings': [{'path': 'candidate.txt', 'line': 1, 'description': 'bad'}], 'acceptance_evidence': [],
                  'attempts': ['write']}))
""".replace("CANDIDATE", candidate))
            result = execute(packet(repo, candidate), env(command))
            self.assertEqual(result["status"], "fail")
            self.assertEqual(result["failure"]["code"], "forbidden-effect")

    def test_rejects_credential_reference_in_child_findings_without_echoing_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, candidate = make_repo(root)
            command = fake_child(root, """
import json
print(json.dumps({'schema': 'agent-platform.child-review-result/v1', 'verdict': 'needs-fix',
                  'candidate_sha': 'CANDIDATE', 'reviewer_run_id': 'review-run-1',
                  'reviewer_family': 'codex', 'author_family': 'claude',
                  'findings': [{'path': 'candidate.txt', 'line': 1,
                                'description': 'secret://codex-test'}], 'acceptance_evidence': [], 'attempts': []}))
""".replace("CANDIDATE", candidate))
            result = execute(packet(repo, candidate), env(command))
            self.assertEqual(result["status"], "fail")
            self.assertEqual(result["failure"]["code"], "credential-leak")
            self.assertNotIn("secret://codex-test", json.dumps(result))


if __name__ == "__main__":
    unittest.main()
