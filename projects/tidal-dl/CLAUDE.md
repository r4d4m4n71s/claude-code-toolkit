# tidal-dl — Claude Code Context

## Project
Private TIDAL downloader. HiRes FLAC 24-bit/192kHz + Dolby Atmos eac-3.
Stack: Python >=3.12, tidalapi (MIT), pycryptodome, mutagen, ffmpeg.
Repo: https://github.com/r4d4m4n71s/tidal-dl (private)
All persistent state: `~/.config/tidal-dl/` (config.toml, credentials.json, logs)

## Project status
**2590 tests on `main`** | No active backlog.
54+ sprints completed (S1-S54, Q1, P1-P3, pipeline decomposition, unified credential store).
Full history: `docs/sprints.md`

## Global rule overrides

| Global rule | This project |
|-------------|-------------|
| `pydantic` for data models | `dataclasses` — no pydantic dependency |
| Async-first I/O (`asyncio`, `httpx`) | Fully synchronous — `requests` + `subprocess`; tidalapi has no async API |
| Line length: 88 (Black) | `line-length = 100`, linter is `ruff` (see `[tool.ruff]` in pyproject.toml) |
| Python 3.10+ | `requires-python = ">=3.12"`, ruff target `py312` |

## Critical rules

### Security
- `credentials.py` is NEVER committed — it is in `.gitignore`
- `credentials.py` imports are always **lazy** (inside functions, never at module top)
- **NEVER merge to `main` or `dev` without explicit user approval**

### Smoke testing
- **NEVER run `tidal-dl dl` (downloads) without a proxy-enabled profile**

### Code conventions
- Every non-init module: `from __future__ import annotations` as the first import
- Every module with I/O or side effects: `from tidal_dl.logger import get_logger` / `log = get_logger(__name__)`
  Exception: `logger.py` itself and pure-logic modules (`utils/paths.py`, `providers/base.py`)
- Config reading: `tomllib` (stdlib, read-only). Config writing: `tomlkit` (preserves comments/formatting)

### Architecture
- Dependency direction: cli -> commands -> download/metadata/catalog/sessions -> config/logger/exceptions -> nothing
- API layer: api/ -> commands -> download/metadata/catalog/sessions -> config/logger/exceptions -> nothing

### Git workflow
- **NEVER push directly to `main`**. Always use feature branches.
- Branch: `feat/<scope>` or `sprint/s<N>` from `main`. Tag: `git tag sN-complete`.
- Commit format: `<type>(<scope>): <summary>` — details in `rules/commit-conventions.md`

## Module map
```
tidal_dl/
├── credentials.py        (NOT in repo)
├── exceptions.py
├── intents.py
├── logger.py
├── config.py
├── cli.py
├── api/                  session.py, facade.py
├── commands/             collection.py, info.py, wizard.py, library.py, library_sync.py, retag.py
├── auth/                 credential_store.py, device_flow.py, token_store.py, qobuz_auth.py
├── sessions/             builder.py, pool.py, fingerprint.py, http.py, fingerprint_registry.py
├── proxy/                iproxy.py, discovery.py, strategy.py, store.py
├── catalog/              resolver.py
├── download/             pipeline.py, batch_setup.py, item_processor.py, retry.py, track.py, governor.py, quality.py, segments.py, decrypt.py, video.py
├── events/               models.py, collector.py, encoding.py, sender.py
├── metadata/             tagger.py, artist.py, musicbrainz.py, playlist.py, qobuz_helpers.py
├── providers/            base.py, tidal.py, resolver.py, qobuz.py
└── utils/                ffmpeg.py, paths.py, progress.py, report.py, timing.py
```

## Code search
Use `Grep`/`Glob` + `Read` for navigation. The module map above and MEMORY.md provide sufficient context.

## Docs (load on demand — ~12 active files, see rules/workflow.md for lifecycle)
- Architecture: @docs/architecture.md
- Architecture review: @docs/architecture-review.md
- Config matrix: @docs/config-matrix.md
- Qobuz setup: @docs/qobuz-setup.md
- Reference: @docs/reference.md
- Smoke tests: @docs/smoke-tests.md
- Spec: @docs/spec.md
- Sprint history: @docs/sprints.md
- Security research: @docs/tidal-security-research.md
- User guide: @docs/user-guide.md
- Session context: @.claude/session-notes.md

## Workflow rules (load on demand)
- Sprint pipeline & agents: @rules/workflow.md
- Architecture review process: @rules/architecture-review.md
- Commit conventions: @rules/commit-conventions.md
- Security research process: @rules/security-research.md

## Session notes
- `/compact` focus hint: `Focus on tidal_dl [module] and current acceptance criteria`
- Cost target: < $2/session
- **Session notes rolling window**: keep only the last 5 entries in `session-notes.md`.
  When adding a 6th, drop the oldest entry.
- **Memory sync**: after every sprint merge, check MEMORY.md against CLAUDE.md for drift.
  Say "check memory consistency" or "check memory" for an immediate comparison.
