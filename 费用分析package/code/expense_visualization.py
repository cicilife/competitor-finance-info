#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财报费用可视化工具
功能：趋势图、对比图、词云、雷达图等
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 非交互式后端
from matplotlib import font_manager
import seaborn as sns
from collections import Counter
import re
import json
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# ============================================================================
# 第一部分：基础图表
# ============================================================================

class ExpenseVisualizer:
    """费用可视化工具"""

    def __init__(self, data, output_dir='/workspace/charts'):
        self.data = data
        self.output_dir = output_dir
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'tertiary': '#F18F01',
            'quaternary': '#C73E1D',
            'success': '#3A9679',
            'warning': '#F7B801'
        }

    def plot_expense_trend(self, company, expense_type, save_path=None):
        """绘制费用趋势图"""
        filtered = self.data[
            (self.data['company'] == company) &
            (self.data['expense_type'] == expense_type)
        ].sort_values('fiscal_year')

        if len(filtered) == 0:
            print(f"无数据：{company} - {expense_type}")
            return

        fig, axes = plt.subplots(2, 1, figsize=(12, 8))

        # 子图1：费用金额趋势
        ax1 = axes[0]
        ax1.plot(filtered['fiscal_year'], filtered['amount_usd'] / 1e6,
                 marker='o', linewidth=2, color=self.colors['primary'])
        ax1.set_ylabel('费用金额（百万美元）', fontsize=11)
        ax1.set_title(f'{company} - {expense_type.upper()} 费用趋势', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.fill_between(filtered['fiscal_year'], filtered['amount_usd'] / 1e6,
                         alpha=0.3, color=self.colors['primary'])

        # 子图2：费用占比趋势
        ax2 = axes[1]
        ax2.bar(filtered['fiscal_year'], filtered['expense_ratio_pct'],
                color=self.colors['secondary'], alpha=0.8)
        ax2.set_ylabel('费用占营收比（%）', fontsize=11)
        ax2.set_xlabel('财年', fontsize=11)
        ax2.grid(True, alpha=0.3, axis='y')

        # 添加数值标签
        for i, (year, ratio) in enumerate(zip(filtered['fiscal_year'], filtered['expense_ratio_pct'])):
            ax2.annotate(f'{ratio:.1f}%', xy=(year, ratio),
                        ha='center', va='bottom', fontsize=10)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ 趋势图已保存：{save_path}")

        plt.close()

    def plot_expense_structure_comparison(self, brands=None, save_path=None):
        """绘制费用结构对比图"""
        if brands:
            filtered = self.data[self.data['brand'].isin(brands)]
        else:
            filtered = self.data

        # 计算各品牌各费用类型的平均占比
        grouped = filtered.groupby(['brand', 'expense_type'])['expense_ratio_pct'].mean().reset_index()

        # 创建透视表
        pivot = grouped.pivot(index='brand', columns='expense_type', values='expense_ratio_pct')
        pivot = pivot.fillna(0)

        # 绘制堆叠柱状图
        fig, ax = plt.subplots(figsize=(14, 8))

        expense_types = pivot.columns.tolist()
        bottom = np.zeros(len(pivot))

        colors = [self.colors['primary'], self.colors['secondary'],
                  self.colors['tertiary'], self.colors['quaternary'],
                  self.colors['success'], self.colors['warning']]

        for i, expense_type in enumerate(expense_types):
            ax.bar(pivot.index, pivot[expense_type], bottom=bottom,
                   label=expense_type.upper(), color=colors[i % len(colors)], alpha=0.8)
            bottom += pivot[expense_type].values

        ax.set_ylabel('费用占营收比（%）', fontsize=12)
        ax.set_xlabel('品牌', fontsize=12)
        ax.set_title('品牌费用结构对比', fontsize=14, fontweight='bold')
        ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
        ax.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ 结构对比图已保存：{save_path}")

        plt.close()

    def plot_brand_efficiency_radar(self, brands=None, save_path=None):
        """绘制品牌效率雷达图"""
        if brands:
            filtered = self.data[self.data['brand'].isin(brands)]
        else:
            filtered = self.data

        # 计算各品牌的指标
        metrics = filtered.groupby('brand').agg({
            'expense_ratio_pct': 'mean',
            'yoy_growth_pct': 'mean',
            'amount_usd': 'sum'
        }).reset_index()

        # 归一化处理
        for col in ['expense_ratio_pct', 'yoy_growth_pct']:
            max_val = metrics[col].max()
            if max_val > 0:
                metrics[f'{col}_norm'] = metrics[col] / max_val * 100

        # 绘制雷达图
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

        categories = ['费用效率', '增长表现', '费用规模']
        N = len(categories)

        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]

        colors = [self.colors['primary'], self.colors['secondary'],
                  self.colors['tertiary'], self.colors['quaternary']]

        for idx, brand in enumerate(metrics['brand'].values):
            values = [
                100 - metrics.iloc[idx]['expense_ratio_pct_norm'],  # 费用效率（越低越好）
                metrics.iloc[idx]['yoy_growth_pct_norm'],  # 增长表现
                min(metrics.iloc[idx]['amount_usd'] / metrics['amount_usd'].max() * 100, 100)
            ]
            values += values[:1]

            ax.plot(angles, values, 'o-', linewidth=2, label=brand, color=colors[idx % len(colors)])
            ax.fill(angles, values, alpha=0.25, color=colors[idx % len(colors)])

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=12)
        ax.set_title('品牌效率对比雷达图', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1))

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ 雷达图已保存：{save_path}")

        plt.close()

    def plot_keyword_wordcloud(self, keyword_data, save_path=None):
        """绘制关键词词云"""
        try:
            from wordcloud import WordCloud
        except ImportError:
            print("请安装 wordcloud 库：pip install wordcloud")
            return

        # 构建词频字典
        word_freq = {}
        for category, keywords in keyword_data.items():
            for keyword, count in keywords:
                word_freq[keyword] = count

        # 生成词云
        wordcloud = WordCloud(
            width=1200,
            height=800,
            background_color='white',
            max_words=100,
            colormap='viridis',
            prefer_horizontal=0.7
        ).generate_from_frequencies(word_freq)

        fig, ax = plt.subplots(figsize=(14, 10))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('费用相关关键词词云', fontsize=14, fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ 词云图已保存：{save_path}")

        plt.close()

    def plot_keyword_frequency_bar(self, keyword_data, save_path=None):
        """绘制关键词频率柱状图"""
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        categories = ['expense_types', 'trends', 'drivers']
        titles = ['费用类型', '趋势变化', '驱动因素']
        colors = [self.colors['primary'], self.colors['secondary'], self.colors['tertiary']]

        for idx, (category, title) in enumerate(zip(categories, titles)):
            ax = axes[idx]
            keywords = keyword_data.get(category, [])[:10]

            if keywords:
                words = [k for k, _ in keywords]
                counts = [c for _, c in keywords]

                bars = ax.barh(words, counts, color=colors[idx], alpha=0.8)
                ax.set_xlabel('出现次数', fontsize=11)
                ax.set_title(title, fontsize=12, fontweight='bold')
                ax.invert_yaxis()

                # 添加数值标签
                for bar, count in zip(bars, counts):
                    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                            str(count), va='center', fontsize=10)

        plt.suptitle('关键词频率分析', fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ 关键词柱状图已保存：{save_path}")

        plt.close()

    def plot_expense_heatmap(self, companies=None, save_path=None):
        """绘制费用热力图"""
        if companies:
            filtered = self.data[self.data['company'].isin(companies)]
        else:
            filtered = self.data

        # 创建透视表
        pivot = filtered.pivot_table(
            values='expense_ratio_pct',
            index='company',
            columns='expense_type',
            aggfunc='mean'
        ).fillna(0)

        fig, ax = plt.subplots(figsize=(12, 8))

        sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlOrRd',
                    center=None, ax=ax, cbar_kws={'label': '费用占营收比（%）'})

        ax.set_title('费用占比热力图', fontsize=14, fontweight='bold')
        ax.set_xlabel('费用类型', fontsize=12)
        ax.set_ylabel('公司', fontsize=12)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ 热力图已保存：{save_path}")

        plt.close()

    def plot_growth_comparison(self, brands=None, save_path=None):
        """绘制增长率对比图"""
        if brands:
            filtered = self.data[self.data['brand'].isin(brands)]
        else:
            filtered = self.data

        # 计算各品牌各费用类型的平均增长率
        grouped = filtered.groupby(['brand', 'expense_type'])['yoy_growth_pct'].mean().reset_index()

        pivot = grouped.pivot(index='brand', columns='expense_type', values='yoy_growth_pct')

        fig, ax = plt.subplots(figsize=(14, 8))

        pivot.plot(kind='bar', ax=ax, width=0.8, alpha=0.8)

        ax.set_ylabel('同比增长率（%）', fontsize=12)
        ax.set_xlabel('品牌', fontsize=12)
        ax.set_title('品牌费用增长率对比', fontsize=14, fontweight='bold')
        ax.legend(title='费用类型', bbox_to_anchor=(1.02, 1))
        ax.grid(True, alpha=0.3, axis='y')
        ax.axhline(y=0, color='black', linewidth=0.8)

        # 旋转x轴标签
        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ 增长率对比图已保存：{save_path}")

        plt.close()


