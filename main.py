#!/usr/bin/env python3
"""
Jarvis AI Agent - 智能助手
支持浏览器操作、API调用、本地文件处理
"""

import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 检查API密钥可用性
def check_api_keys():
    """检查API密钥配置状态"""
    status = {
        'openai': bool(os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'your_openai_api_key_here'),
        'google': bool(os.getenv('GOOGLE_API_KEY') and os.getenv('GOOGLE_API_KEY') != 'your_google_api_key_here'),
        'github': bool(os.getenv('GITHUB_TOKEN') and os.getenv('GITHUB_TOKEN') != 'your_github_token_here')
    }
    return status

class JarvisAgent:
    def __init__(self):
        self.driver = None
        self.api_status = check_api_keys()
        self.print_startup_info()
        self.setup_browser()
    
    def print_startup_info(self):
        """打印启动信息和API状态"""
        print("🤖 Jarvis AI Agent 启动中...")
        print("=" * 50)
        print("📊 API服务状态:")
        print(f"  OpenAI API: {'✅ 已配置' if self.api_status['openai'] else '❌ 未配置 (AI对话功能不可用)'}")
        print(f"  Google API: {'✅ 已配置' if self.api_status['google'] else '❌ 未配置 (Google API功能不可用)'}")
        print(f"  GitHub API: {'✅ 已配置' if self.api_status['github'] else '❌ 未配置 (GitHub API功能不可用)'}")
        print("=" * 50)
        print("💡 提示: 浏览器自动化功能无需API密钥即可使用")
        if not any(self.api_status.values()):
            print("💡 如需AI功能，请在.env文件中配置相应的API密钥")
        print("=" * 50)
    
    def setup_browser(self):
        """设置浏览器 - 使用真实Chrome避免检测"""
        try:
            # 使用undetected-chromedriver避免被检测
            options = uc.ChromeOptions()
            
            # 保持浏览器可见，方便人工处理验证码
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            # 使用用户数据目录，保持登录状态
            user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome/Jarvis")
            options.add_argument(f"--user-data-dir={user_data_dir}")
            
            # 设置窗口大小
            options.add_argument("--window-size=1280,720")
            
            self.driver = uc.Chrome(options=options)
            print("✅ 浏览器启动成功")
            
        except Exception as e:
            print(f"❌ 浏览器启动失败: {e}")
            print("💡 请确保已安装Google Chrome浏览器")
            print("💡 如遇权限问题，请在系统偏好设置中允许")
    
    def open_url(self, url):
        """打开指定URL"""
        if not self.driver:
            print("❌ 浏览器未启动，无法打开URL")
            return False
            
        try:
            self.driver.get(url)
            print(f"✅ 已打开: {url}")
            return True
        except Exception as e:
            print(f"❌ 打开URL失败: {e}")
            return False
    
    def search_google(self, query):
        """Google搜索"""
        if not self.driver:
            print("❌ 浏览器未启动，无法进行搜索")
            return False
            
        try:
            self.driver.get("https://www.google.com")
            
            # 等待搜索框加载
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            search_box.clear()
            search_box.send_keys(query)
            search_box.submit()
            
            print(f"✅ Google搜索完成: {query}")
            return True
            
        except Exception as e:
            print(f"❌ Google搜索失败: {e}")
            print("💡 提示: 如遇到验证码，请手动处理后继续")
            return False
    
    def call_api(self, url, method="GET", headers=None, data=None):
        """调用第三方API - 不依赖特定API密钥"""
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=30)
            
            response.raise_for_status()
            print(f"✅ API调用成功: {url}")
            return response.json()
            
        except Exception as e:
            print(f"❌ API调用失败: {e}")
            return None
    
    def call_openai_api(self, prompt, model="gpt-3.5-turbo"):
        """调用OpenAI API - 需要API密钥"""
        if not self.api_status['openai']:
            print("❌ OpenAI API密钥未配置")
            print("💡 请在.env文件中设置OPENAI_API_KEY")
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
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            if "choices" in result:
                answer = result["choices"][0]["message"]["content"]
                print(f"✅ OpenAI API调用成功")
                return answer
            
        except Exception as e:
            print(f"❌ OpenAI API调用失败: {e}")
            return None
    
    def execute_python_code(self, code):
        """执行Python代码 - 无需API密钥"""
        try:
            # 创建安全的执行环境
            safe_globals = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'str': str,
                    'int': int,
                    'float': float,
                    'list': list,
                    'dict': dict,
                    'range': range,
                    'enumerate': enumerate,
                    'zip': zip,
                    'sum': sum,
                    'max': max,
                    'min': min,
                }
            }
            
            # 允许导入常用模块
            import datetime
            import math
            import json
            safe_globals.update({
                'datetime': datetime,
                'math': math,
                'json': json,
            })
            
            exec(code, safe_globals)
            print("✅ Python代码执行成功")
            return True
        except Exception as e:
            print(f"❌ Python代码执行失败: {e}")
            return False
    
    def wait_for_manual_action(self, message="请手动处理验证码或其他操作，完成后按回车继续..."):
        """等待用户手动操作"""
        print(f"⏸️  {message}")
        input()
        print("▶️  继续执行...")
    
    def get_current_url(self):
        """获取当前页面URL"""
        if self.driver:
            return self.driver.current_url
        return None
    
    def get_page_title(self):
        """获取当前页面标题"""
        if self.driver:
            return self.driver.title
        return None
    
    def take_screenshot(self, filename="screenshot.png"):
        """截图"""
        if not self.driver:
            print("❌ 浏览器未启动，无法截图")
            return False
            
        try:
            self.driver.save_screenshot(filename)
            print(f"✅ 截图保存: {filename}")
            return True
        except Exception as e:
            print(f"❌ 截图失败: {e}")
            return False
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            print("✅ 浏览器已关闭")
            self.driver = None

