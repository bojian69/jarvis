#!/usr/bin/env python3
"""
Jarvis AI Agent v1.0 运行脚本
原始版本的运行脚本
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def install_dependencies():
    """安装依赖包"""
    print("📦 正在安装v1.0依赖包...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    if requirements_file.exists():
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                         check=True)
            print("✅ v1.0依赖包安装完成！")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 依赖包安装失败: {e}")
            return False
    else:
        print("❌ requirements.txt文件不存在")
        return False

def check_environment():
    """检查环境配置"""
    print("🔍 检查v1.0环境配置...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python版本过低，需要Python 3.8+")
        return False
    
    print(f"✅ Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查.env文件
    env_file = Path("../.env")  # 在上级目录
    if not env_file.exists():
        print("⚠️ .env文件不存在，某些功能可能无法使用")
    else:
        print("✅ .env文件存在")
    
    return True

def run_gui():
    """运行GUI界面"""
    print("🚀 启动v1.0 Streamlit GUI界面...")
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "gui.py"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ GUI启动失败: {e}")
    except KeyboardInterrupt:
        print("\n👋 GUI已关闭")

def run_main():
    """运行主程序"""
    print("🚀 启动v1.0主程序...")
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 主程序启动失败: {e}")
    except KeyboardInterrupt:
        print("\n👋 主程序已关闭")

def show_status():
    """显示系统状态"""
    print("📊 Jarvis AI Agent v1.0 状态")
    print("=" * 50)
    
    # Python环境
    print(f"🐍 Python版本: {sys.version}")
    print(f"📁 工作目录: {os.getcwd()}")
    
    # 文件检查
    files_to_check = [
        "main.py",
        "gui.py",
        "api_tools.py",
        "browser_tools.py",
        "requirements.txt"
    ]
    
    print("\n📋 文件检查:")
    for file_path in files_to_check:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
    
    print("=" * 50)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Jarvis AI Agent v1.0 运行脚本")
    parser.add_argument("--install", action="store_true", help="安装依赖包")
    parser.add_argument("--check", action="store_true", help="检查环境")
    parser.add_argument("--gui", action="store_true", help="启动GUI界面")
    parser.add_argument("--main", action="store_true", help="启动主程序")
    parser.add_argument("--status", action="store_true", help="显示状态")
    
    args = parser.parse_args()
    
    # 如果没有参数，显示帮助
    if not any(vars(args).values()):
        parser.print_help()
        print("\n💡 快速开始:")
        print("  python run.py --install    # 安装依赖")
        print("  python run.py --check      # 检查环境")
        print("  python run.py --gui        # 启动GUI界面")
        print("  python run.py --main       # 启动主程序")
        print("\n⚠️  注意: 这是v1.0版本，推荐使用v2.0版本获得更好体验")
        print("  cd ../v2 && python run.py --gui")
        return
    
    if args.install:
        if not install_dependencies():
            sys.exit(1)
    
    if args.check:
        if not check_environment():
            sys.exit(1)
    
    if args.status:
        show_status()
    
    if args.gui:
        run_gui()
    elif args.main:
        run_main()

if __name__ == "__main__":
    main()
