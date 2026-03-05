import os
import requests
from datetime import datetime
from openai import OpenAI
import json

def main():
    # 从环境变量读取API Key（安全）
    api_key = os.getenv('KIMI_API_KEY')
    if not api_key:
        print("错误：未设置 KIMI_API_KEY")
        return
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.moonshot.cn/v1"
    )
    
    # 今天的日期
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"开始生成 {today} 的政策监控报告...")
    
    # 提示词（你可以修改监控关键词）
    prompt = """请搜索并分析今天发布的以下领域政策信息：
1. 城市更新/城市生命线
2. 公路安全韧性提升/公路安全运营  
3. 地质灾害监测/城市地质
4. 水库大坝安全监测
5. 地铁施工期监测

请搜索关键词："城市更新政策"、"城市生命线试点"、"公路安全韧性"、"地质灾害监测"、"水库大坝安全监测"、"地铁施工监测"

输出要求：
1. 只保留过去24小时发布的内容
2. 每条政策格式：
   【标签：政策/竞品/项目】政策名称（发布机构）
   - 核心变化：50字内概括
   - 对我司影响：高/中/低  
   - 建议动作：需要谁配合
   - 原文链接
   
3. 如无重要政策，回复："今日无重大政策更新"
4. 最后加："本周累计监控：X条，已闭环：Y条"
"""
    
    try:
        # 调用Kimi K2模型（支持联网搜索）
        response = client.chat.completions.create(
            model="kimi-k2-0905-preview",  # 或 kimi-k2-turbo-preview
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        result = response.choices[0].message.content
        print("获取成功，正在保存...")
        
        # 创建reports文件夹（如果不存在）
        if not os.path.exists('reports'):
            os.makedirs('reports')
        
        # 保存为markdown文件
        filename = f'reports/{today}_policy_report.md'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f'# 市场情报日报 - {today}\n\n')
            f.write(result)
            f.write(f'\n\n---\n生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        
        print(f"报告已保存：{filename}")
        
    except Exception as e:
        print(f"出错了：{e}")
        # 即使出错也生成空报告，防止GitHub Actions失败
        with open(f'reports/{today}_error.md', 'w') as f:
            f.write(f'# 生成失败 - {today}\n错误信息：{e}')

if __name__ == "__main__":
    main()
