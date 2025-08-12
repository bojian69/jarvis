#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化外挂存储目录
"""

import os
from pathlib import Path

def init_external_storage():
    """初始化外挂磁盘存储目录"""
    base_path = Path("/Volumes/common/jarvis")
    
    # 创建必要的目录
    directories = [
        base_path / "documents" / "pdf",
        base_path / "documents" / "markdown", 
        base_path / "documents" / "raw",
        base_path / "vector_db",
        base_path / "uploads",
        base_path / "cache",
        base_path / "logs"
    ]
    
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            os.chmod(directory, 0o755)
            print(f"✅ 创建目录: {directory}")
        except Exception as e:
            print(f"❌ 创建目录失败 {directory}: {e}")
    
    print("🎉 外挂存储初始化完成")

if __name__ == "__main__":
    init_external_storage()