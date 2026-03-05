"""
数据录入工具

支持多种方式录入预测数据：
- 粘贴模式：解析聊天文本
- CSV 导入：从表格导入
- 自动补全：调用 stock_query 补全量价字段
"""

import json
import csv
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .data_model import PredictionRecord, EnrichedStock, EnrichedPrediction
from .stock_query import StockDataQuery, StockQueryError


class IngestError(Exception):
    """数据录入异常"""
    pass


class DataIngestor:
    """数据录入器"""

    def __init__(self, stock_query: Optional[StockDataQuery] = None):
        """
        初始化录入器

        Args:
            stock_query: 股票查询器实例，如果为 None 则创建新实例
        """
        self.stock_query = stock_query or StockDataQuery()

    def parse_chat_text(self, text: str) -> PredictionRecord:
        """
        解析聊天文本，提取预测记录

        这是一个简化实现，实际应该使用 LLM 来解析复杂的聊天文本。

        Args:
            text: 聊天文本

        Returns:
            预测记录

        Raises:
            IngestError: 解析失败时抛出
        """
        # TODO: 使用 LLM 解析聊天文本
        # 当前返回一个示例实现
        raise IngestError("parse_chat_text 需要 LLM 支持，当前未实现")

    def import_from_csv(self, file_path: str) -> List[PredictionRecord]:
        """
        从 CSV 文件导入预测记录

        CSV 格式应包含以下列：
        - date: 日期
        - time: 盘后/盘前（post_market 或 pre_market）
        - model: 模型名称
        - prompt: 提问文本
        - prediction_id: 唯一标识
        - predicted_stocks: 推荐标的
        - limit_up_result: 实际涨停结果（可选）
        - is_sealed: 是否封板（可选）
        - is_touched: 是否触板（可选）

        Args:
            file_path: CSV 文件路径

        Returns:
            预测记录列表

        Raises:
            IngestError: 导入失败时抛出
        """
        try:
            records = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # 转换布尔值
                    is_sealed = None
                    if 'is_sealed' in row and row['is_sealed']:
                        is_sealed = row['is_sealed'].lower() in ('true', '1', 'yes')

                    is_touched = None
                    if 'is_touched' in row and row['is_touched']:
                        is_touched = row['is_touched'].lower() in ('true', '1', 'yes')

                    # 创建预测记录
                    record = PredictionRecord(
                        date=row['date'],
                        time=row['time'],
                        model=row.get('model', 'Miromind'),
                        prompt=row['prompt'],
                        prediction_id=row['prediction_id'],
                        predicted_stocks=row['predicted_stocks'],
                        limit_up_result=row.get('limit_up_result'),
                        is_sealed=is_sealed,
                        is_touched=is_touched,
                        raw_cot=row.get('raw_cot'),
                        cited_source_titles=row.get('cited_source_titles', '').split('|') if row.get('cited_source_titles') else [],
                        source_quality=row.get('source_quality')
                    )
                    records.append(record)

            return records

        except FileNotFoundError:
            raise IngestError(f"文件不存在: {file_path}")
        except KeyError as e:
            raise IngestError(f"CSV 缺少必需列: {e}")
        except Exception as e:
            raise IngestError(f"导入 CSV 失败: {str(e)}")

    def enrich_with_stock_data(self, record: PredictionRecord) -> EnrichedPrediction:
        """
        使用 AKShare 补全量价字段

        Args:
            record: 预测记录

        Returns:
            增强后的预测记录

        Raises:
            IngestError: 补全失败时抛出
        """
        try:
            # 解析股票代码（从 predicted_stocks 文本中提取）
            stock_codes = self._extract_stock_codes(record.predicted_stocks)

            if not stock_codes:
                # 没有找到股票代码，返回未增强的记录
                return EnrichedPrediction(
                    prediction=record,
                    enriched_stocks=[],
                    cot_analysis=None
                )

            # 批量查询股票数据
            try:
                stock_data_map = self.stock_query.batch_query(stock_codes, record.date)
            except StockQueryError as e:
                print(f"警告: 查询股票数据失败: {e}", file=sys.stderr)
                stock_data_map = {}

            # 构建增强股票列表
            enriched_stocks = []
            for code in stock_codes:
                if code in stock_data_map:
                    data = stock_data_map[code]
                    enriched_stock = EnrichedStock(
                        code=code,
                        name=data.get('name', ''),
                        board_count=data.get('board_count', 1),
                        prev_close=data.get('close', 0),
                        limit_up_price=data.get('close', 0) * 1.1,  # 简化计算
                        next_day_open=None,  # 需要次日数据
                        next_day_high=None,
                        premium_rate=None,
                        sector=None,
                        volume=data.get('volume'),
                        turnover_rate=data.get('turnover_rate'),
                        seal_amount=None
                    )
                    enriched_stocks.append(enriched_stock)

            return EnrichedPrediction(
                prediction=record,
                enriched_stocks=enriched_stocks,
                cot_analysis=None
            )

        except Exception as e:
            raise IngestError(f"补全股票数据失败: {str(e)}")

    def _extract_stock_codes(self, text: str) -> List[str]:
        """
        从文本中提取股票代码

        简化实现：假设股票代码是 6 位数字

        Args:
            text: 包含股票代码的文本

        Returns:
            股票代码列表
        """
        import re
        # 匹配 6 位数字（A 股代码格式）
        pattern = r'\b\d{6}\b'
        codes = re.findall(pattern, text)
        return list(set(codes))  # 去重

    def save_prediction(self, prediction: EnrichedPrediction, output_dir: str) -> str:
        """
        保存预测记录为 JSON 文件

        Args:
            prediction: 增强后的预测记录
            output_dir: 输出目录

        Returns:
            保存的文件路径

        Raises:
            IngestError: 保存失败时抛出
        """
        try:
            # 创建输出目录
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            # 生成文件名
            filename = f"{prediction.prediction.prediction_id}.json"
            file_path = output_path / filename

            # 保存为 JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(prediction.model_dump(), f, ensure_ascii=False, indent=2)

            return str(file_path)

        except Exception as e:
            raise IngestError(f"保存预测记录失败: {str(e)}")

    def import_and_enrich(self, csv_path: str, output_dir: str) -> List[str]:
        """
        从 CSV 导入并自动补全，保存为 JSON

        Args:
            csv_path: CSV 文件路径
            output_dir: 输出目录

        Returns:
            保存的文件路径列表

        Raises:
            IngestError: 处理失败时抛出
        """
        # 导入 CSV
        records = self.import_from_csv(csv_path)

        # 逐条补全并保存
        saved_files = []
        for record in records:
            try:
                enriched = self.enrich_with_stock_data(record)
                file_path = self.save_prediction(enriched, output_dir)
                saved_files.append(file_path)
                print(f"已保存: {file_path}")
            except Exception as e:
                print(f"警告: 处理记录 {record.prediction_id} 失败: {e}", file=sys.stderr)

        return saved_files
