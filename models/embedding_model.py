#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
嵌入模型 - 文本向量化
"""

import numpy as np
from typing import List
import logging

class EmbeddingModel:
    def __init__(self, config: dict):
        self.model = None
        self.dim = 384
        
        try:
            from sentence_transformers import SentenceTransformer
            model_name = config.get("embedding_model", "paraphrase-multilingual-MiniLM-L12-v2")
            self.model = SentenceTransformer(model_name)
            self.dim = self.model.get_sentence_embedding_dimension()
            logging.info(f"使用语义嵌入模型: {model_name}, 维度: {self.dim}")
        except ImportError:
            logging.warning("sentence-transformers未安装，使用简化嵌入模型")
            self.dim = config.get("embedding_dim", 384)
        except Exception as e:
            logging.warning(f"加载嵌入模型失败: {e}，使用简化模型")
    
    def encode(self, texts: List[str]) -> List[List[float]]:
        """将文本编码为向量"""
        try:
            if self.model:
                # 使用真正的语义嵌入模型
                embeddings = self.model.encode(texts)
                return embeddings.tolist()
            else:
                # 备用：基于词汇的简单相似度
                return self._simple_encode(texts)
        except Exception as e:
            logging.error(f"文本编码失败: {e}")
            return self._simple_encode(texts)
    
    def _simple_encode(self, texts: List[str]) -> List[List[float]]:
        """简单的基于词汇的编码"""
        embeddings = []
        for text in texts:
            # 基于词汇特征的简单向量化
            words = text.lower().split()
            vector = np.zeros(self.dim)
            
            for i, word in enumerate(words[:50]):  # 最多处理50个词
                # 为每个词生成特征
                word_hash = hash(word) % self.dim
                vector[word_hash] += 1.0
                
                # 添加位置权重
                if i < len(vector):
                    vector[i] += 0.5
            
            # 归一化
            if np.linalg.norm(vector) > 0:
                vector = vector / np.linalg.norm(vector)
            
            embeddings.append(vector.tolist())
        
        return embeddings