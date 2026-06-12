import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skills.workflow_orchestrator import WorkflowOrchestrator

def test_toread_only():
    """仅测试探路者数据提取"""
    config = {
        'pdf_directory': r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\Toread探路者',
        'template_path': r'C:\Users\CICI\Projects\Competitor Finance Info\Finance data template.xlsx',
        'output_directory': os.path.join(os.path.dirname(__file__), 'output'),
        'target_unit': '千元',
        'currency_rates': {
            'USD': 7.24,
            'EUR': 7.86
        }
    }
    
    orchestrator = WorkflowOrchestrator(config)
    
    pdf_files = [
        r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\Toread探路者\探路者：2025年年度报告.pdf'
    ]
    
    print("="*80)
    print("测试探路者数据提取")
    print("="*80)
    
    brand = '探路者控股集团股份有限公司'
    
    try:
        if not orchestrator.filler.load_template():
            print("❌ 无法加载模板")
            return
        
        extracted = orchestrator.extractor.extract_china_a_stock_format(pdf_files[0])
        
        print(f"\n提取的数据:")
        print(f"文件: {extracted['file_name']}")
        print(f"数据: {extracted['data']}")
        
        if extracted['errors']:
            print(f"错误: {extracted['errors']}")
            return
        
        normalized = orchestrator.normalizer.normalize_data(extracted.get('data', {}))
        print(f"\n标准化后的数据:")
        for metric, items in normalized.items():
            print(f"  {metric}: {items}")
        
        # 查找品牌行
        row = orchestrator.filler.find_brand_row(brand)
        print(f"\n品牌行: {row}")
        
        # 填写模板
        orchestrator.fill_template(brand, normalized, pdf_files[0])
        
        # 打印报告
        print(f"\n填写的单元格: {orchestrator.report['filled_cells']}")
        print(f"警告: {orchestrator.report['warnings']}")
        
        # 添加溯源记录到Excel
        orchestrator.tracker.add_to_excel(orchestrator.filler.wb)
        
        # 保存source tracking到JSON文件
        tracker_path = orchestrator.tracker.save_to_file('source_tracking_test_toread.json')
        print(f"\nSource tracking保存到: {tracker_path}")
        
        # 保存Excel
        timestamp = 'test_toread_v3'
        output_path = os.path.join(config['output_directory'], f"Finance data template_{timestamp}.xlsx")
        orchestrator.filler.save(output_path)
        
        print(f"\n✅ 测试完成！")
        print(f"输出文件: {output_path}")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_toread_only()