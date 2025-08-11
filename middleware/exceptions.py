#!/usr/bin/env python3
"""
中间件异常类
"""

class MiddlewareError(Exception):
    """中间件基础异常"""
    pass

class ValidationError(MiddlewareError):
    """验证错误"""
    pass

class AuthenticationError(MiddlewareError):
    """认证错误"""
    pass

class RateLimitError(MiddlewareError):
    """限流错误"""
    pass