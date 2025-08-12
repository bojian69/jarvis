# 🏗️ 本地文档知识库 - 项目架构

## 📁 目录结构
```
jarvis/
├── 📂 core/                    # 核心业务逻辑
│   ├── knowledge_engine.py    # 知识库引擎
│   ├── document_processor.py  # 文档处理器
│   ├── vector_manager.py      # 向量管理器
│   └── query_engine.py        # 查询引擎
├── 📂 api/                     # API接口层
│   ├── routes.py              # 路由定义
│   ├── handlers.py            # 请求处理器
│   └── middleware.py          # 中间件
├── 📂 web/                     # 前端界面
│   ├── static/                # 静态资源
│   │   ├── css/
│   │   ├── js/
│   │   └── assets/
│   └── templates/             # HTML模板
├── 📂 models/                  # 模型层
│   ├── llm_interface.py       # LLM接口
│   ├── embedding_model.py     # 嵌入模型
│   └── model_manager.py       # 模型管理器
├── 📂 storage/                 # 数据存储
│   ├── documents/             # 文档存储
│   │   ├── pdf/              # PDF文件
│   │   ├── markdown/         # Markdown文件
│   │   └── raw/              # 原始文件
│   ├── vector_db/            # 向量数据库
│   ├── uploads/              # 临时上传
│   └── cache/                # 缓存文件
├── 📂 utils/                   # 工具函数
│   ├── file_utils.py         # 文件操作
│   ├── text_utils.py         # 文本处理
│   └── logger.py             # 日志工具
├── 📂 config/                  # 配置文件
│   ├── settings.py           # 系统配置
│   ├── model_config.py       # 模型配置
│   └── database_config.py    # 数据库配置
├── 📂 tests/                   # 测试文件
│   ├── test_core/
│   ├── test_api/
│   └── test_models/
├── 📂 logs/                    # 日志文件
├── app.py                     # 应用入口
├── requirements.txt           # 依赖包
└── README.md                  # 项目说明
```

## 🔧 技术栈
- **后端**: Flask + SocketIO
- **向量数据库**: ChromaDB
- **文档处理**: PyPDF2, python-markdown
- **嵌入模型**: sentence-transformers
- **本地LLM**: Ollama (Qwen2.5)
- **前端**: HTML5 + JavaScript + CSS3

## 🚀 核心功能模块

### 1. 文档处理引擎
- PDF文本提取和解析
- Markdown格式处理
- 文档分块和预处理
- 元数据提取和管理

### 2. 向量化引擎
- 多语言文本嵌入
- 向量索引构建
- 相似度计算
- 增量更新支持

### 3. 查询引擎
- 语义搜索
- 混合检索(关键词+向量)
- 结果排序和过滤
- 上下文聚合

### 4. 生成引擎
- 本地LLM集成
- 提示词工程
- 流式响应
- 多轮对话支持