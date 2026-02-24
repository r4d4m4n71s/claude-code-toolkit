#!/usr/bin/env bash
# claude-init — Claude Code project toolkit
#
# Purpose:
#   Bash predecessor to claude-init.py — kept for reference.
#   The canonical implementation is claude-init.py (Python, Rich + Questionary UI).
#
#   Two commands:
#     setup        Install global Claude Code config into ~/.claude/
#                  (agents, templates, CLAUDE.md, self as claude-init binary)
#     (default)    Scaffold Claude Code files in the current project directory
#
# Install:
#   mkdir -p ~/.claude/bin && cp claude-init.sh ~/.claude/bin/claude-init && chmod +x ~/.claude/bin/claude-init
#   Add to ~/.bashrc or ~/.zshrc: export PATH="$HOME/.claude/bin:$PATH"
#
# Usage:
#   claude-init setup              Install global agents, templates, and rules
#   claude-init [options]          Scaffold project files in current directory

set -euo pipefail

# --- Constants ---
CLAUDE_DIR="$HOME/.claude"
AGENTS_DIR="$CLAUDE_DIR/agents"
TEMPLATES_DIR="$CLAUDE_DIR/templates"
BIN_DIR="$CLAUDE_DIR/bin"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

log_ok()      { echo -e "  ${GREEN}✓${NC} $1"; }
log_skip()    { echo -e "  ${YELLOW}⊘${NC} $1 ${YELLOW}(exists)${NC}"; }
log_updated() { echo -e "  ${GREEN}✓${NC} $1 ${BLUE}(updated, backup saved)${NC}"; }
log_warn()    { echo -e "  ${YELLOW}⊘${NC} $1"; }

# --- Helper: copy with skip/backup logic ---
safe_copy() {
    local src="$1" dest="$2" label="$3" force="${4:-false}"

    if [[ -f "$dest" ]]; then
        if [[ "$force" != true ]]; then
            log_skip "$label"
            return
        fi
        local backup_dir="$CLAUDE_DIR/backups/$(date +%Y%m%d-%H%M%S)"
        mkdir -p "$backup_dir"
        cp "$dest" "$backup_dir/$(basename "$dest")"
        cp "$src" "$dest"
        log_updated "$label"
    else
        mkdir -p "$(dirname "$dest")"
        cp "$src" "$dest"
        log_ok "$label"
    fi
}

# ╔═══════════════════════════════════════════════════╗
# ║  SETUP — one-time global install                  ║
# ╚═══════════════════════════════════════════════════╝

do_setup() {
    local force=false
    local source_dir=""

    while [[ $# -gt 0 ]]; do
        case $1 in
            --from)   source_dir="$2"; shift 2 ;;
            --force)  force=true; shift ;;
            -h|--help) setup_help; exit 0 ;;
            *)        echo "Unknown option: $1"; setup_help; exit 1 ;;
        esac
    done

    # Determine source: explicit --from, or detect toolkit directory
    if [[ -z "$source_dir" ]]; then
        # Check if running from inside the toolkit
        local script_dir
        script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        if [[ -f "$script_dir/CLAUDE.md" && -d "$script_dir/agents" ]]; then
            source_dir="$script_dir"
        else
            echo -e "${RED}Error:${NC} Cannot find toolkit files."
            echo "Run from inside the toolkit directory, or use: claude-init setup --from /path/to/toolkit"
            exit 1
        fi
    fi

    echo ""
    echo -e "${BOLD}Claude Code — Global Setup${NC}"
    echo ""

    mkdir -p "$AGENTS_DIR" "$TEMPLATES_DIR" "$BIN_DIR"

    # Global CLAUDE.md
    safe_copy "$source_dir/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md" "~/.claude/CLAUDE.md" "$force"

    # Agents
    for agent in architect developer tester documentator; do
        local src=""
        [[ -f "$source_dir/agents/$agent.md" ]] && src="$source_dir/agents/$agent.md"
        [[ -z "$src" && -f "$source_dir/$agent.md" ]] && src="$source_dir/$agent.md"
        if [[ -z "$src" ]]; then
            log_warn "$agent.md not found, skipping"
            continue
        fi
        safe_copy "$src" "$AGENTS_DIR/$agent.md" "~/.claude/agents/$agent.md" "$force"
    done

    # Templates
    local templates=( "CLAUDE.project-template.md" "CONVENTIONS.md" "session-notes.md"
                      "settings.json" "settings.local.json" ".mcp.json.template" )
    for file in "${templates[@]}"; do
        local src=""
        [[ -f "$source_dir/templates/$file" ]] && src="$source_dir/templates/$file"
        [[ -z "$src" && -f "$source_dir/$file" ]] && src="$source_dir/$file"
        if [[ -z "$src" ]]; then
            log_warn "$file not found, skipping"
            continue
        fi
        safe_copy "$src" "$TEMPLATES_DIR/$file" "~/.claude/templates/$file" "$force"
    done

    # Self-install the script
    local self_path="${BASH_SOURCE[0]}"
    if [[ -f "$self_path" ]]; then
        cp "$self_path" "$BIN_DIR/claude-init"
        chmod +x "$BIN_DIR/claude-init"
        log_ok "~/.claude/bin/claude-init"
    fi

    echo ""
    if echo "$PATH" | grep -q "$BIN_DIR"; then
        echo -e "${GREEN}✓${NC} ~/.claude/bin is already in PATH"
    else
        echo "Add to your shell profile (~/.bashrc or ~/.zshrc):"
        echo ""
        echo "  export PATH=\"\$HOME/.claude/bin:\$PATH\""
    fi
    echo ""
    echo "Done. Now run ${BOLD}claude-init${NC} inside any project directory."
    echo ""
}

