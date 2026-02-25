# Claude Code Toolkit

Opinionated context scaffolding for Claude Code — install global rules, agents, and per-project templates with a single bash script.

## Repository layout

```
claude-code-toolkit/
└── context/
    └── scrum_template/          ← Scrum / software-project flavour
        ├── init-global.sh       ← Installs global context  → ~/.claude/
        ├── init-project.sh      ← Installs project context → <project>/.claude/
        ├── global/
        │   ├── CLAUDE.md        ← Global rules (all projects)
        │   └── agents/
        │       ├── architect.md
        │       ├── developer.md
        │       ├── tester.md
        │       └── documentator.md
        └── project/
            ├── CLAUDE.md        ← Per-project rules template
            ├── CONVENTIONS.md   ← Git / code conventions
            ├── session-notes.md ← Session log
            ├── settings.json    ← Shared tool permissions (commit this)
            ├── settings.local.json  ← Personal env vars (git-ignored)
            └── .mcp.json.template   ← Qdrant MCP server config
```

## Setup — global context (once per machine)

Installs `CLAUDE.md` and the agent definitions into `~/.claude/`.

```bash
cd context/scrum_template
./init-global.sh
```

If files already exist, the script skips them and tells you how many were skipped.
Use `--force` to overwrite — existing files are backed up with a timestamp first:

```bash
./init-global.sh --force
```

## Setup — project context (once per project)

Installs all project files into `<project>/.claude/`.
`<project-name>` inside `CLAUDE.md` is automatically replaced with the actual folder name.

```bash
# from inside the project directory
/path/to/context/scrum_template/init-project.sh

# or pass the path explicitly
./init-project.sh /path/to/my-project

# overwrite existing files (backs them up first)
./init-project.sh /path/to/my-project --force
```

### What gets installed

| Source | Destination |
|--------|-------------|
| `project/CLAUDE.md` | `<project>/.claude/CLAUDE.md` (project-name substituted) |
| `project/CONVENTIONS.md` | `<project>/.claude/CONVENTIONS.md` |
| `project/session-notes.md` | `<project>/.claude/session-notes.md` |
| `project/settings.json` | `<project>/.claude/settings.json` |
| `project/settings.local.json` | `<project>/.claude/settings.local.json` |
| `project/.mcp.json.template` | `<project>/.claude/.mcp.json.template` |

> **Note:** `settings.local.json` contains personal env vars (API key, model overrides).
> Add it to `.gitignore` — never commit it.

## Adding a new template

1. Create `context/<template-name>/` with the same `global/` and `project/` structure.
2. Copy and adapt `init-global.sh` and `init-project.sh` from `scrum_template`.
3. That's it — no central registry to update.
