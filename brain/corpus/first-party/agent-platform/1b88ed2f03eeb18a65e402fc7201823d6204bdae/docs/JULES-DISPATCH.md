# Jules dispatch contract

This contract admits only two Jules entry modes. Jules remains an executor behind
the agent-platform controller; it is not a second queue, lifecycle authority, or
promotion mechanism.

## Native GitHub dispatch

`NativeGitHubDispatcher.prepare()` validates an already observed GitHub issue or
pull request. The target must be an exact HTTPS URL, the labels must include
`jules` case-insensitively, and the body must contain non-empty explicit sections:

```text
Objective: ...
Acceptance Criteria: ...
Exact Target: ...
```

This adapter does not add labels or mutate GitHub. Jules documents starting a task
from an issue by applying the `jules` label and requiring the Jules GitHub App to
have repository access: [Starting tasks from GitHub Issues](https://jules.google/docs/running-tasks/#starting-tasks-from-github-issues).

## Direct API dispatch

`DirectApiTaskPacket` binds all of the following remote identities and bounded
instructions:

- repository and exact Jules source resource;
- exact remote branch;
- immutable input revision;
- full 40-hex GitHub-visible candidate commit;
- exact GitHub issue or pull request URL;
- owned repository paths;
- exact commands, expected output, and stop conditions; and
- task, attempt, receipt, and idempotency identities.

Before the injected session creator can issue `POST /sessions`, the dispatcher:

1. fetches the exact Jules source resource and requires one exact branch match;
2. asks a read-only GitHub compare verifier to prove the candidate is reachable
   from that remote branch; and
3. records a durable pending intent before the single session create.

An absent, ambiguous, or mismatched source/branch/candidate denies before the POST.
The packet has no workspace field, rejects local-worktree command references, and
the generated prompt explicitly prohibits local or unpushed bytes. Jules’ API
requires a source and starting branch in `sourceContext`: [Sources](https://jules.google/docs/api/reference/sources/)
and [Sessions](https://jules.google/docs/api/reference/sessions).

## Review binding

Review admission uses the same remote proof but additionally requires
`branch_head == candidate_commit`; a merely local or reachable-but-not-pushed
candidate is denied. `bind_review_decision()` accepts only the exact JSON keys
`verdict`, `candidate_commit`, `reviewer_run_id`, and `findings`, and returns the
decision together with the exact remote-head binding. It does not merge, write
accepted source, or promote a candidate.

The older session `sessions/1685163324513780378` from the generic fixture is stale
executor evidence only. It is not Gate C review evidence.

The Gate C reviewer seam in `tools/jules/reviewer.py` accepts the controller's
workspace identity as local evidence, but never sends that path to Jules. The Jules
packet contains only the exact repository, source resource, remote branch, input
revision, pushed candidate OID, GitHub target, owned paths, commands, and stop
conditions. An injected input-revision verifier and the merged remote-head proof are
required before the first create.

The reviewer creates at most one session for an immutable packet, persists its
session/binding before polling, and reuses that binding after the initiating process
stops. A lost create response is reconciled through the documented session list/get
surfaces only when the pending intent has a valid creation watermark and the remote
session has a later `createTime`, exact prompt identity, task/attempt identity, source,
and branch. A provider idempotency identity is used when the provider exposes one;
otherwise a title/source/branch-only or prompt-less match is ambiguous and denied.
Zero or multiple matches deny and never issue a second POST. It requires an explicit
`AWAITING_USER_FEEDBACK` session plus an `agentMessaged` activity ID, sends the reply
through that same `sessions/{id}:sendMessage` endpoint, then requires an observed
`userMessaged` activity containing its run marker and a distinct later agent activity
ID absent from the pre-reply baseline. Concurrent resumes claim a durable message
intent with a local CAS; a losing resume only reconciles an observed message and
never sends a duplicate. Sender and observer receipt writers also reconcile an
identical durable intent/result after the receipt CAS, so neither caller surfaces
a race error. Missing proof, timeout, malformed output, or a wrong
candidate is a denial with a durable failure history whose current pointer is
superseded by the final receipt after a later successful resume.

On completion the adapter returns exactly:

```json
{"verdict":"PASS|FAIL|UNSURE","candidate_commit":"<full OID>","reviewer_run_id":"<run>","findings":[]}
```

The receipt binds the complete immutable task semantics (objective, acceptance
criteria, owned paths, exact commands, and stop conditions), as well as task, attempt,
input, candidate, source, branch, session, activity, artifact, and pull-request
metadata digests in one hash-linked chain. Before terminal acceptance the controller
must prove the exact input-to-candidate range; terminal session source/branch context
and every activity artifact change-set `baseCommitId` must still match that packet.
Jules `Session.outputs` are interpreted only as documented pull-request outputs;
candidate change sets are collected from `Activity.artifacts`, so this lane does not
require or trigger PR creation. Pull-request metadata is observed only; the MVP has
no PR-creation, merge, deletion, queue, or promotion path. A real Jules session is
not admissible until the controller supplies an exact
pushed GitHub-visible candidate and a separately provisioned opaque key reference.

## Receipts and recovery

Every direct create requires an immutable pending intent. A resolved receipt is
reused on retry; an unresolved or mismatched pending intent is reconciled only by
the documented list/get session identity proof and otherwise denies without creating
a replacement session. The receipt binds the exact candidate, source, branch,
issue/PR, session, request digest, and response digest. Runtime activity continuation
remains on Jules’ documented `sendMessage` surface; no private API is assumed. The
review deadline is established before any source, remote-proof, create, list/get,
activity, or message call, and each provider seam receives only its remaining budget.
