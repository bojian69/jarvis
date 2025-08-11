#!/usr/bin/env python3
"""
Jarvis Agent - 中间件架构版本
统一的智能助手，集成所有功能
"""

import sys
import os
import subprocess
import argparse
import logging
import time
from middleware import MiddlewareManager, Request, Response
from middleware.browser import BrowserMiddleware
from middleware.api import APIMiddleware
from middleware.python_executor import PythonExecutorMiddleware
from middleware.logging import LoggingMiddleware
from middleware.validation import ValidationMiddleware

class JarvisAgent:
    """Jarvis智能助手 - 中间件架构版本"""
    
    def __init__(self):
        self._setup_logging()
        self.logger = logging.getLogger("jarvis")
        self.logger.info("初始化Jarvis Agent...")
        
        self.middleware_manager = MiddlewareManager()
        self._setup_middlewares()
        self._print_startup_info()
        
        self.logger.info("Jarvis Agent初始化完成")
    
    def _setup_middlewares(self):
        """设置中间件"""
        self.middleware_manager.add(LoggingMiddleware())
        self.middleware_manager.add(ValidationMiddleware())
        self.middleware_manager.add(BrowserMiddleware())
        self.middleware_manager.add(APIMiddleware())
        self.middleware_manager.add(PythonExecutorMiddleware())
    
    def _setup_logging(self):
        """设置日志"""
        os.makedirs('logs', exist_ok=True)
        log_file = f'logs/jarvis_{time.strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_file, encoding='utf-8')
            ]
        )
    
    def _print_startup_info(self):
        """打印启动信息"""
        startup_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print("🤖 Jarvis AI Agent - 中间件架构")
        print("=" * 50)
        print(f"⏰ 启动时间: {startup_time}")
        print("💡 核心功能无需API密钥即可使用")
        print("=" * 50)
        
        self.logger.info(f"Jarvis Agent启动 - {startup_time}")
        self.logger.info("中间件架构已加载")
    
    def open_url(self, url: str) -> Response:
        """打开URL"""
        request = Request(action='browser_open_url', data={'url': url})
        return self.middleware_manager.process(request)
    
    def search_google(self, query: str) -> Response:
        """Google搜索"""
        request = Request(action='browser_search_google', data={'query': query})
        return self.middleware_manager.process(request)
    
    def take_screenshot(self, filename: str = None) -> Response:
        """截图"""
        data = {'filename': filename} if filename else {}
        request = Request(action='browser_screenshot', data=data)
        return self.middleware_manager.process(request)
    
    def close_browser(self) -> Response:
        """关闭浏览器"""
        request = Request(action='browser_close')
        return self.middleware_manager.process(request)
    
    def open_student_housing_london(self) -> Response:
        """打开学生住房网站并选择London城市"""
        request = Request(action='browser_housing_london')
        return self.middleware_manager.process(request)
    
    def wait_for_manual_action(self, message: str = "请手动处理验证码或其他操作，完成后按回车继续...") -> Response:
        """等待用户手动操作"""
        request = Request(action='browser_wait_manual', data={'message': message})
        return self.middleware_manager.process(request)
    
    def get_current_url(self) -> Response:
        """获取当前页面URL"""
        request = Request(action='browser_get_url')
        return self.middleware_manager.process(request)
    
    def get_page_title(self) -> Response:
        """获取当前页面标题"""
        request = Request(action='browser_get_title')
        return self.middleware_manager.process(request)
    
    def call_api(self, url: str, method: str = "GET", headers: dict = None, data: dict = None) -> Response:
        """调用第三方API"""
        request_data = {'url': url, 'method': method, 'headers': headers or {}, 'data': data or {}}
        request = Request(action='api_call', data=request_data)
        return self.middleware_manager.process(request)
    
    def call_api_get(self, url: str, headers: dict = None, params: dict = None) -> Response:
        """GET请求"""
        data = {'url': url, 'headers': headers or {}, 'params': params or {}}
        request = Request(action='api_get', data=data)
        return self.middleware_manager.process(request)
    
    def call_api_post(self, url: str, data: dict = None, headers: dict = None) -> Response:
        """POST请求"""
        request_data = {'url': url, 'data': data or {}, 'headers': headers or {}}
        request = Request(action='api_post', data=request_data)
        return self.middleware_manager.process(request)
    
    def call_openai_api(self, prompt: str, model: str = 'gpt-3.5-turbo') -> Response:
        """调用OpenAI API"""
        data = {'prompt': prompt, 'model': model}
        request = Request(action='api_openai', data=data)
        return self.middleware_manager.process(request)
    
    def call_github_api(self, endpoint: str) -> Response:
        """调用GitHub API"""
        data = {'endpoint': endpoint}
        request = Request(action='api_github', data=data)
        return self.middleware_manager.process(request)
    
    def call_weather_api(self, city: str) -> Response:
        """调用天气API"""
        data = {'city': city}
        request = Request(action='api_weather', data=data)
        return self.middleware_manager.process(request)
    
    def execute_python_code(self, code: str) -> Response:
        """执行Python代码"""
        data = {'code': code}
        request = Request(action='python_execute', data=data)
        return self.middleware_manager.process(request)

