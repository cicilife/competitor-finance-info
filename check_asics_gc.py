import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\Asics\Consolidated Financial Statements and Auditor's Report 2025.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(f"总页数: {len(pdf.pages)}")
    print("=" * 80)
    # 搜索包含China/Asia/segment的页
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text() or ''
        if any(kw in text for kw in ['China', 'Greater China', 'East Asia', 'Southeast', 'Segment']):
            print(f"\n--- 第{i}页 ---")
            print(text[:1500])