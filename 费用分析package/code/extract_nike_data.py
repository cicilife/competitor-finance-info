#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nike财报数据提取脚本
从Nike 10-K PDF中提取费用数据并整理成分析模板格式
"""

import pdfplumber
import re
import csv
from datetime import datetime

# Nike 10-K文件路径
NIKE_10K_PATH = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\NIKE耐克\Nike-Inc-2025_10K.pdf"

def extract_text_from_pdf(pdf_path):
    """从PDF提取所有文本"""
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)
    return all_text

def find_income_statement_pages(pages):
    """查找利润表相关页面"""
    income_statement_pages = []
    for i, page in enumerate(pages):
        if "CONSOLIDATED STATEMENTS OF INCOME" in page or "Revenue" in page:
            if "expense" in page.lower() or "cost" in page.lower():
                income_statement_pages.append((i, page))
    return income_statement_pages

def parse_expense_data(text):
    """解析费用数据"""
    expenses = {}

    # Nike的费用项目通常包括：
    # - Cost of sales
    # - Selling and administrative expense
    # - Interest expense (income)
    # - Other expense (income)

    lines = text.split('\n')

    for i, line in enumerate(lines):
        line_clean = line.strip()

        # 查找Cost of sales
        if re.match(r'Cost of sales', line_clean, re.IGNORECASE):
            # 尝试提取数字
            numbers = re.findall(r'[\$,]?([\d,]+)', line_clean)
            if numbers:
                expenses['cost_of_sales'] = numbers

        # 查找Selling and administrative expense
        if re.match(r'Selling and administrative', line_clean, re.IGNORECASE) or \
           re.match(r'SG&A', line_clean, re.IGNORECASE):
            numbers = re.findall(r'[\$,]?([\d,]+)', line_clean)
            if numbers:
                expenses['sga'] = numbers

        # 查找Interest income
        if re.match(r'Interest income', line_clean, re.IGNORECASE):
            numbers = re.findall(r'[\$,]?([\d,]+)', line_clean)
            if numbers:
                expenses['interest_income'] = numbers

        # 查找Interest expense
        if re.match(r'Interest expense', line_clean, re.IGNORECASE):
            numbers = re.findall(r'[\$,]?([\d,]+)', line_clean)
            if numbers:
                expenses['interest_expense'] = numbers

        # 查找Total net income
        if re.match(r'Net income', line_clean, re.IGNORECASE):
            numbers = re.findall(r'[\$,]?([\d,]+)', line_clean)
            if numbers:
                expenses['net_income'] = numbers

    return expenses

def extract_fiscal_year_data(text):
    """提取财年数据"""
    # Nike的财年通常截止于5月31日
    # 2025财年指FY2025 (截止2025年5月31日)

    data = {
        'revenue': None,
        'cost_of_sales': None,
        'gross_margin': None,
        'sga': None,
        'interest_expense': None,
        'other_expense': None,
        'net_income': None
    }

    lines = text.split('\n')

    for i, line in enumerate(lines):
        line_clean = line.strip()

        # Revenue
        if 'Revenue' in line_clean and data['revenue'] is None:
            numbers = re.findall(r'[\$,]?([\d,]+)', line_clean)
            if numbers and len(numbers) >= 1:
                try:
                    # 取第一个数字作为Revenue
                    data['revenue'] = int(numbers[0].replace(',', ''))
                except:
                    pass

        # Cost of sales
        if 'Cost of sales' in line_clean and data['cost_of_sales'] is None:
            numbers = re.findall(r'[\$,]?([\d,]+)', line_clean)
            if numbers and len(numbers) >= 1:
                try:
                    data['cost_of_sales'] = int(numbers[0].replace(',', ''))
                except:
                    pass

        # Gross margin
        if 'Gross profit' in line_clean or 'Gross margin' in line_clean:
            if data['gross_margin'] is None:
                numbers = re.findall(r'[\$,]?([\d,]+)', line_clean)
                if numbers and len(numbers) >= 1:
                    try:
                        data['gross_margin'] = int(numbers[0].replace(',', ''))
                    except:
                        pass

        # Selling and administrative expense
        if ('Selling and administrative' in line_clean or 'SG&A' in line_clean) and data['sga'] is None:
            numbers = re.findall(r'[\$,]?([\d,]+)', line_clean)
            if numbers and len(numbers) >= 1:
                try:
                    data['sga'] = int(numbers[0].replace(',', ''))
                except:
                    pass

        # Interest expense
        if 'Interest expense' in line_clean and data['interest_expense'] is None:
            numbers = re.findall(r'[\$,]?([\d,]+)', line_clean)
            if numbers and len(numbers) >= 1:
                try:
                    data['interest_expense'] = int(numbers[0].replace(',', ''))
                except:
                    pass

        # Other expense
        if 'Other expense' in line_clean and 'income' not in line_clean.lower():
            numbers = re.findall(r'[\$,]?([\d,]+)', line_clean)
            if numbers and len(numbers) >= 1:
                try:
                    data['other_expense'] = int(numbers[0].replace(',', ''))
                except:
                    pass

        # Net income
        if 'Net income' in line_clean and 'income' in line_clean.lower():
            numbers = re.findall(r'[\$,]?([\d,]+)', line_clean)
            if numbers and len(numbers) >= 1:
                try:
                    data['net_income'] = int(numbers[0].replace(',', ''))
                except:
                    pass

    return data

def extract_tables_from_pdf(pdf_path):
    """提取PDF中的表格数据"""
    tables_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    if table:
                        tables_data.append({
                            'page': i + 1,
                            'table': table
                        })
    return tables_data

def find_expense_table(tables_data):
    """查找费用相关表格"""
    expense_tables = []

    for item in tables_data:
        table = item['table']
        for row in table:
            if row:
                row_text = ' '.join([str(cell) for cell in row if cell])
                if 'selling' in row_text.lower() or 'revenue' in row_text.lower():
                    expense_tables.append(item)
                    break

    return expense_tables

def print_expense_summary(data):
    """打印费用汇总"""
    print("\n" + "="*60)
    print("Nike FY2025 费用数据汇总")
    print("="*60)

    for key, value in data.items():
        if value is not None and isinstance(value, (int, float)):
            print(f"{key}: ${value:,.0f} million")
        else:
            print(f"{key}: {value}")

    # 计算衍生指标
    if data.get('revenue') and data.get('sga'):
        sga_ratio = (data['sga'] / data['revenue']) * 100
        print(f"\nSG&A占营收比: {sga_ratio:.1f}%")

    if data.get('revenue') and data.get('cost_of_sales'):
        gross_margin = ((data['revenue'] - data['cost_of_sales']) / data['revenue']) * 100
        print(f"毛利率: {gross_margin:.1f}%")

def main():
    print("开始提取Nike 10-K数据...")
    print(f"文件路径: {NIKE_10K_PATH}")

    # 提取文本
    print("\n[1/3] 提取PDF文本...")
    pages = extract_text_from_pdf(NIKE_10K_PATH)
    print(f"共提取 {len(pages)} 页文本")

    # 查找利润表页面
    print("\n[2/3] 查找利润表数据...")
    income_pages = find_income_statement_pages(pages)
    print(f"找到 {len(income_pages)} 个可能包含利润表的页面")

    # 提取财年数据
    print("\n[3/3] 解析费用数据...")
    fiscal_data = {}

    for i, page_text in enumerate(pages):
        # Nike FY2025 (截止2025年5月31日)
        if "May 31, 2025" in page_text and "May 31, 2024" in page_text:
            data = extract_fiscal_year_data(page_text)
            if data.get('revenue'):
                fiscal_data['FY2025'] = data

        # Nike FY2024 (截止2024年5月31日)
        if "May 31, 2024" in page_text and "May 31, 2023" in page_text:
            data = extract_fiscal_year_data(page_text)
            if data.get('revenue'):
                fiscal_data['FY2024'] = data

        # Nike FY2023 (截止2023年5月31日)
        if "May 31, 2023" in page_text and "May 31, 2022" in page_text:
            data = extract_fiscal_year_data(page_text)
            if data.get('revenue'):
                fiscal_data['FY2023'] = data

    # 打印结果
    for fy, data in fiscal_data.items():
        print(f"\n{fy}:")
        print_expense_summary(data)

    # 提取表格数据
    print("\n\n提取表格数据...")
    tables = extract_tables_from_pdf(NIKE_10K_PATH)
    print(f"共找到 {len(tables)} 个表格")

    expense_tables = find_expense_table(tables)
    print(f"找到 {len(expense_tables)} 个费用相关表格")

    if expense_tables:
        print("\n费用表预览 (第一页):")
        for row in expense_tables[0]['table'][:5]:
            print(row)

    return fiscal_data, tables

if __name__ == '__main__':
    fiscal_data, tables = main()