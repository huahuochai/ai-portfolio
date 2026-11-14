# 官方 RAG 流水线与我的代码映射表
| 行 | 官方流水线 | 第三列：我原本代码里的设计 (rag_qa.py) |
| 1 | Load + Split | 使用 `TextLoader` 读取文件，`RecursiveCharacterTextSplitter` 切割（chunk_size=500, overlap=50）。 |
| 2 | Embed + Store | 使用 `OllamaEmbeddings` 嵌入，存入本地 `Chroma` 向量库并持久化。 |
| 3 | Retrieve | 使用 `get_retriever().invoke(question)` 检索，top-k=3。 |
| 4 | Prompt + Generate | 使用 `build_prompt()` 拼接资料，调 `llm.ask()` 生成。 |
| 5 | Deploy + Evaluate | W7完成了幻觉对照表评估；后续计划用网页部署。 |