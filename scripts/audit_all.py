#!/usr/bin/env python3
"""
Unified Audit Tool

Combines registry audit and SDK audit into a single comprehensive health check.

Audit scopes:
- registry: Check tool registry completeness (scripts, tests, skills)
- sdk: Check SDK packages for structure and manifest compliance
- skills: Check skills entry files for valid frontmatter
- docs: Check documentation for consistency
- all: Run all audits (default)

Exit codes:
    0 - All checks passed
    2 - Parameter error
    3 - Runtime error (audit failures found)
"""

import argparse
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Add SDK path for imports
sdk_path = Path(__file__).parent.parent / "sdks" / "infra-core"
sys.path.insert(0, str(sdk_path / "api"))

from audit import audit_sdk, audit_skills, audit_docs, AuditSeverity


def parse_args():
    parser = argparse.ArgumentParser(
        description="Unified audit tool for registry, SDK, skills, and docs"
    )
    parser.add_argument(
        "scope",
        nargs="?",
        default="all",
        choices=["all", "registry", "sdk", "skills", "docs"],
        help="Audit scope (default: all)"
    )
    parser.add_argument(
        "--registry",
        type=str,
        default="registry/tools.yaml",
        help="Path to the tool registry YAML file"
    )
    parser.add_argument(
        "--sdk-dir",
        type=str,
        default="sdks",
        help="Path to SDK directory"
    )
    parser.add_argument(
        "--skills-dir",
        type=str,
        default=".claude/skills",
        help="Path to skills directory"
    )
    parser.add_argument(
        "--docs-dir",
        type=str,
        default="docs",
        help="Path to docs directory"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Generate template files for missing components (registry only)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only output errors, no success messages"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output including INFO level"
    )
    return parser.parse_args()


def audit_registry_tools(registry_path: str, fix: bool = False) -> tuple:
    """
    Run registry audit (reuse existing logic).
    Returns (passed, error_count, output_lines).
    """
    import yaml

    path = Path(registry_path)
    if not path.exists():
        return False, 1, [f"[ERROR] Registry not found: {registry_path}"]

    try:
        with open(path, 'r', encoding='utf-8') as f:
            tools = yaml.safe_load(f) or []
    except Exception as e:
        return False, 1, [f"[ERROR] Failed to load registry: {e}"]

    if not tools:
        return True, 0, ["[INFO] No tools registered"]

    errors = 0
    lines = []
    all_tool_ids = {t.get('id') for t in tools if t.get('id')}

    for tool in tools:
        tool_id = tool.get('id', 'unknown')
        entry = tool.get('entry', '')

        # Check script exists
        if entry:
            script_path = None
            for part in entry.split():
                if part.endswith('.py'):
                    script_path = Path(part)
                    break

            if script_path and not script_path.exists():
                errors += 1
                lines.append(f"[ERROR] {tool_id}: Script not found: {script_path}")

        # Check smoke test exists
        if entry:
            for part in entry.split():
                if part.endswith('.py'):
                    script_name = Path(part).stem
                    smoke_path = Path(f"scripts/smoke/smoke_{script_name}.sh")
                    if not smoke_path.exists():
                        errors += 1
                        lines.append(f"[ERROR] {tool_id}: Smoke test not found: {smoke_path}")
                    break

        # Check version
        if not tool.get('version'):
            lines.append(f"[WARN] {tool_id}: Missing version field")

        # Check dependencies
        for dep in tool.get('depends_on', []):
            if dep not in all_tool_ids:
                errors += 1
                lines.append(f"[ERROR] {tool_id}: Unknown dependency: {dep}")

    return errors == 0, errors, lines


