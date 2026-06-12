import pandas as pd
from datetime import datetime
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

db_path = r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务数据库_标准模板v2.xlsx'

print("="*80)
print("Updating Anta (安踏) data in Database")
print("="*80)

# 安踏集团层面数据（来自第13页五年财务概览，单位：百万元人民币）
anta_group_data = {
    'FY2025': {'Revenue': 80219, 'Gross Profit': 49734, 'Gross Margin': 62.0, 'OpProfit': 19091, 'NetMargin': 19.5},
    'FY2024': {'Revenue': 70826, 'Gross Profit': 44032, 'Gross Margin': 62.2, 'OpProfit': 16595, 'NetMargin': 24.0},
    'FY2023': {'Revenue': 62356, 'Gross Profit': 39028, 'Gross Margin': 62.6, 'OpProfit': 15367, 'NetMargin': 16.42}  # 净利率=10236/62356
}

print("\n安踏集团层面数据（百万元人民币）:")
for fy, data in anta_group_data.items():
    print(f"{fy}: 收入={data['Revenue']}, 毛利={data['Gross Profit']}, 毛利率={data['Gross Margin']}%, 经营溢利={data['OpProfit']}, 净利率={data['NetMargin']}%")

# 读取Database
df = pd.read_excel(db_path, sheet_name='Database')
print(f"\n原始Database行数: {len(df)}")

# 找到安踏体育用品有限公司的区域为"中国/亚洲"或"中国/全球"或"TOTAL"的数据
anta_mask = (df['公司名称'].str.contains('安踏体育用品有限公司', case=False, na=False))
# 排除DTC直营和电商数据
anta_group_mask = anta_mask & df['区域'].isin(['中国/亚洲', '中国/全球', 'TOTAL'])
anta_indices = df[anta_group_mask].index.tolist()

print(f"\n安踏集团层面现有数据行索引: {anta_indices}")

# 删除这些行
df_cleaned = df[~anta_group_mask].copy()
print(f"删除后Database行数: {len(df_cleaned)}")

# 准备新数据行
new_rows = []

for fy, data in anta_group_data.items():
    # 营业收入 (千元人民币 = 百万元 * 1000)
    new_rows.append({
        '#': 1,  # 安踏对应brand list编号
        '公司名称': '安踏体育用品有限公司',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Revenue / sales',
        '报告周期': fy,
        '数据值': data['Revenue'] * 1000000,
        '单位': 'RMB',
        '数据来源': '安踏体育：二零二五年年报.pdf',
        '所在页码': '13',
        '原文摘录': f'收入 {data["Revenue"]}',
        '归一化周期': fy,
        '归一化指标名称': '营业收入',
        '归 一化指标数值': data['Revenue'] * 1000,  # 千元人民币
        '归一化计算逻辑/折算说明': '百万元×1000=千元RMB',
        '备注（披露范围等）': '集团层面TOTAL',
        '最后更新': datetime.now().strftime('%Y-%m-%d')
    })

    # 毛利
    new_rows.append({
        '#': 1,
        '公司名称': '安踏体育用品有限公司',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Gross margin / Gross profit',
        '报告周期': fy,
        '数据值': data['Gross Profit'] * 1000000,
        '单位': 'RMB',
        '数据来源': '安踏体育：二零二五年年报.pdf',
        '所在页码': '13',
        '原文摘录': f'毛利 {data["Gross Profit"]}',
        '归一化周期': fy,
        '归一化指标名称': '毛利',
        '归 一化指标数值': data['Gross Profit'] * 1000,  # 千元人民币
        '归一化计算逻辑/折算说明': '百万元×1000=千元RMB',
        '备注（披露范围等）': '集团层面TOTAL',
        '最后更新': datetime.now().strftime('%Y-%m-%d')
    })

    # 毛利率
    new_rows.append({
        '#': 1,
        '公司名称': '安踏体育用品有限公司',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Gross margin rate / Gross profit%',
        '报告周期': fy,
        '数据值': data['Gross Margin'],
        '单位': '%',
        '数据来源': '安踏体育：二零二五年年报.pdf',
        '所在页码': '13',
        '原文摘录': f'毛利率 {data["Gross Margin"]}%',
        '归一化周期': fy,
        '归一化指标名称': '毛利率',
        '归 一化指标数值': data['Gross Margin'],
        '归一化计算逻辑/折算说明': '直接使用原始百分比',
        '备注（披露范围等）': '集团层面TOTAL',
        '最后更新': datetime.now().strftime('%Y-%m-%d')
    })

    # 经营溢利
    new_rows.append({
        '#': 1,
        '公司名称': '安踏体育用品有限公司',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Operating Profit / EBIT',
        '报告周期': fy,
        '数据值': data['OpProfit'] * 1000000,
        '单位': 'RMB',
        '数据来源': '安踏体育：二零二五年年报.pdf',
        '所在页码': '13',
        '原文摘录': f'經營溢利 {data["OpProfit"]}',
        '归一化周期': fy,
        '归一化指标名称': '经营利润',
        '归 一化指标数值': data['OpProfit'] * 1000,  # 千元人民币
        '归一化计算逻辑/折算说明': '百万元×1000=千元RMB',
        '备注（披露范围等）': '集团层面TOTAL',
        '最后更新': datetime.now().strftime('%Y-%m-%d')
    })

    # 净利率
    new_rows.append({
        '#': 1,
        '公司名称': '安踏体育用品有限公司',
        '品牌名称': 'TTL',
        '区域': 'TOTAL',
        '指标名称（原始）': 'Net profit margin / 淨溢利率',
        '报告周期': fy,
        '数据值': data['NetMargin'],
        '单位': '%',
        '数据来源': '安踏体育：二零二五年年报.pdf',
        '所在页码': '12',
        '原文摘录': f'淨溢利率 {data["NetMargin"]}%',
        '归一化周期': fy,
        '归一化指标名称': '净利率',
        '归 一化指标数值': data['NetMargin'],
        '归一化计算逻辑/折算说明': '股东应占溢利/收入×100%',
        '备注（披露范围等）': '集团层面TOTAL',
        '最后更新': datetime.now().strftime('%Y-%m-%d')
    })

