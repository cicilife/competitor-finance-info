import pandas as pd
import json
import sys

# Configure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read Excel file
xlsx_file = r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\网页报告\运动品牌财务数据源_网页database.xlsx'
df = pd.read_excel(xlsx_file, sheet_name='Database', header=None)

# Assign column names
df.columns = [f'col_{i}' for i in range(len(df.columns))]
df_data = df.iloc[1:].copy()  # Skip header row

# Company name mapping (Chinese/English to ID)
# Note: adidas AG is skipped as it's redundant with Adidas
name_mapping = {
    '安踏': 'anta',
    '李宁': 'lining',
    '探路者': 'tanzhe',
    '比音勒芬': 'biyorn',
    'Adidas': 'adidas',
    '斯凯奇': 'skechers',
    '安德玛': 'under_armour',
    'ASICS': 'asics',
    'Nike': 'nike',
    '捷安特': 'giant',
    '牧高笛': 'mobigadi',
    'Lululemon': 'lululemon',
    '威富集团': 'vf_corp',
    '昂跑': 'on_holding',
    '361度': '361',
    '滔搏': 'topgolf',
    '特步': 'xtep',
    '哥伦比亚': 'columbia',
    '亚玛芬': 'amer_sports',
    '彪马': 'puma',
    'Topgolf Callaway': 'topgolf',
    'Canada Goose': 'canada_goose',
    '美津浓': 'mizuno',
    '奔赴自然(伯希和）': 'berthi',
    'Uniqlo': 'uniqlo',
    'Inditex': 'inditex',
    'Decathlon SA': 'decathlon',
}

# Color mapping
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
    'uniqlo': '#000000',
    'inditex': '#000000',
    'decathlon': '#000000',
}

# Helper functions
def safe_float(val):
    if pd.isna(val):
        return None
    try:
        return float(val)
    except:
        return None

def parse_fy_year(fy_str):
    """Parse FY2025 -> 2025, FY20240531 -> 2024, etc."""
    if pd.isna(fy_str):
        return None
    fy_str = str(fy_str)
    if fy_str.startswith('FY'):
        year_str = fy_str[2:6]
        try:
            return int(year_str)
        except:
            return None
    return None

def get_region(company_name):
    """Get region based on company name"""
    regions = {
        'nike': '大中华区',
        'adidas': '大中华区',
        'anta': '中国公司',
        'lining': '中国公司',
        'tanzhe': '中国公司',
        'biyorn': '中国公司',
        'giant': '亚洲',
        'mobigadi': '中国公司',
        'xtep': '中国公司',
        '361': '中国公司',
        'berthi': '中国公司',
        'skechers': 'TOTAL',
        'under_armour': 'APAC',
        'asics': 'TOTAL',
        'lululemon': 'TOTAL',
        'vf_corp': 'APAC',
        'on_holding': 'APAC',
        'topgolf': '亚太',
        'columbia': 'LAAP',
        'amer_sports': 'TOTAL',
        'puma': 'TOTAL',
        'canada_goose': 'TOTAL',
        'mizuno': 'TOTAL',
        'uniqlo': 'TOTAL',
        'inditex': 'TOTAL',
        'decathlon': 'TOTAL',
    }
    return regions.get(company_name, 'TOTAL')

