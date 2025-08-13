#!/usr/bin/env python3
"""测试知识库文档检索功能"""

import sys
sys.path.append('.')

from core.knowledge_engine import KnowledgeEngine
from config.settings import get_config

def test_knowledge_retrieval():
    """测试知识库检索功能"""
    config = get_config()
    engine = KnowledgeEngine(config)
    
    # 测试添加markdown文档
    md_file = "/Volumes/common/jarvis/documents/markdown/setup_guide.md"
    print("📄 添加文档到知识库...")
    result = engine.add_document(md_file, "markdown")
    print(f"添加结果: {result}")
    
    # 测试查询
    questions = [
        "如何安装Ollama？",
        "推荐什么模型？",
        "文件存储结构是什么？",
        "轻量级模型有哪些？"
    ]
    
    print("\n🔍 测试查询功能:")
    for question in questions:
        print(f"\n问题: {question}")
        answer = engine.query(question)
        print(f"回答: {answer['answer'][:200]}...")
        print(f"来源数量: {len(answer['sources'])}")

if __name__ == "__main__":
    test_knowledge_retrieval()