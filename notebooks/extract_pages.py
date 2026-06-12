import pdfplumber
import os

docs_dir = r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\docs"
annual_report = os.path.join(docs_dir, "安踏-2025年报.pdf")

print("="*80)
print("提取安踏2025年报中的财务数据")
print("="*80)

with pdfplumber.open(annual_report) as pdf:
    total_pages = len(pdf.pages)

    print("\n" + "="*80)
    print("第10-15页内容 (财务概览部分)")
    print("="*80)

    for i in range(9, min(15, total_pages)):
        page = pdf.pages[i]
        text = page.extract_text()
        if text:
            print(f"\n========== 第{i+1}页 ==========")
            print(text[:4000])

            tables = page.extract_tables()
            if tables:
                print("\n[提取的表格]")
                for t_idx, table in enumerate(tables):
                    print(f"\n--- 表格 {t_idx + 1} ---")
                    for row in table[:15]:
                        print(row)
