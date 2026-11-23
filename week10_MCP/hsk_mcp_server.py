import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath
weekpath.load_env()

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    from mcp.server import MCPServer as FastMCP

VOCAB = os.path.join(os.path.dirname(__file__), "..", "week03_Python", "生词表.csv")
mcp = FastMCP("hsk-tools")

@mcp.tool()
def hsk_level(word: str) -> str:
    """查询某个词属于 HSK 几级。"""
    with open(VOCAB, encoding="utf-8") as f:
        reader = list(csv.reader(f))
        # 忽略表头，直接按位置硬抓
        for row in reader[1:]:
            if len(row) >= 3 and row[0].strip() == str(word).strip():
                return "%s -> %s 级" % (word, row[2].strip())
    return "未找到 %s" % word

@mcp.tool()
def list_by_level(level: str) -> str:
    """列出某一 HSK 等级的全部词汇。"""
    out = []
    with open(VOCAB, encoding="utf-8") as f:
        reader = list(csv.reader(f))
        for row in reader[1:]:
            if len(row) >= 3 and row[2].strip() == str(level).strip():
                out.append(row[0].strip())
    return "、".join(out) if out else "该等级暂无词汇"

@mcp.tool()
def count_by_level(level: str) -> str:
    """统计某一 HSK 等级有多少个词汇。"""
    count = 0
    with open(VOCAB, encoding="utf-8") as f:
        reader = list(csv.reader(f))
        for row in reader[1:]:
            if len(row) >= 3 and row[2].strip() == str(level).strip():
                count += 1
    return "HSK %s 级共有 %d 个词汇" % (level, count)

if __name__ == "__main__":
    mcp.run()