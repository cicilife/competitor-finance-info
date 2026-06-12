import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skills.workflow_orchestrator import WorkflowOrchestrator

def test_361_only():
    """仅测试361度数据提取"""
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    raw_text_dir = os.path.join(output_dir, 'raw_text_extracts')
    
    config = {
        'pdf_directory': r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\361度',
        'template_path': r'C:\Users\CICI\Projects\Competitor Finance Info\Finance data template.xlsx',
        'output_directory': output_dir,
        'raw_text_directory': raw_text_dir,
        'target_unit': '千元',
        'currency_rates': {
            'USD': 7.24,
            'EUR': 7.86
        }
    }
    
    orchestrator = WorkflowOrchestrator(config)
    
    pdf_files = [
        r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\361度\361度：二零二五年年报.pdf'
    ]
    
    print("="*80)
    print("测试361度数据提取")
    print("="*80)
    
    brand = '361 度国际有限公司'
    
    try:
        if not orchestrator.filler.load_template():
            print("❌ 无法加载模板")
            return
        
        extracted = orchestrator.extractor.extract_hk_stock_format(pdf_files[0])
        
        print(f"\n提取的数据:")
        print(f"文件: {extracted['file_name']}")
        print(f"数据: {extracted['data']}")
        
        if extracted['errors']:
            print(f"错误: {extracted['errors']}")
        
        normalized = orchestrator.normalizer.normalize_data(extracted.get('data', {}))
        print(f"\n标准化后的数据:")
        for metric, items in normalized.items():
            print(f"  {metric}: {items}")
        
        row = orchestrator.filler.find_brand_row(brand)
        print(f"\n品牌行: {row}")
        
        if row:
            orchestrator.fill_template(brand, normalized, pdf_files[0])
            
            print(f"\n填写的单元格: {orchestrator.report['filled_cells']}")
            print(f"警告: {orchestrator.report['warnings']}")
            
            orchestrator.tracker.add_to_excel(orchestrator.filler.wb)
            
            tracker_path = orchestrator.tracker.save_to_file('source_tracking_test_361.json')
            print(f"\nSource tracking保存到: {tracker_path}")
            
            timestamp = 'test_361_v1'
            output_path = os.path.join(config['output_directory'], f"Finance data template_{timestamp}.xlsx")
            orchestrator.filler.save(output_path)
            
            print(f"\n✅ 测试完成！")
            print(f"输出文件: {output_path}")
        else:
            print(f"\n❌ 未找到品牌: {brand}")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_361_only()