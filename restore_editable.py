"""
Fix remaining 14 broken <tag class="> instances.
"""
import re

SRC = r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\网页报告\Section 1-项目回顾.html"

with open(SRC, "r", encoding="utf-8") as f:
    html = f.read()

# P3 3 p blocks
p3_bodies = [
    '理解<strong>运动户外行业</strong>整体发展趋势，建立行业坐标系',
    '如何用技术手段对<strong>数据收集和解析流程</strong>提效',
    '从<strong>财务视角</strong>探索可以助力迪卡侬经营提效的机会',
]
for body in p3_bodies:
    html = html.replace(
        f'<p class=">{body}</p>',
        f'<p class="editable" contenteditable="true">{body}</p>',
        1
    )

# P8 caliber side notes
html = html.replace(
    '<h3 class=">口径说明</h3>',
    '<h3 class="editable" contenteditable="true">口径说明</h3>',
    1
)
html = re.sub(
    r'<span class="><strong>时间口径：</strong>',
    r'<span class="editable" contenteditable="true"><strong>时间口径：</strong>',
    html
)
html = re.sub(
    r'<span class="><strong>区域口径：</strong>',
    r'<span class="editable" contenteditable="true"><strong>区域口径：</strong>',
    html
)
html = re.sub(
    r'<span class="><strong>货币单位：</strong>',
    r'<span class="editable" contenteditable="true"><strong>货币单位：</strong>',
    html
)

# P11 5 lessons
p11_lessons = [
    ('<strong>百万日元</strong> vs <strong>10 亿日元</strong>（×1000 vs ×1,000,000）千万不能混',),
    ('<div>在上一版基础上<span style="color: rgb(0, 102, 204); font-weight: 700;">追加</span></div><div><span style="color: rgb(0, 102, 204); font-weight: 700;"><br></span></div><div><span style="color: rgb(0, 102, 204); font-weight: 700;">刚刚补的2025年数据怎么丢了</span><span style="color: rgb(0, 102, 204); font-weight: 700;"></span></div>',),
    ('<strong>中国内地 &gt; 大中华区 &gt; 亚太区 &gt; TOTAL</strong>',),
    ('要<em>明确标注来自【文件名】【页码】【原文】</em><div><em><br></em></div><div><span style="background-color: rgb(30, 232, 154);">取自表格，记录表名</span><em></em></div>',),
    ('港股用<strong>v1</strong>，美股用v2，欧股用 <b>...</b>',),
]
for (body,) in p11_lessons:
    html = html.replace(
        f'<p class=">{body}</p>',
        f'<p class="editable" contenteditable="true">{body}</p>',
        1
    )

# P12 h3 2
html = html.replace(
    '<h3 class=">运动品牌财务数据源 · 网页版 database</h3>',
    '<h3 class="editable" contenteditable="true">运动品牌财务数据源 · 网页版 database</h3>',
    1
)
html = html.replace(
    '<h3 class=">Section 2 · 运动品牌财务报告</h3>',
    '<h3 class="editable" contenteditable="true">Section 2 · 运动品牌财务报告</h3>',
    1
)

with open(SRC, "w", encoding="utf-8") as f:
    f.write(html)

# 验证破损 class
import subprocess
r1 = subprocess.run(
    ['powershell', '-Command', f"(Select-String -Path '{SRC}' -Pattern 'class=\"' | Where-Object {{ $_.Line -match 'class=\"\\s' -or $_.Line -match 'class=\">' }} | Measure-Object).Count"],
    capture_output=True, text=True
)
print(f"残留破损 class 数: {r1.stdout.strip()}")

r2 = subprocess.run(
    ['powershell', '-Command', f"(Get-Content '{SRC}' | Select-String -Pattern 'editable|contenteditable' | Measure-Object).Count"],
    capture_output=True, text=True
)
print(f"恢复后 editable 引用数: {r2.stdout.strip()}")
