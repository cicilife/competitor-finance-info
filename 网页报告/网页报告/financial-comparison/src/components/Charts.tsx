// 类型定义
interface YearData {
  revenue: number | null;
  revenueYoy: number | null;
  grossMargin: number | null;
  netMargin: number | null;
  operatingProfitMargin: number | null;
  sameStoreSalesGrowth: number | null;
  operatingExpenseRatio: number | null;
  inventoryTurnoverDays: number | null;
  salesPerStore: number | null;
  operatingProfit: number | null;
}

interface CompanyData {
  id: string;
  name: string;
  nameCn: string;
  region: string;
  color: string;
  years: {
    [year: string]: YearData;
  };
}

// 颜色映射
const COLORS: Record<string, string> = {
  lululemon: "#9333EA",
  nike: "#EA580C",
  adidas: "#059669",
  canada_goose: "#6B7280",
  tanzhe: "#4F46E5",
  anta: "#DC2626",
  lining: "#2563EB",
  skechers: "#7C3AED",
  puma: "#0891B2",
  asics: "#059669",
  mizuno: "#84CC16",
  columbia: "#F97316",
  giant: "#14B8A6",
  topgolf: "#EC4899",
  vf_corp: "#6366F1",
  on_holding: "#8B5CF6",
  under_armour: "#0EA5E9",
  "361": "#10B981",
  amer_sports: "#F59E0B",
  berthi: "#84CC16",
  xtep: "#EF4444",
  biyorn: "#F472B6",
  mobigadi: "#22D3EE",
};

// 获取公司颜色
const getCompanyColor = (id: string): string => {
  return COLORS[id] || "#6B7280";
};

// 获取公司名称
const getCompanyName = (company: CompanyData): string => {
  return company.nameCn || company.name;
};

