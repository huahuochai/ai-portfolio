import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # 告诉客户端如何启动服务端
    params = StdioServerParameters(command="D:\\python314\\python.exe", args=["hsk_mcp_server.py"])
    
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            
            # 第一步：发现工具
            tools = await s.list_tools()
            print("\n=== 发现工具列表 ===")
            print([t.name for t in tools.tools])
            
            # 第二步：调用工具测试
            print("\n=== 调用工具测试 ===")
            res1 = await s.call_tool("hsk_level", {"word": "把"})
            print("hsk_level('把') 返回:", res1.content[0].text)
            
            res2 = await s.call_tool("list_by_level", {"level": "3"})
            print("list_by_level('3') 返回:", res2.content[0].text)
            
            # 测试你新加的第3个工具
            res3 = await s.call_tool("count_by_level", {"level": "3"})
            print("count_by_level('3') 返回:", res3.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())