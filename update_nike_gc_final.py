import pandas as pd
from datetime import datetime
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

db_path = r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务数据库_标准模板v2.xlsx'
temp_output = r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务数据库_标准模板v2_nike_gc_update.xlsx'

print("="*80)
print("Updating Nike Greater China Data in Database")
print("="*80)

# 汇率 (USD/CNY)
exchange_rates = {
    'FY2023': 7.10,
    'FY2024': 7.24,
    'FY2025': 7.27
}

# Nike Greater China data from PDF (单位：百万美元)
nike_gc_usd = {
    'FY2025': {'Revenue': 6586, 'Gross Profit': 3028, 'Gross Margin': 46.0, 'EBIT': 1602},
    'FY2024': {'Revenue': 7545, 'Gross Profit': 3784, 'Gross Margin': 50.2, 'EBIT': 2309},
    'FY2023': {'Revenue': 7248, 'Gross Profit': 3696, 'Gross Margin': 51.0, 'EBIT': 2283}
}

print("\n原始数据 (百万美元):")
for fy, data in nike_gc_usd.items():
    print(f"{fy}: Revenue=${data['Revenue']}M, GP=${data['Gross Profit']}M, GM={data['Gross Margin']}%, EBIT=${data['EBIT']}M")

# 读取Database
df = pd.read_excel(db_path, sheet_name='Database')
print(f"\n原始Database行数: {len(df)}")

# 1. 删除现有的Nike大中华区数据
nike_gc_mask = (df['公司名称'].str.contains('Nike', case=False, na=False)) & (df['区域'] == '大中华区')
nike_gc_indices = df[nike_gc_mask].index.tolist()
print(f"\nNike大中华区现有数据行索引: {nike_gc_indices}")

# 删除这些行
df_cleaned = df[~nike_gc_mask].copy()
print(f"删除Nike大中华区数据后行数: {len(df_cleaned)}")

# 2. 添加新的Nike大中华区数据
new_rows = []

for fy, data in nike_gc_usd.items():
    rate = exchange_rates[fy]
    
    # Revenue: 转换为千元人民币
    rev_krmb = data['Revenue'] * rate * 1000  # $M * 汇率 = 百万元RMB，再乘1000得到千元
    
    # Gross Profit: 转换为千元人民币
    gp_krmb = data['Gross Profit'] * rate * 1000  # $M * 汇率 = 百万元RMB
    
    # EBIT: 转换为千元人民币
    ebit_krmb = data['EBIT'] * rate * 1000  # $M * 汇率 = 百万元RMB

    # FY2025 Revenue
    new_rows.append({
        '#': 4,
        '公司名称': 'Nike',
        '品牌名称': 'TTL',
        '区域': '大中华区',
        '指标名称（原始）': '营业收入',
        '报告周期': fy,
        '数据值': data['Revenue'] * 1000000,
        '单位': 'USD',
        '数据来源': 'Nike-Inc-2025_10K.pdf',
        '所在页码': '43',
        '原文摘录': f'TOTAL REVENUES ${data["Revenue"]}M',
        '归一化周期': fy,
        '归一化指标名称': '营业收入',
        '归 一化指标数值': rev_krmb,
        '归一化计算逻辑/折算说明': f'百万美元×{rate}×1000=千元RMB',
        '备注（披露范围等）': '大中华区',
        '最后更新': datetime.now().strftime('%Y-%m-%d')
    })

    # Gross Profit
    new_rows.append({
        '#': 4,
        '公司名称': 'Nike',
        '品牌名称': 'TTL',
        '区域': '大中华区',
        '指标名称（原始）': '毛利',
        '报告周期': fy,
        '数据值': data['Gross Profit'] * 1000000,
        '单位': 'USD',
        '数据来源': 'Nike-Inc-2025_10K.pdf',
        '所在页码': '43',
        '原文摘录': f'Gross profit ${data["Gross Profit"]}M',
        '归一化周期': fy,
        '归一化指标名称': '毛利',
        '归 一化指标数值': gp_krmb,
        '归一化计算逻辑/折算说明': f'百万美元×{rate}×1000=千元RMB',
        '备注（披露范围等）': '大中华区',
        '最后更新': datetime.now().strftime('%Y-%m-%d')
    })

    # Gross Margin
    new_rows.append({
        '#': 4,
        '公司名称': 'Nike',
        '品牌名称': 'TTL',
        '区域': '大中华区',
        '指标名称（原始）': '毛利率',
        '报告周期': fy,
        '数据值': data['Gross Margin'],
        '单位': '%',
        '数据来源': 'Nike-Inc-2025_10K.pdf',
        '所在页码': '43',
        '原文摘录': f'Gross margin {data["Gross Margin"]}%',
        '归一化周期': fy,
        '归一化指标名称': '毛利率',
        '归 一化指标数值': data['Gross Margin'],
        '归一化计算逻辑/折算说明': '直接使用原始百分比',
        '备注（披露范围等）': '大中华区',
        '最后更新': datetime.now().strftime('%Y-%m-%d')
    })

    # EBIT
    new_rows.append({
        '#': 4,
        '公司名称': 'Nike',
        '品牌名称': 'TTL',
        '区域': '大中华区',
        '指标名称（原始）': '经营利润(EBIT)',
        '报告周期': fy,
        '数据值': data['EBIT'] * 1000000,
        '单位': 'USD',
        '数据来源': 'Nike-Inc-2025_10K.pdf',
        '所在页码': '43',
        '原文摘录': f'EARNINGS BEFORE INTEREST AND TAXES ${data["EBIT"]}M',
        '归一化周期': fy,
        '归一化指标名称': '经营利润',
        '归 一化指标数值': ebit_krmb,
        '归一化计算逻辑/折算说明': f'百万美元×{rate}×1000=千元RMB',
        '备注（披露范围等）': '大中华区',
        '最后更新': datetime.now().strftime('%Y-%m-%d')
    })

