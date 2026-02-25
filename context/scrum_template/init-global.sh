#!/usr/bin/env bash
# Purpose: Install global Claude Code context (CLAUDE.md + agents/) to ~/.claude/
# Usage:   ./init-global.sh [--force]
#   --force   Back up existing files before overwriting instead of skipping them.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR/global"
DEST="$HOME/.claude"
FORCE=false
SKIPPED=0

# ── argument parsing ──────────────────────────────────────────────────────────
for arg in "$@"; do
    case "$arg" in
        --force) FORCE=true ;;
        *) echo "Unknown argument: $arg" >&2; exit 1 ;;
    esac
done

# ── helpers ───────────────────────────────────────────────────────────────────
install_file() {
    local src="$1"
    local dst="$2"

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
    cp "$src" "$dst"
    echo "  [ok]     $dst"
}

# ── main ──────────────────────────────────────────────────────────────────────
echo "==> Installing global context to $DEST"
mkdir -p "$DEST"

install_file "$SRC/CLAUDE.md" "$DEST/CLAUDE.md"

if [[ -d "$SRC/agents" ]]; then
    mkdir -p "$DEST/agents"
    for f in "$SRC/agents"/*; do
        install_file "$f" "$DEST/agents/$(basename "$f")"
    done
fi

if (( SKIPPED > 0 )); then
    echo ""
    echo "  $SKIPPED file(s) already existed and were skipped."
    echo "  Re-run with --force to overwrite them (existing files will be backed up)."
fi
echo "Done."
