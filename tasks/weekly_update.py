import os
import sys
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.database import NewsDatabase
from modules.crawler import PDFCrawler
from modules.news_collector import NewsCollector
from modules.report_generator import ReportGenerator

logger = logging.getLogger("weekly_update")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/weekly_update.log", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

def load_brands_to_db(db: NewsDatabase, config_path: str = "config/brands.yaml"):
    import yaml
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    for brand in config["brands"]:
        db.add_brand(
            name=brand["name"],
            english_name=brand.get("english_name"),
            category=brand.get("category"),
            focus=brand.get("focus")
        )
    logger.info(f"Loaded {len(config['brands'])} brands to database")

def crawl_financial_pdfs():
    logger.info("Starting PDF crawl...")
    db = NewsDatabase()
    pdf_crawler = PDFCrawler(save_dir="data/raw/pdf")
    
    brands = db.get_brands()
    for brand in brands:
        brand_name = brand["name"]
        logger.info(f"Crawling PDFs for {brand_name}")
        
        import yaml
        with open("config/brands.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
        brand_config = next((b for b in config["brands"] if b["name"] == brand_name), None)
        if not brand_config:
            continue
        
        for source in brand_config.get("sources", []):
            if source["type"] == "ir":
                try:
                    logger.info(f"Fetching IR page: {source['url']}")
                    html = pdf_crawler.get_html(source["url"])
                    pdf_links = pdf_crawler.extract_pdf_links(html, source["url"])
                    
                    downloaded = pdf_crawler.download_pdfs(brand_name, pdf_links)
                    for item in downloaded:
                        db.add_pdf_report(
                            brand_name=brand_name,
                            filename=item["filename"],
                            file_path=item["file_path"],
                            report_type="年报" if item["quarter"] == "年报" else "季报",
                            year=item["year"],
                            quarter=item["quarter"]
                        )
                    logger.info(f"Downloaded {len(downloaded)} PDFs for {brand_name}")
                except Exception as e:
                    logger.error(f"Failed to crawl {brand_name}: {str(e)[:100]}")
    
    db.close()
    logger.info("PDF crawl completed")

def crawl_news():
    logger.info("Starting news crawl...")
    collector = NewsCollector()
    collector.load_sources()
    
    load_brands_to_db(collector.db)
    
    results = collector.run(crawl_rss=True, crawl_brand_sites=False)
    logger.info(f"News crawl completed: {results['rss_items']} items from {results['sources_crawled']} sources")
    
    if results["errors"]:
        logger.warning(f"Errors occurred: {', '.join(results['errors'])}")
    
    collector.close()

def generate_report():
    logger.info("Generating weekly report...")
    generator = ReportGenerator()
    report_path = generator.generate_weekly_report()
    logger.info(f"Report generated: {report_path}")
    generator.close()

def main():
    logger.info("="*60)
    logger.info(f"Weekly update started at {datetime.now()}")
    logger.info("="*60)
    
    try:
        crawl_news()
    except Exception as e:
        logger.error(f"News crawl failed: {str(e)[:100]}")
    
    try:
        crawl_financial_pdfs()
    except Exception as e:
        logger.error(f"PDF crawl failed: {str(e)[:100]}")
    
    try:
        generate_report()
    except Exception as e:
        logger.error(f"Report generation failed: {str(e)[:100]}")
    
    logger.info("="*60)
    logger.info(f"Weekly update completed at {datetime.now()}")
    logger.info("="*60)

if __name__ == "__main__":
    main()