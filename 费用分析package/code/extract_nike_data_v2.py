#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nike财报数据提取脚本 v2
使用表格解析方式提取费用数据
"""

import pdfplumber
import re

NIKE_10K_PATH = r"C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\NIKE耐克\Nike-Inc-2025_10K.pdf"

def extract_income_statement_tables(pdf_path):
    """提取利润表表格"""
    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    if table:
                        # 转换为字符串检查
                        table_str = str(table)
                        if 'Revenue' in table_str or 'revenue' in table_str:
                            all_tables.append({
                                'page': page_num + 1,
                                'table': table
                            })

    return all_tables

def parse_income_table(table):
    """解析利润表数据"""
    # Nike利润表结构（单位：百万美元）
    # 通常是3列或4列：FY2025, FY2024, FY2023

    data = {
        'revenue': {},
        'cost_of_sales': {},
        'gross_profit': {},
        'selling_and_admin': {},
        'interest_income': {},
        'interest_expense': {},
        'other_income': {},
        'net_income': {}
    }

    current_category = None

    for row in table:
        if not row:
            continue

        row_text = [str(cell).strip() if cell else '' for cell in row]

        # 打印原始行便于调试
        # print(row_text)

        # 查找关键词并提取数据
        row_str = ' '.join(row_text).lower()

        if 'revenue' in row_str and 'cost' not in row_str:
            # Revenue行
            numbers = extract_numbers_from_row(row_text)
            if len(numbers) >= 1:
                data['revenue']['FY2025'] = numbers[0]
            if len(numbers) >= 2:
                data['revenue']['FY2024'] = numbers[1]
            if len(numbers) >= 3:
                data['revenue']['FY2023'] = numbers[2]

        elif 'cost of sales' in row_str or 'cost of revenue' in row_str:
            # Cost of sales行
            numbers = extract_numbers_from_row(row_text)
            if len(numbers) >= 1:
                data['cost_of_sales']['FY2025'] = numbers[0]
            if len(numbers) >= 2:
                data['cost_of_sales']['FY2024'] = numbers[1]
            if len(numbers) >= 3:
                data['cost_of_sales']['FY2023'] = numbers[2]

        elif 'gross profit' in row_str:
            # Gross profit行
            numbers = extract_numbers_from_row(row_text)
            if len(numbers) >= 1:
                data['gross_profit']['FY2025'] = numbers[0]
            if len(numbers) >= 2:
                data['gross_profit']['FY2024'] = numbers[1]
            if len(numbers) >= 3:
                data['gross_profit']['FY2023'] = numbers[2]

        elif 'selling and administrative' in row_str or 'sga' in row_str:
            # Selling and administrative expense
            numbers = extract_numbers_from_row(row_text)
            if len(numbers) >= 1:
                data['selling_and_admin']['FY2025'] = numbers[0]
            if len(numbers) >= 2:
                data['selling_and_admin']['FY2024'] = numbers[1]
            if len(numbers) >= 3:
                data['selling_and_admin']['FY2023'] = numbers[2]

        elif 'interest income' in row_str and 'expense' not in row_str:
            numbers = extract_numbers_from_row(row_text)
            if len(numbers) >= 1:
                data['interest_income']['FY2025'] = numbers[0]
            if len(numbers) >= 2:
                data['interest_income']['FY2024'] = numbers[1]
            if len(numbers) >= 3:
                data['interest_income']['FY2023'] = numbers[2]

        elif 'interest expense' in row_str:
            numbers = extract_numbers_from_row(row_text)
            if len(numbers) >= 1:
                data['interest_expense']['FY2025'] = numbers[0]
            if len(numbers) >= 2:
                data['interest_expense']['FY2024'] = numbers[1]
            if len(numbers) >= 3:
                data['interest_expense']['FY2023'] = numbers[2]

        elif 'other' in row_str and ('income' in row_str or 'expense' in row_str):
            numbers = extract_numbers_from_row(row_text)
            if len(numbers) >= 1:
                data['other_income']['FY2025'] = numbers[0]
            if len(numbers) >= 2:
                data['other_income']['FY2024'] = numbers[1]
            if len(numbers) >= 3:
                data['other_income']['FY2023'] = numbers[2]

        elif 'net income' in row_str and 'income' in row_str:
            numbers = extract_numbers_from_row(row_text)
            if len(numbers) >= 1:
                data['net_income']['FY2025'] = numbers[0]
            if len(numbers) >= 2:
                data['net_income']['FY2024'] = numbers[1]
            if len(numbers) >= 3:
                data['net_income']['FY2023'] = numbers[2]

    return data

def extract_numbers_from_row(row):
    """从行中提取数字"""
    numbers = []

    for cell in row:
        if not cell:
            continue

        cell_str = str(cell).strip()

        # 移除$符号和括号（负数）
        cell_str = cell_str.replace('$', '').replace(',', '').replace('(', '-').replace(')', '')

        # 查找数字
        matches = re.findall(r'-?[\d]+(?:\.[\d]+)?', cell_str)
        for match in matches:
            try:
                num = float(match)
                if num > 100:  # 过滤掉太小的数字（可能是年份）
                    numbers.append(num)
            except:
                pass

    return numbers

def print_income_statement(data):
    """打印利润表"""
    print("\n" + "="*80)
    print("Nike Inc. 合并利润表 (单位：百万美元)")
    print("="*80)

    years = ['FY2023', 'FY2024', 'FY2025']

    for item, item_data in data.items():
        if any(item_data.values()):  # 只打印有数据的项
            values = []
            for year in years:
                val = item_data.get(year)
                if val:
                    values.append(f"${val:,.0f}")
                else:
                    values.append("-")
            print(f"{item:25} | {' | '.join([f'{v:>15}' for v in values])}")

def calculate_metrics(data):
    """计算衍生指标"""
    print("\n" + "="*80)
    print("衍生指标分析")
    print("="*80)

    for year in ['FY2023', 'FY2024', 'FY2025']:
        revenue = data['revenue'].get(year)
        cogs = data['cost_of_sales'].get(year)
        sga = data['selling_and_admin'].get(year)
        net_income = data['net_income'].get(year)

        if revenue and cogs:
            gross_margin = (revenue - cogs) / revenue * 100
            print(f"{year}: 毛利率 = {gross_margin:.1f}%")

        if revenue and sga:
            sga_ratio = sga / revenue * 100
            print(f"{year}: SG&A占营收比 = {sga_ratio:.1f}%")

        if revenue and net_income:
            net_margin = net_income / revenue * 100
            print(f"{year}: 净利率 = {net_margin:.1f}%")

def extract_mda_text(pdf_path):
    """提取MD&A文本"""
    mda_texts = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and ('management' in text.lower() or 'discussion' in text.lower() or
                         'operating' in text.lower() and 'expense' in text.lower()):
                mda_texts.append({
                    'page': page_num + 1,
                    'text': text
                })

    return mda_texts

def main():
    print("Nike 10-K 数据提取 v2")
    print("="*60)

    # 提取利润表
    print("\n[步骤1] 提取利润表...")
    tables = extract_income_statement_tables(NIKE_10K_PATH)
    print(f"找到 {len(tables)} 个利润表")

    if tables:
        # 使用第一个表格
        income_data = parse_income_table(tables[0]['table'])
        print_income_statement(income_data)
        calculate_metrics(income_data)

        # 打印原始表格以便调试
        print("\n\n原始表格内容 (前10行):")
        for i, row in enumerate(tables[0]['table'][:10]):
            print(f"Row {i}: {row}")

    # 提取MD&A文本
    print("\n\n[步骤2] 提取MD&A文本...")
    mda_texts = extract_mda_text(NIKE_10K_PATH)
    print(f"找到 {len(mda_texts)} 个MD&A相关页面")

    if mda_texts:
        print("\n前2页MD&A预览 (前500字符):")
        for item in mda_texts[:2]:
            print(f"\n--- Page {item['page']} ---")
            print(item['text'][:500])

    return income_data, mda_texts

if __name__ == '__main__':
    income_data, mda_texts = main()