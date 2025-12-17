#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI日报报告生成器 - 最终修复版
完全消除类定义错误
"""

import json
import os
import glob
import shutil
from datetime import datetime

def main():
    """主函数"""
    print("开始生成日报...")
    
    # 创建目录
    os.makedirs('output/daily', exist_ok=True)
    os.makedirs('output/export', exist_ok=True)
    os.makedirs('docs/daily', exist_ok=True)
    os.makedirs('docs/images', exist_ok=True)
    
    # 获取今天日期
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"今天是: {today}")
    
    # 尝试读取处理后的数据
    processed_file = f'output/daily/processed_{today}.json'
    news_file = f'output/daily/news_{today}.json'
    
    if os.path.exists(processed_file):
        input_file = processed_file
        print(f"读取处理后的文件: {input_file}")
    elif os.path.exists(news_file):
        input_file = news_file
        print(f"读取原始新闻文件: {input_file}")
    else:
        print(f"没有找到今天的新闻文件")
        return
    
    # 读取数据
    with open(input_file, 'r', encoding='utf-8') as f:
        news_items = json.load(f)
    
    print(f"找到 {len(news_items)} 条新闻")
    
    # 获取今日图片列表
    image_files = get_today_images(today)
    
    # 生成Markdown报告
    markdown = generate_markdown_report(today, news_items, image_files)
    
    # 保存报告
    report_file = f'output/daily/report_{today}.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    # 保存到docs目录
    docs_file = f'docs/daily/{today}.md'
    with open(docs_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    # 生成小红书导出
    xhs_content = generate_xiaohongshu_export(today, news_items, image_files)
    xhs_file = f'output/export/xiaohongshu_{today}.txt'
    with open(xhs_file, 'w', encoding='utf-8') as f:
        f.write(xhs_content)
    
    # 生成抖音导出
    dy_content = generate_douyin_export(today, news_items)
    dy_file = f'output/export/douyin_{today}.txt'
    with open(dy_file, 'w', encoding='utf-8') as f:
        f.write(dy_content)
    
    # 复制图片到docs目录（用于网页显示）
    copy_images_to_docs(today, image_files)
    
    print(f"✅ 报告生成成功！")
    print(f"   日报: {report_file}")
    print(f"   小红书导出: {xhs_file}")
    print(f"   抖音导出: {dy_file}")
    
    return True

def get_today_images(today):
    """获取今日生成的图片"""
    image_dir = f'output/images/{today}'
    image_files = []
    
    if os.path.exists(image_dir):
        # 查找所有PNG图片
        png_files = glob.glob(f'{image_dir}/*.png')
        jpg_files = glob.glob(f'{image_dir}/*.jpg')
        
        # 按文件名排序
        all_files = sorted(png_files + jpg_files)
        
        for img_file in all_files[:3]:  # 只取前3张
            image_files.append({
                'path': img_file,
                'filename': os.path.basename(img_file)
            })
    
    print(f"找到 {len(image_files)} 张图片")
    return image_files

def copy_images_to_docs(today, image_files):
    """复制图片到docs目录"""
    docs_image_dir = f'docs/images/{today}'
    os.makedirs(docs_image_dir, exist_ok=True)
    
    copied_count = 0
    for img_info in image_files:
        try:
            src_path = img_info['path']
            dst_filename = img_info['filename']
            dst_path = f'{docs_image_dir}/{dst_filename}'
            
            # 复制文件
            shutil.copy2(src_path, dst_path)
            copied_count += 1
            print(f"复制图片: {dst_filename}")
            
        except Exception as e:
            print(f"复制图片失败: {e}")
    
    if copied_count > 0:
        print(f"已复制 {copied_count} 张图片到 {docs_image_dir}")

def generate_markdown_report(today, news_items, image_files):
    """生成Markdown报告"""
    
    # 获取主要来源
    sources = []
    for item in news_items:
        source = item.get('source', '')
        if source and source not in sources:
            sources.append(source)
    
    # 构建报告
    report = f"""# 🤖 AI与机器人日报 {today}

