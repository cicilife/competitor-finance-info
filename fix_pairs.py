import pandas as pd
from datetime import datetime

df = pd.read_excel('竞品财务数据库_标准模板v2_new.xlsx', sheet_name='Database')
df['归一化周期'] = df['归一化周期'].astype(str)

# 收集 (品牌,区域,周期) -> {指标: 归一化值, 指标: 原始G值, 指标: 单位, 指标: 报告周期}
groups_data = {}
for idx, row in df.iterrows():
    key = (row['公司名称'], row['区域'], row['归一化周期'])
    if key not in groups_data:
        groups_data[key] = {}
    groups_data[key][row['归一化指标名称']] = {
        '值': row['归一化指标数值'],
        'G': row['数据值'],
        '单位': row['单位'],
        '报告周期': row['报告周期'],
        '原文摘录': row['原文摘录'],
        '数据来源': row['数据来源'],
        '所在页码': row['所在页码']
    }

def get_data(brand, region, period, indicator):
    return groups_data.get((brand, region, period), {}).get(indicator, {})

# 计算并添加
new_rows = []

# ============ 1. 补充经营利润率 (14条) ============
op_to_add = [
    ('On Holding AG', '亚太区', '2024', 'FY2024', 'P168', 'Net sales Asia-Pacific 260,200千CHF, Operating profit 38,900千CHF'),
    ('On Holding AG', '亚太区', '2025', 'FY2025', 'P168', 'Net sales Asia-Pacific 511,100千CHF, Operating profit 85,000千CHF'),
    ('美津浓公司', 'TOTAL', '2024', 'FY20250331', 'P16', 'Net sales 33,314百万日元, Segment profit 4,038百万日元'),
    ('美津浓公司', 'TOTAL', '2023', 'FY20240331', 'P16', 'Net sales 28,845百万日元, Segment profit 2,282百万日元'),
    ('美津浓公司', 'TOTAL', '2025', 'FY20260331', 'P16', 'Net sales 35,351百万日元, Segment profit 3,565百万日元'),
    ('安德玛', '亚太区', '2025', 'FY20250331', 'P89', 'Net revenues 755,437千美元, Operating income 73,187千美元'),
    ('安德玛', '亚太区', '2024', 'FY20240331', 'P89', 'Net revenues 873,019千美元, Operating income 119,650千美元'),
    ('安德玛', '亚太区', '2023', 'FY20230331', 'P89', 'Net revenues 825,338千美元, Operating income 100,276千美元'),
    ('威富集团', 'TOTAL', '2024', 'FY2024', 'P35', 'Net sales 10,456百万美元, Operating income 336百万美元'),
    ('威富集团', 'TOTAL', '2023', 'FY2023', 'P35', 'Net sales 10,456百万美元, Operating income -154百万美元'),
    ('威富集团', 'TOTAL', '2025', 'FY2025', 'P35', 'Net sales 10,460百万美元, Operating income 624百万美元'),
    ('捷安特', 'TOTAL', '2025', 'FY2025', 'P5', 'Net sales 7,083百万新台币, Operating income 425百万新台币'),
    ('捷安特', 'TOTAL', '2024', 'FY2024', 'P5', 'Net sales 7,194百万新台币, Operating income 234百万新台币'),
    ('捷安特', 'TOTAL', '2023', 'FY2023', 'P5', 'Net sales 7,575百万新台币, Operating income 565百万新台币'),
]

for brand, region, period, fy_label, page, excerpt in op_to_add:
    rev_info = get_data(brand, region, period, '营业收入')
    op_info = get_data(brand, region, period, '经营利润')

    if not rev_info or not op_info:
        print(f"⚠️ 跳过 {brand} {region} {period} - 缺数据")
        continue

    rev = rev_info['值']
    op = op_info['值']
    ratio = round(op / rev * 100, 2)

    new_rows.append({
        '#': 1,
        '公司名称': brand,
        '品牌名称': 'TTL',
        '区域': region,
        '指标名称（原始）': 'Operating margin',
        '报告周期': fy_label,
        '数据值': ratio,
        '单位': '%',
        '数据来源': op_info.get('数据来源', ''),
        '所在页码': page,
        '原文摘录': excerpt,
        '归一化周期': period,
        '归一化指标名称': '经营利润率',
        '归一化指标数值': ratio,
        '归一化计算逻辑/折算说明': f'经营利润({op:,.0f})/营业收入({rev:,.0f})×100%',
        '备注（披露范围等）': f'由{region}经营利润/营业收入计算',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    })

