import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2_new.xlsx', sheet_name='Database')

# 看 adidas 数据
adidas = df[df['公司名称'].str.contains('adidas', case=False, na=False)]
print("=== adidas 数据 ===")
for idx, row in adidas.iterrows():
    print(f"  {row['报告周期']:<10} | {row['区域']:<8} | {str(row['归一化指标名称']):<15} | G={row['数据值']} | {row['单位']:<10} | M={row['归一化指标数值']} | 归一化周期={row['归一化周期']}")

print("\n\n=== Columbia 数据 ===")
col = df[df['公司名称'].str.contains('Columbia|哥伦比亚', case=False, na=False)]
for idx, row in col.iterrows():
    print(f"  {row['报告周期']:<10} | {row['区域']:<8} | {str(row['归一化指标名称']):<15} | G={row['数据值']} | {row['单位']:<10} | M={row['归一化指标数值']} | 归一化周期={row['归一化周期']}")

print("\n\n=== 安德玛 数据 ===")
ua = df[df['公司名称'].str.contains('安德玛|Under', case=False, na=False)]
for idx, row in ua.iterrows():
    print(f"  {row['报告周期']:<10} | {row['区域']:<8} | {str(row['归一化指标名称']):<15} | G={row['数据值']} | {row['单位']:<10} | M={row['归一化指标数值']} | 归一化周期={row['归一化周期']}")