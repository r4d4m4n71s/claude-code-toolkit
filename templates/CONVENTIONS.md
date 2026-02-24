<!--
  Purpose: Template for each project's CONVENTIONS.md file.
  Installed by: claude-init → Init project → copied to <project>/CONVENTIONS.md.
  Documents git branching, commit message format, code style, and file naming.
  Edit the "Scopes" in the Commit Messages section to match your module names.
-->

# Conventions

> Git, branching, and code conventions for this project. Referenced by `CLAUDE.md`.

---

## Branching Strategy

| Branch | Purpose | Merges into |
|--------|---------|-------------|
| `main` | Stable, tagged releases | — |
| `dev` | Integration branch (optional) | `main` |
| `sN/slug` | Sprint work (e.g., `s8/polish`) | `main` or `dev` |
| `fix/slug` | Hotfixes | `main` |

- Create sprint branches from `main` (or `dev` if used).
- Sprint branches are short-lived — merge and delete after sprint completion.
- Always use `--no-ff` when merging sprint branches to preserve history.

---

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <short description>

[optional body]

[optional footer(s)]
```

**Types:**

| Type | When to use |
|------|------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test` | Adding or updating tests |
| `docs` | Documentation only |
| `chore` | Build, tooling, CI, dependencies |
| `perf` | Performance improvement |

**Scopes** match top-level module names (e.g., `auth`, `download`, `cli`, `config`, `utils`).

**Examples:**
```
feat(download): add per-segment retry with exponential backoff
fix(metadata): correct M4A freeform atom constant name
test(pipeline): add video download mock and retry tests
docs(sprints): update S8 completion status
refactor(sessions): extract fingerprint re-application to helper
```

**Rules:**
- Subject line: imperative mood, lowercase, no period, max 72 characters.
- Body: wrap at 80 characters. Explain *what* and *why*, not *how*.
- One logical change per commit — never batch unrelated changes.

---

## Tags

Tag every sprint completion on `main`:

```
git tag -a s<N>-complete -m "Sprint <N>: <title>"
```

Example: `git tag -a s8-complete -m "Sprint 8: Polish & Stability"`

---

## Pull Requests (if applicable)

- PR title follows commit message format: `feat(scope): description`.
- PR description includes: what changed, why, how to test.
- Squash-merge feature branches unless individual commits are meaningful.

---

## Code Style

- **Formatter:** Black (line length 88).
- **Linter:** Ruff.
- **Import order:** stdlib → third-party → local (enforced by Ruff/isort).
- **Type checking:** mypy or pyright in strict mode where feasible.

---

## File Naming

- Python modules: `snake_case.py`
- Test files: `test_<module_name>.py`
- Documentation: `kebab-case.md` or `snake_case.md` (pick one per project, stay consistent).
- Config files: lowercase (`config.toml`, `pyproject.toml`).
