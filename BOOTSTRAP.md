# Framework Bootstrap Guide

> 本文件是 AI 初始化新项目的指南。

## 快速开始

将本框架部署到新项目：

```bash
# 方法 1: 使用初始化工具（推荐）
python scripts/init_project.py --target /path/to/new/project

# 方法 2: 手动复制
cp -r core/* /path/to/new/project/
cp CLAUDE.md /path/to/new/project/
cp requirements.txt /path/to/new/project/
```

## 初始化后的目录结构

```
new_project/
├── CLAUDE.md              # 项目上下文（已复制）
├── requirements.txt       # Python 依赖（已复制）
├── core/                  # 核心框架（已复制）
│   ├── docs/              # 规范文档
│   ├── registry/          # 工具注册表
│   ├── scripts/           # 基础工具
│   └── .agent/            # AI 技能
└── project/               # 项目特定内容（待创建）
    ├── tools/             # 项目工具
    └── config/            # 项目配置
```

## 首次使用检查清单

初始化后，按以下步骤验证：

1. [ ] 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

2. [ ] 验证基础工具
   ```bash
   python core/scripts/list_tools.py --registry core/registry/tools.yaml
   ```

3. [ ] 运行健康检查
   ```bash
   python core/scripts/audit_registry.py --registry core/registry/tools.yaml
   ```

4. [ ] 读取 CLAUDE.md 理解项目规则

## AI 初始化指令

当 AI 收到"初始化项目"的请求时，执行以下步骤：

### Step 1: 创建目录结构
```bash
mkdir -p project/tools project/config
```

### Step 2: 验证框架完整性
```bash
python core/scripts/audit_registry.py --registry core/registry/tools.yaml
```

### Step 3: 询问项目信息
- 项目名称
- 项目描述
- 主要用途

### Step 4: 自定义 CLAUDE.md
根据项目信息更新 CLAUDE.md 中的项目描述。

### Step 5: 确认完成
```bash
python core/scripts/list_tools.py --registry core/registry/tools.yaml
```

## 添加新工具的位置

| 工具类型 | 位置 | 说明 |
|---------|------|------|
| 框架工具 | `core/scripts/` | 可跨项目复用的通用工具 |
| 项目工具 | `project/tools/` | 项目特定的工具 |

## 注册表管理

- 框架工具注册在 `core/registry/tools.yaml`
- 项目工具注册在 `project/registry/tools.yaml`（如需要）

## 常见问题

### Q: 如何升级框架？
A: 从最新版本复制 `core/` 目录，保留 `project/` 不变。

### Q: 项目工具和框架工具冲突怎么办？
A: 项目工具使用不同的 ID 前缀（如 `proj-xxx`）。

### Q: 如何贡献通用工具回框架？
A: 将工具从 `project/tools/` 移至 `core/scripts/`，并更新注册表。
