import os
import re
import time
import random
import logging
import requests
import yaml
import ssl
from urllib.parse import urljoin, quote
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

logger = logging.getLogger(__name__)

class PDFCrawlerV2:
    def __init__(self, config_path: str = None):
        self.config = self.load_config(config_path)
        self.session = self.create_session()
        self.storage_root = self.config.get('storage', {}).get('root_dir', '竞品财务PDF库')
        self.verify_ssl = self.config.get('crawler', {}).get('verify_ssl', False)

    def load_config(self, config_path: str) -> dict:
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'data_sources.yaml')

        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def create_session(self):
        session = requests.Session()
        session.headers.update({
            'User-Agent': self.config.get('crawler', {}).get('user_agent',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        return session

    def safe_filename(self, filename: str) -> str:
        illegal_chars = r'[\\/:*?"<>|]'
        return re.sub(illegal_chars, '_', filename).strip()

    def generate_filename(self, brand_name: str, year: str, period_type: str, report_nature: str = "财务报告") -> str:
        parts = [brand_name, year, period_type, report_nature]
        filename = "_".join(str(p) for p in parts if p)
        return self.safe_filename(filename) + ".pdf"

    def create_brand_dir(self, brand_name: str) -> str:
        brand_dir = os.path.join(self.storage_root, brand_name)
        os.makedirs(brand_dir, exist_ok=True)
        return brand_dir

    def is_pdf_valid(self, file_path: str) -> bool:
        if not os.path.exists(file_path):
            return False

        min_size = self.config.get('crawler', {}).get('quality', {}).get('min_file_size', 10240)
        if os.path.getsize(file_path) < min_size:
            return False

        if self.config.get('crawler', {}).get('quality', {}).get('verify_pdf_header', True):
            try:
                with open(file_path, 'rb') as f:
                    header = f.read(5)
                    return header.startswith(b'%PDF')
            except:
                return False

        return True

    def download_pdf(self, url: str, save_path: str, brand_name: str) -> dict:
        result = {
            'url': url,
            'save_path': save_path,
            'brand': brand_name,
            'success': False,
            'error': None,
            'filename': os.path.basename(save_path)
        }

        if os.path.exists(save_path) and self.is_pdf_valid(save_path):
            logger.info(f"文件已存在且有效: {save_path}")
            result['success'] = True
            result['skipped'] = True
            return result

        try:
            max_retries = self.config.get('crawler', {}).get('max_retries', 3)
            timeout = self.config.get('crawler', {}).get('timeout', 30)

            for attempt in range(max_retries):
                try:
                    response = self.session.get(url, timeout=timeout, stream=True, verify=self.verify_ssl)
                    response.raise_for_status()

                    max_size = self.config.get('crawler', {}).get('download', {}).get('max_file_size', 52428800)
                    content_length = response.headers.get('content-length')
                    if content_length and int(content_length) > max_size:
                        result['error'] = f"文件过大: {content_length} bytes"
                        return result

                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    chunk_size = self.config.get('crawler', {}).get('download', {}).get('chunk_size', 8192)

                    with open(save_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)

                    if self.is_pdf_valid(save_path):
                        result['success'] = True
                        logger.info(f"下载成功: {save_path}")
                        return result
                    else:
                        result['error'] = "PDF验证失败"
                        if os.path.exists(save_path):
                            os.remove(save_path)

                except Exception as e:
                    if attempt < max_retries - 1:
                        delay = self.config.get('crawler', {}).get('delay', 2) * (attempt + 1)
                        time.sleep(delay)
                    else:
                        result['error'] = str(e)

        except Exception as e:
            result['error'] = str(e)

        return result

    def search_official_ir(self, brand_name: str, ir_url: str) -> list:
        pdf_links = []

        try:
            logger.info(f"搜索官方IR: {brand_name} - {ir_url}")
            response = self.session.get(ir_url, timeout=30, verify=self.verify_ssl)
            response.raise_for_status()

            html = response.text

            pdf_pattern = r'href=["\']([^"\']+\.pdf[^"\']*)["\']'
            for match in re.finditer(pdf_pattern, html, re.IGNORECASE):
                pdf_url = match.group(1)
                full_url = urljoin(ir_url, pdf_url)
                if full_url not in pdf_links:
                    pdf_links.append(full_url)

            financial_keywords = ['annual', 'quarter', 'report', 'financial', 'earnings',
                                 '年报', '季报', '财报', '业绩', '投资者']

            link_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>'
            for match in re.finditer(link_pattern, html, re.IGNORECASE):
                url = match.group(1)
                text = match.group(2)

                if any(kw.lower() in url.lower() or kw in text for kw in financial_keywords):
                    full_url = urljoin(ir_url, url)
                    if full_url not in pdf_links and full_url.lower().endswith('.pdf'):
                        pdf_links.append(full_url)

            logger.info(f"找到 {len(pdf_links)} 个PDF链接")

        except Exception as e:
            logger.error(f"搜索官方IR失败: {brand_name} - {str(e)}")

        return pdf_links

    def search_eastmoney(self, brand_name: str, stock_code: str = None) -> list:
        pdf_links = []

        try:
            if not stock_code:
                return pdf_links

            search_url = f"https://so.eastmoney.com/StockSearch/search?searchkey={quote(brand_name)}&mType=14"

            response = self.session.get(search_url, timeout=30, verify=self.verify_ssl)
            if response.status_code == 200:
                data = response.json()
                if data.get('Result'):
                    for item in data['Result'][:5]:
                        report_url = item.get('PdfUrl', '')
                        if report_url and report_url.endswith('.pdf'):
                            pdf_links.append(report_url)

            logger.info(f"东方财富找到 {len(pdf_links)} 个PDF")

        except Exception as e:
            logger.error(f"搜索东方财富失败: {brand_name} - {str(e)}")

        return pdf_links

    def search_cninfo(self, brand_name: str) -> list:
        pdf_links = []

        try:
            search_url = "http://www.cninfo.com.cn/new/fulltextSearch/full"
            data = {
                'searchkey': brand_name,
                'sdate': '',
                'edate': '',
                'isfulltext': 'false',
                'sortName': 'nothing',
                'sortType': 'desc',
                'pageNum': '1'
            }

            response = self.session.post(search_url, data=data, timeout=30, verify=self.verify_ssl)
            if response.status_code == 200:
                result = response.json()
                for item in result.get('announcements', [])[:10]:
                    adjunct_url = item.get('adjunctUrl', '')
                    if adjunct_url and adjunct_url.endswith('.pdf'):
                        full_url = 'http://www.cninfo.com.cn' + adjunct_url
                        pdf_links.append(full_url)

            logger.info(f"巨潮资讯找到 {len(pdf_links)} 个PDF")

        except Exception as e:
            logger.error(f"搜索巨潮资讯失败: {brand_name} - {str(e)}")

        return pdf_links

    def extract_year_from_url(self, url: str, text: str = "") -> str:
        combined_text = url + " " + text

        year_match = re.search(r'(20[12][0-9])', combined_text)
        if year_match:
            return year_match.group(1)

        return str(datetime.now().year)

    def extract_period_from_url(self, url: str, text: str = "") -> str:
        combined_text = url + " " + text

        if 'annual' in combined_text.lower() or '年报' in combined_text:
            return '年报'

        quarter_match = re.search(r'Q([1-4])', combined_text, re.IGNORECASE)
        if quarter_match:
            return f"Q{quarter_match.group(1)}季报"

        if 'q1' in combined_text.lower() or '第一季度' in combined_text:
            return 'Q1季报'
        if 'q2' in combined_text.lower() or '第二季度' in combined_text:
            return 'Q2季报'
        if 'q3' in combined_text.lower() or '第三季度' in combined_text:
            return 'Q3季报'
        if 'q4' in combined_text.lower() or '第四季度' in combined_text:
            return 'Q4季报'

        if 'half' in combined_text.lower() or '半年' in combined_text:
            return '半年报'

        return '年报'

    def process_brand(self, brand_info: dict) -> dict:
        brand_name = brand_info['name']
        logger.info(f"\n{'='*60}")
        logger.info(f"处理品牌: {brand_name}")
        logger.info(f"{'='*60}")

        result = {
            'brand': brand_name,
            'pdf_found': 0,
            'pdf_downloaded': 0,
            'pdf_skipped': 0,
            'pdf_failed': 0,
            'errors': []
        }

        brand_dir = self.create_brand_dir(brand_name)

        if brand_info.get('official_ir'):
            official_pdfs = self.search_official_ir(brand_name, brand_info['official_ir'])
            result['pdf_found'] += len(official_pdfs)

            for pdf_url in official_pdfs:
                year = self.extract_year_from_url(pdf_url)
                period = self.extract_period_from_url(pdf_url)
                filename = self.generate_filename(brand_name, year, period)
                save_path = os.path.join(brand_dir, filename)

                download_result = self.download_pdf(pdf_url, save_path, brand_name)
                if download_result['success']:
                    if download_result.get('skipped'):
                        result['pdf_skipped'] += 1
                    else:
                        result['pdf_downloaded'] += 1
                else:
                    result['pdf_failed'] += 1
                    result['errors'].append(f"{filename}: {download_result['error']}")

                time.sleep(random.uniform(1, 3))

        stock_codes = brand_info.get('stock_codes', {})
        if stock_codes.get('hk'):
            cninfo_pdfs = self.search_cninfo(brand_name)
            result['pdf_found'] += len(cninfo_pdfs)

            for pdf_url in cninfo_pdfs:
                year = self.extract_year_from_url(pdf_url)
                period = self.extract_period_from_url(pdf_url)
                filename = self.generate_filename(brand_name, year, period)
                save_path = os.path.join(brand_dir, filename)

                download_result = self.download_pdf(pdf_url, save_path, brand_name)
                if download_result['success']:
                    if download_result.get('skipped'):
                        result['pdf_skipped'] += 1
                    else:
                        result['pdf_downloaded'] += 1
                else:
                    result['pdf_failed'] += 1
                    result['errors'].append(f"{filename}: {download_result['error']}")

                time.sleep(random.uniform(1, 3))

        logger.info(f"\n{brand_name} 完成:")
        logger.info(f"  发现PDF: {result['pdf_found']}")
        logger.info(f"  新增下载: {result['pdf_downloaded']}")
        logger.info(f"  跳过(已存在): {result['pdf_skipped']}")
        logger.info(f"  失败: {result['pdf_failed']}")

        return result

    def run_all(self, brands_config_path: str = None) -> dict:
        if brands_config_path is None:
            brands_config_path = os.path.join(os.path.dirname(__file__), 'brands_config.yaml')

        with open(brands_config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        brands = config.get('brands', [])

        logger.info(f"\n开始处理 {len(brands)} 个品牌的财报...")

        all_results = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(self.process_brand, brand): brand for brand in brands}

            for future in as_completed(futures):
                brand = futures[future]
                try:
                    result = future.result()
                    all_results.append(result)
                except Exception as e:
                    logger.error(f"处理品牌异常: {brand['name']} - {str(e)}")

        summary = {
            'total_brands': len(brands),
            'total_found': sum(r['pdf_found'] for r in all_results),
            'total_downloaded': sum(r['pdf_downloaded'] for r in all_results),
            'total_skipped': sum(r['pdf_skipped'] for r in all_results),
            'total_failed': sum(r['pdf_failed'] for r in all_results),
            'details': all_results
        }

        logger.info(f"\n{'='*60}")
        logger.info("全部完成 - 汇总:")
        logger.info(f"  总品牌数: {summary['total_brands']}")
        logger.info(f"  总发现PDF: {summary['total_found']}")
        logger.info(f"  总新增下载: {summary['total_downloaded']}")
        logger.info(f"  总跳过: {summary['total_skipped']}")
        logger.info(f"  总失败: {summary['total_failed']}")
        logger.info(f"{'='*60}")

        return summary


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    crawler = PDFCrawlerV2()
    results = crawler.run_all()

    print("\n\n最终结果:")
    print(f"新增下载: {results['total_downloaded']} 个PDF")
    print(f"跳过: {results['total_skipped']} 个PDF")
    print(f"失败: {results['total_failed']} 个PDF")