# ============================================================================
# 第二部分：文本分析可视化
# ============================================================================

class TextVisualizer:
    """文本分析可视化工具"""

    def __init__(self, annotated_texts, output_dir='/workspace/charts'):
        self.annotated_texts = annotated_texts
        self.output_dir = output_dir

    def plot_annotation_distribution(self, annotation_type, save_path=None):
        """绘制标注分布图"""
        counts = Counter()

        for text_data in self.annotated_texts:
            if annotation_type in text_data.get('annotations', {}):
                value = text_data['annotations'][annotation_type]
                if value:
                    counts[value] += 1

        if not counts:
            return

        fig, ax = plt.subplots(figsize=(10, 6))

        labels = list(counts.keys())
        values = list(counts.values())

        colors = plt.cm.Set3(range(len(labels)))

        wedges, texts, autotexts = ax.pie(
            values, labels=labels, autopct='%1.1f%%',
            colors=colors, startangle=90
        )

        ax.set_title(f'{annotation_type} 标注分布', fontsize=14, fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ 标注分布图已保存：{save_path}")

        plt.close()

    def plot_sentiment_timeline(self, save_path=None):
        """绘制情感倾向时间线"""
        sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}

        timeline_data = []
        for text_data in self.annotated_texts:
            sentiment = text_data.get('annotations', {}).get('sentiment')
            if sentiment:
                timeline_data.append({
                    'period': text_data.get('period', 'Unknown'),
                    'company': text_data.get('company', 'Unknown'),
                    'sentiment_score': sentiment_map.get(sentiment, 0)
                })

        if not timeline_data:
            return

        df = pd.DataFrame(timeline_data)

        fig, ax = plt.subplots(figsize=(14, 6))

        for company in df['company'].unique():
            company_data = df[df['company'] == company].sort_values('period')
            ax.plot(company_data['period'], company_data['sentiment_score'],
                    marker='o', linewidth=2, label=company)

        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax.set_ylabel('情感倾向', fontsize=12)
        ax.set_xlabel('期间', fontsize=12)
        ax.set_title('费用描述情感倾向时间线', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_yticks([-1, 0, 1])
        ax.set_yticklabels(['负面', '中性', '正面'])

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ 情感时间线图已保存：{save_path}")

        plt.close()

    def plot_driver_analysis(self, save_path=None):
        """绘制驱动因素分析图"""
        driver_counts = Counter()

        for text_data in self.annotated_texts:
            driver = text_data.get('annotations', {}).get('driver')
            if driver:
                driver_counts[driver] += 1

        if not driver_counts:
            return

        fig, ax = plt.subplots(figsize=(10, 6))

        drivers = list(driver_counts.keys())
        counts = list(driver_counts.values())

        # 翻译驱动因素名称
        driver_names = {
            'business_expansion': '业务扩张',
            'investment': '投资驱动',
            'efficiency': '效率提升',
            'external': '外部因素',
            'restructuring': '重组整合',
            'one_time': '一次性'
        }

        labels = [driver_names.get(d, d) for d in drivers]

        bars = ax.barh(labels, counts, color='#2E86AB', alpha=0.8)

        ax.set_xlabel('提及次数', fontsize=12)
        ax.set_title('费用变化驱动因素分析', fontsize=14, fontweight='bold')

        for bar, count in zip(bars, counts):
            ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                    str(count), va='center', fontsize=11)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ 驱动因素分析图已保存：{save_path}")

        plt.close()


