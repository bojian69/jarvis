#!/usr/bin/env python3
"""
Jarvis启动脚本
提供多种启动方式，支持无API密钥运行
"""

import sys
import os
import subprocess
import argparse

def check_dependencies():
    """检查依赖是否安装"""
    required_packages = {
        'selenium': 'selenium',
        'requests': 'requests', 
        'streamlit': 'streamlit',
        'undetected-chromedriver': 'undetected_chromedriver',
        'python-dotenv': 'dotenv'
    }
    
    missing_packages = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    return missing_packages

def run_cli():
    """命令行模式"""
    print("🤖 启动Jarvis CLI模式...")
    
    # 检查依赖
    missing = check_dependencies()
    if missing:
        print(f"❌ 缺少依赖包: {', '.join(missing)}")
        print("💡 请运行: python run.py --install")
        return
    
    try:
        from jarvis_agent import demo_cli
        demo_cli()
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("💡 请确保所有依赖已正确安装")
    except Exception as e:
        print(f"❌ 程序运行失败: {e}")

def run_gui():
    """运行GUI模式"""
    print("🤖 启动Jarvis GUI模式...")
    
    # 检查依赖
    missing = check_dependencies()
    if missing:
        print(f"❌ 缺少依赖包: {', '.join(missing)}")
        print("💡 请运行: python run.py --install")
        return
    
    try:
        print("🌐 正在启动Web界面...")
        print("💡 浏览器将自动打开，如未打开请访问: http://localhost:8501")
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "gui_middleware.py",
            "--server.headless", "true",
            "--server.fileWatcherType", "none",
            "--browser.gatherUsageStats", "false"
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ GUI启动失败: {e}")
        print("💡 请检查streamlit是否正确安装")
    except FileNotFoundError:
        print("❌ 找不到Python或Streamlit")
        print("💡 请确保 Python和Streamlit已正确安装")
    except KeyboardInterrupt:
        print("\n🛑 用户中断程序")

def install_dependencies():
    """安装依赖"""
    print("📦 正在安装项目依赖...")
    
    if not os.path.exists("requirements.txt"):
        print("❌ 找不到requirements.txt文件")
        return
    
    try:
        # 升级pip
        print("⬆️ 升级pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # 安装依赖
        print("📥 安装依赖包...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        
        print("✅ 依赖安装完成")
        
        # 验证安装
        print("🔍 验证安装...")
        missing = check_dependencies()
        if missing:
            print(f"⚠️ 以下包可能未正确安装: {', '.join(missing)}")
        else:
            print("✅ 所有依赖包安装成功")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        print("💡 请检查网络连接和Python环境")

def main():
    parser = argparse.ArgumentParser(description="Jarvis AI Agent 启动器")
    parser.add_argument("--mode", choices=["cli", "gui"], default="gui", 
                       help="启动模式 (默认: gui)")
    parser.add_argument("--install", action="store_true", 
                       help="安装依赖")
    parser.add_argument("--check", action="store_true", 
                       help="检查环境配置")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🤖 Jarvis AI Agent 启动器")
    print("智能助手 - 支持浏览器操作、API调用、Python执行")
    print("=" * 60)
    
    if args.install:
        install_dependencies()
        return
    
    if args.check:
        missing = check_dependencies()
        if missing:
            print(f"❌ 缺少依赖: {', '.join(missing)}")
        else:
            print("✅ 所有依赖已安装")
        return
    
    # 启动前检查
    print("🔍 启动前检查...")
    missing = check_dependencies()
    if missing:
        print(f"❌ 缺少依赖包: {', '.join(missing)}")
        print("💡 请运行: python run.py --install")
        return
    
    print(f"🚀 启动模式: {args.mode.upper()}")
    
    if args.mode == "cli":
        run_cli()
    else:
        run_gui()

if __name__ == "__main__":
    main()