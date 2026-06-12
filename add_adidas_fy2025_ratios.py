import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

# 删除可能重复的Adidas FY2025数据
mask = (
    df['公司名称'].str.contains('adidas', case=False, na=False) &
    (df['区域'] == 'TOTAL') &
    (df['报告周期'] == 'FY2025')
)
to_delete = df[mask]
df = df.drop(to_delete.index)
print(f"删除已存在的Adidas FY2025数据: {len(to_delete)}条")

eur_to_cny = 7.8

# FY2025 全部数据 (来源: adidas FY 2025 Results P13)
fy2025_data = [
    # 绝对值数据
    ('Net sales', '24,811', 24811, '百万欧元', '营业收入', None),
    ('Gross profit', '12,804', 12804, '百万欧元', '毛利', None),
    ('Other operating expenses', '10,871', 10871, '百万欧元', '运营费用', None),
    ('Marketing and point-of-sale expenses', '3,079', 3079, '百万欧元', '广告及市场费用', None),
    ('Operating overhead expenses', '7,792', 7792, '百万欧元', '管理及运营费用', None),
    ('Operating profit', '2,056', 2056, '百万欧元', '经营利润', None),
    ('Income before taxes', '1,820', 1820, '百万欧元', '税前利润', None),
    ('Income taxes', '443', 443, '百万欧元', '所得税', None),
    ('Net income from continuing operations', '1,377', 1377, '百万欧元', '净利润', None),
    ('Net income', '1,385', 1385, '百万欧元', '净利润(含discontinued)', None),
    ('Net income attributable to shareholders', '1,340', 1340, '百万欧元', '归属母公司净利润', None),

    # 比率数据
    ('Gross margin (% of net sales)', '51.6%', 51.6, '%', '毛利率', 516),
    ('Operating profit margin (% of net sales)', '8.3%', 8.3, '%', '经营利润率', 83),
    ('Net income from continuing operations margin', '5.6%', 5.6, '%', '净利率', 56),
    ('Net income margin', '5.6%', 5.6, '%', '净利率(含discontinued)', 56),
    ('Other operating expenses ratio', '43.8%', 43.8, '%', '运营费用率', 438),
    ('Marketing and POS expenses ratio', '12.4%', 12.4, '%', '广告及市场费用率', 124),
    ('Operating overhead expenses ratio', '31.4%', 31.4, '%', '管理及运营费用率', 314),
    ('Income before taxes margin', '7.3%', 7.3, '%', '税前利润率', 73),
    ('Tax rate', '24.3%', 24.3, '%', '实际税率', 243),
]

# FY2024 比率补充 (从年报P361 + FY2025 P13 对比)
fy2024_ratios = [
    ('Gross margin (% of net sales)', '50.8%', 50.8, '%', '毛利率', 508),
    ('Operating profit margin (% of net sales)', '5.6%', 5.6, '%', '经营利润率', 56),
    ('Net income from continuing operations margin', '3.5%', 3.5, '%', '净利率', 35),
    ('Net income margin', '3.5%', 3.5, '%', '净利率(含discontinued)', 35),
    ('Other operating expenses ratio', '46.2%', 46.2, '%', '运营费用率', 462),
    ('Marketing and POS expenses ratio', '12.0%', 12.0, '%', '广告及市场费用率', 120),
    ('Operating overhead expenses ratio', '34.2%', 34.2, '%', '管理及运营费用率', 342),
]

# FY2023 比率补充 (从年报P361)
fy2023_ratios = [
    ('Gross margin (% of net sales)', '47.5%', 47.5, '%', '毛利率', 475),
    ('Operating profit margin (% of net sales)', '1.3%', 1.3, '%', '经营利润率', 13),
    ('Net income from continuing operations margin', '-0.3%', -0.3, '%', '净利率', -3),
    ('Net income margin', '-0.1%', -0.1, '%', '净利率(含discontinued)', -1),
    ('Other operating expenses ratio', '47.0%', 47.0, '%', '运营费用率', 470),
    ('Marketing and POS expenses ratio', '11.8%', 11.8, '%', '广告及市场费用率', 118),
    ('Operating overhead expenses ratio', '35.2%', 35.2, '%', '管理及运营费用率', 352),
]

