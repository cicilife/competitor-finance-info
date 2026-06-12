#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
计算各品牌费用类型和驱动因素的标准化指数（每100段落提及次数）
便于横向纵向比较
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
    """加载品牌数据"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_total_paragraphs(data):
    """获取总段落数"""
    return data.get('total_paragraphs', data.get('annotation_summary', {}).get('total_paragraphs', 1))

def calculate_expense_index(data):
    """计算费用类型指数（每100段落提及次数）"""
    summary = data.get('annotation_summary', {})
    expense_types = summary.get('expense_types', {})
    total = get_total_paragraphs(data)

    if total == 0:
        total = 1

    # 计算每100段落的提及次数
    index = {}
    for expense, count in expense_types.items():
        index[expense] = round((count / total) * 100, 1)

    return index

def calculate_driver_index(data):
    """计算驱动因素指数（每100段落提及次数）"""
    summary = data.get('annotation_summary', {})
    drivers = summary.get('drivers', {})
    total = get_total_paragraphs(data)

    if total == 0:
        total = 1

    # 计算每100段落的提及次数
    index = {}
    for driver, count in drivers.items():
        index[driver] = round((count / total) * 100, 1)

    return index

def print_expense_table():
    """打印费用类型指数表格"""
    print("\n" + "=" * 120)
    print("【费用类型关键词频率指数】（每100段落提及次数，便于横向纵向比较）")
    print("=" * 120)

    # 收集所有费用类型
    all_expenses = set()
    brand_expense_index = {}

    for brand, filename in BRANDS.items():
        try:
            data = load_brand_data(filename)
            index = calculate_expense_index(data)
            brand_expense_index[brand] = index
            all_expenses.update(index.keys())
        except Exception as e:
            print(f"Error loading {brand}: {e}")

    # 按字母顺序排列品牌
    brands_sorted = sorted(brand_expense_index.keys(), key=lambda x: x)

    # 表头
    print(f"\n{'费用类型':<12}", end="")
    for brand in brands_sorted[:10]:  # 只显示前10个品牌
        print(f"{brand:>10}", end="")
    print()
    print("-" * 120)

    # 费用类型
    expense_order = ['技术成本', '运营费用', '门店成本', '营销费用', '研发费用', '人力成本', '数字营销', '物流成本', 'SG&A费用']

    for expense in expense_order:
        print(f"{expense:<12}", end="")
        for brand in brands_sorted[:10]:
            val = brand_expense_index[brand].get(expense, '-')
            print(f"{val:>10}", end="")
        print()

    # 原始词频表格
    print("\n" + "=" * 120)
    print("【费用类型原始词频】")
    print("=" * 120)

    print(f"\n{'费用类型':<12}", end="")
    for brand in brands_sorted[:10]:
        print(f"{brand:>10}", end="")
    print()
    print("-" * 120)

    for expense in expense_order:
        print(f"{expense:<12}", end="")
        for brand in brands_sorted[:10]:
            data = load_brand_data(BRANDS[brand])
            val = data.get('annotation_summary', {}).get('expense_types', {}).get(expense, '-')
            print(f"{val:>10}", end="")
        print()

def print_driver_table():
    """打印驱动因素指数表格"""
    print("\n" + "=" * 120)
    print("【驱动因素关键词频率指数】（每100段落提及次数，便于横向纵向比较）")
    print("=" * 120)

    # 收集所有驱动因素
    all_drivers = set()
    brand_driver_index = {}

    for brand, filename in BRANDS.items():
        try:
            data = load_brand_data(filename)
            index = calculate_driver_index(data)
            brand_driver_index[brand] = index
            all_drivers.update(index.keys())
        except Exception as e:
            print(f"Error loading {brand}: {e}")

    # 按字母顺序排列品牌
    brands_sorted = sorted(brand_driver_index.keys(), key=lambda x: x)

    # 表头
    print(f"\n{'驱动因素':<12}", end="")
    for brand in brands_sorted[:10]:  # 只显示前10个品牌
        print(f"{brand:>10}", end="")
    print()
    print("-" * 120)

    # 驱动因素
    driver_order = ['外部因素', '投资驱动', '业务扩张', 'DTC转型', '品牌建设', '产品创新', '效率提升', '供应链', '人力成本']

    for driver in driver_order:
        print(f"{driver:<12}", end="")
        for brand in brands_sorted[:10]:
            val = brand_driver_index[brand].get(driver, '-')
            print(f"{val:>10}", end="")
        print()

    # 原始词频表格
    print("\n" + "=" * 120)
    print("【驱动因素原始词频】")
    print("=" * 120)

    print(f"\n{'驱动因素':<12}", end="")
    for brand in brands_sorted[:10]:
        print(f"{brand:>10}", end="")
    print()
    print("-" * 120)

    for driver in driver_order:
        print(f"{driver:<12}", end="")
        for brand in brands_sorted[:10]:
            data = load_brand_data(BRANDS[brand])
            val = data.get('annotation_summary', {}).get('drivers', {}).get(driver, '-')
            print(f"{val:>10}", end="")
        print()

def print_copy_format():
    """打印可复制格式"""
    print("\n" + "=" * 120)
    print("【可复制格式 - 费用类型指数】")
    print("=" * 120)

    brand_order = ['Nike', 'Adidas', '安踏', '361度', 'PUMA', 'On', 'UA', 'Asics', 'CG', 'Amer']
    expense_order = ['技术成本', '运营费用', '门店成本', '营销费用', '研发费用', '人力成本', '数字营销', '物流成本', 'SG&A费用']

    print(f"\n费用类型\t" + "\t".join(brand_order))
    for expense in expense_order:
        print(f"{expense}", end="\t")
        for brand in brand_order:
            try:
                data = load_brand_data(BRANDS[brand])
                total = get_total_paragraphs(data)
                count = data.get('annotation_summary', {}).get('expense_types', {}).get(expense, 0)
                index = round((count / total) * 100, 1) if total > 0 else '-'
                print(f"{index}", end="\t")
            except:
                print(f"-", end="\t")
        print()

    print("\n" + "=" * 120)
    print("【可复制格式 - 驱动因素指数】")
    print("=" * 120)

    brand_order = ['Nike', 'Adidas', '安踏', '361度', 'PUMA', 'CG', 'Amer', 'VF', '滔搏', '捷安特']
    driver_order = ['外部因素', '投资驱动', '业务扩张', 'DTC转型', '品牌建设', '产品创新', '效率提升', '供应链']

    print(f"\n驱动因素\t" + "\t".join(brand_order))
    for driver in driver_order:
        print(f"{driver}", end="\t")
        for brand in brand_order:
            try:
                data = load_brand_data(BRANDS[brand])
                total = get_total_paragraphs(data)
                count = data.get('annotation_summary', {}).get('drivers', {}).get(driver, 0)
                index = round((count / total) * 100, 1) if total > 0 else '-'
                print(f"{index}", end="\t")
            except:
                print(f"-", end="\t")
        print()

if __name__ == '__main__':
    print_expense_table()
    print_driver_table()
    print_copy_format()
