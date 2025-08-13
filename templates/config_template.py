#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{{project_name}} 配置模板
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 服务器配置
SERVER_CONFIG = {
    "host": "{{host}}",
    "port": {{port}},
    "debug": {{debug}}
}

# 存储配置
STORAGE_CONFIG = {
    "documents_path": "{{documents_path}}",
    "vector_db_path": "{{vector_db_path}}",
    "uploads_path": "{{uploads_path}}",
    "cache_path": "{{cache_path}}"
}

# 模型配置
MODEL_CONFIG = {
    "llm_url": "{{llm_url}}",
    "llm_model": "{{llm_model}}",
    "embedding_model": "{{embedding_model}}",
    "embedding_dim": {{embedding_dim}}
}

# 文档处理配置
DOCUMENT_CONFIG = {
    "max_file_size": {{max_file_size}},
    "supported_types": {{supported_types}},
    "chunk_size": {{chunk_size}},
    "chunk_overlap": {{chunk_overlap}}
}

# 搜索配置
SEARCH_CONFIG = {
    "default_top_k": {{default_top_k}},
    "max_top_k": {{max_top_k}},
    "relevance_threshold": {{relevance_threshold}},
    "keyword_weight": {{keyword_weight}},
    "vector_weight": {{vector_weight}}
}

# 安全配置
SECURITY_CONFIG = {
    "secret_key": os.environ.get('FLASK_SECRET_KEY', '{{default_secret_key}}'),
    "max_content_length": {{max_content_length}},
    "allowed_extensions": {{allowed_extensions}}
}

def get_config() -> dict:
    """获取完整配置"""
    return {
        **SERVER_CONFIG,
        **STORAGE_CONFIG,
        **MODEL_CONFIG,
        **DOCUMENT_CONFIG,
        **SEARCH_CONFIG,
        **SECURITY_CONFIG
    }