import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\Asics\Consolidated Financial Statements and Auditor's Report 2025.pdf"

with pdfplumber.open(pdf_path) as pdf:
    # P65 (index 64) and 后续页
    for i in [64, 65, 66, 67]:
        text = pdf.pages[i].extract_text() or ''
        if 'People' in text or 'China' in text or 'PRC' in text:
            print(f"\n=== 第{i+1}页 ===")
            print(text)
            break