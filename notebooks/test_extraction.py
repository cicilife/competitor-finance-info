import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.financial_processor_v2 import FinancialProcessorV2
from modules.excel_exporter_v2 import ExcelExporterV2

processor = FinancialProcessorV2()
exporter = ExcelExporterV2()

all_data = []

# 处理docs目录
if os.path.exists('docs'):
    docs_data = processor.process_all_pdfs_flat('docs', '安踏体育')
    all_data.extend(docs_data)

# 处理竞品财务PDF库
if os.path.exists('竞品财务PDF库'):
    pdf_data = processor.process_all_pdfs('竞品财务PDF库')
    all_data.extend(pdf_data)

# 对齐周期
aligned = processor.align_periods(all_data)

print(f"总处理文件数: {len(all_data)}")
print(f"成功提取数据: {len(aligned)}")

# 简单打印数据
print("\n前5条数据:")
for data in aligned[:5]:
    print(f"\n{data['brand']} - {data['filename']}")
    print(f"  年份: {data.get('year')}")
    print(f"  营收: {data.get('revenue_cny')}")
    print(f"  净利润: {data.get('profit_cny')}")
    print(f"  门店数: {data.get('store_count')}")

# 导出到新文件
output_path = f"data/processed/financial_data_v2_{len(all_data)}.xlsx"
os.makedirs("data/processed", exist_ok=True)

print(f"\n正在导出到: {output_path}")
# 暂时不传入品牌信息，简化测试
exporter.export_to_excel(aligned, output_path, brand_info_list=[])
print("导出完成！")
