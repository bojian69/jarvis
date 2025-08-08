#!/usr/bin/env python3
"""
增强日志系统
支持多级别日志、截图保存、结构化日志
"""

import logging
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from logging.handlers import RotatingFileHandler

class Logger:
    """增强日志管理器"""
    
    def __init__(self, config):
        self.config = config
        self.logs_dir = config.logs_dir
        self.screenshots_dir = self.logs_dir / "screenshots"
        
        # 创建日志器
        self.logger = logging.getLogger('jarvis')
        self.logger.setLevel(getattr(logging, config.get('logging.level', 'INFO')))
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """设置日志处理器"""
        formatter = logging.Formatter(
            self.config.get('logging.format', 
                           '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 文件处理器 - 不同级别分别记录
        log_levels = ['debug', 'info', 'error']
        for level in log_levels:
            log_file = self.logs_dir / level / f"{level}.log"
            log_file.parent.mkdir(exist_ok=True)
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=self._parse_size(self.config.get('logging.max_file_size', '10MB')),
                backupCount=self.config.get('logging.backup_count', 5),
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            
            # 设置不同级别的过滤器
            if level == 'debug':
                file_handler.setLevel(logging.DEBUG)
            elif level == 'info':
                file_handler.setLevel(logging.INFO)
                file_handler.addFilter(lambda record: record.levelno < logging.ERROR)
            elif level == 'error':
                file_handler.setLevel(logging.ERROR)
            
            self.logger.addHandler(file_handler)
    
    def _parse_size(self, size_str: str) -> int:
        """解析文件大小字符串"""
        size_str = size_str.upper()
        if size_str.endswith('KB'):
            return int(size_str[:-2]) * 1024
        elif size_str.endswith('MB'):
            return int(size_str[:-2]) * 1024 * 1024
        elif size_str.endswith('GB'):
            return int(size_str[:-2]) * 1024 * 1024 * 1024
        else:
            return int(size_str)
    
    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """调试日志"""
        self._log_with_extra(logging.DEBUG, message, extra)
    
    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """信息日志"""
        self._log_with_extra(logging.INFO, message, extra)
    
    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """警告日志"""
        self._log_with_extra(logging.WARNING, message, extra)
    
    def error(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """错误日志"""
        self._log_with_extra(logging.ERROR, message, extra)
    
    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """严重错误日志"""
        self._log_with_extra(logging.CRITICAL, message, extra)
    
    def _log_with_extra(self, level: int, message: str, extra: Optional[Dict[str, Any]] = None):
        """带额外信息的日志记录"""
        if extra:
            # 将额外信息添加到消息中
            extra_str = json.dumps(extra, ensure_ascii=False, indent=2)
            message = f"{message}\n额外信息: {extra_str}"
        
        self.logger.log(level, message)
    
    def save_screenshot(self, driver, description: str = "", action: str = "") -> Optional[str]:
        """保存截图到日志目录"""
        if not self.config.get('screenshots.enabled', True):
            return None
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"{timestamp}_{action}_{description}.png".replace(" ", "_")
            filepath = self.screenshots_dir / filename
            
            # 保存截图
            driver.save_screenshot(str(filepath))
            
            # 记录截图信息
            screenshot_info = {
                "timestamp": timestamp,
                "action": action,
                "description": description,
                "filepath": str(filepath),
                "url": driver.current_url if hasattr(driver, 'current_url') else "N/A",
                "title": driver.title if hasattr(driver, 'title') else "N/A"
            }
            
            self.info(f"📸 截图已保存: {filename}", screenshot_info)
            return str(filepath)
            
        except Exception as e:
            self.error(f"截图保存失败: {e}")
            return None
    
    def log_action(self, action: str, details: Dict[str, Any], success: bool = True):
        """记录操作日志"""
        log_data = {
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "details": details
        }
        
        if success:
            self.info(f"✅ 操作成功: {action}", log_data)
        else:
            self.error(f"❌ 操作失败: {action}", log_data)
    
    def log_api_call(self, api_name: str, endpoint: str, method: str, 
                     status_code: Optional[int] = None, response_time: Optional[float] = None,
                     error: Optional[str] = None):
        """记录API调用日志"""
        api_log = {
            "api_name": api_name,
            "endpoint": endpoint,
            "method": method,
            "timestamp": datetime.now().isoformat(),
            "status_code": status_code,
            "response_time": response_time,
            "error": error
        }
        
        if error:
            self.error(f"🔴 API调用失败: {api_name} {method} {endpoint}", api_log)
        else:
            self.info(f"🟢 API调用成功: {api_name} {method} {endpoint}", api_log)
    
    def get_recent_logs(self, level: str = "info", lines: int = 100) -> list:
        """获取最近的日志记录"""
        log_file = self.logs_dir / level / f"{level}.log"
        
        if not log_file.exists():
            return []
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return all_lines[-lines:] if len(all_lines) > lines else all_lines
        except Exception as e:
            self.error(f"读取日志文件失败: {e}")
            return []
