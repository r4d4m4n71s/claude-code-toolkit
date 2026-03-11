# tidal-dl — Claude Code Context

## Project
Private TIDAL downloader. HiRes FLAC 24-bit/192kHz + Dolby Atmos eac-3.
Stack: Python >=3.12, tidalapi (MIT), pycryptodome, mutagen, ffmpeg.
Repo: https://github.com/r4d4m4n71s/tidal-dl (private)
All persistent state: `~/.config/tidal-dl/` (config.toml, credentials.json, logs)

## Project status
**2590 tests on `main`**
L1 complete (S49-S53). S54 complete (Batch N — 15 findings resolved). Q1 Qobuz quality check complete. B8/B10/B11 closed (future-monitoring). No active backlog.

### Completed sprints
S1 (auth), S2 (first download), S3 (concurrent), S4 (quality output — ffmpeg remux, mutagen tags, decrypt),
S5 (Dolby Atmos — eac-3, fingerprint re-application), S6 (proxy strategy — single-identity model),
S7 (user-facing CLI — status, dl flags, path templates, 119 tests),
S8 (polish & stability — retry logic, progress bar, video wiring, 134 tests),
S9 (download profiles — named presets, inheritance, credential rotation, video quality, 162 tests),
S10 (lyrics — unsynced lyrics embedded in FLAC/M4A, 172 tests),
S11 (download report — per-batch events, console summary, JSON file, 228 tests),
S12 (hardening — PKCS7 validation, typed exceptions, rate-limit backoff, tz-aware expiry, 288 tests),
S13 (robustness — JitterState per-batch, hasattr MixV2 fix, ConnectionDownError in video, 305 tests),
S14 (tech debt — lazy logger, NullHandler, TokenStatus dataclass, ProgressCallback alias, 318 tests),
S15 (quality of life — proxy masking, TokenStatus.token_age_days, _download_video_item, ArtistLike/CredentialLike protocols, playlist pagination cap, 342 tests),
S16 (proxy completeness — video fully proxied, ConnectionDownError parity, segment fast-fail, masked logs, 355 tests),
S17 (catalog correctness — MixV2 pagination, tagger null-guard, streaming segment write, jitter reset, 377 tests),
S18 (type safety — Item union annotation, artist_mode ConfigError guard, 396 tests),
S19 (error handling completeness — corrupt token AuthExpiredError, empty URL guard, --file validation, ConfigError at CLI, double-unlink fix, template validation at load, 415 tests),
S20 (retry logic correctness — Retry-After honor, FFmpegError permanent skip, catalog rate-limit guard, mpegdash pin, 425 tests),
S21 (security quick wins — per-device UA, device ID persistence, MixV2 deviceType, catalog_session ensure_valid, 435 tests),
S22 (security hardening — TLS/HTTP2 fingerprint via curl-adapter, DNS leak prevention, client_version update to 2.3.0, 445 tests),
S23 (architecture quality — per-credential token age, config property caching, input() removal, ProxyStore enforcement, country_code persistence, 458 tests),
S24 (DX & observability — config defaults single source of truth, HLS URL resolution, configurable file log level, jitter test isolation, 465 tests),
S25 (playback event reporting — B2 streaming metrics, 3 events per track, SDK envelope, SQS batch encoding, fire-and-forget sender, opt-in config, 502 tests),
S26 (event safety + CLI robustness — thread-safe event context, dedicated sender session, fresh tokens, events on abort, ConfigError/AuthExpiredError CLI catches, 521 tests),
S28 (UX & library metadata — login cred label, quality diff on skip, artist bio/image, album cover.jpg, synced lyrics .lrc, skip_videos, 584 tests),
S28b (D4+E8+E9 — ALBUMARTIST/COPYRIGHT tags, .m3u8 playlist save, sync command, Walkman profile, 625 tests),
S28c (D4b+D4c — extended tags + track enrichment: composer, totals, key, peak, UPC, full album fetch, template fix, 650 tests),
S27 (events polish + tech debt — video events, envelope name field, backoff comment, init docstrings, logger annotations, status events field, 670 tests),
S29 (correctness & security — video proxy leak fix, proxy log masking, quality diff crash, enrichment rate-limit, cover art dedup, config key warnings, peak truthiness, resolver type, future annotations, 682 tests),
S30 (DX & tech debt — persist read optimization, EventSender close, lazy %s logging, video quality validation, login pool comment, config cache invalidation, unused param removal, sync flag comment, country_code guard, stderr config error, ConfigError re-raise, per-credential refresh threshold, 693 tests),
S31 (low priority / structural — Atmos cache, decrypt existence check, memory bound comment, M3U8 sanitisation, pipeline split into quality.py + track.py, event discard log, 723 tests),
S32 (download governor — self-tuning rate limiter, token bucket, adaptive capacity, 3 presets, per-credential history, enabled by default, 818 tests),
S33 (collection command — download all favorites without URLs, type filter, in-memory dedup, album cache pre-seeding, state persistence, governor integration, dry-run, 853 tests),
S34 (plan estimator — --plan/--preset flags for dl and collection, multi-preset comparison, session estimation, collection progress in status, enriched state file, 909 tests),
S35 (correctness & safety — None expiry guard, governor 429 drift fix, governor.json chmod, UTF-8 encoding on governor + report files, record_session finally guard, 940 tests),
S36 (tech debt & DX polish — PRESETS import scope, public API renames, dead save_state removal, module-level governor validation sets, type annotations for CollectionResult/GovernorPreset/Item, 940 tests),
S37 (correctness & quick fixes — duplicate config warnings, collection state on partial success, rate-limit abort, session summary log, stealth tier resolution, .dec cleanup, CLI override helper, MixV2 collection fallback, 1013 tests),
S38 (remaining I-series — ISRC copy-on-duplicate, batch risk warning, governor thread safety, passive browse list optimization, single-syscall file check, proxy HEAD status check, fingerprint caching, emit_report public API, event context getter, sanitise dedup, history window class constant, 1062 tests),
S39 (smoke test improvements — proxy timeout fix, cross-batch ISRC cache, --output-dir flag, --no-governor flag, region quality warning, proxy resume hint, playlist_dir config, dated log files, millisecond timestamps, commented-out config defaults, 1062 tests),
S40 (MusicBrainz genre enrichment — ISRC-to-genre lookup, multi-level genre cascade, session caches, FLAC multi-value + M4A semicolon-separated GENRE tag, genre_lookup config, 1111 tests),
S41 (info + retag — metadata inspection without downloading, retag Phase 1 genre-only backfill via MusicBrainz, 3-level caching, table/json/csv output, K1 resolved, 1341 tests),
S42 (library stats + export + enhanced status — status --library, tidal-dl export CSV/JSON, governor/report stats in status, L1 backlog added, 1437 tests),
S43 (resolve command + per-profile proxy — cross-account pipeline, tidal-dl resolve URL→track URLs, --file batch, --dedup, --format urls/json/count, per-profile proxy_url with 3-way resolution, login proxy notification, 1513 tests),
S44 (library-sync — cross-account favorites & playlist sync, to-local snapshots, sync_write_enabled guard, SyncRateLimiter 30/hr, additive/mirror modes, playlist deep sync, audit log, 1607 tests),
S45 (profile permissions + login safety + library-sync batch — permissions field query-only/download-tracks-only/download-videos-only/download, CLI guard + pipeline filtering, login proxy warning box, batch playlist strategy sync_track_strategy=playlist ~50x faster, playlist upsert by UUID/name, catalog_jitter removed from library-sync, 1670 tests),
S46+S47 (library-sync perf + type safety & code dedup — batch favorites add ~20x faster, truncation warnings, playlist rate limiter, SKIPPED_TRACK EventType, governor public property, shared tag helpers, _emit_report hack removed, dead _context removed, per-profile proxy in fingerprint registry, 1809 tests),
S48 (remaining Batch M — MB thread-safe rate limit, genre_miss_count rename, SyncRateLimiter cap, catalog_session cache, Governor zero-margin guard, M3U8 relative_to guard, .dec extension fix, .lrc cleanup on failure, 1824 tests),
S49/L1a (module domain reorganization — 9 modules moved into commands/, download/, metadata/, sessions/ subpackages, no backward-compat shims, 1907 tests),
S50/L1b (API layer + exception consolidation — tidal_dl/exceptions.py TidalDLError hierarchy, tidal_dl/api/session.py TidalSession context manager + build_pool() move, tidal_dl/api/facade.py TidalAPI facade, no backward-compat shims, 2000 tests),
S51/L1c (intent system — tidal_dl/intents.py with 6 presets, 5-layer config resolution, --intent CLI flag, 2074 tests),
S52/L1d (wizard enhancement — tidal_dl/commands/wizard.py interactive setup, --estimate/--recommend/--profile, 2116 tests),
S53/L1e (documentation — architecture-summary, user-guide, reference updated; sessions/exceptions.py + credentials.example.py removed, 2115 tests),
S54/Batch N (post-L1 correctness + cleanup — pool cleanup, wizard profile fix, parse_url public, active_name property, CONFIG_DIR DRY, safety_order(), 15 findings, 2140 tests),
Smoke test fixes (token refresh persistence, enrichment-before-skip ordering, ASCII quality diff separator, DNS warning downgrade, 725 tests),
UX polish (setup command, user guide rewrite, reports subfolder, 733 tests),
Q1 (Qobuz catalog quality check — ISRC-based cross-provider comparison, credential extraction from web player, rate-limited API client, segment progress callback, 2317 tests),
Retag --fix-quality (TIDAL_QUALITY tag correction from stream properties, write_quality_tag, SUPPORTED_TAGS export, 2344 tests),
P1 (multi-provider protocol — DownloadProvider protocol, StreamInfo/QualityInfo dataclasses, TidalProvider adapter, SourceResolver priority/best-quality, download_sources config, 2415 tests),
Pipeline decomposition (pipeline.py 1538→461 lines, extracted batch_setup.py + item_processor.py + retry.py + track.py, pytest-xdist 3x speedup, 2481 tests),
P3 (Qobuz fingerprint hardening + UX polish — make_qobuz_session TLS+proxy+UA rotation, PROVIDER_FALLBACK event, direct download progress, 13 fingerprint vectors, 2526 tests),
Unified credential store (single credentials.json for all TIDAL + Qobuz tokens, proxy mismatch detection, auto-migration from scattered files, IProxy.get_mapped_profile_name(), test isolation fixture, 2590 tests)

