import pandas as pd
from datetime import datetime
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

db_path = r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务数据库_标准模板v2.xlsx'

print("="*80)
print("更新Database - 安踏、李宁、特步、361度")
print("="*80)

# 汇率 HKD/CNY (用于港股)
hkd_rates = {'FY2023': 0.91, 'FY2024': 0.93, 'FY2025': 0.94}

# ============== 数据定义 ==============

# 安踏 (#19) - 单位百万元人民币
anta_data = {
    'FY2025': {'Revenue': 80219, 'Gross Profit': 49734, 'Gross Margin': 62.0, 'OpProfit': 19091, 'NetMargin': 19.5},
    'FY2024': {'Revenue': 70826, 'Gross Profit': 44032, 'Gross Margin': 62.2, 'OpProfit': 16595, 'NetMargin': 24.0},
    'FY2023': {'Revenue': 62356, 'Gross Profit': 39028, 'Gross Margin': 62.6, 'OpProfit': 15367, 'NetMargin': 16.42}
}

# 李宁 (#18) - 单位百万元人民币
lining_data = {
    'FY2025': {'Revenue': 29598, 'Gross Profit': 14489, 'Gross Margin': 49.0, 'NetMargin': 9.9},
    'FY2024': {'Revenue': 28676, 'Gross Profit': 14156, 'Gross Margin': 49.4, 'NetMargin': 8.8},
    'FY2023': {'Revenue': 27598, 'Gross Profit': 13361, 'Gross Margin': 48.4, 'NetMargin': 8.6}
}

# 特步 (#22) - 单位百万元人民币
xtep_data = {
    'FY2025': {'Revenue': 11535, 'Gross Profit': 4706, 'Gross Margin': 40.8, 'NetMargin': 7.8},
    'FY2024': {'Revenue': 10387, 'Gross Profit': 4415, 'Gross Margin': 42.5, 'NetMargin': 8.6},
    'FY2023': {'Revenue': 9362, 'Gross Profit': 3830, 'Gross Margin': 40.9, 'NetMargin': 8.5}
}

# 361度 (#17) - 单位百万元人民币
deg_data = {
    'FY2025': {'Revenue': 7304, 'Gross Profit': 2834, 'Gross Margin': 38.8, 'NetMargin': 9.6},
    'FY2024': {'Revenue': 7352, 'Gross Profit': 2948, 'Gross Margin': 40.1, 'NetMargin': 9.8},
    'FY2023': {'Revenue': 6602, 'Gross Profit': 2568, 'Gross Margin': 38.9, 'NetMargin': 8.7}
}

# ============== 读取Database ==============
df = pd.read_excel(db_path, sheet_name='Database')
print(f"原始Database行数: {len(df)}")

# ============== 删除旧的港股品牌TOTAL数据 ==============
hk_brands = ['安踏体育用品有限公司', '李宁公司', '特步国际控股有限公司', '361 度国际有限公司']
old_mask = df['公司名称'].isin(hk_brands) & (df['区域'] == 'TOTAL')
old_count = old_mask.sum()
df_cleaned = df[~old_mask].copy()
print(f"删除旧数据行数: {old_count}")
print(f"清理后Database行数: {len(df_cleaned)}")

# ============== 生成新数据行 ==============
new_rows = []

