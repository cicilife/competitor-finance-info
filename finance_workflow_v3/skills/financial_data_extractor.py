import os
import re
from utils.pdf_reader import read_pdf

class FinancialDataExtractor:
    def __init__(self, config):
        self.config = config
    
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
            result['errors'].append(f"提取数据时出错: {str(e)}")
            import traceback
            traceback.print_exc()
        
        return result
    
    def extract_china_a_stock_format(self, pdf_path):
        """提取中国A股财报格式的数据"""
        return self.extract_general_format(pdf_path)
    
    def extract_hk_stock_format(self, pdf_path):
        """提取港股财报格式的数据"""
        return self.extract_general_format(pdf_path)
    
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
            if isinstance(row, dict):
                row_values = []
                for key, value in row.items():
                    if value is not None and str(value).strip():
                        row_values.append(str(value).strip())
                if row_values:
                    lines.append(' '.join(row_values))
            elif isinstance(row, (list, tuple)):
                row_values = []
                for value in row:
                    if value is not None and str(value).strip():
                        row_values.append(str(value).strip())
                if row_values:
                    lines.append(' '.join(row_values))
        
        return '\n'.join(lines)
