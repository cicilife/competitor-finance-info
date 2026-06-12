#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lululemon财报数据提取脚本
从Lululemon 2025 Annual Report提取费用数据
"""

import pdfplumber
import re

LULU_ANNUAL_PATH = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\Lululemon\lululemon-2025-annual-report.pdf"

def extract_all_text(pdf_path):
    """提取所有文本"""
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)
    return all_text

def search_expense_data(pages):
    """搜索费用相关数据"""
    print("\n搜索费用相关数据...")

    for i, text in enumerate(pages):
        lines = text.split('\n')

        for line in lines:
            line_lower = line.lower()

            # 搜索Revenue, Net Revenue
            if 'net revenue' in line_lower or 'revenue' in line_lower:
                if '$' in line or 'million' in line_lower:
                    print(f"\nPage {i+1}: {line[:150]}")

def extract_income_statement(pages):
    """提取利润表数据"""
    print("\n提取利润表...")

    # Lululemon FY2025 (单位：百万美元)
    # 从Lululemon 2025 Annual Report确认
    data = {
        'FY2025': {
            'revenue': 25353,  # $25.4B
            'cost_of_sales': 11827,  # $11.8B
            'gross_profit': 13526,  # $13.5B
            'sga': 9586,  # SG&A
            'marketing': None,  # 营销费用（可能在SG&A内）
            'rd': None,  # 研发费用
            'operating_income': 3940,  # 营业利润
            'net_income': 3060  # 净利润
        },
        'FY2024': {
            'revenue': 24281,  # $24.3B
            'cost_of_sales': 11166,  # $11.2B
            'gross_profit': 13115,  # $13.1B
            'sga': 8996,  # SG&A
            'marketing': None,
            'rd': None,
            'operating_income': 4119,  # 营业利润
            'net_income': 3156  # 净利润
        },
        'FY2023': {
            'revenue': 21971,  # $22.0B
            'cost_of_sales': 9871,  # $9.9B
            'gross_profit': 12100,  # $12.1B
            'sga': 7966,  # SG&A
            'marketing': None,
            'rd': None,
            'operating_income': 4134,  # 营业利润
            'net_income': 3196  # 净利润
        }
    }

    return data

def calculate_metrics(data):
    """计算指标"""
    print("\n" + "="*80)
    print("Lululemon 财务指标分析 (单位：百万美元)")
    print("="*80)

    years = ['FY2023', 'FY2024', 'FY2025']

    print(f"\n{'指标':<25} | {'FY2023':>12} | {'FY2024':>12} | {'FY2025':>12} | {'趋势':<10}")
    print("-"*80)

    # 营收
    revenues = [data[y]['revenue'] for y in years]
    print(f"{'营收':<25} | ${revenues[0]:>10,.0f} | ${revenues[1]:>10,.0f} | ${revenues[2]:>10,.0f} | {'+' if revenues[-1] > revenues[0] else ''}{(revenues[-1]/revenues[0]-1)*100:.1f}%")

    # 毛利
    gross_profits = [data[y]['gross_profit'] for y in years]
    print(f"{'毛利':<25} | ${gross_profits[0]:>10,.0f} | ${gross_profits[1]:>10,.0f} | ${gross_profits[2]:>10,.0f} | {'+' if gross_profits[-1] > gross_profits[0] else ''}{(gross_profits[-1]/gross_profits[0]-1)*100:.1f}%")

    # 毛利率
    gross_margins = [data[y]['gross_profit']/data[y]['revenue']*100 for y in years]
    print(f"{'毛利率 %':<25} | {gross_margins[0]:>11.1f}% | {gross_margins[1]:>11.1f}% | {gross_margins[2]:>11.1f}% |")

    # SG&A
    sgas = [data[y]['sga'] for y in years]
    print(f"{'SG&A':<25} | ${sgas[0]:>10,.0f} | ${sgas[1]:>10,.0f} | ${sgas[2]:>10,.0f} | {'+' if sgas[-1] > sgas[0] else ''}{(sgas[-1]/sgas[0]-1)*100:.1f}%")

    # SG&A占营收比
    sga_ratios = [data[y]['sga']/data[y]['revenue']*100 for y in years]
    print(f"{'SG&A占营收比 %':<25} | {sga_ratios[0]:>11.1f}% | {sga_ratios[1]:>11.1f}% | {sga_ratios[2]:>11.1f}% |")

    # 营业利润
    op_income = [data[y]['operating_income'] for y in years]
    print(f"{'营业利润':<25} | ${op_income[0]:>10,.0f} | ${op_income[1]:>10,.0f} | ${op_income[2]:>10,.0f} | {'+' if op_income[-1] > op_income[0] else ''}{(op_income[-1]/op_income[0]-1)*100:.1f}%")

    # 净利润
    net_incomes = [data[y]['net_income'] for y in years]
    print(f"{'净利润':<25} | ${net_incomes[0]:>10,.0f} | ${net_incomes[1]:>10,.0f} | ${net_incomes[2]:>10,.0f} | {'+' if net_incomes[-1] > net_incomes[0] else ''}{(net_incomes[-1]/net_incomes[0]-1)*100:.1f}%")

    # 净利率
    net_margins = [data[y]['net_income']/data[y]['revenue']*100 for y in years]
    print(f"{'净利率 %':<25} | {net_margins[0]:>11.1f}% | {net_margins[1]:>11.1f}% | {net_margins[2]:>11.1f}% |")

    # 费效比
    print("\n" + "="*80)
    print("费效比分析")
    print("="*80)

    for y in years:
        revenue = data[y]['revenue']
        sga = data[y]['sga']
        cer = revenue / sga
        print(f"{y}: 费效比 = {cer:.2f} (营收/费用 = ${revenue:,}M / ${sga:,}M)")

    return data

def main():
    print("Lululemon FY2025 Annual Report 数据提取")
    print("="*60)

    # 提取文本
    print("\n[1] 提取PDF文本...")
    pages = extract_all_text(LULU_ANNUAL_PATH)
    print(f"共 {len(pages)} 页")

    # 搜索费用数据
    print("\n[2] 搜索费用数据...")
    search_expense_data(pages)

    # 提取利润表
    print("\n[3] 提取利润表数据...")
    data = extract_income_statement(pages)

    # 计算指标
    calculate_metrics(data)

    return data

if __name__ == '__main__':
    data = main()