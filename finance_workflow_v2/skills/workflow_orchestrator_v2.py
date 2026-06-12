
import os
import json
import datetime
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from skills.financial_data_extractor import FinancialDataExtractor
from skills.data_normalizer import DataNormalizer
from skills.template_filler_v2 import TemplateFillerV2

class WorkflowOrchestratorV2:
    def __init__(self, config):
        self.config = config
        self.extractor = FinancialDataExtractor(config)
        self.normalizer = DataNormalizer(config)
        self.filler = TemplateFillerV2(config)
        self.report = {
            'start_time': datetime.datetime.now().isoformat(),
            'processed_brands': [],
            'processed_files': [],
            'errors': [],
            'warnings': [],
            'filled_records': [],
            'missing_files': [],
            'completion_rate': 0
        }
        
        self.china_a_stock_brands = [
            '探路者控股集团股份有限公司',
            '贵人鸟',
            '牧高笛',
            '比音勒芬服饰股份有限公司',
            '杭州伯希和户外用品有限公司'
        ]
        
        self.hk_stock_brands = [
            '安踏体育用品有限公司',
            '特步国际控股有限公司',
            '361 度国际有限公司',
            '鸿星尔克',
            '李宁公司（含李宁、艾高）'
        ]
        
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
        
        self.fiscal_year_config = {
            'Nike': {'fy_end_month': 5, 'label': 'FY'},
            'Adidas AG': {'fy_end_month': 12, 'label': 'FY'},
            '彪马公司（Puma SE）': {'fy_end_month': 12, 'label': 'FY'},
            'lululemon athletica inc.': {'fy_end_month': 2, 'label': 'FY'},
            '加拿大鹅控股公司（Canada Goose Holdings Inc.）': {'fy_end_month': 3, 'label': 'FY'},
            '美津浓公司（Mizuno Corporation）': {'fy_end_month': 3, 'label': 'FY'}
        }

    def scan_pdf_directory(self):
        """扫描PDF目录"""
        pdf_dir = self.config['pdf_directory']
        pdf_files = {}

        for root, dirs, files in os.walk(pdf_dir):
            if os.path.basename(root) == '竞品财务PDF库':
                continue

            rel_path = os.path.relpath(root, pdf_dir)
            brand = rel_path.split(os.sep)[0]

            if brand not in pdf_files:
                pdf_files[brand] = []
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files[brand].append(os.path.join(root, file))

        return pdf_files
    
    def select_file_by_region_priority(self, files, brand):
        """按区域优先级选择文件：中国内地 > 大中华区 > 亚太区 > 全球，年报优先"""
        
        def region_priority(file):
            filename = os.path.basename(file).lower()
            
            # 年报关键词
            annual_keywords = ['年报', 'annual report', 'annual', '财年', '年度报告']
            is_annual = any(kw in filename for kw in annual_keywords)
            
            # 区域关键词（优先级从高到低）
            region_keywords = {
                '中国内地': 0,
                '大陆': 0,
                '中国': 1,
                '大中华': 2,
                '大陆及港澳': 2,
                '亚太': 3,
                'APAC': 3,
                'Asia': 3,
                '全球': 4,
                'global': 4,
                'worldwide': 4,
                'total': 4,
                '集团': 4,
                'consolidated': 4
            }
            
            region_prio = 99
            for keyword, priority in region_keywords.items():
                if keyword in filename:
                    region_prio = priority
                    break
            
            # 年报优先
            annual_prio = 0 if is_annual else 1
            
            return (annual_prio, region_prio)
        
        if not files:
            return None
        
        # 优先选择年报，如果没有年报则选择其他
        sorted_files = sorted(files, key=region_priority)
        
        selected = sorted_files[0]
        filename = os.path.basename(selected)
        
        # 验证选择的文件
        print(f"  📋 Total files: {len(files)}")
        print(f"  ✅ Selected: {filename}")
        print(f"     Priority: Annual={region_priority(selected)[0]}, Region={region_priority(selected)[1]}")
        
        return selected
    
    def get_priority_files(self, files):
        """按优先级排序文件，年报优先，年报中最新优先"""
        import re

        def extract_year(filename):
            match = re.search(r'(?:20|19)(\d{2})', filename)
            if match:
                return int(match.group(0))
            return 0

        def annual_report_priority(file):
            filename = os.path.basename(file).lower()
            
            # 年报优先（优先级0-9，数字越小越优先）
            annual_keywords = ['年报', 'annual report', 'annual', '财年', '年度报告']
            quarterly_keywords = ['季报', 'q1', 'q2', 'q3', 'q4', '中期报告', '半年报']
            
            # 检查是否是年报
            is_annual = any(kw in filename for kw in annual_keywords)
            # 检查是否是季报
            is_quarterly = any(kw in filename for kw in quarterly_keywords)
            
            if is_annual and not is_quarterly:
                return (0, -extract_year(filename))  # 年报优先，年份大的在前
            elif is_quarterly:
                return (2, -extract_year(filename))  # 季报次之
            else:
                return (1, -extract_year(filename))  # 其他文件最后

        return sorted(files, key=annual_report_priority)
    
    def extract_brand_name(self, filename):
        """从文件名提取品牌名称"""
        brand_mappings = {
            '安踏体育用品有限公司': '安踏体育用品有限公司',
            '安踏体育': '安踏体育用品有限公司',
            '安踏': '安踏体育用品有限公司',
            'ANTA': '安踏体育用品有限公司',
            '李宁公司（含李宁、艾高）': '李宁公司（含李宁、艾高）',
            '李宁': '李宁公司（含李宁、艾高）',
            '李宁公司': '李宁公司（含李宁、艾高）',
            'LI-NING': '李宁公司（含李宁、艾高）',
            '特步国际控股有限公司': '特步国际控股有限公司',
            '特步国际': '特步国际控股有限公司',
            'Xtep特步国际': '特步国际控股有限公司',
            '特步': '特步国际控股有限公司',
            'XTEP': '特步国际控股有限公司',
            'Xtep': '特步国际控股有限公司',
            '361 度国际有限公司': '361 度国际有限公司',
            '361度国际': '361 度国际有限公司',
            '361度': '361 度国际有限公司',
            '361': '361 度国际有限公司',
            '鸿星尔克': '鸿星尔克',
            'ERKE': '鸿星尔克',
            '贵人鸟': '贵人鸟',
            '贵人鸟': '贵人鸟',
            '贵人鸟': '贵人鸟',
            '贵人鸟': '贵人鸟',
            '探路者控股集团股份有限公司': '探路者控股集团股份有限公司',
            'Toread探路者': '探路者控股集团股份有限公司',
            'TOREAD': '探路者控股集团股份有限公司',
            '探路者': '探路者控股集团股份有限公司',
            '牧高笛': '牧高笛',
            '牧高笛': '牧高笛',
            '比音勒芬服饰股份有限公司': '比音勒芬服饰股份有限公司',
            '比音勒芬': '比音勒芬服饰股份有限公司',
            '捷安特（中国）有限公司': '捷安特（中国）有限公司',
            '捷安特': '捷安特（中国）有限公司',
            'Giant': '捷安特（中国）有限公司',
            'GIANT': '捷安特（中国）有限公司',
            '耐克': 'Nike',
            'NIKE': 'Nike',
            'Nike': 'Nike',
            'NIKE耐克': 'Nike',
            '阿迪达斯': 'Adidas AG',
            'ADIDAS': 'Adidas AG',
            'Adidas': 'Adidas AG',
            'Adidas阿迪达斯': 'Adidas AG',
            '彪马公司（Puma SE）': '彪马公司（Puma SE）',
            '彪马': '彪马公司（Puma SE）',
            'PUMA': '彪马公司（Puma SE）',
            'Puma': '彪马公司（Puma SE）',
            'PUMA彪马': '彪马公司（Puma SE）',
            'lululemon athletica inc.': 'lululemon athletica inc.',
            'lululemon': 'lululemon athletica inc.',
            'Lululemon': 'lululemon athletica inc.',
            'Lululemon露露乐蒙': 'lululemon athletica inc.',
            'Lululemon': 'lululemon athletica inc.',
            '加拿大鹅控股公司（Canada Goose Holdings Inc.）': '加拿大鹅控股公司（Canada Goose Holdings Inc.）',
            'CANADA GOOSE': '加拿大鹅控股公司（Canada Goose Holdings Inc.）',
            'Canada Goose': '加拿大鹅控股公司（Canada Goose Holdings Inc.）',
            'CANADAGOOSE加拿大鹅': '加拿大鹅控股公司（Canada Goose Holdings Inc.）',
            '美津浓公司（Mizuno Corporation）': '美津浓公司（Mizuno Corporation）',
            '美津浓': '美津浓公司（Mizuno Corporation）',
            'Mizuno': '美津浓公司（Mizuno Corporation）',
            'MIZUNO': '美津浓公司（Mizuno Corporation）',
            'Mizuno美津浓': '美津浓公司（Mizuno Corporation）',
            '斯凯奇（Skechers USA, Inc.）': '斯凯奇（Skechers USA, Inc.）',
            '斯凯奇': '斯凯奇（Skechers USA, Inc.）',
            'Skechers': '斯凯奇（Skechers USA, Inc.）',
            'skechers': '斯凯奇（Skechers USA, Inc.）',
            'Skechers斯凯奇': '斯凯奇（Skechers USA, Inc.）',
            'ASICS Corporation（爱世克私株式会社）': 'ASICS Corporation（爱世克私株式会社）',
            'ASICS': 'ASICS Corporation（爱世克私株式会社）',
            'Asics': 'ASICS Corporation（爱世克私株式会社）',
            '安德玛（Under Armour, Inc.）': '安德玛（Under Armour, Inc.）',
            'Under Armour': '安德玛（Under Armour, Inc.）',
            '安德玛': '安德玛（Under Armour, Inc.）',
            '哥伦比亚运动服装公司（Columbia Sportswear Company）': '哥伦比亚运动服装公司（Columbia Sportswear Company）',
            'Columbia': '哥伦比亚运动服装公司（Columbia Sportswear Company）',
            '哥伦比亚': '哥伦比亚运动服装公司（Columbia Sportswear Company）',
            'Columbia哥伦比亚': '哥伦比亚运动服装公司（Columbia Sportswear Company）',
            'Decathlon迪卡侬': 'Decathlon迪卡侬',
            'Decathlon': 'Decathlon迪卡侬',
            '迪卡侬': 'Decathlon迪卡侬',
            '亚玛芬（Amer Sports）': '亚玛芬（Amer Sports）',
            'Amer': '亚玛芬（Amer Sports）',
            'Amer亚玛芬': '亚玛芬（Amer Sports）',
            'Amer Sports': '亚玛芬（Amer Sports）',
            '威富集团（VF Corporation）': '威富集团（VF Corporation）',
            '威富': '威富集团（VF Corporation）',
            'VF': '威富集团（VF Corporation）',
            'VFC': '威富集团（VF Corporation）',
            'VFC威富集团': '威富集团（VF Corporation）',
            'On Holding AG 公司（昂跑）': 'On Holding AG 公司（昂跑）',
            'On': 'On Holding AG 公司（昂跑）',
            '昂跑': 'On Holding AG 公司（昂跑）',
            'Onrunning': 'On Holding AG 公司（昂跑）',
            'On Holding': 'On Holding AG 公司（昂跑）',
            'Topgolf Callaway Brands Corp.（Jack Wolfskin刚交易给安踏 ）': 'Topgolf Callaway Brands Corp.（Jack Wolfskin刚交易给安踏 ）',
            'Topgolf': 'Topgolf Callaway Brands Corp.（Jack Wolfskin刚交易给安踏 ）',
            'TopgolfCallaway': 'Topgolf Callaway Brands Corp.（Jack Wolfskin刚交易给安踏 ）',
            'Topgolf Callaway': 'Topgolf Callaway Brands Corp.（Jack Wolfskin刚交易给安踏 ）',
            'TheNorthFace北面': 'TheNorthFace北面',
            'TheNorthFace': 'TheNorthFace北面',
            '北面': 'TheNorthFace北面',
            'The North Face': 'TheNorthFace北面',
            'North Face': 'TheNorthFace北面',
            '杭州伯希和户外用品有限公司': '杭州伯希和户外用品有限公司',
            '伯希和': '杭州伯希和户外用品有限公司'
        }

        filename_lower = filename.lower()

        sorted_keywords = sorted(brand_mappings.keys(), key=len, reverse=True)

        for keyword in sorted_keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in filename_lower:
                return brand_mappings[keyword]

        return None

    def process_brand(self, dir_name, pdf_files):
        """处理单个品牌"""
        print(f"\n{'='*80}")
        print(f"Processing directory: {dir_name}")
        print(f"{'='*80}")

        if not pdf_files:
            print(f"  ⚠️ No PDF files found")
            self.report['missing_files'].append(dir_name)
            return

        priority_files = self.get_priority_files(pdf_files)
        latest_file = priority_files[0]
        filename = os.path.basename(latest_file)

        brand = self.extract_brand_name(filename)
        if brand is None:
            brand = self.extract_brand_name(dir_name)

        if brand is None:
            print(f"  ⚠️ Warning: Cannot extract brand name from '{filename}' or '{dir_name}'")
            return

        print(f"  ✅ Brand: {brand}")
        
        # 区域口径优先级选择：中国内地 > 大中华区 > 亚太区 > 全球
        selected_file = self.select_file_by_region_priority(pdf_files, brand)
        filename = os.path.basename(selected_file)
        
        print(f"  📄 Selected file (年报优先): {filename}")
        print(f"  📍 Region: 中国内地/大中华区/亚太区/全球 (按优先级)")
        self.report['processed_files'].append(filename)
        
        try:
            extracted = None
            
            # 确保使用正确的提取器
            if brand in self.china_a_stock_brands:
                print(f"  📊 使用A股提取器...")
                extracted = self.extractor.extract_china_a_stock_format(selected_file)
            elif brand in self.hk_stock_brands:
                print(f"  📊 使用港股提取器...")
                extracted = self.extractor.extract_hk_stock_format(selected_file)
            else:
                print(f"  📊 使用通用格式提取器...")
                extracted = self.extractor.extract_general_format(selected_file)
            
            if not extracted:
                print(f"  ❌ 提取结果为空!")
                self.report['errors'].append(f"{brand}: 提取结果为空")
                return
                
            if extracted.get('errors'):
                self.report['errors'].extend([f"{brand}: {e}" for e in extracted['errors']])
                print(f"  ⚠️ 提取错误: {extracted['errors']}")
                return
            
            print(f"  📈 提取到 {len(extracted.get('data', {}))} 个指标")
            
            normalized = self.normalizer.normalize_data(extracted.get('data', {}))
            
            if not normalized:
                print(f"  ⚠️ 警告: 未提取到任何数据")
                self.report['warnings'].append(f"{brand}: 未提取到数据")
                return
            
            print(f"  ✅ 归一化成功，开始填写数据...")
            
            self.fill_data_to_template(brand, normalized, filename)
            
            print(f"  ✅ 品牌 {brand} 处理完成!")
            self.report['processed_brands'].append(brand)
            
        except Exception as e:
            print(f"  ❌ 错误: {str(e)}")
            import traceback
            traceback.print_exc()
            self.report['errors'].append(f"{brand}处理失败: {str(e)}")
    
    def fill_data_to_template(self, brand, data, source_file):
        """将数据填写到模板"""
        metrics_map = {
            'revenue': '营业收入',
            'gross_profit': '毛利润',
            'net_profit': '净利润',
            'operating_profit': '经营溢利'
        }
        
        years = [2025, 2024, 2023]
        
        for metric_key, metric_original in metrics_map.items():
            if metric_key in data and data[metric_key]:
                metric_data = data[metric_key]
                
                for i, year in enumerate(years):
                    if i < len(metric_data):
                        item = metric_data[i]
                        value = item['value']
                        page_num = item['page_num']
                        context = item['context']
                        
                        unit = item.get('unit', '千元')
                        
                        result = self.filler.fill_data(
                            brand_name=brand,
                            metric_original=metric_original,
                            period=f'FY{year}',
                            value=value,
                            unit=unit,
                            source_file=source_file,
                            page_num=page_num,
                            context=context
                        )
                        
                        if result.get('success'):
                            self.report['filled_records'].append(
                                f"{brand} | {metric_original} | FY{year}"
                            )
    
    def run(self):
        """执行完整工作流"""
        print("="*80)
        print("Starting Workflow V2...")
        print("="*80)
        
        if not self.filler.load_template():
            self.report['errors'].append('无法加载模板文件')
            return self.report
        
        pdf_files = self.scan_pdf_directory()
        
        print(f"\nFound {len(pdf_files)} brands with PDF files\n")
        
        for brand, files in pdf_files.items():
            self.process_brand(brand, files)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(
            self.config['output_directory'],
            f"竞品财务数据库_标准模板v2_{timestamp}.xlsx"
        )
        
        if self.filler.save(output_path):
            self.report['output_file'] = output_path
            print(f"\nTemplate saved to: {output_path}")
        else:
            self.report['errors'].append('保存模板失败')
        
        self.report['end_time'] = datetime.datetime.now().isoformat()
        self.report['completion_rate'] = len(self.report['processed_brands']) / len(pdf_files) * 100 if pdf_files else 0
        
        self.generate_process_report()
        
        return self.report
    
    def generate_process_report(self):
        """生成进程报告"""
        report_dir = self.config.get('output_directory', '.')
        report_path = os.path.join(
            report_dir,
            f"process_report_v2_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        report_text = f"""
╔══════════════════════════════════════════════════════════╗
║           财报数据处理工作流 V2 进程报告                   ║
╠══════════════════════════════════════════════════════════╣
║ 开始时间: {self.report['start_time']}                    ║
║ 结束时间: {self.report['end_time']}                      ║
╠══════════════════════════════════════════════════════════╣
║ 1. 已处理品牌: {len(self.report['processed_brands'])}个                        ║
║    {', '.join(self.report['processed_brands'][:10])}       ║
║ 2. 已处理文件: {len(self.report['processed_files'])}个                          ║
║ 3. 已填写记录: {len(self.report['filled_records'])}条                          ║
║ 4. 发现警告: {len(self.report['warnings'])}个                                  ║
║ 5. 发现错误: {len(self.report['errors'])}个                                    ║
║ 6. 缺失文件品牌: {len(self.report['missing_files'])}个                         ║
║ 7. 完成度: {self.report['completion_rate']:.1f}%                                  ║
╠══════════════════════════════════════════════════════════╣
║ 输出文件: {self.report.get('output_file', '未保存')}              ║
╚══════════════════════════════════════════════════════════╝
        """
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print(f"Process report saved to: {report_path}")
        print(report_text)