setup_help() {
    cat <<EOF
Usage: claude-init setup [OPTIONS]

One-time install of global agents, templates, and rules into ~/.claude/.

Options:
  --from DIR    Path to toolkit directory (auto-detected if running from it)
  --force       Overwrite existing files (originals backed up to ~/.claude/backups/)
  -h, --help    Show this help

Installs:
  ~/.claude/CLAUDE.md                Global rules
  ~/.claude/agents/*.md              Architect, developer, tester, documentator
  ~/.claude/templates/*              Project scaffolding templates
  ~/.claude/bin/claude-init          This script
EOF
}

# ╔═══════════════════════════════════════════════════╗
# ║  PROJECT — scaffold files in current directory     ║
# ╚═══════════════════════════════════════════════════╝

do_project() {
    local project_name="" collection_name="" no_mcp=false force=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --name)        project_name="$2"; shift 2 ;;
            --collection)  collection_name="$2"; shift 2 ;;
            --no-mcp)      no_mcp=true; shift ;;
            --force)       force=true; shift ;;
            -h|--help)     project_help; exit 0 ;;
            *)             echo "Unknown option: $1"; project_help; exit 1 ;;
        esac
    done

    project_name="${project_name:-$(basename "$(pwd)")}"

    # Verify templates exist
    if [[ ! -d "$TEMPLATES_DIR" ]]; then
        echo -e "${RED}Error:${NC} Templates not found at $TEMPLATES_DIR"
        echo "Run ${BOLD}claude-init setup${NC} first."
        exit 1
    fi

    echo ""
    echo -e "${BOLD}Claude Code — Project Init:${NC} ${project_name}"
    echo "Directory: $(pwd)"
    echo ""

    # CLAUDE.md — replace placeholder with project name
    if [[ -f "CLAUDE.md" ]] && [[ "$force" != true ]]; then
        log_skip "CLAUDE.md"
    else
        sed "s/<project-name>/${project_name}/g" "$TEMPLATES_DIR/CLAUDE.project-template.md" > "CLAUDE.md"
        log_ok "CLAUDE.md"
    fi

    # CONVENTIONS.md
    safe_copy "$TEMPLATES_DIR/CONVENTIONS.md" "CONVENTIONS.md" "CONVENTIONS.md" "$force"

    # docs/session-notes.md
    mkdir -p docs
    safe_copy "$TEMPLATES_DIR/session-notes.md" "docs/session-notes.md" "docs/session-notes.md" "$force"

    # .claude/settings.json
    mkdir -p .claude
    safe_copy "$TEMPLATES_DIR/settings.json" ".claude/settings.json" ".claude/settings.json" "$force"

    # .claude/settings.local.json
    safe_copy "$TEMPLATES_DIR/settings.local.json" ".claude/settings.local.json" ".claude/settings.local.json" "$force"

    # .mcp.json
    if [[ "$no_mcp" != true ]]; then
        if [[ -f ".mcp.json" ]] && [[ "$force" != true ]]; then
            log_skip ".mcp.json"
        else
            if [[ -n "$collection_name" ]]; then
                sed "s/your-collection-name/${collection_name}/g; s/project-search/${project_name}-search/g" \
                    "$TEMPLATES_DIR/.mcp.json.template" > ".mcp.json"
            else
                cp "$TEMPLATES_DIR/.mcp.json.template" ".mcp.json"
            fi
            log_ok ".mcp.json"
        fi
    fi

    # .gitignore
    local gi_entry=".claude/settings.local.json"
    if [[ -f ".gitignore" ]]; then
        if ! grep -qF "$gi_entry" ".gitignore"; then
            echo -e "\n# Claude Code — personal settings\n$gi_entry" >> ".gitignore"
            log_ok ".gitignore (added settings.local.json)"
        else
            log_skip ".gitignore (entry present)"
        fi
    else
        echo -e "# Claude Code — personal settings\n$gi_entry" > ".gitignore"
        log_ok ".gitignore"
    fi

    echo ""
    echo "Next steps:"
    echo "  1. Edit CLAUDE.md — fill in project description, module map, rules"
    echo "  2. Edit CONVENTIONS.md — adjust commit scopes to match your modules"
    if [[ "$no_mcp" != true ]] && [[ -z "$collection_name" ]]; then
        echo "  3. Edit .mcp.json — set your collection name (or delete if not using)"
    fi
    echo ""
}

project_help() {
    cat <<EOF
Usage: claude-init [OPTIONS]

Scaffold Claude Code project files in the current directory.
Existing files are skipped unless --force is used.

Options:
  --name NAME         Project name (default: directory name)
  --collection NAME   Qdrant collection name (auto-configures .mcp.json)
  --no-mcp            Skip .mcp.json creation
  --force             Overwrite existing files
  -h, --help          Show this help

Examples:
  claude-init
  claude-init --name myapp --collection myapp-search
  claude-init --no-mcp
  claude-init --force
EOF
}

# ╔═══════════════════════════════════════════════════╗
# ║  MAIN — route to setup or project                 ║
# ╚═══════════════════════════════════════════════════╝

main_help() {
    cat <<EOF
claude-init — Claude Code project toolkit

Commands:
  claude-init setup [OPTIONS]    One-time global install (agents, templates, rules)
  claude-init [OPTIONS]          Scaffold project files in current directory

Run 'claude-init setup --help' or 'claude-init --help' for details.
EOF
}

case "${1:-}" in
    setup)  shift; do_setup "$@" ;;
    -h|--help)
        if [[ $# -eq 1 ]]; then
            main_help
        else
            project_help
        fi
        ;;
    *)      do_project "$@" ;;
esac
