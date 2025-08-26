#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker环境配置 - 支持环境变量配置
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

def get_env_bool(key: str, default: bool = False) -> bool:
    """获取布尔类型环境变量"""
    value = os.getenv(key, str(default)).lower()
    return value in ('true', '1', 'yes', 'on')

def get_env_int(key: str, default: int) -> int:
    """获取整数类型环境变量"""
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default

def get_env_float(key: str, default: float) -> float:
    """获取浮点类型环境变量"""
    try:
        return float(os.getenv(key, str(default)))
    except ValueError:
        return default

# 服务器配置
SERVER_CONFIG = {
    "host": os.getenv("JARVIS_HOST", "0.0.0.0"),
    "port": get_env_int("JARVIS_PORT", 8080),
    "debug": get_env_bool("JARVIS_DEBUG", False)
}

# 存储配置 - 支持环境变量覆盖
STORAGE_CONFIG = {
    "documents_path": Path(os.getenv("JARVIS_DOCUMENTS_PATH", "/data/documents")),
    "vector_db_path": Path(os.getenv("JARVIS_VECTOR_DB_PATH", "/data/vector_db")),
    "uploads_path": Path(os.getenv("JARVIS_UPLOADS_PATH", "/data/uploads")),
    "cache_path": Path(os.getenv("JARVIS_CACHE_PATH", "/data/cache")),
    "logs_path": Path(os.getenv("JARVIS_LOGS_PATH", "/data/logs"))
}

# 模型配置
MODEL_CONFIG = {
    "llm_url": os.getenv("JARVIS_LLM_URL", "http://host.docker.internal:11434"),
    "llm_model": os.getenv("JARVIS_LLM_MODEL", "qwen2.5:7b"),
    "embedding_model": os.getenv("JARVIS_EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")
}

# 文档处理配置
DOCUMENT_CONFIG = {
    "max_file_size": get_env_int("JARVIS_MAX_FILE_SIZE", 50 * 1024 * 1024),  # 50MB
    "supported_types": ["pdf", "markdown"],
    "chunk_size": get_env_int("JARVIS_CHUNK_SIZE", 500),
    "chunk_overlap": get_env_int("JARVIS_CHUNK_OVERLAP", 50)
}

# 搜索配置
SEARCH_CONFIG = {
    "default_top_k": get_env_int("JARVIS_DEFAULT_TOP_K", 3),
    "max_top_k": get_env_int("JARVIS_MAX_TOP_K", 10),
    "relevance_threshold": get_env_float("JARVIS_RELEVANCE_THRESHOLD", 0.1),
    "keyword_weight": get_env_float("JARVIS_KEYWORD_WEIGHT", 0.3),
    "vector_weight": get_env_float("JARVIS_VECTOR_WEIGHT", 0.7),
    "max_summary_length": get_env_int("JARVIS_MAX_SUMMARY_LENGTH", 600),
    "use_smart_summary": get_env_bool("JARVIS_USE_SMART_SUMMARY", True)
}

# 日志配置
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "log_file": STORAGE_CONFIG["logs_path"] / "jarvis.log",
    "max_file_size": get_env_int("LOG_MAX_FILE_SIZE", 10 * 1024 * 1024),  # 10MB
    "backup_count": get_env_int("LOG_BACKUP_COUNT", 5)
}

def get_config() -> dict:
    """获取完整配置"""
    # 确保所有目录存在
    for path in STORAGE_CONFIG.values():
        if isinstance(path, Path):
            path.mkdir(parents=True, exist_ok=True)
    
    return {
        **SERVER_CONFIG,
        **STORAGE_CONFIG,
        **MODEL_CONFIG,
        **DOCUMENT_CONFIG,
        **SEARCH_CONFIG,
        **LOGGING_CONFIG
    }

# 配置验证
def validate_config():
    """验证配置有效性"""
    config = get_config()
    
    # 检查必要的目录权限
    for key, path in STORAGE_CONFIG.items():
        if isinstance(path, Path):
            try:
                path.mkdir(parents=True, exist_ok=True)
                # 测试写权限
                test_file = path / ".test_write"
                test_file.touch()
                test_file.unlink()
            except Exception as e:
                print(f"警告: 无法访问 {key} 目录 {path}: {e}")
    
    # 检查端口范围
    if not (1 <= config["port"] <= 65535):
        raise ValueError(f"端口号无效: {config['port']}")
    
    # 检查文件大小限制
    if config["max_file_size"] <= 0:
        raise ValueError(f"最大文件大小无效: {config['max_file_size']}")
    
    print("✅ 配置验证通过")
    return True

if __name__ == "__main__":
    # 配置测试
    validate_config()
    config = get_config()
    print("🔧 当前配置:")
    for key, value in config.items():
        print(f"  {key}: {value}")