# 竞品财报费用分析框架 v2.0

## 更新日期：2026-06-05

## 一、框架概述

本框架旨在系统化分析竞品财报中关于经营费用（Operating Expenses）、SG&A（销售及管理费用）及其他费用项目的趋势、差异和关键描述。通过文本打标和定量分析，为业务决策提供数据支持。

### 1.1 分析目标

- 量化各类费用的趋势变化和占比变动
- 识别品牌/公司间的费用结构差异
- **新增：关注运营效率，筛选费效比高的品牌**
- **新增：分析DTC转型、供应链等体育用品行业特定驱动因素**
- 提取高频费用类型和关键描述词
- 发现费用变化的驱动因素和解释性文本

### 1.2 分析维度

本框架包含以下分析维度：

| 维度类别 | 具体分析内容 | 数据来源 | 优先级 |
|---------|------------|---------|-------|
| 费用趋势 | 费用金额、占比、增长率的时序变化 | 财务数据表 | P0 |
| 品牌差异 | 不同品牌费用结构对比 | 财务数据表 | P0 |
| **费效分析** | **费用效率指标（费用/营收比、人均费用）** | **财务数据表** | **P0** |
| 费用类型 | 各费用类型（SG&A、R&D、营销等）分布 | 财务数据表 | P1 |
| 文本关键词 | 费用相关描述词频分析 | MD&A文本 | P1 |
| 驱动因素 | 费用变化的解释性原因 | MD&A文本 | P1 |
| **效率指标** | **效率趋势、效率驱动因素** | **MD&A文本** | **P1** |

---

## 二、数据收集规范

### 2.1 财务数据收集

**收集范围**：

- 季度/年度费用数据（至少3年历史数据）
- 费用明细科目（SG&A、R&D、Marketing、COGS、物流成本等）
- 费用占营收比（Expense as % of Revenue）
- 费用同比/环比增长率
- **新增：人均费用、单位产出费用、费用效率指标**

**数据格式**：

```
company,brand,period,fiscal_year,fiscal_quarter,expense_type,amount_usd,revenue_usd,expense_ratio_pct,yoy_growth_pct,headcount,efficiency_metric
```

### 2.2 文本数据收集

**收集范围**：

- MD&A（管理层讨论与分析）章节
- 经营费用相关段落
- 费用解释和说明文字
- **效率相关讨论、DTC转型、供应链成本分析**

**文本来源**：

- 10-K/10-Q年报
- 投资者电话会议记录
- 财报新闻稿

---

## 三、标注体系 v2.0

### 3.1 费用类型标注

| 费用类型 | 标签 | 说明 | 关键词示例 |
|---------|------|------|----------|
| SG&A | sga | 销售及管理费用 | selling, general, administrative, SG&A, 分销费用 |
| 研发费用 | rd | 研发支出 | research, development, R&D, 产品创新 |
| 营销费用 | marketing | 市场推广费用 | marketing, advertising, promotion, 品牌建设 |
| 运营费用 | operating_expense | 运营相关费用 | operating, operations, 运营费用, 经营成本 |
| 人力成本 | personnel | 人工相关费用 | employee, compensation, headcount, 人力成本 |
| 技术成本 | technology | 技术/云服务费用 | technology, cloud, IT, 数字化 |
| **物流成本** | **logistics** | **仓储物流费用** | **logistics, fulfillment, shipping, 物流, 配送** |
| **数字营销** | **marketing_digital** | **电商/DTC渠道费用** | **digital marketing, DTC, e-commerce, 电商, 直销** |
| **门店成本** | **real_estate** | **门店租赁运营费用** | **store, rent, lease, 门店, 租金** |
| 法律合规 | legal | 法律和合规费用 | legal, compliance, regulatory |
| 其他费用 | other | 其他费用 | other, miscellaneous |

### 3.2 趋势标注

| 趋势类型 | 标签 | 说明 |
|---------|------|------|
| 上升 | increase | 费用增加 |
| 下降 | decrease | 费用减少 |
| 持平 | stable | 费用基本不变 |
| 波动 | volatile | 费用波动 |
| 新增 | new | 新费用项目 |
| 削减 | reduction | 费用削减 |

### 3.3 驱动因素标注 v2.0