def convert_to_thousand_rmb(value, unit):
    """Convert various currency units to thousand RMB (千元)"""
    if value is None:
        return None

    unit = str(unit).strip()

    # Exchange rates
    USD_TO_CNY = 7.2
    EUR_TO_CNY = 8.17
    JPY_TO_CNY = 0.048
    CHF_TO_CNY = 8.2
    CAD_TO_CNY = 5.2
    TWD_TO_CNY = 0.22

    if unit == '千元人民币':
        return value  # Already in thousand RMB
    elif unit == '千元':
        return value  # Already in thousand RMB
    elif unit == 'RMB':
        return value / 1000  # Convert from RMB (元) to 千元
    elif unit == '百万欧元':
        return value * 1000 * EUR_TO_CNY  # Million EUR -> Thousand RMB
    elif unit == '百万美元':
        return value * 1000 * USD_TO_CNY  # Million USD -> Thousand RMB
    elif unit == '百万日元':
        return value * 1000 * JPY_TO_CNY  # Million JPY -> Thousand RMB
    elif unit == '千美元':
        return value * USD_TO_CNY  # Thousand USD -> Thousand RMB
    elif unit == '千欧元':
        return value * EUR_TO_CNY  # Thousand EUR -> Thousand RMB
    elif unit == '千CHF':
        return value * CHF_TO_CNY  # Thousand CHF -> Thousand RMB
    elif unit == '千CAD':
        return value * CAD_TO_CNY  # Thousand CAD -> Thousand RMB
    elif unit == '千新台币元' or unit == '千元TWD':
        return value * TWD_TO_CNY  # Thousand TWD -> Thousand RMB
    elif unit in ['USD', 'CHF in millions']:
        if 'CHF' in str(unit):
            return value * 1000 * CHF_TO_CNY
        return value * 1000 * USD_TO_CNY
    elif unit == '10亿日元':
        return value * 1000000 * JPY_TO_CNY  # Billion JPY -> Thousand RMB
    elif unit == 'JPY':
        return value * JPY_TO_CNY / 1000  # JPY -> Thousand RMB (rough)
    else:
        return value  # Return as-is for unknown units

# Metric name mapping
metric_mapping = {
    # Revenue metrics
    '收入': 'revenue',
    '营业收入': 'revenue',
    'Revenues': 'revenue',
    'Revenue': 'revenue',
    'Net sales': 'revenue',
    'Net revenues': 'revenue',
    'Total revenue': 'revenue',
    'Total revenues': 'revenue',
    'Net sales - Asia-Pacific': 'revenue',
    'Net sales - Greater China': 'revenue',
    'Net revenues - Greater China': 'revenue',
    'Net revenues - Asia': 'revenue',
    'Net revenues - Asia-Pacific': 'revenue',
    'Net sales - China': 'revenue',
    'Net sales - China Mainland': 'revenue',
    'Net sales - Asia and Oceania': 'revenue',
    'China sales': 'revenue',
    'Total revenue - Greater China': 'revenue',
    'Total revenue - Asia Pacific': 'revenue',

    # Gross profit metrics
    '毛利': 'gross_profit',
    '毛利润': 'gross_profit',
    'Gross profit': 'gross_profit',
    'Gross Profit': 'gross_profit',

    # Gross margin metrics
    '毛利率': 'gross_margin',
    'Gross margin': 'gross_margin',
    'Gross Margin': 'gross_margin',
    'Gross margin (% of net sales)': 'gross_margin',

    # Operating profit metrics
    '经营溢利': 'operating_profit',
    '经营利润': 'operating_profit',
    '营业利润': 'operating_profit',
    'Operating profit': 'operating_profit',
    'Operating Profit': 'operating_profit',
    'Operating income': 'operating_profit',
    'Income from operations': 'operating_profit',
    'EBIT': 'operating_profit',
    'Business Profit': 'operating_profit',
    'Operating profit - Asia-Pacific': 'operating_profit',

    # Net margin metrics
    '净利率': 'net_margin',
    '净利润率': 'net_margin',
    '淨利潤率': 'net_margin',
    'Net margin': 'net_margin',
    'Net Margin': 'net_margin',
    'Net profit': 'net_margin',
    'Net Profit': 'net_margin',
    'Net income': 'net_margin',
    'Net Income': 'net_margin',
    'Net result': 'net_margin',
    'Net margin (Net result / Net sales)': 'net_margin',
    'Net income from continuing operations': 'net_margin',
    'Net income/(loss)': 'net_margin',
    'Net income/(loss) attributable to shareholders': 'net_margin',
    'Net income from continuing operations margin': 'net_margin',
    'Net income margin': 'net_margin',
    '权益持有人应佔利润率': 'net_margin',
    '本公司权益持有人应佔利润': 'net_income',

    # Operating margin metrics
    '经营利润率': 'operating_profit_margin',
    '營運溢利率': 'operating_profit_margin',
    '經營溢利率': 'operating_profit_margin',
    'Operating margin': 'operating_profit_margin',
    'Operating Margin': 'operating_profit_margin',
    'Operating profit margin': 'operating_profit_margin',
    'Operating profit margin (% of net sales)': 'operating_profit_margin',
    'EBIT margin': 'operating_profit_margin',
    'EBIT Margin': 'operating_profit_margin',

    # Expense ratio metrics
    '广告及推广费用率': 'marketing_ratio',
    '广告费用率': 'marketing_ratio',
    'Marketing and point-of-sale expenses': 'marketing_ratio',
    'Marketing and POS expenses ratio': 'marketing_ratio',

    '员工成本率': 'labor_cost_ratio',
    '研发活动成本比率': 'rd_ratio',

    '经营费用率': 'opex_ratio',
    '运营费用率': 'opex_ratio',
    '运营费用率(SG&A)': 'opex_ratio',
    'SG&A率': 'opex_ratio',
    'SG&A ratio': 'opex_ratio',
    'SG&A expenses ratio': 'opex_ratio',
    'Operating expense ratio': 'opex_ratio',
    'Operating overhead expenses ratio': 'opex_ratio',
    'Other operating expenses ratio': 'opex_ratio',

    # Inventory metrics
    '存货周转天数': 'inventory_days',
    '平均存货周转期': 'inventory_days',
    'Days inventory outstanding (DIO)': 'inventory_days',
    'Days sales of inventory': 'inventory_days',

    # Sales per store metrics
    '单店平均零售额 / Sales per store': 'sales_per_store',
    'Sales per store': 'sales_per_store',
    '单店收入': 'sales_per_store',
}

