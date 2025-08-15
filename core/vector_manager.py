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
        db_path = str(config["vector_db_path"])
        
        # 确保目录存在且有写权限
        import os
        from pathlib import Path
        Path(db_path).mkdir(parents=True, exist_ok=True)
        os.chmod(db_path, 0o755)
        
        # 禁用遥测以避免错误日志
        import os
        os.environ['ANONYMIZED_TELEMETRY'] = 'False'
        
        self.client = chromadb.PersistentClient(path=db_path)
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
    
    def get_document_content(self, filename: str) -> str:
        """从向量数据库获取文档内容"""
        try:
            if self.collection:
                # 获取所有数据
                all_results = self.collection.get()
                
                # 查找匹配的文件
                content_parts = []
                for i, metadata in enumerate(all_results['metadatas']):
                    if metadata['filename'] == filename:
                        content_parts.append(all_results['documents'][i])
                
                if content_parts:
                    # 合并所有片段
                    return '\n\n'.join(content_parts)
            else:
                # 备用存储
                content_parts = []
                for doc in self.documents:
                    if doc['metadata']['filename'] == filename:
                        content_parts.append(doc['content'])
                
                if content_parts:
                    return '\n\n'.join(content_parts)
            
            return None
        except Exception as e:
            logging.error(f"获取文档内容失败: {e}")
            return None