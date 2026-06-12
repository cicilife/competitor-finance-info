# 财报费用分析框架

## 项目概述

这是一个完整的财报费用分析框架，用于系统化分析竞品财报中的经营费用、SG&A等数据趋势和驱动因素。框架包含数据收集、文本标注、定量分析和可视化输出的完整流程。

## 目录结构

```
/workspace/
├── docs/                          # 文档目录
│   ├── expense_analysis_framework.md   # 分析框架设计
│   └── implementation_guide.md          # 实施指南
├── data/                          # 数据目录
│   ├── expense_data_template.csv         # 数据收集模板
│   ├── text_labeling_schema.json        # 文本标注Schema
│   └── sample_annotated_texts.json       # 标注示例数据
├── code/                          # 代码目录
│   ├── expense_analysis.py             # 定量分析脚本
│   └── expense_visualization.py         # 可视化脚本
└── charts/                        # 图表输出目录
```

## 快速开始

### 1. 数据准备

使用 `data/expense_data_template.csv` 模板收集费用数据，确保包含以下字段：

- company, brand, period, fiscal_year, fiscal_quarter
- expense_type, amount_usd, revenue_usd, expense_ratio_pct
- yoy_growth_pct, qoq_growth_pct, notes

### 2. 文本标注

参考 `data/text_labeling_schema.json` 进行文本标注：

- expense_type: 费用类型（sga, rd, marketing等）
- trend: 趋势变化（increase, decrease, stable等）
- driver: 驱动因素（business_expansion, investment等）
- sentiment: 情感倾向（positive, negative, neutral）

### 3. 运行分析

```python
from code.expense_analysis import ExpenseDataLoader, TrendAnalyzer

# 加载数据
loader = ExpenseDataLoader()
data = loader.load_from_csv('data/expense_data_template.csv')

# 趋势分析
analyzer = TrendAnalyzer(data)
cagr = analyzer.calculate_cagr('示例公司', 'sga')
```

### 4. 生成可视化

```python
from code.expense_visualization import ExpenseVisualizer

visualizer = ExpenseVisualizer(data)
visualizer.plot_expense_trend('示例公司', 'sga', 'charts/trend.png')
```

## 主要功能

### 定量分析

- 年复合增长率（CAGR）计算
- 费用占比变化趋势分析
- 品牌间费用差距对比
- 关键词词频统计分析

### 可视化输出

- 费用趋势折线图
- 品牌对比雷达图
- 费用结构堆叠图
- 关键词词云图

## 注意事项

1. 数据来源：使用公司官方财报（10-K/10-Q）
2. 标注质量：建议进行双人独立标注并检验一致性
3. 汇率处理：统一转换为美元并注明汇率来源
4. 时间对齐：确保各公司数据按相同财年/季度对齐

## 版本信息

- 版本：v1.0
- 创建日期：2026年6月
- 适用范围：消费品牌财报费用分析