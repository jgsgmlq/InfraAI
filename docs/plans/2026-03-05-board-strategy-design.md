# 打板策略逆向工程与 Workflow 设计方案

> 日期：2026-03-05
> 状态：P1 阶段已完成 ✅
> SDK：board-strategy
> 分支：board-strategy-design
> 最后更新：2026-03-05 16:30

## 实施进度

- ✅ **P1 — 数据基础**（已完成 100%）
  - ✅ SDK 基础结构（__init__.py, version.py, manifest.yaml）
  - ✅ 数据模型（api/data_model.py）- PredictionRecord, EnrichedStock, CoTAnalysis
  - ✅ AKShare 查询封装（api/stock_query.py）- 单只/批量查询、缓存、涨停板查询
  - ✅ 数据录入工具（api/ingest.py）- CSV 导入、自动补全、JSON 保存
  - ✅ CLI 框架（cli/main.py）- 6 个子命令框架
  - ✅ 测试覆盖（tests/）- 16 个测试全部通过
  - ✅ 文档（README.md, requirements.txt）
- ⏳ **P2 — 逆向工程**（待实施）
- ⏳ **P3 — 流水线**（待实施）
- ⏳ **P4 — 验证迭代**（待实施）

**测试状态：**
```
tests/test_data_model.py:    5 passed ✅
tests/test_stock_query.py:   5 passed ✅
tests/test_ingest.py:        6 passed ✅
-----------------------------------
Total:                      16 passed ✅
```

**Git 提交记录：**
- `5d93807` - feat: implement board-strategy SDK P1 phase (data foundation)
- `e53e33e` - feat: complete board-strategy SDK P1 phase implementation
- `44f791c` - feat: add remaining P1 phase files

---

## 背景

量化研究员使用 Miromind 大模型进行 A 股连板晋级预测盲测，积累了 20+ 条"小样本、厚数据"。每天进行盘后 + 盘前两次预测配对。目前预测过程为"黑盒"模式，需要：

1. **逆向工程**：拆解 CoT，提取有效因子，归因成功/失败原因
2. **重构 Workflow**：从一问一答改造为多步骤、逻辑透明的自动化流水线

## 设计决策

- **路线**：自底向上（先标注后建模）— 数据驱动，适合小样本厚数据
- **行情数据源**：AKShare（免费、覆盖 A 股全市场）
- **产出方式**：先方案后工具，逐步实现
- **RAG 系统**：当前不使用，后期可能接入。设计中预留接口，标记 `[RAG-READY]`

## 关键约束

1. **数据来源**：Miromind 网页端对话，手动复制粘贴 CoT 文本保存
2. **信息来源限制**：CoT 中关联的外部来源只能复制标题，无法复制完整 URL
3. **标题质量**：混合情况 — 有些清晰可溯源，有些模糊
4. **无 RAG**：当前不依赖任何外部资讯检索，纯量价数据 + CoT 文本分析
5. **应对策略**：检索源分析采用"标题语义分析"，通过标题关键词判断信息类型

## 第一部分：数据标准化层

### 1.1 现有数据字段

用户已有的表格数据：

| 字段 | 说明 |
|------|------|
| 日期 | 预测日期 |
| 时间 | 盘后/盘前 |
| 模型 | 使用的模型（Miromind） |
| prompt | 原始提问文本 |
| ID | 唯一标识 |
| 预测结果 | 模型推荐的标的 |
| 涨停结果 | 实际涨停情况 |
| 是否封板 | bool |
| 是否触板 | bool |

另有部分原始聊天记录（含完整 CoT、检索源标题、工具调用痕迹），尚未结构化。

### 1.2 统一数据模型

