
import os
import json
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.excel_handler import add_source_track_row

class SourceTracker:
    def __init__(self, config):
        self.config = config
        self.records = []
    
    def add_record(self, data):
        """添加一条溯源记录"""
        record = {
            '品牌': data.get('品牌', ''),
            '指标名称': data.get('指标名称', ''),
            '数值': data.get('数值', ''),
            '单位': data.get('单位', '千元'),
            '周期': data.get('周期', '年度'),
            '报告期': data.get('报告期', ''),
            '报告日期': data.get('报告日期', ''),
            '文件名称': data.get('文件名称', ''),
            '页码': data.get('页码', ''),
            '具体位置': data.get('具体位置', ''),
            '数据类型': data.get('数据类型', ''),
            '模板单元格': data.get('模板单元格', ''),
            '来源说明': data.get('来源说明', '')
        }
        
        self.records.append(record)
        return len(self.records)
    
    def add_to_excel(self, wb):
        """将所有记录写入Excel"""
        for record in self.records:
            add_source_track_row(wb, record)
        
        return len(self.records)
    
    def save_to_file(self, filename=None):
        """保存记录到JSON文件"""
        if filename is None:
            filename = 'source_tracking_records.json'
        
        output_path = os.path.join(self.config['output_directory'], filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)
        
        return output_path
    
    def generate_report(self):
        """生成溯源报告"""
        report = {
            'total_records': len(self.records),
            'brands': list(set(r['品牌'] for r in self.records)),
            'metrics': list(set(r['指标名称'] for r in self.records)),
            'files': list(set(r['文件名称'] for r in self.records if r['文件名称'])),
            'records': self.records
        }
        
        return report
    
    def validate_records(self):
        """验证记录完整性"""
        errors = []
        
        for i, record in enumerate(self.records, 1):
            if not record['品牌']:
                errors.append(f"记录{i}: 缺少品牌")
            if not record['指标名称']:
                errors.append(f"记录{i}: 缺少指标名称")
            if record['数值'] is None or record['数值'] == '':
                errors.append(f"记录{i}: 缺少数值")
            if not record['模板单元格']:
                errors.append(f"记录{i}: 缺少模板单元格位置")
        
        return errors
    
    def get_records_by_brand(self, brand):
        """按品牌筛选记录"""
        return [r for r in self.records if r['品牌'] == brand]
    
    def get_records_by_metric(self, metric):
        """按指标筛选记录"""
        return [r for r in self.records if r['指标名称'] == metric]
