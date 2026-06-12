import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skills.workflow_orchestrator import WorkflowOrchestrator

def test_main_workflow():
    """测试主工作流 - 处理所有品牌"""
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    raw_text_dir = os.path.join(output_dir, 'raw_text_extracts')
    
    config = {
        'pdf_directory': r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库',
        'template_path': r'C:\Users\CICI\Projects\Competitor Finance Info\Finance data template_with_biyin.xlsx',
        'output_directory': output_dir,
        'raw_text_directory': raw_text_dir,
        'target_unit': '千元',
        'currency_rates': {
            'USD': 7.24,
            'EUR': 7.86
        },
        'priority_files': [
            '2025年年度报告', '二零二五年年报', '2025年度报告',
            '2025年报', '2024年年度报告', '二零二四年年报', '2024年度报告',
            '2026Q1', 'Q1 2026', '2026年第一季度'
        ]
    }
    
    print("="*80)
    print("运行主工作流")
    print("="*80)
    
    orchestrator = WorkflowOrchestrator(config)
    
    try:
        report = orchestrator.run()
        
        print("\n" + "="*80)
        print("工作流执行报告")
        print("="*80)
        print(f"已处理品牌: {', '.join(report['processed_brands'])}")
        print(f"已处理文件: {len(report['processed_files'])}个")
        print(f"已填写单元格: {len(report['filled_cells'])}个")
        print(f"警告: {len(report['warnings'])}个")
        print(f"错误: {len(report['errors'])}个")
        print(f"完成度: {report['completion_rate']:.1f}%")
        print(f"输出文件: {report.get('output_file', '未保存')}")
        
        if report['filled_cells']:
            print("\n填写的单元格:")
            for cell in report['filled_cells']:
                print(f"  {cell}")
        
        if report['warnings']:
            print("\n警告信息:")
            for warning in report['warnings']:
                print(f"  ⚠️ {warning}")
        
        if report['errors']:
            print("\n错误信息:")
            for error in report['errors']:
                print(f"  ❌ {error}")
        
        print("\n✅ 主工作流测试完成！")
        
    except Exception as e:
        print(f"\n❌ 工作流执行失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_main_workflow()