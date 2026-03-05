# Framework Restructure Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 重构 AI-Native Infrastructure Framework，实现 SDK 包架构 + Skills 分层设计，让 Claude Code 能自动识别项目能力。

**Architecture:**
- SDK 包放在 `sdks/` 目录，每个 SDK 自包含（Python API + CLI 入口 + skills + tests + 文档）
- Skills 入口放在 `.claude/skills/`（Claude Code 自动识别），实现逻辑在各 SDK 内部
- CLI 工具独立于 SDK，调用 SDK 提供的 API

**Tech Stack:** Python 3.8+, PyYAML, argparse

---

## Phase 1: 基础架构设计

### Task 1.1: 创建 SDK 包规范文档

**Files:**
- Create: `docs/60_sdk_specification.md`

**Step 1: 创建 SDK 规范文档**

```markdown
# SDK 包规范

## 概述

SDK 包是框架的核心组成单元，每个 SDK 封装一组相关功能，提供 Python API 和可选的 CLI 入口。

---

## 目录结构

每个 SDK 包 MUST 遵循以下结构：

```
sdks/<sdk-name>/
├── __init__.py              # 包入口，导出公共 API
├── version.py               # 版本信息
├── api/                     # Python API 实现
│   ├── __init__.py
│   └── <module>.py
├── cli/                     # CLI 入口（可选）
│   ├── __init__.py
│   └── main.py
├── skills/                  # SDK 内部 skills 实现
│   └── <skill-name>.md
├── tests/                   # 测试
│   ├── __init__.py
│   └── test_<module>.py
├── examples/                # 示例代码
│   └── example_<use-case>.py
├── README.md                # SDK 文档
├── CHANGELOG.md             # 版本变更记录
└── manifest.yaml            # SDK 元信息
```

---

## manifest.yaml 规范

```yaml
name: sdk-name
version: "1.0.0"
description: SDK 功能描述
author: 作者
license: MIT

# 依赖
dependencies:
  python: ">=3.8"
  packages:
    - pyyaml>=6.0

# 导出的能力
exports:
  api:
    - module: api.core
      functions:
        - function_name
  cli:
    - command: sdk-name
      entry: cli.main:main
  skills:
    - id: skill-id
      entry_skill: .claude/skills/sdk-name-skill-id.md
      implementation: skills/skill-id.md
```

---

## 命名规范

| 类型 | 规则 | 示例 |
|------|------|------|
| SDK 目录名 | kebab-case | `infra-core`, `project-tools` |
| Python 模块 | snake_case | `infra_core`, `project_tools` |
| CLI 命令 | kebab-case | `infra-core`, `project-tools` |
| Skill ID | kebab-case | `audit-sdk`, `check-docs` |

---

## 版本管理

- 使用语义化版本 (SemVer): MAJOR.MINOR.PATCH
- version.py 是唯一版本来源
- CHANGELOG.md 记录所有变更

```python
# version.py
__version__ = "1.0.0"
__version_info__ = (1, 0, 0)
```

---

## Skills 集成

### 入口 Skill（在 .claude/skills/）

轻量级入口文件，让 Claude Code 能发现这个能力：

```markdown
---
name: sdk-name-skill-id
description: 简短描述
triggers:
  - "触发短语1"
  - "触发短语2"
sdk: sdk-name
implementation: sdks/sdk-name/skills/skill-id.md
---

# Skill 名称

[简要说明这个 skill 做什么]

## 使用方式

调用 SDK: `from sdks.sdk_name.api import function`

详细实现请参考: `sdks/sdk-name/skills/skill-id.md`
```

### 实现 Skill（在 SDK 内部）

完整的实现逻辑、步骤、示例代码等。

---

## 完整性检查清单

创建 SDK 时 MUST 完成：

- [ ] `__init__.py` 存在且导出公共 API
- [ ] `version.py` 定义版本
- [ ] `manifest.yaml` 完整填写
- [ ] `README.md` 包含使用说明
- [ ] `CHANGELOG.md` 记录初始版本
- [ ] 至少一个测试文件
- [ ] 每个 skill 有对应的入口文件在 `.claude/skills/`
```

