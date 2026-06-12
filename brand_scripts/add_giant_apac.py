"""
添加捷安特亚太区数据
数据来源: Giant 2025 Annual Report (P86) & Giant 2024 Annual Report (P93)
"""
import pandas as pd
from datetime import datetime

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

# ============ 捷安特亚太区数据 ============
# Giant FY2025 Regional Sales (P86): Asia区域 19,472,389 NTD thousands
# Giant FY2024 Regional Sales (P93): Asia区域 30,950,178 NTD thousands
# Note: Giant的"Asia"包含中国大陆及其他亚洲市场

giant_apac_data = [
    # FY2025 亚太区
    {
        '报告周期': 'FY2025',
        '指标名称（原始）': 'Net sales - Asia Pacific',
        '数据值': 19472389,
        '单位': '千新台币元',
        '原文摘录': 'Asia Sales value 19,472,389 NTD thousands (FY2025, 32.32% of total)',
        'source_file': 'Giant 2025_Annual_Report_EN.pdf',
        'page': 86,
    },
    # FY2024 亚太区
    {
        '报告周期': 'FY2024',
        '指标名称（原始）': 'Net sales - Asia Pacific',
        '数据值': 30950178,
        '单位': '千新台币元',
        '原文摘录': 'Asia Sales value 30,950,178 NTD thousands (FY2024, 43.42% of total)',
        'source_file': 'Giant 2024_annual_report.pdf',
        'page': 93,
    },
]

# 指标中文映射
indicator_cn_map = {
    'Net sales - Asia Pacific': '营业收入',
}

# 检查已存在的记录
giant_mask = df['公司名称'].str.contains('Giant|捷安特', case=False, na=False)
apac_mask = df['区域'] == '亚太区'

existing = df[giant_mask & apac_mask]
print(f"已存在的捷安特亚太区记录数: {len(existing)}")

# 添加新记录
new_rows = []
today = datetime.now().strftime('%Y-%m-%d')

for item in giant_apac_data:
    fy = item['报告周期']
    indicator = item['指标名称（原始）']
    dup_mask = giant_mask & (df['区域'] == '亚太区') & \
               (df['报告周期'] == fy) & \
               (df['指标名称（原始）'] == indicator)

    if dup_mask.any():
        print(f"  跳过已存在: {fy} | {indicator}")
        continue

    val = item['数据值']
    unit = item['单位']
    orig = item['原文摘录']
    source_file = item['source_file']
    page_num = item['page']

    # 新台币转人民币约 0.23 (TWD to CNY)
    twd_to_cny = 0.23
    if unit == '千新台币元':
        normalized_val = val * twd_to_cny  # 千元人民币
        calc_logic = '千新台币元×0.23=千元人民币'
    else:
        normalized_val = val
        calc_logic = ''

    new_row = {
        '#': len(df) + len(new_rows) + 1,
        '公司名称': '捷安特股份有限公司',
        '品牌名称': 'GIANT',
        '区域': '亚太区',
        '指标名称（原始）': indicator,
        '报告周期': fy,
        '数据值': val,
        '单位': unit,
        '数据来源': source_file,
        '所在页码': page_num,
        '原文摘录': orig,
        '归一化周期': fy,
        '归一化指标名称': indicator_cn_map.get(indicator, ''),
        '归一化指标数值': normalized_val,
        '归一化计算逻辑/折算说明': calc_logic,
        '备注（披露范围等）': '亚太区(含中国大陆)',
        '最后更新': today,
    }
    new_rows.append(new_row)
    print(f"  + 添加: {fy} | {indicator} | {val} 千新台币 -> {normalized_val} 千元")

if new_rows:
    df_new = pd.DataFrame(new_rows)
    df = pd.concat([df, df_new], ignore_index=True)
    df.to_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database', index=False)
    print(f"\n✅ 已添加 {len(new_rows)} 条捷安特亚太区记录")
else:
    print("\n⚠️ 没有新记录需要添加")

# 验证
print("\n=== 验证捷安特亚太区数据 ===")
giant_apac = df[(df['公司名称'].str.contains('Giant|捷安特', case=False, na=False)) & (df['区域'] == '亚太区')]
print(giant_apac[['报告周期', '指标名称（原始）', '数据值', '单位', '归一化指标数值']].to_string(index=False))
