#!/usr/bin/env python3
"""
Jarvis AI Agent 统一运行脚本
支持选择不同版本运行
"""

import sys
import subprocess
import argparse
from pathlib import Path

def run_v1(args):
    """运行v1.0版本"""
    print("🚀 启动 Jarvis AI Agent v1.0...")
    v1_dir = Path("v1")
    if not v1_dir.exists():
        print("❌ v1目录不存在")
        return False
    
    # 构建v1运行命令
    cmd = [sys.executable, "v1/run.py"]
    if args.install:
        cmd.append("--install")
    if args.check:
        cmd.append("--check")
    if args.gui:
        cmd.append("--gui")
    if args.status:
        cmd.append("--status")
    
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ v1.0启动失败: {e}")
        return False

def run_v2(args):
    """运行v2.0版本"""
    print("🚀 启动 Jarvis AI Agent v2.0...")
    v2_dir = Path("v2")
    if not v2_dir.exists():
        print("❌ v2目录不存在")
        return False
    
    # 切换到v2目录并运行
    import os
    original_dir = os.getcwd()
    
    try:
        os.chdir("v2")
        
        # 构建v2运行命令
        cmd = [sys.executable, "run.py"]
        if args.install:
            cmd.append("--install")
        if args.check:
            cmd.append("--check")
        if args.gui:
            cmd.append("--gui")
        if args.cli:
            cmd.append("--cli")
        if args.agent:
            cmd.append("--agent")
        if args.headless:
            cmd.append("--headless")
        if args.status:
            cmd.append("--status")
        
        subprocess.run(cmd, check=True)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ v2.0启动失败: {e}")
        return False
    finally:
        os.chdir(original_dir)

def show_project_status():
    """显示项目状态"""
    print("📊 Jarvis AI Agent 项目状态")
    print("=" * 60)
    
    # 检查版本目录
    v1_exists = Path("v1").exists()
    v2_exists = Path("v2").exists()
    
    print("📁 版本目录:")
    print(f"  v1.0 (原始版本): {'✅ 存在' if v1_exists else '❌ 不存在'}")
    print(f"  v2.0 (优化版本): {'✅ 存在' if v2_exists else '❌ 不存在'}")
    
    # 检查配置文件
    env_exists = Path(".env").exists()
    print(f"\n⚙️  配置文件:")
    print(f"  .env: {'✅ 存在' if env_exists else '❌ 不存在'}")
    
    # 推荐使用版本
    print(f"\n💡 推荐:")
    if v2_exists:
        print("  使用 v2.0 版本获得最佳体验")
        print("  python run.py --v2 --gui")
    elif v1_exists:
        print("  使用 v1.0 版本")
        print("  python run.py --v1 --gui")
    else:
        print("  请检查项目文件完整性")
    
    print("=" * 60)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Jarvis AI Agent 统一运行脚本")
    
    # 版本选择
    version_group = parser.add_mutually_exclusive_group()
    version_group.add_argument("--v1", action="store_true", help="使用v1.0版本")
    version_group.add_argument("--v2", action="store_true", help="使用v2.0版本 (推荐)")
    
    # 通用操作
    parser.add_argument("--install", action="store_true", help="安装依赖包")
    parser.add_argument("--check", action="store_true", help="检查环境")
    parser.add_argument("--status", action="store_true", help="显示状态")
    
    # 启动选项
    parser.add_argument("--gui", action="store_true", help="启动GUI界面")
    parser.add_argument("--cli", action="store_true", help="启动CLI界面 (仅v2.0)")
    parser.add_argument("--agent", action="store_true", help="启动代理模式 (仅v2.0)")
    parser.add_argument("--headless", action="store_true", help="无头模式 (仅v2.0)")
    
    args = parser.parse_args()
    
    # 如果没有参数，显示帮助和状态
    if not any(vars(args).values()):
        parser.print_help()
        print("\n" + "=" * 60)
        show_project_status()
        print("\n💡 快速开始:")
        print("  # 推荐使用v2.0版本")
        print("  python run.py --v2 --install    # 安装v2.0依赖")
        print("  python run.py --v2 --gui        # 启动v2.0 Web界面")
        print("  python run.py --v2 --cli        # 启动v2.0 命令行界面")
        print("")
        print("  # 使用v1.0版本")
        print("  python run.py --v1 --install    # 安装v1.0依赖")
        print("  python run.py --v1 --gui        # 启动v1.0 Web界面")
        return
    
    # 显示项目状态
    if args.status and not (args.v1 or args.v2):
        show_project_status()
        return
    
    # 选择版本运行
    if args.v1:
        success = run_v1(args)
    elif args.v2:
        success = run_v2(args)
    else:
        # 默认使用v2.0
        print("💡 未指定版本，默认使用v2.0版本")
        success = run_v2(args)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
