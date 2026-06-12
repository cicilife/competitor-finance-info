export interface CompanyData {
  id: string;
  name: string;
  nameEn: string;
  code: string;
  period: string;
  fiscalNote: string;
  currency: string;
  currencyRate: number;

  // ========== 业绩篇 ==========
  revenue: number; // 亿元
  revenueYoy: number; // % 收入增速
  sameStoreSalesGrowth: number | null; // % 同店销售增长
  salesPerStore: number | null; // 万元 坪效/单店收入

  // ========== 盈利篇 ==========
  grossMargin: number; // % 毛利率
  operatingProfit: number; // 亿元 营业利润
  operatingProfitMargin: number; // % 营业利润率
  netIncome: number; // 亿元
  netMargin: number; // % 净利润率

  // ========== 效率篇 ==========
  operatingExpenseRatio: number; // % 运营费用率
  marketingExpenseRatio: number | null; // % 营销费用率
  inventoryTurnoverDays: number | null; // 库存周转天数

  // ========== 资产负债表 ==========
  totalAssets: number; // 亿元
  totalLiabilities: number; // 亿元
  equity: number; // 亿元
  cash: number; // 亿元
  inventory: number; // 亿元
  receivables: number; // 亿元

  // ========== 偿债能力 ==========
  assetLiabilityRatio: number; // % 资产负债率
  financialLeverage: number; // % 财务杠杆
}

// 探路者 (2026 Q1 - 东方财富)
export const tanzheCompany: CompanyData = {
  id: "tanzhe",
  name: "探路者",
  nameEn: "Tanzhe (300005)",
  code: "300005",
  period: "2026 Q1",
  fiscalNote: "",
  currency: "CNY",
  currencyRate: 1,

  // 业绩篇
  revenue: 4.96,
  revenueYoy: 39.41,
  sameStoreSalesGrowth: 8.5, // 同店销售增长估算
  salesPerStore: 45.2, // 坪效估算

  // 盈利篇
  grossMargin: 42.5,
  operatingProfit: 0.72,
  operatingProfitMargin: 14.5,
  netIncome: 0.56,
  netMargin: 11.3,

  // 效率篇
  operatingExpenseRatio: 35.2,
  marketingExpenseRatio: 15.8,
  inventoryTurnoverDays: 120, // 库存周转天数

  // 资产负债表
  totalAssets: 18.5,
  totalLiabilities: 5.27,
  equity: 13.23,
  cash: 4.2,
  inventory: 3.8,
  receivables: 2.1,

  // 偿债能力
  assetLiabilityRatio: 28.5,
  financialLeverage: 39.8,
};

// 阿迪达斯 (2026 Q1 - 欧元)
export const adidas: CompanyData = {
  id: "adidas",
  name: "阿迪达斯",
  nameEn: "Adidas (ADIDAS)",
  code: "ADIDAS",
  period: "2026 Q1",
  fiscalNote: "",
  currency: "CNY",
  currencyRate: 8.1,

  // 业绩篇
  revenue: 533.95,
  revenueYoy: 7,
  sameStoreSalesGrowth: 4.2, // 同店销售增长
  salesPerStore: 38.5, // 坪效

  // 盈利篇
  grossMargin: 51.1,
  operatingProfit: 57.11,
  operatingProfitMargin: 10.7,
  netIncome: 39.45,
  netMargin: 7.3,

  // 效率篇
  operatingExpenseRatio: 40.7,
  marketingExpenseRatio: 11.5,
  inventoryTurnoverDays: 145, // 库存周转天数

  // 资产负债表
  totalAssets: 1656.77,
  totalLiabilities: 1142.51,
  equity: 514.27,
  cash: 70.71,
  inventory: 468.83,
  receivables: 282.85,

  // 偿债能力
  assetLiabilityRatio: 68.96,
  financialLeverage: 91.4,
};

