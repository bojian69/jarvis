#!/usr/bin/env python3
"""测试多文档整合回答功能"""

import sys
sys.path.append('.')

from core.knowledge_engine import KnowledgeEngine
from config.settings import get_config

def test_multi_document_query():
    """测试多文档查询整合"""
    config = get_config()
    engine = KnowledgeEngine(config)
    
    print("🔍 测试多文档整合查询功能...")
    
    # 测试查询
    test_questions = [
        "如何安装和配置系统？",
        "系统有哪些核心特性？",
        "技术架构是什么样的？",
        "如何使用这个系统？"
    ]
    
    for question in test_questions:
        print(f"\n❓ 问题: {question}")
        print("-" * 50)
        
        try:
            result = engine.query(question, top_k=5)
            
            print("🤖 AI回答:")
            print(result["answer"])
            
            if result["sources"]:
                print(f"\n📚 参考来源 ({len(result['sources'])} 个文档):")
                for i, source in enumerate(result["sources"], 1):
                    print(f"{i}. {source['source']}")
                    if 'score' in source:
                        print(f"   相似度: {source['score']:.2f}")
            
            print("\n" + "="*60)
            
        except Exception as e:
            print(f"❌ 查询失败: {e}")

def test_knowledge_stats():
    """测试知识库统计"""
    config = get_config()
    engine = KnowledgeEngine(config)
    
    print("\n📊 知识库统计信息:")
    stats = engine.get_stats()
    print(f"文档数量: {stats.get('document_count', 0)}")
    print(f"向量数量: {stats.get('vector_count', 0)}")

if __name__ == "__main__":
    test_knowledge_stats()
    test_multi_document_query()