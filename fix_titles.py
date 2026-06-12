import re
SRC = r'c:\Users\CICI\Documents\trae_projects\competitor_finance_info\网页报告\Section 2-运动品牌财务报告.html'
with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

# ============= 修正 1: h2 标题 =============
title_replacements = [
    ('<h2>2. 品牌营收表现</h2>',                                                  '<h2>2.1 品牌营收气泡图</h2>'),
    ('<h2>2.5 重点品牌财报信息 <span',                                            '<h2>2.2 重点品牌财报信息Highlight <span'),
    ('<h2>3. 品牌盈利情况</h2>',                                                  '<h2>2.3 品牌盈利情况</h2>'),
    ('<h2>4. 安踏 &amp; 361° 经营费用细分</h2>',                                  '<h2>3.1 安踏 &amp; 361° 经营费用细分</h2>'),
    ('<h2>5. 费用与驱动因素文本分析</h2>',                                        '<h2>3.2 费用与驱动因素文本分析</h2>'),
    ('<h2>6. 安踏 &amp; 361° 财报文本情感分析</h2>',                              '<h2>3.3 安踏 &amp; 361° 财报文本情感分析</h2>'),
    ('<h2>7. 综合报告 · 行业分析</h2>',                                           '<h2>4. 综合报告下载</h2>'),
]
for old, new in title_replacements:
    if old in html:
        html = html.replace(old, new)
        print(f'  replaced h2: {old[:40]}...')
    else:
        print(f'  NOT FOUND h2: {old[:40]}...')

# ============= 修正 2: hero meta nav 文本 + 顺序 =============
# 当前 meta nav 内容 (从 verify3 看到):
#   sec-1 -> 1. 行业趋势
#   sec-2-1 -> 2. 品牌营收气泡图
#   sec-2-2 -> 2.5 重点品牌 Highlight
#   sec-2-3 -> 3. 品牌盈利情况
#   sec-3-1 -> 4. 安踏 & 361° 经营费用细分
#   sec-3-2 -> 5. 费用与驱动因素文本分析
#   sec-3-3 -> 6. 安踏 & 361° 财报文本情感分析
#   sec-4 -> 7. 综合报告 · 行业分析
# 目标顺序: 1 → 2.1 → 2.3 → 2.2 → 3.1 → 3.2 → 3.3 → 4

# 先更新文本
text_replacements = [
    ('>2. 品牌营收气泡图<',     '>2.1 品牌营收气泡图<'),
    ('>2.5 重点品牌 Highlight<', '>2.2 重点品牌 Highlight<'),
    ('>3. 品牌盈利情况<',       '>2.3 品牌盈利情况<'),
    ('>4. 安踏 &amp; 361° 经营费用细分<', '>3.1 安踏 &amp; 361° 经营费用细分<'),
    ('>5. 费用与驱动因素文本分析<', '>3.2 费用与驱动因素文本分析<'),
    ('>6. 安踏 &amp; 361° 财报文本情感分析<', '>3.3 安踏 &amp; 361° 财报文本情感分析<'),
    ('>7. 综合报告 · 行业分析<', '>4. 综合报告下载<'),
]
for old, new in text_replacements:
    html = html.replace(old, new)
    print(f'  text replaced: {old[:30]}...')

# 重新排序 meta nav - 用最稳的方式：整块替换
old_meta = '''      <a href="#sec-1">1. 行业趋势</a>
      <a href="#sec-2-1">2.1 品牌营收气泡图</a>
      <a href="#sec-2-2">2.2 重点品牌 Highlight</a>
      <a href="#sec-2-3">2.3 品牌盈利情况</a>
      <a href="#sec-3-1">3.1 安踏 &amp; 361° 经营费用细分</a>
      <a href="#sec-3-2">3.2 费用与驱动因素文本分析</a>
      <a href="#sec-3-3">3.3 安踏 &amp; 361° 财报文本情感分析</a>
      <a href="#sec-4">4. 综合报告下载</a>'''
new_meta = '''      <a href="#sec-1">1. 行业趋势</a>
      <a href="#sec-2-1">2.1 品牌营收气泡图</a>
      <a href="#sec-2-3">2.3 品牌盈利情况</a>
      <a href="#sec-2-2">2.2 重点品牌 Highlight</a>
      <a href="#sec-3-1">3.1 安踏 &amp; 361° 经营费用细分</a>
      <a href="#sec-3-2">3.2 费用与驱动因素文本分析</a>
      <a href="#sec-3-3">3.3 安踏 &amp; 361° 财报文本情感分析</a>
      <a href="#sec-4">4. 综合报告下载</a>'''
if old_meta in html:
    html = html.replace(old_meta, new_meta)
    print('  meta nav reordered (1->2.1->2.3->2.2->3.1->3.2->3.3->4)')
else:
    print('  WARN: meta nav block not found verbatim, doing fuzzy')
    # 简单办法：用 href 唯一性 + 在原位置用更长的标识替换顺序
    # 实际上 fuzzy 替换已经更新了文本，重新排序需要更复杂处理

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'WRITTEN: {len(html)} bytes')
