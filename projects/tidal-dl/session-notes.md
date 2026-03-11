# Session Notes

> Running log of sprint sessions. Append after every major task.
> Most recent entry first.

---

## 2026-03-11 — Unified Credential Store

**Branch:** `main` (merged from `feat/unified-credential-store`)

### Accomplished
| File/Area | Change |
|-----------|--------|
| `tidal_dl/auth/credential_store.py` | NEW — UnifiedCredentialStore singleton, TidalTokenData/TidalProfileData/QobuzData/CredentialFile dataclasses, thread-safe atomic writes, auto-migration from scattered files, JWT decode |
| `tidal_dl/auth/token_store.py` | Dropped `location` param, removed `token_path_for()` and `TOKEN_DIR`, delegates to UnifiedCredentialStore |
| `tidal_dl/auth/qobuz_auth.py` | QobuzCredentialStore + QobuzUserTokenStore delegate to UnifiedCredentialStore, Qobuz country_code + subscription_offer |
| `tidal_dl/api/session.py` | Proxy mismatch detection in `build_pool()`, `set_profile_metadata()` after pool creation |
| `tidal_dl/cli.py` | `_cmd_status()` reads from UnifiedCredentialStore, shows email/proxy_profile |
| `tidal_dl/proxy/iproxy.py` | Added concrete `get_mapped_profile_name()` to IProxy ABC |
| `tidal_dl/proxy/strategy.py` | Added `proxy_profile_name` property |
| `proxy-st/provider.py` | `get_mapped_profile_name()` delegates to `_resolve_profile()` (separate commit needed) |
| `tests/unit/test_credential_store.py` | NEW — 64 tests for unified store |
| `tests/conftest.py` | Added `_isolate_credential_store` fixture — redirects singleton to tmp_path, prevents temp file leaks |
| 10 test files | Patch path updates for new `get_token_status` signature and credential store constructors |
| `docs/tidal-security-research.md` | Qobuz API endpoint inventory (27 endpoints), TIDAL clients endpoint doc |
| `docs/reference.md` | Updated file locations + Qobuz credentials section |

**Test count:** 2590 tests, 0 failures.

### Current state
- Merged to `main`. Feature branch deleted.
- proxy-st `provider.py` committed on its `main`.
- MEMORY.md updated.

### Next steps
1. No active backlog.

---

## 2026-03-10 — P3 Qobuz fingerprint hardening + UX polish

**Branch:** `main`

### Accomplished
| File/Area | Change |
|-----------|--------|
| `sessions/http.py` | Added `make_qobuz_session()` factory (TLS + proxy + 5-UA rotation pool) |
| `auth/qobuz_auth.py` | Threaded `proxy_url` through all 4 HTTP functions |
| `providers/qobuz.py` | Removed hardcoded UA, QobuzClient uses `make_qobuz_session` fallback |
| `download/batch_setup.py` | Quality-check client gets pool session + proxy_url |
| `cli.py` | Login --qobuz resolves proxy from config |
| `utils/report.py` | Added `PROVIDER_FALLBACK` EventType |
| `download/pipeline.py` | Emits PROVIDER_FALLBACK for non-TIDAL providers |
| `download/track.py` | Provider attribution `[qobuz]` tag + `on_progress` in `_download_direct` |
| `utils/progress.py` | Added `print_download_progress()` |
| `sessions/fingerprint_registry.py` | Added 2 Qobuz vectors (11→13) |
| `providers/base.py` | Removed `Provider` ABC legacy stub |
| `providers/resolver.py` | Added ISRC quality cache for best-quality strategy |

**Test count:** 2526 tests, 0 failures.

### Current state
- P3 complete on `main`. All Qobuz HTTP now hardened (TLS fingerprint + proxy + UA rotation).

### Next steps
1. Qobuz smoke tests Q4/Q5 (need proxy download).
2. No active backlog.

---

## 2026-03-10 — Pipeline decomposition + test parallelization

**Branch:** `main` (merged from `feat/pipeline-decomposition`)

### Accomplished
| File/Area | Change |
|-----------|--------|
| `tidal_dl/download/pipeline.py` | 1538→461 lines (-70%), thin orchestrator only |
| `tidal_dl/download/batch_setup.py` | NEW — BatchContext dataclass, build_batch_context(), teardown_batch() |
| `tidal_dl/download/item_processor.py` | NEW — prepare_track(), post_download(), handle_video(), inter_track_delay() |
| `tidal_dl/download/retry.py` | NEW — retry_download_track() with exception dispatch |
| `tidal_dl/download/track.py` | Expanded — TrackDownloadResult, _download_track(), _download_direct() |
| `pyproject.toml` | Added pytest-xdist, default `-n 8` workers (18.8s→6.1s, 3x speedup) |

**Test count:** 2481 tests, 0 failures (6.1s parallel).

### Current state
- Pipeline decomposition complete and merged to `main`.

### Next steps
1. P2/P3 Qobuz work.

---

## 2026-03-10 — P1 Multi-provider protocol + test speedup

**Branch:** `main` (merged from `feat/multi-provider`)

### Accomplished
| File/Area | Change |
|-----------|--------|
| `tidal_dl/providers/base.py` | `StreamInfo`, `QualityInfo` frozen dataclasses + `DownloadProvider` Protocol |
| `tidal_dl/providers/tidal.py` | NEW — `TidalProvider` adapter wrapping SessionPool → StreamInfo |
| `tidal_dl/providers/resolver.py` | NEW — `SourceResolver` with `priority` and `best-quality` strategies |
| `tidal_dl/config.py` | Added `download_sources: list[str]` + `source_strategy: str` |

**Test count:** 2415 tests, 0 failures.

### Current state
- P1 merged to `main`. Multi-provider foundation in place.

### Next steps
1. P2: QobuzProvider + pipeline wiring.

---

## 2026-03-10 — Retag --fix-quality + B8/B10/B11 closure

**Branch:** `main` (merged from `feat/retag-fix-quality`)

### Accomplished
| File/Area | Change |
|-----------|--------|
| `tidal_dl/commands/retag.py` | Added `write_quality_tag()`, `_retag_quality()`, `SUPPORTED_TAGS` export |
| `tidal_dl/cli.py` | Added `--fix-quality` flag |
| `docs/architecture-review*.md` | B8/B10/B11 closed as future-monitoring |

**Test count:** 2344 tests, 0 failures.

### Current state
- Merged to `main`. Feature branch deleted.

### Next steps
1. Pipeline integration smoke tests (Q4-A through Q4-E) — need proxy download.