new_df = pd.DataFrame(new_rows)
print(f"\n新增安踏集团层面数据行数: {len(new_df)}")

# 合并数据
df_final = pd.concat([df_cleaned, new_df], ignore_index=True)
print(f"合并后Database行数: {len(df_final)}")

# 保存
df_final.to_excel(db_path, sheet_name='Database', index=False)
print(f"\n✅ 已更新: {db_path}")

# 验证
print("\n" + "="*80)
print("验证 - 安踏体育用品有限公司 TOTAL数据:")
print("="*80)

df_verify = pd.read_excel(db_path, sheet_name='Database')
anta_verify = df_verify[(df_verify['公司名称'].str.contains('安踏体育用品有限公司', case=False, na=False)) & (df_verify['区域'] == 'TOTAL')]

print(f"\n安踏TOTAL数据 ({len(anta_verify)} 行):")
print(anta_verify[['#', '公司名称', '区域', '指标名称（原始）', '报告周期', '归一化指标名称', '归 一化指标数值', '单位']].to_string())

print("\n" + "="*80)
print("数据摘要 (千元人民币):")
print("="*80)
for fy in ['FY2023', 'FY2024', 'FY2025']:
    fy_data = anta_verify[anta_verify['报告周期'] == fy]
    if not fy_data.empty:
        rev = fy_data[fy_data['归一化指标名称'] == '营业收入']['归 一化指标数值'].values
        gp = fy_data[fy_data['归一化指标名称'] == '毛利']['归 一化指标数值'].values
        gm = fy_data[fy_data['归一化指标名称'] == '毛利率']['归 一化指标数值'].values
        op = fy_data[fy_data['归一化指标名称'] == '经营利润']['归 一化指标数值'].values
        nm = fy_data[fy_data['归一化指标名称'] == '净利率']['归 一化指标数值'].values
        
        print(f"\n{fy}:")
        if len(rev) > 0: print(f"  营业收入: {rev[0]:,.0f} 千元RMB")
        if len(gp) > 0: print(f"  毛利: {gp[0]:,.0f} 千元RMB")
        if len(gm) > 0: print(f"  毛利率: {gm[0]}%")
        if len(op) > 0: print(f"  经营利润: {op[0]:,.0f} 千元RMB")
        if len(nm) > 0: print(f"  净利率: {nm[0]}%")
