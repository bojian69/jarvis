#!/usr/bin/env python3
"""
Jarvis AI Agent v2.0 - 主入口文件
优化版本，支持模块化架构和中间件
"""

import sys
import argparse
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.agent import JarvisAgent
from src.ui.gui import main as gui_main
from src.ui.cli import main as cli_main

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Jarvis AI Agent v2.0")
    parser.add_argument("--mode", choices=["gui", "cli", "agent"], default="gui",
                       help="运行模式: gui(Web界面), cli(命令行), agent(纯代理)")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--headless", action="store_true", help="无头模式运行浏览器")
    
    args = parser.parse_args()
    
    if args.mode == "gui":
        print("🚀 启动 Streamlit GUI 界面...")
        gui_main()
    
    elif args.mode == "cli":
        print("🚀 启动命令行界面...")
        cli_main()
    
    elif args.mode == "agent":
        print("🚀 启动纯代理模式...")
        try:
            with JarvisAgent(args.config) as agent:
                if args.headless:
                    agent.setup_browser(headless=True)
                else:
                    agent.setup_browser()
                
                print("✅ Agent 启动成功，按 Ctrl+C 退出")
                
                # 保持运行
                try:
                    while True:
                        command = input("jarvis> ").strip()
                        if command.lower() in ["quit", "exit"]:
                            break
                        
                        if command:
                            # 简单的命令解析
                            parts = command.split()
                            if len(parts) >= 2:
                                cmd_type = parts[0]
                                cmd_action = parts[1]
                                cmd_name = f"{cmd_type}_{cmd_action}"
                                
                                # 提取参数
                                kwargs = {}
                                if len(parts) > 2:
                                    if cmd_name == "browser_navigate":
                                        kwargs["url"] = parts[2]
                                    elif cmd_name == "browser_click":
                                        kwargs["selector"] = parts[2]
                                    elif cmd_name == "browser_input":
                                        kwargs["selector"] = parts[2]
                                        kwargs["text"] = " ".join(parts[3:])
                                    elif cmd_name == "api_openai_chat":
                                        kwargs["message"] = " ".join(parts[2:])
                                
                                result = agent.execute_command(cmd_name, **kwargs)
                                print(f"结果: {result}")
                            else:
                                print("❌ 命令格式错误，请使用: <模块> <操作> [参数]")
                
                except KeyboardInterrupt:
                    print("\n👋 程序被用户中断")
                
        except Exception as e:
            print(f"❌ Agent 启动失败: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
