#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nike MD&A文本提取与关键词标注脚本
从Nike 10-K中提取MD&A文本，并按v2 schema进行自动关键词标注
"""

import pdfplumber
import re
import json
from collections import Counter

NIKE_10K_PATH = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\NIKE耐克\Nike-Inc-2025_10K.pdf"

# 关键词词典（来自v2 schema）
KEYWORD_DICT = {
    'expense_types': {
        'sga': ['selling and administrative', 'SG&A', 'general and administrative', 'distribution', 'sales and marketing'],
        'rd': ['research and development', 'R&D', 'innovation', 'product development', 'design and development'],
        'marketing': ['marketing', 'advertising', 'promotion', 'brand', 'customer acquisition', 'demand creation'],
        'operating_expense': ['operating', 'operations', 'operational', 'facilities', 'logistics'],
        'personnel': ['employee', 'compensation', 'headcount', 'personnel', 'workforce', 'salary', 'benefits'],
        'technology': ['technology', 'digital', 'IT', 'cloud', 'software', 'data', 'cybersecurity'],
        'logistics': ['logistics', 'fulfillment', 'shipping', 'warehousing', 'supply chain', 'distribution cost'],
        'marketing_digital': ['digital marketing', 'e-commerce', 'DTC', 'direct-to-consumer', 'online', 'ecommerce'],
        'real_estate': ['store', 'retail', 'rent', 'lease', 'real estate', 'footprint', 'physical'],
        'legal': ['legal', 'compliance', 'regulatory', 'litigation', 'settlement']
    },
    'trends': {
        'increase': ['increase', 'grew', 'growth', 'higher', 'increased', 'rose', 'up', 'higher', 'growth', 'expanded'],
        'decrease': ['decrease', 'declined', 'lower', 'reduced', 'decline', 'fell', 'down', 'improved', 'lower'],
        'stable': ['stable', 'consistent', 'unchanged', 'flat', 'similar', 'maintained', 'remained'],
        'volatile': ['volatile', 'fluctuate', 'fluctuation', 'variable', 'unstable', 'variability'],
        'new': ['new', 'added', 'additional', 'first time', 'newly', 'launched', 'introduced'],
        'reduction': ['reduction', 'cut', 'restructuring', 'streamline', 'optimization', 'right-sizing', 'efficiency']
    },
    'drivers': {
        'business_expansion': ['growth', 'expansion', 'scale', 'volume', 'business growth', 'new markets', 'international', 'global'],
        'investment': ['investment', 'initiative', 'strategic', 'transformation', 'venture', 'project', 'investing'],
        'efficiency': ['efficiency', 'optimization', 'automation', 'productivity', 'cost saving', 'improved', 'leverage', 'scale', 'cost discipline'],
        'dtc_transformation': ['DTC', 'direct-to-consumer', 'e-commerce', 'digital channel', 'owned channel', 'direct sales', 'owned retail'],
        'brand_building': ['brand building', 'brand investment', 'brand building initiatives', 'brand activation', 'brand equity', 'brand marketing'],
        'product_innovation': ['product innovation', 'new product', 'innovation', 'R&D', 'product development', 'technology innovation', 'design'],
        'supply_chain': ['supply chain', 'logistics', 'sourcing', 'supplier', 'procurement', 'inventory', 'manufacturing', 'vendor'],
        'external': ['currency', 'inflation', 'regulatory', 'macroeconomic', 'pandemic', 'economic', 'geopolitical', 'tariff', 'foreign exchange', 'fx'],
        'restructuring': ['restructuring', 'reorganization', 'integration', 'acquisition', 'merger', 'consolidation', 'divestiture'],
        'one_time': ['one-time', 'special', 'impairment', 'restructuring charge', 'legal settlement', 'settlement', 'one-off', 'non-recurring']
    },
    'efficiency_indicators': {
        'high_efficiency': ['efficiency', 'improved', 'optimization', 'cost reduction', 'productivity', 'leverage', 'scale', 'cost discipline', 'streamline'],
        'low_efficiency': ['inefficiency', 'cost increase', 'margin pressure', 'headwind', 'challenges', 'difficult', 'adverse'],
        'investment_mode': ['investment mode', 'strategic investment', 'building', 'investing in growth', 'investing for future', 'front-loaded']
    }
}

# 趋势词映射
TREND_MAPPING = {
    'increase': '上升',
    'decrease': '下降',
    'stable': '持平',
    'volatile': '波动',
    'new': '新增',
    'reduction': '削减'
}

EXPENSE_MAPPING = {
    'sga': 'SG&A费用',
    'rd': '研发费用',
    'marketing': '营销费用',
    'operating_expense': '运营费用',
    'personnel': '人力成本',
    'technology': '技术成本',
    'logistics': '物流成本',
    'marketing_digital': '数字营销',
    'real_estate': '门店成本',
    'legal': '法律合规'
}

DRIVER_MAPPING = {
    'business_expansion': '业务扩张',
    'investment': '投资驱动',
    'efficiency': '效率提升',
    'dtc_transformation': 'DTC转型',
    'brand_building': '品牌建设',
    'product_innovation': '产品创新',
    'supply_chain': '供应链',
    'external': '外部因素',
    'restructuring': '重组整合',
    'one_time': '一次性'
}

def extract_mda_text(pdf_path):
    """提取MD&A相关文本"""
    mda_texts = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                # 查找MD&A相关页面
                text_lower = text.lower()
                mda_keywords = [
                    'management', 'discussion', 'operating', 'expense', 'revenue',
                    'selling and administrative', 'demand creation', 'gross profit',
                    'operating income', 'financial condition', 'liquidity'
                ]

                matches = sum(1 for kw in mda_keywords if kw in text_lower)
                if matches >= 2:
                    mda_texts.append({
                        'page': page_num + 1,
                        'text': text,
                        'match_count': matches
                    })

    return mda_texts

def extract_expense_paragraphs(text):
    """从文本中提取费用相关段落"""
    paragraphs = []
    lines = text.split('\n')

    current_para = []
    for line in lines:
        line = line.strip()
        if len(line) < 20:
            if current_para:
                para_text = ' '.join(current_para)
                if len(para_text) > 100:  # 过滤太短的段落
                    paragraphs.append(para_text)
                current_para = []
        else:
            current_para.append(line)

    # 处理最后一段
    if current_para:
        para_text = ' '.join(current_para)
        if len(para_text) > 100:
            paragraphs.append(para_text)

    return paragraphs

def annotate_text(text):
    """对文本进行关键词标注"""
    text_lower = text.lower()

    annotations = {
        'expense_types': [],
        'trends': [],
        'drivers': [],
        'efficiency_indicators': []
    }

    # 标注费用类型
    for exp_type, keywords in KEYWORD_DICT['expense_types'].items():
        for kw in keywords:
            if kw.lower() in text_lower:
                if exp_type not in annotations['expense_types']:
                    annotations['expense_types'].append(exp_type)

    # 标注趋势
    for trend, keywords in KEYWORD_DICT['trends'].items():
        for kw in keywords:
            if kw.lower() in text_lower:
                if trend not in annotations['trends']:
                    annotations['trends'].append(trend)

    # 标注驱动因素
    for driver, keywords in KEYWORD_DICT['drivers'].items():
        for kw in keywords:
            if kw.lower() in text_lower:
                if driver not in annotations['drivers']:
                    annotations['drivers'].append(driver)

    # 标注效率指标
    for eff_type, keywords in KEYWORD_DICT['efficiency_indicators'].items():
        for kw in keywords:
            if kw.lower() in text_lower:
                if eff_type not in annotations['efficiency_indicators']:
                    annotations['efficiency_indicators'].append(eff_type)

    return annotations

def extract_sentiment(text):
    """判断情感倾向"""
    text_lower = text.lower()

    positive_words = ['improved', 'increased', 'growth', 'optimistic', 'strong', 'positive', 'achieved', 'success', 'favorable']
    negative_words = ['declined', 'decrease', 'challenge', 'difficult', 'negative', 'weak', 'concern', 'adverse', 'headwind', 'pressure']

    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)

    if pos_count > neg_count:
        return '正面'
    elif neg_count > pos_count:
        return '负面'
    else:
        return '中性'

def find_percentages(text):
    """提取文本中的百分比数字"""
    # 查找如 "XX%" 或 "increased/decreased by XX%"
    percentages = []

    # 匹配百分比
    pct_matches = re.findall(r'(\d+(?:\.\d+)?)\s*%', text)
    percentages.extend([float(p) for p in pct_matches])

    # 匹配增长/下降描述
    growth_matches = re.findall(r'(increased|decreased| grew | declined | rose | fell )\\s*by\\s*(\\d+(?:\\.\\d+)?)', text, re.IGNORECASE)
    for match in growth_matches:
        try:
            percentages.append(float(match[1]))
        except:
            pass

    return list(set(percentages))

def main():
    print("Nike MD&A 文本提取与标注")
    print("="*60)

    # 提取MD&A文本
    print("\n[1] 提取MD&A文本...")
    mda_texts = extract_mda_text(NIKE_10K_PATH)
    print(f"找到 {len(mda_texts)} 个MD&A相关页面")

    # 提取费用相关段落
    print("\n[2] 提取费用相关段落...")
    all_paragraphs = []

    for item in mda_texts:
        paragraphs = extract_expense_paragraphs(item['text'])
        for para in paragraphs:
            all_paragraphs.append({
                'page': item['page'],
                'text': para
            })

    print(f"提取了 {len(all_paragraphs)} 个段落")

    # 对段落进行标注
    print("\n[3] 标注段落...")
    annotated_paragraphs = []

    for i, para_item in enumerate(all_paragraphs):
        text = para_item['text']
        annotations = annotate_text(text)

        # 只保留有标注的段落
        if any(annotations.values()):
            sentiment = extract_sentiment(text)
            percentages = find_percentages(text)

            annotated_paragraphs.append({
                'id': f'nike_mda_{i+1:03d}',
                'page': para_item['page'],
                'original_text': text[:500],  # 限制长度
                'annotations': {
                    'expense_types': [EXPENSE_MAPPING.get(e, e) for e in annotations['expense_types']],
                    'trends': [TREND_MAPPING.get(t, t) for t in annotations['trends']],
                    'drivers': [DRIVER_MAPPING.get(d, d) for d in annotations['drivers']],
                    'efficiency': annotations['efficiency_indicators'],
                    'sentiment': sentiment
                },
                'percentages': percentages[:5] if percentages else [],
                'raw_annotation': annotations
            })

    print(f"有效标注段落: {len(annotated_paragraphs)} 个")

    # 统计标注分布
    print("\n[4] 标注分布统计...")
    expense_counter = Counter()
    trend_counter = Counter()
    driver_counter = Counter()
    sentiment_counter = Counter()

    for para in annotated_paragraphs:
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

    print("\n情感倾向分布:")
    for sentiment, count in sentiment_counter.most_common():
        print(f"  {sentiment}: {count}")

    # 保存标注结果
    print("\n[5] 保存标注结果...")
    output_data = {
        'version': '2.0',
        'company': 'Nike',
        'report_type': '10-K FY2025',
        'total_pages': len(mda_texts),
        'total_paragraphs': len(annotated_paragraphs),
        'annotation_summary': {
            'expense_types': dict(expense_counter),
            'trends': dict(trend_counter),
            'drivers': dict(driver_counter),
            'sentiments': dict(sentiment_counter)
        },
        'annotated_paragraphs': annotated_paragraphs
    }

    output_path = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\费用分析package\data\nike_mda_annotations.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"标注结果已保存到: {output_path}")

    # 打印示例标注
    print("\n[6] 示例标注段落:")
    for para in annotated_paragraphs[:3]:
        print(f"\n--- {para['id']} (Page {para['page']}) ---")
        print(f"原文: {para['original_text'][:200]}...")
        print(f"标注: {para['annotations']}")

    return annotated_paragraphs, output_data

if __name__ == '__main__':
    paragraphs, data = main()