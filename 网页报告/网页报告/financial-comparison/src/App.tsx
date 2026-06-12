import { useState, useMemo } from "react";
import {
  PerformanceSection,
  ProfitabilitySection,
  EfficiencySection,
  ComprehensiveView,
  TrendSection,
} from "./components/Charts";
import { DataMarker, InlineCommentMarker } from "./components/DataMarker";
import { dataComments } from "./data/comments";
import excelData from "./data/excelData.json";
import "./App.css";

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

// 公司颜色映射
const companyColors: Record<string, { bg: string; text: string; border: string; hex: string }> = {
  lululemon: { bg: "from-purple-500 to-purple-600", text: "text-purple-200", border: "border-purple-400", hex: "#9333EA" },
  nike: { bg: "from-orange-500 to-orange-600", text: "text-orange-200", border: "border-orange-400", hex: "#EA580C" },
  adidas: { bg: "from-emerald-500 to-emerald-600", text: "text-emerald-200", border: "border-emerald-400", hex: "#059669" },
  canada_goose: { bg: "from-gray-600 to-gray-700", text: "text-gray-200", border: "border-gray-400", hex: "#6B7280" },
  tanzhe: { bg: "from-indigo-500 to-indigo-600", text: "text-indigo-200", border: "border-indigo-400", hex: "#4F46E5" },
  anta: { bg: "from-red-500 to-red-600", text: "text-red-200", border: "border-red-400", hex: "#DC2626" },
  lining: { bg: "from-blue-500 to-blue-600", text: "text-blue-200", border: "border-blue-400", hex: "#2563EB" },
  skechers: { bg: "from-violet-500 to-violet-600", text: "text-violet-200", border: "border-violet-400", hex: "#7C3AED" },
  puma: { bg: "from-cyan-500 to-cyan-600", text: "text-cyan-200", border: "border-cyan-400", hex: "#0891B2" },
  asics: { bg: "from-teal-500 to-teal-600", text: "text-teal-200", border: "border-teal-400", hex: "#059669" },
  mizuno: { bg: "from-lime-500 to-lime-600", text: "text-lime-200", border: "border-lime-400", hex: "#84CC16" },
  columbia: { bg: "from-amber-500 to-amber-600", text: "text-amber-200", border: "border-amber-400", hex: "#F97316" },
  361: { bg: "from-green-500 to-green-600", text: "text-green-200", border: "border-green-400", hex: "#10B981" },
  xtep: { bg: "from-red-600 to-red-700", text: "text-red-200", border: "border-red-400", hex: "#EF4444" },
};

// 获取默认颜色
const getDefaultColor = (id: string) => {
  const colors = companyColors[id];
  if (colors) return colors;
  // 生成随机颜色
  const hue = (id.charCodeAt(0) * 137) % 360;
  return {
    bg: `from-hsl-[${hue}]-500 to-hsl-[${hue}]-600`,
    text: `text-hsl-[${hue}]-200`,
    border: `border-hsl-[${hue}]-400`,
    hex: `hsl(${hue}, 70%, 50%)`,
  };
};

// 检查是否有注释
const hasComment = (companyId: string, metric: string): boolean => {
  return dataComments.some(c =>
    (c.companyId === companyId || companyId === 'all') &&
    (c.metric === metric || c.metric === 'all')
  );
};

// 获取注释数量
const getCommentCount = (companyId: string, metric: string): number => {
  return dataComments.filter(c =>
    (c.companyId === companyId || companyId === 'all') &&
    (c.metric === metric || c.metric === 'all')
  ).length;
};

