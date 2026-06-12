import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2_new.xlsx', sheet_name='Database')

# 把归一化周期转字符串
df['归一化周期'] = df['归一化周期'].astype(str)

# 收集所有 (品牌, 区域, 归一化周期) 组合
groups = df.groupby(['公司名称', '区域', '归一化周期']).size().reset_index()[['公司名称','区域','归一化周期']]
print(f"总组合数: {len(groups)}")

# 检查每组的指标配对
groups_with_rev = set()
groups_with_data = {}  # (品牌,区域,周期) -> {指标: 值}

for idx, row in df.iterrows():
    key = (row['公司名称'], row['区域'], row['归一化周期'])
    if row['归一化指标名称'] == '营业收入':
        groups_with_rev.add(key)
    if key not in groups_with_data:
        groups_with_data[key] = {}
    groups_with_data[key][row['归一化指标名称']] = row['归一化指标数值']

# 找缺配对且有营业收入的
print(f"\n有营业收入的组合数: {len(groups_with_rev)}")

# 检查
need_fix = {
    '有毛利无毛利率': [],
    '有经营利润无经营利润率': [],
    '有净利润无净利率': [],
    '有运营费用无运营费用率': [],
    '有毛利率无毛利': [],
    '有经营利润率无经营利润': [],
    '有净利率无净利润': [],
    '有运营费用率无运营费用': []
}

for key in groups_with_rev:
    brand, region, period = key
    if brand is None or region is None or period == 'nan':
        continue
    data = groups_with_data[key]

    # 毛利-毛利率
    if '毛利' in data and '毛利率' not in data:
        need_fix['有毛利无毛利率'].append((brand, region, period, data.get('毛利')))
    if '毛利率' in data and '毛利' not in data:
        need_fix['有毛利率无毛利'].append((brand, region, period, data.get('毛利率')))

    # 经营利润-经营利润率
    if '经营利润' in data and '经营利润率' not in data:
        need_fix['有经营利润无经营利润率'].append((brand, region, period, data.get('经营利润')))
    if '经营利润率' in data and '经营利润' not in data:
        need_fix['有经营利润率无经营利润'].append((brand, region, period, data.get('经营利润率')))

    # 净利润-净利率
    if '净利润' in data and '净利率' not in data:
        need_fix['有净利润无净利率'].append((brand, region, period, data.get('净利润')))
    if '净利率' in data and '净利润' not in data:
        need_fix['有净利率无净利润'].append((brand, region, period, data.get('净利率')))

    # 运营费用-运营费用率
    if '运营费用' in data and '运营费用率' not in data:
        need_fix['有运营费用无运营费用率'].append((brand, region, period, data.get('运营费用')))
    if '运营费用率' in data and '运营费用' not in data:
        need_fix['有运营费用率无运营费用'].append((brand, region, period, data.get('运营费用率')))

for key, items in need_fix.items():
    print(f"\n{key}: {len(items)} 条")
    for brand, region, period, val in items:
        print(f"  {brand:<25} | {region:<10} | {period} | 值={val}")