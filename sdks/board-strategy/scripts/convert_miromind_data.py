#!/usr/bin/env python3
"""
转换 Miromind 原始数据为标准格式

将用户的原始 CSV 数据转换为 board-strategy SDK 的标准格式。
"""

import sys
import csv
import json
from pathlib import Path
from datetime import datetime

# 添加 SDK 到路径
sdk_root = Path(__file__).parent.parent
sys.path.insert(0, str(sdk_root))

from api.data_model import PredictionRecord


def parse_date(date_str):
    """转换日期格式：2026.1.26 -> 2026-01-26"""
    try:
        parts = date_str.split('.')
        year = parts[0]
        month = parts[1].zfill(2)
        day = parts[2].zfill(2)
        return f"{year}-{month}-{day}"
    except:
        return date_str


def parse_time(time_str):
    """转换时间为 post_market 或 pre_market"""
    try:
        hour = int(time_str.split(':')[0])
        if hour < 12:
            return "pre_market"
        else:
            return "post_market"
    except:
        return "post_market"


def parse_bool(value):
    """转换布尔值"""
    if not value or value.strip() == '':
        return None
    return value.strip() == '是'


def convert_csv(input_file, output_dir):
    """
    转换 CSV 文件

    Args:
        input_file: 输入 CSV 文件路径
        output_dir: 输出目录
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    records = []
    current_date = None
    current_time = None
    current_model = None
    current_prompt = None

    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # 处理合并单元格：如果当前行的日期/时间/模型/prompt 为空，使用上一行的值
            if row['日期'].strip():
                current_date = parse_date(row['日期'])
            if row['时间'].strip():
                current_time = parse_time(row['时间'])
            if row['模型'].strip():
                current_model = row['模型']
            if row['prompt'].strip():
                current_prompt = row['prompt']

            # 跳过没有 ID 的行
            if not row['ID'].strip():
                continue

            # 生成 prediction_id
            stock_code = row['ID'].strip()
            prediction_id = f"{current_date}-{current_time}-{stock_code}"

            # 解析涨停结果
            limit_up_result = row['涨停结果'].strip() if row['涨停结果'].strip() else None

            # 创建预测记录
            try:
                record = PredictionRecord(
                    date=current_date,
                    time=current_time,
                    model=current_model,
                    prompt=current_prompt,
                    prediction_id=prediction_id,
                    predicted_stocks=row['预测结果'].strip(),
                    limit_up_result=limit_up_result,
                    is_sealed=parse_bool(row['是否封板']),
                    is_touched=parse_bool(row['是否触板']),
                    raw_cot=None,  # 原始数据中没有 CoT
                    cited_source_titles=[],
                    source_quality=None
                )

                records.append(record)

                # 保存为 JSON
                output_file = output_path / f"{prediction_id}.json"
                with open(output_file, 'w', encoding='utf-8') as out:
                    json.dump(record.model_dump(), out, ensure_ascii=False, indent=2)

                print(f"✓ 已转换: {prediction_id}")

            except Exception as e:
                print(f"✗ 转换失败 {stock_code}: {e}", file=sys.stderr)

    print(f"\n转换完成！共处理 {len(records)} 条记录")
    print(f"输出目录: {output_path.absolute()}")

    return records


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python convert_miromind_data.py <input_csv> [output_dir]")
        print("示例: python convert_miromind_data.py D:\\infra_demo\\project\\data.csv data/predictions")
        sys.exit(2)

    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/predictions"

    if not Path(input_file).exists():
        print(f"错误: 文件不存在: {input_file}", file=sys.stderr)
        sys.exit(3)

    try:
        convert_csv(input_file, output_dir)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
