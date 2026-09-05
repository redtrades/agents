# Emerging Patterns in Agent Systems (2026)
## Research Report: Architecture & Design Patterns for Phase 1+

**Research Date:** September 2026  
**Focus:** Production-grade patterns from Karpathy, Gary Tan, and top GitHub repos  
**Audience:** Phase 1+ system design and tier system architecture

---

## Executive Summary

The 2026 agent landscape has matured from "the year of agents" to "the decade of agents." Key patterns have solidified:

- **Agentic discipline over vibe coding** — structured specs, diff review, eval loops (Karpathy)
- **Human-in-the-loop as standard safety pattern** — 95.5% of orgs implement approval checkpoints after incidents
- **Memory as first-class infrastructure** — context window is the program; memory is the persistent substrate
- **Model tiering proven production pattern** — cheap fast models for routing, capable models for reasoning
- **Skills ≠ Tools** — skills include procedure, constraints, canonical code; routing is the bottleneck
- **Orchestration over choreography** — explicit state machines win over conversational drift
- **Evidence trails required for trust** — execution provenance, not input-output pairs, for audit & governance

---

## Part 1: Karpathy's Framework for Agentic Systems

### A. The Shift: From Coding to Prompting
**Key Insight:** "The context window is now the program, and the LLM is the interpreter."

Karpathy's latest position at Anthropic (joined May 2026) emphasizes a fundamental shift:
- You no longer program in Python—you program in English
- Prompt files, specs, and knowledge bases matter more than syntax
- This reframes agent design: **specs and diffs replace traditional code review**

### B. Agentic Engineering vs. Vibe Coding
Karpathy's 5 predictions on agentic engineering (Sequoia Ascent 2026):

1. **Discipline is non-negotiable** — design specs before prompting, review diffs, build eval loops
2. **Directed agents, not autonomous chaos** — engineer agents like you engineer any system
3. **December 2025 was an inflection point** — models now good enough that "I can't remember the last time I corrected a model"
4. **The decade, not the year** — critical infrastructure still missing:
   - No strong memory systems
   - No reliable multi-modal perception
   - Minimal continual learning
   - Limited computer use and environmental interaction
5. **AGI still 10-15 years away** — agents are a necessary step, not the destination

