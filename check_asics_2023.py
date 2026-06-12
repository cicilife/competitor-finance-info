import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 2024年报P59之前可能有2023年的geographical data
pdf_path = r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\Asics\2024Q4 Annual Report.pdf"

with pdfplumber.open(pdf_path) as pdf:
    # 找包含2023年geographical和China的页
    for i in range(50, 60):
        text = pdf.pages[i].extract_text() or ''
        if ('Greater China' in text or 'PRC' in text or 'People' in text) and '2023' in text:
            print(f"\n=== 第{i+1}页 ===")
            print(text)