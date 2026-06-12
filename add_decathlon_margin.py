import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2_new.xlsx', sheet_name='Database')

# 删除已存在的Decathlon Net margin数据
mask = (
    df['公司名称'].str.contains('Decathlon|迪卡侬', case=False, na=False) &
    (df['指标名称（原始）'].str.contains('Net margin|净利率', case=False, na=False))
)
existing = df[mask]
df = df.drop(existing.index)
print(f"删除已存在的净利率数据: {len(existing)}条")

new_rows = [
    {
        '#': 28,
        '公司名称': 'Decathlon SA',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Net margin (Net result / Net sales)',
        '报告周期': 'FY2024',
        '数据值': 4.86,  # 787/16200 = 4.86%
        '单位': '%',
        '数据来源': 'Decathlon Group\'s 2024 Performance.html 计算',
        '所在页码': 'N/A (HTML)',
        '原文摘录': 'Net sales = 16.2 billion euros. Net result = 787 million euros',
        '归一化周期': 'FY2024',
        '归一化指标名称': '净利率',
        '归一化指标数值': 4.86,
        '归一化计算逻辑/折算说明': 'Net result (€787M) / Net sales (€16,200M) × 100%',
        '备注（披露范围等）': '集团TOTAL, Net result/Net sales',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    },
    {
        '#': 28,
        '公司名称': 'Decathlon SA',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Net margin (Net result / Net sales)',
        '报告周期': 'FY2023',
        '数据值': 5.97,  # 931/15600 = 5.97%
        '单位': '%',
        '数据来源': '迪卡侬2023年业绩报告 计算',
        '所在页码': '新闻报道',
        '原文摘录': '2023年迪卡侬集团业绩达156亿欧元...净利润高达9.31亿欧元',
        '归一化周期': 'FY2023',
        '归一化指标名称': '净利率',
        '归一化指标数值': 5.97,
        '归一化计算逻辑/折算说明': 'Net result (€931M) / Net sales (€15,600M) × 100%',
        '备注（披露范围等）': '集团TOTAL',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    },
    {
        '#': 28,
        '公司名称': 'Decathlon SA',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Net margin (Net result / Net sales)',
        '报告周期': 'FY2022',
        '数据值': 5.99,  # 923/15400 = 5.99%
        '单位': '%',
        '数据来源': '迪卡侬2022年业绩报告 计算',
        '所在页码': '新闻报道',
        '原文摘录': '2022年集团收入154亿欧元...净利润9.23亿欧元',
        '归一化周期': 'FY2022',
        '归一化指标名称': '净利率',
        '归一化指标数值': 5.99,
        '归一化计算逻辑/折算说明': 'Net result (€923M) / Net sales (€15,400M) × 100%',
        '备注（披露范围等）': '集团TOTAL',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    }
]

df_new = pd.DataFrame(new_rows)
existing_cols = df.columns.tolist()
for col in existing_cols:
    if col not in df_new.columns:
        df_new[col] = None
df_new = df_new[existing_cols]

df_combined = pd.concat([df, df_new], ignore_index=True)

target = '竞品财务数据库_标准模板v2_new.xlsx'
df_combined.to_excel(target, sheet_name='Database', index=False)

print(f"\n✅ 已添加Decathlon净利率数据 {len(new_rows)}条")
print("\n=== 验证 ===")
dec = df_combined[
    df_combined['公司名称'].str.contains('Decathlon|迪卡侬', case=False, na=False) &
    df_combined['指标名称（原始）'].str.contains('Net margin', case=False, na=False)
]
for idx, row in dec.iterrows():
    print(f"  {row['报告周期']} | 净利率: {row['数据值']}%")