### C. Memory Architecture Implications
The survey "Agent Memory in the Second Half" identifies five cognitive memory types agents need:
- **Sensory**: Immediate perception (current task input, recent context)
- **Working**: Intermediate reasoning (current step's state, intermediate results)
- **Episodic**: What happened (task history, execution traces, outcomes)
- **Semantic**: What is true (facts, relationships, skill knowledge)
- **Procedural**: How to do it (skill procedures, tool usage patterns)

**Key Innovation:** Memory is becoming *learnable* — agents can optimize which experiences to retain short-term and which to consolidate long-term.

---

## Part 2: Gary Tan's Agent Coordination Framework

### A. gstack Project (Launched March 12, 2026)
**Claim:** 600,000 lines of production code in 60 days (10,000–20,000 usable lines per day, part-time)

**Key Architecture:**
- Role specialization via "skill files as employees"
- Resolver tables as organizational structure
- Curated "company brain" as institutional memory
- **Human-orchestrated**, not autonomous multi-agent coordination

**Important Distinction:** gstack is NOT autonomous multi-agent handoff. It requires humans to route between agents. For autonomous delegation (research agent → synthesis agent), you need LangGraph or CrewAI.

### B. Y Combinator Batch Results (Winter 2025)
- **25% of YC companies** had 95% AI-generated codebases
- **Productivity multiplier claimed:** 400x by treating AI as full workforce
- **Fastest-growing and most profitable batch** in YC history

**Insight for Your Tier System:** YC companies are successfully segmenting roles by capability tier, not just ability level.

### C. Agent Coordination Patterns (YC Thesis)
Gary Tan emphasizes:
- **Skill files as reusable, transferable units** — fits your "skills" abstraction
- **Org-chart thinking for agent teams** — hierarchy reduces cognitive load on routing
- **Shared institutional memory** — not scattered per-agent stores
- **Explicit handoff protocols** — vs. letting agents figure it out

---

## Part 3: GitHub Agent Framework Analysis (2026 Landscape)

### Production Framework Landscape

#### 1. **LangGraph** (LangChain)
- **Best for:** Explicit control, state machines, complex control flow
- **Steepest learning curve** but maximum transparency
- **Memory:** Customizable short-term (state) + long-term (external storage)
- **Storage:** SQLite/PostgreSQL with LangGraph schema
- **Production pattern:** Most common for orchestration layer in 2026

**Memory Strategy:** State lives in the graph; external retrieval via tool calls.

#### 2. **CrewAI**
- **Best for:** Structured, deterministic, auditable workflows with clear roles
- **Coordination:** Hierarchical (Orchestrator → Workers → Results consolidation)
- **Agents:** Have explicit role, tools, responsibilities; deterministic handoff
- **Memory:** Built-in memory types at `./.crewai/memory` (LanceDB)
- **Output:** Highly structured, testable pipelines

**Weakness:** Doesn't handle autonomous inter-agent routing; humans decide handoff.

#### 3. **AutoGen** (Microsoft)
- **Best for:** Iterative reasoning, code execution, agent-to-agent review
- **Coordination:** Conversational (agents talk, collaborate dynamically)
- **Flexibility:** High, but at cost of growing complexity and edge cases
- **Memory:** Conversation history + ChromaDB external store
- **Challenge:** 60% failure cases come from context/data quality, not model limits

**Key Issue:** AutoGen and LangGraph memory systems don't interoperate. User preferences in AutoGen session invisible to LangGraph orchestrator.

#### 4. **LlamaIndex**
- **Best for:** RAG (retrieval-augmented generation), data ingestion, retrieval routing
- **Agents:** Secondary concern; primary is retrieval infrastructure
- **Production pattern:** LlamaIndex for RAG + LangGraph for orchestration
- **Routing:** Domain-based index routing; recommended when indexes exceed 100M chunks
- **Memory:** Separate indices per domain + routing layer

**Emerging pattern:** Index router is a bottleneck; multi-domain systems need separate indices.

#### 5. **Pydantic AI**
- **Best for:** Type-safe, conventional agents; FastAPI-style developer experience
- **Model-agnostic:** Works with Claude, GPT, others
- **Typing:** Explicit contracts on inputs, tools, outputs
- **Scale:** Not a multi-agent framework; single agent with strong typing
- **Team fit:** Best if your team values explicit contracts and type safety

**18.3K stars (2026), growing.** Strong for well-defined, bounded agent tasks.

#### 6. **Anthropic Agent SDK**
- **Released:** April 2026 (alongside Claude 4.6)
- **First-class primitive:** Computer use as part of core agent design
- **Stars:** 3.4K–6.9K (low star count, high relevance-per-install for Anthropic API users)
- **Positioning:** Competing with OpenAI Agents SDK (March 2026) and Google ADK (April 2026)

**Significance:** 2026 is the year of the "agent harness" — infrastructure to wrap models for long-running tasks.

### Framework Comparison Matrix

| Dimension | LangGraph | CrewAI | AutoGen | LlamaIndex | Pydantic AI |
|-----------|-----------|--------|---------|-----------|------------|
| **Control** | Maximum | High | Medium | Medium | High |
| **Memory** | Flexible | Built-in | Conversational | Index-based | Simple |
| **Routing** | Explicit | Hierarchical | Conversational | Index-based | N/A (single) |
| **Multi-agent** | Yes, complex | Yes, structured | Yes, dynamic | Secondary | No |
| **Interop** | Weak with CrewAI/AutoGen | Weak with LangGraph | Weak with LangGraph | Works with others | Works with others |
| **Production scale** | High | Medium | Medium | High | Growing |

---

## Part 4: Emerging Production Patterns (2026)

### A. The Model Tiering Pattern (Proven in Production)

**Pattern:** Use small, fast, cheap models for routing and triage; capable models for reasoning.

```
User Input
    ↓
[Haiku/Mini] - Router/Triage (classify task, select agent path)
    ↓ (if simple task)
[Haiku/Mini] - Execute (handle straightforward work)
    ↓ (if complex task)
[Sonnet/GPT-4] - Reasoning (complex multi-step reasoning, code generation)
    ↓ (if very complex)
[Opus/GPT-4-turbo] - Complex reasoning (scientific, novel problems)
```

**Cost Impact:** 90% of requests answer at tier-1 (Haiku); 9% escalate to Sonnet; <1% need Opus.

**Routing Confidence:** Request routes locally if confidence > dynamic threshold; otherwise escalate.

### B. Context Management: The Tiered Memory Approach

**Short-term Memory:** Extended context windows + strategic prompting
- What: Current task state, recent messages, active reasoning
- Storage: Stays in prompt/context window
- TTL: Single interaction or short session

**Long-term Memory:** Persistent retrieval-augmented stores
- What: Task history, learned patterns, user preferences, skill knowledge
- Storage: Knowledge graphs (best for agents), vector stores, key-value stores
- Retrieval: Via tool calls or prompt injection before agent runs

**Critical Finding:** Long-term memory is "the biggest unlock, but the biggest challenge." Knowledge graphs preferred for deterministic, traceable agent RAG.

### C. Skill Routing (Not Just Tool Routing)

**Distinction:** A *skill* is not a *tool*.
- **Tool:** Atomic "input → call → output" function
- **Skill:** Complete procedure, including constraints, canonical code, edge cases, call sequences

**2026 Pattern:** Skills router retrieves right skill from pool based on task.

**Key Frameworks:**
- **SkillRouter:** Uses retriever + reranker on full skill content (not just names/descriptions)
- **SkillOrchestra:** Learns missing capabilities by comparing success/failure trajectories
- **AgentSkillOS:** Organizes skills as capability tree; caches successful orchestration plans

**Finding:** Skill names are poor routing signals; full skill context matters.

### D. Execution Observability & Evidence Trails

**Standard Practice in 2026:** Capture full execution provenance, not just input-output.

**What to track:**
- Model calls (LLM inputs, outputs, reasoning)
- Tool invocations (what called, with what args, what returned)
- Memory operations (what retrieved, what stored)
- State transitions (workflow steps, decisions, branches)
- Handoffs (agent-to-agent, human-in-the-loop gates)
- Errors (transient vs. permanent, recovery attempts)
- Latency, cost, outcome

**For Audit & Governance:** Regulated industries (finance, healthcare) require evidence of policy-compliant behavior, not just task completion.

### E. Human-in-the-Loop as Standard Safety Pattern

**Adoption:** 95.5% of organizations took action to mitigate agent risks after incident; human-in-the-loop most common response.

**Two patterns:**
- **Human-in-the-loop (HITL):** Approve before action executes (slow, for high stakes)
- **Human-on-the-loop (HOOTL):** Action executes; human can intervene during/after

**Key principle:** Gate should live in workflow (structural), not negotiated in prompt.

**Use cases for approval:**
- Sending emails, making API calls
- Financial transactions, data deletion
- High-risk actions (changing configs, escalating privileges)

### F. Failure Recovery Patterns

**Retry strategies:**
- **Fixed retry:** Try, wait fixed time, retry up to N times (low-stakes, infrequent failures)
- **Exponential backoff:** Progressive wait times (1s, 2s, 4s, 8s) to let services recover
- **Circuit breaker:** Three states (Closed → Open → Half-Open) to prevent retry storms
- **Jitter:** Add randomness to prevent synchronized retry storms across agents

**Agent-specific challenge:** Context loss on restart. Solutions:
- Checkpoint state before retry
- Resume from last good checkpoint
- Replay learned preferences

### G. Autonomous vs. Constrained: Autonomy Levels

**Five-level framework (2026 consensus):**
- **L1 (Operator):** Human directs every step
- **L2 (Collaborator):** Agent proposes, human confirms
- **L3 (Consultant):** Agent acts, human can override
- **L4 (Approver):** Agent acts, human audits
- **L5 (Observer):** Agent plans & executes autonomously; humans only if blocked

**Key insight:** Autonomy should not be static—constrain by trust model and market costs, not just capability.

**Reality check:** People make ~70% of planning decisions; Claude does ~80% of execution. Autonomy is task-dependent.

---

## Part 5: What's Becoming Standard Practice in 2026

### Production Readiness Gap
- **78% of enterprises** have AI agent pilots
- **<15% in production scale** — significant experimentation-to-deployment gap
- **60% of production failures** are data/context/governance, not model limits

### Architecture Consensus

**Single Agent vs. Multi-Agent:**
- Single agent with strong prompting often equals multi-agent system performance
- But: Multi-agent excels for diverse perspectives and role-based work
- Research shows both can work; the difference is engineering discipline

**Orchestration Pattern:**
- Explicit state machines win over conversational drift
- Lead Agent (designated coordinator) is most common for multi-agent
- Hierarchical patterns (supervisor + workers) dominate production deployments

**Memory as Infrastructure:**
- Context window is the program
- Memory substrate is non-negotiable for long-horizon tasks
- Separate indices for domains (>100M chunks per index = latency hit)

**Evaluation Frameworks:**
- Dual-track: Does it complete? Does it follow correct reasoning path?
- 7 dimensions → 25 sub-dimensions → 130-item rubric for production evaluation
- τ-bench, WebArena, SWE-bench Verified are emerging standards

---

## Part 6: Prompt-Based vs. Code-Based Agents

### The Distinction

**Prompt-based (CrewAI, higher-level frameworks):**
- Define agents via YAML/config with role, goals, constraints
- Framework handles orchestration, message passing, memory
- Easier to modify behavior (edit config/prompt)
- Less control over internal decision-making

**Code-based (LangGraph, Anthropic SDK, lower-level frameworks):**
- Define agents via Python with explicit step functions, state machines
- You control every transition, every decision point
- Harder to modify (code changes)
- Maximum transparency and control

### When Each Wins

**Use CrewAI/prompt-based when:**
- Workflow roles are well-defined and stable
- You need deterministic, auditable pipelines
- Team is non-technical or prefers config over code
- SLAs and handoff contracts are explicit

**Use LangGraph/code-based when:**
- Complex control flow, loops, branching
- You need fine-grained state management
- Workflow is still evolving and you need flexibility
- Production requirements demand maximum observability

### Critical Finding: Framework Matters Less Than Prompts

**80/20 rule:** Spend 80% of your time on prompt engineering and task descriptions; 20% on framework selection.

The difference between a working and broken system is almost always:
- Quality of agent instructions
- Precision of tool definitions
- Clarity of task decomposition
- NOT which framework you chose

---

## Part 7: Recommendations for Your Setup

### For Phase 1 (MVP)

1. **Start with LangGraph + LlamaIndex**
   - LangGraph for orchestration (explicit state, debugging)
   - LlamaIndex for retrieval (battle-tested RAG)
   - Both are production-grade and well-documented

2. **Implement model tiering immediately**
   - Haiku for routing/triage (0.8-3B params, <$0.50/M tokens)
   - Sonnet for core reasoning (20B equiv, $3/M tokens)
   - Reserve Opus for <1% of tasks (complex novel problems)

3. **Build skill registry as first-class infrastructure**
   - Each skill includes: procedure, constraints, canonical code, edge cases, success/failure criteria
   - Implement SkillRouter pattern (retriever + reranker on full skill content)
   - Cache successful orchestration plans

4. **Implement approval gates for irreversible actions**
   - Email sending, data deletion, financial transactions
   - Make gates structural (workflow-enforced), not prompt-negotiated
   - Log all approvals for audit trail

5. **Adopt evidence-trail observability from day one**
   - Capture execution provenance, not just input-output
   - Include: model calls, tool use, memory ops, state transitions, errors
   - Use structured logging so traces are machine-readable

### For Phase 1.5 (Scaling)

6. **Implement shared memory substrate**
   - Separate indices by domain (knowledge graph preferred for agents)
   - Domain router selects index based on task semantic matching
   - Cache retrieval results to avoid re-reading same docs

7. **Adopt evaluation rubric discipline**
   - Measure both task completion AND reasoning correctness
   - Build eval loops before going to production (not after)
   - Use both lab benchmarks and production failure analysis

8. **Design autonomy levels explicitly**
   - Start agents at L2–L3 (collaborator/consultant)
   - Escalate to L4–L5 only for low-risk tasks or with perfect track record
   - Use task-dependent constraints, not single L-rating per agent

### What NOT to Do

**Avoid:**
- Building your own multi-agent coordination from scratch (use LangGraph)
- Mixing AutoGen and LangGraph memory (they don't interop; pick one)
- Relying on conversational drift for production workflows (use state machines)
- Skipping approval gates on high-risk actions (95.5% of orgs regretted this)
- Treating memory as an afterthought (it's infrastructure, not feature)

---

## Part 8: Clarifying Questions for Mike

### On Architecture & Tier System

1. **Skill routing vs. simple function routing?** Your tier system suggests skills (with procedures & constraints), not atomic tools. Should the Phase 1 router assume each tier-bound agent has a skill registry? Or should routing be at the task level, with skills as internal detail?

2. **Autonomy model for your tiers?** Each tier appears to map to a capability level (Haiku → L2 routing, Sonnet → L3 reasoning). Should tiers also map to autonomy levels (what each tier is allowed to decide without human gate)? Or is autonomy per-skill?

3. **Cross-tier memory sharing?** If Haiku routes to Sonnet, should Sonnet see Haiku's reasoning? Should both see shared long-term memory (user preferences, learned patterns)? Or is memory per-tier?

### On Memory & Context

4. **Second brain architecture?** You mentioned this in requirements. Is this:
   - A shared knowledge graph across all agents?
   - Tiered (fast local memory for current task, slow global memory for learned patterns)?
   - Indexed by domain or by agent capability level?

5. **Context window as the program?** Karpathy's framing suggests specs live in prompt context. For your tier system, should each tier have a fixed context budget? Should Haiku get less context than Sonnet by design?

### On Coordination & Handoff

6. **Autonomous vs. human-orchestrated handoff?** Your setup resembles gstack (human-orchestrated) but could evolve to autonomous. Should Phase 1 assume humans route between tiers? Should Phase 1.5 add autonomous routing (e.g., Haiku decides to escalate)?

7. **Skill vs. tool routing?** Should routing decisions consider the full skill procedure (constraints, edge cases) or just the skill description/name? SkillRouter suggests full-content routing is worth the retrieval cost.

### On Observability & Governance

8. **Evidence trail scope for your tiers?** Should execution traces differ by tier (e.g., Haiku gets lightweight traces, Sonnet gets full provenance)? Or uniform trace format across all tiers for aggregation?

---

## References & Sources

### Karpathy & Frontier AI
- [Karpathy's Sequoia Talk: 5 Predictions About Agentic Engineering](https://www.mindstudio.ai/blog/karpathy-sequoia-talk-5-predictions-agentic-engineering)
- [The Decade of AI Agents: Karpathy on AGI Timeline](https://www.flowhunt.io/blog/the-decade-of-ai-agents-andrej-karpathy-agi-timeline/)
- [Andrej Karpathy's AI Engineering Playbook (2026)](https://www.aibuilderclub.com/blog/karpathy-ai-engineering-playbook)

### Agent Memory & Cognitive Science
- [A Survey of Agent Memory in the Second Half](https://arxiv.org/abs/2602.06052)
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
- [Always-On Agents: A Survey of Persistent Memory, State, and Governance](https://arxiv.org/pdf/2606.30306)
- [Beyond RAG for Agent Memory: Retrieval by Decoupling and Aggregation](https://arxiv.org/pdf/2602.02007)

### Gary Tan & YC Coordination
- [Garry Tan's gstack and the Rise of AI Agent Teams](https://agentscodex.com/posts/2026-03-20-garry-tan-gstack-agent-teams-claude-code/)
- [Garry Tan Showcases AI Agent Frameworks](https://www.startuphub.ai/ai-news/artificial-intelligence/2026/garry-tan-showcases-ai-agent-frameworks)

### Framework Analysis & Comparisons
- [CrewAI vs LangGraph vs AutoGen: Choosing the Right Multi-Agent Framework](https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen)
- [AI Agent Memory: Comparative Analysis of LangGraph, CrewAI, and AutoGen](https://dev.to/foxgem/ai-agent-memory-a-comparative-analysis-of-langgraph-crewai-and-autogen-31dp)
- [First-hand Comparison of LangGraph, CrewAI and AutoGen](https://aaronyuqi.medium.com/first-hand-comparison-of-langgraph-crewai-and-autogen-30026e60b563)
- [What is LlamaIndex? RAG and Agents Framework in 2026](https://futureagi.com/blog/what-is-llamaindex-2026)
- [LangChain vs LlamaIndex 2026: Complete Framework Guide](https://itsourcecode.com/ai-framework/langchain-vs-llamaindex-2026-complete-guide/)
- [AI Agent Frameworks (2026 Update): 8 SDKs Compared](https://www.morphllm.com/ai-agent-framework)

### Agentic Workflows & Patterns
- [Agentic Workflows in 2026: The Ultimate Guide](https://www.vellum.ai/blog/agentic-workflows-emerging-architectures-and-design-patterns)
- [Agentic Workflows for 2026 — Supermemory](https://supermemory.ai/blog/agentic-workflows-vp-engineering-guide)
- [Agentic Workflow Architectures: 2026 Guide](https://www.stackai.com/blog/the-2026-guide-to-agentic-workflow-architectures)
- [Agentic AI Workflows in Production: Patterns, Pitfalls, and Best Practices](https://devstarsj.github.io/2026/06/23/agentic-ai-workflows-production-patterns-2026/)
- [Top AI Agentic Workflow Patterns That Will Lead in 2026](https://ai.plainenglish.io/top-ai-agentic-workflow-patterns-that-will-lead-in-2026-2468bf088dc6)

### Skill Routing & Tool Selection
- [SkillRouter: Skill Routing for LLM Agents at Scale](https://arxiv.org/pdf/2603.22455)
- [Skill Is Not Document: Query-Conditional Benchmark and Two-Stage Retriever](https://arxiv.org/pdf/2606.03565)
- [Agent Skill Evaluation and Evolution: Frameworks and Benchmarks](https://arxiv.org/html/2606.11435v1)
- [Latency-Quality Routing for Functionally Equivalent Tools in LLM Agents](https://arxiv.org/pdf/2605.14241)

### Observability & Execution Provenance
- [Agent Observability: The Complete Guide for 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance](https://arxiv.org/html/2606.04990v1)
- [What Is Agent Observability? A 2026 Developer Guide](https://mlflow.org/articles/what-is-agent-observability-a-2026-developer-guide/)
- [AI Agent Observability: A Complete Guide for 2026 & Beyond](https://atlan.com/know/ai-agent-observability/)

### Multi-Agent Routing & Tiering
- [Self-Resource Allocation in Multi-Agent LLM Systems](https://arxiv.org/pdf/2504.02051)
- [Tiered Agentic Oversight: Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482)
- [Orchestrating Intelligence: Confidence-Aware Routing for Multi-Agent Collaboration](https://arxiv.org/pdf/2601.04861)
- [Beyond Individual Intelligence: Surveying Collaboration and Failure Attribution](https://arxiv.org/pdf/2605.14892)

### Failure Recovery & Reliability
- [Multi-Agent System Reliability: Failure Patterns and Production Validation](https://www.getmaxim.ai/articles/multi-agent-system-reliability-failure-patterns-root-causes-and-production-validation-strategies/)
- [Multi-Agent AI Systems: Why They Fail and How to Fix Coordination Issues](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them)
- [AI Agent Retry Patterns - Exponential Backoff Guide 2026](https://fast.io/resources/ai-agent-retry-patterns/)

### Autonomy & Human-in-the-Loop
- [Levels of Autonomy for AI Agents](https://arxiv.org/pdf/2506.12469)
- [Autonomy and Agency in Agentic AI: Architectural Tactics for Regulated Contexts](https://arxiv.org/pdf/2605.12105)
- [Intelligent AI Delegation](https://arxiv.org/html/2602.11865v1)
- [AI Agent Autonomy Levels: How Much Freedom Is Too Much?](https://apptitude.io/blog/ai-agent-autonomy-levels-decision-framework/)
- [Human-in-the-Loop AI: When (and Why) Machines Still Need a Person](https://www.avepoint.com/blog/strategy-blog/human-in-the-loop-ai)
- [Human-in-the-Loop AI Agents: The 2026 Guide](https://pickaxe.co/post/human-in-the-loop-ai-agents)
- [Human-in-the-Loop AI Agents: How to Add Approvals, Escalation, and Safe Autonomy](https://medium.com/@arvisionlab/human-in-the-loop-ai-agents-how-to-add-approvals-escalation-and-safe-autonomy-in-production-0a21e359781c)

### Evaluation & Production Readiness
- [AI Agent Benchmarks: The 2026 Enterprise Evaluation Guide](https://www.automationanywhere.com/company/blog/ai-agent-benchmarks)
- [How to Build an Agent Evaluation Framework with Metrics, Rubrics, and Benchmarks](https://galileo.ai/blog/agent-evaluation-framework-metrics-rubrics-benchmarks)
- [AI Agent Evaluation: Frameworks and Metrics Beyond the Benchmarks](https://www.algolia.com/blog/ai/ai-agent-evaluation-frameworks-metrics-testing-strategies)
- [AI Agent Evaluation (2026): Metrics, Frameworks, and Production Failures](https://www.morphllm.com/ai-agent-evaluation)
- [AlphaEval: Evaluating Agents in Production](https://arxiv.org/pdf/2604.12162)

### GitHub Frameworks & Ecosystem
- [Top 15 AI Agent Frameworks in 2026](https://pickaxe.co/post/top-ai-agent-frameworks)
- [Awesome AI Agents for 2026](https://github.com/ARUNAGIRINATHAN-K/awesome-ai-agents-2026)
- [Awesome AI Agents 2026: 300+ Resources](https://github.com/caramaschiHG/awesome-ai-agents-2026)
- [AI Agent Framework GitHub Rankings May 2026](https://presenc.ai/research/ai-agent-framework-github-rankings-2026)
- [Top 10 Most Starred AI Agent Frameworks on GitHub 2026](https://dev.to/ialijr/top-10-most-starred-ai-agent-frameworks-on-github-2026-3d4o)

---

## Next Steps

1. **Clarify autonomy & tier mapping** with Mike (Questions 1–3)
2. **Spec memory substrate** based on feedback (Question 4)
3. **Proto Phase 1 stack** using LangGraph + LlamaIndex
4. **Build eval framework** before first production push
5. **Design approval gates** for irreversible actions (Question 8)

---

**Report compiled:** September 4, 2026  
**Focus level:** Production-ready patterns, not theoretical deep dives  
**Next review:** After Phase 1 MVP launch  
