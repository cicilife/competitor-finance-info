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

EXPENSE_KEYWORDS = ['费用', '成本', '支出', '开', '营销', '研发', '人力', '门店', '运营', '广告', '物流', '数字化', '技术']

def load_brand_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def count_expense_paragraphs(data):
    """统计费用相关段落数"""
    count = 0
    for para in data.get('annotated_paragraphs', []):
        text = para.get('original_text', '')
        # 检查是否包含费用关键词
        if any(kw in text for kw in EXPENSE_KEYWORDS):
            count += 1
    return count

def get_total_paragraphs(data):
    return data.get('total_paragraphs', len(data.get('annotated_paragraphs', [])))

def calculate_both_index(data):
    """计算两种指数"""
    summary = data.get('annotation_summary', {})
    expense_types = summary.get('expense_types', {})
    total = get_total_paragraphs(data)
    expense_count = count_expense_paragraphs(data)

    if total == 0:
        total = 1
    if expense_count == 0:
        expense_count = 1

    result = {}
    for expense, freq in expense_types.items():
        result[expense] = {
            'freq': freq,
            'index_total': round((freq / total) * 100, 1),  # 以总段落为分母
            'index_expense': round((freq / expense_count) * 100, 1)  # 以费用段落为分母
        }

    return result, total, expense_count

def print_expense_table():
    """打印费用类型指数表"""
    brand_order = ['Nike', 'Adidas', '安踏', '361度', 'PUMA', 'On', 'UA', 'Asics', 'CG', 'Amer']
    expense_order = ['技术成本', '运营费用', '门店成本', '营销费用', '研发费用', '人力成本', '数字营销', '物流成本', 'SG&A费用']

    # 1. 以总段落为分母（信息渗透度）
    print("\n" + "=" * 140)
    print("【费用类型指数 v1：信息渗透度】（以财报总段落数为分母，每100段落提及次数）")
    print("=" * 140)
    print(f"\n{'费用类型':<10}" + "".join([f"{b:>10}" for b in brand_order]) + f"{'总段落':>8}")
    print("-" * 140)

    totals = {}
    for expense in expense_order:
        row = f"{expense:<10}"
        for brand in brand_order:
            try:
                data = load_brand_data(BRANDS[brand])
                result, total, _ = calculate_both_index(data)
                val = result.get(expense, {}).get('index_total', '-')
                totals[brand] = total
                row += f"{val:>10}"
            except:
                row += f"{'-':>10}"
        row += f"{totals.get(brand, '-'):>8}"
        print(row)

    # 打印总段落数
    print(f"\n{'总段落数':<10}" + "".join([f"{totals.get(b, '-'):>10}" for b in brand_order]))

    # 2. 以费用相关段落为分母（费用讨论密度）
    print("\n" + "=" * 140)
    print("【费用类型指数 v2：费用讨论密度】（以费用相关段落数为分母，每100段落提及次数）")
    print("=" * 140)

    expense_counts = {}
    for brand in brand_order:
        try:
            data = load_brand_data(BRANDS[brand])
            _, _, expense_count = calculate_both_index(data)
            expense_counts[brand] = expense_count
        except:
            expense_counts[brand] = '-'

    print(f"\n{'费用类型':<10}" + "".join([f"{b:>10}" for b in brand_order]) + f"{'费用段落':>8}")
    print("-" * 140)

    for expense in expense_order:
        row = f"{expense:<10}"
        for brand in brand_order:
            try:
                data = load_brand_data(BRANDS[brand])
                result, _, _ = calculate_both_index(data)
                val = result.get(expense, {}).get('index_expense', '-')
                row += f"{val:>10}"
            except:
                row += f"{'-':>10}"
        row += f"{expense_counts.get(brand, '-'):>8}"
        print(row)

    print(f"\n{'费用段落数':<10}" + "".join([f"{expense_counts.get(b, '-'):>10}" for b in brand_order]))

    # 可复制格式
    print("\n" + "=" * 140)
    print("【可复制格式 - 费用类型指数 v1：信息渗透度】")
    print("=" * 140)
    print(f"\n费用类型\t" + "\t".join(brand_order) + "\t总段落")
    for expense in expense_order:
        print(f"{expense}", end="\t")
        for brand in brand_order:
            try:
                data = load_brand_data(BRANDS[brand])
                result, _, _ = calculate_both_index(data)
                val = result.get(expense, {}).get('index_total', '-')
                print(f"{val}", end="\t")
            except:
                print(f"-", end="\t")
        print(f"{totals.get(brand, '-'):}")

    print("\n" + "=" * 140)
    print("【可复制格式 - 费用类型指数 v2：费用讨论密度】")
    print("=" * 140)
    print(f"\n费用类型\t" + "\t".join(brand_order) + "\t费用段落")
    for expense in expense_order:
        print(f"{expense}", end="\t")
        for brand in brand_order:
            try:
                data = load_brand_data(BRANDS[brand])
                result, _, _ = calculate_both_index(data)
                val = result.get(expense, {}).get('index_expense', '-')
                print(f"{val}", end="\t")
            except:
                print(f"-", end="\t")
        print(f"{expense_counts.get(brand, '-')}")

