import pdfplumber
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\Adidas阿迪达斯\adidasAG_FY_2025_Results_EN_Final_tb9z6m.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(f"总页数: {len(pdf.pages)}")
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text() or ''
        if 'Marketing and point-of-sale' in text or 'Net income' in text or 'Operating profit' in text:
            if re.search(r'€[\s\d,]+', text) and ('%' in text or 'margin' in text.lower()):
                print(f"\n=== 第{i}页 ===")
                print(text[:3000])
                print("---")