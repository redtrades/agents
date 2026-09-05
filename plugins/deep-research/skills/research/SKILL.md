---
name: research
description: Research a question against primary sources and write cited Markdown findings. Use when the task is "find out" rather than "what do you already know"  -  current events, tooling or version facts, prior-art surveys, API or spec behavior, or any claim that moves faster than the training cutoff. Not for questions answerable from the codebase in front of you.
---
# Research

## Method

1. **Primary sources only.** Official docs, source code, specs, first-party APIs
    -  not a secondary write-up of them. Follow every claim back to the source
   that owns it.
2. **Cite every factual claim** with its source: URL, file path and line, or doc
   section.
3. **Be specific and quantified.** "The matcher stage takes ~2.3s per notice due
   to sequential API calls", not "the matcher is slow".
4. **Follow the failure trail** to the root cause in code or config when
   investigating an issue.
5. **Write one Markdown file**, saved where the repo already keeps such notes
   (match the existing convention; if none, pick a sensible place and say
   where). Flag any outdated docs the research exposes.

## Degrees of freedom

Default to a direct research pass in this session. Spin up a **background agent**
(`Agent` tool) only when the reading is large enough that parallel work is
worthwhile and the user has not asked you to stay hands-on  -  a background agent
fragments the synthesis, which is usually the point of the task.

## Structured outputs

For a system or architecture teardown (diagnosis → proposals → prioritization →
risks → roadmap), see [references/architecture-teardown.md](references/architecture-teardown.md).

<!-- agent-configs generated source-sha256: 4bcfef05593cb3f8aea65b2c4a3a81534363862faffc096be201fd98a89feb69 -->
