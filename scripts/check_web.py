#!/usr/bin/env python3
# 检查网页文件

import os
import json
from datetime import datetime
import glob

def check_web_files():
    """检查网页文件"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    print("🔍 检查网页文件...")
    
    # 检查docs目录
    docs_files = []
    for root, dirs, files in os.walk('docs'):
        for file in files:
            filepath = os.path.join(root, file)
            relpath = os.path.relpath(filepath, 'docs')
            size = os.path.getsize(filepath)
            docs_files.append({
                'path': relpath,
                'size': size,
                'full_url': f'https://d7pj9kj4pq-hash.github.io/-ai-robotics-daily/{relpath}'
            })
    
    # 生成文件列表JSON
    files_json = {
        'last_checked': datetime.now().isoformat(),
        'total_files': len(docs_files),
        'files': docs_files[:50]  # 只显示前50个文件
    }
    
    with open('docs/files.json', 'w', encoding='utf-8') as f:
        json.dump(files_json, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 找到 {len(docs_files)} 个文件")
    print(f"📄 文件列表已保存到: docs/files.json")
    
    # 生成简单的HTML索引
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>文件索引 - AI机器人日报</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; }
        .file { padding: 10px; border-bottom: 1px solid #eee; }
        .file a { color: #0066cc; text-decoration: none; }
        .file a:hover { text-decoration: underline; }
        .size { color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>📁 AI机器人日报文件索引</h1>
    <p>最后更新: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
    <div id="file-list">
"""
    
    for file_info in docs_files:
        html_content += f"""
        <div class="file">
            <a href="/-ai-robotics-daily/{file_info['path']}" target="_blank">{file_info['path']}</a>
            <span class="size">({file_info['size']} bytes)</span>
        </div>
"""
    
    html_content += """
    </div>
    <script>
        // 自动加载files.json
        fetch('./files.json')
            .then(r => r.json())
            .then(data => {
                console.log('文件列表:', data);
            });
    </script>
</body>
</html>
"""
    
    with open('docs/file-index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"🌐 索引页面: docs/file-index.html")
    
    # 检查关键文件
    key_files = [
        'docs/index.html',
        'docs/daily/2025-12-17.md',
        'docs/daily/2025-12-18.md',
        'docs/images/2025-12-17/info.json',
        'docs/images/2025-12-18/info.json'
    ]
    
    for file in key_files:
        if os.path.exists(file):
            print(f"✅ {file} - 存在")
        else:
            print(f"❌ {file} - 不存在")
    
    return True

if __name__ == '__main__':
    check_web_files()
