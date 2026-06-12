import os
import json
import logging
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
from .crawler import NewsCrawler
from .database import NewsDatabase

logger = logging.getLogger(__name__)

class NewsCollector:
    def __init__(self, db_path: str = "data/processed/reports.db"):
        self.db = NewsDatabase(db_path)
        self.crawler = NewsCrawler()
        self.news_sources = []

    def load_sources(self, config_path: str = "config/sources.yaml"):
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            self.news_sources = config.get("news_sources", [])
            self.search_keywords = config.get("search_keywords", {})

    def fetch_rss_feed(self, rss_url: str) -> List[Dict]:
        try:
            feed = feedparser.parse(rss_url)
            items = []
            for entry in feed.entries:
                item = {
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "summary": entry.get("summary", ""),
                    "published": entry.get("published", ""),
                    "content": entry.get("content", "")
                }
                items.append(item)
            return items
        except Exception as e:
            logger.error(f"Failed to fetch RSS feed {rss_url}: {str(e)[:50]}")
            return []

    def search_keywords_in_text(self, text: str, keywords: List[str]) -> bool:
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)

    def process_rss_news(self, source_name: str, news_items: List[Dict]) -> int:
        count = 0
        brand_keywords = ["迪卡侬", "安踏", "李宁", "特步", "361度", "滔搏", "宝胜", "耐克", "阿迪达斯", "Lululemon", "PUMA"]
        
        for item in news_items:
            title = item.get("title", "")
            url = item.get("url", "")
            
            if not url or not title:
                continue
            
            if self.db.url_exists(url):
                continue
            
            matched_brand = None
            for brand in brand_keywords:
                if brand in title or brand in (item.get("summary", "") or ""):
                    matched_brand = brand
                    break
            
            if matched_brand or self.search_keywords_in_text(title, ["运动品牌", "体育用品"]):
                try:
                    summary = item.get("summary", "")[:200]
                    content = item.get("content", "")
                    if isinstance(content, list):
                        content = content[0].get("value", "") if content else ""
                    
                    tags = self.crawler.classify_content(title + " " + summary)
                    
                    self.db.add_news_item(
                        title=title,
                        url=url,
                        source=source_name,
                        brand_name=matched_brand,
                        content=content[:5000],
                        content_type=tags[0] if tags else "其他",
                        publish_date=item.get("published", ""),
                        summary=summary,
                        tags=tags
                    )
                    count += 1
                except Exception as e:
                    logger.error(f"Failed to process news {url}: {str(e)[:50]}")
        
        return count

    def crawl_brand_news(self, brand_name: str, news_url: str) -> int:
        count = 0
        try:
            html = self.crawler.get_html(news_url)
            news_items = self.crawler.extract_links(html, news_url)
            
            for item in news_items:
                url = item["url"]
                title = item["text"]
                
                if self.db.url_exists(url):
                    continue
                
                try:
                    article_html = self.crawler.get_html(url)
                    parsed = self.crawler.parse_news_page(article_html, url)
                    
                    self.db.add_news_item(
                        title=parsed["title"],
                        url=url,
                        source=brand_name + "官网",
                        brand_name=brand_name,
                        content=parsed["content"],
                        content_type=parsed["tags"][0] if parsed["tags"] else "其他",
                        publish_date=parsed["publish_date"],
                        summary=parsed["summary"],
                        tags=parsed["tags"]
                    )
                    count += 1
                except Exception as e:
                    logger.error(f"Failed to crawl {url}: {str(e)[:50]}")
        
        except Exception as e:
            logger.error(f"Failed to crawl {news_url}: {str(e)[:50]}")
        
        return count

    def run(self, crawl_rss: bool = True, crawl_brand_sites: bool = True) -> Dict:
        results = {
            "rss_items": 0,
            "brand_items": 0,
            "sources_crawled": 0,
            "errors": []
        }
        
        if crawl_rss:
            for source in self.news_sources:
                if "rss" in source:
                    logger.info(f"Crawling RSS feed: {source['name']}")
                    try:
                        news_items = self.fetch_rss_feed(source["rss"])
                        count = self.process_rss_news(source["name"], news_items)
                        results["rss_items"] += count
                        results["sources_crawled"] += 1
                        logger.info(f"Found {count} news items from {source['name']}")
                    except Exception as e:
                        logger.error(f"Failed to crawl {source['name']}: {str(e)[:50]}")
                        results["errors"].append(f"{source['name']}: {str(e)[:50]}")
        
        if crawl_brand_sites:
            brands = self.db.get_brands()
            for brand in brands:
                logger.info(f"Crawling news for brand: {brand['name']}")
        
        return results

    def get_weekly_news(self, days: int = 7) -> List[Dict]:
        end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        return self.db.get_news_by_date_range(start_date, end_date)

    def close(self):
        self.db.close()