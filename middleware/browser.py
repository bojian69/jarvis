#!/usr/bin/env python3
"""
浏览器中间件
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

from .core import BaseMiddleware
from .request import Request, Response
from .exceptions import MiddlewareError

class BrowserMiddleware(BaseMiddleware):
    """浏览器操作中间件"""
    
    def __init__(self):
        super().__init__("BrowserMiddleware")
        self.driver = None
        self.wait = None
    
    def before_process(self, request: Request) -> None:
        """初始化浏览器"""
        if request.action.startswith('browser_') and not self.driver:
            self._setup_browser()
    
    def process(self, request: Request, response: Response) -> None:
        """处理浏览器操作"""
        action = request.action
        
        if action == 'browser_open_url':
            self._open_url(request, response)
        elif action == 'browser_search_google':
            self._search_google(request, response)
        elif action == 'browser_screenshot':
            self._take_screenshot(request, response)
        elif action == 'browser_close':
            self._close_browser(request, response)
        elif action == 'browser_housing_london':
            self._open_student_housing_london(request, response)
        elif action == 'browser_wait_manual':
            self._wait_for_manual_action(request, response)
        elif action == 'browser_get_url':
            self._get_current_url(request, response)
        elif action == 'browser_get_title':
            self._get_page_title(request, response)
    
    def _setup_browser(self):
        """设置浏览器"""
        try:
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--window-size=1280,720")
            
            user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome/JarvisMiddleware")
            os.makedirs(user_data_dir, exist_ok=True)
            options.add_argument(f"--user-data-dir={user_data_dir}")
            
            try:
                self.driver = webdriver.Chrome(options=options)
            except:
                self.driver = uc.Chrome(options=options, version_main=138)
            
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            self.wait = WebDriverWait(self.driver, 10)
            
        except Exception as e:
            raise MiddlewareError(f"浏览器启动失败: {e}")
    
    def _open_url(self, request: Request, response: Response):
        """打开URL"""
        url = request.get('url')
        if not url:
            response.set_error("URL参数缺失")
            return
        
        try:
            self.driver.get(url)
            response.set_data('url', url)
            response.set_data('title', self.driver.title)
        except Exception as e:
            response.set_error(f"打开URL失败: {e}")
    
    def _search_google(self, request: Request, response: Response):
        """Google搜索"""
        query = request.get('query')
        if not query:
            response.set_error("搜索关键词缺失")
            return
        
        try:
            self.driver.get("https://www.google.com")
            search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
            search_box.clear()
            search_box.send_keys(query)
            search_box.submit()
            response.set_data('query', query)
        except Exception as e:
            response.set_error(f"搜索失败: {e}")
    
    def _take_screenshot(self, request: Request, response: Response):
        """截图"""
        filename = request.get('filename', f'screenshot_{int(time.time())}.png')
        try:
            self.driver.save_screenshot(filename)
            response.set_data('filename', filename)
        except Exception as e:
            response.set_error(f"截图失败: {e}")
    
    def _close_browser(self, request: Request, response: Response):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None
            response.set_data('closed', True)
    
    def _open_student_housing_london(self, request: Request, response: Response):
        """打开学生住房网站并选择London城市"""
        if not self.driver:
            response.set_error("浏览器未启动")
            return
        
        try:
            url = "https://wearehomesforstudents.com/agent-booking/xejs-uhomes"
            self.driver.get(url)
            response.set_data('url', url)
            response.set_data('action', 'housing_london_opened')
        except Exception as e:
            response.set_error(f"打开学生住房网站失败: {e}")
    
    def _wait_for_manual_action(self, request: Request, response: Response):
        """等待用户手动操作"""
        message = request.get('message', '请手动处理验证码或其他操作，完成后按回车继续...')
        print(f"⏸️  {message}")
        input()
        print("▶️  继续执行...")
        response.set_data('manual_action_completed', True)
    
    def _get_current_url(self, request: Request, response: Response):
        """获取当前页面URL"""
        if self.driver:
            response.set_data('url', self.driver.current_url)
        else:
            response.set_error("浏览器未启动")
    
    def _get_page_title(self, request: Request, response: Response):
        """获取当前页面标题"""
        if self.driver:
            response.set_data('title', self.driver.title)
        else:
            response.set_error("浏览器未启动")