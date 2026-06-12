import os
import sys
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/main.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("main")

def load_config():
    import yaml
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def init_database():
    from modules.database import NewsDatabase
    db = NewsDatabase()
    
    import yaml
    with open("config/brands.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    for brand in config["brands"]:
        db.add_brand(
            name=brand["name"],
            english_name=brand.get("english_name"),
            category=brand.get("category"),
            focus=brand.get("focus")
        )
    db.close()
    logger.info("Database initialized with brands")

def crawl_financial_pdfs():
    logger.info("Starting financial PDF crawl...")
    from modules.database import NewsDatabase
    from modules.crawler import PDFCrawler
    
    db = NewsDatabase()
    pdf_crawler = PDFCrawler(save_dir="data/raw/pdf")
    
    import yaml
    with open("config/brands.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    for brand in config["brands"]:
        brand_name = brand["name"]
        logger.info(f"Processing: {brand_name}")
        
        for source in brand.get("sources", []):
            if source["type"] == "ir":
                try:
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
                    logger.info(f"Downloaded {len(downloaded)} PDFs")
                except Exception as e:
                    logger.error(f"Failed to crawl {brand_name}: {str(e)[:50]}")
    
    db.close()

def crawl_news():
    logger.info("Starting news crawl...")
    from modules.news_collector import NewsCollector
    
    collector = NewsCollector()
    collector.load_sources()
    results = collector.run(crawl_rss=True, crawl_brand_sites=False)
    logger.info(f"News crawl completed: {results['rss_items']} items")
    collector.close()

def generate_report():
    logger.info("Generating weekly report...")
    from modules.report_generator import ReportGenerator
    
    generator = ReportGenerator()
    report_path = generator.generate_weekly_report()
    logger.info(f"Report generated: {report_path}")
    generator.close()

def extract_financial_data():
    logger.info("Extracting financial data from PDFs (V2)...")
    from modules.financial_processor_v2 import FinancialProcessorV2
    from modules.excel_exporter_v2 import ExcelExporterV2
    from modules.database import NewsDatabase
    
    processor = FinancialProcessorV2()
    
    pdf_dirs = ["data/raw/pdf", "竞品财务PDF库", "docs"]
    
    all_data = []
    for pdf_dir in pdf_dirs:
        if os.path.exists(pdf_dir):
            if pdf_dir == "docs":
                docs_data = processor.process_all_pdfs_flat(pdf_dir, "安踏体育")
                all_data.extend(docs_data)
            else:
                data_list = processor.process_all_pdfs(pdf_dir)
                all_data.extend(data_list)
    
    aligned_data = processor.align_periods(all_data)
    
    logger.info(f"Extracted financial data from {len(aligned_data)} PDFs")
    
    db = NewsDatabase()
    brands = db.get_brands()
    db.close()
    
    exporter = ExcelExporterV2()
    output_path = f"data/processed/financial_data_{datetime.now().strftime('%Y%m%d')}.xlsx"
    exporter.export_to_excel(aligned_data, output_path, brands)
    
    logger.info(f"Financial data exported to: {output_path}")
    
    return output_path

def generate_news_brief():
    logger.info("Generating news brief...")
    from modules.news_brief import NewsBriefGenerator
    from modules.database import NewsDatabase
    
    db = NewsDatabase()
    news_list = db.get_latest_news(limit=1000)
    db.close()
    
    generator = NewsBriefGenerator()
    brief_path = generator.generate_detailed_report(news_list)
    
    logger.info(f"News brief generated: {brief_path}")
    
    return brief_path

def show_stats():
    from modules.database import NewsDatabase
    
    db = NewsDatabase()
    
    news_count = len(db.get_latest_news(limit=10000))
    pdf_count = len(db.get_pdf_reports())
    brands = db.get_brands()
    
    print("\n" + "="*50)
    print("项目统计信息")
    print("="*50)
    print(f"品牌数量: {len(brands)}")
    print(f"新闻资讯: {news_count} 条")
    print(f"PDF报告: {pdf_count} 份")
    print("\n品牌列表:")
    for brand in brands:
        print(f"  - {brand['name']} ({brand['category']})")
    
    db.close()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="迪卡侬竞品资讯收集系统")
    parser.add_argument("--init", action="store_true", help="初始化数据库")
    parser.add_argument("--crawl-pdf", action="store_true", help="抓取财务PDF")
    parser.add_argument("--crawl-news", action="store_true", help="抓取新闻资讯")
    parser.add_argument("--generate-report", action="store_true", help="生成周度报告")
    parser.add_argument("--update", action="store_true", help="执行完整更新流程")
    parser.add_argument("--stats", action="store_true", help="显示统计信息")
    parser.add_argument("--schedule", action="store_true", help="启动定时任务")
    parser.add_argument("--extract-financial", action="store_true", help="提取财务数据并导出Excel")
    parser.add_argument("--generate-brief", action="store_true", help="生成新闻简报")
    parser.add_argument("--full-report", action="store_true", help="生成完整报告（财务数据+新闻简报）")
    
    args = parser.parse_args()
    
    if args.init:
        init_database()
    
    if args.crawl_pdf:
        crawl_financial_pdfs()
    
    if args.crawl_news:
        crawl_news()
    
    if args.generate_report:
        generate_report()
    
    if args.extract_financial:
        extract_financial_data()
    
    if args.generate_brief:
        generate_news_brief()
    
    if args.full_report:
        extract_financial_data()
        generate_news_brief()
    
    if args.update:
        init_database()
        crawl_news()
        crawl_financial_pdfs()
        generate_report()
    
    if args.stats:
        show_stats()
    
    if args.schedule:
        from tasks.scheduler import start_scheduler
        start_scheduler()
    
    if not any([args.init, args.crawl_pdf, args.crawl_news, args.generate_report, args.update, args.stats, args.schedule, args.extract_financial, args.generate_brief, args.full_report]):
        parser.print_help()

if __name__ == "__main__":
    main()