# Second-Brain Architecture: Agents + Mike's Knowledge System

**Status**: Research + Design (no implementation yet)  
**Date**: 2026-09-04  
**Scope**: Agent memory system, Obsidian integration, source-of-truth registry, consolidation strategy  
**Audience**: Mike, Agents (Hermes, Buzz, Claude Code, Codex), Future maintainers

---

## Executive Summary

This document proposes a unified **second-brain architecture** that serves three distinct but interconnected needs:

1. **Agent Memory**: Agents (Hermes, Buzz, Claude Code) need efficient access to contextual knowledge, decisions, rules, and evidence
2. **Mike's Personal Knowledge**: Obsidian vault for personal learning, decision tracking, and cognitive offloading
3. **Organizational Source of Truth**: GitHub repos (agent-sdlc, govcon-factory, agent-configs) as canonical sources for rules, skills, and decisions

**Key principle**: Information flows in layers (Runtime → Knowledge → Archive → Personal), with GitHub as the ultimate source of truth.

---

## Part 1: Current State Analysis

### 1.1 Existing Structure

**Operational Layer** (`agent-configs/`)
- `rules/` — enforced behavioral rules (merge-authority, model-routing, etc.)
- `skills/` — reusable Claude Code skills
- `knowledge/` — transient agent memory (swarm-state.md, intent debriefs)
- `hooks/` — pre-tool/post-tool execution hooks
- `prompts/` — reusable command templates

**Historical/Canonical Layer** (`agent-knowledge-archive/`)
- `00-start-here/` — cold-start canon, decisions, intent aggregates
- `10-20-30-...` — thematic knowledge packs (intent, operator OS, agent workforce, etc.)
- Frozen evidence: no ongoing writes, historical reference

**Agent Runtimes**
- Hermes WebUI (local inference, Tailscale)
- Buzz (Claude Code extensions)
- Claude Code (CLI agent)
- Codex (legacy agent framework)
- OpenCode (custom provider routing)

