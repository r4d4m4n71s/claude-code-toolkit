# Sprint Workflow & Agent Orchestration

> Loaded on demand when running sprints. Trigger: "start sprint N" or "plan sprint N".

---

## Tiered Pipeline

Choose the right process for the task scope:

| Tier | Scope | Steps | Approvals |
|------|-------|-------|-----------|
| **Micro** | 1-2 files, clear fix/change | Read -> edit -> test -> commit | 1 (commit) |
| **Standard** | 3-5 files, known pattern | Architect sketch (in-conversation) -> dev+test -> commit | 2 (plan + commit) |
| **Major** | 6+ files, design decisions, new subsystems | Full agent pipeline (below) | Batch or step-by-step |

**Auto-triage**: When the user describes a task, assess scope and suggest the appropriate tier before starting.

---

## Major Tier — Full Agent Pipeline

1. **architect** — confirm -> invoke -> present plan -> wait for user approval
2. **developer + tester** — confirm (both together) -> invoke in parallel
3. **run unit tests** — `.venv/bin/pytest tests/ -v --tb=short`; fix failures before proceeding
4. **documentator** — confirm -> invoke -> integrate result
5. **commit / merge / push** — always in main conversation, never inside an agent
6. **docs sync** — move resolved items from `architecture-review.md` -> `architecture-review-done.md`; update sprint plan; update CLAUDE.md test count; add sprint entry to `docs/sprints.md`
7. **memory sync** — check MEMORY.md against CLAUDE.md and update if needed

**Batch approval option** (Major tier only):
> *"Running full sprint pipeline (architect -> dev+test -> documentator). Approve all steps, or step-by-step?"*

A single "approve all" cuts 3 interruptions per sprint.

---

## Agent Confirmation Rule

Before invoking a Task agent, present a one-line notice and wait for approval:

*"Invoking [AGENT NAME] agent to [brief purpose]. Proceed?"*

A "yes" triggers the agent immediately. Never invoke agents silently.

---

## Agent Models

| Agent | Model | Thinking |
|-------|-------|----------|
| `architect` | opus | yes |
| `developer` | sonnet | no |
| `tester` | sonnet | no |
| `documentator` | sonnet | no |
| `Explore` | sonnet | no |
| `research` (general-purpose) | opus | yes |

---

## Agent Context Templates

| Agent | Pass in |
|-------|---------|
| `architect` | Sprint goal, affected module list from module map, constraints (no breaking changes etc.) |
| `developer` | Architect's approved plan + function signatures of files to change (full file content only if >50% of the file changes) |
| `tester` | Architect's approved plan + interfaces/contracts (not implementation) |
| `documentator` | Changed files list + session-notes update + module map changes + smoke test updates when new user-facing behaviour is added |

---

## When to Use Agents vs Direct Work

| Scope | Approach |
|-------|----------|
| 1-2 files, clear scope | Work directly in main conversation |
| 3+ files, or design decisions needed | Use agents (see pipeline above) |
| "Where is X implemented?" | `Explore` agent instead of grep + read loops |

All agents inherit CLAUDE.md rules.
All git operations follow the Permissions Model (commit/push/merge need approval).

---

## Error Handling

- User rejects architect's plan -> revise and re-invoke architect, or abandon the sprint
- Developer/tester agent fails or returns errors -> diagnose and fix in main conversation, then re-invoke
- Tests fail after developer agent -> fix in main conversation (not via agent re-invocation)

---

## Sprint Trigger Phrase

When the user says **"start sprint N"** or **"plan sprint N"**:
1. Assess scope -> suggest tier (Micro/Standard/Major)
2. If Major: offer batch approval
3. Execute pipeline per tier

---

## Post-Sprint Bookkeeping

Only 3 update points after each sprint:

| Update | When | What |
|--------|------|------|
| **session-notes.md** | After every major task | What changed, current state, next steps |
| **CLAUDE.md** | Only when critical rules, module map, or status changes | Test count + one-liner status |
| **docs/sprints.md** | After sprint merge | Sprint details (single source of truth for history) |

MEMORY.md: only update if a new gotcha/pitfall was discovered. Do not duplicate sprint status.
