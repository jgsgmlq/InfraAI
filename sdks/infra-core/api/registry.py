"""
Registry management module.

Provides functions to load, validate, and query tool registries.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union

import yaml


class RegistryError(Exception):
    """Base exception for registry operations."""
    pass


class RegistryNotFoundError(RegistryError):
    """Registry file not found."""
    pass


class RegistryValidationError(RegistryError):
    """Registry validation failed."""
    pass


def load_registry(path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Load a registry file.

    Args:
        path: Path to the registry YAML file.

    Returns:
        List of tool entries.

    Raises:
        RegistryNotFoundError: If the file doesn't exist.
        RegistryError: If the file can't be parsed.
    """
    path = Path(path)

    if not path.exists():
        raise RegistryNotFoundError(f"Registry not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise RegistryError(f"Failed to parse registry: {e}")

    if data is None:
        return []

    if not isinstance(data, list):
        raise RegistryError("Registry must be a list of tools")

    return data


def validate_registry(
    tools: List[Dict[str, Any]],
    strict: bool = False
) -> Tuple[bool, List[str]]:
    """
    Validate registry entries.

    Args:
        tools: List of tool entries to validate.
        strict: If True, treat warnings as errors.

    Returns:
        Tuple of (is_valid, list_of_issues).
    """
    required_fields = ["id", "name", "entry", "description"]
    recommended_fields = ["version", "aliases", "examples"]

    issues = []

    for i, tool in enumerate(tools):
        tool_id = tool.get("id", f"tool[{i}]")

        # Check required fields
        for field in required_fields:
            if field not in tool:
                issues.append(f"[ERROR] {tool_id}: missing required field '{field}'")

        # Check recommended fields (warnings)
        if strict:
            for field in recommended_fields:
                if field not in tool:
                    issues.append(f"[WARN] {tool_id}: missing recommended field '{field}'")

    # Check for duplicate IDs
    ids = [t.get("id") for t in tools if t.get("id")]
    duplicates = set(x for x in ids if ids.count(x) > 1)
    for dup in duplicates:
        issues.append(f"[ERROR] Duplicate tool ID: '{dup}'")

    has_errors = any("[ERROR]" in issue for issue in issues)

    return (not has_errors, issues)
