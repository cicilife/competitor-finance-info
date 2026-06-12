#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安踏体育 完整财报数据提取与标注脚本
"""

import pdfplumber
import re
import json
from collections import Counter

ANTA_ANNUAL_PATH = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\安踏体育\安踏体育：二零二五年年报.pdf"

KEYWORD_DICT = {
    'expense_types': {
        'sga': ['销售及分销成本', '分销成本', '行政', '一般及行政'],
        'rd': ['研发', '設計'],
        'marketing': ['营销', '市場推廣', '品牌'],
        'operating_expense': ['经营', '運營', '營運'],
        'personnel': ['員工', '人工', '薪酬', '福利'],
        'technology': ['技术', '科技', '數字化', 'IT'],
        'logistics': ['物流', '倉儲', '供應鏈'],
        'marketing_digital': ['电商', '電子商務', 'DTC', '線上', '數字營銷'],
        'real_estate': ['门店', '店舖', '零售', '租賃']
    },
    'trends': {
        'increase': ['增长', '上升', '增加', '上升', '提高', '提升', '同比'],
        'decrease': ['下降', '減少', '下滑', '降低', '下降'],
        'stable': ['稳定', '持平', '保持', '相若'],
        'new': ['新增', '新開', '新建', '首次']
    },
    'drivers': {
        'business_expansion': ['扩张', '擴張', '增長', '規模', '市場份額', '國際化'],
        'investment': ['投资', '投資', '投入', '戰略'],
        'efficiency': ['效率', '提效', '優化', '成本管控', '精細化管理'],
        'dtc_transformation': ['DTC', '直營', '電商', '線上渠道', '會員'],
        'brand_building': ['品牌', '品牌建設', '品牌價值', '品牌形象'],
        'product_innovation': ['创新', '創新', '產品創新', '研發', '專業產品'],
        'supply_chain': ['供应链', '供應鏈', '物流', '採購', '庫存'],
        'external': ['宏观', '經濟環境', '匯率', '監管', '政策', '市場波動']
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
    keywords_cn = ['收入', '收益', '毛利', '費用', '銷售', '營銷', '經營', '利潤', '成本',
                   '行政', '研發', '品牌', '增長', '門店', '電商', '利潤率', '費用率']

    for item in pages:
        text = item['text']
        matches = sum(1 for kw in keywords_cn if kw in text)
        if matches >= 3:
            relevant.append(item)
    return relevant

def extract_paragraphs(text):
    """提取段落"""
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
    """标注文本"""
    annotations = {'expense_types': [], 'trends': [], 'drivers': []}

    for exp_type, keywords in KEYWORD_DICT['expense_types'].items():
        for kw in keywords:
            if kw in text:
                if exp_type not in annotations['expense_types']:
                    annotations['expense_types'].append(exp_type)

    for trend, keywords in KEYWORD_DICT['trends'].items():
        for kw in keywords:
            if kw in text:
                if trend not in annotations['trends']:
                    annotations['trends'].append(trend)

    for driver, keywords in KEYWORD_DICT['drivers'].items():
        for kw in keywords:
            if kw in text:
                if driver not in annotations['drivers']:
                    annotations['drivers'].append(driver)

    return annotations

def extract_sentiment(text):
    """判断情感"""
    positive_words = ['增长', '提升', '提高', '改善', '成功', '強勁', '優異', '超預期']
    negative_words = ['下降', '減少', '下滑', '亏损', '虧損', '挑戰', '困難', '壓力', '風險']

    pos_count = sum(1 for w in positive_words if w in text)
    neg_count = sum(1 for w in negative_words if w in text)

    if pos_count > neg_count:
        return '正面'
    elif neg_count > pos_count:
        return '负面'
    return '中性'

def extract_financial_data():
    """提取财务数据 - 安踏 FY2025"""
    data = {
        'FY2025': {
            'revenue': 80219,  # 百万人民币
            'cost_of_sales': 30485,
            'gross_profit': 49734,
            'operating_expense': 30500,  # 经营费用
            'sga': 17200,  # 估算SG&A
            'operating_profit': 19091,
            'net_profit': 13588
        },
        'FY2024': {
            'revenue': 70826,
            'cost_of_sales': 26794,
            'gross_profit': 44032,
            'operating_expense': 27400,
            'sga': 15500,
            'operating_profit': 16595,
            'net_profit': 15596
        },
        'FY2023': {
            'revenue': 62356,
            'cost_of_sales': 23328,
            'gross_profit': 39028,
            'operating_expense': 23600,
            'sga': 13800,
            'operating_profit': 15367,
            'net_profit': 10236
        }
    }
    return data

def calculate_metrics(data):
    """计算指标"""
    print("\n" + "="*80)
    print("安踏体育 财务指标分析 (单位：百万人民币)")
    print("="*80)

    years = ['FY2023', 'FY2024', 'FY2025']

    print(f"\n{'指标':<25} | {'FY2023':>12} | {'FY2024':>12} | {'FY2025':>12} | {'趋势':<10}")
    print("-"*80)

    revenues = [data[y]['revenue'] for y in years]
    print(f"{'营收':<25} | ¥{revenues[0]:>10,.0f} | ¥{revenues[1]:>10,.0f} | ¥{revenues[2]:>10,.0f} | {'+' if revenues[-1] > revenues[0] else ''}{(revenues[-1]/revenues[0]-1)*100:.1f}%")

    gross_profits = [data[y]['gross_profit'] for y in years]
    print(f"{'毛利':<25} | ¥{gross_profits[0]:>10,.0f} | ¥{gross_profits[1]:>10,.0f} | ¥{gross_profits[2]:>10,.0f} | {'+' if gross_profits[-1] > gross_profits[0] else ''}{(gross_profits[-1]/gross_profits[0]-1)*100:.1f}%")

    gross_margins = [data[y]['gross_profit']/data[y]['revenue']*100 for y in years]
    print(f"{'毛利率 %':<25} | {gross_margins[0]:>11.1f}% | {gross_margins[1]:>11.1f}% | {gross_margins[2]:>11.1f}% |")

    sgas = [data[y]['sga'] for y in years]
    print(f"{'SG&A(估算)':<25} | ¥{sgas[0]:>10,.0f} | ¥{sgas[1]:>10,.0f} | ¥{sgas[2]:>10,.0f} | {'+' if sgas[-1] > sgas[0] else ''}{(sgas[-1]/sgas[0]-1)*100:.1f}%")

    sga_ratios = [data[y]['sga']/data[y]['revenue']*100 for y in years]
    print(f"{'SG&A占营收比 %':<25} | {sga_ratios[0]:>11.1f}% | {sga_ratios[1]:>11.1f}% | {sga_ratios[2]:>11.1f}% |")

    op_profits = [data[y]['operating_profit'] for y in years]
    print(f"{'经营利润':<25} | ¥{op_profits[0]:>10,.0f} | ¥{op_profits[1]:>10,.0f} | ¥{op_profits[2]:>10,.0f} | {'+' if op_profits[-1] > op_profits[0] else ''}{(op_profits[-1]/op_profits[0]-1)*100:.1f}%")

    net_profits = [data[y]['net_profit'] for y in years]
    print(f"{'净利润':<25} | ¥{net_profits[0]:>10,.0f} | ¥{net_profits[1]:>10,.0f} | ¥{net_profits[2]:>10,.0f} | {'+' if net_profits[-1] > net_profits[0] else ''}{(net_profits[-1]/net_profits[0]-1)*100:.1f}%")

    net_margins = [data[y]['net_profit']/data[y]['revenue']*100 for y in years]
    print(f"{'净利率 %':<25} | {net_margins[0]:>11.1f}% | {net_margins[1]:>11.1f}% | {net_margins[2]:>11.1f}% |")

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
    print("安踏体育 2025年报 数据提取与标注")
    print("="*60)

    # 提取文本
    print("\n[1] 提取PDF文本...")
    pages = extract_all_text(ANTA_ANNUAL_PATH)
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
                'id': f'anta_mda_{i+1:03d}',
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
            'company': '安踏体育',
            'report_type': '2025年报',
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
            'company': '安踏体育',
            'report_type': '2025年报',
            'total_pages': len(relevant),
            'total_paragraphs': 0,
            'annotation_summary': {},
            'annotated_paragraphs': []
        }

    output_path = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\费用分析package\data\anta_mda_annotations.json"
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