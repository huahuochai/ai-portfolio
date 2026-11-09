# 官方 RAG 流水线与我的 rag_qa.py 映射表

1. **加载 (Document Loading)**：官方流水线使用 Document Loaders 读取文件。对应我代码里的 `TextLoader(CORPUS, encoding="utf-8")`，读取了本地的《等级标准》文件。
2. **分块 (Splitting)**：官方使用 Text Splitters 切割长文本。对应我代码里的 `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)`，把长文本切成了 500 字一段。
3. **向量化存储 (Storage)**：官方使用 Embeddings + VectorStore 存入数据库。对应我代码里的 `OllamaEmbeddings` 将文本转为向量，并由 `Chroma.from_documents` 存入本地 `chroma_db` 文件夹。
4. **检索 (Retrieval)**：官方使用 Retriever 来查询。对应我代码里的 `get_retriever().invoke(question)`，根据用户的提问，在向量库中找出最相似的 3 个片段。
5. **生成 (Generation)**：官方将上下文填入 Prompt 交给 LLM。对应我代码里的 `build_prompt` 把资料和问题拼装起来，最后交给 `llm.ask()` 双引擎去生成最终回答。