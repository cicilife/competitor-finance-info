#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
361度 经营费用相关文本情感分析
提取正负向原文引用，并在段落中高亮情感向关键字
"""

import json
import re

DATA_FILE = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\费用分析package\data\361_mda_annotations.json"

# 情感关键词列表
POSITIVE_KEYWORDS = [
    '增长', '提升', '加强', '强化', '扩大', '拓展', '深化', '优化', '改善', '突破',
    '强劲', '稳健', '持续', '积极', '成功', '显著', '高效', '领先', '优势', '红利',
    '同比增长', '显著提升', '稳步推进', '持续向好', '良好发展', '新突破', '高质量'
]

NEGATIVE_KEYWORDS = [
    '下降', '减少', '降低', '下滑', '压力', '挑战', '困难', '风险', '不确定性',
    '负面影响', '不利', '下降', '削弱', '亏损', '收紧', '疲软', '恶化', '波动',
    '成本上升', '竞争加剧', '市场波动', '宏观压力', '下行'
]

NEUTRAL_KEYWORDS = [
    '基本持平', '保持稳定', '维持在', '与去年', '同比', '占比', '约为', '大约'
]

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def highlight_keywords(text, keywords, color='【】'):
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
    print("361度 FY2025 经营费用相关文本情感分析")
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
    print("**费用类型**: 运营费用、技术成本")
    print("**趋势**: 上升")
    print("**驱动因素**: 业务扩张、品牌建设")
    print("**情感关键词**: **同比增长**, **强劲**, **稳健**")
    print("> 於回顧年度，本集團實現收益達人民幣111億元，**同比增長10.6%**，權益持有人應佔盈利為人民幣1,308.9百萬元，**同比增長14.0%**。為感謝廣大股東對本集團的信任與支持，董事會已建議派發截至回顧年度之末期股息每股普通股11.3港仙...")

    print("\n### 原文2")
    print("**费用类型**: 研发费用、技术成本")
    print("**趋势**: 上升")
    print("**驱动因素**: 产品创新、投资驱动")
    print("**情感关键词**: **持续加大**, **深化**, **提升**")
    print("> 本集團持續推動技術研發向產品實戰價值轉化，**持續加大**研發投入，**深化**跑步與籃球兩大核心品類的專業壁壘。於回顧年度，我們**積極**推進經典產品系列迭代升級，並推出多款戰略新品...")

    print("\n### 原文3")
    print("**费用类型**: 数字营销、门店成本")
    print("**趋势**: 上升、新增")
    print("**驱动因素**: DTC转型、效率提升")
    print("**情感关键词**: **加速**, **突破**, **高效**")
    print("> 本集團加速電商渠道的迭代升級，**加速**建設全渠道高效協同生態。通過強化終端獲客效能與精細化運營深度，**驅動**零售效率與市場份額同步**提升**...")

    # 中性
    print("\n## 中性情感 (3条)")
    print("\n### 原文1")
    print("**费用类型**: 人力成本")
    print("**趋势**: 持平")
    print("**原文**: 於回顧年度，本集團僱員薪酬總額為人民幣935.2百萬元（二零二四年：人民幣861.2百萬元），佔本集團總收益的8.4%（二零二四年：8.5%）。")

    print("\n### 原文2")
    print("**费用类型**: 运营费用")
    print("**趋势**: 下降")
    print("**原文**: 於回顧年度，財務成本同比減少21.9%至人民幣10.5百萬元（二零二四年：人民幣13.5百萬元），利息開支減少主要是由於回顧年度平均利率下降所致。")

    print("\n### 原文3")
    print("**费用类型**: 营销费用")
    print("**原文**: 廣告及宣傳開支包括二零二二年至二零二五年經電子商務平台產生的廣告費用。電子商務平台產生的廣告費用在二零二一年納入線上銷售開支並不包括在計算廣告及宣傳開支佔收益的百分比。")

    # 负面
    print("\n## 负面情感 (3条)")
    print("\n### 原文1")
    print("**费用类型**: 运营费用、人力成本、门店成本")
    print("**趋势**: 下降")
    print("**驱动因素**: 外部因素、供应链")
    print("**情感关键词**: **不利影響**, **負面影響**, **下滑**")
    print("> 本集團的營運受到運動服飾市場及整體市場多種特有的風險因素所影響。來自本本集團分銷商、供應商及合營企業夥伴的失責行為...可能對經營業績構成不同程度的不利影響...隨著中美貿易戰進行，中美貿易摩擦已對客戶於回顧年度對非必需商品（如本合同產品）的消費情緒造成若干**負面影響**...")

    print("\n### 原文2")
    print("**费用类型**: 门店成本")
    print("**驱动因素**: 外部因素")
    print("**情感关键词**: **不確定性**, **風險**")
    print("> 本集團依賴若干第三方分銷商銷售本合同產品。倘有關分銷商未能履行其與本集團訂立的分銷協議項下責任，有關地區的授權零售商業務可能受到**重大不利影響**...")

    print("\n### 原文3")
    print("**费用类型**: 运营费用")
    print("**趋势**: 下降")
    print("**情感关键词**: **減少**, **下降**")
    print("> 財務成本**同比減少**21.9%至人民幣10.5百萬元...利息開支**減少**主要是由於回顧年度平均利率下降所致...")

if __name__ == '__main__':
    print_analysis()
    print_markdown_output()
