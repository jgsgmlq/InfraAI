# SDK 稳定性原则实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 更新 CLAUDE.md，添加 SDK 稳定性原则和工作模式识别机制，确保 AI 默认不会随意修改框架层文件。

**Architecture:** 在 CLAUDE.md 的关键位置插入新的规则章节，包括架构定位、工作模式识别、HARD GATES 和更新的工作流程。

**Tech Stack:** Markdown 文档编辑

---

## Task 1: 添加 SDK 稳定性原则章节

**Files:**
- Modify: `CLAUDE.md:66-82` (在"关键规则（HARD RULES）"部分之后添加)

**Step 1: 在 HARD RULES 部分后添加 SDK 稳定性原则**

在 `CLAUDE.md` 的第 82 行（`### FORBIDDEN（禁止行为）` 部分之后）插入新章节：

```markdown
### SDK 稳定性原则（CRITICAL）

**D:\infra_demo\ 是一个可移植的 IDE 平台，包含框架层和项目层。**

#### 架构定位

- **框架层**（稳定，不随意修改）：`sdks/`、`scripts/`、`.claude/`、`docs/`、`core/`、`registry/`
- **项目层**（用户工作区）：在根目录下创建的项目子目录（如 `my-app/`、`data-analysis/`）

**架构类比**：
- SDK 框架 = npm 包库（提供可复用的工具）
- 用户项目 = 使用 npm 包的应用（调用工具，不修改工具源码）

#### 工作模式识别

AI 有两种工作模式：

1. **项目开发模式（默认）**：
   - 在 `D:\infra_demo\<project-name>\` 子目录中工作
   - 调用 SDK 的 API 和 CLI 工具
   - 不修改框架层文件
   - 新功能先在项目中实现和验证

2. **SDK 开发模式（受限触发）**：
   - 只有在以下**任一条件**满足时才进入：
     - 当前工作目录是 `D:\infra_demo\` 且用户命令涉及修改框架层
     - 用户明确下达命令（包含"修改 SDK"、"扩展 SDK"、"创建 SDK 工具"、"更新 SDK"、"SDK 开发"、"编写 SDK"、"修改框架工具"、"扩展框架"等关键词）
     - 用户的命令意图明确表示要修改框架层文件（`sdks/`、`scripts/`、`.claude/`、`docs/`、`core/`、`registry/`）

#### SDK 稳定性 HARD GATES

**MUST（必须遵守）**：
- 默认项目开发模式，除非明确触发 SDK 开发模式
- 用户项目必须在独立子目录中，不得与框架目录冲突（不能命名为 `sdks`、`scripts`、`docs`、`.claude`、`core`、`registry` 等）
- 新功能优先在项目中实现，成熟后再询问用户是否迁移到 SDK
- 不确定当前模式时，必须先询问用户
- 创建项目时，必须先询问项目名称，然后在 `D:\infra_demo\<project-name>\` 下创建项目目录

**FORBIDDEN（禁止行为）**：
- 禁止在项目开发模式下修改框架层文件（`sdks/`、`scripts/`、`.claude/`、`docs/`、`core/`、`registry/`）
- 禁止在没有明确触发条件的情况下进入 SDK 开发模式
- 禁止在根目录 `D:\infra_demo\` 直接创建项目文件（如 `index.js`、`main.py`、`app.py` 等）
- 禁止擅自将项目代码迁移到 SDK（必须先询问用户）
```

**Step 2: 验证插入位置**

运行以下命令确认修改：

```bash
grep -n "SDK 稳定性原则" CLAUDE.md
```

Expected: 显示新添加的章节行号

**Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add SDK stability principle to CLAUDE.md

Add critical SDK stability rules:
- Define portable IDE platform architecture (framework layer + project layer)
- Establish project development mode (default) vs SDK development mode
- Add mode recognition mechanism with multiple triggers
- Define HARD GATES to prevent accidental SDK modifications

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Task 2: 更新工作流程章节

**Files:**
- Modify: `CLAUDE.md:105-126` (替换现有的"工作流程"部分)

**Step 1: 替换工作流程章节**

将 `CLAUDE.md` 的第 105-126 行（`## 工作流程` 部分）替换为：

```markdown
## 工作流程

当收到新需求时，按以下顺序执行：

### 1. 判断工作模式

- **默认**：项目开发模式
- **检查**：是否满足 SDK 开发模式的触发条件？
  - 当前工作目录是 `D:\infra_demo\` 且命令涉及修改框架层？
  - 用户明确下达修改 SDK 的命令？
  - 用户的命令意图明确表示要修改框架层文件？
- **不确定时**：询问用户

### 2. 项目开发模式流程

```
1. 确认项目目录 → 是否已有项目目录？
   ↓ 没有
2. 询问项目名称 → 用户提供项目名称（如 my-web-app）
   ↓
3. 创建项目目录 → mkdir D:\infra_demo\<project-name>
   ↓
4. 切换到项目目录 → cd D:\infra_demo\<project-name>
   ↓
5. 查看现有 SDK → python scripts/list_tools.py
   ↓
6. 有现成能力？ → 调用 SDK API 或 CLI
   ↓ 没有
7. 在项目中实现功能
   ↓
8. 功能成熟后，询问是否迁移到 SDK
```

### 3. SDK 开发模式流程

```
1. 确认用户意图 → 确实要修改 SDK？
   ↓ 是
2. 查看现有 SDK → ls sdks/
   ↓
3. 按规范创建/扩展 SDK：
   - [ ] sdks/<sdk>/api/<module>.py
   - [ ] sdks/<sdk>/tests/test_<module>.py
   - [ ] sdks/<sdk>/skills/<skill>.md
   - [ ] .claude/skills/<sdk>-<skill>.md
   - [ ] 更新 manifest.yaml
   ↓
