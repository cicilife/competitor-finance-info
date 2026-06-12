import os, re

BASE = r'c:\Users\CICI\Documents\trae_projects\competitor_finance_info\网页报告'

# ============= 顶导移除函数 =============
def remove_topnav_css(html):
    start_marker = '/* ============= 顶部跨页导航 ============= */'
    start = html.find(start_marker)
    if start == -1:
        return html
    end_marker = '.topnav-meta {'
    end_start = html.find(end_marker, start)
    if end_start == -1:
        return html
    i = html.find('{', end_start); brace = 1; i += 1
    while i < len(html) and brace > 0:
        if html[i] == '{': brace += 1
        elif html[i] == '}': brace -= 1
        i += 1
    end = i
    while end < len(html) and html[end] in ' \t\n':
        end += 1
    return html[:start] + html[end:]

def remove_topnav_html(html):
    start_marker = '<!-- ============= 顶部跨页导航 ============= -->'
    start = html.find(start_marker)
    if start == -1:
        return html
    end = html.find('</nav>', start)
    if end == -1:
        return html
    end += len('</nav>')
    while end < len(html) and html[end] in ' \t\n':
        end += 1
    return html[:start] + html[end:]

def revert_topnav(path):
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    if 'class="topnav"' not in html:
        print(f'  skip (no topnav): {os.path.basename(path)}')
        return
    html = remove_topnav_css(html)
    html = remove_topnav_html(html)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  reverted: {os.path.basename(path)} ({os.path.getsize(path)} bytes)')

# ============= Step 1: 还原 Section 1/3/4（去掉顶导） =============
print('--- Revert topnav from Section 1 / 3 / 4 ---')
revert_topnav(os.path.join(BASE, 'Section 1-项目回顾.html'))
revert_topnav(os.path.join(BASE, 'Section 4-分析师的Alpha.html'))  # 先去掉顶导
# 重命名回 Section 3
sec4 = os.path.join(BASE, 'Section 4-分析师的Alpha.html')
sec3 = os.path.join(BASE, 'Section 3-分析师的Alpha.html')
if os.path.exists(sec4):
    if os.path.exists(sec3): os.remove(sec3)
    os.rename(sec4, sec3)
    print(f'  renamed: Section 4-分析师的Alpha.html → Section 3-分析师的Alpha.html')

# ============= Step 2: 删除新建的 Section 3-Highlight（合并到 Section 2） =============
sec3hl = os.path.join(BASE, 'Section 3-重点品牌财报信息Highlight.html')
if os.path.exists(sec3hl):
    os.remove(sec3hl)
    print(f'  deleted: Section 3-重点品牌财报信息Highlight.html')

# ============= Step 3: 还原 Section 2 顶导（不再多页） =============
print('--- Revert topnav from Section 2 ---')
revert_topnav(os.path.join(BASE, 'Section 2-运动品牌财务报告.html'))

print('REVERT DONE')