def main():
    """主程序"""
    jarvis = JarvisAgent()
    
    if not jarvis.driver:
        print("❌ 浏览器启动失败，程序退出")
        return
    
    try:
        print("\n🚀 开始演示Jarvis功能...")
        
        # 1. 打开Google
        print("\n1️⃣ 打开Google首页")
        jarvis.open_url("https://www.google.com")
        time.sleep(2)
        
        # 2. 进行搜索
        print("\n2️⃣ 执行Google搜索")
        jarvis.search_google("Python AI开发教程")
        time.sleep(3)
        
        # 3. 截图
        print("\n3️⃣ 保存当前页面截图")
        jarvis.take_screenshot("google_search_result.png")
        
        # 4. 显示当前页面信息
        print(f"\n4️⃣ 当前页面信息:")
        print(f"   URL: {jarvis.get_current_url()}")
        print(f"   标题: {jarvis.get_page_title()}")
        
        # 5. 等待用户手动操作
        print("\n5️⃣ 等待用户操作")
        jarvis.wait_for_manual_action("您可以手动浏览页面，完成后按回车继续...")
        
        # 6. 调用公开API示例
        print("\n6️⃣ 调用GitHub公开API")
        api_result = jarvis.call_api("https://api.github.com/users/octocat")
        if api_result:
            print(f"   GitHub用户: {api_result.get('name', 'N/A')}")
            print(f"   公开仓库: {api_result.get('public_repos', 'N/A')}")
        
        # 7. 测试OpenAI API（如果已配置）
        print("\n7️⃣ 测试AI对话功能")
        ai_response = jarvis.call_openai_api("用一句话介绍Python编程语言")
        if ai_response:
            print(f"   AI回答: {ai_response}")
        
        # 8. 执行Python代码示例
        print("\n8️⃣ 执行Python代码")
        python_code = """
import datetime
import math

print("=" * 40)
print("🐍 Python代码执行演示")
print("=" * 40)
print(f"当前时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"圆周率: {math.pi:.6f}")
print("Hello from Jarvis AI Agent!")

# 简单计算
numbers = [1, 2, 3, 4, 5]
print(f"数字列表: {numbers}")
print(f"列表总和: {sum(numbers)}")
print(f"列表平均值: {sum(numbers)/len(numbers):.2f}")
print("=" * 40)
"""
        jarvis.execute_python_code(python_code)
        
        # 9. 打开更多网站示例
        print("\n9️⃣ 访问更多网站")
        sites = [
            ("GitHub", "https://github.com"),
            ("Stack Overflow", "https://stackoverflow.com")
        ]
        
        for name, url in sites:
            print(f"   正在打开 {name}...")
            jarvis.open_url(url)
            time.sleep(2)
            print(f"   ✅ {name} 已打开")
        
        print("\n🎉 演示完成！")
        print("💡 您可以继续手动操作浏览器，或按Ctrl+C退出程序")
        
        # 保持程序运行，让用户可以继续操作
        while True:
            user_input = input("\n输入命令 (help/quit): ").strip().lower()
            if user_input == 'quit':
                break
            elif user_input == 'help':
                print("""
可用命令:
- quit: 退出程序
- help: 显示帮助
- url <网址>: 打开指定网址
- search <关键词>: Google搜索
- screenshot: 截图
- info: 显示当前页面信息
                """)
            elif user_input.startswith('url '):
                url = user_input[4:].strip()
                jarvis.open_url(url)
            elif user_input.startswith('search '):
                query = user_input[7:].strip()
                jarvis.search_google(query)
            elif user_input == 'screenshot':
                filename = f"screenshot_{int(time.time())}.png"
                jarvis.take_screenshot(filename)
            elif user_input == 'info':
                print(f"URL: {jarvis.get_current_url()}")
                print(f"标题: {jarvis.get_page_title()}")
            else:
                print("未知命令，输入 'help' 查看帮助")
        
    except KeyboardInterrupt:
        print("\n🛑 用户中断程序")
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
    finally:
        jarvis.close()

if __name__ == "__main__":
    main()
