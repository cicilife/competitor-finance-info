import re, os
base = r'c:\Users\CICI\Documents\trae_projects\competitor_finance_info\网页报告'
files = ['Section 1-项目回顾.html', 'Section 2-运动品牌财务报告.html',
         'Section 3-分析师的Alpha.html', '重点品牌财报信息Highlight.html']
for f in files:
    p = os.path.join(base, f)
    if not os.path.exists(p):
        print(f'NOT FOUND: {f}')
        continue
    with open(p, 'r', encoding='utf-8') as fh:
        html = fh.read()
    title = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    has_topnav = ('topnav' in html) or ('page-nav' in html)
    body_start = html.find('<body>')
    print(f'=== {f} ===')
    print(f'  title: {title.group(1) if title else "?"}')
    print(f'  has topnav mention: {has_topnav}')
    snippet = html[body_start:body_start+200]
    print(f'  body snippet: {snippet[:150]!r}')
    print()
