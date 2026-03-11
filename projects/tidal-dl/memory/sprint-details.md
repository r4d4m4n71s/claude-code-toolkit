# Sprint Details (S39-S48)

Detailed per-sprint notes moved from MEMORY.md to keep it under 200 lines.
For full sprint history see `docs/sprints.md`.

## S39 Additions (2026-03-04)
- **Logger**: dated filenames (`tidal-dl-YYYY-MM-DD.log`), millisecond timestamps
- **Config**: `playlist_dir` field; fresh config has most fields commented out
- **CLI flags**: `--output-dir`/`-o`, `--no-governor` on `dl` and `collection`
- **ISRC cache**: shared across `--file` URLs via `download()` → `download_items()` params
- **Proxy**: resume hint on ProxyDownError; HEAD timeout 10→20s
- **Quality**: one-time region quality warning on first quality skip

## S40 MusicBrainz Genre (2026-03-04)
- `tidal_dl/musicbrainz.py` — ISRC→MBID→recording→genres via MusicBrainz API
- Rate limit: 1.1s timestamp guard, no separate rate limiter
- Genre cascade: recording genres (full) + artist genres (half weight), top 5, title-case
- Caches: `isrc_mbid_cache` + `recording_cache` as dict params (not global state)
- Config: `genre_lookup: bool = True`
- Tagger: FLAC multi-value GENRE, M4A semicolon-joined `\xa9gen`
- v2 API genre (G21) rejected — MusicBrainz = zero TIDAL exposure

## S41 Info + Retag (2026-03-04)
- `tidal_dl/info.py` — 5 dataclasses, 5 fetch functions, 3 formatters
- `tidal_dl/retag.py` — Phase 1 genre-only backfill via MusicBrainz, 3-level cache
- K1 Phase 1 done. 1341 tests

## S42 Library Stats + Export (2026-03-04)
- `tidal_dl/library.py` — scan, export CSV/JSON, stats aggregation
- CLI: `status --library`, `export` subcommand
- L1 module reorganization added to backlog. 1437 tests

## S43 Resolve Command + Per-Profile Proxy (2026-03-04)
- `tidal-dl resolve` — expand URLs into track/video URLs
- Per-profile `proxy_url` with 3-way resolution. 1513 tests

## S44 Library Sync (2026-03-04)
- `tidal_dl/library_sync.py` — cross-account sync (snapshot, diff, apply)
- SyncRateLimiter (30/hr, cap 50), additive/mirror modes
- Write guard, dry-run, audit log. 1607 tests

## S45 Permissions + Login Safety + Batch Sync (2026-03-05)
- `ProfileConfig.permissions` (4 values), CLI guard, pipeline filtering
- Login warning box (proxy hygiene)
- Batch playlist strategy (~50x faster), playlist upsert. 1670 tests

## S46+S47 Library-Sync Perf + Type Safety (2026-03-05)
- Batch favorites ~20x faster, shared tag helpers
- SKIPPED_TRACK EventType, governor public property. 1809 tests

## S48 Remaining Batch M (2026-03-05)
- MB thread-safe rate limit, governor zero-margin guard
- .dec extension fix, .lrc cleanup on failure. 1824 tests

## S49/L1a Module Domain Reorganization (2026-03-06)
- 9 modules moved into domain subpackages (commands/, download/, metadata/, sessions/)
- No backward-compat shims — old paths removed entirely
- 83 new layout tests, 223 patch targets updated. 1907 tests

## S50/L1b API Layer + Exception Consolidation (2026-03-06)
- `tidal_dl/exceptions.py`: TidalDLError base + 9 consolidated subclasses
- `tidal_dl/api/session.py`: TidalSession context manager + build_pool() moved from pipeline
- `tidal_dl/api/facade.py`: TidalAPI stateless facade
- Old exception definitions removed from 7 modules, no shims
- `_exc` alias pattern: old modules reference via `_exc.ConfigError(...)`. 2000 tests

## S51/L1c Intent System (2026-03-06)
- `tidal_dl/intents.py`: 6 presets, INTENTS registry, safer_intent(), describe_intent(), intent_risk()
- `config.py`: `intent` field on ProfileConfig, 5-layer resolution (explicit > intent > stealth > parent > default)
- `cli.py`: `--intent` flag on dl/collection/library-sync, _apply_cli_overrides() updated
- library-sync now also has --stealth flag + _apply_cli_overrides() call. 2074 tests

## S52/L1d Wizard Enhancement (2026-03-06)
- `tidal_dl/commands/wizard.py`: interactive setup wizard (choose → estimate → recommend → confirm)
- IntentSummary/WizardResult dataclasses, input_fn/print_fn injection for testability
- cli.py: setup subparser --estimate/--recommend/--profile, _cmd_setup dispatch
- Estimation: intent → governor_preset → PRESETS[preset].tracks_per_hour. 2116 tests
