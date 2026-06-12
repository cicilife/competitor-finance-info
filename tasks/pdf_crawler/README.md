# 财报PDF爬虫使用说明

## 📁 项目结构

```
tasks/pdf_crawler/
├── __init__.py              # Python包初始化
├── crawler.py               # 核心爬虫模块
├── main.py                  # 命令行入口
├── data_sources.yaml        # 数据源配置（多数据源）
├── brands_config.yaml       # 品牌配置（含股票代码）
└── README.md                # 本文档
```

## 🚀 快速开始

### 1. 查看配置的品牌列表
```bash
python tasks/pdf_crawler/main.py --list
```

### 2. 检查已下载的PDF
```bash
python tasks/pdf_crawler/main.py --check
```

### 3. 爬取单个品牌的财报
```bash
python tasks/pdf_crawler/main.py --brand 安踏体育
```

### 4. 爬取所有品牌的财报
```bash
python tasks/pdf_crawler/main.py
```

## 📊 数据源

### 支持的数据源

| 数据源类型 | 说明 | 优先级 |
|-----------|------|--------|
| 官方IR页面 | 各公司投资者关系官网 | 高 |
| 巨潮资讯 | 中国上市公司财报公告 | 高 |
| 东方财富 | 财经综合平台 | 中 |
| 雪球 | 投资社区 | 中 |
| 百度/必应搜索 | 搜索引擎 | 低 |

### 配置的数据源

```yaml
# 官方IR
- 安踏体育: https://ir.anta.com
- 李宁: https://ir.lining.com.hk
- 特步国际: https://ir.xtep.com
- 361度: https://ir.361sport.com
- 滔搏国际: https://ir.topsports.com.hk
- 宝胜国际: https://ir.pou-sheng.com
- NIKE: https://investor.nike.com
- Adidas: https://www.adidas-group.com/en/investors
- Lululemon: https://investor.lululemon.com
- PUMA: https://www.pumagroup.com/investor-relations

# 财经平台
- 巨潮资讯 (cninfo.com.cn)
- 东方财富 (eastmoney.com)
- 雪球 (xueqiu.com)
```

## 📂 存储结构

所有PDF文件存储在 `竞品财务PDF库/` 目录下，按品牌分子文件夹：

```
竞品财务PDF库/
├── 安踏体育/
│   ├── 安踏体育_2025_年报_财务报告.pdf
│   ├── 安踏体育_2026_Q1季报_投资者简报.pdf
│   └── ...
├── 李宁/
│   ├── 李宁_2025_年报_财务报告.pdf
│   └── ...
├── 特步国际/
│   └── ...
└── ...
```

### 文件命名规则

```
{品牌名}_{年份}_{报告期}_{报告性质}.pdf

示例：
- 安踏体育_2025_年报_财务报告.pdf
- 安踏体育_2026_Q1季报_投资者简报.pdf
- 李宁_2025_年报_英文版.pdf
```

## ⚙️ 配置说明

### brands_config.yaml - 品牌配置

```yaml
brands:
  - name: 安踏体育
    english_name: ANTA Sports
    stock_codes:
      hk: "02020"        # 港股代码
      us: ""              # 美股代码
    keywords:
      - 安踏
      - ANTA Sports
    official_ir: "https://ir.anta.com"
```

### data_sources.yaml - 数据源配置

```yaml
crawler:
  max_retries: 3         # 最大重试次数
  timeout: 30             # 请求超时（秒）
  delay: 2               # 请求间隔（秒）
  verify_ssl: false      # 是否验证SSL证书

storage:
  root_dir: "竞品财务PDF库"  # 存储根目录
```

## 🔧 高级用法

### 修改品牌配置

编辑 `brands_config.yaml` 添加新品牌：

```yaml
brands:
  - name: 新品牌名称
    english_name: New Brand
    stock_codes:
      hk: "港股代码"
      us: "美股代码"
    keywords:
      - 关键词1
      - 关键词2
    official_ir: "IR页面URL"
```

### 添加数据源

编辑 `data_sources.yaml` 添加新的财经平台或搜索源。

## ⚠️ 注意事项

1. **官方IR网站限制**：部分官方IR网站需要登录或有人机验证
2. **版权问题**：财报PDF仅供内部研究使用，请遵守相关版权法规
3. **请求频率**：已配置合理的请求间隔，避免对目标网站造成压力
4. **SSL证书**：部分网站证书问题，已配置跳过验证

## 💡 手动获取财报的建议

如果自动爬取失败，可以手动从以下渠道获取财报：

### 中国公司
1. **巨潮资讯** (cninfo.com.cn) - 最权威的中国上市公司公告
2. **东方财富** (eastmoney.com) - 财务数据全
3. **新浪财经** (finance.sina.com.cn) - 股票数据

### 国际公司
1. **NIKE Investor Relations** - investor.nike.com
2. **Adidas Investor Relations** - adidas-group.com/en/investors
3. **Lululemon Investor Relations** - investor.lululemon.com

### 下载后存放
将手动下载的PDF文件放入对应品牌文件夹即可，命名遵循规则：
```
{品牌名}_{年份}_{报告期}.pdf
```

## 📈 下一步

获取PDF后，使用财务数据提取功能：
```bash
python main.py --extract-financial
```

这将自动从PDF中提取财务数据并生成Excel报表。