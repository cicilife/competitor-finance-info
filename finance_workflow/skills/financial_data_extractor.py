import os
import re
from utils.pdf_reader import read_pdf

class FinancialDataExtractor:
    def __init__(self, config):
        self.config = config
    
    def parse_financial_statement(self, pdf_path):
        """解析财务报表"""
        result = {
            'file_path': pdf_path,
            'file_name': os.path.basename(pdf_path),
            'data': {},
            'clean_data': {},
            'raw_text_saved': False,
            'errors': []
        }
        
        try:
            pages = read_pdf(pdf_path)
            
            if not pages:
                result['errors'].append('无法读取PDF内容')
                return result
            
            all_text = "\n".join([page['text'] for page in pages])
            
            result['data'] = self.extract_key_metrics(all_text)
            result['clean_data'] = self.clean_extracted_data(result['data'])
            
        except Exception as e:
            result['errors'].append(f'解析财务报表时出错: {str(e)}')
        
        return result
    
    def extract_key_metrics(self, text):
        """提取关键财务指标"""
        metrics = {}
        
        revenue_patterns = [
            r'营业收入[\s:：]+([\d,\.]+)',
            r'Revenue[\s:：]+([\d,\.]+)',
            r'营业总收入[\s:：]+([\d,\.]+)'
        ]
        
        for pattern in revenue_patterns:
            match = re.search(pattern, text)
            if match:
                metrics['revenue'] = match.group(1)
                break
        
        profit_patterns = [
            r'净利润[\s:：]+([\d,\.-]+)',
            r'Net[\s_]?Profit[\s:：]+([\d,\.-]+)',
            r'归属于母公司所有者的净利润[\s:：]+([\d,\.-]+)'
        ]
        
        for pattern in profit_patterns:
            match = re.search(pattern, text)
            if match:
                metrics['net_profit'] = match.group(1)
                break
        
        gross_profit_patterns = [
            r'毛利润[\s:：]+([\d,\.]+)',
            r'Gross[\s_]?Profit[\s:：]+([\d,\.]+)'
        ]
        
        for pattern in gross_profit_patterns:
            match = re.search(pattern, text)
            if match:
                metrics['gross_profit'] = match.group(1)
                break
        
        return metrics
    
    def clean_extracted_data(self, data):
        """清洗提取的数据"""
        cleaned = {}

        for key, value in data.items():
            if value:
                try:
                    cleaned[key] = [{'value': float(value.replace(',', '').replace(' ', '')), 'unit': '元', 'context': '', 'page_num': 1}]
                except ValueError:
                    cleaned[key] = [{'value': value, 'unit': '元', 'context': '', 'page_num': 1}]

        return cleaned
    
    def extract_china_a_stock_format(self, pdf_path):
        """提取中国A股财报格式的数据（如探路者格式）"""
        result = {
            'file_path': pdf_path,
            'file_name': os.path.basename(pdf_path),
            'data': {},
            'raw_text_saved': False,
            'errors': []
        }
        
        try:
            pages = read_pdf(pdf_path)
            
            if not pages:
                result['errors'].append('无法读取PDF内容')
                return result
            
            found_net_profit_global = False
            
            for page in pages:
                text = page['text']
                page_num = page['page_num']
                
                if '营业收入（元）' in text:
                    lines = text.split('\n')
                    
                    found_revenue = False
                    for i, line in enumerate(lines):
                        if '营业收入（元）' in line and '与主营业务无关' not in line and not found_revenue:
                            combined_line = line
                            
                            numbers = re.findall(r'([\d,]+(\.\d+)?)', combined_line)
                            float_numbers = []
                            for num_str, _ in numbers:
                                try:
                                    val = float(num_str.replace(',', ''))
                                    if val >= 100000000:
                                        float_numbers.append(val)
                                except:
                                    pass
                            
                            if len(float_numbers) >= 3:
                                result['data']['revenue'] = [
                                    {'value': float_numbers[0], 'page_num': page_num, 'unit': '元', 'context': combined_line},
                                    {'value': float_numbers[1], 'page_num': page_num, 'unit': '元', 'context': combined_line},
                                    {'value': float_numbers[2], 'page_num': page_num, 'unit': '元', 'context': combined_line}
                                ]
                                found_revenue = True
                
                if '归属于上市公司股东' in text and not found_net_profit_global:
                    lines = text.split('\n')
                    for i, line in enumerate(lines):
                        if '归属于上市公司股东' in line and '扣除非经常性损益' not in line and not found_net_profit_global:
                            data_line_index = -1
                            
                            for j in range(i, min(i + 5, len(lines))):
                                if '的净利润' in lines[j] and '扣除非经常性损益' not in lines[j]:
                                    if j > i + 1:
                                        data_line_index = j - 1
                                        break
                                
                            if data_line_index >= 0:
                                data_line = lines[data_line_index]
                                
                                numbers = re.findall(r'([\-]?[\d,]+(\.\d+)?)', data_line)
                                float_numbers = []
                                for num_str, _ in numbers:
                                    try:
                                        val = float(num_str.replace(',', ''))
                                        if abs(val) >= 1000000:
                                            float_numbers.append(val)
                                    except:
                                        pass
                                
                                if len(float_numbers) >= 3:
                                    result['data']['net_profit'] = [
                                        {'value': float_numbers[0], 'page_num': page_num, 'unit': '元', 'context': data_line},
                                        {'value': float_numbers[1], 'page_num': page_num, 'unit': '元', 'context': data_line},
                                        {'value': float_numbers[2], 'page_num': page_num, 'unit': '元', 'context': data_line}
                                    ]
                                    found_net_profit_global = True
                
                if '毛利率' in text and 'gross_profit' not in result['data'] and 'revenue' in result['data']:
                    lines = text.split('\n')
                    for i, line in enumerate(lines):
                        if '毛利率' in line:
                            for j in range(i, min(i + 10, len(lines))):
                                numbers = re.findall(r'([\d,]+(\.\d+)?)', lines[j])
                                if len(numbers) >= 2:
                                    try:
                                        float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                        gross_margins = [n for n in float_numbers if 10 < n < 100]
                                        if len(gross_margins) >= 1:
                                            revenues = [item['value'] for item in result['data']['revenue']]
                                            gross_profits = []
                                            margin = gross_margins[0] / 100
                                            for k, rev in enumerate(revenues[:3]):
                                                gross_profits.append(rev * margin)
                                            result['data']['gross_profit'] = [
                                                {'value': gross_profits[0], 'page_num': page_num, 'unit': '元', 'context': lines[j]},
                                                {'value': gross_profits[1], 'page_num': page_num, 'unit': '元', 'context': lines[j]},
                                                {'value': gross_profits[2] if len(gross_profits) > 2 else gross_profits[1], 'page_num': page_num, 'unit': '元', 'context': lines[j]}
                                            ]
                                            break
                                    except:
                                        pass
        
        except Exception as e:
            result['errors'].append(f'提取数据时出错: {str(e)}')
        
        return result
    
    def extract_hk_stock_format(self, pdf_path):
        """提取港股财报格式的数据（如361度格式）"""
        result = {
            'file_path': pdf_path,
            'file_name': os.path.basename(pdf_path),
            'data': {},
            'raw_text_saved': False,
            'errors': []
        }
        
        try:
            pages = read_pdf(pdf_path)
            
            if not pages:
                result['errors'].append('无法读取PDF内容')
                return result
            
            for page in pages:
                text = page['text']
                page_num = page['page_num']
                lines = text.split('\n')
                
                for i, line in enumerate(lines):
                    if '人民幣千元' in line or '盈利能力數據' in line:
                        data_start = i + 1
                        for j in range(data_start, min(data_start + 10, len(lines))):
                            data_line = lines[j]
                            
                            if '收益' in data_line and '盈利' not in data_line:
                                numbers = re.findall(r'([\d,]+(\.\d+)?)', data_line)
                                float_numbers = []
                                for num_str, _ in numbers:
                                    try:
                                        val = float(num_str.replace(',', ''))
                                        if val >= 100000:
                                            float_numbers.append(val)
                                    except:
                                        pass
                                
                                if len(float_numbers) >= 3:
                                    result['data']['revenue'] = [
                                        {'value': float_numbers[0] * 1000, 'page_num': page_num, 'unit': '元', 'context': data_line},
                                        {'value': float_numbers[1] * 1000, 'page_num': page_num, 'unit': '元', 'context': data_line},
                                        {'value': float_numbers[2] * 1000, 'page_num': page_num, 'unit': '元', 'context': data_line}
                                    ]
                            
                            if '毛利' in data_line and '毛利率' not in data_line:
                                numbers = re.findall(r'([\d,]+(\.\d+)?)', data_line)
                                float_numbers = []
                                for num_str, _ in numbers:
                                    try:
                                        val = float(num_str.replace(',', ''))
                                        if val >= 10000:
                                            float_numbers.append(val)
                                    except:
                                        pass
                                
                                if len(float_numbers) >= 3:
                                    result['data']['gross_profit'] = [
                                        {'value': float_numbers[0] * 1000, 'page_num': page_num, 'unit': '元', 'context': data_line},
                                        {'value': float_numbers[1] * 1000, 'page_num': page_num, 'unit': '元', 'context': data_line},
                                        {'value': float_numbers[2] * 1000, 'page_num': page_num, 'unit': '元', 'context': data_line}
                                    ]
                            
                            if '權益持有人應佔溢利' in data_line or '股东应占溢利' in data_line:
                                numbers = re.findall(r'([\d,]+(\.\d+)?)', data_line)
                                float_numbers = []
                                for num_str, _ in numbers:
                                    try:
                                        val = float(num_str.replace(',', ''))
                                        if val >= 10000:
                                            float_numbers.append(val)
                                    except:
                                        pass
                                
                                if len(float_numbers) >= 3:
                                    result['data']['net_profit'] = [
                                        {'value': float_numbers[0] * 1000, 'page_num': page_num, 'unit': '元', 'context': data_line},
                                        {'value': float_numbers[1] * 1000, 'page_num': page_num, 'unit': '元', 'context': data_line},
                                        {'value': float_numbers[2] * 1000, 'page_num': page_num, 'unit': '元', 'context': data_line}
                                    ]
                            
                            if '經營溢利' in data_line or '经营溢利' in data_line:
                                numbers = re.findall(r'([\d,]+(\.\d+)?)', data_line)
                                float_numbers = []
                                for num_str, _ in numbers:
                                    try:
                                        val = float(num_str.replace(',', ''))
                                        if val >= 10000:
                                            float_numbers.append(val)
                                    except:
                                        pass
                                
                                if len(float_numbers) >= 3:
                                    result['data']['operating_profit'] = [
                                        {'value': float_numbers[0] * 1000, 'page_num': page_num, 'unit': '元', 'context': data_line},
                                        {'value': float_numbers[1] * 1000, 'page_num': page_num, 'unit': '元', 'context': data_line},
                                        {'value': float_numbers[2] * 1000, 'page_num': page_num, 'unit': '元', 'context': data_line}
                                    ]
        
        except Exception as e:
            result['errors'].append(f'提取数据时出错: {str(e)}')
        
        return result
    
    def extract_general_format(self, pdf_path):
        """通用财务数据提取器，支持多种PDF格式"""
        result = {
            'file_path': pdf_path,
            'file_name': os.path.basename(pdf_path),
            'data': {},
            'raw_text_saved': False,
            'errors': []
        }
        
        try:
            pages = read_pdf(pdf_path, include_tables=True)
            
            if not pages:
                result['errors'].append('无法读取PDF内容')
                return result
            
            for page in pages:
                page_num = page.get('page_num', 1)
                text = page.get('text', '')
                lines = text.split('\n')

                for i, line in enumerate(lines):
                    if re.search(r'total net sales\s+\d+', line, re.IGNORECASE):
                        numbers = re.findall(r'([\d,]+)', line)
                        if len(numbers) >= 2:
                            try:
                                float_numbers = [float(n.replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 1000]
                                if len(float_numbers) >= 2 and 'revenue' not in result['data']:
                                    result['data']['revenue'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]},
                                        {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]}
                                    ]
                            except:
                                pass

                    if re.search(r'sales.*?€[\d,]+.*?million.*?previous year.*?€[\d,]+', line, re.IGNORECASE):
                        numbers = re.findall(r'€([\d,]+)', line)
                        if len(numbers) >= 2:
                            try:
                                float_numbers = [float(n.replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 1000]
                                if len(float_numbers) >= 2 and 'revenue' not in result['data']:
                                    result['data']['revenue'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]},
                                        {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]}
                                    ]
                            except:
                                pass

                    if re.search(r'decreased by.*?to €[\d,]+.*?million', line, re.IGNORECASE):
                        match = re.search(r'to €([\d,]+)\.?\d* million', line, re.IGNORECASE)
                        if match:
                            numbers = re.findall(r'€([\d,]+)', line)
                            if len(numbers) >= 2:
                                try:
                                    float_numbers = [float(n.replace(',', '')) for n in numbers]
                                    float_numbers = [n for n in float_numbers if n >= 1000]
                                    if len(float_numbers) >= 2 and 'revenue' not in result['data']:
                                        result['data']['revenue'] = [
                                            {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]},
                                            {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]}
                                        ]
                                except:
                                    pass

                    if re.search(r'^\s*Revenue\s+[\d,]+\.?\d*\s+[\d,]+\.?\d*\s+[\d,]+\.?\d*', line, re.IGNORECASE):
                        numbers = re.findall(r'([\d,]+(?:\.\d+)?)', line)
                        if len(numbers) >= 3:
                            try:
                                float_numbers = [float(n.replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 100]
                                if len(float_numbers) >= 3 and 'revenue' not in result['data']:
                                    result['data']['revenue'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]},
                                        {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]},
                                        {'value': float_numbers[2] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]}
                                    ]
                            except:
                                pass

                    if re.search(r'CAD \$\s*[\d,]+\.?\d*\s+[\d,]+\.?\d*\s+[\d,]+\.?\d*', line):
                        numbers = re.findall(r'([\d,]+(?:\.\d+)?)', line)
                        if len(numbers) >= 3:
                            try:
                                float_numbers = [float(n.replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 100]
                                if len(float_numbers) >= 3 and 'revenue' not in result['data']:
                                    result['data']['revenue'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]},
                                        {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]},
                                        {'value': float_numbers[2] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]}
                                    ]
                            except:
                                pass

                    if re.search(r'^\s*Gross profit\s+[\d,]+\.?\d*', line, re.IGNORECASE):
                        numbers = re.findall(r'([\d,]+(?:\.\d+)?)', line)
                        if len(numbers) >= 3:
                            try:
                                float_numbers = [float(n.replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 100]
                                if len(float_numbers) >= 3 and 'gross_profit' not in result['data']:
                                    result['data']['gross_profit'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]},
                                        {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]},
                                        {'value': float_numbers[2] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]}
                                    ]
                            except:
                                pass

                    if re.search(r'Net (income|loss)\s+[\d,]+\.?\d*\s+[\d,]+\.?\d*', line, re.IGNORECASE):
                        numbers = re.findall(r'([\d,]+(?:\.\d+)?)', line)
                        if len(numbers) >= 2:
                            try:
                                float_numbers = [float(n.replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 10]
                                if len(float_numbers) >= 2 and 'net_profit' not in result['data']:
                                    result['data']['net_profit'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]},
                                        {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]}
                                    ]
                            except:
                                pass

                    if re.search(r'gross profit.*€\s*[\d,]+.*from.*€\s*[\d,]+', line, re.IGNORECASE):
                        numbers = re.findall(r'€\s*([\d,]+)', line)
                        if len(numbers) >= 2:
                            try:
                                float_numbers = [float(n.replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 1000]
                                if len(float_numbers) >= 2 and 'gross_profit' not in result['data']:
                                    result['data']['gross_profit'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]},
                                        {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]}
                                    ]
                            except:
                                pass

                    if re.search(r'operating profit.*€\s*[\d,]+', line, re.IGNORECASE):
                        numbers = re.findall(r'€\s*([\d,]+)', line)
                        if len(numbers) >= 1:
                            try:
                                float_numbers = [float(n.replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 100]
                                if len(float_numbers) >= 1 and 'operating_profit' not in result['data']:
                                    result['data']['operating_profit'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]}
                                    ]
                            except:
                                pass

                    if re.search(r'net income.*continuing operations.*€\s*[\d,]+', line, re.IGNORECASE):
                        numbers = re.findall(r'€\s*([\d,]+)', line)
                        if len(numbers) >= 1:
                            try:
                                float_numbers = [float(n.replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 100]
                                if len(float_numbers) >= 1 and 'net_profit' not in result['data']:
                                    result['data']['net_profit'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]}
                                    ]
                            except:
                                pass

                    if re.search(r'^\s*revenue\s+', line) or re.search(r'^\s*income\s+', line, re.IGNORECASE):
                        numbers = re.findall(r'([\d,]+(\.\d+)?)', line)
                        if len(numbers) >= 3:
                            try:
                                float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 1000]
                                if len(float_numbers) >= 3 and 'revenue' not in result['data']:
                                    result['data']['revenue'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[2] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line}
                                    ]
                            except:
                                pass
                    
                    if '收入（附註' in line:
                        numbers = re.findall(r'([\d,]+(\.\d+)?)', line)
                        if len(numbers) >= 3:
                            try:
                                float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 1000]
                                if len(float_numbers) >= 3 and 'revenue' not in result['data']:
                                    result['data']['revenue'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[2] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line}
                                    ]
                            except:
                                pass
                    
                    if '营业收入' in line and '与主营业务无关' not in line:
                        numbers = re.findall(r'([\d,]+(\.\d+)?)', line)
                        if len(numbers) >= 3:
                            try:
                                float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 100000000]
                                if len(float_numbers) >= 3 and 'revenue' not in result['data']:
                                    result['data']['revenue'] = [
                                        {'value': float_numbers[0], 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[1], 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[2], 'page_num': page_num, 'unit': '元', 'context': line}
                                    ]
                            except:
                                pass

                    if re.search(r'^收入\s+[\d,]+', line) or re.search(r'^\s*收入\s+[\d,]+', line) or re.search(r'^revenue\s+[\d,]+', line, re.IGNORECASE):
                        numbers = re.findall(r'([\d,]+)', line)
                        if len(numbers) >= 2:
                            try:
                                float_numbers = [float(n.replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 1000]
                                if len(float_numbers) >= 2 and 'revenue' not in result['data']:
                                    rev_values = []
                                    for v in float_numbers[:5]:
                                        rev_values.append({'value': v * 1000000, 'page_num': page_num, 'unit': '元', 'context': line.strip()[:100]})
                                    result['data']['revenue'] = rev_values
                            except:
                                pass
                
                    if re.search(r'(归属于上市公司股东的净利润|股东应占溢利|权益持有人应占溢利)', line):
                        if '扣除非经常性损益' not in line:
                            if i + 1 < len(lines):
                                next_line = lines[i + 1]
                                numbers = re.findall(r'([-]?[\d,]+(\.\d+)?)', next_line)
                                if len(numbers) >= 3:
                                    try:
                                        float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                        float_numbers = [n for n in float_numbers if abs(n) >= 1000000]
                                        if len(float_numbers) >= 3 and 'net_profit' not in result['data']:
                                            result['data']['net_profit'] = [
                                                {'value': float_numbers[0], 'page_num': page_num, 'unit': '元', 'context': line},
                                                {'value': float_numbers[1], 'page_num': page_num, 'unit': '元', 'context': line},
                                                {'value': float_numbers[2], 'page_num': page_num, 'unit': '元', 'context': line}
                                            ]
                                    except:
                                        pass
                
                    if '归属于上市公司股东的' in line and '净利润' not in line:
                        if '扣除非经常性损益' not in line and 'net_profit' not in result['data']:
                            for j in range(i, min(i + 5, len(lines))):
                                if '净利润' in lines[j] and '扣除非经常性损益' not in lines[j]:
                                    if j > i:
                                        data_line = lines[j - 1]
                                        numbers = re.findall(r'([-]?[\d,]+(\.\d+)?)', data_line)
                                        if len(numbers) >= 3:
                                            try:
                                                float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                                float_numbers = [n for n in float_numbers if abs(n) >= 1000000]
                                                if len(float_numbers) >= 3:
                                                    result['data']['net_profit'] = [
                                                        {'value': float_numbers[0], 'page_num': page_num, 'unit': '元', 'context': data_line},
                                                        {'value': float_numbers[1], 'page_num': page_num, 'unit': '元', 'context': data_line},
                                                        {'value': float_numbers[2], 'page_num': page_num, 'unit': '元', 'context': data_line}
                                                    ]
                                                    break
                                            except:
                                                pass
                
                    if re.search(r'^毛利\s+', line):
                        numbers = re.findall(r'([\d,]+(\.\d+)?)', line)
                        if len(numbers) >= 3:
                            try:
                                float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 1000]
                                if len(float_numbers) >= 3 and 'gross_profit' not in result['data']:
                                    result['data']['gross_profit'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[2] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line}
                                    ]
                            except:
                                pass
                
                    if re.search(r'^Gross profit', line, re.IGNORECASE):
                        numbers = re.findall(r'([\d,]+(\.\d+)?)', line)
                        if len(numbers) >= 3:
                            try:
                                float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 1000]
                                if len(float_numbers) >= 3 and 'gross_profit' not in result['data']:
                                    result['data']['gross_profit'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[2] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line}
                                    ]
                            except:
                                pass
                
                    if '股東應佔溢利' in line and '經調整' not in line and 'net_profit' not in result['data']:
                        numbers = re.findall(r'([\d,]+(\.\d+)?)', line)
                        if len(numbers) >= 3:
                            try:
                                float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 1000]
                                if len(float_numbers) >= 3:
                                    result['data']['net_profit'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[2] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line}
                                    ]
                            except:
                                pass
                
                    if '毛利（附註' in line:
                        numbers = re.findall(r'([\d,]+(\.\d+)?)', line)
                        if len(numbers) >= 3:
                            try:
                                float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 1000]
                                if len(float_numbers) >= 3 and 'gross_profit' not in result['data']:
                                    result['data']['gross_profit'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[2] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line}
                                    ]
                            except:
                                pass
                
                    if '营业成本' in line and not '毛利率' in line:
                        numbers = re.findall(r'([\d,]+(\.\d+)?)', line)
                        if len(numbers) >= 3:
                            try:
                                float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 1000000]
                                if len(float_numbers) >= 3 and 'gross_profit' not in result['data'] and 'revenue' in result['data']:
                                    revenues = [item['value'] for item in result['data']['revenue']]
                                    gross_profits = []
                                    for idx, cost in enumerate(float_numbers[:3]):
                                        if idx < len(revenues):
                                            gross_profits.append(revenues[idx] - cost)
                                        else:
                                            gross_profits.append(cost)
                                    result['data']['gross_profit'] = [
                                        {'value': gross_profits[0], 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': gross_profits[1], 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': gross_profits[2], 'page_num': page_num, 'unit': '元', 'context': line}
                                    ]
                            except:
                                pass
                
                    if re.search(r'^Revenues\s+\$', line):
                        numbers = re.findall(r'([\d,]+(\.\d+)?)', line)
                        if len(numbers) >= 3:
                            try:
                                float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 1000]
                                if len(float_numbers) >= 3 and 'revenue' not in result['data']:
                                    result['data']['revenue'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[2] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line}
                                    ]
                            except:
                                pass
                
                    if re.search(r'^NET INCOME\s+\$', line) or re.search(r'^Net income\s+\$', line):
                        numbers = re.findall(r'([\d,]+(\.\d+)?)', line)
                        if len(numbers) >= 3:
                            try:
                                float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 100]
                                if len(float_numbers) >= 3 and 'net_profit' not in result['data']:
                                    result['data']['net_profit'] = [
                                        {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[2] * 1000000, 'page_num': page_num, 'unit': '元', 'context': line}
                                    ]
                            except:
                                pass
                
                    if '毛利率' in line:
                        for j in range(i, min(i + 10, len(lines))):
                            if lines[j].strip():
                                numbers = re.findall(r'([\d,]+(\.\d+)?)', lines[j])
                                if len(numbers) >= 2:
                                    try:
                                        float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                        gross_margins = [n for n in float_numbers if 10 < n < 100]
                                        if len(gross_margins) >= 1 and 'gross_profit' not in result['data'] and 'revenue' in result['data']:
                                            revenues = [item['value'] for item in result['data']['revenue']]
                                            gross_profits = []
                                            margin = gross_margins[0] / 100
                                            for k, rev in enumerate(revenues[:3]):
                                                gross_profits.append(rev * margin)
                                            result['data']['gross_profit'] = [
                                                {'value': gross_profits[0], 'page_num': page_num, 'unit': '元', 'context': lines[j]},
                                                {'value': gross_profits[1], 'page_num': page_num, 'unit': '元', 'context': lines[j]},
                                                {'value': gross_profits[2] if len(gross_profits) > 2 else gross_profits[1], 'page_num': page_num, 'unit': '元', 'context': lines[j]}
                                            ]
                                            break
                                    except:
                                        pass
                
                    if '营业利润' in line and '营业利润率' not in line:
                        if i + 1 < len(lines):
                            next_line = lines[i + 1]
                            numbers = re.findall(r'([\-]?[\d,]+(\.\d+)?)', next_line)
                            if len(numbers) >= 2:
                                try:
                                    float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                    float_numbers = [n for n in float_numbers if abs(n) >= 1000000]
                                    if len(float_numbers) >= 2 and 'operating_profit' not in result['data']:
                                        result['data']['operating_profit'] = [
                                            {'value': float_numbers[0], 'page_num': page_num, 'unit': '元', 'context': line},
                                            {'value': float_numbers[1], 'page_num': page_num, 'unit': '元', 'context': line},
                                            {'value': float_numbers[1] if len(float_numbers) < 3 else float_numbers[2], 'page_num': page_num, 'unit': '元', 'context': line}
                                        ]
                                except:
                                    pass
                
                    if '净利润' in line and '扣除非经常性损益' not in line and '归属于' not in line:
                        if i + 1 < len(lines) and 'net_profit' not in result['data']:
                            next_line = lines[i + 1]
                            numbers = re.findall(r'([\-]?[\d,]+(\.\d+)?)', next_line)
                            if len(numbers) >= 2:
                                try:
                                    float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                    float_numbers = [n for n in float_numbers if abs(n) >= 1000000]
                                    if len(float_numbers) >= 2:
                                        result['data']['net_profit'] = [
                                            {'value': float_numbers[0], 'page_num': page_num, 'unit': '元', 'context': line},
                                            {'value': float_numbers[1], 'page_num': page_num, 'unit': '元', 'context': line},
                                            {'value': float_numbers[1] if len(float_numbers) < 3 else float_numbers[2], 'page_num': page_num, 'unit': '元', 'context': line}
                                        ]
                                except:
                                    pass
                
                    if '收入' in line.strip() and len(line.strip()) <= 5 and i > 0:
                        prev_line = lines[i-1]
                        numbers = re.findall(r'([\d,]+(\.\d+)?)', prev_line)
                        if len(numbers) >= 3:
                            try:
                                float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 10000]
                                if len(float_numbers) >= 3 and 'revenue' not in result['data']:
                                    result['data']['revenue'] = [
                                        {'value': float_numbers[0] * 1000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[1] * 1000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[2] * 1000, 'page_num': page_num, 'unit': '元', 'context': line}
                                    ]
                            except:
                                pass
                
                    if '毛利' in line.strip() and len(line.strip()) <= 5 and i > 0:
                        prev_line = lines[i-1]
                        numbers = re.findall(r'([\d,]+(\.\d+)?)', prev_line)
                        if len(numbers) >= 3:
                            try:
                                float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                float_numbers = [n for n in float_numbers if n >= 10000]
                                if len(float_numbers) >= 3 and 'gross_profit' not in result['data']:
                                    result['data']['gross_profit'] = [
                                        {'value': float_numbers[0] * 1000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[1] * 1000, 'page_num': page_num, 'unit': '元', 'context': line},
                                        {'value': float_numbers[2] * 1000, 'page_num': page_num, 'unit': '元', 'context': line}
                                    ]
                            except:
                                pass
                
                    if '營業額' in line or '营业额' in line:
                        if i > 0:
                            prev_line = lines[i-1]
                            numbers = re.findall(r'([\d,]+(\.\d+)?)', prev_line)
                            if len(numbers) >= 3:
                                try:
                                    float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                    float_numbers = [n for n in float_numbers if n >= 10000]
                                    if len(float_numbers) >= 3 and 'revenue' not in result['data']:
                                        result['data']['revenue'] = [
                                            {'value': float_numbers[0] * 1000, 'page_num': page_num, 'unit': '元', 'context': line},
                                            {'value': float_numbers[1] * 1000, 'page_num': page_num, 'unit': '元', 'context': line},
                                            {'value': float_numbers[2] * 1000, 'page_num': page_num, 'unit': '元', 'context': line}
                                        ]
                                except:
                                    pass
                
                    if '毛利' in line and '毛利率' not in line:
                        if i > 0:
                            prev_line = lines[i-1]
                            numbers = re.findall(r'([\d,]+(\.\d+)?)', prev_line)
                            if len(numbers) >= 2:
                                try:
                                    float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                    float_numbers = [n for n in float_numbers if n >= 10000]
                                    if len(float_numbers) >= 2 and 'gross_profit' not in result['data']:
                                        result['data']['gross_profit'] = [
                                            {'value': float_numbers[0] * 1000, 'page_num': page_num, 'unit': '元', 'context': line},
                                            {'value': float_numbers[1] * 1000, 'page_num': page_num, 'unit': '元', 'context': line},
                                            {'value': float_numbers[2] * 1000 if len(float_numbers) > 2 else float_numbers[1] * 1000, 'page_num': page_num, 'unit': '元', 'context': line}
                                        ]
                                except:
                                    pass
                
                    if '權益持有人應佔溢利' in line or '股东应占溢利' in line:
                        if i > 0:
                            prev_line = lines[i-1]
                            numbers = re.findall(r'([-]?[\d,]+(\.\d+)?)', prev_line)
                            if len(numbers) >= 3:
                                try:
                                    float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                    float_numbers = [n for n in float_numbers if abs(n) >= 1000]
                                    if len(float_numbers) >= 3 and 'net_profit' not in result['data']:
                                        result['data']['net_profit'] = [
                                            {'value': float_numbers[0] * 1000, 'page_num': page_num, 'unit': '元', 'context': line},
                                            {'value': float_numbers[1] * 1000, 'page_num': page_num, 'unit': '元', 'context': line},
                                            {'value': float_numbers[2] * 1000, 'page_num': page_num, 'unit': '元', 'context': line}
                                        ]
                                except:
                                    pass

                tables = page.get('tables', [])
                for table in tables:
                    table_text = self.table_to_text(table)
                    table_lines = table_text.split('\n')

                    for tbl_line in table_lines:
                        if re.search(r'^\s*revenue\s+', tbl_line, re.IGNORECASE) or re.search(r'^\s*net\s+销售额', tbl_line, re.IGNORECASE):
                            numbers = re.findall(r'([\d,]+(\.\d+)?)', tbl_line)
                            if len(numbers) >= 3:
                                try:
                                    float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                    float_numbers = [n for n in float_numbers if n >= 1000]
                                    if len(float_numbers) >= 3 and 'revenue' not in result['data']:
                                        result['data']['revenue'] = [
                                            {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': tbl_line},
                                            {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': tbl_line},
                                            {'value': float_numbers[2] * 1000000, 'page_num': page_num, 'unit': '元', 'context': tbl_line}
                                        ]
                                except:
                                    pass

                        if re.search(r'^\s*gross\s+profit\s+', tbl_line, re.IGNORECASE):
                            numbers = re.findall(r'([\d,]+(\.\d+)?)', tbl_line)
                            if len(numbers) >= 3:
                                try:
                                    float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                    float_numbers = [n for n in float_numbers if n >= 1000]
                                    if len(float_numbers) >= 3 and 'gross_profit' not in result['data']:
                                        result['data']['gross_profit'] = [
                                            {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': tbl_line},
                                            {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': tbl_line},
                                            {'value': float_numbers[2] * 1000000, 'page_num': page_num, 'unit': '元', 'context': tbl_line}
                                        ]
                                except:
                                    pass

                        if re.search(r'^\s*net\s+(income|profit)\s+', tbl_line, re.IGNORECASE):
                            numbers = re.findall(r'([\d,]+(\.\d+)?)', tbl_line)
                            if len(numbers) >= 3:
                                try:
                                    float_numbers = [float(n[0].replace(',', '')) for n in numbers]
                                    float_numbers = [n for n in float_numbers if n >= 100]
                                    if len(float_numbers) >= 3 and 'net_profit' not in result['data']:
                                        result['data']['net_profit'] = [
                                            {'value': float_numbers[0] * 1000000, 'page_num': page_num, 'unit': '元', 'context': tbl_line},
                                            {'value': float_numbers[1] * 1000000, 'page_num': page_num, 'unit': '元', 'context': tbl_line},
                                            {'value': float_numbers[2] * 1000000, 'page_num': page_num, 'unit': '元', 'context': tbl_line}
                                        ]
                                except:
                                    pass

        except Exception as e:
            result['errors'].append(f'提取数据时出错: {str(e)}')
        
        return result
    
    def calculate_growth_rate(self, current, previous):
        """计算增长率"""
        if previous is None or previous == 0:
            return None
        return (current - previous) / previous * 100
    
    def calculate_gross_margin(self, gross_profit, revenue):
        """计算毛利率"""
        if revenue is None or revenue == 0:
            return None
        return gross_profit / revenue * 100
    
    def table_to_text(self, table_data):
        """将表格数据转换为文本格式"""
        if not table_data:
            return ""
        
        lines = []
        for row in table_data:
            row_values = []
            for key, value in row.items():
                if value is not None and str(value).strip():
                    row_values.append(str(value).strip())
            if row_values:
                lines.append(' '.join(row_values))
        
        return '\n'.join(lines)
    
    def batch_extract(self, pdf_paths):
        """批量提取多个PDF文件"""
        results = []
        
        for pdf_path in pdf_paths:
            if os.path.exists(pdf_path):
                result = self.parse_financial_statement(pdf_path)
                results.append(result)
            else:
                results.append({
                    'file_path': pdf_path,
                    'errors': ['文件不存在']
                })
        
        return results