def print_driver_table():
    """打印驱动因素指数表"""
    brand_order = ['Nike', 'Adidas', '安踏', '361度', 'PUMA', 'CG', 'Amer', 'VF', '滔搏', '捷安特']
    driver_order = ['外部因素', '投资驱动', '业务扩张', 'DTC转型', '品牌建设', '产品创新', '效率提升', '供应链']

    def get_driver_index(data, driver):
        summary = data.get('annotation_summary', {})
        return summary.get('drivers', {}).get(driver, 0)

    def count_expense_paragraphs_driver(data):
        count = 0
        for para in data.get('annotated_paragraphs', []):
            text = para.get('original_text', '')
            if any(kw in text for kw in EXPENSE_KEYWORDS):
                count += 1
        return count if count > 0 else 1

    # 1. 以总段落为分母（信息渗透度）
    print("\n" + "=" * 140)
    print("【驱动因素指数 v1：信息渗透度】（以财报总段落数为分母，每100段落提及次数）")
    print("=" * 140)

    totals = {}
    for brand in brand_order:
        try:
            data = load_brand_data(BRANDS[brand])
            totals[brand] = get_total_paragraphs(data)
        except:
            totals[brand] = '-'

    print(f"\n{'驱动因素':<10}" + "".join([f"{b:>10}" for b in brand_order]) + f"{'总段落':>8}")
    print("-" * 140)

    for driver in driver_order:
        row = f"{driver:<10}"
        for brand in brand_order:
            try:
                data = load_brand_data(BRANDS[brand])
                total = totals.get(brand, 1)
                if total == '-':
                    total = 1
                freq = get_driver_index(data, driver)
                val = round((freq / total) * 100, 1)
                row += f"{val:>10}"
            except:
                row += f"{'-':>10}"
        row += f"{totals.get(brand, '-'):>8}"
        print(row)

    # 2. 以费用相关段落为分母（费用讨论密度）
    print("\n" + "=" * 140)
    print("【驱动因素指数 v2：费用讨论密度】（以费用相关段落数为分母，每100段落提及次数）")
    print("=" * 140)

    expense_counts = {}
    for brand in brand_order:
        try:
            data = load_brand_data(BRANDS[brand])
            expense_counts[brand] = count_expense_paragraphs_driver(data)
        except:
            expense_counts[brand] = '-'

    print(f"\n{'驱动因素':<10}" + "".join([f"{b:>10}" for b in brand_order]) + f"{'费用段落':>8}")
    print("-" * 140)

    for driver in driver_order:
        row = f"{driver:<10}"
        for brand in brand_order:
            try:
                data = load_brand_data(BRANDS[brand])
                expense_count = expense_counts.get(brand, 1)
                if expense_count == '-':
                    expense_count = 1
                freq = get_driver_index(data, driver)
                val = round((freq / expense_count) * 100, 1)
                row += f"{val:>10}"
            except:
                row += f"{'-':>10}"
        row += f"{expense_counts.get(brand, '-'):>8}"
        print(row)

    # 可复制格式
    print("\n" + "=" * 140)
    print("【可复制格式 - 驱动因素指数 v1：信息渗透度】")
    print("=" * 140)
    print(f"\n驱动因素\t" + "\t".join(brand_order) + "\t总段落")
    for driver in driver_order:
        print(f"{driver}", end="\t")
        for brand in brand_order:
            try:
                data = load_brand_data(BRANDS[brand])
                total = totals.get(brand, 1)
                if total == '-':
                    total = 1
                freq = get_driver_index(data, driver)
                val = round((freq / total) * 100, 1)
                print(f"{val}", end="\t")
            except:
                print(f"-", end="\t")
        print(f"{totals.get(brand, '-')}")

    print("\n" + "=" * 140)
    print("【可复制格式 - 驱动因素指数 v2：费用讨论密度】")
    print("=" * 140)
    print(f"\n驱动因素\t" + "\t".join(brand_order) + "\t费用段落")
    for driver in driver_order:
        print(f"{driver}", end="\t")
        for brand in brand_order:
            try:
                data = load_brand_data(BRANDS[brand])
                expense_count = expense_counts.get(brand, 1)
                if expense_count == '-':
                    expense_count = 1
                freq = get_driver_index(data, driver)
                val = round((freq / expense_count) * 100, 1)
                print(f"{val}", end="\t")
            except:
                print(f"-", end="\t")
        print(f"{expense_counts.get(brand, '-')}")

if __name__ == '__main__':
    print_expense_table()
    print_driver_table()
