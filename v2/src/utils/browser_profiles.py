#!/usr/bin/env python3
"""
浏览器配置文件检测工具
自动检测本地浏览器配置和插件
"""

import os
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class BrowserProfileDetector:
    """浏览器配置文件检测器"""
    
    def __init__(self):
        self.system = platform.system()
        self.user_home = Path.home()
    
    def get_chrome_profiles(self) -> Dict[str, Path]:
        """获取Chrome浏览器配置文件路径"""
        profiles = {}
        
        if self.system == "Darwin":  # macOS
            chrome_base = self.user_home / "Library/Application Support/Google/Chrome"
        elif self.system == "Windows":
            chrome_base = self.user_home / "AppData/Local/Google/Chrome/User Data"
        elif self.system == "Linux":
            chrome_base = self.user_home / ".config/google-chrome"
        else:
            return profiles
        
        if not chrome_base.exists():
            return profiles
        
        # 检查默认配置文件
        default_profile = chrome_base / "Default"
        if default_profile.exists():
            profiles["Default"] = default_profile.parent
        
        # 检查其他配置文件
        for profile_dir in chrome_base.glob("Profile *"):
            if profile_dir.is_dir():
                profile_name = profile_dir.name
                profiles[profile_name] = chrome_base
        
        return profiles
    
    def get_edge_profiles(self) -> Dict[str, Path]:
        """获取Edge浏览器配置文件路径"""
        profiles = {}
        
        if self.system == "Darwin":  # macOS
            edge_base = self.user_home / "Library/Application Support/Microsoft Edge"
        elif self.system == "Windows":
            edge_base = self.user_home / "AppData/Local/Microsoft/Edge/User Data"
        elif self.system == "Linux":
            edge_base = self.user_home / ".config/microsoft-edge"
        else:
            return profiles
        
        if not edge_base.exists():
            return profiles
        
        # 检查默认配置文件
        default_profile = edge_base / "Default"
        if default_profile.exists():
            profiles["Default"] = default_profile.parent
        
        return profiles
    
    def get_available_browsers(self) -> Dict[str, Dict[str, Path]]:
        """获取所有可用的浏览器配置"""
        browsers = {}
        
        chrome_profiles = self.get_chrome_profiles()
        if chrome_profiles:
            browsers["Chrome"] = chrome_profiles
        
        edge_profiles = self.get_edge_profiles()
        if edge_profiles:
            browsers["Edge"] = edge_profiles
        
        return browsers
    
    def get_chrome_extensions(self, profile_path: Path) -> List[Dict[str, str]]:
        """获取Chrome扩展信息"""
        extensions = []
        
        if self.system == "Darwin":  # macOS
            extensions_dir = profile_path / "Default/Extensions"
        elif self.system == "Windows":
            extensions_dir = profile_path / "Default/Extensions"
        elif self.system == "Linux":
            extensions_dir = profile_path / "Default/Extensions"
        else:
            return extensions
        
        if not extensions_dir.exists():
            return extensions
        
        for ext_dir in extensions_dir.iterdir():
            if ext_dir.is_dir():
                # 获取扩展的最新版本
                version_dirs = [d for d in ext_dir.iterdir() if d.is_dir()]
                if version_dirs:
                    latest_version = max(version_dirs, key=lambda x: x.name)
                    manifest_file = latest_version / "manifest.json"
                    
                    if manifest_file.exists():
                        try:
                            import json
                            with open(manifest_file, 'r', encoding='utf-8') as f:
                                manifest = json.load(f)
                            
                            extensions.append({
                                "id": ext_dir.name,
                                "name": manifest.get("name", "Unknown"),
                                "version": latest_version.name,
                                "description": manifest.get("description", "")
                            })
                        except:
                            extensions.append({
                                "id": ext_dir.name,
                                "name": "Unknown Extension",
                                "version": latest_version.name,
                                "description": ""
                            })
        
        return extensions
    
    def get_recommended_profile(self) -> Optional[Tuple[str, str, Path]]:
        """获取推荐的浏览器配置文件"""
        browsers = self.get_available_browsers()
        
        # 优先选择Chrome
        if "Chrome" in browsers:
            chrome_profiles = browsers["Chrome"]
            if "Default" in chrome_profiles:
                return ("Chrome", "Default", chrome_profiles["Default"])
            else:
                # 选择第一个可用的配置文件
                profile_name = list(chrome_profiles.keys())[0]
                return ("Chrome", profile_name, chrome_profiles[profile_name])
        
        # 其次选择Edge
        if "Edge" in browsers:
            edge_profiles = browsers["Edge"]
            if "Default" in edge_profiles:
                return ("Edge", "Default", edge_profiles["Default"])
        
        return None
    
    def validate_profile_path(self, profile_path: Path) -> bool:
        """验证配置文件路径是否有效"""
        if not profile_path.exists():
            return False
        
        # 检查是否包含必要的Chrome配置文件
        required_files = ["Local State", "Default"]
        for file_name in required_files:
            if not (profile_path / file_name).exists():
                return False
        
        return True
    
    def get_profile_info(self, profile_path: Path) -> Dict[str, any]:
        """获取配置文件详细信息"""
        info = {
            "path": str(profile_path),
            "exists": profile_path.exists(),
            "extensions": [],
            "bookmarks_exist": False,
            "history_exist": False,
            "size_mb": 0
        }
        
        if not profile_path.exists():
            return info
        
        # 获取扩展信息
        info["extensions"] = self.get_chrome_extensions(profile_path)
        
        # 检查书签和历史记录
        default_dir = profile_path / "Default"
        if default_dir.exists():
            bookmarks_file = default_dir / "Bookmarks"
            history_file = default_dir / "History"
            
            info["bookmarks_exist"] = bookmarks_file.exists()
            info["history_exist"] = history_file.exists()
        
        # 计算目录大小
        try:
            total_size = sum(f.stat().st_size for f in profile_path.rglob('*') if f.is_file())
            info["size_mb"] = round(total_size / (1024 * 1024), 2)
        except:
            info["size_mb"] = 0
        
        return info
