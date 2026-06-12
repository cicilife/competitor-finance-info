import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any

class NewsBriefGenerator:
    def __init__(self):
        self.category_priority = {
            '企业经营': 1,
            '新品发布': 2,
            '市场推广': 3,
            '渠道策略': 4,
            '其他': 5
        }
        
        self.keywords_high = ['业绩', '财报', '净利润', '亏损', '战略', '收购', '合并', '关店', '开店']
        self.keywords_medium = ['新品', '发布', '营销', '合作', '赞助', '代言人', '活动']
        self.keywords_low = ['动态', '资讯', '报道', '消息']

    def analyze_news_importance(self, title: str, content: str = '') -> int:
        text = f"{title} {content}"
        score = 0
        
        for kw in self.keywords_high:
            if kw in text:
                score += 3
        for kw in self.keywords_medium:
            if kw in text:
                score += 2
        for kw in self.keywords_low:
            if kw in text:
                score += 1
        
        return score

    def categorize_by_brand(self, news_list: List[Dict]) -> Dict[str, List[Dict]]:
        brand_categories = {
            '核心分析': ['Decathlon迪卡侬'],
            '本土竞品': ['安踏体育', '李宁', '特步国际', '361度'],
            '渠道商': ['滔搏国际', '宝胜国际'],
            '国际参考': ['NIKE耐克', 'Adidas阿迪达斯', 'Lululemon', 'PUMA彪马']
        }
        
        result = {}
        for cat_name, brands in brand_categories.items():
            result[cat_name] = [n for n in news_list if n.get('brand_name') in brands]
        
        other_news = [n for n in news_list if n.get('brand_name') not in [b for cats in brand_categories.values() for b in cats]]
        if other_news:
            result['其他品牌'] = other_news
        
        return result

    def highlight_key_events(self, news_list: List[Dict]) -> List[Dict]:
        highlighted = []
        for news in news_list:
            importance = self.analyze_news_importance(news.get('title', ''), news.get('summary', ''))
            if importance >= 3:
                news_copy = news.copy()
                news_copy['importance'] = importance
                news_copy['highlight'] = True
                highlighted.append(news_copy)
        return sorted(highlighted, key=lambda x: x['importance'], reverse=True)

    def generate_brief(self, news_list: List[Dict], period_days: int = 7) -> str:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)
        
        brief = []
        brief.append(f"# 竞品新闻简报")
        brief.append(f"\n**报告周期**: {start_date.strftime('%Y年%m月%d日')} - {end_date.strftime('%Y年%m月%d日')}")
        brief.append(f"**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
        brief.append(f"**资讯总数**: {len(news_list)} 条")
        
        categorized = self.categorize_by_brand(news_list)
        
        for cat_name, items in categorized.items():
            if not items:
                continue
            brief.append(f"\n---\n")
            brief.append(f"## {cat_name}")
            
            content_types = ['企业经营', '新品发布', '市场推广', '渠道策略', '其他']
            for content_type in content_types:
                type_items = [item for item in items if item.get('content_type') == content_type]
                if not type_items:
                    continue
                
                brief.append(f"\n### {content_type}")
                for news in type_items[:5]:
                    importance = self.analyze_news_importance(news.get('title', ''), news.get('summary', ''))
                    importance_marker = '🔥' if importance >= 3 else ''
                    brief.append(f"{importance_marker} **[{news['title']}]({news['url']})**")
                    if news.get('summary'):
                        brief.append(f"  > {news['summary'][:150]}...")
                    brief.append(f"  *来源: {news['source']} | {news.get('publish_date', news.get('crawl_date', '')[:10])}*")
        
        key_events = self.highlight_key_events(news_list)
        if key_events:
            brief.append(f"\n---\n")
            brief.append("## 📌 重点事件提示")
            for event in key_events[:10]:
                brief.append(f"- **{event.get('brand_name', '未知品牌')}**: [{event['title']}]({event['url']})")
        
        summary_stats = self.calculate_stats(news_list)
        brief.append(f"\n---\n")
        brief.append("## 📊 数据统计")
        brief.append(f"- 核心分析品牌资讯: {len(categorized.get('核心分析', []))} 条")
        brief.append(f"- 本土竞品资讯: {len(categorized.get('本土竞品', []))} 条")
        brief.append(f"- 渠道商资讯: {len(categorized.get('渠道商', []))} 条")
        brief.append(f"- 国际参考品牌资讯: {len(categorized.get('国际参考', []))} 条")
        brief.append(f"- 重点事件: {len(key_events)} 件")
        
        brief.append(f"\n*报告由系统自动生成*")
        
        return '\n'.join(brief)

    def calculate_stats(self, news_list: List[Dict]) -> Dict[str, int]:
        stats = {
            'total': len(news_list),
            'by_type': {},
            'by_source': {}
        }
        
        for news in news_list:
            content_type = news.get('content_type', '其他')
            stats['by_type'][content_type] = stats['by_type'].get(content_type, 0) + 1
            
            source = news.get('source', '未知')
            stats['by_source'][source] = stats['by_source'].get(source, 0) + 1
        
        return stats

    def save_brief(self, brief_text: str, output_dir: str = 'output') -> str:
        date_str = datetime.now().strftime('%Y%m%d')
        filename = f"news_brief_{date_str}.md"
        output_path = os.path.join(output_dir, filename)
        
        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(brief_text)
        
        return output_path

    def generate_detailed_report(self, news_list: List[Dict], output_dir: str = 'output') -> str:
        brief = self.generate_brief(news_list)
        return self.save_brief(brief, output_dir)