### Planned sprints (all complete — backlog only)
Full item details and sprint groupings: `docs/architecture-review.md`

~~**S20 — Retry Logic + Dependency Guard** — A2, A6, A10, B9 (done, 425 tests)~~
~~**S21 — Security Quick Wins** — B1, B7, B12, B13 (done, 435 tests)~~
~~**S22 — Security Hardening** — B3, B5, B6 (done, 445 tests)~~
~~**S23 — Architecture Quality** — A5, A8, A9, A11, A13 (done, 458 tests)~~
~~**S24 — DX & Observability** — A14, A15, A17, A18 (done, 465 tests)~~
~~**S25 — Playback Event Reporting** — B2 (done, 502 tests)~~
~~**S26 — Event Safety + CLI Robustness** — C1, C2, C3, C4, C5, C9 (done, 521 tests)~~
~~**S27 — Events Polish + Tech Debt** — C6, C7, C8, C10, C11, C12 (done, 670 tests)~~
~~**S29 — Correctness & Security Quick Fixes** — F2, F5, F9, F13, F16, F18, F20, F23, F27 (done, 682 tests)~~
~~**S30 — DX & Tech Debt** — F1, F3, F6, F7, F8, F10, F12, F14, F15, F19, F25, F26 (done, 693 tests)~~
~~**S31 — Low Priority / Structural** — F4, F11, F17, F21, F22, F24 (done, 723 tests)~~
~~**S34 — Collection Progress & Plan Estimator** — G1 (done, 909 tests)~~
~~**S35 — Correctness & Safety** — H1, H2, H3, H4, H10, H15 (done, 940 tests)~~
~~**S36 — Tech Debt & DX Polish** — H5, H6, H7, H8, H9, H11, H12, H13, H14 (done, 940 tests)~~
~~**S37 — Correctness & Quick Fixes** — I5, I6, I11, I14, I15, I16, I24, I29 (done, 1013 tests)~~
~~**S38 — Remaining I-Series** — I1, I2, I3, I7, I8, I9, I17, I22, I23, I26, I30, I31 (done, 1062 tests)~~
~~**S39 — Smoke Test Improvements** — J1, J2, J3, J4, J5, J6 (done, 1062 tests)~~
~~**S40 — MusicBrainz Genre Enrichment** — D4 (done, 1111 tests)~~
~~**S46+S47 — Library-Sync Perf + Type Safety & Code Dedup** — M2, M3, M4, M5, M6, M8, M9, M12, M14, M16, M19 (done, 1809 tests)~~
~~**S48 — Remaining Batch M** — M1, M7, M10, M11, M13, M15, M17, M18, M20 (done, 1824 tests)~~
~~**S49/L1a — Module Domain Reorganization** — L1 structural moves (done, 1907 tests)~~
~~**S50/L1b — API Layer + Exception Consolidation** — exceptions.py, api/session.py, api/facade.py (done, 2000 tests)~~
~~**S51/L1c — Intent System** — intents.py, 6 presets, 5-layer resolution, --intent CLI (done, 2074 tests)~~
~~**S52/L1d — Wizard Enhancement** — commands/wizard.py, --estimate/--recommend/--profile (done, 2116 tests)~~
~~**S53/L1e — Documentation** — architecture-summary, user-guide, reference, stale file cleanup (done, 2115 tests)~~
~~**S54/Batch N — Post-L1 correctness + cleanup** — N1–N10, N13, N14, N16, N17, N19 (done, 2140 tests)~~
~~**S54b/Batch N backlog** — N11, N12, N18 (done, 2140 tests)~~
~~**Backlog** — B8, B10, B11 closed (future-monitoring). B4 closed via research. I4 done (954 tests). K1 retag Phase 1 done (S41). L1 complete (S49-S53).~~

