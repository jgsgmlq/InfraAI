#!/usr/bin/env python3
"""
Framework Export Tool

Exports the AI-Native Infrastructure Framework as a portable package.
Creates a zip file containing all core framework files.

Exit codes:
    0 - Success
    2 - Parameter error
    3 - Runtime error
"""

import argparse
import json
import os
import sys
import zipfile
from datetime import datetime
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def parse_args():
    parser = argparse.ArgumentParser(
        description="Export the AI-Native Infrastructure Framework as a portable package"
    )
    parser.add_argument(
        "--out",
        type=str,
        default="framework.zip",
        help="Output file path (default: framework.zip)"
    )
    parser.add_argument(
        "--include-project",
        action="store_true",
        help="Include project/ directory in export (not recommended)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be included without creating the archive"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    return parser.parse_args()


def get_framework_root() -> Path:
    """Get the root directory of the framework."""
    return Path(__file__).parent.parent


def should_include(path: Path, framework_root: Path, include_project: bool) -> bool:
    """Determine if a file should be included in the export."""
    rel_path = path.relative_to(framework_root)
    rel_str = str(rel_path).replace('\\', '/')

    # Always exclude
    exclude_patterns = [
        '__pycache__',
        '.git',
        '.env',
        '.venv',
        'venv',
        '.idea',
        '.vscode',
        '*.pyc',
        '*.pyo',
        '.DS_Store',
        'Thumbs.db',
        '*.log',
        '*.tmp',
        'framework.zip',  # Don't include previous exports
    ]

    for pattern in exclude_patterns:
        if pattern.startswith('*'):
            if rel_str.endswith(pattern[1:]):
                return False
        elif pattern in rel_str:
            return False

    # Exclude project-specific files unless requested
    if not include_project:
        exclude_dirs = [
            'project/',
            'docs/PROJECT_VISION.md',
            'docs/REQUIREMENTS.md',
            'docs/IMPLEMENTATION_PLAN.md',
        ]
        for exc in exclude_dirs:
            if rel_str.startswith(exc) or rel_str == exc.rstrip('/'):
                return False

    return True


def get_files_to_export(framework_root: Path, include_project: bool) -> list:
    """Get list of files to include in export."""
    files = []

    # Core directory
    core_dir = framework_root / "core"
    if core_dir.exists():
        for path in core_dir.rglob('*'):
            if path.is_file() and should_include(path, framework_root, include_project):
                files.append(path)

    # Root level files
    root_files = [
        "CLAUDE.md",
        "BOOTSTRAP.md",
        "requirements.txt",
        "README.md",
    ]
    for filename in root_files:
        path = framework_root / filename
        if path.exists():
            files.append(path)

    # Include project if requested
    if include_project:
        project_dir = framework_root / "project"
        if project_dir.exists():
            for path in project_dir.rglob('*'):
                if path.is_file() and should_include(path, framework_root, True):
                    files.append(path)

    # Legacy directories (for backward compatibility, if core doesn't exist)
    if not core_dir.exists():
        for dir_name in ["docs", "registry", "scripts", ".agent"]:
            dir_path = framework_root / dir_name
            if dir_path.exists():
                for path in dir_path.rglob('*'):
                    if path.is_file() and should_include(path, framework_root, include_project):
                        files.append(path)

    return sorted(set(files))


def create_manifest(files: list, framework_root: Path) -> dict:
    """Create a manifest of included files."""
    manifest = {
        "framework": "AI-Native Infrastructure Framework",
        "version": "1.0.0",
        "exported_at": datetime.now().isoformat(),
        "file_count": len(files),
        "files": []
    }

    for path in files:
        rel_path = str(path.relative_to(framework_root)).replace('\\', '/')
        manifest["files"].append({
            "path": rel_path,
            "size": path.stat().st_size
        })

    return manifest


def export_framework(args):
    """Export the framework to a zip file."""
    framework_root = get_framework_root()
    output_path = Path(args.out).resolve()

    print(f"\n{'='*60}")
    print("Exporting AI-Native Infrastructure Framework")
    print(f"Output: {output_path}")
    print(f"{'='*60}\n")

    # Get files to export
    print("Collecting files...")
    files = get_files_to_export(framework_root, args.include_project)

    if not files:
        sys.stderr.write("Error: No files found to export.\n")
        sys.exit(3)

    print(f"Found {len(files)} files to export.\n")

    # Create manifest
    manifest = create_manifest(files, framework_root)

    if args.dry_run:
        print("Dry run - files that would be included:\n")
        for f in manifest["files"]:
            print(f"  {f['path']} ({f['size']} bytes)")
        print(f"\nTotal: {len(files)} files")
        return

    # Create zip file
    print("Creating archive...")

    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add manifest
            manifest_json = json.dumps(manifest, indent=2, ensure_ascii=False)
            zf.writestr('manifest.json', manifest_json)

            # Add files
            for path in files:
                rel_path = str(path.relative_to(framework_root)).replace('\\', '/')
                zf.write(path, rel_path)
                if args.verbose:
                    print(f"  Added: {rel_path}")

        # Get final size
        final_size = output_path.stat().st_size
        size_kb = final_size / 1024

        print(f"\n{'='*60}")
        print("Export complete!")
        print(f"{'='*60}\n")
        print(f"Output: {output_path}")
        print(f"Size: {size_kb:.1f} KB")
        print(f"Files: {len(files)}")
        print("\nTo use this framework:")
        print(f"  1. unzip {output_path.name}")
        print("  2. Read BOOTSTRAP.md for initialization instructions")

    except Exception as e:
        sys.stderr.write(f"Error creating archive: {e}\n")
        sys.exit(3)


def main():
    try:
        args = parse_args()
    except SystemExit as e:
        sys.exit(e.code)

    try:
        export_framework(args)
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(3)


if __name__ == "__main__":
    main()
