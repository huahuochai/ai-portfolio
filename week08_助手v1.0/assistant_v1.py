import sys
import types

# ================= 强行绕开 Windows 拦截的底层补丁 =================
fake_uuid_utils = types.ModuleType("uuid_utils")
fake_uuid_utils.uuid7 = lambda: "fake-uuid"
sys.modules["uuid_utils"] = fake_uuid_utils
sys.modules["uuid_utils.compat"] = fake_uuid_utils
# ===================================================================

import os

# 跨周导入路径设置
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath
weekpath.load_env()

# 导入你前面几周造的“零件”
try:
    # 优先尝试从老师给的统一目录导入
    from week06_双引擎.llm import LLM
    from week07_RAG.rag_qa import retrieve, build_prompt
except ImportError:
    # 如果老师把它们放在同一层，就用这个
    from llm import LLM
    from rag_qa import retrieve, build_prompt

# 系统提示词（人设）
SYSTEM_HINT = "你是国际中文教学助手，面向 HSK3-4 学习者，回答需给出依据。"

def answer(question, use_rag=True, prefer="local"):
    """核心粘合层函数：根据开关决定是否走 RAG"""
    llm = LLM()
    
    if use_rag:
        # RAG 模式：先检索资料，再拼装提示词
        ctx = retrieve(question)
        prompt = SYSTEM_HINT + "\n" + build_prompt(question, ctx)
    else:
        # 纯对话模式：直接问模型
        prompt = SYSTEM_HINT + "\n" + question
        
    # 调用 W6 的双引擎接口
    return llm.ask(prompt, prefer=prefer)

def main():
    print("=" * 50)
    print("🤖 学科智能问答助手 v1.0 已启动")
    print("输入 'exit' 或 'quit' 退出程序")
    print("=" * 50)

    # 开关设置
    use_rag = True 
    prefer = "local" # 优先本地，失败自动切云端
    
    print(f"当前模式：{'📚 基于资料回答 (RAG)' if use_rag else '🧠 纯模型对话'}")
    print(f"当前引擎：{prefer}")

    while True:
        try:
            question = input("\n🙋 你: ")
            if question.lower() in ['exit', 'quit']:
                print("👋 助手已退出。")
                break
            if not question.strip():
                continue
            
            print("🤔 思考中（正在检索并生成回答）...")

            # 调用粘合层
            ans = answer(question, use_rag=use_rag, prefer=prefer)

            print(f"\n🤖 助手:\n{ans}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n👋 助手已退出。")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")

if __name__ == "__main__":
    main()