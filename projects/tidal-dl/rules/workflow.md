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

```
 1. ARCHITECT (Opus + thinking)
    confirm -> invoke -> present plan -> wait for user approval
                          │
 2. DEVELOPER + TESTER (Sonnet, parallel)
    confirm -> invoke both in same message -> integrate results
                          │
 3. UNIT TESTS
    .venv/bin/pytest tests/ -v --tb=short
    fix failures in main conversation before proceeding
                          │
 4. SMOKE TESTS (user-driven, when applicable)
    run relevant sections from docs/smoke-tests.md
    requires proxy-enabled profile — never run without proxy
    see "Smoke Testing" section below
                          │
 5. DOCUMENTATOR (Sonnet)
    confirm -> invoke -> integrate result
                          │
 6. COMMIT / MERGE / PUSH
    always in main conversation, never inside an agent
                          │
 7. DOCS SYNC
    architecture-review.md -> architecture-review-done.md
    update CLAUDE.md test count; add sprint to docs/sprints.md
                          │
 8. MEMORY SYNC
    check MEMORY.md against CLAUDE.md, update if needed
```

**Batch approval option** (Major tier only):
> *"Running full sprint pipeline (architect -> dev+test -> documentator). Approve all steps, or step-by-step?"*

A single "approve all" cuts 3 interruptions per sprint.

---

## Smoke Testing

Smoke tests verify real behavior against live TIDAL/Qobuz APIs through a proxy. They are **user-driven** — never automated without explicit request.

### When to run

| Change type | Smoke test? |
|-------------|------------|
| Internal refactor, no behavior change | No |
| New CLI command or flag | Yes — test the new command |
| Download pipeline change | Yes — run a download through proxy |
| Auth/proxy/fingerprint change | Yes — full login + download cycle |
| Metadata/tagging change | Yes — verify tags on downloaded file |

### How to run

1. Main conversation proposes which smoke test sections to run (from `docs/smoke-tests.md`)
2. User confirms and provides proxy profile if needed
3. Execute with proxy-enabled profile: `tidal-dl dl --profile <proxy-profile> <url>`
4. Verify output (file exists, correct format, correct tags, etc.)
5. Report results in session notes

### Rules

- **NEVER run downloads without a proxy-enabled profile**
- Smoke tests are optional for Micro tier, recommended for Standard when user-facing, required for Major when download/auth behavior changes
- Reference: `docs/smoke-tests.md` (30 sections + Qobuz + wizard)

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

---

## Documentation Lifecycle

### Document types

| Type | Lifespan | Examples |
|------|----------|---------|
| **Living** | Permanent — updated continuously | architecture.md, user-guide.md, smoke-tests.md, reference.md |
| **Plan** | Until implemented, then archive | l1-plan.md, qobuz-integration-plan.md |
| **Record** | Permanent — append-only | sprints.md, architecture-review-done.md |
| **Spec** | Permanent — versioned | spec.md, config-matrix.md |
| **One-off** | Until absorbed into a Living doc, then archive | security-findings-*.md, capture guides |

### Rules

1. **Creation gate** — Before creating a new doc, ask: Can this go in an existing Living doc? If yes, add a section there instead.
2. **Plan archival** — During post-sprint bookkeeping, move completed Plan docs to `docs/archive/`. They served their purpose.
3. **One-off absorption** — One-off docs (findings, guides) should be absorbed into the relevant Living doc within 1-2 sprints, then archived.
4. **Periodic audit** — Every 5 sprints, scan `docs/` for staleness. Archive anything that hasn't been updated in 10+ sprints and isn't a Spec or Record.
5. **Active docs cap** — Target ~12 active files in `docs/` (not counting `docs/archive/`). If over 15, audit immediately.

### Target structure

```
docs/
├── architecture.md           # Living — full architecture
├── architecture-review.md    # Living — active findings + done history
├── config-matrix.md          # Spec — config reference
├── qobuz-setup.md            # Living — Qobuz setup guide
├── reference.md              # Living — CLI + API reference
├── security-findings-*.md    # One-off — absorbed then archived
├── smoke-tests.md            # Living — all smoke tests (TIDAL + Qobuz + wizard)
├── spec.md                   # Spec — original feature spec
├── sprints.md                # Record — sprint history
├── tidal-security-research.md # Living — security knowledge base
├── user-guide.md             # Living — end-user documentation
└── archive/                  # Completed plans, absorbed one-offs
    ├── l1-plan.md
    ├── pipeline-decomposition-plan.md
    └── ...
```
