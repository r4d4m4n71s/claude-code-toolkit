#!/usr/bin/env python3
"""claude-init — Claude Code project toolkit

Purpose:
  Interactive CLI with two commands:
    init-globals  — installs global Claude Code config into ~/.claude/
                    (agents, templates, CLAUDE.md, self as claude-init binary)
    init-project  — scaffolds Claude Code files in the current project directory
                    (CLAUDE.md, CONVENTIONS.md, settings, .mcp.json, session notes)

  Detects existing files before copying, prompts the user to overwrite or skip,
  and creates timestamped backups before any overwrite.

Install:
  python3 claude-init.py init-globals
  (copies itself to ~/.claude/bin/claude-init)

  Add to ~/.bashrc or ~/.zshrc:
    export PATH="$HOME/.claude/bin:$PATH"
"""

import argparse
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependency check — give a clear message before anything else
# ---------------------------------------------------------------------------
try:
    from rich.console import Console
    from rich.panel import Panel
    import questionary
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with:  pip install rich questionary")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CLAUDE_DIR = Path.home() / ".claude"
AGENTS_DIR = CLAUDE_DIR / "agents"
TEMPLATES_DIR = CLAUDE_DIR / "templates"
BIN_DIR = CLAUDE_DIR / "bin"

console = Console()


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
@dataclass
class FilePlan:
    src: Path
    dest: Path
    label: str
    always_update: bool = False  # e.g. bin/claude-init — skips conflict prompt
    conflict: bool = field(init=False, default=False)
    action: str = field(init=False, default="pending")  # install | update | skip

    def __post_init__(self) -> None:
        self.conflict = self.dest.exists() and not self.always_update


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------
def backup_and_copy(src: Path, dest: Path, backup_base: Path) -> None:
    """Back up dest to backup_base/, then overwrite dest with src."""
    backup_base.mkdir(parents=True, exist_ok=True)
    backup_dest = backup_base / dest.name
    shutil.copy2(dest, backup_dest)
    shutil.copy2(src, dest)


def resolve_conflicts(plans: list[FilePlan], force: bool) -> None:
    """Determine .action for every plan, prompting when needed."""
    conflicts = [p for p in plans if p.conflict]

    # No conflicts — everything is new
    if not conflicts:
        for p in plans:
            if p.action == "pending":
                p.action = "install"
        return

    # --force: overwrite all without prompting
    if force:
        console.print(
            f"  [dim]--force: overwriting {len(conflicts)} existing file(s)[/dim]"
        )
        for p in plans:
            if p.action == "pending":
                p.action = "update" if p.conflict else "install"
        return

    # Interactive: ask the user what to do
    console.print()
    console.print(
        f"  [yellow bold]⚠[/yellow bold]  "
        f"[yellow]{len(conflicts)} file(s) already exist:[/yellow]"
    )
    for p in conflicts:
        console.print(f"      {p.label}")
    console.print()

    choice = questionary.select(
        "What would you like to do?",
        choices=[
            "Overwrite all  (originals backed up)",
            "Skip all existing",
            "Decide per file",
            "Quit",
        ],
        style=questionary.Style(
            [
                ("selected", "fg:#00aa00 bold"),
                ("pointer", "fg:#00aa00 bold"),
            ]
        ),
    ).ask()

    if choice is None or choice == "Quit":
        console.print("\n  [dim]Aborted.[/dim]\n")
        sys.exit(0)

    if choice.startswith("Overwrite all"):
        for p in plans:
            if p.action == "pending":
                p.action = "update" if p.conflict else "install"

    elif choice.startswith("Skip all"):
        for p in plans:
            if p.action == "pending":
                p.action = "skip" if p.conflict else "install"

    else:  # Decide per file
        for p in plans:
            if p.action != "pending":
                continue
            if not p.conflict:
                p.action = "install"
            else:
                answer = questionary.confirm(
                    f"{p.label} already exists. Overwrite? (backup will be saved)",
                    default=False,
                ).ask()
                p.action = "update" if answer else "skip"