def add_brand_data(brand_name, brand_id, fy_data, source_file, page_num):
    """添加品牌数据"""
    for fy, data in fy_data.items():
        # 营业收入
        new_rows.append({
            '#': brand_id,
            '公司名称': brand_name,
            '品牌名称': 'TTL',
            '区域': 'TOTAL',
            '指标名称（原始）': '收入',
            '报告周期': fy,
            '数据值': data['Revenue'] * 1000000,
            '单位': 'RMB',
            '数据来源': source_file,
            '所在页码': str(page_num),
            '原文摘录': f'收入 {data["Revenue"]}',
            '归一化周期': fy,
            '归一化指标名称': '营业收入',
            '归 一化指标数值': data['Revenue'] * 1000,
            '归一化计算逻辑/折算说明': '百万元×1000=千元RMB',
            '备注（披露范围等）': '集团层面TOTAL',
            '最后更新': datetime.now().strftime('%Y-%m-%d')
        })

        # 毛利
        if 'Gross Profit' in data:
            new_rows.append({
                '#': brand_id,
                '公司名称': brand_name,
                '品牌名称': 'TTL',
                '区域': 'TOTAL',
                '指标名称（原始）': '毛利',
                '报告周期': fy,
                '数据值': data['Gross Profit'] * 1000000,
                '单位': 'RMB',
                '数据来源': source_file,
                '所在页码': str(page_num),
                '原文摘录': f'毛利 {data["Gross Profit"]}',
                '归一化周期': fy,
                '归一化指标名称': '毛利',
                '归 一化指标数值': data['Gross Profit'] * 1000,
                '归一化计算逻辑/折算说明': '百万元×1000=千元RMB',
                '备注（披露范围等）': '集团层面TOTAL',
                '最后更新': datetime.now().strftime('%Y-%m-%d')
            })

        # 毛利率
        new_rows.append({
            '#': brand_id,
            '公司名称': brand_name,
            '品牌名称': 'TTL',
            '区域': 'TOTAL',
            '指标名称（原始）': '毛利率',
            '报告周期': fy,
            '数据值': data['Gross Margin'],
            '单位': '%',
            '数据来源': source_file,
            '所在页码': str(page_num),
            '原文摘录': f'毛利率 {data["Gross Margin"]}%',
            '归一化周期': fy,
            '归一化指标名称': '毛利率',
            '归 一化指标数值': data['Gross Margin'],
            '归一化计算逻辑/折算说明': '直接使用原始百分比',
            '备注（披露范围等）': '集团层面TOTAL',
            '最后更新': datetime.now().strftime('%Y-%m-%d')
        })

        # 经营溢利 (如果有)
        if 'OpProfit' in data:
            new_rows.append({
                '#': brand_id,
                '公司名称': brand_name,
                '品牌名称': 'TTL',
                '区域': 'TOTAL',
                '指标名称（原始）': '经营溢利',
                '报告周期': fy,
                '数据值': data['OpProfit'] * 1000000,
                '单位': 'RMB',
                '数据来源': source_file,
                '所在页码': str(page_num),
                '原文摘录': f'经营溢利 {data["OpProfit"]}',
                '归一化周期': fy,
                '归一化指标名称': '经营利润',
                '归 一化指标数值': data['OpProfit'] * 1000,
                '归一化计算逻辑/折算说明': '百万元×1000=千元RMB',
                '备注（披露范围等）': '集团层面TOTAL',
                '最后更新': datetime.now().strftime('%Y-%m-%d')
            })

        # 净利率
        if 'NetMargin' in data:
            new_rows.append({
                '#': brand_id,
                '公司名称': brand_name,
                '品牌名称': 'TTL',
                '区域': 'TOTAL',
                '指标名称（原始）': '净利率',
                '报告周期': fy,
                '数据值': data['NetMargin'],
                '单位': '%',
                '数据来源': source_file,
                '所在页码': str(page_num),
                '原文摘录': f'净利率 {data["NetMargin"]}%',
                '归一化周期': fy,
                '归一化指标名称': '净利率',
                '归 一化指标数值': data['NetMargin'],
                '归一化计算逻辑/折算说明': '净利率=净利润÷收入×100%',
                '备注（披露范围等）': '集团层面TOTAL',
                '最后更新': datetime.now().strftime('%Y-%m-%d')
            })

# 添加四家品牌数据
add_brand_data('安踏体育用品有限公司', 19, anta_data, '安踏体育：二零二五年年报.pdf', 13)
add_brand_data('李宁公司', 18, lining_data, '李宁：2025年度报告.pdf', 10)
add_brand_data('特步国际控股有限公司', 22, xtep_data, '特步2025年报.pdf', 10)
add_brand_data('361 度国际有限公司', 17, deg_data, '361度：二零二五年年报.pdf', 64)

new_df = pd.DataFrame(new_rows)
print(f"新增数据行数: {len(new_df)}")

# ============== 合并并保存 ==============
df_final = pd.concat([df_cleaned, new_df], ignore_index=True)
print(f"合并后Database行数: {len(df_final)}")

df_final.to_excel(db_path, sheet_name='Database', index=False)
print(f"\n✅ 已更新: {db_path}")

# ============== 验证 ==============
print("\n" + "="*80)
print("验证 - 四家港股品牌TOTAL数据:")
print("="*80)

df_verify = pd.read_excel(db_path, sheet_name='Database')

for brand_name, brand_id in [
    ('安踏体育用品有限公司', 19),
    ('李宁公司', 18),
    ('特步国际控股有限公司', 22),
    ('361 度国际有限公司', 17)
]:
    brand_data = df_verify[(df_verify['公司名称'] == brand_name) & (df_verify['区域'] == 'TOTAL')]
    if not brand_data.empty:
        print(f"\n【{brand_name}】#={brand_id}")
        for fy in ['FY2023', 'FY2024', 'FY2025']:
            fy_data = brand_data[brand_data['报告周期'] == fy]
            if not fy_data.empty:
                rev = fy_data[fy_data['归一化指标名称'] == '营业收入']['归 一化指标数值'].values
                gm = fy_data[fy_data['归一化指标名称'] == '毛利率']['归 一化指标数值'].values
                if len(rev) > 0: print(f"  {fy}: 收入={rev[0]/1000:.0f}亿元, 毛利率={gm[0] if len(gm)>0 else 'N/A'}%")

print("\n" + "="*80)
print("✅ 更新完成！")
print("="*80)
