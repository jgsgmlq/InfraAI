# Command Palette (list-tools)

## Purpose
列出所有在注册表中注册的工具，以 Markdown 格式输出，方便 AI 和用户快速了解可用的工具。

## When to Use
- 开始新任务前，检查是否有现成工具可用
- 用户询问"有哪些工具"
- 需要了解工具的使用方法和参数

## Trigger Phrases
当用户说以下内容时，应使用此工具：
- "有哪些工具"
- "查看命令面板"
- "show me the tools"
- "what tools are available"
- "list tools"

## Command
```bash
# 使用默认注册表
python scripts/list_tools.py

# 指定注册表路径
python scripts/list_tools.py --registry path/to/tools.yaml
```

## Principles
1. **先查后做**：执行任何任务前，先检查是否有现成工具
2. **单一来源**：registry/tools.yaml 是工具的唯一真实来源
3. **格式友好**：输出 Markdown 格式，便于阅读和解析

## Checkpoints
执行前确认：
1. [ ] 当前目录是否为项目根目录（或已指定 --registry 路径）

## Recovery Strategy
- Exit 0: 成功输出工具列表
- Exit 2: 参数错误，检查 --registry 路径格式
- Exit 3: 注册表文件不存在或格式错误，检查文件路径
- 最多重试 1 次，失败后报告给用户

## HARD GATES (Non-Negotiable)
- [ ] 必须读取 registry/tools.yaml
- [ ] 必须输出 Markdown 格式
- [ ] 必须包含每个工具的 id、name、description、entry
