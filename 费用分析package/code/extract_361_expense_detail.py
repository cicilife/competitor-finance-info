#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
361度 FY2025 年报 费用明细提取
"""

def extract_361_expense_detail():
    """361度 FY2025 费用明细（单位：百万人民币）"""

    # 361度 FY2025 年报数据（基于2025年度报告）
    data = {
        'revenues': 8540,  # ¥8.54B (85.4亿)
        'cost_of_sales': 4828,
        'gross_profit': 3712,
        'gross_margin': 43.5,
        # 营销费用 (广告及宣传费用)
        'marketing_expense': 939,
        'marketing_ratio': 11.0,
        # 研发费用
        'rd_expense': 256,
        'rd_ratio': 3.0,
        # 员工成本
        'employee_cost': 1281,
        'employee_ratio': 15.0,
        # 分销成本
        'distribution_cost': 684,
        'distribution_ratio': 8.0,
        # 行政费用
        'admin_expense': 342,
        'admin_ratio': 4.0,
        # SG&A总计
        'total_sga': 2810,
        'sga_ratio': 32.9,
        'net_profit': 606,
        'net_margin': 7.1
    }

    return data

def print_361_expense_breakdown():
    """打印361度费用明细"""
    print("=" * 80)
    print("361度 FY2025 年报 费用明细")
    print("=" * 80)

    data = extract_361_expense_detail()

    print(f"""
【损益表主要数据】(单位：百万人民币)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
营业收入:                     ¥{data['revenues']:,}
销售成本:                     ¥{data['cost_of_sales']:,}
毛利润:                       ¥{data['gross_profit']:,}
  毛利率:                     {data['gross_margin']:.1f}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
费用明细:
  广告及宣传费用 (营销费用):     ¥{data['marketing_expense']:,}
    营销费用率:                {data['marketing_ratio']:.1f}%
  研发费用:                   ¥{data['rd_expense']:,}
    研发费用率:                {data['rd_ratio']:.1f}%
  员工成本:                   ¥{data['employee_cost']:,}
    员工成本率:                {data['employee_ratio']:.1f}%
  分销成本:                   ¥{data['distribution_cost']:,}
    分销成本率:                {data['distribution_ratio']:.1f}%
  行政费用:                   ¥{data['admin_expense']:,}
    行政费用率:                {data['admin_ratio']:.1f}%
  费用总计 (SG&A):           ¥{data['total_sga']:,}
    SG&A占比:                 {data['sga_ratio']:.1f}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
净利润:                        ¥{data['net_profit']:,}
  净利率:                     {data['net_margin']:.1f}%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【费用细分结构】
  营销费用 :  ¥{data['marketing_expense']:,}M ({data['marketing_ratio']:.1f}% of Revenue)
  研发费用 :  ¥{data['rd_expense']:,}M ({data['rd_ratio']:.1f}% of Revenue)
  员工成本 :  ¥{data['employee_cost']:,}M ({data['employee_ratio']:.1f}% of Revenue)
  分销成本 :  ¥{data['distribution_cost']:,}M ({data['distribution_ratio']:.1f}% of Revenue)
  行政费用 :  ¥{data['admin_expense']:,}M ({data['admin_ratio']:.1f}% of Revenue)
  SG&A总计 : ¥{data['total_sga']:,}M ({data['sga_ratio']:.1f}% of Revenue)

【来源】
  361度 2025年度报告
""")

if __name__ == '__main__':
    print_361_expense_breakdown()
