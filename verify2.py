import os
base = r'c:\Users\CICI\Documents\trae_projects\competitor_finance_info\网页报告'
files = ['Section 1-项目回顾.html', 'Section 2-运动品牌财务报告.html',
         'Section 3-分析师的Alpha.html', 'Section 3-重点品牌财报信息Highlight.html']
for f in files:
    p = os.path.join(base, f)
    if os.path.exists(p):
        print(f'  EXISTS: {f} ({os.path.getsize(p)} bytes)')
    else:
        print(f'  GONE:   {f}')
print()
with open(os.path.join(base, 'Section 2-运动品牌财务报告.html'), 'r', encoding='utf-8') as fh:
    s2 = fh.read()
print('Section 2 has sec-2-5:', 'id="sec-2-5"' in s2)
print('Section 2 has topnav:', 'class="topnav"' in s2)
print('Section 2 has highlight CSS:', '.highlight-card' in s2)
print('Section 2 has 9 highlight cards:', s2.count('highlight-card tone-'))
print('Section 2 has Highlight link in nav:', 'href="#sec-2-5"' in s2)
