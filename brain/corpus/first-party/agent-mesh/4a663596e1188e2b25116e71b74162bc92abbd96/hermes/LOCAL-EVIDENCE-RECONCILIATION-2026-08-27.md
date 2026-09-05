# Local OMLX and Hermes evidence reconciliation

**Checked:** 2026-08-27 on the M1 Max 64GB host. This note separates live state,
historical local reports, and another repository's in-progress working tree. It does
not import GovCon policy or artifacts into agent-mesh.

## Current live state

- OMLX global scheduling is `max_concurrent_requests: 3`,
  `prefill_priority: context`, `chunked_prefill: false`, and
  `decode_fairness: true`. The hot cache is 8GB and the SSD cache is automatic.
- The production `qwen3.8-oq4e` model has native MTP, TurboQuant KV4, and guided
  grammar enabled. VLM MTP, ANE, speculative prefill, and DFlash are disabled.
- Hermes root/default uses OMLX at `127.0.0.1:8300`, model
  `qwen3.8-oq4e`, thinking budget 1024, 4,096 output tokens, low reasoning,
  lean compaction at 51,200 tokens, and no delegation-model pin.
- The short/mid/full benchmark profiles remain low/low/xhigh reasoning with
  4,096/4,096/8,192 output limits. No skill body is preloaded in any profile.

## On-demand skills: measured configuration

Hermes implements progressive disclosure through the `skills` toolset:
`skills_list` exposes metadata, `skill_view` loads a selected skill, and
`skill_manage` handles mutations. The toolset must be enabled for the platform;
merely setting `skills.external_dirs` does not make those tools available.

The stock catalog is not a zero-cost pointer on this host. Enabling it adds the
full name/description index for the installed catalog while still deferring skill
bodies. Measured fresh-session sizes:

| Profile/platform | System bytes | Skills-index bytes | Tool schemas | Tool count |
|---|---:|---:|---:|---:|
| short CLI, skills off | 20,212 | 0 | 13,090 | 7 |
| mid CLI, skills off | 20,208 | 0 | 13,090 | 7 |
| root/default CLI, skills on demand | 45,918 | 24,580 | 16,789 | 10 |
| root/default API/Desktop, skills on demand | 42,179 | 24,580 | 16,789 | 10 |
| full CLI, skills on demand | 47,421 | 24,647 | 16,815 | 10 |

The official command was used to measure this configuration, then reversed. The broad
index contains GovCon/TDIU skills that must remain separate from agent-mesh, so all
Qwen profiles currently keep the `skills` toolset disabled. The table is configuration
cost evidence, not a performance result. A curated agent-coding-only inventory is a
precondition for enabling persistent on-demand discovery.

## Local reports and agent-configs

- `/Users/man/agent-reports/RUNBOOK.md` records an older 8-bit campaign. Its useful
  bounded findings are that `chunked_prefill: true` did not improve the measured
  two/three-agent workload and that three concurrent agents were the practical
  ceiling. Those findings agree with current settings, but its older model and
  `max_concurrent_requests: 8` state are not current authority.
- `/Users/man/agent-reports/omlx-optimization/LOCAL-LLM-OPTIMAL-CONFIG-20260826.md`
  is likewise historical. Its observation that Qwen's template meaningfully
  distinguishes low and xhigh supports the current low/low/xhigh profile split.
- `/Users/man/.hermes/skills/autonomous-ai-agents/hermes-local-models/references/omlx-m64-tuning.md`
  still describes the older 8-bit/max-8 setup and is explicitly non-governing here.
- `/Users/man/agent-configs` was inspected but not modified. It is on
  `work/single-queue-issue-243`, ahead of and behind its remote, with modified and
  untracked files belonging to another active workstream. Its open config-drift
  proposal supports leaving Hermes delegation provider/model/base URL empty; the
  live configuration passes that check. It contains no newer production OMLX
  benchmark that supersedes this repository's evidence.

Source-file SHA-256 prefixes recorded during reconciliation: local RUNBOOK
`e02f6`, local optimization report `e88f3`, historical Hermes tuning reference
`49559`, live OMLX settings `849717`, and live model settings `b0f02`. Hashes are
provenance only; local files remain outside this repository.

## Remaining bounded work

Run the same agentic-coding fixture against short (skills off) and full or root
(on-demand catalog) and record server-reported prompt/cached/completion tokens,
latency, and memory. If the 24.6KB index cost is material, curate a small
agent-coding-only skill inventory before enabling skills on short/mid; do not preload
skill bodies or expose the entire catalog to the minimal profile by default.
