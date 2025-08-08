#!/usr/bin/env python3
"""
API调用模块
增强版API调用功能，支持多种API服务
"""

import os
import time
import requests
import json
from typing import Dict, Any, Optional
from ..core.middleware import with_middleware

class APIModule:
    """API调用模块"""
    
    def __init__(self, config, logger, middleware_manager):
        self.config = config
        self.logger = logger
        self.middleware_manager = middleware_manager
        
        # 创建会话
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.config.get('browser.user_agent', 
                                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        })
        
        # API密钥
        self.api_keys = {
            'openai': os.getenv('OPENAI_API_KEY'),
            'google': os.getenv('GOOGLE_API_KEY'),
            'github': os.getenv('GITHUB_TOKEN'),
            'anthropic': os.getenv('ANTHROPIC_API_KEY')
        }
    
    def execute_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """执行API命令"""
        command_map = {
            'api_openai_chat': self.openai_chat,
            'api_google_search': self.google_search,
            'api_github_search': self.github_search,
            'api_weather': self.get_weather,
            'api_generic_request': self.generic_request,
            'api_test_connection': self.test_connection
        }
        
        if command in command_map:
            return command_map[command](**kwargs)
        else:
            return {"success": False, "error": f"未知的API命令: {command}"}
    
    @with_middleware
    def openai_chat(self, message: str, model: str = "gpt-3.5-turbo", **kwargs) -> Dict[str, Any]:
        """OpenAI聊天API"""
        if not self.api_keys['openai']:
            return {"success": False, "error": "OpenAI API密钥未配置"}
        
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_keys['openai']}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": message}],
                "max_tokens": kwargs.get('max_tokens', 1000),
                "temperature": kwargs.get('temperature', 0.7)
            }
            
            start_time = time.time()
            response = self.session.post(url, headers=headers, json=data, 
                                       timeout=self.config.get('api.timeout', 30))
            response_time = time.time() - start_time
            
            self.logger.log_api_call("OpenAI", url, "POST", response.status_code, response_time)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "response": result['choices'][0]['message']['content'],
                    "model": model,
                    "usage": result.get('usage', {}),
                    "response_time": response_time
                }
            else:
                return {"success": False, "error": f"API调用失败: {response.status_code}"}
                
        except Exception as e:
            self.logger.log_api_call("OpenAI", url, "POST", None, None, str(e))
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def google_search(self, query: str, num_results: int = 10, **kwargs) -> Dict[str, Any]:
        """Google搜索API"""
        if not self.api_keys['google']:
            return {"success": False, "error": "Google API密钥未配置"}
        
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": self.api_keys['google'],
                "cx": os.getenv('GOOGLE_SEARCH_ENGINE_ID'),  # 需要配置搜索引擎ID
                "q": query,
                "num": min(num_results, 10)
            }
            
            start_time = time.time()
            response = self.session.get(url, params=params, 
                                      timeout=self.config.get('api.timeout', 30))
            response_time = time.time() - start_time
            
            self.logger.log_api_call("Google Search", url, "GET", response.status_code, response_time)
            
            if response.status_code == 200:
                result = response.json()
                items = result.get('items', [])
                
                search_results = []
                for item in items:
                    search_results.append({
                        "title": item.get('title', ''),
                        "link": item.get('link', ''),
                        "snippet": item.get('snippet', ''),
                        "displayLink": item.get('displayLink', '')
                    })
                
                return {
                    "success": True,
                    "query": query,
                    "results": search_results,
                    "total_results": result.get('searchInformation', {}).get('totalResults', 0),
                    "response_time": response_time
                }
            else:
                return {"success": False, "error": f"Google搜索失败: {response.status_code}"}
                
        except Exception as e:
            self.logger.log_api_call("Google Search", url, "GET", None, None, str(e))
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def github_search(self, query: str, search_type: str = "repositories", **kwargs) -> Dict[str, Any]:
        """GitHub搜索API"""
        if not self.api_keys['github']:
            return {"success": False, "error": "GitHub Token未配置"}
        
        try:
            url = f"https://api.github.com/search/{search_type}"
            headers = {
                "Authorization": f"token {self.api_keys['github']}",
                "Accept": "application/vnd.github.v3+json"
            }
            params = {
                "q": query,
                "per_page": kwargs.get('per_page', 10),
                "sort": kwargs.get('sort', 'stars'),
                "order": kwargs.get('order', 'desc')
            }
            
            start_time = time.time()
            response = self.session.get(url, headers=headers, params=params,
                                      timeout=self.config.get('api.timeout', 30))
            response_time = time.time() - start_time
            
            self.logger.log_api_call("GitHub", url, "GET", response.status_code, response_time)
            
            if response.status_code == 200:
                result = response.json()
                items = result.get('items', [])
                
                search_results = []
                for item in items:
                    if search_type == "repositories":
                        search_results.append({
                            "name": item.get('name', ''),
                            "full_name": item.get('full_name', ''),
                            "description": item.get('description', ''),
                            "html_url": item.get('html_url', ''),
                            "stars": item.get('stargazers_count', 0),
                            "language": item.get('language', ''),
                            "updated_at": item.get('updated_at', '')
                        })
                
                return {
                    "success": True,
                    "query": query,
                    "search_type": search_type,
                    "results": search_results,
                    "total_count": result.get('total_count', 0),
                    "response_time": response_time
                }
            else:
                return {"success": False, "error": f"GitHub搜索失败: {response.status_code}"}
                
        except Exception as e:
            self.logger.log_api_call("GitHub", url, "GET", None, None, str(e))
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def get_weather(self, city: str = "Beijing", **kwargs) -> Dict[str, Any]:
        """获取天气信息（使用免费API）"""
        try:
            # 使用OpenWeatherMap免费API
            api_key = os.getenv('OPENWEATHER_API_KEY')
            if not api_key:
                # 使用免费的天气API
                url = f"http://wttr.in/{city}?format=j1"
                
                start_time = time.time()
                response = self.session.get(url, timeout=self.config.get('api.timeout', 30))
                response_time = time.time() - start_time
                
                self.logger.log_api_call("Weather", url, "GET", response.status_code, response_time)
                
                if response.status_code == 200:
                    data = response.json()
                    current = data['current_condition'][0]
                    
                    return {
                        "success": True,
                        "city": city,
                        "temperature": current['temp_C'],
                        "description": current['weatherDesc'][0]['value'],
                        "humidity": current['humidity'],
                        "wind_speed": current['windspeedKmph'],
                        "response_time": response_time
                    }
                else:
                    return {"success": False, "error": f"天气API调用失败: {response.status_code}"}
            else:
                # 使用OpenWeatherMap API
                url = "http://api.openweathermap.org/data/2.5/weather"
                params = {
                    "q": city,
                    "appid": api_key,
                    "units": "metric",
                    "lang": "zh_cn"
                }
                
                start_time = time.time()
                response = self.session.get(url, params=params,
                                          timeout=self.config.get('api.timeout', 30))
                response_time = time.time() - start_time
                
                self.logger.log_api_call("OpenWeatherMap", url, "GET", response.status_code, response_time)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    return {
                        "success": True,
                        "city": data['name'],
                        "temperature": data['main']['temp'],
                        "description": data['weather'][0]['description'],
                        "humidity": data['main']['humidity'],
                        "wind_speed": data['wind']['speed'],
                        "response_time": response_time
                    }
                else:
                    return {"success": False, "error": f"天气API调用失败: {response.status_code}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def generic_request(self, url: str, method: str = "GET", **kwargs) -> Dict[str, Any]:
        """通用HTTP请求"""
        try:
            method = method.upper()
            headers = kwargs.get('headers', {})
            params = kwargs.get('params', {})
            data = kwargs.get('data', {})
            json_data = kwargs.get('json', None)
            
            start_time = time.time()
            
            if method == "GET":
                response = self.session.get(url, headers=headers, params=params,
                                          timeout=self.config.get('api.timeout', 30))
            elif method == "POST":
                response = self.session.post(url, headers=headers, params=params,
                                           data=data, json=json_data,
                                           timeout=self.config.get('api.timeout', 30))
            elif method == "PUT":
                response = self.session.put(url, headers=headers, params=params,
                                          data=data, json=json_data,
                                          timeout=self.config.get('api.timeout', 30))
            elif method == "DELETE":
                response = self.session.delete(url, headers=headers, params=params,
                                             timeout=self.config.get('api.timeout', 30))
            else:
                return {"success": False, "error": f"不支持的HTTP方法: {method}"}
            
            response_time = time.time() - start_time
            
            self.logger.log_api_call("Generic", url, method, response.status_code, response_time)
            
            # 尝试解析JSON响应
            try:
                response_data = response.json()
            except:
                response_data = response.text
            
            return {
                "success": response.status_code < 400,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "data": response_data,
                "response_time": response_time
            }
            
        except Exception as e:
            self.logger.log_api_call("Generic", url, method, None, None, str(e))
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def test_connection(self, **kwargs) -> Dict[str, Any]:
        """测试网络连接"""
        try:
            test_urls = [
                "https://www.google.com",
                "https://www.baidu.com",
                "https://httpbin.org/get"
            ]
            
            results = []
            for url in test_urls:
                try:
                    start_time = time.time()
                    response = self.session.get(url, timeout=5)
                    response_time = time.time() - start_time
                    
                    results.append({
                        "url": url,
                        "status_code": response.status_code,
                        "response_time": response_time,
                        "success": response.status_code == 200
                    })
                except Exception as e:
                    results.append({
                        "url": url,
                        "error": str(e),
                        "success": False
                    })
            
            success_count = sum(1 for r in results if r.get('success', False))
            
            return {
                "success": success_count > 0,
                "results": results,
                "success_rate": success_count / len(results),
                "message": f"网络连接测试完成，成功率: {success_count}/{len(results)}"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
