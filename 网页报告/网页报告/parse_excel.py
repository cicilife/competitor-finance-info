import pandas as pd
import json

# 读取Excel文件
xlsx_file = "/workspace/user_input_files/竞品财务数据库_标准模板 (1).xlsx"

# 读取Database sheet
df = pd.read_excel(xlsx_file, sheet_name='Database', header=None)

# 重命名列（使用列索引）
df.columns = [f'col_{i}' for i in range(len(df.columns))]

# 列索引映射
col_mapping = {
    'col_1': 'company',
    'col_2': 'region',
    # 营业收入 (千元)
    'col_3': 'revenue_2023',
    'col_4': 'revenue_2024',
    'col_5': 'revenue_2025',
    # 毛利率
    'col_14': 'gross_margin_2023',
    'col_15': 'gross_margin_2024',
    'col_16': 'gross_margin_2025',
    # 净利率
    'col_26': 'net_margin_2023',
    'col_27': 'net_margin_2024',
    'col_28': 'net_margin_2025',
    # 经营利润 (千元)
    'col_31': 'operating_profit_2023',
    'col_32': 'operating_profit_2024',
    'col_33': 'operating_profit_2025',
    # 同店销售增长
    'col_38': 'same_store_growth_2023',
    'col_39': 'same_store_growth_2024',
    'col_40': 'same_store_growth_2025',
    # 运营费用率
    'col_43': 'opex_ratio_2023',
    'col_44': 'opex_ratio_2024',
    'col_45': 'opex_ratio_2025',
    # 库存周转天数
    'col_48': 'inventory_days_2023',
    'col_49': 'inventory_days_2024',
    'col_50': 'inventory_days_2025',
    # 坪效 (千元/店)
    'col_53': 'sales_per_store_2023',
    'col_54': 'sales_per_store_2024',
    'col_55': 'sales_per_store_2025',
}

# 只保留需要的列
needed_cols = list(col_mapping.keys())
df_selected = df[needed_cols].copy()
df_selected = df_selected.rename(columns=col_mapping)

# 跳过前3行（标题行）
df_selected = df_selected.iloc[3:].copy()

# 公司名映射
name_mapping = {
    'lululemon athletica inc.': 'lululemon',
    '美津浓公司（Mizuno Corporation）': 'mizuno',
    '斯凯奇（Skechers USA, Inc.）': 'skechers',
    'Nike': 'nike',
    'Adidas AG': 'adidas',
    'ASICS Corporation': 'asics',
    '加拿大鹅控股公司': 'canada_goose',
    '彪马公司（Puma SE）': 'puma',
    '亚玛芬（Amer Sports）': 'amer_sports',
    '哥伦比亚运动服装公司': 'columbia',
    '捷安特（中国）有限公司': 'giant',
    'Topgolf Callaway Brands': 'topgolf',
    '威富集团（VF Corporation）': 'vf_corp',
    'On Holding AG（昂跑）': 'on_holding',
    '安德玛（Under Armour）': 'under_armour',
    '361度国际有限公司': '361',
    '李宁公司': 'lining',
    '安踏体育用品有限公司': 'anta',
    '杭州伯希和户外用品有限公司': 'berthi',
    '探路者控股集团股份有限公司': 'tanzhe',
    '特步国际控股有限公司': 'xtep',
    '比音勒芬服饰股份有限公司': 'biyorn',
    '牧高笛': 'mobigadi',
}

# 颜色映射
color_mapping = {
    'lululemon': '#9333EA',
    'nike': '#EA580C',
    'adidas': '#059669',
    'canada_goose': '#6B7280',
    'tanzhe': '#4F46E5',
    'anta': '#DC2626',
    'lining': '#2563EB',
    'skechers': '#7C3AED',
    'puma': '#0891B2',
    'asics': '#059669',
    'mizuno': '#84CC16',
    'columbia': '#F97316',
    'giant': '#14B8A6',
    'topgolf': '#EC4899',
    'vf_corp': '#6366F1',
    'on_holding': '#8B5CF6',
    'under_armour': '#0EA5E9',
    '361': '#10B981',
    'amer_sports': '#F59E0B',
    'berthi': '#84CC16',
    'xtep': '#EF4444',
    'biyorn': '#F472B6',
    'mobigadi': '#22D3EE',
}

