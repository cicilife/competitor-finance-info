
import re
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DataNormalizer:
    def __init__(self, config):
        self.config = config
        self.target_unit = config.get('target_unit', '千元')
        self.currency_rates = config.get('currency_rates', {})
        self.unit_multipliers = {
            '元': 0.001,
            '千元': 1,
            '万元': 10,
            '百万元': 100,
            '亿元': 10000,
            '亿美元': 72400,
            '百万美元': 724,
            '千美元': 0.724
        }
        self.raw_unit_multipliers = {
            '元': 1,
            '千元': 1000,
            '万元': 10000,
            '百万元': 1000000,
            '亿元': 100000000,
            '亿美元': 100000000,
            '百万美元': 1000000,
            '千美元': 1000
        }
    
    def normalize_unit(self, value, original_unit):
        """将数值转换为目标单位（千元）"""
        if original_unit in self.raw_unit_multipliers:
            raw_value = value * self.raw_unit_multipliers[original_unit]
            return raw_value / 1000
        return value
    
    def convert_currency(self, value, from_currency):
        """货币转换为人民币"""
        if from_currency in self.currency_rates:
            rate = self.currency_rates[from_currency]
            return value * rate
        return value
    
    def extract_unit(self, text):
        """从文本中提取单位"""
        unit_patterns = [
            (r'亿元', '亿元'),
            (r'百万元', '百万元'),
            (r'万元', '万元'),
            (r'千元', '千元'),
            (r'亿美元', '亿美元'),
            (r'百万美元', '百万美元'),
            (r'千美元', '千美元'),
            (r'USD|美元', '美元'),
            (r'EUR|欧元|€', '欧元'),
            (r'GBP|英镑', '英镑'),
            (r'JPY|日元', '日元'),
            (r'CAD|CAD\$|加拿大元', '加拿大元')
        ]
        
        for pattern, unit in unit_patterns:
            if re.search(pattern, text):
                return unit
        return '千元'
    
    def normalize_number(self, text):
        """从文本中提取并标准化数字"""
        numbers = re.findall(r'([\d,]+(\.\d+)?)', text)
        if numbers:
            num_str = numbers[0][0].replace(',', '')
            try:
                return float(num_str)
            except:
                return None
        return None
    
    def parse_financial_value(self, text):
        """解析财务数值"""
        value = self.normalize_number(text)
        unit = self.extract_unit(text)
        
        if value is None:
            return None, None
        
        return value, unit
    
    def normalize_data(self, extracted_data):
        """标准化提取的数据"""
        normalized = {}
        
        for metric, items in extracted_data.items():
            normalized[metric] = []
            
            for item in items:
                value = item['value']
                context = item['context']
                unit = item.get('unit', '')
                
                if not unit:
                    unit = self.extract_unit(context)
                
                normalized_value = self.normalize_unit(value, unit)
                normalized_value = self.convert_currency(normalized_value, unit)
                
                normalized[metric].append({
                    'value': normalized_value,
                    'original_value': value,
                    'original_unit': unit,
                    'page_num': item['page_num'],
                    'context': item['context']
                })
        
        return normalized
    
    def validate_data(self, data):
        """验证数据合理性"""
        errors = []
        
        for metric, items in data.items():
            for item in items:
                value = item['value']
                
                if value <= 0:
                    errors.append(f"{metric}: 数值应为正数，当前值: {value}")
                
                if metric in ['revenue', 'gross_profit', 'net_profit', 'operating_profit']:
                    if value < 100:
                        errors.append(f"{metric}: 数值异常偏小，可能单位错误，当前值: {value}")
        
        return errors
