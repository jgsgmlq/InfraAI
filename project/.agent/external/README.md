# External Skills

本目录存放从外部来源导入的 skills。

## 导入方法

### 方法 1: 手动复制

```bash
# 从其他项目复制 skill
cp /path/to/other/project/.agent/skills/useful_skill.md project/.agent/external/

# 从 URL 下载（如果提供）
curl -o project/.agent/external/skill_name.md https://example.com/skills/skill_name.md
```

### 方法 2: 从框架包导入

```bash
# 解压框架包
unzip external_framework.zip -d /tmp/framework

# 复制需要的 skills
cp /tmp/framework/core/.agent/skills/desired_skill.md project/.agent/external/
```

## 导入后的检查清单

- [ ] 检查 skill 是否依赖特定工具
- [ ] 如果依赖工具，确保工具也已导入
- [ ] 更新触发短语以适应项目上下文
- [ ] 测试 skill 是否正常工作

## 外部 Skill 的修改

如果需要修改外部 skill：
1. **不要直接修改** external/ 中的文件（便于后续更新）
2. 复制到 skills/ 目录：
   ```bash
   cp project/.agent/external/skill.md project/.agent/skills/skill_custom.md
   ```
3. 在副本中进行修改

## 来源追踪

建议在导入的 skill 文件顶部添加来源注释：

```markdown
<!--
Source: https://github.com/example/framework
Version: 1.0.0
Imported: 2024-01-15
-->
# Skill Name
...
```
