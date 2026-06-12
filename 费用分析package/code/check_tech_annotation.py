import json

with open('../data/361_mda_annotations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 检查'技术成本'标注的原文，看是否真的是在讨论成本
print('361度 - 标注为"技术成本"的段落中，包含"成本"/"费用"/"支出"的比例:')
cost_keywords = ['成本', '费用', '支出', '投入']
tech_paras = []
for para in data.get('annotated_paragraphs', []):
    annotations = para.get('annotations', {})
    if '技术成本' in annotations.get('expense_types', []):
        text = para.get('original_text', '')
        has_cost = any(kw in text for kw in cost_keywords)
        tech_paras.append((text[:100], has_cost))

print(f'总段落数: {len(tech_paras)}')
print(f'明确提及成本/费用/支出的: {sum(1 for _, has in tech_paras if has)}')
print(f'未明确提及成本的: {sum(1 for _, has in tech_paras if not has)}')

print('\n未明确提及成本的样例:')
count = 0
for text, has in tech_paras:
    if not has and count < 5:
        print(f'  - {text}...')
        count += 1
