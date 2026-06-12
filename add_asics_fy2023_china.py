import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

jpy_to_cny = 0.048

# 添加FY2023 ASICS中国大陆数据 (来源: 2024年报P58)
new_row = {
    '#': 14,
    '公司名称': 'ASICS Corporation',
    '品牌名称': 'TTL',
    '区域': '中国内地',
    '指标名称（原始）': 'Net sales - China Mainland',
    '报告周期': 'FY2023',
    '数据值': 63624,  # 百万日元
    '单位': '百万日元',
    '数据来源': '2024Q4 Annual Report.pdf',
    '所在页码': '58',
    '原文摘录': 'Net sales attributable to "Greater China" of ¥77,572 million for the year ended December 31, 2023 include net sales in the People\'s Republic of China of ¥63,624 million',
    '归一化周期': 'FY2023',
    '归一化指标名称': '营业收入',
    '归一化指标数值': 63624 * 1000 * jpy_to_cny,
    '归一化计算逻辑/折算说明': '百万日元×1000×0.048=千元人民币',
    '备注（披露范围等）': '中国大陆(People\'s Republic of China)',
    '最后更新': '2025-06-09',
    '人工核验': '待核验'
}

df_new = pd.DataFrame([new_row])
existing_cols = df.columns.tolist()
for col in existing_cols:
    if col not in df_new.columns:
        df_new[col] = None
df_new = df_new[existing_cols]

df_combined = pd.concat([df, df_new], ignore_index=True)
df_combined.to_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database', index=False)

print(f"✅ 已添加ASICS FY2023中国大陆数据\n")
print("=== 验证ASICS中国内地全部数据 ===")
asics_china = df_combined[
    df_combined['公司名称'].str.contains('ASICS', case=False, na=False) &
    (df_combined['区域'] == '中国内地')
]
for idx, row in asics_china.iterrows():
    print(f"  {row['报告周期']} | G={row['数据值']} | {row['单位']} | M={row['归一化指标数值']}")