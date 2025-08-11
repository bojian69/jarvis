#!/usr/bin/env python3
"""
中间件核心系统
"""

from abc import ABC, abstractmethod
from typing import List, Callable, Any
import logging
from .request import Request, Response
from .exceptions import MiddlewareError

logger = logging.getLogger(__name__)

class BaseMiddleware(ABC):
    """中间件基类"""
    
    def __init__(self, name: str = None):
        self.name = name or self.__class__.__name__
        self.enabled = True
    
    @abstractmethod
    def process(self, request: Request, response: Response) -> None:
        """处理请求"""
        pass
    
    def before_process(self, request: Request) -> None:
        """预处理"""
        pass
    
    def after_process(self, request: Request, response: Response) -> None:
        """后处理"""
        pass
    
    def on_error(self, request: Request, response: Response, error: Exception) -> None:
        """错误处理"""
        logger.error(f"Middleware {self.name} error: {error}")

class MiddlewareManager:
    """中间件管理器"""
    
    def __init__(self):
        self.middlewares: List[BaseMiddleware] = []
        self.logger = logging.getLogger(__name__)
    
    def add(self, middleware: BaseMiddleware) -> None:
        """添加中间件"""
        self.middlewares.append(middleware)
        self.logger.info(f"Added middleware: {middleware.name}")
    
    def remove(self, middleware_name: str) -> None:
        """移除中间件"""
        self.middlewares = [m for m in self.middlewares if m.name != middleware_name]
        self.logger.info(f"Removed middleware: {middleware_name}")
    
    def process(self, request: Request) -> Response:
        """处理请求"""
        response = Response()
        
        try:
            # 执行预处理
            for middleware in self.middlewares:
                if middleware.enabled:
                    middleware.before_process(request)
            
            # 执行主处理
            for middleware in self.middlewares:
                if middleware.enabled:
                    middleware.process(request, response)
                    if not response.success:
                        break
            
            # 执行后处理
            for middleware in reversed(self.middlewares):
                if middleware.enabled:
                    middleware.after_process(request, response)
                    
        except Exception as e:
            response.set_error(str(e))
            # 执行错误处理
            for middleware in self.middlewares:
                if middleware.enabled:
                    middleware.on_error(request, response, e)
        
        return response