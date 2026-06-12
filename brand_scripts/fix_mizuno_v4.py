import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

jpy_to_cny = 0.048

# 删除所有美津浓数据，重新添加
df = df[~df['公司名称'].str.contains('美津浓|Mizuno', case=False, na=False)]
print(f"删除所有美津浓数据后: {len(df)}行")

new_rows = []

mizuno_data = {
    'FY20260331': {
        'Net sales': 259045,
        'Gross profit': 108467,
        'Gross margin': 41.9,
        'Asia_Net_sales': 35351,
        'Asia_Profit': 3565
    },
    'FY20250331': {
        'Net sales': 240335,
        'Gross profit': 100572,
        'Gross margin': 41.8,
        'Asia_Net_sales': 33314,
        'Asia_Profit': 4038
    },
    'FY20240331': {
        'Net sales': 229711,
        'Gross profit': 93049,
        'Gross margin': 40.5,
        'Asia_Net_sales': 28845,
        'Asia_Profit': 2282
    }
}

for period, data in mizuno_data.items():
    # TOTAL 营业收入
    new_rows.append({
        '#': 10,
        '公司名称': '美津浓公司',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Net sales',
        '报告周期': period,
        '数据值': data['Net sales'],  # 百万日元（原始引用值）
        '单位': '百万日元',
        '数据来源': '260512_MIZUNO_FY25_Financial_result_ENG.pdf',
        '所在页码': '17',
        '原文摘录': f'Net sales ¥{data["Net sales"]:,} million',
        '归一化周期': period,
        '归一化指标名称': '营业收入',
        '归一化指标数值': data['Net sales'] * 1000 * jpy_to_cny,  # 百万日元→千日元→千元人民币
        '归一化计算逻辑/折算说明': '百万日元×1000×0.048=千元人民币',
        '备注（披露范围等）': '集团TOTAL',
        '最后更新': '2025-01-01'
    })

    # TOTAL 毛利
    new_rows.append({
        '#': 10,
        '公司名称': '美津浓公司',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Gross profit',
        '报告周期': period,
        '数据值': data['Gross profit'],
        '单位': '百万日元',
        '数据来源': '260512_MIZUNO_FY25_Financial_result_ENG.pdf',
        '所在页码': '17',
        '原文摘录': f'Gross profit ¥{data["Gross profit"]:,} million',
        '归一化周期': period,
        '归一化指标名称': '毛利润',
        '归一化指标数值': data['Gross profit'] * 1000 * jpy_to_cny,
        '归一化计算逻辑/折算说明': '百万日元×1000×0.048=千元人民币',
        '备注（披露范围等）': '集团TOTAL',
        '最后更新': '2025-01-01'
    })

    # TOTAL 毛利率
    new_rows.append({
        '#': 10,
        '公司名称': '美津浓公司',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Gross margin',
        '报告周期': period,
        '数据值': data['Gross margin'],
        '单位': '%',
        '数据来源': '260512_MIZUNO_FY25_Financial_result_ENG.pdf',
        '所在页码': '17',
        '原文摘录': f'Gross margin {data["Gross margin"]}%',
        '归一化周期': period,
        '归一化指标名称': '毛利率',
        '归一化指标数值': data['Gross margin'],
        '归一化计算逻辑/折算说明': '百分比',
        '备注（披露范围等）': '集团TOTAL',
        '最后更新': '2025-01-01'
    })

    # 亚太区 营业收入
    new_rows.append({
        '#': 10,
        '公司名称': '美津浓公司',
        '品牌名称': 'TTL',
        '区域': '亚太区',
        '指标名称（原始）': 'Net sales - Asia and Oceania',
        '报告周期': period,
        '数据值': data['Asia_Net_sales'],
        '单位': '百万日元',
        '数据来源': '260512_MIZUNO_FY25_Financial_result_ENG.pdf',
        '所在页码': '16',
        '原文摘录': f'Asia and Oceania Net sales ¥{data["Asia_Net_sales"]:,} million',
        '归一化周期': period,
        '归一化指标名称': '营业收入',
        '归一化指标数值': data['Asia_Net_sales'] * 1000 * jpy_to_cny,
        '归一化计算逻辑/折算说明': '百万日元×1000×0.048=千元人民币',
        '备注（披露范围等）': '亚太区',
        '最后更新': '2025-01-01'
    })

    # 亚太区 经营利润
    new_rows.append({
        '#': 10,
        '公司名称': '美津浓公司',
        '品牌名称': 'TTL',
        '区域': '亚太区',
        '指标名称（原始）': 'Segment profit - Asia and Oceania',
        '报告周期': period,
        '数据值': data['Asia_Profit'],
        '单位': '百万日元',
        '数据来源': '260512_MIZUNO_FY25_Financial_result_ENG.pdf',
        '所在页码': '16',
        '原文摘录': f'Asia and Oceania Segment profit ¥{data["Asia_Profit"]:,} million',
        '归一化周期': period,
        '归一化指标名称': '经营利润',
        '归一化指标数值': data['Asia_Profit'] * 1000 * jpy_to_cny,
        '归一化计算逻辑/折算说明': '百万日元×1000×0.048=千元人民币',
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
print("\n验证美津浓数据:")
mizuno = df_combined[df_combined['公司名称'].str.contains('美津浓|Mizuno', case=False, na=False)]
for idx, row in mizuno.iterrows():
    if '%' not in str(row['单位']):
        print(f"{row['报告周期']} | {row['区域']} | {row['指标名称（原始）'][:20]} | G={row['数据值']} | H={row['单位']} | M={row['归一化指标数值']}")

print(f"\n✅ 已更新美津浓数据，共{len(new_rows)}条记录")
print("\n计算逻辑: 百万日元×1000×0.048=千元人民币")