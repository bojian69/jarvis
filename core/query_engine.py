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
        # 1. 直接文件名匹配检查
        direct_match = self._direct_filename_search(query)
        if direct_match:
            return direct_match[:top_k]
        
        # 2. 全文关键词搜索
        fulltext_results = self._fulltext_search(query, top_k)
        if fulltext_results:
            return fulltext_results
        
        # 3. 预处理查询
        processed_query = self._preprocess_query(query)
        
        # 4. 向量搜索 - 增加搜索数量
        vector_results = self.vector_manager.search(processed_query, top_k * 3)
        
        # 5. 文件名匹配增强
        filename_enhanced = self._enhance_with_filename(query, vector_results)
        
        # 6. 关键词匹配增强
        keyword_enhanced = self._enhance_with_keywords(query, filename_enhanced)
        
        # 7. 相关性过滤 - 降低阈值
        filtered_results = self._filter_by_relevance(keyword_enhanced)
        
        # 8. 重新排序
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
    
    def _direct_filename_search(self, query: str) -> List[Dict]:
        """直接文件名搜索"""
        try:
            # 获取所有文档
            all_docs = self.vector_manager.list_documents()
            query_lower = query.lower().strip()
            
            matches = []
            for doc in all_docs:
                filename = doc['filename'].lower().strip()
                filename_no_ext = filename.replace('.md', '').replace('.pdf', '')
                
                # 检查各种匹配情况
                if (query_lower == filename_no_ext or 
                    query_lower in filename_no_ext or 
                    filename_no_ext in query_lower or
                    query_lower == filename):
                    
                    # 获取文档内容
                    content = self.vector_manager.get_document_content(doc['filename'])
                    if content:
                        matches.append({
                            'content': content,
                            'source': doc['filename'],
                            'type': doc['type'],
                            'score': 0.95,  # 给文件名匹配高分
                            'filename_match': 1.0
                        })
            
            return matches
        except Exception as e:
            print(f"直接文件名搜索错误: {e}")
            return []
    
    def _fulltext_search(self, query: str, top_k: int = 3) -> List[Dict]:
        """全文关键词搜索"""
        try:
            # 获取所有文档
            all_docs = self.vector_manager.list_documents()
            query_words = set(re.findall(r'[\w\u4e00-\u9fff]+', query.lower()))
            
            matches = []
            for doc in all_docs:
                # 获取文档内容
                content = self.vector_manager.get_document_content(doc['filename'])
                if not content:
                    continue
                
                content_lower = content.lower()
                content_words = set(re.findall(r'[\w\u4e00-\u9fff]+', content_lower))
                
                # 计算关键词匹配度
                if query_words and content_words:
                    keyword_match = len(query_words & content_words) / len(query_words)
                    
                    # 检查是否包含查询关键词
                    contains_query = any(word in content_lower for word in query_words)
                    
                    if keyword_match >= 0.3 or contains_query:
                        # 计算相关性分数
                        relevance_score = keyword_match
                        if contains_query:
                            relevance_score = max(relevance_score, 0.6)
                        
                        matches.append({
                            'content': content,
                            'source': doc['filename'],
                            'type': doc['type'],
                            'score': relevance_score,
                            'keyword_match': keyword_match
                        })
            
            # 按分数排序
            matches.sort(key=lambda x: x['score'], reverse=True)
            return matches[:top_k]
            
        except Exception as e:
            print(f"全文搜索错误: {e}")
            return []
    
    def _enhance_with_filename(self, query: str, results: List[Dict]) -> List[Dict]:
        """文件名匹配增强"""
        query_lower = query.lower()
        
        for result in results:
            filename = result.get('source', '').lower()
            # 检查文件名匹配
            if query_lower in filename or filename.replace('.md', '').replace('.pdf', '') in query_lower:
                result['filename_match'] = 1.0
                # 文件名匹配给予更高权重
                original_score = result.get('score', 0)
                result['score'] = max(original_score, 0.8)  # 确保文件名匹配的结果有高分
            else:
                result['filename_match'] = 0.0
        
        return results
    
    def _filter_by_relevance(self, results: List[Dict]) -> List[Dict]:
        """相关性过滤 - 降低阈值"""
        filtered = []
        for result in results:
            score = result.get('score', 0)
            keyword_match = result.get('keyword_match', 0)
            filename_match = result.get('filename_match', 0)
            
            # 降低相关性阈值，增加文件名匹配条件
            if score >= 0.1 or keyword_match >= 0.1 or filename_match > 0:
                filtered.append(result)
        return filtered
    
    def _rerank_results(self, query: str, results: List[Dict]) -> List[Dict]:
        """重新排序搜索结果"""
        return sorted(results, key=lambda x: x.get('score', 0), reverse=True)