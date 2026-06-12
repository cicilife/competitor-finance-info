import pdfplumber
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\Adidas阿迪达斯\adidas_annual_report_2024_EN_Final_secured_c8nukv.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text() or ''
        # 寻找费用明细相关
        keywords = ['Marketing and', 'Research and Development', 'Personnel expense', 'Operating expenses', 'Other operating expense']
        if any(kw in text for kw in keywords):
            if re.search(r'€[\s\d,]+', text):
                print(f"\n=== 第{i}页 ===")
                print(text[:3000])
                print("---")