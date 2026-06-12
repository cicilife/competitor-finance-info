import os, re, shutil

BASE = r'c:\Users\CICI\Documents\trae_projects\competitor_finance_info\网页报告'
SRC  = os.path.join(BASE, '重点品牌财报信息Highlight.html')
OLD3 = os.path.join(BASE, 'Section 3-分析师的Alpha.html')
NEW3 = os.path.join(BASE, 'Section 3-重点品牌财报信息Highlight.html')
NEW4 = os.path.join(BASE, 'Section 4-分析师的Alpha.html')

# ============= 统一顶导 HTML / CSS =============
TOPNAV_CSS = """
/* ============= 顶部跨页导航 ============= */
.topnav {
  position: sticky; top: 0; z-index: 9999;
  background: rgba(255,255,255,0.96);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #e5e7eb;
  padding: 10px 28px;
  display: flex; gap: 4px; align-items: center;
  font-family: "Noto Sans SC", "Inter", -apple-system, "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
  font-size: 13.5px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.topnav-brand {
  font-weight: 800; color: #0E2A4A; text-decoration: none;
  margin-right: 14px; padding: 6px 0;
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 14.5px;
  letter-spacing: 0.3px;
}
.topnav-brand .brand-dot {
  display: inline-block; width: 8px; height: 8px; border-radius: 50%;
  background: linear-gradient(135deg, #1d4ed8, #06b6d4);
}
.topnav-link {
  color: #4b5563; text-decoration: none;
  padding: 7px 14px; border-radius: 6px;
  transition: all 0.15s; font-weight: 500;
}
.topnav-link:hover { background: #f1f5f9; color: #0E2A4A; }
.topnav-link.active {
  background: linear-gradient(135deg, #0E2A4A 0%, #1d4ed8 100%);
  color: #fff !important; font-weight: 600;
  box-shadow: 0 2px 6px rgba(14,42,74,0.25);
}
.topnav-spacer { flex: 1; }
.topnav-meta { font-size: 11.5px; color: #94a3b8; padding: 0 10px; }
"""

TOPNAV_HTML = """
<!-- ============= 顶部跨页导航 ============= -->
<nav class="topnav">
  <a href="Section 1-项目回顾.html" class="topnav-brand"><span class="brand-dot"></span>运动品牌财报研究</a>
  <a href="Section 1-项目回顾.html" class="topnav-link ACTIVE_1">1 · 项目回顾</a>
  <a href="Section 2-运动品牌财务报告.html" class="topnav-link ACTIVE_2">2 · 运动品牌财务报告</a>
  <a href="Section 3-重点品牌财报信息Highlight.html" class="topnav-link ACTIVE_3">3 · 重点品牌财报信息Highlight</a>
  <a href="Section 4-分析师的Alpha.html" class="topnav-link ACTIVE_4">4 · 分析师的Alpha</a>
  <span class="topnav-spacer"></span>
  <span class="topnav-meta">PAGEMETA</span>
</nav>
"""

def make_topnav(active_n, meta=''):
    """active_n: 1/2/3/4"""
    html = TOPNAV_HTML
    for n in (1, 2, 3, 4):
        if n == active_n:
            html = html.replace(f'ACTIVE_{n}', 'active')
        else:
            html = html.replace(f'ACTIVE_{n}', '')
    return html.replace('PAGEMETA', meta)

# ============= Step 1: 从源文件创建 Section 3 =============
with open(SRC, 'r', encoding='utf-8') as f:
    src = f.read()

new3 = src
# 替换标题
new3 = new3.replace(
    '<title>2024-2025 国际品牌财报大盘点（中国市场）· 可编辑信息图</title>',
    '<title>重点品牌财报信息Highlight · Section 03</title>'
)
# 替换 h1 标题文字
new3 = new3.replace(
    '<h1 contenteditable="true">2024-2025 国际品牌财报大盘点 · <span class="accent-red">中国市场</span>：<span class="q">增长分化，谁在突围？</span></h1>',
    '<h1 contenteditable="true">重点品牌财报信息 <span class="accent-red">Highlight</span>：<span class="q">增长分化，谁在突围？</span></h1>'
)
# 删掉工具条
new3 = re.sub(r'<!-- 工具条 -->\s*<div class="toolbar">.*?</div>\s*</div>\s*', '', new3, flags=re.DOTALL)
# 注入 topnav CSS（追加到 </style> 之前）
new3 = new3.replace('</style>', TOPNAV_CSS + '\n</style>')
# 在 <body> 之后注入顶导
new3 = new3.replace('<body>\n', '<body>\n' + make_topnav(3, 'FY2024-2025 · 中国市场') + '\n', 1)

with open(NEW3, 'w', encoding='utf-8') as f:
    f.write(new3)
print(f'CREATED: {NEW3} ({os.path.getsize(NEW3)} bytes)')

# ============= Step 2: 重命名 Section 3 → Section 4 =============
if os.path.exists(OLD3):
    if os.path.exists(NEW4):
        os.remove(NEW4)
    shutil.move(OLD3, NEW4)
    print(f'RENAMED: {OLD3} → {NEW4}')
else:
    print(f'NOT FOUND: {OLD3}')

# ============= Step 3: 给 Section 1 / 2 / 4 注入顶导 =============
targets = [
    (os.path.join(BASE, 'Section 1-项目回顾.html'),   1, 'Section 01 · Decathlon'),
    (os.path.join(BASE, 'Section 2-运动品牌财务报告.html'), 2, 'Section 02 · 25+ 品牌综合'),
    (os.path.join(BASE, 'Section 4-分析师的Alpha.html'),    4, 'Section 04 · 阿尔法 α'),
]
for path, n, meta in targets:
    if not os.path.exists(path):
        print(f'NOT FOUND: {path}')
        continue
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    if 'class="topnav"' in html:
        print(f'SKIP (already has topnav): {path}')
        continue
    # 注入 CSS 到 </style> 前
    if '</style>' in html:
        html = html.replace('</style>', TOPNAV_CSS + '\n</style>', 1)
    # 注入 HTML 到 <body> 后
    if '<body>' in html:
        html = html.replace('<body>', '<body>\n' + make_topnav(n, meta) + '\n', 1)
    elif '<body' in html:
        html = re.sub(r'(<body[^>]*>)', r'\1\n' + make_topnav(n, meta) + '\n', html, count=1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'UPDATED: {os.path.basename(path)} ({os.path.getsize(path)} bytes)')

print('DONE')
