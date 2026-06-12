import re
with open('网页报告/Section 2-运动品牌财务报告.html', 'r', encoding='utf-8') as f:
    html = f.read()

ids = re.findall(r'<div class="card" id="(sec-[\d\-]+)">', html)
print('section ids in order:', ids)

h2s = re.findall(r'<h2[^>]*>([^<]+)', html)
print('h2 in order:')
for i, h in enumerate(h2s):
    print(f'  {i+1}. {h.strip()}')

metas = re.findall(r'<a href="#(sec-[\d\-]+)">([^<]+)</a>', html)
print('meta nav:')
for sid, txt in metas:
    print(f'  {sid} -> {txt}')

# Check group dividers
print('group dividers:', len(re.findall(r'class="group-divider', html)))

# Check group titles
print('group titles:', re.findall(r'<h2 class="group-title">([^<]+)</h2>', html))
