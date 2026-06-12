"""
添加ASICS大中华区数据
数据来源: 
- ASICS Integrated Report 2024 (Page 76-77 Financial Summary, Page 30/48 Regional Overview)
- Consolidated Financial Statements and Auditor's Report 2025 (Page 62-65 Segment Information)
"""
import pandas as pd
from datetime import datetime

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

jpy_to_cny = 0.048  # 日元兑人民币汇率

# ============ ASICS大中华区数据 ============
# 来自 ASICS Integrated Report 2024 (FY2023, FY2024)
# Page 76: Financial Summary - By Region
#   Greater China Net Sales: 2024=100,497 百万日元, 2023=77,616 百万日元
#   Greater China Operating Profit: 2024=19,335 百万日元, 2023=13,107 百万日元
# Page 30: Greater China 2024 Operating margin 19.3% (YoY +2.4pp)
# Page 48: Greater China 2024 net sales +29.5%, operating profit +47.5%

# 来自 Consolidated Financial Statements and Auditor's Report 2025 (FY2024, FY2025)
# Page 62: Segment Information FY2024
#   Greater China Sales to customers: ¥100,431 million
#   Greater China Total sales: ¥100,497 million
#   Greater China Segment profit: ¥19,335 million
# Page 63: Segment Information FY2025
#   Greater China Sales to customers: ¥120,236 million
#   Greater China Total sales: ¥120,514 million
#   Greater China Segment profit: ¥25,099 million
# Operating margin FY2025: 25,099/120,236 = 20.9%

asics_gc_data = [
    # FY2025 大中华区
    {
        '报告周期': 'FY2025',
        '指标名称（原始）': 'Net sales - Greater China',
        '数据值': 120236,
        '单位': '百万日元',
        '原文摘录': 'Greater China Sales to customers ¥120,236 million (FY2025)',
        'source_file': "Consolidated Financial Statements and Auditor's Report 2025.pdf",
        'page': 63,
    },
    {
        '报告周期': 'FY2025',
        '指标名称（原始）': 'Operating profit - Greater China',
        '数据值': 25099,
        '单位': '百万日元',
        '原文摘录': 'Greater China Segment profit ¥25,099 million (FY2025)',
        'source_file': "Consolidated Financial Statements and Auditor's Report 2025.pdf",
        'page': 63,
    },
    {
        '报告周期': 'FY2025',
        '指标名称（原始）': 'Operating margin - Greater China',
        '数据值': 20.9,
        '单位': '%',
        '原文摘录': 'Greater China Operating margin 20.9% (FY2025: 25,099/120,236)',
        'source_file': "Consolidated Financial Statements and Auditor's Report 2025.pdf",
        'page': 63,
    },
    # FY2024 大中华区
    {
        '报告周期': 'FY2024',
        '指标名称（原始）': 'Net sales - Greater China',
        '数据值': 100497,
        '单位': '百万日元',
        '原文摘录': 'Greater China Total sales ¥100,497 million (FY2024)',
        'source_file': 'ASICS Integrated Report 2024.pdf',
        'page': 76,
    },
    {
        '报告周期': 'FY2024',
        '指标名称（原始）': 'Operating profit - Greater China',
        '数据值': 19335,
        '单位': '百万日元',
        '原文摘录': 'Greater China Operating profit ¥19,335 million (FY2024)',
        'source_file': 'ASICS Integrated Report 2024.pdf',
        'page': 76,
    },
    {
        '报告周期': 'FY2024',
        '指标名称（原始）': 'Operating margin - Greater China',
        '数据值': 19.3,
        '单位': '%',
        '原文摘录': 'Greater China Operating margin 19.3% (FY2024)',
        'source_file': 'ASICS Integrated Report 2024.pdf',
        'page': 30,
    },
    # FY2023 大中华区
    {
        '报告周期': 'FY2023',
        '指标名称（原始）': 'Net sales - Greater China',
        '数据值': 77616,
        '单位': '百万日元',
        '原文摘录': 'Greater China ¥77,616 million (Net Sales FY2023)',
        'source_file': 'ASICS Integrated Report 2024.pdf',
        'page': 76,
    },
    {
        '报告周期': 'FY2023',
        '指标名称（原始）': 'Operating profit - Greater China',
        '数据值': 13107,
        '单位': '百万日元',
        '原文摘录': 'Greater China Operating profit ¥13,107 million (FY2023)',
        'source_file': 'ASICS Integrated Report 2024.pdf',
        'page': 76,
    },
    {
        '报告周期': 'FY2023',
        '指标名称（原始）': 'Operating margin - Greater China',
        '数据值': 16.9,
        '单位': '%',
        '原文摘录': 'Greater China Operating margin 16.9% (FY2023)',
        'source_file': 'ASICS Integrated Report 2024.pdf',
        'page': 30,
    },
]

