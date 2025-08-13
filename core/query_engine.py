#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强查询引擎 - 优化检索精度
"""

import re
from typing import List, Dict
from .vector_manager import VectorManager

class QueryEngine:
    def __init__(self, config: Dict):
        self.config = config
        self.vector_manager = VectorManager(config)
        self.relevance_threshold = config.get('relevance_threshold', 0.3)
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """增强搜索功能"""
        # 1. 预处理查询
        processed_query = self._preprocess_query(query)
        
        # 2. 向量搜索
        vector_results = self.vector_manager.search(processed_query, top_k * 2)
        
        # 3. 关键词匹配增强
        keyword_enhanced = self._enhance_with_keywords(query, vector_results)
        
        # 4. 相关性过滤
        filtered_results = self._filter_by_relevance(keyword_enhanced)
        
        # 5. 重新排序
        final_results = self._rerank_results(query, filtered_results)
        
        return final_results[:top_k]
    
    def _preprocess_query(self, query: str) -> str:
        """查询预处理"""
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        words = re.findall(r'[\w\u4e00-\u9fff]+', query.lower())
        filtered_words = [w for w in words if w not in stop_words and len(w) > 1]
        return ' '.join(filtered_words) if filtered_words else query
    
    def _enhance_with_keywords(self, query: str, results: List[Dict]) -> List[Dict]:
        """关键词匹配增强"""
        query_words = set(re.findall(r'[\w\u4e00-\u9fff]+', query.lower()))
        
        for result in results:
            content = result.get('content', '').lower()
            content_words = set(re.findall(r'[\w\u4e00-\u9fff]+', content))
            
            if query_words and content_words:
                keyword_match = len(query_words & content_words) / len(query_words)
                original_score = result.get('score', 0)
                result['score'] = original_score * 0.7 + keyword_match * 0.3
                result['keyword_match'] = keyword_match
            else:
                result['keyword_match'] = 0
        
        return results
    
    def _filter_by_relevance(self, results: List[Dict]) -> List[Dict]:
        """相关性过滤"""
        filtered = []
        for result in results:
            score = result.get('score', 0)
            keyword_match = result.get('keyword_match', 0)
            if score >= self.relevance_threshold or keyword_match >= 0.2:
                filtered.append(result)
        return filtered
    
    def _rerank_results(self, query: str, results: List[Dict]) -> List[Dict]:
        """重新排序搜索结果"""
        return sorted(results, key=lambda x: x.get('score', 0), reverse=True)