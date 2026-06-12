"""
添加VF Corporation亚太区数据
数据来源:
- VF 2025 Annual Report P74-75 (Geographic revenues)
"""
import pandas as pd
from datetime import datetime

df = pd.read_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database')

usd_to_cny = 7.2  # 美元兑人民币

# ============ VF Corporation亚太区数据 ============
# 来源: VF 2025 Annual Report P74-75 (Geographic revenues by segment)
vf_apac_data = [
    {
        '报告周期': 'FY2025',
        '指标名称（原始）': 'Net sales - Asia Pacific',
        '数据值': 1403264,
        '单位': '千美元',
        '原文摘录': 'Asia-Pacific $1,403,264 thousand (FY2025)',
        'source_file': 'VF 2025 Annual Report.pdf',
        'page': '74-75',
    },
    {
        '报告周期': 'FY2024',
        '指标名称（原始）': 'Net sales - Asia Pacific',
        '数据值': 1403264,
        '单位': '千美元',
        '原文摘录': 'Asia-Pacific $1,403,264 thousand (FY2024)',
        'source_file': 'VF 2025 Annual Report.pdf',
        'page': '74-75',
    },
]

# 指标中文映射
indicator_cn_map = {
    'Net sales - Asia Pacific': '营业收入',
}

# 添加记录
new_rows = []
today = datetime.now().strftime('%Y-%m-%d')

def process_data(data_list, company_name, brand_name, region, conversion_rate):
    for item in data_list:
        fy = item['报告周期']
        indicator = item['指标名称（原始）']
        dup_mask = (df['公司名称'] == company_name) & \
                   (df['品牌名称'] == brand_name) & \
                   (df['区域'] == region) & \
                   (df['报告周期'] == fy) & \
                   (df['指标名称（原始）'] == indicator)
        
        if dup_mask.any():
            print(f"  [跳过] {company_name} | {brand_name} | {fy} (已存在)")
            continue
        
        val = item['数据值']
        normalized_val = val * conversion_rate
        calc_logic = f'{item["单位"]}×{conversion_rate}=千元人民币'
        
        new_row = {
            '#': len(df) + len(new_rows) + 1,
            '公司名称': company_name,
            '品牌名称': brand_name,
            '区域': region,
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
            '备注（披露范围等）': region,
            '最后更新': today,
        }
        new_rows.append(new_row)
        print(f"  [新增] {company_name} | {brand_name} | {fy} | {val:,} 千美元 -> {normalized_val:,.0f} 千元")

print("="*60)
print("VF Corporation 亚太区数据")
print("="*60)
process_data(vf_apac_data, 'VF Corporation', 'VF', '亚太区', usd_to_cny)

if new_rows:
    df_new = pd.DataFrame(new_rows)
    df = pd.concat([df, df_new], ignore_index=True)
    df.to_excel('竞品财务数据库_标准模板v2.xlsx', sheet_name='Database', index=False)
    print(f"\n{'='*60}")
    print(f"✅ 共新增 {len(new_rows)} 条记录")
else:
    print("\n⚠️ 没有新记录需要添加")

# 验证VF数据
print("\n" + "="*60)
print("验证 - VF Corporation数据")
print("="*60)
vf_mask = df['公司名称'] == 'VF Corporation'
vf_data = df[vf_mask][['公司名称', '品牌名称', '报告周期', '数据值', '单位', '归一化指标数值']]
print(vf_data.sort_values(['品牌名称', '报告周期']).to_string(index=False))
