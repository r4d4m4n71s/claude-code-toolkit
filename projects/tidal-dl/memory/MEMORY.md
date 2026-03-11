# tidal-dl Project Memory

## Topic Files
- `l1-plan.md` — L1 module reorganization plan (5 sprints: S49-S53)
- `sprint-details.md` — per-sprint notes for S39-S48
- Plan doc: `docs/pipeline-decomposition-plan.md` — pipeline.py refactor plan

## Environment
- Python 3.13 (system), uv for venv management
- Run tests: `.venv/bin/pytest tests/ -v --tb=short`
- Install: `uv venv && uv pip install -e ".[dev]"`
- `Quality` is at `tidalapi.Quality` (NOT `tidalapi.session.Quality`) in tidalapi 0.8.11

## Sprint 4 Key Fix
- mutagen `MP4FreeForm.FORMAT_UTF8` does NOT exist — correct constant is `MP4FreeForm.FORMAT_TEXT`

## Proxy Architecture (IProxy plugin system)
- **IProxy ABC** in `tidal_dl/proxy/iproxy.py`: 4 methods (`get_proxies`, `get_proxy`, `is_available`, `renew`)
- **ProxyInfo** frozen dataclass: `url`, `country`, `location`, `session_id`
- **Entry point discovery**: `tidal_dl.proxy_provider` group via `importlib.metadata.entry_points()`
- **proxy-st** implements IProxy as `Provider` class, registered via pyproject.toml entry point
- **ProxyStrategy** wraps IProxy provider; `renew()` delegates to provider
- **Proxy renewal on failure**: `ProxyDownError` → `strategy.renew()` → `pool.reapply_proxy()` → retry
- **Config**: `proxy_provider: str` on ProjectConfig (entry point name, not URL)
- **ProxyStore deleted** — only `mask_proxy_url()` + `describe_connection()` kept in store.py
- **Old 3-way resolution removed** — no more `proxy_url` field, `ProxyConfig`, or `_VALID_PROXY_SCHEMES`
- When no proxy configured: leave `proxies` untouched to preserve OS env proxies

## Key Architecture Notes
- **Unified credential store**: `~/.config/tidal-dl/credentials.json` — single file for all TIDAL profiles + Qobuz tokens. `UnifiedCredentialStore` singleton, thread-safe, atomic writes (same-dir temp + `os.replace`), chmod 0o600. Auto-migrates from old scattered `{cred}_{location}_{profile}.json` files on first read.
- **TokenStore** no longer takes `location` param — `token_path_for()` removed entirely. Delegates to `UnifiedCredentialStore`.
- **Proxy mismatch detection** in `build_pool()`: compares stored `proxy_profile` against `provider.get_mapped_profile_name()` — mismatch clears tokens for re-login.
- **IProxy.get_mapped_profile_name()**: concrete method (not abstract) with default `return None`. proxy-st delegates to `_resolve_profile()`.
- **Test isolation**: `conftest.py` has `_isolate_credential_store` fixture that redirects singleton to `tmp_path` and patches `__init__` default. Prevents temp file leaks to real config dir.
- 8 credentials total: 4 normal + 4 atmos
- Events module (S25+S26): 3 events per track, off by default (lean tier)
- `sessionType: "PLAYBACK"` (not DOWNLOAD) — intentional
- EventSender: dedicated session, `token_getter` callable, try/finally for abort events
- New deps (S22): `curl-cffi>=0.9.0`, `curl-adapter>=1.2.0` for TLS/HTTP2 fingerprint

## TIDAL API Region & Quality (updated 2026-03-09)
- `GET /sessions` returns `countryCode` based on **account registration country**, NOT proxy IP
- `countryCode` is sent with every API request (tidalapi `request.py:76`) — determines catalog region
- A US proxy does NOT unlock HI_RES_LOSSLESS for a CO-registered account — catalog region is account-bound
- Proxy value is IP privacy/anti-detection only, not region-switching
- To get US catalog quality: need a US-registered account
- **API `audioQuality` is unreliable** — reports `LOSSLESS` for genuine HI_RES_LOSSLESS (24-bit/192kHz) streams
- Actual audio quality is determined by stream properties (`bit_depth` + `sample_rate`), not the API label

## TIDAL API Metadata Gotchas
- `session.track(id)` returns **stub album** — missing num_tracks, release_date, upc, copyright
- `album.tracks()` returns tracks with **full album** data
- `track.artist_roles` is **always None** — use `tracks/{id}/contributors` instead
- GENRE: **not in API** — resolved via MusicBrainz ISRC lookup (S40)
- MagicMock gotcha: `getattr(mock, "field", None)` returns MagicMock (truthy!) — use `isinstance()` guards

