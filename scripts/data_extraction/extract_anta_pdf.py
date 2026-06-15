# -*- coding: utf-8 -*-
import pdfplumber
import os

pdf_path = r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\安踏体育\安踏体育：二零二四年年报.pdf'
out_path = r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\anta_pages_1_30.txt'

with open(out_path, 'w', encoding='utf-8') as out:
    with pdfplumber.open(pdf_path) as pdf:
        out.write(f'Total pages: {len(pdf.pages)}\n')
        for i in range(min(30, len(pdf.pages))):
            text = pdf.pages[i].extract_text()
            out.write(f'\n--- Page {i+1} ---\n')
            if text:
                out.write(text)
            else:
                out.write('No text extracted')
print('Done')