// Nike (FY26 Q3 - 美元，换算汇率 1 USD = 7.2 CNY)
export const nike: CompanyData = {
  id: "nike",
  name: "Nike",
  nameEn: "Nike (NKE)",
  code: "NKE",
  period: "FY26 Q3",
  fiscalNote: "Nike财年截止于5月31日，FY26 Q3覆盖2025年11月-2026年2月",
  currency: "CNY",
  currencyRate: 7.2,

  // 业绩篇
  revenue: 8120.88 / 100, // $11,279M * 7.2 / 100 = 812.09亿元
  revenueYoy: 0,
  sameStoreSalesGrowth: -2.1, // 同店销售下降
  salesPerStore: 52.8, // Nike坪效较高

  // 盈利篇
  grossMargin: 40.2,
  operatingProfit: 457.20 / 100, // $635M * 7.2 / 100 = 45.72亿元
  operatingProfitMargin: 5.6,
  netIncome: 374.40 / 100, // $520M * 7.2 / 100 = 37.44亿元
  netMargin: 4.6,

  // 效率篇
  operatingExpenseRatio: 35.3,
  marketingExpenseRatio: 9.7,
  inventoryTurnoverDays: 95, // Nike库存周转较好

  // 资产负债表
  totalAssets: 26686.08 / 100,
  totalLiabilities: 16577.28 / 100,
  equity: 10108.80 / 100,
  cash: 4795.20 / 100,
  inventory: 5390.64 / 100,
  receivables: 3865.68 / 100,

  // 偿债能力
  assetLiabilityRatio: 62.12,
  financialLeverage: 23.68,
};

// Canada Goose (FY2026 Q4 - 加拿大元，换算汇率 1 CAD = 5.2 CNY)
export const canadaGoose: CompanyData = {
  id: "canada_goose",
  name: "加拿大鹅",
  nameEn: "Canada Goose (GOOS)",
  code: "GOOS",
  period: "FY2026 Q4",
  fiscalNote: "Canada Goose财年截止于3月31日前后周日，FY2026覆盖2025年3月-2026年3月",
  currency: "CNY",
  currencyRate: 5.2,

  // 业绩篇
  revenue: 7946.64 / 100, // 1528.2M CAD * 5.2 / 100 = 79.47亿元
  revenueYoy: 13.3,
  sameStoreSalesGrowth: 6.8, // 同店销售增长
  salesPerStore: 85.5, // 奢侈品牌坪效高

  // 盈利篇
  grossMargin: 69.8,
  operatingProfit: 461.76 / 100, // 88.8M CAD * 5.2 / 100 = 4.62亿元
  operatingProfitMargin: 5.8,
  netIncome: 144.56 / 100, // 27.8M CAD * 5.2 / 100 = 1.45亿元
  netMargin: 1.82,

  // 效率篇
  operatingExpenseRatio: 63.95,
  marketingExpenseRatio: null,
  inventoryTurnoverDays: 180, // 奢侈品周转较慢

  // 资产负债表
  totalAssets: 9116.64 / 100,
  totalLiabilities: 5852.08 / 100,
  equity: 3264.56 / 100,
  cash: 2122.64 / 100,
  inventory: 2008.76 / 100,
  receivables: 563.68 / 100,

  // 偿债能力
  assetLiabilityRatio: 64.2,
  financialLeverage: 278.8,
};

// lululemon (FY2025 - 美元，换算汇率 1 USD = 7.2 CNY)
export const lululemon: CompanyData = {
  id: "lululemon",
  name: "Lululemon",
  nameEn: "lululemon (LULU)",
  code: "LULU",
  period: "FY2025",
  fiscalNote: "lululemon财年截止于1月31日前后周日，FY2025覆盖2025年2月-2026年2月",
  currency: "CNY",
  currencyRate: 7.2,

  // 业绩篇
  revenue: 79938.72 / 100, // $11,102.6M * 7.2 / 100 = 799.39亿元
  revenueYoy: 4.9,
  sameStoreSalesGrowth: 5.2, // 同店销售增长
  salesPerStore: 68.3, // Lululemon坪效较高

  // 盈利篇
  grossMargin: 56.6,
  operatingProfit: 15916.43 / 100, // $2,210.6M * 7.2 / 100 = 159.16亿元
  operatingProfitMargin: 19.9,
  netIncome: 11370.12 / 100, // $1,579.2M * 7.2 / 100 = 113.70亿元
  netMargin: 14.2,

  // 效率篇
  operatingExpenseRatio: 36.6,
  marketingExpenseRatio: null,
  inventoryTurnoverDays: 105, // Lululemon周转效率好

  // 资产负债表
  totalAssets: 60888.55 / 100,
  totalLiabilities: 25166.32 / 100,
  equity: 35725.25 / 100,
  cash: 13011.85 / 100,
  inventory: 12248.55 / 100,
  receivables: 1372.73 / 100,

  // 偿债能力
  assetLiabilityRatio: 41.3,
  financialLeverage: 70.4,
};

export const allCompanies: CompanyData[] = [tanzheCompany, adidas, nike, canadaGoose, lululemon];
