import json

with open('../data/nike_mda_annotations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("annotation_summary keys:", data.get('annotation_summary', {}).keys())
print("\ndriver_factors in summary:", data.get('annotation_summary', {}).get('driver_factors', 'NOT FOUND'))

# 检查annotated_paragraphs里的结构
if data.get('annotated_paragraphs'):
    para = data['annotated_paragraphs'][0]
    print("\n第一个段落annotations keys:", para.get('annotations', {}).keys())
    print("driver_factors in para annotations:", para.get('annotations', {}).get('driver_factors', 'NOT FOUND'))
