#!/usr/bin/env python3
"""
浏览器操作模块
增强版浏览器自动化功能，支持中间件和日志
"""

import time
import json
from typing import Dict, Any, Optional, List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from ..core.middleware import with_middleware
from ..utils.browser_profiles import BrowserProfileDetector

class BrowserModule:
    """浏览器操作模块"""
    
    def __init__(self, driver, config, logger, middleware_manager):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.middleware_manager = middleware_manager
        self.wait = WebDriverWait(driver, config.get('browser.timeout', 10))
    
    def execute_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """执行浏览器命令"""
        command_map = {
            'browser_navigate': self.navigate,
            'browser_click': self.click_element,
            'browser_input': self.input_text,
            'browser_scroll': self.scroll_page,
            'browser_screenshot': self.take_screenshot,
            'browser_get_text': self.get_element_text,
            'browser_wait_element': self.wait_for_element,
            'browser_execute_script': self.execute_script,
            'browser_get_page_info': self.get_page_info,
            'browser_search_google': self.search_google,
            'browser_list_profiles': self.list_browser_profiles,
            'browser_get_extensions': self.get_browser_extensions,
        }
        
        if command in command_map:
            return command_map[command](**kwargs)
        else:
            return {"success": False, "error": f"未知的浏览器命令: {command}"}
    
    @with_middleware
    def navigate(self, url: str, **kwargs) -> Dict[str, Any]:
        """导航到指定URL"""
        try:
            self.driver.get(url)
            time.sleep(2)  # 等待页面加载
            
            return {
                "success": True,
                "url": self.driver.current_url,
                "title": self.driver.title,
                "message": f"成功导航到: {url}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def click_element(self, selector: str, by: str = "css", timeout: int = None, **kwargs) -> Dict[str, Any]:
        """点击元素"""
        try:
            by_map = {
                "css": By.CSS_SELECTOR,
                "xpath": By.XPATH,
                "id": By.ID,
                "class": By.CLASS_NAME,
                "tag": By.TAG_NAME,
                "name": By.NAME
            }
            
            by_type = by_map.get(by, By.CSS_SELECTOR)
            wait_time = timeout or self.config.get('browser.timeout', 10)
            wait = WebDriverWait(self.driver, wait_time)
            
            element = wait.until(EC.element_to_be_clickable((by_type, selector)))
            element.click()
            
            return {
                "success": True,
                "message": f"成功点击元素: {selector}",
                "element_text": element.text[:100] if element.text else ""
            }
        except TimeoutException:
            return {"success": False, "error": f"元素不可点击或超时: {selector}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def input_text(self, selector: str, text: str, by: str = "css", clear: bool = True, **kwargs) -> Dict[str, Any]:
        """输入文本"""
        try:
            by_map = {
                "css": By.CSS_SELECTOR,
                "xpath": By.XPATH,
                "id": By.ID,
                "class": By.CLASS_NAME,
                "name": By.NAME
            }
            
            by_type = by_map.get(by, By.CSS_SELECTOR)
            element = self.wait.until(EC.presence_of_element_located((by_type, selector)))
            
            if clear:
                element.clear()
            
            element.send_keys(text)
            
            return {
                "success": True,
                "message": f"成功输入文本到: {selector}",
                "text": text[:100]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def scroll_page(self, direction: str = "down", pixels: int = None, **kwargs) -> Dict[str, Any]:
        """滚动页面"""
        try:
            if pixels:
                if direction == "down":
                    self.driver.execute_script(f"window.scrollBy(0, {pixels});")
                elif direction == "up":
                    self.driver.execute_script(f"window.scrollBy(0, -{pixels});")
            else:
                if direction == "down":
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                elif direction == "up":
                    self.driver.execute_script("window.scrollTo(0, 0);")
            
            time.sleep(1)  # 等待滚动完成
            
            return {
                "success": True,
                "message": f"页面滚动: {direction}",
                "scroll_position": self.driver.execute_script("return window.pageYOffset;")
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def take_screenshot(self, description: str = "", **kwargs) -> Dict[str, Any]:
        """截图"""
        try:
            filepath = self.logger.save_screenshot(self.driver, description, "manual")
            
            return {
                "success": True,
                "message": "截图成功",
                "filepath": filepath,
                "url": self.driver.current_url,
                "title": self.driver.title
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def get_element_text(self, selector: str, by: str = "css", **kwargs) -> Dict[str, Any]:
        """获取元素文本"""
        try:
            by_map = {
                "css": By.CSS_SELECTOR,
                "xpath": By.XPATH,
                "id": By.ID,
                "class": By.CLASS_NAME,
                "tag": By.TAG_NAME
            }
            
            by_type = by_map.get(by, By.CSS_SELECTOR)
            element = self.wait.until(EC.presence_of_element_located((by_type, selector)))
            text = element.text
            
            return {
                "success": True,
                "text": text,
                "message": f"成功获取元素文本: {selector}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def wait_for_element(self, selector: str, by: str = "css", timeout: int = None, **kwargs) -> Dict[str, Any]:
        """等待元素出现"""
        try:
            by_map = {
                "css": By.CSS_SELECTOR,
                "xpath": By.XPATH,
                "id": By.ID,
                "class": By.CLASS_NAME
            }
            
            by_type = by_map.get(by, By.CSS_SELECTOR)
            wait_time = timeout or self.config.get('browser.timeout', 10)
            wait = WebDriverWait(self.driver, wait_time)
            
            element = wait.until(EC.presence_of_element_located((by_type, selector)))
            
            return {
                "success": True,
                "message": f"元素已出现: {selector}",
                "element_text": element.text[:100] if element.text else ""
            }
        except TimeoutException:
            return {"success": False, "error": f"等待元素超时: {selector}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def execute_script(self, script: str, **kwargs) -> Dict[str, Any]:
        """执行JavaScript脚本"""
        try:
            result = self.driver.execute_script(script)
            
            return {
                "success": True,
                "result": result,
                "message": "JavaScript执行成功"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def get_page_info(self, **kwargs) -> Dict[str, Any]:
        """获取页面信息"""
        try:
            info = {
                "url": self.driver.current_url,
                "title": self.driver.title,
                "page_source_length": len(self.driver.page_source),
                "window_size": self.driver.get_window_size(),
                "cookies_count": len(self.driver.get_cookies()),
                "scroll_position": self.driver.execute_script("return window.pageYOffset;"),
                "page_height": self.driver.execute_script("return document.body.scrollHeight;")
            }
            
            return {
                "success": True,
                "info": info,
                "message": "页面信息获取成功"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def search_google(self, query: str, **kwargs) -> Dict[str, Any]:
        """Google搜索"""
        try:
            # 导航到Google
            self.driver.get("https://www.google.com")
            time.sleep(2)
            
            # 查找搜索框
            search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # 等待搜索结果
            self.wait.until(EC.presence_of_element_located((By.ID, "search")))
            time.sleep(2)
            
            # 获取搜索结果
            results = []
            try:
                result_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.g")[:5]  # 前5个结果
                for element in result_elements:
                    try:
                        title_elem = element.find_element(By.CSS_SELECTOR, "h3")
                        link_elem = element.find_element(By.CSS_SELECTOR, "a")
                        
                        results.append({
                            "title": title_elem.text,
                            "url": link_elem.get_attribute("href"),
                            "snippet": element.text[:200]
                        })
                    except:
                        continue
            except:
                pass
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "results_count": len(results),
                "message": f"Google搜索完成: {query}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def list_browser_profiles(self, **kwargs) -> Dict[str, Any]:
        """列出可用的浏览器配置文件"""
        try:
            detector = BrowserProfileDetector()
            browsers = detector.get_available_browsers()
            
            profile_info = {}
            for browser_name, profiles in browsers.items():
                profile_info[browser_name] = {}
                for profile_name, profile_path in profiles.items():
                    info = detector.get_profile_info(profile_path)
                    profile_info[browser_name][profile_name] = {
                        "path": str(profile_path),
                        "extensions_count": len(info["extensions"]),
                        "size_mb": info["size_mb"],
                        "has_bookmarks": info["bookmarks_exist"],
                        "has_history": info["history_exist"]
                    }
            
            # 获取推荐配置
            recommended = detector.get_recommended_profile()
            recommended_info = None
            if recommended:
                browser_name, profile_name, profile_path = recommended
                recommended_info = {
                    "browser": browser_name,
                    "profile": profile_name,
                    "path": str(profile_path)
                }
            
            return {
                "success": True,
                "browsers": profile_info,
                "recommended": recommended_info,
                "message": f"找到 {len(browsers)} 个浏览器配置"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def get_browser_extensions(self, browser_type: str = "Chrome", profile_name: str = "Default", **kwargs) -> Dict[str, Any]:
        """获取浏览器扩展信息"""
        try:
            detector = BrowserProfileDetector()
            browsers = detector.get_available_browsers()
            
            if browser_type not in browsers:
                return {"success": False, "error": f"未找到浏览器: {browser_type}"}
            
            if profile_name not in browsers[browser_type]:
                return {"success": False, "error": f"未找到配置文件: {profile_name}"}
            
            profile_path = browsers[browser_type][profile_name]
            extensions = detector.get_chrome_extensions(profile_path)
            
            # 按名称排序
            extensions.sort(key=lambda x: x["name"])
            
            return {
                "success": True,
                "browser": browser_type,
                "profile": profile_name,
                "extensions": extensions,
                "extensions_count": len(extensions),
                "message": f"找到 {len(extensions)} 个扩展"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
