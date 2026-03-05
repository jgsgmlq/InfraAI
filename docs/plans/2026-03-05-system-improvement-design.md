# 系统改进设计文档

> 日期：2026-03-05
> 状态：已确认

---

## 1. 背景

基于 PRIME_DIRECTIVE 确立的项目定位（用户说人话 → AI 按 Skills 编程 → 工具辅助执行），需要改进系统以更好地服务这一目标。

### 当前问题

| 问题 | 影响 |
|------|------|
| 用户不知道能说什么 | 无法有效利用系统能力 |
| 缺乏上下文感知 | AI 不了解项目当前状态 |
| 外部插件能力不透明 | 用户不知道 superpowers 等插件能帮什么 |
| 日常编程 Skills 缺失 | AI 缺乏编程指导，只能依赖通用能力 |
| 工具输出不便于 AI 解析 | 降低 AI 工作效率 |

---

## 2. 设计目标

1. **用户体验**：用户清楚知道能说什么、系统能做什么
2. **AI 可操作性**：AI 有明确的编程指导（Skills）
3. **工具友好**：工具输出便于 AI 解析和使用
4. **能力透明**：明确哪些能力来自本地、哪些来自外部插件

---

## 3. 设计方案

### 3.1 模块一：增强 /init 初始化体验

**目标**：让用户清楚"能说什么"和"系统有哪些能力"

#### 3.1.1 能力清单展示

初始化时按场景分类展示能力：

```
📋 我能帮你做：

🔧 框架维护
   • "创建新工具" / "创建 SDK"
   • "检查工具健康" / "审查 SDK"
   • "部署框架到新项目"

💻 日常编程（需要时调用 superpowers 插件）
   • "帮我构思方案" → brainstorming
   • "帮我调试这个 bug" → systematic-debugging
   • "帮我写测试" → test-driven-development

💬 需求整理
   • "我有个想法..." → 会引导你逐步明确需求
```

#### 3.1.2 上下文感知

展示项目当前状态：

```
📊 项目状态：
   • 最近修改：<最近一次 commit 信息>
   • SDK 健康：✅ / ⚠️
   • 待办事项：<如果有 TODO 文件>
```

**实现方式**：
- 调用 `git log -1 --oneline` 获取最近提交
- 调用 `audit_all.py --quiet` 检查健康状态

#### 3.1.3 外部插件透明化

明确标注哪些能力来自外部插件：
- 本地能力：直接展示
- 外部能力：标注 `(superpowers 插件)`

---

### 3.2 模块二：Skills 能力补充

**目标**：补充核心日常编程 Skills，复杂场景桥接 superpowers

#### 3.2.1 新增 Skills 清单

| Skill | 用途 | 来源 | 复杂度 |
|-------|------|------|--------|
| `clarify-requirements` | 引导用户整理需求（轻量版） | 自写 | 低 |
| `quick-fix` | 简单 bug 修复指南 | 自写 | 低 |
| `add-feature` | 添加新功能指南 | 自写 | 中 |
| `bridge-superpowers` | 桥接 superpowers 插件的引导 | 自写 | 低 |

#### 3.2.2 Skills 设计原则

1. **轻量优先**：简单场景用本地 Skill，复杂场景桥接 superpowers
2. **明确边界**：每个 Skill 说明何时应转向 superpowers
3. **触发短语覆盖**：中英文常见表达都能触发

#### 3.2.3 clarify-requirements Skill

**用途**：当用户需求不明确时，引导整理需求

**触发短语**：
- "我有个想法..."
- "我想做一个..."
- "帮我想想怎么..."

**流程**：
1. 确认目标：你想解决什么问题？
2. 确认范围：需要实现哪些功能？
3. 确认约束：有哪些限制条件？
4. 输出需求摘要

**与 superpowers:brainstorming 的边界**：
- 简单需求（3 个问题内能明确）→ clarify-requirements
- 复杂需求（需要探索方案、权衡取舍）→ superpowers:brainstorming

#### 3.2.4 quick-fix Skill

**用途**：简单 bug 修复指南

**触发短语**：
- "这里有个 bug"
- "修一下这个错误"
- "fix this"

**流程**：
1. 定位问题：错误信息是什么？
2. 复现问题：能稳定复现吗？
3. 修复并验证
4. 提交修复

