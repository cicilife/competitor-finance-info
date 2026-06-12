import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 0609版本
df_0609 = pd.read_excel('竞品财务数据库_标准模板v2-0609.xlsx', sheet_name='Database')
print(f"=== 0609版本 Database ===")
print(f"总数据条数: {len(df_0609)}")
print(f"列名: {list(df_0609.columns)}")
print()

# 查看归一化指标名称
print("=== 归一化指标名称（如果存在）===")
if '归一化指标名称' in df_0609.columns:
    indicators = df_0609['归一化指标名称'].dropna().unique()
    print(f"归一化指标字段存在，共{len(indicators)}个")
    for ind in sorted(indicators):
        count = len(df_0609[df_0609['归一化指标名称'] == ind])
        print(f"  {ind}: {count}条")
else:
    print("归一化指标名称字段不存在！")
    print("使用'指标名称（原始）'代替")
    indicators = df_0609['指标名称（原始）'].dropna().unique()
    for ind in sorted(indicators):
        count = len(df_0609[df_0609['指标名称（原始）'] == ind])
        print(f"  {ind}: {count}条")

# 查看品牌
print(f"\n=== 品牌列表 ===")
brands = df_0609['公司名称'].dropna().unique()
for brand in sorted(brands):
    count = len(df_0609[df_0609['公司名称'] == brand])
    print(f"  {brand}: {count}条")

# 查看区域
print(f"\n=== 区域列表 ===")
regions = df_0609['区域'].dropna().unique()
for region in sorted(regions):
    count = len(df_0609[df_0609['区域'] == region])
    print(f"  {region}: {count}条")

# 查看报告周期
print(f"\n=== 报告周期 ===")
periods = df_0609['报告周期'].dropna().unique()
for p in sorted(periods):
    count = len(df_0609[df_0609['报告周期'] == p])
    print(f"  {p}: {count}条")