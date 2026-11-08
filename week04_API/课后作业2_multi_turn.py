import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath
weekpath.load_env()

import openai

BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"

_client = None

def get_client():
    global _client
    if _client is None:
        key = os.getenv("DEEPSEEK_API_KEY")
        if not key:
            raise RuntimeError("未配置DEEPSEEK_API_KEY")
        _client = openai.OpenAI(base_url=BASE_URL, api_key=key)
    return _client

# 核心修改点：用一个列表来充当“记忆”
history_messages = []

def ask_with_memory(question):
    global history_messages
    
    # 1. 把用户的新问题存进记忆
    history_messages.append({"role": "user", "content": question})
    
    # 2. 把包含所有历史记录的记忆发给 API
    r = get_client().chat.completions.create(
        model=MODEL,
        messages=history_messages,  # 这里传的是历史记录列表
        temperature=0.7,
        max_tokens=500
    )
    
    # 3. 获取 AI 的回答，并存入记忆，供下一轮使用
    answer = r.choices[0].message.content
    history_messages.append({"role": "assistant", "content": answer})
    
    return answer

if __name__ == "__main__":
    print("=== 多轮对话测试开始（输入 'exit' 退出） ===")
    
    # 我们可以预设一个场景来测试它的记忆力
    # 第一轮
    q1 = "我想写一篇关于《愚公移山》的教案，帮我列两个教学目标。"
    print(f"\n[我]: {q1}")
    a1 = ask_with_memory(q1)
    print(f"[AI]: {a1}")
    
    # 第二轮（注意：这一句里没有提愚公移山，看看它能不能根据上一轮记住）
    q2 = "把刚才的第一个目标扩写成一段具体的教学活动。"
    print(f"\n[我]: {q2}")
    a2 = ask_with_memory(q2)
    print(f"[AI]: {a2}")
    
    print("\n=== 测试结束：如果第二轮的回答依然是关于《愚公移山》的，说明多轮记忆成功！ ===")