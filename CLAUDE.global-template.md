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

1. **Read `docs/session-notes.md`** — understand current state and exact next steps.
2. **Read `CLAUDE.md` in the project root** — load project-specific rules, module map, and conventions.
3. **`git status`** — understand what is in flight (branch, staged changes, unpushed commits).
4. **Run the test suite** — establish a clean baseline. Do not write code against a failing suite.

If any step reveals a problem (failing tests, dirty state, stale notes), **report it before proceeding**.

---

## Git — Mandatory User Approval

**NEVER execute any of the following without showing the exact command and receiving explicit user confirmation:**

| Command | What to show first |
|---------|-------------------|
| `git commit` | Staged diff + proposed commit message |
| `git merge` | Source → target branch, merge strategy |
| `git push` | What will be pushed, to which remote/branch |
| `git rebase` | Rebase plan (which commits, onto what) |
| `git tag` | Tag name + target commit |
| `git branch -d / -D` | Which branch will be deleted |
| `git reset / restore / checkout .` | What will be discarded |

**Commit workflow:**
1. Show `git diff --staged` and the proposed commit message.
2. Ask: *"Shall I commit with this message?"*
3. Execute only after explicit approval.

**Merge/push workflow:**
1. State exactly what will happen (e.g., *"merge `s8/polish` into `main` with `--no-ff`"*).
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
3. **Update `docs/session-notes.md`** after each major task or significant decision.

---

## Security

- **Never commit secrets, credentials, tokens, or API keys.**
- Verify `.gitignore` before `git add` on any new project.
- Read a file before staging it if it might contain sensitive data.
- Token and credential files: `chmod 0o600` always.
- Secrets go in environment variables or a secrets manager — never in source code or config files committed to git.

---

## Model Selection

- **Default:** Sonnet for all tasks.
- **Switch to Opus for:** architecture decisions, complex multi-file refactors, cross-cutting design changes.
- **Always notify the user** when switching models and state the reason.

---

## Context Management

### Session Notes (`docs/session-notes.md`)

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
