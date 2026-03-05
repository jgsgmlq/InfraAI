#!/usr/bin/env python3
"""
Registry Audit Tool

Checks the health of the tool registry:
- Verifies each registered tool has a corresponding script file
- Verifies each tool has a smoke test
- Verifies each tool has a skill document
- Outputs a health report in Markdown format

Exit codes:
    0 - All checks passed
    2 - Parameter error
    3 - Runtime error (missing files, etc.)
"""

import argparse
import sys
import yaml
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def parse_args():
    parser = argparse.ArgumentParser(
        description="Audit the tool registry for completeness and consistency"
    )
    parser.add_argument(
        "--registry",
        type=str,
        default="registry/tools.yaml",
        help="Path to the tool registry YAML file"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Generate template files for missing components"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only output errors, no success messages"
    )
    return parser.parse_args()


def load_registry(registry_path: str) -> list:
    """Load and parse the registry YAML file."""
    path = Path(registry_path)
    if not path.exists():
        sys.stderr.write(f"Error: Registry file not found at {registry_path}\n")
        sys.exit(3)

    try:
        with open(path, 'r', encoding='utf-8') as f:
            registry = yaml.safe_load(f)
            return registry if registry else []
    except Exception as e:
        sys.stderr.write(f"Error reading registry: {e}\n")
        sys.exit(3)


def extract_script_name(entry: str) -> str:
    """Extract script filename from entry command."""
    # e.g., "python scripts/list_tools.py" -> "list_tools"
    parts = entry.split()
    for part in parts:
        if part.endswith('.py'):
            return Path(part).stem
    return None


def check_tool(tool: dict, all_tool_ids: set, fix: bool = False) -> dict:
    """
    Check a single tool for completeness.
    Returns a dict with check results.
    """
    tool_id = tool.get('id', 'unknown')
    tool_name = tool.get('name', 'Unknown')
    entry = tool.get('entry', '')

    result = {
        'id': tool_id,
        'name': tool_name,
        'checks': {
            'script': {'passed': False, 'path': None, 'message': ''},
            'smoke_test': {'passed': False, 'path': None, 'message': ''},
            'skill_doc': {'passed': False, 'path': None, 'message': ''},
            'version': {'passed': False, 'message': ''},
            'dependencies': {'passed': True, 'message': 'No dependencies'},
        },
        'all_passed': False
    }

    script_name = extract_script_name(entry)

    # Check 1: Script file exists
    if entry:
        # Extract path from entry (e.g., "python scripts/list_tools.py")
        script_path = None
        for part in entry.split():
            if part.endswith('.py'):
                script_path = Path(part)
                break

        if script_path and script_path.exists():
            result['checks']['script']['passed'] = True
            result['checks']['script']['path'] = str(script_path)
            result['checks']['script']['message'] = 'Found'
        else:
            result['checks']['script']['message'] = f'Missing: {script_path}'
    else:
        result['checks']['script']['message'] = 'No entry defined'

    # Check 2: Smoke test exists
    if script_name:
        smoke_path = Path(f"scripts/smoke/smoke_{script_name}.sh")
        if smoke_path.exists():
            result['checks']['smoke_test']['passed'] = True
            result['checks']['smoke_test']['path'] = str(smoke_path)
            result['checks']['smoke_test']['message'] = 'Found'
        else:
            result['checks']['smoke_test']['message'] = f'Missing: {smoke_path}'
            if fix:
                create_smoke_template(script_name, entry)
                result['checks']['smoke_test']['message'] += ' (template created)'
    else:
        result['checks']['smoke_test']['message'] = 'Cannot determine script name'

    # Check 3: Skill document exists
    # Try multiple naming conventions and locations
    skill_paths = [
        # Core skills (primary)
        Path(f"core/.agent/skills/{tool_id}.md"),
        Path(f"core/.agent/skills/{tool_id.replace('-', '_')}.md"),
        # Project skills
        Path(f"project/.agent/skills/{tool_id}.md"),
        Path(f"project/.agent/external/{tool_id}.md"),
        # Legacy location (backward compatibility)
        Path(f".agent/skills/{tool_id}.md"),
    ]
    if script_name:
        skill_paths.append(Path(f"core/.agent/skills/{script_name}.md"))
        skill_paths.append(Path(f"project/.agent/skills/{script_name}.md"))

    skill_found = False
    for skill_path in skill_paths:
        if skill_path.exists():
            result['checks']['skill_doc']['passed'] = True
            result['checks']['skill_doc']['path'] = str(skill_path)
            result['checks']['skill_doc']['message'] = 'Found'
            skill_found = True
            break

    if not skill_found:
        result['checks']['skill_doc']['message'] = f'Missing: core/.agent/skills/{tool_id}.md'
        if fix:
            create_skill_template(tool_id, tool_name, tool.get('description', ''))
            result['checks']['skill_doc']['message'] += ' (template created)'

    # Check 4: Version field exists
    if tool.get('version'):
        result['checks']['version']['passed'] = True
        result['checks']['version']['message'] = f"v{tool.get('version')}"
    else:
        result['checks']['version']['message'] = 'Missing version field'

    # Check 5: Dependencies exist
    depends_on = tool.get('depends_on', [])
    if depends_on:
        missing_deps = [dep for dep in depends_on if dep not in all_tool_ids]
        if missing_deps:
            result['checks']['dependencies']['passed'] = False
            result['checks']['dependencies']['message'] = f"Missing: {', '.join(missing_deps)}"
        else:
            result['checks']['dependencies']['passed'] = True
            result['checks']['dependencies']['message'] = f"OK ({len(depends_on)} deps)"

    # Overall status
    result['all_passed'] = all(
        check['passed'] for check in result['checks'].values()
    )

    return result


