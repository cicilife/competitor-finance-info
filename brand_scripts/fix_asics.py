import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

jpy_to_cny = 0.048

# ============ 修正ASICS数据 ============
# 原文: ¥678526M = 678,526百万日元
# 当前错误: G列存储678526000000 (已乘以1,000,000)
# 正确: G列存储678526 (百万日元)

print("=== 修正ASICS数据 ===")
asics_mask = df['公司名称'].str.contains('ASICS|爱世克私', case=False, na=False)

for idx in df[asics_mask].index:
    unit = df.loc[idx, '单位']
    val = df.loc[idx, '数据值']
    indicator = str(df.loc[idx, '指标名称（原始）'])
    orig = str(df.loc[idx, '原文摘录']) if pd.notna(df.loc[idx, '原文摘录']) else ''

    if unit == 'JPY' and '%' not in indicator and 'days' not in indicator:
        # 从原文提取数值，如 ¥678526M -> 678526
        import re
        match = re.search(r'¥([\d.]+)(?:M|B)?', orig)
        if match:
            correct_val = float(match.group(1))
            # 如果当前值已经是 correct_val * 1000000，说明已经错误乘以了1000000
            if abs(val - correct_val * 1000000) < 1000:
                df.loc[idx, '数据值'] = correct_val
                df.loc[idx, '单位'] = '百万日元'
                df.loc[idx, '归一化指标数值'] = correct_val * 1000 * jpy_to_cny
                df.loc[idx, '归一化计算逻辑/折算说明'] = '百万日元×1000×0.048=千元人民币'
                print(f"  {df.loc[idx, '报告周期']} | {indicator[:25]}")
                print(f"    {orig} -> G={correct_val}百万日元 -> M={correct_val * 1000 * jpy_to_cny}千元")

# 保存
df.to_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database', index=False)
print("\n✅ 已保存修正后的数据")

# 验证
print("\n验证ASICS数据:")
asics = df[df['公司名称'].str.contains('ASICS|爱世克私', case=False, na=False)]
for idx, row in asics.iterrows():
    if '%' not in str(row['单位']) and 'days' not in str(row['单位']):
        print(f"{row['报告周期']} | {row['指标名称（原始）'][:20]} | G={row['数据值']} | {row['单位']} | M={row['归一化指标数值']}")