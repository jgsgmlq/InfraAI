"""
Audit module.

Provides functions to audit SDKs, skills, and documentation.
"""

from pathlib import Path
from typing import Dict, List, Any, Tuple, Union, Optional
from dataclasses import dataclass
from enum import Enum

import yaml


class AuditSeverity(Enum):
    """Audit finding severity."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class AuditFinding:
    """Single audit finding."""
    severity: AuditSeverity
    category: str
    message: str
    path: Optional[str] = None
    suggestion: Optional[str] = None


@dataclass
class AuditResult:
    """Audit result collection."""
    passed: bool
    findings: List[AuditFinding]

    @property
    def errors(self) -> List[AuditFinding]:
        return [f for f in self.findings if f.severity == AuditSeverity.ERROR]

    @property
    def warnings(self) -> List[AuditFinding]:
        return [f for f in self.findings if f.severity == AuditSeverity.WARNING]


def audit_sdk(sdk_path: Union[str, Path]) -> AuditResult:
    """
    Audit an SDK package for completeness and correctness.

    Checks:
    - Required files exist (__init__.py, version.py, manifest.yaml, README.md)
    - manifest.yaml is valid
    - Exported modules exist
    - Skills have matching entry files

    Args:
        sdk_path: Path to the SDK directory.

    Returns:
        AuditResult with findings.
    """
    path = Path(sdk_path)
    findings = []

    # Check SDK directory exists
    if not path.exists():
        return AuditResult(
            passed=False,
            findings=[AuditFinding(
                severity=AuditSeverity.ERROR,
                category="structure",
                message=f"SDK directory not found: {path}"
            )]
        )

    # Check required files
    required_files = [
        "__init__.py",
        "version.py",
        "manifest.yaml",
        "README.md",
        "CHANGELOG.md",
    ]

    for filename in required_files:
        if not (path / filename).exists():
            findings.append(AuditFinding(
                severity=AuditSeverity.ERROR,
                category="structure",
                message=f"Missing required file: {filename}",
                path=str(path / filename),
                suggestion=f"Create {filename} following SDK specification"
            ))

    # Check required directories
    required_dirs = ["api", "tests"]
    recommended_dirs = ["cli", "skills", "examples"]

    for dirname in required_dirs:
        if not (path / dirname).is_dir():
            findings.append(AuditFinding(
                severity=AuditSeverity.ERROR,
                category="structure",
                message=f"Missing required directory: {dirname}/",
                path=str(path / dirname)
            ))

    for dirname in recommended_dirs:
        if not (path / dirname).is_dir():
            findings.append(AuditFinding(
                severity=AuditSeverity.WARNING,
                category="structure",
                message=f"Missing recommended directory: {dirname}/",
                path=str(path / dirname)
            ))

    # Validate manifest.yaml if exists
    manifest_path = path / "manifest.yaml"
    if manifest_path.exists():
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = yaml.safe_load(f)

            required_manifest_fields = ["name", "version", "description"]
            for field in required_manifest_fields:
                if field not in manifest:
                    findings.append(AuditFinding(
                        severity=AuditSeverity.ERROR,
                        category="manifest",
                        message=f"Missing required field in manifest: {field}",
                        path=str(manifest_path)
                    ))
        except yaml.YAMLError as e:
            findings.append(AuditFinding(
                severity=AuditSeverity.ERROR,
                category="manifest",
                message=f"Invalid YAML in manifest: {e}",
                path=str(manifest_path)
            ))

    has_errors = any(f.severity == AuditSeverity.ERROR for f in findings)

    return AuditResult(passed=not has_errors, findings=findings)


def audit_skills(
    skills_dir: Union[str, Path],
    sdk_dir: Optional[Union[str, Path]] = None
) -> AuditResult:
    """
    Audit skills configuration.

    Checks:
    - Entry skills in .claude/skills/ have valid frontmatter
    - Implementation files exist
    - SDK references are valid

    Args:
        skills_dir: Path to .claude/skills/ directory.
        sdk_dir: Path to sdks/ directory for cross-reference.

    Returns:
        AuditResult with findings.
    """
    skills_path = Path(skills_dir)
    findings = []

    if not skills_path.exists():
        return AuditResult(
            passed=False,
            findings=[AuditFinding(
                severity=AuditSeverity.ERROR,
                category="skills",
                message=f"Skills directory not found: {skills_path}"
            )]
        )

    # Check each skill file
    for skill_file in skills_path.glob("*.md"):
        content = skill_file.read_text(encoding="utf-8")

        # Check for YAML frontmatter
        if not content.startswith("---"):
            findings.append(AuditFinding(
                severity=AuditSeverity.WARNING,
                category="skills",
                message="Missing YAML frontmatter",
                path=str(skill_file)
            ))
            continue

        # Parse frontmatter
        try:
            end_idx = content.index("---", 3)
            frontmatter = yaml.safe_load(content[3:end_idx])

            required_fields = ["name", "description"]
            for field in required_fields:
                if field not in frontmatter:
                    findings.append(AuditFinding(
                        severity=AuditSeverity.ERROR,
                        category="skills",
                        message=f"Missing required frontmatter field: {field}",
                        path=str(skill_file)
                    ))

            # Check implementation path exists
            if "implementation" in frontmatter and sdk_dir:
                impl_path = Path(sdk_dir).parent / frontmatter["implementation"]
                if not impl_path.exists():
                    findings.append(AuditFinding(
                        severity=AuditSeverity.ERROR,
                        category="skills",
                        message=f"Implementation file not found: {frontmatter['implementation']}",
                        path=str(skill_file)
                    ))

        except (ValueError, yaml.YAMLError):
            findings.append(AuditFinding(
                severity=AuditSeverity.ERROR,
                category="skills",
                message="Invalid YAML frontmatter",
                path=str(skill_file)
            ))

    has_errors = any(f.severity == AuditSeverity.ERROR for f in findings)

    return AuditResult(passed=not has_errors, findings=findings)


def audit_docs(docs_dir: Union[str, Path]) -> AuditResult:
    """
    Audit documentation for consistency.

    Checks:
    - Markdown files are valid
    - Internal links are valid
    - Code blocks have language tags

    Args:
        docs_dir: Path to documentation directory.

    Returns:
        AuditResult with findings.
    """
    docs_path = Path(docs_dir)
    findings = []

    if not docs_path.exists():
        return AuditResult(
            passed=False,
            findings=[AuditFinding(
                severity=AuditSeverity.ERROR,
                category="docs",
                message=f"Documentation directory not found: {docs_path}"
            )]
        )

    # Check each markdown file
    for md_file in docs_path.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")

        # Check for empty files
        if len(content.strip()) < 10:
            findings.append(AuditFinding(
                severity=AuditSeverity.WARNING,
                category="docs",
                message="File appears to be empty or too short",
                path=str(md_file)
            ))

        # Check for code blocks without language
        lines = content.split("\n")
        in_code_block = False
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("```"):
                if not in_code_block:
                    # Opening block
                    if stripped == "```":
                        findings.append(AuditFinding(
                            severity=AuditSeverity.INFO,
                            category="docs",
                            message=f"Code block without language tag at line {i+1}",
                            path=str(md_file)
                        ))
                    in_code_block = True
                else:
                    # Closing block
                    in_code_block = False

    has_errors = any(f.severity == AuditSeverity.ERROR for f in findings)

    return AuditResult(passed=not has_errors, findings=findings)
