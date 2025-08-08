#!/usr/bin/env python3
"""
浏览器操作工具类
专门处理各种浏览器自动化任务
"""

import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class BrowserTools:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def click_element(self, selector, by=By.CSS_SELECTOR):
        """点击元素"""
        try:
            element = self.wait.until(EC.element_to_be_clickable((by, selector)))
            element.click()
            return True
        except Exception as e:
            print(f"❌ 点击元素失败: {e}")
            return False
    
    def input_text(self, selector, text, by=By.CSS_SELECTOR, clear=True):
        """输入文本"""
        try:
            element = self.wait.until(EC.presence_of_element_located((by, selector)))
            if clear:
                element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            print(f"❌ 输入文本失败: {e}")
            return False
    
    def get_text(self, selector, by=By.CSS_SELECTOR):
        """获取元素文本"""
        try:
            element = self.wait.until(EC.presence_of_element_located((by, selector)))
            return element.text
        except Exception as e:
            print(f"❌ 获取文本失败: {e}")
            return None
    
    def scroll_to_element(self, selector, by=By.CSS_SELECTOR):
        """滚动到元素"""
        try:
            element = self.driver.find_element(by, selector)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return True
        except Exception as e:
            print(f"❌ 滚动失败: {e}")
            return False
    
    def take_screenshot(self, filename):
        """截图"""
        try:
            self.driver.save_screenshot(filename)
            print(f"✅ 截图保存: {filename}")
            return True
        except Exception as e:
            print(f"❌ 截图失败: {e}")
            return False
    
    def execute_js(self, script):
        """执行JavaScript"""
        try:
            result = self.driver.execute_script(script)
            return result
        except Exception as e:
            print(f"❌ JavaScript执行失败: {e}")
            return None
    
    def wait_for_page_load(self, timeout=30):
        """等待页面加载完成"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            return True
        except Exception as e:
            print(f"❌ 页面加载超时: {e}")
            return False
    
    def handle_alert(self, accept=True):
        """处理弹窗"""
        try:
            alert = self.driver.switch_to.alert
            if accept:
                alert.accept()
            else:
                alert.dismiss()
            return True
        except Exception as e:
            print(f"❌ 处理弹窗失败: {e}")
            return False
    
    def switch_to_tab(self, tab_index):
        """切换标签页"""
        try:
            tabs = self.driver.window_handles
            if tab_index < len(tabs):
                self.driver.switch_to.window(tabs[tab_index])
                return True
            return False
        except Exception as e:
            print(f"❌ 切换标签页失败: {e}")
            return False
    
    def open_new_tab(self, url=None):
        """打开新标签页"""
        try:
            self.driver.execute_script("window.open('');")
            tabs = self.driver.window_handles
            self.driver.switch_to.window(tabs[-1])
            if url:
                self.driver.get(url)
            return True
        except Exception as e:
            print(f"❌ 打开新标签页失败: {e}")
            return False
