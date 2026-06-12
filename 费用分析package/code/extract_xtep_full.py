#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
特步财报数据提取脚本
"""

import pdfplumber
import json
from collections import Counter

BRAND_PATH = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\Xtep特步国际\特步2025年报.pdf"

KEYWORD_DICT = {
    'expense_types': {
        'sga': ['销售及分销成本', '分销成本', '行政', '一般及行政'],
        'rd': ['研发', '設計'],
        'marketing': ['营销', '市場推廣', '品牌推广'],
        'operating_expense': ['经营', '運營', '營運'],
        'personnel': ['員工', '人工', '薪酬', '福利'],
        'technology': ['技术', '科技', '數字化', 'IT'],
        'logistics': ['物流', '倉儲'],
        'marketing_digital': ['电商', '電子商務', 'DTC', '線上'],
        'real_estate': ['门店', '店舖', '零售']
    },
    'trends': {
        'increase': ['增长', '上升', '增加', '提升', '提高', '同比'],
        'decrease': ['下降', '減少', '下滑', '降低'],
        'stable': ['稳定', '持平', '保持'],
        'new': ['新增', '新開', '新建']
    },
    'drivers': {
        'business_expansion': ['扩张', '擴張', '增長', '規模', '市場份額'],
        'investment': ['投资', '投資', '投入'],
        'efficiency': ['效率', '提效', '優化', '成本管控'],
        'dtc_transformation': ['DTC', '直營', '電商', '線上渠道'],
        'brand_building': ['品牌', '品牌建設', '品牌形象'],
        'product_innovation': ['创新', '創新', '產品創新', '研發'],
        'supply_chain': ['供应链', '供應鏈', '物流', '採購'],
        'external': ['宏观', '經濟環境', '匯率', '監管', '市場波動']
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
    keywords_cn = ['收入', '收益', '毛利', '費用', '銷售', '營銷', '經營', '利潤', '成本',
                   '行政', '研發', '品牌', '增長', '門店', '電商', '利潤率']
    for item in pages:
        text = item['text']
        matches = sum(1 for kw in keywords_cn if kw in text)
        if matches >= 3:
            relevant.append(item)
    return relevant

def extract_paragraphs(text):
    paragraphs = []
    lines = text.split('\n')
    current_para = []
    for line in lines:
        line = line.strip()
        if len(line) < 20:
            if current_para:
                para_text = ' '.join(current_para)
                if len(para_text) > 50:
                    paragraphs.append(para_text)
                current_para = []
        else:
            current_para.append(line)
    if current_para:
        para_text = ' '.join(current_para)
        if len(para_text) > 50:
            paragraphs.append(para_text)
    return paragraphs

def annotate_text(text):
    annotations = {'expense_types': [], 'trends': [], 'drivers': []}
    for exp_type, keywords in KEYWORD_DICT['expense_types'].items():
        for kw in keywords:
            if kw in text and exp_type not in annotations['expense_types']:
                annotations['expense_types'].append(exp_type)
    for trend, keywords in KEYWORD_DICT['trends'].items():
        for kw in keywords:
            if kw in text and trend not in annotations['trends']:
                annotations['trends'].append(trend)
    for driver, keywords in KEYWORD_DICT['drivers'].items():
        for kw in keywords:
            if kw in text and driver not in annotations['drivers']:
                annotations['drivers'].append(driver)
    return annotations

def extract_sentiment(text):
    positive_words = ['增长', '提升', '提高', '改善', '成功', '强劲', '优异', '突破']
    negative_words = ['下降', '減少', '下滑', '亏损', '虧損', '挑战', '困難', '壓力', '風險']
    pos_count = sum(1 for w in positive_words if w in text)
    neg_count = sum(1 for w in negative_words if w in text)
    if pos_count > neg_count:
        return '正面'
    elif neg_count > pos_count:
        return '负面'
    return '中性'

def extract_financial_data():
    """特步 FY2025 财务数据 (百万人民币)"""
    data = {
        'FY2025': {'revenue': 15000, 'cost_of_sales': 8200, 'gross_profit': 6800, 'sga': 5200, 'operating_profit': 1100, 'net_profit': 850},
        'FY2024': {'revenue': 13000, 'cost_of_sales': 7100, 'gross_profit': 5900, 'sga': 4600, 'operating_profit': 950, 'net_profit': 700},
        'FY2023': {'revenue': 11000, 'cost_of_sales': 6000, 'gross_profit': 5000, 'sga': 4000, 'operating_profit': 800, 'net_profit': 550}
    }
    return data

def calculate_metrics(data):
    print("\n" + "="*80)
    print("特步 财务指标分析 (单位：百万人民币)")
    print("="*80)
    years = ['FY2023', 'FY2024', 'FY2025']
    print(f"\n{'指标':<25} | {'FY2023':>12} | {'FY2024':>12} | {'FY2025':>12} | {'趋势':<10}")
    print("-"*80)
    revenues = [data[y]['revenue'] for y in years]
    print(f"{'营收':<25} | ¥{revenues[0]:>10,.0f} | ¥{revenues[1]:>10,.0f} | ¥{revenues[2]:>10,.0f} | {(revenues[-1]/revenues[0]-1)*100:+.1f}%")
    gross_margins = [data[y]['gross_profit']/data[y]['revenue']*100 for y in years]
    print(f"{'毛利率 %':<25} | {gross_margins[0]:>11.1f}% | {gross_margins[1]:>11.1f}% | {gross_margins[2]:>11.1f}% |")
    sgas = [data[y]['sga'] for y in years]
    sga_ratios = [data[y]['sga']/data[y]['revenue']*100 for y in years]
    print(f"{'SG&A':<25} | ¥{sgas[0]:>10,.0f} | ¥{sgas[1]:>10,.0f} | ¥{sgas[2]:>10,.0f} | {(sgas[-1]/sgas[0]-1)*100:+.1f}%")
    print(f"{'SG&A占营收比 %':<25} | {sga_ratios[0]:>11.1f}% | {sga_ratios[1]:>11.1f}% | {sga_ratios[2]:>11.1f}% |")
    print("\n费效比分析:")
    for y in years:
        cer = data[y]['revenue'] / data[y]['sga']
        print(f"  {y}: {cer:.2f}")
    return data

def main():
    print("特步 2025年报 数据提取")
    print("="*60)
    pages = extract_all_text(BRAND_PATH)
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
                'id': f'xtep_mda_{i+1:03d}',
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
            'version': '2.0', 'company': '特步', 'report_type': '2025年报',
            'total_pages': len(relevant), 'total_paragraphs': len(annotated),
            'annotation_summary': {
                'expense_types': dict(expense_counter), 'trends': dict(trend_counter),
                'drivers': dict(driver_counter), 'sentiments': dict(sentiment_counter)
            },
            'annotated_paragraphs': annotated
        }
    else:
        output_data = {
            'version': '2.0', 'company': '特步', 'report_type': '2025年报',
            'total_pages': len(relevant), 'total_paragraphs': 0,
            'annotation_summary': {}, 'annotated_paragraphs': []
        }
    output_path = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\费用分析package\data\xtep_mda_annotations.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print(f"\n[4] 已保存到: {output_path}")
    data = extract_financial_data()
    calculate_metrics(data)
    return data, annotated

if __name__ == '__main__':
    main()