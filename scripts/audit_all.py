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
import json
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


# Error suggestions for common issues
ERROR_SUGGESTIONS = {
    "script_not_found": {
        "causes": ["Script file not created", "Path in registry is incorrect"],
        "fix": "Create the script file or fix the path in registry/tools.yaml",
        "doc": "core/docs/10_tooling_conventions.md"
    },
    "smoke_test_not_found": {
        "causes": ["Smoke test not created", "Naming convention not followed"],
        "fix": "Create scripts/smoke/smoke_<tool_name>.sh",
        "doc": "core/docs/10_tooling_conventions.md"
    },
    "manifest_not_found": {
        "causes": ["SDK structure incomplete", "manifest.yaml not created"],
        "fix": "Run: python sdks/infra-core/cli/main.py create-sdk <name>",
        "doc": "docs/60_sdk_specification.md"
    },
    "unknown_dependency": {
        "causes": ["Dependency tool not registered", "Tool ID typo"],
        "fix": "Register the dependency tool or fix the ID in depends_on",
        "doc": "registry/tools.yaml"
    },
    "missing_frontmatter": {
        "causes": ["Skill file missing YAML frontmatter", "Frontmatter format incorrect"],
        "fix": "Add valid YAML frontmatter with name and description fields",
        "doc": "core/docs/50_skills_system.md"
    }
}


def get_error_suggestion(error_type: str) -> dict:
    """Get suggestion for an error type."""
    return ERROR_SUGGESTIONS.get(error_type, {})


def format_error_with_suggestion(message: str, error_type: str = None, verbose: bool = False) -> list:
    """Format an error message with optional suggestion."""
    lines = [f"[ERROR] {message}"]

    if verbose and error_type:
        suggestion = get_error_suggestion(error_type)
        if suggestion:
            lines.append(f"        Causes: {', '.join(suggestion.get('causes', []))}")
            lines.append(f"        Fix: {suggestion.get('fix', 'N/A')}")
            lines.append(f"        Doc: {suggestion.get('doc', 'N/A')}")

    return lines


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
        help="Show detailed output including suggestions and INFO level"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    return parser.parse_args()


def audit_registry_tools(registry_path: str, fix: bool = False, verbose: bool = False) -> tuple:
    """
    Run registry audit (reuse existing logic).
    Returns (passed, error_count, output_lines, findings_list).
    """
    import yaml

    path = Path(registry_path)
    findings = []

    if not path.exists():
        findings.append({"severity": "error", "message": f"Registry not found: {registry_path}", "type": "registry_not_found"})
        return False, 1, [f"[ERROR] Registry not found: {registry_path}"], findings

    try:
        with open(path, 'r', encoding='utf-8') as f:
            tools = yaml.safe_load(f) or []
    except Exception as e:
        findings.append({"severity": "error", "message": f"Failed to load registry: {e}", "type": "load_error"})
        return False, 1, [f"[ERROR] Failed to load registry: {e}"], findings

    if not tools:
        findings.append({"severity": "info", "message": "No tools registered"})
        return True, 0, ["[INFO] No tools registered"], findings

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
                msg = f"{tool_id}: Script not found: {script_path}"
                lines.extend(format_error_with_suggestion(msg, "script_not_found", verbose))
                findings.append({"severity": "error", "message": msg, "type": "script_not_found", "tool": tool_id})

        # Check smoke test exists
        if entry:
            for part in entry.split():
                if part.endswith('.py'):
                    script_name = Path(part).stem
                    smoke_path = Path(f"scripts/smoke/smoke_{script_name}.sh")
                    if not smoke_path.exists():
                        errors += 1
                        msg = f"{tool_id}: Smoke test not found: {smoke_path}"
                        lines.extend(format_error_with_suggestion(msg, "smoke_test_not_found", verbose))
                        findings.append({"severity": "error", "message": msg, "type": "smoke_test_not_found", "tool": tool_id})
                    break

        # Check version
        if not tool.get('version'):
            msg = f"{tool_id}: Missing version field"
            lines.append(f"[WARN] {msg}")
            findings.append({"severity": "warning", "message": msg, "tool": tool_id})

        # Check dependencies
        for dep in tool.get('depends_on', []):
            if dep not in all_tool_ids:
                errors += 1
                msg = f"{tool_id}: Unknown dependency: {dep}"
                lines.extend(format_error_with_suggestion(msg, "unknown_dependency", verbose))
                findings.append({"severity": "error", "message": msg, "type": "unknown_dependency", "tool": tool_id})

    return errors == 0, errors, lines, findings


