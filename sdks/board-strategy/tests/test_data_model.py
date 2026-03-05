"""
测试数据模型
"""

import pytest
from api.data_model import (
    PredictionRecord,
    EnrichedStock,
    CoTAnalysis,
    FactorsMentioned,
    RetrievalSources,
    EnrichedPrediction
)


def test_prediction_record_creation():
    """测试创建预测记录"""
    record = PredictionRecord(
        date="2026-03-03",
        time="post_market",
        model="Miromind",
        prompt="今天哪些连板股明天可能继续涨停？",
        prediction_id="20260303-post-001",
        predicted_stocks="000001, 000002",
        is_sealed=True,
        is_touched=True
    )

    assert record.date == "2026-03-03"
    assert record.time == "post_market"
    assert record.prediction_id == "20260303-post-001"


def test_prediction_record_json_serialization():
    """测试预测记录的 JSON 序列化"""
    record = PredictionRecord(
        date="2026-03-03",
        time="pre_market",
        model="Miromind",
        prompt="测试提问",
        prediction_id="test-001",
        predicted_stocks="000001",
    )

    # 序列化为字典
    data = record.model_dump()
    assert data["date"] == "2026-03-03"
    assert data["time"] == "pre_market"

    # 从字典反序列化
    record2 = PredictionRecord(**data)
    assert record2.date == record.date
    assert record2.prediction_id == record.prediction_id


def test_enriched_stock_creation():
    """测试创建增强股票数据"""
    stock = EnrichedStock(
        code="000001",
        name="平安银行",
        board_count=3,
        prev_close=10.5,
        limit_up_price=11.55,
        next_day_open=11.80,
        premium_rate=0.022,
        sector="金融"
    )

    assert stock.code == "000001"
    assert stock.board_count == 3
    assert stock.premium_rate == 0.022


def test_cot_analysis_creation():
    """测试创建 CoT 分析结果"""
    factors = FactorsMentioned(
        price_volume=["封单量大", "换手率低"],
        sentiment=["市场情绪高涨"]
    )

    sources = RetrievalSources(
        titles=["政策利好消息"],
        title_categories=["policy"],
        source_count=1,
        source_recency="当天"
    )

    analysis = CoTAnalysis(
        prediction_id="20260303-post-001",
        factors_mentioned=factors,
        confidence_signals=["强烈推荐"],
        risk_warnings=["追高风险"],
        retrieval_sources=sources,
        reasoning_chain=["step1: 识别连板高度", "step2: 分析封板强度"]
    )

    assert analysis.prediction_id == "20260303-post-001"
    assert len(analysis.factors_mentioned.price_volume) == 2
    assert len(analysis.reasoning_chain) == 2


def test_enriched_prediction_creation():
    """测试创建完整的增强预测记录"""
    record = PredictionRecord(
        date="2026-03-03",
        time="post_market",
        model="Miromind",
        prompt="测试",
        prediction_id="test-001",
        predicted_stocks="000001"
    )

    stock = EnrichedStock(
        code="000001",
        name="测试股票",
        board_count=2,
        prev_close=10.0,
        limit_up_price=11.0
    )

    enriched = EnrichedPrediction(
        prediction=record,
        enriched_stocks=[stock],
        cot_analysis=None
    )

    assert enriched.prediction.prediction_id == "test-001"
    assert len(enriched.enriched_stocks) == 1
    assert enriched.enriched_stocks[0].code == "000001"