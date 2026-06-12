import pdfplumber
import os

docs_dir = r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\docs"
annual_report = os.path.join(docs_dir, "安踏-2025年报.pdf")

print("="*80)
print("提取安踏2025年报中的财务数据")
print("="*80)

with pdfplumber.open(annual_report) as pdf:
    total_pages = len(pdf.pages)
    print(f"总页数: {total_pages}")

    keywords_pages = {
        "五年财务概览": None,
        "综合损益表": None,
        "财务概况": None,
        "收入": None,
        "毛利率": None,
        "净利润": None,
    }

    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ""
        for kw in keywords_pages:
            if kw in text and keywords_pages[kw] is None:
                keywords_pages[kw] = i + 1
                print(f"关键词 '{kw}' 首次出现在第{i+1}页")

    print("\n" + "="*80)
    print("详细页面内容（第10-15页 - 财务概览部分）")
    print("="*80)

    for i in range(9, 16):
        if i < total_pages:
            page = pdf.pages[i]
            text = page.extract_text()
            if text:
                print(f"\n--- 第{i+1}页 ---")
                print(text[:3000])
                print("..." if len(text) > 3000 else "")

    print("\n" + "="*80)
    print("五年财务概览页面（第11页附近）")
    print("="*80)

    if keywords_pages["五年财务概览"]:
        page_num = keywords_pages["五年财务概览"] - 1
        for adj in range(-2, 3):
            if 0 <= page_num + adj < total_pages:
                page = pdf.pages[page_num + adj]
                text = page.extract_text() or ""
                if "五年" in text or "財務概覽" in text or "五年概覽" in text:
                    print(f"\n--- 第{page_num + adj + 1}页 ---")
                    print(text)
                    tables = page.extract_tables()
                    if tables:
                        print("\n提取的表格:")
                        for t_idx, table in enumerate(tables):
                            print(f"\n表格 {t_idx + 1}:")
                            for row in table[:10]:
                                print(row)
                    break
