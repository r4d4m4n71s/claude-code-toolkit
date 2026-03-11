# tidal-dl Project Memory

## Environment
- Python 3.13 (system), uv for venv management
- Run tests: `.venv/bin/pytest tests/ -v --tb=short`
- Install: `uv venv && uv pip install -e ".[dev]"`

## Library Gotchas
- `Quality` is at `tidalapi.Quality` (NOT `tidalapi.session.Quality`) in tidalapi 0.8.11
- mutagen `MP4FreeForm.FORMAT_UTF8` does NOT exist — correct constant is `MP4FreeForm.FORMAT_TEXT`
- MagicMock gotcha: `getattr(mock, "field", None)` returns MagicMock (truthy!) — use `isinstance()` guards
- `curl-cffi>=0.9.0`, `curl-adapter>=1.2.0` for TLS/HTTP2 fingerprint

## TIDAL API Gotchas
- `session.track(id)` returns **stub album** — missing num_tracks, release_date, upc, copyright
- `album.tracks()` returns tracks with **full album** data
- `track.artist_roles` is **always None** — use `tracks/{id}/contributors` instead
- GENRE: **not in API** — resolved via MusicBrainz ISRC lookup
- **API `audioQuality` is unreliable** — reports `LOSSLESS` for genuine HI_RES_LOSSLESS (24-bit/192kHz) streams; use `bit_depth` + `sample_rate` instead
- `countryCode` is **account registration country**, NOT proxy IP — proxy is for IP privacy only

## Proxy Architecture
- **IProxy ABC** in `proxy/iproxy.py`: 4 methods (`get_proxies`, `get_proxy`, `is_available`, `renew`)
- **proxy-st** implements IProxy, registered via `tidal_dl.proxy_provider` entry point
- **Config**: `proxy_provider: str` on ProjectConfig (entry point name, not URL)
- When no proxy configured: leave `proxies` untouched to preserve OS env proxies
- Proxy mismatch detection in `build_pool()`: compares stored `proxy_profile` against provider

## Credential Store
- Unified `~/.config/tidal-dl/credentials.json` — all TIDAL + Qobuz tokens
- `UnifiedCredentialStore` singleton, thread-safe, atomic writes, chmod 0o600
- Auto-migrates from old scattered `{cred}_{location}_{profile}.json` files
- 8 TIDAL credentials: 4 normal + 4 atmos
- Test isolation: `conftest.py` `_isolate_credential_store` fixture redirects singleton to `tmp_path`

## Qobuz Gotchas
- Bundle extraction: timezone regex needs `re.IGNORECASE` + `.lower()` on dict keys
- `QobuzClient` rate-limited (1 req/sec), `_sign_request()` for signed URLs
- Credential cache now in unified `credentials.json`

## Events
- `sessionType: "PLAYBACK"` (not DOWNLOAD) — intentional
- Events off by default (lean tier)

## Smoke Tests
- Atmos fixture: track 134788282 (The Weeknd — Blinding Lights, DOLBY_ATMOS). LOW quality in CO region
- Proxy: `_city-manizales` caused timeouts — use `_country-co` without city
