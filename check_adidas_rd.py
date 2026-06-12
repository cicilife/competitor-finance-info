import pdfplumber
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\Adidas阿迪达斯\adidas_annual_report_2024_EN_Final_secured_c8nukv.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text() or ''
        if 'Research and development' in text and ('expenses' in text.lower() or 'million' in text.lower()):
            if '€' in text or re.search(r'\d,\d{3}', text):
                print(f"\n=== 第{i}页 ===")
                print(text[:3000])
                print("---")