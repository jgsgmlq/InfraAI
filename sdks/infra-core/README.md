# infra-core SDK

AI-Native Infrastructure Framework 的核心 SDK。

## 安装

```bash
# 作为项目依赖
pip install -e sdks/infra-core
```

## 功能

- **Registry 管理**: 加载和验证工具注册表
- **SDK 审查**: 检查 SDK 包完整性
- **文档审查**: 检查文档一致性
- **Skills 审查**: 验证 skills 配置

## 使用

### Python API

```python
from sdks.infra_core.api import audit_sdk, audit_docs

# 审查 SDK
result = audit_sdk("sdks/my-sdk")

# 审查文档
result = audit_docs("docs/")
```

### CLI

```bash
infra-core audit-sdk sdks/my-sdk
infra-core audit-docs docs/
```

## Skills

- `infra-core-audit-sdk`: SDK 包完整性审查
- `infra-core-audit-docs`: 文档一致性审查
- `infra-core-create-sdk`: 创建新 SDK 包
