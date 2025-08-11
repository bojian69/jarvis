#!/usr/bin/env python3
"""
API中间件
"""

import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

from .core import BaseMiddleware
from .request import Request, Response
from .exceptions import MiddlewareError, AuthenticationError

load_dotenv()

class APIMiddleware(BaseMiddleware):
    """API调用中间件"""
    
    def __init__(self):
        super().__init__("APIMiddleware")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.api_keys = self._load_api_keys()
    
    def _load_api_keys(self) -> Dict[str, str]:
        """加载API密钥"""
        return {
            'openai': os.getenv('OPENAI_API_KEY', ''),
            'google': os.getenv('GOOGLE_API_KEY', ''),
            'github': os.getenv('GITHUB_TOKEN', ''),
            'weather': os.getenv('WEATHER_API_KEY', '')
        }
    
    def process(self, request: Request, response: Response) -> None:
        """处理API请求"""
        action = request.action
        
        if action == 'api_call':
            self._handle_generic_api(request, response)
        elif action == 'api_get':
            self._handle_get(request, response)
        elif action == 'api_post':
            self._handle_post(request, response)
        elif action == 'api_openai':
            self._handle_openai(request, response)
        elif action == 'api_github':
            self._handle_github(request, response)
        elif action == 'api_weather':
            self._handle_weather(request, response)
    
    def _handle_generic_api(self, request: Request, response: Response):
        """处理通用API调用"""
        url = request.get('url')
        method = request.get('method', 'GET')
        headers = request.get('headers', {})
        data = request.get('data', {})
        
        try:
            if method.upper() == 'GET':
                resp = self.session.get(url, headers=headers, timeout=30)
            elif method.upper() == 'POST':
                resp = self.session.post(url, json=data, headers=headers, timeout=30)
            else:
                response.set_error(f"不支持的HTTP方法: {method}")
                return
            
            resp.raise_for_status()
            response.set_data('result', resp.json() if resp.content else {})
        except Exception as e:
            response.set_error(f"API调用失败: {e}")
    
    def _handle_get(self, request: Request, response: Response):
        """处理GET请求"""
        url = request.get('url')
        headers = request.get('headers', {})
        params = request.get('params', {})
        
        try:
            resp = self.session.get(url, headers=headers, params=params, timeout=30)
            resp.raise_for_status()
            response.set_data('result', resp.json() if resp.content else {})
        except Exception as e:
            response.set_error(f"GET请求失败: {e}")
    
    def _handle_post(self, request: Request, response: Response):
        """处理POST请求"""
        url = request.get('url')
        data = request.get('data', {})
        headers = request.get('headers', {})
        
        try:
            resp = self.session.post(url, json=data, headers=headers, timeout=30)
            resp.raise_for_status()
            response.set_data('result', resp.json() if resp.content else {})
        except Exception as e:
            response.set_error(f"POST请求失败: {e}")
    
    def _handle_openai(self, request: Request, response: Response):
        """处理OpenAI API"""
        if not self.api_keys['openai']:
            response.set_error("OpenAI API密钥未配置")
            return
        
        prompt = request.get('prompt')
        model = request.get('model', 'gpt-3.5-turbo')
        
        headers = {
            "Authorization": f"Bearer {self.api_keys['openai']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000
        }
        
        try:
            resp = self.session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            resp.raise_for_status()
            result = resp.json()
            if "choices" in result:
                response.set_data('answer', result["choices"][0]["message"]["content"])
        except Exception as e:
            response.set_error(f"OpenAI API调用失败: {e}")
    
    def _handle_github(self, request: Request, response: Response):
        """处理GitHub API"""
        endpoint = request.get('endpoint')
        headers = {}
        
        if self.api_keys['github']:
            headers["Authorization"] = f"token {self.api_keys['github']}"
        
        url = f"https://api.github.com/{endpoint}"
        
        try:
            resp = self.session.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
            response.set_data('result', resp.json())
        except Exception as e:
            response.set_error(f"GitHub API调用失败: {e}")
    
    def _handle_weather(self, request: Request, response: Response):
        """处理天气API"""
        if not self.api_keys['weather']:
            response.set_error("天气API密钥未配置")
            return
        
        city = request.get('city')
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_keys['weather'],
            "units": "metric",
            "lang": "zh_cn"
        }
        
        try:
            resp = self.session.get(url, params=params, timeout=30)
            resp.raise_for_status()
            response.set_data('result', resp.json())
        except Exception as e:
            response.set_error(f"天气API调用失败: {e}")