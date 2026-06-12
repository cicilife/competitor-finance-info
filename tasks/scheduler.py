import os
import sys
import time
import logging
import schedule
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger("scheduler")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/scheduler.log", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

def run_weekly_update():
    logger.info("Running scheduled weekly update...")
    try:
        from tasks.weekly_update import main
        main()
        logger.info("Weekly update completed successfully")
    except Exception as e:
        logger.error(f"Weekly update failed: {str(e)[:100]}")

def start_scheduler():
    logger.info("Starting scheduler...")
    
    schedule.every().monday.at("02:00").do(run_weekly_update)
    
    logger.info("Scheduler started. Next run: Monday at 02:00")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

def run_once():
    logger.info("Running one-time update...")
    run_weekly_update()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Competitor News Scheduler")
    parser.add_argument("--run-once", action="store_true", help="Run once and exit")
    args = parser.parse_args()
    
    if args.run_once:
        run_once()
    else:
        start_scheduler()