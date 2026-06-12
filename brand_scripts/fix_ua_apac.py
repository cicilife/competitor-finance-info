import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

usd_to_cny = 7.2

# ============ 修正安德玛亚太区数据 ============
# 数据来源: UA_2025_AnnualReport_Print_FINAL.pdf P89-90
# 单位: 千美元 (thousands of USD)

print("=== 修正安德玛亚太区数据 ===")

# 先删除现有的安德玛亚太区数据
df = df[~((df['公司名称'].str.contains('安德玛|Under Armour', case=False, na=False)) & (df['区域'] == '亚太区'))]
print(f"删除现有亚太区数据后: {len(df)}行")

# 安德玛亚太区数据 (P89-90)
mizuno_apac = {
    'FY2025': {'Net_revenues': 755437, 'Operating_income': 73187},
    'FY2024': {'Net_revenues': 873019, 'Operating_income': 119650},
    'FY2023': {'Net_revenues': 825338, 'Operating_income': 100276}
}

new_rows = []

for fy, data in mizuno_apac.items():
    # 营业收入
    new_rows.append({
        '#': 11,
        '公司名称': '安德玛',
        '品牌名称': 'TTL',
        '区域': '亚太区',
        '指标名称（原始）': 'Net revenues - Asia-Pacific',
        '报告周期': fy,
        '数据值': data['Net_revenues'],
        '单位': '千美元',
        '数据来源': 'UA_2025_AnnualReport_Print_FINAL.pdf',
        '所在页码': '89',
        '原文摘录': f'Asia-Pacific Net revenues ${data["Net_revenues"]:,} thousand',
        '归一化周期': fy,
        '归一化指标名称': '营业收入',
        '归一化指标数值': data['Net_revenues'] * usd_to_cny,
        '归一化计算逻辑/折算说明': '千美元×7.2=千元人民币',
        '备注（披露范围等）': '亚太区（含中国、日本、韩国、澳洲等）',
        '最后更新': '2025-01-01'
    })

    # 经营利润
    new_rows.append({
        '#': 11,
        '公司名称': '安德玛',
        '品牌名称': 'TTL',
        '区域': '亚太区',
        '指标名称（原始）': 'Operating income - Asia-Pacific',
        '报告周期': fy,
        '数据值': data['Operating_income'],
        '单位': '千美元',
        '数据来源': 'UA_2025_AnnualReport_Print_FINAL.pdf',
        '所在页码': '89',
        '原文摘录': f'Asia-Pacific Operating income ${data["Operating_income"]:,} thousand',
        '归一化周期': fy,
        '归一化指标名称': '经营利润',
        '归一化指标数值': data['Operating_income'] * usd_to_cny,
        '归一化计算逻辑/折算说明': '千美元×7.2=千元人民币',
        '备注（披露范围等）': '亚太区',
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
print("\n验证安德玛亚太区数据:")
ua = df_combined[(df_combined['公司名称'].str.contains('安德玛|Under Armour', case=False, na=False)) & (df_combined['区域'] == '亚太区')]
print(ua[['报告周期', '指标名称（原始）', '数据值', '单位', '归一化指标数值', '所在页码']].to_string())

print(f"\n✅ 已更新安德玛亚太区数据，共{len(new_rows)}条记录")