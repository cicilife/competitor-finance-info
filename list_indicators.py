import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2_new.xlsx', sheet_name='Database')

# 列出所有归一化指标名称
print("所有归一化指标名称:")
for n in sorted(df['归一化指标名称'].dropna().unique()):
    print(f"  '{n}'")