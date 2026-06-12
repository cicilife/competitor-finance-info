import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('竞品财务数据库_标准模板v2-0609.xlsx', sheet_name='Database')

# 查看L列"归一化周期"的数据
print("=== L列'归一化周期'数据样本 ===")
periods = df['归一化周期'].dropna().unique()
print(f"去重后共{len(periods)}个值:")
for p in sorted(periods):
    count = len(df[df['归一化周期'].astype(str) == str(p)])
    print(f"  '{p}': {count}条")

# 查看报告周期和归一化周期的对应关系
print("\n=== 报告周期 vs 归一化周期 对应关系 ===")
mapping = df.groupby(['报告周期', '归一化周期']).size().reset_index(name='count')
for _, row in mapping.iterrows():
    print(f"  报告周期: '{row['报告周期']}' → 归一化周期: '{row['归一化周期']}' (count: {row['count']})")