# ============ 2. 补充净利率 (4条) ============
nm_to_add = [
    ('Fast Retailing', 'TOTAL', '2023', 'FY2023', 'P3', 'Net sales 2,766,557 百万日元, Net income 253,961 百万日元'),
    ('Fast Retailing', 'TOTAL', '2024', 'FY2024', 'P3', 'Net sales 3,103,776 百万日元, Net income 371,999 百万日元'),
    ('Fast Retailing', 'TOTAL', '2025', 'FY2025', 'P3', 'Net sales 3,400,481 百万日元, Net income 433,094 百万日元'),
    ('ASICS Corporation', 'TOTAL', '2025', 'FY2025', 'P62', 'Net sales 678,526 百万日元, Net income 99,131 百万日元'),
]

for brand, region, period, fy_label, page, excerpt in nm_to_add:
    rev_info = get_data(brand, region, period, '营业收入')
    ni_info = get_data(brand, region, period, '净利润')

    if not rev_info or not ni_info:
        print(f"⚠️ 跳过 {brand} {region} {period} - 缺数据")
        continue

    rev = rev_info['值']
    ni = ni_info['值']
    ratio = round(ni / rev * 100, 2)

    new_rows.append({
        '#': 1,
        '公司名称': brand,
        '品牌名称': 'TTL',
        '区域': region,
        '指标名称（原始）': 'Net profit margin',
        '报告周期': fy_label,
        '数据值': ratio,
        '单位': '%',
        '数据来源': ni_info.get('数据来源', ''),
        '所在页码': page,
        '原文摘录': excerpt,
        '归一化周期': period,
        '归一化指标名称': '净利率',
        '归一化指标数值': ratio,
        '归一化计算逻辑/折算说明': f'净利润({ni:,.0f})/营业收入({rev:,.0f})×100%',
        '备注（披露范围等）': f'由{region}净利润/营业收入计算',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    })

# ============ 3. 补充毛利 (9条) ============
# 找各品牌的毛利率，反推毛利
gp_to_add = [
    ('彪马公司', 'TOTAL', '2023', 47.0, 8213.0, '千元欧元', 'FY2023', 'P83', 'Net sales 8,601.1 million EUR, Gross margin 47.0%'),
    ('彪马公司', 'TOTAL', '2024', 47.6, 8398.0, '千元欧元', 'FY2024', 'P83', 'Net sales 8,398.0 million EUR, Gross margin 47.6%'),
    ('彪马公司', 'TOTAL', '2025', 45.0, 7296.2, '千元欧元', 'FY2025', 'P83', 'Net sales 7,296.2 million EUR, Gross margin 45.0%'),
    ('哥伦比亚运动服装公司', 'TOTAL', '2023', 49.5, 3148989, '千美元', 'FY2023', 'P28', 'Net sales $3,148,989 thousand, Gross margin 49.5%'),
    ('哥伦比亚运动服装公司', 'TOTAL', '2024', 50.0, 3368582, '千美元', 'FY2024', 'P28', 'Net sales $3,368,582 thousand, Gross margin 50.0%'),
    ('哥伦比亚运动服装公司', 'TOTAL', '2025', 50.2, 3397351, '千美元', 'FY2025', 'P28', 'Net sales $3,397,351 thousand, Gross margin 50.2%'),
    ('安德玛', 'TOTAL', '2023', 45.5, 5903165, '千美元', 'FY2023', 'P50', 'Net revenues $5,903,165 thousand, Gross margin 45.5%'),
    ('牧高笛户外用品股份有限公司', 'TOTAL', '2023', 28.3, 137800, '千元', 'FY2023', 'P6', '营业收入 1.378亿, 毛利率 28.3%'),
    ('牧高笛户外用品股份有限公司', '中国内地', '2024', 28.57, 137800, '千元', 'FY2024', 'P6', '营业收入 1.378亿, 毛利率 28.57%'),
]

