# Board Strategy SDK

> 打板策略逆向工程与 Workflow 系统

用于 A 股连板晋级预测的数据分析和策略执行框架。

## 功能特性

- **数据标准化**：统一的预测记录数据模型
- **行情查询**：基于 AKShare 的 A 股量价数据查询
- **数据录入**：支持 CSV 导入和自动补全
- **CoT 分析**：结构化拆解思维链，提取有效因子
- **归因分析**：因子×结果交叉分析，识别有效因子
- **策略流水线**：五步自动化流水线（标的池→因子打分→排名→盘前修正→决策）

## 安装

```bash
cd sdks/board-strategy
pip install -r requirements.txt
```

## 快速开始

### 1. 数据录入

从 CSV 导入预测记录：

```bash
python cli/main.py ingest -i data.csv -o data/predictions
```

### 2. 数据增强

补全量价数据：

```bash
python cli/main.py enrich -i data/predictions/record.json -o data/enriched
```

### 3. CoT 分析

结构化拆解 CoT：

```bash
python cli/main.py analyze-cot -i data/enriched/record.json -o data/cot_analysis
```

### 4. 归因分析

生成因子×结果矩阵：

```bash
python cli/main.py attribution -i data/cot_analysis -o data/attribution
```

### 5. 运行流水线

执行完整策略流水线：

```bash
python cli/main.py run-pipeline --date 2026-03-03 --stage post
```

## 数据模型

### 预测记录（PredictionRecord）

```python
{
  "date": "2026-03-03",
  "time": "post_market",  # post_market | pre_market
  "model": "Miromind",
  "prompt": "原始提问文本",
  "prediction_id": "唯一标识",
  "predicted_stocks": "推荐标的",
  "is_sealed": true,
  "is_touched": true,
  "raw_cot": "完整 CoT 原文"
}
```

### 增强股票数据（EnrichedStock）

```python
{
  "code": "000001",
  "name": "股票名称",
  "board_count": 3,
  "prev_close": 10.5,
  "limit_up_price": 11.55,
  "volume": 1000000,
  "turnover_rate": 5.0
}
```

## 开发

### 运行测试

```bash
python -m pytest tests/ -v
```

### 测试覆盖率

```bash
python -m pytest tests/ --cov=api --cov-report=html
```

## 实施路线图

- [x] **P1 — 数据基础**：数据模型 + 录入工具 + AKShare 查询
- [ ] **P2 — 逆向工程**：CoT 分析器 + 配对对比 + 归因矩阵
- [ ] **P3 — 流水线**：五步 Workflow 实现 + 配置化
- [ ] **P4 — 验证迭代**：回测工具 + 每日报告 + 因子权重调优

## 技术栈

- **数据模型**：Pydantic 2.0+
- **行情数据**：AKShare
- **数据处理**：Pandas
- **测试**：Pytest

## 许可证

MIT License
