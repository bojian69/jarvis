#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量管理器 - 处理文档向量化和存储
"""

import chromadb
from typing import Dict, List
from models.embedding_model import EmbeddingModel

class VectorManager:
    def __init__(self, config: Dict):
        self.config = config
        self.client = chromadb.PersistentClient(path=config["vector_db_path"])
        self.collection = self.client.get_or_create_collection("documents")
        self.embedding_model = EmbeddingModel(config)
    
    def add_document(self, doc_data: Dict) -> Dict:
        """添加文档到向量数据库"""
        doc_id = doc_data["doc_id"]
        chunks = doc_data["chunks"]
        
        # 生成向量
        embeddings = self.embedding_model.encode(chunks)
        
        # 准备数据
        ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
        metadatas = [{
            "doc_id": doc_id,
            "filename": doc_data["filename"],
            "type": doc_data["type"],
            "chunk_id": i
        } for i in range(len(chunks))]
        
        # 存储到向量数据库
        self.collection.add(
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        
        return {"doc_id": doc_id, "chunks_added": len(chunks)}
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """向量搜索"""
        query_embedding = self.embedding_model.encode([query])[0]
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        documents = []
        for i in range(len(results['documents'][0])):
            documents.append({
                'content': results['documents'][0][i],
                'source': results['metadatas'][0][i]['filename'],
                'type': results['metadatas'][0][i]['type'],
                'score': 1 - results['distances'][0][i]  # 转换为相似度分数
            })
        
        return documents
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {"total_chunks": self.collection.count()}