def create_smoke_template(script_name: str, entry: str):
    """Create a template smoke test file."""
    smoke_dir = Path("scripts/smoke")
    smoke_dir.mkdir(parents=True, exist_ok=True)

    smoke_path = smoke_dir / f"smoke_{script_name}.sh"
    template = f'''#!/usr/bin/env bash

# Smoke test for {script_name}.py

echo "Running smoke tests for {script_name}.py..."

# Test 1: Successful execution
echo "[Test 1] Running with default arguments"
{entry} > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 1 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 1 Passed"

# Test 2: Help flag
echo "[Test 2] Verify --help output"
{entry} --help > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 2 Failed! Expected exit code 0 for help, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 2 Passed"

echo "All smoke tests passed successfully!"
exit 0
'''

    with open(smoke_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(template)


def create_skill_template(tool_id: str, tool_name: str, description: str):
    """Create a template skill document in core/.agent/skills/."""
    skill_dir = Path("core/.agent/skills")
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_path = skill_dir / f"{tool_id}.md"
    template = f'''# {tool_name}

## Purpose
{description if description else '[Describe what this tool does]'}

## When to Use
[Under what conditions should the AI trigger this tool?]

## Trigger Phrases
When the user says:
- "[Example phrase 1]"
- "[Example phrase 2]"

## Principles
1. [Core rule 1]
2. [Core rule 2]

## Recovery Strategy
- Exit 2 (Parameter Error): Check command syntax, show --help
- Exit 3 (Runtime Error): [Describe recovery steps]

## HARD GATES (Non-Negotiable)
- [ ] [Required condition 1]
- [ ] [Required condition 2]
'''

    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(template)


def print_report(results: list, quiet: bool = False):
    """Print the audit report in Markdown format."""
    total = len(results)
    passed = sum(1 for r in results if r['all_passed'])
    failed = total - passed

    print("# Registry Audit Report\n")

    # Summary
    if failed == 0:
        print(f"**Status**: ALL PASSED ({total} tools)\n")
    else:
        print(f"**Status**: {failed} ISSUES FOUND\n")
        print(f"- Total tools: {total}")
        print(f"- Passed: {passed}")
        print(f"- Failed: {failed}\n")

    # Details
    print("## Tool Details\n")

    for result in results:
        status_icon = "PASS" if result['all_passed'] else "FAIL"
        print(f"### {status_icon} {result['name']} (`{result['id']}`)\n")

        if quiet and result['all_passed']:
            continue

        print("| Check | Status | Details |")
        print("|-------|--------|---------|")

        check_names = {
            'script': 'Script File',
            'smoke_test': 'Smoke Test',
            'skill_doc': 'Skill Doc',
            'version': 'Version',
            'dependencies': 'Dependencies'
        }

        for key, check in result['checks'].items():
            icon = "PASS" if check['passed'] else "FAIL"
            print(f"| {check_names[key]} | {icon} | {check['message']} |")

        print()

    # Return exit code
    return 0 if failed == 0 else 3


def main():
    try:
        args = parse_args()
    except SystemExit as e:
        sys.exit(e.code)

    tools = load_registry(args.registry)

    if not tools:
        print("# Registry Audit Report\n")
        print("**Status**: No tools registered.\n")
        sys.exit(0)

    # Collect all tool IDs for dependency checking
    all_tool_ids = {tool.get('id') for tool in tools if tool.get('id')}

    results = [check_tool(tool, all_tool_ids, fix=args.fix) for tool in tools]
    exit_code = print_report(results, quiet=args.quiet)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
