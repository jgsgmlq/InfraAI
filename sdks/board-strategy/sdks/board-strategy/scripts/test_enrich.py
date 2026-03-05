#!/usr/bin/env python3
"""
批量数据增强测试

测试 P1 阶段的完整功能：
1. 读取转换后的预测记录
2. 使用 AKShare 补全量价数据
3. 保存增强后的数据
"""

import sys
import json
from pathlib import Path
import time

# 添加 SDK 到路径
sdk_root = Path(__file__).parent.parent
sys.path.insert(0, str(sdk_root))

from api.data_model import PredictionRecord, EnrichedPrediction
from api.ingest import DataIngestor
from api.stock_query import StockDataQuery


def test_enrich_data(input_dir, output_dir, limit=5):
    """
    测试数据增强功能

    Args:
        input_dir: 输入目录（转换后的预测记录）
        output_dir: 输出目录（增强后的数据）
        limit: 限制处理的文件数量（避免过多 API 调用）
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 创建查询器和录入器
    stock_query = StockDataQuery(cache_enabled=True, cache_ttl=3600)
    ingestor = DataIngestor(stock_query=stock_query)

    # 获取所有预测记录文件
    files = sorted(input_path.glob('*.json'))[:limit]

    print(f"开始测试数据增强功能")
    print(f"输入目录: {input_path.absolute()}")
    print(f"输出目录: {output_path.absolute()}")
    print(f"处理文件数: {len(files)}")
    print("-" * 60)

    success_count = 0
    fail_count = 0
    results = []

    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] 处理: {file_path.name}")

        try:
            # 读取预测记录
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                record = PredictionRecord(**data)

            print(f"  日期: {record.date}")
            print(f"  时间: {record.time}")
            print(f"  预测: {record.predicted_stocks[:50]}...")

            # 数据增强
            try:
                enriched = ingestor.enrich_with_stock_data(record)

                # 保存增强后的数据
                output_file = output_path / file_path.name
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(enriched.model_dump(), f, ensure_ascii=False, indent=2)

                print(f"  ✓ 增强成功: {len(enriched.enriched_stocks)} 只股票")
                success_count += 1

                results.append({
                    'file': file_path.name,
                    'status': 'success',
                    'stocks_count': len(enriched.enriched_stocks),
                    'prediction_id': record.prediction_id
                })

            except Exception as e:
                print(f"  ✗ 增强失败: {e}")
                fail_count += 1

                results.append({
                    'file': file_path.name,
                    'status': 'failed',
                    'error': str(e),
                    'prediction_id': record.prediction_id
                })

            # 避免 API 限流
            time.sleep(0.5)

        except Exception as e:
            print(f"  ✗ 读取失败: {e}")
            fail_count += 1

    # 输出测试报告
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"总计: {len(files)}")

    # 保存测试结果
    report_file = output_path / "test_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total': len(files),
            'success': success_count,
            'failed': fail_count,
            'results': results
        }, f, ensure_ascii=False, indent=2)

    print(f"\n测试报告已保存: {report_file}")

    return success_count, fail_count


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python test_enrich.py <input_dir> [output_dir] [limit]")
        print("示例: python test_enrich.py data/predictions data/enriched 5")
        sys.exit(2)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/enriched"
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    try:
        test_enrich_data(input_dir, output_dir, limit)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(3)


if __name__ == "__main__":
    main()
