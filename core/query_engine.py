#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询引擎 - 处理用户查询和检索
"""

from typing import List, Dict
from .vector_manager import VectorManager

class QueryEngine:
    def __init__(self, config: Dict):
        self.config = config
        self.vector_manager = VectorManager(config)
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """执行搜索查询"""
        # 使用向量搜索
        results = self.vector_manager.search(query, top_k)
        
        # 可以在这里添加更多搜索策略，如关键词搜索、重排序等
        return self._rerank_results(results, query)
    
    def _rerank_results(self, results: List[Dict], query: str) -> List[Dict]:
        """重新排序搜索结果"""
        # 简单的基于分数排序，可以扩展更复杂的排序算法
        return sorted(results, key=lambda x: x['score'], reverse=True)