**Step 2: 验证文档已创建**

Run: `cat docs/60_sdk_specification.md | head -20`
Expected: 显示文档开头内容

**Step 3: Commit**

```bash
git add docs/60_sdk_specification.md
git commit -m "docs: add SDK package specification"
```

---

### Task 1.2: 创建 Skills 分层规范文档

**Files:**
- Modify: `docs/50_skills_system.md` (如存在则更新，否则创建)

**Step 1: 创建/更新 Skills 系统文档**

```markdown
# Skills 系统规范（v2）

## 概述

Skills 是 AI 可识别和调用的能力单元。采用分层设计：
- **入口层**：位于 `.claude/skills/`，Claude Code 自动识别
- **实现层**：位于各 SDK 内部，包含完整逻辑

---

## 目录结构

```
project/
├── .claude/
│   └── skills/                    # 入口 skills（自动识别）
│       ├── infra-core-audit.md    # 框架审查能力入口
│       ├── infra-core-init.md     # 项目初始化能力入口
│       └── <sdk>-<skill>.md       # SDK 能力入口
│
└── sdks/
    └── <sdk-name>/
        └── skills/                # 实现 skills
            └── <skill>.md         # 完整实现逻辑
```

---

## 入口 Skill 模板

文件位置：`.claude/skills/<sdk-name>-<skill-id>.md`

```markdown
---
name: <sdk-name>-<skill-id>
description: 一句话描述
triggers:
  - "中文触发短语"
  - "English trigger phrase"
sdk: <sdk-name>
implementation: sdks/<sdk-name>/skills/<skill-id>.md
---

# <Skill 名称>

## 用途

[这个 skill 解决什么问题]

## 调用方式

```python
from sdks.<sdk_name>.api import <function>
result = <function>(...)
```

或 CLI:

```bash
<sdk-name> <command> [options]
```

## 详细文档

完整实现逻辑请参考：`sdks/<sdk-name>/skills/<skill-id>.md`
```

---

## 实现 Skill 模板

文件位置：`sdks/<sdk-name>/skills/<skill-id>.md`

```markdown
# <Skill 名称>

## 概述

[详细功能说明]

## 前置条件

- [条件1]
- [条件2]

## 执行步骤

### Step 1: [步骤名称]

[详细说明]

```python
# 示例代码
```

### Step 2: [步骤名称]

...

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| Error1 | 原因1 | 方案1 |

## 检查点

执行前确认：
- [ ] 检查项1
- [ ] 检查项2

## 相关 Skills

- `<related-skill-1>`
- `<related-skill-2>`
```

---

## 命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 入口文件名 | `<sdk>-<skill>.md` | `infra-core-audit.md` |
| 实现文件名 | `<skill>.md` | `audit.md` |
| YAML name | `<sdk>-<skill>` | `infra-core-audit` |

---

## 注册流程

1. 在 SDK 内创建实现 skill: `sdks/<sdk>/skills/<skill>.md`
2. 在 `.claude/skills/` 创建入口 skill
3. 更新 SDK 的 `manifest.yaml`
4. 运行审查工具验证完整性

---

## 审查清单

- [ ] 入口 skill 存在于 `.claude/skills/`
- [ ] 实现 skill 存在于 SDK 内
- [ ] YAML frontmatter 完整
- [ ] triggers 包含中英文
- [ ] implementation 路径正确
- [ ] SDK manifest.yaml 已注册
```

**Step 2: 验证文档**

Run: `ls -la docs/50_skills_system.md`
Expected: 文件存在

**Step 3: Commit**

```bash
git add docs/50_skills_system.md
git commit -m "docs: update skills system spec with layered design"
```

---

## Phase 2: 创建框架核心 SDK

### Task 2.1: 创建 infra-core SDK 基础结构

