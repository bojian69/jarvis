#!/usr/bin/env python3
"""测试智能总结功能"""

import sys
sys.path.append('.')

from core.knowledge_engine import KnowledgeEngine
from config.settings import get_config

def test_summary():
    """测试总结功能"""
    config = get_config()
    engine = KnowledgeEngine(config)
    
    # 测试查询
    questions = [
        "如何安装Ollama？",
        "推荐什么模型？",
        "轻量级模型有哪些？"
    ]
    
    print("🔍 测试智能总结功能:")
    print("=" * 50)
    
    for question in questions:
        print(f"\n❓ 问题: {question}")
        print("-" * 30)
        
        # 使用智能总结
        result = engine.query(question, use_summary=True)
        print("📝 智能总结:")
        print(result['answer'])
        print(f"📄 来源数量: {len(result.get('sources', []))}")
        
        print()

if __name__ == "__main__":
    test_summary()