| 因素类型 | 标签 | 说明 | 关键词示例 |
|---------|------|------|----------|
| 业务扩张 | business_expansion | 业务增长导致 | growth, expansion, scale |
| 投资驱动 | investment | 战略投资导致 | investment, initiative, strategic |
| 效率提升 | efficiency | 效率改善导致 | efficiency, optimization, 降本增效 |
| **DTC转型** | **dtc_transformation** | **直销渠道转型** | **DTC, direct-to-consumer, 电商渠道, 直销** |
| **品牌建设** | **brand_building** | **品牌投入** | **brand building, brand investment, 品牌投入** |
| **产品创新** | **product_innovation** | **产品研发创新** | **product innovation, R&D, 产品创新** |
| **供应链** | **supply_chain** | **供应链成本** | **supply chain, logistics, 供应链, 采购** |
| 外部因素 | external | 外部环境影响 | currency, inflation, 汇率, 关税 |
| 重组整合 | restructuring | 重组导致 | restructuring, reorganization |
| 一次性 | one_time | 一次性项目 | one-time, special, 一次性 |

### 3.4 效率指标标注（新增）

| 效率类型 | 标签 | 说明 | 关键词示例 |
|---------|------|------|----------|
| 高效 | high_efficiency | 费用效率提升 | efficiency, improved, 效率提升, 规模效应 |
| 低效 | low_efficiency | 费用效率下降 | cost increase, margin pressure, 成本上升 |
| 投资型 | investment_mode | 战略性投入阶段 | investment mode, strategic, 前置投入 |

### 3.5 品牌标注

| 品牌类型 | 标签 | 说明 |
|---------|------|------|
| 高端品牌 | premium | 高端定位品牌 |
| 大众品牌 | mass | 大众市场品牌 |
| 新兴品牌 | emerging | 新进入品牌 |
| 综合集团 | conglomerate | 多品牌集团 |
| 运动科技 | sports_tech | 技术驱动型运动品牌 |

---

## 四、定量分析方法

### 4.1 趋势分析方法

**时间序列分析**：

- 计算各类费用的年复合增长率（CAGR）
- 分析费用占比的变化趋势
- 识别异常波动和转折点
- **新增：费用效率趋势（费用/营收比变化）**

**计算公式**：

```
CAGR = (End Value / Start Value)^(1/n) - 1

费用占比变化 = (期末占比 - 期初占比) / 期初占比 × 100%

费用效率 = 营业收入 / 费用总额 (越高越好)
人均费用 = 费用总额 / 员工人数
```

### 4.2 品牌差异分析

**横向对比**：

- 同期间各品牌费用结构对比
- 费用效率指标（费用/营收比、人均费用）对比
- 费用增速差异分析
- **新增：费效比排名，筛选高效品牌**

**纵向趋势**：

- 各品牌费用结构的历史演变
- 品牌间费用效率差距的变化趋势

**费效比筛选标准**：
- 费用/营收比 < 行业平均 = 高效
- 人均费用 vs 人均产出比较
- 费用增速 < 营收增速 = 效率改善

### 4.3 关键词分析

**词频统计**：

- 统计费用相关描述词的出现频率
- 识别高频关键词和短语
- 分析关键词随时间的变化

**语义分析**：

- 情感倾向（正面/负面/中性）
- 关注度权重（重要性程度）
- **新增：效率相关关键词权重**

### 4.4 驱动因素归因

**因素归因模型**：

- 建立费用变化与驱动因素的关联
- 计算各因素的贡献度
- 识别主要驱动因素和次要因素
- **新增：DTC转型、品牌建设等特定驱动因素分析**

---

## 五、分析维度详细说明

### 5.1 费用趋势变动分析

**核心指标**：

- 绝对金额变化（同比增长、环比增长）
- 相对占比变化（占营收比、占成本比）
- 效率指标（人均费用、单位产出费用）
- **费效比变化趋势**

**趋势类型识别**：

- 持续上升：连续3个周期以上增长
- 持续下降：连续3个周期以上下降
- **效率改善：费用增速 < 营收增速**
- **效率恶化：费用增速 > 营收增速**
- 周期性波动：与业务周期相关
- 阶梯式变化：阶段性大幅调整

**分析输出**：

- 费用趋势图（折线图、堆叠面积图）
- 费用结构变化热力图
- **费效比趋势图**
- 关键转折点标注

### 5.2 品牌差异分析

**对比维度**：

- 费用规模：总费用金额、各类费用金额
- 费用效率：费用占营收比、人均费用、**费效比**
- 费用结构：各类费用占比
- 费用增速：同比增速、环比增速

**分析方法**：

- 雷达图：多维度品牌对比
- 堆叠柱状图：费用结构对比
- **费效比排名表：筛选高效品牌**
- 箱线图：费用分布对比

**关键发现**：

- 费用规模差异
- 费用结构差异
- **费效比差异（核心筛选指标）**
- 战略差异（费用投向）

### 5.3 费用类型和关键词分析

