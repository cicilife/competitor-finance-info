#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
财报PDF爬虫主程序
专门用于从多个数据源抓取竞品财报PDF

使用方法:
    python main.py                    # 运行所有品牌
    python main.py --brand 安踏体育   # 只运行特定品牌
    python main.py --list             # 列出所有品牌
    python main.py --check            # 检查已下载的文件
"""

import os
import sys
import logging
import argparse
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tasks.pdf_crawler.crawler import PDFCrawlerV2

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/pdf_crawler_{datetime.now().strftime("%Y%m%d")}.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def list_brands(config_path: str = None):
    """列出所有配置的品牌"""
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), 'brands_config.yaml')
    
    import yaml
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    brands = config.get('brands', [])
    
    print(f"\n{'='*80}")
    print(f"共配置 {len(brands)} 个品牌:")
    print(f"{'='*80}")
    
    for i, brand in enumerate(brands, 1):
        stock_info = []
        if brand.get('stock_codes', {}).get('hk'):
            stock_info.append(f"HK:{brand['stock_codes']['hk']}")
        if brand.get('stock_codes', {}).get('us'):
            stock_info.append(f"US:{brand['stock_codes']['us']}")
        
        stock_str = f" ({', '.join(stock_info)})" if stock_info else ""
        
        print(f"{i:2d}. {brand['name']}{stock_str}")
        print(f"    英文名: {brand.get('english_name', 'N/A')}")
        print(f"    IR: {brand.get('official_ir', 'N/A')}")
        print()


def check_downloaded(storage_root: str = "竞品财务PDF库"):
    """检查已下载的PDF文件"""
    if not os.path.exists(storage_root):
        print(f"\n存储目录不存在: {storage_root}")
        return
    
    print(f"\n{'='*80}")
    print(f"已下载的财报PDF文件:")
    print(f"{'='*80}")
    
    total_files = 0
    total_size = 0
    
    for brand_dir in os.listdir(storage_root):
        brand_path = os.path.join(storage_root, brand_dir)
        if not os.path.isdir(brand_path):
            continue
        
        files = [f for f in os.listdir(brand_path) if f.endswith('.pdf')]
        if not files:
            continue
        
        total_files += len(files)
        brand_size = 0
        
        print(f"\n{brand_dir} ({len(files)} 个文件):")
        for filename in sorted(files):
            filepath = os.path.join(brand_path, filename)
            size = os.path.getsize(filepath)
            brand_size += size
            total_size += size
            
            size_mb = size / (1024 * 1024)
            print(f"  - {filename} ({size_mb:.2f} MB)")
        
        print(f"  小计: {brand_size / (1024 * 1024):.2f} MB")
    
    print(f"\n{'='*80}")
    print(f"总计: {total_files} 个文件, {total_size / (1024 * 1024):.2f} MB")
    print(f"{'='*80}")


def run_crawler(brand_name: str = None):
    """运行爬虫"""
    logger.info("="*60)
    logger.info("财报PDF爬虫启动")
    logger.info("="*60)
    
    crawler = PDFCrawlerV2()
    
    if brand_name:
        # 运行单个品牌
        import yaml
        config_path = os.path.join(os.path.dirname(__file__), 'brands_config.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        brands = config.get('brands', [])
        target_brand = None
        
        for brand in brands:
            if brand['name'] == brand_name or brand_name in brand.get('keywords', []):
                target_brand = brand
                break
        
        if target_brand:
            result = crawler.process_brand(target_brand)
            logger.info(f"\n{brand_name} 处理完成:")
            logger.info(f"  发现: {result['pdf_found']}")
            logger.info(f"  下载: {result['pdf_downloaded']}")
            logger.info(f"  跳过: {result['pdf_skipped']}")
            logger.info(f"  失败: {result['pdf_failed']}")
        else:
            logger.error(f"未找到品牌: {brand_name}")
            print(f"\n错误: 未找到品牌 '{brand_name}'")
            print("使用 --list 查看所有可用品牌")
    
    else:
        # 运行所有品牌
        results = crawler.run_all()
        print("\n\n" + "="*80)
        print("爬虫执行完成 - 结果汇总:")
        print("="*80)
        print(f"处理品牌数: {results['total_brands']}")
        print(f"发现PDF数: {results['total_found']}")
        print(f"新增下载: {results['total_downloaded']}")
        print(f"跳过(已存在): {results['total_skipped']}")
        print(f"失败: {results['total_failed']}")
        
        if results['total_failed'] > 0:
            print("\n失败详情:")
            for detail in results['details']:
                if detail['errors']:
                    print(f"\n{detail['brand']}:")
                    for error in detail['errors']:
                        print(f"  - {error}")


def main():
    parser = argparse.ArgumentParser(description='财报PDF爬虫')
    parser.add_argument('--brand', type=str, help='指定要处理的品牌名称')
    parser.add_argument('--list', action='store_true', help='列出所有配置的品牌')
    parser.add_argument('--check', action='store_true', help='检查已下载的文件')
    parser.add_argument('--config', type=str, help='指定配置文件路径')
    
    args = parser.parse_args()
    
    if args.list:
        list_brands(args.config)
    elif args.check:
        check_downloaded()
    else:
        run_crawler(args.brand)


if __name__ == "__main__":
    main()