# 统一的运行功能
def check_dependencies():
    """检查依赖"""
    required_packages = {
        'selenium': 'selenium',
        'requests': 'requests', 
        'streamlit': 'streamlit',
        'undetected-chromedriver': 'undetected_chromedriver',
        'python-dotenv': 'dotenv'
    }
    
    missing_packages = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    return missing_packages

def install_dependencies():
    """安装依赖"""
    logger = logging.getLogger("jarvis")
    print("📦 正在安装依赖...")
    logger.info("开始安装依赖")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖安装完成")
        logger.info("依赖安装成功")
    except subprocess.CalledProcessError as e:
        print("⚠️ 检测到依赖冲突，尝试强制重新安装...")
        logger.warning(f"依赖冲突: {e}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--force-reinstall", "-r", "requirements.txt"])
        print("✅ 依赖安装完成")
        logger.info("依赖强制重新安装成功")

def run_cli():
    """运行命令行版本"""
    logger = logging.getLogger("jarvis")
    print("🚀 启动命令行版本...")
    logger.info("启动CLI模式")
    demo_cli()

def run_gui():
    """运行GUI版本"""
    logger = logging.getLogger("jarvis")
    print("🚀 启动GUI版本...")
    logger.info("启动GUI模式")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "gui_middleware.py"])
    except Exception as e:
        logger.error(f"GUI启动失败: {e}")

def demo_cli():
    """命令行演示程序"""
    jarvis = JarvisAgent()
    
    # 1. 打开网页
    print("\n1️⃣ 打开Google")
    response = jarvis.open_url("https://www.google.com")
    if response.success:
        print(f"✅ 成功打开: {response.data.get('title', 'N/A')}")
    else:
        print(f"❌ 失败: {response.error}")
    
    # 2. 搜索
    print("\n2️⃣ Google搜索")
    response = jarvis.search_google("Python中间件架构")
    if response.success:
        print("✅ 搜索完成")
    else:
        print(f"❌ 搜索失败: {response.error}")
    
    # 3. 截图
    print("\n3️⃣ 截图")
    response = jarvis.take_screenshot("demo.png")
    if response.success:
        print(f"✅ 截图保存: {response.data.get('filename')}")
    else:
        print(f"❌ 截图失败: {response.error}")
    
    # 4. API调用
    print("\n4️⃣ 调用GitHub API")
    response = jarvis.call_github_api("users/octocat")
    if response.success:
        result = response.data.get('result', {})
        print(f"✅ 用户: {result.get('name', 'N/A')}")
    else:
        print(f"❌ API调用失败: {response.error}")
    
    # 5. Python代码执行
    print("\n5️⃣ 执行Python代码")
    code = """
import datetime
import math

print("Hello from Jarvis Middleware!")
print(f"当前时间: {datetime.datetime.now()}")
print(f"圆周率: {math.pi:.6f}")

numbers = [1, 2, 3, 4, 5]
print(f"数字总和: {sum(numbers)}")
"""
    response = jarvis.execute_python_code(code)
    if response.success:
        print("✅ 代码执行成功:")
        print(response.data.get('output', ''))
    else:
        print(f"❌ 代码执行失败: {response.error}")
    
    # 6. 关闭浏览器
    print("\n6️⃣ 关闭浏览器")
    response = jarvis.close_browser()
    if response.success:
        print("✅ 浏览器已关闭")
    else:
        print(f"❌ 关闭失败: {response.error}")
    
    print("\n🎉 演示完成!")

def main():
    # 设置基础日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("jarvis")
    
    parser = argparse.ArgumentParser(description="Jarvis AI Agent - 中间件架构版本")
    parser.add_argument("--mode", choices=["cli", "gui"], default="gui", help="运行模式")
    parser.add_argument("--install", action="store_true", help="安装依赖")
    parser.add_argument("--check", action="store_true", help="检查环境")
    
    args = parser.parse_args()
    logger.info(f"启动参数: {args}")
    
    if args.install:
        install_dependencies()
        return
    
    if args.check:
        missing = check_dependencies()
        if missing:
            print(f"❌ 缺少依赖: {', '.join(missing)}")
            print("❗ 请运行 --install 安装依赖")
        else:
            print("✅ 所有依赖已安装")
            print("🎉 环境检查通过")
        return
    
    # 检查依赖
    missing = check_dependencies()
    if missing:
        print(f"❌ 请先运行 python jarvis_agent.py --install 安装依赖")
        return
    
    logger.info(f"启动模式: {args.mode}")
    if args.mode == "cli":
        run_cli()
    else:
        run_gui()

if __name__ == "__main__":
    main()