## Module map
```
tidal_dl/
├── credentials.py    ← NOT in repo — see tidal_dl/credentials.py.example
├── exceptions.py     ← TidalDLError base + 10 consolidated exception subclasses
├── intents.py        ← 6 intent presets (download-fast/safe/stealth, query-only, library-sync, collection-safe)
├── logger.py         ← get_logger(__name__) — import in every I/O module
├── config.py         ← ProjectConfig.load(profile=) — TOML, profiles with inheritance, STEALTH_TIERS, intent resolution
├── cli.py            ← argparse entry point (dl, login, status, rotate, sync, setup, collection, cleanup, info, retag, export, resolve, library-sync)
├── api/              ← Public programmatic API
│   ├── session.py        ← TidalSession context manager + build_pool()
│   └── facade.py         ← TidalAPI stateless convenience facade
├── commands/         ← CLI subcommand implementations
│   ├── collection.py     ← Fetch and deduplicate user favorites; state persistence
│   ├── info.py           ← Metadata inspection (fetch_track/album/playlist/artist/video_info, formatters)
│   ├── wizard.py         ← Interactive setup wizard (choose intent → estimate → recommend → write)
│   ├── library.py        ← Library scanning, metadata export (CSV/JSON), stats aggregation
│   ├── library_sync.py   ← Cross-account library sync (snapshot, diff, apply, rate limiter, audit)
│   └── retag.py          ← Retag existing files (scan, read, write genre/quality tags, batch with MB caching)
├── auth/             ← credential_store.py, device_flow.py, token_store.py, qobuz_auth.py
│   ├── credential_store.py  ← UnifiedCredentialStore singleton (credentials.json), dataclasses, migration
│   └── qobuz_auth.py        ← Qobuz credential extraction (bundle.js → app_id + secret), caching
├── sessions/         ← builder.py, pool.py, fingerprint.py, http.py, fingerprint_registry.py
│   ├── http.py               ← TLS fingerprint adapter (curl-adapter / curl_cffi)
│   ├── http.py               ← TLS fingerprint adapter (curl-adapter / curl_cffi), make_qobuz_session()
│   └── fingerprint_registry.py ← FingerprintVector registry (13 vectors), build_registry(), log_registry()
├── proxy/            ← iproxy.py (ABC + ProxyInfo), discovery.py (entry point), strategy.py (IProxy-backed), store.py (mask utils)
├── catalog/          ← resolver.py (6 URL types + MixV2 fallback)
├── download/         ← pipeline.py (thin orchestrator), batch_setup.py, item_processor.py, retry.py, track.py, governor.py, quality.py, segments.py, decrypt.py, video.py
│   ├── pipeline.py       ← download_items() loop, download_video_item(), download(), emit_report()
│   ├── batch_setup.py    ← BatchContext dataclass, build_batch_context(), teardown_batch()
│   ├── item_processor.py ← prepare_track(), post_download(), handle_video(), inter_track_delay()
│   ├── retry.py          ← retry_download_track() — retry loop with exception dispatch
│   ├── track.py          ← TrackDownloadResult, _download_track(), _download_direct()
│   ├── governor.py       ← Download governor — token bucket rate limiter, adaptive capacity
│   └── quality.py        ← Stream quality derivation + QobuzQualityResult + check_qobuz_quality()
├── events/           ← models.py, collector.py, encoding.py, sender.py (playback event reporting)
├── metadata/         ← tagger.py, artist.py, musicbrainz.py, playlist.py, qobuz_helpers.py
│   ├── musicbrainz.py    ← ISRC-to-genre lookup via MusicBrainz API, session-level caches
│   ├── playlist.py       ← M3U8 read/write/diff for playlist sync
│   └── qobuz_helpers.py  ← Genre formatting utility for Qobuz hierarchical genres
├── providers/        ← base.py (DownloadProvider protocol + StreamInfo/QualityInfo), tidal.py, resolver.py, qobuz.py
│   ├── tidal.py          ← TidalProvider adapter over SessionPool
│   ├── resolver.py       ← SourceResolver (priority/best-quality strategies)
│   └── qobuz.py          ← QobuzClient (ISRC search, rate-limited API), QobuzTrack dataclass
└── utils/            ← ffmpeg.py, paths.py, progress.py, report.py, timing.py
```

