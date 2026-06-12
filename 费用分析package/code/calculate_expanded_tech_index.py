#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
方案B修正版：重新定义"技术成本"为更广泛的"技术投入/创新支出"
扩大认定范围：不仅限成本/费用，还包括技术研发、创新、数字化的投入相关表述
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

# 重新定义：技术投入/创新支出相关词汇
# 只要包含以下任一组合（技术词 + 投入相关词），即视为技术投入讨论
TECH_KEYWORDS = [
    'technology', 'tech', 'digital', 'it ', 'it,', 'software', 'cloud', 'ai', 'artificial intelligence',
    'data', 'cybersecurity', 'infrastructure', 'platform', 'system', 'automation',
    '技术', '科技', '数字化', '信息化', 'it', '系统', '平台', 'ai', '人工智能', '数字'
]

INVESTMENT_KEYWORDS = [
    'investment', 'invest', 'spending', 'expense', 'cost', 'spending', 'expenditure', 'budget', 'allocation', 'funding',
    '投入', '投资', '支出', '费用', '开支', '预算', '分配', '资金', '投入', '耗费', '成本',
    '研发', 'research', 'development', 'r&d', 'innovation', 'innovate', '创新', '研发'
]

# 费用关键词（原始定义，保留用于其他费用类型）
COST_KEYWORDS = {
    'expense', 'cost', 'spending', 'expenditure', 'fee', 'charge',
    '成本', '费用', '支出', '开支', '花费', '投入', '耗费'
}

# 扩展后的技术投入认定：段落需同时包含 TECH_KEYWORDS + (COST_KEYWORDS 或 INVESTMENT_KEYWORDS)
def is_tech_investment(text):
    """判断段落是否讨论技术投入/创新支出"""
    text_lower = text.lower()

    has_tech = any(tech in text_lower for tech in TECH_KEYWORDS)
    has_investment = any(inv in text_lower for inv in INVESTMENT_KEYWORDS)
    has_cost = any(cost in text_lower for cost in COST_KEYWORDS)

    return has_tech and (has_investment or has_cost)

def is_expense_mention_valid(text, expense_type):
    """判断某费用类型标注是否有效"""
    text_lower = text.lower()

    if expense_type == '技术成本':
        return is_tech_investment(text)

    # 其他费用类型保持原有逻辑
    expense_keywords = {
        '运营费用': ['operating', 'operations', 'operational', '运营', '经营'],
        '门店成本': ['store', 'retail', 'shop', 'outlet', 'storefront', '门店', '店铺', '零售', '专柜'],
        '营销费用': ['marketing', 'advertising', 'promotion', 'campaign', '营销', '广告', '推广', '宣传', '促销'],
        '研发费用': ['research', 'development', 'r&d', '研发', '研究开发', '创新'],
        '人力成本': ['employee', 'compensation', 'salary', 'wage', 'personnel', 'headcount', '人力', '员工', '工资', '薪酬', '福利'],
        '数字营销': ['digital', 'online', 'ecommerce', 'e-commerce', 'social media', '数字', '电商', '线上', '直播'],
        '物流成本': ['logistics', 'shipping', 'fulfillment', 'delivery', 'warehouse', '物流', '仓储', '配送', '运输', '供应链'],
        'SG&A费用': ['selling', 'general', 'administrative', 'g&a', 'sga', '分销', '一般及行政', '管理费用']
    }

    confirm_kws = expense_keywords.get(expense_type, [])
    has_expense_type = any(kw.lower() in text_lower for kw in confirm_kws)
    has_cost_keyword = any(kw.lower() in text_lower for kw in COST_KEYWORDS)

    return has_expense_type and has_cost_keyword

def load_brand_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

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

def calculate_expanded_index():
    """计算扩展定义后的指数"""
    target_brands = ['Nike', '安踏', '361度', 'Lululemon', '李宁', '滔搏']
    expense_order = ['技术成本', '运营费用', '门店成本', '营销费用', '研发费用', '人力成本', '数字营销', '物流成本', 'SG&A费用']

    print("\n" + "=" * 120)
    print("【费用类型指数 - 扩展定义版】")
    print("【技术成本重新定义为：技术投入/创新支出】（技术词 + 投入/研发/成本相关词）")
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
                filtered_count = get_filtered_expense_count(data, expense)
                filtered_index = round((filtered_count / total) * 100, 1) if total > 0 else 0
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

    # v1: 信息渗透度
    print("\n【v1：信息渗透度 - 扩展定义】（以标注段落总数为分母，每100段落提及次数）")
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

    # v2: 费用讨论密度
    print("\n【v2：费用讨论密度 - 扩展定义】（以含费用标注的段落数为分母，每100段落提及次数）")
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

    # 原始 vs 过滤对比
    print("\n" + "=" * 120)
    print("【原始标注 vs 扩展定义后有效标注 对比】")
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
            filtered = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('filtered', 0)
            print(f"{raw:>5}/{filtered:>5}", end="")
        print()

    # 可复制格式
    print("\n" + "=" * 120)
    print("【可复制格式 - 扩展定义 v1：信息渗透度】")
    print("=" * 120)
    print(f"\n费用类型\t" + "\t".join(target_brands))
    for expense in expense_order:
        print(f"{expense}", end="\t")
        for brand in target_brands:
            val = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('index_v1', '-')
            print(f"{val}", end="\t")
        print()

    print("\n" + "=" * 120)
    print("【可复制格式 - 扩展定义 v2：费用讨论密度】")
    print("=" * 120)
    print(f"\n费用类型\t" + "\t".join(target_brands))
    for expense in expense_order:
        print(f"{expense}", end="\t")
        for brand in target_brands:
            val = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('index_v2', '-')
            print(f"{val}", end="\t")
        print()

if __name__ == '__main__':
    calculate_expanded_index()