```json
{
  "date": "2026-03-03",
  "time": "post_market | pre_market",
  "model": "Miromind",
  "prompt": "原始提问文本",
  "prediction_id": "唯一标识",
  "predicted_stocks": "模型输出的推荐标的文本",
  "limit_up_result": "实际涨停结果",
  "is_sealed": true,
  "is_touched": true,
  "raw_cot": "完整 CoT 原文（手动从网页复制粘贴）",
  "cited_source_titles": ["新闻标题1", "研报标题2"],
  "source_quality": "clear | mixed | vague"
}
```

### 1.3 增强数据模型（通过 AKShare 查询补全）

```json
{
  "enriched_stocks": [
    {
      "code": "000001",
      "name": "股票名称",
      "board_count": 3,
      "prev_close": 10.5,
      "limit_up_price": 11.55,
      "next_day_open": 11.80,
      "next_day_high": 12.10,
      "premium_rate": 0.022,
      "sector": "新能源"
    }
  ]
}
```

### 1.4 行情查询工具

`stock-data-query` CLI 工具：
- 输入：股票代码 + 日期
- 输出：量价数据（开高低收、涨停板数、连板数、封单量、换手率等）
- 数据源：AKShare
- 支持批量查询

### 1.5 数据录入工具

`ingest-prediction` CLI 工具：
- 粘贴模式：粘贴聊天文本，LLM 自动解析结构化
- 表格导入：从 CSV/Excel 导入已整理数据
- 自动补全：通过 stock-data-query 补全量价字段

## 第二部分：CoT 逆向工程引擎

### 2.1 CoT 结构化拆解

用本地 LLM 对每条 CoT 执行因子标注，输出结构化维度：

```json
{
  "factors_mentioned": {
    "price_volume": ["封单量大", "换手率低", "缩量加速"],
    "news_catalyst": ["政策利好", "行业事件"],
    "sentiment": ["市场情绪高涨", "亏钱效应弱"],
    "sector_linkage": ["板块联动强", "龙头效应"],
    "technical": ["突破前高", "趋势良好"],
    "timing": ["尾盘加速", "集合竞价放量"]
  },
  "confidence_signals": ["强烈推荐", "大概率"],
  "risk_warnings": ["追高风险", "分歧较大"],
  "retrieval_sources": {
    "titles": ["来源标题1", "来源标题2"],
    "title_categories": ["policy", "industry", "stock_specific", "sentiment"],
    "source_count": 5,
    "source_recency": "1h以内 | 当天 | 隔夜"
  },
  "reasoning_chain": [
    "step1: 识别连板高度",
    "step2: 分析封板强度",
    "step3: 匹配题材热度",
    "step4: 综合判断晋级概率"
  ]
}
```

注意：`retrieval_sources` 基于标题语义分析（非 URL 溯源）。`[RAG-READY]` 后期接入 RAG 后可通过标题反向匹配还原原文。

### 2.2 配对对比分析

对每个交易日的盘后 + 盘前预测对进行自动对比：

| 对比维度 | 分析目标 |
|----------|----------|
| 标的变化 | 盘前新增/删除了哪些票？为什么？ |
| 因子变化 | 哪些因子在盘前被新增/修正？ |
| 信息增量 | 盘前多了什么信息（竞价数据、隔夜消息）？ |
| 来源差异 | 盘前引用了哪些新来源标题？ |
| 结果差异 | 盘前修正后准确率是否提升？ |

### 2.3 归因分析矩阵

因子 × 结果交叉表：

```
              封板成功    炸板失败    未触板
量价因子A       8次        2次        1次    → 胜率 72%
资讯因子B       5次        5次        3次    → 胜率 38%（噪音因子）
情绪因子C       6次        1次        0次    → 胜率 86%（关键因子）
```

输出：有效因子排名表 + 噪音因子黑名单

## 第三部分：打板策略 Workflow 架构

### 3.1 五步流水线