# Build companies data
companies_data = {}

for idx, row in df_data.iterrows():
    company_name_cn = row['col_1']
    metric_name = row['col_3']
    fy_period = row['col_4']
    value = row['col_5']
    unit = row['col_6']

    # Skip if essential data is missing
    if pd.isna(company_name_cn) or pd.isna(metric_name) or pd.isna(fy_period):
        continue

    # Get company ID
    company_id = name_mapping.get(str(company_name_cn).strip())
    if not company_id:
        # Try partial match
        for cn_name, cid in name_mapping.items():
            if cn_name in str(company_name_cn):
                company_id = cid
                break
        if not company_id:
            continue

    # Parse year from FY string
    year = parse_fy_year(fy_period)
    if not year:
        continue

    # Map metric name
    json_metric = metric_mapping.get(str(metric_name).strip())
    if not json_metric:
        continue

    # Initialize company if not exists
    if company_id not in companies_data:
        companies_data[company_id] = {
            'id': company_id,
            'name': company_name_cn,
            'nameCn': company_name_cn,
            'region': get_region(company_id),
            'color': color_mapping.get(company_id, '#6B7280'),
            'years': {}
        }

    # Initialize year if not exists
    year_str = str(year)
    if year_str not in companies_data[company_id]['years']:
        companies_data[company_id]['years'][year_str] = {
            'revenue': None,
            'revenueYoy': None,
            'grossMargin': None,
            'netMargin': None,
            'operatingProfitMargin': None,
            'sameStoreSalesGrowth': None,
            'operatingExpenseRatio': None,
            'inventoryTurnoverDays': None,
            'salesPerStore': None,
            'operatingProfit': None,
        }

    # Convert value
    val = safe_float(value)
    if val is None:
        continue

    # Handle unit conversion
    if json_metric in ['revenue', 'gross_profit', 'operating_profit', 'net_income']:
        # Convert to 千元 RMB
        converted_val = convert_to_thousand_rmb(val, unit)
        if converted_val is not None:
            val = converted_val
    elif unit == '%' or '%' in str(metric_name):
        val = val  # Keep as percentage
    elif json_metric in ['gross_margin', 'net_margin', 'operating_profit_margin', 'opex_ratio',
                         'marketing_ratio', 'labor_cost_ratio', 'rd_ratio']:
        # These should be percentages
        if val > 1:
            val = val  # Already in percentage (e.g., 62 for 62%)
        else:
            val = val * 100  # Convert decimal to percentage (e.g., 0.62 -> 62%)

    # Map to correct JSON field
    year_data = companies_data[company_id]['years'][year_str]

    if json_metric == 'revenue':
        year_data['revenue'] = round(val, 2)
    elif json_metric == 'gross_profit':
        # Store gross profit temporarily, calculate margin later
        if not hasattr(companies_data[company_id], '_temp_gross_profit'):
            companies_data[company_id]['_temp_gross_profit'] = {}
        companies_data[company_id]['_temp_gross_profit'][year_str] = val
    elif json_metric == 'gross_margin':
        year_data['grossMargin'] = round(val, 1)
    elif json_metric == 'net_margin':
        year_data['netMargin'] = round(val, 1)
    elif json_metric == 'net_income':
        year_data['netMargin'] = round((val / year_data['revenue'] * 100), 1) if year_data['revenue'] else None
    elif json_metric == 'operating_profit':
        year_data['operatingProfit'] = round(val, 2)
    elif json_metric == 'operating_profit_margin':
        year_data['operatingProfitMargin'] = round(val, 1)
    elif json_metric == 'opex_ratio':
        year_data['operatingExpenseRatio'] = round(val, 1)
    elif json_metric == 'inventory_days':
        year_data['inventoryTurnoverDays'] = int(val)
    elif json_metric == 'sales_per_store':
        year_data['salesPerStore'] = round(val, 1)

