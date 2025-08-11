#!/usr/bin/env python3
"""
请求和响应对象
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import time

@dataclass
class Request:
    """请求对象"""
    action: str
    data: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取数据"""
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """设置数据"""
        self.data[key] = value

@dataclass
class Response:
    """响应对象"""
    success: bool = True
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    
    def set_error(self, error: str) -> None:
        """设置错误"""
        self.success = False
        self.error = error
    
    def set_data(self, key: str, value: Any) -> None:
        """设置数据"""
        self.data[key] = value