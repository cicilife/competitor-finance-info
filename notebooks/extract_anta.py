import pdfplumber
import os

docs_dir = r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\docs"
files = [
    "安踏-2025年报.pdf",
    "安踏-2026Q1季报.pdf",
    "安踏-2026Q1投资者简报.pdf"
]

for filename in files:
    filepath = os.path.join(docs_dir, filename)
    print(f"\n{'='*60}")
    print(f"文件: {filename}")
    print('='*60)

    with pdfplumber.open(filepath) as pdf:
        print(f"总页数: {len(pdf.pages)}")
        print("\n--- 前5页文本内容预览 ---")
        for i, page in enumerate(pdf.pages[:5]):
            text = page.extract_text()
            if text:
                print(f"\n[第{i+1}页]")
                print(text[:1500] if len(text) > 1500 else text)
                print("..." if len(text) > 1500 else "")
