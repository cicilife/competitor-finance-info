import os
import re
import logging
import pdfplumber
from datetime import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

EXCHANGE_RATES = {
    'USD_CNY': 7.24,
    'EUR_CNY': 7.86,
    'HKD_CNY': 0.92,
    'JPY_CNY': 0.048
}

class FinancialProcessor:
    def __init__(self):
        self.patterns = {
            'revenue': [
                (r'营收[\s\S]*?([\d,.]+)\s*(亿元|亿)', 'CNY', 1),
                (r'营业收入[\s\S]*?([\d,.]+)\s*(亿元|亿)', 'CNY', 1),
                (r'收入[\s\S]*?([\d,.]+)\s*(亿元|亿)', 'CNY', 1),
                (r'Revenue[\s\S]*?([\d,.]+)\s*(billion)', 'USD', 10),
                (r'Revenue[\s\S]*?([\d,.]+)\s*(million)', 'USD', 0.01),
                (r'Revenue[\s\S]*?([\d,.]+)\s*million', 'USD', 0.01),
                (r'营收[\s\S]*?([\d,.]+)\s*(万元|万)', 'CNY', 0.001),
                (r'Total Revenue[\s\S]*?([\d,.]+)', 'CNY', 1),
            ],
            'profit': [
                (r'净利润[\s\S]*?([\d,.]+)\s*(亿元|亿)', 'CNY', 1),
                (r'归属于母公司[\s\S]*?([\d,.]+)\s*(亿元|亿)', 'CNY', 1),
                (r'Net Profit[\s\S]*?([\d,.]+)\s*(billion)', 'USD', 10),
                (r'Net Profit[\s\S]*?([\d,.]+)\s*(million)', 'USD', 0.01),
                (r'净利[\s\S]*?([\d,.]+)\s*(亿元|亿)', 'CNY', 1),
                (r'净利润[\s\S]*?([\d,.]+)\s*(万元|万)', 'CNY', 0.001),
            ],
            'gross_margin': [
                (r'毛利率[\s\S]*?([\d.]+)%', '%', 1),
                (r'Gross Margin[\s\S]*?([\d.]+)%', '%', 1),
                (r'毛利[\s\S]*?([\d.]+)%', '%', 1),
            ],
            'net_margin': [
                (r'净利率[\s\S]*?([\d.]+)%', '%', 1),
                (r'Net Margin[\s\S]*?([\d.]+)%', '%', 1),
                (r'净利润率[\s\S]*?([\d.]+)%', '%', 1),
            ],
            'ebitda': [
                (r'EBITDA[\s\S]*?([\d,.]+)\s*(亿元|亿)', 'CNY', 1),
                (r'EBITDA[\s\S]*?([\d,.]+)\s*(billion)', 'USD', 10),
                (r'EBITDA[\s\S]*?([\d,.]+)\s*(million)', 'USD', 0.01),
            ],
            'assets': [
                (r'总资产[\s\S]*?([\d,.]+)\s*(亿元|亿)', 'CNY', 1),
                (r'Total Assets[\s\S]*?([\d,.]+)\s*(billion)', 'USD', 10),
            ],
            'debt': [
                (r'总负债[\s\S]*?([\d,.]+)\s*(亿元|亿)', 'CNY', 1),
                (r'Total Liabilities[\s\S]*?([\d,.]+)\s*(billion)', 'USD', 10),
            ],
            'cash_flow': [
                (r'经营现金流[\s\S]*?([\d,.]+)\s*(亿元|亿)', 'CNY', 1),
                (r'Operating Cash Flow[\s\S]*?([\d,.]+)\s*(billion)', 'USD', 10),
            ],
            'inventory': [
                (r'存货[\s\S]*?([\d,.]+)\s*(亿元|亿)', 'CNY', 1),
                (r'Inventory[\s\S]*?([\d,.]+)\s*(billion)', 'USD', 10),
            ],
            'store_count': [
                (r'门店数量[\s\S]*?([\d,]+)', None, 1),
                (r'Number of Stores[\s\S]*?([\d,]+)', None, 1),
                (r'Stores[\s\S]*?([\d,]+)', None, 1),
            ],
            'employees': [
                (r'员工人数[\s\S]*?([\d,]+)', None, 1),
                (r'Employees[\s\S]*?([\d,]+)', None, 1),
            ],
        }

    def extract_text_from_pdf(self, pdf_path: str, max_pages: int = 30) -> str:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for i, page in enumerate(pdf.pages):
                    if i >= max_pages:
                        break
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
                return text.strip()
        except Exception as e:
            logger.error(f"Failed to extract text from {pdf_path}: {str(e)[:50]}")
            return ""

    def parse_value(self, pattern: tuple, text: str) -> Optional[Dict]:
        regex, currency, multiplier = pattern
        match = re.search(regex, text, re.IGNORECASE)
        if match:
            try:
                raw_value = match.group(1).replace(',', '')
                value = float(raw_value) * multiplier
                return {'value': value, 'currency': currency, 'pattern': regex}
            except ValueError:
                return None
        return None

    def extract_financial_data(self, text: str) -> Dict[str, Any]:
        result = {}
        
        for key, patterns_list in self.patterns.items():
            for pattern in patterns_list:
                value_info = self.parse_value(pattern, text)
                if value_info:
                    result[key] = value_info
                    break
        
        year_match = re.search(r'(20\d{2})', text)
        if year_match:
            result['year'] = year_match.group(1)
        
        quarter_patterns = [r'Q([1-4])', r'第([一二三四])季度', r'quarter\s*([1-4])']
        for pattern in quarter_patterns:
            quarter_match = re.search(pattern, text, re.IGNORECASE)
            if quarter_match:
                quarter_num = quarter_match.group(1)
                if quarter_num in ['一', '二', '三', '四']:
                    quarter_num = str(['一', '二', '三', '四'].index(quarter_num) + 1)
                result['quarter'] = f"Q{quarter_num}"
                break
        
        if 'annual' in text.lower() or '年报' in text:
            result['period_type'] = 'annual'
        elif 'quarter' in text.lower() or '季报' in text or result.get('quarter'):
            result['period_type'] = 'quarter'
        else:
            result['period_type'] = 'unknown'
        
        return result

    def convert_to_cny(self, value_info: Dict) -> float:
        if value_info['currency'] == 'CNY' or value_info['currency'] is None:
            return value_info['value']
        elif value_info['currency'] == 'USD':
            return value_info['value'] * EXCHANGE_RATES['USD_CNY']
        elif value_info['currency'] == 'EUR':
            return value_info['value'] * EXCHANGE_RATES['EUR_CNY']
        elif value_info['currency'] == 'HKD':
            return value_info['value'] * EXCHANGE_RATES['HKD_CNY']
        elif value_info['currency'] == 'JPY':
            return value_info['value'] * EXCHANGE_RATES['JPY_CNY']
        return value_info['value']

    def process_single_pdf(self, pdf_path: str, brand_name: str) -> Dict[str, Any]:
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return {'brand': brand_name, 'filename': os.path.basename(pdf_path), 'error': 'No text extracted'}
        
        data = self.extract_financial_data(text)
        data['brand'] = brand_name
        data['filename'] = os.path.basename(pdf_path)
        data['pdf_path'] = pdf_path
        
        for key in ['revenue', 'profit', 'ebitda', 'assets', 'debt', 'cash_flow', 'inventory']:
            if key in data and data[key].get('currency'):
                data[f'{key}_cny'] = self.convert_to_cny(data[key])
                data[f'{key}_currency'] = data[key]['currency']
                data[key] = data[key]['value']
        
        if 'gross_margin' in data:
            data['gross_margin'] = data['gross_margin']['value']
        if 'net_margin' in data:
            data['net_margin'] = data['net_margin']['value']
        if 'store_count' in data:
            data['store_count'] = int(data['store_count']['value'])
        if 'employees' in data:
            data['employees'] = int(data['employees']['value'])
        
        return data

    def process_all_pdfs(self, pdf_dir: str = 'data/raw/pdf') -> List[Dict]:
        results = []
        
        if not os.path.exists(pdf_dir):
            return results
        
        for brand_dir in os.listdir(pdf_dir):
            brand_path = os.path.join(pdf_dir, brand_dir)
            if not os.path.isdir(brand_path):
                continue
            
            brand_name = brand_dir
            for root, dirs, files in os.walk(brand_path):
                for filename in files:
                    if filename.lower().endswith('.pdf'):
                        pdf_path = os.path.join(root, filename)
                        logger.info(f"Processing: {brand_name} - {filename}")
                        try:
                            data = self.process_single_pdf(pdf_path, brand_name)
                            results.append(data)
                        except Exception as e:
                            logger.error(f"Error processing {pdf_path}: {str(e)[:50]}")
        
        return results

    def process_all_pdfs_flat(self, pdf_dir: str, brand_name: str) -> List[Dict]:
        results = []
        
        if not os.path.exists(pdf_dir):
            return results
        
        for filename in os.listdir(pdf_dir):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(pdf_dir, filename)
                logger.info(f"Processing: {brand_name} - {filename}")
                try:
                    data = self.process_single_pdf(pdf_path, brand_name)
                    results.append(data)
                except Exception as e:
                    logger.error(f"Error processing {pdf_path}: {str(e)[:50]}")
        
        return results

    def align_periods(self, data_list: List[Dict]) -> List[Dict]:
        aligned = []
        
        for data in data_list:
            year = data.get('year', 'N/A')
            quarter = data.get('quarter', '')
            
            if data.get('period_type') == 'annual':
                period = f"{year}年度"
                period_end = f"{year}-12-31"
            elif quarter:
                period = f"{year}{quarter}"
                quarter_months = {'Q1': '03-31', 'Q2': '06-30', 'Q3': '09-30', 'Q4': '12-31'}
                period_end = f"{year}-{quarter_months.get(quarter, '12-31')}"
            else:
                period = f"{year}"
                period_end = f"{year}-12-31"
            
            aligned_data = data.copy()
            aligned_data['period'] = period
            aligned_data['period_end'] = period_end
            aligned.append(aligned_data)
        
        return sorted(aligned, key=lambda x: (x.get('year', '0'), x.get('quarter', 'Q4')))

    def validate_data(self, data_list: List[Dict]) -> List[Dict]:
        validated = []
        for data in data_list:
            if 'error' in data:
                continue
            if not data.get('year'):
                continue
            validated.append(data)
        return validated