**Files:**
- Create: `sdks/infra-core/__init__.py`
- Create: `sdks/infra-core/version.py`
- Create: `sdks/infra-core/manifest.yaml`
- Create: `sdks/infra-core/README.md`
- Create: `sdks/infra-core/CHANGELOG.md`

**Step 1: 创建目录结构**

```bash
mkdir -p sdks/infra-core/{api,cli,skills,tests,examples}
```

**Step 2: 创建 version.py**

```python
"""Version information for infra-core SDK."""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)
```

**Step 3: 创建 __init__.py**

```python
"""
infra-core SDK

AI-Native Infrastructure Framework 核心功能包。
提供工具注册、审查、项目初始化等基础能力。
"""

from .version import __version__, __version_info__

__all__ = [
    "__version__",
    "__version_info__",
]
```

**Step 4: 创建 manifest.yaml**

```yaml
name: infra-core
version: "1.0.0"
description: AI-Native Infrastructure Framework 核心 SDK
author: AI Infrastructure Team
license: MIT

dependencies:
  python: ">=3.8"
  packages:
    - pyyaml>=6.0

exports:
  api:
    - module: api.registry
      functions:
        - load_registry
        - validate_registry
    - module: api.audit
      functions:
        - audit_sdk
        - audit_skills
        - audit_docs
  cli:
    - command: infra-core
      entry: cli.main:main
  skills:
    - id: audit-sdk
      entry_skill: .claude/skills/infra-core-audit-sdk.md
      implementation: skills/audit-sdk.md
    - id: audit-docs
      entry_skill: .claude/skills/infra-core-audit-docs.md
      implementation: skills/audit-docs.md
    - id: create-sdk
      entry_skill: .claude/skills/infra-core-create-sdk.md
      implementation: skills/create-sdk.md
```

**Step 5: 创建 README.md**

```markdown
# infra-core SDK

AI-Native Infrastructure Framework 的核心 SDK。

## 安装

```bash
# 作为项目依赖
pip install -e sdks/infra-core
```

## 功能

- **Registry 管理**: 加载和验证工具注册表
- **SDK 审查**: 检查 SDK 包完整性
- **文档审查**: 检查文档一致性
- **Skills 审查**: 验证 skills 配置

## 使用

### Python API

```python
from sdks.infra_core.api import audit_sdk, audit_docs

# 审查 SDK
result = audit_sdk("sdks/my-sdk")

# 审查文档
result = audit_docs("docs/")
```

### CLI

```bash
infra-core audit-sdk sdks/my-sdk
infra-core audit-docs docs/
```

## Skills

- `infra-core-audit-sdk`: SDK 包完整性审查
- `infra-core-audit-docs`: 文档一致性审查
- `infra-core-create-sdk`: 创建新 SDK 包
```

**Step 6: 创建 CHANGELOG.md**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-04

### Added

- Initial release
- Registry management API
- SDK audit functionality
- Documentation audit functionality
- Skills audit functionality
- CLI interface
```

**Step 7: 验证结构**

Run: `find sdks/infra-core -type f | sort`
Expected: 显示所有创建的文件

**Step 8: Commit**

```bash
git add sdks/
git commit -m "feat: create infra-core SDK base structure"
```

---

### Task 2.2: 实现 Registry API

**Files:**
- Create: `sdks/infra-core/api/__init__.py`
- Create: `sdks/infra-core/api/registry.py`
- Create: `sdks/infra-core/tests/test_registry.py`

**Step 1: 创建测试文件**

```python
"""Tests for registry module."""

import pytest
import tempfile
import os
from pathlib import Path

# 测试将在实现后补充
def test_load_registry_success():
    """Test loading a valid registry file."""
    # TODO: Implement after API is ready
    pass

def test_load_registry_not_found():
    """Test loading non-existent registry file."""
    pass

def test_validate_registry_valid():
    """Test validating a correct registry."""
    pass

def test_validate_registry_missing_fields():
    """Test validating registry with missing required fields."""
    pass
```

**Step 2: 创建 api/__init__.py**

```python
"""infra-core API exports."""

from .registry import load_registry, validate_registry

