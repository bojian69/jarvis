#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import logging
from typing import List, Dict

class LocalLLM:
    def __init__(self, base_url="http://localhost:11434", model="qwen2.5:7b"):
        self.base_url = base_url
        self.model = model
        self.available = self._check_availability()
        
    def _check_availability(self) -> bool:
        """检查本地模型是否可用"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_response(self, prompt: str, context: List[Dict] = None) -> str:
        """生成回复"""
        if not self.available:
            return "本地模型不可用，请启动Ollama服务"
        
        # 构建上下文
        context_text = ""
        if context:
            context_text = "\n参考文档:\n"
            for doc in context:
                context_text += f"- {doc['content'][:200]}...\n"
        
        full_prompt = f"""基于以下文档内容回答问题:
{context_text}

问题: {prompt}

请用中文回答，如果文档中没有相关信息，请说明。"""

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return "模型响应错误"
                
        except Exception as e:
            logging.error(f"LLM错误: {e}")
            return "生成回复时出错"