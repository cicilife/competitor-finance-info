
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.excel_handler_v2 import (
    load_template, save_workbook, find_existing_data_row, 
    add_database_row, update_database_row, get_brand_info_from_brand_list,
    get_normalized_metrics_mapping
)

class TemplateFillerV2:
    def __init__(self, config):
        self.config = config
        self.template_path = config['template_path']
        self.wb = None
        self.loaded = False
        self.normalized_metrics_map = {}
        
        self.overseas_brands = [
            'Nike',
            'Adidas AG',
            '彪马公司（Puma SE）',
            'lululemon athletica inc.',
            '加拿大鹅控股公司（Canada Goose Holdings Inc.）',
            '美津浓公司（Mizuno Corporation）',
            '捷安特（中国）有限公司',
            '斯凯奇（Skechers USA, Inc.）',
            'ASICS Corporation（爱世克私株式会社）',
            '安德玛（Under Armour, Inc.）',
            '哥伦比亚运动服装公司（Columbia Sportswear Company）',
            '亚玛芬（Amer Sports）',
            '威富集团（VF Corporation）',
            'On Holding AG 公司（昂跑）',
            'Topgolf Callaway Brands Corp.（Jack Wolfskin刚交易给安踏 ）'
        ]
        
        self.region_priority_mapping = {
            'Nike': '北美/全球',
            'Adidas AG': '欧洲/全球',
            '彪马公司（Puma SE）': '欧洲/全球',
            'lululemon athletica inc.': '北美/全球',
            '加拿大鹅控股公司（Canada Goose Holdings Inc.）': '北美/全球',
            '美津浓公司（Mizuno Corporation）': '亚洲/全球',
            '斯凯奇（Skechers USA, Inc.）': '北美/全球',
            'ASICS Corporation（爱世克私株式会社）': '亚洲/全球',
            '安德玛（Under Armour, Inc.）': '北美/全球',
            '哥伦比亚运动服装公司（Columbia Sportswear Company）': '北美/全球',
            '亚玛芬（Amer Sports）': '全球',
            '威富集团（VF Corporation）': '北美/全球',
            'On Holding AG 公司（昂跑）': '欧洲/全球',
            'Topgolf Callaway Brands Corp.（Jack Wolfskin刚交易给安踏 ）': '北美/全球',
            '捷安特（中国）有限公司': '国内'
        }
        
        self.metric_keywords_mapping = {
            'revenue': ['营业收入', 'Revenue', 'revenue', '净销售额', 'Total Revenue', 'Net Sales'],
            'gross_profit': ['毛利润', 'Gross Profit', 'gross profit', '毛利'],
            'net_profit': ['净利润', 'Net Income', 'net income', 'Net Profit', '纯利'],
            'operating_profit': ['经营溢利', 'Operating Income', 'operating income', '营业利润']
        }
        
        self.normalized_metric_names = {
            'revenue': '营业收入',
            'gross_profit': '毛利润',
            'net_profit': '净利润',
            'operating_profit': '经营溢利',
            'gross_margin': '毛利率',
            'net_margin': '净利率'
        }

    def load_template(self):
        """加载模板"""
        print(f"  加载模板: {os.path.basename(self.template_path)}")
        self.wb = load_template(self.template_path)
        self.loaded = self.wb is not None
        
        if self.loaded:
            self.normalized_metrics_map = get_normalized_metrics_mapping(self.wb)
            print(f"  模板加载成功，共加载 {len(self.normalized_metrics_map)} 个指标映射")
        
        return self.loaded
    
    def get_brand_info(self, brand_name):
        """从brand list获取品牌信息"""
        if not self.loaded:
            return None
        
        return get_brand_info_from_brand_list(self.wb, brand_name)
    
    def get_company_name(self, brand_name):
        """获取公司名称"""
        brand_info = self.get_brand_info(brand_name)
        if brand_info:
            return brand_info.get('B', brand_name)
        return brand_name
    
    def get_brand_name_field(self, brand_name):
        """获取品牌名称字段值"""
        brand_info = self.get_brand_info(brand_name)
        if brand_info:
            return brand_info.get('C', 'TTL')
        return 'TTL'
    
    def get_region(self, brand_name):
        """获取区域信息"""
        if brand_name in self.region_priority_mapping:
            return self.region_priority_mapping[brand_name]
        
        if brand_name in self.overseas_brands:
            return '全球'
        
        return '国内'
    
    def identify_metric_type(self, metric_original):
        """识别指标类型"""
        metric_original_upper = metric_original.upper() if metric_original else ''
        
        for metric_type, keywords in self.metric_keywords_mapping.items():
            for keyword in keywords:
                if keyword.upper() in metric_original_upper:
                    return metric_type
        
        if 'margin' in metric_original_lower or '率' in metric_original:
            if 'gross' in metric_original_lower:
                return 'gross_margin'
            if 'net' in metric_original_lower or '净' in metric_original:
                return 'net_margin'
        
        return 'unknown'
    
    def convert_unit(self, value, unit, target_unit='千元'):
        """单位转换"""
        if unit == 'USD' or unit == '美元':
            return value * self.config.get('currency_rates', {}).get('USD', 7.24)
        elif unit == 'EUR' or unit == '欧元':
            return value * self.config.get('currency_rates', {}).get('EUR', 7.86)
        elif unit == 'JPY' or unit == '日元':
            return value / 1000
        elif unit == '百万' or unit == 'M':
            return value * 1000
        elif unit == '亿' or unit == 'Hundred Million':
            return value * 100000
        
        return value
    
    def fill_data(self, brand_name, metric_original, period, value, unit='千元', 
                  source_file='', page_num='', context=''):
        """填写数据到Database"""
        if not self.loaded:
            return {'success': False, 'error': '模板未加载'}
        
        company_name = self.get_company_name(brand_name)
        brand_name_field = self.get_brand_name_field(brand_name)
        region = self.get_region(brand_name)
        
        existing_row = find_existing_data_row(self.wb, company_name, metric_original, period)
        
        data_dict = {
            '公司名称': company_name,
            '品牌名称': brand_name_field,
            '区域': region,
            '指标名称原始': metric_original,
            '报告周期': period,
            '数据值': value,
            '单位': unit,
            '数据来源': source_file,
            '所在页码': page_num,
            '原文摘录': context[:200] if context else '',
            '归一化周期': '年度' if 'FY' in period or '年' in period else '季度',
            '归一化指标名称': self.normalized_metric_names.get(self.identify_metric_type(metric_original), metric_original),
            '归一化指标数值': value if unit == '千元' else self.convert_unit(value, unit),
            '归一化计算逻辑': f'{unit}->千元' if unit != '千元' else '-',
            '备注': 'A' if region == '全球' else 'C'
        }
        
        if existing_row:
            update_database_row(self.wb, existing_row, data_dict)
            print(f"  更新数据: {company_name} | {metric_original} | {period}")
            return {
                'success': True,
                'row': existing_row,
                'action': 'update'
            }
        else:
            new_row = add_database_row(self.wb, data_dict)
            print(f"  新增数据: {company_name} | {metric_original} | {period}")
            return {
                'success': True,
                'row': new_row,
                'action': 'add'
            }
    
    def fill_financial_data(self, brand_name, metric_key, years, values, units, 
                           source_file, page_num, context_template=''):
        """批量填写财务数据"""
        results = []
        
        metric_original = self.normalized_metric_names.get(metric_key, metric_key)
        
        for i, year in enumerate(years):
            if i < len(values) and values[i] is not None:
                value = values[i]
                unit = units[i] if i < len(units) else '千元'
                period = f'FY{year}' if year else year
                
                context = context_template.format(year=year) if context_template else f'{year}年{metric_original}'
                
                result = self.fill_data(
                    brand_name=brand_name,
                    metric_original=metric_original,
                    period=period,
                    value=value,
                    unit=unit,
                    source_file=source_file,
                    page_num=page_num,
                    context=context
                )
                results.append(result)
        
        return results
    
    def save(self, output_path=None):
        """保存文件"""
        if not self.loaded:
            return False

        if output_path is None:
            output_path = self.template_path

        return save_workbook(self.wb, output_path)
    
    def find_latest_processed_file(self):
        """查找output目录中最新的已处理文件"""
        output_dir = self.config.get('output_directory', '')
        if not output_dir or not os.path.exists(output_dir):
            return None

        files = []
        for f in os.listdir(output_dir):
            if f.startswith('竞品财务数据库_标准模板v2_') and f.endswith('.xlsx'):
                files.append(os.path.join(output_dir, f))

        if not files:
            return None

        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return files[0]
    
    def load_latest_processed(self):
        """加载最新的已处理文件"""
        latest = self.find_latest_processed_file()
        if latest:
            print(f"  加载已处理文件: {os.path.basename(latest)}")
            self.wb = load_template(latest)
            self.loaded = self.wb is not None
            if self.loaded:
                self.normalized_metrics_map = get_normalized_metrics_mapping(self.wb)
            return self.loaded
        return False
