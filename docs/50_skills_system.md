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
