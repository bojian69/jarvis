#!/usr/bin/env python3
"""
API调用工具类
处理各种第三方API调用，支持无API密钥运行
"""

import requests
import json
import time
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class APITools:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.api_status = self._check_api_keys()
    
    def _check_api_keys(self):
        """检查API密钥状态"""
        return {
            'openai': bool(os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'your_openai_api_key_here'),
            'google': bool(os.getenv('GOOGLE_API_KEY') and os.getenv('GOOGLE_API_KEY') != 'your_google_api_key_here'),
            'github': bool(os.getenv('GITHUB_TOKEN') and os.getenv('GITHUB_TOKEN') != 'your_github_token_here'),
            'weather': bool(os.getenv('WEATHER_API_KEY') and os.getenv('WEATHER_API_KEY') != 'your_weather_api_key_here')
        }
    
    def get(self, url: str, headers: Optional[Dict] = None, params: Optional[Dict] = None) -> Optional[Dict]:
        """GET请求 - 无需API密钥"""
        try:
            response = self.session.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            print(f"✅ GET请求成功: {url}")
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as e:
            print(f"❌ GET请求失败: {e}")
            return None
        except json.JSONDecodeError:
            return {"text": response.text}
    
    def post(self, url: str, data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Optional[Dict]:
        """POST请求 - 无需API密钥"""
        try:
            response = self.session.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            print(f"✅ POST请求成功: {url}")
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as e:
            print(f"❌ POST请求失败: {e}")
            return None
        except json.JSONDecodeError:
            return {"text": response.text}
    
    def put(self, url: str, data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Optional[Dict]:
        """PUT请求"""
        try:
            response = self.session.put(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            print(f"✅ PUT请求成功: {url}")
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as e:
            print(f"❌ PUT请求失败: {e}")
            return None
    
    def delete(self, url: str, headers: Optional[Dict] = None) -> bool:
        """DELETE请求"""
        try:
            response = self.session.delete(url, headers=headers, timeout=30)
            response.raise_for_status()
            print(f"✅ DELETE请求成功: {url}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ DELETE请求失败: {e}")
            return False
    
    def download_file(self, url: str, filename: str, headers: Optional[Dict] = None) -> bool:
        """下载文件 - 无需API密钥"""
        try:
            response = self.session.get(url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ 文件下载成功: {filename}")
            return True
        except Exception as e:
            print(f"❌ 文件下载失败: {e}")
            return False
    
    def upload_file(self, url: str, file_path: str, field_name: str = "file", 
                   headers: Optional[Dict] = None) -> Optional[Dict]:
        """上传文件"""
        try:
            with open(file_path, 'rb') as f:
                files = {field_name: f}
                response = self.session.post(url, files=files, headers=headers, timeout=60)
                response.raise_for_status()
                print(f"✅ 文件上传成功: {file_path}")
                return response.json() if response.content else {}
        except Exception as e:
            print(f"❌ 文件上传失败: {e}")
            return None
    
    def call_openai_api(self, prompt: str, model: str = "gpt-3.5-turbo") -> Optional[str]:
        """调用OpenAI API - 需要API密钥"""
        if not self.api_status['openai']:
            print("❌ OpenAI API密钥未配置")
            print("💡 请在.env文件中设置OPENAI_API_KEY")
            print("💡 获取地址: https://platform.openai.com/api-keys")
            return None
        
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000
            }
            
            response = self.session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            if "choices" in result:
                print("✅ OpenAI API调用成功")
                return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            print(f"❌ OpenAI API调用失败: {e}")
            return None
    
    def call_github_api(self, endpoint: str) -> Optional[Dict]:
        """调用GitHub API - 公开API无需密钥，私有API需要token"""
        headers = {}
        if self.api_status['github']:
            token = os.getenv('GITHUB_TOKEN')
            headers["Authorization"] = f"token {token}"
            print("✅ 使用GitHub Token进行认证")
        else:
            print("💡 使用GitHub公开API（无需token）")
        
        url = f"https://api.github.com/{endpoint}"
        return self.get(url, headers)
    
    def call_weather_api(self, city: str) -> Optional[Dict]:
        """调用天气API - 需要API密钥"""
        if not self.api_status['weather']:
            print("❌ 天气API密钥未配置")
            print("💡 请在.env文件中设置WEATHER_API_KEY")
            print("💡 获取地址: https://openweathermap.org/api")
            return None
        
        try:
            api_key = os.getenv('WEATHER_API_KEY')
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": api_key,
                "units": "metric",
                "lang": "zh_cn"
            }
            result = self.get(url, params=params)
            if result:
                print(f"✅ 天气API调用成功: {city}")
            return result
        except Exception as e:
            print(f"❌ 天气API调用失败: {e}")
            return None
    
    def call_public_api_examples(self):
        """调用一些无需API密钥的公开API示例"""
        print("🌐 测试公开API...")
        
        # 1. JSONPlaceholder - 测试API
        print("\n1️⃣ 测试JSONPlaceholder API")
        result = self.get("https://jsonplaceholder.typicode.com/posts/1")
        if result:
            print(f"   标题: {result.get('title', 'N/A')}")
        
        # 2. GitHub公开用户信息
        print("\n2️⃣ 测试GitHub公开API")
        result = self.call_github_api("users/octocat")
        if result:
            print(f"   用户: {result.get('name', 'N/A')}")
            print(f"   公开仓库: {result.get('public_repos', 'N/A')}")
        
        # 3. 随机名言API
        print("\n3️⃣ 测试随机名言API")
        result = self.get("https://api.quotable.io/random")
        if result:
            print(f"   名言: {result.get('content', 'N/A')}")
            print(f"   作者: {result.get('author', 'N/A')}")
        
        # 4. IP信息API
        print("\n4️⃣ 测试IP信息API")
        result = self.get("https://httpbin.org/ip")
        if result:
            print(f"   您的IP: {result.get('origin', 'N/A')}")
        
        print("\n✅ 公开API测试完成")
    
    def print_api_status(self):
        """打印API状态信息"""
        print("📊 API服务状态:")
        print(f"  OpenAI API: {'✅ 已配置' if self.api_status['openai'] else '❌ 未配置'}")
        print(f"  Google API: {'✅ 已配置' if self.api_status['google'] else '❌ 未配置'}")
        print(f"  GitHub Token: {'✅ 已配置' if self.api_status['github'] else '❌ 未配置'}")
        print(f"  Weather API: {'✅ 已配置' if self.api_status['weather'] else '❌ 未配置'}")

# 测试函数
def test_api_tools():
    """测试API工具"""
    api = APITools()
    api.print_api_status()
    api.call_public_api_examples()

if __name__ == "__main__":
    test_api_tools()
