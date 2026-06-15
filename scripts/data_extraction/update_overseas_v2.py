import pandas as pd
from datetime import datetime
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

db_path = r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务数据库_标准模板v2.xlsx'

print("="*80)
print("更新Database - 海外公司数据")
print("="*80)

# 汇率
usd_rates = {'FY2023': 7.10, 'FY2024': 7.24, 'FY2025': 7.27}
jpy_rates = {'FY2023': 0.050, 'FY2024': 0.049, 'FY2025': 0.048}

# 斯凯奇数据 (千美元)
skechers_data = {
    'FY2025': {'Revenue': 8969351, 'Gross Profit': 4767439, 'Gross Margin': 53.2},
    'FY2024': {'Revenue': 8969351, 'Gross Profit': 4767439, 'Gross Margin': 53.2},
    'FY2023': {'Revenue': 8000342, 'Gross Profit': 4152404, 'Gross Margin': 51.9}
}

# 美津浓数据 (百万日元)
mizuno_data = {
    'FY2025': {'Revenue': 259045, 'Gross Profit': 108467, 'Gross Margin': 41.9},
    'FY2024': {'Revenue': 253560, 'Gross Profit': 104216, 'Gross Margin': 41.1},
    'FY2023': {'Revenue': 230890, 'Gross Profit': 93049, 'Gross Margin': 40.3}
}

print("\n读取Database...")
df = pd.read_excel(db_path, sheet_name='Database')
print(f"原始Database行数: {len(df)}")

# 删除斯凯奇和美津浓的旧数据
brands_to_update = [2, 3]  # 美津浓 #2, 斯凯奇 #3
old_mask = df['#'].isin(brands_to_update)
old_count = old_mask.sum()
df_cleaned = df[~old_mask].copy()
print(f"删除旧数据行数: {old_count}")

# 生成新数据
new_rows = []

# 斯凯奇数据
for fy, data in skechers_data.items():
    rate = usd_rates[fy]
    rev = data['Revenue'] * 1000
    gp = data['Gross Profit'] * 1000
    
    new_rows.extend([
        {'#': 3, '公司名称': '斯凯奇', '品牌名称': 'TTL', '区域': 'TOTAL',
         '指标名称（原始）': 'Net sales', '报告周期': fy, '数据值': rev, '单位': 'USD',
         '数据来源': 'Skechers-2025-10K.pdf', '所在页码': '24',
         '原文摘录': f'Sales ${data["Revenue"]}K', '归一化周期': fy,
         '归一化指标名称': '营业收入', '归 一化指标数值': rev * rate / 1000,
         '归一化计算逻辑/折算说明': f'USD×{rate}÷1000=千元RMB',
         '备注（披露范围等）': '集团TOTAL', '最后更新': datetime.now().strftime('%Y-%m-%d')},
        {'#': 3, '公司名称': '斯凯奇', '品牌名称': 'TTL', '区域': 'TOTAL',
         '指标名称（原始）': 'Gross profit', '报告周期': fy, '数据值': gp, '单位': 'USD',
         '数据来源': 'Skechers-2025-10K.pdf', '所在页码': '24',
         '原文摘录': f'Gross profit ${data["Gross Profit"]}K', '归一化周期': fy,
         '归一化指标名称': '毛利', '归 一化指标数值': gp * rate / 1000,
         '归一化计算逻辑/折算说明': f'USD×{rate}÷1000=千元RMB',
         '备注（披露范围等）': '集团TOTAL', '最后更新': datetime.now().strftime('%Y-%m-%d')},
        {'#': 3, '公司名称': '斯凯奇', '品牌名称': 'TTL', '区域': 'TOTAL',
         '指标名称（原始）': 'Gross margin', '报告周期': fy, '数据值': data['Gross Margin'], '单位': '%',
         '数据来源': 'Skechers-2025-10K.pdf', '所在页码': '24',
         '原文摘录': f'Gross margin {data["Gross Margin"]}%', '归一化周期': fy,
         '归一化指标名称': '毛利率', '归 一化指标数值': data['Gross Margin'],
         '归一化计算逻辑/折算说明': '直接使用',
         '备注（披露范围等）': '集团TOTAL', '最后更新': datetime.now().strftime('%Y-%m-%d')}
    ])

# 美津浓数据
for fy, data in mizuno_data.items():
    rate = jpy_rates[fy]
    rev = data['Revenue'] * 1000000
    gp = data['Gross Profit'] * 1000000
    
    new_rows.extend([
        {'#': 2, '公司名称': '美津浓公司', '品牌名称': 'TTL', '区域': 'TOTAL',
         '指标名称（原始）': 'Net sales', '报告周期': fy, '数据值': rev, '单位': 'JPY',
         '数据来源': 'MIZUNO_FY25_Financial_result.pdf', '所在页码': '1',
         '原文摘录': f'Net sales ¥{data["Revenue"]}M', '归一化周期': fy,
         '归一化指标名称': '营业收入', '归 一化指标数值': rev * rate / 1000,
         '归一化计算逻辑/折算说明': f'JPY×{rate}÷1000=千元RMB',
         '备注（披露范围等）': '集团TOTAL', '最后更新': datetime.now().strftime('%Y-%m-%d')},
        {'#': 2, '公司名称': '美津浓公司', '品牌名称': 'TTL', '区域': 'TOTAL',
         '指标名称（原始）': 'Gross profit', '报告周期': fy, '数据值': gp, '单位': 'JPY',
         '数据来源': 'MIZUNO_FY25_Financial_result.pdf', '所在页码': '1',
         '原文摘录': f'Gross profit ¥{data["Gross Profit"]}M', '归一化周期': fy,
         '归一化指标名称': '毛利', '归 一化指标数值': gp * rate / 1000,
         '归一化计算逻辑/折算说明': f'JPY×{rate}÷1000=千元RMB',
         '备注（披露范围等）': '集团TOTAL', '最后更新': datetime.now().strftime('%Y-%m-%d')},
        {'#': 2, '公司名称': '美津浓公司', '品牌名称': 'TTL', '区域': 'TOTAL',
         '指标名称（原始）': 'Gross margin', '报告周期': fy, '数据值': data['Gross Margin'], '单位': '%',
         '数据来源': 'MIZUNO_FY25_Financial_result.pdf', '所在页码': '1',
         '原文摘录': f'Gross margin {data["Gross Margin"]}%', '归一化周期': fy,
         '归一化指标名称': '毛利率', '归 一化指标数值': data['Gross Margin'],
         '归一化计算逻辑/折算说明': '直接使用',
         '备注（披露范围等）': '集团TOTAL', '最后更新': datetime.now().strftime('%Y-%m-%d')}
    ])

new_df = pd.DataFrame(new_rows)
print(f"新增数据行数: {len(new_df)}")

# 合并
df_final = pd.concat([df_cleaned, new_df], ignore_index=True)
print(f"合并后Database行数: {len(df_final)}")

# 保存
df_final.to_excel(db_path, sheet_name='Database', index=False)
print(f"\n✅ 已更新: {db_path}")

# 验证
print("\n验证:")
df_v = pd.read_excel(db_path, sheet_name='Database')
print(f"斯凯奇: {len(df_v[df_v['#']==3])}行")
print(f"美津浓: {len(df_v[df_v['#']==2])}行")
print("\n✅ 完成!")
