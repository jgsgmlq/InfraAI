#!/usr/bin/env python3
"""
Project Initialization Tool

Initializes a new project with the AI-Native Infrastructure Framework.
Copies core framework files and sets up the project structure.

Exit codes:
    0 - Success
    2 - Parameter error
    3 - Runtime error
"""

import argparse
import shutil
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def parse_args():
    parser = argparse.ArgumentParser(
        description="Initialize a new project with the AI-Native Infrastructure Framework"
    )
    parser.add_argument(
        "--target",
        type=str,
        required=True,
        help="Target directory for the new project"
    )
    parser.add_argument(
        "--name",
        type=str,
        default="New Project",
        help="Project name (default: New Project)"
    )
    parser.add_argument(
        "--description",
        type=str,
        default="A project using AI-Native Infrastructure Framework",
        help="Project description"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files if present"
    )
    return parser.parse_args()


def get_framework_root() -> Path:
    """Get the root directory of the framework."""
    # This script is in scripts/, framework root is parent
    return Path(__file__).parent.parent


def copy_directory(src: Path, dst: Path, dry_run: bool = False):
    """Copy a directory recursively."""
    if dry_run:
        print(f"  Would copy: {src} -> {dst}")
        return

    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f"  Copied: {src} -> {dst}")


def copy_file(src: Path, dst: Path, dry_run: bool = False):
    """Copy a single file."""
    if dry_run:
        print(f"  Would copy: {src} -> {dst}")
        return

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"  Copied: {src} -> {dst}")


def create_directory(path: Path, dry_run: bool = False):
    """Create a directory."""
    if dry_run:
        print(f"  Would create: {path}")
        return

    path.mkdir(parents=True, exist_ok=True)
    print(f"  Created: {path}")


def customize_claude_md(target: Path, name: str, description: str, dry_run: bool = False):
    """Customize CLAUDE.md with project information."""
    claude_md = target / "CLAUDE.md"

    if dry_run:
        print(f"  Would customize: {claude_md}")
        return

    if claude_md.exists():
        content = claude_md.read_text(encoding='utf-8')

        # Replace project name in title
        content = content.replace(
            "# AI-Native Infrastructure Framework",
            f"# {name}"
        )

        # Add project description after the title
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('> 本文件是'):
                lines[i] = f"> {description}\n>\n> 本框架基于 AI-Native Infrastructure Framework。"
                break

        claude_md.write_text('\n'.join(lines), encoding='utf-8')
        print(f"  Customized: {claude_md}")


def init_project(args):
    """Initialize the project."""
    framework_root = get_framework_root()
    target = Path(args.target).resolve()

    print(f"\n{'='*60}")
    print(f"Initializing project: {args.name}")
    print(f"Target: {target}")
    print(f"{'='*60}\n")

    # Check if target exists
    if target.exists() and not args.force:
        if any(target.iterdir()):
            sys.stderr.write(f"Error: Target directory is not empty: {target}\n")
            sys.stderr.write("Use --force to overwrite existing files.\n")
            sys.exit(3)

    # Step 1: Create target directory
    print("Step 1: Creating target directory...")
    create_directory(target, args.dry_run)

    # Step 2: Copy core framework
    print("\nStep 2: Copying core framework...")
    core_src = framework_root / "core"
    if core_src.exists():
        copy_directory(core_src, target / "core", args.dry_run)
    else:
        # Fallback: copy individual directories if core/ doesn't exist
        print("  Note: core/ not found, copying from root directories...")
        for dir_name in ["docs", "registry", "scripts", ".agent"]:
            src = framework_root / dir_name
            if src.exists():
                copy_directory(src, target / "core" / dir_name, args.dry_run)

    # Step 3: Copy entry files
    print("\nStep 3: Copying entry files...")
    for filename in ["CLAUDE.md", "BOOTSTRAP.md", "requirements.txt"]:
        src = framework_root / filename
        if src.exists():
            copy_file(src, target / filename, args.dry_run)

    # Step 4: Create project directories
    print("\nStep 4: Creating project directories...")
    for dir_path in ["project/tools", "project/config", "project/docs"]:
        create_directory(target / dir_path, args.dry_run)

    # Step 5: Create project registry
    print("\nStep 5: Creating project registry...")
    project_registry = target / "project" / "registry"
    create_directory(project_registry, args.dry_run)

    if not args.dry_run:
        registry_content = """# Project-specific tools registry
# Add your project tools here

# Example:
# - id: proj-example
#   name: Project Example Tool
#   version: "1.0.0"
#   type: cli
#   entry: python project/tools/example.py
#   description: An example project tool
"""
        (project_registry / "tools.yaml").write_text(registry_content, encoding='utf-8')
        print(f"  Created: {project_registry / 'tools.yaml'}")

    # Step 6: Customize CLAUDE.md
    print("\nStep 6: Customizing CLAUDE.md...")
    customize_claude_md(target, args.name, args.description, args.dry_run)

    # Step 7: Create .gitignore
    print("\nStep 7: Creating .gitignore...")
    if not args.dry_run:
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
.env
venv/
.venv/

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db

# Project
*.log
*.tmp
"""
        (target / ".gitignore").write_text(gitignore_content, encoding='utf-8')
        print(f"  Created: {target / '.gitignore'}")

    # Summary
    print(f"\n{'='*60}")
    print("Initialization complete!")
    print(f"{'='*60}\n")

    print("Next steps:")
    print(f"  1. cd {target}")
    print("  2. pip install -r requirements.txt")
    print("  3. python core/scripts/list_tools.py --registry core/registry/tools.yaml")
    print("  4. Read CLAUDE.md to understand the project structure")
    print()


def main():
    try:
        args = parse_args()
    except SystemExit as e:
        sys.exit(e.code)

    try:
        init_project(args)
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(3)


if __name__ == "__main__":
    main()
