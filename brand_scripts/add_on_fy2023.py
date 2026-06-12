import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

chf_to_cny = 8.1

# ============ 添加昂跑FY2023亚太区数据 ============
# 数据来源: Ex-99-3_Annual-Report_FY2024-Website.pdf P168
# FY2023: Asia-Pacific Net sales CHF 141.1 million
# 注意: 昂跑是单一业务板块，不提供地区经营利润分解

print("=== 添加昂跑FY2023亚太区数据 ===")

# 昂跑亚太区FY2023数据
fiscal_year = 'FY20231231'  # 昂跑财年结束于12月31日
data = {
    'Net_sales': 141100  # 141.1 million CHF = 141,100千CHF
}

new_rows = []

# 营业收入
new_rows.append({
    '#': 12,
    '公司名称': 'On Holding AG',
    '品牌名称': 'TTL',
    '区域': '亚太区',
    '指标名称（原始）': 'Net sales - Asia-Pacific',
    '报告周期': 'FY2023',
    '数据值': data['Net_sales'],
    '单位': '千CHF',
    '数据来源': 'Ex-99-3_Annual-Report_FY2024-Website.pdf',
    '所在页码': '168',
    '原文摘录': f'Asia-Pacific Net sales CHF 141.1 million',
    '归一化周期': 'FY2023',
    '归一化指标名称': '营业收入',
    '归一化指标数值': data['Net_sales'] * chf_to_cny,
    '归一化计算逻辑/折算说明': '千CHF×8.1=千元人民币',
    '备注（披露范围等）': '亚太区（单一业务板块，不提供地区经营利润）',
    '最后更新': '2025-01-01'
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
print(f"合并后: {len(df_combined)}行")

# 保存
df_combined.to_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database', index=False)

# 验证
print("\n验证昂跑亚太区数据:")
on = df_combined[(df_combined['公司名称'].str.contains('昂跑|On Holding', case=False, na=False)) & (df_combined['区域'] == '亚太区')]
print(on[['报告周期', '指标名称（原始）', '数据值', '单位', '归一化指标数值']].to_string())

print(f"\n✅ 已添加昂跑FY2023亚太区数据{len(new_rows)}条")