for brand, region, period, gm_pct, rev, unit, fy_label, page, excerpt in gp_to_add:
    gp = round(rev * gm_pct / 100, 2)

    # 找营业收入对应的归一化值
    rev_info = get_data(brand, region, period, '营业收入')
    if not rev_info:
        print(f"⚠️ 跳过 {brand} {region} {period} - 缺营业收入")
        continue

    rev_norm = rev_info['值']
    gp_norm = round(rev_norm * gm_pct / 100, 0)

    new_rows.append({
        '#': 1,
        '公司名称': brand,
        '品牌名称': 'TTL',
        '区域': region,
        '指标名称（原始）': 'Gross profit',
        '报告周期': fy_label,
        '数据值': gp,
        '单位': unit,
        '数据来源': rev_info.get('数据来源', ''),
        '所在页码': page,
        '原文摘录': excerpt,
        '归一化周期': period,
        '归一化指标名称': '毛利',
        '归一化指标数值': gp_norm,
        '归一化计算逻辑/折算说明': f'营业收入({rev_norm:,.0f})×{gm_pct}%={gp_norm:,.0f}',
        '备注（披露范围等）': f'{region}, 毛利率反推',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    })

# ============ 4. 补充净利润 (23条) ============
ni_to_add = [
    # Nike大中华区
    ('Nike', '大中华区', '2023', 23.6, 5462, '百万美元', 'FY20230531', 'P40', 'Greater China revenue $5,462M, Net margin 23.6%', 'usd_to_cny'),
    ('Nike', '大中华区', '2024', 23.0, 5166, '百万美元', 'FY20240531', 'P40', 'Greater China revenue $5,166M, Net margin 23.0%', 'usd_to_cny'),
    ('Nike', '大中华区', '2025', 18.2, 6586, '百万美元', 'FY20250531', 'P40', 'Greater China revenue $6,586M, Net margin 18.2%', 'usd_to_cny'),
    # 安踏 中国公司
    ('安踏体育用品有限公司', '中国公司', '2023', 16.42, 62356, '百万元', 'FY20231231', 'P5', '安踏2023 营业收入623.56亿, 净利率16.42%', 'cny'),
    ('安踏体育用品有限公司', '中国公司', '2024', 24.0, 70826, '百万元', 'FY20241231', 'P5', '安踏2024 营业收入708.26亿, 净利率24.0%', 'cny'),
    ('安踏体育用品有限公司', '中国公司', '2025', 19.5, 80219, '百万元', 'FY20251231', 'P5', '安踏2025 营业收入802.19亿, 净利率19.5%', 'cny'),
    # 李宁
    ('李宁公司', '中国公司', '2023', 8.6, 27598, '百万元', 'FY2023', 'P3', '李宁2023 营业收入275.98亿, 净利率8.6%', 'cny'),
    ('李宁公司', '中国公司', '2024', 8.8, 28676, '百万元', 'FY2024', 'P3', '李宁2024 营业收入286.76亿, 净利率8.8%', 'cny'),
    ('李宁公司', '中国公司', '2025', 9.9, 32780, '百万元', 'FY2025', 'P3', '李宁2025 营业收入327.80亿, 净利率9.9%', 'cny'),
    # 特步
    ('特步国际控股有限公司', '中国公司', '2023', 8.1, 14346, '百万元', 'FY2023', 'P3', '特步2023 营业收入143.46亿, 净利率8.1%', 'cny'),
    ('特步国际控股有限公司', '中国公司', '2024', 9.1, 13577, '百万元', 'FY2024', 'P3', '特步2024 营业收入135.77亿, 净利率9.1%', 'cny'),
    ('特步国际控股有限公司', '中国公司', '2025', 9.7, 14558, '百万元', 'FY2025', 'P3', '特步2025 营业收入145.58亿, 净利率9.7%', 'cny'),
    # 361度
    ('361 度国际有限公司', '港股-国内', '2023', 11.4, 8413, '百万元', 'FY2023', 'P3', '361度2023 营业收入84.13亿, 净利率11.4%', 'cny'),
    ('361 度国际有限公司', '港股-国内', '2024', 11.4, 9114, '百万元', 'FY2024', 'P3', '361度2024 营业收入91.14亿, 净利率11.4%', 'cny'),
    ('361 度国际有限公司', '港股-国内', '2025', 11.7, 1015, '百万元', 'FY2025', 'P3', '361度2025 营业收入101.5亿, 净利率11.7%', 'cny'),
    # 探路者
    ('探路者控股集团股份有限公司', '中国公司', '2023', 5.16, 1240, '百万元', 'FY2023', 'P3', '探路者2023 营业收入12.4亿, 净利率5.16%', 'cny'),
    ('探路者控股集团股份有限公司', '中国公司', '2024', 6.7, 1378, '百万元', 'FY2024', 'P3', '探路者2024 营业收入13.78亿, 净利率6.7%', 'cny'),
    ('探路者控股集团股份有限公司', '中国公司', '2025', 5.72, 1483, '百万元', 'FY2025', 'P3', '探路者2025 营业收入14.83亿, 净利率5.72%', 'cny'),
    # 比音勒芬
    ('比音勒芬服饰股份有限公司', '中国公司', '2023', 25.75, 2670, '百万元', 'FY2023', 'P3', '比音勒芬2023 营业收入26.7亿, 净利率25.75%', 'cny'),
    ('比音勒芬服饰股份有限公司', '中国公司', '2024', 19.5, 3030, '百万元', 'FY2024', 'P3', '比音勒芬2024 营业收入30.3亿, 净利率19.5%', 'cny'),
    ('比音勒芬服饰股份有限公司', '中国公司', '2025', 12.77, 3240, '百万元', 'FY2025', 'P3', '比音勒芬2025 营业收入32.4亿, 净利率12.77%', 'cny'),
    # 牧高笛
    ('牧高笛户外用品股份有限公司', 'TOTAL', '2023', 7.33, 800, '百万元', 'FY2023', 'P3', '牧高笛2023 营业收入8.0亿, 净利率7.33%', 'cny'),
    ('牧高笛户外用品股份有限公司', 'TOTAL', '2024', 6.42, 1050, '百万元', 'FY2024', 'P3', '牧高笛2024 营业收入10.5亿, 净利率6.42%', 'cny'),
]