# ============================================================================
# 主程序入口
# ============================================================================

def main():
    """主程序"""
    print("=" * 60)
    print("财报费用可视化工具 v1.0")
    print("=" * 60)

    # 加载数据
    try:
        data = pd.read_csv('/workspace/data/expense_data_template.csv')
        print(f"✓ 成功加载数据：{len(data)} 条记录")

        # 加载标注文本
        with open('/workspace/data/sample_annotated_texts.json', 'r', encoding='utf-8') as f:
            annotated_texts = json.load(f)['texts']

        # 创建可视化器
        visualizer = ExpenseVisualizer(data)
        text_visualizer = TextVisualizer(annotated_texts)

        # 生成图表
        print("\n正在生成可视化图表...")

        # 趋势图
        visualizer.plot_expense_trend('示例公司', 'sga', '/workspace/charts/trend_example.png')

        # 结构对比图
        visualizer.plot_expense_structure_comparison(None, '/workspace/charts/structure_comparison.png')

        # 雷达图
        visualizer.plot_brand_efficiency_radar(None, '/workspace/charts/efficiency_radar.png')

        # 热力图
        visualizer.plot_expense_heatmap(None, '/workspace/charts/expense_heatmap.png')

        # 增长率对比图
        visualizer.plot_growth_comparison(None, '/workspace/charts/growth_comparison.png')

        # 标注分布图
        text_visualizer.plot_annotation_distribution('expense_type', '/workspace/charts/expense_type_dist.png')
        text_visualizer.plot_annotation_distribution('trend', '/workspace/charts/trend_dist.png')
        text_visualizer.plot_annotation_distribution('driver', '/workspace/charts/driver_dist.png')

        # 情感时间线
        text_visualizer.plot_sentiment_timeline('/workspace/charts/sentiment_timeline.png')

        # 驱动因素分析
        text_visualizer.plot_driver_analysis('/workspace/charts/driver_analysis.png')

        print("\n✓ 所有图表生成完成！")

    except Exception as e:
        print(f"\n✗ 运行出错：{str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()