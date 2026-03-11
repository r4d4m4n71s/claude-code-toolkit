# Development Lifecycle

> Complete reference for the Claude Code-assisted SDLC. This document describes the end-to-end
> process from session startup through coding, testing, documentation, and maintenance.
> Rules are enforced via `CLAUDE.md` (global + project) and on-demand rule files.

---

## 1. Session Startup

Every session begins with context loading — adaptive based on intent:

| Intent | Steps |
|--------|-------|
| **Continuing previous work** | session-notes → git status → targeted file reads |
| **New feature / sprint** | session-notes → git status → load workflow rules → run tests |
| **Bug fix** | session-notes → git status → run tests → read failing module |
| **Docs / config only** | session-notes → git status (skip test suite) |
| **Housekeeping** | MEMORY.md vs CLAUDE.md comparison (no tests needed) |

**Always read first:** `.claude/session-notes.md` and project `CLAUDE.md`.
If any step reveals a problem (failing tests, dirty state, stale notes), **report it before proceeding**.

---

## 2. Context Architecture

Configuration is split into always-loaded and on-demand files to minimize context window usage.

### Always loaded (~300 lines)

| File | Purpose |
|------|---------|
| `~/.claude/CLAUDE.md` | Global rules (permissions, code standards, session hygiene) |
| `<project>/.claude/CLAUDE.md` | Project rules (module map, conventions, status) |
| `MEMORY.md` | Persistent gotchas, environment notes, key decisions |

### Loaded on demand (trigger phrases)

| File | Trigger |
|------|---------|
| `rules/workflow.md` | "start sprint N", "plan sprint N" |
| `rules/architecture-review.md` | "run architecture review" |
| `rules/commit-conventions.md` | When making commits |
| `rules/security-research.md` | "run security research" |

### Session state

| File | Purpose | Update cadence |
|------|---------|---------------|
| `.claude/session-notes.md` | Rolling window of last 5 entries | After every major task |
| `docs/sprints.md` | Permanent sprint history | After sprint merge |

---

## 3. Permissions Model

### Auto-allowed (no confirmation)
- File operations: read, edit, create, delete
- Commands: test runs, linters, build tools, git status/diff/log
- Search: grep, glob, web search, semantic search

### Require explicit approval
- Git writes: `commit`, `merge`, `push`, `rebase`, `tag`, `branch -d`
- Destructive: `git reset --hard`, `rm -rf`, anything affecting shared state
- Agent invocation: switching to any Task agent

### Commit workflow
1. Show `git diff --staged` summary + proposed message
2. Ask: *"Shall I commit with this message?"*
3. Execute only after approval

### Push/merge workflow
1. State what will happen: *"push 2 commits to origin/main"*
2. Ask: *"Shall I proceed?"*
3. Execute only after approval

---

## 4. Tiered Development Pipeline

Every task is triaged into one of three tiers based on scope:

| Tier | Scope | Steps | Approvals |
|------|-------|-------|-----------|
| **Micro** | 1–2 files, clear fix | Read → edit → test → commit | 1 (commit) |
| **Standard** | 3–5 files, known pattern | Architect sketch → dev+test → commit | 2 (plan + commit) |
| **Major** | 6+ files, design decisions | Full agent pipeline | Batch or step-by-step |

**Auto-triage:** When a task is described, assess scope and suggest the appropriate tier before starting.

---

## 5. Major Tier — Full Agent Pipeline

```
 1. ARCHITECT (Opus + extended thinking)
    confirm → invoke → present plan → wait for user approval
                          │
 2. DEVELOPER + TESTER (Sonnet, parallel)
    confirm → invoke both in same message → integrate results
                          │
 3. UNIT TESTS
    .venv/bin/pytest tests/ -v --tb=short
    fix failures in main conversation before proceeding
                          │
 4. SMOKE TESTS (user-driven, when applicable)
    run relevant sections from docs/smoke-tests.md
                          │
 5. DOCUMENTATOR (Sonnet)
    confirm → invoke → integrate result
                          │
 6. COMMIT / MERGE / PUSH
    always in main conversation, never inside an agent
                          │
 7. DOCS SYNC
    update architecture-review files, CLAUDE.md, sprints.md
                          │
 8. MEMORY SYNC
    check MEMORY.md against CLAUDE.md, update if needed
```