# 辅助函数
def safe_float(val):
    if pd.isna(val):
        return None
    try:
        return float(val)
    except:
        return None

def safe_int(val):
    if pd.isna(val):
        return None
    try:
        return int(float(val))
    except:
        return None

# 转换数据
companies_data = []
for idx, row in df_selected.iterrows():
    company_name = row.get('company')
    if pd.isna(company_name) or str(company_name) == 'nan':
        continue

    company_id = name_mapping.get(company_name, company_name.lower().replace(' ', '_')[:15])
    color = color_mapping.get(company_id, '#6B7280')

    # 营业收入转为亿元
    revenue_2023 = safe_float(row.get('revenue_2023')) / 1000 if safe_float(row.get('revenue_2023')) else None
    revenue_2024 = safe_float(row.get('revenue_2024')) / 1000 if safe_float(row.get('revenue_2024')) else None
    revenue_2025 = safe_float(row.get('revenue_2025')) / 1000 if safe_float(row.get('revenue_2025')) else None

    # 毛利率转为百分比
    gross_margin_2023 = safe_float(row.get('gross_margin_2023')) * 100 if safe_float(row.get('gross_margin_2023')) else None
    gross_margin_2024 = safe_float(row.get('gross_margin_2024')) * 100 if safe_float(row.get('gross_margin_2024')) else None
    gross_margin_2025 = safe_float(row.get('gross_margin_2025')) * 100 if safe_float(row.get('gross_margin_2025')) else None

    # 净利率转为百分比
    net_margin_2023 = safe_float(row.get('net_margin_2023')) * 100 if safe_float(row.get('net_margin_2023')) else None
    net_margin_2024 = safe_float(row.get('net_margin_2024')) * 100 if safe_float(row.get('net_margin_2024')) else None
    net_margin_2025 = safe_float(row.get('net_margin_2025')) * 100 if safe_float(row.get('net_margin_2025')) else None

    # 经营利润转为亿元
    op_profit_2023 = safe_float(row.get('operating_profit_2023')) / 1000 if safe_float(row.get('operating_profit_2023')) else None
    op_profit_2024 = safe_float(row.get('operating_profit_2024')) / 1000 if safe_float(row.get('operating_profit_2024')) else None
    op_profit_2025 = safe_float(row.get('operating_profit_2025')) / 1000 if safe_float(row.get('operating_profit_2025')) else None

    # 计算营业利润率
    operating_margin_2023 = (op_profit_2023 / revenue_2023 * 100) if (op_profit_2023 and revenue_2023 and revenue_2023 != 0) else None
    operating_margin_2024 = (op_profit_2024 / revenue_2024 * 100) if (op_profit_2024 and revenue_2024 and revenue_2024 != 0) else None
    operating_margin_2025 = (op_profit_2025 / revenue_2025 * 100) if (op_profit_2025 and revenue_2025 and revenue_2025 != 0) else None

    # 计算收入增速
    revenue_yoy_2024 = None
    revenue_yoy_2025 = None
    if revenue_2023 and revenue_2024 and revenue_2023 != 0:
        revenue_yoy_2024 = ((revenue_2024 - revenue_2023) / revenue_2023 * 100)
    if revenue_2024 and revenue_2025 and revenue_2024 != 0:
        revenue_yoy_2025 = ((revenue_2025 - revenue_2024) / revenue_2024 * 100)

    company = {
        'id': company_id,
        'name': company_name,
        'nameCn': company_name,
        'region': row.get('region'),
        'color': color,
        'years': {
            '2023': {
                'revenue': round(revenue_2023, 2) if revenue_2023 else None,
                'revenueYoy': None,
                'grossMargin': round(gross_margin_2023, 1) if gross_margin_2023 else None,
                'netMargin': round(net_margin_2023, 1) if net_margin_2023 else None,
                'operatingProfitMargin': round(operating_margin_2023, 1) if operating_margin_2023 else None,
                'sameStoreSalesGrowth': round(safe_float(row.get('same_store_growth_2023')) * 100, 1) if safe_float(row.get('same_store_growth_2023')) else None,
                'operatingExpenseRatio': round(safe_float(row.get('opex_ratio_2023')) * 100, 1) if safe_float(row.get('opex_ratio_2023')) else None,
                'inventoryTurnoverDays': safe_int(row.get('inventory_days_2023')),
                'salesPerStore': round(safe_float(row.get('sales_per_store_2023')), 1) if safe_float(row.get('sales_per_store_2023')) else None,
                'operatingProfit': round(op_profit_2023, 2) if op_profit_2023 else None,
            },
            '2024': {
                'revenue': round(revenue_2024, 2) if revenue_2024 else None,
                'revenueYoy': round(revenue_yoy_2024, 1) if revenue_yoy_2024 else None,
                'grossMargin': round(gross_margin_2024, 1) if gross_margin_2024 else None,
                'netMargin': round(net_margin_2024, 1) if net_margin_2024 else None,
                'operatingProfitMargin': round(operating_margin_2024, 1) if operating_margin_2024 else None,
                'sameStoreSalesGrowth': round(safe_float(row.get('same_store_growth_2024')) * 100, 1) if safe_float(row.get('same_store_growth_2024')) else None,
                'operatingExpenseRatio': round(safe_float(row.get('opex_ratio_2024')) * 100, 1) if safe_float(row.get('opex_ratio_2024')) else None,
                'inventoryTurnoverDays': safe_int(row.get('inventory_days_2024')),
                'salesPerStore': round(safe_float(row.get('sales_per_store_2024')), 1) if safe_float(row.get('sales_per_store_2024')) else None,
                'operatingProfit': round(op_profit_2024, 2) if op_profit_2024 else None,
            },
            '2025': {
                'revenue': round(revenue_2025, 2) if revenue_2025 else None,
                'revenueYoy': round(revenue_yoy_2025, 1) if revenue_yoy_2025 else None,
                'grossMargin': round(gross_margin_2025, 1) if gross_margin_2025 else None,
                'netMargin': round(net_margin_2025, 1) if net_margin_2025 else None,
                'operatingProfitMargin': round(operating_margin_2025, 1) if operating_margin_2025 else None,
                'sameStoreSalesGrowth': round(safe_float(row.get('same_store_growth_2025')) * 100, 1) if safe_float(row.get('same_store_growth_2025')) else None,
                'operatingExpenseRatio': round(safe_float(row.get('opex_ratio_2025')) * 100, 1) if safe_float(row.get('opex_ratio_2025')) else None,
                'inventoryTurnoverDays': safe_int(row.get('inventory_days_2025')),
                'salesPerStore': round(safe_float(row.get('sales_per_store_2025')), 1) if safe_float(row.get('sales_per_store_2025')) else None,
                'operatingProfit': round(op_profit_2025, 2) if op_profit_2025 else None,
            }
        }
    }
    companies_data.append(company)

# 保存为JSON
output_file = '/workspace/financial-comparison/src/data/excelData.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(companies_data, f, ensure_ascii=False, indent=2)

print(f"Successfully parsed {len(companies_data)} companies")
print(f"Data saved to: {output_file}")

# 展示部分数据
print("\n" + "="*60)
print("Sample data (lululemon, nike, adidas, tanzhe, anta, lining):")
sample_ids = ['lululemon', 'nike', 'adidas', 'tanzhe', 'anta', 'lining']
for c in companies_data:
    if c['id'] in sample_ids:
        print(f"\n{c['id']}: {c['name']}")
        for year in ['2023', '2024', '2025']:
            y = c['years'][year]
            print(f"  {year}: 收入={y['revenue']}亿, 毛利率={y['grossMargin']}%, 净利率={y['netMargin']}%")