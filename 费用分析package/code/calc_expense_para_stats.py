#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""计算各品牌费用相关段落数的统计"""
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
}

def load_brand_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_expense_para_count(data):
    """统计含费用标注的段落数"""
    count = 0
    for para in data.get('annotated_paragraphs', []):
        annotations = para.get('annotations', {})
        if len(annotations.get('expense_types', [])) > 0:
            count += 1
    return count

def get_total_paragraphs(data):
    return data.get('total_paragraphs', len(data.get('annotated_paragraphs', [])))

def main():
    results = {}
    for brand, filename in BRANDS.items():
        try:
            data = load_brand_data(filename)
            total = get_total_paragraphs(data)
            expense_para = get_expense_para_count(data)
            results[brand] = {
                'total': total,
                'expense_para': expense_para,
                'expense_ratio': round(expense_para / total * 100, 1) if total > 0 else 0
            }
        except Exception as e:
            print(f"Error loading {brand}: {e}")

    # 计算统计值
    expense_paras = [v['expense_para'] for v in results.values()]
    total_paras = [v['total'] for v in results.values()]
    ratios = [v['expense_ratio'] for v in results.values()]

    print("\n" + "=" * 80)
    print("【各品牌费用相关段落数统计】")
    print("=" * 80)

    print(f"\n{'品牌':<12} {'总段落数':>8} {'费用段落数':>10} {'费用段落占比':>12}")
    print("-" * 50)
    for brand in ['Nike', 'Adidas', '安踏', '361度', 'PUMA', 'On', 'UA', 'Asics', 'CG', 'Amer', 'VF', '滔搏', '捷安特', 'Lululemon']:
        if brand in results:
            v = results[brand]
            print(f"{brand:<12} {v['total']:>8} {v['expense_para']:>10} {v['expense_ratio']:>10.1f}%")

    print("-" * 50)
    print(f"\n【费用段落数统计】")
    print(f"  Range: {min(expense_paras)} - {max(expense_paras)}")
    print(f"  平均值: {sum(expense_paras)/len(expense_paras):.1f}")
    sorted_vals = sorted(expense_paras)
    n = len(sorted_vals)
    if n % 2 == 0:
        median = (sorted_vals[n//2-1] + sorted_vals[n//2]) / 2
    else:
        median = sorted_vals[n//2]
    print(f"  中位数: {median:.1f}")

    print(f"\n【总段落数统计】")
    print(f"  Range: {min(total_paras)} - {max(total_paras)}")
    print(f"  平均值: {sum(total_paras)/len(total_paras):.1f}")
    sorted_total = sorted(total_paras)
    n = len(sorted_total)
    if n % 2 == 0:
        median_total = (sorted_total[n//2-1] + sorted_total[n//2]) / 2
    else:
        median_total = sorted_total[n//2]
    print(f"  中位数: {median_total:.1f}")

    print(f"\n【费用段落占比统计】")
    print(f"  Range: {min(ratios):.1f}% - {max(ratios):.1f}%")
    print(f"  平均值: {sum(ratios)/len(ratios):.1f}%")
    sorted_ratios = sorted(ratios)
    n = len(sorted_ratios)
    if n % 2 == 0:
        median_ratio = (sorted_ratios[n//2-1] + sorted_ratios[n//2]) / 2
    else:
        median_ratio = sorted_ratios[n//2]
    print(f"  中位数: {median_ratio:.1f}%")

    print("\n【可复制格式】")
    print(f"费用段落数 - Range: {min(expense_paras)}-{max(expense_paras)}, 平均: {sum(expense_paras)/len(expense_paras):.1f}, 中位数: {median:.1f}")
    print(f"总段落数 - Range: {min(total_paras)}-{max(total_paras)}, 平均: {sum(total_paras)/len(total_paras):.1f}, 中位数: {median_total:.1f}")
    print(f"费用段落占比 - Range: {min(ratios):.1f}%-{max(ratios):.1f}%, 平均: {sum(ratios)/len(ratios):.1f}%, 中位数: {median_ratio:.1f}%")

if __name__ == '__main__':
    main()
