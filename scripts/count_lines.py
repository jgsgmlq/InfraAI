#!/usr/bin/env python3
"""
Count Lines Tool

Counts lines of code in Python files within a directory.

Exit codes:
    0 - Success
    2 - Parameter error
    3 - Runtime error
"""

import argparse
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def parse_args():
    parser = argparse.ArgumentParser(
        description="Count lines of code in Python files"
    )
    parser.add_argument(
        "path",
        type=str,
        nargs="?",
        default=".",
        help="Directory to scan (default: current directory)"
    )
    parser.add_argument(
        "--ext",
        type=str,
        default=".py",
        help="File extension to count (default: .py)"
    )
    parser.add_argument(
        "--no-empty",
        action="store_true",
        help="Exclude empty lines from count"
    )
    return parser.parse_args()


def count_file_lines(file_path: Path, skip_empty: bool = False) -> int:
    """Count lines in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            if skip_empty:
                return sum(1 for line in f if line.strip())
            else:
                return sum(1 for _ in f)
    except Exception as e:
        sys.stderr.write(f"Warning: Cannot read {file_path}: {e}\n")
        return 0


def main():
    try:
        args = parse_args()
    except SystemExit as e:
        sys.exit(e.code)

    target_path = Path(args.path)

    if not target_path.exists():
        sys.stderr.write(f"Error: Path not found: {args.path}\n")
        sys.exit(3)

    if not target_path.is_dir():
        sys.stderr.write(f"Error: Not a directory: {args.path}\n")
        sys.exit(3)

    # Find all matching files
    ext = args.ext if args.ext.startswith('.') else f'.{args.ext}'
    files = list(target_path.rglob(f'*{ext}'))

    if not files:
        print(f"No {ext} files found in {target_path}")
        sys.exit(0)

    # Count lines
    print(f"# Line Count Report ({ext} files)\n")
    print(f"Directory: {target_path.resolve()}\n")
    print("| File | Lines |")
    print("|------|-------|")

    total_lines = 0
    for file in sorted(files):
        lines = count_file_lines(file, args.no_empty)
        total_lines += lines
        rel_path = file.relative_to(target_path)
        print(f"| {rel_path} | {lines} |")

    print(f"\n**Total**: {len(files)} files, {total_lines} lines")
    sys.exit(0)


if __name__ == "__main__":
    main()
