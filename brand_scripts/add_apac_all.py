"""
添加捷安特、奔赴自然(伯希和)亚太区数据
数据来源:
- 捷安特: Giant 2024/2025 Annual Report (FY2024/FY2025, 无FY2023区域数据)
- 奔赴自然: 奔赴自然招股书2025.pdf (P215)
"""
import pandas as pd
from datetime import datetime

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

usd_to_cny = 7.2  # 美元兑人民币
twd_to_cny = 0.23  # 新台币兑人民币
rmb_to_cny = 1.0   # 人民币=人民币

# ============ 捷安特(GIANT)亚太区数据 ============
# 捷安特年报只披露单年区域销售数据，无FY2023对比
# 来源: Giant 2024 Annual Report P93, Giant 2025 Annual Report P86
giant_apac_data = [
    {
        '报告周期': 'FY2025',
        '指标名称（原始）': 'Net sales - Asia Pacific',
        '数据值': 19472389,
        '单位': '千新台币元',
        '原文摘录': 'Asia Sales 19,472,389 NTD thousands (FY2025, 32.32%)',
        'source_file': 'Giant 2025_Annual_Report_EN.pdf',
        'page': 86,
    },
    {
        '报告周期': 'FY2024',
        '指标名称（原始）': 'Net sales - Asia Pacific',
        '数据值': 30950178,
        '单位': '千新台币元',
        '原文摘录': 'Asia Sales 30,950,178 NTD thousands (FY2024, 43.42%)',
        'source_file': 'Giant 2024_annual_report.pdf',
        'page': 93,
    },
]

# ============ 奔赴自然(原伯希和)大中华区数据 ============
# 来源: 奔赴自然招股书2025.pdf P215
# 伯希和是中国内地品牌，营收数据为中国内地总收入
奔赴自然_data = [
    {
        '报告周期': 'FY2025',
        '指标名称（原始）': 'Net sales - China',
        '数据值': 2793000,
        '单位': '千元人民币',
        '原文摘录': '收入由2023年的人民币908.1百万元增加至2024年的人民币1,766.1百万元，并进一步增加至2025年的人民币2,793.0百万元',
        'source_file': '奔赴自然招股书2025.pdf',
        'page': '215',
    },
    {
        '报告周期': 'FY2024',
        '指标名称（原始）': 'Net sales - China',
        '数据值': 1766100,
        '单位': '千元人民币',
        '原文摘录': '收入由2023年的人民币908.1百万元增加至2024年的人民币1,766.1百万元',
        'source_file': '奔赴自然招股书2025.pdf',
        'page': '215',
    },
    {
        '报告周期': 'FY2023',
        '指标名称（原始）': 'Net sales - China',
        '数据值': 908100,
        '单位': '千元人民币',
        '原文摘录': '收入由2023年的人民币908.1百万元',
        'source_file': '奔赴自然招股书2025.pdf',
        'page': '215',
    },
]

# 指标中文映射
indicator_cn_map = {
    'Net sales - Asia Pacific': '营业收入',
    'Net sales - China': '营业收入',
}

# 添加记录
new_rows = []
today = datetime.now().strftime('%Y-%m-%d')

def process_data(data_list, company_name, brand_name, region, conversion_rate, unit):
    for item in data_list:
        fy = item['报告周期']
        indicator = item['指标名称（原始）']
        dup_mask = (df['公司名称'] == company_name) & \
                   (df['品牌名称'] == brand_name) & \
                   (df['区域'] == region) & \
                   (df['报告周期'] == fy) & \
                   (df['指标名称（原始）'] == indicator)
        
        if dup_mask.any():
            print(f"  [跳过] {brand_name} | {fy} (已存在)")
            return
        
        val = item['数据值']
        normalized_val = val * conversion_rate if unit == item['单位'] else val
        calc_logic = f'{item["单位"]}×{conversion_rate}=千元人民币'
        
        new_row = {
            '#': len(df) + len(new_rows) + 1,
            '公司名称': company_name,
            '品牌名称': brand_name,
            '区域': region,
            '指标名称（原始）': indicator,
            '报告周期': fy,
            '数据值': val,
            '单位': item['单位'],
            '数据来源': item['source_file'],
            '所在页码': item['page'],
            '原文摘录': item['原文摘录'],
            '归一化周期': fy,
            '归一化指标名称': indicator_cn_map.get(indicator, ''),
            '归一化指标数值': normalized_val,
            '归一化计算逻辑/折算说明': calc_logic,
            '备注（披露范围等）': region,
            '最后更新': today,
        }
        new_rows.append(new_row)
        print(f"  [新增] {brand_name} | {fy} | {val:,} {item['单位']} -> {normalized_val:,.0f} 千元")

print("="*60)
print("捷安特(GIANT) 亚太区数据")
print("="*60)
process_data(giant_apac_data, '捷安特股份有限公司', 'GIANT', '亚太区', twd_to_cny, '千新台币元')
print("\n备注: 捷安特年报未披露FY2023亚太区区域销售数据")

print("\n" + "="*60)
print("奔赴自然(伯希和) 大中华区数据")
print("="*60)
process_data(奔赴自然_data, '奔赴自然', '奔赴自然', '大中华区', rmb_to_cny, '千元人民币')

if new_rows:
    df_new = pd.DataFrame(new_rows)
    df = pd.concat([df, df_new], ignore_index=True)
    df.to_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database', index=False)
    print(f"\n{'='*60}")
    print(f"✅ 共新增 {len(new_rows)} 条记录")
else:
    print("\n⚠️ 没有新记录需要添加")

# 验证
print("\n" + "="*60)
print("验证 - 亚太区/大中华区数据总览")
print("="*60)
region_mask = (df['区域'] == '亚太区') | (df['区域'] == '大中华区')
region_data = df[region_mask][['公司名称', '品牌名称', '报告周期', '数据值', '单位', '归一化指标数值']].sort_values(['品牌名称', '报告周期'])
print(region_data.to_string(index=False))
