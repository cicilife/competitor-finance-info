import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('竞品财务数据库_标准模板v2-0605核验中.xlsx', sheet_name='Database')

# 查看归一化指标名称
print("=== 所有归一化指标名称 ===")
indicators = df['归一化指标名称'].dropna().unique()
for ind in sorted(indicators):
    count = len(df[df['归一化指标名称'] == ind])
    print(f"  {ind}: {count}条")

# 查看包含毛利的所有记录
print("\n=== 包含毛利的记录 ===")
gross_data = df[df['归一化指标名称'].str.contains('毛', na=False)]
print(f"总数: {len(gross_data)}")
print(gross_data[['公司名称', '归一化指标名称', '归一化周期', '数据值']].to_string())