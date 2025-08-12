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
    
    def query(self, question: str, top_k: int = 3) -> Dict:
        """查询知识库"""
        try:
            # 1. 检索相关文档
            docs = self.query_engine.search(question, top_k)
            
            # 2. 生成回答
            answer = self.llm.generate_answer(question, docs)
            
            return {
                "answer": answer,
                "sources": [{"content": doc["content"][:200], "source": doc["source"]} for doc in docs]
            }
        except Exception as e:
            logging.error(f"查询失败: {e}")
            return {"answer": "查询出错，请稍后重试", "sources": []}
    
    def get_stats(self) -> Dict:
        """获取知识库统计"""
        return self.vector_manager.get_stats()