**Batch approval option** (Major tier only):
> *"Running full sprint pipeline. Approve all steps, or step-by-step?"*

---

## 6. Agent Orchestration

### Agent roster

| Agent | Model | Thinking | Role |
|-------|-------|----------|------|
| `architect` | Opus | Yes | Design, planning, architecture review |
| `developer` | Sonnet | No | Implementation |
| `tester` | Sonnet | No | Test suite creation |
| `documentator` | Sonnet | No | Documentation updates |
| `research` | Opus | Yes | Security research, threat intelligence |
| `Explore` | Sonnet | No | Codebase exploration |

### Invocation rule

Before invoking any agent, present a one-line notice and wait:

*"Invoking [AGENT NAME] agent to [brief purpose]. Proceed?"*

### Context templates

| Agent | Pass in |
|-------|---------|
| `architect` | Sprint goal, affected module list, constraints |
| `developer` | Approved plan + function signatures (full files only if >50% changes) |
| `tester` | Approved plan + interfaces/contracts (not implementation) |
| `documentator` | Changed files list + session-notes + module map changes |

### Error handling

| Situation | Action |
|-----------|--------|
| User rejects architect plan | Revise and re-invoke, or abandon |
| Agent fails or returns errors | Diagnose in main conversation, then re-invoke |
| Tests fail after dev agent | Fix in main conversation (not via re-invocation) |

---

## 7. Before Writing Code

1. **Read the full file** before editing — never edit blind
2. **Search for existing patterns** before creating new ones
3. **Verify tests pass** — never start on a broken baseline
4. **Use semantic search first** if a vector index is configured

---

## 8. After Writing Code

1. **Run tests immediately** — fix failures before moving on
2. **Commit atomically** — one logical change per commit
3. **Update session notes** after each major task

---

## 9. Git Workflow

### Branching
- **Never push directly to `main`** — always use feature branches
- Branch naming: `feat/<scope>` or `sprint/s<N>` from `main`
- After merge: tag `git tag sN-complete`, delete feature branch

### Commit conventions
- Format: `<type>(<scope>): <summary>`
- Types: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `chore`
- Summary: imperative mood, lowercase, no period, max 72 chars
- One logical change per commit — if docs reference changed code, update together

---

## 10. Testing Strategy

### Unit tests
- Framework: `pytest` with `pytest-xdist` (parallel, 8 workers)
- Location: `tests/unit/`
- Run: `.venv/bin/pytest tests/ -v --tb=short`
- Every sprint must end with all tests green

### Smoke tests
- Verify real behavior against live APIs through a proxy
- **User-driven** — never automated without explicit request
- **Always require a proxy-enabled profile** for downloads
- Reference: `docs/smoke-tests.md`

| Change type | Smoke test? |
|-------------|------------|
| Internal refactor | No |
| New CLI command | Yes |
| Download pipeline change | Yes |
| Auth/proxy/fingerprint | Yes — full cycle |
| Metadata/tagging | Yes — verify tags |

---

## 11. Documentation Lifecycle

### Document types

| Type | Lifespan | Examples |
|------|----------|---------|
| **Living** | Permanent — updated continuously | architecture.md, user-guide.md, smoke-tests.md |
| **Plan** | Until implemented, then archive | l1-plan.md, integration-plan.md |
| **Record** | Permanent — append-only | sprints.md, architecture-review-done.md |
| **Spec** | Permanent — versioned | spec.md, config-matrix.md |
| **One-off** | Until absorbed into Living doc | security-findings-*.md, capture guides |

### Rules

1. **Creation gate** — Can this go in an existing Living doc? If yes, add a section instead of a new file
2. **Plan archival** — Move completed Plan docs to `docs/archive/` during post-sprint bookkeeping
3. **One-off absorption** — Absorb into relevant Living doc within 1–2 sprints, then archive
4. **Periodic audit** — Every 5 sprints, scan for staleness. Archive anything untouched in 10+ sprints
5. **Active docs cap** — Target ~12 active files in `docs/`. If over 15, audit immediately

---

## 12. Architecture Diagrams

Maintained as **Mermaid** code blocks in `docs/diagrams/`.

