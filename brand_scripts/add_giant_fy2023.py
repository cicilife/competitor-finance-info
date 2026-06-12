"""
添加捷安特FY2023亚太区数据
数据来源:
- Giant 2023 annual report.pdf P106
"""
import pandas as pd
from datetime import datetime

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

twd_to_cny = 0.23  # 新台币兑人民币

# ============ 捷安特FY2023亚太区数据 ============
# 来源: Giant 2023 annual report.pdf P106
giant_fy2023_data = [
    {
        '报告周期': 'FY2023',
        '指标名称（原始）': 'Net sales - Asia Pacific',
        '数据值': 28802022,
        '单位': '千新台币元',
        '原文摘录': 'Asia Sales 28,802,022 NTD thousands (FY2023, 37.43%)',
        'source_file': 'Giant 2023 annual report.pdf',
        'page': 106,
    },
]

# 指标中文映射
indicator_cn_map = {
    'Net sales - Asia Pacific': '营业收入',
}

# 添加记录
new_rows = []
today = datetime.now().strftime('%Y-%m-%d')

print("="*60)
print("捷安特(GIANT) FY2023 亚太区数据")
print("="*60)

for item in giant_fy2023_data:
    fy = item['报告周期']
    indicator = item['指标名称（原始）']
    dup_mask = (df['公司名称'] == '捷安特股份有限公司') & \
               (df['品牌名称'] == 'GIANT') & \
               (df['区域'] == '亚太区') & \
               (df['报告周期'] == fy) & \
               (df['指标名称（原始）'] == indicator)
    
    if dup_mask.any():
        print(f"  [跳过] GIANT | {fy} (已存在)")
    else:
        val = item['数据值']
        normalized_val = val * twd_to_cny
        calc_logic = f'{item["单位"]}×{twd_to_cny}=千元人民币'
        
        new_row = {
            '#': len(df) + len(new_rows) + 1,
            '公司名称': '捷安特股份有限公司',
            '品牌名称': 'GIANT',
            '区域': '亚太区',
            '指标名称（原始）': indicator,
            '报告周期': fy,
            '数据值': val,
            '单位': item['单位'],
            '数据来源': item['source_file'],
            '所在页码': item['page'],
            '原文摘录': item['原文摘录'],
            '归一化周期': fy,
            '归一化指标名称': indicator_cn_map.get(indicator, ''),
            '归一化指标数值': normalized_val,
            '归一化计算逻辑/折算说明': calc_logic,
            '备注（披露范围等）': '亚太区',
            '最后更新': today,
        }
        new_rows.append(new_row)
        print(f"  [新增] GIANT | {fy} | {val:,} 千新台币 -> {normalized_val:,.0f} 千元")

if new_rows:
    df_new = pd.DataFrame(new_rows)
    df = pd.concat([df, df_new], ignore_index=True)
    df.to_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database', index=False)
    print(f"\n{'='*60}")
    print(f"✅ 共新增 {len(new_rows)} 条记录")
else:
    print("\n⚠️ 没有新记录需要添加")

# 验证
print("\n" + "="*60)
print("验证 - GIANT 亚太区数据")
print("="*60)
giant_mask = (df['公司名称'] == '捷安特股份有限公司') & (df['品牌名称'] == 'GIANT')
giant_data = df[giant_mask][['公司名称', '品牌名称', '报告周期', '数据值', '单位', '归一化指标数值']].sort_values('报告周期')
print(giant_data.to_string(index=False))
