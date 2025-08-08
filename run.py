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
        from main import main
        main()
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("💡 请确保所有依赖已正确安装")
    except Exception as e:
        print(f"❌ 程序运行失败: {e}")

def run_gui():
    """GUI模式"""
    print("🤖 启动Jarvis GUI模式...")
    
    # 检查依赖
    missing = check_dependencies()
    if missing:
        print(f"❌ 缺少依赖包: {', '.join(missing)}")
        print("💡 请运行: python run.py --install")
        return
    
    try:
        # 检查streamlit是否可用
        result = subprocess.run([sys.executable, "-c", "import streamlit"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Streamlit未正确安装")
            print("💡 请运行: pip install streamlit")
            return
        
        print("🌐 正在启动Web界面...")
        print("💡 浏览器将自动打开，如未打开请访问: http://localhost:8501")
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "gui.py",
            "--server.headless", "true",
            "--server.fileWatcherType", "none",
            "--browser.gatherUsageStats", "false"
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ GUI启动失败: {e}")
        print("💡 请检查streamlit是否正确安装")
    except FileNotFoundError:
        print("❌ 找不到Python或Streamlit")
        print("💡 请确保Python和Streamlit已正确安装")
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

def setup_chrome():
    """设置Chrome浏览器"""
    print("🔧 Chrome浏览器设置检查...")
    print("=" * 50)
    
    # 检查Chrome是否安装
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/local/bin/google-chrome"
    ]
    
    chrome_found = False
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ 找到Chrome: {path}")
            chrome_found = True
            break
    
    if not chrome_found:
        print("❌ 未找到Chrome浏览器")
        print("📥 请下载安装Google Chrome:")
        print("   https://www.google.com/chrome/")
        return
    
    # 检查用户数据目录
    user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome/Jarvis")
    if not os.path.exists(user_data_dir):
        print(f"📁 创建用户数据目录: {user_data_dir}")
        os.makedirs(user_data_dir, exist_ok=True)
    else:
        print(f"✅ 用户数据目录已存在: {user_data_dir}")
    
    print("=" * 50)
    print("💡 Chrome设置说明:")
    print("1. 项目使用独立的Chrome用户数据目录")
    print("2. 支持保持登录状态和用户偏好")
    print("3. 使用undetected-chromedriver避免检测")
    print("4. 遇到验证码时可以手动处理")
    print("=" * 50)

def check_env_file():
    """检查环境变量文件"""
    print("🔍 检查环境配置...")
    
    if not os.path.exists(".env"):
        print("⚠️ 未找到.env文件")
        if os.path.exists(".env.example"):
            print("📋 发现.env.example文件，正在复制...")
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ 已创建.env文件")
        else:
            print("💡 请手动创建.env文件并配置API密钥")
    else:
        print("✅ 找到.env文件")
    
    # 检查API密钥配置
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_keys = {
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
            'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY'),
            'GITHUB_TOKEN': os.getenv('GITHUB_TOKEN')
        }
        
        configured_keys = []
        for key, value in api_keys.items():
            if value and value != f'your_{key.lower()}_here':
                configured_keys.append(key)
        
        if configured_keys:
            print(f"✅ 已配置的API密钥: {', '.join(configured_keys)}")
        else:
            print("💡 未配置API密钥，仅浏览器功能可用")
            
    except ImportError:
        print("⚠️ 无法检查API密钥配置（python-dotenv未安装）")

def main():
    parser = argparse.ArgumentParser(description="Jarvis AI Agent 启动器")
    parser.add_argument("--mode", choices=["cli", "gui"], default="gui", 
                       help="启动模式 (默认: gui)")
    parser.add_argument("--install", action="store_true", 
                       help="安装依赖")
    parser.add_argument("--setup", action="store_true", 
                       help="设置Chrome浏览器")
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
    
    if args.setup:
        setup_chrome()
        return
    
    if args.check:
        check_env_file()
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
    
    check_env_file()
    
    print(f"🚀 启动模式: {args.mode.upper()}")
    
    if args.mode == "cli":
        run_cli()
    else:
        run_gui()

if __name__ == "__main__":
    main()
