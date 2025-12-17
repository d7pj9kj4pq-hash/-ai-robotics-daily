#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成日报报告
"""

import json
import os
from datetime import datetime

def generate_daily_report():
    """生成每日报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    input_file = f'output/daily/processed_{today}.json'
    
    if not os.path.exists(input_file):
        print(f"未找到处理后的新闻文件: {input_file}")
        return
    
    # 读取数据
    with open(input_file, 'r', encoding='utf-8') as f:
        news_items = json.load(f)
    
    # 生成Markdown报告
    markdown = f"""# 🤖 AI与机器人日报 {today}

> 自动生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> 共收集 {len(news_items)} 条资讯

---

"""
    
    for i, item in enumerate(news_items, 1):
        markdown += f"""## {i}. {item['title']}

**来源**: {item['source']}  
**发布时间**: {item['published']}

**AI摘要**: {item.get('ai_summary', '暂无摘要')}

**小红书文案**:{item.get('xhs_content','暂无内容')}


**原文链接**: {item['link']}

---

"""
    
    # 保存报告
    os.makedirs('output/daily', exist_ok=True)
    report_file = f'output/daily/report_{today}.md'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    # 同时保存到docs目录
    os.makedirs('docs/daily', exist_ok=True)
    docs_file = f'docs/daily/{today}.md'
    with open(docs_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"报告已生成: {report_file}")
    return report_file

if __name__ == '__main__':
    generate_daily_report()
