SRC = r'c:\Users\CICI\Documents\trae_projects\competitor_finance_info\网页报告\Section 2-运动品牌财务报告.html'
with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

# ============= A) 修 2 个 h2（文件用 & 不是 &amp;） =============
fixes_h2 = [
    ('<h2>4. 安踏 & 361° 经营费用细分</h2>',       '<h2>3.1 安踏 & 361° 经营费用细分</h2>'),
    ('<h2>6. 安踏 & 361° 财报文本情感分析</h2>',    '<h2>3.3 安踏 & 361° 财报文本情感分析</h2>'),
]
for old, new in fixes_h2:
    if old in html:
        html = html.replace(old, new)
        print(f'  h2 fixed: {old[:40]}')
    else:
        print(f'  NOT FOUND: {old[:40]}')

# ============= B) 修 meta nav 文字 + 顺序 =============
# 当前（错位）：
#   sec-2-1 -> 2.1 品牌营收气泡图
#   sec-2-2 -> 2.2 重点品牌 Highlight
#   sec-2-3 -> 2.3 品牌盈利情况
#   sec-3-1 -> 4. 安踏 & 361° 经营费用细分   ← 错
#   sec-3-2 -> 3.2 费用与驱动因素文本分析
#   sec-3-3 -> 6. 安踏 & 361° 财报文本情感分析 ← 错
#   sec-4   -> 4. 综合报告下载

# 先修 2 个文字
fixes_text = [
    ('>4. 安踏 & 361° 经营费用细分<',    '>3.1 安踏 & 361° 经营费用细分<'),
    ('>6. 安踏 & 361° 财报文本情感分析<', '>3.3 安踏 & 361° 财报文本情感分析<'),
]
for old, new in fixes_text:
    if old in html:
        html = html.replace(old, new)
        print(f'  text fixed: {old[:40]}')

# 再修顺序：2.1, 2.3, 2.2 而不是 2.1, 2.2, 2.3
# 当前块:
#       <a href="#sec-2-1">2.1 品牌营收气泡图</a>
#       <a href="#sec-2-2">2.2 重点品牌 Highlight</a>
#       <a href="#sec-2-3">2.3 品牌盈利情况</a>
# 目标:
#       <a href="#sec-2-1">2.1 品牌营收气泡图</a>
#       <a href="#sec-2-3">2.3 品牌盈利情况</a>
#       <a href="#sec-2-2">2.2 重点品牌 Highlight</a>
old_block = '''      <a href="#sec-2-1">2.1 品牌营收气泡图</a>
      <a href="#sec-2-2">2.2 重点品牌 Highlight</a>
      <a href="#sec-2-3">2.3 品牌盈利情况</a>'''
new_block = '''      <a href="#sec-2-1">2.1 品牌营收气泡图</a>
      <a href="#sec-2-3">2.3 品牌盈利情况</a>
      <a href="#sec-2-2">2.2 重点品牌 Highlight</a>'''
if old_block in html:
    html = html.replace(old_block, new_block)
    print('  meta nav reordered 2.1 -> 2.3 -> 2.2')
else:
    print('  WARN: meta nav block not found')

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'WRITTEN: {len(html)} bytes')
