#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lululemon MD&A文本提取 - 优化版
"""

import pdfplumber
import re
import json
from collections import Counter

LULU_ANNUAL_PATH = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\Lululemon\lululemon-2025-annual-report.pdf"

KEYWORD_DICT = {
    'expense_types': {
        'sga': ['selling and administrative', 'SG&A', 'general and administrative'],
        'rd': ['research and development', 'R&D', 'innovation'],
        'marketing': ['marketing', 'advertising', 'brand'],
        'operating_expense': ['operating', 'operations', 'operational'],
        'personnel': ['employee', 'compensation', 'headcount'],
        'technology': ['technology', 'digital', 'IT'],
        'logistics': ['logistics', 'fulfillment', 'supply chain'],
        'real_estate': ['store', 'retail', 'rent']
    },
    'trends': {
        'increase': ['increase', 'grew', 'growth', 'increased', 'rose', 'up'],
        'decrease': ['decrease', 'declined', 'lower', 'reduced', 'down'],
        'stable': ['stable', 'consistent', 'unchanged', 'flat'],
        'new': ['new', 'added', 'launched', 'introduced']
    },
    'drivers': {
        'business_expansion': ['growth', 'expansion', 'scale', 'new markets'],
        'investment': ['investment', 'initiative', 'strategic'],
        'efficiency': ['efficiency', 'optimization', 'cost saving'],
        'dtc_transformation': ['DTC', 'direct-to-consumer', 'e-commerce'],
        'brand_building': ['brand building', 'brand investment'],
        'product_innovation': ['product innovation', 'new product'],
        'supply_chain': ['supply chain', 'logistics', 'sourcing'],
        'external': ['currency', 'inflation', 'regulatory', 'macroeconomic']
    }
}

TREND_MAPPING = {'increase': '上升', 'decrease': '下降', 'stable': '持平', 'new': '新增'}
EXPENSE_MAPPING = {'sga': 'SG&A费用', 'rd': '研发费用', 'marketing': '营销费用', 'operating_expense': '运营费用',
                   'personnel': '人力成本', 'technology': '技术成本', 'logistics': '物流成本', 'real_estate': '门店成本'}
DRIVER_MAPPING = {'business_expansion': '业务扩张', 'investment': '投资驱动', 'efficiency': '效率提升',
                   'dtc_transformation': 'DTC转型', 'brand_building': '品牌建设', 'product_innovation': '产品创新',
                   'supply_chain': '供应链', 'external': '外部因素'}

def extract_all_text(pdf_path):
    """提取所有文本"""
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append({'page': pdf.pages.index(page) + 1, 'text': text})
    return all_text

def search_relevant_pages(pages):
    """搜索相关内容页面"""
    relevant_pages = []

    for item in pages:
        text = item['text'].lower()
        # 扩大搜索范围
        keywords = ['revenue', 'expense', 'cost', 'operating', 'gross', 'profit', 'margin',
                   'selling', 'marketing', 'investment', 'growth', 'increase', 'decrease',
                   'digital', ' DTC', 'brand', 'product', 'store', 'customer']

        matches = sum(1 for kw in keywords if kw in text)
        if matches >= 3:  # 降低阈值
            relevant_pages.append(item)

    return relevant_pages

def extract_paragraphs(text):
    """提取段落"""
    paragraphs = []
    lines = text.split('\n')
    current_para = []

    for line in lines:
        line = line.strip()
        if len(line) < 30:
            if current_para:
                para_text = ' '.join(current_para)
                if len(para_text) > 80:
                    paragraphs.append(para_text)
                current_para = []
        else:
            current_para.append(line)

    if current_para:
        para_text = ' '.join(current_para)
        if len(para_text) > 80:
            paragraphs.append(para_text)

    return paragraphs

def annotate_text(text):
    """标注文本"""
    text_lower = text.lower()
    annotations = {'expense_types': [], 'trends': [], 'drivers': []}

    for exp_type, keywords in KEYWORD_DICT['expense_types'].items():
        for kw in keywords:
            if kw.lower() in text_lower:
                if exp_type not in annotations['expense_types']:
                    annotations['expense_types'].append(exp_type)

    for trend, keywords in KEYWORD_DICT['trends'].items():
        for kw in keywords:
            if kw.lower() in text_lower:
                if trend not in annotations['trends']:
                    annotations['trends'].append(trend)

    for driver, keywords in KEYWORD_DICT['drivers'].items():
        for kw in keywords:
            if kw.lower() in text_lower:
                if driver not in annotations['drivers']:
                    annotations['drivers'].append(driver)

    return annotations

def extract_sentiment(text):
    """判断情感"""
    text_lower = text.lower()
    positive_words = ['improved', 'increased', 'growth', 'strong', 'positive', 'success', 'favorable']
    negative_words = ['declined', 'decrease', 'challenge', 'difficult', 'negative', 'weak', 'concern', 'adverse', 'pressure']

    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)

    if pos_count > neg_count:
        return '正面'
    elif neg_count > pos_count:
        return '负面'
    return '中性'

def main():
    print("Lululemon MD&A 文本提取 v2")
    print("="*60)

    # 提取所有文本
    print("\n[1] 提取所有文本...")
    pages = extract_all_text(LULU_ANNUAL_PATH)
    print(f"共 {len(pages)} 页")

    # 搜索相关内容页面
    print("\n[2] 搜索相关内容页面...")
    relevant_pages = search_relevant_pages(pages)
    print(f"找到 {len(relevant_pages)} 个相关页面")

    # 提取段落
    print("\n[3] 提取段落...")
    all_paragraphs = []
    for item in relevant_pages:
        paragraphs = extract_paragraphs(item['text'])
        for para in paragraphs:
            all_paragraphs.append({'page': item['page'], 'text': para})

    print(f"提取了 {len(all_paragraphs)} 个段落")

    # 标注
    print("\n[4] 标注段落...")
    annotated = []

    for i, para_item in enumerate(all_paragraphs):
        text = para_item['text']
        annotations = annotate_text(text)

        if any(annotations.values()):
            sentiment = extract_sentiment(text)
            annotated.append({
                'id': f'lulu_mda_{i+1:03d}',
                'page': para_item['page'],
                'original_text': text[:500],
                'annotations': {
                    'expense_types': [EXPENSE_MAPPING.get(e, e) for e in annotations['expense_types']],
                    'trends': [TREND_MAPPING.get(t, t) for t in annotations['trends']],
                    'drivers': [DRIVER_MAPPING.get(d, d) for d in annotations['drivers']],
                    'sentiment': sentiment
                }
            })

    print(f"有效标注: {len(annotated)} 个")

    # 统计
    if annotated:
        expense_counter = Counter()
        trend_counter = Counter()
        driver_counter = Counter()
        sentiment_counter = Counter()

        for para in annotated:
            for exp in para['annotations']['expense_types']:
                expense_counter[exp] += 1
            for trend in para['annotations']['trends']:
                trend_counter[trend] += 1
            for driver in para['annotations']['drivers']:
                driver_counter[driver] += 1
            sentiment_counter[para['annotations']['sentiment']] += 1

        print("\n费用类型分布:")
        for exp, count in expense_counter.most_common(10):
            print(f"  {exp}: {count}")

        print("\n趋势分布:")
        for trend, count in trend_counter.most_common():
            print(f"  {trend}: {count}")

        print("\n驱动因素分布:")
        for driver, count in driver_counter.most_common(10):
            print(f"  {driver}: {count}")

        print("\n情感分布:")
        for sentiment, count in sentiment_counter.most_common():
            print(f"  {sentiment}: {count}")

        # 保存
        output_data = {
            'version': '2.0',
            'company': 'Lululemon',
            'report_type': 'Annual Report FY2025',
            'total_pages': len(relevant_pages),
            'total_paragraphs': len(annotated),
            'annotation_summary': {
                'expense_types': dict(expense_counter),
                'trends': dict(trend_counter),
                'drivers': dict(driver_counter),
                'sentiments': dict(sentiment_counter)
            },
            'annotated_paragraphs': annotated
        }
    else:
        # 即使没有标注也保存空结果
        output_data = {
            'version': '2.0',
            'company': 'Lululemon',
            'report_type': 'Annual Report FY2025',
            'total_pages': len(relevant_pages),
            'total_paragraphs': 0,
            'annotation_summary': {},
            'annotated_paragraphs': []
        }

    output_path = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\费用分析package\data\lululemon_mda_annotations.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n已保存到: {output_path}")

    # 打印示例
    if annotated:
        print("\n示例:")
        for para in annotated[:3]:
            print(f"\n--- {para['id']} ---")
            print(f"原文: {para['original_text'][:150]}...")
            print(f"标注: {para['annotations']}")

    return annotated, output_data

if __name__ == '__main__':
    main()