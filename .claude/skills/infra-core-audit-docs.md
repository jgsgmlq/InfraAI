---
name: infra-core-audit-docs
description: 审查文档一致性和完整性
triggers:
  - "检查文档"
  - "审查文档"
  - "audit docs"
  - "check documentation"
sdk: infra-core
implementation: sdks/infra-core/skills/audit-docs.md
---

# 文档审查

检查项目文档的一致性和完整性。

## 用途

- 检查 Markdown 文件格式
- 验证内部链接有效性
- 检查代码块语言标签

## 调用方式

```python
from sdks.infra_core.api import audit_docs

result = audit_docs("docs/")
for finding in result.findings:
    print(f"[{finding.severity.value}] {finding.message}")
```

或 CLI:

```bash
infra-core audit-docs docs/
```

## 详细文档

完整实现逻辑请参考：`sdks/infra-core/skills/audit-docs.md`
