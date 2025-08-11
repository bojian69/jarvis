#!/usr/bin/env python3
"""
依赖冲突修复脚本
"""

import subprocess
import sys

def fix_dependencies():
    """修复依赖冲突"""
    print("🔧 修复依赖冲突...")
    
    # 升级冲突的包
    packages_to_upgrade = [
        "openai>=1.40.1,<2.0.0",
        "python-dotenv>=1.0.1,<2.0.0"
    ]
    
    for package in packages_to_upgrade:
        print(f"📦 升级 {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("✅ 依赖冲突修复完成")

if __name__ == "__main__":
    fix_dependencies()