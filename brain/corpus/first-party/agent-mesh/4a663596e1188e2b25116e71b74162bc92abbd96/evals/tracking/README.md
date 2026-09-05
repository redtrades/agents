# Private benchmark tracking

This package runs the approved Phase 1 path:

`Promptfoo 0.122.1 -> private raw export -> sanitized receipt -> MLflow 3.15.2`

Raw prompts, responses, headers, logs, credentials, and private filesystem paths
must not enter Git or MLflow. MLflow receives only the receipt allowlist: bounded
labels, counts, latency/token/cost aggregates, named-score aggregates, hashes,
verdict, and opaque MLflow identifiers.

## Runtime boundaries

- Promptfoo is project-local under `evals/promptfoo/`; mutable state is isolated
  below `~/.local/share/agent-mesh/benchmarks/raw/`.
- MLflow is installed in the private uv environment below
  `~/.local/share/agent-mesh/mlflow/`.
- The tracking server binds only to `127.0.0.1:5001`, uses one worker, Basic
  Auth, `NO_PERMISSIONS` by default, an exact Host/origin allowlist, and mode
  `0600` private state.
- Tailscale Serve exposes it tailnet-only at
  `https://m64.tailfb03be.ts.net:8446/`. The memorable landing alias is
  `https://m64.tailfb03be.ts.net/mlflow/`.
- This is a foreground/on-demand lifecycle, not an auto-start service. The
  Tailscale route may remain configured while the loopback process is stopped.

## Verify

```sh
cd /Users/man/agent-mesh
python3 -m unittest \
  evals.test_promptfoo_receipt \
  evals.test_mlflow_import \
  evals.test_mlflow_server_contract -v
```

Initialize private state without printing credentials:

```sh
python3 -m evals.tracking.serve_mlflow --initialize-only
```

Run the server in the foreground:

```sh
python3 -m evals.tracking.serve_mlflow
```

The username is `agent-mesh-default`. The generated password remains only in
`~/.config/agent-mesh/mlflow/default.credentials.json` (mode `0600`). Do not
commit it, paste it into issue comments, or embed it in URLs.

## Known boundary

The fixed Promptfoo 0.122.1 dependency currently reports five high-severity
transitive npm audit findings. The loopback-only, no-share, no-cache,
isolated-state fixture minimizes exposure; changing the required version needs
a separate compatibility evaluation.
