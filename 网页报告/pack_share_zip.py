"""打包 Section 2 分享包 (zip)
"""
import os, zipfile
from pathlib import Path

base = Path(r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\网页报告")

files = [
    "Section 2-运动品牌财务报告.html",
    "2026纺织服装行业盘点-信息图.png",
    "2025-2026Q1运动服饰&器械行业分析报告.pdf",
]

# 1. check
for src in files:
    p = base / src
    tag = "OK  " if p.exists() else "MISS"
    size = p.stat().st_size if p.exists() else 0
    print(f"  [{tag}] {src:55s} {size:>10,} bytes")

# 2. README
readme_cn = """# 国际品牌财报 v2 · 运动品牌财务报告 · 分享包

## 解压后如何打开
1. 把 3 个文件保留在同一文件夹内（不要拆开）
2. 用现代浏览器（Chrome / Edge / Safari / Firefox）双击打开:
   `Section 2-运动品牌财务报告.html`
3. 首次加载需要联网（用于加载 ECharts 图表库 CDN）

## 文件清单
| 文件 | 用途 |
|---|---|
| Section 2-运动品牌财务报告.html | 主报告（约 475 KB） |
| 2026纺织服装行业盘点-信息图.png | 第 4 章信息图缩略图（4.3 MB） |
| 2025-2026Q1运动服饰&器械行业分析报告.pdf | 第 4 章综合报告下载源文件（458 KB） |
| README.txt | 本说明文件 |

## 关键章节
- 1. 行业趋势（宏观环境）
- 2.1 品牌营收气泡图
- 2.2 重点品牌 Highlight
- 2.3 品牌盈利情况（净利率折线 · 三段背景带 · 17 品牌）
- 3. 经营费用细探（安踏 & 361度 费用结构 + 文本分析）
- 4. 综合报告下载

## 数据口径
- 数据源: 23 份原始年报 + 财务数据库 v3.1（标注日期 2026-06-07）
- 抽取方式: Python 爬虫 + 人工兜底
- 标注规则: 双重验证（费用类型 = 类型词 ∩ 费用词）
- 财年口径: FY2023 → FY2025 三大财年
  港股 / 美股 / 欧股（采用各自公司财年定义）
- 排名口径: 按 FY2024 净利率排名（不是按毛利率）

## 网络依赖（首次打开需联网）
- ECharts 5.5.0: cdn.jsdelivr.net/npm/echarts@5.5.0
- 部分数据源链接（lululemon IR / Nike 10-K / Puma / 安踏 / 361度 等）—— 点击会跳原网站

## 反馈
财务分析团队
"""
(base / "README.txt").write_text(readme_cn, encoding="utf-8")
print("  [OK  ] README.txt")

# 3. zip
out_zip = base / "国际品牌财报_v2_分享包.zip"
files_to_zip = files + ["README.txt"]

with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
    for f in files_to_zip:
        zf.write(base / f, arcname=f)

print("---")
print(f"Output:  {out_zip}")
print(f"Size:    {out_zip.stat().st_size:,} bytes ({out_zip.stat().st_size / 1024 / 1024:.2f} MB)")
print(f"Files:   {len(files_to_zip)}")
