# Commit Conventions

> Loaded on demand. Reference when making commits or reviewing commit history.

---

## Format

```
<type>(<scope>): <summary>

[optional body]
```

---

## Types

| Type | When |
|------|------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code restructure with no behavior change |
| `perf` | Performance improvement |
| `test` | Adding or updating tests only |
| `docs` | Documentation only |
| `chore` | Config, CI, dependencies, tooling |

---

## Scopes

Match module names: `auth`, `sessions`, `proxy`, `catalog`, `download`, `decrypt`, `metadata`, `events`, `cli`, `config`, `logger`, `utils`, `providers`, `commands`, `api`

---

## Rules

- Summary: imperative mood, lowercase, no period, max 72 chars
- Body (optional): blank line after summary, explain *why* not *what*
- Reference sprint/item IDs in body or summary: `D4c`, `C6`, `S27`
- One logical change per commit — never batch unrelated changes
- Multi-scope changes use the primary scope or omit scope: `feat: ...`

---

## Examples

```
feat(metadata): add COMPOSER and UPC tags to FLAC/M4A
fix(download): handle stub album in single-track URLs
refactor(events): extract envelope builder into helper
chore(config): clean up settings + remove Qdrant MCP
docs: add comprehensive user guide
test(tagger): add edge cases for empty artist_roles
```
