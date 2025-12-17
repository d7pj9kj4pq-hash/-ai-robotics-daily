#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片生成脚本 V2 - 强制更新版
确保每次生成新图片
"""

import os
import json
import random
from datetime import datetime
from PIL import Image, ImageDraw

def create_colorful_image(index, date_str, title=""):
    """创建彩色图片，避免字体问题"""
    # 小红书尺寸
    width, height = 750, 1000
    
    # 随机生成颜色
    bg_color = (
        random.randint(30, 100),    # R
        random.randint(50, 150),    # G  
        random.randint(100, 200)    # B
    )
    
    # 创建图片
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # 绘制顶部色块
    header_color = (
        random.randint(100, 200),
        random.randint(100, 200),
        random.randint(100, 200)
    )
    draw.rectangle([(0, 0), (width, 200)], fill=header_color)
    
    # 绘制中心圆
    circle_color = (255, 255, 255)
    circle_x = width // 2
    circle_y = height // 2
    circle_radius = 100
    
    draw.ellipse([
        (circle_x - circle_radius, circle_y - circle_radius),
        (circle_x + circle_radius, circle_y + circle_radius)
    ], fill=circle_color, outline=(0, 0, 0), width=3)
    
    # 绘制AI图标
    # 绘制三角形（代表AI）
    triangle_points = [
        (circle_x, circle_y - 60),
        (circle_x - 40, circle_y + 40),
        (circle_x + 40, circle_y + 40)
    ]
    draw.polygon(triangle_points, fill=(70, 130, 180))
    
    # 绘制机器人图标
    # 身体
    body_y = circle_y + 150
    draw.rectangle([(circle_x-60, body_y), (circle_x+60, body_y+80)], 
                   fill=(220, 100, 100), outline=(0, 0, 0), width=2)
    # 头部
    draw.rectangle([(circle_x-30, body_y-40), (circle_x+30, body_y)], 
                   fill=(220, 100, 100), outline=(0, 0, 0), width=2)
    # 天线
    draw.line([(circle_x, body_y-40), (circle_x, body_y-80)], 
              fill=(255, 200, 0), width=3)
    draw.ellipse([(circle_x-5, body_y-85), (circle_x+5, body_y-75)], 
                 fill=(255, 200, 0))
    
    # 绘制编号
    draw.text((circle_x, body_y+120), f"#{index}", 
              fill=(255, 255, 255), anchor="mm")
    
    # 绘制日期
    date_text = date_str
    draw.text((width // 2, height - 80), date_text, 
              fill=(200, 200, 200), anchor="mm")
    
    # 绘制类型标签
    type_text = "AI & ROBOTICS"
    draw.text((width // 2, height - 50), type_text, 
              fill=(255, 255, 255), anchor="mm")
    
    return img

def main():
    """主函数"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 创建目录（强制清空旧图片）
    image_dir = f'output/images/{today}'
    
    # 删除旧目录（如果存在）
    if os.path.exists(image_dir):
        import shutil
        shutil.rmtree(image_dir)
        print(f"已删除旧图片目录: {image_dir}")
    
    # 创建新目录
    os.makedirs(image_dir, exist_ok=True)
    print(f"创建新目录: {image_dir}")
    
    # 生成3张图片
    images_info = []
    for i in range(1, 4):
        try:
            # 生成唯一文件名（包含时间戳）
            timestamp = datetime.now().strftime('%H%M%S')
            filename = f'{image_dir}/news_{i}_{timestamp}.png'
            
            # 创建图片
            title = f"AI Robotics News {i}"
            img = create_colorful_image(i, today, title)
            img.save(filename)
            
            images_info.append({
                'index': i,
                'filename': os.path.basename(filename),
                'path': filename,
                'generated_at': datetime.now().isoformat()
            })
            
            print(f"✅ 生成图片: {filename}")
            
        except Exception as e:
            print(f"❌ 生成图片 {i} 失败: {e}")
    
    # 保存图片信息
    info_file = f'{image_dir}/info.json'
    with open(info_file, 'w', encoding='utf-8') as f:
        json.dump(images_info, f, ensure_ascii=False, indent=2)
    
    # 创建标记文件（表示图片已更新）
    marker_file = f'{image_dir}/.updated'
    with open(marker_file, 'w') as f:
        f.write(datetime.now().isoformat())
    
    print(f"🎯 图片生成完成！共 {len(images_info)} 张")
    
    # 验证文件存在
    if os.path.exists(image_dir):
        files = os.listdir(image_dir)
        print(f"📁 目录内容: {files}")
    
    return images_info

if __name__ == '__main__':
    main()