new_rows = []

# FY2025 数据
for orig_term, val_str, val, unit, normalized_name, _ in fy2025_data:
    new_rows.append({
        '#': 2,
        '公司名称': 'adidas AG',
        '品牌名称': 'ADIDAS',
        '区域': 'TOTAL',
        '指标名称（原始）': orig_term,
        '报告周期': 'FY2025',
        '数据值': val,
        '单位': unit,
        '数据来源': 'adidasAG_FY_2025_Results_EN_Final_tb9z6m.pdf',
        '所在页码': '13',
        '原文摘录': f'{orig_term} {val_str} in FY2025 (Condensed Consolidated Income Statement)',
        '归一化周期': 'FY2025',
        '归一化指标名称': normalized_name,
        '归一化指标数值': val * 1000 * eur_to_cny if unit == '百万欧元' else val,
        '归一化计算逻辑/折算说明': '百万欧元×1000×7.8=千元人民币' if unit == '百万欧元' else '百分比直接存储',
        '备注（披露范围等）': '集团TOTAL',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    })

# FY2024 比率
for orig_term, val_str, val, unit, normalized_name, _ in fy2024_ratios:
    new_rows.append({
        '#': 2,
        '公司名称': 'adidas AG',
        '品牌名称': 'ADIDAS',
        '区域': 'TOTAL',
        '指标名称（原始）': orig_term,
        '报告周期': 'FY2024',
        '数据值': val,
        '单位': unit,
        '数据来源': 'adidas_annual_report_2024_EN_Final_secured_c8nukv.pdf',
        '所在页码': '361',
        '原文摘录': f'{orig_term} {val_str} in 2024',
        '归一化周期': 'FY2024',
        '归一化指标名称': normalized_name,
        '归一化指标数值': val,
        '归一化计算逻辑/折算说明': '百分比直接存储',
        '备注（披露范围等）': '集团TOTAL',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    })

# FY2023 比率
for orig_term, val_str, val, unit, normalized_name, _ in fy2023_ratios:
    new_rows.append({
        '#': 2,
        '公司名称': 'adidas AG',
        '品牌名称': 'ADIDAS',
        '区域': 'TOTAL',
        '指标名称（原始）': orig_term,
        '报告周期': 'FY2023',
        '数据值': val,
        '单位': unit,
        '数据来源': 'adidas_annual_report_2024_EN_Final_secured_c8nukv.pdf',
        '所在页码': '361',
        '原文摘录': f'{orig_term} {val_str} in 2023',
        '归一化周期': 'FY2023',
        '归一化指标名称': normalized_name,
        '归一化指标数值': val,
        '归一化计算逻辑/折算说明': '百分比直接存储',
        '备注（披露范围等）': '集团TOTAL',
        '最后更新': '2025-06-09',
        '人工核验': '待核验'
    })

# 创建新DataFrame
df_new = pd.DataFrame(new_rows)
existing_cols = df.columns.tolist()
for col in existing_cols:
    if col not in df_new.columns:
        df_new[col] = None
df_new = df_new[existing_cols]

df_combined = pd.concat([df, df_new], ignore_index=True)
# 文件被占用，使用带时间戳的文件名保存
import datetime
ts = datetime.datetime.now().strftime('%H%M%S')
target = f'竞品财务数据库_标准模板v2_{ts}.xlsx'
df_combined.to_excel(target, sheet_name='Database', index=False)
print(f"\n⚠️ 原文件被占用，已保存为: {target}")

print(f"\n✅ 已添加Adidas FY2025绝对值 + FY2023-2025比率数据 {len(new_rows)}条")
print("\n=== 验证 ===")
adidas_new = df_combined[
    df_combined['公司名称'].str.contains('adidas', case=False, na=False) &
    (df_combined['区域'] == 'TOTAL') &
    (df_combined['归一化指标名称'].isin(['毛利率', '经营利润率', '净利率', '广告及市场费用率', '管理及运营费用率', '运营费用率']))
]
for _, row in adidas_new.iterrows():
    print(f"  {row['报告周期']} | {row['指标名称（原始）'][:30]:<30} | {row['数据值']}{row['单位']}")