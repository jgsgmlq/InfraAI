# 故障排查指南

本文档帮助解决使用 AI-Native Infrastructure Framework 时遇到的常见问题。

---

## 1. 审查工具问题

### 问题：`audit_registry.py` 报告缺少文件

**症状：**
```
[ERROR] my-tool: Script not found: scripts/my_tool.py
[ERROR] my-tool: Smoke test not found: scripts/smoke/smoke_my_tool.sh
```

**原因：**
- 工具已注册但文件未创建
- 文件路径与 registry 中的 `entry` 不匹配

**解决方案：**
1. 运行 `python scripts/audit_registry.py --fix` 自动生成模板
2. 手动检查 `registry/tools.yaml` 中的 `entry` 路径

---

### 问题：`audit-sdk` 报告 manifest 错误

**症状：**
```
[ERROR] Missing required field in manifest: version
```

**原因：**
- `manifest.yaml` 缺少必需字段

**解决方案：**
确保 `manifest.yaml` 包含以下字段：
```yaml
name: my-sdk
version: "1.0.0"
description: SDK description
```

---

### 问题：`audit-skills` 报告 frontmatter 错误

**症状：**
```
[ERROR] Missing required frontmatter field: description
```

**原因：**
- Skill 文件缺少 YAML frontmatter
- frontmatter 缺少必需字段

**解决方案：**
确保 skill 文件以正确的 frontmatter 开头：
```markdown
---
name: my-skill
description: 一句话描述
---

# Skill 内容
```

---

## 2. 导入和路径问题

### 问题：`ModuleNotFoundError: No module named 'yaml'`

**原因：**
- 未安装 PyYAML 依赖

**解决方案：**
```bash
pip install pyyaml
```

---

### 问题：`ImportError: attempted relative import`

**原因：**
- 直接运行 SDK 内部模块而不是通过 CLI

**解决方案：**
1. 从项目根目录运行命令
2. 使用 CLI 入口：
   ```bash
   python sdks/infra-core/cli/main.py audit-sdk sdks/infra-core
   ```

---

### 问题：Windows 路径问题

**症状：**
- 路径中的反斜杠导致错误
- 文件找不到但路径看起来正确

**解决方案：**
1. 使用正斜杠 `/` 而不是反斜杠 `\`
2. 或使用 Python 的 `Path` 对象

---

## 3. Smoke Test 问题

### 问题：Smoke test 在 Windows 上失败

**症状：**
```
bash: python: command not found
```

**原因：**
- Git Bash 无法找到 Python

**解决方案：**
1. 确保 Python 在 PATH 中
2. 使用完整路径：
   ```bash
   /c/Python314/python.exe scripts/list_tools.py
   ```

---

### 问题：Smoke test 权限错误

**症状：**
```
Permission denied
```

**解决方案：**
```bash
chmod +x scripts/smoke/smoke_*.sh
```

---

## 4. SDK 创建问题

### 问题：SDK 结构不完整

**解决方案：**
使用检查清单确保 SDK 包含：
- [ ] `__init__.py`
- [ ] `version.py`
- [ ] `manifest.yaml`
- [ ] `README.md`
- [ ] `CHANGELOG.md`
- [ ] `api/` 目录
- [ ] `tests/` 目录

运行审查确认：
```bash
python sdks/infra-core/cli/main.py audit-sdk sdks/your-sdk
```

---

## 5. Git 和 GitHub 问题

### 问题：SSH 认证失败

**症状：**
```
git@github.com: Permission denied (publickey)
```

**解决方案：**
1. 检查 SSH 密钥是否存在：
   ```bash
   ls ~/.ssh/id_rsa.pub
   ```
2. 将公钥添加到 GitHub: https://github.com/settings/keys
3. 测试连接：
   ```bash
   ssh -T git@github.com
   ```

---

### 问题：SSH agent 未运行

**解决方案：**
```bash
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_rsa
```

---

## 6. 常见错误代码

| 退出码 | 含义 | 常见原因 |
|--------|------|----------|
| 0 | 成功 | - |
| 2 | 参数错误 | 无效的命令行参数 |
| 3 | 运行时错误 | 文件不存在、权限问题、审查失败 |

---

## 7. 获取帮助

如果以上方案都无法解决问题：

1. **查看详细输出**：
   ```bash
   python scripts/audit_all.py --verbose
   ```

2. **检查日志**：
   查看错误输出（stderr）获取详细信息

3. **报告问题**：
   - GitHub Issues: https://github.com/jgsgmlq/InfraAI/issues
   - 包含：错误信息、操作步骤、环境信息（OS、Python 版本）

---

## 8. 快速诊断命令

```bash
# 检查 Python 版本
python --version

# 检查 PyYAML 是否安装
python -c "import yaml; print(yaml.__version__)"

# 运行完整审查
python scripts/audit_all.py

# 检查单个 SDK
python sdks/infra-core/cli/main.py audit-sdk sdks/infra-core -v

# 运行所有测试
python -m pytest sdks/infra-core/tests/ -v
```