# Calculate derived metrics after all data is loaded
for company_id, company_data in companies_data.items():
    years = company_data['years']

    # Calculate gross margin from gross profit and revenue if not directly available
    if '_temp_gross_profit' in company_data:
        for year_str, gross_profit in company_data['_temp_gross_profit'].items():
            if year_str in years and years[year_str]['revenue']:
                years[year_str]['grossMargin'] = round((gross_profit / years[year_str]['revenue']) * 100, 1)
        del company_data['_temp_gross_profit']

    # Calculate operating margin from operating profit and revenue
    for year_str, year_data in years.items():
        if year_data['operatingProfit'] and year_data['revenue']:
            year_data['operatingProfitMargin'] = round((year_data['operatingProfit'] / year_data['revenue']) * 100, 1)

    # Calculate revenue YOY
    for year_str in ['2024', '2025']:
        if year_str in years and str(int(year_str) - 1) in years:
            curr_rev = years[year_str]['revenue']
            prev_rev = years[str(int(year_str) - 1)]['revenue']
            if curr_rev and prev_rev and prev_rev != 0:
                yoy = ((curr_rev - prev_rev) / prev_rev) * 100
                years[year_str]['revenueYoy'] = round(yoy, 1)

# Convert to list
companies_list = list(companies_data.values())

# Sort by company name
companies_list.sort(key=lambda x: x['nameCn'])

# Remove temp attributes
for c in companies_list:
    if '_temp_gross_profit' in c:
        del c['_temp_gross_profit']

# Save to file
output_file = r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\网页报告\网页报告\financial-comparison\src\data\excelData.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(companies_list, f, ensure_ascii=False, indent=2)

print(f"Successfully parsed {len(companies_list)} companies")
print(f"Data saved to: {output_file}")

# Print summary
print("\n=== Sample Data ===")
sample_ids = ['nike', 'adidas', 'anta', 'lining', 'lululemon']
for c in companies_list:
    if c['id'] in sample_ids:
        print(f"\n{c['id']}: {c['nameCn']}")
        for year in ['2023', '2024', '2025']:
            if year in c['years']:
                y = c['years'][year]
                rev = f"{y['revenue']/1000:.0f}亿" if y['revenue'] else "-"
                gm = f"{y['grossMargin']}%" if y['grossMargin'] else "-"
                nm = f"{y['netMargin']}%" if y['netMargin'] else "-"
                print(f"  {year}: 收入={rev}, 毛利率={gm}, 净利率={nm}")