**费用类型分布**：

- 饼图/环形图：费用类型占比
- 堆叠柱状图：各品牌费用类型分布
- 桑基图：费用类型演变

**关键词提取**：

- 词云图：高频关键词可视化
- 词频表：详细词频统计
- 共现网络：关键词关联关系

**关键指标**：

- 费用相关词频统计
- **效率相关词频统计（新增）**
- DTC相关词频统计（新增）
- 增长相关词频统计
- 风险相关词频统计

---

## 六、可补充的分析维度

### 6.1 地理区域分析

- 各区域费用结构和效率
- 区域间费用差异
- 汇率影响分析

### 6.2 产品线分析

- 各产品线费用投入
- 产品线费用效率
- 产品组合费用优化

### 6.3 渠道分析（重点）

- **DTC vs 批发渠道费用对比**
- **各渠道费用效率**
- **渠道费用ROI**

### 6.4 成本效率分析（核心）

- **费效比 = 营收/费用（越高越好）**
- **费用弹性 = 费用增速/营收增速**
- 单位成本趋势
- 规模效应分析
- 成本优化空间

### 6.5 风险与机会分析

- 费用风险识别（过高、波动大）
- **费用效率机会（对比行业标杆）**
- 行业标杆对比

---

## 七、数据处理流程

### 7.1 数据收集

```
1. 财报下载
   └── PDF/HTML格式年报

2. 文本提取
   └── MD&A章节提取
   └── 费用相关段落提取

3. 结构化数据提取
   └── 费用金额表格提取
   └── 时间序列数据整理
```

### 7.2 数据标注

```
1. 文本标注
   ├── 费用类型标注
   ├── 趋势标注
   ├── 驱动因素标注
   ├── 效率指标标注（新增）
   ├── 品牌类型标注

2. 质量检查
   ├── 标注一致性检验
   └── 抽样复核

3. 标注结果输出
   └── 结构化标注数据
```

### 7.3 定量分析

```
1. 描述性统计
   ├── 费用金额统计
   ├── 费用占比统计
   ├── 增长率统计
   ├── 费效比统计（新增）

2. 趋势分析
   ├── 时间序列分析
   ├── 费用效率趋势
   ├── 趋势预测

3. 差异分析
   ├── 品牌间差异
   ├── 时间维度差异
   ├── 费效比排名（新增）

4. 文本分析
   ├── 关键词提取
   ├── 驱动因素归因
   └── 效率关键词分析（新增）
```

### 7.4 可视化输出

```
1. 趋势图表
   └── 费用趋势折线图
   └── 费用结构堆叠图
   └── 费效比趋势图（新增）

2. 对比图表
   └── 品牌对比雷达图
   └── 费用分布箱线图
   └── 费效比排名表（新增）

3. 文本分析
   └── 词云图
   └── 关键词词频表
   └── 驱动因素分布图

4. 综合报告
   └── 分析报告PDF
   └── 交互式仪表板
```

---

## 八、费效比分析专题

### 8.1 费效比定义

```
费效比 = 营业收入 / 运营费用

指标解读：
- 费效比 > 1：每1元费用带来超过1元营收
- 费效比越高越好：表示费用使用效率越高
- 费效比趋势改善：营收增速 > 费用增速
```

### 8.2 费效比筛选标准

**高效品牌特征**：
- 费用/营收比 < 20%（行业优秀水平）
- 费效比持续提升
- 人均费用产出高于行业平均

**分析输出**：
- 费效比排行榜
- 费效比变化趋势图
- 费效比驱动因素分析

### 8.3 费效比驱动因素

| 驱动因素 | 影响方向 | 说明 |
|---------|---------|------|
| DTC渠道占比提升 | 正面 | 减少中间环节，提高费效比 |
| 数字化效率 | 正面 | 降低营销和运营成本 |
| 规模效应 | 正面 | 固定成本摊薄 |
| 供应链优化 | 正面 | 降低物流和采购成本 |
| 品牌投入 | 中性 | 短期费用增加，长期正向 |
| 业务扩张 | 中性 | 可能稀释效率 |

---

## 九、实施步骤

### 第一阶段：框架建立（1周）

1. 确定分析范围和目标
2. 更新数据收集规范（v2.0）
3. 完善标注体系
4. 开发数据处理工具

### 第二阶段：数据收集（2-3周）

1. 收集财报数据
2. 提取文本数据
3. 建立数据库
4. **费效比数据整理**

### 第三阶段：标注分析（2-3周）

1. 文本标注
2. 定量计算
3. 趋势分析
4. **费效比排名**

