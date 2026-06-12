import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2_new.xlsx', sheet_name='Database')

# 四组指标
group1 = ['毛利', '毛利率']
group2 = ['经营利润', '经营利润率']
group3 = ['净利润', '净利率']
group4 = ['运营费用', '运营费用率']

# 把归一化指标名称标准化
df['归一化指标名称'] = df['归一化指标名称'].fillna('')

# 模糊匹配: 检查含有关键词的指标名
def get_count(df, brand, region, period, keywords):
    """统计某品牌+区域+周期 含keywords中任一关键词的数据条数"""
    mask = (
        (df['公司名称'] == brand) &
        (df['区域'] == region) &
        (df['报告周期'] == period) &
        df['归一化指标名称'].str.contains('|'.join(keywords), na=False)
    )
    return mask.sum()

# 找有营业收入和至少一个绝对值指标的行
companies = df['公司名称'].dropna().unique()
print(f"总品牌数: {len(companies)}")

# 统计4组配对
for group_name, kws in [('毛利-毛利率', group1), ('经营利润-经营利润率', group2),
                          ('净利润-净利率', group3), ('运营费用-运营费用率', group4)]:
    print(f"\n{'='*80}\n{group_name}\n{'='*80}")

    # 收集所有 (品牌, 区域, 归一化周期) 组合
    groups = df.groupby(['公司名称', '区域', '归一化周期'])

    need_fix = []
    for (brand, region, period), grp in groups:
        if not period or pd.isna(period):
            continue

        # 检查是否含绝对值指标
        abs_kw = kws[0]  # 毛利/经营利润/净利润/运营费用
        ratio_kw = kws[1]  # 毛利率/经营利润率/净利率/运营费用率

        # 找绝对值
        abs_mask = grp['归一化指标名称'].str.contains(abs_kw, na=False)
        # 排除掉费用率类
        if abs_kw in ['毛利', '净利润', '经营利润']:
            abs_mask = abs_mask & ~grp['归一化指标名称'].str.contains(ratio_kw, na=False)

        # 找比率
        ratio_mask = grp['归一化指标名称'].str.contains(ratio_kw, na=False)

        has_abs = abs_mask.any()
        has_ratio = ratio_mask.any()

        if has_abs and not has_ratio:
            need_fix.append({
                '品牌': brand,
                '区域': region,
                '归一化周期': period,
                '有绝对值': abs_kw,
                '缺比率': ratio_kw
            })
        elif has_ratio and not has_abs:
            need_fix.append({
                '品牌': brand,
                '区域': region,
                '归一化周期': period,
                '有绝对值': '(无)',
                '缺比率': abs_kw
            })

    print(f"  缺配对的数据组合: {len(need_fix)}")
    for item in need_fix[:50]:
        print(f"    {item['品牌']:<20} | {item['区域']:<10} | {item['归一化周期']} | 缺{item['缺比率']} (有{item['有绝对值']})")