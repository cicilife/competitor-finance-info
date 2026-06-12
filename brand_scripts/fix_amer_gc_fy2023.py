import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

usd_to_cny = 7.2

# ============ 修正亚玛芬FY2023大中华区数据 ============
# 原文: FY2023 Greater China Net revenues $844.8 million
# 当前错误数据: $1000.0 million
print("=== 修正亚玛芬FY2023大中华区数据 ===")

amer_mask = df['公司名称'].str.contains('亚玛芬|Amer Sports', case=False, na=False)

for idx in df[amer_mask].index:
    fy = df.loc[idx, '报告周期']
    region = df.loc[idx, '区域']
    indicator = str(df.loc[idx, '指标名称（原始）'])

    if fy == 'FY2023' and 'Greater China' in region and 'Net revenues' in indicator:
        correct_million_usd = 844.8
        correct_thousands_usd = correct_million_usd * 1000  # 844,800千美元

        df.loc[idx, '数据值'] = correct_thousands_usd
        df.loc[idx, '归一化指标数值'] = correct_thousands_usd * usd_to_cny
        df.loc[idx, '原文摘录'] = f'Greater China Net revenues ${correct_million_usd} million'
        df.loc[idx, '归一化计算逻辑/折算说明'] = '千美元×7.2=千元人民币'
        print(f"  FY2023 | Greater China Net revenues")
        print(f"    修正: $1000.0 million -> ${correct_million_usd} million -> {correct_thousands_usd}千美元 -> {correct_thousands_usd * usd_to_cny}千元")

# 保存
df.to_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database', index=False)
print("\n✅ 已保存修正后的数据")

# 验证
print("\n验证亚玛芬大中华区数据:")
amer = df[df['公司名称'].str.contains('亚玛芬|Amer Sports', case=False, na=False)]
gc = amer[amer['区域'] == '大中华区']
print(gc[['报告周期', '指标名称（原始）', '数据值', '单位', '归一化指标数值']].to_string())