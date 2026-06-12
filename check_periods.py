import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('竞品财务数据库_标准模板v2-0609.xlsx', sheet_name='Database')

# 查看Lululemon的报告周期
print("=== Lululemon的报告周期 ===")
ll = df[df['公司名称'] == 'Lululemon athletica inc.']
print(ll['报告周期'].unique())

print("\n=== Nike的报告周期 ===")
nike = df[df['公司名称'] == 'Nike']
print(nike['报告周期'].unique())

print("\n=== Fast Retailing的报告周期 ===")
fr = df[df['公司名称'] == 'Fast Retailing']
print(fr['报告周期'].unique())