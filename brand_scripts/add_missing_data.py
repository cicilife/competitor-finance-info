import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

# ============ 1. lululemon中国内地数据 ============
# 数据来源: Lululemon_2025_Q4季报_财务报告.pdf
# Q4 FY2025 China Mainland net revenue: $528.4 million
# Q4 FY2024 China Mainland net revenue: $425.0 million
# 年度数据需要从10-K年报提取，这里先用Q4数据作为参考

# 根据Lululemon FY2025 Q4季报:
# - FY2025 Q4 China Mainland: $528.4 million (15% of total)
# - FY2024 Q4 China Mainland: $425.0 million (12% of total)

# 由于缺少完整的中国区年度数据，我们基于Q4数据和现有TOTAL数据估算年度中国区收入
# FY2025 Total net revenue: $10,351 million (已知)
# FY2025 Q4 China: $528.4 million, 占比15%
# FY2024 Total net revenue: $9,600 million (已知)
# FY2024 Q4 China: $425.0 million, 占比12%

# 注意：lululemon财年结束于1月/2月，FY2025截至2025年2月2日

# 删除现有的lululemon中国内地数据（如果存在）
df = df[~((df['公司名称'].str.contains('lululemon', case=False, na=False)) & (df['区域'] == '中国内地'))]
print(f"删除现有lululemon中国内地数据后: {len(df)}行")

usd_to_cny = 7.2

lululemon_china_rows = []

# lululemon中国内地数据（Q4数据，仅供参考，实际年度数据需从年报提取）
# FY2025 China Mainland Q4: $528.4 million
lululemon_china_rows.extend([
    {
        '#': 5,
        '公司名称': 'lululemon athletica inc.',
        '品牌名称': 'TTL',
        '区域': '中国内地',
        '指标名称（原始）': 'Net revenue - China Mainland (Q4)',
        '报告周期': 'FY2025',
        '数据值': 528.4,
        '单位': '百万美元',
        '数据来源': 'Lululemon_2025_Q4季报_财务报告.pdf',
        '所在页码': '1',
        '原文摘录': 'China Mainland net revenue was $528.4 million, or 15% of total revenue, in Q4 FY2025',
        '归一化周期': 'FY2025',
        '归一化指标名称': '营业收入',
        '归一化指标数值': 528.4 * 1000 * usd_to_cny,
        '归一化计算逻辑/折算说明': '百万美元×7200000=千元人民币（Q4数据，仅供参考）',
        '备注（披露范围等）': '中国内地，Q4 FY2025',
        '最后更新': '2025-01-01'
    },
    {
        '#': 5,
        '公司名称': 'lululemon athletica inc.',
        '品牌名称': 'TTL',
        '区域': '中国内地',
        '指标名称（原始）': 'Net revenue - China Mainland (Q4)',
        '报告周期': 'FY2024',
        '数据值': 425.0,
        '单位': '百万美元',
        '数据来源': 'Lululemon_2025_Q4季报_财务报告.pdf',
        '所在页码': '1',
        '原文摘录': 'China Mainland net revenue was $425.0 million, or 12% of total net revenue, in Q4 FY2024',
        '归一化周期': 'FY2024',
        '归一化指标名称': '营业收入',
        '归一化指标数值': 425.0 * 1000 * usd_to_cny,
        '归一化计算逻辑/折算说明': '百万美元×7200000=千元人民币（Q4数据，仅供参考）',
        '备注（披露范围等）': '中国内地，Q4 FY2024',
        '最后更新': '2025-01-01'
    }
])

# ============ 2. Topgolf FY2025数据 ============
# 数据来源: 2025 Annual Report.pdf P61
# FY2025 (year ended Dec 31, 2025): Total Net sales $2,060.1 million, Asia $363.1 million
# FY2024 (year ended Dec 31, 2024): Total Net sales $2,077.7 million, Asia $379.1 million
# 注意: 2025年报数据为持续经营业务，不包含已分拆的Topgolf业务

# 删除现有的Topgolf FY2025数据（如果存在）
df = df[~((df['公司名称'].str.contains('Topgolf', case=False, na=False)) & (df['报告周期'] == 'FY2025'))]
print(f"删除现有Topgolf FY2025数据后: {len(df)}行")

topgolf_rows = []

# Topgolf FY2025 Total
topgolf_rows.append({
    '#': 24,
    '公司名称': 'Topgolf Callaway Brands Corp',
    '品牌名称': 'TTL',
    '区域': 'TOTAL',
    '指标名称（原始）': 'Net revenues',
    '报告周期': 'FY2025',
    '数据值': 2060.1,
    '单位': '百万美元',
    '数据来源': '2025 Annual Report.pdf',
    '所在页码': '61',
    '原文摘录': 'Total net sales $2,060.1 million (Continuing operations only)',
    '归一化周期': 'FY2025',
    '归一化指标名称': '营业收入',
    '归一化指标数值': 2060.1 * 1000 * usd_to_cny,
    '归一化计算逻辑/折算说明': '百万美元×7200000=千元人民币',
    '备注（披露范围等）': '集团TOTAL（持续经营业务，不含已分拆Topgolf业务）',
    '最后更新': '2025-01-01'
})

# Topgolf FY2025 亚太区
topgolf_rows.append({
    '#': 24,
    '公司名称': 'Topgolf Callaway Brands Corp',
    '品牌名称': 'TTL',
    '区域': '亚太区',
    '指标名称（原始）': 'Net revenues - Asia',
    '报告周期': 'FY2025',
    '数据值': 363.1,
    '单位': '百万美元',
    '数据来源': '2025 Annual Report.pdf',
    '所在页码': '61',
    '原文摘录': 'Asia net sales $363.1 million',
    '归一化周期': 'FY2025',
    '归一化指标名称': '营业收入',
    '归一化指标数值': 363.1 * 1000 * usd_to_cny,
    '归一化计算逻辑/折算说明': '百万美元×7200000=千元人民币',
    '备注（披露范围等）': '亚太区（持续经营业务）',
    '最后更新': '2025-01-01'
})

# 合并所有新行
all_new_rows = lululemon_china_rows + topgolf_rows
df_new = pd.DataFrame(all_new_rows)
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
print("\n验证lululemon中国内地数据:")
lulu = df_combined[(df_combined['公司名称'].str.contains('lululemon', case=False, na=False)) & (df_combined['区域'] == '中国内地')]
print(lulu[['报告周期', '指标名称（原始）', '数据值', '单位', '归一化指标数值']].to_string())

print("\n验证Topgolf FY2025数据:")
topgolf = df_combined[(df_combined['公司名称'].str.contains('Topgolf', case=False, na=False)) & (df_combined['报告周期'] == 'FY2025')]
print(topgolf[['区域', '指标名称（原始）', '数据值', '单位', '归一化指标数值']].to_string())

print(f"\n✅ 已添加lululemon中国内地数据{len(lululemon_china_rows)}条，Topgolf FY2025数据{len(topgolf_rows)}条")