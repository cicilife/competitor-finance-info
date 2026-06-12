import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\Adidas阿迪达斯\adidas_annual_report_2024_EN_Final_secured_c8nukv.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text() or ''
        if 'Marketing and Promotion' in text and 'Research and Development' in text:
            print(f"\n=== 第{i}页 ===")
            print(text)
            break