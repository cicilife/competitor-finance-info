import json

with open('../data/nike_mda_annotations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('Nike - 标注为"技术成本"的段落分析:')
cost_keywords = ['cost', 'expense', 'spending', '费用', '成本', '支出', '投入']
tech_paras = []
for para in data.get('annotated_paragraphs', []):
    annotations = para.get('annotations', {})
    if '技术成本' in annotations.get('expense_types', []):
        text = para.get('original_text', '')
        has_cost = any(kw.lower() in text.lower() for kw in cost_keywords)
        tech_paras.append((text[:100], has_cost))

print(f'总段落数: {len(tech_paras)}')
print(f'明确提及成本/费用/支出的: {sum(1 for _, has in tech_paras if has)}')
print(f'未明确提及成本的: {sum(1 for _, has in tech_paras if not has)}')

print('\n未明确提及成本的样例 (前5条):')
count = 0
for text, has in tech_paras:
    if not has and count < 5:
        print(f'  - {text}...')
        count += 1
