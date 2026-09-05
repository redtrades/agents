# Disler's Best-of-Breed Agent Patterns: Comprehensive Research

**Research Date**: September 4, 2026  
**Researcher**: Claude Code Agent  
**Focus Repos**: 
- `super-simple-software-factory` (3.9k stars)
- `claude-code-hooks-mastery` (3.9k stars)
- `claude-code-hooks-multi-agent-observability` (1.5k stars)
- `pi-vs-claude-code` (1.7k stars)
- `always-on-ai-assistant` (998 stars)
- `multi-agent-postgres-data-analytics` (887 stars)

---

## Executive Summary

Disler's research identifies **five core patterns** that make agentic systems reliable, observable, and maintainable:

1. **Envelope + Gates Architecture** — agents output structured JSON validated by deterministic gates, not prose predictions
2. **Phase-Based Orchestration** — Python owns sequencing/retries; agents own bounded work inside named phases
3. **Hierarchical Hook Integration** — lifecycle events stream to persistent SQLite, enabling live observability without WebSocket
4. **Prompt Specialization** — each agent gets distinct system/user prompts, model, thinking level, and write permissions
5. **Multi-Agent Coordination** — peer-to-peer messaging, team dispatch, and context passing patterns for parallel execution

**Adopting these patterns improves**:
- Error recovery (same session, cost one message vs. cold restart)
- Observability (queryable trace replaces opaque transcripts)
- Reusability (agent roster as YAML + skills as stamped directories)
- Safety (validation before running, predictable permission model)

---

## Part 1: Agent Response Formatting

### 1.1 The Envelope Pattern (Core Innovation)

**Problem Solved**: Free-form agent outputs lead to parsing ambiguity, unvalidated claims, and expensive retry loops.

**Disler Solution**: Agents return strictly-typed JSON envelopes, never markdown or prose.

```python
# Base envelope all agents return
class EnvelopeBase(BaseModel):
    status: Literal["success", "fail"]
    summary: str = ""
    artifacts: list[str] = Field(default_factory=list)
    notes_for_next_agent: str = ""

# Specialized envelopes per workflow phase
class PlanOutput(EnvelopeBase):
    specification_path: str
    acceptance_criteria: list[str]

class BuildOutput(EnvelopeBase):
    changed_files: list[str]
    commit_message: str

class TestOutput(EnvelopeBase):
    test_count: int
    pass_count: int
    failure_summary: str
```

**Key Properties**:
- **Strongly Typed**: Pydantic validates shape before processing
- **Phase-Specific**: Each workflow phase defines its own contract
- **Bidirectional Metadata**: `notes_for_next_agent` chains context between phases
- **No Free-Form Text**: Status and summary only; details go in structured fields

**Adoption Pattern for 105-Skill Setup**:
```yaml
# In skill definition
response_envelope:
  type: SkillOutput
  fields:
    status: success | fail | partial
    result: Any  # type-specific per skill
    errors: list[str]
    evidence: dict  # proof of work
    next_action: str  # what to do next
```

### 1.2 Gate Verification Pattern

**Core Insight**: "Agent proposes, code disposes." Never trust declarations—validate actual outcomes.

**Built-in Gates** (from SSSF):
```python
gates = {
    "artifacts_exist": lambda artifacts: all(os.path.exists(a) for a in artifacts),
    "files_non_empty": lambda files: all(os.path.getsize(f) > 0 for f in files),
    "json_parses": lambda envelope: json.loads(envelope) is not None,
    "diff_matches_claims": lambda diff, claims: validate_claims_in_diff(diff, claims),
    "tests_pass": lambda cmd: subprocess.run(cmd, capture_output=True).returncode == 0,
}
```

**Application Pattern**:
1. Agent returns envelope with claims (e.g., `changed_files: [src/api.py, tests/api_test.py]`)
2. Code immediately runs gates:
   ```python
   gate_results = {
       "files_exist": gates["artifacts_exist"] (envelope.changed_files),
       "tests_pass": gates["tests_pass"] (["pytest", "tests/"])
   }
   ```
3. **If gates pass**: proceed to next phase
4. **If gates fail**: re-prompt same session with corrections (cost: one message + context window reuse)

**Adoption Recommendation**:
- Create skill-level gates that validate output before skill completion
- Example for a code-review skill:
  ```python
  @gate
  def annotations_present(output: ReviewOutput) -> bool:
      return all(finding.file_path and finding.line_number 
                 for finding in output.findings)
  
  @gate
  def severity_valid(output: ReviewOutput) -> bool:
      valid_severities = {"critical", "major", "minor", "suggestion"}
      return all(f.severity in valid_severities for f in output.findings)
  ```

### 1.3 Error Formatting + Recovery

**Disler's Principle**: "Corrections in same session, not cold restarts."

