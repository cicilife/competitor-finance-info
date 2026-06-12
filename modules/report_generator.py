import os
import json
from datetime import datetime, timedelta
from typing import Dict, List
from .database import NewsDatabase

class ReportGenerator:
    def __init__(self, db_path: str = "data/processed/reports.db", output_dir: str = "output"):
        self.db = NewsDatabase(db_path)
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_weekly_report(self, week_start_date: datetime = None) -> str:
        if week_start_date is None:
            today = datetime.now()
            week_start_date = today - timedelta(days=today.weekday())
        
        week_end_date = week_start_date + timedelta(days=6)
        report_date_str = week_start_date.strftime("%Y%m%d")
        
        start_datetime = week_start_date.strftime("%Y-%m-%d 00:00:00")
        end_datetime = week_end_date.strftime("%Y-%m-%d 23:59:59")
        
        news_items = self.db.get_news_by_date_range(start_datetime, end_datetime)
        
        report = self._format_report(news_items, week_start_date, week_end_date)
        
        report_path = os.path.join(self.output_dir, f"weekly_report_{report_date_str}.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        
        self.db.add_weekly_report(
            report_date=week_start_date.strftime("%Y-%m-%d"),
            news_count=len(news_items),
            pdf_count=0,
            report_path=report_path
        )
        
        return report_path

    def _format_report(self, news_items: List[Dict], start_date: datetime, end_date: datetime) -> str:
        brand_categories = {
            "核心分析": ["Decathlon迪卡侬"],
            "本土竞品": ["安踏体育", "李宁", "特步国际", "361度"],
            "渠道商": ["滔搏国际", "宝胜国际"],
            "国际参考": ["NIKE耐克", "Adidas阿迪达斯", "Lululemon", "PUMA彪马"]
        }
        
        content_type_order = ["企业经营", "新品发布", "市场推广", "渠道策略", "其他"]
        
        report = []
        report.append(f"# 迪卡侬竞品资讯周报")
        report.append(f"\n**报告周期**: {start_date.strftime('%Y年%m月%d日')} - {end_date.strftime('%Y年%m月%d日')}")
        report.append(f"**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
        report.append(f"**资讯总数**: {len(news_items)} 条")
        
        for category_name, brands in brand_categories.items():
            category_news = [item for item in news_items if item["brand_name"] in brands]
            if not category_news:
                continue
            
            report.append(f"\n---\n")
            report.append(f"## {category_name}")
            
            for brand in brands:
                brand_news = [item for item in category_news if item["brand_name"] == brand]
                if not brand_news:
                    continue
                
                report.append(f"\n### {brand}")
                
                for content_type in content_type_order:
                    type_news = [item for item in brand_news if item["content_type"] == content_type]
                    if not type_news:
                        continue
                    
                    report.append(f"\n#### {content_type}")
                    for news in type_news:
                        publish_date = news["publish_date"] if news["publish_date"] else news["crawl_date"]
                        report.append(f"- **[{news['title']}]({news['url']})**")
                        if news["summary"]:
                            report.append(f"  > {news['summary'][:100]}...")
                        report.append(f"  *来源: {news['source']} | {publish_date}*")
        
        if news_items:
            report.append(f"\n---\n")
            report.append("## 重点资讯摘要")
            
            important_keywords = ["业绩", "财报", "新品", "战略", "合作", "开店", "关店"]
            important_news = [
                item for item in news_items 
                if any(keyword in item["title"] for keyword in important_keywords)
            ][:5]
            
            for news in important_news:
                report.append(f"- **{news['brand_name']}**: {news['title']}")
        
        report.append(f"\n---\n")
        report.append("*报告由系统自动生成*")
        
        return "\n".join(report)

    def generate_summary_report(self, days: int = 30) -> str:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        news_items = self.db.get_news_by_date_range(
            start_date.strftime("%Y-%m-%d 00:00:00"),
            end_date.strftime("%Y-%m-%d 23:59:59")
        )
        
        summary = {
            "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            "total_news": len(news_items),
            "by_brand": {},
            "by_type": {},
            "top_sources": {}
        }
        
        for news in news_items:
            brand = news["brand_name"] or "未知"
            content_type = news["content_type"] or "其他"
            source = news["source"] or "未知"
            
            summary["by_brand"][brand] = summary["by_brand"].get(brand, 0) + 1
            summary["by_type"][content_type] = summary["by_type"].get(content_type, 0) + 1
            summary["top_sources"][source] = summary["top_sources"].get(source, 0) + 1
        
        summary_path = os.path.join(self.output_dir, f"summary_{end_date.strftime('%Y%m%d')}.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        return summary_path

    def close(self):
        self.db.close()