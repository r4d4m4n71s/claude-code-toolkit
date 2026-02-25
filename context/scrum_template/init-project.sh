#!/usr/bin/env bash
# Purpose: Install project Claude Code context into <project>/
#   - <project>/.claude/  ← from project/.claude/
#   - <project>/          ← from project/ root (CONVENTIONS.md, .mcp.json)
# Usage:   ./init-project.sh [project-path] [--force]
#   project-path  Target project directory (default: current working directory).
#   --force       Back up existing files before overwriting instead of skipping them.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR/project"
FORCE=false
SKIPPED=0
PROJECT_PATH=""

# ── argument parsing ──────────────────────────────────────────────────────────
for arg in "$@"; do
    case "$arg" in
        --force) FORCE=true ;;
        -*) echo "Unknown option: $arg" >&2; exit 1 ;;
        *)
            if [[ -n "$PROJECT_PATH" ]]; then
                echo "Unexpected argument: $arg" >&2; exit 1
            fi
            PROJECT_PATH="$arg"
            ;;
    esac
done

[[ -z "$PROJECT_PATH" ]] && PROJECT_PATH="$(pwd)"
PROJECT_PATH="$(realpath "$PROJECT_PATH")"
PROJECT_NAME="$(basename "$PROJECT_PATH")"
DEST="$PROJECT_PATH/.claude"

# ── helpers ───────────────────────────────────────────────────────────────────
install_file() {
    local src="$1"
    local dst="$2"
    local substitute="${3:-false}"

    if [[ -e "$dst" ]]; then
        if [[ "$FORCE" == true ]]; then
            local backup="${dst}.bak.$(date +%Y%m%d_%H%M%S)"
            echo "  [backup] $(basename "$dst")  →  $backup"
            mv "$dst" "$backup"
        else
            echo "  [skip]   $dst  (exists)"
            (( SKIPPED++ )) || true
            return
        fi
    fi

    mkdir -p "$(dirname "$dst")"

    if [[ "$substitute" == true ]]; then
        sed "s/<project-name>/${PROJECT_NAME}/g" "$src" > "$dst"
    else
        cp "$src" "$dst"
    fi

    echo "  [ok]     $dst"
}

# ── main ──────────────────────────────────────────────────────────────────────
echo "==> Installing project context"
echo "    Project : $PROJECT_NAME"
echo "    Target  : $PROJECT_PATH"
mkdir -p "$DEST"

# Files in project/.claude/ → <project>/.claude/
for f in "$SRC/.claude"/* "$SRC/.claude"/.[!.]*; do
    [[ -f "$f" ]] || continue
    fname="$(basename "$f")"
    if [[ "$fname" == "CLAUDE.md" ]]; then
        install_file "$f" "$DEST/$fname" true
    else
        install_file "$f" "$DEST/$fname"
    fi
done

# Files at project/ root → <project>/ root
for f in "$SRC"/* "$SRC"/.[!.]*; do
    [[ -f "$f" ]] || continue
    install_file "$f" "$PROJECT_PATH/$(basename "$f")"
done

if (( SKIPPED > 0 )); then
    echo ""
    echo "  $SKIPPED file(s) already existed and were skipped."
    echo "  Re-run with --force to overwrite them (existing files will be backed up)."
fi
echo "Done."