## Global rule overrides
These project-specific rules override `~/.claude/CLAUDE.md` where they conflict:

| Global rule | This project |
|-------------|-------------|
| `pydantic` for data models | `dataclasses` — no pydantic dependency |
| Async-first I/O (`asyncio`, `httpx`) | Fully synchronous — `requests` + `subprocess`; tidalapi has no async API |
| Line length: 88 (Black) | `line-length = 100`, linter is `ruff` (see `[tool.ruff]` in pyproject.toml) |
| Python 3.10+ | `requires-python = ">=3.12"`, ruff target `py312` |

## Critical rules

### Security
- `credentials.py` is NEVER committed — it is in `.gitignore`
- `credentials.py` imports are always **lazy** (inside functions, never at module top) — file is absent from repo
- **NEVER merge to `main` or `dev` without explicit user approval**

### Smoke testing
- **NEVER run `tidal-dl dl` (downloads) without a proxy-enabled profile** — all download smoke tests must go through the proxy to avoid exposing the real IP to TIDAL servers

### Code conventions
- Every non-init module: `from __future__ import annotations` as the first import
- Every module with I/O or side effects: `from tidal_dl.logger import get_logger` / `log = get_logger(__name__)`
  Exception: `logger.py` itself and pure-logic modules (`utils/paths.py`, `providers/base.py`)
