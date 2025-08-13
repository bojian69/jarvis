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
        
        # 使用内存数据库避免兼容性问题
        try:
            self.client = chromadb.Client()
            self.collection = self.client.get_or_create_collection("documents")
        except:
            # 备用方案：简单存储
            self.client = None
            self.collection = None
            self.documents = []
        
        self.embedding_model = EmbeddingModel(config)
    
    def add_document(self, doc_data: Dict) -> Dict:
        """添加文档到向量数据库"""
        doc_id = doc_data["doc_id"]
        chunks = doc_data["chunks"]
        
        # 生成向量
        embeddings = self.embedding_model.encode(chunks)
        
        if self.collection:
            # 使用ChromaDB
            ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
            metadatas = [{
                "doc_id": doc_id,
                "filename": doc_data["filename"],
                "type": doc_data["type"],
                "chunk_id": i
            } for i in range(len(chunks))]
            
            self.collection.add(
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
        else:
            # 备用存储
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                self.documents.append({
                    'id': f"{doc_id}_{i}",
                    'content': chunk,
                    'embedding': embedding,
                    'metadata': {
                        'doc_id': doc_id,
                        'filename': doc_data['filename'],
                        'type': doc_data['type']
                    }
                })
        
        return {"doc_id": doc_id, "chunks_added": len(chunks)}
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """向量搜索"""
        query_embedding = self.embedding_model.encode([query])[0]
        
        if self.collection:
            # 使用ChromaDB搜索
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
                    'score': 1 - results['distances'][0][i]
                })
        else:
            # 备用搜索：简单余弦相似度
            import numpy as np
            documents = []
            
            for doc in self.documents:
                # 计算余弦相似度
                similarity = np.dot(query_embedding, doc['embedding']) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(doc['embedding'])
                )
                
                documents.append({
                    'content': doc['content'],
                    'source': doc['metadata']['filename'],
                    'type': doc['metadata']['type'],
                    'score': float(similarity)
                })
            
            # 按相似度排序
            documents.sort(key=lambda x: x['score'], reverse=True)
            documents = documents[:top_k]
        
        return documents
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        try:
            total_chunks = self.collection.count()
            
            # 获取所有文档信息
            if total_chunks > 0:
                all_results = self.collection.get()
                documents = {}
                
                for metadata in all_results['metadatas']:
                    filename = metadata['filename']
                    doc_type = metadata['type']
                    if filename not in documents:
                        documents[filename] = {
                            'type': doc_type,
                            'chunks': 0
                        }
                    documents[filename]['chunks'] += 1
                
                return {
                    "total_chunks": total_chunks,
                    "document_count": len(documents),
                    "documents": documents
                }
            else:
                return {
                    "total_chunks": 0,
                    "document_count": 0,
                    "documents": {}
                }
        except Exception as e:
            return {"error": str(e), "total_chunks": 0, "document_count": 0}
    
    def list_documents(self) -> List[Dict]:
        """列出所有文档"""
        try:
            all_results = self.collection.get()
            documents = {}
            
            for i, metadata in enumerate(all_results['metadatas']):
                filename = metadata['filename']
                if filename not in documents:
                    documents[filename] = {
                        'filename': filename,
                        'type': metadata['type'],
                        'doc_id': metadata['doc_id'],
                        'chunks': 0,
                        'sample_content': all_results['documents'][i][:100] + "..."
                    }
                documents[filename]['chunks'] += 1
            
            return list(documents.values())
        except Exception as e:
            return []