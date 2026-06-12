import json

with open('../data/anta_mda_annotations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 检查安踏 标注为"技术成本"的段落
print('安踏 - 标注为"技术成本"的段落（原始22条）:')
cost_keywords = ['成本', '费用', '支出', '投入', 'expense', 'cost', 'spending']

count = 0
for para in data.get('annotated_paragraphs', []):
    annotations = para.get('annotations', {})
    if '技术成本' in annotations.get('expense_types', []):
        text = para.get('original_text', '')
        has_cost = any(kw in text for kw in cost_keywords)
        if not has_cost:
            count += 1
            if count <= 5:
                print(f'\n{count}. [无费用词] {text[:150]}...')
        else:
            print(f'\n{count}. [有费用词] {text[:150]}...')

print(f'\n\n总结: 无费用关键词的段落: {count} 条')
