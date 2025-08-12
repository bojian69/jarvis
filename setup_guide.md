# 本地知识库部署指南

## 1. 安装依赖
```bash
pip install -r requirements.txt
```

## 2. 安装本地模型 (推荐Ollama)

### 安装Ollama
```bash
# macOS
brew install ollama

# 或下载安装包: https://ollama.ai/download
```

### 下载推荐模型
```bash
# 中文能力强的模型
ollama pull qwen2.5:7b

# 或者轻量级模型
ollama pull qwen2.5:1.5b
```

### 启动Ollama服务
```bash
ollama serve
```

## 3. 文件存储结构
```
jarvis/
├── documents/          # 文档存储
│   ├── pdf/           # PDF文件
│   ├── markdown/      # Markdown文件
│   └── metadata/      # 文档元数据
├── knowledge_db/      # 向量数据库
└── uploads/          # 临时上传目录
```

## 4. 使用方式
1. 启动服务: `python app.py`
2. 访问: http://localhost:8080
3. 上传PDF或MD文件
4. 基于文档内容提问

## 5. 模型选择建议

### 轻量级 (4GB内存)
- qwen2.5:1.5b
- gemma2:2b

### 标准配置 (8GB内存)
- qwen2.5:7b
- llama3.1:8b

### 高性能 (16GB内存)
- qwen2.5:14b
- llama3.1:70b