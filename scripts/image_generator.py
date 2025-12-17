#!/usr/bin/env python3
# 极简图片生成器

import os
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def main():
    """生成3张简单的图片"""
    today = datetime.now().strftime('%Y-%m-%d')
    image_dir = f'output/images/{today}'
    
    # 创建目录
    if os.path.exists(image_dir):
        import shutil
        shutil.rmtree(image_dir)
    
    os.makedirs(image_dir, exist_ok=True)
    
    images_info = []
    
    # 3种不同的颜色
    colors = [
        (70, 130, 180),   # 钢蓝色
        (220, 100, 100),  # 珊瑚红
        (100, 180, 100)   # 草绿色
    ]
    
    for i in range(1, 4):
        try:
            # 创建图片
            width, height = 800, 800
            img = Image.new('RGB', (width, height), color=colors[i-1])
            draw = ImageDraw.Draw(img)
            
            # 绘制边框
            draw.rectangle([(50, 50), (width-50, height-50)], 
                          outline=(255, 255, 255), width=10)
            
            # 绘制圆形
            circle_size = 200
            circle_x = width // 2
            circle_y = height // 2 - 50
            draw.ellipse([(circle_x-circle_size//2, circle_y-circle_size//2),
                         (circle_x+circle_size//2, circle_y+circle_size//2)],
                        outline=(255, 255, 255), width=5)
            
            # 绘制AI图标
            # 三角形
            triangle_points = [
                (circle_x, circle_y - 80),
                (circle_x - 60, circle_y + 40),
                (circle_x + 60, circle_y + 40)
            ]
            draw.polygon(triangle_points, fill=(255, 255, 255))
            
            # 添加文字
            try:
                font = ImageFont.truetype("Arial", 40)
            except:
                font = ImageFont.load_default()
            
            # 编号
            draw.text((circle_x, circle_y + 120), f"#{i}", 
                     fill=(255, 255, 255), font=font, anchor="mm")
            
            # 日期
            draw.text((circle_x, height - 100), today, 
                     fill=(200, 200, 200), font=font, anchor="mm")
            
            # 保存
            filename = f'{image_dir}/news_{i}.png'
            img.save(filename)
            
            images_info.append({
                'index': i,
                'filename': f'news_{i}.png',
                'path': filename
            })
            
            print(f"✅ 生成图片: {filename}")
            
        except Exception as e:
            print(f"❌ 生成图片{i}失败: {e}")
    
    # 保存图片信息
    info_file = f'{image_dir}/info.json'
    with open(info_file, 'w', encoding='utf-8') as f:
        json.dump(images_info, f, ensure_ascii=False, indent=2)
    
    print(f"🎯 图片生成完成！共 {len(images_info)} 张")
    return images_info

if __name__ == '__main__':
    main()
