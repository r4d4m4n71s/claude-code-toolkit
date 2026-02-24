# Claude Code Project Toolkit

Opinionated scaffolding for Claude Code projects: global rules, multi-agent team, per-project templates — one Python CLI does everything.

## What's Included

```
claude-code-toolkit/
├── claude-init.py               ← Main script (Python, Rich + Questionary UI)
├── claude-init.sh               ← Legacy bash script (kept for reference)
├── CLAUDE.global-template.md    ← Global rules template → ~/.claude/CLAUDE.md
├── agents/
│   ├── architect.md             ← Orchestrator (Opus)
│   ├── developer.md             ← Implementation (Sonnet)
│   ├── tester.md                ← Test suite (Sonnet)
│   └── documentator.md          ← Documentation (Haiku)
└── templates/
    ├── CLAUDE.project-template.md   ← Per-project CLAUDE.md
    ├── CONVENTIONS.md               ← Git/code conventions
    ├── session-notes.md             ← Session log
    ├── settings.json                ← Shared tool permissions (commit this)
    ├── settings.local.json          ← Personal env vars (git-ignored)
    └── .mcp.json.template           ← Qdrant MCP server config
```

## Requirements

- Python 3.10+
- `rich` and `questionary` — installed into a local venv

## Install (once)

```bash
git clone <repo-url> claude-code-toolkit
cd claude-code-toolkit

# Create venv and install dependencies
python3 -m venv .venv
.venv/bin/pip install rich questionary

# Install global config into ~/.claude/
.venv/bin/python claude-init.py init-globals
```

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export PATH="$HOME/.claude/bin:$PATH"
```

After that, `claude-init` is available globally — no venv activation needed.

## Use (every new project)

```bash
cd ~/my-new-project
claude-init init-project
```

Creates:

```
my-new-project/
├── .claude/
│   ├── settings.json        # Shared tool permissions (commit this)
│   └── settings.local.json  # Personal env vars (git-ignored)
├── .mcp.json                # MCP server config (if configured)
├── .gitignore               # Adds .claude/settings.local.json entry
├── CLAUDE.md                # Project context (fill in)
├── CONVENTIONS.md           # Git/code conventions
└── docs/
    └── session-notes.md     # Session log
```

Existing files are **never silently overwritten**. When conflicts are found, the script prompts:

```
  ⚠  3 file(s) already exist:
      CLAUDE.md
      CONVENTIONS.md
      .claude/settings.json

? What would you like to do?
❯ Overwrite all  (originals backed up)
  Skip all existing
  Decide per file
  Quit
```

Backups are saved to `.claude/backups/YYYYMMDD-HHMMSS/` before any overwrite.

## Commands

### `init-globals` — install into `~/.claude/`

```bash
claude-init init-globals                    # auto-detect toolkit directory
claude-init init-globals --from /path/to/toolkit
claude-init init-globals --force            # overwrite all without prompting
```

Installs: `CLAUDE.md`, four agent files, six template files, and the `claude-init`
binary itself into `~/.claude/`. The binary is always updated on each run.

### `init-project` — scaffold a project

```bash
claude-init init-project                              # project name = directory name
claude-init init-project --name myapp
claude-init init-project --name myapp --collection myapp-search   # configure Qdrant
claude-init init-project --no-mcp                    # skip .mcp.json
claude-init init-project --force                     # overwrite all without prompting
```

## Agent Team

```
User request
    │
    ▼
Architect (Opus) ── plan ──► Developer (Sonnet) ── code
    │                              │
    │                              ▼
    │◄── review ◄──────── Tester (Sonnet) ── tests
    │
    ▼
Documentator (Haiku) ── docs
    │
    ▼
Final delivery
```

Invoke via Claude Code: `@architect <your request>`

## Customization

- **Project-specific agents:** add `.md` files to `<project>/.claude/agents/`
- **Slash commands:** create files in `<project>/.claude/commands/`
- **Permissions:** edit `.claude/settings.json` allow/deny lists to match your stack
- **Update agents globally:** edit `~/.claude/agents/*.md` — changes apply to all projects
- **Re-run global install:** `claude-init init-globals --force` (backs up originals)
