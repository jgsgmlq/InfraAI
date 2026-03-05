# Project Initialization Tool

## Purpose
初始化新项目，复制 AI-Native Infrastructure Framework 的核心文件，并设置项目目录结构。

## When to Use
- 开始一个新项目时
- 将框架部署到已有项目时
- 用户说"初始化项目"或"创建新项目"

## Trigger Phrases
当用户说以下内容时，应使用此工具：
- "初始化一个新项目"
- "创建新项目"
- "部署框架到..."
- "init project"
- "bootstrap new project"

## Command
```bash
# 基本用法
python scripts/init_project.py --target /path/to/new/project

# 指定项目名称和描述
python scripts/init_project.py --target /path/to/project --name "My Project" --description "项目描述"

# 预览模式（不实际执行）
python scripts/init_project.py --target /path/to/project --dry-run

# 强制覆盖已有文件
python scripts/init_project.py --target /path/to/project --force
```

## Principles
1. **非破坏性**：默认不覆盖已有目录，需要 `--force` 明确指定
2. **完整初始化**：一次性创建所有必要的目录和文件
3. **可预览**：`--dry-run` 可以预览将要执行的操作

## Checkpoints
执行前确认：
1. [ ] 目标路径是否正确
2. [ ] 项目名称
3. [ ] 是否需要覆盖已有内容

## Recovery Strategy

### Exit 0 (Success)
- 项目初始化成功
- 运行 `python core/scripts/audit_registry.py` 验证

### Exit 2 (Parameter Error)
- 检查 `--target` 是否提供
- 运行 `--help` 查看正确用法

### Exit 3 (Runtime Error)
- 目标目录非空：使用 `--force` 或选择新路径
- 权限错误：检查目录权限
- 源文件缺失：确保在框架根目录执行

## HARD GATES (Non-Negotiable)
- [ ] 必须提供 `--target` 参数
- [ ] 初始化后必须能通过 `audit_registry.py` 检查
- [ ] CLAUDE.md 必须被正确自定义
