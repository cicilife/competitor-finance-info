import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2_new.xlsx', sheet_name='Database')

# 修正Fast Retailing所有"10亿日元"单位数据
mask = (
    df['公司名称'].str.contains('Fast|迅销', case=False, na=False) &
    (df['单位'] == '10亿日元')
)

print(f"待修正行数: {mask.sum()}")

jpy_to_cny = 0.048
# 10亿日元 = 1,000,000千日元
# 1千日元 = 1千元日元的1/1000? 不对
# 10亿日元 = 1,000,000 千日元
# 1千日元 = 1000日元
# 所以 10亿日元 = 1,000,000 千日元
# 换算为千元人民币: 10亿日元 × 1,000,000 (转千) × 0.048 (汇率)

fixed_count = 0
for idx in df[mask].index:
    g_val = df.loc[idx, '数据值']
    new_m = g_val * 1000000 * jpy_to_cny
    old_m = df.loc[idx, '归一化指标数值']
    df.loc[idx, '归一化指标数值'] = new_m
    df.loc[idx, '归一化计算逻辑/折算说明'] = '10亿日元×1,000,000×0.048=千元人民币'
    fixed_count += 1
    print(f"  {df.loc[idx, '报告周期']} | {str(df.loc[idx, '指标名称（原始）'])[:25]:<25} | G={g_val} | M: {old_m} -> {new_m}")

print(f"\n共修正 {fixed_count} 条")

# 保存为新文件
import datetime
ts = datetime.datetime.now().strftime('%H%M%S')
target = f'竞品财务数据库_标准模板v2_new.xlsx'
df.to_excel(target, sheet_name='Database', index=False)
print(f"\n✅ 已保存到: {target}")