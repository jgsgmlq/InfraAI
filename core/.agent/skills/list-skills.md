# List Skills Tool

## Purpose
列出所有可用的 skills，帮助 AI 了解自己有哪些能力可用。

## When to Use
- 开始新对话时，了解可用能力
- 用户问"你能做什么"
- 需要找特定功能时

## Trigger Phrases
当用户说以下内容时，应使用此工具：
- "有哪些 skills"
- "你能做什么"
- "list skills"
- "what can you do"

## Command
```bash
# 列出所有 skills
python scripts/list_skills.py

# 详细模式（含触发短语和命令）
python scripts/list_skills.py --verbose

# 只看核心 skills
python scripts/list_skills.py --location core

# 只看项目 skills
python scripts/list_skills.py --location project
```

## Principles
1. 自动扫描所有标准位置
2. 跳过模板文件和 README
3. 输出 Markdown 格式

## Recovery Strategy
- Exit 0: 成功列出 skills
- Exit 2: 参数错误，检查 --location 值

## HARD GATES (Non-Negotiable)
- [ ] 必须扫描 core、project、external 三个位置
- [ ] 必须输出 skill 名称和用途