```
T-1 盘后触发                              T日 盘前触发
    │                                        │
    ▼                                        ▼
┌─────────┐   ┌──────────┐   ┌─────────┐  ┌──────────┐   ┌─────────┐
│ Step 1   │→ │ Step 2    │→ │ Step 3   │  │ Step 4    │→ │ Step 5   │
│ 标的池   │   │ 因子打分  │   │ 排名筛选 │  │ 盘前修正  │   │ 最终决策 │
│ 构建     │   │ 引擎      │   │ 输出     │  │ 引擎      │   │ 输出     │
└─────────┘   └──────────┘   └─────────┘  └──────────┘   └─────────┘
     ↑              ↑              ↑             ↑              ↑
  AKShare       量价因子       规则约束      集合竞价数据    置信度阈值
  涨停板池      因子模型        可追溯        量价修正       风控规则
```

### 3.2 各步骤详解

**Step 1 — 标的池构建（T-1 盘后）**
- 输入：当日涨停板数据（AKShare 自动获取）
- 过滤规则：连板 ≥ N 板、非 ST、非次新（可配置）
- 输出：候选标的池（约 10-30 只）
- `[RAG-READY]` 后期可为每只票检索最新相关新闻和研报

**Step 2 — 因子打分引擎（T-1 盘后）**
- 按逆向工程提取出的有效因子逐项打分
- LLM 结构化输出（JSON），每个因子 0-10 分 + 理由
- 每个因子独立打分，禁止"综合判断"
- 当前仅使用量价类因子；`[RAG-READY]` 后期可加入资讯因子

**Step 3 — 排名筛选输出（T-1 盘后）**
- 按加权总分排名，输出 Top 5
- 附带因子得分卡 + 风险标记
- 完整打分记录写入数据库

**Step 4 — 盘前修正引擎（T日 09:00-09:25）**
- 输入：Step 3 的 Top 5 + 集合竞价量价数据
- 数据源：AKShare 集合竞价数据（如可获取）
- LLM 重新评估，输出修正后 Top 5 + 修正理由
- `[RAG-READY]` 后期可加入隔夜公告、外盘变化等资讯增量

**Step 5 — 最终决策输出（T日 09:25）**
- 置信度过滤：低于阈值标记为"观望"
- 风控规则：单日最大仓位、连续亏损暂停等
- 输出：标的 + 操作建议 + 完整推理链 + 风控状态

### 3.3 设计原则

| 原则 | 说明 |
|------|------|
| 透明可追溯 | 每步输出结构化 JSON，每个判断有明确因子依据 |
| 因子独立 | 每个因子单独打分，禁止 LLM 做模糊"综合判断" |
| 双时点验证 | 盘后初筛 + 盘前修正，利用信息时差提升准确率 |
| 强制记录 | 所有中间过程写入数据库，供事后归因分析 |
| 规则可配置 | 过滤阈值、因子权重、风控参数均为可调配置项 |
| RAG 预留 | 所有资讯检索点标记 `[RAG-READY]`，当前不启用 |

## 第四部分：SDK 架构

### 4.1 目录结构

```
sdks/board-strategy/
├── __init__.py
├── version.py
├── manifest.yaml
├── api/
│   ├── data_model.py          # 预测记录数据模型
│   ├── ingest.py              # 数据录入与标准化
│   ├── stock_query.py         # AKShare 行情查询封装
│   ├── cot_analyzer.py        # CoT 结构化拆解引擎
│   ├── attribution.py         # 归因分析（因子×结果矩阵）
│   ├── factor_scorer.py       # 因子打分引擎
│   ├── workflow.py            # 五步流水线编排
│   └── config.py              # 可配置参数
├── cli/
│   └── main.py                # CLI 入口
│       # 子命令：ingest, enrich, analyze-cot, attribution, run-pipeline, backtest
├── skills/
│   ├── reverse-engineer.md    # 逆向工程 Skill
│   ├── run-pipeline.md        # 运行流水线 Skill
│   └── daily-report.md        # 每日策略报告 Skill
├── tests/
│   ├── test_data_model.py
│   ├── test_cot_analyzer.py
│   ├── test_attribution.py
│   └── test_factor_scorer.py
└── data/
    ├── predictions/           # 预测记录存储
    ├── enriched/              # 增强后的数据
    └── config.yaml            # 策略配置文件
```