### 第四阶段：可视化输出（1周）

1. 图表制作
2. 报告撰写
3. 工具开发

---

## 十、工具推荐

### 数据收集

- PDF解析：PDFplumber、PyPDF2
- 文本提取：正则表达式、BeautifulSoup
- API接口：EDGAR API、Wind

### 数据分析

- Python：Pandas、NumPy、SciPy
- 数据库：SQLite、PostgreSQL
- 文本分析：NLTK、spaCy

### 可视化

- 图表：Matplotlib、Seaborn、Plotly
- 词云：wordcloud
- 仪表板：Streamlit、Power BI

---

## 十一、附录

### 附录A：费用类型关键词词典 v2.0

```
SG&A: ["selling", "general", "administrative", "SGA", "sales and marketing", "distribution", "G&A", "分销费用", "一般及行政"]
研发: ["research", "development", "R&D", "innovation", "product development", "研发", "产品创新"]
营销: ["marketing", "advertising", "promotion", "brand", "customer acquisition", "营销", "品牌建设"]
运营: ["operating", "operations", "operational", "facilities", "运营费用", "经营成本"]
人力: ["employee", "compensation", "headcount", "personnel", "workforce", "salary", "人力成本"]
技术: ["technology", "cloud", "software", "IT", "infrastructure", "data", "数字化", "IT"]
物流: ["logistics", "fulfillment", "shipping", "warehousing", "distribution cost", "物流", "仓储", "配送"]
数字营销: ["digital marketing", "e-commerce", "social media", "DTC", "direct-to-consumer", "电商", "数字营销", "直播"]
门店成本: ["store", "retail", "rent", "lease", "real estate", "门店", "租金", "店面"]
法律: ["legal", "compliance", "regulatory", "litigation", "settlement", "法律", "合规"]
```

### 附录B：驱动因素关键词词典 v2.0

```
业务扩张: ["growth", "expansion", "scale", "volume", "business growth", "new markets", "业务增长", "市场扩张"]
投资驱动: ["investment", "initiative", "strategic", "transformation", "venture", "project", "投资", "战略投入"]
效率提升: ["efficiency", "optimization", "automation", "productivity", "cost saving", "improved", "效率提升", "降本增效"]
DTC转型: ["DTC", "direct-to-consumer", "e-commerce", "digital channel", "owned channel", "DTC转型", "直销", "电商渠道"]
品牌建设: ["brand building", "brand investment", "brand building initiatives", "品牌建设", "品牌投入"]
产品创新: ["product innovation", "new product", "innovation", "R&D", "product development", "产品创新", "技术创新"]
供应链: ["supply chain", "logistics", "sourcing", "supplier", "procurement", "供应链", "物流"]
外部因素: ["currency", "inflation", "regulatory", "macroeconomic", "pandemic", "economic", "汇率", "通胀", "关税"]
重组整合: ["restructuring", "reorganization", "integration", "acquisition", "merger", "consolidation", "重组", "整合"]
一次性: ["one-time", "special", "impairment", "restructuring charge", "legal settlement", "settlement", "一次性", "特殊项目"]
```

### 附录C：效率指标关键词词典

```
高效: ["efficiency", "improved", "optimization", "cost reduction", "productivity", "leverage", "scale", "效率提升", "改善", "规模效应"]
低效: ["inefficiency", "cost increase", "margin pressure", "headwind", "成本上升", "压力"]
投资型: ["investment mode", "strategic investment", "building", "investing in growth", "战略性投入", "前置投入"]
```

### 附录D：分析指标定义

| 指标名称 | 定义 | 计算方法 |
|---------|------|---------|
| 费用占营收比 | 费用占营业收入的比率 | 费用金额 / 营业收入 × 100% |
| 费用增长率 | 费用同比/环比变化 | (本期费用 - 上期费用) / 上期费用 × 100% |
| 人均费用 | 费用总额 / 员工人数 | 费用金额 / 平均员工人数 |
| **费效比** | **每元费用带来的营收** | **营业收入 / 费用总额** |
| **费用效率** | **费用增速与营收增速之比** | **费用增速 / 营收增速** |
| 费用弹性 | 费用增速与营收增速之比 | 费用增速 / 营收增速 |

---

**版本**：v2.0
**更新日期**：2026-06-05
**主要更新**：
1. 新增费用类型：物流成本、数字营销、门店成本
2. 新增驱动因素：DTC转型、品牌建设、产品创新、供应链
3. 新增效率指标标注体系
4. 优化费效比分析维度
5. 扩展中英文关键词词典
**适用范围**：消费品牌及体育用品行业财报费用分析
