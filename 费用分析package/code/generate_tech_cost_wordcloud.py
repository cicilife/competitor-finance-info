#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成"技术成本"相关文本的词云，按情感正负向区分
"""

import json
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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
            text_clean = clean_text(original_text)

            if sentiment == '正面':
                positive_texts.append(text_clean)
            elif sentiment == '中性':
                neutral_texts.append(text_clean)
            elif sentiment == '负面':
                negative_texts.append(text_clean)

    return positive_texts, neutral_texts, negative_texts

def clean_text(text):
    """清洗文本"""
    # 移除特殊字符和数字，保留中文和英文
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def tokenize_text(text):
    """中英文分词"""
    # 移除非字母字符（保留中文）
    words = []
    for word in re.findall(r'[\w\u4e00-\u9fff]+', text):
        if len(word) > 2:  # 过滤太短的词
            words.append(word.lower())
    return words

def generate_wordcloud(texts, title, color='Blues'):
    """生成词云"""
    if not texts:
        return None

    # 合并所有文本
    all_text = ' '.join(texts)

    # 分词
    words = tokenize_text(all_text)
    word_text = ' '.join(words)

    if not word_text.strip():
        return None

    # 生成词云
    wc = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap=color,
        max_words=50,
        font_path='C:/Windows/Fonts/simhei.ttf',  # 中文黑体
        min_font_size=10,
        max_font_size=100
    )

    wc.generate(word_text)
    return wc

def plot_wordclouds(positive_texts, neutral_texts, negative_texts):
    """绘制三个情感分组的词云"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # 正面 - 绿色系
    wc_pos = generate_wordcloud(positive_texts, '正面情感', 'Greens')
    if wc_pos:
        axes[0].imshow(wc_pos, interpolation='bilinear')
        axes[0].set_title(f'正面 (技术成本)\n{len(positive_texts)}条', fontsize=14, color='green')
    else:
        axes[0].set_title('正面 (无数据)', fontsize=14, color='green')
    axes[0].axis('off')

    # 中性 - 蓝色系
    wc_neu = generate_wordcloud(neutral_texts, '中性情感', 'Blues')
    if wc_neu:
        axes[1].imshow(wc_neu, interpolation='bilinear')
        axes[1].set_title(f'中性 (技术成本)\n{len(neutral_texts)}条', fontsize=14, color='blue')
    else:
        axes[1].set_title('中性 (无数据)', fontsize=14, color='blue')
    axes[1].axis('off')

    # 负面 - 红色系
    wc_neg = generate_wordcloud(negative_texts, '负面情感', 'Reds')
    if wc_neg:
        axes[2].imshow(wc_neg, interpolation='bilinear')
        axes[2].set_title(f'负面 (技术成本)\n{len(negative_texts)}条', fontsize=14, color='red')
    else:
        axes[2].set_title('负面 (无数据)', fontsize=14, color='red')
    axes[2].axis('off')

    plt.suptitle('Nike FY2025 "技术成本" 相关文本词云（按情感分组）', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\费用分析package\reports\tech_cost_wordcloud.png',
                dpi=150, bbox_inches='tight')
    plt.show()
    print("词云已保存至: tech_cost_wordcloud.png")

def print_summary(positive_texts, neutral_texts, negative_texts):
    """打印文本摘要"""
    print("=" * 80)
    print("Nike FY2025 '技术成本' 相关文本统计")
    print("=" * 80)
    print(f"\n正面情感段落数: {len(positive_texts)}")
    print(f"中性情感段落数: {len(neutral_texts)}")
    print(f"负面情感段落数: {len(negative_texts)}")

    print("\n" + "-" * 40)
    print("正面情感样例 (前3条):")
    print("-" * 40)
    for i, text in enumerate(positive_texts[:3], 1):
        print(f"{i}. {text[:100]}...")

    print("\n" + "-" * 40)
    print("中性情感样例 (前3条):")
    print("-" * 40)
    for i, text in enumerate(neutral_texts[:3], 1):
        print(f"{i}. {text[:100]}...")

    print("\n" + "-" * 40)
    print("负面情感样例 (前3条):")
    print("-" * 40)
    for i, text in enumerate(negative_texts[:3], 1):
        print(f"{i}. {text[:100]}...")

def main():
    print("加载数据...")
    data = load_data()

    print("提取'技术成本'相关段落...")
    positive_texts, neutral_texts, negative_texts = extract_tech_cost_paragraphs(data)

    print_summary(positive_texts, neutral_texts, negative_texts)

    print("\n生成词云...")
    plot_wordclouds(positive_texts, neutral_texts, negative_texts)

if __name__ == '__main__':
    main()
