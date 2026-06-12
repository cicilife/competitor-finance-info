import os, re
base = r'c:\Users\CICI\Documents\trae_projects\competitor_finance_info\网页报告'
files = ['Section 1-项目回顾.html', 'Section 2-运动品牌财务报告.html',
         'Section 3-重点品牌财报信息Highlight.html', 'Section 4-分析师的Alpha.html']
print('SECTION ORDER:')
for f in files:
    p = os.path.join(base, f)
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as fh:
            html = fh.read()
        title = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
        has_topnav = 'topnav-link' in html
        active = re.findall(r'class="topnav-link active">([^<]+)<', html)
        print(f'  OK {f}')
        print(f'     title: {title.group(1) if title else "?"}')
        print(f'     topnav present: {has_topnav} | active: {active}')
    else:
        print(f'  MISSING: {f}')
print()
old3 = os.path.join(base, 'Section 3-分析师的Alpha.html')
print('OLD Section 3 removed:', not os.path.exists(old3))
