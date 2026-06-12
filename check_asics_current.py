import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

print(f"当前ASICS行数: {len(df[df['公司名称'].str.contains('ASICS', case=False, na=False)])}")
print("\n当前ASICS数据:")
asics = df[df['公司名称'].str.contains('ASICS', case=False, na=False)]
print(asics[['区域', '报告周期', '指标名称（原始）', '数据值', '单位']].to_string())