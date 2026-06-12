# 文本标注与关键词归类 Schema 定义

**版本**: v2.0
**更新日期**: 2026-06-07

---

## 1. 标注对象与范围

- **标注范围**: 年报全文（MD&A + 财务报表附注）
- **段落定义**: 按PDF自然换行切分，最小30字符，最大500字符
- **分母标准**: 两种指数使用不同分母（见第三章）

---

## 2. 费用类型关键词定义

### 2.1 技术成本
**定义**: 与技术投入、研发、创新相关的费用讨论

关键词（中英文）:
```
技术, 科技, 数字化, 信息化, 系统, 平台, AI, 人工智能
technology, tech, digital, IT, software, cloud, data, cybersecurity
infrastructure, platform, system, automation
研发, 研究开发, 创新, innovation, research, development
技术成本, 技术费用, 技术投入, 研发投入, 创新投入, IT成本, IT费用
```

### 2.2 运营费用
**定义**: 与日常运营、设施相关的费用

关键词:
```
运营, 经营, 营业, 营业费用, 运营费用, 经营费用
operating, operations, operational, facilities
```

### 2.3 门店成本
**定义**: 与零售门店、租金、租赁相关的费用

关键词:
```
门店, 店铺, 租金, 店面, 零售, 商业地产, 专柜, 租赁
store, retail, shop, outlet, rent, lease, real estate
```

### 2.4 营销费用
**定义**: 与市场推广、广告、促销、品牌建设相关的费用

关键词:
```
营销, 市场推广, 广告, 推广, 宣传, 促销
marketing, advertising, promotion, campaign
品牌建设, 品牌投入, 品牌投资, 品牌推广, 品牌营销, 品牌活动
brand building, brand investment, brand awareness, brand equity, brand campaign
```

### 2.5 研发费用
**定义**: 与产品/技术研发直接相关的费用

关键词:
```
研发, 研究开发, 产品创新, 技术创新
research, development, R&D, innovation, new product, new technology
研发费用, 研发投入
```

### 2.6 人力成本
**定义**: 与员工薪酬、福利、人力资源相关的费用

关键词:
```
人力, 员工, 工资, 薪酬, 福利, 人力费用, 人员费用, 员工成本
employee, compensation, salary, wage, personnel, headcount, workforce, labor
```

### 2.7 数字营销
**定义**: 与电商、线上渠道、社交媒体相关的营销费用

关键词:
```
数字营销, 电商, 线上, 直播, 社交媒体
digital marketing, e-commerce, ecommerce, social media, online
DTC, direct-to-consumer, direct to consumer, 自有零售
```

### 2.8 物流成本
**定义**: 与仓储、配送、供应链相关的费用

关键词:
```
物流, 仓储, 配送, 运输, 供应链, 履约
logistics, shipping, fulfillment, delivery, warehouse, supply chain
物流成本, 仓储成本, 运输成本
```

### 2.9 SG&A费用
**定义**: 销货成本及管理费用汇总

关键词:
```
SG&A, SGA, 分销, 一般及行政, 管理费用, 销售及管理费用, 销售及管理
selling, general, administrative, g&a, distribution
```

---

## 3. 双重验证规则

### 3.1 验证逻辑

**背景**: 仅包含费用类型关键词的段落可能被误标（如"技术实力显著增强"标为"技术成本"），因此引入双重验证。

**验证条件（必须同时满足）**:

| 条件 | 说明 |
|-----|------|
| **条件1** | 段落包含上述费用类型关键词之一 |
| **条件2** | 段落同时包含费用/成本/支出/投入相关词汇 |

**条件2关键词**:
```
英文: cost, costs, expense, expenses, spending, expenditure, fee, fees, charge, charges, budget, allocation, funded, funding
中文: 投入, 投资, 支出, 花费, 耗费, 消耗, 费用, 开支, 成本, 价款, 付费
     加大, 加强, 强化, 深化, 建设, 增加, 增长, 提高, 扩充, 扩展, 配置
```

