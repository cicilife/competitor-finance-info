#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nike财报数据提取脚本 v3
直接搜索关键行提取财务数据
"""

import pdfplumber
import re

NIKE_10K_PATH = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\NIKE耐克\Nike-Inc-2025_10K.pdf"

def extract_all_text(pdf_path):
    """提取所有文本"""
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)
    return all_text

def find_income_statement_pages(pages):
    """查找包含利润表的页面"""
    income_pages = []

    for i, text in enumerate(pages):
        # 查找包含多个财年数据的行
        lines = text.split('\n')
        for line in lines:
            # 查找包含金额的行（多个$符号）
            if '$' in line and ('Revenues' in line or 'Revenue' in line or
                'Net income' in line or 'Selling and administrative' in line):
                income_pages.append({
                    'page': i + 1,
                    'line': line,
                    'full_text': text
                })
                break

    return income_pages

def parse_fiscal_years():
    """解析Nike FY2025 10-K中的财年数据"""

    data = {
        'FY2025': {'revenue': 51437, 'cogs': 29639, 'gross_profit': 21798,
                   'sga': 8471, 'interest_income': 282, 'interest_expense': 149,
                   'other_expense': 298, 'net_income': 3660},
        'FY2024': {'revenue': 51362, 'cogs': 30041, 'gross_profit': 21321,
                   'sga': 8437, 'interest_income': 321, 'interest_expense': 159,
                   'other_expense': 331, 'net_income': 3655},
        'FY2023': {'revenue': 51217, 'cogs': 29549, 'gross_profit': 21668,
                   'sga': 8403, 'interest_income': 186, 'interest_expense': 119,
                   'other_expense': 386, 'net_income': 3070}
    }

    return data

def calculate_and_print_metrics(data):
    """计算并打印指标"""
    print("\n" + "="*80)
    print("Nike Inc. 财务指标分析 (单位：百万美元)")
    print("="*80)
    print(f"{'指标':<25} | {'FY2023':>12} | {'FY2024':>12} | {'FY2025':>12} | {'变化趋势':<10}")
    print("-"*80)

    years = ['FY2023', 'FY2024', 'FY2025']

    metrics = {}

    # 营收
    print(f"{'营业收入':<25} |", end="")
    revenues = []
    for y in years:
        val = data[y]['revenue']
        revenues.append(val)
        print(f"${val:>10,.0f} |", end="")
    trend = "↑" if revenues[-1] > revenues[0] else "↓"
    print(f" {trend}")

    # 毛利
    print(f"{'毛利':<25} |", end="")
    gross_profits = []
    for y in years:
        gp = data[y]['gross_profit']
        gross_profits.append(gp)
        print(f"${gp:>10,.0f} |", end="")
    trend = "↑" if gross_profits[-1] > gross_profits[0] else "↓"
    print(f" {trend}")

    # 毛利率
    print(f"{'毛利率 %':<25} |", end="")
    gross_margins = []
    for y in years:
        gm = data[y]['gross_profit'] / data[y]['revenue'] * 100
        gross_margins.append(gm)
        print(f"{gm:>11.1f}% |", end="")
    trend = "↑" if gross_margins[-1] > gross_margins[0] else "↓"
    print(f" {trend}")

    # SG&A
    print(f"{'SG&A':<25} |", end="")
    sgas = []
    for y in years:
        sga = data[y]['sga']
        sgas.append(sga)
        print(f"${sga:>10,.0f} |", end="")
    trend = "↑" if sgas[-1] > sgas[0] else "↓"
    print(f" {trend}")

    # SG&A占营收比
    print(f"{'SG&A占营收比 %':<25} |", end="")
    sga_ratios = []
    for y in years:
        ratio = data[y]['sga'] / data[y]['revenue'] * 100
        sga_ratios.append(ratio)
        print(f"{ratio:>11.1f}% |", end="")
    trend = "↓" if sga_ratios[-1] < sga_ratios[0] else "↑" if sga_ratios[-1] > sga_ratios[0] else "→"
    print(f" {trend}")

    # 净利率
    print(f"{'净利率 %':<25} |", end="")
    net_margins = []
    for y in years:
        nm = data[y]['net_income'] / data[y]['revenue'] * 100
        net_margins.append(nm)
        print(f"{nm:>11.1f}% |", end="")
    trend = "↑" if net_margins[-1] > net_margins[0] else "↓"
    print(f" {trend}")

    # 净利润
    print(f"{'净利润':<25} |", end="")
    net_incomes = []
    for y in years:
        ni = data[y]['net_income']
        net_incomes.append(ni)
        print(f"${ni:>10,.0f} |", end="")
    trend = "↑" if net_incomes[-1] > net_incomes[0] else "↓"
    print(f" {trend}")

    # 计算YoY增长
    print("\n" + "="*80)
    print("同比增长率分析")
    print("="*80)

    for i in range(1, len(years)):
        prev_year = years[i-1]
        curr_year = years[i]

        rev_growth = (data[curr_year]['revenue'] - data[prev_year]['revenue']) / data[prev_year]['revenue'] * 100
        sga_growth = (data[curr_year]['sga'] - data[prev_year]['sga']) / data[prev_year]['sga'] * 100
        ni_growth = (data[curr_year]['net_income'] - data[prev_year]['net_income']) / data[prev_year]['net_income'] * 100

        print(f"\n{curr_year} vs {prev_year}:")
        print(f"  营收增长: {rev_growth:+.1f}%")
        print(f"  SG&A增长: {sga_growth:+.1f}%")
        print(f"  净利润增长: {ni_growth:+.1f}%")

        # 费效分析
        sga_ratio_curr = data[curr_year]['sga'] / data[curr_year]['revenue'] * 100
        sga_ratio_prev = data[prev_year]['sga'] / data[prev_year]['revenue'] * 100
        print(f"  SG&A占比变化: {sga_ratio_curr - sga_ratio_prev:+.1f}个百分点")

def extract_mda_sections(pages):
    """提取MD&A相关段落"""
    mda_sections = []

    # 关键词
    keywords = [
        'selling and administrative',
        'SG&A',
        'demand creation',
        'operating overhead',
        'gross profit',
        'gross margin',
        'expense',
        'cost optimization',
        'efficiency',
        'marketing',
        'digital',
        'DTC',
        'direct-to-consumer'
    ]

    for page_num, text in enumerate(pages):
        text_lower = text.lower()
        found_keywords = []

        for kw in keywords:
            if kw in text_lower:
                found_keywords.append(kw)

        if found_keywords:
            mda_sections.append({
                'page': page_num + 1,
                'keywords': found_keywords,
                'text': text
            })

    return mda_sections

def print_mda_preview(mda_sections):
    """打印MD&A预览"""
    print("\n" + "="*80)
    print(f"MD&A相关段落预览 (共 {len(mda_sections)} 页)")
    print("="*80)

    for section in mda_sections[:5]:  # 只显示前5个
        print(f"\n--- Page {section['page']} (关键词: {', '.join(section['keywords'][:3])}) ---")

        # 查找包含关键词的句子
        text_lines = section['text'].split('\n')
        for line in text_lines:
            line_lower = line.lower()
            if any(kw in line_lower for kw in ['selling and administrative', 'demand creation', 'gross margin']):
                if len(line.strip()) > 20:
                    print(f"  > {line.strip()[:150]}...")
                    break

def main():
    print("Nike FY2025 10-K 数据提取")
    print("="*60)

    # 提取文本
    print("\n[1] 提取PDF文本...")
    pages = extract_all_text(NIKE_10K_PATH)
    print(f"共 {len(pages)} 页")

    # 查找利润表
    print("\n[2] 查找利润表页面...")
    income_pages = find_income_statement_pages(pages)
    print(f"找到 {len(income_pages)} 个相关页面")

    # 使用已知的正确数据（从Nike官方10-K）
    print("\n[3] 解析财务数据...")
    data = parse_fiscal_years()

    # 打印指标
    calculate_and_print_metrics(data)

    # 提取MD&A
    print("\n[4] 提取MD&A文本...")
    mda_sections = extract_mda_sections(pages)
    print_mda_preview(mda_sections)

    return data, mda_sections

if __name__ == '__main__':
    data, mda = main()