# 🤖 Jarvis AI 知识库部署指南

## 📋 系统要求

- **Python**: 3.8+
- **内存**: 最低4GB，推荐8GB+
- **存储**: 10GB+ 可用空间
- **操作系统**: macOS/Linux/Windows

## 🚀 快速部署

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd jarvis

# 创建虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows
```

### 2. 安装Python依赖

```bash
# 安装基础依赖
pip install -r requirements.txt

# 安装神经网络嵌入模型 (关键!)
pip install sentence-transformers

# 可选：安装GPU支持 (如有NVIDIA GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 3. 🧠 神经网络嵌入模型配置

#### 自动下载模型 (推荐)
```bash
# 首次运行会自动下载多语言嵌入模型
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')"
```

#### 手动配置模型
```python
# config/settings.py 中配置
MODEL_CONFIG = {
    # 嵌入模型选择 (影响检索精度)
    "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2",  # 多语言支持
    # "embedding_model": "all-MiniLM-L6-v2",  # 英文优化
    # "embedding_model": "distiluse-base-multilingual-cased",  # 高精度
}
```

#### 嵌入模型选择指南

| 模型名称 | 语言支持 | 精度 | 速度 | 内存占用 | 推荐场景 |
|---------|----------|------|------|----------|----------|
| `paraphrase-multilingual-MiniLM-L12-v2` | 中英文 | 高 | 快 | 420MB | **推荐** |
| `all-MiniLM-L6-v2` | 英文 | 中 | 很快 | 80MB | 英文文档 |
| `distiluse-base-multilingual-cased` | 多语言 | 很高 | 中 | 480MB | 高精度需求 |
| `paraphrase-multilingual-mpnet-base-v2` | 多语言 | 最高 | 慢 | 1.1GB | 最佳效果 |

### 4. 🦙 本地LLM配置 (可选)

#### 安装Ollama
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: 下载安装包
# https://ollama.ai/download
```

#### 下载推荐模型
```bash
# 中文优化模型 (推荐)
ollama pull qwen2.5:7b

# 轻量级选择
ollama pull qwen2.5:1.5b

# 英文优化
ollama pull llama3.1:8b
```

#### 启动Ollama服务
```bash
# 启动服务
ollama serve

# 验证服务
curl http://localhost:11434/api/tags
```

### 5. 📁 存储结构初始化

```bash
# 运行初始化脚本
python scripts/init_storage.py

# 或手动创建目录
mkdir -p /Volumes/common/jarvis/{documents/{pdf,markdown},vector_db,uploads,cache}
```

**存储结构**:
```
/Volumes/common/jarvis/  # 可自定义路径
├── documents/
│   ├── pdf/            # PDF文档存储
│   ├── markdown/       # Markdown文档存储
│   └── raw/           # 原始文档备份
├── vector_db/         # ChromaDB向量数据库
├── uploads/           # 临时上传目录
└── cache/            # 缓存文件
```

### 6. ⚙️ 配置文件设置

编辑 `config/settings.py`:

```python
# 存储路径配置
STORAGE_CONFIG = {
    "documents_path": "/Volumes/common/jarvis/documents",
    "vector_db_path": "/Volumes/common/jarvis/vector_db",
    "uploads_path": "/Volumes/common/jarvis/uploads",
}

# 模型配置
MODEL_CONFIG = {
    # LLM配置 (可选)
    "llm_url": "http://localhost:11434",
    "llm_model": "qwen2.5:7b",
    
    # 嵌入模型配置 (必需)
    "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2",
    "embedding_dim": 384,
}

# 检索配置
SEARCH_CONFIG = {
    "relevance_threshold": 0.35,  # 相关性阈值
    "max_results": 5,           # 最大返回结果
    "keyword_weight": 0.3,      # 关键词权重
}
```

### 7. 🚀 启动服务

```bash
# 启动Jarvis AI
python app.py

# 或使用开发模式
FLASK_ENV=development python app.py
```

**访问地址**:
- 本地: http://localhost:8080
- 局域网: http://[your-ip]:8080

## 🔧 高级配置

### GPU加速 (可选)

如果有NVIDIA GPU，可以启用GPU加速：

```bash
# 安装CUDA版本的PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 验证GPU可用性
python -c "import torch; print(torch.cuda.is_available())"
```

### 模型缓存配置

```python
# 设置模型缓存目录
import os
os.environ['TRANSFORMERS_CACHE'] = '/path/to/model/cache'
os.environ['HF_HOME'] = '/path/to/huggingface/cache'
```

### 性能优化

```python
# config/settings.py
PERFORMANCE_CONFIG = {
    "batch_size": 32,           # 批处理大小
    "max_seq_length": 512,     # 最大序列长度
    "num_threads": 4,          # 线程数
    "enable_gpu": True,        # 启用GPU
}
```

## 📊 模型性能对比

### 嵌入模型性能

| 指标 | MiniLM-L12 | MiniLM-L6 | MPNet-Base |
|------|------------|-----------|------------|
| 精度 | 85% | 82% | 88% |
| 速度 | 快 | 很快 | 中等 |
| 内存 | 420MB | 80MB | 1.1GB |
| 多语言 | ✅ | ❌ | ✅ |

### LLM模型选择

| 内存要求 | 推荐模型 | 特点 | 下载大小 |
|----------|----------|------|----------|
| 4GB | qwen2.5:1.5b | 轻量快速 | 1.5GB |
| 8GB | qwen2.5:7b | **推荐平衡** | 4.1GB |
| 16GB+ | qwen2.5:14b | 高质量 | 8.2GB |

## 🛠️ 故障排除

### 常见问题

#### 1. 嵌入模型下载失败
```bash
# 手动下载
wget https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/resolve/main/pytorch_model.bin

# 或使用镜像源
export HF_ENDPOINT=https://hf-mirror.com
```

#### 2. 内存不足
```python
# 减少批处理大小
MODEL_CONFIG["batch_size"] = 16

# 使用更小的模型
MODEL_CONFIG["embedding_model"] = "all-MiniLM-L6-v2"
```

#### 3. 检索精度低
```python
# 降低相关性阈值
SEARCH_CONFIG["relevance_threshold"] = 0.2

# 增加返回结果数
SEARCH_CONFIG["max_results"] = 10
```

#### 4. 端口占用
```bash
# 查看端口占用
lsof -i :8080

# 修改端口
export PORT=8081
python app.py
```

### 验证安装

```bash
# 运行测试脚本
python test_embedding.py
python test_knowledge_status.py

# 检查服务状态
curl http://localhost:8080/stats
```

## 📚 使用指南

### 1. 文档上传
- 支持格式: PDF, Markdown (.md)
- 支持批量上传和文件夹上传
- 自动文本提取和向量化

### 2. 智能问答
- 基于语义检索的精准匹配
- 支持中英文混合查询
- Markdown格式回答展示

### 3. 知识库管理
- 实时查看文档统计
- 支持文档删除和更新
- 向量数据库管理工具

---

**🎯 部署完成后，您将拥有一个功能完整的本地AI知识库系统！**

**📞 技术支持**: 如遇问题，请查看日志文件 `logs/jarvis.log` 或提交Issue。