"""
测试数据录入工具
"""

import pytest
import tempfile
import csv
from pathlib import Path
from unittest.mock import Mock, patch

from api.ingest import DataIngestor, IngestError
from api.data_model import PredictionRecord, EnrichedStock
from api.stock_query import StockDataQuery


@pytest.fixture
def sample_csv_file():
    """创建示例 CSV 文件"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'date', 'time', 'model', 'prompt', 'prediction_id',
            'predicted_stocks', 'is_sealed', 'is_touched'
        ])
        writer.writeheader()
        writer.writerow({
            'date': '2026-03-03',
            'time': 'post_market',
            'model': 'Miromind',
            'prompt': '测试提问',
            'prediction_id': 'test-001',
            'predicted_stocks': '000001, 000002',
            'is_sealed': 'true',
            'is_touched': 'true'
        })
        temp_path = f.name

    yield temp_path

    # 清理
    Path(temp_path).unlink(missing_ok=True)


def test_ingestor_initialization():
    """测试录入器初始化"""
    ingestor = DataIngestor()
    assert ingestor.stock_query is not None


def test_import_from_csv(sample_csv_file):
    """测试从 CSV 导入"""
    ingestor = DataIngestor()
    records = ingestor.import_from_csv(sample_csv_file)

    assert len(records) == 1
    assert records[0].prediction_id == 'test-001'
    assert records[0].date == '2026-03-03'
    assert records[0].is_sealed is True


def test_import_from_nonexistent_csv():
    """测试导入不存在的 CSV 文件"""
    ingestor = DataIngestor()

    with pytest.raises(IngestError, match="文件不存在"):
        ingestor.import_from_csv("nonexistent.csv")


def test_extract_stock_codes():
    """测试提取股票代码"""
    ingestor = DataIngestor()

    # 测试提取 6 位数字代码
    codes = ingestor._extract_stock_codes("推荐 000001 和 000002")
    assert "000001" in codes
    assert "000002" in codes

    # 测试去重
    codes = ingestor._extract_stock_codes("000001, 000001, 000002")
    assert len(codes) == 2


def test_enrich_with_stock_data():
    """测试补全股票数据"""
    # 创建模拟的股票查询器
    mock_query = Mock(spec=StockDataQuery)
    mock_query.batch_query.return_value = {
        "000001": {
            "code": "000001",
            "name": "平安银行",
            "close": 10.5,
            "volume": 1000000,
            "turnover_rate": 5.0,
            "board_count": 2
        }
    }

    ingestor = DataIngestor(stock_query=mock_query)

    record = PredictionRecord(
        date="2026-03-03",
        time="post_market",
        model="Miromind",
        prompt="测试",
        prediction_id="test-001",
        predicted_stocks="000001"
    )

    enriched = ingestor.enrich_with_stock_data(record)

    assert enriched.prediction.prediction_id == "test-001"
    assert len(enriched.enriched_stocks) == 1
    assert enriched.enriched_stocks[0].code == "000001"


def test_save_prediction():
    """测试保存预测记录"""
    from api.data_model import EnrichedPrediction

    ingestor = DataIngestor()

    record = PredictionRecord(
        date="2026-03-03",
        time="post_market",
        model="Miromind",
        prompt="测试",
        prediction_id="test-save-001",
        predicted_stocks="000001"
    )

    enriched = EnrichedPrediction(
        prediction=record,
        enriched_stocks=[],
        cot_analysis=None
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = ingestor.save_prediction(enriched, tmpdir)

        # 验证文件已创建
        assert Path(file_path).exists()
        assert "test-save-001.json" in file_path