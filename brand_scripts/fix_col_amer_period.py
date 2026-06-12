import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

usd_to_cny = 7.2

# ============ 1. 修正哥伦比亚数据 ============
# 原文: $3397351 thousand = 3,397,351千美元
# 当前错误: 数据值=24460927.2，单位=千元
# 正确应为: 数据值=3397351，单位=千美元，归一化=3397351×7.2
print("=== 修正哥伦比亚 ===")
col_mask = df['公司名称'].str.contains('哥伦比亚|Columbia', case=False, na=False)

for idx in df[col_mask].index:
    unit = df.loc[idx, '单位']
    val = df.loc[idx, '数据值']
    indicator = str(df.loc[idx, '指标名称（原始）'])

    if unit == '千元' and val > 1e7:  # 千元单位但数值特别大的（说明是美元千元未转换）
        # 从原文摘录提取原始千美元数值
        orig = str(df.loc[idx, '原文摘录']) if pd.notna(df.loc[idx, '原文摘录']) else ''

        import re
        # 匹配 $后面的数字
        match = re.search(r'\$([\d,]+)\s*thousand', orig)
        if match:
            thousands_usd = float(match.group(1).replace(',', ''))
            df.loc[idx, '数据值'] = thousands_usd
            df.loc[idx, '单位'] = '千美元'
            normalized = thousands_usd * usd_to_cny
            df.loc[idx, '归一化指标数值'] = normalized
            df.loc[idx, '归一化计算逻辑/折算说明'] = '千美元×7.2=千元人民币'
            print(f"  {df.loc[idx, '报告周期']} | {indicator[:25]}")
            print(f"    修正: {val}千元 -> {thousands_usd}千美元 -> {normalized}千元")

# ============ 2. 修正亚玛芬数据 ============
# 原文: $6566.2 million = 6,566,200千美元
print("\n=== 修正亚玛芬 ===")
amer_mask = df['公司名称'].str.contains('亚玛芬|Amer Sports', case=False, na=False)

for idx in df[amer_mask].index:
    unit = df.loc[idx, '单位']
    val = df.loc[idx, '数据值']
    indicator = str(df.loc[idx, '指标名称（原始）'])

    if unit == '千元' and val > 1e7:  # 千元单位但数值特别大的
        orig = str(df.loc[idx, '原文摘录']) if pd.notna(df.loc[idx, '原文摘录']) else ''

        import re
        # 匹配 $6566.2 million 或 $4500.0 million 格式
        match = re.search(r'\$([\d,.]+)\s*million', orig)
        if match:
            million_usd = float(match.group(1).replace(',', ''))
            thousands_usd = million_usd * 1000
            df.loc[idx, '数据值'] = thousands_usd
            df.loc[idx, '单位'] = '千美元'
            normalized = thousands_usd * usd_to_cny
            df.loc[idx, '归一化指标数值'] = normalized
            df.loc[idx, '归一化计算逻辑/折算说明'] = '千美元×7.2=千元人民币'
            print(f"  {df.loc[idx, '报告周期']} | {indicator[:25]}")
            print(f"    修正: {val}千元 -> {thousands_usd}千美元 -> {normalized}千元")

# ============ 3. 修正昂跑报告周期格式 ============
# 昂跑财年结束于12月31日，应标注为FY20231231格式
print("\n=== 修正昂跑报告周期 ===")
on_mask = df['公司名称'].str.contains('昂跑|On Holding', case=False, na=False)

for idx in df[on_mask].index:
    old_period = df.loc[idx, '报告周期']
    if old_period.startswith('FY2025'):
        df.loc[idx, '报告周期'] = 'FY20251231'
        df.loc[idx, '归一化周期'] = 'FY20251231'
        print(f"  {old_period} -> FY20251231")
    elif old_period.startswith('FY2024'):
        df.loc[idx, '报告周期'] = 'FY20241231'
        df.loc[idx, '归一化周期'] = 'FY20241231'
        print(f"  {old_period} -> FY20241231")
    elif old_period.startswith('FY2023'):
        df.loc[idx, '报告周期'] = 'FY20231231'
        df.loc[idx, '归一化周期'] = 'FY20231231'
        print(f"  {old_period} -> FY20231231")

# 保存
df.to_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database', index=False)
print("\n✅ 已保存修正后的数据")

# 验证
print("\n=== 验证修正结果 ===")
print("\n哥伦比亚:")
col = df[df['公司名称'].str.contains('哥伦比亚|Columbia', case=False, na=False)]
print(col[['报告周期', '指标名称（原始）', '数据值', '单位', '归一化指标数值']].head(6).to_string())

print("\n亚玛芬:")
amer = df[df['公司名称'].str.contains('亚玛芬|Amer Sports', case=False, na=False)]
print(amer[['报告周期', '指标名称（原始）', '数据值', '单位', '归一化指标数值']].head(6).to_string())

print("\n昂跑:")
on = df[df['公司名称'].str.contains('昂跑|On Holding', case=False, na=False)]
print(on[['报告周期', '指标名称（原始）', '数据值', '单位', '归一化指标数值']].head(6).to_string())