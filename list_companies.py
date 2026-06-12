import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2_new.xlsx', sheet_name='Database')
print('所有公司名列表:')
companies = df['公司名称'].dropna().unique()
for c in sorted(companies):
    print(f'  {c}')