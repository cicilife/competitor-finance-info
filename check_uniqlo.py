import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2_new.xlsx', sheet_name='Database')
uniqlo = df[df['公司名称'].str.contains('Fast|迅销|优衣库|UNIQLO', case=False, na=False)]
print('Uniqlo数据行数:', len(uniqlo))
for idx, row in uniqlo.iterrows():
    term = str(row['指标名称（原始）'])[:30]
    period = str(row['报告周期'])
    g_val = row['数据值']
    unit = str(row['单位'])
    m_val = row['归一化指标数值']
    print(f'  {period} | {term:<30} | G={g_val} | {unit} | M={m_val}')