#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI机器人资讯自动收集器
"""

import requests
import feedparser
import yaml
import json
from datetime import datetime
import time

def fetch_news():
    """收集AI相关新闻"""
    print("开始收集AI机器人资讯...")
    
    # 读取配置
    with open('config/sources.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    all_news = []
    
    for source in config['rss_sources']:
        try:
            print(f"正在抓取: {source['name']}")
            feed = feedparser.parse(source['url'])
            
            for entry in feed.entries[:3]:  # 每个源取3条
                title = entry.title
                # 检查是否包含AI关键词
                if any(keyword.lower() in title.lower() for keyword in ['AI', '人工智能', '机器人', '机器学习']):
                    news_item = {
                        'title': title,
                        'summary': entry.get('summary', ''),
                        'link': entry.link,
                        'source': source['name'],
                        'published': datetime.now().strftime('%Y-%m-%d %H:%M')
                    }
                    all_news.append(news_item)
            
            time.sleep(1)  # 避免请求过快
            
        except Exception as e:
            print(f"抓取 {source['name']} 失败: {e}")
            continue
    
    # 保存到文件
    today = datetime.now().strftime('%Y-%m-%d')
    os.makedirs('output/daily', exist_ok=True)
    
    output_file = f'output/daily/news_{today}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)
    
    print(f"成功收集 {len(all_news)} 条资讯")
    return all_news

if __name__ == '__main__':
    import os
    os.makedirs('output', exist_ok=True)
    fetch_news()
