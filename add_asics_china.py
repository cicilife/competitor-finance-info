import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

# 删除已有的ASICS中国大陆数据
mask_china = (
    df['公司名称'].str.contains('ASICS', case=False, na=False) &
    (df['区域'] == '中国内地')
)
df = df[~mask_china]
print(f"删除已存在的ASICS中国内地数据: {mask_china.sum()}条")

jpy_to_cny = 0.048

# ASICS中国大陆数据 (来源: ASICS Consolidated Financial Statements 2025 P65, 2024年报P59)
# FY2024: 中国大陆 ¥83,026 million (P65)
# FY2025: 中国大陆 ¥99,151 million (P65)
# FY2023: 暂无详细数据

new_rows = []

# FY2025 中国大陆 Net sales
new_rows.append({
    '#': 14,
    '公司名称': 'ASICS Corporation',
    '品牌名称': 'TTL',
    '区域': '中国内地',
    '指标名称（原始）': 'Net sales - China Mainland',
    '报告周期': 'FY2025',
    '数据值': 99151,  # 百万日元
    '单位': '百万日元',
    '数据来源': "Consolidated Financial Statements and Auditor's Report 2025.pdf",
    '所在页码': '65',
    '原文摘录': 'Net sales attributable to "Greater China" of ¥120,244 million for the year ended December 31, 2025 include net sales in the People\'s Republic of China of ¥99,151 million',
    '归一化周期': 'FY2025',
    '归一化指标名称': '营业收入',
    '归一化指标数值': 99151 * 1000 * jpy_to_cny,
    '归一化计算逻辑/折算说明': '百万日元×1000×0.048=千元人民币',
    '备注（披露范围等）': '中国大陆(People\'s Republic of China)',
    '最后更新': '2025-06-09',
    '人工核验': '待核验'
})

# FY2024 中国大陆 Net sales
new_rows.append({
    '#': 14,
    '公司名称': 'ASICS Corporation',
    '品牌名称': 'TTL',
    '区域': '中国内地',
    '指标名称（原始）': 'Net sales - China Mainland',
    '报告周期': 'FY2024',
    '数据值': 83026,  # 百万日元
    '单位': '百万日元',
    '数据来源': "Consolidated Financial Statements and Auditor's Report 2025.pdf",
    '所在页码': '65',
    '原文摘录': 'Net sales attributable to "Greater China" of ¥100,490 million for the year ended December 31, 2024 include net sales in the People\'s Republic of China of ¥83,026 million',
    '归一化周期': 'FY2024',
    '归一化指标名称': '营业收入',
    '归一化指标数值': 83026 * 1000 * jpy_to_cny,
    '归一化计算逻辑/折算说明': '百万日元×1000×0.048=千元人民币',
    '备注（披露范围等）': '中国大陆(People\'s Republic of China)',
    '最后更新': '2025-06-09',
    '人工核验': '待核验'
})

# 创建新记录DataFrame
df_new = pd.DataFrame(new_rows)
existing_cols = df.columns.tolist()
for col in existing_cols:
    if col not in df_new.columns:
        df_new[col] = None
df_new = df_new[existing_cols]

# 合并
df_combined = pd.concat([df, df_new], ignore_index=True)

# 保存
df_combined.to_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database', index=False)

print(f"\n✅ 已添加ASICS中国大陆数据 {len(new_rows)}条")
print("\n=== 验证 ===")
asics_china = df_combined[
    df_combined['公司名称'].str.contains('ASICS', case=False, na=False) &
    (df_combined['区域'] == '中国内地')
]
for idx, row in asics_china.iterrows():
    print(f"  {row['报告周期']} | {row['指标名称（原始）'][:30]:<30} | G={row['数据值']} | {row['单位']} | M={row['归一化指标数值']}")

print(f"\n说明: FY2023年中国大陆数据需从2023年报提取(暂无文件)")