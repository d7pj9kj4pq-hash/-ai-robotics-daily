#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成脚本 - 优化版
生成Markdown报告和导出文件
"""

import json
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        # 创建必要的目录
        os.makedirs('output/daily', exist_ok=True)
        os.makedirs('docs/daily', exist_ok=True)
        os.makedirs('output/export', exist_ok=True)
    
    def generate_daily_report(self):
        """生成每日报告"""
        today = datetime.now().strftime('%Y-%m-%d')
        input_file = f'output/daily/processed_{today}.json'
        
        if not os.path.exists(input_file):
            print(f"未找到处理后的资讯文件: {input_file}")
            # 尝试使用原始数据
            input_file = f'output/daily/news_{today}.json'
            if not os.path.exists(input_file):
                print(f"也没有原始新闻文件")
                return None
        
        # 读取数据
        with open(input_file, 'r', encoding='utf-8') as f:
            news_items = json.load(f)
        
        # 生成Markdown报告
        markdown_report = self._generate_markdown_report(today, news_items)
        
        # 生成小红书导出文件
        xhs_export = self._export_for_xiaohongshu(today, news_items)
        
        # 生成抖音导出文件
        dy_export = self._export_for_douyin(today, news_items)
        
        print(f"✅ 报告生成完成!")
        print(f"  日报: output/daily/report_{today}.md")
        print(f"  小红书导出: output/export/xiaohongshu_{today}.txt")
        print(f"  抖音导出: output/export/douyin_{today}.txt")
        
        return markdown_report
    
    def _generate_markdown_report(self, date, news_items):
        """生成Markdown格式报告"""
        
        report = f"""# 🤖 AI与机器人日报 {date}

> 自动生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> 共收集到 {len(news_items)} 条资讯

---

"""
        
        for i, item in enumerate(news_items[:8], 1):  # 只展示前8条
            title = item.get('title', '')
            summary = item.get('ai_summary', item.get('summary', '暂无摘要'))
            source = item.get('source', '未知')
            link = item.get('link', '#')
            
            # 获取小红书内容（如果有）
            xhs_content = item.get('xhs_content', '')
            
            report += f"""## {i}. {title}

**来源**: {source}
**发布时间**: {item.get('published', '未知')}

**摘要**: {summary}

"""
            
            if xhs_content and xhs_content != "生成失败":
                report += f"""**小红书文案**:{xhs_content[:300]}...
            report += f"""**原文链接**: [点击查看]({link})
        report += f"""
## 📊 今日统计

- **资讯总数**: {len(news_items)} 条
- **主要来源**: {', '.join(set([item.get('source', '') for item in news_items if item.get('source')]))}
- **生成方式**: GitHub Actions + AI处理

## 🎯 发布建议

### 小红书发布
1. 使用生成的 `xiaohongshu_{date}.txt` 文件
2. 每篇配1-2张相关图片
3. 发布时间: 11:00-13:00 或 19:00-21:00

### 抖音发布
1. 使用生成的 `douyin_{date}.txt` 脚本
2. 制作15-30秒短视频
3. 添加热门话题和BGM

> 本报告由自动化系统生成，数据来源于公开科技资讯。
"""
        
        # 保存Markdown文件
        report_file = f'output/daily/report_{date}.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 同时保存到docs目录
        docs_file = f'docs/daily/{date}.md'
        with open(docs_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report
    
    def _export_for_xiaohongshu(self, date, news_items):
        """生成小红书导出文件"""
        export_content = f"""# 小红书AI日报发布稿 - {date}
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
# 共 {len(news_items)} 篇，建议每天发布2-3篇

"""
        
        for i, item in enumerate(news_items[:5], 1):  # 只导出前5篇
            title = item.get('title', '')
            xhs_content = item.get('xhs_content', '')
            
            if xhs_content and xhs_content != "生成失败":
                export_content += f"""\n{'='*60}
第{i}篇: {title[:30]}...

{xhs_content}

---
"""
            else:
                # 如果没有AI生成的内容，使用摘要
                summary = item.get('ai_summary', item.get('summary', ''))
                export_content += f"""\n{'='*60}
第{i}篇: {title[:30]}...

🤖 {title}

{summary[:200]}...

#AI日报 #{item.get('source', '科技')} #人工智能

---
"""
        
        export_file = f'output/export/xiaohongshu_{date}.txt'
        with open(export_file, 'w', encoding='utf-8') as f:
            f.write(export_content)
        
        return export_content
    
    def _export_for_douyin(self, date, news_items):
        """生成抖音导出文件"""
        export_content = f"""# 抖音短视频脚本 - {date}
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

"""
        
        for i, item in enumerate(news_items[:3], 1):  # 只导出前3篇
            title = item.get('title', '')
            summary = item.get('ai_summary', item.get('summary', ''))
            
            export_content += f"""\n{'='*60}
视频{i}: {title[:20]}...

【开头5秒】
(动态画面+大字标题)
{title}

【10秒核心】
(快速切换画面)
{summary[:100]}

【结尾5秒】
(提问互动)
你对这个AI技术感兴趣吗？
评论区告诉我！

#AI科技 #{item.get('source', '科技')}
---
"""
        
        export_file = f'output/export/douyin_{date}.txt'
        with open(export_file, 'w', encoding='utf-8') as f:
            f.write(export_content)
        
        return export_content

def main():
    generator = ReportGenerator()
    generator.generate_daily_report()

if __name__ == '__main__':
    main()