function CompanyCard({ company, year }: { company: CompanyData; year: string }) {
  const colors = companyColors[company.id] || getDefaultColor(company.id);
  const yearData = company.years[year];

  return (
    <div className={`bg-gradient-to-br ${colors.bg} rounded-xl shadow-lg p-6 text-white`}>
      <div className="flex justify-between items-start">
        <div>
          <h2 className="text-2xl font-bold">{company.nameCn || company.name}</h2>
          <p className={colors.text}>区域: {company.region}</p>
          <p className={`${colors.text} mt-1`}>{year}年度</p>
        </div>
        <div className="text-right">
          <p className={`text-sm ${colors.text}`}>营业收入</p>
          <DataMarker companyId={company.id} metric="revenue" year={year}>
            <p className="text-3xl font-bold cursor-help">
              {yearData.revenue ? `${(yearData.revenue / 1000).toFixed(0)}亿` : "-"}
            </p>
          </DataMarker>
          {yearData.revenueYoy !== null && (
            <DataMarker companyId={company.id} metric="revenueYoy" year={year}>
              <p className={`text-sm ${yearData.revenueYoy >= 0 ? "text-green-300" : "text-red-300"} cursor-help`}>
                {yearData.revenueYoy >= 0 ? "↑" : "↓"} {yearData.revenueYoy.toFixed(1)}%
              </p>
            </DataMarker>
          )}
        </div>
      </div>
      <div className="grid grid-cols-3 gap-4 mt-6">
        <div>
          <p className={`text-sm ${colors.text}`}>毛利率</p>
          <DataMarker companyId={company.id} metric="grossMargin" year={year}>
            <p className="text-xl font-semibold cursor-help">
              {yearData.grossMargin !== null ? `${yearData.grossMargin.toFixed(1)}%` : "-"}
            </p>
          </DataMarker>
        </div>
        <div>
          <p className={`text-sm ${colors.text}`}>净利率</p>
          <DataMarker companyId={company.id} metric="netMargin" year={year}>
            <p className="text-xl font-semibold cursor-help">
              {yearData.netMargin !== null ? `${yearData.netMargin.toFixed(1)}%` : "-"}
            </p>
          </DataMarker>
        </div>
        <div>
          <p className={`text-sm ${colors.text}`}>营业费用率</p>
          <DataMarker companyId={company.id} metric="operatingExpenseRatio" year={year}>
            <p className="text-xl font-semibold cursor-help">
              {yearData.operatingExpenseRatio !== null ? `${yearData.operatingExpenseRatio.toFixed(1)}%` : "-"}
            </p>
          </DataMarker>
        </div>
      </div>
    </div>
  );
}

