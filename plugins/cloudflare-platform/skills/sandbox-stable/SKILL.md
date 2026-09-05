---
name: sandbox-stable
description: Use when building or changing Cloudflare Sandbox apps on the current stable @cloudflare/sandbox package (default npm tag) - commands, sessions, files, ports, tunnels, terminals, bridge, production, or deprecated-API cleanup while staying on stable. Not for @cloudflare/sandbox@next (use sandbox-next) or for porting to 1.0 (use sandbox-migrate-to-next).
---
# Sandbox SDK  -  stable package

## Overview

Isolated Linux environments on [Cloudflare Containers](https://developers.cloudflare.com/containers/), driven from Workers.

**Prefer the main Sandbox docs and installed stable types over memory.** This skill is a gate, a contract, and a retrieval map - not a full manual.

This line is the **current stable** default npm package. The main [Sandbox documentation](https://developers.cloudflare.com/sandbox/) describes it. Existing apps can stay here and keep shipping.

We recommend **new projects** on `@cloudflare/sandbox@next` with **`sandbox-next`**. When you can, plan a move with **`sandbox-migrate-to-next`** so you are ready when 1.0 becomes the stable release. Do not force that port unless the user asks.
## 1. Gate  -  confirm the package line

Before writing code, inspect the app:

| Check | Must match |
| ----- | ---------- |
| npm dependency | Default `@cloudflare/sandbox` (**not** `@next` / preview tags) |
| Container image | Matching **stable** image (not `cloudflare/sandbox:next`) |

| If you find… | Action |
| ------------ | ------ |
| `@cloudflare/sandbox@next` or a `next` image | **Stop.** Load **`sandbox-next`**. |
| User wants to port to 1.0 / `@next` | **Stop.** Load **`sandbox-migrate-to-next`**. Do not half-apply preview APIs on a stable package. |
| Only cleaning deprecated stable APIs | Stay here; use the [2026 deprecation guide](https://developers.cloudflare.com/sandbox/guides/2026-deprecation/). That is **not** a move to `@next`. |

Never mix a stable Worker package with an `@next` container image (or the reverse).

Skills install: [Agent setup](https://developers.cloudflare.com/agent-setup/) · [cloudflare/skills](https://github.com/cloudflare/skills)
## 2. Contract  -  non-negotiables

- `await sandbox.exec(command)` takes a **command string** and resolves when the command **finishes**, with buffered `stdout` / `stderr` / `exitCode` (and related fields).
- Long-running and streaming work use the **stable** command APIs (`startProcess`, `execStream`, and related helpers) - not the `@next` single-handle model. Open the Commands docs; do not invent `@next` `output()` handles on stable.
- **Sessions** can preserve working directory and environment across commands (default session / `enableDefaultSession`, `createSession`). See Sessions docs when state must carry across calls.
- Interactive browser terminals often use **`sandbox.terminal(request)`** and session/xterm helpers on stable - not preview `createTerminal` unless the package is `@next`.
- Prefer **RPC** transport when using tunnels or large/binary streaming. HTTP/WebSocket transports are deprecated (cleanup guide below).
- Files, mounts, ports, tunnels, backups, lifecycle, and interpreter: use main docs for signatures; trust installed **stable** types.
- Non-secret config in sandbox env; live credentials in the Worker. Use outbound handlers when processes call external APIs.
- Production preview hostnames need wildcard DNS on a custom domain when using those URL patterns.
- Do **not** apply `@next` argv/`process.output()` APIs while the dependency is still stable.
- Self-deployed **bridge** stays on the stable package and image. [Bridge](https://developers.cloudflare.com/sandbox/bridge/)

Minimal shape:

```ts
import { getSandbox, proxyToSandbox, Sandbox } from "@cloudflare/sandbox";

export { Sandbox };

const sandbox = getSandbox(env.Sandbox, "user-123");
const result = await sandbox.exec('python3 -c "print(2 + 2)"');
// result.stdout, result.exitCode, result.success
```
## 4. Before you ship

- Worker package and container image on the **same stable** line  
- Typecheck against installed stable types  
- No live secrets in sandbox env  
- If using deprecated transports/helpers, finish or track [2026 deprecation](https://developers.cloudflare.com/sandbox/guides/2026-deprecation/) cleanup  
- When the team is ready for 1.0, use **`sandbox-migrate-to-next`** - do not force cutover unprompted

## Extended Reference & Deep Mechanics

For complete implementations, edge cases, and detailed recipes, see [references/details.md](references/details.md).
