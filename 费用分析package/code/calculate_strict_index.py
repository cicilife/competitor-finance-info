#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schema v3.1修正版：使用更严格的关键词进行后验过滤
只统计同时满足：(1)包含费用类型严格关键词 AND (2)包含费用/成本/支出词汇 的标注
"""

import json
import os

DATA_DIR = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\费用分析package\data"

# 更严格的费用类型关键词（修正后schema）
EXPENSE_KEYWORDS = {
    '技术成本': ['technology cost', 'tech cost', 'it cost', 'technology expense', 'it expense',
                '技术成本', '技术费用', 'IT成本', 'IT费用', '技术投入', '数字化投入', '技术服务费'],
    '运营费用': ['operating expense', 'operations expense', 'operational cost', 'operating cost',
                '运营费用', '经营费用', '运营成本', '经营成本', '营业费用'],
    '门店成本': ['store cost', 'store expense', 'store rent', 'lease expense', 'retail rent',
                '门店成本', '店铺租金', '店面费用', '零售租金', '租赁费用', '专柜费用'],
    '营销费用': ['marketing expense', 'advertising expense', 'promotion expense', 'marketing cost',
                'advertising cost', 'marketing spending', 'brand investment', 'brand expense',
                '营销费用', '广告费用', '宣传费用', '推广费用', '促销费用', '市场推广费用', '品牌投入', '品牌费用'],
    '研发费用': ['R&D', 'R&D expense', 'R&D spending', 'research and development', 'research expense',
                '研发费用', '研发支出', '研究开发费用', '技术创新投入', '研发投入'],
    '人力成本': ['employee cost', 'compensation expense', 'personnel cost', 'labor cost', 'headcount cost',
                '人力成本', '员工成本', '人员费用', '人力费用', '工资费用', '薪酬费用', '员工福利费用'],
    '数字营销': ['digital marketing expense', 'e-commerce expense', 'online marketing expense', 'DTC expense',
                '数字营销费用', '电商费用', '在线营销费用', '直播费用', '社交媒体费用', '数字推广费用'],
    '物流成本': ['logistics cost', 'fulfillment cost', 'shipping cost', 'warehousing cost', 'distribution cost',
                '物流成本', '仓储成本', '配送成本', '运输成本', '供应链成本', '履约成本'],
    'SG&A费用': ['selling expense', 'general expense', 'administrative expense', 'SGA', 'G&A expense',
                '分销费用', '一般及行政费用', '管理费用', '销售及管理费用']
}

# 费用/成本/支出相关词汇
COST_KEYWORDS = [
    'cost', 'costs', 'expense', 'expenses', 'spending', 'expenditure',
    'budget', 'allocation', 'funded', 'funding', '投入', '投资', '支出', '费用', '开支', '成本', '耗费', '花费', '消耗',
    '加大', '加强', '强化', '深化', '建设', '增加', '增长', '提高', '扩充', '扩展', '配置'
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
    """严格验证：检查段落是否真正在讨论该费用类型"""
    text_lower = text.lower()

    # 条件1：包含该费用类型的严格关键词
    expense_kws = EXPENSE_KEYWORDS.get(expense_type, [])
    has_expense_keyword = any(kw.lower() in text_lower for kw in expense_kws)

    # 条件2：包含费用/成本/支出相关词汇
    has_cost_keyword = any(kw.lower() in text_lower for kw in COST_KEYWORDS)

    return has_expense_keyword and has_cost_keyword

def get_validated_count(data, expense_type):
    """获取通过严格验证的有效标注数"""
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

def calculate_strict_index():
    """计算通过严格验证的指数"""
    target_brands = ['Nike', 'Adidas', '安踏', '361度', 'PUMA', 'On', 'UA', 'Asics', 'CG', 'Amer', 'VF', '滔搏', '捷安特', 'Lululemon']
    expense_order = ['技术成本', '运营费用', '门店成本', '营销费用', '研发费用', '人力成本', '数字营销', '物流成本', 'SG&A费用']

    print("\n" + "=" * 120)
    print("【费用类型指数 - 严格验证版 (Schema v3.1)】")
    print("【验证规则】：(1)包含费用类型严格关键词 AND (2)包含费用/成本/支出词汇")
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

    # v1: 信息渗透度
    print("\n【v1：信息渗透度 - 严格验证】（以标注段落总数为分母，每100段落提及次数）")
    print(f"\n{'费用类型':<12}", end="")
    for brand in target_brands:
        print(f"{brand:>10}", end="")
    print()
    print("-" * 120)

    for expense in expense_order:
        print(f"{expense:<12}", end="")
        for brand in target_brands:
            val = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('index_v1', '-')
            print(f"{val:>10}", end="")
        print()

    # v2: 费用讨论密度
    print("\n【v2：费用讨论密度 - 严格验证】（以含费用标注的段落数为分母，每100段落提及次数）")
    print(f"\n{'费用类型':<12}", end="")
    for brand in target_brands:
        print(f"{brand:>10}", end="")
    print()
    print("-" * 120)

    for expense in expense_order:
        print(f"{expense:<12}", end="")
        for brand in target_brands:
            val = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('index_v2', '-')
            print(f"{val:>10}", end="")
        print()

    # 原始 vs 严格验证对比
    print("\n" + "=" * 120)
    print("【原始标注 vs 严格验证后有效标注 对比 (原始/验证后)】")
    print("=" * 120)

    print(f"\n{'费用类型':<12}", end="")
    for brand in target_brands:
        print(f"{brand:>14}", end="")
    print()
    print("-" * 160)
    for expense in expense_order:
        print(f"{expense:<12}", end="")
        for brand in target_brands:
            raw = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('raw', 0)
            validated = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('validated', 0)
            print(f"{raw:>5}/{validated:>5}", end="")
        print()

    # 可复制格式
    print("\n" + "=" * 120)
    print("【可复制格式 - 严格验证 v1：信息渗透度】")
    print("=" * 120)
    print(f"\n费用类型\t" + "\t".join(target_brands))
    for expense in expense_order:
        print(f"{expense}", end="\t")
        for brand in target_brands:
            val = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('index_v1', '-')
            print(f"{val}", end="\t")
        print()

    print("\n" + "=" * 120)
    print("【可复制格式 - 严格验证 v2：费用讨论密度】")
    print("=" * 120)
    print(f"\n费用类型\t" + "\t".join(target_brands))
    for expense in expense_order:
        print(f"{expense}", end="\t")
        for brand in target_brands:
            val = results.get(brand, {}).get('expenses', {}).get(expense, {}).get('index_v2', '-')
            print(f"{val}", end="\t")
        print()

if __name__ == '__main__':
    calculate_strict_index()
