# Security Research Process

> Loaded on demand. Trigger: "run security research" / "update security research".
> Recommended cadence: after every 2-3 sprints, or before any fingerprint/proxy/auth change.

---

## Process

1. Invoke the **research** agent (Opus + extended thinking)
2. Pass the project-specific prompt from `research/research-agent.md`
3. Agent reads `docs/tidal-security-research.md`, searches the web, analyzes source code, and updates the knowledge base
4. Agent returns a gap report summary to the main conversation

---

## Knowledge Base

`docs/tidal-security-research.md` — the living document (10 sections):
1. Threat model
2. Credentials
3. Fingerprinting
4. Behavioral anti-detection
5. Proxy
6. Downloads
7. API
8. Gaps
9. Changelog
10. Family & multi-account risk analysis

**Consult before** any feature or patch that touches auth, proxy, timing, headers, or download patterns.

---

## Key Source Files for Analysis

| File | Security surface |
|------|-----------------|
| `tidal_dl/sessions/fingerprint.py` | Device fingerprint headers |
| `tidal_dl/sessions/http.py` | TLS fingerprint adapter, make_qobuz_session() |
| `tidal_dl/sessions/fingerprint_registry.py` | 13 fingerprint vectors |
| `tidal_dl/sessions/builder.py` | Session construction with fingerprint |
| `tidal_dl/sessions/pool.py` | Dual session management, thread-safe token ops |
| `tidal_dl/utils/timing.py` | Anti-detection jitter and timing |
| `tidal_dl/auth/token_store.py` | Token refresh randomization, periodic re-login |
| `tidal_dl/auth/credential_store.py` | Unified credential store, proxy mismatch detection |
| `tidal_dl/proxy/strategy.py` | Single-identity proxy, IP leak prevention |
| `tidal_dl/download/segments.py` | Concurrent segment download, proxy inheritance |
| `tidal_dl/download/governor.py` | Token bucket rate limiter, adaptive capacity |
| `tidal_dl/events/sender.py` | Playback event reporting |
| `tidal_dl/providers/qobuz.py` | Qobuz API client, signed requests |
| `tidal_dl/credentials.py.example` | Credential inventory and rotation order |

---

## Web Intelligence Scope

### Official / Primary
- TIDAL API documentation and changelogs
- TIDAL app store release notes (Android TV, mobile — version changes, permissions)
- Qobuz API and terms of service changes
- Widevine / PlayReady / FairPlay DRM announcements

### Technical / Security Community
- GitHub: `tamland/python-tidal` (tidalapi) issues, PRs, commits
- GitHub: `streamrip`, `orpheusdl`, `tiddl`, `lucida` — active projects and DMCA patterns
- GitHub: DMCA takedowns repo (`github/dmca`) — music downloader patterns
- TLS fingerprinting: JA3/JA4 signatures, HTTP/2 fingerprint research
- Anti-bot vendors: DataDome, Akamai, Cloudflare blog posts
- Proxy detection: ASN blacklists, residential IP scoring, WebRTC leak research
- okhttp fingerprint analysis (TIDAL uses okhttp 4.9.x)

### Community / OSINT
- Reddit: r/ripmedia, r/musichoarder, r/tidal, r/selfhosted, r/datahoarder
- Hydra/Orpheus/RED tracker forums (public channels)
- Hacker News: streaming DRM, music piracy enforcement
- Archive.org / Wayback Machine for removed tools/docs

### Legal / Compliance
- DMCA actions against music downloaders (tidal-dl-ng DMCA'd — monitor pattern)
- TIDAL terms of service updates
- API rate limit and usage policy changes
- RIAA / IFPI enforcement trends

### Academic / Research
- Traffic analysis and device fingerprinting papers
- Behavioral biometrics for bot detection
- DRM circumvention detection studies