### 4.2 技术选型

| 组件 | 技术 | 理由 |
|------|------|------|
| 行情数据 | AKShare | 免费、覆盖 A 股全市场涨停板数据 |
| 数据存储 | JSON → SQLite | 初期 JSON 快速迭代，后期迁移 SQLite |
| LLM 调用 | 本地模型 API | CoT 分析、因子打分均由本地 LLM 执行 |
| RAG 检索 | `[RAG-READY]` 预留 | 当前不使用，后期接入用户自建向量库 |
| 流水线编排 | Python + cron/手动 | 简单可靠，不引入额外框架 |

### 4.3 实施路线图

| 阶段 | 内容 | 产出 | 状态 |
|------|------|------|------|
| P1 — 数据基础 | 数据模型 + 录入工具 + AKShare 查询 | 20+ 条数据结构化完成 | ✅ 已完成 |
| P2 — 逆向工程 | CoT 分析器 + 配对对比 + 归因矩阵 | 有效因子排名表 | ⏳ 待实施 |
| P3 — 流水线 | 五步 Workflow 实现 + 配置化 | 可运行的策略流水线 | ⏳ 待实施 |
| P4 — 验证迭代 | 回测工具 + 每日报告 + 因子权重调优 | 策略稳定性验证 | ⏳ 待实施 |

---

## P1 阶段实施详情

### 已完成的模块

**1. 数据模型（api/data_model.py）**
- `PredictionRecord`：预测记录基础模型
- `EnrichedStock`：增强股票数据模型
- `CoTAnalysis`：CoT 分析结果模型
- `FactorsMentioned`：因子分类模型
- `RetrievalSources`：检索源信息模型
- `EnrichedPrediction`：完整增强预测记录

**2. AKShare 查询封装（api/stock_query.py）**
- `StockDataQuery` 类：
  - `query_stock_data(code, date)`：单只股票查询
  - `batch_query(codes, date)`：批量查询（支持重试）
  - `query_limit_up_stocks(date)`：涨停板股票查询
  - 内置缓存机制（可配置 TTL）
  - 错误处理和重试逻辑

**3. 数据录入工具（api/ingest.py）**
- `DataIngestor` 类：
  - `import_from_csv(file_path)`：从 CSV 导入
  - `enrich_with_stock_data(record)`：自动补全量价数据
  - `save_prediction(prediction, output_dir)`：保存为 JSON
  - `import_and_enrich(csv_path, output_dir)`：一键导入并增强
  - 自动提取股票代码（正则匹配）

**4. CLI 框架（cli/main.py）**
- 6 个子命令：
  - `ingest`：数据录入与标准化
  - `enrich`：通过 AKShare 补全量价数据
  - `analyze-cot`：CoT 结构化拆解（待实现）
  - `attribution`：归因分析（待实现）
  - `run-pipeline`：运行五步流水线（待实现）
  - `backtest`：回测工具（待实现）

**5. 测试覆盖（tests/）**
- `test_data_model.py`：5 个测试（序列化、反序列化、验证）
- `test_stock_query.py`：5 个测试（查询、缓存、错误处理）
- `test_ingest.py`：6 个测试（导入、提取、补全、保存）

### 使用示例

```bash
# 安装依赖
cd sdks/board-strategy
pip install -r requirements.txt

# 从 CSV 导入预测记录
python cli/main.py ingest -i data.csv -o data/predictions

# 补全量价数据
python cli/main.py enrich -i data/predictions/record.json -o data/enriched

# 运行测试
python -m pytest tests/ -v
```

### 待用户测试的功能

1. CSV 导入功能（需要准备符合格式的 CSV 文件）
2. AKShare 数据查询（需要网络连接）
3. 数据增强和保存功能

---
