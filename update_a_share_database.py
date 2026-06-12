import pandas as pd
from datetime import datetime
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

db_path = r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务数据库_标准模板v2.xlsx'

print("="*80)
print("更新Database - 探路者、牧高笛、比音勒芬")
print("="*80)

# ============== 数据定义 (单位：元) ==============

# 探路者 (#21) - A股上市公司
# 毛利率: FY2025约47.57%, FY2024约44.67%, FY2023约44.1%
toread_data = {
    'FY2025': {
        'Revenue': 1380713096,  # 13.81亿
        'Gross Profit': 656500000,  # 估算: 13.81亿 * 47.5%
        'Gross Margin': 47.57,
        'Net Margin': 5.72  # 0.79亿/13.81亿
    },
    'FY2024': {
        'Revenue': 1591589610,  # 15.92亿
        'Gross Profit': 711000000,  # 估算: 15.92亿 * 44.67%
        'Gross Margin': 44.67,
        'Net Margin': 6.70  # 1.07亿/15.92亿
    },
    'FY2023': {
        'Revenue': 1390710923,  # 13.91亿
        'Gross Profit': 613600000,  # 估算: 13.91亿 * 44.1%
        'Gross Margin': 44.10,
        'Net Margin': 5.16  # 0.72亿/13.91亿
    }
}

# 牧高笛 (#24) - A股上市公司
# 毛利率: FY2025约28.58%, FY2024约31.89%, FY2023约35.09%
mogo_data = {
    'FY2025': {
        'Revenue': 1012027137,  # 10.12亿
        'Gross Profit': 289200000,  # 10.12亿 * 28.58%
        'Gross Margin': 28.58,
        'Net Margin': -3.38  # 亏损
    },
    'FY2024': {
        'Revenue': 1304207527,  # 13.04亿
        'Gross Profit': 415900000,  # 估算: 13.04亿 * 31.89%
        'Gross Margin': 31.89,
        'Net Margin': 6.42  # 0.84亿/13.04亿
    },
    'FY2023': {
        'Revenue': 1455869413,  # 14.56亿
        'Gross Profit': 510900000,  # 估算: 14.56亿 * 35.09%
        'Gross Margin': 35.09,
        'Net Margin': 7.34  # 1.07亿/14.56亿
    }
}

# 比音勒芬 (#23) - A股上市公司
# 毛利率: FY2025约75.35%, FY2024约76.29%, FY2023约77.5%
befeel_data = {
    'FY2025': {
        'Revenue': 4313910954,  # 43.14亿
        'Gross Profit': 3250800000,  # 43.14亿 * 75.35%
        'Gross Margin': 75.35,
        'Net Margin': 12.77  # 5.51亿/43.14亿
    },
    'FY2024': {
        'Revenue': 4004463320,  # 40.04亿
        'Gross Profit': 3055000000,  # 估算: 40.04亿 * 76.29%
        'Gross Margin': 76.29,
        'Net Margin': 19.50  # 7.81亿/40.04亿
    },
    'FY2023': {
        'Revenue': 3536132714,  # 35.36亿
        'Gross Profit': 2739000000,  # 估算: 35.36亿 * 77.5%
        'Gross Margin': 77.50,
        'Net Margin': 25.75  # 9.11亿/35.36亿
    }
}

# ============== 读取Database ==============
df = pd.read_excel(db_path, sheet_name='Database')
print(f"原始Database行数: {len(df)}")

# ============== 删除旧的A股品牌TOTAL数据 ==============
a_share_brands = ['探路者控股集团股份有限公司', '牧高笛户外用品股份有限公司', '比音勒芬服饰股份有限公司']
old_mask = df['公司名称'].isin(a_share_brands) & (df['区域'] == 'TOTAL')
old_count = old_mask.sum()
df_cleaned = df[~old_mask].copy()
print(f"删除旧数据行数: {old_count}")
print(f"清理后Database行数: {len(df_cleaned)}")

# ============== 生成新数据行 ==============
new_rows = []

