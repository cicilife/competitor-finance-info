import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2_new.xlsx', sheet_name='Database')

def find_value(df, brand, region, period, indicator_name):
    """精确匹配"""
    mask = (
        (df['公司名称'] == brand) &
        (df['区域'] == region) &
        (df['归一化周期'] == str(period)) &
        (df['归一化指标名称'] == indicator_name)
    )
    if mask.any():
        return df.loc[mask, '归一化指标数值'].iloc[0]
    return None

# 4组配对检查
groups = [
    ('毛利', '毛利率'),
    ('经营利润', '经营利润率'),
    ('净利润', '净利率'),
    ('运营费用', '运营费用率')
]

# 排除 净利率(含discontinued) 这类特殊名
for abs_ind, ratio_ind in groups:
    print(f"\n{'='*80}\n{abs_ind}-{ratio_ind} 缺失情况\n{'='*80}")

    companies = df['公司名称'].dropna().unique()
    miss_abs = []  # 有比率无绝对值
    miss_ratio = []  # 有绝对值无比率

    for brand in companies:
        for region in df[df['公司名称']==brand]['区域'].unique():
            for period in df[(df['公司名称']==brand) & (df['区域']==region)]['归一化周期'].unique():
                if pd.isna(period):
                    continue
                period = str(period)
                abs_v = find_value(df, brand, region, period, abs_ind)
                ratio_v = find_value(df, brand, region, period, ratio_ind)

                if abs_v is not None and ratio_v is None:
                    miss_ratio.append((brand, region, period, abs_v))
                elif ratio_v is not None and abs_v is None:
                    miss_abs.append((brand, region, period, ratio_v))

    print(f"  有{ratio_ind}无{abs_ind}: {len(miss_abs)} 条")
    for brand, region, period, ratio_v in miss_abs:
        rev = find_value(df, brand, region, period, '营业收入')
        calc = round(ratio_v * rev / 100, 0) if rev else 0
        print(f"    {brand:<25} | {region:<12} | {period} | {ratio_ind}={ratio_v}% | 推算{abs_ind}={calc:,.0f}")

    print(f"  有{abs_ind}无{ratio_ind}: {len(miss_ratio)} 条")
    for brand, region, period, abs_v in miss_ratio:
        rev = find_value(df, brand, region, period, '营业收入')
        calc = round(abs_v / rev * 100, 2) if rev else 0
        print(f"    {brand:<25} | {region:<12} | {period} | {abs_ind}={abs_v:,.0f} | 营收={rev:,.0f} | 推算{ratio_ind}={calc}%")