new_df = pd.DataFrame(new_rows)
print(f"\n新增Nike大中华区数据行数: {len(new_df)}")

# 3. 合并数据
df_final = pd.concat([df_cleaned, new_df], ignore_index=True)
print(f"合并后Database行数: {len(df_final)}")

# 4. 保存到临时文件
df_final.to_excel(temp_output, sheet_name='Database', index=False)
print(f"\n✅ 已保存到临时文件: {temp_output}")

# 验证
print("\n" + "="*80)
print("验证 - Nike大中华区数据:")
print("="*80)

df_verify = pd.read_excel(temp_output, sheet_name='Database')
nike_gc_verify = df_verify[
    (df_verify['公司名称'].str.contains('Nike', case=False, na=False)) & 
    (df_verify['区域'] == '大中华区')
]

print(f"\nNike大中华区数据 ({len(nike_gc_verify)} 行):")
print(nike_gc_verify[['#', '公司名称', '区域', '指标名称（原始）', '报告周期', '数据值', '单位', '归一化指标名称', '归 一化指标数值']].to_string())

print("\n" + "="*80)
print("数据摘要 (千元人民币):")
print("="*80)
for fy in ['FY2023', 'FY2024', 'FY2025']:
    fy_data = nike_gc_verify[nike_gc_verify['报告周期'] == fy]
    if not fy_data.empty:
        rev = fy_data[fy_data['归一化指标名称'] == '营业收入']['归 一化指标数值'].values
        gp = fy_data[fy_data['归一化指标名称'] == '毛利']['归 一化指标数值'].values
        gm = fy_data[fy_data['归一化指标名称'] == '毛利率']['归 一化指标数值'].values
        ebit = fy_data[fy_data['归一化指标名称'] == '经营利润']['归 一化指标数值'].values
        
        print(f"\n{fy} (汇率 USD/CNY = {exchange_rates[fy]}):")
        if len(rev) > 0: print(f"  营业收入: {rev[0]:,.0f} 千元RMB (原始 ${nike_gc_usd[fy]['Revenue']}M)")
        if len(gp) > 0: print(f"  毛利: {gp[0]:,.0f} 千元RMB (原始 ${nike_gc_usd[fy]['Gross Profit']}M)")
        if len(gm) > 0: print(f"  毛利率: {gm[0]}%")
        if len(ebit) > 0: print(f"  经营利润: {ebit[0]:,.0f} 千元RMB (原始 ${nike_gc_usd[fy]['EBIT']}M)")

print("\n" + "="*80)
print("⚠️  请关闭 Excel 中的原文件后，手动复制临时文件覆盖原文件")
print("="*80)
print(f"临时文件路径: {temp_output}")
print(f"原文件路径: {db_path}")
