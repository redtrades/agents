---
name: htmlvspec
description: Creates a visual engineering implementation plan as a single self-contained HTML page saved to specs/<name>.html  -  the plan authored directly in styled HTML, with one AI-generated diagram image per section (hero + per major H2) generated in parallel and embedded inline, plus a freeform HTML zone for custom HTML/CSS/SVG/JS that aids comprehension. Images are always generated. Use when the user says "htmlvspec", wants a visual/illustrated HTML implementation plan, a browser-openable spec with per-section diagrams, or any HTML plan where images are required. argument-hint: "[user prompt]"
---
# htmlvspec
## Purpose

Produce a **visual** engineering implementation plan as **one self-contained HTML page**  - 
`specs/<plan-name>.html`  -  that you can open directly in a browser. The plan is authored
**directly in HTML** using the template below, with **one AI-generated diagram image per
section** (hero + per major H2) generated in parallel and embedded inline, and a dedicated
**Freeform** zone that lets you author any HTML you want (interactive toggles, animated SVG
flows, comparison matrices, decision trees, etc.) to make the plan clearer and richer than
prose could.

Phases, in order:

1. **Plan phase**  -  analyze, explore, design (same thinking as a normal spec).
2. **HTML authoring phase**  -  write the plan into the **HTML Plan Template**.
3. **Image phase**  -  generate one diagram per section in **parallel** and embed them inline.
4. **Freeform phase**  -  enrich the page with custom HTML per the **Freeform Instruction Set**.
## Variables

USER_PROMPT: $1
ALL_ARGUMENTS: $ARGUMENTS
PLAN_OUTPUT_DIRECTORY: `specs/`
PLAN_SLUG: kebab-case name derived from the plan topic (e.g. `in-memory-ttl-lru-cache`)
HTML_OUTPUT: `specs/htmlvspec-<PLAN_SLUG>.html`   -  **the filename MUST always begin with the `htmlvspec-` prefix**
IMAGE_DIR: `specs/htmlvspec-<PLAN_SLUG>/`   -  sibling directory matching the HTML filename (same `htmlvspec-` prefix)
IMAGE_GENERATOR: `~/.claude/skills/htmlvspec/scripts/generate_image.py`
IMAGE_SIZE: `2048x1152` (wide 16:9 by default)
IMAGE_QUALITY: `high`
HERO_IMAGE_NAME: `00-hero.png`
MAX_TEXT_LABELS_PER_IMAGE: 10
MAX_TOTAL_IMAGES: 10
## Workflow

### Phase 1  -  Plan
1. THINK HARD: parse the USER_PROMPT; settle task type, complexity, and the architecture.
2. Explore the codebase for patterns and relevant files.
3. Decide the section set and the PLAN_SLUG.

### Phase 2  -  Author the HTML
4. Create `specs/` if missing. Write `specs/htmlvspec-<PLAN_SLUG>.html` from the **HTML Plan Template**, filling every applicable section with detailed content. Leave the section `<figure>` slots pointing at `htmlvspec-<PLAN_SLUG>/NN-*.png`  -  those files are generated in the next phase.

### Phase 3  -  Generate images in parallel
5. **Prerequisite key check**:
   ```bash
   ( [ -n "$OPENAI_API_KEY" ] || grep -q OPENAI_API_KEY .env 2>/dev/null ) && echo "OPENAI_API_KEY found" || echo "OPENAI_API_KEY missing"
   ```
   The generator reads `OPENAI_API_KEY` from the environment or a `.env` in the current working directory. If missing, stop and ask the user to set it.
6. Write the **shared style brief** once. Draft a per-image prompt for the hero + each section image (style is global, composition is local; ≤10 labels each).
7. **Fire every image at once  -  in parallel.** Each call takes many seconds; running them sequentially wastes minutes for no reason. There are two acceptable parallel patterns; **pick one and execute it in a single tool call/turn**.

   **Pattern A  -  one Bash call, every image as a background job, then `wait`:**
   ```bash
   GEN=~/.claude/skills/htmlvspec/scripts/generate_image.py
   DIR=specs/htmlvspec-<PLAN_SLUG>     # matches the htmlvspec- prefix of the .html file
   uv run "$GEN" "<brief + hero composition>"      "$DIR/00-hero.png" &
   uv run "$GEN" "<brief + section-1 composition>" "$DIR/01-solution-approach.png" &
   uv run "$GEN" "<brief + section-2 composition>" "$DIR/02-architecture.png" &
   uv run "$GEN" "<brief + section-3 composition>" "$DIR/03-data-model.png" --size 1024x1024 &
   wait
   echo "all images done"
   ```
   The trailing `&` puts each job in the background so they all start immediately; `wait` blocks until they're all done. The generator creates parent dirs itself, so every job can start simultaneously.

   **Pattern B  -  N parallel Bash tool calls in a single message.** If you can issue multiple tool calls in one turn, dispatch each `generate_image.py` as its own Bash call in the same message. The tool harness runs them concurrently  -  same effect as Pattern A.

   **Anti-pattern (do not do this):** issuing one Bash call, waiting for it to return, then issuing the next. That is sequential and forbidden here. If you find yourself about to do that, stop and switch to Pattern A or B.

   `wide` (2048x1152) is the default; pass `--size 1024x1024`/`1152x2048` only when a section needs square/tall.
8. After `wait`, verify each PNG exists and is non-empty. Regenerate any failed section image (a single background job is fine). If the **hero** failed, stop and report.

### Phase 4  -  Freeform enrichment
9. Author the **Freeform** section and any in-section enrichments per the **Freeform Instruction Set** above  -  inline SVG/CSS/JS, self-contained, on-theme, additive.

### Phase 5  -  Finish
10. Confirm the `<img>` `src` paths are **relative** and match the generated filenames. Validate the HTML is well-formed (see Validation).
11. Follow the **Report Format**.
## Report Format

```markdown
✅ Visual HTML Implementation Plan Created

File: specs/htmlvspec-<PLAN_SLUG>.html  (open in a browser)
Topic: <brief description of what the plan covers>
Images: <count succeeded> / <count attempted> in specs/htmlvspec-<PLAN_SLUG>/
Freeform: <one line on what custom HTML you added, if any>

Key Components:
- <main component 1>
- <main component 2>
- <main component 3>

Open with: open specs/htmlvspec-<PLAN_SLUG>.html
```
## Validation

```bash
# file exists and is non-trivial HTML
test -s specs/htmlvspec-<PLAN_SLUG>.html && head -1 specs/htmlvspec-<PLAN_SLUG>.html | grep -qi '<!DOCTYPE html>' && echo "HTML ok"
# every <img src> file exists; paths relative; no prompt used more than 10 labels
```

## Extended Reference & Deep Mechanics

For complete implementations, edge cases, and detailed recipes, see [references/details.md](references/details.md).