**Pattern**:
```
GATE FAILURE: diff_matches_claims
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your envelope claimed to add health endpoint but diff shows:
  - removed: /src/routes.py line 42-45
  + added: /src/health.js line 1-30

Your claims: ["changed_files: [src/routes.py]"]
Actual diff shows: routes.py NOT in output, health.js unexpected

CORRECTION NEEDED:
  1. Review actual diff above
  2. Update envelope.changed_files to match reality
  3. Explain discrepancies in notes_for_next_agent
  4. Return corrected envelope
```

**Benefits over cold restarts**:
- Agent retains context (doesn't recompute the whole phase)
- Cost = 1 correction message vs. N regeneration attempts
- Success rate improves because agent sees what actually happened

**Adoption for Claude Code**:
```python
# In skill/hook error handler
def handle_gate_failure(envelope, gate_name, gate_error):
    correction_prompt = f"""
    GATE FAILURE: {gate_name}
    ────────────────────────
    {gate_error}
    
    Original envelope:
    {json.dumps(envelope, indent=2)}
    
    Please correct and resubmit.
    """
    # Re-prompt same agent session, not cold restart
    agent.send_message(correction_prompt)
```

### 1.4 Multi-Step Response Breaking

**Pattern**: Break complex work into phases; each agent returns a bounded envelope.

```
Workflow: adw_plan_build_test_quality
Phase 1: Engineer → Planner
  Returns: { specification_path, acceptance_criteria, notes_for_builder }
  
Phase 2: Planner output → Builder
  Receives: specification_path in notes_for_next_agent
  Returns: { changed_files, commit_message, notes_for_tester }
  
Phase 3: Builder output → Tester
  Receives: changed_files to test
  Returns: { test_count, pass_count, failure_summary, notes_for_fixer }
  
Phase 4: Tester output → Reviewer (or circle back to Builder)
  Receives: test failures
  Returns: { approval | rejection, feedback_for_builder }
```

**Key Benefit**: Each phase is independent, replayable, and can use different models/thinking levels.

**Adoption Pattern**:
```yaml
# skill definition with multi-step output
skill:
  name: code_review_multi_step
  steps:
    - name: analyze
      output: AnalysisOutput
    - name: format_findings
      output: FormattedFindingsOutput
    - name: validate
      output: FinalReviewOutput  # strongly-typed at end
```

---

## Part 2: Code Formatting Standards

### 2.1 Prompt Formatting

**Disler Pattern**: Separate system and user prompts per agent.

**Directory Structure**:
```
adws/adw_data/prompt_engineering/
├── planner/
│   ├── system.md          # Role, constraints, output format
│   └── user.md            # Task-specific instructions
├── builder/
│   ├── system.md
│   └── user.md
├── reviewer/
│   ├── system.md
│   └── user.md
```

**Example System Prompt** (from SSSF):
```markdown
# System: Planner Agent

You are a specification expert. Your role is to:
1. Convert vague requests into implementable plans
2. Define acceptance criteria upfront
3. Generate a specification file in YAML format
4. Output a structured PlanOutput envelope

## Output Format (REQUIRED)
You MUST return valid JSON matching this type:
{
  "status": "success" | "fail",
  "summary": "one-line summary",
  "specification_path": "specs/feature-name.yaml",
  "acceptance_criteria": ["criterion 1", "criterion 2"],
  "notes_for_next_agent": "context for builder"
}

## Constraints
- Specifications must be under 500 lines
- Acceptance criteria must be testable
- Do not write code; write specifications
```

**Example User Prompt**:
```markdown
# User: Planning Request

REQUEST:
{{ user_request }}

CONTEXT FROM PREVIOUS PHASES:
{{ previous_agent_notes }}

SPECIFICATION TEMPLATE:
```yaml
name: {{ feature_name }}
description: {{ brief_description }}
acceptance_criteria:
  - criterion 1
  - criterion 2
changes:
  - file: path/to/file
    reason: why changed
```

YOUR TASK:
1. Read the request
2. Output a specification YAML file
3. Return the envelope with specification_path set
```

### 2.2 Code Snippet Formatting in Agent Prompts

**Disler's Approach**: Inline code with language tags and annotations.

```markdown
# System Prompt for Code Generation

When showing code fixes, use this format:

\`\`\`python
# Before: the problematic code
def old_function():
    return data  # BUG: data not defined

# After: the corrected code
def new_function():
    result = fetch_data()  # FIXED: now fetches
    return result
\`\`\`

When explaining changes:
- Use `inline_code` for variable/function names
- Use \`\`\`diff\`\`\` for showing file diffs
- Annotate with // CHANGE or # TODO: so agent knows intent
```

**Adoption for Skills**:
```python
# In skill system prompt
PROMPT_TEMPLATE = """
When returning code modifications, format as:

```{language}
# BEFORE
{old_code}

# AFTER
{new_code}

# EXPLANATION
{why changed}
```

Never embed multiple changes in one block. One change = one block.
"""
```

### 2.3 Test Case Formatting

**Disler Pattern**: Test output as structured TestOutput envelope.

```python
class TestOutput(EnvelopeBase):
    test_count: int
    pass_count: int
    fail_count: int
    skipped_count: int
    failures: list[TestFailure]

class TestFailure(BaseModel):
    test_name: str
    file_path: str
    line_number: int
    error_message: str
    assertion: str
```

**Example Test Output**:
```json
{
  "status": "fail",
  "summary": "8/10 tests passed",
  "test_count": 10,
  "pass_count": 8,
  "fail_count": 2,
  "failures": [
    {
      "test_name": "test_api_endpoint_404",
      "file_path": "tests/api_test.py",
      "line_number": 45,
      "error_message": "AssertionError: 404 != 200",
      "assertion": "assert response.status_code == 200"
    }
  ],
  "notes_for_next_agent": "Tests 5 and 7 fail due to missing /health endpoint"
}
```

**Usage Pattern**: Builder receives failures as `notes_for_next_agent`, eliminating need to re-parse test output.

### 2.4 Diff Presentation

**Format**: Three-section diff for agent clarity.

```
DIFF SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Files changed: 3
Lines added: 42
Lines removed: 18
Net change: +24 lines

AFFECTED FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- src/api.py (modified)
- tests/api_test.py (new)
- config.yaml (modified)

UNIFIED DIFF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
--- a/src/api.py
+++ b/src/api.py
@@ -10,6 +10,8 @@
 def health_check():
-    return {"status": "ok"}
+    return {
+        "status": "ok",
+        "timestamp": time.time()
+    }
```

**Adoption**: Structure diffs this way before sending to next agent in phase chain.

---

## Part 3: Prompt Patterns

### 3.1 System Prompt Structure

**Disler's Pattern**: Five-section system prompts.

```
[1] ROLE & CONTEXT (Who you are)
[2] OUTPUT FORMAT (What to return)
[3] CONSTRAINTS (Hard rules)
[4] EVALUATION CRITERIA (How success is measured)
[5] ERROR HANDLING (What to do when stuck)
```

**Template**:
```markdown
# System: {{ Agent Name }}

## Role
You are a {{ specialized title }}. Your responsibility is to {{ core purpose }}.

## Output Format
You MUST return JSON matching this Pydantic model:
{
  "status": "success" | "fail",
  ...
}

Do not return markdown, prose, or any other format.

## Constraints
- Constraint 1: {{ specific rule }}
- Constraint 2: {{ specific rule }}
- Hard limit: {{ quantified boundary }}

## Success Criteria
Your output is successful if:
1. {{ measurable criterion }}
2. {{ measurable criterion }}

These will be validated by automated gates.

## If Stuck
If you cannot complete the task:
1. Set status: "fail"
2. Explain reason in summary
3. List attempted approaches in notes_for_next_agent
4. Do not guess or fabricate solutions
```

### 3.2 Few-Shot Examples

**Disler's Approach**: 2-3 examples, not 10+. Format as envelope pairs.

```markdown
## Examples

### Example 1: Successful Plan
INPUT: "Add user authentication"
OUTPUT:
{
  "status": "success",
  "summary": "Auth specification created",
  "specification_path": "specs/auth.yaml",
  "acceptance_criteria": [
    "JWT tokens issued on login",
    "Tokens validated on protected routes",
    "Expired tokens rejected with 401"
  ],
  "notes_for_next_agent": "Use bcrypt for password hashing. See specs/auth.yaml for full flow."
}

### Example 2: Failure Case
INPUT: "Make it faster" (vague)
OUTPUT:
{
  "status": "fail",
  "summary": "Request too vague for specification",
  "notes_for_next_agent": "Ask: what component? what metric? what baseline?"
}
```

**Benefit**: Two examples that show both success and failure handling. No over-specification.

### 3.3 Constraint Specification

**Disler Pattern**: Separate hard constraints from soft preferences.

```markdown
## Hard Constraints (MUST)
- [ ] Output is valid JSON
- [ ] All fields present (even if null)
- [ ] File paths use forward slashes
- [ ] No references to external APIs

## Soft Preferences (SHOULD)
- Keep summaries under 200 characters
- Group related changes together
- Suggest optimizations in notes_for_next_agent
- Include reasoning for complex decisions
```

**Implementation**:
```python
# Mark hard constraints for validation
HARD_CONSTRAINTS = {
    "json_valid": lambda output: json.loads(output) is not None,
    "required_fields": lambda data: all(k in data for k in ["status", "summary"]),
}

# Use for gate failures
if not HARD_CONSTRAINTS["json_valid"] (agent_output):
    # This is a hard failure—correction needed
    raise GateFailure("Output is not valid JSON")
```

### 3.4 Verification Patterns

**Disler's Self-Check Approach**: Include verification steps in the prompt.

```markdown
## Before You Submit

1. [ ] JSON parses in Python: json.loads(output)
2. [ ] All fields match the schema
3. [ ] No null values in required fields
4. [ ] Paths exist or will be created by next phase
5. [ ] Notes for next agent explain any ambiguities

If any check fails, fix and resubmit.
```

**Adoption for Skills**:
```python
# In skill prompt
VERIFICATION_CHECKLIST = """
Before returning your result:
1. Validate your output against the skill schema
2. Verify all evidence files exist
3. Check that recommendations are actionable
4. Ensure error messages are specific (not generic)

If you cannot pass all checks, return status: "fail" with explanation.
"""
```

---

## Part 4: Skills/Tools Organization

### 4.1 Disler's Agent Roster Pattern

**Core Concept**: Each agent is a role with distinct model, thinking level, tools, and prompts.

```yaml
# sssf.config.yaml pattern
defaults:
  coding_agent: pi
  model: google/gemini-3.6-flash
  thinking: medium
  protected_files:
    - adws/adw_modules/
    - adws/adw_sssf_config/
  data_dir: adws/adw_data

agents:
  - name: planner
    model: fireworks/accounts/fireworks/models/kimi-k3
    thinking: high
    color: "#a78bfa"
    purpose: "Turn requests into implementable plans"
    prompt_engineering:
      system: adws/adw_data/prompt_engineering/planner/system.md
      user: adws/adw_data/prompt_engineering/planner/user.md
    writes:
      - specs/
    tools:
      - read_files
      - create_files

  - name: builder
    model: google/gemini-3.6-flash
    thinking: medium
    color: "#34d399"
    purpose: "Implement specifications with code"
    prompt_engineering:
      system: adws/adw_data/prompt_engineering/builder/system.md
      user: adws/adw_data/prompt_engineering/builder/user.md
    writes:
      - src/
      - tests/
    tools:
      - read_files
      - create_files
      - bash_execute

  - name: reviewer
    model: google/gemini-3.6-flash
    thinking: high
    color: "#f87171"
    purpose: "Validate code quality and security"
    prompt_engineering:
      system: adws/adw_data/prompt_engineering/reviewer/system.md
      user: adws/adw_data/prompt_engineering/reviewer/user.md
    writes: []  # read-only
    tools:
      - read_files
      - bash_execute_readonly
```

**Key Properties**:
- **One YAML file defines agent roster** — no scattered configs
- **Different models at different cost/speed** — planner gets expensive model, builder uses cheaper
- **Thinking levels vary** — planner: high, builder: medium
- **Write permissions bounded** — reviewer writes nowhere
- **Tools per agent** — reviewer doesn't get bash write access

### 4.2 Tool/Skill Routing Logic

**Pattern**: Route tools based on agent role, phase, and output type.

```python
# Pseudocode for skill/tool dispatcher
class AgentPhaseRouter:
    def route(self, agent_name: str, phase: str, envelope: EnvelopeBase) -> str:
        """Return next agent/skill based on output."""
        
        # Route by envelope status
        if envelope.status == "fail":
            return "reviewer"  # send to validator
        
        # Route by phase sequence
        phase_chains = {
            "plan": "build",
            "build": "test",
            "test": "review",
            "review": "document" if envelope.approval else "builder"  # loop or proceed
        }
        return phase_chains.get(phase, "engineer")  # default to human decision
    
    def get_tools_for_agent(self, agent_name: str) -> list[str]:
        """Return tools available to this agent."""
        config = self.load_config()
        agent = config.agents.get(agent_name)
        return agent.tools if agent else []
```

**Adoption for 105-Skill Setup**:
```yaml
# skill router config
skill_dispatch:
  - condition: "output.type == 'review_findings'"
    next_skill: "code_review_formatter"
  
  - condition: "output.status == 'fail' && attempt_count < 3"
    next_skill: "same_agent_retry"  # correction in same session
  
  - condition: "output.severity == 'critical'"
    next_skill: "alert_human"  # escalate
```

### 4.3 Error Handling in Skill Chains

**Pattern**: Explicit error contracts at skill boundaries.

```python
# Skill defines what can go wrong
class SkillError(BaseModel):
    skill_name: str
    error_type: Literal["parse", "validation", "timeout", "permission", "resource"]
    message: str
    recovery_action: str  # what to do next

# Skill chain catches and routes errors
def run_skill_chain(skills: list[str]):
    for skill in skills:
        try:
            output = run_skill(skill)
        except SkillError as e:
            if e.error_type == "parse":
                # Correction: re-prompt same agent
                output = re_prompt_with_error(skill, e.message)
            elif e.error_type == "timeout":
                # Escalate: skip to manual review
                return escalate_to_human(e)
            elif e.error_type == "permission":
                # Halt: request permission interactively
                grant_permission(e.resource)
                output = run_skill(skill)  # retry
```

### 4.4 Skill Composition Patterns

**Disler's Approach**: Workflows are 40-180 lines, composable sequences.

```python
# Example workflow: adw_plan_build_test
async def adw_plan_build_test(request: str, adw_id: str = None):
    session = create_or_resume_session(adw_id)
    
    # Phase 1: Planning
    planner_input = UserPrompt(text=request)
    plan_output = await run_phase(
        agent="planner",
        prompt=planner_input,
        envelope_type=PlanOutput,
        gates=["json_parses", "specification_exists"]
    )
    if plan_output.status == "fail":
        return session.fail_with(plan_output)
    
    # Phase 2: Building
    builder_input = BuilderPrompt(
        plan=plan_output.specification_path,
        context=plan_output.notes_for_next_agent
    )
    build_output = await run_phase(
        agent="builder",
        prompt=builder_input,
        envelope_type=BuildOutput,
        gates=["json_parses", "files_exist", "git_commit_valid"]
    )
    if build_output.status == "fail":
        return session.fail_with(build_output)
    
    # Phase 3: Testing
    tester_input = TesterPrompt(
        files=build_output.changed_files,
        context=build_output.notes_for_next_agent
    )
    test_output = await run_phase(
        agent="tester",
        prompt=tester_input,
        envelope_type=TestOutput,
        gates=["json_parses", "tests_executed"]
    )
    
    return session.succeed_with({
        "plan": plan_output,
        "build": build_output,
        "test": test_output
    })
```

**Reusability**:
- Copy and modify the closest workflow
- Change agent names, prompts, or gate list
- New workflow is now runnable with same infrastructure

---

## Part 5: Response Chaining

### 5.1 Multi-Agent Conversation Model

**Disler Pattern**: Explicit conversation flows, not free-form chaining.

```python
# Define who talks to whom
CONVERSATION_FLOW_PLAN_BUILD_TEST = {
    1: {
        "speaker": "engineer",  # human
        "listener": "planner",
        "contract": PlanOutput
    },
    2: {
        "speaker": "planner",
        "listener": "builder",
        "contract": BuildOutput
    },
    3: {
        "speaker": "builder",
        "listener": "tester",
        "contract": TestOutput
    },
    4: {
        "speaker": "tester",
        "listener": "reviewer",
        "contract": ReviewOutput
    }
}

# Execute flow
for step_num, flow in CONVERSATION_FLOW_PLAN_BUILD_TEST.items():
    input_envelope = previous_output if step_num > 1 else initial_request
    output_envelope = run_agent(
        agent=flow["listener"],
        input_envelope=input_envelope,
        contract_type=flow["contract"]
    )
    # Validate gate before proceeding
    assert validate_envelope(output_envelope, flow["contract"])
    previous_output = output_envelope
```

**Key Benefit**: Conversation flow is explicit, testable, and differs from implementation.

### 5.2 Context Passing Between Agents

**Pattern**: Use `notes_for_next_agent` field for asynchronous context.

```python
# Phase 1 output
plan_output = PlanOutput(
    status="success",
    specification_path="specs/feature.yaml",
    notes_for_next_agent="""
    BUILDER CONTEXT:
    - Use async/await for all I/O
    - Database migrations in alembic/versions/
    - Tests must pass before commit
    - Reference spec sections: 2.1-2.4 for API design
    
    BUILDER TOOLS:
    - Can write to src/ and tests/
    - Cannot modify config files
    """
)

# Phase 2: Builder receives context
builder_prompt = f"""
SPECIFICATION: {load_file(plan_output.specification_path)}

CONTEXT FROM PLANNER:
{plan_output.notes_for_next_agent}

TASK:
Implement the specification above.
"""
```

**Advantages**:
- No special context passing mechanism needed
- Context is visible in traces
- Next agent can decide to ignore context if invalid
- Context survives through error corrections

### 5.3 State Management Across Turns

**Disler's SQLite Trace Pattern**:

```sql
-- All state lives in one database
CREATE TABLE sessions (
    adw_id TEXT PRIMARY KEY,
    status TEXT,  -- active, success, fail
    total_tokens INTEGER,
    started_at DATETIME,
    ended_at DATETIME
);

CREATE TABLE phases (
    phase_id TEXT PRIMARY KEY,
    adw_id TEXT,  -- FK to sessions
    seq INTEGER,
    name TEXT,     -- planner, builder, tester
    kind TEXT,     -- agent, code, engineer
    owner TEXT,    -- agent name
    status TEXT,   -- running, success, fail
    started_at DATETIME,
    ended_at DATETIME
);

CREATE TABLE envelopes (
    envelope_id TEXT PRIMARY KEY,
    phase_id TEXT,  -- FK to phases
    type TEXT,      -- PlanOutput, BuildOutput, etc.
    data JSON,      -- full envelope JSON
    created_at DATETIME
);

CREATE TABLE gate_results (
    gate_id TEXT PRIMARY KEY,
    envelope_id TEXT,  -- FK to envelopes
    gate_name TEXT,    -- "json_parses", "files_exist"
    passed BOOLEAN,
    error_message TEXT
);
```

**State Query Patterns**:
```sql
-- Current session status
SELECT status, total_tokens FROM sessions WHERE adw_id = ? ORDER BY started_at DESC LIMIT 1;

-- What happened in phase 2?
SELECT data FROM envelopes WHERE phase_id IN (
    SELECT phase_id FROM phases WHERE adw_id = ? AND seq = 2
);

-- Which gates failed?
SELECT gate_name, error_message FROM gate_results WHERE envelope_id = ? AND passed = false;

-- Replay session from phase 3 onward
SELECT * FROM phases WHERE adw_id = ? AND seq >= 3 ORDER BY seq;
```

**Adoption for Claude Code + MCP**:
- Store session state in persistent SQLite instead of transcript
- Query state instead of parsing chat history
- Resume incomplete phases without re-running earlier work

### 5.4 Evidence Collection from Responses

**Pattern**: Agents include evidence links in envelopes.

```python
class ReviewOutput(EnvelopeBase):
    status: Literal["approved", "rejected", "revision_needed"]
    findings: list[Finding]
    evidence: dict[str, str]  # links to proof
    
class Finding(BaseModel):
    severity: Literal["critical", "major", "minor"]
    rule: str
    file_path: str
    line_number: int
    message: str
    evidence_url: str  # link to test, lint report, etc.

# Example output
review = ReviewOutput(
    status="revision_needed",
    findings=[
        Finding(
            severity="major",
            rule="unused_import",
            file_path="src/api.py",
            line_number=5,
            message="Module 're' imported but never used",
            evidence_url="lint_report.html#L5"
        )
    ],
    evidence={
        "lint_report": "adws/adw_data/output/lint_report.html",
        "test_failure": "adws/adw_data/output/test_report.json",
        "diff": "adws/adw_data/output/changes.diff"
    },
    notes_for_next_agent="See lint_report for full details. Fixes needed in 3 files."
)
```

**Benefit**: Next agent (or human reviewer) can follow evidence links instead of re-running analysis.

---

## Part 6: Adoption Roadmap

### Immediate Wins (Week 1)

1. **Create Envelope Types**
   - Define `SkillOutput` base class for your skill ecosystem
   - Derive specialized envelopes per skill family
   - Add to shared type library

2. **Establish Response Validation**
   - Implement gate system for skill outputs
   - Wire gates into skill completion handlers
   - Create correction flow for failed gates

3. **Separate Prompts**
   - Move inline prompts to `.claude/prompt_templates/{skill}/system.md` and `user.md`
   - Reference them in skill configs via YAML
   - Add prompt versioning (v1, v2, ...)

### Medium-Term (Week 2-3)

4. **Build Observable Trace**
   - Create SQLite schema for skill execution traces
   - Log all events: skill_start, phase_complete, gate_pass, gate_fail
   - Write query templates for common forensics

5. **Implement Skill Routing**
   - Create router based on envelope status and type
   - Define conversation flows for multi-skill sequences
   - Test error routing (fail → retry, critical → escalate)

6. **Create Skill Roster YAML**
   - Document each skill's role, model preference, tools, write permissions
   - Reference in orchestration layer
   - Enable dynamic skill selection

### Long-Term (Week 4+)

7. **Build Observability Dashboard**
   - SQLite → Vue.js live session waterfall
   - Filter by skill/status/time window
   - Drill into phase details and gate results

8. **Standardize Workflows**
   - Document common patterns (code review, planning, building)
   - Provide templates for 80/20 use cases
   - Enable skill composition without custom code

9. **Establish Correction Loop**
   - Same-session corrections for validation failures
   - Track correction counts and success rates
   - Analyze failure patterns for prompt improvements

---

## Part 7: Key Differences from Current Setup

### Your Setup (105 Skills, Marketplace)
- Skills are independent, fire-and-forget
- No shared response envelope type
- Prompts mixed with skill definitions
- Limited multi-agent coordination
- Transcript is primary audit trail

### Disler's Setup (SSSF, Observable)
- Skills are nodes in explicit workflows
- Strongly-typed envelopes at every boundary
- Prompts separated, versioned, referenceable
- Multi-agent orchestration is first-class
- SQLite trace is audit trail; transcript is secondary

### Comparison Table

| Dimension | Current | Disler | Recommendation |
|-----------|---------|--------|-----------------|
| Response Type | varies | JSON envelope | adopt envelope pattern |
| Validation | per-skill | automated gates | adopt gates |
| Error Recovery | cold restart | same-session correction | adopt correction flow |
| Multi-Agent | task-based | phase-based orchestration | adopt workflow chains |
| Observability | transcript search | queryable trace | adopt SQLite trace |
| Routing Logic | ad-hoc | explicit flow config | adopt flow definitions |
| Prompt Storage | embedded | separate YAML | adopt separation |
| Tool Access | global | per-agent | adopt roster pattern |

---

## Part 8: Integration Points

### Claude Code Hooks + SSSF Pattern

```python
# .claude/hooks/PostToolUseSuccess.py
# Integrate Disler's gate pattern

import json
from pathlib import Path

def validate_skill_output(tool_name, tool_use_id, result):
    """Gate pattern applied to Claude Code hooks."""
    
    # Parse skill output as envelope
    try:
        envelope = json.loads(result)
    except json.JSONDecodeError:
        return False, "Output is not valid JSON"
    
    # Validate required fields
    if not all(k in envelope for k in ["status", "summary"]):
        return False, "Missing required envelope fields"
    
    # Gate-specific validation
    if tool_name == "code_review":
        # Check for evidence links
        if "evidence" not in envelope:
            return False, "Code review missing evidence links"
    
    return True, "OK"

# Store result in trace database
import sqlite3
db = sqlite3.connect(".claude/trace.db")
db.execute("""
    INSERT INTO tool_results (tool_name, tool_use_id, envelope, validated)
    VALUES (?, ?, ?, ?)
""", (tool_name, tool_use_id, result, validated))
db.commit()
```

### MCP Server Integration

```python
# MCP tool returns structured envelope
class SkillExecutor(MCPTool):
    def execute(self, skill_name: str, prompt: str) -> SkillOutput:
        # Run skill (via skill system or local agent)
        result = run_skill(skill_name, prompt)
        
        # Validate against envelope schema
        envelope = SkillOutput(**result)
        
        # Store in trace
        self.trace_db.record_skill_execution(
            skill=skill_name,
            envelope=envelope,
            gates_passed=validate_gates(envelope)
        )
        
        return envelope
```

### Workflow Definition in Claude Code Settings

```json
{
  "workflows": {
    "code_review_to_fix": {
      "steps": [
        {
          "skill": "code_review",
          "contract": "CodeReviewOutput",
          "gates": ["findings_present", "severity_valid"],
          "on_fail": "correct_in_same_session"
        },
        {
          "skill": "fix_code",
          "contract": "FixOutput",
          "gates": ["files_changed", "tests_pass"],
          "on_fail": "ask_builder_retry"
        }
      ]
    }
  }
}
```

---

## Part 9: Concrete Examples for Adoption

### Example 1: Code Review Skill with Envelope Pattern

**Before** (current):
```python
skill_definition = {
    "name": "code_review",
    "prompt": "Review this code and find bugs...",
    "output": "list of findings"  # vague
}
```

**After** (Disler pattern):
```python
# skills/code_review/definition.yaml
name: code_review
model: gpt-4
thinking: high
purpose: Find bugs and style issues in code
output_contract:
  type: CodeReviewOutput
  required_fields:
    - status: "success" | "fail"
    - findings: list[Finding]
    - evidence_links: dict[str, str]

gates:
  - name: findings_valid
    check: all(f.line_number and f.file_path for f in findings)
  - name: severity_meaningful
    check: all(f.severity in ["critical", "major", "minor"] for f in findings)
  - name: evidence_exists
    check: all(path_exists(link) for link in evidence_links.values())

# skills/code_review/prompts/system.md
# Code Review Agent

You are an expert code reviewer. Your job is to:
1. Find bugs, security issues, and style problems
2. Provide line-by-line feedback
3. Return structured findings with evidence

## Output Format
Return JSON matching CodeReviewOutput:
{
  "status": "success",
  "summary": "Found 3 issues",
  "findings": [{
    "severity": "major",
    "file": "src/api.py",
    "line": 42,
    "message": "SQL injection vulnerability",
    "evidence_url": "lint_report.html#L42"
  }],
  "evidence_links": {
    "lint_report": "output/lint_report.html",
    "test_coverage": "output/coverage.json"
  }
}
```

### Example 2: Multi-Skill Workflow with Corrections

**Workflow**: Plan → Build → Test (with error recovery)

```python
# .claude/workflows/plan_build_test.py
async def plan_build_test_workflow(request: str):
    session = Session.new()
    
    # Phase 1: Planning
    plan = await run_phase(
        session=session,
        phase_name="planning",
        skill="planner",
        input=request,
        contract=PlanOutput,
        gates=["json_parses", "spec_valid", "criteria_testable"]
    )
    if plan.status == "fail":
        return session.fail(plan)
    
    # Phase 2: Building
    build = await run_phase(
        session=session,
        phase_name="building",
        skill="builder",
        input=plan.notes_for_next_agent,
        contract=BuildOutput,
        gates=["json_parses", "files_changed", "git_valid"],
        retry_on_fail=True,  # ← KEY: correct in same session
        max_corrections=2
    )
    if build.status == "fail":
        return session.fail(build)
    
    # Phase 3: Testing
    test = await run_phase(
        session=session,
        phase_name="testing",
        skill="tester",
        input=build.notes_for_next_agent,
        contract=TestOutput,
        gates=["json_parses", "tests_run", "coverage_threshold"],
        loop_on_fail_to=None  # don't retry tester, fail instead
    )
    
    return session.succeed({
        "plan": plan,
        "build": build,
        "test": test
    })

async def run_phase(session, phase_name, skill, input, contract, gates, retry_on_fail=False, max_corrections=1):
    """Run a phase, validating output against gates."""
    
    phase = session.create_phase(phase_name, skill)
    
    for attempt in range(max_corrections + 1):
        # Run skill
        output_json = await skill_runner.execute(skill, input)
        
        try:
            envelope = contract(**json.loads(output_json))
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt < max_corrections:
                input = f"{output_json}\n\nERROR: {e}\n\nPlease correct."
                continue
            return create_failed_envelope(f"Invalid output after {max_corrections} attempts")
        
        # Run gates
        gate_results = validate_gates(envelope, gates)
        phase.record_gates(gate_results)
        
        if all(gate_results.values()):
            return envelope  # success!
        
        if not retry_on_fail or attempt == max_corrections - 1:
            return envelope  # return with failed gates
        
        # Prepare correction prompt
        failures = {k: v for k, v in gate_results.items() if not v}
        input = build_correction_prompt(output_json, failures)
    
    return create_failed_envelope("Max correction attempts exceeded")
```

---

## Part 10: Risks and Mitigations

### Risk 1: Envelope Drift
**Problem**: System and implementation envelope definitions diverge.  
**Mitigation**:
- Single source of truth: Pydantic model in type library
- Generate prompts from model via introspection
- Grep strategy: "find all TypeCheckingError patterns and fix"

### Risk 2: Gate False Positives
**Problem**: Gates reject valid output due to buggy gate logic.  
**Mitigation**:
- Test gates independently with unit tests
- Log all gate inputs/outputs in trace
- Use logs to debug failing gates

### Risk 3: Prompt Entropy
**Problem**: Different agents get different prompts for same task.  
**Mitigation**:
- Version all prompts in git
- Use role-specific templates, not per-instance prompts
- Audit prompt changes via git history

### Risk 4: Correction Loops That Never Converge
**Problem**: Agent keeps failing the same gate.  
**Mitigation**:
- Set `max_corrections` limit (default: 2)
- Escalate to human if corrections exhausted
- Log repeated failures for prompt refinement

---

## Part 11: Summary & Quick Start

### Adopt in This Order

1. **Create envelope types** (1 hour)
   - Define `SkillOutput` base class
   - Derive 3-5 specialized types
   - Commit to type library

2. **Wire gates into skills** (2 hours)
   - Pick one skill, add 2-3 gates
   - Test gate behavior
   - Extend to next skill

3. **Separate prompts** (1 hour)
   - Move 1-2 skill prompts to `.claude/prompts/{skill}/system.md`
   - Reference from skill config
   - Repeat for high-traffic skills

4. **Build trace database** (2 hours)
   - Create 5-table SQLite schema (sessions, phases, events, envelopes, gates)
   - Log all skill execution
   - Write 3-4 query templates

5. **Implement correction flow** (2 hours)
   - When gates fail, re-prompt same agent
   - Track correction counts
   - Test with intentionally broken prompt

6. **Create workflow examples** (3 hours)
   - Implement 2 workflows (Plan → Build, Code Review → Fix)
   - Use explicit flow definitions
   - Document for team

**Total: ~11 hours to adopt core patterns**

### Resources

- **SSSF Repo**: https://github.com/disler/super-simple-software-factory — 40-180 line workflows, SQLite trace, gate system
- **Hooks Mastery**: https://github.com/disler/claude-code-hooks-mastery — hook patterns and sub-agent orchestration
- **Observability**: https://github.com/disler/claude-code-hooks-multi-agent-observability — multi-agent tracing and live dashboard
- **Pi vs Claude Code**: https://github.com/disler/pi-vs-claude-code — multi-agent coordination patterns

### Key Takeaway

**Disler's core insight**: "Code owns sequencing, agents own bounded work." This separation enables:
- Observable execution (queryable trace)
- Reusable workflows (copy and modify)
- Reliable error recovery (corrections in same session)
- Clear agent responsibilities (each agent knows its role)

Adopting this pattern transforms 105 independent skills into a cohesive orchestrated system where each skill is a node in explicit, testable workflows.

---

**End of Research Document**
