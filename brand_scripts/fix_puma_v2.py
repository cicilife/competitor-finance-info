import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

eur_to_cny = 7.8

# ============ 修正彪马数据 ============
# 原文: €7296.2 million -> 7,296,200千欧元
# 归一化: 7,296,200千欧元 × 7.8 = 56,910,360千元人民币
print("=== 修正彪马 ===")
puma_mask = df['公司名称'].str.contains('彪马|PUMA', case=False, na=False)

for idx in df[puma_mask].index:
    unit = df.loc[idx, '单位']
    val = df.loc[idx, '数据值']
    indicator = str(df.loc[idx, '指标名称（原始）'])
    orig = str(df.loc[idx, '原文摘录']) if pd.notna(df.loc[idx, '原文摘录']) else ''

    # 只处理非%指标
    if '%' not in unit:
        import re
        # 匹配 €7296.2 million 格式
        match = re.search(r'€([\d,.]+)\s*million', orig)
        if match:
            million_eur = float(match.group(1).replace(',', ''))
            thousands_eur = million_eur * 1000

            # 修正数据值和单位
            df.loc[idx, '数据值'] = thousands_eur
            df.loc[idx, '单位'] = '千欧元'
            df.loc[idx, '归一化指标数值'] = thousands_eur * eur_to_cny
            df.loc[idx, '归一化计算逻辑/折算说明'] = '千欧元×7.8=千元人民币'
            print(f"  {df.loc[idx, '报告周期']} | {indicator[:25]}")
            print(f"    修正: {val}千元 -> {thousands_eur}千欧元 -> {thousands_eur * eur_to_cny}千元")

# 保存
df.to_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database', index=False)
print("\n✅ 已保存修正后的数据")

# 验证
print("\n验证彪马数据:")
puma = df[df['公司名称'].str.contains('彪马|PUMA', case=False, na=False)]
for idx, row in puma.iterrows():
    if '%' not in row['单位']:
        print(f"{row['报告周期']} | {row['指标名称（原始）'][:25]} | 值={row['数据值']} | {row['单位']} | 归={row['归一化指标数值']}")