import pandas as pd
from datetime import datetime
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

db_path = r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务数据库_标准模板v2.xlsx'

print("="*80)
print("更新Database - Adidas大中华区完整数据")
print("="*80)

# 汇率 EUR/CNY (来自汇率及口径说明)
eur_rates = {'FY2023': 7.85, 'FY2024': 8.17, 'FY2025': 8.30}

# Adidas大中华区完整数据 (来源: annual-report-adidas-ar25.pdf 第111页, adidas_annual_report_2024.pdf 第113页)
adidas_gc_data = {
    'FY2025': {
        'Revenue': 3623,  # €M
        'Gross Profit': 1904,  # €M (直接披露)
        'Gross Margin': 52.6,  # %
        'OpProfit': 802,  # €M
        'OpMargin': 22.1,  # %
        'Source': 'annual-report-adidas-ar25.pdf',
        'Page': '111'
    },
    'FY2024': {
        'Revenue': 3459,  # €M
        'Gross Profit': round(3459 * 0.496, 0),  # €M (计算: 1717)
        'Gross Margin': 49.6,  # %
        'OpProfit': 714,  # €M
        'OpMargin': 20.6,  # %
        'Source': 'adidas_annual_report_2024_EN_Final_secured.pdf',
        'Page': '113'
    },
    'FY2023': {
        'Revenue': 3190,  # €M
        'Gross Profit': round(3190 * 0.487, 0),  # €M (计算: 1554)
        'Gross Margin': 48.7,  # %
        'OpProfit': 553,  # €M
        'OpMargin': 17.3,  # %
        'Source': 'adidas_annual_report_2024_EN_Final_secured.pdf',
        'Page': '113'
    }
}

print("\nAdidas大中华区数据:")
for fy, data in adidas_gc_data.items():
    print(f"{fy}: 收入=€{data['Revenue']}M, 毛利率={data['Gross Margin']}%, 经营利润=€{data['OpProfit']}M")

# ============== 读取Database ==============
df = pd.read_excel(db_path, sheet_name='Database')
print(f"\n原始Database行数: {len(df)}")

# ============== 删除旧的Adidas大中华区数据 ==============
adidas_mask = (df['公司名称'].str.contains('Adidas', case=False, na=False)) & \
              (df['区域'].str.contains('大中华|China|亚太', case=False, na=False))
old_count = adidas_mask.sum()
df_cleaned = df[~adidas_mask].copy()
print(f"删除旧Adidas大中华区数据行数: {old_count}")
print(f"清理后Database行数: {len(df_cleaned)}")

# ============== 生成新数据行 ==============
new_rows = []

