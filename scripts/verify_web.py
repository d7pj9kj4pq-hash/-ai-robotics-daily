#!/usr/bin/env python3
# 验证网页文件

import os
from datetime import datetime

def verify_web_files():
    """验证网页文件是否正确生成"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    print("🔍 开始验证网页文件...")
    
    # 检查docs目录结构
    required_dirs = ['docs/daily', 'docs/images']
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ 目录存在: {dir_path}")
        else:
            print(f"❌ 目录缺失: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
            print(f"   已创建目录")
    
    # 检查今日日报文件
    daily_file = f'docs/daily/{today}.md'
    if os.path.exists(daily_file):
        size = os.path.getsize(daily_file)
        print(f"✅ 日报文件存在: {daily_file} ({size}字节)")
    else:
        print(f"❌ 日报文件缺失: {daily_file}")
    
    # 检查今日图片
    image_dir = f'docs/images/{today}'
    if os.path.exists(image_dir):
        images = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        print(f"✅ 图片目录存在: {image_dir} ({len(images)}张图片)")
        for img in images[:3]:
            print(f"   - {img}")
    else:
        print(f"⚠️  图片目录缺失: {image_dir}")
    
    # 检查主页文件
    if os.path.exists('docs/index.html'):
        size = os.path.getsize('docs/index.html')
        print(f"✅ 主页文件存在: docs/index.html ({size}字节)")
    else:
        print(f"❌ 主页文件缺失: docs/index.html")
    
    # 生成简单的README
    readme_content = f"""# AI机器人日报系统

## 网页访问地址
https://您的用户名.github.io/ai-robotics-daily/

## 最新更新
- 最后检查: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 今日日报: {today}.md
- 图片数量: {len(images) if 'images' in locals() else 0}张

## 文件结构
docs/
├── index.html # 主页
├── daily/ # 日报目录
│ └── {today}.md # 今日日报
└── images/ # 图片目录
└── {today}/ # 今日图片

  
## 手动刷新
如果页面未更新，请：
1. 按 Ctrl+F5 强制刷新浏览器缓存
2. 等待GitHub Pages自动部署（通常需要1-5分钟）
3. 检查GitHub Actions是否运行成功
"""
    
    with open('docs/README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ 验证完成！")
    print(f"📝 访问地址: https://您的用户名.github.io/ai-robotics-daily/")
    print("💡 提示: GitHub Pages部署可能需要几分钟时间")

if __name__ == '__main__':
    verify_web_files()