def execute_plans(
    plans: list[FilePlan], backup_base: Path
) -> tuple[int, int, int]:
    """Execute all plans and return (installed, updated, skipped)."""
    installed = updated = skipped = 0

    for p in plans:
        if p.always_update:
            p.dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p.src, p.dest)
            p.dest.chmod(0o755)
            console.print(f"  [green]✓[/green] {p.label}  [dim](updated)[/dim]")
            updated += 1

        elif p.action == "install":
            p.dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p.src, p.dest)
            console.print(f"  [green]✓[/green] {p.label}")
            installed += 1

        elif p.action == "update":
            backup_and_copy(p.src, p.dest, backup_base)
            console.print(
                f"  [green]✓[/green] {p.label}  [blue](backup saved)[/blue]"
            )
            updated += 1

        elif p.action == "skip":
            console.print(
                f"  [yellow]⊘[/yellow] {p.label}  [dim](skipped)[/dim]"
            )
            skipped += 1

    return installed, updated, skipped


def detect_source_dir() -> Path:
    """Return the toolkit root (the directory that contains agents/ and templates/)."""
    script_dir = Path(__file__).resolve().parent
    if (script_dir / "agents").is_dir() and (script_dir / "templates").is_dir():
        return script_dir
    console.print(
        "[red]Error:[/red] Cannot find toolkit files (agents/ and templates/ directories)."
    )
    console.print(
        "Run from inside the toolkit directory, or use: "
        "[bold]--from /path/to/toolkit[/bold]"
    )
    sys.exit(1)


def find_global_claude_md(source_dir: Path) -> Path | None:
    """Return the source file for ~/.claude/CLAUDE.md (template name varies)."""
    for name in ("CLAUDE.global-template.md", "CLAUDE.md"):
        p = source_dir / name
        if p.exists():
            return p
    return None


def print_summary(installed: int, updated: int, skipped: int) -> None:
    console.print()
    console.rule(style="dim")
    console.print(
        f"  Done.  [green]{installed} installed[/green] · "
        f"[blue]{updated} updated[/blue] · "
        f"[dim]{skipped} skipped[/dim]"
    )


# ---------------------------------------------------------------------------
# Command: init-globals
# ---------------------------------------------------------------------------
def cmd_init_globals(args: argparse.Namespace) -> None:
    source_dir = (
        Path(args.source_from).resolve() if args.source_from else detect_source_dir()
    )

    console.print()
    console.print(
        Panel.fit("[bold]Claude Code — Global Setup[/bold]", border_style="blue")
    )
    console.print(f"  Source:  {source_dir}")
    console.print(f"  Target:  {CLAUDE_DIR}")
    console.print()

    plans: list[FilePlan] = []

    # CLAUDE.md
    claude_src = find_global_claude_md(source_dir)
    if claude_src:
        plans.append(FilePlan(claude_src, CLAUDE_DIR / "CLAUDE.md", "~/.claude/CLAUDE.md"))
    else:
        console.print(
            "  [yellow]⊘[/yellow] CLAUDE.md source not found in toolkit, skipping"
        )

    # Agents
    for agent in ("architect", "developer", "tester", "documentator"):
        src = source_dir / "agents" / f"{agent}.md"
        if src.exists():
            plans.append(
                FilePlan(src, AGENTS_DIR / f"{agent}.md", f"~/.claude/agents/{agent}.md")
            )
        else:
            console.print(
                f"  [yellow]⊘[/yellow] agents/{agent}.md not found, skipping"
            )

    # Templates
    for name in (
        "CLAUDE.project-template.md",
        "CONVENTIONS.md",
        "session-notes.md",
        "settings.json",
        "settings.local.json",
        ".mcp.json.template",
    ):
        src = source_dir / "templates" / name
        if src.exists():
            plans.append(
                FilePlan(src, TEMPLATES_DIR / name, f"~/.claude/templates/{name}")
            )
        else:
            console.print(f"  [yellow]⊘[/yellow] templates/{name} not found, skipping")

    # Self-install (always updated, no conflict prompt)
    plans.append(
        FilePlan(
            Path(__file__).resolve(),
            BIN_DIR / "claude-init",
            "~/.claude/bin/claude-init",
            always_update=True,
        )
    )

    # Pre-scan report
    console.print("  Checking files...\n")
    for p in plans:
        if p.always_update:
            console.print(f"    [dim]—[/dim] {p.label}  [dim](always updated)[/dim]")
        elif p.conflict:
            console.print(f"    [yellow]⚠[/yellow] {p.label}  [yellow](exists)[/yellow]")
        else:
            console.print(f"    [green]·[/green] {p.label}  [dim](new)[/dim]")

    # Resolve conflicts, then execute
    CLAUDE_DIR.mkdir(parents=True, exist_ok=True)
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    BIN_DIR.mkdir(parents=True, exist_ok=True)

    resolve_conflicts(plans, force=args.force)

    console.print()
    backup_base = CLAUDE_DIR / "backups" / datetime.now().strftime("%Y%m%d-%H%M%S")
    installed, updated, skipped = execute_plans(plans, backup_base)

    print_summary(installed, updated, skipped)
    console.print()

    bin_dir_str = str(BIN_DIR)
    if bin_dir_str in os.environ.get("PATH", "").split(os.pathsep):
        console.print(f"  [green]✓[/green] {BIN_DIR} is already in PATH")
    else:
        console.print(
            "  Add to your shell profile "
            "([dim]~/.bashrc[/dim] or [dim]~/.zshrc[/dim]):\n"
        )
        console.print('    export PATH="$HOME/.claude/bin:$PATH"')

    console.print()
    console.print(
        "  Run [bold]claude-init init-project[/bold] inside any project directory."
    )
    console.print()


