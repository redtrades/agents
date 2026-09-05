---
name: request-complexity-classifier
description: Automatically infer request complexity and invoke appropriate skill tier Use when classifying user prompts into difficulty tiers 1 through 4.
tiers: [1, 2, 3, 4]
required_for: [all]
version: 1.0
author: agent-configs
---
# Request Complexity Classifier

**Analyze incoming requests and route to appropriate tier (1-4) with right skills.**

## Quick Start

Invoked automatically before every task. Agent reads request → determines tier → loads skills → executes.

## Algorithm

```
1. Parse request for tier signals (keywords, scope, risk)
2. Classify to tier 1-4
3. Check for user override (explicit tier prefix)
4. Load skills for that tier
5. Set workflow depth
6. Log classification for learning
```

## Tier Detection

### Tier 1: Quick (Typo, Config, Doc)
- Keywords: typo, doc, fix (alone), config, fast (not "quick feature")
- Scope: <50 lines, 1-3 files
- Risk: none
- Example: "Fix typo in README"
- Note: "quick" is only tier-1 when not paired with feature-words

### Tier 2: MVP (Bug Fix, Small Feature)
- Keywords: bug fix, MVP, quick feature, simple, small feature
- Scope: <500 lines, 3-10 files
- Risk: low
- Example: "Fix login form validation"

### Tier 3: Standard (Feature, Refactor)
- Keywords: feature, refactor, enhancement, standard
- Scope: 500-2000 lines, 10-30 files
- Risk: medium
- Example: "Add dark mode to dashboard"

### Tier 4: Audit (Production, Security, Compliance)
- Keywords: production, security, performance, critical, audit, compliance
- Scope: 2000+ lines, 30+ files
- Risk: high
- Example: "Audit session token handling"

## User Overrides

Prefix request with explicit tier:
```
"Quick fix: typo in docs" → tier-1 (override)
"MVP: add login form" → tier-2 (override)
"Standard: refactor auth" → tier-3 (override)
"Production: security audit" → tier-4 (override)
```

Agent respects override and adjusts workflow accordingly.

## Skill Routing

```
Tier 1: no skills (direct execution)
Tier 2: lean-build, response-format
Tier 3: superpowers, research, verify-before-asserting
Tier 4: superpowers, research, verify-before-asserting, sssf-sandbox-orchestrator
```

## Learning & Tracking

Log each classification in `knowledge/swarm-state.md`:
```yaml
classification:
  - request: "fix typo"
    inferred: 1
    actual: 1
    success: true
```

Target: 90%+ accuracy over 20-request window.

## Output

Returns:
```json
{
  "tier": 2,
  "confidence": 0.95,
  "skills": ["lean-build", "response-format"],
  "workflow": "investigate → implement → test → review",
  "override": false,
  "rationale": "Bug fix, localized scope, low risk"
}
```

## Integration

- Called via PreToolUse hook in settings.json
- Reads request context from AGENTS.md
- Routes to rules/tiering-strategy.md
- Logs results to knowledge/swarm-state.md

## Testing

Test with sample requests:
- Tier 1: "Fix typo in README"
- Tier 2: "Bug fix: login validation"
- Tier 3: "Add dark mode feature"
- Tier 4: "Production security audit"

Expected: 90%+ correct classification.
