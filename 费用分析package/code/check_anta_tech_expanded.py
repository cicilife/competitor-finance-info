import json

with open('../data/anta_mda_annotations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 重新检查安踏被标为"技术成本"的段落
TECH_KEYWORDS = ['technology', 'tech', 'digital', 'it', 'software', 'cloud', 'ai', 'data', '系统', '平台', '技术', '科技', '数字化', '信息化', 'ai']
COST_KEYWORDS = ['investment', 'invest', 'spending', 'expense', 'cost', 'budget', 'allocation', '投入', '投资', '支出', '费用', '开支', '成本', '研发', '创新']

tech_paras = []
for para in data.get('annotated_paragraphs', []):
    annotations = para.get('annotations', {})
    if '技术成本' in annotations.get('expense_types', []):
        text = para.get('original_text', '')
        has_tech = any(tech in text.lower() for tech in [k.lower() for k in TECH_KEYWORDS])
        has_cost = any(cost in text.lower() for cost in [k.lower() for k in COST_KEYWORDS])
        tech_paras.append((text[:120], has_tech, has_cost))

print(f'安踏"技术成本"标注段落共 {len(tech_paras)} 条\n')
print('同时有技术词+费用词的段落:')
count = 0
for text, has_tech, has_cost in tech_paras:
    if has_tech and has_cost:
        count += 1
        if count <= 5:
            print(f'\n{count}. {text}...')

print(f'\n符合扩展定义的段落: {count}/{len(tech_paras)}')
