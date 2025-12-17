#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成周报
"""

import json
import os
from datetime import datetime, timedelta

def generate_weekly_report():
    """生成周度报告"""
    print("开始生成周报...")
    
    # 获取过去7天的数据
    weekly_news = []
    
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        file_path = f'output/daily/processed_{date}.json'
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                daily_news = json.load(f)
                weekly_news.extend(daily_news)
    
    if not weekly_news:
        print("本周没有数据")
        return
    
    # 计算统计数据
    source_counts = {}
    for item in weekly_news:
        source = item.get('source', '未知')
        source_counts[source] = source_counts.get(source, 0) + 1
    
    # 按标题关键词分类
    categories = {
        'AI大模型': 0,
        '机器人': 0,
        '自动驾驶': 0,
        '芯片硬件': 0,
        '其他': 0
    }
    
    for item in weekly_news:
        title = item.get('title', '').lower()
        if any(keyword in title for keyword in ['gpt', '大模型', 'llm']):
            categories['AI大模型'] += 1
        elif '机器人' in title or 'robotics' in title:
            categories['机器人'] += 1
        elif '自动驾驶' in title or '无人驾驶' in title:
            categories['自动驾驶'] += 1
        elif any(keyword in title for keyword in ['芯片', 'gpu', '硬件']):
            categories['芯片硬件'] += 1
        else:
            categories['其他'] += 1
    
    # 生成周报Markdown
    week_num = datetime.now().isocalendar()[1]
    start_date = (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    markdown = f"""# 📊 AI与机器人周报 第{week_num}周

**统计周期**: {start_date} 至 {end_date}
**资讯总数**: {len(weekly_news)} 条

## 📈 本周数据概览

### 资讯来源分布
"""
    
    for source, count in source_counts.items():
        markdown += f"- **{source}**: {count} 条\n"
    
    markdown += "\n### 内容分类统计\n"
    for category, count in categories.items():
        markdown += f"- **{category}**: {count} 条\n"
    
    markdown += f"""
### 趋势分析
1. 本周最活跃来源: {max(source_counts, key=source_counts.get)}
2. 最热门领域: {max(categories, key=categories.get)}
3. 平均每天资讯数: {len(weekly_news)//7} 条

## 🏆 本周热门资讯（前5）

"""
    
    # 简单按标题长度和关键词评分（实际中可以更复杂）
    def calculate_score(item):
        score = 0
        title = item.get('title', '')
        # 关键词加分
        keywords = ['突破', '重大', '首次', '革命性', '重磅']
        for keyword in keywords:
            if keyword in title:
                score += 3
        # 标题长度加分（长标题通常更详细）
        score += min(len(title) / 10, 5)
        return score
    
    weekly_news.sort(key=calculate_score, reverse=True)
    
    for i, item in enumerate(weekly_news[:5], 1):
        markdown += f"""### {i}. {item['title']}

**来源**: {item.get('source', '未知')}
**发布时间**: {item.get('published', '未知')}

**摘要**: {item.get('ai_summary', item.get('summary', '无摘要'))[:150]}...

[查看原文]({item.get('link', '#')})

---
"""
    
    # 保存周报
    os.makedirs('output/weekly', exist_ok=True)
    report_file = f'output/weekly/report_week{week_num}.md'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"周报已生成: {report_file}")
    return report_file

if __name__ == '__main__':
    generate_weekly_report()
