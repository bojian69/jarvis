#!/usr/bin/env python3
"""
验证中间件
"""

from typing import Dict, Any, List
from .core import BaseMiddleware
from .request import Request, Response
from .exceptions import ValidationError

class ValidationMiddleware(BaseMiddleware):
    """请求验证中间件"""
    
    def __init__(self):
        super().__init__("ValidationMiddleware")
        self.validation_rules = {
            'browser_open_url': ['url'],
            'browser_search_google': ['query'],
            'browser_screenshot': [],
            'api_get': ['url'],
            'api_post': ['url'],
            'api_openai': ['prompt'],
            'api_github': ['endpoint'],
            'api_weather': ['city'],
            'python_execute': ['code']
        }
    
    def process(self, request: Request, response: Response) -> None:
        """验证请求参数"""
        action = request.action
        
        if action not in self.validation_rules:
            return
        
        required_fields = self.validation_rules[action]
        missing_fields = []
        
        for field in required_fields:
            if not request.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            response.set_error(f"缺少必需参数: {', '.join(missing_fields)}")
            return
        
        # 特定验证
        if action == 'browser_open_url':
            url = request.get('url')
            if not (url.startswith('http://') or url.startswith('https://')):
                response.set_error("URL格式无效")
        
        elif action == 'python_execute':
            code = request.get('code')
            # 基础安全检查
            dangerous_keywords = ['import os', 'import sys', '__import__', 'eval']
            for keyword in dangerous_keywords:
                if keyword in code:
                    response.set_error(f"代码包含危险关键词: {keyword}")
                    return