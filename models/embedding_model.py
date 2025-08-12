#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
嵌入模型 - 文本向量化（简单实现）
"""

import hashlib
import numpy as np
from typing import List
import logging

class EmbeddingModel:
    def __init__(self, config: dict):
        self.dim = config.get("embedding_dim", 384)
        logging.info(f"使用简单嵌入模型，维度: {self.dim}")
    
    def encode(self, texts: List[str]) -> List[List[float]]:
        """将文本编码为向量"""
        try:
            embeddings = []
            for text in texts:
                # 使用哈希生成稳定向量
                hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
                np.random.seed(hash_val % (2**32))
                embedding = np.random.normal(0, 1, self.dim)
                embeddings.append(embedding.tolist())
            return embeddings
        except Exception as e:
            logging.error(f"文本编码失败: {e}")
            raise