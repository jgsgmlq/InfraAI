---
name: infra-core-create-sdk
description: 创建新的 SDK 包
triggers:
  - "创建 SDK"
  - "新建 SDK"
  - "create SDK"
  - "new SDK package"
sdk: infra-core
implementation: sdks/infra-core/skills/create-sdk.md
---

# 创建 SDK

使用模板创建符合规范的新 SDK 包。

## 用途

- 自动生成 SDK 目录结构
- 创建标准配置文件
- 初始化版本和 changelog

## 调用方式

```bash
infra-core create-sdk my-new-sdk --description "我的 SDK"
```

## 生成内容

```
sdks/my-new-sdk/
├── __init__.py
├── version.py
├── manifest.yaml
├── README.md
├── CHANGELOG.md
├── api/
├── cli/
├── skills/
├── tests/
└── examples/
```

## 详细文档

完整实现逻辑请参考：`sdks/infra-core/skills/create-sdk.md`