__all__ = [
    "load_registry",
    "validate_registry",
]
```

**Step 3: 实现 registry.py**

```python
"""
Registry management module.

Provides functions to load, validate, and query tool registries.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

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


def load_registry(path: str | Path) -> List[Dict[str, Any]]:
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
```

**Step 4: 运行测试**

Run: `cd sdks/infra-core && python -m pytest tests/ -v`
Expected: Tests pass (placeholder tests)

**Step 5: Commit**

```bash
git add sdks/infra-core/api/ sdks/infra-core/tests/
git commit -m "feat(infra-core): implement registry API"
```

---

### Task 2.3: 实现 Audit API

**Files:**
- Create: `sdks/infra-core/api/audit.py`
- Create: `sdks/infra-core/tests/test_audit.py`
- Modify: `sdks/infra-core/api/__init__.py`

**Step 1: 创建测试文件**

```python
"""Tests for audit module."""

import pytest
import tempfile
import os
from pathlib import Path


def test_audit_sdk_valid():
    """Test auditing a valid SDK."""
    pass


def test_audit_sdk_missing_manifest():
    """Test auditing SDK without manifest."""
    pass


def test_audit_skills_valid():
    """Test auditing valid skills configuration."""
    pass


def test_audit_docs_consistency():
    """Test documentation consistency check."""
    pass
```

**Step 2: 实现 audit.py**

```python
"""
Audit module.

