#!/usr/bin/env python3
"""
Jarvis AI Agent 统一演示脚本
支持选择不同版本进行演示
"""

import sys
import subprocess
import argparse
from pathlib import Path

def demo_v1():
    """演示v1.0版本"""
    print("🎬 Jarvis AI Agent v1.0 演示")
    print("=" * 50)
    
    v1_dir = Path("v1")
    if not v1_dir.exists():
        print("❌ v1目录不存在")
        return False
    
    print("v1.0版本特性:")
    print("- 🌐 基础浏览器自动化")
    print("- 🔌 API调用功能")
    print("- 🖥️ Streamlit Web界面")
    print("- 📝 基础日志记录")
    
    print("\n启动v1.0 Web界面进行演示...")
    try:
        subprocess.run([sys.executable, "v1/run.py", "--gui"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ v1.0演示启动失败: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 v1.0演示结束")
        return True

def demo_v2():
    """演示v2.0版本"""
    print("🎬 Jarvis AI Agent v2.0 演示")
    print("=" * 50)
    
    v2_dir = Path("v2")
    if not v2_dir.exists():
        print("❌ v2目录不存在")
        return False
    
    print("v2.0版本特性:")
    print("- 🏗️ 模块化架构")
    print("- 🛡️ 中间件系统")
    print("- 📋 增强日志系统")
    print("- 📸 自动截图记录")
    print("- ⚙️ 配置管理系统")
    print("- 🖥️ Web + CLI 双界面")
    
    print("\n选择演示方式:")
    print("1. 功能演示脚本 (推荐)")
    print("2. Web界面演示")
    print("3. 命令行界面演示")
    
    try:
        choice = input("请选择 (1-3): ").strip()
        
        if choice == "1":
            print("\n🚀 运行功能演示脚本...")
            subprocess.run([sys.executable, "v2/demo.py"], check=True)
        elif choice == "2":
            print("\n🚀 启动Web界面...")
            subprocess.run([sys.executable, "v2/run.py", "--gui"], check=True)
        elif choice == "3":
            print("\n🚀 启动命令行界面...")
            subprocess.run([sys.executable, "v2/run.py", "--cli"], check=True)
        else:
            print("❌ 无效选择")
            return False
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ v2.0演示启动失败: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 v2.0演示结束")
        return True

def compare_versions():
    """版本对比演示"""
    print("📊 Jarvis AI Agent 版本对比")
    print("=" * 60)
    
    comparison = [
        ("特性", "v1.0", "v2.0"),
        ("代码结构", "单文件集中", "模块化分离 ✅"),
        ("日志系统", "基础日志", "多级别日志 ✅"),
        ("截图管理", "手动保存", "自动截图 ✅"),
        ("中间件支持", "❌", "完整支持 ✅"),
        ("配置管理", "环境变量", "配置文件+环境变量 ✅"),
        ("用户界面", "Web界面", "Web+CLI界面 ✅"),
        ("错误处理", "基础处理", "增强处理+重试 ✅"),
        ("扩展性", "有限", "高度可扩展 ✅"),
    ]
    
    # 打印表格
    for i, (feature, v1, v2) in enumerate(comparison):
        if i == 0:
            print(f"| {feature:<12} | {v1:<15} | {v2:<20} |")
            print("|" + "-" * 14 + "|" + "-" * 17 + "|" + "-" * 22 + "|")
        else:
            print(f"| {feature:<12} | {v1:<15} | {v2:<20} |")
    
    print("\n💡 推荐:")
    print("- 新用户和生产环境: 使用 v2.0 ⭐")
    print("- 快速上手和学习: 可以从 v1.0 开始")
    print("- 功能扩展和定制: 选择 v2.0")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Jarvis AI Agent 演示脚本")
    parser.add_argument("--v1", action="store_true", help="演示v1.0版本")
    parser.add_argument("--v2", action="store_true", help="演示v2.0版本")
    parser.add_argument("--compare", action="store_true", help="版本对比")
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        print("🎬 Jarvis AI Agent 演示")
        print("=" * 40)
        print("选择演示内容:")
        print("1. v1.0 版本演示")
        print("2. v2.0 版本演示 (推荐)")
        print("3. 版本对比")
        print("4. 退出")
        
        try:
            choice = input("\n请选择 (1-4): ").strip()
            
            if choice == "1":
                demo_v1()
            elif choice == "2":
                demo_v2()
            elif choice == "3":
                compare_versions()
            elif choice == "4":
                print("👋 再见！")
            else:
                print("❌ 无效选择")
        except KeyboardInterrupt:
            print("\n👋 演示结束")
    else:
        if args.v1:
            demo_v1()
        elif args.v2:
            demo_v2()
        elif args.compare:
            compare_versions()

if __name__ == "__main__":
    main()
