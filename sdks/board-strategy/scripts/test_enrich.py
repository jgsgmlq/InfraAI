#!/usr/bin/env python3
"""批量数据增强测试"""

import sys
import json
from pathlib import Path
import time

sdk_root = Path(__file__).parent.parent
sys.path.insert(0, str(sdk_root))

from api.data_model import PredictionRecord
from api.ingest import DataIngestor
from api.stock_query import StockDataQuery

def test_enrich_data(input_dir, output_dir, limit=5):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    stock_query = StockDataQuery(cache_enabled=True, cache_ttl=3600)
    ingestor = DataIngestor(stock_query=stock_query)

    files = sorted(input_path.glob('*.json'))[:limit]

    print(f"开始测试数据增强功能")
    print(f"处理文件数: {len(files)}")
    print("-" * 60)

    success_count = 0
    fail_count = 0

    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] {file_path.name}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                record = PredictionRecord(**data)

            print(f"  日期: {record.date}, 时间: {record.time}")

            try:
                enriched = ingestor.enrich_with_stock_data(record)
                
                output_file = output_path / file_path.name
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(enriched.model_dump(), f, ensure_ascii=False, indent=2)

                print(f"  OK: {len(enriched.enriched_stocks)} stocks")
                success_count += 1

            except Exception as e:
                print(f"  FAIL: {e}")
                fail_count += 1

            time.sleep(0.5)

        except Exception as e:
            print(f"  ERROR: {e}")
            fail_count += 1

    print(f"\n成功: {success_count}, 失败: {fail_count}")
    return success_count, fail_count

if __name__ == "__main__":
    input_dir = sys.argv[1] if len(sys.argv) > 1 else "data/predictions"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/enriched"
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    test_enrich_data(input_dir, output_dir, limit)