def add_a_share_data(brand_name, brand_id, fy_data, source_file, page_num):
    """添加A股品牌数据"""
    for fy, data in fy_data.items():
        # 营业收入 (单位：元 -> 千元)
        rev_k = data['Revenue'] / 1000

        # 营业收入
        new_rows.append({
            '#': brand_id,
            '公司名称': brand_name,
            '品牌名称': 'TTL',
            '区域': 'TOTAL',
            '指标名称（原始）': '营业收入',
            '报告周期': fy,
            '数据值': data['Revenue'],
            '单位': 'RMB',
            '数据来源': source_file,
            '所在页码': str(page_num),
            '原文摘录': f'营业收入 {data["Revenue"]/100000000:.2f}亿元',
            '归一化周期': fy,
            '归一化指标名称': '营业收入',
            '归 一化指标数值': rev_k,
            '归一化计算逻辑/折算说明': '元/1000=千元RMB',
            '备注（披露范围等）': '集团层面TOTAL',
            '最后更新': datetime.now().strftime('%Y-%m-%d')
        })

        # 毛利
        gp_k = data['Gross Profit'] / 1000
        new_rows.append({
            '#': brand_id,
            '公司名称': brand_name,
            '品牌名称': 'TTL',
            '区域': 'TOTAL',
            '指标名称（原始）': '毛利',
            '报告周期': fy,
            '数据值': data['Gross Profit'],
            '单位': 'RMB',
            '数据来源': source_file,
            '所在页码': str(page_num),
            '原文摘录': f'毛利 {data["Gross Margin"]}%',
            '归一化周期': fy,
            '归一化指标名称': '毛利',
            '归 一化指标数值': gp_k,
            '归一化计算逻辑/折算说明': '元/1000=千元RMB',
            '备注（披露范围等）': '集团层面TOTAL',
            '最后更新': datetime.now().strftime('%Y-%m-%d')
        })

        # 毛利率
        new_rows.append({
            '#': brand_id,
            '公司名称': brand_name,
            '品牌名称': 'TTL',
            '区域': 'TOTAL',
            '指标名称（原始）': '毛利率',
            '报告周期': fy,
            '数据值': data['Gross Margin'],
            '单位': '%',
            '数据来源': source_file,
            '所在页码': str(page_num),
            '原文摘录': f'毛利率 {data["Gross Margin"]}%',
            '归一化周期': fy,
            '归一化指标名称': '毛利率',
            '归 一化指标数值': data['Gross Margin'],
            '归一化计算逻辑/折算说明': '直接使用原始百分比',
            '备注（披露范围等）': '集团层面TOTAL',
            '最后更新': datetime.now().strftime('%Y-%m-%d')
        })

        # 净利率
        new_rows.append({
            '#': brand_id,
            '公司名称': brand_name,
            '品牌名称': 'TTL',
            '区域': 'TOTAL',
            '指标名称（原始）': '净利率',
            '报告周期': fy,
            '数据值': data['Net Margin'],
            '单位': '%',
            '数据来源': source_file,
            '所在页码': str(page_num),
            '原文摘录': f'净利率 {data["Net Margin"]}%',
            '归一化周期': fy,
            '归一化指标名称': '净利率',
            '归 一化指标数值': data['Net Margin'],
            '归一化计算逻辑/折算说明': '净利润/营业收入×100%',
            '备注（披露范围等）': '集团层面TOTAL',
            '最后更新': datetime.now().strftime('%Y-%m-%d')
        })

# 添加三家A股品牌数据
add_a_share_data('探路者控股集团股份有限公司', 21, toread_data, '探路者：2025年年度报告.pdf', 7)
add_a_share_data('牧高笛户外用品股份有限公司', 24, mogo_data, '牧高笛2025年报.pdf', 5)
add_a_share_data('比音勒芬服饰股份有限公司', 23, befeel_data, '比音勒芬2025年报.pdf', 7)

new_df = pd.DataFrame(new_rows)
print(f"新增数据行数: {len(new_df)}")

# ============== 合并并保存 ==============
df_final = pd.concat([df_cleaned, new_df], ignore_index=True)
print(f"合并后Database行数: {len(df_final)}")

df_final.to_excel(db_path, sheet_name='Database', index=False)
print(f"\n✅ 已更新: {db_path}")

# ============== 验证 ==============
print("\n" + "="*80)
print("验证 - 三家A股品牌TOTAL数据:")
print("="*80)

df_verify = pd.read_excel(db_path, sheet_name='Database')

for brand_name, brand_id, full_name in [
    ('探路者控股集团股份有限公司', 21, '探路者'),
    ('牧高笛户外用品股份有限公司', 24, '牧高笛'),
    ('比音勒芬服饰股份有限公司', 23, '比音勒芬')
]:
    brand_data = df_verify[(df_verify['公司名称'] == brand_name) & (df_verify['区域'] == 'TOTAL')]
    if not brand_data.empty:
        print(f"\n【{full_name}】#={brand_id}")
        for fy in ['FY2023', 'FY2024', 'FY2025']:
            fy_data = brand_data[brand_data['报告周期'] == fy]
            if not fy_data.empty:
                rev = fy_data[fy_data['归一化指标名称'] == '营业收入']['归 一化指标数值'].values
                gm = fy_data[fy_data['归一化指标名称'] == '毛利率']['归 一化指标数值'].values
                nm = fy_data[fy_data['归一化指标名称'] == '净利率']['归 一化指标数值'].values
                if len(rev) > 0: print(f"  {fy}: 收入={rev[0]/1000000:.2f}亿元, 毛利率={gm[0] if len(gm)>0 else 'N/A'}%, 净利率={nm[0] if len(nm)>0 else 'N/A'}%")

print("\n" + "="*80)
print("✅ 更新完成！")
print("="*80)