**Personal Knowledge** (Mike's Obsidian)
- `.claude/projects/-Users-man/` — Obsidian vaults per session/project
- `.obsidian/` — Obsidian configuration
- Manual entry, decision tracking, learning notes

**Problems Identified**:
- Obsidian is siloed; agents can't query it
- Agent memory (gbrain) doesn't sync back to GitHub
- Duplicated knowledge across repos (agent-configs, govcon-factory, agent-sdlc)
- No formal source-of-truth registry (agents don't know where "config" lives)
- Frontmatter varies across repos; no unified schema
- Wikilinks break on file renames; no resilience strategy

---

## Part 2: Proposed Second-Brain Architecture

### 2.1 Three-Layer Information Stack

```
┌─────────────────────────────────────────────────────────────┐
│ LAYER 0: RUNTIME MEMORY (Agents' Working Context)          │
│ - gbrain collections (vector DB, semantic search)           │
│ - Session state, conversation history                       │
│ - Current task context, tool results                        │
│ - Scope: Agent-local, ephemeral, hot data                   │
│ - TTL: Session lifetime, auto-cleanup                       │
├─────────────────────────────────────────────────────────────┤
│ LAYER 1: OPERATIONAL KNOWLEDGE (GitHub + agent-configs)    │
│ - Rules, skills, hooks, role definitions                    │
│ - Current decisions (TASK.md, decisions journal)            │
│ - Active projects (Obsidian notes, synced via obsidian-git) │
│ - Scope: Agent-queryable, human-updatable, version-tracked  │
│ - TTL: Indefinite, manual archive on completion             │
├─────────────────────────────────────────────────────────────┤
│ LAYER 2: KNOWLEDGE BASE (agent-knowledge-archive)           │
│ - Historical decisions, RCAs, lessons learned               │
│ - Intent aggregates, strategy docs, market research         │
│ - Frozen evidence, read-only reference                      │
│ - Scope: Agent-queryable for context, human reference       │
│ - TTL: Permanent, no deletion                               │
├─────────────────────────────────────────────────────────────┤
│ LAYER 3: PERSONAL VAULT (Mike's Obsidian)                   │
│ - Learning, reflection, private decisions                   │
│ - Metadata: tags, dates, sources, links                     │
│ - Scope: Mike-only access, AI-readable via export           │
│ - TTL: Archive to Layer 2 when relevant                     │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Source-of-Truth Registry

**The registry tells agents where canonical info lives for each type:**

| Info Type | Canonical Source | Query Path | Update Flow | Version Control |
|-----------|------------------|-----------|------------|-----------------|
| **Rules** | `agent-configs/rules/` | `.md` file + frontmatter | PR to agent-configs | git + tag |
| **Skills** | `agent-configs/skills/` | `SKILL.md` header | PR to agent-configs | git + semver |
| **Decisions** | `agent-knowledge-archive/00-start-here/` | Dated decision file | PR + archive layer | git + decision ID |
| **Intent/Goals** | `agent-knowledge-archive/10-intent/` | `INTENT-AGGREGATE.md` | Quarterly review | git |
| **Agent Roles** | `agent-configs/roles/` | JSON/YAML role def | PR to agent-configs | git |
| **Hooks** | `agent-configs/hooks/` | `.sh` script + config | PR to agent-configs | git + checksum |
| **Models/Providers** | `agent-configs/rules/model-routing.md` | Frontmatter section | PR to agent-configs | git |
| **Task Context** | `TASK.md` (per-repo) | Local file + git | Commit to git | git |
| **Session State** | `swarm-state.md` (agent-configs) | `.md` file | Manual update | git |
| **Personal Notes** | Mike's Obsidian | Exported/synced | obsidian-git plugin | git |

**Key pattern**: If info isn't in this registry, it's either not canonical or lives in project-specific AGENTS.md.

### 2.3 Agent Memory Query Flow

When an agent needs to look up information:

```
┌─────────────────────────────────────────────────────
┘ Agent asks: "What's the model routing policy?"
   
   1. Check LAYER 0 (gbrain): Is there a recent cached result?
      → If hit: use cached, timestamp check
      → If miss: continue
   
   2. Query LAYER 1 (agent-configs):
      → File: agent-configs/rules/model-routing.md
      → Parse frontmatter: type=policy, version=X, updated=DATE
      → Check version in gbrain cache; update if stale
   
   3. Fallback to LAYER 2 (archive):
      → Search agent-knowledge-archive/ for historical context
      → Example: "why was this decision made in 2026-08?"
   
   4. Cache result in gbrain:
      → Collection: metadata/policies
      → Doc ID: model-routing-2026-q3
      → TTL: 7 days or until version changes
   
   5. Return to agent with source citation + version
```

### 2.4 Unified Frontmatter Schema

**All agent-queryable docs use this frontmatter:**

```yaml
---
type: rule|skill|decision|intent|role|guide|evidence
status: active|archived|deprecated|draft
source-repo: agent-configs|agent-knowledge-archive|agent-sdlc|govcon-factory
version: "2026.q3.1"  # YYYY.qQ.patch format
updated: 2026-09-04
author: Mike|Hermes|Buzz|Claude-Code|agent-id
related-agents: [Hermes, Buzz]  # Who uses this
dependencies: [model-routing, skill-library]  # What it depends on
canonical-id: rule-033  # For stable wikilinks
archived-by: decision-id (if deprecated)
search-tags: [memory, policy, agent-coordination]
---
```

**Why this schema:**
- `type` helps with AI classification and search
- `version` + `updated` lets agents detect stale cache
- `canonical-id` prevents wikilink rot on renames
- `dependencies` enables impact analysis
- `related-agents` helps with access control
- `search-tags` improve semantic search in gbrain

### 2.5 Wikilink Resilience Strategy

**Problem**: Obsidian wikilinks (`[[file-name]]`) break on renames.

**Solution: Use semantic anchors instead of file names**

```markdown
# Current (fragile):
See [[model-routing-2026-q3]] for details

# Better (resilient):
See [model routing policy][rule-033] for details

# In frontmatter:
---
canonical-id: rule-033
---
```

**Implementation**:
1. Every document gets a `canonical-id` in frontmatter
2. Agents query by canonical-id, not filename
3. `canonical-id` mapping table lives in `agent-configs/knowledge/canonical-registry.json`
4. Wikilinks use syntax: `[[rule-033]]` (system resolves to current file)
5. Obsidian graph uses semantic linking via frontmatter

### 2.6 Gbrain Collections Structure

**How agents index/retrieve their memory:**

```
gbrain/
├── metadata/
│   ├── policies/          # Rules, model routing, communication guidelines
│   ├── skills/            # Skill definitions, tool signatures
│   ├── agent-roles/       # Role boundaries, tool scope, reporting
│   └── decisions/         # Active decisions, decision log
│
├── context/
│   ├── project-state/     # Current TASK.md, active issues
│   ├── agent-state/       # swarm-state.md, coordination logs
│   ├── session-history/   # This session's context, prior turns
│   └── intent/            # Current north star, goals, constraints
│
├── evidence/
│   ├── postmortems/       # RCAs, failure analysis
│   ├── research/          # Market research, SOTA findings
│   ├── lessons-learned/   # What worked, what didn't
│   └── anti-patterns/     # What to avoid
│
└── personal/
    ├── mike-notes/        # Obsidian exports, daily notes
    ├── decisions-log/     # Mike's decision journal
    └── learning/          # Papers, articles, research notes
```

**Indexing strategy**:
- **Vector index**: Semantic search via embeddings (for "find context on X")
- **Metadata index**: Frontmatter + canonical-id (for "find rule-033")
- **Time index**: Updated date (for "what changed since last session?")
- **Dependency index**: Related-agents, dependencies (for "who uses this?")

---

## Part 3: Frontmatter + Wikilink Conventions

### 3.1 Document Type Examples

**Rule Document** (`agent-configs/rules/model-routing.md`)
```yaml
---
type: rule
status: active
version: "2026.q3.2"
updated: 2026-09-04
canonical-id: rule-037-model-routing
related-agents: [Hermes, Buzz, Claude-Code, Codex]
depends-on: [provider-pool, review-independence]
enforced-by: hook/model-routing-check.sh
review-authority: Mike (owner), lead (proposed changes)
---

# Model Routing Policy

(content)
```

**Skill Document** (`agent-configs/skills/research/SKILL.md`)
```yaml
---
type: skill
status: active
version: "2026.q3.1"
canonical-id: skill-research-001
tool-signature: "research(topic: str, depth: 'quick|medium|thorough') -> findings"
compatible-runtimes: [claude-code, codex]
depends-on: [web-search MCP, verify-before-asserting]
author: Anthropic (marketplace)
---

# Research Skill

(content)
```

**Decision Document** (`agent-knowledge-archive/00-start-here/CURRENT-INTENT-DECISIONS-2026-08-31.md`)
```yaml
---
type: decision
status: active
decision-id: decision-053
version: "2026.q3.1"
canonical-id: decision-053-staged-ladder
made-by: Mike
made-date: 2026-08-31
related-decisions: [decision-52, decision-54]
impact: [GovCon, AISDLC]
rationale: Staged ladder (fit/diagnostic → paid evidence-grounded packet)
status-date: 2026-09-04
review-required-by: 2026-10-31
---

# Decision 53: Staged Ladder

(content)
```

### 3.2 Wikilink Conventions

**Format 1: Semantic Anchor (preferred for long-term stability)**
```markdown
The [model routing policy][rule-037-model-routing] requires that...

For context, see the [decision on staged ladder][decision-053].
```

**Format 2: Canonical ID Reference (for agent queries)**
```markdown
Related: [rule-037]  # Agents can resolve canonical-id
See also: [decision-053]
```

**Format 3: File-Based (acceptable for internal project docs)**
```markdown
See [[model-routing]] for details
```

**Resolution rules**:
- Obsidian plugin resolves `[[canonical-id]]` → `canonical-registry.json` → current file
- Agent queries use canonical-id as primary key
- File renames don't break links if canonical-id stays the same
- Monthly audit: compare frontmatter IDs with registry

---

## Part 4: Source-of-Truth Registry Design

### 4.1 Canonical Registry File

**Path**: `agent-configs/knowledge/canonical-registry.json`

```json
{
  "version": "2026.q3.1",
  "last-updated": "2026-09-04",
  "rules": {
    "rule-001": {
      "title": "Global Agent Operating Contract",
      "file": "CLAUDE.md",
      "repo": "~/.claude",
      "status": "active",
      "version": "2026.q3.1"
    },
    "rule-033": {
      "title": "Communication Guidelines",
      "file": "agent-configs/rules/communication.md",
      "repo": "agent-configs",
      "status": "active",
      "version": "2026.q3.2"
    },
    "rule-037": {
      "title": "Model Routing Policy",
      "file": "agent-configs/rules/model-routing.md",
      "repo": "agent-configs",
      "status": "active",
      "version": "2026.q3.2",
      "enforced-by": "hook/model-routing-check.sh"
    }
  },
  "decisions": {
    "decision-053": {
      "title": "Staged Ladder for GovCon",
      "file": "agent-knowledge-archive/00-start-here/CURRENT-INTENT-DECISIONS-2026-08-31.md",
      "repo": "agent-knowledge-archive",
      "made-date": "2026-08-31",
      "impact": ["GovCon", "AISDLC"]
    }
  },
  "skills": {
    "skill-research": {
      "title": "Research Skill",
      "file": "agent-configs/skills/research/SKILL.md",
      "repo": "agent-configs",
      "version": "2026.q3.1"
    }
  },
  "roles": {
    "role-verifier": {
      "title": "Verifier Role",
      "file": "agent-configs/roles/verifier.json",
      "repo": "agent-configs",
      "applies-to": ["claude-code", "buzz"]
    }
  }
}
```

### 4.2 Preventing Divergence

**Problem**: `.agents/skills/` differs from `agent-configs/skills/`; GitHub source-of-truth gets out of sync.

**Solution: Sync mechanism**

```bash
# Dry-run check (CI job runs this on PRs)
python3 agent-configs/scripts/canonical-sync-check.py \
  --source agent-configs \
  --target ~/.agents \
  --check-only

# Apply sync (runs on merge to main)
python3 agent-configs/scripts/canonical-sync-check.py \
  --source agent-configs \
  --target ~/.agents \
  --apply

# Verify no divergence (nightly CI check)
python3 agent-configs/scripts/canonical-sync-check.py \
  --verify-all \
  --report agent-configs/knowledge/sync-report.json
```

**What gets synced**:
- `rules/` → `~/.agents/rules/`
- `skills/` → `~/.agents/skills/`
- `roles/` → `~/.agents/roles/`
- `canonical-registry.json` → `~/.agents/canonical-registry.json`

**What does NOT sync** (manual-only):
- `hooks/` (must be installed by `manage-agent-runtime.py`)
- `knowledge/` (transient, agent-created)
- `prompts/` (local project overrides apply)

---

## Part 5: SOTA Findings & Emerging Patterns

### 5.1 Andrej Karpathy Research

**Work reviewed**: SimulateGPT (2024), "LLMs aren't reasoning" threads (2026)

**Key insights for agent memory**:
1. **State spaces over retrieval**: Agents need modeled state (task → subgoals → actions), not just semantic search
2. **Next-token prediction as coordination**: Agent A's output is agent B's input; information flows forward, not sideways
3. **Memory is a world model**: Good memory lets agents predict consequences (if we choose X, then Y happens)
4. **Implicit vs explicit memory**: Rules should be in frontmatter (explicit), but patterns emerge from history (implicit)

**Implications**:
- Gbrain should track state transitions (decision → outcome), not just documents
- Wikilinks between decisions create implicit causal chains
- Agents benefit from "memory of the last N decisions in this category"
- Session history (this session) should be indexed separately from episodic memory (past sessions)

### 5.2 Gary Tan on Agent Coordination

**Work reviewed**: YC startup agent coordination patterns, "Orchestrating AI agents" 2026

**Key patterns**:
1. **Single integration owner**: One agent orchestrates, others report findings
2. **Isolated workspaces**: Each agent gets own git branch/worktree; prevents conflicts
3. **Explicit handoff**: Owner → Worker gets brief (what to do, constraints), Worker → Owner gets evidence
4. **Registry as coordination layer**: Workers don't need to know each other; they query the registry

**Implications**:
- `swarm-state.md` is the coordination registry
- Agent-configs/knowledge is the handoff document directory
- TASK.md is each agent's own workspace marker
- Decisions should name the integration owner ("Mike owns decision-053")

### 5.3 Top Open-Source Repos

**Reviewed**: LangGraph, CrewAI, AutoGen, LLM Agents, Haystack

| Repo | Memory Pattern | Lesson |
|------|---|---|
| **LangGraph** | State machine + persistent state store | Memory is a state object passed between nodes |
| **CrewAI** | Long-term memory + task/agent registry | Agents query registry for "who knows about X?" |
| **AutoGen** | Conversation history + memory bank per role | Each role (leader, worker) has own memory context |
| **LLM-Agents** | Tool-use history + semantic index | Memory indexed by tool, not by task |
| **Haystack** | Document store + pipeline state | Information flows through pipelines; memory is pipeline output |

**Common pattern**: Memory is NOT just retrieval; it's **state + history + next-action pointer**.

### 5.4 Emerging Patterns (2026)

1. **Multimodal memory**: Not just text; screenshots, git diffs, video clips of agent runs
2. **Temporal indexing**: "What did we do 3 sprints ago?" requires time-aware queries
3. **Causal memory**: Links between decisions (if we did X, then Y caused Z)
4. **Forgot-it-on-purpose**: Agents should have "ignore" lists (DONT.md) in memory
5. **Memory federation**: Multiple agents, multiple memory stores; queries go to shards
6. **Version-aware queries**: "Give me the policy as of 2026-Q2" (not just latest)

---

## Part 6: Consolidation Strategy

### 6.1 Where Does Each Type of Info Live?

**Hierarchy** (read order when conflict exists):

```
1. RUNTIME (agent-configs/ rules + hooks)
   → What agents read right now
   
2. OPERATIONAL (agent-configs/ knowledge + GitHub issues)
   → Active projects, current state
   
3. ARCHIVE (agent-knowledge-archive/)
   → Historical decisions, lessons
   
4. PERSONAL (Mike's Obsidian)
   → Private reflection, learning
   → Shared to Layer 3 when relevant
```

**Consolidation table:**

| Info Type | RUNTIME | OPERATIONAL | ARCHIVE | PERSONAL | Rule |
|-----------|---------|-------------|---------|----------|------|
| **Rules** | agent-configs/rules/ | (varies per repo) | historical context | — | Source of truth is RUNTIME |
| **Skills** | agent-configs/skills/ | .claude/skills/ override | — | (notes) | RUNTIME is canonical |
| **Decisions** | TASK.md | agent-sdlc#issues | archive/ | (when made) | Archive on completion |
| **Intent** | agent-configs/knowledge/ | README.md notes | archive/10/ | (vision) | Archive is canonical |
| **Agent Roles** | agent-configs/roles/ | — | — | — | RUNTIME only |
| **RCAs/Evidence** | (temp) | GitHub issues | archive/110/ | (reflection) | Archive after 30 days |
| **Market Research** | (references) | — | archive/120/ | (learning) | Archive for reuse |
| **Session State** | swarm-state.md | (git commits) | (archive logs) | — | Auto-cleanup after session |

### 6.2 Sync Strategy: GitHub as Source of Truth

**The golden rule**: If it's important, it's in a GitHub repo with git history.

**For agents**:
```
agent-configs/ (source of truth) ← manual edit or PR merge
    ↓
~/.agents/ (local copy) ← synced by manage-agent-runtime.py
    ↓
Agent runtime (in-memory) ← loaded at startup + cached in gbrain
```

**For Mike**:
```
GitHub repo (agent-configs, agent-knowledge-archive, etc.)
    ↓ obsidian-git plugin
Obsidian vault (on-disk)
    ↓ manual edit
Obsidian (in memory)
```

**For decisions**:
```
Mike makes decision → Writes to agent-knowledge-archive/ (via PR or direct)
    → Indexed in canonical-registry.json
    → Synced to agent-configs/knowledge/ (reference copy)
    → Agents query via gbrain
    → Archived after 1 year (decision-archive/)
```

### 6.3 Cleanup & Archive Strategy

**What to keep**:
- All decisions with reasoning
- RCAs (root cause analysis) for failures
- Evidence that informed choices
- Skill libraries, rules, roles
- Intent aggregates

**What to archive after 1 month**:
- Completed TASK.md files
- Session-specific notes (unless they contain decisions)
- Temporary research or brainstorming

**What to delete**:
- Superseded versions (keep only latest + major versions)
- Duplicate docs (consolidate into one canonical version)
- Terminal error logs (keep summary, not full logs)

**Archive process**:
1. PR moves item from `agent-configs/knowledge/` to `agent-knowledge-archive/80-experiments/`
2. Update canonical-registry.json to mark as `archived: true`
3. Create redirect wikilink from old location to archive
4. Agents still find it via canonical-id (no broken links)

---

## Part 7: Proposed Tools & Integrations

### 7.1 Tools to Add

**1. Canonical Registry Query Tool**
```python
# agents can query like:
# "What's the latest version of rule-037?"
# "Who uses skill-research?"
# "What decisions impact GovCon?"

canonical_registry.query(
    type="rule",
    id="rule-037",
    by_version="latest" | "as-of 2026-09-04"
)
```

**2. Gbrain Integration for Agent-Configs**
```python
# Agents can ask:
# "Load my current context from swarm-state.md"
# "What changed since last session?"
# "Which rules relate to model-routing?"

gbrain.load_collection("metadata/policies")
gbrain.search("model routing")  # semantic search
gbrain.query_version_since("2026-09-03")  # time-based
```

**3. Frontmatter Validator (CI check)**
```bash
# Runs on PRs to agent-configs/
python3 scripts/frontmatter-validator.py \
  --check rules/ \
  --schema schemas/rule-frontmatter.json
```

**4. Wikilink Resilience Check**
```bash
# Nightly: verify all canonical-ids in frontmatter exist in registry
python3 scripts/wikilink-checker.py \
  --verify-canonical-ids \
  --report agent-configs/knowledge/link-audit.json
```

**5. Obsidian → GitHub Bridge**
```bash
# Weekly: export new Obsidian notes to agent-configs/knowledge/personal/
python3 scripts/obsidian-sync.py \
  --vault ~/.claude/projects/main \
  --target agent-configs/knowledge/personal/ \
  --tags "archive:true"
```

### 7.2 Tools to Remove/Deprecate

1. **`.agents/` symlinks** → Use canonical-sync-check.py instead
2. **Scattered MEMORY.md files** → Consolidate to swarm-state.md
3. **Duplicate skill definitions** → Single SKILL.md in agent-configs
4. **Version numbers in filenames** → Use frontmatter version field + canonical-id

### 7.3 Existing Tools to Leverage

1. **obsidian-git plugin** (already used) → Sync Mike's vault to GitHub
2. **manage-agent-runtime.py** (existing) → Add canonical-sync-check step
3. **GitHub Actions** → CI checks for frontmatter, canonical-id, wikilinks
4. **Claude Code skills** → Query canonical-registry (built-in via MCP)

---

## Part 8: Implementation Roadmap (If Approved)

### Phase 1: Foundation (Week 1)
- [ ] Define canonical-registry.json schema + initial population
- [ ] Add frontmatter schema to `schemas/` directory
- [ ] Update agent-configs/AGENTS.md with registry definition
- [ ] Create this doc in GitHub (agent-configs/docs/)

### Phase 2: Tooling (Week 2)
- [ ] Implement canonical-registry.py (query + sync)
- [ ] Add frontmatter-validator.py (CI check)
- [ ] Create wikilink-checker.py (verify canonical-ids)
- [ ] Add obsidian-sync.py (weekly export)

### Phase 3: Migration (Week 3-4)
- [ ] Audit existing docs; assign canonical-ids
- [ ] Add frontmatter to 80% of agent-configs/rules/
- [ ] Consolidate duplicate skills
- [ ] Test canonical-sync-check on agent-configs → ~/.agents

### Phase 4: Validation (Week 5)
- [ ] CI green on frontmatter checks
- [ ] Gbrain queries working (agent tests)
- [ ] Obsidian sync passing
- [ ] Wikilink audit shows no breaks

---

## Part 9: 10 Clarifying Questions for Mike

### Q1: Obsidian Ownership
**Question**: Should Mike's Obsidian vault stay personal (no agent access), or should agents read (but not write) to it?
- **Option A**: Keep private; weekly export only (lower risk)
- **Option B**: Grant read-only agent access; agents cite Obsidian notes as context (more powerful, but requires vaultless access)

### Q2: Gbrain Backend
**Question**: What's your preferred backend for gbrain storage?
- **Option A**: Postgres + pgvector (if you have existing Postgres setup)
- **Option B**: SQLite + embedding index (simpler, local)
- **Option C**: Separate vector DB (Qdrant, Weaviate; if you want scale)

### Q3: Canonical-ID Scheme
**Question**: Should canonical-IDs follow a pattern (e.g., `rule-NNN`, `decision-NNN`, `skill-XXX`), or free-form (semantic)?
- **Option A**: Pattern + number (easier to scan, but less descriptive)
- **Option B**: Semantic (rule-model-routing, decision-staged-ladder; more readable)
- **Option C**: Hybrid (prefix + suffix; e.g., `rule:model-routing:2026-q3`)

### Q4: Wikilink Strategy
**Question**: Should you keep using Obsidian's `[[file]]` syntax, or migrate to semantic links?
- **Option A**: Keep `[[file]]` + add canonical-id as alias (minimal change)
- **Option B**: Use `[[canonical-id]]` everywhere (requires Obsidian plugin)
- **Option C**: Use both; support both patterns (more flexible, more maintenance)

### Q5: Decision Versioning
**Question**: When a decision changes, should you create a new entry or update the existing one?
- **Option A**: New entry only (immutable; full audit trail)
- **Option B**: Update + git history (less clutter; still traceable)
- **Option C**: Both (superseded entries link to new ones; best for readers)

### Q6: Agent Access to Personal Vault
**Question**: If agents get read access to Obsidian, should they index ALL notes, or only tagged ones?
- **Option A**: All notes (maximum context, but privacy risk)
- **Option B**: Only notes tagged `#archive:true` or `#for-agents` (explicit opt-in)
- **Option C**: Separate "agent-visible" Obsidian vault (maximum control)

### Q7: Consolidation Frequency
**Question**: How often should old TASK.md files, research notes, etc. be consolidated to archives?
- **Option A**: Monthly (regular, but frequent moves)
- **Option B**: Quarterly (fewer moves, longer retention)
- **Option C**: Manual (only when you notice clutter; least overhead)

### Q8: GBrain Collection Hierarchy
**Question**: Should gbrain have a flat structure (all docs indexed globally) or hierarchical (collections → subcollections)?
- **Option A**: Flat (faster queries, all info equally weighted)
- **Option B**: Hierarchical (metadata/policies, context/project-state, etc.; better organization)
- **Option C**: Hybrid (collections for major categories, flat within each)

### Q9: Source-of-Truth Conflicts
**Question**: If agent-configs/rules/ and ~/.agents/rules/ diverge (out of sync), which wins?
- **Option A**: Always agent-configs (source of truth; agents get latest)
- **Option B**: Always ~/.agents (agents use cached version; safer for running systems)
- **Option C**: Depends on type (rules = agent-configs; roles = ~/.agents)

### Q10: Integration with Agent-SDLC
**Question**: Should agent-sdlc (the AISDLC repo) have its own canonical-registry entries, or inherit from agent-configs?
- **Option A**: Inherit entirely (single registry; less duplication)
- **Option B**: Agent-sdlc has own entries (project-specific decisions; more autonomy)
- **Option C**: Hybrid (core rules inherit; project-specific decisions are local)

---

## Part 10: Risk Analysis & Mitigation

### Risk 1: Over-Indexing
**Risk**: Indexing every document into gbrain creates noise; semantic search becomes less useful.
**Mitigation**: Only index documents with frontmatter; use `type` and `status` filters to exclude drafts/deprecated.

### Risk 2: Divergence Between Sources
**Risk**: agent-configs/rules/ and ~/.agents/rules/ get out of sync; agents run with stale policy.
**Mitigation**: CI check on every PR + nightly sync-validator + clear ownership (GitHub is source).

### Risk 3: Broken Wikilinks
**Risk**: If file renames happen, canonical-id system fails if IDs aren't updated.
**Mitigation**: Weekly wikilink audit; GitHub Actions enforces canonical-id presence in frontmatter.

### Risk 4: Privacy Leaks
**Risk**: If agents get Obsidian access, sensitive personal notes might leak into GitHub or shared logs.
**Mitigation**: Explicit tagging (`#archive:true`); agents never write to Obsidian; separate vault for agent-visible notes.

### Risk 5: Registry Staleness
**Risk**: canonical-registry.json grows stale; agents get wrong paths.
**Mitigation**: Registry is auto-generated from frontmatter (single source of truth); CI regenerates it on every merge.

### Risk 6: Gbrain Storage Costs
**Risk**: Indexing everything increases storage/compute; agents slow down.
**Mitigation**: Tiered indexing (hot: recent 30 days; warm: 30-90 days; cold: archive). Time-based pruning policy.

---

## Part 11: Success Metrics

**How will you know this architecture works?**

1. **Agent queries reduce context latency** (agents find answers in <100ms vs. scanning docs manually)
2. **Zero broken wikilinks** (canonical-id system prevents link rot)
3. **Decision traceability improves** (can trace any active rule back to decision that created it)
4. **Consolidation happens regularly** (old TASK.md files get archived automatically)
5. **Sync verification passes** (agent-configs ↔ ~/.agents stays in sync 100%)
6. **Frontmatter compliance** (all new docs have valid frontmatter; CI enforces)
7. **Personal vault stays clean** (Obsidian exports to archives weekly without manual work)
8. **Multi-agent coordination improves** (swarm-state.md is the single source of truth for who's doing what)

---

## Part 12: Appendices

### A. Canonical-ID Naming Convention Proposal

```
Type    | Prefix    | Example
--------|-----------|---------------------
Rule    | rule-     | rule-037-model-routing
        |           | (or rule-037 if used with file path)
Decision| decision- | decision-053-staged-ladder
        |           | (or decision-053)
Skill   | skill-    | skill-research-001
        |           | (or skill-research)
Role    | role-     | role-verifier
        |           | (or role-verifier-v1)
Intent  | intent-   | intent-2026-q3-north-star
        |           | (or intent-2026-q3)
Evidence| evidence- | evidence-rca-2026-09-03
        |           | (or evidence-2026-09-03)
```

### B. Frontmatter Validation Schema (JSON Schema)

```json
{
  "type": "object",
  "required": ["type", "status", "version", "canonical-id"],
  "properties": {
    "type": {
      "enum": ["rule", "skill", "decision", "intent", "role", "guide", "evidence"]
    },
    "status": {
      "enum": ["active", "draft", "archived", "deprecated"]
    },
    "version": {
      "pattern": "^[0-9]{4}\\.q[1-4]\\.[0-9]+$"
    },
    "canonical-id": {
      "pattern": "^(rule|decision|skill|role|intent|evidence)-[a-z0-9-]+$"
    },
    "updated": {
      "type": "string",
      "format": "date"
    },
    "related-agents": {
      "type": "array",
      "items": {"enum": ["Hermes", "Buzz", "Claude-Code", "Codex"]}
    }
  }
}
```

### C. Obsidian Plugin Recommendation

**obsidian-front-matter-title** or **obsidian-alias**
- Display canonical-id as document identifier in graph view
- Create aliases so `[[rule-037]]` resolves to actual filename

**obsidian-git**
- Already using; ensure configured to sync weekly
- Set branch to `main` (not personal branches)

**obsidian-dataview**
- Query documents by frontmatter (e.g., "Show all active rules")
- Useful for Mike's personal view of the system

---

## Conclusion

This architecture unifies three distinct knowledge systems (agent memory, operational rules, personal learning) into one coherent layer stack, with GitHub as the source of truth and semantic indexing (gbrain) as the fast-access layer.

**Key design principles**:
- Information flows in layers (Runtime → Operational → Archive → Personal)
- Canonical-ID + frontmatter prevent wikilink rot
- GitHub repos are source of truth; local copies are caches
- Agents query via registry (don't need to know file paths)
- Regular consolidation keeps the system lean and coherent

**Next step**: Schedule debrief with Mike to answer Q1–Q10, then begin Phase 1 implementation.

---

**Document version**: 2026.q3.1  
**Last updated**: 2026-09-04  
**Status**: Research + Design (awaiting Mike's input)
