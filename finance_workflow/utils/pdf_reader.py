
import pdfplumber
import os
import json

try:
    import tabula
    TABULA_AVAILABLE = True
except ImportError:
    TABULA_AVAILABLE = False
    print("Warning: tabula-py not installed, table extraction will be disabled")

def read_pdf(pdf_path, max_pages=100, include_tables=False):
    """读取PDF文件并返回每页的文本内容"""
    pages = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages[:max_pages]):
                text = page.extract_text()
                page_data = {
                    'page_num': i + 1,
                    'text': text
                }
                
                if include_tables and TABULA_AVAILABLE:
                    tables = extract_tables_from_page(pdf_path, i + 1)
                    if tables:
                        page_data['tables'] = tables
                
                if text or (include_tables and 'tables' in page_data):
                    pages.append(page_data)
        return pages
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return []

def extract_tables_from_page(pdf_path, page_num):
    """从指定页面提取表格数据"""
    if not TABULA_AVAILABLE:
        return []
    
    try:
        tables = tabula.read_pdf(
            pdf_path,
            pages=str(page_num),
            multiple_tables=True,
            guess=True,
            encoding='utf-8'
        )
        
        result = []
        for table in tables:
            if table is not None and not table.empty:
                table_data = table.to_dict('records')
                if table_data:
                    result.append(table_data)
        
        return result
    except Exception as e:
        print(f"Error extracting tables from page {page_num}: {e}")
        return []

def search_text(pages, keywords):
    """在PDF页面中搜索关键词"""
    results = []
    for page in pages:
        text = page['text']
        page_num = page['page_num']
        
        for keyword in keywords:
            if keyword.lower() in text.lower():
                start = text.lower().find(keyword.lower())
                context_start = max(0, start - 200)
                context_end = min(len(text), start + 200 + len(keyword))
                context = text[context_start:context_end]
                
                results.append({
                    'page_num': page_num,
                    'keyword': keyword,
                    'context': context,
                    'position': start
                })
    return results

def extract_financial_numbers(text):
    """从文本中提取财务数字（保留原始值，不做单位转换）"""
    import re
    numbers = []
    
    unit_patterns = [
        (r'([\d,]+(\.\d+)?)\s*亿元', '亿元'),
        (r'([\d,]+(\.\d+)?)\s*亿[\s元]', '亿元'),
        (r'([\d,]+(\.\d+)?)\s*百万元', '百万元'),
        (r'([\d,]+(\.\d+)?)\s*百万[\s元]', '百万元'),
        (r'([\d,]+(\.\d+)?)\s*万元', '万元'),
        (r'([\d,]+(\.\d+)?)\s*万[\s元]', '万元'),
        (r'([\d,]+(\.\d+)?)\s*千元', '千元'),
        (r'([\d,]+(\.\d+)?)\s*千[\s元]', '千元'),
        (r'(\d{1,3}(?:,\d{3}){2,}(?:\.\d+)?)\s*(?:元|人民币|CNY)', '元'),
        (r'(\d{1,3}(?:,\d{3}){2,}(?:\.\d+)?)', '')
    ]
    
    for pattern, unit in unit_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            num_str = match[0].replace(',', '')
            try:
                num = float(num_str)
                if num >= 1000:
                    numbers.append((num, unit))
            except:
                pass
    
    return sorted(list(set(numbers)), key=lambda x: x[0], reverse=True)

def save_raw_text(pdf_path, pages, output_dir):
    """保存提取的原始文本到文件"""
    filename = os.path.basename(pdf_path).replace('.pdf', '.json')
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)
    
    return output_path
