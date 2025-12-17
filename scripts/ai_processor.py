#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI处理脚本 - 使用智谱API
"""

import os
import json
import requests
from datetime import datetime

def process_with_ai():
    """使用AI处理新闻"""
    today = datetime.now().strftime('%Y-%m-%d')
    input_file = f'output/daily/news_{today}.json'
    
    if not os.path.exists(input_file):
        print(f"未找到新闻文件: {input_file}")
        return []
    
    # 读取新闻
    with open(input_file, 'r', encoding='utf-8') as f:
        news_items = json.load(f)
    
    # 获取API密钥
    api_key = os.getenv('ZHIPU_API_KEY', '')
    if not api_key:
        print("警告：未设置ZHIPU_API_KEY，使用模拟数据")
        return news_items
    
    # 处理每条新闻
    processed_news = []
    
    for i, item in enumerate(news_items[:5]):  # 只处理前5条，避免API限制
        try:
            # 调用智谱API
            url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            prompt = f"请用小红书风格总结这条科技新闻：{item['title']}。要求：1. 简洁有趣 2. 加emoji 3. 加话题标签"
            
            data = {
                "model": "glm-4",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 200
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                ai_summary = response.json()["choices"][0]["message"]["content"]
                item['ai_summary'] = ai_summary
                
                # 生成小红书文案
                xhs_content = f"🤖 {item['title']}\n\n{ai_summary}\n\n#AI日报 #{item['source']} #科技前沿"
                item['xhs_content'] = xhs_content
                
            else:
                item['ai_summary'] = item['summary'][:100] + "..."
                item['xhs_content'] = f"{item['title']}\n\n{item['summary'][:100]}..."
            
            processed_news.append(item)
            
            # 慢一点，避免频繁调用API
            import time
            time.sleep(1)
            
        except Exception as e:
            print(f"处理第{i+1}条新闻失败: {e}")
            continue
    
    # 保存处理结果
    output_file = f'output/daily/processed_{today}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_news, f, ensure_ascii=False, indent=2)
    
    print(f"成功处理 {len(processed_news)} 条新闻")
    return processed_news

if __name__ == '__main__':
    process_with_ai()
