#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片生成脚本（简化版）
如果环境没有PIL库，这个脚本会跳过
"""

import os
import json
from datetime import datetime

def generate_simple_images():
    """生成简单的图片"""
    try:
        # 尝试导入PIL，如果失败就跳过
        from PIL import Image, ImageDraw, ImageFont
        has_pil = True
    except ImportError:
        print("PIL库未安装，跳过图片生成")
        has_pil = False
        return []
    
    if not has_pil:
        return []
    
    today = datetime.now().strftime('%Y-%m-%d')
    input_file = f'output/daily/processed_{today}.json'
    
    if not os.path.exists(input_file):
        print(f"未找到处理后的新闻文件: {input_file}")
        return []
    
    # 读取数据
    with open(input_file, 'r', encoding='utf-8') as f:
        news_items = json.load(f)
    
    os.makedirs(f'output/images/{today}', exist_ok=True)
    
    images_info = []
    
    # 只处理前3条新闻
    for i, item in enumerate(news_items[:3]):
        try:
            # 创建简单图片
            width, height = 800, 600
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)
            
            # 尝试使用字体
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # 绘制标题
            title = item['title']
            # 分割长标题
            lines = []
            words = title.split()
            current_line = ""
            
            for word in words:
                if len(current_line) + len(word) <= 40:
                    current_line += word + " "
                else:
                    lines.append(current_line)
                    current_line = word + " "
            
            if current_line:
                lines.append(current_line)
            
            # 绘制文本
            y = 50
            for line in lines[:4]:  # 最多4行
                draw.text((50, y), line[:50], font=font, fill='black')
                y += 40
            
            # 绘制分割线
            draw.line([(50, y+10), (width-50, y+10)], fill='gray', width=2)
            
            # 绘制来源和时间
            source_text = f"来源: {item['source']} | {today}"
            draw.text((50, y+30), source_text, font=font, fill='blue')
            
            # 保存图片
            filename = f'output/images/{today}/news_{i+1}.png'
            image.save(filename)
            
            images_info.append({
                'title': item['title'],
                'image_path': filename,
                'xhs_content': item.get('xhs_content', '')
            })
            
            print(f"已生成图片: {filename}")
            
        except Exception as e:
            print(f"生成第{i+1}张图片失败: {e}")
            continue
    
    # 保存图片信息
    if images_info:
        info_file = f'output/images/{today}/info.json'
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(images_info, f, ensure_ascii=False, indent=2)
    
    return images_info

if __name__ == '__main__':
    generate_simple_images()