**验证函数伪代码**:
```
is_valid_expense_annotation(text, expense_type):
    has_expense_keyword = any(kw in text for kw in EXPENSE_KEYWORDS[expense_type])
    has_cost_keyword = any(kw in text for kw in COST_KEYWORDS)
    return has_expense_keyword AND has_cost_keyword
```

### 3.2 指数计算方式

| 指数 | 公式 | 含义 |
|-----|------|------|
| **v1 信息渗透度** | (有效标注数 / 总段落数) × 100 | 费用讨论在年报全文中的渗透程度 |
| **v2 讨论密度** | (有效标注数 / 含费用标注段落数) × 100 | 在费用相关讨论中的集中程度 |

---

## 4. 驱动因素关键词定义

### 4.1 外部因素
```
外部, 宏观, 经济, 汇率, 地缘, 疫情, 通胀, 利率, 市场环境, 外部环境
external, macro, economy, currency, geopolitical, pandemic, inflation, interest rate
```

### 4.2 投资驱动
```
投资, 投入, 支出, 资本支出, 资金投入, 加投
investment, invest, spending, capex, capital expenditure, funded
```

### 4.3 业务扩张
```
扩张, 增长, 成长, 规模化, 新市场, 新店, 拓展, 开店
expansion, grow, growth, scale, new market, new region, new store
```

### 4.4 DTC转型
```
DTC, 直面消费者, 直营, 自有零售, 渠道转型
DTC, direct-to-consumer, direct to consumer, owned retail, consumer direct
```

### 4.5 品牌建设
```
品牌建设, 品牌投入, 品牌投资, 品牌推广, 品牌营销, 品牌活动
brand building, brand investment, brand awareness, brand equity, brand campaign
```

### 4.6 产品创新
```
创新, 新产品, 新技术, 研发, 产品开发, 产品创新, 差异化
innovation, innovative, new product, new technology, R&D, product development
```

### 4.7 效率提升
```
效率, 提升, 优化, 降低成本, 精简, 自动化, 改善
efficiency, improve, optimization, cost reduction, streamline, automation
```

### 4.8 供应链
```
供应链, 供应商, 采购, 物流, 库存, 仓储
supply chain, supplier, sourcing, logistics, inventory, warehouse
```

---

## 5. 情感倾向判断标准

### 5.1 情感词库

**正面情感词**:
```
增长, 提升, 改善, 加强, 强化, 优化, 突破, 成功, 显著, 强劲, 稳健
increase, improve, enhance, strengthen, optimize, breakthrough, success, significant, strong, solid
```

**负面情感词**:
```
下降, 减少, 下滑, 不利, 风险, 挑战, 困难, 下降, 负增长, 压力
decrease, decline, reduce, adverse, risk, challenge, difficulty, pressure, headwind
```

**中性词**:
```
持平, 稳定, 符合预期, 与去年持平
stable, stable, in line, flat
```

### 5.2 情感判断规则

段落情感 = 该段落中情感词的加权组合：
- 正面词数 > 负面词数 → 正面
- 正面词数 < 负面词数 → 负面
- 相近或无情感词 → 中性

---

## 6. 数据来源

| 品牌 | 年报来源 | 标注文件 |
|------|---------|---------|
| Nike | Nike FY2025 10-K | nike_mda_annotations.json |
| Adidas | Adidas FY2025 Annual Report | adidas_mda_annotations.json |
| 安踏 | 安踏体育 FY2025 年报 | anta_mda_annotations.json |
| 361度 | 361度 FY2025 年报 | 361_mda_annotations.json |
| ... | ... | ... |

---

## 7. 版本历史

| 版本 | 日期 | 更新内容 |
|-----|------|---------|
| v1.0 | 2026-06-01 | 初始标注schema |
| v2.0 | 2026-06-07 | 增加双重验证规则；扩展技术成本定义（含研发/创新） |
