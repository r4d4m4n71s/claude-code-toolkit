# <project-name> — Claude Code Context

<!--
  Purpose: Template for each project's root CLAUDE.md file.
  Installed by: claude-init → Init project → copied to <project>/CLAUDE.md.
  Extends ~/.claude/CLAUDE.md (global rules) — cannot weaken them.
  Fill in each section and delete inline comments that don't apply.
-->

## Project

<!-- One paragraph: what the project does, core stack, repo link. -->

**Description:** ...
**Stack:** Python 3.12, ...
**Repo:** https://github.com/...

## Current Sprint

<!-- Update this every time a new sprint starts. -->

**Sprint N — Title** · branch: `sN/slug`
**Goal:** One-sentence sprint goal.
**Key files:** `path/to/file.py`, ...

### Completed Sprints

<!-- One line per sprint: SN (topic). Keep it compact. -->

S1 (auth), S2 (core feature), S3 (...)

## Module Map

<!-- Directory tree of your source package. Keep it current. -->

```
project/
├── config.py         ← Brief description
├── cli.py            ← Brief description
├── module_a/         ← Brief description
│   ├── core.py
│   └── helpers.py
└── utils/            ← Brief description
    └── ...
```

## Critical Rules

<!-- Project-specific rules that Claude must always follow. Keep these few and non-negotiable. -->

- `credentials.py` is NEVER committed — it is in `.gitignore`.
- Every module starts with: `from project.logger import get_logger` / `log = get_logger(__name__)`.
- Dependency direction: `cli → services → core → config/logger → nothing`.
- Commit scopes match module names: `auth`, `download`, `cli`, `config`, `utils`, etc.
- **NEVER merge to `main` or `dev` without explicit user approval.**

## Semantic Search

<!-- If you use a vector index (Qdrant, Chroma, etc.), document how to use it. Delete this section if not applicable. -->

A Qdrant MCP server is configured as `<collection-name>`.

**Use `qdrant-find` FIRST (before reading files) when:**
- Looking for where a specific behaviour is implemented.
- Checking if a pattern already exists before writing new code.
- Navigating to the right file for a feature.
- Understanding how modules connect.

**Read files directly when:**
- You already know the exact file and need the full content.
- Writing new code that must match the exact current implementation.
- Debugging a specific line number from an error trace.

**Index lifecycle — `qdrant-store` triggers:**

| Trigger | Action |
|---------|--------|
| New function or module written | Store immediately after writing |
| Existing function signature changed | Update the entry for that module |
| Cross-module refactor | Re-index all affected modules |
| Sprint completion | Re-index every module touched in the sprint |

- Description format: `"<module>/<file>.py — <function_name>: <what it does>"`
- One entry per logical unit (class, key function, or closely related helpers).
- **Do NOT index:** test files, docs, config files, or trivial helpers.

## Docs

<!-- List project docs with loading guidance. Use @ references for Claude Code. -->

| Doc | Path | When to load |
|-----|------|-------------|
| Spec | `@docs/spec.md` | When clarifying requirements |
| Architecture | `@docs/architecture.md` | When understanding or changing design |
| Sprint details | `@docs/sprints.md` | When reviewing sprint scope |
| Git conventions | `@CONVENTIONS.md` | When unsure about commit/branch style |
| Session notes | `@.claude/session-notes.md` | **Always at session start**; update after major tasks |

**Load on demand — do NOT load all docs at session start.**

## Session Hygiene

<!-- Project-specific context management tips. -->

- `/clear` between sprints — never carry stale context forward.
- `/compact Focus on <project> <module> and current acceptance criteria` when context fills mid-sprint.
- `/cost` to monitor token usage — target < $N/session.
