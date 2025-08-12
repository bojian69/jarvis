#!/usr/bin/env python3
"""简单的文本嵌入实现，不依赖外部模型"""

import hashlib
import numpy as np
from typing import List

class SimpleEmbedding:
    """简单的文本嵌入实现"""
    
    def __init__(self, dim=384):
        self.dim = dim
    
    def encode(self, texts):
        """将文本转换为向量"""
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = []
        for text in texts:
            # 使用哈希和字符统计生成向量
            hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
            np.random.seed(hash_val % (2**32))
            embedding = np.random.normal(0, 1, self.dim)
            embeddings.append(embedding)
        
        return np.array(embeddings)

def test_embedding():
    """测试嵌入功能"""
    model = SimpleEmbedding()
    test_texts = ["你好", "世界", "测试"]
    embeddings = model.encode(test_texts)
    print(f"嵌入成功！维度: {embeddings.shape}")
    return True

if __name__ == "__main__":
    test_embedding()