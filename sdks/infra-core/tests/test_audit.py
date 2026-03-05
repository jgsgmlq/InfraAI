"""Tests for audit module."""

import pytest
import tempfile
import os
import shutil
from pathlib import Path
import sys

# Add the api directory to path for direct import
api_path = Path(__file__).parent.parent / "api"
sys.path.insert(0, str(api_path))

from audit import (
    audit_sdk,
    audit_skills,
    audit_docs,
    AuditResult,
    AuditFinding,
    AuditSeverity,
)


class TestAuditSDK:
    """Tests for audit_sdk function."""

    def test_audit_sdk_valid(self):
        """Test auditing a valid SDK."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sdk_path = Path(tmpdir) / "test-sdk"
            sdk_path.mkdir()

            # Create required files
            (sdk_path / "__init__.py").write_text("# init")
            (sdk_path / "version.py").write_text('__version__ = "1.0.0"')
            (sdk_path / "manifest.yaml").write_text(
                "name: test-sdk\nversion: '1.0.0'\ndescription: Test SDK"
            )
            (sdk_path / "README.md").write_text("# Test SDK")
            (sdk_path / "CHANGELOG.md").write_text("# Changelog")

            # Create required directories
            (sdk_path / "api").mkdir()
            (sdk_path / "tests").mkdir()

            # Create recommended directories
            (sdk_path / "cli").mkdir()
            (sdk_path / "skills").mkdir()
            (sdk_path / "examples").mkdir()

            result = audit_sdk(sdk_path)
            assert result.passed is True
            assert len(result.errors) == 0

    def test_audit_sdk_missing_manifest(self):
        """Test auditing SDK without manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sdk_path = Path(tmpdir) / "test-sdk"
            sdk_path.mkdir()

            # Create some files but not manifest
            (sdk_path / "__init__.py").write_text("# init")
            (sdk_path / "version.py").write_text('__version__ = "1.0.0"')
            (sdk_path / "README.md").write_text("# Test SDK")
            (sdk_path / "CHANGELOG.md").write_text("# Changelog")
            (sdk_path / "api").mkdir()
            (sdk_path / "tests").mkdir()

            result = audit_sdk(sdk_path)
            assert result.passed is False
            assert any("manifest.yaml" in f.message for f in result.errors)

    def test_audit_sdk_not_found(self):
        """Test auditing non-existent SDK directory."""
        result = audit_sdk("/nonexistent/sdk/path")
        assert result.passed is False
        assert len(result.errors) == 1
        assert "not found" in result.errors[0].message.lower()

    def test_audit_sdk_missing_required_files(self):
        """Test auditing SDK with missing required files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sdk_path = Path(tmpdir) / "test-sdk"
            sdk_path.mkdir()

            # Only create one file
            (sdk_path / "__init__.py").write_text("# init")

            result = audit_sdk(sdk_path)
            assert result.passed is False
            # Should have errors for: version.py, manifest.yaml, README.md, CHANGELOG.md, api/, tests/
            assert len(result.errors) >= 5

    def test_audit_sdk_missing_required_dirs(self):
        """Test auditing SDK with missing required directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sdk_path = Path(tmpdir) / "test-sdk"
            sdk_path.mkdir()

            # Create required files
            (sdk_path / "__init__.py").write_text("# init")
            (sdk_path / "version.py").write_text('__version__ = "1.0.0"')
            (sdk_path / "manifest.yaml").write_text(
                "name: test-sdk\nversion: '1.0.0'\ndescription: Test SDK"
            )
            (sdk_path / "README.md").write_text("# Test SDK")
            (sdk_path / "CHANGELOG.md").write_text("# Changelog")
            # Don't create api/ and tests/ directories

            result = audit_sdk(sdk_path)
            assert result.passed is False
            assert any("api" in f.message for f in result.errors)
            assert any("tests" in f.message for f in result.errors)

    def test_audit_sdk_missing_recommended_dirs(self):
        """Test auditing SDK with missing recommended directories gives warnings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sdk_path = Path(tmpdir) / "test-sdk"
            sdk_path.mkdir()

            # Create all required files and dirs
            (sdk_path / "__init__.py").write_text("# init")
            (sdk_path / "version.py").write_text('__version__ = "1.0.0"')
            (sdk_path / "manifest.yaml").write_text(
                "name: test-sdk\nversion: '1.0.0'\ndescription: Test SDK"
            )
            (sdk_path / "README.md").write_text("# Test SDK")
            (sdk_path / "CHANGELOG.md").write_text("# Changelog")
            (sdk_path / "api").mkdir()
            (sdk_path / "tests").mkdir()
            # Don't create cli/, skills/, examples/

            result = audit_sdk(sdk_path)
            assert result.passed is True  # warnings don't fail
            assert len(result.warnings) == 3  # cli, skills, examples

    def test_audit_sdk_invalid_manifest_yaml(self):
        """Test auditing SDK with invalid YAML in manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sdk_path = Path(tmpdir) / "test-sdk"
            sdk_path.mkdir()

            (sdk_path / "__init__.py").write_text("# init")
            (sdk_path / "version.py").write_text('__version__ = "1.0.0"')
            (sdk_path / "manifest.yaml").write_text("invalid: yaml: [")
            (sdk_path / "README.md").write_text("# Test SDK")
            (sdk_path / "CHANGELOG.md").write_text("# Changelog")
            (sdk_path / "api").mkdir()
            (sdk_path / "tests").mkdir()

            result = audit_sdk(sdk_path)
            assert result.passed is False
            assert any("invalid yaml" in f.message.lower() for f in result.errors)

    def test_audit_sdk_manifest_missing_fields(self):
        """Test auditing SDK with manifest missing required fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sdk_path = Path(tmpdir) / "test-sdk"
            sdk_path.mkdir()

            (sdk_path / "__init__.py").write_text("# init")
            (sdk_path / "version.py").write_text('__version__ = "1.0.0"')
            (sdk_path / "manifest.yaml").write_text("name: test-sdk")  # missing version and description
            (sdk_path / "README.md").write_text("# Test SDK")
            (sdk_path / "CHANGELOG.md").write_text("# Changelog")
            (sdk_path / "api").mkdir()
            (sdk_path / "tests").mkdir()

            result = audit_sdk(sdk_path)
            assert result.passed is False
            assert any("version" in f.message for f in result.errors)
            assert any("description" in f.message for f in result.errors)


class TestAuditSkills:
    """Tests for audit_skills function."""

    def test_audit_skills_valid(self):
        """Test auditing valid skills configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skills_path = Path(tmpdir) / "skills"
            skills_path.mkdir()

            # Create a valid skill file
            skill_content = """---
name: test-skill
description: A test skill
---

# Test Skill

This is a test skill.
"""
            (skills_path / "test-skill.md").write_text(skill_content)

            result = audit_skills(skills_path)
            assert result.passed is True
            assert len(result.errors) == 0

    def test_audit_skills_not_found(self):
        """Test auditing non-existent skills directory."""
        result = audit_skills("/nonexistent/skills/path")
        assert result.passed is False
        assert "not found" in result.findings[0].message.lower()

    def test_audit_skills_missing_frontmatter(self):
        """Test auditing skill without YAML frontmatter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skills_path = Path(tmpdir) / "skills"
            skills_path.mkdir()

            # Create a skill file without frontmatter
            (skills_path / "bad-skill.md").write_text("# Bad Skill\n\nNo frontmatter here.")

            result = audit_skills(skills_path)
            assert result.passed is True  # warnings don't fail
            assert len(result.warnings) == 1
            assert "frontmatter" in result.warnings[0].message.lower()

    def test_audit_skills_missing_required_fields(self):
        """Test auditing skill with missing required frontmatter fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skills_path = Path(tmpdir) / "skills"
            skills_path.mkdir()

            # Create skill with incomplete frontmatter
            skill_content = """---
name: incomplete-skill
---

# Incomplete Skill
"""
            (skills_path / "incomplete.md").write_text(skill_content)

            result = audit_skills(skills_path)
            assert result.passed is False
            assert any("description" in f.message for f in result.errors)

    def test_audit_skills_invalid_yaml_frontmatter(self):
        """Test auditing skill with invalid YAML in frontmatter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skills_path = Path(tmpdir) / "skills"
            skills_path.mkdir()

            skill_content = """---