for fy, data in adidas_gc_data.items():
    rate = eur_rates[fy]
    
    # Revenue
    new_rows.append({
        '#': 5,
        '公司名称': 'Adidas AG',
        '品牌名称': 'TTL',
        '区域': '大中华区',
        '指标名称（原始）': 'Net sales',
        '报告周期': fy,
        '数据值': data['Revenue'] * 1000000,
        '单位': 'EUR',
        '数据来源': data['Source'],
        '所在页码': data['Page'],
        '原文摘录': f'Net sales €{data["Revenue"]} million',
        '归一化周期': fy,
        '归一化指标名称': '营业收入',
        '归 一化指标数值': data['Revenue'] * 1000 * rate,
        '归一化计算逻辑/折算说明': f'百万欧元×{rate}×1000=千元RMB',
        '备注（披露范围等）': '大中华区',
        '最后更新': datetime.now().strftime('%Y-%m-%d')
    })
    
    # Gross Profit
    new_rows.append({
        '#': 5,
        '公司名称': 'Adidas AG',
        '品牌名称': 'TTL',
        '区域': '大中华区',
        '指标名称（原始）': 'Gross profit',
        '报告周期': fy,
        '数据值': data['Gross Profit'] * 1000000,
        '单位': 'EUR',
        '数据来源': data['Source'],
        '所在页码': data['Page'],
        '原文摘录': f'Gross profit €{data["Gross Profit"]} million',
        '归一化周期': fy,
        '归一化指标名称': '毛利',
        '归 一化指标数值': data['Gross Profit'] * 1000 * rate,
        '归一化计算逻辑/折算说明': f'百万欧元×{rate}×1000=千元RMB',
        '备注（披露范围等）': '大中华区',
        '最后更新': datetime.now().strftime('%Y-%m-%d')
    })
    
    # Gross Margin
    new_rows.append({
        '#': 5,
        '公司名称': 'Adidas AG',
        '品牌名称': 'TTL',
        '区域': '大中华区',
        '指标名称（原始）': 'Gross margin',
        '报告周期': fy,
        '数据值': data['Gross Margin'],
        '单位': '%',
        '数据来源': data['Source'],
        '所在页码': data['Page'],
        '原文摘录': f'Gross margin {data["Gross Margin"]}%',
        '归一化周期': fy,
        '归一化指标名称': '毛利率',
        '归 一化指标数值': data['Gross Margin'],
        '归一化计算逻辑/折算说明': '直接使用原始百分比',
        '备注（披露范围等）': '大中华区',
        '最后更新': datetime.now().strftime('%Y-%m-%d')
    })
    
    # Operating Profit
    new_rows.append({
        '#': 5,
        '公司名称': 'Adidas AG',
        '品牌名称': 'TTL',
        '区域': '大中华区',
        '指标名称（原始）': 'Operating profit',
        '报告周期': fy,
        '数据值': data['OpProfit'] * 1000000,
        '单位': 'EUR',
        '数据来源': data['Source'],
        '所在页码': data['Page'],
        '原文摘录': f'Operating profit €{data["OpProfit"]} million',
        '归一化周期': fy,
        '归一化指标名称': '经营利润',
        '归 一化指标数值': data['OpProfit'] * 1000 * rate,
        '归一化计算逻辑/折算说明': f'百万欧元×{rate}×1000=千元RMB',
        '备注（披露范围等）': '大中华区',
        '最后更新': datetime.now().strftime('%Y-%m-%d')
    })
    
    # Operating Margin
    new_rows.append({
        '#': 5,
        '公司名称': 'Adidas AG',
        '品牌名称': 'TTL',
        '区域': '大中华区',
        '指标名称（原始）': 'Operating margin',
        '报告周期': fy,
        '数据值': data['OpMargin'],
        '单位': '%',
        '数据来源': data['Source'],
        '所在页码': data['Page'],
        '原文摘录': f'Operating margin {data["OpMargin"]}%',
        '归一化周期': fy,
        '归一化指标名称': '经营利润率',
        '归 一化指标数值': data['OpMargin'],
        '归一化计算逻辑/折算说明': '直接使用原始百分比',
        '备注（披露范围等）': '大中华区',
        '最后更新': datetime.now().strftime('%Y-%m-%d')
    })

new_df = pd.DataFrame(new_rows)
print(f"新增Adidas大中华区数据行数: {len(new_df)}")

# ============== 合并并保存 ==============
df_final = pd.concat([df_cleaned, new_df], ignore_index=True)
print(f"合并后Database行数: {len(df_final)}")

df_final.to_excel(db_path, sheet_name='Database', index=False)
print(f"\n✅ 已更新: {db_path}")

# ============== 验证 ==============
print("\n" + "="*80)
print("验证 - Adidas大中华区数据:")
print("="*80)

df_verify = pd.read_excel(db_path, sheet_name='Database')
adidas_verify = df_verify[(df_verify['公司名称'].str.contains('Adidas', case=False, na=False)) & 
                           (df_verify['区域'] == '大中华区')]

print(f"\nAdidas大中华区数据 ({len(adidas_verify)} 行):")
for fy in ['FY2023', 'FY2024', 'FY2025']:
    fy_data = adidas_verify[adidas_verify['报告周期'] == fy]
    if not fy_data.empty:
        print(f"\n{fy}:")
        for _, row in fy_data.iterrows():
            indicator = row['归一化指标名称']
            value = row['归 一化指标数值']
            unit = row['单位']
            orig_value = row['数据值']
            if unit == '%':
                print(f"  {indicator}: {value}%")
            else:
                print(f"  {indicator}: {value/1000000:.2f}十亿元RMB (€{orig_value/1000000:.0f}M)")

print("\n" + "="*80)
print("✅ 更新完成！")
print("="*80)
