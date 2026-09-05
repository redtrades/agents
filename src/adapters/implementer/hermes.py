"""Fail-closed, local-only Hermes implementer adapter."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Mapping, Sequence


COMMAND_ENV = "AGENT_PLATFORM_HERMES_COMMAND"
REQUEST_SCHEMA = "agent-platform.phase-request/v1"
CHILD_SCHEMA = "agent-platform.child-implementer-result/v1"
RESULT_SCHEMA = "agent-platform.phase-result/v1"
_SHA = re.compile(r"^[0-9a-f]{40}$")
_FORBIDDEN = {"push", "git_push", "merge", "git_merge", "gh_write", "github_write", "pull_request", "pr"}
_SHELLS = {"sh", "bash", "zsh", "fish", "cmd", "powershell", "pwsh"}


class AdapterError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _fail(packet: Mapping[str, Any] | None, code: str, message: str) -> dict[str, Any]:
    issue = packet.get("issue") if isinstance(packet, Mapping) else None
    issue_number = issue.get("number") if isinstance(issue, Mapping) else None
    run_id = packet.get("run_id", "") if isinstance(packet, Mapping) else ""
    input_revision = packet.get("input_revision", "") if isinstance(packet, Mapping) else ""
    return {
        "schema": RESULT_SCHEMA,
        "phase": "implement",
        "status": "fail",
        "issue_number": issue_number if isinstance(issue_number, int) else None,
        "run_id": run_id if isinstance(run_id, str) else "",
        "actor_family": "hermes",
        "input_revision": input_revision if isinstance(input_revision, str) else "",
        "candidate_revision": None,
        "changed_paths": [],
        "commit_count": 0,
        "failure": {"code": code, "message": message},
    }


def _require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AdapterError("invalid-request", f"{name} is required")
    return value


def _validate_packet(packet: Any) -> dict[str, Any]:
    if not isinstance(packet, dict):
        raise AdapterError("invalid-request", "request must be an object")
    required = {
        "schema", "phase", "issue", "run_id", "cwd", "input_revision",
        "owned_paths", "objective", "acceptance_criteria", "author_family",
    }
    if set(packet) != required:
        raise AdapterError("invalid-request", "request fields are not exact")
    if packet["schema"] != REQUEST_SCHEMA or packet["phase"] != "implement":
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
    cwd = Path(_require_string(packet["cwd"], "cwd"))
    if not cwd.is_absolute() or not cwd.is_dir():
        raise AdapterError("invalid-request", "cwd must be an existing absolute directory")
    if not isinstance(packet["input_revision"], str) or not _SHA.fullmatch(packet["input_revision"]):
        raise AdapterError("invalid-request", "input revision is invalid")
    paths = packet["owned_paths"]
    if not isinstance(paths, list) or not paths or any(
        not isinstance(path, str) or not path or Path(path).is_absolute() or ".." in Path(path).parts
        for path in paths
    ) or len(set(paths)) != len(paths):
        raise AdapterError("invalid-request", "owned paths are invalid")
    _require_string(packet["objective"], "objective")
    criteria = packet["acceptance_criteria"]
    if not isinstance(criteria, list) or not criteria or any(
        not isinstance(item, str) or not item.strip() for item in criteria
    ):
        raise AdapterError("invalid-request", "acceptance criteria are invalid")
    if packet["author_family"] != "hermes":
        raise AdapterError("family-conflict", "implementer family must be hermes")
    return packet


def _argv_from_env(environment: Mapping[str, str]) -> list[str]:
    raw = environment.get(COMMAND_ENV)
    if not raw:
        raise AdapterError("missing-binding", "required Hermes command binding is missing")
    try:
        argv = json.loads(raw)
    except (TypeError, json.JSONDecodeError) as exc:
        raise AdapterError("invalid-binding", "Hermes command binding is not a JSON argv") from exc
    if not isinstance(argv, list) or not argv or any(not isinstance(item, str) or not item for item in argv):
        raise AdapterError("invalid-binding", "Hermes command binding is not a nonempty argv")
    executable = Path(argv[0]).name.lower()
    if executable in _SHELLS or any(item in {"-c", "/c", "-command", "-z", "--oneshot"} for item in argv):
        raise AdapterError("forbidden-effect", "shell interpolation and caller-supplied prompts are forbidden")
    lowered = {item.lower() for item in argv}
    if "gh" in lowered or ("git" in lowered and lowered.intersection({"push", "merge"})):
        raise AdapterError("forbidden-effect", "GitHub and remote write commands are forbidden")
    return argv


def _git(cwd: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(cwd), *args], check=False, capture_output=True, text=True, shell=False
    )
    if result.returncode != 0:
        raise AdapterError("git-failure", "required local Git check failed")
    return result.stdout.strip()


def _status_paths(cwd: Path) -> set[str]:
    result = subprocess.run(
        ["git", "-C", str(cwd), "status", "--porcelain=v1", "--untracked-files=all"],
        check=False, capture_output=True, text=True, shell=False,
    )
    if result.returncode != 0:
        raise AdapterError("git-failure", "required local Git status check failed")
    paths: set[str] = set()
    for line in result.stdout.splitlines():
        if len(line) < 4:
            raise AdapterError("git-failure", "local Git status was malformed")
        value = line[3:]
        if " -> " in value:
            paths.update(value.split(" -> ", 1))
        else:
            paths.add(value)
    return paths


def _contains_environment(raw: str, environment: Mapping[str, str]) -> bool:
    guarded = {"HOME", "HERMES_HOME", "TMPDIR"}
    values = {
        value for key, value in environment.items()
        if key in guarded or any(word in key.upper() for word in ("SECRET", "TOKEN", "KEY", "PASSWORD", "AUTH"))
    }
    return any(value and len(value) >= 8 and value in raw for value in values)


def _is_ancestor(cwd: Path, base: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(cwd), "merge-base", "--is-ancestor", base, "HEAD"],
        check=False, capture_output=True, text=True, shell=False,
    )
    return result.returncode == 0


def _commits_since(cwd: Path, base: str) -> int:
    try:
        count = int(_git(cwd, "rev-list", "--count", f"{base}..HEAD"))
    except ValueError as exc:
        raise AdapterError("git-failure", "local Git commit count was malformed") from exc
    if count < 0:
        raise AdapterError("git-failure", "local Git commit count was invalid")
    return count


def _within_owned(path: str, owned: Sequence[str]) -> bool:
    normalized = path.replace("\\", "/")
    return not Path(normalized).is_absolute() and ".." not in Path(normalized).parts and any(
        normalized == root or normalized.startswith(root.rstrip("/") + "/") for root in owned
    )


def _child_result(raw: str) -> dict[str, Any]:
    try:
        result = json.loads(raw)
    except (TypeError, json.JSONDecodeError) as exc:
        raise AdapterError("malformed-child-output", "child output was not valid JSON") from exc
    expected = {"schema", "status", "candidate_revision", "changed_paths", "commit_count", "attempts"}
    if not isinstance(result, dict) or set(result) != expected or result["schema"] != CHILD_SCHEMA:
        raise AdapterError("malformed-child-output", "child output fields were not exact")
    if result["status"] != "success":
        raise AdapterError("child-failed", "child phase did not succeed")
    if not isinstance(result["candidate_revision"], str) or not _SHA.fullmatch(result["candidate_revision"]):
        raise AdapterError("malformed-child-output", "child candidate revision was invalid")
    paths = result["changed_paths"]
    if not isinstance(paths, list) or any(not isinstance(path, str) or not path for path in paths) or len(set(paths)) != len(paths):
        raise AdapterError("malformed-child-output", "child changed paths were invalid")
    if not isinstance(result["commit_count"], int) or result["commit_count"] not in (0, 1):
        raise AdapterError("malformed-child-output", "child commit count was invalid")
    attempts = result["attempts"]
    if not isinstance(attempts, list) or any(not isinstance(item, str) for item in attempts):
        raise AdapterError("malformed-child-output", "child attempts were invalid")
    if {item.lower() for item in attempts}.intersection(_FORBIDDEN):
        raise AdapterError("forbidden-effect", "child reported a remote or merge attempt")
    return result


def _prompt(packet: Mapping[str, Any]) -> str:
    return json.dumps({
        "schema": "agent-platform.hermes-implementer-prompt/v1",
        "request": packet,
        "constraints": {
            "cwd": packet["cwd"],
            "input_revision": packet["input_revision"],
            "owned_paths": packet["owned_paths"],
            "maximum_commits": 1,
            "allowed_tools": ["terminal", "file"],
            "forbidden_effects": sorted(_FORBIDDEN),
        },
        "return_contract": {
            "schema": CHILD_SCHEMA,
            "exact_fields": ["schema", "status", "candidate_revision", "changed_paths", "commit_count", "attempts"],
            "format": "one JSON object only; no markdown or commentary",
        },
    }, sort_keys=True, separators=(",", ":"))


def execute(packet: Mapping[str, Any], environment: Mapping[str, str] | None = None) -> dict[str, Any]:
    packet_value: dict[str, Any] | None = packet if isinstance(packet, dict) else None
    try:
        packet_value = _validate_packet(packet)
        env = dict(os.environ if environment is None else environment)
        argv = _argv_from_env(env)
        cwd = Path(packet_value["cwd"]).resolve()
        cwd_identity = (cwd.stat().st_dev, cwd.stat().st_ino)
        root = Path(_git(cwd, "rev-parse", "--show-toplevel")).resolve()
        if root != cwd or _git(cwd, "rev-parse", "HEAD") != packet_value["input_revision"]:
            raise AdapterError("subject-mismatch", "implementer subject does not match input revision")
        if _status_paths(cwd):
            raise AdapterError("subject-mismatch", "implementer workspace was not clean")
        child = subprocess.run(
            [*argv, "-z", _prompt(packet_value)], cwd=str(cwd), env=env,
            capture_output=True, text=True, check=False, shell=False,
        )
        if child.returncode != 0:
            raise AdapterError("child-failed", "child process failed")
        if _contains_environment(child.stdout, env):
            raise AdapterError("credential-leak", "child output contained an environment value")
        result = _child_result(child.stdout)
        if (cwd.stat().st_dev, cwd.stat().st_ino) != cwd_identity:
            raise AdapterError("subject-mismatch", "cwd identity changed")
        if Path(_git(cwd, "rev-parse", "--show-toplevel")).resolve() != cwd:
            raise AdapterError("subject-mismatch", "Git subject root changed")
        candidate = _git(cwd, "rev-parse", "HEAD")
        if candidate != result["candidate_revision"]:
            raise AdapterError("subject-mismatch", "child candidate does not match local HEAD")
        commit_count = _commits_since(cwd, packet_value["input_revision"])
        if not _is_ancestor(cwd, packet_value["input_revision"]):
            raise AdapterError("subject-mismatch", "candidate is not based on the input revision")
        if commit_count > 1 or commit_count != result["commit_count"]:
            raise AdapterError("forbidden-effect", "implementer commit bound was exceeded or mismatched")
        dirty_paths = _status_paths(cwd)
        if dirty_paths:
            raise AdapterError("forbidden-effect", "implementer left uncommitted changes")
        changed_paths = set(
            path for path in _git(cwd, "diff", "--name-only", packet_value["input_revision"], "HEAD").splitlines() if path
        )
        if set(result["changed_paths"]) != changed_paths or any(
            not _within_owned(path, packet_value["owned_paths"]) for path in changed_paths
        ):
            raise AdapterError("forbidden-effect", "changed paths exceeded the admitted scope")
        return {
            "schema": RESULT_SCHEMA,
            "phase": "implement",
            "status": "success",
            "issue_number": packet_value["issue"]["number"],
            "run_id": packet_value["run_id"],
            "actor_family": "hermes",
            "input_revision": packet_value["input_revision"],
            "candidate_revision": candidate,
            "changed_paths": sorted(changed_paths),
            "commit_count": commit_count,
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
