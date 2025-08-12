# AI配置 (可选)
OPENAI_API_KEY = "your-api-key-here"  # 如需OpenAI集成

# 本地模型配置
LOCAL_LLM_URL = "http://localhost:11434"  # Ollama服务地址
LOCAL_LLM_MODEL = "qwen2.5:7b"  # 使用的模型

# 知识库配置
KNOWLEDGE_DB_PATH = "./knowledge_db"  # 向量数据库路径
DOCUMENT_STORAGE_PATH = "./documents"  # 文档存储路径
MAX_FILE_SIZE = 50 * 1024 * 1024  # 最大文件大小 50MB

# 服务器配置
HOST = "0.0.0.0"
PORT = 8080

# 浏览器默认页面
DEFAULT_URL = "https://www.google.com"