## Key Design Decisions
- **Pipeline decomposition (done)**: `pipeline.py` 1538→461 lines (-70%). 4 new modules: `batch_setup.py` (196, BatchContext), `item_processor.py` (559, per-item logic), `retry.py` (249, retry + exception dispatch), `track.py` (372, _download_track). ~210 test patches updated. pytest-xdist added (8 workers, 18.8s→6.1s)
- **Governor (S32)**: token bucket, 3 presets, adaptive margin, enabled by default (aggressive via lean tier)
- **Collection (S33)**: fetch all favorites, album cache pre-seeding, state persistence, dedup by (type, id)
- **Stealth tiers**: lean/balanced/full bundle events, governor, noise, timing. Resolution: explicit > stealth > parent > default
- **Cleanup command**: scans for temp files, clears collection state, optional governor/report reset
- **Library sync (S44)**: SyncRateLimiter 30/hr cap 50, additive/mirror, write guard, dual pools
- **Permissions (S45)**: 4 values, CLI guard, pipeline filtering (SKIPPED_VIDEO/SKIPPED_TRACK)
- **Batch playlist (S45)**: ~50x faster via playlist upsert, jitter removed from library_sync
- **Stream-based quality detection**: `derive_stream_quality()` in `quality.py` uses `stream.bit_depth` + `stream.sample_rate` as ground truth (API `audioQuality` is unreliable). Two-pass quality floor: step 5b pre-check allows LOSSLESS through when floor is HI_RES_LOSSLESS; post-stream check uses real values. `TIDAL_QUALITY` tag reflects actual stream quality
- **retag --fix-quality**: Done. `write_quality_tag()` + `_retag_quality()` in `retag.py`, `SUPPORTED_TAGS` exported, `--fix-quality` CLI flag
- **Multi-provider (P1-P3)**: `DownloadProvider` Protocol in `providers/base.py`, `StreamInfo`/`QualityInfo` frozen dataclasses, `TidalProvider` adapter, `QobuzProvider` (ISRC cross-lookup + signed file URL), `SourceResolver` (priority/best-quality + ISRC quality cache). P2 wired: pipeline uses SourceResolver, `_download_direct()` for Qobuz single-GET, `ProviderError` cause unwrapping in retry. P3 hardened: `make_qobuz_session()` factory (TLS+proxy+UA rotation), `PROVIDER_FALLBACK` event, direct download progress, 13 fingerprint vectors. 2590 tests (after credential store)

## Security Research Status (updated 2026-03-06)
- B2 (events): done (S25+S26). B4 (x-tidal-token): closed
- G15 (download_statistics): Medium. G16 (sessionType): closed intentional
- G20 (DataDome expansion): High. G21 (v2 API genre): closed, MusicBrainz instead
- Section 10 added: family & multi-account risk analysis
- Key: tidal-dl-ng DMCA'd, tiddl active with zero events, Widevine L1 existential risk

## Git Conventions
- Feature branches for code sprints, direct to `main` for docs/config
- Branch: `feat/<scope>` or `sprint/s<N>`. Tag: `git tag sN-complete`
- Commit: `feat(scope): message`. Scopes match module names

## Architecture Review
- All batches (A through N) complete. B8/B10/B11 closed (future-monitoring). No active backlog.
- L1 (S49-S53) + S54/Batch N (all 18 items) done. IProxy refactor done. Q1 Qobuz done. P1-P3 multi-provider done. Pipeline decomposition done. Unified credential store done. 2590 tests on `main`.
- F13 cover art: `fetch_cover` public alias, `tag()` accepts `cover_bytes`
- F20 video proxy: `_ProxyError` captured at import time

## S54 Public API Changes (Batch N)
- `catalog/resolver.py`: `parse_url()` (was `_parse_url`) — now public
- `config.py`: `ProjectConfig.active_name` property (was `_active_name`) — use this everywhere
- `sessions/pool.py`: `SessionPool.close()` — call in cleanup; `TidalSession.__exit__` does this automatically
- `intents.py`: `safety_order() -> list[str]` (was `_SAFETY_ORDER`) — now public
- `config.py`: `CONFIG_DIR` exported — import from here; `logger.py` has private copy to avoid circular import

## Qobuz Integration (Q1 — Phase 1 catalog-only)
- **Credential extraction**: `auth/qobuz_auth.py` — scrapes bundle.js from Qobuz web player for app_id + app_secret
- **Bundle extraction gotcha**: timezone regex needs `re.IGNORECASE` + `.lower()` on dict keys (bundle uses `"Europe/London"`, seeds use `"london"`)
- **QobuzClient**: `providers/qobuz.py` — rate-limited (1 req/sec), `search_by_isrc()`, `get_track()`, `_sign_request()` (Phase 2)
- **Quality check**: `download/quality.py` `check_qobuz_quality()` — ISRC lookup, kHz↔Hz conversion, per-batch cache
- **Pipeline integration**: lazy QobuzClient init in `download_items()`, post-download comparison, `QUALITY_AVAILABLE_ELSEWHERE` report event
- **Config**: `qobuz_quality_check: bool = False` on ProfileConfig
- **Credential cache**: now in `credentials.json` (unified store), was `qobuz_app.json`
- **Smoke tests**: `docs/smoke-tests-qobuz.md` — 10/17 passing (Phases 1-3 automated, Phase 4-5 need proxy download)
- **Segment progress**: `on_segment` callback in `download_segments()`, `print_segment_progress()` with `\r` overwrite
- **Genre helpers**: `metadata/qobuz_helpers.py` — `format_qobuz_genres()` for hierarchical genre flattening

## Smoke Tests
- 30 sections (0-29) in `docs/smoke-tests.md`
- **Suite A: ALL PASS** — §0-29 complete across 3 runs (2026-02-28, 2026-03-01, 2026-03-05, 2026-03-06)
- Bug found & fixed: `_cmd_info` unhandled `ObjectNotFound` — catch added in cli.py
- Atmos fixture: track 134788282 (The Weeknd — Blinding Lights, DOLBY_ATMOS). Note: LOW quality in CO region
- Proxy note: `_city-manizales` caused timeouts 2026-03-06 — use `_country-co` without city

## L1 Complete (S49-S53)
- L1a (S49): 9 module moves into domain packages
- L1b (S50): `tidal_dl/api/` (TidalSession context manager) + `tidal_dl/exceptions.py`
- L1c (S51): Intent system — 6 intents, 5-layer resolution
- L1d (S52): Wizard: choose → estimate → recommend → confirm
- L1e (S53): Documentation
- `build_pool()` lives in `api/session.py` (moved from `pipeline.py` in L1b)