invalid: yaml: [
---

# Bad YAML
"""
            (skills_path / "bad-yaml.md").write_text(skill_content)

            result = audit_skills(skills_path)
            assert result.passed is False
            assert any("invalid" in f.message.lower() for f in result.errors)

    def test_audit_skills_empty_directory(self):
        """Test auditing empty skills directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skills_path = Path(tmpdir) / "skills"
            skills_path.mkdir()

            result = audit_skills(skills_path)
            assert result.passed is True
            assert len(result.findings) == 0


class TestAuditDocs:
    """Tests for audit_docs function."""

    def test_audit_docs_valid(self):
        """Test auditing valid documentation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir) / "docs"
            docs_path.mkdir()

            # Create valid doc files
            (docs_path / "README.md").write_text("# Documentation\n\nThis is valid documentation.")
            (docs_path / "guide.md").write_text("""# Guide

```python
print("hello")
```

More content here.
""")

            result = audit_docs(docs_path)
            assert result.passed is True
            assert len(result.errors) == 0

    def test_audit_docs_not_found(self):
        """Test auditing non-existent docs directory."""
        result = audit_docs("/nonexistent/docs/path")
        assert result.passed is False
        assert "not found" in result.findings[0].message.lower()

    def test_audit_docs_empty_file(self):
        """Test auditing docs with empty file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir) / "docs"
            docs_path.mkdir()

            (docs_path / "empty.md").write_text("")

            result = audit_docs(docs_path)
            assert result.passed is True  # warnings don't fail
            assert len(result.warnings) == 1
            assert "empty" in result.warnings[0].message.lower()

    def test_audit_docs_code_block_without_language(self):
        """Test auditing docs with code blocks without language tags."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir) / "docs"
            docs_path.mkdir()

            doc_content = """# Test Doc

