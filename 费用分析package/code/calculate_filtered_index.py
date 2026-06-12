#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
方案B：后验过滤 - 重新计算费用类型指数
只统计段落中明确提及"成本/费用/支出"相关词汇的标注
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

# 费用相关关键词 - 只有包含这些词才视为真正的费用讨论
COST_KEYWORDS = {
    'expense', 'cost', 'spending', 'expenditure', 'fee', 'charge',
    '成本', '费用', '支出', '开支', '花费', '投入', '耗费'
}

# 各费用类型的特征词（与COST_KEYWORDS结合判断）
EXPENSE_CONFIRM_KEYWORDS = {
    '技术成本': ['technology', 'tech', 'it', 'digital', 'software', 'cloud', '技术', 'it', '数字化', '信息化', '系统'],
    '运营费用': ['operating', 'operations', 'operational', '运营', '经营'],
    '门店成本': ['store', 'retail', 'shop', ' outlet', 'storefront', '门店', '店铺', '零售', '专柜'],
    '营销费用': ['marketing', 'advertising', 'promotion', 'campaign', '营销', '广告', '推广', '宣传', '促销'],
    '研发费用': ['research', 'development', 'r&d', '研发', '研究开发', '创新'],
    '人力成本': ['employee', 'compensation', 'salary', 'wage', 'personnel', 'headcount', '人力', '员工', '工资', '薪酬', '福利'],
    '数字营销': ['digital', 'online', 'ecommerce', 'e-commerce', 'social media', '数字', '电商', '线上', '直播'],
    '物流成本': ['logistics', 'shipping', 'fulfillment', 'delivery', 'warehouse', '物流', '仓储', '配送', '运输', '供应链'],
    'SG&A费用': ['selling', 'general', 'administrative', 'g&a', 'sga', '分销', '一般及行政', '管理费用']
}

def load_brand_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def is_cost_related_paragraph(text):
    """判断段落是否真正讨论费用（包含费用关键词）"""
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in COST_KEYWORDS)

def is_expense_mention_valid(text, expense_type):
    """判断某费用类型标注是否有效（段落中既有所属费用词又有费用关键词）"""
    text_lower = text.lower()

    # 检查是否包含该费用类型的特征词
    confirm_kws = EXPENSE_CONFIRM_KEYWORDS.get(expense_type, [])
    has_expense_type = any(kw.lower() in text_lower for kw in confirm_kws)

    # 检查是否包含费用关键词
    has_cost_keyword = any(kw.lower() in text_lower for kw in COST_KEYWORDS)

    # 两个条件都满足才视为有效
    return has_expense_type and has_cost_keyword

def get_filtered_expense_count(data, expense_type):
    """获取过滤后的有效费用标注数"""
    count = 0
    for para in data.get('annotated_paragraphs', []):
        annotations = para.get('annotations', {})
        if expense_type in annotations.get('expense_types', []):
            text = para.get('original_text', '')
            if is_expense_mention_valid(text, expense_type):
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

def calculate_filtered_index():
    """计算过滤后的指数"""
    target_brands = ['Nike', '安踏', '361度', 'Lululemon', '李宁', '滔搏']
    expense_order = ['技术成本', '运营费用', '门店成本', '营销费用', '研发费用', '人力成本', '数字营销', '物流成本', 'SG&A费用']

    print("\n" + "=" * 120)
    print("【费用类型指数 - 后验过滤版】（仅统计明确提及费用的标注）")
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
                # 原始标注数
                raw_count = data.get('annotation_summary', {}).get('expense_types', {}).get(expense, 0)
                # 过滤后有效数
                filtered_count = get_filtered_expense_count(data, expense)
                # 过滤后指数（以总段落为分母）
                filtered_index = round((filtered_count / total) * 100, 1) if total > 0 else 0
                # 过滤后指数v2（以费用段落为分母）
                filtered_index_v2 = round((filtered_count / expense_para) * 100, 1) if expense_para > 0 else 0

                brand_result['expenses'][expense] = {
                    'raw': raw_count,
                    'filtered': filtered_count,
                    'index_v1': filtered_index,
                    'index_v2': filtered_index_v2
                }

            results[brand] = brand_result
        except Exception as e:
            print(f"Error loading {brand}: {e}")

    # 打印v1: 信息渗透度（过滤后）
    print("\n【v1：信息渗透度 - 过滤后】（以标注段落总数为分母，每100段落提及次数）")
    print(f"\n{'费用类型':<10}", end="")
    for brand in target_brands:
        print(f"{brand:>10}", end="")
    print(f"{'过滤率':>10}")
    print("-" * 90)

    for expense in expense_order:
        print(f"{expense:<10}", end="")
        for brand in target_brands:
            val = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('index_v1', '-')
            print(f"{val:>10}", end="")
        # 打印过滤率
        total_raw = sum(results.get(b, {}).get('expenses', {}).get(expense, {}).get('raw', 0) for b in target_brands)
        total_filtered = sum(results.get(b, {}).get('expenses', {}).get(expense, {}).get('filtered', 0) for b in target_brands)
        filter_rate = f"{(1-total_filtered/total_raw)*100:.0f}%" if total_raw > 0 else "-"
        print(f"{filter_rate:>10}")
        print()

    # 打印v2: 费用讨论密度（过滤后）
    print("\n【v2：费用讨论密度 - 过滤后】（以含费用标注的段落数为分母，每100段落提及次数）")
    print(f"\n{'费用类型':<10}", end="")
    for brand in target_brands:
        print(f"{brand:>10}", end="")
    print()
    print("-" * 90)

    for expense in expense_order:
        print(f"{expense:<10}", end="")
        for brand in target_brands:
            val = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('index_v2', '-')
            print(f"{val:>10}", end="")
        print()

    # 打印原始 vs 过滤对比
    print("\n" + "=" * 120)
    print("【原始标注 vs 过滤后有效标注 对比】")
    print("=" * 120)
    print(f"\n{'费用类型':<10}", end="")
    for brand in target_brands:
        print(f"{brand:>16}", end="")
    print()
    print("-" * 120)
    print(f"{'':<10}", end="")
    for brand in target_brands:
        print(f"{'原始/过滤':>16}", end="")
    print()
    print("-" * 120)

    for expense in expense_order:
        print(f"{expense:<10}", end="")
        for brand in target_brands:
            raw = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('raw', 0)
            filtered = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('filtered', 0)
            print(f"{raw:>6}/{filtered:>6}", end="")
        print()

    # 可复制格式
    print("\n" + "=" * 120)
    print("【可复制格式 - 过滤后指数 v1：信息渗透度】")
    print("=" * 120)
    print(f"\n费用类型\t" + "\t".join(target_brands))
    for expense in expense_order:
        print(f"{expense}", end="\t")
        for brand in target_brands:
            val = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('index_v1', '-')
            print(f"{val}", end="\t")
        print()

    print("\n" + "=" * 120)
    print("【可复制格式 - 过滤后指数 v2：费用讨论密度】")
    print("=" * 120)
    print(f"\n费用类型\t" + "\t".join(target_brands))
    for expense in expense_order:
        print(f"{expense}", end="\t")
        for brand in target_brands:
            val = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('index_v2', '-')
            print(f"{val}", end="\t")
        print()

if __name__ == '__main__':
    calculate_filtered_index()
