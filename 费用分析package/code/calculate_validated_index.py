#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
方案B：双重验证规则
只统计同时满足：(1)包含费用类型关键词 AND (2)包含费用/成本/支出相关词汇 的标注
"""

import json
import os

DATA_DIR = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\费用分析package\data"

# 费用类型关键词
EXPENSE_KEYWORDS = {
    '技术成本': ['technology', 'tech', 'digital', 'it ', 'it,', 'software', 'cloud', 'ai', 'data', 'cybersecurity',
                'infrastructure', 'platform', 'system', 'automation', '技术', '科技', '数字化', '信息化', '系统', '平台', 'ai'],
    '运营费用': ['operating', 'operations', 'operational', 'facilities', '运营', '经营', '营业'],
    '门店成本': ['store', 'retail', 'shop', 'outlet', 'storefront', 'rent', 'lease', 'real estate',
               '门店', '店铺', '租金', '店面', '商业地产', '专柜'],
    '营销费用': ['marketing', 'advertising', 'promotion', 'campaign', 'brand building', '营销', '市场推广', '广告', '推广', '宣传', '促销'],
    '研发费用': ['research', 'development', 'r&d', 'innovation', '研发', '研究开发', '创新'],
    '人力成本': ['employee', 'compensation', 'salary', 'wage', 'personnel', 'headcount', 'workforce', 'labor',
               '人力', '员工', '工资', '薪酬', '福利', '人力费用', '人员'],
    '数字营销': ['digital marketing', 'e-commerce', 'ecommerce', 'social media', 'online', 'digital',
               '数字营销', '电商', '线上', '直播', '社交媒体'],
    '物流成本': ['logistics', 'shipping', 'fulfillment', 'delivery', 'warehouse', 'supply chain',
               '物流', '仓储', '配送', '运输', '供应链', '履约'],
    'SG&A费用': ['selling', 'general', 'administrative', 'g&a', 'sga', 'distribution',
               '分销', '一般及行政', '管理费用']
}

# 费用/成本/支出/投入相关词汇（必须同时包含这些词之一，才算有效费用讨论）
COST_KEYWORDS = [
    'cost', 'costs', 'costing', 'expense', 'expenses', 'expensive', 'spending', 'expenditure',
    'fee', 'fees', 'charge', 'charges', 'budget', 'allocation', 'funded', 'funding',
    '投入', '投资', '支出', '花费', '耗费', '消耗', '费用', '开支', '成本', '价款', '付费',
    '加大', '加强', '强化', '深化', '建设', '配置', '增加', '增长', '提高', '扩充', '扩展'
]

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

def is_valid_expense_annotation(text, expense_type):
    """双重验证：检查段落是否真正在讨论该费用类型"""
    text_lower = text.lower()

    # 条件1：包含该费用类型的关键词
    expense_kws = EXPENSE_KEYWORDS.get(expense_type, [])
    has_expense_keyword = any(kw.lower() in text_lower for kw in expense_kws)

    # 条件2：包含费用/成本/支出相关词汇
    has_cost_keyword = any(kw.lower() in text_lower for kw in COST_KEYWORDS)

    return has_expense_keyword and has_cost_keyword

def get_validated_count(data, expense_type):
    """获取通过双重验证的有效标注数"""
    count = 0
    for para in data.get('annotated_paragraphs', []):
        annotations = para.get('annotations', {})
        if expense_type in annotations.get('expense_types', []):
            text = para.get('original_text', '')
            if is_valid_expense_annotation(text, expense_type):
                count += 1
    return count

def get_total_paragraphs(data):
    return data.get('total_paragraphs', len(data.get('annotated_paragraphs', [])))

def get_expense_para_count(data):
    """统计含费用标注的段落数"""
    count = 0
    for para in data.get('annotated_paragraphs', []):
        annotations = para.get('annotations', {})
        if len(annotations.get('expense_types', [])) > 0:
            count += 1
    return count

def calculate_validated_index():
    """计算通过双重验证的指数"""
    target_brands = ['Nike', '安踏', '361度', 'Lululemon', '李宁', '滔搏']
    expense_order = ['技术成本', '运营费用', '门店成本', '营销费用', '研发费用', '人力成本', '数字营销', '物流成本', 'SG&A费用']

    print("\n" + "=" * 120)
    print("【费用类型指数 - 双重验证版】")
    print("【验证规则】：(1)包含费用类型关键词 AND (2)包含费用/成本/支出词汇")
    print("=" * 120)

    results = {}
    for brand in target_brands:
        filename = BRANDS.get(brand)
        if not filename:
            continue
        try:
            data = load_brand_data(filename)
            total = get_total_paragraphs(data)
            expense_para = get_expense_para_count(data)

            brand_result = {'total': total, 'expense_para': expense_para, 'expenses': {}}

            for expense in expense_order:
                raw_count = data.get('annotation_summary', {}).get('expense_types', {}).get(expense, 0)
                validated_count = get_validated_count(data, expense)
                validated_index_v1 = round((validated_count / total) * 100, 1) if total > 0 else 0
                validated_index_v2 = round((validated_count / expense_para) * 100, 1) if expense_para > 0 else 0

                brand_result['expenses'][expense] = {
                    'raw': raw_count,
                    'validated': validated_count,
                    'index_v1': validated_index_v1,
                    'index_v2': validated_index_v2
                }

            results[brand] = brand_result
        except Exception as e:
            print(f"Error loading {brand}: {e}")

    # v1: 信息渗透度（双重验证后）
    print("\n【v1：信息渗透度 - 双重验证】（以标注段落总数为分母，每100段落提及次数）")
    print(f"\n{'费用类型':<12}", end="")
    for brand in target_brands:
        print(f"{brand:>10}", end="")
    print()
    print("-" * 90)

    for expense in expense_order:
        print(f"{expense:<12}", end="")
        for brand in target_brands:
            val = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('index_v1', '-')
            print(f"{val:>10}", end="")
        print()

    # v2: 费用讨论密度（双重验证后）
    print("\n【v2：费用讨论密度 - 双重验证】（以含费用标注的段落数为分母，每100段落提及次数）")
    print(f"\n{'费用类型':<12}", end="")
    for brand in target_brands:
        print(f"{brand:>10}", end="")
    print()
    print("-" * 90)

    for expense in expense_order:
        print(f"{expense:<12}", end="")
        for brand in target_brands:
            val = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('index_v2', '-')
            print(f"{val:>10}", end="")
        print()

    # 原始 vs 双重验证对比
    print("\n" + "=" * 120)
    print("【原始标注 vs 双重验证后有效标注 对比】")
    print("=" * 120)

    print(f"\n{'费用类型':<12}", end="")
    for brand in target_brands:
        print(f"{brand:>14}", end="")
    print()
    print("-" * 120)
    for expense in expense_order:
        print(f"{expense:<12}", end="")
        for brand in target_brands:
            raw = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('raw', 0)
            validated = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('validated', 0)
            print(f"{raw:>5}/{validated:>5}", end="")
        print()

    # 可复制格式
    print("\n" + "=" * 120)
    print("【可复制格式 - 双重验证 v1：信息渗透度】")
    print("=" * 120)
    print(f"\n费用类型\t" + "\t".join(target_brands))
    for expense in expense_order:
        print(f"{expense}", end="\t")
        for brand in target_brands:
            val = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('index_v1', '-')
            print(f"{val}", end="\t")
        print()

    print("\n" + "=" * 120)
    print("【可复制格式 - 双重验证 v2：费用讨论密度】")
    print("=" * 120)
    print(f"\n费用类型\t" + "\t".join(target_brands))
    for expense in expense_order:
        print(f"{expense}", end="\t")
        for brand in target_brands:
            val = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('index_v2', '-')
            print(f"{val}", end="\t")
        print()

if __name__ == '__main__':
    calculate_validated_index()
