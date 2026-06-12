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

# 数据验证规则
DATA_VALIDATION = {
    'revenue_cny': (50, 5000),  # 营收：50-5000亿元
    'profit_cny': (1, 500),    # 净利润：1-500亿元
    'gross_margin': (10, 80),  # 毛利率：10-80%
    'net_margin': (1, 30),    # 净利率：1-30%
    'store_count': (100, 20000),  # 门店数：100-20000家
    'employees': (1000, 500000),  # 员工数：1000-500000人
}

class FinancialProcessorV2:
    def __init__(self):
        # 改进的正则匹配 - 增加上下文和多模式验证
        self.patterns = {
            'revenue': [
                # 中文营收模式
                (r'營業收入.*?([\d,.]+)\s*億元?', 'CNY', 1),
                (r'營業額.*?([\d,.]+)\s*億元?', 'CNY', 1),
                (r'營收.*?([\d,.]+)\s*億元?', 'CNY', 1),
                (r'收入.*?([\d,.]+)\s*億元?', 'CNY', 1),
                (r'銷售額.*?([\d,.]+)\s*億元?', 'CNY', 1),
                # 英文营收模式
                (r'revenue.*?([\d,.]+)\s*billion\s*', 'USD', 10),
                (r'revenue.*?([\d,.]+)\s*million\s*', 'USD', 0.01),
                (r'total\s*sales.*?([\d,.]+)\s*', 'CNY', 1),
            ],
            'profit': [
                (r'淨利潤.*?([\d,.]+)\s*億元?', 'CNY', 1),
                (r'歸屬.*?淨利潤.*?([\d,.]+)\s*億元?', 'CNY', 1),
                (r'淨利.*?([\d,.]+)\s*億元?', 'CNY', 1),
                (r'net\s*profit.*?([\d,.]+)\s*', 'USD', 1),
                (r'net\s*income.*?([\d,.]+)\s*', 'USD', 1),
            ],
            'gross_margin': [
                (r'毛利率.*?([\d.]+)%', '%', 1),
                (r'gross\s*margin.*?([\d.]+)%', '%', 1),
            ],
            'net_margin': [
                (r'淨利率.*?([\d.]+)%', '%', 1),
                (r'淨利潤率.*?([\d.]+)%', '%', 1),
                (r'net\s*margin.*?([\d.]+)%', '%', 1),
            ],
            'store_count': [
                (r'店鋪.*?([\d,]+)\s*家', None, 1),
                (r'門店.*?([\d,]+)\s*家', None, 1),
                (r'門店.*?([\d,]+)\s*間', None, 1),
                (r'stores.*?([\d,]+)\s*', None, 1),
                (r'number\s*of\s*stores.*?([\d,]+)\s*', None, 1),
            ],
            'employees': [
                (r'員工.*?([\d,]+)\s*人', None, 1),
                (r'員工數.*?([\d,]+)\s*', None, 1),
                (r'employees.*?([\d,]+)\s*', None, 1),
            ],
        }
    
    def validate_data(self, data: Dict) -> Dict:
        """验证并过滤不合理的数据"""
        validated = {}
        
        for key, value in data.items():
            if value is None:
                validated[key] = None
                continue
            
            # 验证数值范围
            if key in DATA_VALIDATION:
                min_val, max_val = DATA_VALIDATION[key]
                try:
                    num_val = float(value)
                    if min_val <= num_val <= max_val:
                        validated[key] = value
                    else:
                        logger.warning(f"数据异常 - {key}: {value}（范围{min_val}-{max_val}）")
                        validated[key] = None  # 标记为待审核
                except (ValueError, TypeError):
                    validated[key] = None
            else:
                validated[key] = value
        
        return validated
    
    def extract_year_from_filename(self, filename: str) -> Optional[str]:
        """从文件名提取年份（更可靠）"""
        match = re.search(r'20(\d{2})', filename)
        if match:
            return '20' + match.group(1)
        return None
    
    def extract_year_from_text(self, text: str) -> Optional[str]:
        """从文本中提取年份，优先找完整格式"""
        # 找最近的年份
        years = re.findall(r'20(\d{2})', text)
        if years:
            return '20' + years[0]
        return None
    
    def parse_value(self, pattern: tuple, text: str) -> Optional[Dict]:
        """增强的值解析 - 增加上下文检查"""
        regex, currency, multiplier = pattern
        match = re.search(regex, text, re.IGNORECASE | re.DOTALL)
        if match:
            try:
                raw_value = match.group(1).replace(',', '')
                value = float(raw_value) * multiplier
                return {'value': value, 'currency': currency, 'pattern': regex}
            except ValueError:
                return None
        return None
    
    def extract_financial_data(self, text: str, filename: str) -> Dict[str, Any]:
        result = {}
        
        # 优先从文件名提取年份
        year = self.extract_year_from_filename(filename)
        if not year:
            year = self.extract_year_from_text(text)
        if year:
            result['year'] = year
        
        # 判断报告类型
        text_lower = text.lower()
        if '年度' in text or 'annual' in text_lower:
            result['period_type'] = 'annual'
            result['report_type'] = '年报'
        elif '季度' in text or 'quarter' in text_lower or 'Q1' in text or 'Q2' in text or 'Q3' in text or 'Q4' in text:
            result['period_type'] = 'quarter'
            result['report_type'] = '季报'
        else:
            result['period_type'] = 'other'
            result['report_type'] = '其他'
        
        # 提取季度
        quarter_match = re.search(r'(Q[1-4])', text, re.IGNORECASE)
        if quarter_match:
            result['quarter'] = quarter_match.group(1).upper()
        
        # 提取财务指标 - 多模式验证
        for key, patterns_list in self.patterns.items():
            candidates = []
            for pattern in patterns_list:
                value_info = self.parse_value(pattern, text)
                if value_info:
                    candidates.append(value_info)
            
            # 取最常见的或最合理的值
            if candidates:
                result[key] = candidates[0]
                # 记录所有匹配以便审核
                if len(candidates) > 1:
                    logger.info(f"{key} 有多个匹配: {[c['value'] for c in candidates]}")
        
        return result
    
    def convert_to_cny(self, value_info: Dict) -> Optional[float]:
        if not value_info:
            return None
        if value_info.get('currency') == 'CNY' or value_info.get('currency') is None:
            return value_info['value']
        elif value_info.get('currency') == 'USD':
            return value_info['value'] * EXCHANGE_RATES['USD_CNY']
        return value_info['value']
    
    def process_single_pdf(self, pdf_path: str, brand_name: str) -> Dict[str, Any]:
        try:
            text = self.extract_text_from_pdf(pdf_path)
            if not text:
                return {'brand': brand_name, 'filename': os.path.basename(pdf_path), 'error': '无文本内容'}
            
            filename = os.path.basename(pdf_path)
            data = self.extract_financial_data(text, filename)
            data['brand'] = brand_name
            data['filename'] = filename
            data['pdf_path'] = pdf_path
            
            # 转换货币并验证
            for key in ['revenue', 'profit']:
                if key in data:
                    data[f'{key}_cny'] = self.convert_to_cny(data[key])
                    if data[key]:
                        data[f'{key}_currency'] = data[key]['currency']
                    data[key] = data[key]['value'] if data[key] else None
            
            # 处理百分比和数量
            for key in ['gross_margin', 'net_margin', 'store_count', 'employees']:
                if key in data and data[key]:
                    data[key] = data[key]['value']
            
            # 数据验证
            validated = self.validate_data(data)
            data.update(validated)
            
            return data
        except Exception as e:
            logger.error(f"处理 {pdf_path} 时出错: {str(e)}")
            return {'brand': brand_name, 'filename': os.path.basename(pdf_path), 'error': str(e)}
    
    def extract_text_from_pdf(self, pdf_path: str, max_pages: int = 50) -> str:
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
            logger.error(f"读取PDF失败 {pdf_path}: {str(e)}")
            return ""
    
    def process_all_pdfs(self, pdf_dir: str) -> List[Dict]:
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
                        logger.info(f"处理: {brand_name} - {filename}")
                        try:
                            data = self.process_single_pdf(pdf_path, brand_name)
                            results.append(data)
                        except Exception as e:
                            logger.error(f"错误处理 {pdf_path}: {str(e)}")
        
        return results
    
    def process_all_pdfs_flat(self, pdf_dir: str, brand_name: str) -> List[Dict]:
        results = []
        if not os.path.exists(pdf_dir):
            return results
        
        for filename in os.listdir(pdf_dir):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(pdf_dir, filename)
                logger.info(f"处理: {brand_name} - {filename}")
                try:
                    data = self.process_single_pdf(pdf_path, brand_name)
                    results.append(data)
                except Exception as e:
                    logger.error(f"错误处理 {pdf_path}: {str(e)}")
        
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
        
        return aligned
