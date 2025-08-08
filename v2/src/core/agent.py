#!/usr/bin/env python3
"""
Jarvis主代理类
整合所有功能模块，提供统一接口
"""

import os
import time
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc

from .config import Config
from .logger import Logger
from .middleware import MiddlewareManager, LoggingMiddleware, ScreenshotMiddleware, RetryMiddleware
from ..modules.browser import BrowserModule
from ..modules.api import APIModule
from ..modules.code import CodeModule
from ..utils.browser_profiles import BrowserProfileDetector

class JarvisAgent:
    """Jarvis AI Agent 主类"""
    
    def __init__(self, config_file: Optional[str] = None):
        # 初始化配置
        self.config = Config(config_file)
        
        # 初始化日志
        self.logger = Logger(self.config)
        
        # 初始化中间件管理器
        self.middleware_manager = MiddlewareManager()
        self._setup_middleware()
        
        # 初始化浏览器
        self.driver = None
        
        # 初始化功能模块
        self.browser_module = None
        self.api_module = None
        self.code_module = None
        
        # 打印启动信息
        self._print_startup_info()
    
    def _setup_middleware(self):
        """设置中间件"""
        # 日志中间件
        self.middleware_manager.add_middleware(LoggingMiddleware(self.logger))
        
        # 截图中间件
        self.middleware_manager.add_middleware(
            ScreenshotMiddleware(self.logger, lambda: self.driver)
        )
        
        # 重试中间件
        self.middleware_manager.add_middleware(
            RetryMiddleware(
                max_retries=self.config.get('api.retry_count', 3),
                delay=self.config.get('api.retry_delay', 1)
            )
        )
    
    def _print_startup_info(self):
        """打印启动信息"""
        self.logger.info("🤖 Jarvis AI Agent 启动中...")
        self.logger.info("=" * 50)
        self.logger.info("📊 API服务状态:")
        
        for service, status in self.config.api_status.items():
            status_text = "✅ 已配置" if status else "❌ 未配置"
            self.logger.info(f"  {service.upper()} API: {status_text}")
        
        self.logger.info("=" * 50)
        self.logger.info("💡 提示: 浏览器自动化功能无需API密钥即可使用")
        
        if not any(self.config.api_status.values()):
            self.logger.info("💡 如需AI功能，请在.env文件中配置相应的API密钥")
        
        self.logger.info("=" * 50)
    
    def setup_browser(self, headless: bool = None, use_local_profile: bool = True, 
                      browser_type: str = "auto", profile_name: str = "Default") -> bool:
        """设置浏览器
        
        Args:
            headless: 是否使用无头模式
            use_local_profile: 是否使用本地浏览器配置文件
            browser_type: 浏览器类型 ("auto", "Chrome", "Edge")
            profile_name: 配置文件名称
        """
        try:
            if self.driver:
                self.logger.info("🌐 浏览器已经启动")
                return True
            
            self.logger.info("🌐 正在启动浏览器...")
            
            # 获取浏览器配置
            browser_config = self.config.browser_config
            if headless is not None:
                browser_config['headless'] = headless
            
            # Chrome选项
            chrome_options = Options()
            
            # 检测并使用本地浏览器配置
            if use_local_profile:
                profile_detector = BrowserProfileDetector()
                
                if browser_type == "auto":
                    # 自动选择推荐的浏览器配置
                    recommended = profile_detector.get_recommended_profile()
                    if recommended:
                        browser_name, profile, profile_path = recommended
                        self.logger.info(f"🔍 检测到本地浏览器: {browser_name} - {profile}")
                        
                        # 获取配置文件信息
                        profile_info = profile_detector.get_profile_info(profile_path)
                        self.logger.info(f"📊 配置文件信息: {len(profile_info['extensions'])} 个扩展, "
                                       f"{profile_info['size_mb']} MB")
                        
                        # 设置用户数据目录
                        chrome_options.add_argument(f"--user-data-dir={profile_path}")
                        chrome_options.add_argument(f"--profile-directory={profile}")
                        
                        # 显示扩展信息
                        if profile_info['extensions']:
                            self.logger.info("🧩 将使用现有扩展:")
                            for ext in profile_info['extensions'][:5]:  # 显示前5个扩展
                                self.logger.info(f"  - {ext['name']} (v{ext['version']})")
                            if len(profile_info['extensions']) > 5:
                                self.logger.info(f"  ... 还有 {len(profile_info['extensions']) - 5} 个扩展")
                    else:
                        self.logger.warning("⚠️ 未检测到本地浏览器配置，使用默认配置")
                        use_local_profile = False
                else:
                    # 使用指定的浏览器类型
                    browsers = profile_detector.get_available_browsers()
                    if browser_type in browsers and profile_name in browsers[browser_type]:
                        profile_path = browsers[browser_type][profile_name]
                        self.logger.info(f"🔍 使用指定浏览器: {browser_type} - {profile_name}")
                        
                        chrome_options.add_argument(f"--user-data-dir={profile_path}")
                        chrome_options.add_argument(f"--profile-directory={profile_name}")
                    else:
                        self.logger.warning(f"⚠️ 未找到指定的浏览器配置: {browser_type} - {profile_name}")
                        use_local_profile = False
            
            # 基础浏览器选项
            if browser_config.get('headless', False):
                chrome_options.add_argument('--headless')
            
            # 如果使用本地配置文件，保持现有设置
            if use_local_profile:
                # 使用本地配置文件时的选项
                chrome_options.add_argument('--no-first-run')
                chrome_options.add_argument('--no-default-browser-check')
                # 保持所有现有扩展启用
                chrome_options.add_argument('--disable-extensions-file-access-check')
                chrome_options.add_argument('--disable-extensions-http-throttling')
            else:
                # 不使用本地配置文件时的基础选项
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--disable-web-security')
                chrome_options.add_argument('--allow-running-insecure-content')
            
            # 设置窗口大小
            window_size = browser_config.get('window_size', [1920, 1080])
            chrome_options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
            
            # 设置用户代理
            user_agent = browser_config.get('user_agent')
            if user_agent:
                chrome_options.add_argument(f'--user-agent={user_agent}')
            
            # 创建驱动
            try:
                # 首先尝试使用 undetected_chromedriver
                self.driver = uc.Chrome(options=chrome_options)
                self.logger.info("✅ 使用 undetected_chromedriver 启动成功")
            except Exception as e:
                self.logger.warning(f"⚠️ undetected_chromedriver 启动失败: {e}")
                self.logger.info("🔄 尝试使用标准 ChromeDriver...")
                
                # 回退到标准 ChromeDriver
                try:
                    self.driver = webdriver.Chrome(options=chrome_options)
                    self.logger.info("✅ 使用标准 ChromeDriver 启动成功")
                except Exception as e2:
                    self.logger.error(f"❌ 标准 ChromeDriver 也启动失败: {e2}")
                    return False
            
            # 设置反检测
            if self.driver:
                try:
                    self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                except:
                    pass
            
            # 初始化浏览器模块
            self.browser_module = BrowserModule(self.driver, self.config, self.logger, self.middleware_manager)
            
            # 显示浏览器信息
            if use_local_profile:
                self.logger.info("✅ 浏览器启动成功 - 使用本地配置文件")
                self.logger.info("💡 您的登录状态、书签、扩展等都已保留")
            else:
                self.logger.info("✅ 浏览器启动成功 - 使用默认配置")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 浏览器启动失败: {e}")
            return False
    
    def setup_modules(self):
        """初始化功能模块"""
        # API模块
        self.api_module = APIModule(self.config, self.logger, self.middleware_manager)
        
        # 代码执行模块
        self.code_module = CodeModule(self.config, self.logger, self.middleware_manager)
        
        self.logger.info("✅ 功能模块初始化完成")
    
    def get_browser_module(self) -> Optional[BrowserModule]:
        """获取浏览器模块"""
        if not self.browser_module:
            if self.setup_browser():
                return self.browser_module
        return self.browser_module
    
    def get_api_module(self) -> APIModule:
        """获取API模块"""
        if not self.api_module:
            self.setup_modules()
        return self.api_module
    
    def get_code_module(self) -> CodeModule:
        """获取代码执行模块"""
        if not self.code_module:
            self.setup_modules()
        return self.code_module
    
    def execute_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """执行命令"""
        try:
            self.logger.info(f"🎯 执行命令: {command}")
            
            # 根据命令类型分发到不同模块
            if command.startswith('browser_'):
                browser_module = self.get_browser_module()
                if not browser_module:
                    return {"success": False, "error": "浏览器模块未初始化"}
                return browser_module.execute_command(command, **kwargs)
            
            elif command.startswith('api_'):
                api_module = self.get_api_module()
                return api_module.execute_command(command, **kwargs)
            
            elif command.startswith('code_'):
                code_module = self.get_code_module()
                return code_module.execute_command(command, **kwargs)
            
            else:
                return {"success": False, "error": f"未知命令: {command}"}
        
        except Exception as e:
            self.logger.error(f"命令执行失败: {e}")
            return {"success": False, "error": str(e)}
    
    def close(self):
        """关闭代理"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.logger.info("🔒 浏览器已关闭")
            
            self.logger.info("👋 Jarvis Agent 已关闭")
            
        except Exception as e:
            self.logger.error(f"关闭时出错: {e}")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
