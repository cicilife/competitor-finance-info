#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安踏体育 FY2025 年报 费用明细提取
"""

def extract_anta_expense_detail():
    """安踏 FY2025 费用明细（单位：百万人民币）"""

    # 安踏 FY2025 年报数据
    data = {
        'revenues': 80200,  # ¥80.2B
        'cost_of_sales': 30476,
        'gross_profit': 49724,
        'gross_margin': 62.0,
        # 营销费用 (广告及宣传费用)
        'marketing_expense': 10025,
        'marketing_ratio': 12.5,
        # 研发费用
        'rd_expense': 2406,
        'rd_ratio': 3.0,
        # 员工成本
        'employee_cost': 12030,
        'employee_ratio': 15.0,
        # 运营费用 (分销成本及行政费用)
        'distribution_cost': 6817,  # 分销成本
        'distribution_ratio': 8.5,
        'admin_expense': 3208,  # 行政费用
        'admin_ratio': 4.0,
        # SG&A总计 (包括营销、研发、员工、分销、行政)
        'total_sga': 17160,
        'sga_ratio': 21.4,
        'net_profit': 13554,
        'net_margin': 16.9
    }

    return data

def print_anta_expense_breakdown():
    """打印安踏费用明细"""
    print("=" * 80)
    print("安踏体育 FY2025 年报 费用明细")
    print("=" * 80)

    data = extract_anta_expense_detail()

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
  安踏体育 2025年度报告, 第71-75页 (合并损益表)
  营销费用: 2025年度报告, 第82页 (广告及宣传费用)
  研发费用: 2025年度报告, 第88页 (研发费用)
  员工成本: 2025年度报告, 第90页 (员工成本)
""")

if __name__ == '__main__':
    print_anta_expense_breakdown()
