import os
import sys
import json
import datetime
import csv
import requests

# 跨周导入设置
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath
weekpath.load_env()

# 配置 API
API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/v1/chat/completions"

# ================= 1. 定义 3 个工具 =================
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_pinyin_tones(pinyin_str):
    demo_dict = {
        "ni hao": "nǐ hǎo",
        "zhong guo": "zhōng guó",
        "xue xi": "xué xí",
        "yu gong yi shan": "yú gōng yí shān"
    }
    if pinyin_str.lower() in demo_dict:
        return f"拼音 '{pinyin_str}' 加上声调后是: {demo_dict[pinyin_str.lower()]}"
    return f"词库中未收录拼音 '{pinyin_str}'。"

def query_hsk_level(word):
    csv_path = os.path.join(os.path.dirname(__file__), "..", "week03_Python", "生词表.csv")
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['词语'] == word:
                    return f"{word} 的词性是 {row['词性']}，等级是 {row['等级']}"
        return f"词库中未找到 '{word}'"
    except Exception as e:
        return f"读取词库失败: {e}"

# ================= 2. 工具说明 =================
tools_schema = [
    {"type": "function", "function": {"name": "get_current_time", "description": "获取当前时间", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "add_pinyin_tones", "description": "拼音加声调", "parameters": {"type": "object", "properties": {"pinyin_str": {"type": "string"}}, "required": ["pinyin_str"]}}},
    {"type": "function", "function": {"name": "query_hsk_level", "description": "查词汇HSK等级", "parameters": {"type": "object", "properties": {"word": {"type": "string"}}, "required": ["word"]}}}
]

# ================= 3. 核心循环逻辑（支持多步连环调用） =================
def agent_chat(user_question):
    print(f"\n🙋 你: {user_question}")
    messages = [{"role": "user", "content": user_question}]
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    # 多步循环，最多循环 5 次
    for step in range(5):
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "tools": tools_schema,
            "temperature": 0.1
        }
        
        resp = requests.post(URL, json=payload, headers=headers)
        message = resp.json()["choices"][0]["message"]
        
        # 如果模型没有要求调用工具，说明准备好最终回答了
        if not message.get("tool_calls"):
            print(f"🤖 助手最终回答:\n{message['content']}")
            print("-" * 50)
            return message['content']

        # 把模型要求调用的意图存进历史
        messages.append(message)
        
        # 处理模型发出的所有工具调用
        for tool_call in message["tool_calls"]:
            func_name = tool_call["function"]["name"]
            args = json.loads(tool_call["function"]["arguments"])
            
            print(f"--- [轨迹记录] 第 {step+1} 步，模型决定调用工具: {func_name} ---")
            print(f"--- [轨迹记录] 传入参数: {args} ---")
            
            # 执行真实的本地函数
            if func_name == "get_current_time":
                tool_result = get_current_time()
            elif func_name == "add_pinyin_tones":
                tool_result = add_pinyin_tones(args.get("pinyin_str", ""))
            elif func_name == "query_hsk_level":
                tool_result = query_hsk_level(args.get("word", ""))
            else:
                tool_result = "未知工具"
                
            print(f"--- [轨迹记录] 工具返回结果: {tool_result} ---")
            
            # 把工具执行结果塞回给模型
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": tool_result
            })
            
    print("❌ 达到最大循环次数，强制结束。")
    print("-" * 50)
    return ""

if __name__ == "__main__":
    # 1. 单独问：查时间
    agent_chat("现在北京时间几点？学生马上要上晚自习了。")
    
    # 2. 单独问：拼音加调
    agent_chat("帮我把拼音 'yu gong yi shan' 加上声调。")
    
    # 3. 单独问：查词表
    agent_chat("'著名' 这个词是 HSK 几级词汇？")
    
    # 4. 连环问（多步调用）：同时查时间和词汇
    agent_chat("现在北京时间几点了？顺便帮我查一下'著名'这个词是几级词汇？")