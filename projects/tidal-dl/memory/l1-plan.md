# L1 Module Domain Reorganization — Plan Summary

Full plan: `docs/l1-plan.md`

## Sprint Breakdown
- **L1a (S49)**: DONE — 9 modules moved into domain packages, no shims, 1907 tests.
- **L1b (S50)**: DONE — exceptions.py (TidalDLError + 9 subclasses), api/session.py (TidalSession + build_pool), api/facade.py (TidalAPI), 2000 tests.
- **L1c (S51)**: DONE — intents.py (6 presets, INTENTS registry, safer_intent, 5-layer resolution), --intent CLI, 2074 tests.
- **L1d (S52)**: DONE — commands/wizard.py (interactive setup, estimation, recommendation), --estimate/--recommend/--profile, 2116 tests.
- **L1e (S53)**: DONE — docs updated (architecture-summary, user-guide, reference), sessions/exceptions.py + credentials.example.py removed, 2115 tests.

## Module Moves (L1a)
| Module | From | To |
|--------|------|----|
| `fingerprint_registry.py` | `tidal_dl/` | `sessions/` |
| `playlist.py` | `tidal_dl/` | `metadata/` |
| `musicbrainz.py` | `tidal_dl/` | `metadata/` |
| `governor.py` | `tidal_dl/` | `download/` |
| `retag.py` | `tidal_dl/` | `commands/` |
| `info.py` | `tidal_dl/` | `commands/` |
| `library.py` | `tidal_dl/` | `commands/` |
| `library_sync.py` | `tidal_dl/` | `commands/` |
| `collection.py` | `tidal_dl/` | `commands/` |

No backward-compat shims — old paths are gone entirely.

## Key Decisions
1. **Session**: explicit context manager (`with TidalSession(...) as s:`)
2. **Config**: both TOML + programmatic, converging on `ProfileConfig`
3. **Errors**: consolidate in L1b — new `TidalDLError` base class
4. **Intents**: `download-fast`, `download-safe`, `download-stealth`, `query-only`, `library-sync`, `collection-safe`
5. **Resolution order**: explicit TOML > intent > stealth tier > parent > dataclass default
6. **build_pool() moves**: `pipeline.py` → `api/session.py`

## Stays Put
- `cli.py` (758 test refs, entry point)
- `config.py` (core infra)
- `logger.py` (shortest path)
- `credentials.py` (security contract)