# 指标中文映射
indicator_cn_map = {
    'Net sales - Greater China': '营业收入',
    'Operating profit - Greater China': '经营溢利',
    'Operating margin - Greater China': '经营利润率',
}

# 检查已存在的记录
asics_mask = df['公司名称'].str.contains('ASICS', case=False, na=False)
gc_mask = df['区域'] == '大中华区'

existing = df[asics_mask & gc_mask]
print(f"已存在的ASICS大中华区记录数: {len(existing)}")

# 添加新记录
new_rows = []
today = datetime.now().strftime('%Y-%m-%d')

for item in asics_gc_data:
    # 检查是否已存在相同记录
    fy = item['报告周期']
    indicator = item['指标名称（原始）']
    dup_mask = (df['公司名称'].str.contains('ASICS', case=False, na=False)) & \
               (df['区域'] == '大中华区') & \
               (df['报告周期'] == fy) & \
               (df['指标名称（原始）'] == indicator)

    if dup_mask.any():
        print(f"  跳过已存在: {fy} | {indicator}")
        continue

    val = item['数据值']
    unit = item['单位']
    orig = item['原文摘录']
    source_file = item.get('source_file', 'ASICS Integrated Report 2024.pdf')
    page_num = item.get('page', 76)

    # 计算归一化值（千元人民币）
    if unit == '百万日元':
        normalized_val = val * 1000 * jpy_to_cny
        calc_logic = '百万日元×1000×0.048=千元人民币'
    elif unit == '%':
        normalized_val = val
        calc_logic = '百分比指标，归一化后数值不变'
    else:
        normalized_val = val
        calc_logic = ''

    new_row = {
        '#': len(df) + len(new_rows) + 1,
        '公司名称': 'ASICS Corporation',
        '品牌名称': 'ASICS',
        '区域': '大中华区',
        '指标名称（原始）': indicator,
        '报告周期': fy,
        '数据值': val,
        '单位': unit,
        '数据来源': source_file,
        '所在页码': page_num,
        '原文摘录': orig,
        '归一化周期': fy,
        '归一化指标名称': indicator_cn_map.get(indicator, ''),
        '归一化指标数值': normalized_val,
        '归一化计算逻辑/折算说明': calc_logic,
        '备注（披露范围等）': '大中华区(集团口径)',
        '最后更新': today,
    }
    new_rows.append(new_row)
    print(f"  + 添加: {fy} | {indicator} | {val} {unit} -> {normalized_val} 千元")

if new_rows:
    df_new = pd.DataFrame(new_rows)
    df = pd.concat([df, df_new], ignore_index=True)
    df.to_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database', index=False)
    print(f"\n✅ 已添加 {len(new_rows)} 条ASICS大中华区记录")
else:
    print("\n⚠️ 没有新记录需要添加")

# 验证
print("\n=== 验证ASICS大中华区数据 ===")
asics_gc = df[(df['公司名称'].str.contains('ASICS', case=False, na=False)) & (df['区域'] == '大中华区')]
print(asics_gc[['报告周期', '指标名称（原始）', '数据值', '单位', '归一化指标数值', '归一化计算逻辑/折算说明']].to_string(index=False))
