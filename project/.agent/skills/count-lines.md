# Count Lines Tool

## Purpose
统计指定目录下代码文件的行数，输出每个文件的行数和总数。

## When to Use
- 需要了解项目代码量时
- 代码审查时统计变更量
- 项目报告需要代码行数数据

## Trigger Phrases
当用户说以下内容时，应使用此工具：
- "统计代码行数"
- "有多少行代码"
- "count lines"
- "代码量统计"

## Command
```bash
# 统计当前目录的 .py 文件
python scripts/count_lines.py

# 统计指定目录
python scripts/count_lines.py /path/to/project

# 统计其他类型文件
python scripts/count_lines.py --ext .js

# 排除空行
python scripts/count_lines.py --no-empty
```

## Principles
1. 递归扫描所有子目录
2. 输出 Markdown 格式便于阅读
3. 忽略无法读取的文件（只警告，不中断）

## Recovery Strategy

### Exit 0 (Success)
- 成功输出统计结果

### Exit 2 (Parameter Error)
- 检查参数格式
- 运行 --help 查看用法

### Exit 3 (Runtime Error)
- 路径不存在：检查路径拼写
- 不是目录：确保指向目录而非文件

## HARD GATES (Non-Negotiable)
- [ ] 输出 Markdown 表格格式
- [ ] 显示每个文件的行数
- [ ] 显示总文件数和总行数
