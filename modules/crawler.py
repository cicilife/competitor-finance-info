import os
import re
import time
import random
import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from requests.utils import requote_uri
from urllib.parse import urljoin, urlparse
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

class BaseCrawler:
    def __init__(self, user_agent: str = None, timeout: int = 30, max_retries: int = 3, delay: float = 2.0):
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        self.timeout = timeout
        self.max_retries = max_retries
        self.delay = delay
        self.session = self._build_session()

    def _build_session(self):
        session = requests.Session()
        retry_strategy = Retry(
            total=self.max_retries,
            connect=self.max_retries,
            read=self.max_retries,
            redirect=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers.update({"User-Agent": self.user_agent})
        return session

    def safe_url(self, url: str) -> str:
        return requote_uri(url)

    def get_html(self, url: str, use_playwright: bool = False) -> str:
        url = self.safe_url(url)
        if not use_playwright:
            for attempt in range(self.max_retries):
                try:
                    response = self.session.get(url, timeout=self.timeout)
                    response.raise_for_status()
                    time.sleep(random.uniform(self.delay, self.delay * 1.5))
                    return response.text
                except Exception as e:
                    logger.warning(f"Request attempt {attempt + 1} failed for {url}: {str(e)[:50]}")
                    time.sleep(random.uniform(2, 4))
        
        for attempt in range(self.max_retries):
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    context = browser.new_context(user_agent=self.user_agent)
                    page = context.new_page()
                    page.goto(url, timeout=60000, wait_until="networkidle")
                    page.wait_for_timeout(3000)
                    html = page.content()
                    browser.close()
                    time.sleep(random.uniform(self.delay, self.delay * 1.5))
                    return html
            except Exception as e:
                logger.warning(f"Playwright attempt {attempt + 1} failed for {url}: {str(e)[:50]}")
                time.sleep(random.uniform(3, 5))
        
        raise Exception(f"Failed to get {url} after {self.max_retries} attempts")

    def extract_links(self, html: str, base_url: str, pattern: str = None) -> list:
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full_url = urljoin(base_url, href)
            if pattern and not re.search(pattern, full_url, re.IGNORECASE):
                continue
            links.append({"url": full_url, "text": a.get_text(strip=True)})
        return links

    def download_file(self, url: str, save_path: str) -> bool:
        url = self.safe_url(url)
        try:
            response = self.session.get(url, stream=True, timeout=self.timeout)
            response.raise_for_status()
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            time.sleep(random.uniform(self.delay, self.delay * 1.5))
            return True
        except Exception as e:
            logger.error(f"Failed to download {url}: {str(e)[:50]}")
            return False

class NewsCrawler(BaseCrawler):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content_keywords = {
            "企业经营": ["业绩", "财报", "营收", "利润", "净利润", "亏损", "盈利", "投资者关系"],
            "新品发布": ["新品", "发布", "上市", "新系列", "联名款", "限量版"],
            "市场推广": ["营销", "广告", "赞助", "合作", "活动", "赛事", "代言人"],
            "渠道策略": ["门店", "开店", "关店", "电商", "线上", "线下", "渠道", "新零售"]
        }

    def classify_content(self, text: str) -> list:
        text_lower = text.lower()
        categories = []
        for category, keywords in self.content_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                categories.append(category)
        return categories if categories else ["其他"]

    def parse_news_page(self, html: str, url: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.get_text(strip=True) if soup.title else ""
        
        content = ""
        for tag in soup.find_all(["p", "article", "div"]):
            if tag.get("class"):
                if any(cls in ["content", "article-content", "post-content", "main-content"] for cls in tag.get("class")):
                    content = tag.get_text(separator="\n", strip=True)
                    break
        if not content:
            content = soup.get_text(separator="\n", strip=True)[:5000]
        
        publish_date = ""
        for pattern in [r"\d{4}-\d{2}-\d{2}", r"\d{4}年\d{1,2}月\d{1,2}日"]:
            match = re.search(pattern, html)
            if match:
                publish_date = match.group()
                break
        
        summary = content[:200] if len(content) > 200 else content
        
        return {
            "title": title,
            "url": url,
            "content": content,
            "publish_date": publish_date,
            "summary": summary,
            "tags": self.classify_content(title + " " + content)
        }

class PDFCrawler(BaseCrawler):
    def __init__(self, save_dir: str = "data/raw/pdf", **kwargs):
        super().__init__(**kwargs)
        self.save_dir = save_dir
        self.fin_keywords = ["年报", "季报", "财报", "财务", "业绩", "公告", "新闻稿", "投资者", "IR", "Annual", "Quarter", "Earnings"]

    def extract_pdf_links(self, html: str, base_url: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        pdf_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full_url = urljoin(base_url, href)
            if full_url.lower().endswith(".pdf"):
                text = a.get_text(strip=True)
                if any(keyword.lower() in text.lower() or keyword.lower() in full_url.lower() for keyword in self.fin_keywords):
                    pdf_links.append({"url": full_url, "text": text})
        return pdf_links

    def extract_report_metadata(self, text: str, pdf_url: str) -> tuple:
        text_lower = (text or "").lower()
        year = None
        quarter = None

        year_match = re.search(r"(20\d{2}|19\d{2})", text_lower)
        if year_match:
            year = year_match.group(1)
        else:
            url_year = re.search(r"(20\d{2}|19\d{2})", pdf_url)
            year = url_year.group(1) if url_year else None

        quarter_patterns = [
            (r"q([1-4])", lambda m: f"Q{m.group(1)}"),
            (r"第([一二三四])季度", lambda m: f"Q{['一', '二', '三', '四'].index(m.group(1)) + 1}"),
            (r"(first|1st)\s+quarter", lambda m: "Q1"),
            (r"(second|2nd)\s+quarter", lambda m: "Q2"),
            (r"(third|3rd)\s+quarter", lambda m: "Q3"),
            (r"(fourth|4th)\s+quarter", lambda m: "Q4"),
        ]
        for pattern, formatter in quarter_patterns:
            match = re.search(pattern, text_lower)
            if match:
                quarter = formatter(match)
                break

        if not quarter:
            url_lower = pdf_url.lower()
            for pattern, formatter in quarter_patterns:
                match = re.search(pattern, url_lower)
                if match:
                    quarter = formatter(match)
                    break

        if not quarter and ("annual" in text_lower or "年报" in text_lower):
            quarter = "年报"
        if not quarter and ("quarter" in text_lower or "季报" in text_lower):
            quarter = "季报"

        return year, quarter

    def format_filename(self, title: str, pdf_url: str) -> str:
        title = title.strip() if title else os.path.basename(urlparse(pdf_url).path) or "document"
        year, quarter = self.extract_report_metadata(title, pdf_url)
        safe_title = re.sub(r'[\\/:*?"<>|]', "", title)
        name_parts = []
        if year and year not in safe_title:
            name_parts.append(year)
        if quarter and quarter not in safe_title:
            name_parts.append(quarter)
        name_parts.append(safe_title)
        return " ".join(part for part in name_parts if part).strip() + ".pdf"

    def download_pdfs(self, brand: str, pdf_links: list) -> list:
        downloaded = []
        for link in pdf_links:
            filename = self.format_filename(link["text"], link["url"])
            save_path = os.path.join(self.save_dir, brand, filename)
            
            if os.path.exists(save_path):
                logger.info(f"Already exists: {save_path}")
                continue
            
            logger.info(f"Downloading: {link['url']}")
            if self.download_file(link["url"], save_path):
                year, quarter = self.extract_report_metadata(link["text"], link["url"])
                downloaded.append({
                    "filename": filename,
                    "file_path": save_path,
                    "url": link["url"],
                    "year": year,
                    "quarter": quarter,
                    "title": link["text"]
                })
        
        return downloaded