Some text.

```
code without language
```

More text.
"""
            (docs_path / "test.md").write_text(doc_content)

            result = audit_docs(docs_path)
            assert result.passed is True  # INFO level doesn't fail
            info_findings = [f for f in result.findings if f.severity == AuditSeverity.INFO]
            assert len(info_findings) == 1
            assert "language tag" in info_findings[0].message.lower()

    def test_audit_docs_with_language_tag(self):
        """Test auditing docs with proper code block language tags."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir) / "docs"
            docs_path.mkdir()

            doc_content = """# Test Doc

```python
print("hello")
```

```bash
echo "hello"
```
"""
            (docs_path / "test.md").write_text(doc_content)

            result = audit_docs(docs_path)
            assert result.passed is True
            info_findings = [f for f in result.findings if f.severity == AuditSeverity.INFO]
            assert len(info_findings) == 0

    def test_audit_docs_nested_directory(self):
        """Test auditing docs in nested directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir) / "docs"
            docs_path.mkdir()
            (docs_path / "subdir").mkdir()

            (docs_path / "README.md").write_text("# Root Doc\n\nContent here.")
            (docs_path / "subdir" / "nested.md").write_text("# Nested Doc\n\nMore content.")

            result = audit_docs(docs_path)
            assert result.passed is True


class TestAuditResult:
    """Tests for AuditResult dataclass."""

    def test_audit_result_errors_property(self):
        """Test errors property filters correctly."""
        result = AuditResult(
            passed=False,
            findings=[
                AuditFinding(AuditSeverity.ERROR, "cat", "error 1"),
                AuditFinding(AuditSeverity.WARNING, "cat", "warning 1"),
                AuditFinding(AuditSeverity.ERROR, "cat", "error 2"),
                AuditFinding(AuditSeverity.INFO, "cat", "info 1"),
            ]
        )
        assert len(result.errors) == 2
        assert all(f.severity == AuditSeverity.ERROR for f in result.errors)

    def test_audit_result_warnings_property(self):
        """Test warnings property filters correctly."""
        result = AuditResult(
            passed=True,
            findings=[
                AuditFinding(AuditSeverity.ERROR, "cat", "error 1"),
                AuditFinding(AuditSeverity.WARNING, "cat", "warning 1"),
                AuditFinding(AuditSeverity.WARNING, "cat", "warning 2"),
            ]
        )
        assert len(result.warnings) == 2
        assert all(f.severity == AuditSeverity.WARNING for f in result.warnings)
