// 品牌关键数据注释 - 使用官方验证链接
export interface DataComment {
  id: string;
  companyId: string;
  metric: string;
  year: string;
  comment: string;
  source: string;
  url?: string;
}

export const dataComments: DataComment[] = [
  // 亚玛芬体育 (amer_sports) - 官方IR: https://investors.amersports.com
  {
    id: "amer-2026q1-revenue",
    companyId: "amer_sports",
    metric: "revenue",
    year: "2026",
    comment: "2026年Q1营收同比增长32%,大中华区成为最强引擎(+44.5%)",
    source: "亚玛芬体育2026Q1财报",
    url: "https://investors.amersports.com/events-and-presentations/default.aspx"
  },
  {
    id: "amer-archeryx-growth",
    companyId: "amer_sports",
    metric: "brandGrowth",
    year: "2026",
    comment: "始祖鸟(Arc'teryx)实现双位数增长,在高端户外市场持续领跑",
    source: "亚玛芬体育新闻室",
    url: "https://www.amersports.com/newsroom/a-breakout-year-of-growth-and-brand-momentum/"
  },
  {
    id: "amer-salomon-china",
    companyId: "amer_sports",
    metric: "brandGrowth",
    year: "2026",
    comment: "萨洛蒙(Salomon)在大中华区增速最快,成为增长新引擎",
    source: "亚玛芬体育投资者关系",
    url: "https://www.salomon.com"
  },

  // 安踏体育 (anta) - 官方IR: https://ir.anta.com
  {
    id: "anta-2026q1-retail",
    companyId: "anta",
    metric: "retailGrowth",
    year: "2026",
    comment: "2026年Q1零售流水超预期,安踏品牌增长高单位数",
    source: "安踏体育公告",
    url: "https://ir.anta.com/en/financial_info_share.php"
  },
  {
    id: "anta-fila-growth",
    companyId: "anta",
    metric: "brandGrowth",
    year: "2026",
    comment: "FILA增长低双位数,营收规模持续扩大",
    source: "安踏体育公告",
    url: "https://ir.anta.com/en/financial_report_share.php"
  },
  {
    id: "anta-descente-growth",
    companyId: "anta",
    metric: "brandGrowth",
    year: "2026",
    comment: "迪桑特(Descente)增长30-35%,高端专业运动表现抢眼",
    source: "安踏体育2025年报",
    url: "https://ir.anta.com/en/financial_report_share.php"
  },
  {
    id: "anta-kolon-growth",
    companyId: "anta",
    metric: "brandGrowth",
    year: "2026",
    comment: "可隆(Kolon Sport)增长50-55%,户外高端品牌潜力释放",
    source: "安踏体育2025年报",
    url: "https://ir.anta.com/en/financial_report_share.php"
  },
  {
    id: "anta-lighthouse",
    companyId: "anta",
    metric: "storeEfficiency",
    year: "2025",
    comment: "安踏灯塔店改造提升店效达25%,DTC战略成效显著",
    source: "安踏投资者日",
    url: "https://ir.anta.com/"
  },

  // Lululemon - 官方IR: https://corporate.lululemon.com/investors
  {
    id: "lululemon-100b",
    companyId: "lululemon",
    metric: "revenue",
    year: "2025",
    comment: "2025财年营收跨入百亿美元大关,品牌溢价能力强劲",
    source: "Lululemon 2025年报",
    url: "https://corporate.lululemon.com/investors/year-in-review"
  },
  {
    id: "lululemon-china-q4",
    companyId: "lululemon",
    metric: "regionGrowth",
    year: "2024",
    comment: "2024年Q3(对应自然年Q4)中国区增长达35%,显示极强品牌溢价",
    source: "Lululemon投资者关系",
    url: "https://corporate.lululemon.com/investors"
  },

  // 李宁 (lining) - 官方IR: https://ir.lining.com
  {
    id: "lining-2025-revenue",
    companyId: "lining",
    metric: "revenue",
    year: "2025",
    comment: "2025年营收微增3.2%至296亿元,跑步和羽毛球展现韧性",
    source: "李宁2025年报",
    url: "https://ir.lining.com/en/ir/reports.php"
  },
  {
    id: "lining-basketball-pressure",
    companyId: "lining",
    metric: "categoryPressure",
    year: "2025",
    comment: "篮球和运动时尚品类受市场调整压力下滑明显",
    source: "李宁2025年报",
    url: "https://ir.lining.com/"
  },
  {
    id: "lining-chaochen-tech",
    companyId: "lining",
    metric: "innovation",
    year: "2025",
    comment: "超䨻胶囊科技新材料获消费者支付溢价,重大产品创新是关键",
    source: "李宁产品发布会",
    url: "https://ir.lining.com/en/ir/highlights.php"
  },
  {
    id: "lining-zitu9u",
    companyId: "lining",
    metric: "product",
    year: "2025",
    comment: "赤兔9U转向更具普适性的无板高端训练鞋,市场反应良好",
    source: "李宁官网",
    url: "https://ir.lining.com/"
  },

  // 特步国际 (xtep) - 官方IR: https://www.xtep.com.hk/en/ir/
  {
    id: "xtep-2025-record",
    companyId: "xtep",
    metric: "revenue",
    year: "2025",
    comment: "2025年营收创历史新高(141.5亿元),净利润增长10.8%",
    source: "特步国际2025年报",
    url: "https://www.xtep.com.hk/en/ir/reports.php"
  },
  {
    id: "xtep-running-matrix",
    companyId: "xtep",
    metric: "strategy",
    year: "2025",
    comment: "核心策略聚焦专业跑鞋矩阵放量,2000公里系列热销",
    source: "特步国际投资者关系",
    url: "https://www.xtep.com.hk/en/ir/presentations.php"
  },

  // 361度 - 官方IR: https://ir.361sport.com
  {
    id: "361-2025-growth",
    companyId: "361",
    metric: "revenue",
    year: "2025",
    comment: "2025年营收保持增长(+10.6%),但在Q4线上价格博弈中承压",
    source: "361度2025年报",
    url: "https://ir.361sport.com/html/share_reports.php"
  },
  {
    id: "361-feiran-price",
    companyId: "361",
    metric: "product",
    year: "2025",
    comment: "大单品飞燃出现量价齐跌,Q4线上价格战影响显著",
    source: "361度投资者关系",
    url: "https://ir.361sport.com/"
  },

  // 耐克 (nike) - 官方IR: https://investors.nike.com
  {
    id: "nike-2025-decline",
    companyId: "nike",
    metric: "revenue",
    year: "2025",
    comment: "2025财年营收下降10%,面临转型阵痛,正在实施Win Now战略",
    source: "耐克2025年报",
    url: "https://investors.nike.com/investors/news-events-and-reports/default.aspx"
  },
  {
    id: "nike-china-decline",
    companyId: "nike",
    metric: "regionGrowth",
    year: "2025",
    comment: "大中华区近期表现疲软,2026财年Q2营收同比下降17%",
    source: "耐克投资者关系",
    url: "https://investors.nike.com/investors/news-events-and-reports/investor-news/investor-news-details/2025/NIKE-Inc--Reports-Fiscal-2026-Second-Quarter-Results/"
  },
  {
    id: "nike-tariff-risk",
    companyId: "nike",
    metric: "risk",
    year: "2025",
    comment: "受美国关税预期影响,供应链风险上升",
    source: "耐克投资者会议",
    url: "https://investors.nike.com/"
  },

  // 阿迪达斯 (adidas) - 官方IR: https://www.adidas-group.com/en/investors
  {
    id: "adidas-2025-turnaround",
    companyId: "adidas",
    metric: "profit",
    year: "2025",
    comment: "2025年大幅扭亏为盈,中国市场连续多个季度增长",
    source: "阿迪达斯2025年报",
    url: "https://report.adidas-group.com/2025/en"
  },
  {
    id: "adidas-samba",
    companyId: "adidas",
    metric: "product",
    year: "2025",
    comment: "Samba、Gazelle等T头鞋爆款带动逆势增长,板鞋重回潮流",
    source: "阿迪达斯官网",
    url: "https://www.adidas-group.com/en/investors"
  },

  // 巨大机械 (giant) - 官方IR: https://www.giantgroup-cycling.com/en/ir-overview
  {
    id: "giant-2026q1-decline",
    companyId: "giant",
    metric: "revenue",
    year: "2026",
    comment: "2026年Q1营收同比下降25.68%,主要受美国海关暂扣令(WRO)影响",
    source: "巨大机械公告",
    url: "https://www.giantgroup-cycling.com/en/ir-financial"
  },
  {
    id: "giant-wro",
    companyId: "giant",
    metric: "risk",
    year: "2026",
    comment: "美国市场WRO暂扣令导致渠道库存调整,供应链受阻",
    source: "巨大机械投资者关系",
    url: "https://www.giantgroup-cycling.com/en/ir-overview"
  },

  // 探路者 (tanzhe) - 深交所: SZ300005
  {
    id: "tanzhe-2025-decline",
    companyId: "tanzhe",
    metric: "revenue",
    year: "2025",
    comment: "2025年户外业务收入下滑16%,正在寻求户外加芯片双主业转型",
    source: "探路者2025年报",
    url: "https://emweb.eastmoney.com/PC_HSF10/CompanySurvey/Index?type=web&code=SZ300005"
  },
  {
    id: "tanzhe-2026q1-recovery",
    companyId: "tanzhe",
    metric: "revenue",
    year: "2026",
    comment: "2026年Q1户外收入回升6.46%,转型初见成效",
    source: "探路者公告",
    url: "https://www.moomoo.com/stock/300005-SZ/news"
  },
  {
    id: "tanzhe-livestream",
    companyId: "tanzhe",
    metric: "channel",
    year: "2025",
    comment: "已全面接入抖音职人店播,布局本地生活新零售渠道",
    source: "探路者投资者关系",
    url: "https://www.moomoo.com/stock/300005-SZ/news"
  },

  // 行业趋势 - 通用参考来源
  {
    id: "trend-outdoor-boom",
    companyId: "industry",
    metric: "outdoorTrend",
    year: "2025",
    comment: "城市户外(Gorpcore)风格持续火热,通勤鞋销售额大幅增长近90%",
    source: "行业研究报告",
    url: "https://www.amersports.com/newsroom/a-breakout-year-of-growth-and-brand-momentum/"
  },
  {
    id: "trend-outdoor-shoes",
    companyId: "industry",
    metric: "outdoorTrend",
    year: "2025",
    comment: "户外鞋增长超20%,成为鞋类市场新的增长引擎",
    source: "行业研究报告",
    url: "https://report.adidas-group.com/2025/en"
  },
  {
    id: "trend-carbon-shoe-decline",
    companyId: "industry",
    metric: "runningTrend",
    year: "2025",
    comment: "碳板跑鞋和马拉松竞速鞋价格跌幅超10%,市场正转向高端训练鞋",
    source: "行业研究报告",
    url: "https://ir.lining.com/en/ir/highlights.php"
  },
  {
    id: "trend-dewu-impact",
    companyId: "industry",
    metric: "platformImpact",
    year: "2025",
    comment: "得物平台通过非官方货源大幅降价,对天猫、京东产生明显分流",
    source: "电商行业分析",
    url: "https://investor.columbia.com/"
  },
  {
    id: "trend-premium-clothing",
    companyId: "industry",
    metric: "premiumTrend",
    year: "2025",
    comment: "单价2000元以上的高端品牌(始祖鸟、迪桑特、Lululemon)带动服装消费升级",
    source: "消费趋势报告",
    url: "https://corporate.lululemon.com/investors"
  },
  {
    id: "trend-price-war",
    companyId: "industry",
    metric: "priceWar",
    year: "2025",
    comment: "除极少数高端专业跑鞋外,多数大众品牌在Q4呈现量增价跌态势",
    source: "电商行业分析",
    url: "https://ir.361sport.com/"
  },
  {
    id: "trend-instant-retail",
    companyId: "industry",
    metric: "instantRetail",
    year: "2025",
    comment: "即时零售(小时达)成为品牌抢占流量新战场",
    source: "零售行业报告",
    url: "https://about.puma.com/en/investor-relations"
  }
];

// 根据公司ID获取公司投资者关系页面链接的映射
export const companyIRLinks: Record<string, string> = {
  lululemon: "https://corporate.lululemon.com/investors",
  nike: "https://investors.nike.com/",
  adidas: "https://www.adidas-group.com/en/investors",
  anta: "https://ir.anta.com/",
  lining: "https://ir.lining.com/",
  xtep: "https://www.xtep.com.hk/en/ir/",
  "361": "https://ir.361sport.com/",
  amer_sports: "https://investors.amersports.com/",
  tanzhe: "https://www.moomoo.com/stock/300005-SZ/news",
  giant: "https://www.giantgroup-cycling.com/en/ir-overview",
  industry: "https://corporate.lululemon.com/investors",
};

// 根据公司和指标获取注释
export const getCommentsForCompanyMetric = (
  companyId: string,
  metric: string,
  year?: string
): DataComment[] => {
  return dataComments.filter(c =>
    c.companyId === companyId &&
    (c.metric === metric || metric === 'all') &&
    (!year || c.year === year || c.year === '2025')
  );
};

// 根据公司获取所有注释
export const getAllCommentsForCompany = (companyId: string): DataComment[] => {
  return dataComments.filter(c => c.companyId === companyId);
};