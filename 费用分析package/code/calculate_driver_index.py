#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
驱动因素指数 - 修正字段名
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
}

def load_brand_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_driver_count(data, driver_type):
    count = 0
    for para in data.get('annotated_paragraphs', []):
        annotations = para.get('annotations', {})
        # 修正：使用 'drivers' 而不是 'driver_factors'
        if driver_type in annotations.get('drivers', []):
            count += 1
    return count

def get_total_paragraphs(data):
    return data.get('total_paragraphs', len(data.get('annotated_paragraphs', [])))

def get_driver_para_count(data):
    count = 0
    for para in data.get('annotated_paragraphs', []):
        annotations = para.get('annotations', {})
        if len(annotations.get('drivers', [])) > 0:
            count += 1
    return count

def calculate_driver_index():
    target_brands = ['Nike', 'Adidas', '安踏', '361度', 'PUMA', 'On', 'UA', 'Asics', 'CG', 'Amer', 'VF', '滔搏', '捷安特']
    driver_order = ['外部因素', '投资驱动', '业务扩张', 'DTC转型', '品牌建设', '产品创新', '效率提升', '供应链']

    print("\n" + "=" * 120)
    print("【驱动因素指数】")
    print("=" * 120)

    results = {}
    for brand in target_brands:
        filename = BRANDS.get(brand)
        if not filename:
            continue
        try:
            data = load_brand_data(filename)
            total = get_total_paragraphs(data)
            driver_para = get_driver_para_count(data)

            brand_result = {'total': total, 'driver_para': driver_para, 'drivers': {}}

            for driver in driver_order:
                # 修正：从 summary 的 'drivers' 而不是 'driver_factors'
                raw_count = data.get('annotation_summary', {}).get('drivers', {}).get(driver, 0)
                validated_count = get_driver_count(data, driver)
                index_v1 = round((validated_count / total) * 100, 1) if total > 0 else 0
                index_v2 = round((validated_count / driver_para) * 100, 1) if driver_para > 0 else 0

                brand_result['drivers'][driver] = {
                    'raw': raw_count,
                    'validated': validated_count,
                    'index_v1': index_v1,
                    'index_v2': index_v2
                }

            results[brand] = brand_result
        except Exception as e:
            print(f"Error loading {brand}: {e}")

    # v1: 信息渗透度
    print("\n【v1：信息渗透度】（以标注段落总数为分母，每100段落提及次数）")
    print(f"\n{'驱动因素':<12}", end="")
    for brand in target_brands:
        print(f"{brand:>8}", end="")
    print()
    print("-" * 120)

    for driver in driver_order:
        print(f"{driver:<12}", end="")
        for brand in target_brands:
            val = results.get(brand, {}).get('drivers', {}).get(driver, {}).get('index_v1', '-')
            print(f"{val:>8}", end="")
        print()

    # v2: 驱动因素讨论密度
    print("\n【v2：驱动因素讨论密度】（以含驱动因素标注的段落数为分母，每100段落提及次数）")
    print(f"\n{'驱动因素':<12}", end="")
    for brand in target_brands:
        print(f"{brand:>8}", end="")
    print()
    print("-" * 120)

    for driver in driver_order:
        print(f"{driver:<12}", end="")
        for brand in target_brands:
            val = results.get(brand, {}).get('drivers', {}).get(driver, {}).get('index_v2', '-')
            print(f"{val:>8}", end="")
        print()

    # 原始 vs 验证对比
    print("\n" + "=" * 120)
    print("【原始标注 vs 验证后 (原始/验证后)】")
    print("=" * 120)

    print(f"\n{'驱动因素':<12}", end="")
    for brand in target_brands:
        print(f"{brand:>12}", end="")
    print()
    print("-" * 120)
    for driver in driver_order:
        print(f"{driver:<12}", end="")
        for brand in target_brands:
            raw = results.get(brand, {}).get('drivers', {}).get(driver, {}).get('raw', 0)
            validated = results.get(brand, {}).get('drivers', {}).get(driver, {}).get('validated', 0)
            print(f"{raw:>5}/{validated:>5}", end="")
        print()

    # 可复制格式
    print("\n" + "=" * 120)
    print("【可复制格式 v1：信息渗透度】")
    print("=" * 120)
    print(f"\n驱动因素\t" + "\t".join(target_brands))
    for driver in driver_order:
        print(f"{driver}", end="\t")
        for brand in target_brands:
            val = results.get(brand, {}).get('drivers', {}).get(driver, {}).get('index_v1', '-')
            print(f"{val}", end="\t")
        print()

    print("\n" + "=" * 120)
    print("【可复制格式 v2：驱动因素讨论密度】")
    print("=" * 120)
    print(f"\n驱动因素\t" + "\t".join(target_brands))
    for driver in driver_order:
        print(f"{driver}", end="\t")
        for brand in target_brands:
            val = results.get(brand, {}).get('drivers', {}).get(driver, {}).get('index_v2', '-')
            print(f"{val}", end="\t")
        print()

if __name__ == '__main__':
    calculate_driver_index()
