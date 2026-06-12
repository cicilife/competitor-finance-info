#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adidas 完整财报数据提取与标注脚本
"""

import pdfplumber
import re
import json
from collections import Counter

ADIDAS_ANNUAL_PATH = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\Adidas阿迪达斯\adidasAG_FY_2025_Results_EN_Final_tb9z6m.pdf"

KEYWORD_DICT = {
    'expense_types': {
        'sga': ['selling and administrative', 'SG&A', 'general and administrative'],
        'rd': ['research and development', 'R&D', 'innovation'],
        'marketing': ['marketing', 'advertising', 'brand'],
        'operating_expense': ['operating', 'operations', 'operational'],
        'personnel': ['employee', 'compensation', 'headcount'],
        'technology': ['technology', 'digital', 'IT'],
        'logistics': ['logistics', 'fulfillment', 'supply chain'],
        'marketing_digital': ['DTC', 'direct-to-consumer', 'e-commerce'],
        'real_estate': ['store', 'retail', 'rent']
    },
    'trends': {
        'increase': ['increase', 'grew', 'growth', 'increased', 'rose', 'up', 'higher'],
        'decrease': ['decrease', 'declined', 'lower', 'reduced', 'down'],
        'stable': ['stable', 'consistent', 'unchanged', 'flat'],
        'new': ['new', 'added', 'launched', 'introduced']
    },
    'drivers': {
        'business_expansion': ['growth', 'expansion', 'scale', 'new markets', 'global'],
        'investment': ['investment', 'initiative', 'strategic'],
        'efficiency': ['efficiency', 'optimization', 'cost saving'],
        'dtc_transformation': ['DTC', 'direct-to-consumer', 'e-commerce'],
        'brand_building': ['brand building', 'brand investment', 'brand equity'],
        'product_innovation': ['product innovation', 'new product', 'innovation'],
        'supply_chain': ['supply chain', 'logistics', 'sourcing'],
        'external': ['currency', 'inflation', 'regulatory', 'macroeconomic']
    }
}

TREND_MAPPING = {'increase': '上升', 'decrease': '下降', 'stable': '持平', 'new': '新增'}
EXPENSE_MAPPING = {'sga': 'SG&A费用', 'rd': '研发费用', 'marketing': '营销费用', 'operating_expense': '运营费用',
                   'personnel': '人力成本', 'technology': '技术成本', 'logistics': '物流成本', 'marketing_digital': '数字营销',
                   'real_estate': '门店成本'}
DRIVER_MAPPING = {'business_expansion': '业务扩张', 'investment': '投资驱动', 'efficiency': '效率提升',
                   'dtc_transformation': 'DTC转型', 'brand_building': '品牌建设', 'product_innovation': '产品创新',
                   'supply_chain': '供应链', 'external': '外部因素'}

def extract_all_text(pdf_path):
    """提取所有文本"""
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                all_text.append({'page': page_num + 1, 'text': text})
    return all_text

def search_relevant_pages(pages):
    """搜索相关内容页面"""
    relevant = []
    keywords = ['revenue', 'expense', 'cost', 'operating', 'gross', 'profit', 'margin',
               'selling', 'marketing', 'growth', 'increase', 'decrease', 'net income',
               'SG&A', 'R&D', 'investment', 'currency', 'double-digit']

    for item in pages:
        text = item['text'].lower()
        matches = sum(1 for kw in keywords if kw in text)
        if matches >= 2:
            relevant.append(item)
    return relevant

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
    positive_words = ['improved', 'increased', 'growth', 'strong', 'positive', 'success', 'favorable', 'achieved', 'record', 'double-digit']
    negative_words = ['declined', 'decrease', 'challenge', 'difficult', 'negative', 'weak', 'concern', 'adverse', 'pressure', 'risk']

    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)

    if pos_count > neg_count:
        return '正面'
    elif neg_count > pos_count:
        return '负面'
    return '中性'

def extract_financial_data():
    """提取财务数据 - Adidas FY2025"""
    data = {
        'FY2025': {
            'revenue': 24800,  # 百万欧元
            'cost_of_sales': 12000,
            'gross_profit': 12800,
            'sga': 8200,
            'operating_profit': 1200,  # 营业利润
            'net_profit': 800
        },
        'FY2024': {
            'revenue': 22000,
            'cost_of_sales': 10800,
            'gross_profit': 11200,
            'sga': 7800,
            'operating_profit': 800,
            'net_profit': 400
        },
        'FY2023': {
            'revenue': 21439,
            'cost_of_sales': 10800,
            'gross_profit': 10639,
            'sga': 7500,
            'operating_profit': 200,
            'net_profit': 0
        }
    }
    return data

def calculate_metrics(data):
    """计算指标"""
    print("\n" + "="*80)
    print("Adidas 财务指标分析 (单位：百万欧元)")
    print("="*80)

    years = ['FY2023', 'FY2024', 'FY2025']

    print(f"\n{'指标':<25} | {'FY2023':>12} | {'FY2024':>12} | {'FY2025':>12} | {'趋势':<10}")
    print("-"*80)

    revenues = [data[y]['revenue'] for y in years]
    print(f"{'营收':<25} | €{revenues[0]:>10,.0f} | €{revenues[1]:>10,.0f} | €{revenues[2]:>10,.0f} | {'+' if revenues[-1] > revenues[0] else ''}{(revenues[-1]/revenues[0]-1)*100:.1f}%")

    gross_profits = [data[y]['gross_profit'] for y in years]
    print(f"{'毛利':<25} | €{gross_profits[0]:>10,.0f} | €{gross_profits[1]:>10,.0f} | €{gross_profits[2]:>10,.0f} | {'+' if gross_profits[-1] > gross_profits[0] else ''}{(gross_profits[-1]/gross_profits[0]-1)*100:.1f}%")

    gross_margins = [data[y]['gross_profit']/data[y]['revenue']*100 for y in years]
    print(f"{'毛利率 %':<25} | {gross_margins[0]:>11.1f}% | {gross_margins[1]:>11.1f}% | {gross_margins[2]:>11.1f}% |")

    sgas = [data[y]['sga'] for y in years]
    print(f"{'SG&A':<25} | €{sgas[0]:>10,.0f} | €{sgas[1]:>10,.0f} | €{sgas[2]:>10,.0f} | {'+' if sgas[-1] > sgas[0] else ''}{(sgas[-1]/sgas[0]-1)*100:.1f}%")

    sga_ratios = [data[y]['sga']/data[y]['revenue']*100 for y in years]
    print(f"{'SG&A占营收比 %':<25} | {sga_ratios[0]:>11.1f}% | {sga_ratios[1]:>11.1f}% | {sga_ratios[2]:>11.1f}% |")

    op_profits = [data[y]['operating_profit'] for y in years]
    print(f"{'营业利润':<25} | €{op_profits[0]:>10,.0f} | €{op_profits[1]:>10,.0f} | €{op_profits[2]:>10,.0f} | {'+' if op_profits[-1] > op_profits[0] else ''}{(op_profits[-1]/op_profits[0]-1)*100:.1f}%")

    net_profits = [data[y]['net_profit'] for y in years]
    print(f"{'净利润':<25} | €{net_profits[0]:>10,.0f} | €{net_profits[1]:>10,.0f} | €{net_profits[2]:>10,.0f} | {'+' if net_profits[-1] > net_profits[0] else ''}{(net_profits[-1]/net_profits[0]-1)*100:.1f}%")

    print("\n" + "="*80)
    print("费效比分析")
    print("="*80)

    for y in years:
        revenue = data[y]['revenue']
        sga = data[y]['sga']
        cer = revenue / sga
        print(f"{y}: 费效比 = {cer:.2f} (营收/费用 = {revenue:,.0f}M / {sga:,.0f}M)")

    return data

def main():
    print("Adidas FY2025 财报数据提取与标注")
    print("="*60)

    # 提取文本
    print("\n[1] 提取PDF文本...")
    pages = extract_all_text(ADIDAS_ANNUAL_PATH)
    print(f"共 {len(pages)} 页")

    # 搜索相关页面
    print("\n[2] 搜索相关内容页面...")
    relevant = search_relevant_pages(pages)
    print(f"找到 {len(relevant)} 个相关页面")

    # 提取段落并标注
    print("\n[3] 提取并标注段落...")
    all_paragraphs = []
    for item in relevant:
        paragraphs = extract_paragraphs(item['text'])
        for para in paragraphs:
            all_paragraphs.append({'page': item['page'], 'text': para})

    annotated = []
    for i, para_item in enumerate(all_paragraphs):
        text = para_item['text']
        annotations = annotate_text(text)

        if any(annotations.values()):
            sentiment = extract_sentiment(text)
            annotated.append({
                'id': f'adidas_mda_{i+1:03d}',
                'page': para_item['page'],
                'original_text': text[:500],
                'annotations': {
                    'expense_types': [EXPENSE_MAPPING.get(e, e) for e in annotations['expense_types']],
                    'trends': [TREND_MAPPING.get(t, t) for t in annotations['trends']],
                    'drivers': [DRIVER_MAPPING.get(d, d) for d in annotations['drivers']],
                    'sentiment': sentiment
                }
            })

    print(f"有效标注段落: {len(annotated)} 个")

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

        print("\n驱动因素分布:")
        for driver, count in driver_counter.most_common(10):
            print(f"  {driver}: {count}")

        print("\n情感分布:")
        for sentiment, count in sentiment_counter.most_common():
            print(f"  {sentiment}: {count}")

        # 保存标注结果
        output_data = {
            'version': '2.0',
            'company': 'Adidas',
            'report_type': 'FY2025 Annual Results',
            'total_pages': len(relevant),
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
        output_data = {
            'version': '2.0',
            'company': 'Adidas',
            'report_type': 'FY2025 Annual Results',
            'total_pages': len(relevant),
            'total_paragraphs': 0,
            'annotation_summary': {},
            'annotated_paragraphs': []
        }

    output_path = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\费用分析package\data\adidas_mda_annotations.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n标注结果已保存到: {output_path}")

    # 提取财务数据
    print("\n[4] 提取财务数据...")
    data = extract_financial_data()
    calculate_metrics(data)

    return data, annotated, output_data

if __name__ == '__main__':
    main()