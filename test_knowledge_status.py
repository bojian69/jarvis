#!/usr/bin/env python3
"""测试知识库状态查询功能"""

import sys
sys.path.append('.')

from core.knowledge_engine import KnowledgeEngine
from config.settings import get_config

def test_knowledge_status():
    """测试知识库状态查询"""
    config = get_config()
    engine = KnowledgeEngine(config)
    
    print("🔍 测试知识库状态查询...")
    
    # 测试元查询
    meta_questions = [
        "你现在有哪些知识库",
        "知识库里有什么文档",
        "包含哪些内容",
        "有多少文档",
        "知识库统计"
    ]
    
    for question in meta_questions:
        print(f"\n❓ 问题: {question}")
        print("-" * 50)
        
        try:
            result = engine.query(question)
            print("🤖 AI回答:")
            print(result["answer"])
            
            if result["sources"]:
                print(f"\n📚 参考来源:")
                for source in result["sources"]:
                    print(f"- {source['source']}")
            
        except Exception as e:
            print(f"❌ 查询失败: {e}")
        
        print("\n" + "="*60)

def test_direct_stats():
    """直接测试统计功能"""
    config = get_config()
    engine = KnowledgeEngine(config)
    
    print("\n📊 直接获取知识库统计:")
    stats = engine.get_stats()
    print(f"统计结果: {stats}")
    
    print("\n📋 文档列表:")
    docs = engine.list_documents()
    if docs:
        for doc in docs:
            print(f"- {doc['filename']} ({doc['type']}, {doc['chunks']} 片段)")
    else:
        print("暂无文档")

if __name__ == "__main__":
    test_direct_stats()
    test_knowledge_status()