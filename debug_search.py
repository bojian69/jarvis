#!/usr/bin/env python3
"""调试搜索功能"""

import sys
sys.path.append('.')

from core.knowledge_engine import KnowledgeEngine
from config.settings import get_config

def debug_search():
    """调试搜索功能"""
    config = get_config()
    engine = KnowledgeEngine(config)
    
    # 先查看知识库状态
    print("📊 知识库状态:")
    stats = engine.get_stats()
    print(f"文档数量: {stats.get('document_count', 0)}")
    print(f"总片段: {stats.get('total_chunks', 0)}")
    
    if stats.get('documents'):
        print("\n📋 文档列表:")
        for filename, info in stats['documents'].items():
            print(f"- {filename} ({info['type']}, {info['chunks']} 片段)")
    
    # 测试搜索
    query = "insights Churn Analysis"
    print(f"\n🔍 搜索查询: '{query}'")
    print("-" * 50)
    
    # 直接测试向量搜索
    print("1. 原始向量搜索结果:")
    raw_results = engine.vector_manager.search(query, 10)
    for i, doc in enumerate(raw_results, 1):
        print(f"{i}. 相似度: {doc.get('score', 0):.3f}")
        print(f"   来源: {doc.get('source', 'unknown')}")
        print(f"   内容: {doc.get('content', '')[:100]}...")
        print()
    
    # 测试查询引擎过滤
    print("2. 查询引擎过滤结果:")
    filtered_results = engine.query_engine.search(query, 5)
    for i, doc in enumerate(filtered_results, 1):
        print(f"{i}. 相似度: {doc.get('score', 0):.3f}")
        print(f"   来源: {doc.get('source', 'unknown')}")
        print(f"   内容: {doc.get('content', '')[:100]}...")
        print()
    
    # 测试完整查询
    print("3. 完整查询结果:")
    result = engine.query(query)
    print(f"回答: {result['answer'][:200]}...")
    print(f"来源数量: {len(result.get('sources', []))}")

if __name__ == "__main__":
    debug_search()