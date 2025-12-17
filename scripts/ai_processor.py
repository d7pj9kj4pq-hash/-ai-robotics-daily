#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI处理脚本 - 优化版（支持多平台格式）
"""

import os
import json
import requests
import re
from datetime import datetime

class AIProcessor:
    def __init__(self):
        self.api_key = os.getenv('ZHIPU_API_KEY')
        self.base_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        
        # 不同平台的内容模板
        self.platform_templates = {
            'xiaohongshu': {
                'emoji_prefix': '🤖',
                'hashtags': ['#AI日报', '#科技前沿', '#人工智能', '#黑科技'],
                'max_length': 600
            },
            'douyin': {
                'emoji_prefix': '🔥',
                'hashtags': ['#AI', '#科技', '#人工智能', '#知识分享'],
                'max_length': 200
            },
            'zhihu': {
                'emoji_prefix': '💡',
                'hashtags': [],
                'max_length': 1000
            }
        }
    
    def _clean_text_for_ai(self, text):
        """为AI处理清理文本"""
        if not text:
            return ""
        
        # 移除特殊字符但保留中文标点
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s，。！？、：；（）《》【】「」""''-]', '', text)
        
        # 截断到合理长度
        return text[:1000].strip()
    
    def _create_ai_prompt(self, news_item, platform='xiaohongshu'):
        """创建AI提示词"""
        title = news_item.get('title', '')
        summary = news_item.get('summary', '')
        source = news_item.get('source', '')
        
        # 清理文本
        clean_title = self._clean_text_for_ai(title)
        clean_summary = self._clean_text_for_ai(summary)
        
        platform_config = self.platform_templates.get(platform, self.platform_templates['xiaohongshu'])
        
        prompt_templates = {
            'xiaohongshu': f"""请将以下科技新闻转化为小红书风格的文案：

【原文信息】
标题：{clean_title}
来源：{source}
摘要：{clean_summary}

【具体要求】
1. 语言风格：活泼、亲切、有网感，使用emoji点缀
2. 结构：
   - 开头用吸引眼球的句子（带{platform_config['emoji_prefix']}emoji）
   - 分点列出核心亮点（用✅图标）
   - 分享个人看法或启发（用💭emoji）
   - 结尾引导互动（用👇emoji）
3. 内容要点：
   - 突出数据（如有数字要强调）
   - 说明应用场景
   - 分析行业趋势
4. 长度：{platform_config['max_length']}字以内
5. 标签：自动生成3-5个相关话题标签

请直接输出文案内容，不要加任何解释。""",
            
            'douyin': f"""请将以下科技新闻转化为抖音短视频脚本：

【原文信息】
标题：{clean_title}
摘要：{clean_summary}

【脚本要求】
1. 时长：15-30秒短视频
2. 结构：
   - 开头：悬念式（3秒吸引注意力）
   - 中间：核心信息点（快速切换画面）
   - 结尾：提问互动
3. 风格：节奏快、信息密集、有记忆点
4. 包含：画面对应描述、字幕建议、BGM建议
5. 标签：推荐热门话题标签

请输出完整脚本。"""
        }
        
        return prompt_templates.get(platform, prompt_templates['xiaohongshu'])
    
    def _extract_key_data(self, text):
        """从文本中提取关键数据"""
        data_points = []
        
        # 查找数字+单位
        patterns = [
            r'(\d+\.?\d*)\s*亿',
            r'(\d+\.?\d*)\s*万',
            r'(\d+\.?\d*)\s*%',
            r'(\d+)\s*个',
            r'(\d+)\s*位',
            r'增长\s*(\d+\.?\d*)\s*%',
            r'突破\s*(\d+)',
            r'达到\s*(\d+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            data_points.extend(matches)
        
        return data_points[:5]  # 返回前5个数据点
    
    def call_glm_api(self, prompt, max_tokens=800):
        """调用智谱GLM API"""
        if not self.api_key:
            print("⚠️ 警告：未设置ZHIPU_API_KEY，使用模拟数据")
            return "这是模拟的AI生成内容。请设置ZHIPU_API_KEY获取真实AI处理结果。"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "glm-4",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": max_tokens,
            "top_p": 0.9
        }
        
        try:
            print(f"调用AI API，prompt长度: {len(prompt)}")
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"❌ API调用失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ API调用异常: {e}")
            return None
    
    def process_news_item(self, news_item):
        """处理单条新闻"""
        print(f"处理: {news_item.get('title', '')[:50]}...")
        
        # 提取关键数据
        key_data = self._extract_key_data(news_item.get('summary', ''))
        
        # 生成小红书文案
        xhs_prompt = self._create_ai_prompt(news_item, 'xiaohongshu')
        xhs_content = self.call_glm_api(xhs_prompt, 600)
        
        # 生成抖音脚本
        dy_prompt = self._create_ai_prompt(news_item, 'douyin')
        dy_content = self.call_glm_api(dy_prompt, 400)
        
        # 生成知乎风格摘要
        zh_prompt = self._create_ai_prompt(news_item, 'zhihu')
        zh_content = self.call_glm_api(zh_prompt, 300)
        
        # 生成简单摘要（备用）
        simple_prompt = f"用一句话总结：{news_item.get('title', '')}"
        simple_summary = self.call_glm_api(simple_prompt, 100) or news_item.get('summary', '')[:150]
        
        # 构建结果
        result = {
            **news_item,
            'key_data': key_data,
            'simple_summary': simple_summary,
            'xhs_content': xhs_content or "生成失败",
            'douyin_content': dy_content or "生成失败",
            'zhihu_summary': zh_content or simple_summary,
            'processed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ai_processed': bool(xhs_content)
        }
        
        return result
    
    def process_daily_news(self):
        """处理每日资讯"""
        today = datetime.now().strftime('%Y-%m-%d')
        input_file = f'output/daily/news_{today}.json'
        
        if not os.path.exists(input_file):
            print(f"❌ 未找到今日资讯文件: {input_file}")
            return []
        
        # 读取新闻
        with open(input_file, 'r', encoding='utf-8') as f:
            news_items = json.load(f)
        
        print(f"开始处理 {len(news_items)} 条资讯...")
        
        processed_items = []
        success_count = 0
        
        for i, item in enumerate(news_items):
            print(f"[{i+1}/{len(news_items)}] ", end="")
            
            try:
                processed_item = self.process_news_item(item)
                processed_items.append(processed_item)
                
                if processed_item['ai_processed']:
                    success_count += 1
                    print("✅ 成功")
                else:
                    print("⚠️ 部分成功")
                
                # API调用间隔，避免频率限制
                import time
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ 失败: {e}")
                # 添加失败标记但保留原始数据
                item['ai_processed'] = False
                item['ai_error'] = str(e)
                processed_items.append(item)
                continue
        
        # 保存处理结果
        output_file = f'output/daily/processed_{today}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_items, f, ensure_ascii=False, indent=2)
        
        print(f"\n📊 处理完成统计:")
        print(f"  总数: {len(processed_items)}")
        print(f"  成功: {success_count}")
        print(f"  失败: {len(processed_items) - success_count}")
        print(f"  保存到: {output_file}")
        
        return processed_items

def main():
    processor = AIProcessor()
    processor.process_daily_news()

if __name__ == '__main__':
    main()
