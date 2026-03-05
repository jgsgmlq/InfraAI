"""
SDK Scaffold module.

Provides functions to create new SDK packages with proper structure.
"""

from pathlib import Path
from typing import Optional
from datetime import date


def create_sdk(
    sdk_name: str,
    target_dir: str = "sdks",
    description: str = "",
    author: str = "AI Infrastructure Team",
    version: str = "1.0.0",
    dry_run: bool = False
) -> dict:
    """
    Create a new SDK package with standard structure.

    Args:
        sdk_name: Name of the SDK (kebab-case, e.g., 'my-sdk')
        target_dir: Directory to create SDK in (default: 'sdks')
        description: SDK description
        author: Author name
        version: Initial version
        dry_run: If True, only show what would be created

    Returns:
        dict with 'success', 'path', 'files_created', 'message'
    """
    # Validate SDK name (kebab-case)
    if not sdk_name or not sdk_name.replace('-', '').replace('_', '').isalnum():
        return {
            'success': False,
            'path': None,
            'files_created': [],
            'message': f"Invalid SDK name: {sdk_name}. Use kebab-case (e.g., 'my-sdk')"
        }

    sdk_path = Path(target_dir) / sdk_name
    files_to_create = []

    # Check if already exists
    if sdk_path.exists() and not dry_run:
        return {
            'success': False,
            'path': str(sdk_path),
            'files_created': [],
            'message': f"SDK already exists: {sdk_path}"
        }

    # Define files to create
    today = date.today().isoformat()

    files = {
        "__init__.py": f'''"""
{sdk_name} SDK

{description if description else 'SDK description here.'}
"""

try:
    from .version import __version__, __version_info__
except ImportError:
    __version__ = "{version}"
    __version_info__ = tuple(int(x) for x in "{version}".split('.'))

__all__ = [
    "__version__",
    "__version_info__",
]
''',

        "version.py": f'''"""Version information for {sdk_name} SDK."""

__version__ = "{version}"
__version_info__ = tuple(int(x) for x in __version__.split('.'))
''',

        "manifest.yaml": f'''name: {sdk_name}
version: "{version}"
description: {description if description else 'SDK description'}
author: {author}
license: MIT

dependencies:
  python: ">=3.8"
  packages: []

exports:
  api: []
  cli: []
  skills: []
''',

        "README.md": f'''# {sdk_name} SDK

{description if description else 'SDK description here.'}

## Installation

```bash
pip install -e sdks/{sdk_name}
```

## Usage

### Python API

```python
# Import from the SDK
from {sdk_name.replace('-', '_')}.api import your_function
```

### CLI

```bash
{sdk_name} --help
```

## Development

### Run tests

```bash
python -m pytest sdks/{sdk_name}/tests/ -v
```

## License

MIT
''',

        "CHANGELOG.md": f'''# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [{version}] - {today}

### Added

- Initial release
''',

        "api/__init__.py": f'''"""{sdk_name} API exports."""

__all__ = []
''',

        "cli/__init__.py": f'''"""{sdk_name} CLI module."""
''',

        "cli/main.py": f'''#!/usr/bin/env python3
"""
{sdk_name} CLI

Command-line interface for {sdk_name}.
"""

import argparse
import sys
from pathlib import Path

# Add SDK root to path
sdk_root = Path(__file__).parent.parent
sys.path.insert(0, str(sdk_root))

from version import __version__


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="{sdk_name}",
        description="{description if description else 'SDK CLI'}"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{sdk_name} {{__version__}}"
    )

    args = parser.parse_args()

    # No subcommand provided
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
''',

        "skills/.gitkeep": "",

        "tests/__init__.py": f'''"""{sdk_name} tests."""
''',

        "tests/test_placeholder.py": f'''"""Placeholder tests for {sdk_name}."""

import pytest


def test_placeholder():
    """Remove this once real tests are added."""
    assert True
''',

        "examples/.gitkeep": "",
    }

    # Create files
    files_created = []

    if dry_run:
        for filepath in files.keys():
            full_path = sdk_path / filepath
            files_created.append(str(full_path))
    else:
        # Create directories
        for subdir in ['api', 'cli', 'skills', 'tests', 'examples']:
            (sdk_path / subdir).mkdir(parents=True, exist_ok=True)

        # Write files
        for filepath, content in files.items():
            full_path = sdk_path / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding='utf-8')
            files_created.append(str(full_path))

    return {
        'success': True,
        'path': str(sdk_path),
        'files_created': files_created,
        'message': f"SDK created at {sdk_path}" if not dry_run else f"Would create SDK at {sdk_path}"
    }
