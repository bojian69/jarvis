# 🤖 Jarvis AI 本地文档知识库

> 企业级本地化文档智能问答系统，支持PDF/Markdown文档上传，基于向量检索和本地LLM实现智能问答

## ✨ 核心特性

- 📄 **多格式支持**: PDF、Markdown文档智能解析
- 🧠 **本地LLM**: 集成Ollama，支持Qwen2.5等中文优化模型
- 🔍 **语义检索**: 基于向量相似度的智能文档检索
- 💾 **向量存储**: ChromaDB持久化向量数据库
- 🌐 **Web界面**: 实时交互的现代化界面
- 🔒 **数据安全**: 完全本地化部署，数据不出本地

## 🏗️ 系统架构

```
📁 jarvis/
├── 🧠 core/           # 核心业务逻辑
│   ├── knowledge_engine.py    # 知识库引擎
│   ├── document_processor.py  # 文档处理器
│   ├── vector_manager.py      # 向量管理器
│   └── query_engine.py        # 查询引擎
├── 🤖 models/         # AI模型层
│   ├── llm_interface.py       # LLM接口
│   └── embedding_model.py     # 嵌入模型
├── 💾 storage/        # 数据存储
│   ├── documents/             # 文档存储
│   ├── vector_db/             # 向量数据库
│   └── uploads/               # 临时上传
└── ⚙️ config/         # 配置管理
```

## 🚀 快速开始

### 1. 环境准备
```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装Ollama (macOS)
brew install ollama

# 下载中文模型
ollama pull qwen2.5:7b
```

### 2. 初始化存储
```bash
# 初始化外挂存储目录
python scripts/init_storage.py
```

### 3. 启动服务
```bash
# 启动Ollama服务
ollama serve

# 启动Jarvis AI
python app.py
```

### 4. 使用系统
- 访问: http://localhost:8080
- 上传PDF或Markdown文档
- 基于文档内容智能问答

## 📊 技术栈

| 组件 | 技术选型 | 说明 |
|------|----------|------|
| **后端框架** | Flask + SocketIO | 轻量级Web框架，支持实时通信 |
| **向量数据库** | ChromaDB | 开源向量数据库，易于部署 |
| **文档处理** | PyPDF2 + Markdown | PDF和Markdown解析 |
| **嵌入模型** | sentence-transformers | 多语言文本向量化 |
| **本地LLM** | Ollama + Qwen2.5 | 本地大语言模型服务 |
| **前端** | HTML5 + JavaScript | 现代化Web界面 |

## 🔧 配置说明

### 模型配置 (config/settings.py)
```python
MODEL_CONFIG = {
    "llm_url": "http://localhost:11434",     # Ollama服务地址
    "llm_model": "qwen2.5:7b",              # 使用的LLM模型
    "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2"  # 嵌入模型
}
```

### 存储配置 (外挂磁盘)
```python
STORAGE_CONFIG = {
    "documents_path": "/Volumes/common/jarvis/documents",    # 文档存储
    "vector_db_path": "/Volumes/common/jarvis/vector_db",    # 向量数据库
    "uploads_path": "/Volumes/common/jarvis/uploads",        # 临时上传
    "cache_path": "/Volumes/common/jarvis/cache"             # 缓存文件
}
```

### 推荐模型选择
| 内存要求 | 推荐模型 | 特点 |
|----------|----------|------|
| 4GB | qwen2.5:1.5b | 轻量级，响应快 |
| 8GB | qwen2.5:7b | 平衡性能和资源 |
| 16GB+ | qwen2.5:14b | 高质量回答 |

## 📈 使用流程

1. **文档上传** → 系统解析PDF/MD文件
2. **文本分块** → 智能切分长文档
3. **向量化** → 生成文本嵌入向量
4. **存储** → 保存到ChromaDB
5. **查询** → 用户提问触发语义检索
6. **生成** → LLM基于检索结果生成回答

## 📝 详细文档

- [部署指南](setup_guide.md) - 详细的环境配置和部署说明
- [项目架构](project_structure.md) - 完整的系统架构设计
- [API文档](api/README.md) - 接口使用说明

## 🤝 贡献

欢迎提交Issue和Pull Request来改进项目！

## 📄 许可证

MIT License

---

**🎯 适用场景**: 企业文档管理、个人知识库、学术研究、技术文档问答