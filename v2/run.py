#!/usr/bin/env python3
"""
Jarvis AI Agent v2.0 运行脚本
提供便捷的启动和管理功能
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def install_dependencies():
    """安装依赖包"""
    print("📦 正在安装依赖包...")
    
    requirements = [
        "selenium==4.15.0",
        "requests==2.31.0",
        "beautifulsoup4==4.12.2",
        "streamlit==1.28.0",
        "openai==1.3.0",
        "python-dotenv==1.0.0",
        "pandas==2.1.0",
        "undetected-chromedriver==3.5.4"
    ]
    
    for package in requirements:
        try:
            print(f"安装 {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} 安装失败: {e}")
            return False
    
    print("✅ 所有依赖包安装完成！")
    return True

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python版本过低，需要Python 3.8+")
        return False
    
    print(f"✅ Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查.env文件（在上级目录）
    env_file = Path("../.env")
    if not env_file.exists():
        print("⚠️ .env文件不存在，将创建示例文件")
        create_env_example()
    else:
        print("✅ .env文件存在")
    
    # 检查必要目录
    directories = ["logs", "logs/screenshots", "logs/debug", "logs/error", "logs/info", "config"]
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 创建目录: {directory}")
        else:
            print(f"✅ 目录存在: {directory}")
    
    return True

def create_env_example():
    """创建.env示例文件"""
    env_content = """# Jarvis AI Agent 配置文件
# 复制此文件为 .env 并填入真实的API密钥

# OpenAI API配置
OPENAI_API_KEY=your_openai_api_key_here

# Google API配置
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here

# GitHub API配置
GITHUB_TOKEN=your_github_token_here

# Anthropic API配置
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# 天气API配置（可选）
OPENWEATHER_API_KEY=your_openweather_api_key_here
"""
    
    with open("../.env", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("✅ .env示例文件已创建")

def run_gui():
    """运行GUI界面"""
    print("🚀 启动Streamlit GUI界面...")
    try:
        # 使用简化的启动脚本
        subprocess.run([sys.executable, "start_gui.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ GUI启动失败: {e}")
        print("\n💡 请尝试手动启动:")
        print("   python start_gui.py")
        print("   或者: python -m streamlit run src/ui/gui.py")
    except KeyboardInterrupt:
        print("\n👋 GUI已关闭")

def run_cli():
    """运行CLI界面"""
    print("🚀 启动命令行界面...")
    try:
        subprocess.run([sys.executable, "src/ui/cli.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ CLI启动失败: {e}")
    except KeyboardInterrupt:
        print("\n👋 CLI已关闭")

def run_agent(headless=False):
    """运行纯代理模式"""
    print("🚀 启动代理模式...")
    cmd = [sys.executable, "main.py", "--mode", "agent"]
    if headless:
        cmd.append("--headless")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 代理启动失败: {e}")
    except KeyboardInterrupt:
        print("\n👋 代理已关闭")

def show_status():
    """显示系统状态"""
    print("📊 Jarvis AI Agent v2.0 状态")
    print("=" * 50)
    
    # Python环境
    print(f"🐍 Python版本: {sys.version}")
    print(f"📁 工作目录: {os.getcwd()}")
    
    # 文件检查
    files_to_check = [
        "main.py",
        "src/core/agent.py",
        "src/modules/browser.py",
        "src/modules/api.py",
        "src/modules/code.py",
        "../.env"
    ]
    
    print("\n📋 文件检查:")
    for file_path in files_to_check:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
    
    # 目录检查
    directories = ["logs", "config", "src"]
    print("\n📁 目录检查:")
    for directory in directories:
        if Path(directory).exists():
            print(f"✅ {directory}")
        else:
            print(f"❌ {directory}")
    
    print("=" * 50)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Jarvis AI Agent v2.0 运行脚本")
    parser.add_argument("--install", action="store_true", help="安装依赖包")
    parser.add_argument("--check", action="store_true", help="检查环境")
    parser.add_argument("--gui", action="store_true", help="启动GUI界面")
    parser.add_argument("--cli", action="store_true", help="启动CLI界面")
    parser.add_argument("--agent", action="store_true", help="启动代理模式")
    parser.add_argument("--headless", action="store_true", help="无头模式")
    parser.add_argument("--status", action="store_true", help="显示状态")
    
    args = parser.parse_args()
    
    # 如果没有参数，显示帮助
    if not any(vars(args).values()):
        parser.print_help()
        print("\n💡 快速开始:")
        print("  python run_v2.py --install    # 安装依赖")
        print("  python run_v2.py --check      # 检查环境")
        print("  python run_v2.py --gui        # 启动GUI界面")
        print("  python run_v2.py --cli        # 启动CLI界面")
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
    elif args.cli:
        run_cli()
    elif args.agent:
        run_agent(args.headless)

if __name__ == "__main__":
    main()
