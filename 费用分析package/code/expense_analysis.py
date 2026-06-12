#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财报费用分析工具
功能：趋势分析、品牌对比、关键词提取、定量计算
"""

import pandas as pd
import numpy as np
import re
from collections import Counter, defaultdict
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# 第一部分：数据加载和预处理
# ============================================================================

class ExpenseDataLoader:
    """费用数据加载器"""

    def __init__(self):
        self.data = None
        self.companies = []
        self.brands = []
        self.expense_types = []

    def load_from_csv(self, file_path):
        """从CSV文件加载费用数据"""
        try:
            self.data = pd.read_csv(file_path)
            self._extract_metadata()
            print(f"✓ 成功加载数据：{len(self.data)} 条记录")
            return self.data
        except Exception as e:
            print(f"✗ 数据加载失败：{str(e)}")
            return None

    def _extract_metadata(self):
        """提取元数据"""
        if self.data is not None:
            self.companies = self.data['company'].unique().tolist()
            self.brands = self.data['brand'].unique().tolist()
            self.expense_types = self.data['expense_type'].unique().tolist()

    def filter_by_company(self, company_name):
        """按公司筛选数据"""
        if self.data is not None:
            return self.data[self.data['company'] == company_name]
        return None

    def filter_by_brand(self, brand_name):
        """按品牌筛选数据"""
        if self.data is not None:
            return self.data[self.data['brand'] == brand_name]
        return None

    def filter_by_period(self, start_year, end_year=None):
        """按时间范围筛选数据"""
        if self.data is not None:
            mask = self.data['fiscal_year'] >= start_year
            if end_year:
                mask &= self.data['fiscal_year'] <= end_year
            return self.data[mask]
        return None

    def get_summary(self):
        """获取数据摘要"""
        if self.data is not None:
            return {
                'total_records': len(self.data),
                'companies': self.companies,
                'brands': self.brands,
                'expense_types': self.expense_types,
                'date_range': f"{self.data['fiscal_year'].min()}-{self.data['fiscal_year'].max()}"
            }
        return None


# ============================================================================
# 第二部分：趋势分析
# ============================================================================

class TrendAnalyzer:
    """趋势分析器"""

    def __init__(self, data):
        self.data = data

    def calculate_cagr(self, company, expense_type, years=3):
        """计算年复合增长率"""
        filtered = self.data[
            (self.data['company'] == company) &
            (self.data['expense_type'] == expense_type)
        ].sort_values('fiscal_year')

        if len(filtered) < 2:
            return None

        start_value = filtered['amount_usd'].iloc[0]
        end_value = filtered['amount_usd'].iloc[-1]
        n_years = filtered['fiscal_year'].iloc[-1] - filtered['fiscal_year'].iloc[0]

        if n_years == 0 or start_value == 0:
            return None

        cagr = (end_value / start_value) ** (1 / n_years) - 1
        return round(cagr * 100, 2)

    def calculate_expense_ratio_trend(self, company, expense_type):
        """计算费用占比变化趋势"""
        filtered = self.data[
            (self.data['company'] == company) &
            (self.data['expense_type'] == expense_type)
        ].sort_values(['fiscal_year', 'fiscal_quarter'])

        if len(filtered) < 2:
            return None

        first_ratio = filtered['expense_ratio_pct'].iloc[0]
        last_ratio = filtered['expense_ratio_pct'].iloc[-1]
        change = last_ratio - first_ratio

        return {
            'first_ratio': round(first_ratio, 2),
            'last_ratio': round(last_ratio, 2),
            'absolute_change': round(change, 2),
            'relative_change': round((change / first_ratio) * 100, 2) if first_ratio != 0 else None
        }

    def get_growth_rate_stats(self, company=None):
        """获取增长率统计"""
        if company:
            filtered = self.data[self.data['company'] == company]
        else:
            filtered = self.data

        return {
            'avg_yoy_growth': round(filtered['yoy_growth_pct'].mean(), 2),
            'median_yoy_growth': round(filtered['yoy_growth_pct'].median(), 2),
            'max_yoy_growth': round(filtered['yoy_growth_pct'].max(), 2),
            'min_yoy_growth': round(filtered['yoy_growth_pct'].min(), 2),
            'std_yoy_growth': round(filtered['yoy_growth_pct'].std(), 2)
        }

    def identify_trend_pattern(self, company, expense_type):
        """识别趋势模式"""
        filtered = self.data[
            (self.data['company'] == company) &
            (self.data['expense_type'] == expense_type)
        ].sort_values('fiscal_year')

        if len(filtered) < 3:
            return "数据不足"

        growth_rates = filtered['yoy_growth_pct'].values

        # 持续上升检测
        if all(growth_rates[i] > growth_rates[i-1] for i in range(1, len(growth_rates))):
            if all(r > 0 for r in growth_rates):
                return "持续上升"

        # 持续下降检测
        if all(growth_rates[i] < growth_rates[i-1] for i in range(1, len(growth_rates))):
            if all(r < 0 for r in growth_rates):
                return "持续下降"

        # 周期性波动检测
        if len(growth_rates) >= 4:
            peaks = sum(1 for i in range(1, len(growth_rates)-1)
                       if growth_rates[i] > growth_rates[i-1] and growth_rates[i] > growth_rates[i+1])
            if peaks >= 2:
                return "周期性波动"

        return "无明显趋势"

    def generate_trend_report(self):
        """生成趋势分析报告"""
        report = []

        for company in self.data['company'].unique():
            for expense_type in self.data['expense_type'].unique():
                cagr = self.calculate_cagr(company, expense_type)
                ratio_trend = self.calculate_expense_ratio_trend(company, expense_type)
                pattern = self.identify_trend_pattern(company, expense_type)

                report.append({
                    'company': company,
                    'expense_type': expense_type,
                    'cagr': cagr,
                    'ratio_trend': ratio_trend,
                    'pattern': pattern
                })

        return pd.DataFrame(report)


# ============================================================================
# 第三部分：品牌对比分析
# ============================================================================

class BrandComparator:
    """品牌对比分析器"""

    def __init__(self, data):
        self.data = data

    def compare_expense_structure(self, brands=None):
        """比较费用结构"""
        if brands:
            filtered = self.data[self.data['brand'].isin(brands)]
        else:
            filtered = self.data

        # 按品牌和费用类型分组计算平均占比
        grouped = filtered.groupby(['brand', 'expense_type'])['expense_ratio_pct'].mean().reset_index()

        # 转换为宽表格式
        pivot = grouped.pivot(index='brand', columns='expense_type', values='expense_ratio_pct')

        return pivot.fillna(0)

    def compare_expense_efficiency(self, brands=None):
        """比较费用效率"""
        if brands:
            filtered = self.data[self.data['brand'].isin(brands)]
        else:
            filtered = self.data

        # 计算各品牌费用/营收比
        efficiency = filtered.groupby('brand').agg({
            'expense_ratio_pct': 'mean',
            'yoy_growth_pct': 'mean',
            'amount_usd': 'sum'
        }).reset_index()

        efficiency.columns = ['brand', 'avg_expense_ratio', 'avg_growth_rate', 'total_expense']

        return efficiency

    def rank_brands_by_metric(self, metric='expense_ratio_pct', ascending=True):
        """按指标对品牌排序"""
        ranked = self.data.groupby('brand')[metric].mean().reset_index()
        ranked = ranked.sort_values(metric, ascending=ascending)
        ranked['rank'] = range(1, len(ranked) + 1)

        return ranked

    def calculate_expense_gap(self, brand1, brand2, expense_type):
        """计算两个品牌间的费用差距"""
        data1 = self.data[self.data['brand'] == brand1]
        data2 = self.data[self.data['brand'] == brand2]

        if len(data1) == 0 or len(data2) == 0:
            return None

        ratio1 = data1[data1['expense_type'] == expense_type]['expense_ratio_pct'].mean()
        ratio2 = data2[data2['expense_type'] == expense_type]['expense_ratio_pct'].mean()

        return {
            'brand1': brand1,
            'brand2': brand2,
            'expense_type': expense_type,
            'ratio1': round(ratio1, 2),
            'ratio2': round(ratio2, 2),
            'gap': round(ratio1 - ratio2, 2),
            'gap_pct': round(((ratio1 - ratio2) / ratio2) * 100, 2) if ratio2 != 0 else None
        }

    def generate_comparison_matrix(self):
        """生成品牌对比矩阵"""
        brands = self.data['brand'].unique()
        matrix = pd.DataFrame(index=brands, columns=brands)

        for b1 in brands:
            for b2 in brands:
                if b1 != b2:
                    avg_ratio1 = self.data[self.data['brand'] == b1]['expense_ratio_pct'].mean()
                    avg_ratio2 = self.data[self.data['brand'] == b2]['expense_ratio_pct'].mean()
                    matrix.loc[b1, b2] = round(avg_ratio1 - avg_ratio2, 2)
                else:
                    matrix.loc[b1, b2] = 0

        return matrix


# ============================================================================
# 第四部分：关键词分析
# ============================================================================

class KeywordAnalyzer:
    """关键词分析器"""

    def __init__(self, text_data=None):
        self.text_data = text_data if text_data else []
        self.keyword_dict = self._load_default_keywords()

    def _load_default_keywords(self):
        """加载默认关键词词典"""
        return {
            'expense_types': {
                'sga': ['selling', 'general', 'administrative', 'SGA', 'sales and marketing', 'distribution'],
                'rd': ['research', 'development', 'R&D', 'innovation', 'product development'],
                'marketing': ['marketing', 'advertising', 'promotion', 'brand', 'customer acquisition'],
                'operating_expense': ['operating', 'operations', 'operational', 'facilities', 'logistics'],
                'personnel': ['employee', 'compensation', 'headcount', 'personnel', 'workforce', 'salary'],
                'technology': ['technology', 'cloud', 'software', 'IT', 'infrastructure', 'data'],
                'legal': ['legal', 'compliance', 'regulatory', 'litigation', 'settlement'],
                'other': ['other', 'miscellaneous', 'general']
            },
            'trends': {
                'increase': ['increase', 'grew', 'growth', 'higher', 'increased', 'rose', 'up'],
                'decrease': ['decrease', 'declined', 'lower', 'reduced', 'decline', 'fell', 'down'],
                'stable': ['stable', 'consistent', 'unchanged', 'flat', 'similar'],
                'volatile': ['volatile', 'fluctuate', 'fluctuation', 'variable', 'unstable'],
                'new': ['new', 'added', 'additional', 'first time', 'newly'],
                'reduction': ['reduction', 'cut', 'restructuring', 'streamline', 'optimization']
            },
            'drivers': {
                'business_expansion': ['growth', 'expansion', 'scale', 'volume', 'business growth', 'new markets'],
                'investment': ['investment', 'initiative', 'strategic', 'transformation', 'venture', 'project'],
                'efficiency': ['efficiency', 'optimization', 'automation', 'productivity', 'cost saving', 'improved'],
                'external': ['currency', 'inflation', 'regulatory', 'macroeconomic', 'pandemic', 'economic'],
                'restructuring': ['restructuring', 'reorganization', 'integration', 'acquisition', 'merger', 'consolidation'],
                'one_time': ['one-time', 'special', 'impairment', 'restructuring charge', 'legal settlement', 'settlement']
            }
        }

    def add_text(self, text):
        """添加文本数据"""
        self.text_data.append(text)

    def add_texts(self, texts):
        """批量添加文本数据"""
        self.text_data.extend(texts)

    def extract_keywords(self, category='expense_types'):
        """提取指定类别的关键词"""
        word_counts = Counter()

        for text in self.text_data:
            text_lower = text.lower()
            for keyword_list in self.keyword_dict.get(category, {}).values():
                for keyword in keyword_list:
                    count = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower))
                    if count > 0:
                        word_counts[keyword] += count

        return word_counts.most_common()

    def analyze_keyword_frequency(self, min_count=1):
        """分析关键词频率"""
        results = {
            'expense_types': self.extract_keywords('expense_types'),
            'trends': self.extract_keywords('trends'),
            'drivers': self.extract_keywords('drivers')
        }

        filtered_results = {}
        for category, keywords in results.items():
            filtered = [(k, c) for k, c in keywords if c >= min_count]
            filtered_results[category] = filtered

        return filtered_results

    def get_keyword_cooccurrence(self, top_n=10):
        """获取关键词共现关系"""
        cooccurrence = defaultdict(lambda: defaultdict(int))

        for text in self.text_data:
            text_lower = text.lower()
            found_keywords = []

            for category, keywords in self.keyword_dict.items():
                for keyword_list in keywords.values():
                    for keyword in keyword_list:
                        if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower):
                            found_keywords.append(keyword)

            # 统计共现
            for i in range(len(found_keywords)):
                for j in range(i+1, len(found_keywords)):
                    if found_keywords[i] != found_keywords[j]:
                        cooccurrence[found_keywords[i]][found_keywords[j]] += 1

        # 转换为可读格式
        result = {}
        for kw1, related in cooccurrence.items():
            if len(result) < top_n:
                top_related = sorted(related.items(), key=lambda x: -x[1])[:5]
                if top_related:
                    result[kw1] = dict(top_related)

        return result

    def generate_keyword_report(self):
        """生成关键词分析报告"""
        frequency = self.analyze_keyword_frequency()

        report = {
            'total_texts': len(self.text_data),
            'categories': {}
        }

        for category, keywords in frequency.items():
            if keywords:
                report['categories'][category] = {
                    'total_mentions': sum(c for _, c in keywords),
                    'unique_keywords': len(keywords),
                    'top_keywords': keywords[:10]
                }

        return report


# ============================================================================
# 第五部分：定量计算工具
# ============================================================================

class ExpenseCalculator:
    """费用计算工具"""

    @staticmethod
    def calculate_cagr(start_value, end_value, years):
        """计算年复合增长率"""
        if years == 0 or start_value == 0:
            return None
        return (end_value / start_value) ** (1 / years) - 1

    @staticmethod
    def calculate_expense_ratio(expense, revenue):
        """计算费用占比"""
        if revenue == 0:
            return None
        return expense / revenue

    @staticmethod
    def calculate_growth_rate(current, previous):
        """计算增长率"""
        if previous == 0:
            return None
        return (current - previous) / previous

    @staticmethod
    def calculate_performance_index(expense_ratio, industry_avg):
        """计算绩效指数"""
        if industry_avg == 0:
            return None
        return expense_ratio / industry_avg

    @staticmethod
    def calculate_efficiency_score(amount, revenue, headcount):
        """计算效率分数"""
        if revenue == 0 or headcount == 0:
            return None

        expense_per_revenue = amount / revenue
        expense_per_person = amount / headcount

        # 综合效率分数（越低越好）
        return (expense_per_revenue + expense_per_person) / 2


# ============================================================================
# 第六部分：分析报告生成
# ============================================================================

class AnalysisReporter:
    """分析报告生成器"""

    def __init__(self, data, text_data=None):
        self.data = data
        self.text_data = text_data if text_data else []
        self.trend_analyzer = TrendAnalyzer(data)
        self.brand_comparator = BrandComparator(data)
        self.keyword_analyzer = KeywordAnalyzer(text_data)

    def generate_full_report(self):
        """生成完整分析报告"""
        report = {
            'report_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_summary': self._generate_data_summary(),
            'trend_analysis': self._generate_trend_analysis(),
            'brand_comparison': self._generate_brand_comparison(),
            'keyword_analysis': self._generate_keyword_analysis(),
            'key_findings': self._generate_key_findings()
        }

        return report

    def _generate_data_summary(self):
        """生成数据摘要"""
        return {
            'total_records': len(self.data),
            'companies': self.data['company'].unique().tolist(),
            'brands': self.data['brand'].unique().tolist(),
            'expense_types': self.data['expense_type'].unique().tolist(),
            'date_range': f"{self.data['fiscal_year'].min()}-{self.data['fiscal_year'].max()}",
            'total_expense': self.data['amount_usd'].sum(),
            'avg_expense_ratio': self.data['expense_ratio_pct'].mean()
        }

    def _generate_trend_analysis(self):
        """生成趋势分析"""
        return self.trend_analyzer.generate_trend_report().to_dict('records')

    def _generate_brand_comparison(self):
        """生成品牌对比"""
        return {
            'expense_structure': self.brand_comparator.compare_expense_structure().to_dict(),
            'efficiency_comparison': self.brand_comparator.compare_expense_efficiency().to_dict(),
            'comparison_matrix': self.brand_comparator.generate_comparison_matrix().to_dict()
        }

    def _generate_keyword_analysis(self):
        """生成关键词分析"""
        return self.keyword_analyzer.generate_keyword_report()

    def _generate_key_findings(self):
        """生成关键发现"""
        findings = []

        # 费用趋势发现
        for company in self.data['company'].unique():
            for expense_type in self.data['expense_type'].unique():
                pattern = self.trend_analyzer.identify_trend_pattern(company, expense_type)
                if pattern in ['持续上升', '持续下降']:
                    findings.append({
                        'type': 'trend',
                        'company': company,
                        'expense_type': expense_type,
                        'finding': f"{company}的{expense_type}呈现{pattern}"
                    })

        # 品牌差异发现
        brands = self.data['brand'].unique()
        if len(brands) >= 2:
            for i in range(len(brands)):
                for j in range(i+1, len(brands)):
                    gap = self.brand_comparator.calculate_expense_gap(brands[i], brands[j], 'sga')
                    if gap and abs(gap['gap']) > 2:
                        findings.append({
                            'type': 'brand_gap',
                            'brands': [brands[i], brands[j]],
                            'finding': f"{brands[i]}与{brands[j]}的SG&A费用占比差距为{gap['gap']}个百分点"
                        })

        return findings

    def export_report(self, output_path):
        """导出报告到JSON文件"""
        report = self.generate_full_report()

        # 自定义JSON编码器，处理numpy类型
        class NumpyEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, (np.integer, np.int64)):
                    return int(obj)
                elif isinstance(obj, (np.floating, np.float64)):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                return super().default(obj)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, cls=NumpyEncoder)

        print(f"✓ 报告已导出至：{output_path}")
        return report


# ============================================================================
# 主程序入口
# ============================================================================

def main():
    """主程序"""
    print("=" * 60)
    print("财报费用分析工具 v1.0")
    print("=" * 60)

    # 示例数据加载
    try:
        loader = ExpenseDataLoader()
        data = loader.load_from_csv('/workspace/data/expense_data_template.csv')

        if data is not None:
            # 生成完整报告
            reporter = AnalysisReporter(data)
            report = reporter.generate_full_report()

            print("\n" + "=" * 60)
            print("分析报告摘要")
            print("=" * 60)

            print(f"\n数据摘要：")
            print(f"  - 总记录数：{report['data_summary']['total_records']}")
            print(f"  - 公司：{', '.join(report['data_summary']['companies'])}")
            print(f"  - 品牌：{', '.join(report['data_summary']['brands'])}")
            print(f"  - 费用类型：{', '.join(report['data_summary']['expense_types'])}")

            print(f"\n关键发现：")
            for i, finding in enumerate(report['key_findings'][:5], 1):
                print(f"  {i}. {finding['finding']}")

            # 导出报告
            reporter.export_report('/workspace/reports/expense_analysis_report.json')

    except Exception as e:
        print(f"\n✗ 运行出错：{str(e)}")
        print("请确保数据文件存在于指定路径")


if __name__ == '__main__':
    main()