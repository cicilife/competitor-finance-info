import os, re
p = r'c:\Users\CICI\Documents\trae_projects\competitor_finance_info\网页报告'
files = ['Section 1-项目回顾.html', 'Section 2-运动品牌财务报告.html',
         'Section 3-分析师的Alpha.html', '国际品牌财报大通盘_可编辑.html',
         '国内品牌财报情感分析_可编辑.html', '运动品牌财务报告_气泡图.html']
for f in files:
    full = os.path.join(p, f)
    if not os.path.exists(full):
        print(f'{f}: 不存在')
        continue
    with open(full, 'r', encoding='utf-8') as fh:
        content = fh.read()
    kws = ['sec-7', '综合报告', '信息图', '2024-2025', '2026纺织', 'sec-6', 'sec-5']
    hits = [kw for kw in kws if kw in content]
    cards = re.findall(r'class="card"', content)
    print(f'{f}:')
    print(f'  size: {os.path.getsize(full)}, cards: {len(cards)}')
    print(f'  contains: {hits}')
