import os
import sys
import json
import traceback
from datetime import datetime
from openai import OpenAI

# ==================== 第1步：自动创建文件夹（解决 FileNotFoundError）====================
# 获取当前文件所在目录，确保 reports 文件夹存在
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)  # 自动创建，如果已存在则不报错

# ==================== 第2步：配置 API（解决 401 认证错误）====================
# 从环境变量读取 API Key（GitHub Secrets 会自动注入到这里）
API_KEY = os.environ.get("KIMI_API_KEY") or os.environ.get("OPENAI_API_KEY")

# 检查 API Key 是否存在
if not API_KEY:
    print("❌ 错误：没有找到 API Key")
    print("请检查 GitHub Secrets 是否设置了 KIMI_API_KEY 或 OPENAI_API_KEY")
    sys.exit(1)

# 初始化 AI 客户端
# 注意：如果使用 Kimi(月之暗面)，必须设置 base_url；如果用 OpenAI 官方，删除 base_url 这行
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.moonshot.cn/v1"  # ← Kimi API 地址，如果用 OpenAI 请删除这行
)

# ==================== 第3步：业务逻辑（你原来的代码）====================
def search_policies():
    """
    这里放你原来的"搜索政策"代码
    如果没有特殊逻辑，可以删除这个函数
    """
    # 示例：返回今天日期
    today = datetime.now().strftime('%Y-%m-%d')
    return today

def generate_report(date_str):
    """
    生成政策监控报告
    如果有原来的生成逻辑，把代码放在这里
    """
    try:
        # 调用 AI 生成报告
        response = client.chat.completions.create(
            model="moonshot-v1-8k",  # Kimi 模型名，如果用 OpenAI 改为 "gpt-3.5-turbo" 等
            messages=[
                {"role": "system", "content": "你是政策分析专家，负责生成每日政策监控简报。"},
                {"role": "user", "content": f"请生成 {date_str} 的城市更新、地质灾害监测、基础设施相关政策监控报告，包括：1）政策名称+发布机构；2）核心变化；3）影响评级；4）建议动作"}
            ],
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        
        # 保存到 reports 文件夹（现在肯定不会报 FileNotFoundError 了）
        report_path = os.path.join(REPORTS_DIR, f'{date_str}_report.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# 政策监控报告 - {date_str}\n\n{content}")
        
        print(f"✅ 报告已生成：{report_path}")
        return True
        
    except Exception as e:
        # 如果 AI 调用失败，保存错误信息到文件
        error_path = os.path.join(REPORTS_DIR, f'{date_str}_error.md')
        with open(error_path, 'w', encoding='utf-8') as f:
            f.write(f"# 执行错误 - {date_str}\n\n")
            f.write(f"错误类型：{type(e).__name__}\n")
            f.write(f"错误信息：{str(e)}\n\n")
            f.write("详细堆栈：\n```\n")
            f.write(traceback.format_exc())
            f.write("\n```")
        
        print(f"❌ 执行出错，错误日志已保存：{error_path}")
        raise  # 继续抛出错误，让 GitHub Actions 显示失败

# ==================== 第4步：主程序入口（保持原有结构）====================
def main():
    print("开始生成政策监控报告...")
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"日期：{today}")
    
    try:
        # 这里调用你原来的业务逻辑
        generate_report(today)
        print("✅ 全部完成！")
        
    except Exception as e:
        print(f"❌ 程序异常：{e}")
        sys.exit(1)  # 非零退出码让 GitHub Actions 显示红色失败

if __name__ == "__main__":
    main()
