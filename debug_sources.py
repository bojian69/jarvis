#!/usr/bin/env python3
"""调试来源文件名问题"""

import sys
sys.path.append('.')

from core.knowledge_engine import KnowledgeEngine
from config.settings import get_config

def debug_sources():
    """调试来源文件名"""
    config = get_config()
    engine = KnowledgeEngine(config)
    
    # 获取统计信息
    stats = engine.get_stats()
    print("📊 知识库统计:")
    print(f"文档数量: {stats.get('document_count', 0)}")
    print(f"总片段: {stats.get('total_chunks', 0)}")
    
    # 列出所有文档
    docs = engine.list_documents()
    print("\n📋 文档列表:")
    for doc in docs:
        print(f"- 文件名: {doc['filename']}")
        print(f"  类型: {doc['type']}")
        print(f"  片段: {doc['chunks']}")
        print()
    
    # 测试查询
    result = engine.query("churn analysis", use_summary=False)
    print("🔍 查询结果:")
    print(f"回答: {result['answer'][:100]}...")
    print("📄 来源:")
    for source in result.get('sources', []):
        print(f"- {source['source']}")

if __name__ == "__main__":
    debug_sources()