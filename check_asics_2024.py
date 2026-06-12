import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 查找2023年中国大陆数据
pdf_path = r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\Asics\2024Q4 Annual Report.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(f"总页数: {len(pdf.pages)}")
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text() or ''
        if 'People' in text and 'China' in text:
            print(f"\n=== 第{i}页 ===")
            print(text[:2000])