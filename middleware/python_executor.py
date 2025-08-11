#!/usr/bin/env python3
"""
Python代码执行中间件
"""

import sys
from io import StringIO
import contextlib
import datetime
import math
import json

from .core import BaseMiddleware
from .request import Request, Response
from .exceptions import MiddlewareError

class PythonExecutorMiddleware(BaseMiddleware):
    """Python代码执行中间件"""
    
    def __init__(self):
        super().__init__("PythonExecutorMiddleware")
        self.safe_globals = self._create_safe_globals()
    
    def _create_safe_globals(self):
        """创建安全的执行环境"""
        return {
            '__builtins__': {
                'print': print,
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'list': list,
                'dict': dict,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'sum': sum,
                'max': max,
                'min': min,
                'abs': abs,
                'round': round,
                'sorted': sorted,
                'reversed': reversed,
            },
            'datetime': datetime,
            'math': math,
            'json': json,
        }
    
    def process(self, request: Request, response: Response) -> None:
        """处理Python代码执行"""
        if request.action != 'python_execute':
            return
        
        code = request.get('code')
        if not code:
            response.set_error("代码内容缺失")
            return
        
        try:
            output = StringIO()
            with contextlib.redirect_stdout(output):
                exec(code, self.safe_globals.copy())
            
            result = output.getvalue()
            response.set_data('output', result)
            response.set_data('executed', True)
            
        except Exception as e:
            response.set_error(f"代码执行失败: {e}")