### Why Mermaid
- Zero dependencies — renders natively on GitHub and in VSCode
- Git-friendly — plain text, clean diffs
- LLM-friendly — widely trained, easy to generate and update
- VSCode extension: `bierner.markdown-mermaid`

### Maintenance rules

1. **Update on change** — any sprint that changes depicted flow must update the diagram in the same commit
2. **Review trigger** — during architecture reviews, verify diagrams match code
3. **Creation gate** — only add a diagram if it helps understand the system faster than reading code
4. **Keep it high-level** — structure and flow, not implementation. Max ~30 nodes; split if larger

---

## 13. Architecture Review

**Cadence:** after every 3+ sprints merged to `main`.

### Process
1. Invoke **architect agent** — full codebase read of production modules
2. Produce findings in standardized table schema (Id, Problem, Priority, Severity, Effort, Sprint, Status)
3. Append to `docs/architecture-review.md` with `Status = backlog`
4. On sprint complete: move resolved items to `docs/architecture-review-done.md`

---

## 14. Post-Sprint Bookkeeping

Only 3 update points after each sprint:

| Update | When | What |
|--------|------|------|
| **session-notes.md** | After every major task | What changed, current state, next steps |
| **CLAUDE.md** | When rules, module map, or status changes | Test count + one-liner status |
| **docs/sprints.md** | After sprint merge | Sprint details (single source of truth) |

MEMORY.md: only update if a new gotcha was discovered. Never duplicate sprint status.

---

## 15. Memory Hygiene

`MEMORY.md` and `CLAUDE.md` can drift. CLAUDE.md is always authoritative.

### What belongs in MEMORY.md
- Environment setup (install, run tests)
- API/library gotchas that cause subtle bugs
- Decisions that would be wrong to re-derive

### What does NOT belong
- Anything already in CLAUDE.md (no duplication)
- Anything findable by reading the code
- Historical sprint notes (that's `docs/sprints.md`)

### Consistency check
Triggered by: "check memory consistency" or "check memory", or after every sprint merge.
1. Read both files
2. CLAUDE.md is authoritative — update MEMORY.md where they conflict
3. Remove duplicated entries
4. Delete topic files (`memory/*.md`) for completed work

---

## 16. Periodic Hygiene (Garbage Collection)

**Cadence:** after every architecture review (~5 sprints), or when clutter is noticeable.

1. **Branches** — `git branch --merged main` → delete all merged feature/sprint branches
2. **Untracked artifacts** — `git clean -n -d` → delete leaked test artifacts, caches, temp dirs
3. **Test organization** — verify test files are in correct directories
4. **Research files** — check for absorbed content → delete
5. **Large files** — find files >10 MB outside .git/.venv → evaluate if still needed

---

## 17. Security

- **Never commit secrets, credentials, tokens, or API keys**
- Verify `.gitignore` before `git add` on new projects
- Read files before staging if they might contain sensitive data
- Token/credential files: `chmod 0o600` always
- Secrets in environment variables or secrets manager — never in source

---

## 18. Code Standards (Python)

Global defaults (project CLAUDE.md may override):

- Python 3.10+ syntax and features
- Type hints on every function/method signature
- PEP 8 compliance, line length per project config
- Logger in every I/O module: `from <project>.logger import get_logger`
- `pathlib.Path` for filesystem operations
- No global mutable state — dependency injection

---

## Lifecycle Flow Summary

```
Session Start
    │
    ├── Load context (session-notes, CLAUDE.md, git status)
    ├── Run tests (establish baseline)
    │
    ▼
Task Triage (Micro / Standard / Major)
    │
    ├── [Micro]    Read → Edit → Test → Commit
    ├── [Standard] Sketch → Dev+Test → Commit
    └── [Major]    Architect → Dev+Test → Unit Tests → Smoke Tests
                       → Documentator → Commit → Docs Sync → Memory Sync
    │
    ▼
Post-Sprint Bookkeeping
    │
    ├── session-notes.md
    ├── CLAUDE.md (if needed)
    ├── docs/sprints.md
    └── MEMORY.md (if new gotcha)
    │
    ▼
Periodic Maintenance (~every 5 sprints)
    │
    ├── Architecture review
    ├── Diagram verification
    ├── Documentation audit
    ├── Memory consistency check
    └── Garbage collection
```
