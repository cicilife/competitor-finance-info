
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.excel_handler import (
    load_template, save_workbook, get_cell_value, set_cell_value,
    find_brand_row, find_column_by_header, format_cell, get_column_letter_from_num,
    ensure_brand_exists
)

class TemplateFiller:
    def __init__(self, config):
        self.config = config
        self.template_path = config['template_path']
        self.wb = None
        self.loaded = False

    def find_latest_processed_file(self):
        """查找output目录中最新的已处理文件"""
        output_dir = self.config.get('output_directory', '')
        if not output_dir or not os.path.exists(output_dir):
            return None

        files = []
        for f in os.listdir(output_dir):
            if f.startswith('Finance data template_') and f.endswith('.xlsx'):
                files.append(os.path.join(output_dir, f))

        if not files:
            return None

        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return files[0]

    def load_template(self):
        """加载模板，优先使用最新的已处理文件"""
        latest_processed = self.find_latest_processed_file()
        if latest_processed:
            print(f"  加载已处理文件: {os.path.basename(latest_processed)}")
            self.wb = load_template(latest_processed)
        else:
            print(f"  加载原始模板: {os.path.basename(self.template_path)}")
            self.wb = load_template(self.template_path)

        self.loaded = self.wb is not None
        return self.loaded
    
    def find_brand_row(self, brand_name):
        """查找品牌所在行，如果不存在则自动插入"""
        if not self.loaded:
            return None

        existing_row = find_brand_row(self.wb, brand_name, 'database')
        if existing_row is not None:
            return existing_row

        return ensure_brand_exists(self.wb, brand_name, 'database')
    
    def find_target_column(self, metric, year):
        """查找指标和年份对应的列"""
        if not self.loaded:
            return None
        
        column_mapping = {
            'revenue': {
                '2023': 4,    # D
                '2024': 5,    # E
                '2025': 6,    # F
                '2026Q1': 7,  # G
                '2026E': 8    # H
            },
            'revenue_growth': {
                '2024': 10,   # J
                '2025': 11,   # K
                '2026Q1': 12, # L
                '2026E': 13   # M
            },
            'gross_profit': {
                '2023': 16,   # P
                '2024': 17,   # Q
                '2025': 18,   # R
                '2026Q1': 19, # S
                '2025E': 20   # T
            },
            'gross_profit_growth': {
                '2024': 22,   # V
                '2025': 23,   # W
                '2026Q1': 24, # X
                '2026E': 25   # Y
            },
            'gross_margin': {
                '2023': 26,   # Z
                '2024': 27,   # AA
                '2025': 28,   # AB
                '2026Q1': 29, # AC
                '2025E': 30   # AD
            },
            'net_profit': {
                '2023': 28,   # \ (Column 28)
                '2024': 29,   # ] (Column 29)
                '2025': 30,   # ^ (Column 30)
                '2026Q1': 31, # _ (Column 31)
                '2025E': 32   # ` (Column 32)
            },
            'net_profit_growth': {
                '2024': 34,   # b (Column 34)
                '2025': 35,   # c (Column 35)
                '2026Q1': 36, # d (Column 36)
                '2026E': 37   # e (Column 37)
            }
        }
        
        if metric in column_mapping and year in column_mapping[metric]:
            return column_mapping[metric][year]
        return None
    
    def get_column_number(self, col_num):
        """列号直接返回（兼容旧代码）"""
        return col_num
    
    def fill_data(self, brand_name, metric, year, value, overwrite=False):
        """填写数据到指定位置"""
        if not self.loaded:
            return {'success': False, 'error': '模板未加载'}
        
        row = self.find_brand_row(brand_name)
        if row is None:
            return {'success': False, 'error': f'未找到品牌: {brand_name}'}
        
        col_letter = self.find_target_column(metric, year)
        if col_letter is None:
            return {'success': False, 'error': f'未找到指标列: {metric}-{year}'}
        
        col_num = self.get_column_number(col_letter)
        
        existing_value = get_cell_value(self.wb, 'database', row, col_num)
        
        if existing_value is not None and existing_value != value and not overwrite:
            return {
                'success': False,
                'error': f'数据不匹配: 当前值={existing_value}, 新值={value}',
                'existing_value': existing_value,
                'new_value': value,
                'cell': f'{col_letter}{row}'
            }
        
        if 'growth' in metric:
            stored_value = value / 100
            format_cell(self.wb, 'database', row, col_num, is_number=True, format_str='0.1%')
        else:
            stored_value = value
            format_cell(self.wb, 'database', row, col_num, is_number=True, format_str='#,##0')
        
        set_cell_value(self.wb, 'database', row, col_num, stored_value)
        
        return {
            'success': True,
            'cell': f'第{col_num}列第{row}行',
            'row': row,
            'col': col_num,
            'value': value
        }
    
    def calculate_growth(self, brand_name, metric, year):
        """计算同比增速"""
        if not self.loaded:
            return {'success': False, 'error': '模板未加载'}
        
        row = self.find_brand_row(brand_name)
        if row is None:
            return {'success': False, 'error': f'未找到品牌: {brand_name}'}
        
        current_col_letter = self.find_target_column(metric, year)
        previous_year = str(int(year[:4]) - 1) + year[4:] if 'Q' in year else str(int(year) - 1)
        previous_col_letter = self.find_target_column(metric, previous_year)
        
        if not current_col_letter or not previous_col_letter:
            return {'success': False, 'error': '列映射不存在'}
        
        current_col = self.get_column_number(current_col_letter)
        previous_col = self.get_column_number(previous_col_letter)
        
        current_value = get_cell_value(self.wb, 'database', row, current_col)
        previous_value = get_cell_value(self.wb, 'database', row, previous_col)
        
        if current_value is None or previous_value is None or previous_value == 0:
            return {'success': False, 'error': '缺少计算数据'}
        
        growth = (current_value - previous_value) / previous_value * 100
        
        growth_metric = f'{metric}_growth'
        growth_col_letter = self.find_target_column(growth_metric, year)
        
        if growth_col_letter:
            growth_col = self.get_column_number(growth_col_letter)
            set_cell_value(self.wb, 'database', row, growth_col, growth)
            format_cell(self.wb, 'database', row, growth_col, is_number=True)
            
            return {
                'success': True,
                'growth': growth,
                'cell': f'{growth_col_letter}{row}',
                'formula': f'({current_value}-{previous_value})/{previous_value}*100'
            }
        
        return {'success': False, 'error': '增速列不存在'}
    
    def save(self, output_path=None):
        """保存文件"""
        if not self.loaded:
            return False

        if output_path is None:
            output_path = self.template_path

        return save_workbook(self.wb, output_path)

    def get_original_values(self, brand):
        """获取模板中品牌的原始数值，用于与提取数据比对"""
        if not self.loaded:
            return {}

        row = self.find_brand_row(brand)
        if row is None:
            return {}

        original_values = {}

        metrics_cols = {
            'revenue': [4, 5, 6],
            'gross_profit': [16, 17, 18],
            'net_profit': [28, 29, 30]
        }

        for metric, cols in metrics_cols.items():
            values = []
            for col in cols:
                cell_value = self.get_cell_value('database', row, col)
                if cell_value and isinstance(cell_value, (int, float)):
                    values.append(cell_value)
            if values:
                original_values[metric] = values

        return original_values
