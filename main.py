import os
from datetime import datetime
from openai import OpenAI

def main():
    # 1. 确保 reports 目录存在（解决 FileNotFoundError）
    os.makedirs('reports', exist_ok=True)
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    try:
        # 2. 初始化客户端（兼容 Kimi API）
        api_key = os.environ.get("KIMI_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API Key 未设置")
            
        client = OpenAI(
            api_key=api_key,
            base_url=os.environ.get("API_BASE_URL", "https://api.moonshot.cn/v1")  # 默认为 Kimi
        )
        
        # 你的业务逻辑...
        response = client.chat.completions.create(...)
        
    except Exception as e:
        # 3. 错误日志现在可以安全写入
        error_msg = f"Error: {str(e)}\n\nTraceback: {traceback.format_exc()}"
        with open(f'reports/{today}_error.md', 'w', encoding='utf-8') as f:
            f.write(f"# 执行错误报告 - {today}\n\n{error_msg}")
        raise

if __name__ == "__main__":
    main()
