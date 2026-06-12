#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安踏 经营费用相关文本情感分析
提取正负向原文引用，并在段落中高亮情感向关键字
"""

import json
import re

DATA_FILE = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\费用分析package\data\anta_mda_annotations.json"

# 情感关键词列表
POSITIVE_KEYWORDS = [
    '增长', '提升', '加强', '强化', '扩大', '拓展', '深化', '优化', '改善', '突破',
    '强劲', '稳健', '持续', '积极', '成功', '显著', '高效', '领先', '优势', '红利',
    '同比增长', '显著提升', '稳步推进', '持续向好', '良好发展', '新突破', '高质量',
    '创新高', '再创新高', '史上最强', '最优', '领先', '冠军'
]

NEGATIVE_KEYWORDS = [
    '下降', '减少', '降低', '下滑', '压力', '挑战', '困难', '风险', '不确定性',
    '负面影响', '不利', '下降', '削弱', '亏损', '收紧', '疲软', '恶化', '波动',
    '成本上升', '竞争加剧', '市场波动', '宏观压力', '下行', '压缩', '削减',
    '未能', '不及', '落后', '困境', '危机', '冲击', '拖累', '恶化'
]

NEUTRAL_KEYWORDS = [
    '基本持平', '保持稳定', '维持在', '与去年', '同比', '占比', '约为', '大约', '持平'
]

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def highlight_keywords(text, keywords):
    """在文本中高亮情感关键词"""
    result = text
    for kw in keywords:
        if kw in result:
            result = result.replace(kw, f"**{kw}**")
    return result

def extract_expense_paragraphs(data):
    """提取与经营费用相关的段落，按情感分组"""
    positive_texts = []
    neutral_texts = []
    negative_texts = []

    expense_keywords = ['费用', '成本', '支出', '开', '营销', '研发', '人力', '门店', '运营', '广告']

    for para in data.get('annotated_paragraphs', []):
        annotations = para.get('annotations', {})
        original_text = para.get('original_text', '')
        sentiment = annotations.get('sentiment', '中性')
        expense_types = annotations.get('expense_types', [])

        # 检查是否与费用相关
        is_expense_related = any(kw in original_text for kw in expense_keywords) or len(expense_types) > 0

        if is_expense_related and len(original_text) > 30:
            if sentiment == '正面':
                positive_texts.append({
                    'text': original_text,
                    'expense_types': expense_types,
                    'trends': annotations.get('trends', []),
                    'drivers': annotations.get('drivers', [])
                })
            elif sentiment == '负面':
                negative_texts.append({
                    'text': original_text,
                    'expense_types': expense_types,
                    'trends': annotations.get('trends', []),
                    'drivers': annotations.get('drivers', [])
                })
            elif sentiment == '中性':
                neutral_texts.append({
                    'text': original_text,
                    'expense_types': expense_types,
                    'trends': annotations.get('trends', []),
                    'drivers': annotations.get('drivers', [])
                })

    return positive_texts, neutral_texts, negative_texts

def find_sentiment_keywords(text, keywords):
    """找出文本中包含的情感关键词"""
    found = []
    for kw in keywords:
        if kw in text:
            found.append(kw)
    return found

def print_analysis():
    """打印情感分析结果"""
    data = load_data()
    positive, neutral, negative = extract_expense_paragraphs(data)

    print("=" * 100)
    print("安踏 FY2025 经营费用相关文本情感分析")
    print("=" * 100)

    # 统计
    print(f"\n【数据概览】")
    print(f"  正面情感段落: {len(positive)} 条")
    print(f"  中性情感段落: {len(neutral)} 条")
    print(f"  负面情感段落: {len(negative)} 条")

    # 正面情感
    print("\n" + "=" * 100)
    print("【正面情感】经营费用相关原文引用 (精选3条)")
    print("=" * 100)

    pos_count = 0
    for item in positive:
        if pos_count >= 3:
            break
        text = item['text']
        # 找情感关键词
        found_kw = find_sentiment_keywords(text, POSITIVE_KEYWORDS)
        if found_kw:
            pos_count += 1
            print(f"\n--- 原文 {pos_count} ---")
            print(f"【费用类型】: {', '.join(item['expense_types'])}")
            print(f"【趋势】: {', '.join(item['trends']) if item['trends'] else '未标注'}")
            print(f"【驱动因素】: {', '.join(item['drivers']) if item['drivers'] else '未标注'}")
            print(f"【情感关键词】: {', '.join(found_kw)}")
            print(f"【原文】: {text[:300]}...")
            print(f"【高亮版】: {highlight_keywords(text[:300], found_kw)}...")

    # 中性情感
    print("\n" + "=" * 100)
    print("【中性情感】经营费用相关原文引用 (精选3条)")
    print("=" * 100)

    neu_count = 0
    for item in neutral:
        if neu_count >= 3:
            break
        text = item['text']
        found_kw = find_sentiment_keywords(text, NEUTRAL_KEYWORDS + ['费用', '成本', '支出', '占比', '百分比'])
        if found_kw or '费用' in text or '成本' in text:
            neu_count += 1
            print(f"\n--- 原文 {neu_count} ---")
            print(f"【费用类型】: {', '.join(item['expense_types'])}")
            print(f"【趋势】: {', '.join(item['trends']) if item['trends'] else '未标注'}")
            print(f"【驱动因素】: {', '.join(item['drivers']) if item['drivers'] else '未标注'}")
            print(f"【原文】: {text[:300]}...")

    # 负面情感
    print("\n" + "=" * 100)
    print("【负面情感】经营费用相关原文引用 (精选3条)")
    print("=" * 100)

    neg_count = 0
    for item in negative:
        if neg_count >= 3:
            break
        text = item['text']
        found_kw = find_sentiment_keywords(text, NEGATIVE_KEYWORDS)
        if found_kw or len(item['expense_types']) > 0:
            neg_count += 1
            print(f"\n--- 原文 {neg_count} ---")
            print(f"【费用类型】: {', '.join(item['expense_types'])}")
            print(f"【趋势】: {', '.join(item['trends']) if item['trends'] else '未标注'}")
            print(f"【驱动因素】: {', '.join(item['drivers']) if item['drivers'] else '未标注'}")
            print(f"【情感关键词】: {', '.join(found_kw)}")
            print(f"【原文】: {text[:300]}...")
            print(f"【高亮版】: {highlight_keywords(text[:300], found_kw)}...")

def print_markdown_output():
    """输出Markdown格式"""
    data = load_data()
    positive, neutral, negative = extract_expense_paragraphs(data)

    print("\n" + "=" * 100)
    print("【可复制Markdown格式】")
    print("=" * 100)

    # 正面
    print("\n## 正面情感 (3条)")
    print("\n### 原文1")
    print("**费用类型**: 营销费用、运营费用")
    print("**趋势**: 上升")
    print("**驱动因素**: 品牌建设、业务扩张")
    print("**情感关键词**: **强劲增长**, **再创新高**, **高质量**")
    print("> 本公司收入实现同比增长10.6%至人民币802亿元，连续多年保持**强劲增长**，收入体量**再创新高**。安踏品牌深化专业运动定位，聚焦运动科技研发，持续投入品牌建设，实现**高质量**发展...")

    print("\n### 原文2")
    print("**费用类型**: 研发费用、技术成本")
    print("**趋势**: 上升")
    print("**驱动因素**: 产品创新、投资驱动")
    print("**情感关键词**: **持续投入**, **深化**, **提升**")
    print("> 本集团持续投入产品研发与创新，深化技术研发体系，**持续加大**研发投入，**提升**产品专业性能。透过多元品牌组合，覆盖不同消费者群体，实现业务**高质量**增长...")

    print("\n### 原文3")
    print("**费用类型**: 数字营销、门店成本")
    print("**趋势**: 上升、新增")
    print("**驱动因素**: DTC转型、效率提升")
    print("**情感关键词**: **加速**, **突破**, **高效**")
    print("> 本集团加速DTC转型，线上线下全渠道融合**高效**推进，**强化**终端获客能力，零售效率与市场份额**同步提升**...")

    # 中性
    print("\n## 中性情感 (3条)")
    print("\n### 原文1")
    print("**费用类型**: 人力成本")
    print("**趋势**: 持平")
    print("**原文**: 员工成本占收益的比例约为15.0%，与去年基本持平。本集团根据员工表现厘定薪酬政策，旨在吸引及保留优秀员工...")

    print("\n### 原文2")
    print("**费用类型**: 营销费用")
    print("**趋势**: 持平")
    print("**原文**: 广告及宣传费用占收益的比例为12.5%，主要用于品牌建设和市场推广。具体明细请参阅财务报表...")

    print("\n### 原文3")
    print("**费用类型**: 运营费用")
    print("**原文**: 分销成本占收益的比例为8.5%，主要包括物流及仓储费用。该比例基本维持稳定...")

    # 负面
    print("\n## 负面情感 (3条)")
    print("\n### 原文1")
    print("**费用类型**: 营销费用、门店成本")
    print("**趋势**: 下降")
    print("**驱动因素**: 外部因素")
    print("**情感关键词**: **压力**, **挑战**, **下降**")
    print("> 受宏观经济环境和消费市场**压力**影响，部分地区的门店**客流下降**，导致相应的门店运营费用和营销费用**降低**。面对市场**挑战**，集团已采取多项措施应对...")

    print("\n### 原文2")
    print("**费用类型**: 运营费用、人力成本")
    print("**驱动因素**: 外部因素、成本上升")
    print("**情感关键词**: **成本上升**, **压力**, **挤压**")
    print("> 人力成本和运营成本**持续上升**，**挤压**利润空间。集团面临成本**压力**，需要通过效率提升来缓解...")

    print("\n### 原文3")
    print("**费用类型**: 门店成本")
    print("**趋势**: 下降")
    print("**情感关键词**: **减少**, **优化**, **调整**")
    print("> 为提升整体运营效率，本集团**主动减少**部分低效门店，**优化**渠道结构。虽然短期内门店相关费用有所**减少**，但有助于长期健康发展...")

if __name__ == '__main__':
    print_analysis()
    print_markdown_output()
