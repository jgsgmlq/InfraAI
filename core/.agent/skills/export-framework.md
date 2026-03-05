# Framework Export Tool

## Purpose
将 AI-Native Infrastructure Framework 导出为可移植的压缩包，方便分发和部署到其他项目。

## When to Use
- 需要将框架分享给他人时
- 准备部署到新环境时
- 创建框架的备份时

## Trigger Phrases
当用户说以下内容时，应使用此工具：
- "导出框架"
- "打包框架"
- "export framework"
- "创建框架包"
- "备份框架"

## Command
```bash
# 基本导出
python scripts/export_framework.py

# 指定输出文件
python scripts/export_framework.py --out my_framework.zip

# 预览模式（不实际导出）
python scripts/export_framework.py --dry-run

# 详细输出
python scripts/export_framework.py --verbose

# 包含项目特定文件（不推荐）
python scripts/export_framework.py --include-project
```

## Principles
1. **只导出核心**：默认不包含项目特定文件（project/）
2. **包含清单**：生成 manifest.json 记录导出内容
3. **可验证**：导出后可通过 audit 工具验证完整性

## Checkpoints
执行前确认：
1. [ ] 输出文件路径是否正确
2. [ ] 是否需要包含项目特定文件

## Recovery Strategy

### Exit 0 (Success)
- 导出成功
- 验证生成的 zip 文件

### Exit 2 (Parameter Error)
- 检查参数格式
- 运行 `--help` 查看正确用法

### Exit 3 (Runtime Error)
- 权限错误：检查输出路径权限
- 空间不足：确保有足够磁盘空间
- 文件冲突：使用 `--out` 指定不同路径

## Output Structure
导出的 zip 包含：

```
framework.zip
├── manifest.json          # 内容清单
├── CLAUDE.md              # 项目上下文
├── BOOTSTRAP.md           # 初始化指南
├── requirements.txt       # Python 依赖
└── core/                  # 核心框架
    ├── docs/
    ├── registry/
    ├── scripts/
    └── .agent/
```

## HARD GATES (Non-Negotiable)
- [ ] 必须生成 manifest.json
- [ ] 必须包含 core/ 目录
- [ ] 必须包含 CLAUDE.md, BOOTSTRAP.md, requirements.txt
- [ ] 默认不包含 project/ 目录