**与 superpowers:systematic-debugging 的边界**：
- 简单 bug（错误明显、原因清晰）→ quick-fix
- 复杂 bug（原因不明、需要深入分析）→ superpowers:systematic-debugging

#### 3.2.5 add-feature Skill

**用途**：添加新功能指南

**触发短语**：
- "添加一个功能"
- "实现这个需求"
- "add feature"

**流程**：
1. 确认需求（必要时调用 clarify-requirements）
2. 确认实现位置
3. 编写代码
4. 编写测试
5. 验证并提交

**与 superpowers 的边界**：
- 简单功能（单文件、明确需求）→ add-feature
- 复杂功能（多文件、需要设计）→ superpowers:brainstorming + writing-plans

#### 3.2.6 bridge-superpowers Skill

**用途**：告诉 AI 和用户可用的 superpowers 能力

**内容**：列出 superpowers 插件的主要能力和触发方式

---

### 3.3 模块三：工具辅助能力增强

**目标**：让工具输出更便于 AI 解析和使用

#### 3.3.1 统一输出格式

为以下工具添加输出选项：

| 工具 | 新增选项 | 用途 |
|------|----------|------|
| `list_tools.py` | `--json` | JSON 格式输出，便于程序解析 |
| `list_tools.py` | `--compact` | 精简表格输出，便于快速查看 |
| `list_skills.py` | `--json` | JSON 格式输出 |
| `list_skills.py` | `--compact` | 精简表格输出 |
| `audit_all.py` | `--json` | JSON 格式输出审查结果 |

**JSON 输出格式示例**：
```json
{
  "tools": [
    {"id": "list-tools", "name": "Command Palette", "command": "python scripts/list_tools.py"}
  ],
  "count": 1
}
```

#### 3.3.2 审查工具整合

- `audit_all.py` 作为主入口
- 整合 registry、SDK、skills、docs 审查
- 统一输出格式和退出码

#### 3.3.3 错误提示增强

错误信息包含：
1. 错误描述
2. 可能原因
3. 修复建议
4. 相关文档链接

**示例**：
```
[ERROR] SDK manifest not found: sdks/my-sdk/manifest.yaml

可能原因：
  • SDK 目录结构不完整
  • manifest.yaml 文件名拼写错误

修复建议：
  • 运行: python sdks/infra-core/cli/main.py create-sdk my-sdk
  • 或手动创建 manifest.yaml（参考 docs/60_sdk_specification.md）
```

---

## 4. 交付物清单

### 4.1 模块一：/init 增强

| 交付物 | 类型 | 说明 |
|--------|------|------|
| `.claude/commands/init.md` | 更新 | 新的初始化流程定义 |

### 4.2 模块二：Skills 补充

| 交付物 | 类型 | 说明 |
|--------|------|------|
| `core/.agent/skills/clarify-requirements.md` | 新增 | 需求整理 Skill |
| `core/.agent/skills/quick-fix.md` | 新增 | 简单 bug 修复 Skill |
| `core/.agent/skills/add-feature.md` | 新增 | 添加功能 Skill |
| `core/.agent/skills/bridge-superpowers.md` | 新增 | superpowers 桥接 Skill |

### 4.3 模块三：工具增强

| 交付物 | 类型 | 说明 |
|--------|------|------|
| `scripts/list_tools.py` | 更新 | 添加 --json, --compact |
| `scripts/list_skills.py` | 更新 | 添加 --json, --compact |
| `scripts/audit_all.py` | 更新 | 添加 --json, 增强错误提示 |

---

## 5. 实施优先级

| 优先级 | 模块 | 原因 |
|--------|------|------|
| P0 | /init 增强 | 直接影响用户第一印象和使用体验 |
| P1 | Skills 补充 | 扩展 AI 编程指导能力 |
| P1 | 工具增强 | 提升 AI 工作效率 |

---

## 6. 验收标准

1. `/init` 后用户能清楚知道可以说什么
2. 简单需求可通过本地 Skills 完成，无需每次调用 superpowers
3. 复杂需求能平滑过渡到 superpowers
4. 工具输出支持 JSON 和 compact 格式
5. 错误提示包含修复建议

---

## 7. 后续步骤

调用 `superpowers:writing-plans` 创建详细实施计划。
