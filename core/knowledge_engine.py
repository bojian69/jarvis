#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库引擎 - 核心业务逻辑
"""

import logging
from typing import List, Dict, Optional
from .document_processor import DocumentProcessor
from .vector_manager import VectorManager
from .query_engine import QueryEngine
from models.llm_interface import LLMInterface

class KnowledgeEngine:
    def __init__(self, config: Dict):
        self.config = config
        self.doc_processor = DocumentProcessor(config)
        self.vector_manager = VectorManager(config)
        self.query_engine = QueryEngine(config)
        self.llm = LLMInterface(config)
        
        logging.info("知识库引擎初始化完成")
    
    def add_document(self, file_path: str, doc_type: str) -> Dict:
        """添加文档到知识库"""
        try:
            # 1. 处理文档
            doc_data = self.doc_processor.process_document(file_path, doc_type)
            
            # 2. 向量化存储
            result = self.vector_manager.add_document(doc_data)
            
            return {"success": True, "doc_id": result["doc_id"]}
        except Exception as e:
            logging.error(f"添加文档失败: {e}")
            return {"success": False, "error": str(e)}
    
    def query(self, question: str, top_k: int = 5) -> Dict:
        """查询知识库"""
        try:
            # 先检查是否是元查询（关于知识库本身的问题）
            meta_result = self.handle_meta_query(question)
            if meta_result:
                return meta_result
            
            # 1. 检索相关文档
            docs = self.query_engine.search(question, top_k)
            
            # 2. 生成回答
            answer = self.llm.generate_answer(question, docs)
            
            # 3. 准备来源信息，按文档分组
            sources_by_doc = {}
            for doc in docs:
                source = doc["source"]
                if source not in sources_by_doc:
                    sources_by_doc[source] = {
                        "source": source,
                        "content": doc["content"][:150],
                        "score": doc.get("score", 0)
                    }
                else:
                    # 如果同一文档有多个片段，合并内容
                    existing_content = sources_by_doc[source]["content"]
                    new_content = doc["content"][:150]
                    if new_content not in existing_content:
                        sources_by_doc[source]["content"] = existing_content + "..." + new_content
            
            return {
                "answer": answer,
                "sources": list(sources_by_doc.values())[:3]  # 最多显示3个不同文档的来源
            }
        except Exception as e:
            logging.error(f"查询失败: {e}")
            return {"answer": "查询出错，请稍后重试", "sources": []}
    
    def get_stats(self) -> Dict:
        """获取知识库统计"""
        return self.vector_manager.get_stats()
    
    def list_documents(self) -> List[Dict]:
        """列出所有文档"""
        return self.vector_manager.list_documents()
    
    def handle_meta_query(self, question: str) -> Dict:
        """处理元查询（关于知识库本身的问题）"""
        question_lower = question.lower()
        
        # 检测是否是关于知识库的问题
        meta_keywords = ['知识库', '文档', '有哪些', '包含', '存储', '上传', '统计']
        if any(keyword in question_lower for keyword in meta_keywords):
            stats = self.get_stats()
            documents = self.list_documents()
            
            if stats.get('document_count', 0) == 0:
                answer = """## 📁 知识库状态

目前知识库为 **空**，没有上传任何文档。

### 📝 如何使用
1. **上传文档**: 点击上方的“上传文档”按钮
2. **支持格式**: PDF、Markdown (.md) 文件
3. **开始提问**: 上传后即可基于文档内容提问

### ✨ 功能特性
- 🔍 **智能检索**: 基于语义的文档搜索
- 🤖 **AI问答**: 结合多个文档片段综合回答
- 📊 **Markdown支持**: 丰富的格式化展示"""
            else:
                answer_parts = [f"## 📁 知识库概览\n"]
                answer_parts.append(f"📊 **统计信息**")
                answer_parts.append(f"- 文档数量: **{stats['document_count']}** 个")
                answer_parts.append(f"- 文本片段: **{stats['total_chunks']}** 个\n")
                
                answer_parts.append("📄 **已上传文档**")
                for i, doc in enumerate(documents, 1):
                    doc_type_icon = "📝" if doc['type'] == 'markdown' else "📰"
                    answer_parts.append(f"{i}. {doc_type_icon} **{doc['filename']}**")
                    answer_parts.append(f"   - 类型: {doc['type'].upper()}")
                    answer_parts.append(f"   - 片段: {doc['chunks']} 个")
                    answer_parts.append(f"   - 预览: {doc['sample_content']}\n")
                
                answer_parts.append("💡 **使用建议**")
                answer_parts.append("- 可以针对以上文档内容提问")
                answer_parts.append("- 系统会自动检索相关信息并综合回答")
                
                answer = '\n'.join(answer_parts)
            
            return {
                "answer": answer,
                "sources": [{"source": "知识库系统", "content": "系统内置信息"}]
            }
        
        return None