import argparse
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

def print_palette(tools: list):
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
    print_palette(tools)
    sys.exit(0)

if __name__ == "__main__":
    main()
