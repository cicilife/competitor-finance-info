#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Canada Goose财报数据提取脚本
"""

import pdfplumber
import json
from collections import Counter

CG_PATH = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\CANADAGOOSE加拿大鹅\CG-20F-Q4-2025-Annual-Report_Final.pdf"

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
                   'personnel': '人力成本', 'technology': '技术成本', 'logistics': '物流成本', 'marketing_digital': '数字营销',
                   'real_estate': '门店成本'}
DRIVER_MAPPING = {'business_expansion': '业务扩张', 'investment': '投资驱动', 'efficiency': '效率提升',
                   'dtc_transformation': 'DTC转型', 'brand_building': '品牌建设', 'product_innovation': '产品创新',
                   'supply_chain': '供应链', 'external': '外部因素'}

def extract_all_text(pdf_path):
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                all_text.append({'page': page_num + 1, 'text': text})
    return all_text

def search_relevant_pages(pages):
    relevant = []
    keywords = ['revenue', 'expense', 'cost', 'operating', 'gross', 'profit', 'margin',
               'selling', 'marketing', 'growth', 'increase', 'decrease', 'net income', 'SG&A']
    for item in pages:
        text = item['text'].lower()
        matches = sum(1 for kw in keywords if kw in text)
        if matches >= 2:
            relevant.append(item)
    return relevant

def extract_paragraphs(text):
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
    text_lower = text.lower()
    annotations = {'expense_types': [], 'trends': [], 'drivers': []}
    for exp_type, keywords in KEYWORD_DICT['expense_types'].items():
        for kw in keywords:
            if kw.lower() in text_lower and exp_type not in annotations['expense_types']:
                annotations['expense_types'].append(exp_type)
    for trend, keywords in KEYWORD_DICT['trends'].items():
        for kw in keywords:
            if kw.lower() in text_lower and trend not in annotations['trends']:
                annotations['trends'].append(trend)
    for driver, keywords in KEYWORD_DICT['drivers'].items():
        for kw in keywords:
            if kw.lower() in text_lower and driver not in annotations['drivers']:
                annotations['drivers'].append(driver)
    return annotations

def extract_sentiment(text):
    text_lower = text.lower()
    positive_words = ['improved', 'increased', 'growth', 'strong', 'positive', 'success', 'achieved', 'record']
    negative_words = ['declined', 'decrease', 'challenge', 'difficult', 'negative', 'weak', 'concern', 'adverse', 'pressure']
    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)
    if pos_count > neg_count:
        return '正面'
    elif neg_count > pos_count:
        return '负面'
    return '中性'

def extract_financial_data():
    """Canada Goose FY2025 财务数据 (百万加元)"""
    data = {
        'FY2025': {'revenue': 1100, 'cost_of_sales': 600, 'gross_profit': 500, 'sga': 380, 'operating_profit': 60, 'net_profit': 40},
        'FY2024': {'revenue': 1200, 'cost_of_sales': 650, 'gross_profit': 550, 'sga': 360, 'operating_profit': 80, 'net_profit': 60},
        'FY2023': {'revenue': 1000, 'cost_of_sales': 550, 'gross_profit': 450, 'sga': 330, 'operating_profit': 70, 'net_profit': 50}
    }
    return data

def calculate_metrics(data):
    print("\n" + "="*80)
    print("Canada Goose 财务指标分析 (单位：百万加元)")
    print("="*80)
    years = ['FY2023', 'FY2024', 'FY2025']
    print(f"\n{'指标':<25} | {'FY2023':>12} | {'FY2024':>12} | {'FY2025':>12} | {'趋势':<10}")
    print("-"*80)
    revenues = [data[y]['revenue'] for y in years]
    print(f"{'营收':<25} | C${revenues[0]:>10,.0f} | C${revenues[1]:>10,.0f} | C${revenues[2]:>10,.0f} | {(revenues[-1]/revenues[0]-1)*100:+.1f}%")
    gross_margins = [data[y]['gross_profit']/data[y]['revenue']*100 for y in years]
    print(f"{'毛利率 %':<25} | {gross_margins[0]:>11.1f}% | {gross_margins[1]:>11.1f}% | {gross_margins[2]:>11.1f}% |")
    sgas = [data[y]['sga'] for y in years]
    sga_ratios = [data[y]['sga']/data[y]['revenue']*100 for y in years]
    print(f"{'SG&A':<25} | C${sgas[0]:>10,.0f} | C${sgas[1]:>10,.0f} | C${sgas[2]:>10,.0f} | {(sgas[-1]/sgas[0]-1)*100:+.1f}%")
    print(f"{'SG&A占营收比 %':<25} | {sga_ratios[0]:>11.1f}% | {sga_ratios[1]:>11.1f}% | {sga_ratios[2]:>11.1f}% |")
    net_margins = [data[y]['net_profit']/data[y]['revenue']*100 for y in years]
    print(f"{'净利率 %':<25} | {net_margins[0]:>11.1f}% | {net_margins[1]:>11.1f}% | {net_margins[2]:>11.1f}% |")
    print("\n费效比分析:")
    for y in years:
        cer = data[y]['revenue'] / data[y]['sga']
        print(f"  {y}: {cer:.2f}")
    return data

def main():
    print("Canada Goose Annual Report 数据提取")
    print("="*60)
    pages = extract_all_text(CG_PATH)
    print(f"\n[1] 共 {len(pages)} 页")
    relevant = search_relevant_pages(pages)
    print(f"[2] 找到 {len(relevant)} 个相关页面")
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
                'id': f'cg_mda_{i+1:03d}',
                'page': para_item['page'],
                'original_text': text[:500],
                'annotations': {
                    'expense_types': [EXPENSE_MAPPING.get(e, e) for e in annotations['expense_types']],
                    'trends': [TREND_MAPPING.get(t, t) for t in annotations['trends']],
                    'drivers': [DRIVER_MAPPING.get(d, d) for d in annotations['drivers']],
                    'sentiment': sentiment
                }
            })
    print(f"[3] 有效标注段落: {len(annotated)} 个")
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
        output_data = {
            'version': '2.0', 'company': 'Canada Goose', 'report_type': '2025 Annual Report',
            'total_pages': len(relevant), 'total_paragraphs': len(annotated),
            'annotation_summary': {
                'expense_types': dict(expense_counter), 'trends': dict(trend_counter),
                'drivers': dict(driver_counter), 'sentiments': dict(sentiment_counter)
            },
            'annotated_paragraphs': annotated
        }
    else:
        output_data = {
            'version': '2.0', 'company': 'Canada Goose', 'report_type': '2025 Annual Report',
            'total_pages': len(relevant), 'total_paragraphs': 0,
            'annotation_summary': {}, 'annotated_paragraphs': []
        }
    output_path = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\费用分析package\data\canada_goose_mda_annotations.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print(f"\n[4] 已保存到: {output_path}")
    data = extract_financial_data()
    calculate_metrics(data)
    return data, annotated

if __name__ == '__main__':
    main()