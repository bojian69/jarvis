#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能总结器 - 对检索内容进行总结
"""

import re
from typing import List, Dict

class ContentSummarizer:
    def __init__(self, config: Dict):
        self.config = config
        self.max_summary_length = config.get('max_summary_length', 600)
    
    def summarize_search_results(self, query: str, search_results: List[Dict]) -> str:
        """对搜索结果进行智能总结"""
        if not search_results:
            return f"抱歉，没有找到与「{query}」相关的内容。"
        
        # 1. 提取关键信息
        key_info = self._extract_key_information(query, search_results)
        
        # 2. 生成总结
        summary = self._generate_summary(query, key_info)
        
        return summary
    
    def _extract_key_information(self, query: str, results: List[Dict]) -> Dict:
        """提取关键信息"""
        query_keywords = set(re.findall(r'[\w\u4e00-\u9fff]+', query.lower()))
        
        key_info = {
            'main_points': [],
            'relevant_content': [],
            'sources': set(),
            'keywords_found': set()
        }
        
        for result in results:
            content = result.get('content', '')
            source = result.get('source', '未知来源')
            score = result.get('score', 0)
            
            # 提取相关句子
            sentences = self._split_sentences(content)
            relevant_sentences = []
            
            for sentence in sentences:
                sentence_words = set(re.findall(r'[\w\u4e00-\u9fff]+', sentence.lower()))
                # 计算句子与查询的相关性
                relevance = len(query_keywords & sentence_words) / len(query_keywords) if query_keywords else 0
                
                if relevance > 0.1 or score > 0.5:  # 相关性阈值
                    relevant_sentences.append({
                        'text': sentence.strip(),
                        'relevance': relevance,
                        'source': source
                    })
                    key_info['keywords_found'].update(query_keywords & sentence_words)
            
            # 按相关性排序并取前几句
            relevant_sentences.sort(key=lambda x: x['relevance'], reverse=True)
            key_info['relevant_content'].extend(relevant_sentences[:2])
            key_info['sources'].add(source)
        
        # 去重并排序
        key_info['relevant_content'] = sorted(
            key_info['relevant_content'], 
            key=lambda x: x['relevance'], 
            reverse=True
        )[:5]  # 最多5个关键句子
        
        return key_info
    
    def _split_sentences(self, text: str) -> List[str]:
        """分割句子"""
        # 中英文句子分割
        sentences = re.split(r'[。！？；\.\!\?\;]', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    def _generate_summary(self, query: str, key_info: Dict) -> str:
        """生成总结"""
        relevant_content = key_info['relevant_content']
        sources = key_info['sources']
        keywords_found = key_info['keywords_found']
        
        if not relevant_content:
            return f"找到了相关文档，但没有发现与「{query}」直接相关的具体内容。"
        
        # 构建总结
        summary_parts = []
        
        # 开头
        if keywords_found:
            found_keywords = '、'.join(list(keywords_found)[:3])
            summary_parts.append(f"关于「{query}」，找到以下相关信息：")
        else:
            summary_parts.append(f"根据检索结果，关于「{query}」的信息如下：")
        
        # 主要内容
        main_content = []
        for i, item in enumerate(relevant_content[:3], 1):
            content = item['text']
            # 限制每个要点的长度
            if len(content) > 200:
                content = content[:200] + "..."
            main_content.append(f"{i}. {content}")
        
        summary_parts.extend(main_content)
        
        # 来源信息
        if sources:
            source_list = list(sources)[:6]  # 最多显示6个来源
            if len(source_list) == 1:
                summary_parts.append(f"\n📄 来源：{source_list[0]}")
            else:
                sources_text = "、".join(source_list)
                summary_parts.append(f"\n📄 来源：{sources_text}")
        
        # 组合总结
        full_summary = "\n\n".join(summary_parts)
        
        # 长度控制
        if len(full_summary) > self.max_summary_length:
            full_summary = full_summary[:self.max_summary_length] + "..."
        
        return full_summary
    
    def _extract_key_phrases(self, text: str, query: str) -> List[str]:
        """提取关键短语"""
        query_words = set(re.findall(r'[\w\u4e00-\u9fff]+', query.lower()))
        
        # 简单的关键短语提取
        phrases = []
        sentences = self._split_sentences(text)
        
        for sentence in sentences:
            sentence_words = set(re.findall(r'[\w\u4e00-\u9fff]+', sentence.lower()))
            if query_words & sentence_words:  # 包含查询词的句子
                # 提取包含查询词的短语
                words = re.findall(r'[\w\u4e00-\u9fff]+', sentence)
                for i, word in enumerate(words):
                    if word.lower() in query_words:
                        # 提取前后各2个词作为短语
                        start = max(0, i-2)
                        end = min(len(words), i+3)
                        phrase = ''.join(words[start:end])
                        if len(phrase) > 4:
                            phrases.append(phrase)
        
        return phrases[:5]  # 返回前5个关键短语