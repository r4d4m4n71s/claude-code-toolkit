# Global Claude Code Rules

> These rules apply to **ALL** projects. Project-level `CLAUDE.md` files extend but cannot weaken these rules.

---

## Session Startup

Adaptive startup based on session intent:

| Intent | Steps |
|--------|-------|
| **Continuing previous work** | session-notes -> git status -> targeted file reads |
| **New feature / sprint** | session-notes -> git status -> load workflow rules -> run tests |
| **Bug fix** | session-notes -> git status -> run tests -> read failing module |
| **Docs / config only** | session-notes -> git status (skip test suite) |
| **Housekeeping** ("check memory") | MEMORY.md vs CLAUDE.md comparison (no tests needed) |

Always read `.claude/session-notes.md` and project `CLAUDE.md` first.
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

### What belongs in MEMORY.md
- Environment setup (how to install, run tests)
- API/library gotchas that cause subtle bugs
- Decisions that would be wrong to re-derive

### What does NOT belong in MEMORY.md
- Anything already in CLAUDE.md (no duplication)
- Anything findable by reading the code (module descriptions, function signatures)
- Historical sprint/feature notes (that's what `docs/sprints.md` is for)

### Consistency check

When the user says **"check memory consistency"** or **"check memory"**:
1. Read both MEMORY.md and CLAUDE.md.
2. CLAUDE.md is authoritative — update MEMORY.md where they conflict.
3. Remove MEMORY.md entries that duplicate CLAUDE.md content.

Also check after every sprint merge or significant CLAUDE.md update.

### Topic files cleanup
- Memory topic files (e.g., `l1-plan.md`, `sprint-details.md`) should be deleted when their subject is complete.
- During consistency checks, scan `memory/` for files beyond `MEMORY.md` and delete any that reference completed work.

---

## Code Standards (Python)

These apply when working on Python projects (project-level CLAUDE.md may override):

- Python 3.10+ syntax and features.
- Type hints on every function/method signature.
- PEP 8 compliance. Line length: 88 (Black default).
- Every module starts with a logger: `from <project>.logger import get_logger` / `log = get_logger(__name__)`.
- `pathlib.Path` for all filesystem operations.
- `pydantic` for data validation and settings.
- Async-first for I/O: `asyncio`, `httpx.AsyncClient`, `aiofiles`.
- No global mutable state — dependency injection.
