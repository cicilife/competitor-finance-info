
import os
import json
import sys

def read_pdf(pdf_path, include_tables=False):
    """读取PDF文件并提取文本内容"""
    try:
        from pdfminer.high_level import extract_text
        from pdfminer.layout import LAParams
        import pdfplumber
        
        text = extract_text(pdf_path, laparams=LAParams())
        
        if include_tables:
            try:
                tables_data = []
                with pdfplumber.open(pdf_path) as pdf:
                    for i, page in enumerate(pdf.pages):
                        tables = page.extract_tables()
                        if tables:
                            for table in tables:
                                if table:
                                    for row in table:
                                        if row:
                                            tables_data.append({
                                                'page': i + 1,
                                                'data': row
                                            })
                
                pages = []
                for i, line in enumerate(text.split('\n')):
                    tables_on_page = [t for t in tables_data if t['page'] == i + 1]
                    pages.append({
                        'page_num': i + 1,
                        'text': line,
                        'tables': [t['data'] for t in tables_on_page]
                    })
                
                if not pages:
                    pages = [{'page_num': i + 1, 'text': line, 'tables': []} 
                            for i, line in enumerate(text.split('\n'))]
                
                return pages
            except:
                pass
        
        pages = [{'page_num': i + 1, 'text': line, 'tables': []} 
                for i, line in enumerate(text.split('\n'))]
        
        return pages
        
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return []
