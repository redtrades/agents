# Ox Alpha free-window snapshot — 2026-08-26 ~15:49 ET

Secondary to the omlx/Hermes qwen3.8-oq4e pass. Possible free-window end
~27 Aug 2026. Catalog only — no paid/completion probe.

Source: `GET http://127.0.0.1:3100/v1/models` (FreeLLMAPI gateway, auth via
`HERMES_CUSTOM_FREELLMAPI_API_KEY`). Gateway dashboard HTTP 200.

| field | value |
|---|---|
| catalog size | 197 |
| `available: true` | 93 |
| `available: false` | 104 |
| Ox Alpha id in catalog | **`openrouter/ox-alpha`** (name "Ox Alpha") |
| `stealth/ox-alpha` | **absent** from catalog |
| available | true (`unavailable_reason`: null) |
| context_length | 1,048,576 |
| tools | yes (`tools`, `tool_choice`, `parallel_tool_calls`, `reasoning_effort`, …) |

Hermes still has `providers.freellmapi.default_model: stealth/ox-alpha` and
registers only that slug under `models:`. That slug is **not** in today's
gateway list; the live id is `openrouter/ox-alpha`. Alias drift — not patched
in this pass (omlx/Hermes local was the primary job).

Prior note: `knowledge/ox-alpha-multi-provider-research-2026-08-25.md`.
