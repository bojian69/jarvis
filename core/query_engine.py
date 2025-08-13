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
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """执行搜索查询"""
        # 使用向量搜索，获取更多候选结果
        results = self.vector_manager.search(query, min(top_k * 3, 15))
        
        # 过滤低相关性结果
        filtered_results = self._filter_results(results, query)
        
        # 重新排序并限制数量
        reranked_results = self._rerank_results(filtered_results, query)
        
        return reranked_results[:top_k]
    
    def _rerank_results(self, results: List[Dict], query: str) -> List[Dict]:
        """重新排序搜索结果"""
        # 基于分数和内容长度的综合排序
        def score_function(doc):
            base_score = doc.get('score', 0)
            content_length = len(doc.get('content', ''))
            # 给予较长内容轻微加分，但主要还是基于相似度
            length_bonus = min(content_length / 1000, 0.1)
            return base_score + length_bonus
        
        return sorted(results, key=score_function, reverse=True)
    
    def _filter_results(self, results: List[Dict], query: str) -> List[Dict]:
        """过滤搜索结果，提高准确性"""
        if not results:
            return results
        
        # 动态调整相似度阈值
        min_score = 0.35  # 降低初始阈值
        filtered = [doc for doc in results if doc.get('score', 0) >= min_score]
        
        # 如果结果仍然为空，进一步降低阈值
        if len(filtered) == 0:
            min_score = 0.2
            filtered = [doc for doc in results if doc.get('score', 0) >= min_score]
        
        # 按相似度排序
        filtered.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        # 智能去重：避免来自同一文档的过多片段
        seen_sources = {}
        deduplicated = []
        
        for doc in filtered:
            source = doc.get('source', 'unknown')
            score = doc.get('score', 0)
            
            # 高相似度的片段可以多取一些
            max_per_doc = 2 if score > 0.5 else 1
            
            if seen_sources.get(source, 0) < max_per_doc:
                deduplicated.append(doc)
                seen_sources[source] = seen_sources.get(source, 0) + 1
        
        return deduplicated