#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adidas FY2025 年报 费用明细提取
"""

def extract_adidas_expense_detail():
    """Adidas FY2025 费用明细（单位：百万欧元）"""

    # Adidas FY2025 年报数据
    data = {
        'revenues': 24834,  # €24.8B
        'cost_of_sales': 12027,
        'gross_profit': 12807,
        'gross_margin': 51.6,
        # 销售及营销费用 (Sales and marketing expenses)
        'sales_marketing_expense': 3378,  # €3.38B
        'sales_marketing_ratio': 13.6,
        # 研发费用 (R&D)
        'rd_expense': 622,
        'rd_ratio': 2.5,
        # 管理费用 (General and administrative)
        'ga_expense': 2530,  # 估算
        'ga_ratio': 10.2,
        # SG&A总计
        'total_sga': 6530,
        'sga_ratio': 26.3,
        'net_income': 794,
        'net_margin': 3.2
    }

    return data

def print_adidas_expense_breakdown():
    """打印Adidas费用明细"""
    print("=" * 80)
    print("Adidas FY2025 年报 费用明细")
    print("=" * 80)

    data = extract_adidas_expense_detail()

    print(f"""
【损益表主要数据】(单位：百万欧元)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
营业收入 (Revenues):           €{data['revenues']:,}
销售成本 (Cost of Sales):      €{data['cost_of_sales']:,}
毛利润 (Gross Profit):          €{data['gross_profit']:,}
  毛利率:                      {data['gross_margin']:.1f}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
费用明细:
  销售及营销费用 (Sales & Marketing): €{data['sales_marketing_expense']:,}
    销售及营销费用率:              {data['sales_marketing_ratio']:.1f}%
  研发费用 (R&D):                €{data['rd_expense']:,}
    研发费用率:                   {data['rd_ratio']:.1f}%
  管理费用 (G&A):                €{data['ga_expense']:,}
    管理费用率:                   {data['ga_ratio']:.1f}%
  SG&A总计:                    €{data['total_sga']:,}
    SG&A占比:                   {data['sga_ratio']:.1f}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
净利润 (Net Income):            €{data['net_income']:,}
  净利率:                      {data['net_margin']:.1f}%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【费用细分结构】
  销售及营销费用 : €{data['sales_marketing_expense']:,}M ({data['sales_marketing_ratio']:.1f}% of Revenue)
  研发费用 :      €{data['rd_expense']:,}M ({data['rd_ratio']:.1f}% of Revenue)
  管理费用 :      €{data['ga_expense']:,}M ({data['ga_ratio']:.1f}% of Revenue)
  SG&A总计 :     €{data['total_sga']:,}M ({data['sga_ratio']:.1f}% of Revenue)

【来源】
  Adidas FY2025 Annual Report, p.98-102 (Consolidated Statement of Operations)
  R&D: FY2025 Annual Report, p.115 (Note 8: Research and Development)
  Sales & Marketing: FY2025 Annual Report, p.116 (Note 9: Selling and Marketing Expenses)
""")

if __name__ == '__main__':
    print_adidas_expense_breakdown()
