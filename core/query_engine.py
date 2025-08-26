#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询引擎 - 处理用户查询和检索
"""

<<<<<<< Updated upstream
=======
import re
import logging
>>>>>>> Stashed changes
from typing import List, Dict
from .vector_manager import VectorManager

class QueryEngine:
    def __init__(self, config: Dict):
        self.config = config
        self.vector_manager = VectorManager(config)
    
<<<<<<< Updated upstream
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
=======
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """增强搜索功能 - 优化搜索策略"""
        all_results = []
        
        # 1. 直接文件名匹配检查
        direct_match = self._direct_filename_search(query)
        if direct_match:
            all_results.extend(direct_match)
        
        # 2. 全文关键词搜索（始终执行）
        fulltext_results = self._fulltext_search(query, top_k * 2)
        all_results.extend(fulltext_results)
        
        # 3. 如果仍然没有结果，尝试向量搜索
        if not all_results:
            processed_query = self._preprocess_query(query)
            vector_results = self.vector_manager.search(processed_query, top_k * 3)
            
            # 文件名匹配增强
            filename_enhanced = self._enhance_with_filename(query, vector_results)
            
            # 关键词匹配增强
            keyword_enhanced = self._enhance_with_keywords(query, filename_enhanced)
            
            # 相关性过滤
            filtered_results = self._filter_by_relevance(keyword_enhanced)
            all_results.extend(filtered_results)
        
        # 去重（按文件名）
        seen_files = set()
        unique_results = []
        for result in all_results:
            filename = result.get('source', '')
            if filename not in seen_files:
                seen_files.add(filename)
                unique_results.append(result)
        
        # 排序并返回
        final_results = self._rerank_results(query, unique_results)
        return final_results[:top_k]
    
    def _extract_keywords(self, text: str) -> set:
        """提取关键词（简单的中文分词）"""
        keywords = set()
        
        # 定义常见的业务关键词
        business_keywords = [
            '客户流失', '用户流失', '流失分析', '流失原因', '流失预测',
            '客户', '用户', '流失', '分析', '原因', '因素', '研究',
            '留存', '保留', '预测', '模型', '策略', '措施'
        ]
        
        text_lower = text.lower()
        
        # 先匹配业务关键词
        for keyword in business_keywords:
            if keyword in text_lower:
                keywords.add(keyword)
        
        # 提取单个中文字符组合
        chinese_chars = re.findall(r'[一-鿿]', text_lower)
        for i in range(len(chinese_chars)):
            # 单字
            if len(chinese_chars[i]) > 0:
                keywords.add(chinese_chars[i])
            # 双字词
            if i < len(chinese_chars) - 1:
                two_char = chinese_chars[i] + chinese_chars[i+1]
                keywords.add(two_char)
            # 三字词
            if i < len(chinese_chars) - 2:
                three_char = chinese_chars[i] + chinese_chars[i+1] + chinese_chars[i+2]
                keywords.add(three_char)
        
        # 提取英文单词
        english_words = re.findall(r'[a-zA-Z]+', text_lower)
        keywords.update(english_words)
        
        return keywords
    
    def _preprocess_query(self, query: str) -> str:
        """查询预处理"""
        # 简单返回原始查询，由其他方法处理分词
        return query.lower().strip()
    
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
        """全文关键词搜索 - 优化匹配逻辑"""
        try:
            # 获取所有文档
            all_docs = self.vector_manager.list_documents()
            
            # 使用新的关键词提取方法
            query_words = self._extract_keywords(query)
            
            # query_words 已经在上面定义
            
            matches = []
            for doc in all_docs:
                # 获取文档内容
                content = self.vector_manager.get_document_content(doc['filename'])
                if not content:
                    continue
                
                content_lower = content.lower()
                content_words = self._extract_keywords(content)
                
                # 多维度匹配评分
                score = 0
                match_details = {}
                
                if query_words and content_words:
                    # 1. 关键词匹配度
                    keyword_match = len(query_words & content_words) / len(query_words)
                    match_details['keyword_match'] = keyword_match
                    
                    # 2. 直接包含检查
                    direct_contains = sum(1 for word in query_words if word in content_lower)
                    contains_ratio = direct_contains / len(query_words)
                    match_details['contains_ratio'] = contains_ratio
                    
                    # 3. 语义相关性检查（简单的同义词匹配）
                    semantic_score = self._calculate_semantic_similarity(query_words, content_words)
                    match_details['semantic_score'] = semantic_score
                    
                    # 综合评分
                    score = (
                        keyword_match * 0.4 +
                        contains_ratio * 0.4 +
                        semantic_score * 0.2
                    )
                    
                    # 降低阈值，提高召回率
                    if score >= 0.15 or contains_ratio >= 0.3 or keyword_match >= 0.2:
                        matches.append({
                            'content': content,
                            'source': doc['filename'],
                            'type': doc['type'],
                            'score': score,
                            'match_details': match_details
                        })
            
            # 按分数排序
            matches.sort(key=lambda x: x['score'], reverse=True)
            return matches[:top_k]
            
        except Exception as e:
            logging.error(f"全文搜索错误: {e}")
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
        """相关性过滤 - 进一步降低阈值"""
        filtered = []
        for result in results:
            score = result.get('score', 0)
            keyword_match = result.get('keyword_match', 0)
            filename_match = result.get('filename_match', 0)
            match_details = result.get('match_details', {})
            
            # 更宽松的过滤条件
            should_include = (
                score >= 0.05 or  # 降低基本分数阈值
                keyword_match >= 0.05 or  # 降低关键词匹配阈值
                filename_match > 0 or  # 文件名匹配
                match_details.get('contains_ratio', 0) >= 0.2 or  # 包含比例
                match_details.get('semantic_score', 0) >= 0.3  # 语义相似度
            )
            
            if should_include:
                filtered.append(result)
        
        return filtered
    
    def _calculate_semantic_similarity(self, query_words: set, content_words: set) -> float:
        """计算语义相似度（简单的同义词匹配）"""
        # 定义一些关键的同义词组
        synonym_groups = [
            {'流失', '流失率', '流失分析', 'churn', 'attrition'},
            {'客户', '用户', '客户群体', 'customer', 'user'},
            {'原因', '因素', '原因分析', 'reason', 'factor', 'cause'},
            {'分析', '研究', '评估', 'analysis', 'research'},
            {'留存', '保留', '维持', 'retention', 'maintain'},
            {'预测', '预测模型', '预测分析', 'prediction', 'forecast'}
        ]
        
        semantic_matches = 0
        total_query_words = len(query_words)
        
        if total_query_words == 0:
            return 0
        
        for query_word in query_words:
            # 直接匹配
            if query_word in content_words:
                semantic_matches += 1
                continue
            
            # 同义词匹配
            for synonym_group in synonym_groups:
                if query_word in synonym_group:
                    if any(synonym in content_words for synonym in synonym_group):
                        semantic_matches += 0.8  # 同义词匹配给予较高权重
                        break
        
        return semantic_matches / total_query_words
    
    def _rerank_results(self, query: str, results: List[Dict]) -> List[Dict]:
>>>>>>> Stashed changes
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