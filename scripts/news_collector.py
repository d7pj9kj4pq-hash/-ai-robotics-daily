#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI机器人资讯自动收集器（优化版）
"""

import requests
import feedparser
import yaml
import json
import re
from datetime import datetime
import time
import os

class NewsCollector:
    def __init__(self):
        with open('config/sources.yaml', 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        os.makedirs('output/daily', exist_ok=True)
    
    def clean_html_tags(self, text):
        """清理HTML标签和格式"""
        if not text:
            return ""
        
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        
        # 替换HTML实体
        html_entities = {
            '&nbsp;': ' ', '&amp;': '&', '&lt;': '<', '&gt;': '>',
            '&quot;': '"', '&#39;': "'", '&ldquo;': '"', '&rdquo;': '"',
            '&lsquo;': "'", '&rsquo;': "'", '&middot;': '·'
        }
        
        for entity, replacement in html_entities.items():
            text = text.replace(entity, replacement)
        
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        
        # 截断到合适长度
        return text.strip()[:500]
    
    def fetch_rss_news(self):
        """从RSS源获取资讯"""
        news_items = []
        
        for source in self.config['rss_sources']:
            try:
                print(f"正在抓取: {source['name']}")
                feed = feedparser.parse(source['url'])
                
                for entry in feed.entries[:5]:  # 每个源取5条
                    if self._is_ai_related(entry.title):
                        # 清理摘要内容
                        raw_summary = entry.get('summary', entry.title)
                        cleaned_summary = self.clean_html_tags(raw_summary)
                        
                        news_item = {
                            'title': entry.title,
                            'summary': cleaned_summary,
                            'raw_summary': raw_summary,  # 保留原始用于调试
                            'link': entry.link,
                            'source': source['name'],
                            'published': entry.get('published', datetime.now().strftime('%Y-%m-%d %H:%M')),
                            'category': self._categorize_news(entry.title)
                        }
                        news_items.append(news_item)
                
                time.sleep(1)  # 避免请求过快
                
            except Exception as e:
                print(f"抓取 {source['name']} 失败: {e}")
                continue
        
        return news_items
    
    def _is_ai_related(self, title):
        """判断内容是否与AI/机器人相关"""
        if not title:
            return False
        
        text = title.lower()
        keywords = [
            'ai', '人工智能', '机器学习', '深度学习', '神经网络',
            '机器人', 'robotics', 'robotic', '大模型', 'gpt',
            '自动驾驶', '无人驾驶', '智能驾驶', 'llm',
            '计算机视觉', '图像识别', '语音识别', 'nlu',
            '智能家居', '物联网', 'iot', '智能硬件'
        ]
        return any(keyword in text for keyword in keywords)
    
    def _categorize_news(self, title):
        """根据标题分类"""
        title_lower = title.lower()
        
        categories = {
            '医疗健康': ['医疗', '健康', '医生', '医院', '诊断', '病理'],
            '机器人': ['机器人', 'robotics', 'robotic', '机械臂', '无人机'],
            '自动驾驶': ['驾驶', '自动', '无人', '汽车', '交通'],
            '芯片硬件': ['芯片', 'gpu', 'tpu', '硬件', '半导体'],
            '大模型': ['大模型', 'llm', 'gpt', '文心', '通义'],
            '教育': ['教育', '学习', '培训', '课程'],
            '金融': ['金融', '银行', '投资', '证券', '保险']
        }
        
        for category, keywords in categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return 'AI通用'
    
    def save_news(self, news_items):
        """保存资讯到文件"""
        today = datetime.now().strftime('%Y-%m-%d')
        filename = f'output/daily/news_{today}.json'
        
        # 添加质量检查标记
        for item in news_items:
            item['quality_score'] = self._calculate_quality_score(item)
            item['collected_at'] = datetime.now().isoformat()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(news_items, f, ensure_ascii=False, indent=2)
        
        print(f"已保存 {len(news_items)} 条资讯到 {filename}")
        return filename
    
    def _calculate_quality_score(self, item):
        """计算内容质量分数"""
        score = 0
        
        # 标题长度适中加分
        title_len = len(item.get('title', ''))
        if 20 <= title_len <= 50:
            score += 2
        elif 10 <= title_len < 20 or 50 < title_len <= 80:
            score += 1
        
        # 摘要长度适中加分
        summary_len = len(item.get('summary', ''))
        if 100 <= summary_len <= 300:
            score += 2
        
        # 包含数字加分（通常有数据支撑）
        if re.search(r'\d+', item.get('title', '') + item.get('summary', '')):
            score += 1
        
        # 来源权威性加分
        authoritative_sources = ['机器之心', '量子位', 'MIT', 'IEEE']
        if item.get('source') in authoritative_sources:
            score += 2
        
        return min(score, 5)  # 最高5分

def main():
    collector = NewsCollector()
    
    print("开始收集AI机器人资讯...")
    print(f"资讯源数量: {len(collector.config['rss_sources'])}")
    
    all_news = []
    all_news.extend(collector.fetch_rss_news())
    
    # 去重（基于标题）
    unique_news = []
    seen_titles = set()
    
    for news in all_news:
        title = news['title']
        if title not in seen_titles:
            seen_titles.add(title)
            unique_news.append(news)
    
    # 按质量分数排序
    unique_news.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
    
    # 保存
    collector.save_news(unique_news[:10])  # 取前10条
    
    # 输出统计信息
    categories = {}
    for news in unique_news[:10]:
        cat = news.get('category', '未知')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📊 收集统计:")
    print(f"总收集数: {len(unique_news)}")
    print(f"精选数: {min(10, len(unique_news))}")
    print("分类分布:")
    for cat, count in categories.items():
        print(f"  {cat}: {count}条")
    
    # 保存到data.json供周报使用
    with open('output/data.json', 'w', encoding='utf-8') as f:
        json.dump({
            'last_updated': datetime.now().isoformat(),
            'news_count': len(unique_news),
            'news': unique_news[:10],
            'categories': categories
        }, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
