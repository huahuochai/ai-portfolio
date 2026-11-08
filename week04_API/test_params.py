import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import weekpath
weekpath.load_env()

from week04_API.week4_api_bot import ask

print("=== 1. temperature=0.0 看确定性 ===")
print(ask("用一句话说明什么是把字句", temperature=0.0, max_tokens=60))

print("\n=== 2. temperature=1.5 看发散 ===")
print(ask("用一句话说明什么是把字句", temperature=1.5, max_tokens=60))

print("\n=== 3. max_tokens=15 看截断 ===")
print(ask("用一句话说明什么是把字句", temperature=0.0, max_tokens=15))
from week04_API.week4_api_bot import get_client, MODEL

r = get_client().chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "用一句话说明什么是把字句"}],
)
print("输入tokens:", r.usage.prompt_tokens)
print("输出tokens:", r.usage.completion_tokens)