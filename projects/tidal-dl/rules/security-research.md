# Security Research Process

> Loaded on demand. Trigger: "run security research" / "update security research".
> Recommended cadence: after every 2-3 sprints, or before any fingerprint/proxy/auth change.

---

## Process

1. Invoke a **general-purpose** agent with **Opus model** + extended thinking
2. Pass the full prompt from `research/research-agent.md`
3. Agent reads `docs/tidal-security-research.md`, searches the web for TIDAL API/anti-piracy changes,
   analyzes source code for new exposure, and updates the knowledge base
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
