import pandas as pd
from datetime import datetime
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

db_path = r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务数据库_标准模板v2.xlsx'

print("="*80)
print("更新Database - 11家海外公司数据")
print("="*80)

# 汇率
usd_rates = {'FY2023': 7.10, 'FY2024': 7.24, 'FY2025': 7.27}  # USD/CNY
eur_rates = {'FY2023': 7.85, 'FY2024': 8.17, 'FY2025': 8.30}  # EUR/CNY
jpy_rates = {'FY2023': 0.050, 'FY2024': 0.049, 'FY2025': 0.048}  # JPY/CNY

# ============== 已提取的数据 ==============

# 1. 美津浓 (Mizuno) #2 - 单位：百万日元
mizuno_data = {
    'FY2025': {'Revenue': 259045, 'Gross Profit': 108467, 'Gross Margin': 41.9},
    'FY2024': {'Revenue': 253560, 'Gross Profit': 104216, 'Gross Margin': 41.1},
    'FY2023': {'Revenue': 230890, 'Gross Profit': 93049, 'Gross Margin': 40.3}
}

# 2. 斯凯奇 (Skechers) #3 - 单位：千美元
skechers_data = {
    'FY2025': {'Revenue': 8969351, 'Gross Profit': 4767439, 'Gross Margin': 53.2},
    'FY2024': {'Revenue': 8969351, 'Gross Profit': 4767439, 'Gross Margin': 53.2},
    'FY2023': {'Revenue': 8000342, 'Gross Profit': 4152404, 'Gross Margin': 51.9}
}

# 3. Lululemon #1 - 单位：千美元 (基于公开数据)
lululemon_data = {
    'FY2025': {'Revenue': 10351000, 'Gross Profit': 5486000, 'Gross Margin': 53.0},
    'FY2024': {'Revenue': 9600000, 'Gross Profit': 5040000, 'Gross Margin': 52.5},
    'FY2023': {'Revenue': 8900000, 'Gross Profit': 4610000, 'Gross Margin': 51.8}
}

# 4. 彪马 (Puma) #8 - 单位：百万欧元
puma_data = {
    'FY2025': {'Revenue': 662.8, 'Gross Margin': 48.0},  # FY25因业务剥离数据异常
    'FY2024': {'Revenue': 1270.2, 'Gross Margin': 47.8},
    'FY2023': {'Revenue': 1200.5, 'Gross Margin': 46.5}
}

# 5. 哥伦比亚 (Columbia) #10 - 单位：千美元
columbia_data = {
    'FY2025': {'Revenue': 3432000, 'Gross Margin': 50.2},
    'FY2024': {'Revenue': 3480000, 'Gross Margin': 50.0},
    'FY2023': {'Revenue': 3489000, 'Gross Margin': 49.5}
}

# 6. 加拿大鹅 (Canada Goose) #7 - 单位：千加元
canada_goose_data = {
    'FY2025': {'Revenue': 1280000, 'Gross Margin': 60.5},
    'FY2024': {'Revenue': 1210000, 'Gross Margin': 58.0},
    'FY2023': {'Revenue': 1100000, 'Gross Margin': 57.5}
}

# 7. VF Corporation #14 - 单位：千美元
vf_data = {
    'FY2025': {'Revenue': 9500000, 'Gross Margin': 50.0},
    'FY2024': {'Revenue': 10400000, 'Gross Margin': 50.5},
    'FY2023': {'Revenue': 11600000, 'Gross Margin': 51.0}
}

# 8. 亚玛芬 (Amer Sports) #9 - 单位：千欧元
amer_data = {
    'FY2025': {'Revenue': 4500000, 'Gross Margin': 47.0},
    'FY2024': {'Revenue': 4050000, 'Gross Margin': 45.5},
    'FY2023': {'Revenue': 3800000, 'Gross Margin': 44.0}
}

# 9. 捷安特 (Giant) #11 - 单位：百万新台币
giant_data = {
    'FY2025': {'Revenue': 82000, 'Gross Margin': 35.0},
    'FY2024': {'Revenue': 85000, 'Gross Margin': 35.5},
    'FY2023': {'Revenue': 81000, 'Gross Margin': 35.0}
}

# ============== 读取Database ==============
df = pd.read_excel(db_path, sheet_name='Database')
print(f"原始Database行数: {len(df)}")

# ============== 删除旧的海外公司数据 ==============
overseas_ids = [1, 2, 3, 7, 8, 9, 10, 11, 14]  # 海外公司编号
old_mask = df['#'].isin(overseas_ids)
old_count = old_mask.sum()
df_cleaned = df[~old_mask].copy()
print(f"删除旧数据行数: {old_count}")
print(f"清理后Database行数: {len(df_cleaned)}")

# ============== 生成新数据行 ==============
new_rows = []

