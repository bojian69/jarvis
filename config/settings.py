#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统配置
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 服务器配置
SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8080,
    "debug": True
}

# 存储配置
STORAGE_CONFIG = {
    "documents_path": Path("/Volumes/common/jarvis/documents"),
    "vector_db_path": Path("/Volumes/common/jarvis/vector_db"),
    "uploads_path": Path("/Volumes/common/jarvis/uploads"),
    "cache_path": Path("/Volumes/common/jarvis/cache")
}

# 模型配置
MODEL_CONFIG = {
    "llm_url": "http://localhost:11434",
    "llm_model": "qwen2.5:7b",
    "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2"
}

# 文档处理配置
DOCUMENT_CONFIG = {
    "max_file_size": 50 * 1024 * 1024,  # 50MB
    "supported_types": ["pdf", "markdown"],
    "chunk_size": 500,
    "chunk_overlap": 50
}

# 搜索配置
SEARCH_CONFIG = {
    "default_top_k": 3,
    "max_top_k": 10,
    "relevance_threshold": 0.3,  # 相关性阈值
    "keyword_weight": 0.3,       # 关键词权重
    "vector_weight": 0.7,        # 向量相似度权重
    "max_summary_length": 600,   # 总结最大长度
    "use_smart_summary": True    # 启用智能总结
}

def get_config() -> dict:
    """获取完整配置"""
    return {
        **SERVER_CONFIG,
        **STORAGE_CONFIG,
        **MODEL_CONFIG,
        **DOCUMENT_CONFIG,
        **SEARCH_CONFIG
    }