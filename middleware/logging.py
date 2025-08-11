#!/usr/bin/env python3
"""
日志中间件
"""

import logging
import time
from typing import Dict, Any

from .core import BaseMiddleware
from .request import Request, Response

class LoggingMiddleware(BaseMiddleware):
    """日志记录中间件"""
    
    def __init__(self, log_level=logging.INFO):
        super().__init__("LoggingMiddleware")
        self.logger = logging.getLogger("jarvis")
        self.logger.setLevel(log_level)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def process(self, request, response):
        """处理请求 - 日志中间件不需要处理逻辑"""
        pass
    
    def before_process(self, request: Request) -> None:
        """记录请求开始"""
        self.logger.info(f"开始处理请求: {request.action}")
        request.metadata['start_time'] = time.time()
    
    def after_process(self, request: Request, response: Response) -> None:
        """记录请求完成"""
        duration = time.time() - request.metadata.get('start_time', 0)
        status = "成功" if response.success else "失败"
        self.logger.info(f"请求处理完成: {request.action} - {status} - 耗时: {duration:.2f}s")
    
    def on_error(self, request: Request, response: Response, error: Exception) -> None:
        """记录错误"""
        self.logger.error(f"请求处理错误: {request.action} - {error}")