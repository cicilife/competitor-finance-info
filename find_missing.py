import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2_new.xlsx', sheet_name='Database')

def find_value(df, brand, region, period, indicator_name):
    """查找特定 (品牌,区域,周期,指标) 的归一化值"""
    mask = (
        (df['公司名称'] == brand) &
        (df['区域'] == region) &
        (df['归一化周期'] == str(period)) &
        (df['归一化指标名称'] == indicator_name)
    )
    if mask.any():
        return df.loc[mask, '归一化指标数值'].iloc[0]
    return None

def find_period_value(df, brand, region, period, kws):
    """模糊匹配"""
    mask = (
        (df['公司名称'] == brand) &
        (df['区域'] == region) &
        (df['归一化周期'] == str(period)) &
        df['归一化指标名称'].str.contains('|'.join(kws), na=False) &
        ~df['归一化指标名称'].str.contains('率|费用率', na=False)
    )
    if mask.any():
        return df.loc[mask, '归一化指标数值'].iloc[0], df.loc[mask, '归一化指标名称'].iloc[0]
    return None, None

def add_ratio_row(df, brand, brand_short, region, period, abs_val, abs_indicator, ratio_indicator, fy_label, source, page, excerpt):
    """添加比率行"""
    # 找同区域同期营业收入
    rev = find_value(df, brand, region, str(period), '营业收入')
    if not rev or rev == 0:
        return False

    ratio_val = round(abs_val / rev * 100, 2)

    new_row = {
        '#': 1,
        '公司名称': brand,
        '品牌名称': brand_short,
        '区域': region,
        '指标名称（原始）': abs_indicator + ' ratio',
        '报告周期': fy_label,
        '数据值': ratio_val,
        '单位': '%',
        '数据来源': source,
        '所在页码': page,
        '原文摘录': excerpt,
        '归一化周期': str(period),
        '归一化指标名称': ratio_indicator,
        '归一化指标数值': ratio_val,
        '归一化计算逻辑/折算说明': f'{abs_indicator}({abs_val:,.0f})/营业收入({rev:,.0f})×100%',
        '备注（披露范围等）': f'集团{region}, 由{abs_indicator}/营业收入计算',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    }
    return new_row

# 读取需要补充的所有数据并计算
# 从原数据库里读取
new_rows = []

# 毛利-毛利率
gp_pairs = [
    # adidas
    ('adidas AG', 'adidas', 'TOTAL', '2024', '2024', 11734, 'Gross profit', '毛利率', 'annual-report-adidas-ar24.pdf', '183', 'Gross profit €11,734 million'),
    # Columbia: 需要看是否有毛利数据
    # Under Armour
    # Puma - 需要从原数据读取
    # 牧高笛
]

# 找有毛利没毛利率的
companies = df['公司名称'].dropna().unique()
need_gp = []
for brand in companies:
    for region in df[df['公司名称']==brand]['区域'].unique():
        for period in df[(df['公司名称']==brand) & (df['区域']==region)]['归一化周期'].unique():
            if pd.isna(period):
                continue
            gp_v, gp_n = find_period_value(df, brand, region, str(period), ['毛利'])
            gm_v = find_value(df, brand, region, str(period), '毛利率')
            if gp_v and not gm_v:
                need_gp.append((brand, region, str(period), gp_v, gp_n))
print("有毛利无毛利率:", need_gp)

# 找有经营利润无经营利润率
need_op = []
for brand in companies:
    for region in df[df['公司名称']==brand]['区域'].unique():
        for period in df[(df['公司名称']==brand) & (df['区域']==region)]['归一化周期'].unique():
            if pd.isna(period):
                continue
            op_v, op_n = find_period_value(df, brand, region, str(period), ['经营利润', '经营溢利', 'EBIT', 'Operating profit'])
            om_v = find_value(df, brand, region, str(period), '经营利润率')
            if op_v and not om_v:
                need_op.append((brand, region, str(period), op_v, op_n))
print("\n有经营利润无经营利润率:", need_op)

# 找有净利润无净利率
need_ni = []
for brand in companies:
    for region in df[df['公司名称']==brand]['区域'].unique():
        for period in df[(df['公司名称']==brand) & (df['区域']==region)]['归一化周期'].unique():
            if pd.isna(period):
                continue
            ni_v, ni_n = find_period_value(df, brand, region, str(period), ['净利润'])
            nm_v = find_value(df, brand, region, str(period), '净利率')
            if ni_v and not nm_v:
                need_ni.append((brand, region, str(period), ni_v, ni_n))
print("\n有净利润无净利率:", need_ni)

# 找有净利率无净利润
need_nm = []
for brand in companies:
    for region in df[df['公司名称']==brand]['区域'].unique():
        for period in df[(df['公司名称']==brand) & (df['区域']==region)]['归一化周期'].unique():
            if pd.isna(period):
                continue
            ni_v, ni_n = find_period_value(df, brand, region, str(period), ['净利润'])
            nm_v = find_value(df, brand, region, str(period), '净利率')
            if nm_v and not ni_v:
                need_nm.append((brand, region, str(period), nm_v))
print("\n有净利率无净利润:", need_nm)