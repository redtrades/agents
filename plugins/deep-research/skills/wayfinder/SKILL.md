---
name: wayfinder
description: Plan a huge chunk of work  -  more than one agent session can hold  -  as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear. disable-model-invocation: true Use when breaking down large architectural multi-session initiatives into roadmap maps.
---

# Wayfinder

## Overview

A loose idea has arrived  -  too big for one agent session, and wrapped in fog: the way from here to the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the destination. This skill charts the way as a **shared map** on the repo's issue tracker, then works its **decision tickets**  -  questions whose resolution is a decision, not slices of a build to execute  -  one at a time until the route is clear.

The destination varies per effort, and naming it is the first act of charting  -  it shapes every ticket. It might be a spec to hand off and iterate on, a decision to lock before planning starts, or a change made in place like a data-structure migration. The map is domain-agnostic  -  engineering work, course content, whatever fits the shape.
## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the way is clear  -  nothing left to decide before someone goes and does the thing. The pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off. An effort can override this in its **Notes**  -  carrying execution into the map itself  -  but absent that, produce decisions, not deliverables.
## Refer by name

Every map and ticket is an issue, so it has a **name**  -  its title. In everything the human reads  -  narration, the map's Decisions-so-far  -  refer to it by that name, never by a bare id, number, or slug. A wall of `#42, #43, #44` is illegible; names read at a glance. The id and URL don't vanish  -  a name wraps its link  -  but they ride _inside_ the name, never stand in for it.
## The Map

The map is a single issue on this repo's issue tracker, labelled `wayfinder:map`  -  the canonical artifact. Its tickets are child issues of the map.

The map is an **index**, not a store. It lists the decisions made and points at the tickets that hold their detail; a decision lives in exactly one place  -  its ticket  -  so the map never restates it, only gists it and links.

**Where the map, its child tickets, blocking, and frontier queries physically live is tracker-specific.** The issue tracker should have been provided to you  -  run `/setup-matt-pocock-skills` if not. Consult the tracker doc's "Wayfinding operations" section for how _this_ repo expresses them. If no tracker has been provided, default to the local-markdown tracker.

### The map body

The whole map at low resolution, loaded once per session. Open tickets are **not** listed  -  they are open child issues, found by query.

```markdown## Destination

<what reaching the end of this map looks like  -  the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>
## Notes

<domain; skills every session should consult; standing preferences for this effort>
## Decisions so far

<!-- the index  -  one line per closed ticket: enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link)  -  <one-line gist of the answer>
## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->
## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduates -->
```

### Tickets

Each ticket is a **child issue** of the map; the tracker's issue id is its identity. Its body is the question, sized to one 100K token agent session:

```markdown## Question

<the decision or investigation this ticket resolves>
```

Each ticket carries a `wayfinder:<type>` label  -  one of `research`, `prototype`, `grilling`, `task` (see [Ticket Types](#ticket-types)).

A session **claims** a ticket by assigning it to the dev driving the map, **first**, before any work, so concurrent sessions skip it. That assignee _is_ the claim: an open, unassigned ticket is unclaimed.

Blocking uses the tracker's **native** dependency relationship  -  essential because it renders the frontier _visually_ in the tracker's own UI, so the human sees what's takeable without opening the map. Only a tracker that lacks native blocking falls back to a body convention. A ticket is **unblocked** when every ticket blocking it is closed; the **frontier** is the open, unblocked, unclaimed children  -  the edge of the known.

The answer isn't part of the body  -  it's recorded on resolution (see [Work through the map](#work-through-the-map)). Assets created while resolving a ticket are linked from the issue, not pasted in.
## Ticket Types

Every ticket is either **HITL**  -  human in the loop, worked _with_ a human who speaks for themselves  -  or **AFK**, driven by the agent alone. A HITL ticket only resolves through that live exchange; the agent never stands in for the human's side of it (a grilling agent that answers its own questions has broken this).

- **Research** (AFK): Reading documentation, third-party APIs, or local resources like knowledge bases to surface a fact a decision waits on. Resolved by a `/research` **subagent**. Use when knowledge outside the current working directory is required.
- **Prototype** (HITL): Raise the fidelity of the discussion by making a cheap, rough, concrete artifact to react to  -  an outline, a rough take, a stub, or UI/logic code via the /prototype skill. Links the prototype as an asset. Use when "how should it look" or "how should it behave" is the key question.
- **Grilling** (HITL): Conversation. The default case. Always invoke the /grilling and /domain-modeling skills.
- **Task** (HITL or AFK): Manual work that must happen before a _decision_ can be made  -  nothing to decide, prototype, or research, but the discussion is blocked until it's done. Signing up for a service so its API can be judged, provisioning access, moving data so its shape can be seen. This is the one type that _does_ rather than decides  -  and it earns its place by unblocking a decision, not by delivering the destination. The agent drives it alone where it can (AFK); otherwise it hands the human a precise checklist (HITL). Resolved when the work is done; the answer records what was done and any resulting facts (credentials location, new URLs, row counts) later tickets depend on.

## Extended Reference & Deep Mechanics

For complete implementations, edge cases, and detailed recipes, see [references/details.md](references/details.md).
