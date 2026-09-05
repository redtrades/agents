"""Fail-closed, read-only Codex-family exact-candidate reviewer adapter."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Mapping, Sequence


COMMAND_ENV = "AGENT_PLATFORM_CODEX_COMMAND"
CREDENTIAL_REF_ENV = "AGENT_PLATFORM_CODEX_CREDENTIAL_REF"
REQUEST_SCHEMA = "agent-platform.phase-request/v1"
CHILD_SCHEMA = "agent-platform.child-review-result/v1"
RESULT_SCHEMA = "agent-platform.review-result/v1"
_SHA = re.compile(r"^[0-9a-f]{40}$")
_FAMILIES = {"codex", "claude", "gemini"}
_SHELLS = {"sh", "bash", "zsh", "fish", "cmd", "powershell", "pwsh"}
_FORBIDDEN = {"write", "push", "git_push", "merge", "git_merge", "gh_write", "github_write", "pull_request", "pr"}
_CODEX_PROVIDER_CONFIG = (
    'model_provider="freellmapi"',
    'model_providers.freellmapi.name="FreeLLMAPI"',
    'model_providers.freellmapi.base_url="http://127.0.0.1:3100/v1"',
    'model_providers.freellmapi.wire_api="responses"',
    'model_providers.freellmapi.env_key="FREELLMAPI_API_KEY"',
    "model_providers.freellmapi.requires_openai_auth=false",
)
_CODEX_IMPLEMENTER_FAMILY = "other:codex-implementer"
_REDUCED_INDEPENDENCE = {
    "level": "reduced",
    "distinct_principal": False,
    "reason": "same Codex family with a distinct run and ephemeral context; not distinct-principal proof",
}


class AdapterError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _fail(packet: Mapping[str, Any] | None, code: str, message: str) -> dict[str, Any]:
    issue = packet.get("issue") if isinstance(packet, Mapping) else None
    issue_number = issue.get("number") if isinstance(issue, Mapping) else None
    return {
        "schema": RESULT_SCHEMA,
        "phase": "review",
        "status": "fail",
        "issue_number": issue_number if isinstance(issue_number, int) else None,
        "candidate_sha": packet.get("candidate_sha") if isinstance(packet, Mapping) and isinstance(packet.get("candidate_sha"), str) else None,
        "reviewer_run_id": packet.get("reviewer_run_id") if isinstance(packet, Mapping) and isinstance(packet.get("reviewer_run_id"), str) else "",
        "reviewer_family": "codex",
        "author_family": packet.get("author_family") if isinstance(packet, Mapping) and isinstance(packet.get("author_family"), str) else "",
        "verdict": None,
        "findings": [],
        "independence": _REDUCED_INDEPENDENCE if isinstance(packet, Mapping) and packet.get("author_family") == _CODEX_IMPLEMENTER_FAMILY else None,
        "failure": {"code": code, "message": message},
    }


def _require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AdapterError("invalid-request", f"{name} is required")
    return value


def _family(value: Any) -> bool:
    return isinstance(value, str) and (value in _FAMILIES or (value.startswith("other:") and len(value) > 6))


def _validate_packet(packet: Any) -> dict[str, Any]:
    if not isinstance(packet, dict):
        raise AdapterError("invalid-request", "request must be an object")
    required = {
        "schema", "phase", "issue", "run_id", "reviewer_run_id", "cwd",
        "candidate_sha", "reviewer_family", "author_family", "acceptance_criteria",
    }
    if set(packet) != required:
        raise AdapterError("invalid-request", "request fields are not exact")
    if packet["schema"] != REQUEST_SCHEMA or packet["phase"] != "review":
        raise AdapterError("invalid-request", "request schema or phase is invalid")
    issue = packet["issue"]
    if not isinstance(issue, dict) or set(issue) != {"number", "url"}:
        raise AdapterError("invalid-request", "issue binding is invalid")
    if not isinstance(issue["number"], int) or issue["number"] < 1:
        raise AdapterError("invalid-request", "issue number is invalid")
    if not isinstance(issue["url"], str) or not re.fullmatch(
        rf"https://github\.com/[^/]+/[^/]+/issues/{issue['number']}", issue["url"]
    ):
        raise AdapterError("invalid-request", "issue URL is invalid")
    _require_string(packet["run_id"], "run_id")
    _require_string(packet["reviewer_run_id"], "reviewer_run_id")
    if packet["run_id"] == packet["reviewer_run_id"]:
        raise AdapterError("family-conflict", "reviewer run and implementer run must differ")
    cwd = Path(_require_string(packet["cwd"], "cwd"))
    if not cwd.is_absolute() or not cwd.is_dir():
        raise AdapterError("invalid-request", "cwd must be an existing absolute directory")
    if not isinstance(packet["candidate_sha"], str) or not _SHA.fullmatch(packet["candidate_sha"]):
        raise AdapterError("invalid-request", "candidate SHA is invalid")
    if packet["reviewer_family"] != "codex" or not _family(packet["reviewer_family"]):
        raise AdapterError("family-conflict", "reviewer family must be codex")
    if not _family(packet["author_family"]):
        raise AdapterError("invalid-request", "author family is invalid")
    if packet["author_family"] == packet["reviewer_family"]:
        raise AdapterError("family-conflict", "reviewer and author families must differ")
    criteria = packet["acceptance_criteria"]
    if not isinstance(criteria, list) or not criteria or any(not isinstance(item, str) or not item.strip() for item in criteria):
        raise AdapterError("invalid-request", "acceptance criteria are invalid")
    return packet


def _argv_from_env(environment: Mapping[str, str], cwd: Path | None = None) -> list[str]:
    raw = environment.get(COMMAND_ENV)
    credential = environment.get(CREDENTIAL_REF_ENV)
    if not raw or not credential:
        raise AdapterError("missing-binding", "required family binding is missing")
    if not credential.startswith("secret://"):
        raise AdapterError("invalid-binding", "credential binding is not opaque")
    try:
        argv = json.loads(raw)
    except (TypeError, json.JSONDecodeError) as exc:
        raise AdapterError("invalid-binding", "command binding is not a JSON argv") from exc
    if not isinstance(argv, list) or not argv or any(not isinstance(item, str) or not item for item in argv):
        raise AdapterError("invalid-binding", "command binding is not a nonempty argv")
    executable = Path(argv[0]).name.lower()
    if executable in _SHELLS or any(item in {"/c", "-command"} for item in argv):
        raise AdapterError("forbidden-effect", "shell interpolation is forbidden")
    _validate_codex_provider_config(argv, executable)
    if credential == "secret://codex-host-auth":
        expected = [
            "-a", "never", "exec", "--ignore-user-config", "--ignore-rules",
            "--strict-config", "--ephemeral", "-C", str(cwd), "-s", "read-only",
            "--output-schema",
        ]
        if cwd is None or executable != "codex" or argv[1:len(expected) + 1] != expected or \
                len(argv) != len(expected) + 3 or argv[-1] != "-":
            raise AdapterError("forbidden-effect", "Codex reviewer command is not the controller-generated read-only argv")
    lowered = {item.lower() for item in argv}
    if "gh" in lowered or ("git" in lowered and lowered.intersection({"push", "merge"})):
        raise AdapterError("forbidden-effect", "GitHub and repository writes are forbidden")
    return argv


def _validate_codex_provider_config(argv: Sequence[str], executable: str) -> None:
    values: list[str] = []
    index = 0
    while index < len(argv):
        option = argv[index]
        if option == "-c":
            if index + 1 >= len(argv):
                raise AdapterError("forbidden-effect", "untrusted Codex configuration is forbidden")
            values.append(argv[index + 1])
            index += 2
            continue
        if option == "--config" or option.startswith("--config=") or option.startswith("-c"):
            raise AdapterError("forbidden-effect", "untrusted Codex configuration is forbidden")
        index += 1
    if values and (executable != "codex" or tuple(values) != _CODEX_PROVIDER_CONFIG):
        raise AdapterError("forbidden-effect", "untrusted Codex configuration is forbidden")


def _git(cwd: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(cwd), *args], check=False, capture_output=True, text=True, shell=False,
    )
    if result.returncode != 0:
        raise AdapterError("git-failure", "required local Git check failed")
    return result.stdout.strip()


def _status(cwd: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(cwd), "status", "--porcelain=v1", "--untracked-files=all"],
        check=False, capture_output=True, text=True, shell=False,
    )
    if result.returncode != 0:
        raise AdapterError("git-failure", "required local Git status check failed")
    return result.stdout


def _contains_credential(raw: str, environment: Mapping[str, str]) -> bool:
    values = {
        value for key, value in {**os.environ, **dict(environment)}.items()
        if key == CREDENTIAL_REF_ENV
        or any(word in key.upper() for word in ("SECRET", "TOKEN", "KEY", "PASSWORD", "AUTH"))
    }
    return any(value and len(value) >= 8 and value in raw for value in values)


def _child_result(raw: str, packet: Mapping[str, Any]) -> dict[str, Any]:
    try:
        result = json.loads(raw)
    except (TypeError, json.JSONDecodeError) as exc:
        raise AdapterError("malformed-child-output", "child output was not valid JSON") from exc
    expected = {"schema", "verdict", "candidate_sha", "reviewer_run_id", "reviewer_family", "author_family", "findings", "acceptance_evidence", "attempts"}
    if not isinstance(result, dict) or set(result) != expected or result["schema"] != CHILD_SCHEMA:
        raise AdapterError("malformed-child-output", "child output fields were not exact")
    if result["verdict"] not in {"pass", "needs-fix", "reject"}:
        raise AdapterError("malformed-child-output", "child verdict was invalid")
    for key in ("candidate_sha",):
        if not isinstance(result[key], str) or not _SHA.fullmatch(result[key]):
            raise AdapterError("malformed-child-output", "child binding was invalid")
    if result["candidate_sha"] != packet["candidate_sha"] or result["reviewer_run_id"] != packet["reviewer_run_id"] or result["reviewer_family"] != packet["reviewer_family"] or result["author_family"] != packet["author_family"]:
        raise AdapterError("subject-mismatch", "child review bindings do not match the admitted subject")
    findings = result["findings"]
    if not isinstance(findings, list) or any(
        not isinstance(item, dict) or set(item) != {"path", "line", "description"}
        or not isinstance(item["path"], str) or not item["path"] or Path(item["path"]).is_absolute() or ".." in Path(item["path"]).parts
        or not isinstance(item["line"], int) or item["line"] < 1
        or not isinstance(item["description"], str) or not item["description"].strip()
        for item in findings
    ):
        raise AdapterError("malformed-child-output", "child findings were invalid")
    if result["verdict"] == "pass" and findings:
        raise AdapterError("malformed-child-output", "passing review cannot contain findings")
    if result["verdict"] != "pass" and not findings:
        raise AdapterError("malformed-child-output", "non-passing review requires findings")
    attempts = result["attempts"]
    if not isinstance(attempts, list) or any(not isinstance(item, str) for item in attempts):
        raise AdapterError("malformed-child-output", "child attempts were invalid")
    if {item.lower() for item in attempts}.intersection(_FORBIDDEN):
        raise AdapterError("forbidden-effect", "child reported a write or merge attempt")
    evidence = result["acceptance_evidence"]
    criteria = packet["acceptance_criteria"]
    if not isinstance(evidence, list) or any(
        not isinstance(item, dict) or set(item) != {"criterion", "candidate_sha"}
        or item["criterion"] != criterion
        or item["candidate_sha"] != packet["candidate_sha"]
        for item, criterion in zip(evidence, criteria)
    ) or (result["verdict"] == "pass" and len(evidence) != len(criteria)):
        raise AdapterError("incomplete-evidence", "child acceptance evidence was incomplete")
    return result


def execute(packet: Mapping[str, Any], environment: Mapping[str, str] | None = None) -> dict[str, Any]:
    """Run one read-only Codex review and always return a typed, redacted result."""
    packet_value: dict[str, Any] | None = packet if isinstance(packet, dict) else None
    try:
        packet_value = _validate_packet(packet)
        env = os.environ if environment is None else environment
        cwd = Path(packet_value["cwd"]).resolve()
        argv = _argv_from_env(env, cwd)
        cwd_identity = (cwd.stat().st_dev, cwd.stat().st_ino)
        if Path(_git(cwd, "rev-parse", "--show-toplevel")).resolve() != cwd:
            raise AdapterError("subject-mismatch", "review cwd is not the Git subject root")
        if _git(cwd, "rev-parse", "HEAD") != packet_value["candidate_sha"] or _status(cwd):
            raise AdapterError("subject-mismatch", "review workspace is not the exact clean candidate")
        prompt = json.dumps({**packet_value, "mode": "read-only"}, sort_keys=True, separators=(",", ":"))
        child = subprocess.run(
            argv, cwd=str(cwd), env={**os.environ, **dict(env)}, input=prompt,
            capture_output=True, text=True, check=False, shell=False,
        )
        if child.returncode != 0:
            raise AdapterError("child-failed", "child process failed")
        if _contains_credential(child.stdout, env):
            raise AdapterError("credential-leak", "child output contained a credential")
        result = _child_result(child.stdout, packet_value)
        if (cwd.stat().st_dev, cwd.stat().st_ino) != cwd_identity:
            raise AdapterError("subject-mismatch", "review cwd identity changed")
        if _git(cwd, "rev-parse", "HEAD") != packet_value["candidate_sha"] or _status(cwd):
            raise AdapterError("forbidden-effect", "reviewer changed the candidate workspace")
        return {
            "schema": RESULT_SCHEMA,
            "phase": "review",
            "status": "success",
            "issue_number": packet_value["issue"]["number"],
            "candidate_sha": packet_value["candidate_sha"],
            "reviewer_run_id": packet_value["reviewer_run_id"],
            "reviewer_family": "codex",
            "author_family": packet_value["author_family"],
            "verdict": result["verdict"],
            "findings": result["findings"],
            "acceptance_evidence": result["acceptance_evidence"],
            "independence": _REDUCED_INDEPENDENCE if packet_value["author_family"] == _CODEX_IMPLEMENTER_FAMILY else None,
            "failure": None,
        }
    except AdapterError as exc:
        return _fail(packet_value, exc.code, exc.message)
    except (OSError, subprocess.SubprocessError):
        return _fail(packet_value, "child-failure", "phase process could not be executed")


def main(argv: Sequence[str] | None = None) -> int:
    del argv
    try:
        raw = sys.stdin.read()
        request = json.loads(raw) if raw.strip() else json.loads(os.environ.get("AGENT_PLATFORM_PACKET_JSON", ""))
    except (json.JSONDecodeError, OSError):
        result = _fail(None, "malformed-request", "request was not valid JSON")
    else:
        result = execute(request)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
