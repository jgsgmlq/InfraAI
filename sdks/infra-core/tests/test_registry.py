"""Tests for registry module."""

import pytest
import tempfile
import os
import sys
from pathlib import Path

# Add the api directory to path for direct import
api_path = Path(__file__).parent.parent / "api"
sys.path.insert(0, str(api_path))

from registry import (
    load_registry,
    validate_registry,
    RegistryError,
    RegistryNotFoundError,
)


class TestLoadRegistry:
    """Tests for load_registry function."""

    def test_load_registry_success(self):
        """Test loading a valid registry file."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.yaml', delete=False, encoding='utf-8'
        ) as f:
            f.write("""
- id: test-tool
  name: Test Tool
  entry: python test.py
  description: A test tool
""")
            f.flush()
            temp_path = f.name

        try:
            result = load_registry(temp_path)
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0]['id'] == 'test-tool'
            assert result[0]['name'] == 'Test Tool'
        finally:
            os.unlink(temp_path)

    def test_load_registry_not_found(self):
        """Test loading non-existent registry file."""
        with pytest.raises(RegistryNotFoundError) as exc_info:
            load_registry('/nonexistent/path/registry.yaml')
        assert 'not found' in str(exc_info.value).lower()

    def test_load_registry_empty_file(self):
        """Test loading an empty registry file."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.yaml', delete=False, encoding='utf-8'
        ) as f:
            f.write("")
            temp_path = f.name

        try:
            result = load_registry(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_load_registry_invalid_yaml(self):
        """Test loading a file with invalid YAML syntax."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.yaml', delete=False, encoding='utf-8'
        ) as f:
            f.write("invalid: yaml: content: [")
            temp_path = f.name

        try:
            with pytest.raises(RegistryError) as exc_info:
                load_registry(temp_path)
            assert 'parse' in str(exc_info.value).lower()
        finally:
            os.unlink(temp_path)

    def test_load_registry_not_a_list(self):
        """Test loading a registry that is not a list."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.yaml', delete=False, encoding='utf-8'
        ) as f:
            f.write("key: value\nanother: thing")
            temp_path = f.name

        try:
            with pytest.raises(RegistryError) as exc_info:
                load_registry(temp_path)
            assert 'list' in str(exc_info.value).lower()
        finally:
            os.unlink(temp_path)

    def test_load_registry_multiple_tools(self):
        """Test loading a registry with multiple tools."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.yaml', delete=False, encoding='utf-8'
        ) as f:
            f.write("""
- id: tool-1
  name: Tool 1
  entry: python tool1.py
  description: First tool
- id: tool-2
  name: Tool 2
  entry: python tool2.py
  description: Second tool
- id: tool-3
  name: Tool 3
  entry: python tool3.py
  description: Third tool
""")
            temp_path = f.name

        try:
            result = load_registry(temp_path)
            assert len(result) == 3
            assert result[0]['id'] == 'tool-1'
            assert result[1]['id'] == 'tool-2'
            assert result[2]['id'] == 'tool-3'
        finally:
            os.unlink(temp_path)


class TestValidateRegistry:
    """Tests for validate_registry function."""

    def test_validate_registry_valid(self):
        """Test validating a correct registry."""
        tools = [
            {
                'id': 'test-tool',
                'name': 'Test Tool',
                'entry': 'python test.py',
                'description': 'A test tool'
            }
        ]
        is_valid, issues = validate_registry(tools)
        assert is_valid is True
        assert len(issues) == 0

    def test_validate_registry_missing_fields(self):
        """Test validating registry with missing required fields."""
        tools = [
            {
                'id': 'incomplete-tool',
                # missing: name, entry, description
            }
        ]
        is_valid, issues = validate_registry(tools)
        assert is_valid is False
        assert len(issues) == 3  # missing name, entry, description
        assert any('name' in issue for issue in issues)
        assert any('entry' in issue for issue in issues)
        assert any('description' in issue for issue in issues)

    def test_validate_registry_missing_id(self):
        """Test validating registry where tool is missing id."""
        tools = [
            {
                'name': 'No ID Tool',
                'entry': 'python test.py',
                'description': 'Tool without ID'
            }
        ]
        is_valid, issues = validate_registry(tools)
        assert is_valid is False
        assert any('id' in issue.lower() for issue in issues)

    def test_validate_registry_duplicate_ids(self):
        """Test validating registry with duplicate tool IDs."""
        tools = [
            {'id': 'dup-tool', 'name': 'Tool 1', 'entry': 'a.py', 'description': 'First'},
            {'id': 'dup-tool', 'name': 'Tool 2', 'entry': 'b.py', 'description': 'Second'},
        ]
        is_valid, issues = validate_registry(tools)
        assert is_valid is False
        assert any('duplicate' in issue.lower() for issue in issues)

    def test_validate_registry_strict_mode(self):
        """Test strict mode warns about missing recommended fields."""
        tools = [
            {
                'id': 'basic-tool',
                'name': 'Basic Tool',
                'entry': 'python basic.py',
                'description': 'A basic tool'
                # missing: version, aliases, examples (recommended)
            }
        ]
        # Non-strict mode: should pass
        is_valid, issues = validate_registry(tools, strict=False)
        assert is_valid is True
        assert len(issues) == 0

        # Strict mode: should have warnings
        is_valid, issues = validate_registry(tools, strict=True)
        assert is_valid is True  # warnings don't make it invalid
        assert len(issues) == 3  # version, aliases, examples
        assert all('[WARN]' in issue for issue in issues)

    def test_validate_registry_empty_list(self):
        """Test validating an empty registry."""
        is_valid, issues = validate_registry([])
        assert is_valid is True
        assert len(issues) == 0

    def test_validate_registry_complete_tool(self):
        """Test validating a tool with all fields."""
        tools = [
            {
                'id': 'complete-tool',
                'name': 'Complete Tool',
                'entry': 'python complete.py',
                'description': 'A complete tool with all fields',
                'version': '1.0.0',
                'aliases': ['ct', 'comptool'],
                'examples': ['python complete.py --help']
            }
        ]
        is_valid, issues = validate_registry(tools, strict=True)
        assert is_valid is True
        assert len(issues) == 0
