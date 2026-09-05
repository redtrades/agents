"""Fail-closed Codex implementer adapter with deterministic Git reconciliation."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Mapping, Sequence

if __package__ in (None, ""):
    _repo_root = str(Path(__file__).resolve().parents[3])
    if _repo_root not in sys.path:
        sys.path.insert(0, _repo_root)

try:
    from .opencode import (
        AdapterError,
        _git,
        _status_paths,
        _validate_packet as _validate_common_packet,
        _within_owned,
    )
except (ImportError, ValueError):
    from src.adapters.implementer.opencode import (
        AdapterError,
        _git,
        _status_paths,
        _validate_packet as _validate_common_packet,
        _within_owned,
    )


COMMAND_ENV = "AGENT_PLATFORM_CODEX_COMMAND"
CREDENTIAL_REF_ENV = "AGENT_PLATFORM_CODEX_CREDENTIAL_REF"
CHILD_SCHEMA = "agent-platform.child-implementer-result/v1"
RESULT_SCHEMA = "agent-platform.phase-result/v1"
AUTHOR_FAMILY = "other:codex-implementer"
_RUN_ID = re.compile(r"^[a-z0-9][a-z0-9-]{7,63}$")
_FORBIDDEN = {"push", "git_push", "merge", "git_merge", "gh_write", "github_write", "pull_request", "pr"}
_CONTROLLER_ACTOR = "agent/mvp-one-shot"


def _fail(
    packet: Mapping[str, Any] | None, code: str, message: str, diagnostic: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    issue = packet.get("issue") if isinstance(packet, Mapping) else None
    issue_number = issue.get("number") if isinstance(issue, Mapping) else None
    failure: dict[str, Any] = {"code": code, "message": message}
    if diagnostic is not None:
        failure["diagnostic"] = dict(diagnostic)
    return {
        "schema": RESULT_SCHEMA,
        "phase": "implement",
        "status": "fail",
        "issue_number": issue_number if isinstance(issue_number, int) else None,
        "run_id": packet.get("run_id", "") if isinstance(packet, Mapping) else "",
        "actor_family": AUTHOR_FAMILY,
        "input_revision": packet.get("input_revision", "") if isinstance(packet, Mapping) else "",
        "candidate_revision": None,
        "changed_paths": [],
        "commit_count": 0,
        "failure": failure,
    }


def _validate_packet(packet: Any) -> dict[str, Any]:
    if not isinstance(packet, dict) or packet.get("author_family") != AUTHOR_FAMILY:
        raise AdapterError("family-conflict", "implementer family must be the bounded Codex implementer role")
    common = {**packet, "author_family": "opencode"}
    _validate_common_packet(common)
    return packet


def _argv_from_env(environment: Mapping[str, str], cwd: Path) -> list[str]:
    raw = environment.get(COMMAND_ENV)
    reference = environment.get(CREDENTIAL_REF_ENV)
    if not raw or not reference:
        raise AdapterError("missing-binding", "required Codex bindings are missing")
    if reference != "secret://codex-host-auth":
        raise AdapterError("invalid-binding", "Codex authentication reference is not admitted")
    try:
        argv = json.loads(raw)
    except (TypeError, json.JSONDecodeError) as exc:
        raise AdapterError("invalid-binding", "Codex command binding is not a JSON argv") from exc
    expected = [
        "-a", "never", "exec", "--ignore-user-config", "--ignore-rules",
        "--strict-config", "--ephemeral", "-C", str(cwd), "-s", "workspace-write", "-",
    ]
    if not isinstance(argv, list) or not argv or Path(str(argv[0])).name != "codex" or argv[1:] != expected:
        raise AdapterError("forbidden-effect", "Codex command binding is not the controller-generated workspace-write argv")
    return argv


def _contains_environment(raw: str, environment: Mapping[str, str]) -> bool:
    values = {
        value for key, value in environment.items()
        if key in {"HOME", "TMPDIR", "CODEX_HOME", CREDENTIAL_REF_ENV}
        or any(word in key.upper() for word in ("SECRET", "TOKEN", "KEY", "PASSWORD", "AUTH", "CREDENTIAL"))
    }
    return any(value and len(value) >= 8 and value in raw for value in values)


def _stderr_category(stderr: str) -> str:
    value = stderr.lower()
    if any(token in value for token in ("authentication", "not logged in", "unauthorized", "forbidden", "401", "403")):
        return "authentication"
    if any(token in value for token in ("timed out", "timeout", "deadline exceeded")):
        return "timeout"
    if any(token in value for token in ("permission denied", "sandbox", "tool call", "workspace")):
        return "tool"
    if any(token in value for token in ("command not found", "no such file", "executable")):
        return "cli"
    return "unknown"


def _child_diagnostic(child: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    return {
        "child_exit_status": child.returncode,
        "stdout_sha256": hashlib.sha256(child.stdout.encode("utf-8")).hexdigest(),
        "stderr_sha256": hashlib.sha256(child.stderr.encode("utf-8")).hexdigest(),
        "stderr_category": _stderr_category(child.stderr),
    }


def _prompt(packet: Mapping[str, Any]) -> str:
    prompt_packet = {
        "schema": "agent-platform.codex-implementer-prompt/v1",
        "request": packet,
        "constraints": {
            "cwd": packet["cwd"],
            "input_revision": packet["input_revision"],
            "owned_paths": packet["owned_paths"],
            "maximum_commits": 0,
            "forbidden_effects": sorted(_FORBIDDEN),
            "github_credentials": "absent",
        },
        "execution_contract": {
            "packet": "complete-and-authoritative",
            "action": "execute-now",
            "remote_context": "do-not-access-github-network-or-refetch-issue-or-pr",
            "workspace": "use-only-admitted-local-cwd-and-local-git",
            "changes": "owned-paths-only",
            "commit": "model-must-not-commit; controller-commits-validated-paths",
            "result": "return-exact-child-envelope",
        },
        "return_contract": {
            "schema": CHILD_SCHEMA,
            "status": "success",
            "exact_fields": ["schema", "status", "candidate_revision", "changed_paths", "commit_count", "attempts"],
            "format": "one JSON object only; no markdown or commentary",
        },
    }
    instructions = (
        "Execute the task now. The JSON packet below is complete and authoritative. "
        "Use only local tools, the admitted cwd, and local Git; do not access GitHub or the network, "
        "and do not re-fetch any issue or pull request. Do not merely summarize or echo the packet. "
        "Change only owned paths. Do not create or alter Git history. The controller will commit validated edits. "
        "Return success only after edits exist, with candidate_revision equal to the current input HEAD, commit_count 0, "
        "and the exact changed paths. Then output exactly the required child JSON object and nothing else."
    )
    return f"{instructions}\n{json.dumps(prompt_packet, sort_keys=True, separators=(',', ':'))}"


def _controller_identity(cwd: Path, packet: Mapping[str, Any]) -> tuple[str, str]:
    run_id = packet["run_id"]
    if not isinstance(run_id, str) or not _RUN_ID.fullmatch(run_id):
        raise AdapterError("invalid-request", "run ID is not valid for controller Git identity")
    expected_email = f"agent+mvp-one-shot.{run_id}@agents.invalid"
    if _git(cwd, "config", "--local", "user.name") != "Agent mvp-one-shot" or \
            _git(cwd, "config", "--local", "user.email") != expected_email:
        raise AdapterError("subject-mismatch", "candidate-local Git identity is not bound to the admitted run")
    return _CONTROLLER_ACTOR, expected_email


def _git_metadata_path(cwd: Path) -> Path:
    expected = Path(f"{cwd}.git").resolve()
    actual = Path(_git(cwd, "rev-parse", "--absolute-git-dir")).resolve()
    if actual != expected or not actual.is_dir() or not (cwd / ".git").is_file():
        raise AdapterError("subject-mismatch", "candidate Git metadata is not an isolated sibling directory")
    return actual


def _digest_git_lines(cwd: Path, *args: str) -> str:
    values = sorted({value for value in _git(cwd, *args).splitlines() if value})
    return hashlib.sha256("\n".join(values).encode("utf-8")).hexdigest()


def _metadata_invariants(cwd: Path) -> dict[str, str]:
    return {
        "metadata_path": str(_git_metadata_path(cwd)),
        "head": _git(cwd, "rev-parse", "HEAD"),
        "head_ref": _git(cwd, "symbolic-ref", "-q", "HEAD"),
        "staged_digest": _digest_git_lines(cwd, "diff", "--cached", "--name-status"),
        "config_digest": _digest_git_lines(cwd, "config", "--local", "--list"),
        "refs_digest": _digest_git_lines(cwd, "show-ref", "--head"),
        "object_oid_digest": _digest_git_lines(cwd, "cat-file", "--batch-all-objects", "--batch-check=%(objectname)"),
    }


def _sanitized_git_environment() -> dict[str, str]:
    return {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}


def _controller_git(cwd: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(cwd), *args], check=False, capture_output=True, text=True,
        shell=False, env=_sanitized_git_environment(),
    )
    if result.returncode != 0:
        raise AdapterError("git-failure", "controller local Git command failed")
    return result.stdout.strip()


def _unstaged_paths(cwd: Path) -> set[str]:
    staged = {path for path in _git(cwd, "diff", "--cached", "--name-only").splitlines() if path}
    if staged:
        raise AdapterError("forbidden-effect", "model staged local paths")
    tracked = {path for path in _git(cwd, "diff", "--name-only").splitlines() if path}
    untracked = {path for path in _git(cwd, "ls-files", "--others", "--exclude-standard").splitlines() if path}
    return tracked | untracked


def _validated_workspace_edits(cwd: Path, packet: Mapping[str, Any]) -> list[str]:
    input_revision = packet["input_revision"]
    if _git(cwd, "rev-parse", "HEAD") != input_revision:
        raise AdapterError("forbidden-effect", "model altered Git history")
    paths = _unstaged_paths(cwd)
    if not paths or any(not _within_owned(path, packet["owned_paths"]) for path in paths):
        raise AdapterError("forbidden-effect", "model edits were empty, staged, or outside owned paths")
    return sorted(paths)


def _controller_commit(cwd: Path, packet: Mapping[str, Any], paths: Sequence[str]) -> None:
    actor, email = _controller_identity(cwd, packet)
    _controller_git(cwd, "add", "--", *paths)
    result = subprocess.run(
        [
            "git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgSign=false", "-C", str(cwd),
            "commit", "--no-gpg-sign", "-m", f"mvp: implement issue #{packet['issue']['number']}",
            "-m", f"Agent-Actor: {actor}\nAgent-Run-ID: {packet['run_id']}",
        ],
        check=False, capture_output=True, text=True, shell=False, env=_sanitized_git_environment(),
    )
    if result.returncode != 0:
        raise AdapterError("git-failure", "controller local commit failed")
    expected_author = f"Agent mvp-one-shot <{email}>"
    expected_message = (
        f"mvp: implement issue #{packet['issue']['number']}\n\n"
        f"Agent-Actor: {actor}\nAgent-Run-ID: {packet['run_id']}"
    )
    if _controller_git(cwd, "log", "-1", "--format=%an <%ae>") != expected_author or \
            _controller_git(cwd, "log", "-1", "--format=%B") != expected_message:
        raise AdapterError("forbidden-effect", "controller commit identity or trailers drifted")


def execute(packet: Mapping[str, Any], environment: Mapping[str, str] | None = None) -> dict[str, Any]:
    """Run one bounded Codex implementation and return a typed, redacted result."""
    packet_value: dict[str, Any] | None = packet if isinstance(packet, dict) else None
    try:
        packet_value = _validate_packet(packet)
        env = dict(os.environ if environment is None else environment)
        cwd = Path(packet_value["cwd"]).resolve()
        argv = _argv_from_env(env, cwd)
        cwd_identity = (cwd.stat().st_dev, cwd.stat().st_ino)
        if Path(_git(cwd, "rev-parse", "--show-toplevel")).resolve() != cwd or \
                _git(cwd, "rev-parse", "HEAD") != packet_value["input_revision"] or _status_paths(cwd):
            raise AdapterError("subject-mismatch", "implementer subject is not the clean input revision")
        metadata_before = _metadata_invariants(cwd)
        child = subprocess.run(
            argv, cwd=str(cwd), env=env, input=_prompt(packet_value),
            capture_output=True, text=True, check=False, shell=False,
        )
        if child.returncode != 0:
            failure = AdapterError("child-failed", "child process failed")
            failure.diagnostic = _child_diagnostic(child)
            raise failure
        if _contains_environment(child.stdout, env):
            raise AdapterError("credential-leak", "child output contained an environment value")
        if (cwd.stat().st_dev, cwd.stat().st_ino) != cwd_identity or \
                Path(_git(cwd, "rev-parse", "--show-toplevel")).resolve() != cwd:
            raise AdapterError("subject-mismatch", "Git subject identity changed")
        if _metadata_invariants(cwd) != metadata_before:
            raise AdapterError("forbidden-effect", "Git metadata changed during model phase")
        paths = _validated_workspace_edits(cwd, packet_value)
        _controller_commit(cwd, packet_value, paths)
        candidate = _git(cwd, "rev-parse", "HEAD")
        ancestor = subprocess.run(
            ["git", "-C", str(cwd), "merge-base", "--is-ancestor", packet_value["input_revision"], "HEAD"],
            check=False, capture_output=True, text=True, shell=False,
        )
        try:
            commit_count = int(_git(cwd, "rev-list", "--count", f"{packet_value['input_revision']}..HEAD"))
        except ValueError as exc:
            raise AdapterError("git-failure", "local Git commit count was malformed") from exc
        if ancestor.returncode != 0 or commit_count != 1:
            raise AdapterError("forbidden-effect", "controller commit ancestry or bound was invalid")
        if _status_paths(cwd):
            raise AdapterError("forbidden-effect", "implementer left uncommitted changes")
        changed_paths = {
            path for path in _git(cwd, "diff", "--name-only", packet_value["input_revision"], "HEAD").splitlines() if path
        }
        if changed_paths != set(paths) or any(
            not _within_owned(path, packet_value["owned_paths"]) for path in changed_paths
        ):
            raise AdapterError("forbidden-effect", "changed paths exceeded the admitted scope")
        return {
            "schema": RESULT_SCHEMA,
            "phase": "implement",
            "status": "success",
            "issue_number": packet_value["issue"]["number"],
            "run_id": packet_value["run_id"],
            "actor_family": AUTHOR_FAMILY,
            "input_revision": packet_value["input_revision"],
            "candidate_revision": candidate,
            "changed_paths": sorted(changed_paths),
            "commit_count": commit_count,
            "failure": None,
        }
    except AdapterError as exc:
        return _fail(packet_value, exc.code, exc.message, getattr(exc, "diagnostic", None))
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
