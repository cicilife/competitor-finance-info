#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
计算两种标准化指数：
1. 以财报总段落数为分母（信息渗透度）
2. 以费用相关段落数为分母（费用讨论密度）
"""

import json
import os

DATA_DIR = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\费用分析package\data"

BRANDS = {
    'Nike': 'nike_mda_annotations.json',
    'Adidas': 'adidas_mda_annotations.json',
    '安踏': 'anta_mda_annotations.json',
    '361度': '361_mda_annotations.json',
    'PUMA': 'puma_mda_annotations.json',
    'On': 'on_mda_annotations.json',
    'UA': 'ua_mda_annotations.json',
    'Asics': 'asics_mda_annotations.json',
    'CG': 'canada_goose_mda_annotations.json',
    'Amer': 'amer_mda_annotations.json',
    'VF': 'vf_mda_annotations.json',
    '滔搏': 'topsport_mda_annotations.json',
    '捷安特': 'giant_mda_annotations.json',
    'Lululemon': 'lululemon_mda_annotations.json',
    'Skechers': 'skechers_mda_annotations.json',
    'Columbia': 'columbia_mda_annotations.json',
    '特步': 'xtep_mda_annotations.json',
    '比音勒芬': 'biyin_mda_annotations.json',
    '牧高笛': 'mogo_mda_annotations.json',
    '探路者': 'toread_mda_annotations.json',
    '李宁': 'lining_mda_annotations.json',
}

def load_brand_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_annotated_count(data):
    """获取标注段落数（annotated_paragraphs数组长度）"""
    return len(data.get('annotated_paragraphs', []))

def get_expense_para_count(data):
    """统计含有费用类型标注的段落数"""
    count = 0
    for para in data.get('annotated_paragraphs', []):
        annotations = para.get('annotations', {})
        expense_types = annotations.get('expense_types', [])
        if len(expense_types) > 0:
            count += 1
    return count

def get_driver_para_count(data):
    """统计含有驱动因素标注的段落数"""
    count = 0
    for para in data.get('annotated_paragraphs', []):
        annotations = para.get('annotations', {})
        drivers = annotations.get('drivers', [])
        if len(drivers) > 0:
            count += 1
    return count

def print_expense_table():
    """打印费用类型指数表"""
    brand_order = ['Nike', 'Adidas', '安踏', '361度', 'PUMA', 'On', 'UA', 'Asics', 'CG', 'Amer']
    expense_order = ['技术成本', '运营费用', '门店成本', '营销费用', '研发费用', '人力成本', '数字营销', '物流成本', 'SG&A费用']

    # 收集各品牌数据
    brand_data = {}
    for brand in brand_order:
        try:
            data = load_brand_data(BRANDS[brand])
            annotated_count = get_annotated_count(data)
            expense_para_count = get_expense_para_count(data)
            summary = data.get('annotation_summary', {})
            expense_types = summary.get('expense_types', {})

            result = {}
            for expense in expense_order:
                freq = expense_types.get(expense, 0)
                result[expense] = {
                    'freq': freq,
                    'index_total': round((freq / annotated_count) * 100, 1) if annotated_count > 0 else 0,
                    'index_expense': round((freq / expense_para_count) * 100, 1) if expense_para_count > 0 else 0
                }

            brand_data[brand] = {
                'result': result,
                'annotated_count': annotated_count,
                'expense_para_count': expense_para_count
            }
        except Exception as e:
            print(f"Error loading {brand}: {e}")

    # v1: 信息渗透度
    print("\n" + "=" * 150)
    print("【费用类型指数 v1：信息渗透度】（以标注段落总数为分母，每100段落提及次数）")
    print("=" * 150)

    print(f"\n{'费用类型':<10}" + "".join([f"{b:>10}" for b in brand_order]) + f"{'标注段落':>8}")
    print("-" * 150)

    for expense in expense_order:
        row = f"{expense:<10}"
        for brand in brand_order:
            val = brand_data.get(brand, {}).get('result', {}).get(expense, {}).get('index_total', '-')
            row += f"{val:>10}"
        print(row)

    print(f"\n{'标注段落':<10}" + "".join([f"{brand_data.get(b, {}).get('annotated_count', '-'):>10}" for b in brand_order]))

    # v2: 费用讨论密度
    print("\n" + "=" * 150)
    print("【费用类型指数 v2：费用讨论密度】（以含费用标注的段落数为分母，每100段落提及次数）")
    print("=" * 150)

    print(f"\n{'费用类型':<10}" + "".join([f"{b:>10}" for b in brand_order]) + f"{'费用段落':>8}")
    print("-" * 150)

    for expense in expense_order:
        row = f"{expense:<10}"
        for brand in brand_order:
            val = brand_data.get(brand, {}).get('result', {}).get(expense, {}).get('index_expense', '-')
            row += f"{val:>10}"
        print(row)

    print(f"\n{'费用段落':<10}" + "".join([f"{brand_data.get(b, {}).get('expense_para_count', '-'):>10}" for b in brand_order]))

    # 可复制格式
    print("\n" + "=" * 150)
    print("【可复制格式 - 费用类型指数 v1：信息渗透度】")
    print("=" * 150)
    print(f"\n费用类型\t" + "\t".join(brand_order) + "\t标注段落")
    for expense in expense_order:
        print(f"{expense}", end="\t")
        for brand in brand_order:
            val = brand_data.get(brand, {}).get('result', {}).get(expense, {}).get('index_total', '-')
            print(f"{val}", end="\t")
        print(f"{brand_data.get(brand, {}).get('annotated_count', '-')}")

    print("\n" + "=" * 150)
    print("【可复制格式 - 费用类型指数 v2：费用讨论密度】")
    print("=" * 150)
    print(f"\n费用类型\t" + "\t".join(brand_order) + "\t费用段落")
    for expense in expense_order:
        print(f"{expense}", end="\t")
        for brand in brand_order:
            val = brand_data.get(brand, {}).get('result', {}).get(expense, {}).get('index_expense', '-')
            print(f"{val}", end="\t")
        print(f"{brand_data.get(brand, {}).get('expense_para_count', '-')}")

def print_driver_table():
    """打印驱动因素指数表"""
    brand_order = ['Nike', 'Adidas', '安踏', '361度', 'PUMA', 'CG', 'Amer', 'VF', '滔搏', '捷安特']
    driver_order = ['外部因素', '投资驱动', '业务扩张', 'DTC转型', '品牌建设', '产品创新', '效率提升', '供应链']

    # 收集各品牌数据
    brand_data = {}
    for brand in brand_order:
        try:
            data = load_brand_data(BRANDS[brand])
            annotated_count = get_annotated_count(data)
            driver_para_count = get_driver_para_count(data)
            summary = data.get('annotation_summary', {})
            drivers = summary.get('drivers', {})

            result = {}
            for driver in driver_order:
                freq = drivers.get(driver, 0)
                result[driver] = {
                    'freq': freq,
                    'index_total': round((freq / annotated_count) * 100, 1) if annotated_count > 0 else 0,
                    'index_driver': round((freq / driver_para_count) * 100, 1) if driver_para_count > 0 else 0
                }

            brand_data[brand] = {
                'result': result,
                'annotated_count': annotated_count,
                'driver_para_count': driver_para_count
            }
        except Exception as e:
            print(f"Error loading {brand}: {e}")

    # v1: 信息渗透度
    print("\n" + "=" * 150)
    print("【驱动因素指数 v1：信息渗透度】（以标注段落总数为分母，每100段落提及次数）")
    print("=" * 150)

    print(f"\n{'驱动因素':<10}" + "".join([f"{b:>10}" for b in brand_order]) + f"{'标注段落':>8}")
    print("-" * 150)

    for driver in driver_order:
        row = f"{driver:<10}"
        for brand in brand_order:
            val = brand_data.get(brand, {}).get('result', {}).get(driver, {}).get('index_total', '-')
            row += f"{val:>10}"
        print(row)

    print(f"\n{'标注段落':<10}" + "".join([f"{brand_data.get(b, {}).get('annotated_count', '-'):>10}" for b in brand_order]))

    # v2: 驱动因素讨论密度
    print("\n" + "=" * 150)
    print("【驱动因素指数 v2：驱动因素讨论密度】（以含驱动因素标注的段落数为分母，每100段落提及次数）")
    print("=" * 150)

    print(f"\n{'驱动因素':<10}" + "".join([f"{b:>10}" for b in brand_order]) + f"{'驱动段落':>8}")
    print("-" * 150)

    for driver in driver_order:
        row = f"{driver:<10}"
        for brand in brand_order:
            val = brand_data.get(brand, {}).get('result', {}).get(driver, {}).get('index_driver', '-')
            row += f"{val:>10}"
        print(row)

    print(f"\n{'驱动段落':<10}" + "".join([f"{brand_data.get(b, {}).get('driver_para_count', '-'):>10}" for b in brand_order]))

    # 可复制格式
    print("\n" + "=" * 150)
    print("【可复制格式 - 驱动因素指数 v1：信息渗透度】")
    print("=" * 150)
    print(f"\n驱动因素\t" + "\t".join(brand_order) + "\t标注段落")
    for driver in driver_order:
        print(f"{driver}", end="\t")
        for brand in brand_order:
            val = brand_data.get(brand, {}).get('result', {}).get(driver, {}).get('index_total', '-')
            print(f"{val}", end="\t")
        print(f"{brand_data.get(brand, {}).get('annotated_count', '-')}")

    print("\n" + "=" * 150)
    print("【可复制格式 - 驱动因素指数 v2：驱动因素讨论密度】")
    print("=" * 150)
    print(f"\n驱动因素\t" + "\t".join(brand_order) + "\t驱动段落")
    for driver in driver_order:
        print(f"{driver}", end="\t")
        for brand in brand_order:
            val = brand_data.get(brand, {}).get('result', {}).get(driver, {}).get('index_driver', '-')
            print(f"{val}", end="\t")
        print(f"{brand_data.get(brand, {}).get('driver_para_count', '-')}")

if __name__ == '__main__':
    print_expense_table()
    print_driver_table()