// ========== 业绩篇图表 ==========
export function PerformanceSection({ company1, company2, company3, year }: {
  company1: CompanyData;
  company2: CompanyData;
  company3: CompanyData;
  year: string;
}) {
  const companies = [
    { company: company1, name: getCompanyName(company1), id: company1.id, color: getCompanyColor(company1.id) },
    { company: company2, name: getCompanyName(company2), id: company2.id, color: getCompanyColor(company2.id) },
    { company: company3, name: getCompanyName(company3), id: company3.id, color: getCompanyColor(company3.id) },
  ];

  const getYearData = (company: CompanyData): YearData => company.years[year] || {} as YearData;

  // 计算收入最大值（用于柱状图）
  const revenues = companies.map(c => getYearData(c.company).revenue || 0);
  const maxRevenue = Math.max(...revenues, 1);

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
        <span className="w-3 h-3 rounded-full bg-blue-500"></span>
        业绩篇
      </h2>

      {/* 营业收入大卡片 */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        {companies.map((item, idx) => {
          const yearData = getYearData(item.company);
          return (
            <div key={idx} className="text-center p-4 rounded-lg" style={{ backgroundColor: `${item.color}10` }}>
              <p className="text-sm text-gray-600 mb-1">{item.name}</p>
              <p className="text-2xl font-bold" style={{ color: item.color }}>
                {yearData.revenue ? (yearData.revenue / 1000).toFixed(0) : "-"}
              </p>
              <p className="text-xs text-gray-500">亿元</p>
            </div>
          );
        })}
      </div>

      {/* 收入增速对比 */}
      <div className="mb-4">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">收入增速对比</h3>
        <div className="flex items-end justify-around h-40 gap-4">
          {companies.map((item, idx) => {
            const yearData = getYearData(item.company);
            const yoy = yearData.revenueYoy || 0;
            return (
              <div key={idx} className="flex flex-col items-center flex-1">
                <div className="relative w-full flex justify-center">
                  <div
                    className="w-16 rounded-t-md transition-all"
                    style={{
                      height: `${Math.max(Math.abs(yoy) / 50 * 120, 8)}px`,
                      backgroundColor: yoy >= 0 ? item.color : "#EF4444",
                    }}
                  />
                </div>
                <p className="text-lg font-bold mt-2" style={{ color: item.color }}>
                  {yoy !== null ? `${yoy >= 0 ? "+" : ""}${yoy.toFixed(1)}%` : "-"}
                </p>
                <p className="text-xs text-gray-500">{item.name}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* 同店销售增长 & 坪效 */}
      <div className="grid grid-cols-2 gap-4">
        {/* 同店销售增长 */}
        <div>
          <h3 className="text-sm font-semibold text-gray-700 mb-3">同店销售增长</h3>
          <div className="space-y-2">
            {companies.map((item, idx) => {
              const yearData = getYearData(item.company);
              const sss = yearData.sameStoreSalesGrowth;
              return (
                <div key={idx} className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 w-16">{item.name}</span>
                  <div className="flex-1 mx-2">
                    <div className="h-4 bg-gray-100 rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full"
                        style={{
                          width: `${Math.min(Math.abs(sss || 0) / 10 * 100, 100)}%`,
                          backgroundColor: sss !== null && sss >= 0 ? item.color : "#EF4444",
                        }}
                      />
                    </div>
                  </div>
                  <span className={`text-sm font-medium w-16 text-right ${sss !== null && sss >= 0 ? "text-green-600" : "text-red-600"}`}>
                    {sss !== null ? `${sss >= 0 ? "+" : ""}${sss.toFixed(1)}%` : "-"}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* 坪效/单店收入 */}
        <div>
          <h3 className="text-sm font-semibold text-gray-700 mb-3">坪效/单店收入 (千元)</h3>
          <div className="space-y-2">
            {companies.map((item, idx) => {
              const yearData = getYearData(item.company);
              return (
                <div key={idx} className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 w-16">{item.name}</span>
                  <div className="flex-1 mx-2">
                    <div className="h-4 bg-gray-100 rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full"
                        style={{
                          width: `${Math.min((yearData.salesPerStore || 0) / 2000 * 100, 100)}%`,
                          backgroundColor: item.color,
                        }}
                      />
                    </div>
                  </div>
                  <span className="text-sm font-medium w-20 text-right">
                    {yearData.salesPerStore !== null ? `${yearData.salesPerStore.toFixed(0)}` : "-"}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

// ========== 盈利篇图表 ==========
export function ProfitabilitySection({ company1, company2, company3, year }: {
  company1: CompanyData;
  company2: CompanyData;
  company3: CompanyData;
  year: string;
}) {
  const companies = [
    { company: company1, name: getCompanyName(company1), id: company1.id, color: getCompanyColor(company1.id) },
    { company: company2, name: getCompanyName(company2), id: company2.id, color: getCompanyColor(company2.id) },
    { company: company3, name: getCompanyName(company3), id: company3.id, color: getCompanyColor(company3.id) },
  ];

  const getYearData = (company: CompanyData): YearData => company.years[year] || {} as YearData;

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
        <span className="w-3 h-3 rounded-full bg-green-500"></span>
        盈利篇
      </h2>

      {/* 三大利润率对比 */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        {companies.map((item, idx) => {
          const yearData = getYearData(item.company);
          return (
            <div key={idx} className="text-center">
              <div className="flex justify-center gap-4 mb-4">
                {/* 毛利率 */}
                <div>
                  <div className="relative w-16 h-16">
                    <svg viewBox="0 0 100 100" className="w-full h-full transform -rotate-90">
                      <circle cx="50" cy="50" r="40" fill="none" stroke="#E5E7EB" strokeWidth="8" />
                      <circle
                        cx="50" cy="50" r="40" fill="none"
                        stroke={item.color}
                        strokeWidth="8"
                        strokeDasharray={`${Math.min(yearData.grossMargin || 0, 70) * 2.51} 251`}
                        strokeLinecap="round"
                      />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-sm font-bold">
                        {yearData.grossMargin !== null ? `${yearData.grossMargin.toFixed(0)}%` : "-"}
                      </span>
                    </div>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">毛利率</p>
                </div>
                {/* 营业利润率 */}
                <div>
                  <div className="relative w-16 h-16">
                    <svg viewBox="0 0 100 100" className="w-full h-full transform -rotate-90">
                      <circle cx="50" cy="50" r="40" fill="none" stroke="#E5E7EB" strokeWidth="8" />
                      <circle
                        cx="50" cy="50" r="40" fill="none"
                        stroke={item.color}
                        strokeWidth="8"
                        strokeDasharray={`${Math.min(yearData.operatingProfitMargin || 0, 30) * 2.51} 251`}
                        strokeLinecap="round"
                      />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-sm font-bold">
                        {yearData.operatingProfitMargin !== null ? `${yearData.operatingProfitMargin.toFixed(1)}%` : "-"}
                      </span>
                    </div>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">营业利润率</p>
                </div>
                {/* 净利润率 */}
                <div>
                  <div className="relative w-16 h-16">
                    <svg viewBox="0 0 100 100" className="w-full h-full transform -rotate-90">
                      <circle cx="50" cy="50" r="40" fill="none" stroke="#E5E7EB" strokeWidth="8" />
                      <circle
                        cx="50" cy="50" r="40" fill="none"
                        stroke={item.color}
                        strokeWidth="8"
                        strokeDasharray={`${Math.min(yearData.netMargin || 0, 20) * 2.51} 251`}
                        strokeLinecap="round"
                      />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-sm font-bold">
                        {yearData.netMargin !== null ? `${yearData.netMargin.toFixed(1)}%` : "-"}
                      </span>
                    </div>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">净利率</p>
                </div>
              </div>
              <p className="text-sm font-medium" style={{ color: item.color }}>{item.name}</p>
            </div>
          );
        })}
      </div>

      {/* 利润对比柱状图 */}
      <div>
        <h3 className="text-sm font-semibold text-gray-700 mb-3">利润对比 (亿元)</h3>
        <div className="flex items-end justify-around h-48 gap-4">
          {/* 营业利润 */}
          <div className="flex flex-col items-center flex-1">
            <div className="flex gap-2 items-end h-36">
              {companies.map((item, idx) => {
                const yearData = getYearData(item.company);
                const opProfit = (yearData.operatingProfit || 0) / 1000; // 千元转亿
                const maxOpProfit = Math.max(...companies.map(c => (getYearData(c.company).operatingProfit || 0) / 1000), 1);
                return (
                  <div
                    key={idx}
                    className="w-12 rounded-t-md transition-all"
                    style={{
                      height: `${Math.max((opProfit / maxOpProfit) * 140, 8)}px`,
                      backgroundColor: item.color,
                    }}
                  />
                );
              })}
            </div>
            <p className="text-xs text-gray-500 mt-2">营业利润</p>
          </div>
        </div>
        {/* 图例 */}
        <div className="flex justify-center gap-6 mt-4 text-xs">
          {companies.map((item, idx) => (
            <span key={idx} className="flex items-center gap-1">
              <span className="w-3 h-3 rounded" style={{ backgroundColor: item.color }}></span>
              {item.name}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

// ========== 效率篇图表 ==========
export function EfficiencySection({ company1, company2, company3, year }: {
  company1: CompanyData;
  company2: CompanyData;
  company3: CompanyData;
  year: string;
}) {
  const companies = [
    { company: company1, name: getCompanyName(company1), id: company1.id, color: getCompanyColor(company1.id) },
    { company: company2, name: getCompanyName(company2), id: company2.id, color: getCompanyColor(company2.id) },
    { company: company3, name: getCompanyName(company3), id: company3.id, color: getCompanyColor(company3.id) },
  ];

  const getYearData = (company: CompanyData): YearData => company.years[year] || {} as YearData;

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
        <span className="w-3 h-3 rounded-full bg-orange-500"></span>
        效率篇
      </h2>

      {/* 运营费用率对比 */}
      <div className="mb-6">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">运营费用率 (越低越好)</h3>
        <div className="flex items-end justify-around h-48 gap-4">
          {companies.map((item, idx) => {
            const yearData = getYearData(item.company);
            const opex = yearData.operatingExpenseRatio || 0;
            return (
              <div key={idx} className="flex flex-col items-center flex-1">
                <p className="text-2xl font-bold mb-2" style={{ color: item.color }}>
                  {opex !== null ? `${opex.toFixed(1)}%` : "-"}
                </p>
                <div
                  className="w-20 rounded-t-md transition-all"
                  style={{
                    height: `${Math.max((opex / 70) * 140, 8)}px`,
                    backgroundColor: item.color,
                  }}
                />
                <p className="text-sm text-gray-600 mt-2">{item.name}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* 库存周转天数 */}
      <div>
        <h3 className="text-sm font-semibold text-gray-700 mb-3">库存周转天数 (越低越好)</h3>
        <div className="space-y-3">
          {companies.map((item, idx) => {
            const yearData = getYearData(item.company);
            const invDays = yearData.inventoryTurnoverDays;
            return (
              <div key={idx} className="flex items-center justify-between">
                <span className="text-sm text-gray-600 w-16">{item.name}</span>
                <div className="flex-1 mx-2">
                  <div className="h-6 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full"
                      style={{
                        width: `${Math.min((invDays || 0) / 250 * 100, 100)}%`,
                        backgroundColor: item.color,
                      }}
                    />
                  </div>
                </div>
                <span className="text-sm font-medium w-16 text-right">
                  {invDays !== null ? `${invDays}天` : "-"}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

// ========== 综合评分雷达图 ==========
export function ComprehensiveView({ company1, company2, company3, year }: {
  company1: CompanyData;
  company2: CompanyData;
  company3: CompanyData;
  year: string;
}) {
  const companies = [
    { company: company1, name: getCompanyName(company1), color: getCompanyColor(company1.id) },
    { company: company2, name: getCompanyName(company2), color: getCompanyColor(company2.id) },
    { company: company3, name: getCompanyName(company3), color: getCompanyColor(company3.id) },
  ];

  const getYearData = (company: CompanyData): YearData => company.years[year] || {} as YearData;

  // 雷达图尺寸
  const size = 320;
  const centerX = size / 2;
  const centerY = size / 2;
  const maxRadius = 130;

  // 定义指标类型
  interface MetricDef {
    name: string;
    max: number;
    key: keyof YearData;
    inverse?: boolean;
  }

  // 同类指标邻近排列，同色系显示
  const metricGroups: Array<{ name: string; color: string; metrics: MetricDef[] }> = [
    {
      name: "盈利类",
      color: "#22C55E",
      metrics: [
        { name: "毛利率", max: 70, key: "grossMargin" },
        { name: "净利率", max: 20, key: "netMargin" },
        { name: "营业利润率", max: 30, key: "operatingProfitMargin" },
      ]
    },
    {
      name: "增长类",
      color: "#3B82F6",
      metrics: [
        { name: "收入增速", max: 50, key: "revenueYoy" },
        { name: "同店增长", max: 10, key: "sameStoreSalesGrowth" },
      ]
    },
    {
      name: "效率类",
      color: "#F97316",
      metrics: [
        { name: "库存周转", max: 200, key: "inventoryTurnoverDays", inverse: true },
        { name: "运营费用率", max: 70, key: "operatingExpenseRatio", inverse: true },
      ]
    },
  ];

  const allMetrics: MetricDef[] = metricGroups.flatMap(g => g.metrics);
  const numMetrics = allMetrics.length;
  const getAngle = (index: number) => (Math.PI * 2 * index) / numMetrics - Math.PI / 2;

  // 获取指标归一化值
  const getNormalizedValue = (company: CompanyData, metric: MetricDef) => {
    const yearData = getYearData(company);
    let value = yearData[metric.key] as number;
    if (value === null || value === undefined) value = 0;
    if (metric.inverse) {
      return Math.max(0, metric.max - value) / metric.max;
    } else {
      return Math.min(value, metric.max) / metric.max;
    }
  };

  // 绘制雷达图网格和轴
  const gridLevels = [0.25, 0.5, 0.75, 1];
  const gridLines = gridLevels.map(level => {
    const points = allMetrics.map((_, i) => {
      const angle = getAngle(i);
      const r = maxRadius * level;
      return `${centerX + r * Math.cos(angle)},${centerY + r * Math.sin(angle)}`;
    }).join(' ');
    return points;
  });

  const axisLines = allMetrics.map((_, i) => {
    const angle = getAngle(i);
    const x2 = centerX + maxRadius * Math.cos(angle);
    const y2 = centerY + maxRadius * Math.sin(angle);
    return { x1: centerX, y1: centerY, x2, y2 };
  });

  // 计算每个公司的数据点
  const companyPolygons = companies.map(c => {
    const points = allMetrics.map((m, i) => {
      const value = getNormalizedValue(c.company, m);
      const angle = getAngle(i);
      const r = maxRadius * value;
      return `${centerX + r * Math.cos(angle)},${centerY + r * Math.sin(angle)}`;
    }).join(' ');
    return { name: c.name, color: c.color, points };
  });

  // 计算综合得分
  const calculateScore = (company: CompanyData) => {
    let total = 0;
    allMetrics.forEach(m => {
      total += getNormalizedValue(company, m);
    });
    return Math.round((total / numMetrics) * 100);
  };

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
        <span className="w-3 h-3 rounded-full bg-purple-500"></span>
        综合评分对比
      </h2>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* 雷达图 */}
        <div className="flex-shrink-0">
          <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="mx-auto">
            <circle cx={centerX} cy={centerY} r={maxRadius} fill="none" stroke="#E5E7EB" strokeWidth="1" />
            {gridLines.map((points, i) => (
              <polygon key={i} points={points} fill="none" stroke="#E5E7EB" strokeWidth="1" />
            ))}
            {axisLines.map((line, i) => (
              <line key={i} x1={line.x1} y1={line.y1} x2={line.x2} y2={line.y2} stroke="#D1D5DB" strokeWidth="1" />
            ))}
            {companyPolygons.map((poly, i) => (
              <polygon
                key={i}
                points={poly.points}
                fill={poly.color}
                fillOpacity={0.15}
                stroke={poly.color}
                strokeWidth="2"
              />
            ))}
            {companies.map((c, ci) => (
              allMetrics.map((m, mi) => {
                const value = getNormalizedValue(c.company, m);
                const angle = getAngle(mi);
                const r = maxRadius * value;
                const cx = centerX + r * Math.cos(angle);
                const cy = centerY + r * Math.sin(angle);
                return (
                  <circle key={`${ci}-${mi}`} cx={cx} cy={cy} r={4} fill={c.color} stroke="white" strokeWidth={2} />
                );
              })
            ))}
            {allMetrics.map((m, i) => {
              const angle = getAngle(i);
              const labelR = maxRadius + 25;
              const x = centerX + labelR * Math.cos(angle);
              const y = centerY + labelR * Math.sin(angle);
              const textAnchor: "start" | "middle" | "end" = Math.cos(angle) < -0.1 ? "end" : Math.cos(angle) > 0.1 ? "start" : "middle";
              const dy = "0.35em";
              return (
                <text key={i} x={x} y={y} textAnchor={textAnchor} dy={dy} fontSize={11} fill="#6B7280" fontWeight={500}>
                  {m.name}
                </text>
              );
            })}
          </svg>
          <div className="flex justify-center gap-6 mt-4 text-xs">
            {companies.map((item, idx) => (
              <span key={idx} className="flex items-center gap-1">
                <span className="w-3 h-3 rounded" style={{ backgroundColor: item.color }}></span>
                {item.name}
              </span>
            ))}
          </div>
        </div>

        {/* 右侧：指标分组展示 */}
        <div className="flex-1 space-y-4">
          {metricGroups.map((group) => (
            <div key={group.name} className="border rounded-lg p-4">
              <h3 className="text-sm font-semibold mb-3 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: group.color }}></span>
                <span style={{ color: group.color }}>{group.name}</span>
              </h3>
              <div className="space-y-2">
                {group.metrics.map((metric, mi) => (
                  <div key={mi} className="flex items-center gap-2">
                    <span className="w-20 text-xs text-gray-500">{metric.name}</span>
                    <div className="flex-1 flex gap-1">
                      {companies.map((c, ci) => {
                        const value = getNormalizedValue(c.company, metric);
                        const yearData = getYearData(c.company);
                        return (
                          <div
                            key={ci}
                            className="h-5 rounded flex items-center justify-center px-1"
                            style={{
                              width: `${Math.max(value * 100, 10)}%`,
                              backgroundColor: c.color,
                              minWidth: "24px"
                            }}
                          >
                            <span className="text-xs text-white font-medium truncate">
                              {metric.inverse
                                ? `${(yearData[metric.key] as number || 0).toFixed(0)}天`
                                : `${(yearData[metric.key] as number || 0).toFixed(1)}%`
                              }
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}

          {/* 综合得分排名 */}
          <div className="border rounded-lg p-4 bg-gray-50">
            <h3 className="text-sm font-semibold mb-3">综合得分排名</h3>
            <div className="space-y-2">
              {[...companies].sort((a, b) => calculateScore(b.company) - calculateScore(a.company)).map((c, idx) => (
                <div key={idx} className="flex items-center gap-3">
                  <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white ${
                    idx === 0 ? 'bg-yellow-500' : idx === 1 ? 'bg-gray-400' : 'bg-orange-400'
                  }`}>
                    {idx + 1}
                  </span>
                  <span className="w-20 text-sm font-medium" style={{ color: c.color }}>{c.name}</span>
                  <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div className="h-full rounded-full" style={{ width: `${calculateScore(c.company)}%`, backgroundColor: c.color }} />
                  </div>
                  <span className="text-sm font-bold w-10 text-right">{calculateScore(c.company)}分</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ========== 三年趋势图表 ==========
export function TrendSection({ company1, company2, company3 }: {
  company1: CompanyData;
  company2: CompanyData;
  company3: CompanyData;
}) {
  const companies = [
    { company: company1, name: getCompanyName(company1), color: getCompanyColor(company1.id) },
    { company: company2, name: getCompanyName(company2), color: getCompanyColor(company2.id) },
    { company: company3, name: getCompanyName(company3), color: getCompanyColor(company3.id) },
  ];

  const years = ["2023", "2024", "2025"];

  // 计算收入趋势
  const getRevenueData = (company: CompanyData) => years.map(y => (company.years[y]?.revenue || 0) / 1000);

  // 计算毛利率趋势
  const getGrossMarginData = (company: CompanyData) => years.map(y => company.years[y]?.grossMargin || null);

  // 计算净利率趋势
  const getNetMarginData = (company: CompanyData) => years.map(y => company.years[y]?.netMargin || null);

  return (
    <div className="space-y-6">
      {/* 收入趋势 */}
      <div>
        <h3 className="text-sm font-semibold text-gray-700 mb-3">营业收入趋势 (亿元)</h3>
        <div className="flex items-end justify-around h-48 gap-4">
          {years.map((year, yi) => (
            <div key={year} className="flex gap-2 items-end h-40">
              {companies.map((c, ci) => {
                const revenues = getRevenueData(c.company);
                const maxRev = Math.max(...companies.flatMap(co => getRevenueData(co.company)), 1);
                return (
                  <div
                    key={ci}
                    className="w-10 rounded-t-md transition-all"
                    style={{
                      height: `${Math.max((revenues[yi] / maxRev) * 160, 4)}px`,
                      backgroundColor: c.color,
                    }}
                  />
                );
              })}
            </div>
          ))}
        </div>
        <div className="flex justify-around mt-2">
          {years.map(year => (
            <span key={year} className="text-xs text-gray-500 w-24 text-center">{year}</span>
          ))}
        </div>
        <div className="flex justify-center gap-6 mt-4 text-xs">
          {companies.map((c, idx) => (
            <span key={idx} className="flex items-center gap-1">
              <span className="w-3 h-3 rounded" style={{ backgroundColor: c.color }}></span>
              {c.name}
            </span>
          ))}
        </div>
      </div>

      {/* 毛利率趋势 */}
      <div>
        <h3 className="text-sm font-semibold text-gray-700 mb-3">毛利率趋势 (%)</h3>
        <div className="flex items-end justify-around h-40 gap-4">
          {years.map((year, yi) => (
            <div key={year} className="flex gap-2 items-end h-32">
              {companies.map((c, ci) => {
                const margins = getGrossMarginData(c.company);
                const maxMargin = 80;
                return (
                  <div
                    key={ci}
                    className="w-10 rounded-t-md transition-all"
                    style={{
                      height: `${Math.max(((margins[yi] || 0) / maxMargin) * 128, 4)}px`,
                      backgroundColor: c.color,
                    }}
                  />
                );
              })}
            </div>
          ))}
        </div>
        <div className="flex justify-around mt-2">
          {years.map(year => (
            <span key={year} className="text-xs text-gray-500 w-24 text-center">{year}</span>
          ))}
        </div>
      </div>

      {/* 净利率趋势 */}
      <div>
        <h3 className="text-sm font-semibold text-gray-700 mb-3">净利率趋势 (%)</h3>
        <div className="flex items-end justify-around h-40 gap-4">
          {years.map((year, yi) => (
            <div key={year} className="flex gap-2 items-end h-32">
              {companies.map((c, ci) => {
                const margins = getNetMarginData(c.company);
                const maxMargin = 30;
                return (
                  <div
                    key={ci}
                    className="w-10 rounded-t-md transition-all"
                    style={{
                      height: `${Math.max(((margins[yi] || 0) / maxMargin) * 128, 4)}px`,
                      backgroundColor: c.color,
                    }}
                  />
                );
              })}
            </div>
          ))}
        </div>
        <div className="flex justify-around mt-2">
          {years.map(year => (
            <span key={year} className="text-xs text-gray-500 w-24 text-center">{year}</span>
          ))}
        </div>
      </div>
    </div>
  );
}