> 自动生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> 共收集到 {len(news_items)} 条资讯

"""
    
    # 如果有图片，显示图片
    if image_files:
        report += "\n## 🖼️ 今日配图\n\n"
        for i, img_info in enumerate(image_files, 1):
            img_filename = img_info['filename']
            # 使用docs目录的相对路径
            report += f"![AI图片{i}](./images/{today}/{img_filename})\n\n"
        report += "---\n\n"
    
    # 添加新闻内容
    report += "## 📰 今日精选资讯\n\n"
    
    for i, item in enumerate(news_items[:8], 1):
        title = item.get('title', '无标题')
        summary = item.get('ai_summary', item.get('summary', '暂无摘要'))
        source = item.get('source', '未知')
        link = item.get('link', '#')
        
        report += f"### {i}. {title}\n\n"
        report += f"**来源**: {source}\n"
        report += f"**发布时间**: {item.get('published', '未知')}\n\n"
        report += f"**摘要**: {summary}\n\n"
        
        # 如果有小红书内容
        xhs_content = item.get('xhs_content', '')
        if xhs_content and xhs_content != "生成失败":
            report += "**小红书文案**:\n"
            report += "```\n"
            report += f"{xhs_content[:300]}"
            if len(xhs_content) > 300:
                report += "..."
            report += "\n```\n\n"
        
        report += f"**原文链接**: [点击查看]({link})\n\n"
        report += "---\n\n"
    
    # 统计信息
    report += f"""## 📊 今日统计

- **资讯总数**: {len(news_items)} 条
- **主要来源**: {', '.join(sources[:5])}
- **图片数量**: {len(image_files)} 张
- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🎯 发布建议

### 小红书发布
1. 使用生成的小红书导出文件
2. 每篇配1-2张相关图片
3. 发布时间: 11:00-13:00 或 19:00-21:00

### 抖音发布
1. 使用生成的抖音脚本
2. 制作15-30秒短视频
3. 添加热门话题和BGM

> 本报告由自动化系统生成，仅供学习参考。
"""
    
    return report

def generate_xiaohongshu_export(today, news_items, image_files):
    """生成小红书导出内容"""
    
    content = f"""# 小红书AI日报发布稿 - {today}
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
# 共 {len(news_items)} 篇，建议每天发布2-3篇
# 可用图片: {len(image_files)} 张

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
        
        # 图片建议
        if i <= len(image_files):
            content += f"\n配图建议: 使用图片 {i} (已生成)"
        else:
            content += f"\n配图建议: 科技感图片1-2张"
        
        content += f"\n发布时间: 建议间隔2-3小时\n"
        content += "---\n"
    
    return content

def generate_douyin_export(today, news_items):
    """生成抖音导出内容"""
    
    content = f"""# 抖音短视频脚本 - {today}
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
# 共 {len(news_items)} 个主题可选

"""
    
    for i, item in enumerate(news_items[:3], 1):
        title = item.get('title', '')
        summary = item.get('ai_summary', item.get('summary', ''))
        
        content += f"\n{'='*60}\n"
        content += f"视频{i}: {title[:20]}...\n\n"
        content += "【开头5秒】\n"
        content += "(动态画面+大字标题)\n"
        content += f"{title}\n\n"
        content += "【10秒核心】\n"
        content += "(快速切换画面)\n"
        content += f"{summary[:100]}\n\n"
        content += "【结尾5秒】\n"
        content += "(提问互动)\n"
        content += "你对这个AI技术感兴趣吗？\n"
        content += "评论区告诉我！\n\n"
        content += f"#AI科技 #{item.get('source', '科技')} #人工智能\n"
        content += "---\n"
    
    return content

if __name__ == '__main__':
    main()
