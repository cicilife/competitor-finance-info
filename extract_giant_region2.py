import pdfplumber
import os

# Search for regional sales breakdown in Giant FY2025 report
pdf_dir = r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\捷安特'
pdf_path = os.path.join(pdf_dir, "Giant 2025_Annual_Report_EN.pdf")

print("=== 捷安特 Regional Sales Data ===")
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ''
        # Look for sales by location/region tables
        if 'Sales value as' in text or 'Location' in text:
            print(f"\n--- Page {i+1} ---")
            print(text[:3000])