def audit_all_sdks(sdk_dir: str) -> tuple:
    """
    Audit all SDK packages in the directory.
    Returns (passed, error_count, output_lines).
    """
    sdk_path = Path(sdk_dir)
    if not sdk_path.exists():
        return True, 0, ["[INFO] SDK directory not found, skipping"]

    errors = 0
    lines = []

    for sdk_subdir in sdk_path.iterdir():
        if not sdk_subdir.is_dir():
            continue
        if sdk_subdir.name.startswith('.'):
            continue

        result = audit_sdk(sdk_subdir)

        for finding in result.findings:
            if finding.severity == AuditSeverity.ERROR:
                errors += 1
                lines.append(f"[ERROR] {sdk_subdir.name}: {finding.message}")
            elif finding.severity == AuditSeverity.WARNING:
                lines.append(f"[WARN] {sdk_subdir.name}: {finding.message}")

    if not lines:
        lines.append(f"[OK] All SDKs passed audit")

    return errors == 0, errors, lines


def run_skills_audit(skills_dir: str, sdk_dir: str) -> tuple:
    """
    Run skills audit.
    Returns (passed, error_count, output_lines).
    """
    result = audit_skills(skills_dir, sdk_dir)

    errors = 0
    lines = []

    for finding in result.findings:
        if finding.severity == AuditSeverity.ERROR:
            errors += 1
            lines.append(f"[ERROR] {finding.message}")
        elif finding.severity == AuditSeverity.WARNING:
            lines.append(f"[WARN] {finding.message}")

    if not lines:
        lines.append("[OK] All skills passed audit")

    return errors == 0, errors, lines


def run_docs_audit(docs_dir: str, verbose: bool = False) -> tuple:
    """
    Run documentation audit.
    Returns (passed, error_count, output_lines).
    """
    result = audit_docs(docs_dir)

    errors = 0
    warnings = 0
    lines = []

    for finding in result.findings:
        if finding.severity == AuditSeverity.ERROR:
            errors += 1
            lines.append(f"[ERROR] {finding.message}")
        elif finding.severity == AuditSeverity.WARNING:
            warnings += 1
            lines.append(f"[WARN] {finding.message}")
        elif finding.severity == AuditSeverity.INFO and verbose:
            lines.append(f"[INFO] {finding.message}")

    if errors == 0 and warnings == 0:
        lines.append("[OK] All docs passed audit")

    return errors == 0, errors, lines


def print_section(title: str, lines: list, quiet: bool = False):
    """Print a section of the report."""
    if quiet and not any('[ERROR]' in l or '[WARN]' in l for l in lines):
        return

    print(f"\n## {title}\n")
    for line in lines:
        print(line)


def main():
    try:
        args = parse_args()
    except SystemExit as e:
        sys.exit(e.code)

    print("# Unified Audit Report\n")

    total_errors = 0
    scopes_run = []

    # Registry audit
    if args.scope in ['all', 'registry']:
        passed, errors, lines = audit_registry_tools(args.registry, args.fix)
        total_errors += errors
        scopes_run.append(('Registry Tools', passed, lines))

    # SDK audit
    if args.scope in ['all', 'sdk']:
        passed, errors, lines = audit_all_sdks(args.sdk_dir)
        total_errors += errors
        scopes_run.append(('SDK Packages', passed, lines))

    # Skills audit
    if args.scope in ['all', 'skills']:
        passed, errors, lines = run_skills_audit(args.skills_dir, args.sdk_dir)
        total_errors += errors
        scopes_run.append(('Skills', passed, lines))

    # Docs audit
    if args.scope in ['all', 'docs']:
        passed, errors, lines = run_docs_audit(args.docs_dir, args.verbose)
        total_errors += errors
        scopes_run.append(('Documentation', passed, lines))

    # Summary
    all_passed = total_errors == 0
    status = "ALL PASSED" if all_passed else f"{total_errors} ERRORS FOUND"
    print(f"**Status**: {status}")

    # Print each section
    for title, passed, lines in scopes_run:
        print_section(title, lines, args.quiet)

    # Final summary
    print("\n---")
    print(f"\n**Summary**: {len(scopes_run)} scopes audited, {total_errors} errors")

    sys.exit(0 if all_passed else 3)


if __name__ == "__main__":
    main()
