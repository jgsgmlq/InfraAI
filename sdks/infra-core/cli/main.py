#!/usr/bin/env python3
"""
infra-core CLI

Command-line interface for AI-Native Infrastructure Framework core operations.
"""

import argparse
import sys
from pathlib import Path

# Add SDK parent to path for imports
sdk_root = Path(__file__).parent.parent
sys.path.insert(0, str(sdk_root))

from api import (
    audit_sdk,
    audit_skills,
    audit_docs,
    AuditSeverity,
)
from api.scaffold import create_sdk
from version import __version__


def cmd_audit_sdk(args):
    """Handle audit-sdk command."""
    result = audit_sdk(args.path)

    if not args.quiet:
        print(f"Auditing SDK: {args.path}")
        print("-" * 40)

    for finding in result.findings:
        severity = finding.severity.value.upper()
        print(f"[{severity}] {finding.message}")
        if finding.path and args.verbose:
            print(f"        Path: {finding.path}")
        if finding.suggestion and args.verbose:
            print(f"        Fix: {finding.suggestion}")

    if not args.quiet:
        print("-" * 40)
        if result.passed:
            print("SDK audit passed")
        else:
            print(f"SDK audit failed ({len(result.errors)} errors)")

    return 0 if result.passed else 3


def cmd_audit_docs(args):
    """Handle audit-docs command."""
    result = audit_docs(args.path)

    if not args.quiet:
        print(f"Auditing docs: {args.path}")
        print("-" * 40)

    for finding in result.findings:
        severity = finding.severity.value.upper()
        print(f"[{severity}] {finding.message}")
        if finding.path and args.verbose:
            print(f"        Path: {finding.path}")

    if not args.quiet:
        print("-" * 40)
        if result.passed:
            print("Docs audit passed")
        else:
            print(f"Docs audit failed ({len(result.errors)} errors)")

    return 0 if result.passed else 3


def cmd_audit_skills(args):
    """Handle audit-skills command."""
    result = audit_skills(args.path, args.sdk_dir)

    if not args.quiet:
        print(f"Auditing skills: {args.path}")
        print("-" * 40)

    for finding in result.findings:
        severity = finding.severity.value.upper()
        print(f"[{severity}] {finding.message}")
        if finding.path and args.verbose:
            print(f"        Path: {finding.path}")

    if not args.quiet:
        print("-" * 40)
        if result.passed:
            print("Skills audit passed")
        else:
            print(f"Skills audit failed ({len(result.errors)} errors)")

    return 0 if result.passed else 3


def cmd_create_sdk(args):
    """Handle create-sdk command."""
    result = create_sdk(
        sdk_name=args.name,
        target_dir=args.target,
        description=args.description or "",
        author=args.author or "AI Infrastructure Team",
        version=args.version or "1.0.0",
        dry_run=args.dry_run
    )

    if result['success']:
        if args.dry_run:
            print(f"Would create SDK at: {result['path']}")
            print("\nFiles to create:")
            for f in result['files_created']:
                print(f"  - {f}")
        else:
            print(f"SDK created at: {result['path']}")
            print(f"\nFiles created: {len(result['files_created'])}")
            if args.verbose:
                for f in result['files_created']:
                    print(f"  - {f}")
            print("\nNext steps:")
            print(f"  1. cd {result['path']}")
            print(f"  2. Edit manifest.yaml and README.md")
            print(f"  3. Add your API code to api/")
            print(f"  4. Run: python sdks/infra-core/cli/main.py audit-sdk {result['path']}")
        return 0
    else:
        print(f"Error: {result['message']}", file=sys.stderr)
        return 3


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="infra-core",
        description="AI-Native Infrastructure Framework CLI"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"infra-core {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # audit-sdk command
    audit_sdk_parser = subparsers.add_parser(
        "audit-sdk",
        help="Audit an SDK package"
    )
    audit_sdk_parser.add_argument("path", help="Path to SDK directory")
    audit_sdk_parser.add_argument("-v", "--verbose", action="store_true")
    audit_sdk_parser.add_argument("-q", "--quiet", action="store_true")
    audit_sdk_parser.set_defaults(func=cmd_audit_sdk)

    # audit-docs command
    audit_docs_parser = subparsers.add_parser(
        "audit-docs",
        help="Audit documentation"
    )
    audit_docs_parser.add_argument("path", help="Path to docs directory")
    audit_docs_parser.add_argument("-v", "--verbose", action="store_true")
    audit_docs_parser.add_argument("-q", "--quiet", action="store_true")
    audit_docs_parser.set_defaults(func=cmd_audit_docs)

    # audit-skills command
    audit_skills_parser = subparsers.add_parser(
        "audit-skills",
        help="Audit skills configuration"
    )
    audit_skills_parser.add_argument("path", help="Path to skills directory")
    audit_skills_parser.add_argument("--sdk-dir", help="Path to sdks directory")
    audit_skills_parser.add_argument("-v", "--verbose", action="store_true")
    audit_skills_parser.add_argument("-q", "--quiet", action="store_true")
    audit_skills_parser.set_defaults(func=cmd_audit_skills)

    # create-sdk command
    create_sdk_parser = subparsers.add_parser(
        "create-sdk",
        help="Create a new SDK package"
    )
    create_sdk_parser.add_argument("name", help="SDK name (kebab-case, e.g., 'my-sdk')")
    create_sdk_parser.add_argument("--target", default="sdks", help="Target directory (default: sdks)")
    create_sdk_parser.add_argument("--description", help="SDK description")
    create_sdk_parser.add_argument("--author", help="Author name")
    create_sdk_parser.add_argument("--version", help="Initial version (default: 1.0.0)")
    create_sdk_parser.add_argument("--dry-run", action="store_true", help="Show what would be created")
    create_sdk_parser.add_argument("-v", "--verbose", action="store_true")
    create_sdk_parser.set_defaults(func=cmd_create_sdk)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 2

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
