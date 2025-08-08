#!/usr/bin/env python3
"""
中间件系统
支持请求/响应拦截、日志记录、错误处理等
"""

import time
import functools
from typing import Callable, Any, Dict, List, Optional
from abc import ABC, abstractmethod

class Middleware(ABC):
    """中间件基类"""
    
    @abstractmethod
    def before_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """请求前处理"""
        pass
    
    @abstractmethod
    def after_request(self, context: Dict[str, Any], result: Any) -> Any:
        """请求后处理"""
        pass
    
    @abstractmethod
    def on_error(self, context: Dict[str, Any], error: Exception) -> Optional[Any]:
        """错误处理"""
        pass

class LoggingMiddleware(Middleware):
    """日志中间件"""
    
    def __init__(self, logger):
        self.logger = logger
    
    def before_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context['start_time'] = time.time()
        self.logger.debug(f"🚀 开始执行: {context.get('action', 'Unknown')}")
        return context
    
    def after_request(self, context: Dict[str, Any], result: Any) -> Any:
        duration = time.time() - context.get('start_time', 0)
        self.logger.info(f"✅ 执行完成: {context.get('action', 'Unknown')} (耗时: {duration:.2f}s)")
        return result
    
    def on_error(self, context: Dict[str, Any], error: Exception) -> Optional[Any]:
        duration = time.time() - context.get('start_time', 0)
        self.logger.error(f"❌ 执行失败: {context.get('action', 'Unknown')} (耗时: {duration:.2f}s) - {str(error)}")
        return None

class ScreenshotMiddleware(Middleware):
    """截图中间件"""
    
    def __init__(self, logger, driver_getter: Callable):
        self.logger = logger
        self.get_driver = driver_getter
    
    def before_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # 操作前截图
        if context.get('screenshot_before', False):
            driver = self.get_driver()
            if driver:
                self.logger.save_screenshot(
                    driver, 
                    f"before_{context.get('action', 'action')}", 
                    "before"
                )
        return context
    
    def after_request(self, context: Dict[str, Any], result: Any) -> Any:
        # 操作后截图
        if context.get('screenshot_after', True):
            driver = self.get_driver()
            if driver:
                self.logger.save_screenshot(
                    driver, 
                    f"after_{context.get('action', 'action')}", 
                    "after"
                )
        return result
    
    def on_error(self, context: Dict[str, Any], error: Exception) -> Optional[Any]:
        # 错误时截图
        driver = self.get_driver()
        if driver:
            self.logger.save_screenshot(
                driver, 
                f"error_{context.get('action', 'action')}", 
                "error"
            )
        return None

class RetryMiddleware(Middleware):
    """重试中间件"""
    
    def __init__(self, max_retries: int = 3, delay: float = 1.0):
        self.max_retries = max_retries
        self.delay = delay
    
    def before_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context['retry_count'] = 0
        return context
    
    def after_request(self, context: Dict[str, Any], result: Any) -> Any:
        return result
    
    def on_error(self, context: Dict[str, Any], error: Exception) -> Optional[Any]:
        retry_count = context.get('retry_count', 0)
        if retry_count < self.max_retries:
            context['retry_count'] = retry_count + 1
            time.sleep(self.delay)
            return 'RETRY'  # 特殊返回值表示需要重试
        return None

class ValidationMiddleware(Middleware):
    """参数验证中间件"""
    
    def __init__(self, validators: Dict[str, Callable] = None):
        self.validators = validators or {}
    
    def before_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        action = context.get('action')
        if action in self.validators:
            validator = self.validators[action]
            if not validator(context):
                raise ValueError(f"参数验证失败: {action}")
        return context
    
    def after_request(self, context: Dict[str, Any], result: Any) -> Any:
        return result
    
    def on_error(self, context: Dict[str, Any], error: Exception) -> Optional[Any]:
        return None

class MiddlewareManager:
    """中间件管理器"""
    
    def __init__(self):
        self.middlewares: List[Middleware] = []
    
    def add_middleware(self, middleware: Middleware):
        """添加中间件"""
        self.middlewares.append(middleware)
    
    def remove_middleware(self, middleware_class):
        """移除指定类型的中间件"""
        self.middlewares = [m for m in self.middlewares if not isinstance(m, middleware_class)]
    
    def execute_with_middleware(self, func: Callable, context: Dict[str, Any]) -> Any:
        """使用中间件执行函数"""
        # 执行前置中间件
        for middleware in self.middlewares:
            try:
                context = middleware.before_request(context)
            except Exception as e:
                # 如果前置中间件出错，执行错误处理
                for error_middleware in reversed(self.middlewares):
                    try:
                        result = error_middleware.on_error(context, e)
                        if result is not None:
                            return result
                    except:
                        continue
                raise e
        
        # 执行主函数（支持重试）
        max_attempts = 10  # 防止无限重试
        attempt = 0
        
        while attempt < max_attempts:
            try:
                result = func(**context.get('args', {}))
                
                # 执行后置中间件
                for middleware in reversed(self.middlewares):
                    try:
                        result = middleware.after_request(context, result)
                    except Exception as e:
                        # 后置中间件出错，执行错误处理
                        for error_middleware in reversed(self.middlewares):
                            try:
                                error_result = error_middleware.on_error(context, e)
                                if error_result is not None:
                                    return error_result
                            except:
                                continue
                        raise e
                
                return result
                
            except Exception as e:
                # 执行错误中间件
                should_retry = False
                for middleware in reversed(self.middlewares):
                    try:
                        error_result = middleware.on_error(context, e)
                        if error_result == 'RETRY':
                            should_retry = True
                        elif error_result is not None:
                            return error_result
                    except:
                        continue
                
                if not should_retry:
                    raise e
                
                attempt += 1
        
        raise Exception(f"达到最大重试次数 ({max_attempts})")

def with_middleware(func=None, **context_kwargs):
    """装饰器：为函数添加中间件支持"""
    def decorator(f):
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            # 获取实例的中间件管理器
            middleware_manager = getattr(self, 'middleware_manager', None)
            if not middleware_manager:
                # 如果没有中间件管理器，直接执行函数
                return f(self, *args, **kwargs)
            
            context = {
                'action': f.__name__,
                'args': kwargs,
                **context_kwargs
            }
            
            # 创建一个包装函数来执行原始方法
            def execute_func(**exec_kwargs):
                return f(self, **exec_kwargs)
            
            return middleware_manager.execute_with_middleware(execute_func, context)
        return wrapper
    
    if func is None:
        return decorator
    else:
        return decorator(func)
