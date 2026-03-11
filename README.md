# Claude Code Configuration

Version-controlled Claude Code workflow configuration, SDLC rules, and project context files.

## Purpose

Track changes to Claude Code configuration files that live outside project repos:
- Global `CLAUDE.md` (applies to all projects)
- Per-project `CLAUDE.md`, rules, session notes, and memory files

## Structure

```
claude-config/
├── global/
│   └── CLAUDE.md                 ← ~/.claude/CLAUDE.md (global rules)
├── projects/
│   └── tidal-dl/
│       ├── CLAUDE.md             ← project root CLAUDE.md
│       ├── session-notes.md      ← .claude/session-notes.md
│       ├── rules/                ← on-demand workflow rules (loaded when needed)
│       │   ├── workflow.md           ← sprint pipeline, agent orchestration
│       │   ├── architecture-review.md ← review process, table schema
│       │   ├── commit-conventions.md  ← commit types, scopes, examples
│       │   └── security-research.md   ← research process, trigger phrases
│       └── memory/
│           └── MEMORY.md         ← auto-memory (gotchas, pitfalls, env setup)
└── README.md
```

## Workflow

1. Edit files here first
2. Commit changes with clear messages
3. Deploy: copy changed files to their installed locations
   - `global/CLAUDE.md` → `~/.claude/CLAUDE.md`
   - `projects/tidal-dl/CLAUDE.md` → `<tidal-dl>/.claude/CLAUDE.md`
   - etc.

## Deployment script

```bash
# Deploy global config
cp global/CLAUDE.md ~/.claude/CLAUDE.md

# Deploy tidal-dl project config
TIDAL_DL="/media/r4d4m4n71s/SOS/sw/programing/Tidal dl/tidal-dl"
cp projects/tidal-dl/CLAUDE.md "$TIDAL_DL/.claude/CLAUDE.md"
cp projects/tidal-dl/session-notes.md "$TIDAL_DL/.claude/session-notes.md"
```
