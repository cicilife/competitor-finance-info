import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

# 删除可能重复的Adidas数据
mask = (
    df['公司名称'].str.contains('adidas', case=False, na=False) &
    (df['区域'] == 'TOTAL') &
    (df['报告周期'].isin(['FY2024', 'FY2023']))
)
existing = df[mask]
new_indicators = ['Net income/(loss)', 'Net income from continuing operations',
                  'Marketing and point-of-sale expenses', 'Distribution and selling expenses',
                  'General and administration expenses', 'Research and development expenses',
                  'Personnel expenses']
existing_to_remove = existing[existing['指标名称（原始）'].isin(new_indicators)]
df = df.drop(existing_to_remove.index)
print(f"删除已存在的Adidas相关数据: {len(existing_to_remove)}条")

eur_to_cny = 7.8

new_rows = []

# FY2024 数据
data_2024 = [
    ('Net income from continuing operations', '824', 'Net income from continuing operations', '824', 'Net income from continuing operations €824 million'),
    ('Net income/(loss) attributable to shareholders', '764', 'Net income attributable to shareholders', '764', 'net income attributable to shareholders...amounted to €764 million in 2024'),
    ('Net income/(loss)', '832', 'Net income/(loss)', '832', 'Net income/(loss) 832'),
    ('Marketing and point-of-sale expenses', '2,841', 'Marketing and point-of-sale expenses', '2841', 'Marketing and point-of-sale expenses 2,841'),
    ('Distribution and selling expenses', '5,936', 'Distribution and selling expenses', '5936', 'Distribution and selling expenses 5,936'),
    ('General and administration expenses', '2,138', 'General and administration expenses', '2138', 'General and administration expenses 2,138'),
    ('Other operating expenses', '10,945', 'Other operating expenses', '10945', 'Other operating expenses 10,945'),
]

# FY2023 数据
data_2023 = [
    ('Net income from continuing operations', '-58', 'Net income from continuing operations', '-58', 'Net loss of €58 million'),
    ('Net income/(loss) attributable to shareholders', '-75', 'Net income attributable to shareholders', '-75', 'net loss of €75 million'),
    ('Net income/(loss)', '-14', 'Net income/(loss)', '-14', 'Net income/(loss) -14'),
    ('Marketing and point-of-sale expenses', '2,528', 'Marketing and point-of-sale expenses', '2528', 'Marketing and point-of-sale expenses 2,528'),
    ('Distribution and selling expenses', '5,547', 'Distribution and selling expenses', '5547', 'Distribution and selling expenses 5,547'),
    ('General and administration expenses', '1,839', 'General and administration expenses', '1839', 'General and administration expenses 1,839'),
    ('Other operating expenses', '10,070', 'Other operating expenses', '10070', 'Other operating expenses 10,070'),
]

indicator_mapping = {
    'Net income from continuing operations': '净利润',
    'Net income/(loss) attributable to shareholders': '归属母公司净利润',
    'Net income/(loss)': '净利润',
    'Marketing and point-of-sale expenses': '广告及市场费用',
    'Distribution and selling expenses': '分销与销售费用',
    'General and administration expenses': '管理费用',
    'Other operating expenses': '运营费用'
}

for year, data_list in [('FY2024', data_2024), ('FY2023', data_2023)]:
    for orig_term, _, _, val_str, orig_excerpt in data_list:
        val = float(val_str.replace(',', ''))
        # 计算各费用率
        rate = None
        if 'expenses' in orig_term.lower() and val != 0:
            # 销售额2024=23,683, 2023=21,427
            if year == 'FY2024':
                rate = round(val / 23683 * 100, 1)
            else:
                rate = round(val / 21427 * 100, 1)

        new_rows.append({
            '#': 2,
            '公司名称': 'adidas AG',
            '品牌名称': 'ADIDAS',
            '区域': 'TOTAL',
            '指标名称（原始）': orig_term,
            '报告周期': year,
            '数据值': val,
            '单位': '百万欧元',
            '数据来源': 'adidas_annual_report_2024_EN_Final_secured_c8nukv.pdf',
            '所在页码': '361',
            '原文摘录': orig_excerpt,
            '归一化周期': year,
            '归一化指标名称': indicator_mapping[orig_term],
            '归一化指标数值': val * 1000 * eur_to_cny,
            '归一化计算逻辑/折算说明': '百万欧元×1000×7.8=千元人民币',
            '备注（披露范围等）': f'集团TOTAL {"(占销售额"+str(rate)+"%)" if rate else ""}',
            '最后更新': '2025-06-09',
            '人工核验': '待核验'
        })

# 创建新DataFrame
df_new = pd.DataFrame(new_rows)
existing_cols = df.columns.tolist()
for col in existing_cols:
    if col not in df_new.columns:
        df_new[col] = None
df_new = df_new[existing_cols]

df_combined = pd.concat([df, df_new], ignore_index=True)
df_combined.to_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database', index=False)

print(f"\n✅ 已添加Adidas净利润和经营费用细分数据 {len(new_rows)}条")
print("\n=== 验证 ===")
adidas_new = df_combined[
    df_combined['公司名称'].str.contains('adidas', case=False, na=False) &
    (df_combined['区域'] == 'TOTAL') &
    (df_combined['归一化指标名称'].isin(['净利润', '归属母公司净利润', '广告及市场费用', '分销与销售费用', '管理费用', '运营费用']))
]
for idx, row in adidas_new.iterrows():
    print(f"  {row['报告周期']} | {row['指标名称（原始）'][:35]:<35} | G={row['数据值']} | M={row['归一化指标数值']}")

print(f"\n说明:")
print(f"- 广告/营销费用占比: 2024=12.0%, 2023=11.8%")
print(f"- 分销/销售费用占比: 2024=25.1%, 2023=25.9%")
print(f"- 管理费用占比: 2024=9.0%, 2023=8.6%")
print(f"- 其他运营费用占比: 2024=46.2%, 2023=47.0%")
print(f"- 注: R&D和Personnel费用未单独披露，包含在成本和销售费用中")
print(f"  - R&D员工2024=1,047人, 2023=993人")
print(f"  - 员工总数2024=59,137人, 2023=57,485人")