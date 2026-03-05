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