- Config reading: `tomllib` (stdlib, read-only). Config writing: `tomlkit` (preserves comments/formatting)

### Architecture
- Dependency direction: cli → commands → download/metadata/catalog/sessions → config/logger/exceptions → nothing
- API layer: api/ → commands → download/metadata/catalog/sessions → config/logger/exceptions → nothing

### Git branching workflow
- **NEVER push directly to `main`**. Always use feature branches.
- Sprint/feature work: create `feat/<scope>` or `sprint/s<N>` branch from `main`
- When ready: merge feature branch → `main` (with user approval)
- Tag after merge: `git tag s<N>-complete`
- Delete feature branch after merge

### Commit message convention
Format: `<type>(<scope>): <summary>`

**Types:**
| Type | When |
|------|------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code restructure with no behavior change |
| `perf` | Performance improvement |
| `test` | Adding or updating tests only |
| `docs` | Documentation only |
| `chore` | Config, CI, dependencies, tooling |

**Scopes** (match module names):
`auth`, `sessions`, `proxy`, `catalog`, `download`, `decrypt`, `metadata`, `events`, `cli`, `config`, `logger`, `utils`, `providers`, `commands`, `api`

**Rules:**
- Summary: imperative mood, lowercase, no period, max 72 chars
- Body (optional): blank line after summary, explain *why* not *what*
- Reference sprint/item IDs in body or summary: `D4c`, `C6`, `S27`
- One logical change per commit — never batch unrelated changes
- Multi-scope changes use the primary scope or omit scope: `feat: ...`

