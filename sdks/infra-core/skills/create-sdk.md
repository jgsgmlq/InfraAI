# 创建 SDK - 实现文档

## 概述

创建符合框架规范的新 SDK 包，自动生成所有必需文件和目录结构。

## 前置条件

- 确定 SDK 名称（kebab-case）
- 确定 SDK 功能描述
- 确定初始版本（默认 1.0.0）

## 执行步骤

### Step 1: 确认 SDK 信息

与用户确认：
- [ ] SDK 名称（例：`my-new-sdk`）
- [ ] 功能描述
- [ ] 是否需要 CLI 入口
- [ ] 初始 skills 列表

### Step 2: 创建目录结构

```bash
mkdir -p sdks/<sdk-name>/{api,cli,skills,tests,examples}
```

### Step 3: 创建核心文件

按以下顺序创建：
1. `version.py`
2. `__init__.py`
3. `manifest.yaml`
4. `README.md`
5. `CHANGELOG.md`

### Step 4: 创建 API 占位

```python
# api/__init__.py
"""<sdk-name> API exports."""

__all__ = []
```

### Step 5: 创建测试占位

```python
# tests/__init__.py
"""<sdk-name> tests."""
```

```python
# tests/test_placeholder.py
"""Placeholder tests."""

def test_placeholder():
    """Remove this once real tests are added."""
    pass
```

### Step 6: 运行审查

```bash
infra-core audit-sdk sdks/<sdk-name>
```

确保通过所有检查。

### Step 7: 创建入口 Skills（如需）

如果 SDK 有 skills，在 `.claude/skills/` 创建入口文件。

## 检查点

执行完成后确认：
- [ ] 所有必需文件存在
- [ ] manifest.yaml 格式正确
- [ ] audit-sdk 检查通过
- [ ] README 包含基本使用说明

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| Directory exists | SDK 已存在 | 使用 --force 覆盖或更换名称 |
| Invalid name | 名称不符合 kebab-case | 修正名称格式 |

## 相关 Skills

- `infra-core-audit-sdk`: 审查创建的 SDK
