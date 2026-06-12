import pdfplumber
import os

pdf_files = [
    ('docs/安踏-2025年报.pdf', '安踏体育'),
    ('docs/安踏-2026Q1季报.pdf', '安踏体育'),
    ('竞品财务PDF库/Lululemon/年报/2024 Annual report.pdf', 'Lululemon'),
    ('竞品财务PDF库/PUMA彪马/年报/年报 Access our Annual Report 2025 here.pdf', 'PUMA彪马'),
]

def analyze_pdf(pdf_path, brand):
    print(f"\n{'='*100}")
    print(f"分析文件: {pdf_path}")
    print('='*100)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # 查看前3页的文本内容
            for i in range(min(3, len(pdf.pages))):
                page = pdf.pages[i]
                text = page.extract_text()
                if text:
                    print(f"\n--- 第 {i+1} 页内容预览 ---")
                    print(text[:1000])
                # 提取表格
                tables = page.extract_tables()
                if tables:
                    print(f"\n--- 第 {i+1} 页包含 {len(tables)} 个表格 ---")
                    for idx, table in enumerate(tables[:2]):
                        print(f"\n表格 {idx+1}:")
                        for row in table[:5]:
                            print(row)
    except Exception as e:
        print(f"错误: {e}")

for pdf_path, brand in pdf_files:
    if os.path.exists(pdf_path):
        analyze_pdf(pdf_path, brand)
