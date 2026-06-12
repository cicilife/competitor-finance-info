
import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skills.workflow_orchestrator import WorkflowOrchestrator

def load_config():
    """加载配置文件"""
    config_path = 'config/config.json'
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

def main():
    """主函数"""
    print("="*80)
    print("              财报数据处理工作流")
    print("="*80)
    
    config = load_config()
    if not config:
        print("无法加载配置文件，退出程序")
        return
    
    orchestrator = WorkflowOrchestrator(config)
    report = orchestrator.run()
    
    print("\n" + "="*80)
    print("工作流执行完成！")
    print("="*80)
    print(f"处理品牌数: {len(report['processed_brands'])}")
    print(f"处理文件数: {len(report['processed_files'])}")
    print(f"填写单元格数: {len(report['filled_cells'])}")
    print(f"完成度: {report['completion_rate']:.1f}%")
    
    if report['errors']:
        print(f"\n错误 ({len(report['errors'])}):")
        for error in report['errors']:
            print(f"  - {error}")
    
    if report['warnings']:
        print(f"\n警告 ({len(report['warnings'])}):")
        for warning in report['warnings']:
            print(f"  - {warning}")

if __name__ == "__main__":
    main()