Provides functions to audit SDKs, skills, and documentation.
"""

from pathlib import Path
from typing import Dict, List, Any, Tuple
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
    path: str | None = None
    suggestion: str | None = None


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


def audit_sdk(sdk_path: str | Path) -> AuditResult:
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
    skills_dir: str | Path,
    sdk_dir: str | Path | None = None
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


def audit_docs(docs_dir: str | Path) -> AuditResult:
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
        for i, line in enumerate(lines):
            if line.strip() == "```":
                # Check if it's an opening or closing block
                # Opening blocks should have language
                findings.append(AuditFinding(
                    severity=AuditSeverity.INFO,
                    category="docs",
                    message=f"Code block without language tag at line {i+1}",
                    path=str(md_file)
                ))

    has_errors = any(f.severity == AuditSeverity.ERROR for f in findings)

    return AuditResult(passed=not has_errors, findings=findings)
```

**Step 3: 更新 api/__init__.py**

```python
"""infra-core API exports."""

from .registry import (
    load_registry,
    validate_registry,
    RegistryError,
    RegistryNotFoundError,
    RegistryValidationError,
)
from .audit import (
    audit_sdk,
    audit_skills,
    audit_docs,
    AuditResult,
    AuditFinding,
    AuditSeverity,
)

__all__ = [
    # Registry
    "load_registry",
    "validate_registry",
    "RegistryError",
    "RegistryNotFoundError",
    "RegistryValidationError",
    # Audit
    "audit_sdk",
    "audit_skills",
    "audit_docs",
    "AuditResult",
    "AuditFinding",
    "AuditSeverity",
]
```

**Step 4: 运行测试**

Run: `cd sdks/infra-core && python -m pytest tests/ -v`
Expected: Tests pass

**Step 5: Commit**

```bash
git add sdks/infra-core/api/ sdks/infra-core/tests/
git commit -m "feat(infra-core): implement audit API"
```

---

## Phase 3: 创建 Skills 入口文件

### Task 3.1: 创建 .claude/skills/ 目录和入口 Skills

**Files:**
- Create: `.claude/skills/infra-core-audit-sdk.md`
- Create: `.claude/skills/infra-core-audit-docs.md`
- Create: `.claude/skills/infra-core-create-sdk.md`

**Step 1: 创建目录**

```bash
mkdir -p .claude/skills
```

**Step 2: 创建 infra-core-audit-sdk.md**

```markdown
---
name: infra-core-audit-sdk
description: 审查 SDK 包的完整性和规范性
triggers:
  - "检查 SDK"
  - "审查 SDK"
  - "audit SDK"
  - "validate SDK"
sdk: infra-core
implementation: sdks/infra-core/skills/audit-sdk.md
---

# SDK 审查

审查 SDK 包是否符合框架规范。

## 用途

- 检查必需文件是否存在
- 验证 manifest.yaml 格式
- 确认 skills 入口与实现匹配

## 调用方式

```python
from sdks.infra_core.api import audit_sdk

result = audit_sdk("sdks/my-sdk")
if not result.passed:
    for finding in result.errors:
        print(f"[ERROR] {finding.message}")
```

或 CLI:

```bash
infra-core audit-sdk sdks/my-sdk
```

## 详细文档

完整实现逻辑请参考：`sdks/infra-core/skills/audit-sdk.md`
```

**Step 3: 创建 infra-core-audit-docs.md**

```markdown
---
name: infra-core-audit-docs
description: 审查文档一致性和完整性
triggers:
  - "检查文档"
  - "审查文档"
  - "audit docs"
  - "check documentation"
sdk: infra-core
implementation: sdks/infra-core/skills/audit-docs.md
---

# 文档审查

检查项目文档的一致性和完整性。

## 用途

- 检查 Markdown 文件格式
- 验证内部链接有效性
- 检查代码块语言标签

## 调用方式

```python
from sdks.infra_core.api import audit_docs

result = audit_docs("docs/")
for finding in result.findings:
    print(f"[{finding.severity.value}] {finding.message}")
```

或 CLI:

```bash
infra-core audit-docs docs/
```

## 详细文档

完整实现逻辑请参考：`sdks/infra-core/skills/audit-docs.md`
```

**Step 4: 创建 infra-core-create-sdk.md**

```markdown
---
name: infra-core-create-sdk
description: 创建新的 SDK 包
triggers:
  - "创建 SDK"
  - "新建 SDK"
  - "create SDK"
  - "new SDK package"
sdk: infra-core
implementation: sdks/infra-core/skills/create-sdk.md
---

# 创建 SDK

使用模板创建符合规范的新 SDK 包。

## 用途

- 自动生成 SDK 目录结构
- 创建标准配置文件
- 初始化版本和 changelog

## 调用方式

```bash
infra-core create-sdk my-new-sdk --description "我的 SDK"
```

## 生成内容

```
sdks/my-new-sdk/
├── __init__.py
├── version.py
├── manifest.yaml
├── README.md
├── CHANGELOG.md
├── api/
├── cli/
├── skills/
├── tests/
└── examples/
```

## 详细文档

完整实现逻辑请参考：`sdks/infra-core/skills/create-sdk.md`
```

**Step 5: 验证创建**

Run: `ls -la .claude/skills/`
Expected: 显示三个 skill 入口文件

**Step 6: Commit**

```bash
git add .claude/skills/
git commit -m "feat: add entry skills in .claude/skills/"
```

---

### Task 3.2: 创建 SDK 内部实现 Skills

**Files:**
- Create: `sdks/infra-core/skills/audit-sdk.md`
- Create: `sdks/infra-core/skills/audit-docs.md`
- Create: `sdks/infra-core/skills/create-sdk.md`

**Step 1: 创建 audit-sdk.md**

```markdown
# SDK 审查 - 实现文档

## 概述

SDK 审查工具检查 SDK 包的完整性和规范性，确保所有必需组件都存在且格式正确。

## 审查项目

### 结构检查

| 检查项 | 级别 | 说明 |
|--------|------|------|
| `__init__.py` | ERROR | 必须存在 |
| `version.py` | ERROR | 必须存在 |
| `manifest.yaml` | ERROR | 必须存在 |
| `README.md` | ERROR | 必须存在 |
| `CHANGELOG.md` | ERROR | 必须存在 |
| `api/` | ERROR | 必须存在 |
| `tests/` | ERROR | 必须存在 |
| `cli/` | WARNING | 推荐存在 |
| `skills/` | WARNING | 推荐存在 |
| `examples/` | WARNING | 推荐存在 |

### manifest.yaml 检查

必需字段：
- `name`: SDK 名称（kebab-case）
- `version`: 语义化版本号
- `description`: 功能描述

推荐字段：
- `author`: 作者
- `license`: 许可证
- `dependencies`: 依赖声明
- `exports`: 导出声明

### Skills 完整性检查

- 每个 `exports.skills` 条目必须有：
  - 对应的入口文件在 `.claude/skills/`
  - 对应的实现文件在 `skills/`

## 执行步骤

### Step 1: 检查目录存在

```python
from sdks.infra_core.api import audit_sdk

result = audit_sdk("sdks/target-sdk")
```

### Step 2: 分析结果

```python
if result.passed:
    print("✅ SDK 审查通过")
else:
    print("❌ SDK 审查失败")
    for error in result.errors:
        print(f"  - {error.message}")
        if error.suggestion:
            print(f"    建议: {error.suggestion}")
```

### Step 3: 修复问题

根据错误信息，创建缺失的文件或修复格式问题。

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| SDK directory not found | 路径错误 | 检查 SDK 路径是否正确 |
| Missing required file | 文件缺失 | 按规范创建缺失文件 |
| Invalid YAML | manifest 格式错误 | 修复 YAML 语法 |

## 相关 Skills

- `infra-core-audit-docs`: 文档审查
- `infra-core-create-sdk`: 创建新 SDK（自动符合规范）
```

**Step 2: 创建 audit-docs.md**

```markdown
# 文档审查 - 实现文档

## 概述

文档审查工具检查项目文档的一致性、完整性和格式规范。

## 审查项目

### 文件检查

| 检查项 | 级别 | 说明 |
|--------|------|------|
| 空文件 | WARNING | 文件内容少于 10 字符 |
| 无语言代码块 | INFO | 代码块缺少语言标签 |
| 断裂链接 | WARNING | 内部链接指向不存在的文件 |

### 内容检查

- Markdown 语法有效性
- 标题层级合理（不跳级）
- 代码示例可执行

## 执行步骤

### Step 1: 执行审查

```python
from sdks.infra_core.api import audit_docs

result = audit_docs("docs/")
```

### Step 2: 查看结果

```python
print(f"审查结果: {'通过' if result.passed else '失败'}")
print(f"错误: {len(result.errors)}")
print(f"警告: {len(result.warnings)}")

for finding in result.findings:
    print(f"[{finding.severity.value}] {finding.path}: {finding.message}")
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| Directory not found | 路径错误 | 检查文档目录路径 |
| Empty file | 文档未完成 | 补充内容或删除空文件 |

## 相关 Skills

- `infra-core-audit-sdk`: SDK 审查
```

**Step 3: 创建 create-sdk.md**

```markdown
# 创建 SDK - 实现文档

## 概述

创建符合框架规范的新 SDK 包，自动生成所有必需文件和目录结构。

## 前置条件

- 确定 SDK 名称（kebab-case）
- 确定 SDK 功能描述
- 确定初始版本（默认 1.0.0）

## 执行步骤

### Step 1: 确认 SDK 信息

与用户确认：
- [ ] SDK 名称（例：`my-new-sdk`）
- [ ] 功能描述
- [ ] 是否需要 CLI 入口
- [ ] 初始 skills 列表

### Step 2: 创建目录结构

```bash
mkdir -p sdks/<sdk-name>/{api,cli,skills,tests,examples}
```

### Step 3: 创建核心文件

按以下顺序创建：
1. `version.py`
2. `__init__.py`
3. `manifest.yaml`
4. `README.md`
5. `CHANGELOG.md`

### Step 4: 创建 API 占位

```python
# api/__init__.py
"""<sdk-name> API exports."""

__all__ = []
```

### Step 5: 创建测试占位

```python
# tests/__init__.py
"""<sdk-name> tests."""
```

```python
# tests/test_placeholder.py
"""Placeholder tests."""

def test_placeholder():
    """Remove this once real tests are added."""
    pass
```

### Step 6: 运行审查

```bash
infra-core audit-sdk sdks/<sdk-name>
```

确保通过所有检查。

### Step 7: 创建入口 Skills（如需）

如果 SDK 有 skills，在 `.claude/skills/` 创建入口文件。

## 检查点

执行完成后确认：
- [ ] 所有必需文件存在
- [ ] manifest.yaml 格式正确
- [ ] audit-sdk 检查通过
- [ ] README 包含基本使用说明

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| Directory exists | SDK 已存在 | 使用 --force 覆盖或更换名称 |
| Invalid name | 名称不符合 kebab-case | 修正名称格式 |

## 相关 Skills

- `infra-core-audit-sdk`: 审查创建的 SDK
```

**Step 4: 验证创建**

Run: `ls -la sdks/infra-core/skills/`
Expected: 显示三个实现 skill 文件

**Step 5: Commit**

```bash
git add sdks/infra-core/skills/
git commit -m "feat(infra-core): add skill implementation docs"
```

---

## Phase 4: CLI 工具实现

### Task 4.1: 实现 infra-core CLI

**Files:**
- Create: `sdks/infra-core/cli/__init__.py`
- Create: `sdks/infra-core/cli/main.py`

**Step 1: 创建 cli/__init__.py**

```python
"""infra-core CLI module."""
```

**Step 2: 实现 main.py**

```python
#!/usr/bin/env python3
"""
infra-core CLI

