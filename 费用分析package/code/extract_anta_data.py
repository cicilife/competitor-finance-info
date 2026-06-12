#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安踏体育财报数据提取脚本
"""

import pdfplumber
import re

ANTA_ANNUAL_PATH = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\安踏体育\安踏体育：二零二五年年报.pdf"

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
    keywords_cn = ['收入', '收益', '毛利', '费用', '销售', '营销', '经营', '利润', '净利',
                   '成本', '行政', '研发', '品牌', '增长', '下降', '门店', '电商']

    for item in pages:
        text = item['text']
        text_lower = text.lower()
        matches = sum(1 for kw in keywords_cn if kw in text)
        if matches >= 3:
            relevant.append(item)
    return relevant

def main():
    print("安踏体育 2025年报 数据提取")
    print("="*60)

    # 提取文本
    print("\n[1] 提取PDF文本...")
    pages = extract_all_text(ANTA_ANNUAL_PATH)
    print(f"共 {len(pages)} 页")

    # 搜索相关页面
    print("\n[2] 搜索相关内容页面...")
    relevant = search_relevant_pages(pages)
    print(f"找到 {len(relevant)} 个相关页面")

    # 打印前几个相关页面的内容预览
    print("\n[3] 内容预览...")
    for item in relevant[:5]:
        print(f"\n--- Page {item['page']} ---")
        print(item['text'][:300])
        print("...")

    return pages, relevant

if __name__ == '__main__':
    main()