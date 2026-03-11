<!--
  Purpose: Template for ~/.claude/CLAUDE.md — global rules that apply to ALL
  Claude Code projects on this machine. Installed by: claude-init → Init globals.
  Edit the installed copy at ~/.claude/CLAUDE.md, not this source file.
-->

# Global Claude Code Rules

> These rules apply to **ALL** projects. Project-level `CLAUDE.md` files extend but cannot weaken these rules.

---

## Session Startup

At the start of every session, in this order:

1. **Read `.claude/session-notes.md`** — understand current state and exact next steps.
2. **Read `CLAUDE.md` in the project root** — load project-specific rules, module map, and conventions.
3. **`git status`** — understand what is in flight (branch, staged changes, unpushed commits).
4. **Run the test suite** — establish a clean baseline. Do not write code against a failing suite.

If any step reveals a problem (failing tests, dirty state, stale notes), **report it before proceeding**.

---

## Permissions Model

### Auto-allowed (no confirmation needed)
- **File operations:** read, edit, create, delete project files
- **Command execution:** test runs, linters, build tools, git status/diff/log, package managers
- **Search & exploration:** grep, glob, web search, Qdrant queries, file reads

### Require explicit user approval
- **Git write operations:** `commit`, `merge`, `push`, `rebase`, `tag`, `branch -d/-D`
- **Destructive commands:** `git reset --hard`, `git checkout .`, `rm -rf`, `drop table`, anything that discards uncommitted work or affects shared state
- **Agent invocation:** switching to a Task agent (architect, developer, tester, documentator, Explore, etc.)

### Commit workflow (approval required)
1. Show `git diff --staged` summary and the proposed commit message.
2. Ask: *"Shall I commit with this message?"*
3. Execute only after explicit approval.

### Push/merge workflow (approval required)
1. State exactly what will happen (e.g., *"push 2 commits to origin/main"*).
2. Ask: *"Shall I proceed?"*
3. Execute only after explicit approval.

**Commit style:**
- One logical change per commit — never batch unrelated changes.
- If docs reference the changed code, update them in the same commit.
- Use conventional commits: `feat(scope): message`, `fix(scope): message`, `refactor(scope): message`.

---

## Before Writing Code

1. **Read the full file** before editing it — never edit blind.
2. **Search for existing patterns** before creating new ones — avoid duplication.
3. **Verify tests pass** — never start a change on a broken baseline.
4. **Use semantic search first** (if a vector index is configured) to find where behaviour lives before reading files manually.

---

## After Writing Code

1. **Run tests immediately** — fix failures before moving on.
2. **Commit atomically** — one logical change per commit.
3. **Update `.claude/session-notes.md`** after each major task or significant decision.

---

## Security

- **Never commit secrets, credentials, tokens, or API keys.**
- Verify `.gitignore` before `git add` on any new project.
- Read a file before staging it if it might contain sensitive data.
- Token and credential files: `chmod 0o600` always.
- Secrets go in environment variables or a secrets manager — never in source code or config files committed to git.

---

## Model Selection

- **Opus** (`claude-opus-4-6`): main conversation, `architect`, `research` agents.
- **Sonnet** (`claude-sonnet-4-6`): `developer`, `tester`, `documentator`, `Explore` agents.
- **Extended thinking:** enabled for `architect` and `research` agents.

---

## Context Management

### Session Notes (`.claude/session-notes.md`)

After every major task or significant decision, **prepend** an entry with:

```markdown
## YYYY-MM-DD — Summary title

**Branch:** `branch-name`

### Accomplished
| File/Area | Change |
|-----------|--------|
| `path/to/file.py` | What changed and why |

**Test count:** N tests, M failures.

### Current state
- What is done, what is in flight.

### Next steps
1. Concrete next action.
2. ...
```

Most recent entry goes first.

### Session Hygiene

- `/clear` between sprints or major context shifts — never carry stale context forward.
- `/compact` with a focus statement when context fills mid-task.
- `/cost` to monitor token usage periodically.

---

## Documentation

- Keep sprint/task status current — stale status is worse than no status.
- Never leave placeholder code (`{ ... }`) in architecture docs — use real or clearly-labelled pseudocode.
- Remove completed TODO items rather than leaving them checked off.
- Load docs on demand — do **not** load all project docs at session start.

---

## Memory Hygiene

`MEMORY.md` (auto-memory) and `CLAUDE.md` can drift apart over time. CLAUDE.md is always authoritative.

### When to sync

| Trigger | What to check |
|---------|--------------|
| Sprint or major feature completes | Sprint status, architectural decisions, key design choices |
| CLAUDE.md is significantly updated | MEMORY.md for contradictions or now-redundant entries |
| Session notes reveal changes since last session | Sprint status and credential/config model in MEMORY.md |

### Consistency check procedure

1. Read both MEMORY.md and CLAUDE.md.
2. Compare overlapping sections: sprint status, architectural decisions, code conventions, key fixes.
3. CLAUDE.md is authoritative — update MEMORY.md where they conflict.
4. Remove MEMORY.md entries that duplicate CLAUDE.md content (redundancy has no value).

### On-demand trigger

When the user says **"check memory consistency"** or **"check memory"** → run the consistency check immediately and report findings before making any changes.

---

## Code Standards (Python)

These apply when working on Python projects:

- Python 3.10+ syntax and features.
- Type hints on every function/method signature.
- PEP 8 compliance. Line length: 88 (Black default).
- Every module starts with a logger: `from <project>.logger import get_logger` / `log = get_logger(__name__)`.
- `pathlib.Path` for all filesystem operations.
- `pydantic` for data validation and settings.
- Async-first for I/O: `asyncio`, `httpx.AsyncClient`, `aiofiles`.
- No global mutable state — dependency injection.
