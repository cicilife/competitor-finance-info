import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2_new.xlsx', sheet_name='Database')

# 删除已存在的Decathlon FY2025数据
mask = (
    df['公司名称'].str.contains('Decathlon|迪卡侬', case=False, na=False) &
    (df['报告周期'] == 'FY2025')
)
existing = df[mask]
df = df.drop(existing.index)
print(f"删除已存在的Decathlon FY2025数据: {len(existing)}条")

eur_to_cny = 7.8

# Decathlon 2025年数据 (来源: decathlon-group_global-annual-results-2025_press-release.pdf P3)
new_rows = [
    {
        '#': 28,
        '公司名称': 'Decathlon SA',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Net sales',
        '报告周期': 'FY2025',
        '数据值': 16800,  # 16.8 billion euros
        '单位': '百万欧元',
        '数据来源': 'decathlon-group_global-annual-results-2025_press-release.pdf',
        '所在页码': '3',
        '原文摘录': 'Net sales = 16.8 billion euros',
        '归一化周期': 'FY2025',
        '归一化指标名称': '营业收入',
        '归一化指标数值': 16800 * 1000 * eur_to_cny,
        '归一化计算逻辑/折算说明': '百万欧元×1000×7.8=千元人民币',
        '备注（披露范围等）': '集团TOTAL',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    },
    {
        '#': 28,
        '公司名称': 'Decathlon SA',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Net result',
        '报告周期': 'FY2025',
        '数据值': 910,  # 910 million euros
        '单位': '百万欧元',
        '数据来源': 'decathlon-group_global-annual-results-2025_press-release.pdf',
        '所在页码': '3',
        '原文摘录': 'Net result = 910 million euros',
        '归一化周期': 'FY2025',
        '归一化指标名称': '净利润',
        '归一化指标数值': 910 * 1000 * eur_to_cny,
        '归一化计算逻辑/折算说明': '百万欧元×1000×7.8=千元人民币',
        '备注（披露范围等）': '集团TOTAL',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    },
    {
        '#': 28,
        '公司名称': 'Decathlon SA',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'EBITDA',
        '报告周期': 'FY2025',
        '数据值': 1800,  # 1.8 billion euros
        '单位': '百万欧元',
        '数据来源': 'decathlon-group_global-annual-results-2025_press-release.pdf',
        '所在页码': '3',
        '原文摘录': 'EBITDA = 1.8 billion euros',
        '归一化周期': 'FY2025',
        '归一化指标名称': 'EBITDA',
        '归一化指标数值': 1800 * 1000 * eur_to_cny,
        '归一化计算逻辑/折算说明': '百万欧元×1000×7.8=千元人民币',
        '备注（披露范围等）': '集团TOTAL, EBITDA',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    },
    {
        '#': 28,
        '公司名称': 'Decathlon SA',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Gross Merchandise Volume',
        '报告周期': 'FY2025',
        '数据值': 20700,  # 20.7 billion euros
        '单位': '百万欧元',
        '数据来源': 'decathlon-group_global-annual-results-2025_press-release.pdf',
        '所在页码': '3',
        '原文摘录': 'Gross Merchandise Volume (GMV) = 20.7 billion euros',
        '归一化周期': 'FY2025',
        '归一化指标名称': '商品交易总额',
        '归一化指标数值': 20700 * 1000 * eur_to_cny,
        '归一化计算逻辑/折算说明': '百万欧元×1000×7.8=千元人民币',
        '备注（披露范围等）': '集团TOTAL, GMV含批发和零售总额',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    },
    {
        '#': 28,
        '公司名称': 'Decathlon SA',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Number of stores',
        '报告周期': 'FY2025',
        '数据值': 1902,
        '单位': '家',
        '数据来源': 'decathlon-group_global-annual-results-2025_press-release.pdf',
        '所在页码': '3',
        '原文摘录': 'Number of stores = 1,902',
        '归一化周期': 'FY2025',
        '归一化指标名称': '门店数',
        '归一化指标数值': 1902,
        '归一化计算逻辑/折算说明': '门店数直接存储',
        '备注（披露范围等）': '集团TOTAL, 全球门店数',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    },
    {
        '#': 28,
        '公司名称': 'Decathlon SA',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Digital sales share',
        '报告周期': 'FY2025',
        '数据值': 20.2,
        '单位': '%',
        '数据来源': 'decathlon-group_global-annual-results-2025_press-release.pdf',
        '所在页码': '3',
        '原文摘录': 'Digital sales share (ecommerce, connected orders in stores, external marketplace) = 20.2%',
        '归一化周期': 'FY2025',
        '归一化指标名称': '数字渠道占比',
        '归一化指标数值': 20.2,
        '归一化计算逻辑/折算说明': '百分比直接存储',
        '备注（披露范围等）': '集团TOTAL, 含电商、店内线上下单、外部市场',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    },
    {
        '#': 28,
        '公司名称': 'Decathlon SA',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Number of countries',
        '报告周期': 'FY2025',
        '数据值': 82,
        '单位': '个',
        '数据来源': 'decathlon-group_global-annual-results-2025_press-release.pdf',
        '所在页码': '3',
        '原文摘录': 'Global presence = 82 countries/regions',
        '归一化周期': 'FY2025',
        '归一化指标名称': '覆盖国家数',
        '归一化指标数值': 82,
        '归一化计算逻辑/折算说明': '国家数直接存储',
        '备注（披露范围等）': '集团TOTAL, 业务覆盖国家/地区数',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    },
    {
        '#': 28,
        '公司名称': 'Decathlon SA',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Number of teammates',
        '报告周期': 'FY2025',
        '数据值': 102913,
        '单位': '人',
        '数据来源': 'decathlon-group_global-annual-results-2025_press-release.pdf',
        '所在页码': '3',
        '原文摘录': 'Number of Teammates = 102,913',
        '归一化周期': 'FY2025',
        '归一化指标名称': '员工数',
        '归一化指标数值': 102913,
        '归一化计算逻辑/折算说明': '员工数直接存储',
        '备注（披露范围等）': '集团TOTAL, 全球员工数(Teammates)',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    },
    {
        '#': 28,
        '公司名称': 'Decathlon SA',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Net margin (Net result / Net sales)',
        '报告周期': 'FY2025',
        '数据值': 5.42,  # 910/16800 = 5.42%
        '单位': '%',
        '数据来源': 'decathlon-group_global-annual-results-2025_press-release.pdf 计算',
        '所在页码': '3',
        '原文摘录': 'Net sales = 16.8 billion euros. Net result = 910 million euros',
        '归一化周期': 'FY2025',
        '归一化指标名称': '净利率',
        '归一化指标数值': 5.42,
        '归一化计算逻辑/折算说明': 'Net result (€910M) / Net sales (€16,800M) × 100%',
        '备注（披露范围等）': '集团TOTAL, 同比2024年4.86%回升',
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
df_combined.to_excel('竞品财务数据库_标准模板v2_new.xlsx', sheet_name='Database', index=False)

print(f"\n✅ 已添加Decathlon FY2025数据 {len(new_rows)}条")
print("\n=== 验证 ===")
dec = df_combined[df_combined['公司名称'].str.contains('Decathlon|迪卡侬', case=False, na=False)]
for idx, row in dec.iterrows():
    print(f"  {row['报告周期']} | {row['区域']:<10} | {str(row['指标名称（原始）'])[:25]:<25} | G={row['数据值']} | {row['单位']} | M={row['归一化指标数值']}")