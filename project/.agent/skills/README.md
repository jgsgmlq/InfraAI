# Project Skills

本目录存放项目特定的 skills，不随框架移植。

## 目录结构

```
project/.agent/
├── skills/          # 自己编写的项目 skills
│   └── README.md
└── external/        # 从外部导入的 skills
    └── README.md
```

## 如何添加自定义 Skill

1. 复制模板：
   ```bash
   cp core/.agent/skills/_skill_template.md project/.agent/skills/my_skill.md
   ```

2. 编辑 skill 文件，填写：
   - Purpose（用途）
   - Trigger Phrases（触发短语）
   - Command（命令）
   - Recovery Strategy（恢复策略）
   - HARD GATES（硬性要求）

3. 如果 skill 对应一个工具，确保工具已注册在 `project/registry/tools.yaml`

## 命名规范

| 类型 | 命名 | 示例 |
|------|------|------|
| 工具类 skill | `<tool-id>.md` | `data-processor.md` |
| 流程类 skill | `<action>_<target>.md` | `deploy_production.md` |
| 外部导入 | `<source>_<name>.md` | `github_pr_review.md` |