def audit_all_sdks(sdk_dir: str, verbose: bool = False) -> tuple:
    """
    Audit all SDK packages in the directory.
    Returns (passed, error_count, output_lines, findings_list).
    """
    sdk_path_dir = Path(sdk_dir)
    findings = []

    if not sdk_path_dir.exists():
        findings.append({"severity": "info", "message": "SDK directory not found, skipping"})
        return True, 0, ["[INFO] SDK directory not found, skipping"], findings

    errors = 0
    lines = []

    for sdk_subdir in sdk_path_dir.iterdir():
        if not sdk_subdir.is_dir():
            continue
        if sdk_subdir.name.startswith('.'):
            continue

        result = audit_sdk(sdk_subdir)

        for finding in result.findings:
            if finding.severity == AuditSeverity.ERROR:
                errors += 1
                msg = f"{sdk_subdir.name}: {finding.message}"
                error_type = "manifest_not_found" if "manifest" in finding.message.lower() else None
                lines.extend(format_error_with_suggestion(msg, error_type, verbose))
                findings.append({"severity": "error", "message": msg, "sdk": sdk_subdir.name})
            elif finding.severity == AuditSeverity.WARNING:
                lines.append(f"[WARN] {sdk_subdir.name}: {finding.message}")
                findings.append({"severity": "warning", "message": finding.message, "sdk": sdk_subdir.name})

    if not lines:
        lines.append("[OK] All SDKs passed audit")

    return errors == 0, errors, lines, findings


def run_skills_audit(skills_dir: str, sdk_dir: str, verbose: bool = False) -> tuple:
    """
    Run skills audit.
    Returns (passed, error_count, output_lines, findings_list).
    """
    result = audit_skills(skills_dir, sdk_dir)

    errors = 0
    lines = []
    findings = []

    for finding in result.findings:
        if finding.severity == AuditSeverity.ERROR:
            errors += 1
            error_type = "missing_frontmatter" if "frontmatter" in finding.message.lower() else None
            lines.extend(format_error_with_suggestion(finding.message, error_type, verbose))
            findings.append({"severity": "error", "message": finding.message})
        elif finding.severity == AuditSeverity.WARNING:
            lines.append(f"[WARN] {finding.message}")
            findings.append({"severity": "warning", "message": finding.message})

    if not lines:
        lines.append("[OK] All skills passed audit")

    return errors == 0, errors, lines, findings


def run_docs_audit(docs_dir: str, verbose: bool = False) -> tuple:
    """
    Run documentation audit.
    Returns (passed, error_count, output_lines, findings_list).
    """
    result = audit_docs(docs_dir)

    errors = 0
    warnings = 0
    lines = []
    findings = []

    for finding in result.findings:
        if finding.severity == AuditSeverity.ERROR:
            errors += 1
            lines.append(f"[ERROR] {finding.message}")
            findings.append({"severity": "error", "message": finding.message})
        elif finding.severity == AuditSeverity.WARNING:
            warnings += 1
            lines.append(f"[WARN] {finding.message}")
            findings.append({"severity": "warning", "message": finding.message})
        elif finding.severity == AuditSeverity.INFO and verbose:
            lines.append(f"[INFO] {finding.message}")
            findings.append({"severity": "info", "message": finding.message})

    if errors == 0 and warnings == 0:
        lines.append("[OK] All docs passed audit")

    return errors == 0, errors, lines, findings


def print_section(title: str, lines: list, quiet: bool = False):
    """Print a section of the report."""
    if quiet and not any('[ERROR]' in l or '[WARN]' in l for l in lines):
        return

    print(f"\n## {title}\n")
    for line in lines:
        print(line)


def output_json_report(scopes_results: list, total_errors: int):
    """Output the audit report in JSON format."""
    report = {
        "status": "passed" if total_errors == 0 else "failed",
        "total_errors": total_errors,
        "scopes": []
    }

    for title, passed, lines, findings in scopes_results:
        report["scopes"].append({
            "name": title,
            "passed": passed,
            "findings": findings
        })

    print(json.dumps(report, ensure_ascii=False, indent=2))


def main():
    try:
        args = parse_args()
    except SystemExit as e:
        sys.exit(e.code)

    total_errors = 0
    scopes_results = []

    # Registry audit
    if args.scope in ['all', 'registry']:
        passed, errors, lines, findings = audit_registry_tools(args.registry, args.fix, args.verbose)
        total_errors += errors
        scopes_results.append(('Registry Tools', passed, lines, findings))

    # SDK audit
    if args.scope in ['all', 'sdk']:
        passed, errors, lines, findings = audit_all_sdks(args.sdk_dir, args.verbose)
        total_errors += errors
        scopes_results.append(('SDK Packages', passed, lines, findings))

    # Skills audit
    if args.scope in ['all', 'skills']:
        passed, errors, lines, findings = run_skills_audit(args.skills_dir, args.sdk_dir, args.verbose)
        total_errors += errors
        scopes_results.append(('Skills', passed, lines, findings))

    # Docs audit
    if args.scope in ['all', 'docs']:
        passed, errors, lines, findings = run_docs_audit(args.docs_dir, args.verbose)
        total_errors += errors
        scopes_results.append(('Documentation', passed, lines, findings))

    # Output
    if args.json:
        output_json_report(scopes_results, total_errors)
    else:
        print("# Unified Audit Report\n")

        all_passed = total_errors == 0
        status = "ALL PASSED" if all_passed else f"{total_errors} ERRORS FOUND"
        print(f"**Status**: {status}")

        # Print each section
        for title, passed, lines, findings in scopes_results:
            print_section(title, lines, args.quiet)

        # Final summary
        print("\n---")
        print(f"\n**Summary**: {len(scopes_results)} scopes audited, {total_errors} errors")

        if total_errors > 0 and not args.verbose:
            print("\nTip: Run with --verbose for fix suggestions")

    sys.exit(0 if total_errors == 0 else 3)


if __name__ == "__main__":
    main()
