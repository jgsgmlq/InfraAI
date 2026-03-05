"""
数据模型定义

包含预测记录、增强股票数据、CoT 分析结果等数据结构。
"""

from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class PredictionRecord(BaseModel):
    """预测记录 - 对应 1.2 统一数据模型"""

    date: str = Field(..., description="预测日期，格式：YYYY-MM-DD")
    time: Literal["post_market", "pre_market"] = Field(..., description="盘后或盘前")
    model: str = Field(default="Miromind", description="使用的模型")
    prompt: str = Field(..., description="原始提问文本")
    prediction_id: str = Field(..., description="唯一标识")
    predicted_stocks: str = Field(..., description="模型输出的推荐标的文本")
    limit_up_result: Optional[str] = Field(None, description="实际涨停结果")
    is_sealed: Optional[bool] = Field(None, description="是否封板")
    is_touched: Optional[bool] = Field(None, description="是否触板")
    raw_cot: Optional[str] = Field(None, description="完整 CoT 原文")
    cited_source_titles: List[str] = Field(default_factory=list, description="引用的来源标题")
    source_quality: Optional[Literal["clear", "mixed", "vague"]] = Field(None, description="来源质量")

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2026-03-03",
                "time": "post_market",
                "model": "Miromind",
                "prompt": "今天哪些连板股明天可能继续涨停？",
                "prediction_id": "20260303-post-001",
                "predicted_stocks": "股票A, 股票B",
                "is_sealed": True,
                "is_touched": True
            }
        }


class EnrichedStock(BaseModel):
    """增强股票数据 - 对应 1.3 增强数据模型"""

    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    board_count: int = Field(..., description="连板数")
    prev_close: float = Field(..., description="前收盘价")
    limit_up_price: float = Field(..., description="涨停价")
    next_day_open: Optional[float] = Field(None, description="次日开盘价")
    next_day_high: Optional[float] = Field(None, description="次日最高价")
    premium_rate: Optional[float] = Field(None, description="溢价率")
    sector: Optional[str] = Field(None, description="所属板块")
    volume: Optional[float] = Field(None, description="成交量")
    turnover_rate: Optional[float] = Field(None, description="换手率")
    seal_amount: Optional[float] = Field(None, description="封单量")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "000001",
                "name": "平安银行",
                "board_count": 3,
                "prev_close": 10.5,
                "limit_up_price": 11.55,
                "next_day_open": 11.80,
                "next_day_high": 12.10,
                "premium_rate": 0.022,
                "sector": "金融"
            }
        }


class FactorsMentioned(BaseModel):
    """CoT 中提到的因子"""

    price_volume: List[str] = Field(default_factory=list, description="量价因子")
    news_catalyst: List[str] = Field(default_factory=list, description="资讯催化")
    sentiment: List[str] = Field(default_factory=list, description="市场情绪")
    sector_linkage: List[str] = Field(default_factory=list, description="板块联动")
    technical: List[str] = Field(default_factory=list, description="技术面")
    timing: List[str] = Field(default_factory=list, description="时机因子")


class RetrievalSources(BaseModel):
    """检索源信息"""

    titles: List[str] = Field(default_factory=list, description="来源标题列表")
    title_categories: List[Literal["policy", "industry", "stock_specific", "sentiment"]] = Field(
        default_factory=list, description="标题分类"
    )
    source_count: int = Field(default=0, description="来源数量")
    source_recency: Optional[Literal["1h以内", "当天", "隔夜"]] = Field(None, description="来源时效性")


class CoTAnalysis(BaseModel):
    """CoT 分析结果 - 对应 2.1 CoT 结构化拆解"""

    prediction_id: str = Field(..., description="关联的预测记录 ID")
    factors_mentioned: FactorsMentioned = Field(..., description="提到的因子")
    confidence_signals: List[str] = Field(default_factory=list, description="置信度信号")
    risk_warnings: List[str] = Field(default_factory=list, description="风险警告")
    retrieval_sources: RetrievalSources = Field(..., description="检索源信息")
    reasoning_chain: List[str] = Field(default_factory=list, description="推理链")

    class Config:
        json_schema_extra = {
            "example": {
                "prediction_id": "20260303-post-001",
                "factors_mentioned": {
                    "price_volume": ["封单量大", "换手率低"],
                    "sentiment": ["市场情绪高涨"]
                },
                "confidence_signals": ["强烈推荐"],
                "risk_warnings": ["追高风险"],
                "retrieval_sources": {
                    "titles": ["政策利好消息"],
                    "title_categories": ["policy"],
                    "source_count": 1,
                    "source_recency": "当天"
                },
                "reasoning_chain": [
                    "step1: 识别连板高度",
                    "step2: 分析封板强度"
                ]
            }
        }


class EnrichedPrediction(BaseModel):
    """增强后的预测记录（包含股票详细数据）"""

    prediction: PredictionRecord = Field(..., description="原始预测记录")
    enriched_stocks: List[EnrichedStock] = Field(default_factory=list, description="增强后的股票数据")
    cot_analysis: Optional[CoTAnalysis] = Field(None, description="CoT 分析结果")
