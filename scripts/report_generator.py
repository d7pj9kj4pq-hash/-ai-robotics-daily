#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI日报报告生成器 - 简化版
"""

import json
import os
from datetime import datetime

def main():
    """主函数"""
    print("开始生成日报...")
    
    # 创建目录
    os.makedirs('output/daily', exist_ok=True)
    os.makedirs('output/export', exist_ok=True)
    os.makedirs('docs/daily', exist_ok=True)
    
    # 获取今天日期
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 尝试读取处理后的数据
    processed_file = f'output/daily/processed_{today}.json'
    news_file = f'output/daily/news_{today}.json'
    
    if os.path.exists(processed_file):
        input_file = processed_file
    elif os.path.exists(news_file):
        input_file = news_file
    else:
        print(f"没有找到今天的新闻文件")
        return
    
    print(f"读取文件: {input_file}")
    
    # 读取数据
    with open(input_file, 'r', encoding='utf-8') as f:
        news_items = json.load(f)
    
    print(f"找到 {len(news_items)} 条新闻")
    
    # 生成Markdown报告
    markdown = generate_markdown_report(today, news_items)
    
    # 保存报告
    report_file = f'output/daily/report_{today}.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    # 保存到docs目录
    docs_file = f'docs/daily/{today}.md'
    with open(docs_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    # 生成小红书导出
    xhs_content = generate_xiaohongshu_export(today, news_items)
    xhs_file = f'output/export/xiaohongshu_{today}.txt'
    with open(xhs_file, 'w', encoding='utf-8') as f:
        f.write(xhs_content)

    # 获取最新图片
        image_dir = f'output/images/{date}'
        if os.path.exists(image_dir):
            # 查找最新的PNG图片
            import glob
            image_files = glob.glob(f'{image_dir}/*.png')
            if image_files:
                # 取前3张图片
                for img_idx, img_path in enumerate(image_files[:3], 1):
                    img_filename = os.path.basename(img_path)
                    report += f"![AI图片{img_idx}]({img_path})\n\n"
        else:
            report += "> 注：图片生成中...\n\n"
    
    print(f"✅ 报告生成成功！")
    print(f"   日报: {report_file}")
    print(f"   小红书导出: {xhs_file}")

def generate_markdown_report(date, news_items):
    """生成Markdown报告"""
    
    report = f"""# 🤖 AI与机器人日报 {date}

> 自动生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> 共收集到 {len(news_items)} 条资讯

---

"""
    
    for i, item in enumerate(news_items[:8], 1):
        title = item.get('title', '无标题')
        summary = item.get('ai_summary', item.get('summary', '暂无摘要'))
        source = item.get('source', '未知')
        link = item.get('link', '#')
        
        report += f"## {i}. {title}\n\n"
        report += f"**来源**: {source}\n"
        report += f"**发布时间**: {item.get('published', '未知')}\n\n"
        report += f"**摘要**: {summary}\n\n"
        
        # 如果有小红书内容
        xhs_content = item.get('xhs_content', '')
        if xhs_content and xhs_content != "生成失败":
            report += "**小红书文案**:\n"
            report += "```\n"
            report += f"{xhs_content[:300]}\n"
            report += "```\n\n"
        
        report += f"**原文链接**: [点击查看]({link})\n\n"
        report += "---\n\n"
    
    # 统计信息
    sources = []
    for item in news_items:
        source = item.get('source', '')
        if source and source not in sources:
            sources.append(source)
    
    report += f"""## 📊 今日统计

- **资讯总数**: {len(news_items)} 条
- **主要来源**: {', '.join(sources[:5])}
- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🎯 发布建议

1. **小红书**: 使用生成的小红书文案，配1-2张相关图片
2. **抖音**: 制作15-30秒短视频，突出核心数据
3. **微博**: 使用摘要部分，添加热门话题

> 本报告由自动化系统生成，仅供学习参考。
"""
    
    return report

def generate_xiaohongshu_export(date, news_items):
    """生成小红书导出内容"""
    
    content = f"""# 小红书AI日报发布稿 - {date}
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
# 共 {len(news_items)} 篇，建议每天发布2-3篇

"""
    
    for i, item in enumerate(news_items[:5], 1):
        title = item.get('title', '')
        
        content += f"\n{'='*60}\n"
        content += f"第{i}篇: {title[:40]}\n\n"
        
        xhs_content = item.get('xhs_content', '')
        if xhs_content and xhs_content != "生成失败":
            content += f"{xhs_content}\n"
        else:
            summary = item.get('ai_summary', item.get('summary', ''))
            content += f"🤖 {title}\n\n"
            content += f"{summary[:200]}\n\n"
            content += f"#AI日报 #{item.get('source', '科技')} #人工智能\n"
        
        content += f"\n配图建议: 科技感图片1-2张\n"
        content += f"发布时间: 建议间隔2-3小时\n"
        content += "---\n"
    
    return content

if __name__ == '__main__':
    main()