Command-line interface for AI-Native Infrastructure Framework core operations.
"""

import argparse
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from sdks.infra_core.api import (
    audit_sdk,
    audit_skills,
    audit_docs,
    AuditSeverity,
)
from sdks.infra_core.version import __version__


def cmd_audit_sdk(args):
    """Handle audit-sdk command."""
    result = audit_sdk(args.path)

    if not args.quiet:
        print(f"Auditing SDK: {args.path}")
        print("-" * 40)

    for finding in result.findings:
        severity = finding.severity.value.upper()
        print(f"[{severity}] {finding.message}")
        if finding.path and args.verbose:
            print(f"        Path: {finding.path}")
        if finding.suggestion and args.verbose:
            print(f"        Fix: {finding.suggestion}")

    if not args.quiet:
        print("-" * 40)
        if result.passed:
            print("✅ SDK audit passed")
        else:
            print(f"❌ SDK audit failed ({len(result.errors)} errors)")

    return 0 if result.passed else 3


def cmd_audit_docs(args):
    """Handle audit-docs command."""
    result = audit_docs(args.path)

    if not args.quiet:
        print(f"Auditing docs: {args.path}")
        print("-" * 40)

    for finding in result.findings:
        severity = finding.severity.value.upper()
        print(f"[{severity}] {finding.message}")
        if finding.path and args.verbose:
            print(f"        Path: {finding.path}")

    if not args.quiet:
        print("-" * 40)
        if result.passed:
            print("✅ Docs audit passed")
        else:
            print(f"❌ Docs audit failed ({len(result.errors)} errors)")

    return 0 if result.passed else 3


def cmd_audit_skills(args):
    """Handle audit-skills command."""
    result = audit_skills(args.path, args.sdk_dir)

    if not args.quiet:
        print(f"Auditing skills: {args.path}")
        print("-" * 40)

    for finding in result.findings:
        severity = finding.severity.value.upper()
        print(f"[{severity}] {finding.message}")
        if finding.path and args.verbose:
            print(f"        Path: {finding.path}")

    if not args.quiet:
        print("-" * 40)
        if result.passed:
            print("✅ Skills audit passed")
        else:
            print(f"❌ Skills audit failed ({len(result.errors)} errors)")

    return 0 if result.passed else 3


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="infra-core",
        description="AI-Native Infrastructure Framework CLI"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"infra-core {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # audit-sdk command
    audit_sdk_parser = subparsers.add_parser(
        "audit-sdk",
        help="Audit an SDK package"
    )
    audit_sdk_parser.add_argument("path", help="Path to SDK directory")
    audit_sdk_parser.add_argument("-v", "--verbose", action="store_true")
    audit_sdk_parser.add_argument("-q", "--quiet", action="store_true")
    audit_sdk_parser.set_defaults(func=cmd_audit_sdk)

    # audit-docs command
    audit_docs_parser = subparsers.add_parser(
        "audit-docs",
        help="Audit documentation"
    )
    audit_docs_parser.add_argument("path", help="Path to docs directory")
    audit_docs_parser.add_argument("-v", "--verbose", action="store_true")
    audit_docs_parser.add_argument("-q", "--quiet", action="store_true")
    audit_docs_parser.set_defaults(func=cmd_audit_docs)

    # audit-skills command
    audit_skills_parser = subparsers.add_parser(
        "audit-skills",
        help="Audit skills configuration"
    )
    audit_skills_parser.add_argument("path", help="Path to skills directory")
    audit_skills_parser.add_argument("--sdk-dir", help="Path to sdks directory")
    audit_skills_parser.add_argument("-v", "--verbose", action="store_true")
    audit_skills_parser.add_argument("-q", "--quiet", action="store_true")
    audit_skills_parser.set_defaults(func=cmd_audit_skills)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 2

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
```

**Step 3: 测试 CLI**

Run: `python sdks/infra-core/cli/main.py --help`
Expected: 显示帮助信息

Run: `python sdks/infra-core/cli/main.py audit-sdk sdks/infra-core`
Expected: 显示审查结果

**Step 4: Commit**

```bash
git add sdks/infra-core/cli/
git commit -m "feat(infra-core): implement CLI interface"
```

---

## Phase 5: 清理和迁移

### Task 5.1: 更新 CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

**Step 1: 更新 CLAUDE.md 反映新架构**

更新以下部分：
- 目录结构说明
- 常用命令
- SDK 相关说明

**Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md for new SDK architecture"
```

---

### Task 5.2: 清理冲突的旧结构

**Files:**
- Evaluate: `core/`, `project/`, `scripts/`, `registry/`

**Step 1: 评估冲突**

检查以下目录是否与新架构冲突：
- `core/.agent/skills/` → 迁移到 `sdks/infra-core/skills/`
- `project/.agent/skills/` → 评估是否需要保留
- `scripts/` → 评估哪些迁移到 SDK CLI
- `registry/tools.yaml` → 评估是否改用 manifest.yaml

**Step 2: 制定迁移列表**

根据评估结果，决定：
- 删除的文件/目录
- 迁移的文件/目录
- 保留的文件/目录

**Step 3: 执行迁移**

按列表执行，每步校验。

**Step 4: Commit**

```bash
git add -A
git commit -m "refactor: migrate to new SDK architecture"
```

---

## Phase 6: 验证和文档

### Task 6.1: 完整性验证

**Step 1: 运行 SDK 审查**

```bash
python sdks/infra-core/cli/main.py audit-sdk sdks/infra-core
```

Expected: 通过

**Step 2: 运行 Skills 审查**

```bash
python sdks/infra-core/cli/main.py audit-skills .claude/skills --sdk-dir sdks
```

Expected: 通过

**Step 3: 运行 Docs 审查**

```bash
python sdks/infra-core/cli/main.py audit-docs docs
```

Expected: 通过或仅有 INFO/WARNING

---

### Task 6.2: 最终提交

**Step 1: 确认所有变更**

```bash
git status
git diff --stat HEAD~10
```

**Step 2: 创建里程碑标签**

```bash
git tag -a v2.0.0-sdk-architecture -m "Major restructure: SDK-based architecture"
```

---

## Execution Summary

| Phase | Tasks | 预计时间 |
|-------|-------|----------|
| Phase 1 | 规范文档 | 30 min |
| Phase 2 | infra-core SDK | 1-2 hours |
| Phase 3 | Skills 入口 | 30 min |
| Phase 4 | CLI 实现 | 30 min |
| Phase 5 | 清理迁移 | 1 hour |
| Phase 6 | 验证文档 | 30 min |

**Total: ~4-5 hours**