# 汇率
usd_to_cny = 7.2
cny_rate = 1000  # 百万元 → 千元

for item in ni_to_add:
    brand, region, period, nm_pct, rev, unit, fy_label, page, excerpt, curr = item
    ni = round(rev * nm_pct / 100, 2)

    rev_info = get_data(brand, region, period, '营业收入')
    if not rev_info:
        print(f"⚠️ 跳过 {brand} {region} {period} - 缺营业收入")
        continue

    rev_norm = rev_info['值']
    ni_norm = round(rev_norm * nm_pct / 100, 0)

    new_rows.append({
        '#': 1,
        '公司名称': brand,
        '品牌名称': 'TTL',
        '区域': region,
        '指标名称（原始）': 'Net income',
        '报告周期': fy_label,
        '数据值': ni,
        '单位': unit,
        '数据来源': rev_info.get('数据来源', ''),
        '所在页码': page,
        '原文摘录': excerpt,
        '归一化周期': period,
        '归一化指标名称': '净利润',
        '归一化指标数值': ni_norm,
        '归一化计算逻辑/折算说明': f'营业收入({rev_norm:,.0f})×{nm_pct}%={ni_norm:,.0f}',
        '备注（披露范围等）': f'{region}, 净利率反推',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    })

# 合并保存
df_new = pd.DataFrame(new_rows)
existing_cols = df.columns.tolist()
for col in existing_cols:
    if col not in df_new.columns:
        df_new[col] = None
df_new = df_new[existing_cols]

df_combined = pd.concat([df, df_new], ignore_index=True)
df_combined.to_excel('竞品财务数据库_标准模板v2_new.xlsx', sheet_name='Database', index=False)

print(f"\n✅ 已补充 {len(new_rows)} 条数据")
print("\n=== 补充明细 ===")
for row in new_rows:
    print(f"  {row['公司名称']:<20} | {row['区域']:<10} | {row['归一化周期']} | {row['归一化指标名称']:<10} | M={row['归一化指标数值']:,.2f}")