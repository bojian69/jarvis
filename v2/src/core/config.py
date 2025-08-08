#!/usr/bin/env python3
"""
配置管理模块
统一管理所有配置项
"""

import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from pathlib import Path

class Config:
    """配置管理类"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.project_root = Path(__file__).parent.parent.parent
        self.config_dir = self.project_root / "config"
        self.logs_dir = self.project_root / "logs"
        
        # 确保目录存在
        self.config_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        (self.logs_dir / "screenshots").mkdir(exist_ok=True)
        (self.logs_dir / "debug").mkdir(exist_ok=True)
        (self.logs_dir / "error").mkdir(exist_ok=True)
        (self.logs_dir / "info").mkdir(exist_ok=True)
        
        # 加载环境变量
        load_dotenv()
        
        # 加载配置文件
        self.config_file = config_file or str(self.config_dir / "settings.json")
        self.settings = self._load_config()
        
        # API状态检查
        self.api_status = self._check_api_keys()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            "browser": {
                "headless": False,
                "window_size": [1920, 1080],
                "timeout": 10,
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "use_local_profile": True,
                "browser_type": "auto",  # "auto", "Chrome", "Edge"
                "profile_name": "Default",
                "enable_extensions": True,
                "load_images": True,
                "enable_javascript": True
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "max_file_size": "10MB",
                "backup_count": 5
            },
            "api": {
                "timeout": 30,
                "retry_count": 3,
                "retry_delay": 1
            },
            "screenshots": {
                "enabled": True,
                "quality": 90,
                "format": "PNG"
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # 合并配置
                    default_config.update(user_config)
            else:
                # 创建默认配置文件
                self._save_config(default_config)
        except Exception as e:
            print(f"⚠️ 配置文件加载失败，使用默认配置: {e}")
        
        return default_config
    
    def _save_config(self, config: Dict[str, Any]):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ 配置文件保存失败: {e}")
    
    def _check_api_keys(self) -> Dict[str, bool]:
        """检查API密钥状态"""
        return {
            'openai': bool(os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'your_openai_api_key_here'),
            'google': bool(os.getenv('GOOGLE_API_KEY') and os.getenv('GOOGLE_API_KEY') != 'your_google_api_key_here'),
            'github': bool(os.getenv('GITHUB_TOKEN') and os.getenv('GITHUB_TOKEN') != 'your_github_token_here'),
            'anthropic': bool(os.getenv('ANTHROPIC_API_KEY') and os.getenv('ANTHROPIC_API_KEY') != 'your_anthropic_api_key_here')
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值，支持点号分隔的嵌套键"""
        keys = key.split('.')
        value = self.settings
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split('.')
        config = self.settings
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self._save_config(self.settings)
    
    @property
    def browser_config(self) -> Dict[str, Any]:
        """浏览器配置"""
        return self.settings.get('browser', {})
    
    @property
    def logging_config(self) -> Dict[str, Any]:
        """日志配置"""
        return self.settings.get('logging', {})
    
    @property
    def api_config(self) -> Dict[str, Any]:
        """API配置"""
        return self.settings.get('api', {})
    
    @property
    def screenshots_config(self) -> Dict[str, Any]:
        """截图配置"""
        return self.settings.get('screenshots', {})