4. 运行 audit-sdk 验证
   ↓
5. 完成
```
```

**Step 2: 验证修改**

运行以下命令确认修改：

```bash
grep -A 5 "判断工作模式" CLAUDE.md
```

Expected: 显示新的工作流程内容

**Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update workflow to include mode recognition

Update workflow section to:
- Add mode recognition step (project vs SDK development)
- Add project creation flow with directory setup
- Add SDK development flow with confirmation
- Clarify when to ask user for mode confirmation

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Task 3: 更新 AI 行为约束章节

**Files:**
- Modify: `CLAUDE.md:130-148` (扩展"AI 行为约束"部分)

**Step 1: 在 AI 行为约束部分添加项目创建规则**

在 `CLAUDE.md` 的第 130 行（`## AI 行为约束` 部分）之后，在"创建 SDK 前"之前插入：

```markdown
### 判断工作模式时

- 默认处于项目开发模式
- 检查是否满足 SDK 开发模式的触发条件
- 不确定时，必须先询问用户
- 不要擅自进入 SDK 开发模式

### 创建项目前

- 询问项目名称和用途
- 确认项目名称不与框架目录冲突
- 在 `D:\infra_demo\` 下创建项目子目录
- 不要在根目录直接创建项目文件

### 创建项目时

- 先切换到项目目录
- 查看现有 SDK 能力（运行 `python scripts/list_tools.py`）
- 优先使用 SDK 工具，而不是重新实现

### 创建项目后

- 如果实现了通用功能，询问用户是否迁移到 SDK
- 不要擅自修改框架层文件
- 不要擅自将项目代码迁移到 SDK
```

**Step 2: 验证修改**

运行以下命令确认修改：

```bash
grep -A 3 "判断工作模式时" CLAUDE.md
```

Expected: 显示新添加的行为约束

**Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add project creation rules to AI behavior constraints

Add detailed AI behavior rules for:
- Mode recognition and confirmation
- Project creation workflow
- Project directory setup
- SDK tool usage priority
- Feature migration to SDK

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Task 4: 更新目录结构说明

**Files:**
- Modify: `CLAUDE.md:20-57` (更新"目录结构"部分)

**Step 1: 在目录结构中添加项目层说明**

在 `CLAUDE.md` 的第 56 行（`└── registry/` 之后）添加：

```markdown
│
├── [项目层 - 用户工作区]
├── my-web-app/              # 用户项目示例 1
│   ├── src/
│   └── ...
├── data-analysis/           # 用户项目示例 2
│   ├── notebooks/
│   └── ...
└── <project-name>/          # 其他用户项目
    └── ...
```

**Step 2: 更新架构说明**

将第 59-62 行的"架构说明"部分更新为：

```markdown
**架构说明**：
- **框架层**：`sdks/`、`scripts/`、`.claude/`、`docs/`、`core/`、`registry/` - 稳定的工具库，不随意修改
- **项目层**：根目录下的项目子目录（如 `my-app/`）- 用户工作区，灵活开发
- Skills 入口层：`.claude/skills/` - Claude Code 自动识别
- `scripts/`, `registry/`: 保留用于后向兼容
```

**Step 3: 验证修改**

运行以下命令确认修改：

```bash
grep -A 5 "项目层" CLAUDE.md | head -10
```

Expected: 显示新添加的项目层说明

**Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update directory structure to show project layer

Update directory structure documentation to:
- Add project layer examples (my-web-app, data-analysis)
- Clarify framework layer vs project layer distinction
- Update architecture description

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Task 5: 验证完整性

**Files:**
- Read: `CLAUDE.md`

**Step 1: 验证所有修改已应用**

运行以下命令检查关键章节：

```bash
# 检查 SDK 稳定性原则
grep -n "SDK 稳定性原则" CLAUDE.md

# 检查工作模式识别
grep -n "工作模式识别" CLAUDE.md

# 检查项目层说明
grep -n "项目层" CLAUDE.md

# 检查 AI 行为约束
grep -n "判断工作模式时" CLAUDE.md
```

Expected: 所有关键章节都存在

**Step 2: 读取完整的 CLAUDE.md**

```bash
cat CLAUDE.md
```

Expected: 文档结构完整，所有新章节都已添加

**Step 3: 运行健康检查**

```bash
python scripts/audit_all.py
```

Expected: 无新的错误（board-strategy 的错误是已知的）

**Step 4: 最终 Commit（如有遗漏）**

如果发现任何遗漏或需要调整的地方，进行最终修改并提交：

```bash
git add CLAUDE.md
git commit -m "docs: final adjustments to SDK stability documentation

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## 验收标准

实施完成后，CLAUDE.md 应该包含：

1. ✅ **SDK 稳定性原则章节**：
   - 架构定位（框架层 vs 项目层）
   - 工作模式识别（项目开发模式 vs SDK 开发模式）
   - SDK 稳定性 HARD GATES

2. ✅ **更新的工作流程**：
   - 判断工作模式步骤
   - 项目开发模式流程（包含项目创建）
   - SDK 开发模式流程（包含确认步骤）

3. ✅ **扩展的 AI 行为约束**：
   - 判断工作模式时的规则
   - 创建项目前/时/后的规则
   - 明确禁止的行为

4. ✅ **更新的目录结构**：
   - 包含项目层示例
   - 明确框架层和项目层的区别

---

## 预期效果

实施后，AI 将：

1. **默认不修改框架层**：除非明确触发 SDK 开发模式
2. **创建项目时询问名称**：在独立子目录中创建项目
3. **优先使用 SDK 工具**：而不是重新实现
4. **功能成熟后询问迁移**：不擅自将项目代码迁移到 SDK
5. **不确定时询问用户**：而不是擅自假设

---

**计划结束**
