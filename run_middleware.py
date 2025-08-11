#!/usr/bin/env python3
"""
Jarvis 中间件版本启动脚本
"""

import sys
import argparse
import subprocess
import os

def check_dependencies():
    """检查依赖"""
    try:
        import selenium
        import undetected_chromedriver
        import requests
        import streamlit
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        return False

def install_dependencies():
    """安装依赖"""
    print("📦 正在安装依赖...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ 依赖安装完成")

def run_cli():
    """运行命令行版本"""
    print("🚀 启动命令行版本...")
    from jarvis_agent import main
    main()

def run_gui():
    """运行GUI版本"""
    print("🚀 启动GUI版本...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "gui_middleware.py"])

def main():
    parser = argparse.ArgumentParser(description="Jarvis AI Agent - 中间件架构版本")
    parser.add_argument("--mode", choices=["cli", "gui"], default="gui", help="运行模式")
    parser.add_argument("--install", action="store_true", help="安装依赖")
    parser.add_argument("--check", action="store_true", help="检查环境")
    
    args = parser.parse_args()
    
    if args.install:
        install_dependencies()
        return
    
    if args.check:
        if check_dependencies():
            print("🎉 环境检查通过")
        else:
            print("❌ 环境检查失败，请运行 --install 安装依赖")
        return
    
    # 检查依赖
    if not check_dependencies():
        print("❌ 请先运行 python run_middleware.py --install 安装依赖")
        return
    
    print("🤖 Jarvis AI Agent - 中间件架构版本")
    print("=" * 50)
    
    if args.mode == "cli":
        run_cli()
    else:
        run_gui()

if __name__ == "__main__":
    main()