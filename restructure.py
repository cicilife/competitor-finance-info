import os, re, json

BASE = r'c:\Users\CICI\Documents\trae_projects\competitor_finance_info\网页报告'
SRC  = os.path.join(BASE, 'Section 2-运动品牌财务报告.html')

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

# ============= 1) 8 个 section 切分 =============
# 每个 section 从 <div class="card" id="sec-X"> 开始，到下一个 <div class="card" 之前结束
card_pat = re.compile(r'<div class="card" id="(sec-[\d\-]+)">')
positions = [(m.start(), m.end(), m.group(1)) for m in card_pat.finditer(html)]
print('sections found:', [p[2] for p in positions])

# 切出每个 section 字符串（从 div 开始到下一段 div 之前）
sections = {}
for i, (s, e, sid) in enumerate(positions):
    end = positions[i+1][0] if i + 1 < len(positions) else html.find('\n</div>\n', s)
    # 末尾要把这个 card 的 </div> 也包含
    # 找最近的 "\n  </div>\n" 或 "\n</div>\n" 之后
    chunk = html[s:end]
    sections[sid] = chunk

# ============= 2) 重新编号映射 =============
# 当前 id -> 新 id
id_map = {
    'sec-1':   'sec-1',
    'sec-2':   'sec-2-1',
    'sec-3':   'sec-2-3',
    'sec-2-5': 'sec-2-2',
    'sec-4':   'sec-3-1',
    'sec-5':   'sec-3-2',
    'sec-6':   'sec-3-3',
    'sec-7':   'sec-4',
}
# 当前 h2 文本前缀 -> 新 h2 文本
title_map = [
    # 严格匹配整段 h2
    ('<h2>1. 行业趋势</h2>',                                                     '<h2>1. 行业趋势</h2>'),
    ('<h2>2. 品牌营收表现</h2>',                                                 '<h2>2.1 品牌营收气泡图</h2>'),
    ('<h2>2.5 重点品牌财报信息 <span',                                            '<h2>2.2 重点品牌财报信息Highlight <span'),
    ('<h2>3. 品牌盈利情况</h2>',                                                 '<h2>2.3 品牌盈利情况</h2>'),
    ('<h2>4. 安踏 &amp; 361° 经营费用细分</h2>',                                 '<h2>3.1 安踏 &amp; 361° 经营费用细分</h2>'),
    ('<h2>5. 费用与驱动因素文本分析</h2>',                                       '<h2>3.2 费用与驱动因素文本分析</h2>'),
    ('<h2>6. 安踏 &amp; 361° 财报文本情感分析</h2>',                             '<h2>3.3 安踏 &amp; 361° 财报文本情感分析</h2>'),
    ('<h2>7. 综合报告 · 行业分析</h2>',                                          '<h2>4. 综合报告下载</h2>'),
]

# ============= 3) 在每个 section 字符串内做替换 =============
def renumber_section(chunk, old_id, new_id):
    c = chunk
    if old_id == new_id:
        return c
    c = c.replace(f'id="{old_id}"', f'id="{new_id}"')
    return c

new_sections = {}
for old_id, chunk in sections.items():
    new_id = id_map[old_id]
    c = renumber_section(chunk, old_id, new_id)
    new_sections[new_id] = c

# ============= 4) 标题替换（在所有 section 上统一做） =============
all_html = '\n'.join(new_sections.values())
for old_h2, new_h2 in title_map:
    all_html = all_html.replace(old_h2, new_h2)
# meta 导航中旧的链接文字 "2. 品牌营收气泡图" → "2.1 品牌营收气泡图" 等
all_html = all_html.replace('>2. 品牌营收气泡图<', '>2.1 品牌营收气泡图<')
all_html = all_html.replace('>2.5 重点品牌 Highlight<', '>2.2 重点品牌 Highlight<')
all_html = all_html.replace('>3. 品牌盈利情况<', '>2.3 品牌盈利情况<')
all_html = all_html.replace('>4. 安踏 &amp; 361° 经营费用细分<', '>3.1 安踏 &amp; 361° 经营费用细分<')
all_html = all_html.replace('>5. 费用与驱动因素文本分析<', '>3.2 费用与驱动因素文本分析<')
all_html = all_html.replace('>6. 安踏 &amp; 361° 财报文本情感分析<', '>3.3 安踏 &amp; 361° 财报文本情感分析<')
all_html = all_html.replace('>7. 综合报告 · 行业分析<', '>4. 综合报告下载<')

# ============= 5) 重新排序 =============
# 目标顺序：sec-1, sec-2-1, sec-2-3, sec-2-2, sec-3-1, sec-3-2, sec-3-3, sec-4
order = ['sec-1', 'sec-2-1', 'sec-2-3', 'sec-2-2', 'sec-3-1', 'sec-3-2', 'sec-3-3', 'sec-4']

# 但 all_html 是 \n 拼接的，没法按 section 拆分 — 重新构造
ordered_chunks = []
for new_id in order:
    ordered_chunks.append(new_sections[new_id])

