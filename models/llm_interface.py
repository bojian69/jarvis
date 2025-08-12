#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM接口 - 本地大语言模型接口
"""

import requests
import logging
from typing import List, Dict

class LLMInterface:
    def __init__(self, config: Dict):
        self.base_url = config.get("llm_url", "http://localhost:11434")
        self.model = config.get("llm_model", "qwen2.5:7b")
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """检查模型是否可用"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_answer(self, question: str, context_docs: List[Dict]) -> str:
        """基于上下文生成回答"""
        if not self.available:
            return "本地模型服务不可用，请检查Ollama是否启动"
        
        # 构建上下文
        context = self._build_context(context_docs)
        prompt = self._build_prompt(question, context)
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return "模型响应异常"
                
        except Exception as e:
            logging.error(f"LLM生成错误: {e}")
            return "生成回答时出现错误"
    
    def _build_context(self, docs: List[Dict]) -> str:
        """构建上下文文本"""
        if not docs:
            return "没有找到相关文档。"
        
        context = "参考文档内容:\n"
        for i, doc in enumerate(docs, 1):
            context += f"{i}. {doc['content'][:300]}...\n"
        
        return context
    
    def _build_prompt(self, question: str, context: str) -> str:
        """构建提示词"""
        return f"""你是一个专业的文档分析助手。请基于提供的文档内容回答用户问题。

{context}

用户问题: {question}

请根据上述文档内容回答问题。如果文档中没有相关信息，请明确说明。回答要准确、简洁、有条理。"""