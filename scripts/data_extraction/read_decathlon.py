import sys

sys.stdout.reconfigure(encoding='utf-8')

# 迪卡侬HTML文件
with open(r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\Decathlon迪卡侬\Decathlon Group's 2024 Performance.html", 'r', encoding='utf-8') as f:
    content = f.read()

# 查找关键数据
import re

# 查找含"billion"或"million"或"€"的数据
for kw in ['revenue', 'profit', 'sales', '€', 'billion', 'million', 'EBIT', 'operating']:
    for match in re.finditer(rf'.{{0,100}}{kw}.{{0,100}}', content, re.IGNORECASE):
        print(match.group(0).strip())
        print('---')