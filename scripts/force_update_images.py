#!/usr/bin/env python3
# 强制更新图片脚本

import os
import sys
from datetime import datetime

def force_update():
    """强制更新所有图片"""
    print("开始强制更新图片...")
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 1. 删除旧的图片目录
    image_dir = f'output/images/{today}'
    if os.path.exists(image_dir):
        import shutil
        shutil.rmtree(image_dir)
        print(f"已删除: {image_dir}")
    
    # 2. 运行图片生成脚本
    print("运行图片生成脚本...")
    os.system('python scripts/image_generator_v2.py')
    
    # 3. 验证结果
    if os.path.exists(image_dir):
        files = os.listdir(image_dir)
        print(f"✅ 更新成功！生成文件: {len(files)} 个")
        for f in files:
            print(f"  - {f}")
    else:
        print("❌ 更新失败，目录未创建")
    
    return 0

if __name__ == '__main__':
    sys.exit(force_update())
