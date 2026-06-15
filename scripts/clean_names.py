import pandas as pd

df = pd.read_excel('竞品财务数据库_标准模板v2_new.xlsx', sheet_name='Database')

# 修正有空格或异常的归一化指标名称
corrections = {
    '净利 润': '净利润',
    '净 利润': '净利润',
    '毛利 ': '毛利',
    '毛 利': '毛利',
    '经营利润 ': '经营利润',
    '经营利 润': '经营利润',
    '经营利润率 ': '经营利润率',
    '经营利润 率': '经营利润率',
    '经营溢利': '经营利润',  # 港股特有叫法
    '毛 利': '毛利',
    '净利润 ': '净利润',
}

# 找出所有有空格/异常的指标名
all_names = df['归一化指标名称'].unique()
for name in all_names:
    if pd.isna(name):
        continue
    has_space = ' ' in name
    if has_space:
        clean = name.strip().replace(' ', '')
        print(f"  异常名: '{name}' -> '{clean}'")
        # 替换
        df.loc[df['归一化指标名称'] == name, '归一化指标名称'] = clean

# 归一化指标名称的标准化
df['归一化指标名称'] = df['归一化指标名称'].replace({
    '净利 润': '净利润',
    '净 利润': '净利润',
    '毛利 ': '毛利',
    '毛 利': '毛利',
    '经营利润 ': '经营利润',
    '经营利 润': '经营利润',
    '经营利润率 ': '经营利润率',
    '经营利润 率': '经营利润率',
    '经营溢利': '经营利润',
})

# 再检查
print("\n修正后所有归一化指标名:")
for n in sorted(df['归一化指标名称'].dropna().unique()):
    print(f"  '{n}'")

df.to_excel('竞品财务数据库_标准模板v2_new.xlsx', sheet_name='Database', index=False)
print("\n✅ 已修正并存档")