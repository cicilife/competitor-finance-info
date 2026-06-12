import json

with open('../data/anta_mda_annotations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 检查安踏被标为"营销费用"的段落
MARKETING_KWS = ['marketing', 'advertising', 'promotion', 'campaign', 'brand building', '营销', '市场推广', '广告', '推广', '宣传', '促销']
COST_KWS = ['cost', 'expense', 'spending', 'budget', '投入', '投资', '支出', '费用', '开支', '成本', '加大', '加强', '强化', '深化', '建设', '增加', '增长', '提高', '扩充', '扩展']

marketing_paras = []
for para in data.get('annotated_paragraphs', []):
    annotations = para.get('annotations', {})
    if '营销费用' in annotations.get('expense_types', []):
        text = para.get('original_text', '')
        has_mkt = any(kw.lower() in text.lower() for kw in MARKETING_KWS)
        has_cost = any(kw.lower() in text.lower() for kw in COST_KWS)
        marketing_paras.append((text[:100], has_mkt, has_cost))

print(f'安踏"营销费用"标注段落共 {len(marketing_paras)} 条\n')
print('通过验证的段落（有营销词+有费用词）:')
count = 0
for text, has_mkt, has_cost in marketing_paras:
    if has_mkt and has_cost:
        count += 1
        print(f'\n{count}. {text}...')

print(f'\n\n通过验证: {count}/{len(marketing_paras)}')

print('\n\n未通过验证的段落样例:')
not_passed = [(t, h) for t, hm, h in marketing_paras if not (hm and h)]
for i, (text, has_cost) in enumerate(not_passed[:5]):
    print(f'{i+1}. {text}...')
