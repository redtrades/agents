# CI gates

`tools/ci/run_gates.py` is the first executable evidence boundary for this
repository. It runs deterministic commands only after the checked-out Git commit
matches the expected event subject, then writes a JSON receipt containing the
tested commit, tree, commands, exit codes, and output digests.

The GitHub Actions workflow runs on pull requests and on `main`. Pull-request
receipts bind to GitHub's checked-out merge subject; `main` receipts bind to the
accepted integration commit. A failed or stale subject returns nonzero and still
uploads its receipt.

This slice proves execution and exact-subject evidence. It does not yet prove a
separate cryptographic CI principal or authorize automatic promotion. Promotion
must remain disabled until the controller validates a trusted workflow/run
identity, the receipt, independent review, and the expected integration head.

Run the same gates locally:

```bash
python3 tools/ci/run_gates.py \
  --receipt /tmp/agent-platform-ci-receipt.json \
  --expected-subject "$(git rev-parse HEAD)" \
  --gate-json '{"name":"governing-policy","argv":["python3","tests/docs/test_governing_policy.py"]}' \
  --gate-json '{"name":"identity-helper","argv":["python3","tests/identity/test_configure_git_identity.py"]}' \
  --gate-json '{"name":"identity-range","argv":["python3","tests/identity/test_validate_commit_range.py"]}' \
  --gate-json '{"name":"ci-runner-tests","argv":["python3","tests/ci/test_run_gates.py"]}'
```
