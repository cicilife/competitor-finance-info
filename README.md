# 竞品财务数据库 (Competitor Finance Info)

> 全球运动品牌财报数据汇总与分析系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 项目简介

本项目汇总全球主要运动品牌的财报数据，涵盖港股、A股、美股、欧股、日股、台股六大市场，包含21个核心品牌100+条数据。

### 覆盖品牌

| 市场 | 品牌 | 报告期间 |
|------|------|---------|
| **港股** | 安踏(ANTA)、李宁、特步、361度、滔搏 | FY2023-FY2025 |
| **A股** | 探路者、比音勒芬、牧高笛 | FY2023-FY2025 |
| **美股** | Nike、Adidas、Skechers、Columbia、Lululemon、Under Armour、On Holding、Amer Sports、VF Corp | FY2023-FY2025 |
| **欧股** | Adidas、Puma、On Holding、Amer Sports | FY2023-FY2025 |
| **日股** | ASICS、Fast Retailing | FY2023-FY2025 |
| **台股** | 捷安特(Giant) | FY2023-FY2025 |

## 核心数据指标

### 1. 营业收入类
- 营业收入(Net Revenue / Net Sales)
- 净利润(Net Income / Net Profit)
- 归属母公司净利润(Net Income Attributable to Shareholders)

### 2. 成本/费用类
- 毛利(Gross Profit)
- 经营利润(EBIT / Operating Profit)
- 经营费用(Operating Expenses)
- 分销与销售费用(Distribution and Selling Expenses)

### 3. 比率类(28个核心指标)
- 毛利率(Gross Margin)
- 经营利润率(EBIT Margin)
- 净利率(Net Profit Margin)
- 经营费用率(Operating Expense Ratio) - **4种不同市场口径**
- 员工/广告/研发费用率

### 4. 运营指标
- 门店数(Number of Stores)
- 单店收入(Sales per Store)
- 库存周转天数(Days Inventory Outstanding)
- 数字渠道占比(Digital Sales Ratio)

## 经营费用率 4 种市场口径

| 口径 | 适用市场 | 计算公式 | 包含项目 |
|------|---------|---------|---------|
| **口径A** | 港股(滔搏/特步) | 销售及分销 + 一般及行政 | 销售+管理 |
| **口径B** | 港股(安踏/李宁) | 1 - 毛利率 - 经营利润率 | 全部经营支出 |
| **口径C** | 港股(361度) | 广告 + 员工 + 研发 | 广告+员工+研发 |
| **口径D** | A股 | 销售 + 管理 + 研发 | 销售+管理+研发 |

## 项目结构

```
competitor_finance_info/
├── README.md                          # 本文件
├── SKILL_V3_GUIDE.md                  # 核心工作流文档
├── main.py                            # 项目主入口
├── 竞品财务数据库_标准模板v2_latest.xlsx  # 最新数据库
├── 竞品财务数据库_标准模板v2.xlsx        # 当前工作数据库
├── data_versions/                     # 历史版本归档
├── scripts/                           # 项目脚本
│   ├── temp_scripts/                  # 临时脚本(已git忽略)
│   ├── data_extraction/               # 数据提取脚本
│   └── quality_check/                 # 质量检查脚本
├── docs/                              # 文档
├── config/                            # 配置文件
├── modules/                           # 核心模块
├── tasks/                             # 任务定义
├── notebooks/                         # Jupyter notebooks
├── 竞品财务PDF库/                      # 原始PDF年报(已git忽略)
├── 网页报告/                          # 网页报告输出
└── logs/                              # 运行日志
```

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/your-username/competitor-finance-info.git
cd competitor-finance-info
```

### 2. 安装依赖

```bash
pip install pandas openpyxl pdfplumber
```

### 3. 数据提取流程

```bash
# 1. 放置PDF年报到 竞品财务PDF库/ 目录
# 2. 运行数据提取
python main.py
```

## 工作流文档

详细的工作流见 [SKILL_V3_GUIDE.md](./SKILL_V3_GUIDE.md)，包含：

1. **数据提取规范** - 如何从PDF年报提取数据
2. **指标归一化** - 中英文对照、口径统一
3. **质量检查** - 4组配对指标、来源溯源
4. **数据修正流程** - 反推公式、对比验证

## 数据来源

- **港股年报**: HKEX披露易 (https://www.hkex.com.hk)
- **A股年报**: 巨潮资讯网 (http://www.cninfo.com.cn)
- **美股10-K**: SEC EDGAR (https://www.sec.gov/edgar)
- **欧股年报**: 上市公司IR页面
- **日股年报**: TDnet (https://www.release.tdnet.info)
- **台股年报**: 公开资讯观测站 (https://mops.twse.com.tw)

## 数据质量

- ✅ 716+ 条数据，覆盖21个品牌
- ✅ 每个数据点都有来源页码和原文摘录
- ✅ 4种经营费用率口径已明确标注
- ✅ 已修正60+条错误数据

## 更新日志

### v2 (Latest)
- 修正安踏2025年报经营费用率(38.2%/38.8%/41.1%)
- 修正滔搏经营费用率(33.1%/32.8%/33.8%)
- 修正李宁/特步/361度/探路者/比音勒芬/牧高笛等6个品牌
- 新增20+条费用分项(员工/广告/研发)
- 整理项目结构,清理100+临时脚本
- 添加 `.gitignore` 排除临时文件和大文件

### v1 (Initial)
- 导入现有项目
- 716+条数据,21个品牌,28个核心指标

## 贡献指南

欢迎提交 Pull Request。请确保：

1. 新数据有明确的PDF年报来源和页码
2. 经营费用率必须明确标注口径(A/B/C/D)
3. 提交前运行质量检查脚本

## 许可证

MIT License

## 联系方式

- 仓库: https://github.com/cicilife/competitor-finance-info
- 邮箱: wusi159753@163.com

---

**最后更新**: 2026-06-15