# 在 sec-2-1 之前插入组头 "2. 品牌重点财务指标"
group_header_2 = (
    '\n  <!-- ============= 2. 品牌重点财务指标 · 分组 ============= -->\n'
    '  <div class="group-divider group-blue">\n'
    '    <h2 class="group-title">2. 品牌重点财务指标</h2>\n'
    '    <span class="group-subtitle">Brand Key Financial Metrics · 营收 · 盈利 · Highlight</span>\n'
    '  </div>\n'
)
# 在 sec-3-1 之前插入组头 "3. 经营费用细探"
group_header_3 = (
    '\n  <!-- ============= 3. 经营费用细探 · 分组 ============= -->\n'
    '  <div class="group-divider group-orange">\n'
    '    <h2 class="group-title">3. 经营费用细探</h2>\n'
    '    <span class="group-subtitle">Operating Expense Deep Dive · 费用细分 · 文本分析 · 情感分析</span>\n'
    '  </div>\n'
)

# 重新组装（带组头）
final_sections = []
for new_id in order:
    if new_id == 'sec-2-1':
        final_sections.append(group_header_2)
    if new_id == 'sec-3-1':
        final_sections.append(group_header_3)
    final_sections.append(new_sections[new_id])

# ============= 6) 提取 hero（前段）+ 尾巴（hoverPanel + script） =============
# hero: 从头到第一个 <div class="card" id="sec-1"> 之前
first_card_start = positions[0][0]
hero_html = html[:first_card_start]

# 尾巴：从最后一个 section 结束到文件末尾
# 找最后一个 </div>（关闭 page）之后
last_section_end_in_html = positions[-1][0]
# 找从 last_section_end 之后到 hoverPanel / script 的部分
tail_marker = '\n<div id="hoverPanel">'
tail_pos = html.find(tail_marker, last_section_end_in_html)
if tail_pos == -1:
    tail_pos = html.find('<div id="hoverPanel">', last_section_end_in_html)
if tail_pos == -1:
    # 取最后 section 结束到文件末尾
    tail_html = ''
else:
    tail_html = html[tail_pos:]

# ============= 7) 重新拼装 =============
new_html = hero_html + '\n'.join(final_sections) + tail_html

# ============= 8) 更新 hero meta 导航（替换旧链接） =============
old_meta = '''      <a href="#sec-1">1. 行业趋势</a>
      <a href="#sec-2">2. 品牌营收气泡图</a>
      <a href="#sec-2-5">2.5 重点品牌 Highlight</a>
      <a href="#sec-3">3. 品牌盈利情况</a>
      <a href="#sec-4">4. 安踏 &amp; 361° 经营费用细分</a>
      <a href="#sec-5">5. 费用与驱动因素文本分析</a>
      <a href="#sec-6">6. 安踏 &amp; 361° 财报文本情感分析</a>
      <a href="#sec-7">7. 综合报告 · 行业分析</a>'''
new_meta = '''      <a href="#sec-1">1. 行业趋势</a>
      <a href="#sec-2-1">2.1 品牌营收气泡图</a>
      <a href="#sec-2-3">2.3 品牌盈利情况</a>
      <a href="#sec-2-2">2.2 重点品牌 Highlight</a>
      <a href="#sec-3-1">3.1 安踏 &amp; 361° 经营费用细分</a>
      <a href="#sec-3-2">3.2 费用与驱动因素文本分析</a>
      <a href="#sec-3-3">3.3 安踏 &amp; 361° 财报文本情感分析</a>
      <a href="#sec-4">4. 综合报告下载</a>'''
if old_meta in new_html:
    new_html = new_html.replace(old_meta, new_meta)
    print('meta nav updated')
else:
    print('WARN: meta nav not matched, trying fuzzy...')
    # fuzzy: replace href values only
    replacements = [
        ('href="#sec-2"', 'href="#sec-2-1"'),
        ('href="#sec-2-5"', 'href="#sec-2-2"'),
        ('href="#sec-3"', 'href="#sec-2-3"'),
        ('href="#sec-4"', 'href="#sec-3-1"'),
        ('href="#sec-5"', 'href="#sec-3-2"'),
        ('href="#sec-6"', 'href="#sec-3-3"'),
        ('href="#sec-7"', 'href="#sec-4"'),
    ]
    for old, new in replacements:
        new_html = new_html.replace(old, new)
    # 注意：这种全局替换会影响其他地方的引用（good，保留）

# ============= 9) JS getElementById / querySelector 引用 =============
# 已通过 #8 中的 href 替换顺带处理了一部分。检查是否还有遗漏
js_id_replacements = [
    ("getElementById('sec-2')",   "getElementById('sec-2-1')"),
    ("getElementById('sec-2-5')", "getElementById('sec-2-2')"),
    ("getElementById('sec-3')",   "getElementById('sec-2-3')"),
    ("getElementById('sec-4')",   "getElementById('sec-3-1')"),
    ("getElementById('sec-5')",   "getElementById('sec-3-2')"),
    ("getElementById('sec-6')",   "getElementById('sec-3-3')"),
    ("getElementById('sec-7')",   "getElementById('sec-4')"),
    ('getElementById("sec-2")',   'getElementById("sec-2-1")'),
    ('getElementById("sec-2-5")', 'getElementById("sec-2-2")'),
    ('getElementById("sec-3")',   'getElementById("sec-2-3")'),
    ('getElementById("sec-4")',   'getElementById("sec-3-1")'),
    ('getElementById("sec-5")',   'getElementById("sec-3-2")'),
    ('getElementById("sec-6")',   'getElementById("sec-3-3")'),
    ('getElementById("sec-7")',   'getElementById("sec-4")'),
]
for old, new in js_id_replacements:
    new_html = new_html.replace(old, new)

# ============= 10) 写入 =============
with open(SRC, 'w', encoding='utf-8') as f:
    f.write(new_html)
print(f'WRITTEN: {os.path.getsize(SRC)} bytes')
