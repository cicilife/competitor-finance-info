import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skills.workflow_orchestrator import WorkflowOrchestrator

def test_combined():
    """同时测试探路者和361度数据提取"""
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    raw_text_dir = os.path.join(output_dir, 'raw_text_extracts')
    
    config = {
        'pdf_directory': r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库',
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
    
    # 加载模板
    if not orchestrator.filler.load_template():
        print("❌ 无法加载模板")
        return
    
    print("="*80)
    print("同时处理探路者和361度数据")
    print("="*80)
    
    # 处理探路者
    print("\n--- 处理探路者 ---")
    brand_toread = '探路者控股集团股份有限公司'
    pdf_toread = r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\Toread探路者\探路者：2025年年度报告.pdf'
    
    try:
        extracted_toread = orchestrator.extractor.extract_china_a_stock_format(pdf_toread)
        print(f"提取文件: {extracted_toread['file_name']}")
        
        if extracted_toread['errors']:
            print(f"错误: {extracted_toread['errors']}")
        else:
            normalized_toread = orchestrator.normalizer.normalize_data(extracted_toread.get('data', {}))
            row_toread = orchestrator.filler.find_brand_row(brand_toread)
            print(f"品牌行: {row_toread}")
            
            orchestrator.fill_template(brand_toread, normalized_toread, pdf_toread)
            print(f"探路者填写的单元格: {len(orchestrator.report['filled_cells'])}个")
    except Exception as e:
        print(f"探路者处理失败: {str(e)}")
    
    # 处理361度
    print("\n--- 处理361度 ---")
    brand_361 = '361 度国际有限公司'
    pdf_361 = r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库\361度\361度：二零二五年年报.pdf'
    
    try:
        extracted_361 = orchestrator.extractor.extract_hk_stock_format(pdf_361)
        print(f"提取文件: {extracted_361['file_name']}")
        
        if extracted_361['errors']:
            print(f"错误: {extracted_361['errors']}")
        else:
            normalized_361 = orchestrator.normalizer.normalize_data(extracted_361.get('data', {}))
            row_361 = orchestrator.filler.find_brand_row(brand_361)
            print(f"品牌行: {row_361}")
            
            orchestrator.fill_template(brand_361, normalized_361, pdf_361)
            print(f"361度填写的单元格: {len(orchestrator.report['filled_cells'])}个")
    except Exception as e:
        print(f"361度处理失败: {str(e)}")
    
    # 添加溯源记录到Excel
    record_count = orchestrator.tracker.add_to_excel(orchestrator.filler.wb)
    print(f"\nSource tracking记录数: {record_count}条")
    
    # 保存source tracking到JSON
    tracker_path = orchestrator.tracker.save_to_file('source_tracking_combined.json')
    print(f"Source tracking保存到: {tracker_path}")
    
    # 保存Excel
    timestamp = 'combined_toread_361'
    output_path = os.path.join(config['output_directory'], f"Finance data template_{timestamp}.xlsx")
    orchestrator.filler.save(output_path)
    
    print(f"\n✅ 合并处理完成！")
    print(f"输出文件: {output_path}")
    print(f"\n填写的单元格汇总:")
    for cell in orchestrator.report['filled_cells']:
        print(f"  {cell}")

if __name__ == "__main__":
    test_combined()