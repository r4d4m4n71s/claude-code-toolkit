# Architecture Review Process

> Loaded on demand. Trigger: "run architecture review" / "plan architecture review" / "start architecture review".
> Recommended cadence: after every 3+ sprints merged to `main`.

---

## Overview

A full-codebase read by the architect agent to find bugs, correctness gaps,
tech debt, performance issues, and improvement opportunities across production modules.

---

## Review Files

| File | Purpose |
|------|---------|
| `docs/architecture-review.md` | Active findings — `backlog`, `planned`, `in-progress` |
| `docs/architecture-review-done.md` | Historical record — all `done` items |

Both files stay sorted **priority descending** within each review batch.

---

## Review Process

1. Invoke the **architect agent** with scope: "full codebase architecture review of `tidal_dl/`"
2. Architect reads all production modules (not tests, docs, or config files)
3. Produces findings in the table schema below; groups by proposed sprint
4. Append new findings to `docs/architecture-review.md` with `Status = backlog`
5. Assign a batch prefix letter (A, B, C, ...) to all new items in the review
6. Update `Planned sprints` section in CLAUDE.md with the new sprint list

### Incremental review option

Instead of full codebase read, scope to modules changed since last review:
```bash
git diff --name-only <last-review-tag>..HEAD -- tidal_dl/
```

---

## Table Schema — 8 columns

`Id | Problem | Description | Priority | Severity | Effort | Sprint | Status`

| Column | Values / Description |
|--------|---------------------|
| Id | Batch letter + number (e.g. `A1`, `B3`) |
| Problem | Short label (3-5 words) |
| Description | What's wrong and why it matters. Include affected files here. |
| Priority | 1 (critical) to 5 (nice-to-have) |
| Severity | critical / high / medium / low |
| Effort | XS / S / M / L / XL |
| Sprint | Target sprint (e.g. `S55`) or `backlog` |
| Status | `backlog` / `planned` / `in-progress` / `done` |

---

## Maintenance Rules

- **On sprint start:** set `Status = in-progress` for all items in that sprint
- **On sprint complete & merged to `main`** (mandatory post-merge step):
  1. Move resolved rows from `architecture-review.md` -> `architecture-review-done.md`
  2. Set `Status = done` on moved rows
  3. Update the sprint plan table (strike through completed sprint)
  4. Update CLAUDE.md: test count + completed sprints list
  5. Add sprint entry to `docs/sprints.md` (overview table + detailed section)
  6. Commit the docs sync updates
- **New finding mid-sprint:** add to `architecture-review.md` with `Status = backlog`
- **Cross-check rule:** any sprint that resolves review items MUST update both review files
