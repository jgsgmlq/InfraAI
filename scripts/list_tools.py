import argparse
import json
import sys
import yaml
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def parse_args():
    parser = argparse.ArgumentParser(
        description="Command Palette: List available tools registered in the infrastructure"
    )
    parser.add_argument(
        "--registry",
        type=str,
        default="registry/tools.yaml",
        help="Path to the tool registry YAML file"
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

def load_registry(registry_path: str) -> list:
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


def output_json(tools: list):
    """Output tools in JSON format."""
    result = {
        "tools": [
            {
                "id": t.get("id", ""),
                "name": t.get("name", ""),
                "version": t.get("version", ""),
                "description": t.get("description", ""),
                "command": t.get("entry", ""),
                "aliases": t.get("aliases", []),
                "deprecated": t.get("deprecated", False)
            }
            for t in tools
        ],
        "count": len(tools)
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def output_compact(tools: list):
    """Output tools in compact table format."""
    if not tools:
        print("No tools registered.")
        return

    print(f"{'ID':<20} {'NAME':<25} {'VERSION':<10}")
    print("-" * 55)
    for t in tools:
        tool_id = t.get('id', '')[:20]
        name = t.get('name', '')[:25]
        version = t.get('version', '')[:10]
        deprecated = " [D]" if t.get('deprecated') else ""
        print(f"{tool_id:<20} {name:<25} {version:<10}{deprecated}")
    print(f"\nTotal: {len(tools)} tools")


def print_palette(tools: list):
    """Output tools in full markdown format."""
    print("# Command Palette\n")
    if not tools:
        print("No tools registered.")
        return

    for tool in tools:
        # Header with version
        version = tool.get('version', '')
        version_str = f" v{version}" if version else ""
        deprecated = " [DEPRECATED]" if tool.get('deprecated') else ""
        print(f"## {tool.get('name', 'Unknown')} ({tool.get('id', 'unknown')}){version_str}{deprecated}")

        print(f"**Description**: {tool.get('description', '')}")
        print(f"**Type**: {tool.get('type', 'cli')}")
        print(f"**Command**: `{tool.get('entry', '')}`")

        # Aliases (natural language)
        aliases = tool.get('aliases', [])
        if aliases:
            print(f"**Aliases**: {', '.join(aliases)}")

        # Dependencies
        depends_on = tool.get('depends_on', [])
        if depends_on:
            print(f"**Depends on**: {', '.join(depends_on)}")

        print()  # Empty line after metadata

        flags = tool.get('flags', [])
        if flags:
            print("### Flags:")
            for flag in flags:
                req = "(Required)" if flag.get('required') else "(Optional)"
                print(f"- `{flag.get('name')}`: {flag.get('description')} {req}")
            print()

        examples = tool.get('examples', [])
        if examples:
            print("### Examples:")
            for eg in examples:
                print(f"  {eg}")
            print()

        print("---")


def main():
    try:
        args = parse_args()
    except SystemExit as e:
        # argparse uses exit code 2 for parameter errors
        sys.exit(e.code)

    tools = load_registry(args.registry)

    if args.json:
        output_json(tools)
    elif args.compact:
        output_compact(tools)
    else:
        print_palette(tools)

    sys.exit(0)

if __name__ == "__main__":
    main()
