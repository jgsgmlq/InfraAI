# Portability Guide

本文档说明框架的可移植性设计和使用方法。

## 分层架构

```
┌─────────────────────────────────────────────┐
│                  项目层                      │
│  project/tools/  project/config/            │
│  项目特定的工具和配置                         │
│  ❌ 不移植                                   │
├─────────────────────────────────────────────┤
│                  核心层                      │
│  core/docs/  core/scripts/  core/.agent/    │
│  通用规范、基础工具、技能系统                  │
│  ✅ 可移植                                   │
├─────────────────────────────────────────────┤
│                  入口层                      │
│  CLAUDE.md  BOOTSTRAP.md  requirements.txt  │
│  项目上下文和初始化指南                       │
│  ✅ 可移植（需自定义）                        │
└─────────────────────────────────────────────┘
```

## 可移植内容清单

### 完全可移植（直接复制）

| 路径 | 内容 | 说明 |
|------|------|------|
| `core/` | 整个目录 | 框架核心 |
| `requirements.txt` | Python 依赖 | 基础依赖 |
| `BOOTSTRAP.md` | 初始化指南 | AI 读取 |

### 可移植但需自定义

| 路径 | 内容 | 需要修改 |
|------|------|----------|
| `CLAUDE.md` | 项目上下文 | 项目名称、描述 |

### 不可移植

| 路径 | 内容 | 原因 |
|------|------|------|
| `project/` | 项目特定内容 | 项目相关 |
| `docs/PROJECT_VISION.md` | 项目愿景 | 项目相关 |
| `docs/REQUIREMENTS.md` | 需求清单 | 项目相关 |
| `docs/IMPLEMENTATION_PLAN.md` | 实施计划 | 项目相关 |

---

## 移植方法

### 方法 1: 使用初始化工具（推荐）

```bash
python scripts/init_project.py --target /path/to/new/project --name "My Project"
```

### 方法 2: 使用打包工具

```bash
# 导出框架包
python scripts/export_framework.py --out framework.zip

# 在新项目中解压
cd /path/to/new/project
unzip framework.zip
```

### 方法 3: 手动复制

```bash
# 1. 复制核心框架
cp -r core/ /path/to/new/project/

# 2. 复制入口文件
cp CLAUDE.md BOOTSTRAP.md requirements.txt /path/to/new/project/

# 3. 创建项目目录
mkdir -p /path/to/new/project/project/{tools,config}

# 4. 自定义 CLAUDE.md
# 编辑 /path/to/new/project/CLAUDE.md 更新项目信息
```

---

## 升级框架

当框架有新版本时：

```bash
# 1. 备份项目特定内容
cp -r project/ project_backup/

# 2. 更新核心框架
rm -rf core/
cp -r /path/to/new/framework/core/ ./

# 3. 更新入口文件（注意保留自定义内容）
# 手动合并 CLAUDE.md 的变化

# 4. 验证
python core/scripts/audit_registry.py --registry core/registry/tools.yaml
```

---

## 扩展点

### 添加项目工具

1. 在 `project/tools/` 创建脚本
2. 在 `project/registry/tools.yaml` 注册（可选）
3. 在 `project/skills/` 添加技能文档（可选）

### 自定义规范

1. 在 `project/docs/` 添加项目特定的规范
2. 在 `CLAUDE.md` 中引用

### 覆盖核心行为

如需修改核心工具行为：
1. 复制 `core/scripts/xxx.py` 到 `project/tools/`
2. 修改副本
3. 更新调用路径

---

## 版本兼容性

| 框架版本 | 兼容性说明 |
|---------|-----------|
| 1.x | 初始版本，基础功能 |

升级时检查 `core/docs/CHANGELOG.md`（如存在）了解变化。

---

## 常见问题

### Q: 核心工具和项目工具 ID 冲突怎么办？
A: 项目工具使用前缀，如 `proj-xxx`，核心工具使用纯名称如 `list-tools`。

### Q: 如何贡献工具回核心框架？
A:
1. 确保工具是通用的，不依赖项目特定内容
2. 移动到 `core/scripts/`
3. 更新 `core/registry/tools.yaml`
4. 添加到 `core/.agent/skills/`

### Q: 框架升级会破坏我的项目工具吗？
A: 不会。`project/` 目录完全独立，框架升级只影响 `core/`。
