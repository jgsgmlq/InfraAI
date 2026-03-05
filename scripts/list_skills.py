#!/usr/bin/env python3
"""
List Skills Tool

Lists all available skills from core, project, and external locations.
Outputs a summary for AI to understand available capabilities.

Exit codes:
    0 - Success
    2 - Parameter error
    3 - Runtime error
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def parse_args():
    parser = argparse.ArgumentParser(
        description="List all available skills"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show full skill content including trigger phrases"
    )
    parser.add_argument(
        "--location",
        type=str,
        choices=["all", "core", "project", "external"],
        default="all",
        help="Filter by skill location (default: all)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Output in compact table format"
    )
    return parser.parse_args()


def find_skill_files() -> dict:
    """Find all skill files in standard locations."""
    locations = {
        "core": Path("core/.agent/skills"),
        "project": Path("project/.agent/skills"),
        "external": Path("project/.agent/external"),
    }

    skills = {}
    for loc_name, loc_path in locations.items():
        skills[loc_name] = []
        if loc_path.exists():
            for f in loc_path.glob("*.md"):
                if f.name.startswith("_") or f.name == "README.md":
                    continue
                skills[loc_name].append(f)

    return skills


def parse_skill_file(file_path: Path) -> dict:
    """Parse a skill file and extract key information."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return {"name": file_path.stem, "error": str(e)}

    skill = {
        "name": file_path.stem,
        "file": str(file_path),
        "title": "",
        "purpose": "",
        "triggers": [],
        "command": "",
    }

    # Extract title (first # heading)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        skill["title"] = title_match.group(1).strip()

    # Extract purpose
    purpose_match = re.search(r'## Purpose\s*\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
    if purpose_match:
        skill["purpose"] = purpose_match.group(1).strip().split('\n')[0]

    # Extract trigger phrases
    trigger_match = re.search(r'## Trigger Phrases\s*\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
    if trigger_match:
        trigger_text = trigger_match.group(1)
        triggers = re.findall(r'[-*]\s*["\'](.+?)["\']', trigger_text)
        skill["triggers"] = triggers[:5]  # Limit to 5

    # Extract command
    command_match = re.search(r'```bash\s*\n(.+?)\n```', content, re.DOTALL)
    if command_match:
        # Get first non-comment line
        for line in command_match.group(1).split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                skill["command"] = line
                break

    return skill


def output_json(skills: dict, location_filter: str):
    """Output skills in JSON format."""
    result = {"skills": [], "count": 0}

    for loc_name, files in skills.items():
        if location_filter != "all" and location_filter != loc_name:
            continue

        for f in sorted(files):
            skill = parse_skill_file(f)
            result["skills"].append({
                "id": skill["name"],
                "title": skill.get("title", ""),
                "purpose": skill.get("purpose", ""),
                "location": loc_name,
                "triggers": skill.get("triggers", []),
                "command": skill.get("command", "")
            })

    result["count"] = len(result["skills"])
    print(json.dumps(result, ensure_ascii=False, indent=2))


def output_compact(skills: dict, location_filter: str):
    """Output skills in compact table format."""
    all_skills = []

    for loc_name, files in skills.items():
        if location_filter != "all" and location_filter != loc_name:
            continue

        for f in sorted(files):
            skill = parse_skill_file(f)
            all_skills.append((loc_name, skill))

    if not all_skills:
        print("No skills found.")
        return

    print(f"{'ID':<25} {'TITLE':<30} {'LOCATION':<10}")
    print("-" * 65)
    for loc_name, skill in all_skills:
        skill_id = skill["name"][:25]
        title = (skill.get("title") or skill["name"])[:30]
        print(f"{skill_id:<25} {title:<30} {loc_name:<10}")

    print(f"\nTotal: {len(all_skills)} skills")


def print_skills(skills: dict, verbose: bool, location_filter: str):
    """Print skills in Markdown format."""
    print("# Available Skills\n")

    total = 0
    for loc_name, files in skills.items():
        if location_filter != "all" and location_filter != loc_name:
            continue

        if not files:
            continue

        total += len(files)
        loc_labels = {
            "core": "Core Framework Skills",
            "project": "Project Skills",
            "external": "External Skills"
        }

        print(f"## {loc_labels.get(loc_name, loc_name)} ({len(files)})\n")

        for f in sorted(files):
            skill = parse_skill_file(f)

            print(f"### {skill['title'] or skill['name']}")
            print(f"**ID**: `{skill['name']}`")
            if skill.get("purpose"):
                print(f"**Purpose**: {skill['purpose']}")

            if verbose:
                if skill.get("triggers"):
                    print(f"**Triggers**: {', '.join(skill['triggers'])}")
                if skill.get("command"):
                    print(f"**Command**: `{skill['command']}`")

            print()

    print(f"---\n**Total**: {total} skills")


def main():
    try:
        args = parse_args()
    except SystemExit as e:
        sys.exit(e.code)

    skills = find_skill_files()

    if args.json:
        output_json(skills, args.location)
    elif args.compact:
        output_compact(skills, args.location)
    else:
        print_skills(skills, args.verbose, args.location)

    sys.exit(0)


if __name__ == "__main__":
    main()
