#!/usr/bin/env python3
"""简单测试文档处理"""

import sys
sys.path.append('.')

from core.document_processor import DocumentProcessor
from config.settings import get_config

def test_document_processing():
    config = get_config()
    processor = DocumentProcessor(config)
    
    # 测试处理markdown文件
    md_file = "/Volumes/common/jarvis/documents/markdown/setup_guide.md"
    print("📄 处理markdown文件...")
    
    try:
        doc_data = processor.process_document(md_file, "markdown")
        print(f"文档ID: {doc_data['doc_id']}")
        print(f"文件名: {doc_data['filename']}")
        print(f"文本长度: {len(doc_data['text'])}")
        print(f"分块数量: {len(doc_data['chunks'])}")
        print(f"前200字符: {doc_data['text'][:200]}...")
        
        print("\n📝 文档分块:")
        for i, chunk in enumerate(doc_data['chunks'][:3]):
            print(f"块 {i+1}: {chunk[:100]}...")
            
    except Exception as e:
        print(f"处理失败: {e}")

if __name__ == "__main__":
    test_document_processing()