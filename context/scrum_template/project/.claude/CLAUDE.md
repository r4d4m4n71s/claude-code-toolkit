<!--
  Purpose: Template for each project's .claude/CLAUDE.md file.
  Installed by: claude-init → Init project → copied to <project>/.claude/CLAUDE.md.
  The string "<project-name>" is substituted with the actual project name on install.
  Fill in all TODO sections before starting work.
-->

# <project-name> — Claude Code Context

## Project
<!-- TODO: One or two sentences describing what this project does. -->
<!-- Stack: language version, key libraries, build tool -->
<!-- Repo: URL (optional) -->
<!-- Persistent state: e.g., ~/.config/<project-name>/ or "none" -->

## Project status
<!-- TODO: Keep this block current — update at the start of each sprint. -->
**Current sprint:** S1 (initial setup)
Next: <!-- immediate next step -->

### Completed sprints
<!-- Fill in as sprints complete: S1 (slug), S2 (slug), ... -->
_(none yet)_

## Module map
<!-- TODO: Replace with your project's actual directory/module layout. -->
```
<project-name>/
├── ...    ← description
└── ...    ← description
```

## Global rule overrides
These project-specific rules override `~/.claude/CLAUDE.md` where they conflict:

| Global rule | This project |
|-------------|-------------|
| _(none — project follows global defaults)_ | — |

<!-- TODO: Add rows only for rules you actually need to override. Examples:
| `pydantic` for data models        | `dataclasses` — no pydantic dependency              |
| Async-first I/O                   | Fully synchronous — reason                          |
| Line length: 88 (Black)           | `line-length = 100`, linter is `ruff`               |
| Python 3.10+                      | `requires-python = ">=3.12"`, ruff target `py312`   |
-->

## Critical rules

### Security
- **NEVER merge to `main` or `dev` without explicit user approval**
<!-- TODO: List project-specific files or secrets that must never be committed. Example:
- `credentials.py` is NEVER committed — it is in `.gitignore`
- Imports of `credentials.py` must always be lazy (inside functions, never at module top)
-->

### Code conventions
<!-- TODO: Document project-specific conventions. Examples:
- Every module starts with: `from __future__ import annotations`
- Every I/O module: `from <project_name>.logger import get_logger` / `log = get_logger(__name__)`
- Config reading: `tomllib` (stdlib, read-only). Config writing: `tomlkit` (preserves formatting).
-->

### Architecture
<!-- TODO: Describe the dependency direction between your modules. Example:
- Dependency direction: cli → core/download/metadata → config/logger → nothing
- Commit scopes (match your module names): cli, config, core, utils
-->

## Semantic search (Qdrant MCP)
<!-- TODO: Set the server name to match your .mcp.json, or remove this entire section
     if you are not using Qdrant. -->
A Qdrant MCP server is configured as `<project-name>-search`.

**Use `qdrant-find` FIRST (before reading files) when:**
- Looking for where a specific behaviour is implemented
- Checking if a pattern already exists before writing new code
- Navigating to the right file for a feature
- Understanding how modules connect

**Read files directly when:**
- You already know the exact file and need the full content
- Writing new code that must match the exact current implementation
- Debugging a specific line number from an error trace

**Index lifecycle — `qdrant-store` triggers:**

| Trigger | Action |
|---------|--------|
| New function or module written | Store immediately after writing |
| Existing function behaviour or signature changed | Update the entry for that module |
| Cross-module refactor | Re-index all affected modules |
| Sprint completion (before merging to main) | Re-index every module touched in the sprint |

- Description format: `"<module>/<file>.py — <function_name>: <what it does in plain English>"`
- One entry per logical unit (class, key function, or closely related group of helpers)
- **Do NOT index:** test files, documentation, config files, or trivial helpers

## Docs (load on demand — do NOT load all at session start)
<!-- TODO: Update paths to match your project's actual documentation.
     For each large doc, maintain a *-summary.md sibling (1-2 pages) to load by default.
     Only pull the full file when the task directly involves writing or changing that content. -->
- Spec summary (load first):      @docs/spec-summary.md
- Full spec (when changing spec'd behaviour): @docs/spec.md
- Architecture summary (load first):          @docs/architecture-summary.md
- Full architecture (when refactoring structure): @docs/architecture.md
- Sprint details:  @docs/sprints.md
- Session context: @.claude/session-notes.md  ← read at session start; update after major tasks

## Project-specific session notes
- `/compact` focus hint: `Focus on <project-name> [module] and current acceptance criteria`
- **Memory sync**: after every sprint merge, check MEMORY.md against CLAUDE.md for drift
- **On-demand**: say "check memory consistency" or "check memory" to trigger an immediate comparison
- **Session notes rolling window**: keep only the last 5 entries in `session-notes.md`.
  When adding a 6th, move the oldest entry to `.claude/session-notes-archive.md` first.

## Agent orchestration

### Confirmation rule — MANDATORY
Before invoking ANY Task agent, always present this message first and wait for a yes:

```
I'm about to invoke the [AGENT NAME] agent to [brief purpose].
Do you want to proceed?
```

A "yes" answer immediately triggers that agent — no further confirmation for that same invocation.
Never invoke agents silently or without this prompt.

### When to use each agent

| Scope | Approach |
|-------|----------|
| 1–2 files, clear scope | Work directly in main conversation |
| 3+ files, or design decisions needed | Use agents (see pipeline below) |
| "Where is X implemented?" | `Explore` agent instead of grep + read loops |

All agents inherit these CLAUDE.md rules and the Qdrant search rules — use `qdrant-find` before reading files.
All git operations follow the global Git — Mandatory User Approval rules.

### Standard sprint pipeline

1. **architect** — confirm → invoke → present plan → wait for user approval of the plan
2. **developer + tester** — confirm (both together) → invoke in parallel (same message)
3. **documentator** — confirm → invoke → integrate result
4. **commit / merge / push** — always in the main conversation, never inside an agent
5. **memory sync** — after merge, check MEMORY.md against CLAUDE.md and update if needed

### Agent context templates

| Agent | Pass in |
|-------|---------|
| `architect` | Sprint goal, affected module list from module map, constraints (no breaking changes etc.) |
| `developer` | Architect's approved plan + function signatures of files to change (full file content only if >50% of the file changes) |
| `tester` | Architect's approved plan + interfaces/contracts (not implementation) |
| `documentator` | Changed files list + session-notes update + module map changes |

### Error handling
- User rejects architect's plan → revise and re-invoke architect, or abandon the sprint
- Developer/tester agent fails or returns errors → diagnose and fix in main conversation, then re-invoke
- Tests fail after developer agent → fix in main conversation (not via agent re-invocation)

### Sprint trigger phrase
When the user says **"start sprint N"** or **"plan sprint N"**:
- Ask: *"I'm about to invoke the architect agent to plan Sprint N. Do you want to proceed?"*
- On yes → immediately invoke `Task(architect)` with sprint goal + relevant file list + constraints
- Present the architect's output and wait for the user to approve the plan
- Ask: *"I'm about to invoke the developer and tester agents in parallel. Do you want to proceed?"*
- On yes → invoke `Task(developer)` + `Task(tester)` in the same message
- Integrate results, ask: *"I'm about to invoke the documentator agent. Do you want to proceed?"*
- On yes → invoke `Task(documentator)`
- Return to main conversation for commit/merge/push
