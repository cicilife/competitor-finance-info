import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')
jpy_to_cny = 0.048

print("=== ASICS数据修正 ===\n")

# 1. 修正TOTAL FY2023 Net sales等 (单位标JPY但数值是元)
asics_total_2023_mask = (
    df['公司名称'].str.contains('ASICS', case=False, na=False) &
    (df['区域'] == 'TOTAL') &
    (df['报告周期'] == 'FY2023') &
    (df['单位'] == 'JPY')
)

# ASICS 2023: Net sales 570,463百万日元, Gross profit 296,896百万, Operating profit 54,215百万, Net profit 35,453百万
asics_2023_data = {
    'Net sales': 570463,
    'Gross profit': 296896,
    'Operating profit': 54215,
    'Net profit': 35453
}

for idx in df[asics_total_2023_mask].index:
    indicator = df.loc[idx, '指标名称（原始）']
    orig = str(df.loc[idx, '原文摘录']) if pd.notna(df.loc[idx, '原文摘录']) else ''

    for key, val in asics_2023_data.items():
        if key.lower() in indicator.lower() or key.replace(' ', '').lower() in indicator.lower():
            df.loc[idx, '数据值'] = val
            df.loc[idx, '单位'] = '百万日元'
            df.loc[idx, '归一化指标数值'] = val * 1000 * jpy_to_cny
            df.loc[idx, '归一化计算逻辑/折算说明'] = '百万日元×1000×0.048=千元人民币'
            print(f"  修正: {indicator} -> G={val}百万日元 -> M={val * 1000 * jpy_to_cny}")
            break

# 2. 修正SG&A 2023/2025数据 (从财报)
# ASICS 2024 SG&A=278,766百万, 2025=318,112百万, 2023=242,680百万
sg_a_data = {
    'FY2025': 318112,
    'FY2024': 278766,
    'FY2023': 242680
}

sg_a_mask = (
    df['公司名称'].str.contains('ASICS', case=False, na=False) &
    (df['区域'] == 'TOTAL') &
    (df['指标名称（原始）'].str.contains('SG&A expenses', case=False, na=False)) &
    (df['单位'] == '百万日元')
)

for idx in df[sg_a_mask].index:
    period = df.loc[idx, '报告周期']
    if period in sg_a_data:
        val = sg_a_data[period]
        df.loc[idx, '数据值'] = val
        df.loc[idx, '单位'] = '百万日元'
        df.loc[idx, '归一化指标数值'] = val * 1000 * jpy_to_cny
        df.loc[idx, '归一化计算逻辑/折算说明'] = '百万日元×1000×0.048=千元人民币'
        print(f"  SG&A修正: {period} -> G={val}百万日元 -> M={val * 1000 * jpy_to_cny}")

# 3. 修正大中华区数据单位 (当前已经是百万日元)
gc_mask = (
    df['公司名称'].str.contains('ASICS', case=False, na=False) &
    (df['区域'] == '大中华区') &
    (df['单位'] == '百万日元')
)

for idx in df[gc_mask].index:
    indicator = df.loc[idx, '指标名称（原始）']
    val = df.loc[idx, '数据值']
    # 确认数据是否需要调整 - 检查M列计算
    if '%' not in indicator and 'days' not in indicator:
        new_m = val * 1000 * jpy_to_cny
        if df.loc[idx, '归一化指标数值'] != new_m:
            df.loc[idx, '归一化指标数值'] = new_m
            df.loc[idx, '归一化计算逻辑/折算说明'] = '百万日元×1000×0.048=千元人民币'
            print(f"  大中华区修正: {indicator} M={new_m}")

# 保存
df.to_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database', index=False)

print("\n=== 验证 ===")
asics = df[df['公司名称'].str.contains('ASICS', case=False, na=False)]
gc = asics[asics['区域'] == '大中华区']
for idx, row in gc.iterrows():
    print(f"  {row['报告周期']} | {row['指标名称（原始）'][:30]:<30} | G={row['数据值']} | {row['单位']} | M={row['归一化指标数值']}")

print("\n✅ 已保存")