# ---------------------------------------------------------------------------
# Command: init-project
# ---------------------------------------------------------------------------
def cmd_init_project(args: argparse.Namespace) -> None:
    if not TEMPLATES_DIR.is_dir():
        console.print(
            f"[red]Error:[/red] Templates not found at {TEMPLATES_DIR}"
        )
        console.print("Run [bold]claude-init init-globals[/bold] first.")
        sys.exit(1)

    project_name: str = args.name or Path.cwd().name
    cwd = Path.cwd()

    console.print()
    console.print(
        Panel.fit("[bold]Claude Code — Project Init[/bold]", border_style="blue")
    )
    console.print(f"  Project:    {project_name}")
    console.print(f"  Directory:  {cwd}")
    console.print()

    # Temp files to clean up after execution
    tmp_paths: list[Path] = []

    try:
        plans: list[FilePlan] = []

        # CLAUDE.md — rendered from template (placeholder substitution)
        claude_tpl = TEMPLATES_DIR / "CLAUDE.project-template.md"
        if claude_tpl.exists():
            content = claude_tpl.read_text().replace("<project-name>", project_name)
            tmp = tempfile.NamedTemporaryFile(
                mode="w", suffix=".md", delete=False, prefix="claude_init_"
            )
            tmp.write(content)
            tmp.close()
            rendered_claude = Path(tmp.name)
            tmp_paths.append(rendered_claude)
            plans.append(FilePlan(rendered_claude, cwd / "CLAUDE.md", "CLAUDE.md"))
        else:
            console.print(
                "  [yellow]⊘[/yellow] CLAUDE.project-template.md not found, skipping"
            )

        # CONVENTIONS.md
        plans.append(
            FilePlan(
                TEMPLATES_DIR / "CONVENTIONS.md",
                cwd / "CONVENTIONS.md",
                "CONVENTIONS.md",
            )
        )

        # docs/session-notes.md
        plans.append(
            FilePlan(
                TEMPLATES_DIR / "session-notes.md",
                cwd / "docs" / "session-notes.md",
                "docs/session-notes.md",
            )
        )

        # .claude/settings.json
        plans.append(
            FilePlan(
                TEMPLATES_DIR / "settings.json",
                cwd / ".claude" / "settings.json",
                ".claude/settings.json",
            )
        )

        # .claude/settings.local.json
        plans.append(
            FilePlan(
                TEMPLATES_DIR / "settings.local.json",
                cwd / ".claude" / "settings.local.json",
                ".claude/settings.local.json",
            )
        )

        # .mcp.json (optional)
        if not args.no_mcp:
            mcp_tpl = TEMPLATES_DIR / ".mcp.json.template"
            if mcp_tpl.exists():
                if args.collection:
                    content = mcp_tpl.read_text()
                    content = content.replace("your-collection-name", args.collection)
                    content = content.replace(
                        "project-search", f"{project_name}-search"
                    )
                    tmp2 = tempfile.NamedTemporaryFile(
                        mode="w",
                        suffix=".json",
                        delete=False,
                        prefix="claude_init_",
                    )
                    tmp2.write(content)
                    tmp2.close()
                    rendered_mcp = Path(tmp2.name)
                    tmp_paths.append(rendered_mcp)
                else:
                    rendered_mcp = mcp_tpl
                plans.append(FilePlan(rendered_mcp, cwd / ".mcp.json", ".mcp.json"))

        # Pre-scan report
        console.print("  Checking files...\n")
        for p in plans:
            if p.conflict:
                console.print(
                    f"    [yellow]⚠[/yellow] {p.label}  [yellow](exists)[/yellow]"
                )
            else:
                console.print(f"    [green]·[/green] {p.label}  [dim](new)[/dim]")

        # .gitignore — append-only, report separately
        gi_path = cwd / ".gitignore"
        gi_entry = ".claude/settings.local.json"
        gi_has_entry = gi_path.exists() and gi_entry in gi_path.read_text()
        if gi_has_entry:
            console.print(f"    [dim]—[/dim] .gitignore  [dim](entry present)[/dim]")
        else:
            console.print(
                f"    [green]·[/green] .gitignore  [dim](entry will be added)[/dim]"
            )

        # Resolve conflicts, then execute
        resolve_conflicts(plans, force=args.force)

        console.print()
        backup_base = (
            cwd / ".claude" / "backups" / datetime.now().strftime("%Y%m%d-%H%M%S")
        )
        installed, updated, skipped = execute_plans(plans, backup_base)

        # .gitignore handling (outside FilePlan — append-only)
        if not gi_has_entry:
            with gi_path.open("a") as f:
                if gi_path.exists() and gi_path.stat().st_size > 0:
                    f.write("\n")
                f.write(f"# Claude Code — personal settings\n{gi_entry}\n")
            console.print(
                f"  [green]✓[/green] .gitignore  [dim](entry added)[/dim]"
            )
            installed += 1

    finally:
        for tmp_path in tmp_paths:
            tmp_path.unlink(missing_ok=True)

    print_summary(installed, updated, skipped)
    console.print()
    console.print("  Next steps:")
    console.print(
        "    1. Edit [bold]CLAUDE.md[/bold] — fill in project description, module map, rules"
    )
    console.print(
        "    2. Edit [bold]CONVENTIONS.md[/bold] — adjust commit scopes to match your modules"
    )
    if not args.no_mcp and not args.collection:
        console.print(
            "    3. Edit [bold].mcp.json[/bold] — set your collection name "
            "(or delete if not using Qdrant)"
        )
    console.print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        prog="claude-init",
        description="Claude Code project toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  claude-init init-globals\n"
            "  claude-init init-globals --from /path/to/toolkit --force\n"
            "  claude-init init-project\n"
            "  claude-init init-project --name myapp --collection myapp-search\n"
            "  claude-init init-project --no-mcp --force\n"
        ),
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    # init-globals
    p_globals = subparsers.add_parser(
        "init-globals",
        help="Install global agents, templates, and rules into ~/.claude/",
        description="One-time install of global agents, templates, and rules into ~/.claude/.",
    )
    p_globals.add_argument(
        "--from",
        dest="source_from",
        metavar="DIR",
        help="Path to toolkit directory (auto-detected if running from it)",
    )
    p_globals.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files without prompting (originals backed up)",
    )

    # init-project
    p_project = subparsers.add_parser(
        "init-project",
        help="Scaffold Claude Code files in the current directory",
        description="Scaffold Claude Code project files in the current directory.",
    )
    p_project.add_argument(
        "--name",
        metavar="NAME",
        help="Project name (default: current directory name)",
    )
    p_project.add_argument(
        "--collection",
        metavar="NAME",
        help="Qdrant collection name (auto-configures .mcp.json)",
    )
    p_project.add_argument(
        "--no-mcp",
        action="store_true",
        help="Skip .mcp.json creation",
    )
    p_project.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files without prompting (originals backed up)",
    )

    args = parser.parse_args()

    if args.command == "init-globals":
        cmd_init_globals(args)
    elif args.command == "init-project":
        cmd_init_project(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
