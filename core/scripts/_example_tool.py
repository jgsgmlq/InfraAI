#!/usr/bin/env python3
"""
Example Tool Template
=====================

This is a reference implementation demonstrating the standard structure
for CLI tools in this framework. Copy this file when creating new tools.

USAGE:
    1. Copy this file: cp _example_tool.py my_new_tool.py
    2. Update the docstring and description
    3. Modify parse_args() for your CLI interface
    4. Implement your logic in main()
    5. Register in registry/tools.yaml
    6. Create smoke test and skill doc

Exit codes (MUST follow this convention):
    0 - Success
    2 - Parameter error (bad arguments, --help)
    3 - Runtime error (file not found, network error, etc.)
"""

# =============================================================================
# IMPORTS
# Standard library imports only - avoid heavy dependencies
# =============================================================================
import argparse
import sys
from pathlib import Path

# Third-party imports (if needed)
# import yaml  # Already in requirements.txt


# =============================================================================
# ARGUMENT PARSING
# Use argparse for consistent CLI interface
# =============================================================================
def parse_args():
    """
    Parse command-line arguments.

    CONVENTIONS:
    - Always include --help (automatic with argparse)
    - Use -- prefix for optional flags
    - Use lowercase with hyphens for flag names
    - Provide clear help text for each argument
    """
    parser = argparse.ArgumentParser(
        # Brief description shown in --help
        description="Example tool demonstrating standard CLI structure",

        # Additional text shown after arguments in --help
        epilog="Example: python scripts/_example_tool.py --input data.txt"
    )

    # Required positional argument (uncomment if needed)
    # parser.add_argument(
    #     "input_file",
    #     type=str,
    #     help="Path to the input file (required)"
    # )

    # Optional flag with value
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Path to input file (optional)"
    )

    # Optional flag with value and choices
    parser.add_argument(
        "--format",
        type=str,
        choices=["json", "yaml", "text"],
        default="text",
        help="Output format (default: text)"
    )

    # Boolean flag (store_true = default False, becomes True if flag present)
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    # Boolean flag for dry-run (recommended for tools that modify state)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )

    return parser.parse_args()


# =============================================================================
# HELPER FUNCTIONS
# Keep functions small and focused
# =============================================================================
def log_verbose(message: str, verbose: bool):
    """
    Print message only if verbose mode is enabled.

    WHY: Separates debug/info output from main output,
    making it easier to parse tool output programmatically.
    """
    if verbose:
        # Use stderr for logging, keep stdout for main output
        sys.stderr.write(f"[INFO] {message}\n")


def log_error(message: str):
    """
    Print error message to stderr.

    WHY: MUST use stderr for errors so that:
    1. Errors are visible even when stdout is redirected
    2. Exit code + stderr = clear error reporting
    """
    sys.stderr.write(f"[ERROR] {message}\n")


def validate_input(input_path: str) -> bool:
    """
    Validate input file exists.

    WHY: Fail fast with clear error messages.
    Always validate inputs before processing.
    """
    if input_path is None:
        return True  # No input specified, that's OK for this example

    path = Path(input_path)
    if not path.exists():
        log_error(f"Input file not found: {input_path}")
        return False

    return True


def process_data(input_path: str, output_format: str, verbose: bool) -> dict:
    """
    Main processing logic.

    WHY: Separate business logic from CLI handling.
    This makes the code easier to test and reuse.
    """
    log_verbose(f"Processing input: {input_path}", verbose)
    log_verbose(f"Output format: {output_format}", verbose)

    # Your actual logic goes here
    result = {
        "status": "success",
        "input": input_path,
        "format": output_format
    }

    return result


def format_output(data: dict, output_format: str) -> str:
    """
    Format output based on requested format.

    WHY: Support multiple output formats for flexibility.
    JSON is good for programmatic consumption,
    text is good for human reading.
    """
    if output_format == "json":
        import json
        return json.dumps(data, indent=2)
    elif output_format == "yaml":
        # Only import yaml if needed
        import yaml
        return yaml.dump(data, default_flow_style=False)
    else:  # text
        lines = [f"{k}: {v}" for k, v in data.items()]
        return "\n".join(lines)


# =============================================================================
# MAIN FUNCTION
# Entry point - handle errors and exit codes
# =============================================================================
def main():
    """
    Main entry point.

    STRUCTURE:
    1. Parse arguments (exit 2 on error - handled by argparse)
    2. Validate inputs (exit 3 on error)
    3. Process data (exit 3 on error)
    4. Output results (exit 0 on success)
    """
    # Step 1: Parse arguments
    # argparse automatically exits with code 2 for bad arguments
    try:
        args = parse_args()
    except SystemExit as e:
        # Preserve argparse exit code (2 for errors, 0 for --help)
        sys.exit(e.code)

    # Step 2: Validate inputs
    if not validate_input(args.input):
        sys.exit(3)  # Runtime error - file not found

    # Step 3: Check dry-run mode
    if args.dry_run:
        log_verbose("Dry-run mode: no changes will be made", True)
        print("Dry-run: would process input and generate output")
        sys.exit(0)

    # Step 4: Process data
    try:
        result = process_data(args.input, args.format, args.verbose)
    except Exception as e:
        log_error(f"Processing failed: {e}")
        sys.exit(3)  # Runtime error

    # Step 5: Output results
    output = format_output(result, args.format)
    print(output)

    # Step 6: Exit successfully
    sys.exit(0)


# =============================================================================
# SCRIPT ENTRY POINT
# Standard Python idiom for executable scripts
# =============================================================================
if __name__ == "__main__":
    main()
