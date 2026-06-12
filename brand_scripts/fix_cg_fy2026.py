import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

cad_to_cny = 5.5

# ============ 修正加拿大鹅报告周期 & 添加FY2026数据 ============
# 数据来源: CG-20F-Q4-2026-Financial-Statements.pdf P28
# 财年结束日期: FY2026 截至2026.3.29, FY2025 截至2025.3.30, FY2024 截至2024.3.31

# 加拿大鹅FY2026, FY2025, FY2024区域数据 (单位: 百万加元)
cg_data = {
    'FY2026': {  # 截至2026.3.29
        'Total revenue': 1528.2,
        'Greater China': 498.3,
        'Asia Pacific (excl Greater China)': 130.0,
        'Asia Pacific': 628.3
    },
    'FY2025': {  # 截至2025.3.30
        'Total revenue': 1348.4,
        'Greater China': 426.5,
        'Asia Pacific (excl Greater China)': 111.3,
        'Asia Pacific': 537.8
    },
    'FY2024': {  # 截至2024.3.31
        'Total revenue': 1333.8,
        'Greater China': 422.2,
        'Asia Pacific (excl Greater China)': 84.7,
        'Asia Pacific': 506.9
    }
}

print("=== 更新加拿大鹅数据 ===")

# 删除现有的加拿大鹅TOTAL和大中华区数据
df = df[~((df['公司名称'].str.contains('加拿大鹅|Canada Goose', case=False, na=False)) & (df['区域'].isin(['TOTAL', '大中华区'])))]
print(f"删除现有数据后: {len(df)}行")

new_rows = []

# 加拿大鹅财年结束日期映射
fiscal_year_end = {
    'FY2026': 'FY20260329',
    'FY2025': 'FY20250330',
    'FY2024': 'FY20240331'
}

for fy, fy_data in cg_data.items():
    fiscal_period = fiscal_year_end[fy]

    # TOTAL 营业收入
    new_rows.append({
        '#': 15,
        '公司名称': 'Canada Goose Holdings Inc',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Total revenue',
        '报告周期': fiscal_period,
        '数据值': fy_data['Total revenue'] * 1000,  # 转为千CAD
        '单位': '千CAD',
        '数据来源': 'CG-20F-Q4-2026-Financial-Statements.pdf',
        '所在页码': '28',
        '原文摘录': f'Total revenue CAD {fy_data["Total revenue"]} million',
        '归一化周期': fiscal_period,
        '归一化指标名称': '营业收入',
        '归一化指标数值': fy_data['Total revenue'] * 1000 * cad_to_cny,
        '归一化计算逻辑/折算说明': '百万CAD×1000×5.5=千元人民币',
        '备注（披露范围等）': '集团TOTAL',
        '最后更新': '2025-01-01'
    })

    # 大中华区营业收入
    new_rows.append({
        '#': 15,
        '公司名称': 'Canada Goose Holdings Inc',
        '品牌名称': 'TTL',
        '区域': '大中华区',
        '指标名称（原始）': 'Total revenue - Greater China',
        '报告周期': fiscal_period,
        '数据值': fy_data['Greater China'] * 1000,
        '单位': '千CAD',
        '数据来源': 'CG-20F-Q4-2026-Financial-Statements.pdf',
        '所在页码': '28',
        '原文摘录': f'Greater China CAD {fy_data["Greater China"]} million',
        '归一化周期': fiscal_period,
        '归一化指标名称': '营业收入',
        '归一化指标数值': fy_data['Greater China'] * 1000 * cad_to_cny,
        '归一化计算逻辑/折算说明': '百万CAD×1000×5.5=千元人民币',
        '备注（披露范围等）': '大中华区（含中国大陆、香港、澳门、台湾）',
        '最后更新': '2025-01-01'
    })

    # 亚太区营业收入
    new_rows.append({
        '#': 15,
        '公司名称': 'Canada Goose Holdings Inc',
        '品牌名称': 'TTL',
        '区域': '亚太区',
        '指标名称（原始）': 'Total revenue - Asia Pacific',
        '报告周期': fiscal_period,
        '数据值': fy_data['Asia Pacific'] * 1000,
        '单位': '千CAD',
        '数据来源': 'CG-20F-Q4-2026-Financial-Statements.pdf',
        '所在页码': '28',
        '原文摘录': f'Asia Pacific CAD {fy_data["Asia Pacific"]} million',
        '归一化周期': fiscal_period,
        '归一化指标名称': '营业收入',
        '归一化指标数值': fy_data['Asia Pacific'] * 1000 * cad_to_cny,
        '归一化计算逻辑/折算说明': '百万CAD×1000×5.5=千元人民币',
        '备注（披露范围等）': '亚太区（含大中华区、日本、韩国、澳洲等）',
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
print("\n验证加拿大鹅数据:")
cg = df_combined[df_combined['公司名称'].str.contains('加拿大鹅|Canada Goose', case=False, na=False)]
print(cg[['报告周期', '区域', '指标名称（原始）', '数据值', '单位', '归一化指标数值']].to_string())

print(f"\n✅ 已更新加拿大鹅数据，共{len(new_rows)}条记录")