---
name: verify-before-asserting
description: How to ground a claim about tooling, config, machine state, or a fast-moving ecosystem before stating it. Use before recommending a tool, config, or architecture; before describing what a setting does or who set it; before running a benchmark or measurement; or before asserting something does or doesn't exist Use when verifying tech stack claims, tool availability, or machine state before asserting.
---
**Search before asserting**, always, for fast-moving ecosystems (local inference, quantization formats, serving runtimes, agent frameworks, and similar). Treat training knowledge here as expired by default  -  named tools, version numbers, benchmark claims, and "X doesn't exist" all need a live check first. State whether a proposal matches current practice, is outdated, or is a legacy idea worth keeping anyway.

**Use established tools for measurement, not custom scripts.** Custom code is for orchestration only  -  looping, collecting, formatting. Every measured number names the standard tool that produced it; if a custom measurement is used anyway, state what gap in the standard tool justified it. A harness that doesn't verify the thing under test is actually doing what it claims is the most common way benchmarks go wrong.

**Check live state, not the file on disk**  -  a config file and a running process can disagree (e.g. `launchctl print` vs. the plist on disk). Drift here presents as an unrelated problem and sends investigation chasing the wrong cause.

**Never describe a setting as someone's deliberate config without checking who set it.** An unfamiliar value is as likely to be a prior agent's default as a real decision.

<!-- agent-configs generated source-sha256: c45ef186f64da41ad4a72d76e3346bf4599422d1d7647bf3f357d3eb1a02e5b0 -->
