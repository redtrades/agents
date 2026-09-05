# Skills Adoption Roadmap

**Priority:** Based on your agent/agentic focus + starred repos analysis  
**Last updated:** 2026-09-04

## Immediate Adoption (Week 1)

These fill gaps in your existing skill library:

### From Awesome Claude Skills (ComposioHQ)
- [ ] **superpowers**  -  Plan-spec-test workflow (complements your lean-build)
- [ ] **context7**  -  Fresh library docs on demand (pairs with your library skill)
- [ ] **debugging-patterns**  -  Structured debugging (extends verify-before-asserting)

### From Claude Skills 380 (alirezarezvani)
- [ ] **tdd-agent**  -  Test-driven development for agents
- [ ] **code-review**  -  Systematic code review (cross-repo standards)
- [ ] **architecture-audit**  -  Design review patterns

## Short-term Adoption (Weeks 2-4)

Fill agentic orchestration + multi-agent patterns:

### Agent Orchestration
- [ ] **agent-coordinator**  -  Multi-agent task distribution
- [ ] **swarm-patterns**  -  Collective problem-solving
- [ ] **tool-router**  -  Smart MCP server selection (Composio integration)

### Development Workflow
- [ ] **incident-response**  -  Production issue handling
- [ ] **knowledge-synthesis**  -  Cross-repo knowledge integration
- [ ] **proposal-drafting**  -  RFC/ADR generation (govcon-relevant)

## Medium-term Adoption (Month 2+)

Specialize by domain/project:

### For agent-sdlc
- [ ] **agent-testing-framework**  -  Unit testing agents
- [ ] **skill-evaluation**  -  Systematic skill assessment
- [ ] **regression-detection**  -  Catch breaking changes

### For govcon-factory
- [ ] **compliance-checker**  -  Regulations + standards audit
- [ ] **proposal-generator**  -  Government proposal templates
- [ ] **cost-analysis**  -  Budget + ROI calculations

### For agent-configs
- [ ] **documentation-generator**  -  Auto-doc from code
- [ ] **example-curator**  -  Real-world examples library
- [ ] **skill-marketplace-manager**  -  Marketplace updates/vetting

## Adoption Process

For each skill:

1. **Source** it from marketplace or community
   ```bash
   git clone https://github.com/ComposioHQ/awesome-claude-skills.git /tmp/source
   cp -r /tmp/source/superpowers ~/agent-configs/skills/superpowers
   ```

2. **Validate** with skill-doctor
   ```bash
   claude skill-doctor superpowers
   ```

3. **Test** in a real task
   ```bash
   cd ~/agent-sdlc && claude --skill superpowers "draft architecture plan"
   ```

4. **Document** in skills library manifest
   ```bash
   echo "- superpowers (v1.0): plan-spec-test workflow" >> ~/agent-configs/SKILLS.md
   ```

5. **Share** your review
   - Star the skill repo if useful
   - File issues if you find problems
   - Contribute improvements back

## Vetting Checklist

Before adding a skill to ~/agent-configs/skills/:

- [ ] SKILL.md has clear frontmatter + description
- [ ] Instructions are <150 lines (concise)
- [ ] Tested on real task (not just example)
- [ ] No hardcoded paths or assumptions
- [ ] Clear scope (what it solves)
- [ ] Skill-doctor passes validation
- [ ] Community has 5+ GitHub stars (validation signal)

## Community Skills Scoring

Based on analysis of top repos:

| Repo | Stars | Skills | Match | Priority |
|------|-------|--------|-------|----------|
| awesome-claude-skills (Composio) | 1000+ | 1000+ | 95% | 🔴 High |
| claude-skills (alirezarezvani) | 380+ | 380+ | 90% | 🔴 High |
| awesome-claude-code-toolkit | 300+ | 35+ | 85% | 🟡 Medium |
| VoltAgent/awesome-agent-skills | 250+ | 1000+ | 80% | 🟡 Medium |

Your starred repos are excellent sources. Prioritize by community validation (stars) + relevance to agent/agentic work.

## Monitoring & Updates

Set a monthly review:

1. Check for new stars in your watchlist (awesome-* repos)
2. Test top new skills (newly starred by community)
3. Retire unused skills from ~/agent-configs/skills/
4. Update this roadmap quarterly

## Current Library Status

Your existing 13+ skills:

✅ **Strong:**
- lean-build (fast iteration)
- research (investigation)
- sssf-sandbox-orchestrator (isolation)
- verify-before-asserting (validation)

🟡 **Gaps to fill:**
- Multi-agent coordination (add agent-coordinator)
- Systematic testing (add tdd-agent)
- Tool selection (add tool-router with Composio)

## Reference: Top Skills by Use Case

### Agent Orchestration
1. sssf-sandbox-orchestrator (you have this ✅)
2. agent-coordinator (from awesome-claude-skills)
3. swarm-patterns (from claude-skills)

### Development
1. lean-build (you have this ✅)
2. superpowers (adopt immediately)
3. tdd-agent (adopt week 2)

### Verification
1. verify-before-asserting (you have this ✅)
2. code-review (adopt week 1)
3. regression-detection (adopt month 2)

### Research & Learning
1. research (you have this ✅)
2. context7 (adopt immediately)
3. library (you have this ✅)

## Quick Action

Start with 3 skills this week:

```bash
# 1. Add superpowers
git clone https://github.com/.../superpowers /tmp/sp
cp -r /tmp/sp ~/agent-configs/skills/superpowers

# 2. Add code-review
git clone https://github.com/.../code-review /tmp/cr
cp -r /tmp/cr ~/agent-configs/skills/code-review

# 3. Add context7
git clone https://github.com/.../context7 /tmp/c7
cp -r /tmp/c7 ~/agent-configs/skills/context7

# Validate all three
claude skill-doctor superpowers code-review context7
```

Then test each in a real task before next adoption cycle.

## Success Metrics

You'll know adoption is working when:

- ✅ Skills load automatically without prompts
- ✅ skill-doctor validation passes consistently
- ✅ Tasks complete faster (skill selection is obvious)
- ✅ No "this skill doesn't apply" mismatches
- ✅ Community skills improve your standard task time by 20%+

Track time before/after for 3-4 tasks per new skill.