**Examples:**
```
feat(metadata): add COMPOSER and UPC tags to FLAC/M4A
fix(download): handle stub album in single-track URLs
refactor(events): extract envelope builder into helper
chore(config): clean up settings + remove Qdrant MCP
docs: add comprehensive user guide
test(tagger): add edge cases for empty artist_roles
```

## Code search
Use `Grep`/`Glob` + `Read` for navigation. The module map above and MEMORY.md provide sufficient context for this codebase's scale (~15 production modules).

## Docs (load on demand — do NOT load all at session start)
- Full spec (when changing spec'd behaviour): @docs/spec.md
- Architecture summary (load first):          @docs/architecture-summary.md
- Full architecture (when refactoring structure): @docs/architecture.md
- Sprint details:  @docs/sprints.md
- Smoke tests:     @docs/smoke-tests.md
- Session context: @.claude/session-notes.md  ← read at start of every session; update after major tasks
- Architecture review — active:   @docs/architecture-review.md        ← load when planning S20+
- Architecture review — done:     @docs/architecture-review-done.md   ← historical record
- Security research (fingerprint/proxy/auth): @docs/tidal-security-research.md
- Research agent prompt:           @research/research-agent.md

## Architecture Review Process

An architecture review is a full-codebase read by the architect agent to find bugs, correctness gaps,
tech debt, performance issues, and improvement opportunities across all production modules.

### Trigger phrases
- `"run architecture review"` / `"plan architecture review"` / `"start architecture review"`
- Recommended cadence: after every 3+ sprints merged to `main`

### Review files
| File | Purpose |
|------|---------|
| `docs/architecture-review.md` | Active findings — `backlog`, `planned`, `in-progress` (sorted by priority desc) |
| `docs/architecture-review-done.md` | Historical record — all `done` items (sorted by review batch, then priority desc) |

### Review process
1. Invoke the **architect agent** with scope: "full codebase architecture review of `tidal_dl/`"
2. Architect reads all production modules (not tests, docs, or config files)
3. Produces findings in the 13-column schema below; groups by proposed sprint
4. Append new findings to `docs/architecture-review.md` with `Status = backlog`
5. Assign a batch prefix letter (A, B, C, …) to all new items in the review
6. Update `Planned sprints` section in this file with the new sprint list

### Table schema — 14 columns
`Id | Problem | Description | Priority | Severity | Complexity | Effort | Type | Field | Files | Probability | Feasibility | Sprint | Status`

Full definitions for each column are at the bottom of both review files.

### Maintenance rules
- **On sprint start:** set `Status = in-progress` for all items in that sprint
- **On sprint complete & merged to `main`:** this is a **mandatory** post-merge step (pipeline step 6):
  1. Move resolved rows from `docs/architecture-review.md` → `docs/architecture-review-done.md`
  2. Set `Status = done` on moved rows
  3. Update the sprint plan table (strike through completed sprint)
  4. Update CLAUDE.md: test count + completed sprints list
  5. Update `docs/sprints.md`: add entry to overview table + detailed sprint section
  6. Commit the docs sync updates
- **New finding mid-sprint:** add to `docs/architecture-review.md` with `Status = backlog`;
  assign to a sprint during next planning session
- Both files stay sorted **priority descending** within each review batch
- Column definitions are duplicated at the bottom of each file (identical schema)
- **Cross-check rule:** any sprint that resolves architecture review items MUST update both review files — never commit sprint code without also updating the review status

## Security Research Process

### Trigger phrases
- `"run security research"` / `"update security research"`

### Process
1. Invoke a **general-purpose** agent with **Opus model**
2. Pass the full prompt from `research/research-agent.md`
3. Agent reads `docs/tidal-security-research.md`, searches the web for TIDAL API/anti-piracy changes,
   analyzes source code for new exposure, and updates the knowledge base
4. Agent returns a gap report summary to the main conversation
5. Recommended cadence: after every 2–3 sprints, or before any fingerprint/proxy/auth change

### Knowledge base
- `docs/tidal-security-research.md` — the living document (9 sections: threat model, credentials,
  fingerprinting, behavioral anti-detection, proxy, downloads, API, gaps, changelog)
- Consult **before** any feature or patch that touches auth, proxy, timing, headers, or download patterns

## Project-specific session notes
- `/compact` focus hint: `Focus on tidal_dl [module] and current acceptance criteria`
- Cost target: < $2/session
- **Memory sync**: after every sprint merge, check MEMORY.md against CLAUDE.md for drift
- **On-demand**: say "check memory consistency" or "check memory" to trigger an immediate comparison
- **Session notes rolling window**: keep only the last 5 entries in `session-notes.md`.
  When adding a 6th, drop the oldest entry — full sprint history lives in `docs/sprints.md`.

## Agent orchestration

### Agent confirmation rule
Before invoking a Task agent, present a one-line notice and wait for approval:

*"Invoking [AGENT NAME] agent to [brief purpose]. Proceed?"*

A "yes" triggers the agent immediately. Never invoke agents silently.

### When to use each agent

| Scope | Approach |
|-------|----------|
| 1–2 files, clear scope | Work directly in main conversation |
| 3+ files, or design decisions needed | Use agents (see pipeline below) |
| "Where is X implemented?" | `Explore` agent instead of grep + read loops |

All agents inherit these CLAUDE.md rules.
All git operations follow the global Permissions Model rules (commit/push/merge need approval).

### Standard sprint pipeline

1. **architect** — confirm → invoke → present plan → wait for user approval of the plan
2. **developer + tester** — confirm (both together) → invoke in parallel (same message)
3. **run unit tests** — `.venv/bin/pytest tests/ -v --tb=short`; fix failures before proceeding
4. **documentator** — confirm → invoke → integrate result
5. **commit / merge / push** — always in the main conversation, never inside an agent
6. **docs sync** — move resolved items from `architecture-review.md` → `architecture-review-done.md`; update sprint plan table; update CLAUDE.md test count + completed sprints list; add sprint entry to `docs/sprints.md` (overview table + detailed section)
7. **memory sync** — after merge, check MEMORY.md against CLAUDE.md and update if needed

### Agent models

Use **Opus** for design/research agents and **Sonnet** for implementation/docs agents.
The `architect` and `research` agents use **extended thinking**.

| Agent | Model | Thinking |
|-------|-------|----------|
| `architect` | opus | yes |
| `developer` | sonnet | no |
| `tester` | sonnet | no |
| `documentator` | sonnet | no |
| `Explore` | sonnet | no |
| `research` (general-purpose) | opus | yes |

### Agent context templates

| Agent | Pass in |
|-------|---------|
| `architect` | Sprint goal, affected module list from module map, constraints (no breaking changes etc.) |
| `developer` | Architect's approved plan + function signatures of files to change (full file content only if >50% of the file changes) |
| `tester` | Architect's approved plan + interfaces/contracts (not implementation) |
| `documentator` | Changed files list + session-notes update + module map changes + smoke test updates (`docs/smoke-tests-*.md`) when new user-facing behaviour is added |

### Error handling
- User rejects architect's plan → revise and re-invoke architect, or abandon the sprint
- Developer/tester agent fails or returns errors → diagnose and fix in main conversation, then re-invoke
- Tests fail after developer agent → fix in main conversation (not via agent re-invocation)

### Sprint trigger phrase
When the user says **"start sprint N"** or **"plan sprint N"**:
- *"Invoking architect agent to plan Sprint N. Proceed?"*
- On yes → invoke `Task(architect)` with sprint goal + relevant file list + constraints
- Present the architect's output and wait for the user to approve the plan
- *"Invoking developer + tester agents in parallel. Proceed?"*
- On yes → invoke `Task(developer)` + `Task(tester)` in the same message
- Integrate results → *"Invoking documentator agent. Proceed?"*
- On yes → invoke `Task(documentator)`
- Return to main conversation for commit/merge/push
