#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成"技术成本"相关文本的词频统计，按情感正负向区分
输出为可复制的纯文本格式
"""

import json
import re
from collections import Counter

# 数据文件路径
DATA_FILE = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\费用分析package\data\nike_mda_annotations.json"

def load_data():
    """加载标注数据"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_tech_cost_paragraphs(data):
    """提取所有标注为"技术成本"的段落，按情感分组"""
    positive_texts = []
    neutral_texts = []
    negative_texts = []

    for para in data.get('annotated_paragraphs', []):
        annotations = para.get('annotations', {})
        expense_types = annotations.get('expense_types', [])
        sentiment = annotations.get('sentiment', '中性')
        original_text = para.get('original_text', '')

        if '技术成本' in expense_types and original_text.strip():
            if sentiment == '正面':
                positive_texts.append(original_text)
            elif sentiment == '中性':
                neutral_texts.append(original_text)
            elif sentiment == '负面':
                negative_texts.append(original_text)

    return positive_texts, neutral_texts, negative_texts

def tokenize_text(texts):
    """中英文分词"""
    words = []
    for text in texts:
        # 提取单词和中文词
        for word in re.findall(r'[\w\u4e00-\u9fff]+', text.lower()):
            if len(word) > 2:
                words.append(word.lower())
    return words

def get_word_frequency(texts, top_n=20):
    """获取词频统计"""
    words = tokenize_text(texts)
    # 停用词列表
    stopwords = {
        'and', 'the', 'to', 'of', 'in', 'for', 'on', 'with', 'as', 'at', 'by',
        'our', 'we', 'are', 'is', 'was', 'were', 'be', 'been', 'being',
        'this', 'that', 'these', 'those', 'it', 'its', 'from', 'or', 'and',
        'have', 'has', 'had', 'not', 'but', 'which', 'all', 'can', 'will',
        'also', 'more', 'than', 'their', 'they', 'them', 'when', 'were',
        '主要', '包括', '我们', '由于', '因此', '但是', '以及', '对于', '关于'
    }
    filtered = [w for w in words if w not in stopwords]
    return Counter(filtered).most_common(top_n)

def print_wordcloud_output(positive_texts, neutral_texts, negative_texts):
    """打印词云格式的输出"""
    print("=" * 80)
    print("Nike FY2025 '技术成本' 相关文本词频统计（按情感分组）")
    print("=" * 80)

    print("\n" + "=" * 80)
    print("【正面情感】相关词汇 TOP 20")
    print("=" * 80)
    pos_freq = get_word_frequency(positive_texts, 20)
    print(f"段落数量: {len(positive_texts)}")
    print("\n词频（由高到低）:")
    for i, (word, count) in enumerate(pos_freq, 1):
        bar = "█" * min(count, 30)
        print(f"{i:2}. {word:20} {count:3} {bar}")

    print("\n" + "=" * 80)
    print("【中性情感】相关词汇 TOP 30")
    print("=" * 80)
    neu_freq = get_word_frequency(neutral_texts, 30)
    print(f"段落数量: {len(neutral_texts)}")
    print("\n词频（由高到低）:")
    for i, (word, count) in enumerate(neu_freq, 1):
        bar = "█" * min(count, 30)
        print(f"{i:2}. {word:20} {count:3} {bar}")

    print("\n" + "=" * 80)
    print("【负面情感】相关词汇 TOP 20")
    print("=" * 80)
    neg_freq = get_word_frequency(negative_texts, 20)
    print(f"段落数量: {len(negative_texts)}")
    print("\n词频（由高到低）:")
    for i, (word, count) in enumerate(neg_freq, 1):
        bar = "█" * min(count, 30)
        print(f"{i:2}. {word:20} {count:3} {bar}")

    # 输出可复制的表格格式
    print("\n" + "=" * 80)
    print("【可复制格式】")
    print("=" * 80)

    print("\n正面情感词汇:")
    print("单词\t\t频次")
    for word, count in pos_freq:
        print(f"{word}\t\t{count}")

    print("\n中性情感词汇:")
    print("单词\t\t频次")
    for word, count in neu_freq:
        print(f"{word}\t\t{count}")

    print("\n负面情感词汇:")
    print("单词\t\t频次")
    for word, count in neg_freq:
        print(f"{word}\t\t{count}")

def main():
    print("加载数据...")
    data = load_data()

    print("提取'技术成本'相关段落...")
    positive_texts, neutral_texts, negative_texts = extract_tech_cost_paragraphs(data)

    print_wordcloud_output(positive_texts, neutral_texts, negative_texts)

if __name__ == '__main__':
    main()