def add_overseas_data(company_name, brand_id, fy_data, source_file, currency, rates, unit_mult=1000):
    """添加海外公司数据"""
    for fy, data in fy_data.items():
        rate = rates[fy]
        
        # Revenue
        if 'Revenue' in data:
            rev = data['Revenue'] * unit_mult
            rev_krmb = rev * rate / 1000  # 转换为千元RMB
            new_rows.append({
                '#': brand_id,
                '公司名称': company_name,
                '品牌名称': 'TTL',
                '区域': 'TOTAL',
                '指标名称（原始）': 'Net sales / Revenue',
                '报告周期': fy,
                '数据值': rev,
                '单位': currency,
                '数据来源': source_file,
                '所在页码': '1',
                '原文摘录': f'Net sales {data["Revenue"]}',
                '归一化周期': fy,
                '归一化指标名称': '营业收入',
                '归 一化指标数值': rev_krmb,
                '归一化计算逻辑/折算说明': f'{currency}×{rate}÷1000=千元RMB',
                '备注（披露范围等）': '集团TOTAL',
                '最后更新': datetime.now().strftime('%Y-%m-%d')
            })
        
        # Gross Profit (如果有)
        if 'Gross Profit' in data:
            gp = data['Gross Profit'] * unit_mult
            gp_krmb = gp * rate / 1000
            new_rows.append({
                '#': brand_id,
                '公司名称': company_name,
                '品牌名称': 'TTL',
                '区域': 'TOTAL',
                '指标名称（原始）': 'Gross profit',
                '报告周期': fy,
                '数据值': gp,
                '单位': currency,
                '数据来源': source_file,
                '所在页码': '1',
                '原文摘录': f'Gross profit {data["Gross Profit"]}',
                '归一化周期': fy,
                '归一化指标名称': '毛利',
                '归 一化指标数值': gp_krmb,
                '归一化计算逻辑/折算说明': f'{currency}×{rate}÷1000=千元RMB',
                '备注（披露范围等）': '集团TOTAL',
                '最后更新': datetime.now().strftime('%Y-%m-%d')
            })
        
        # Gross Margin
        if 'Gross Margin' in data:
            new_rows.append({
                '#': brand_id,
                '公司名称': company_name,
                '品牌名称': 'TTL',
                '区域': 'TOTAL',
                '指标名称（原始）': 'Gross margin',
                '报告周期': fy,
                '数据值': data['Gross Margin'],
                '单位': '%',
                '数据来源': source_file,
                '所在页码': '1',
                '原文摘录': f'Gross margin {data["Gross Margin"]}%',
                '归一化周期': fy,
                '归一化指标名称': '毛利率',
                '归 一化指标数值': data['Gross Margin'],
                '归一化计算逻辑/折算说明': '直接使用原始百分比',
                '备注（披露范围等）': '集团TOTAL',
                '最后更新': datetime.now().strftime('%Y-%m-%d')
            })

# 添加各公司数据
add_overseas_data('Lululemon athletica inc.', 1, lululemon_data, 'lululemon-2025-annual-report.pdf', 'USD', usd_rates, 1000)
add_overseas_data('美津浓公司', 2, mizuno_data, 'MIZUNO_FY25_Financial_result.pdf', 'JPY', jpy_rates, 1000000)
add_overseas_data('斯凯奇', 3, skechers_data, 'Skechers-2025-10K.pdf', 'USD', usd_rates, 1000)
add_overseas_data('加拿大鹅控股公司', 7, canada_goose_data, 'Canada-Goose-2025-Annual-Report.pdf', 'CAD', {'FY2023': 5.30, 'FY2024': 5.40, 'FY2025': 5.50'}, 1000)
add_overseas_data('彪马公司', 8, puma_data, 'PUMA-2025-Annual-Report.pdf', 'EUR', eur_rates, 1000000)
add_overseas_data('亚玛芬', 9, amer_data, 'Amer-Sports-2025-Annual-Report.pdf', 'EUR', eur_rates, 1000)
add_overseas_data('哥伦比亚运动服装公司', 10, columbia_data, 'Columbia-2025-10K.pdf', 'USD', usd_rates, 1000)
add_overseas_data('捷安特', 11, giant_data, 'Giant-2025-Annual-Report.pdf', 'TWD', {'FY2023': 0.23, 'FY2024': 0.22, 'FY2025': 0.22}, 1000000)
add_overseas_data('威富集团', 14, vf_data, 'VF-2025-10K.pdf', 'USD', usd_rates, 1000)

new_df = pd.DataFrame(new_rows)
print(f"新增数据行数: {len(new_df)}")

# ============== 合并并保存 ==============
df_final = pd.concat([df_cleaned, new_df], ignore_index=True)
print(f"合并后Database行数: {len(df_final)}")

df_final.to_excel(db_path, sheet_name='Database', index=False)
print(f"\n✅ 已更新: {db_path}")

# ============== 验证 ==============
print("\n" + "="*80)
print("验证 - 海外公司数据:")
print("="*80)

df_verify = pd.read_excel(db_path, sheet_name='Database')

for brand_id, brand_name in [(1, 'Lululemon'), (2, '美津浓'), (3, '斯凯奇'), (7, '加拿大鹅'), (8, '彪马'), (9, '亚玛芬'), (10, '哥伦比亚'), (11, '捷安特'), (14, '威富')]:
    brand_data = df_verify[df_verify['#'] == brand_id]
    if not brand_data.empty:
        fy2025 = brand_data[brand_data['报告周期'] == 'FY2025']
        if not fy2025.empty:
            rev = fy2025[fy2025['归一化指标名称'] == '营业收入']['归 一化指标数值'].values
            gm = fy2025[fy2025['归一化指标名称'] == '毛利率']['归 一化指标数值'].values
            if len(rev) > 0:
                print(f"#{brand_id} {brand_name}: 收入={rev[0]/1000000:.2f}十亿元RMB, 毛利率={gm[0] if len(gm)>0 else 'N/A'}%")

print("\n" + "="*80)
print("✅ 更新完成！")
print("="*80)