function App() {
  const [selectedCompanies, setSelectedCompanies] = useState<string[]>(["lululemon", "nike", "adidas"]);
  const [selectedYear, setSelectedYear] = useState<string>("2025");
  const [viewMode, setViewMode] = useState<"single" | "trend">("single");
  const [showComments, setShowComments] = useState(true);

  const allCompanies = excelData as CompanyData[];

  const getCompany = (id: string): CompanyData | undefined => {
    return allCompanies.find((c) => c.id === id);
  };

  const selected1 = getCompany(selectedCompanies[0]);
  const selected2 = getCompany(selectedCompanies[1]);
  const selected3 = getCompany(selectedCompanies[2]);

  const toggleCompany = (id: string) => {
    if (selectedCompanies.includes(id)) {
      setSelectedCompanies(selectedCompanies.filter((c) => c !== id));
    } else if (selectedCompanies.length < 3) {
      setSelectedCompanies([...selectedCompanies, id]);
    } else {
      setSelectedCompanies([selectedCompanies[1], selectedCompanies[2], id]);
    }
  };

  // 可用年份
  const availableYears = ["2023", "2024", "2025"];

  // 总注释数量
  const totalComments = dataComments.length;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">运动品牌财务对比分析</h1>
              <p className="text-gray-500 mt-1">
                数据来源: 竞品财务数据库（2023-2025年度）
              </p>
            </div>
            {/* 注释说明 */}
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-sm text-amber-600 bg-amber-50 px-3 py-2 rounded-lg">
                <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="16" x2="12" y2="12" />
                  <line x1="12" y1="8" x2="12.01" y2="8" />
                </svg>
                <span>标记数据含 {totalComments} 条注释</span>
              </div>
              <button
                onClick={() => setShowComments(!showComments)}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  showComments
                    ? "bg-amber-500 text-white"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                {showComments ? "隐藏注释标记" : "显示注释标记"}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Controls */}
      <div className="max-w-7xl mx-auto px-4 py-4 space-y-4">
        {/* Year Selector */}
        <div className="bg-white rounded-xl shadow-sm p-4">
          <div className="flex flex-wrap items-center gap-4">
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">选择年份</h3>
              <div className="flex gap-2">
                {availableYears.map((year) => (
                  <button
                    key={year}
                    onClick={() => setSelectedYear(year)}
                    className={`px-4 py-2 rounded-lg font-medium transition-all ${
                      selectedYear === year
                        ? "bg-blue-600 text-white shadow-md"
                        : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                    }`}
                  >
                    {year}
                  </button>
                ))}
              </div>
            </div>

            <div className="border-l-2 border-gray-200 pl-4">
              <h3 className="text-sm font-semibold text-gray-700 mb-2">视图模式</h3>
              <div className="flex gap-2">
                <button
                  onClick={() => setViewMode("single")}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    viewMode === "single"
                      ? "bg-blue-600 text-white shadow-md"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  单年对比
                </button>
                <button
                  onClick={() => setViewMode("trend")}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    viewMode === "trend"
                      ? "bg-blue-600 text-white shadow-md"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  三年趋势
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Brand Selector */}
        <div className="bg-white rounded-xl shadow-sm p-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">选择对比品牌（选3个）</h3>
          <div className="flex flex-wrap gap-3">
            {allCompanies.map((company) => {
              const isSelected = selectedCompanies.includes(company.id);
              const colors = companyColors[company.id] || getDefaultColor(company.id);
              const commentCount = getCommentCount(company.id, 'all');
              return (
                <button
                  key={company.id}
                  onClick={() => toggleCompany(company.id)}
                  className={`px-4 py-2 rounded-lg border-2 transition-all relative ${
                    isSelected
                      ? `${colors.border} bg-gradient-to-r ${colors.bg} text-white`
                      : "border-gray-200 bg-gray-50 text-gray-700 hover:border-gray-300"
                  }`}
                >
                  <span className="font-medium">{company.nameCn || company.name}</span>
                  {commentCount > 0 && showComments && (
                    <span className="absolute -top-1 -right-1 bg-amber-400 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                      {commentCount}
                    </span>
                  )}
                </button>
              );
            })}
          </div>
          {selectedCompanies.length < 3 && (
            <p className="text-sm text-amber-600 mt-2">请选择至少3个品牌进行对比</p>
          )}
        </div>
      </div>

      {/* Content */}
      {selected1 && selected2 && selected3 && (
        <div className="max-w-7xl mx-auto px-4 py-6">
          {viewMode === "single" ? (
            <>
              {/* Company Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <CompanyCard company={selected1} year={selectedYear} />
                <CompanyCard company={selected2} year={selectedYear} />
                <CompanyCard company={selected3} year={selectedYear} />
              </div>

              {/* Charts */}
              <div className="mt-6">
                <PerformanceSection company1={selected1} company2={selected2} company3={selected3} year={selectedYear} />
              </div>

              <div className="mt-6">
                <ProfitabilitySection company1={selected1} company2={selected2} company3={selected3} year={selectedYear} />
              </div>

              <div className="mt-6">
                <EfficiencySection company1={selected1} company2={selected2} company3={selected3} year={selectedYear} />
              </div>

              <div className="mt-6">
                <ComprehensiveView company1={selected1} company2={selected2} company3={selected3} year={selectedYear} />
              </div>
            </>
          ) : (
            /* Trend View */
            <>
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-blue-500"></span>
                  {selected1.nameCn || selected1.name} vs {selected2.nameCn || selected2.name} vs {selected3.nameCn || selected3.name} - 三年趋势
                  {showComments && (
                    <span className="ml-2 text-sm font-normal text-amber-600 bg-amber-50 px-2 py-1 rounded">
                      点击数据点查看行业注释
                    </span>
                  )}
                </h2>
                <TrendSection company1={selected1} company2={selected2} company3={selected3} />
              </div>
            </>
          )}

          {/* Data Source Note */}
          <div className="bg-white rounded-xl shadow-sm p-6 mt-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-amber-500"></span>
              数据说明与注释
              {showComments && (
                <span className="ml-2 text-xs bg-amber-100 text-amber-700 px-2 py-1 rounded-full">
                  {totalComments} 条注释可用
                </span>
              )}
            </h2>
            <ul className="list-disc list-inside text-gray-600 space-y-2">
              <li>数据来源: 竞品财务数据库_标准模板.xlsx（更新日期: 2026-05-28）</li>
              <li>金额单位: 人民币千元（已换算为亿元展示）</li>
              <li>汇率: USD/CNY=7.2, EUR/CNY=8.17（期末汇率）</li>
              <li className="text-blue-600">
                营业收入、毛利率、净利率、库存周转天数等指标来自各公司年报/季报披露
              </li>
              <li className="text-amber-600">
                带 <span className="inline-flex items-center justify-center w-4 h-4 bg-amber-400 rounded-full text-white text-xs font-bold">i</span> 标记的数据点包含行业研究报告、公司公告等来源的详细注释，点击可查看
              </li>
            </ul>

            {/* 注释来源分类 */}
            {showComments && (
              <div className="mt-4 pt-4 border-t">
                <h3 className="text-sm font-semibold text-gray-700 mb-3">注释来源分类</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  <div className="bg-purple-50 rounded-lg p-3">
                    <p className="text-xs text-purple-600 font-medium">高端品牌</p>
                    <p className="text-sm text-purple-800">
                      {dataComments.filter(c => ['anta', 'lululemon', 'amer_sports'].includes(c.companyId)).length} 条
                    </p>
                  </div>
                  <div className="bg-blue-50 rounded-lg p-3">
                    <p className="text-xs text-blue-600 font-medium">国际品牌</p>
                    <p className="text-sm text-blue-800">
                      {dataComments.filter(c => ['nike', 'adidas'].includes(c.companyId)).length} 条
                    </p>
                  </div>
                  <div className="bg-green-50 rounded-lg p-3">
                    <p className="text-xs text-green-600 font-medium">国产品牌</p>
                    <p className="text-sm text-green-800">
                      {dataComments.filter(c => ['lining', 'xtep', '361'].includes(c.companyId)).length} 条
                    </p>
                  </div>
                  <div className="bg-orange-50 rounded-lg p-3">
                    <p className="text-xs text-orange-600 font-medium">行业趋势</p>
                    <p className="text-sm text-orange-800">
                      {dataComments.filter(c => c.companyId === 'industry').length} 条
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Detailed Table */}
          <div className="bg-white rounded-xl shadow-sm p-6 mt-6 overflow-x-auto">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              详细数据对比表 ({selectedYear}年度)
              {showComments && (
                <span className="ml-2 text-xs text-gray-500">鼠标悬停带标记的数据查看注释</span>
              )}
            </h2>
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50">
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">指标</th>
                  <th className="text-right py-3 px-4 font-semibold relative">
                    {selected1.nameCn || selected1.name}
                    {showComments && getCommentCount(selected1.id, 'all') > 0 && (
                      <span className="absolute top-1 right-1 w-2 h-2 bg-amber-400 rounded-full" title={`${getCommentCount(selected1.id, 'all')} 条注释`} />
                    )}
                  </th>
                  <th className="text-right py-3 px-4 font-semibold relative">
                    {selected2.nameCn || selected2.name}
                    {showComments && getCommentCount(selected2.id, 'all') > 0 && (
                      <span className="absolute top-1 right-1 w-2 h-2 bg-amber-400 rounded-full" title={`${getCommentCount(selected2.id, 'all')} 条注释`} />
                    )}
                  </th>
                  <th className="text-right py-3 px-4 font-semibold relative">
                    {selected3.nameCn || selected3.name}
                    {showComments && getCommentCount(selected3.id, 'all') > 0 && (
                      <span className="absolute top-1 right-1 w-2 h-2 bg-amber-400 rounded-full" title={`${getCommentCount(selected3.id, 'all')} 条注释`} />
                    )}
                  </th>
                </tr>
              </thead>
              <tbody>
                {/* 业绩篇 */}
                <tr className="bg-blue-50">
                  <td colSpan={4} className="py-2 px-4 font-semibold text-blue-700">业绩篇</td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-2 px-4 text-gray-700 flex items-center gap-1">
                    营业收入 (亿元)
                    {showComments && (
                      <DataMarker companyId="industry" metric="revenue">
                        <span className="text-amber-500 cursor-help">*</span>
                      </DataMarker>
                    )}
                  </td>
                  <td className="text-right py-2 px-4">
                    <InlineCommentMarker companyId={selected1.id} metric="revenue" value={selected1.years[selectedYear]?.revenue ? (selected1.years[selectedYear].revenue! / 1000).toFixed(2) : "-"} year={selectedYear} />
                  </td>
                  <td className="text-right py-2 px-4">
                    <InlineCommentMarker companyId={selected2.id} metric="revenue" value={selected2.years[selectedYear]?.revenue ? (selected2.years[selectedYear].revenue! / 1000).toFixed(2) : "-"} year={selectedYear} />
                  </td>
                  <td className="text-right py-2 px-4">
                    <InlineCommentMarker companyId={selected3.id} metric="revenue" value={selected3.years[selectedYear]?.revenue ? (selected3.years[selectedYear].revenue! / 1000).toFixed(2) : "-"} year={selectedYear} />
                  </td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-2 px-4 text-gray-700 flex items-center gap-1">
                    收入增速 (%)
                    {showComments && (
                      <DataMarker companyId="industry" metric="revenueYoy">
                        <span className="text-amber-500 cursor-help">*</span>
                      </DataMarker>
                    )}
                  </td>
                  <td className="text-right py-2 px-4">
                    <InlineCommentMarker companyId={selected1.id} metric="revenueYoy" value={selected1.years[selectedYear]?.revenueYoy !== null ? `${(selected1.years[selectedYear].revenueYoy! >= 0 ? "+" : "")}${selected1.years[selectedYear].revenueYoy!.toFixed(1)}` : "-"} year={selectedYear} />
                  </td>
                  <td className="text-right py-2 px-4">
                    <InlineCommentMarker companyId={selected2.id} metric="revenueYoy" value={selected2.years[selectedYear]?.revenueYoy !== null ? `${(selected2.years[selectedYear].revenueYoy! >= 0 ? "+" : "")}${selected2.years[selectedYear].revenueYoy!.toFixed(1)}` : "-"} year={selectedYear} />
                  </td>
                  <td className="text-right py-2 px-4">
                    <InlineCommentMarker companyId={selected3.id} metric="revenueYoy" value={selected3.years[selectedYear]?.revenueYoy !== null ? `${(selected3.years[selectedYear].revenueYoy! >= 0 ? "+" : "")}${selected3.years[selectedYear].revenueYoy!.toFixed(1)}` : "-"} year={selectedYear} />
                  </td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-2 px-4 text-gray-700">同店销售增长 (%)</td>
                  <td className="text-right py-2 px-4">{selected1.years[selectedYear]?.sameStoreSalesGrowth !== null ? `${(selected1.years[selectedYear].sameStoreSalesGrowth! >= 0 ? "+" : "")}${selected1.years[selectedYear].sameStoreSalesGrowth!.toFixed(1)}` : "-"}</td>
                  <td className="text-right py-2 px-4">{selected2.years[selectedYear]?.sameStoreSalesGrowth !== null ? `${(selected2.years[selectedYear].sameStoreSalesGrowth! >= 0 ? "+" : "")}${selected2.years[selectedYear].sameStoreSalesGrowth!.toFixed(1)}` : "-"}</td>
                  <td className="text-right py-2 px-4">{selected3.years[selectedYear]?.sameStoreSalesGrowth !== null ? `${(selected3.years[selectedYear].sameStoreSalesGrowth! >= 0 ? "+" : "")}${selected3.years[selectedYear].sameStoreSalesGrowth!.toFixed(1)}` : "-"}</td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-2 px-4 text-gray-700">坪效 (千元/店)</td>
                  <td className="text-right py-2 px-4">{selected1.years[selectedYear]?.salesPerStore !== null ? selected1.years[selectedYear].salesPerStore!.toFixed(1) : "-"}</td>
                  <td className="text-right py-2 px-4">{selected2.years[selectedYear]?.salesPerStore !== null ? selected2.years[selectedYear].salesPerStore!.toFixed(1) : "-"}</td>
                  <td className="text-right py-2 px-4">{selected3.years[selectedYear]?.salesPerStore !== null ? selected3.years[selectedYear].salesPerStore!.toFixed(1) : "-"}</td>
                </tr>

                {/* 盈利篇 */}
                <tr className="bg-green-50">
                  <td colSpan={4} className="py-2 px-4 font-semibold text-green-700">盈利篇</td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-2 px-4 text-gray-700 flex items-center gap-1">
                    毛利率 (%)
                    {showComments && (
                      <DataMarker companyId="industry" metric="grossMargin">
                        <span className="text-amber-500 cursor-help">*</span>
                      </DataMarker>
                    )}
                  </td>
                  <td className="text-right py-2 px-4">
                    <InlineCommentMarker companyId={selected1.id} metric="grossMargin" value={selected1.years[selectedYear]?.grossMargin !== null ? `${selected1.years[selectedYear].grossMargin!.toFixed(1)}%` : "-"} year={selectedYear} />
                  </td>
                  <td className="text-right py-2 px-4">
                    <InlineCommentMarker companyId={selected2.id} metric="grossMargin" value={selected2.years[selectedYear]?.grossMargin !== null ? `${selected2.years[selectedYear].grossMargin!.toFixed(1)}%` : "-"} year={selectedYear} />
                  </td>
                  <td className="text-right py-2 px-4">
                    <InlineCommentMarker companyId={selected3.id} metric="grossMargin" value={selected3.years[selectedYear]?.grossMargin !== null ? `${selected3.years[selectedYear].grossMargin!.toFixed(1)}%` : "-"} year={selectedYear} />
                  </td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-2 px-4 text-gray-700">营业利润率 (%)</td>
                  <td className="text-right py-2 px-4">{selected1.years[selectedYear]?.operatingProfitMargin !== null ? `${selected1.years[selectedYear].operatingProfitMargin!.toFixed(1)}%` : "-"}</td>
                  <td className="text-right py-2 px-4">{selected2.years[selectedYear]?.operatingProfitMargin !== null ? `${selected2.years[selectedYear].operatingProfitMargin!.toFixed(1)}%` : "-"}</td>
                  <td className="text-right py-2 px-4">{selected3.years[selectedYear]?.operatingProfitMargin !== null ? `${selected3.years[selectedYear].operatingProfitMargin!.toFixed(1)}%` : "-"}</td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-2 px-4 text-gray-700 flex items-center gap-1">
                    净利率 (%)
                    {showComments && (
                      <DataMarker companyId="industry" metric="netMargin">
                        <span className="text-amber-500 cursor-help">*</span>
                      </DataMarker>
                    )}
                  </td>
                  <td className="text-right py-2 px-4">
                    <InlineCommentMarker companyId={selected1.id} metric="netMargin" value={selected1.years[selectedYear]?.netMargin !== null ? `${selected1.years[selectedYear].netMargin!.toFixed(1)}%` : "-"} year={selectedYear} />
                  </td>
                  <td className="text-right py-2 px-4">
                    <InlineCommentMarker companyId={selected2.id} metric="netMargin" value={selected2.years[selectedYear]?.netMargin !== null ? `${selected2.years[selectedYear].netMargin!.toFixed(1)}%` : "-"} year={selectedYear} />
                  </td>
                  <td className="text-right py-2 px-4">
                    <InlineCommentMarker companyId={selected3.id} metric="netMargin" value={selected3.years[selectedYear]?.netMargin !== null ? `${selected3.years[selectedYear].netMargin!.toFixed(1)}%` : "-"} year={selectedYear} />
                  </td>
                </tr>

                {/* 效率篇 */}
                <tr className="bg-orange-50">
                  <td colSpan={4} className="py-2 px-4 font-semibold text-orange-700">效率篇</td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-2 px-4 text-gray-700">运营费用率 (%)</td>
                  <td className="text-right py-2 px-4">{selected1.years[selectedYear]?.operatingExpenseRatio !== null ? `${selected1.years[selectedYear].operatingExpenseRatio!.toFixed(1)}%` : "-"}</td>
                  <td className="text-right py-2 px-4">{selected2.years[selectedYear]?.operatingExpenseRatio !== null ? `${selected2.years[selectedYear].operatingExpenseRatio!.toFixed(1)}%` : "-"}</td>
                  <td className="text-right py-2 px-4">{selected3.years[selectedYear]?.operatingExpenseRatio !== null ? `${selected3.years[selectedYear].operatingExpenseRatio!.toFixed(1)}%` : "-"}</td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-2 px-4 text-gray-700">库存周转天数</td>
                  <td className="text-right py-2 px-4">{selected1.years[selectedYear]?.inventoryTurnoverDays !== null ? `${selected1.years[selectedYear].inventoryTurnoverDays}天` : "-"}</td>
                  <td className="text-right py-2 px-4">{selected2.years[selectedYear]?.inventoryTurnoverDays !== null ? `${selected2.years[selectedYear].inventoryTurnoverDays}天` : "-"}</td>
                  <td className="text-right py-2 px-4">{selected3.years[selectedYear]?.inventoryTurnoverDays !== null ? `${selected3.years[selectedYear].inventoryTurnoverDays}天` : "-"}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;