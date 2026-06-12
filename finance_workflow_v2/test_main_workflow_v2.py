import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skills.workflow_orchestrator_v2 import WorkflowOrchestratorV2

def test_main_workflow_v2():
    """运行主工作流 V2 - 处理所有品牌的2023-2025年年报数据"""
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    raw_text_dir = os.path.join(output_dir, 'raw_text_extracts')
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(raw_text_dir, exist_ok=True)
    
    config = {
        'pdf_directory': r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务PDF库',
        'template_path': r'C:\Users\CICI\Documents\trae_projects\competitor_finance_info\竞品财务数据库_标准模板v2.xlsx',
        'output_directory': output_dir,
        'raw_text_directory': raw_text_dir,
        'target_unit': '千元',
        'currency_rates': {
            'USD': 7.24,
            'EUR': 7.86,
            'JPY': 0.048,
            'CAD': 5.28
        },
        'priority_files': [
            '2025年报', '2025年年度', '2025财年', '2025 Annual Report', '2025 annual report',
            '2024年报', '2024年年度', '2024财年', '2024 Annual Report', '2024 annual report',
            '2023年报', '2023年年度', '2023财年', '2023 Annual Report', '2023 annual report'
        ]
    }
    
    print("="*80)
    print("运行财务数据取数工作流 V2")
    print("目标: 修正&补充2023-2025年年报数据")
    print("="*80)
    
    orchestrator = WorkflowOrchestratorV2(config)
    
    try:
        report = orchestrator.run()
        
        print("\n" + "="*80)
        print("工作流 V2 执行报告")
        print("="*80)
        print(f"已处理品牌: {len(report['processed_brands'])}个")
        if report['processed_brands']:
            print(f"  品牌列表: {', '.join(report['processed_brands'])}")
        print(f"已处理文件: {len(report['processed_files'])}个")
        print(f"已填写记录: {len(report['filled_records'])}条")
        print(f"警告: {len(report['warnings'])}个")
        if report['warnings']:
            print("  警告信息:")
            for warning in report['warnings'][:5]:
                print(f"    ⚠️ {warning}")
        print(f"错误: {len(report['errors'])}个")
        if report['errors']:
            print("  错误信息:")
            for error in report['errors'][:5]:
                print(f"    ❌ {error}")
        print(f"完成度: {report['completion_rate']:.1f}%")
        print(f"输出文件: {report.get('output_file', '未保存')}")
        
        if report['filled_records']:
            print(f"\n填写的记录示例 (前10条):")
            for record in report['filled_records'][:10]:
                print(f"  ✅ {record}")
        
        print("\n✅ 主工作流 V2 测试完成！")
        
    except Exception as e:
        print(f"\n❌ 工作流执行失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_main_workflow_v2()
