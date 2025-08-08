#!/usr/bin/env python3
"""
命令行界面
支持交互式命令行操作
"""

import cmd
import json
import sys
from typing import Dict, Any
from pathlib import Path

# 添加项目根目录到Python路径
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
sys.path.insert(0, str(project_root / "src"))

from core.agent import JarvisAgent

class CommandLineInterface(cmd.Cmd):
    """命令行界面类"""
    
    intro = """
🤖 欢迎使用 Jarvis AI Agent v2.0 命令行界面
输入 'help' 查看可用命令，输入 'quit' 退出程序
========================================
"""
    prompt = "jarvis> "
    
    def __init__(self):
        super().__init__()
        self.agent = None
        self.setup_agent()
    
    def setup_agent(self):
        """初始化Agent"""
        try:
            print("🚀 正在启动 Jarvis Agent...")
            self.agent = JarvisAgent()
            print("✅ Jarvis Agent 启动成功！")
        except Exception as e:
            print(f"❌ Agent 启动失败: {e}")
            sys.exit(1)
    
    def do_browser(self, args):
        """浏览器操作命令
        用法: browser <子命令> [参数]
        子命令:
          navigate <url>           - 导航到指定URL
          click <selector>         - 点击元素
          input <selector> <text>  - 输入文本
          screenshot [description] - 截图
          search <query>          - Google搜索
          profiles                - 列出浏览器配置文件
          extensions [browser] [profile] - 显示扩展信息
          setup [--local] [--headless] - 重新设置浏览器
        """
        if not args:
            print("❌ 请指定浏览器子命令")
            return
        
        parts = args.split()
        subcmd = parts[0]
        
        try:
            if subcmd == "navigate" and len(parts) >= 2:
                url = parts[1]
                result = self.agent.execute_command("browser_navigate", url=url)
                self._print_result(result)
            
            elif subcmd == "click" and len(parts) >= 2:
                selector = parts[1]
                result = self.agent.execute_command("browser_click", selector=selector)
                self._print_result(result)
            
            elif subcmd == "input" and len(parts) >= 3:
                selector = parts[1]
                text = " ".join(parts[2:])
                result = self.agent.execute_command("browser_input", selector=selector, text=text)
                self._print_result(result)
            
            elif subcmd == "screenshot":
                description = " ".join(parts[1:]) if len(parts) > 1 else "CLI截图"
                result = self.agent.execute_command("browser_screenshot", description=description)
                self._print_result(result)
            
            elif subcmd == "search" and len(parts) >= 2:
                query = " ".join(parts[1:])
                result = self.agent.execute_command("browser_search_google", query=query)
                self._print_result(result)
            
            elif subcmd == "profiles":
                result = self.agent.execute_command("browser_list_profiles")
                if result.get("success"):
                    print("🌐 可用的浏览器配置文件:")
                    browsers = result.get("browsers", {})
                    for browser_name, profiles in browsers.items():
                        print(f"\n📁 {browser_name}:")
                        for profile_name, info in profiles.items():
                            print(f"  - {profile_name}: {info['extensions_count']} 个扩展, "
                                f"{info['size_mb']} MB")
                    
                    recommended = result.get("recommended")
                    if recommended:
                        print(f"\n🎯 推荐配置: {recommended['browser']} - {recommended['profile']}")
                else:
                    print(f"❌ 获取配置文件失败: {result.get('error')}")
            
            elif subcmd == "extensions":
                browser_type = parts[1] if len(parts) >= 2 else "Chrome"
                profile_name = parts[2] if len(parts) >= 3 else "Default"
                result = self.agent.execute_command("browser_get_extensions", 
                                                  browser_type=browser_type, 
                                                  profile_name=profile_name)
                if result.get("success"):
                    extensions = result.get("extensions", [])
                    print(f"🧩 {browser_type} - {profile_name} 的扩展 ({len(extensions)} 个):")
                    for ext in extensions:
                        print(f"  - {ext['name']} (v{ext['version']})")
                        if ext['description']:
                            desc = ext['description'][:80] + "..." if len(ext['description']) > 80 else ext['description']
                            print(f"    {desc}")
                else:
                    print(f"❌ 获取扩展失败: {result.get('error')}")
            
            elif subcmd == "setup":
                use_local = "--local" in parts
                headless = "--headless" in parts
                print(f"🔄 重新设置浏览器 (本地配置: {use_local}, 无头模式: {headless})")
                
                # 关闭现有浏览器
                if self.agent.driver:
                    self.agent.driver.quit()
                    self.agent.driver = None
                
                # 重新启动
                success = self.agent.setup_browser(headless=headless, use_local_profile=use_local)
                if success:
                    print("✅ 浏览器重新设置成功")
                else:
                    print("❌ 浏览器设置失败")
            
            else:
                print("❌ 无效的浏览器子命令或参数不足")
                
        except Exception as e:
            print(f"❌ 命令执行失败: {e}")
    
    def do_api(self, args):
        """API调用命令
        用法: api <子命令> [参数]
        子命令:
          chat <message>           - OpenAI聊天
          google <query>           - Google搜索
          github <query>           - GitHub搜索
          weather [city]           - 天气查询
          test                     - 连接测试
        """
        if not args:
            print("❌ 请指定API子命令")
            return
        
        parts = args.split()
        subcmd = parts[0]
        
        try:
            if subcmd == "chat" and len(parts) >= 2:
                message = " ".join(parts[1:])
                result = self.agent.execute_command("api_openai_chat", message=message)
                self._print_result(result)
            
            elif subcmd == "google" and len(parts) >= 2:
                query = " ".join(parts[1:])
                result = self.agent.execute_command("api_google_search", query=query)
                self._print_result(result)
            
            elif subcmd == "github" and len(parts) >= 2:
                query = " ".join(parts[1:])
                result = self.agent.execute_command("api_github_search", query=query)
                self._print_result(result)
            
            elif subcmd == "weather":
                city = parts[1] if len(parts) >= 2 else "Beijing"
                result = self.agent.execute_command("api_weather", city=city)
                self._print_result(result)
            
            elif subcmd == "test":
                result = self.agent.execute_command("api_test_connection")
                self._print_result(result)
            
            else:
                print("❌ 无效的API子命令")
                
        except Exception as e:
            print(f"❌ 命令执行失败: {e}")
    
    def do_code(self, args):
        """代码执行命令
        用法: code <子命令> [参数]
        子命令:
          python <code>            - 执行Python代码
          shell <command>          - 执行Shell命令
          read <filepath>          - 读取文件
          write <filepath> <content> - 写入文件
          list [directory]         - 列出目录
          install <package>        - 安装Python包
        """
        if not args:
            print("❌ 请指定代码子命令")
            return
        
        parts = args.split()
        subcmd = parts[0]
        
        try:
            if subcmd == "python" and len(parts) >= 2:
                code = " ".join(parts[1:])
                result = self.agent.execute_command("code_execute_python", code=code)
                self._print_result(result)
            
            elif subcmd == "shell" and len(parts) >= 2:
                command = " ".join(parts[1:])
                result = self.agent.execute_command("code_execute_shell", command=command)
                self._print_result(result)
            
            elif subcmd == "read" and len(parts) >= 2:
                filepath = parts[1]
                result = self.agent.execute_command("code_read_file", filepath=filepath)
                self._print_result(result)
            
            elif subcmd == "write" and len(parts) >= 3:
                filepath = parts[1]
                content = " ".join(parts[2:])
                result = self.agent.execute_command("code_write_file", filepath=filepath, content=content)
                self._print_result(result)
            
            elif subcmd == "list":
                directory = parts[1] if len(parts) >= 2 else "."
                result = self.agent.execute_command("code_list_directory", dirpath=directory)
                self._print_result(result)
            
            elif subcmd == "install" and len(parts) >= 2:
                package = parts[1]
                result = self.agent.execute_command("code_install_package", package=package)
                self._print_result(result)
            
            else:
                print("❌ 无效的代码子命令")
                
        except Exception as e:
            print(f"❌ 命令执行失败: {e}")
    
    def do_status(self, args):
        """显示系统状态"""
        if not self.agent:
            print("❌ Agent 未初始化")
            return
        
        print("📊 Jarvis Agent 状态:")
        print("=" * 40)
        
        # API状态
        print("🔌 API服务状态:")
        for service, status in self.agent.config.api_status.items():
            status_text = "✅ 已配置" if status else "❌ 未配置"
            print(f"  {service.upper()}: {status_text}")
        
        # 浏览器状态
        browser_status = "✅ 已启动" if self.agent.driver else "❌ 未启动"
        print(f"🌐 浏览器状态: {browser_status}")
        
        # 配置信息
        print(f"📁 项目根目录: {self.agent.config.project_root}")
        print(f"📋 日志目录: {self.agent.config.logs_dir}")
        
        print("=" * 40)
    
    def do_logs(self, args):
        """查看日志
        用法: logs [level] [lines]
        level: debug, info, error (默认: info)
        lines: 显示行数 (默认: 10)
        """
        parts = args.split() if args else []
        level = parts[0] if len(parts) >= 1 else "info"
        lines = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 10
        
        if level not in ["debug", "info", "error"]:
            print("❌ 无效的日志级别，请使用: debug, info, error")
            return
        
        try:
            recent_logs = self.agent.logger.get_recent_logs(level, lines)
            if recent_logs:
                print(f"📋 最近 {len(recent_logs)} 条 {level} 日志:")
                print("=" * 50)
                for log in recent_logs:
                    print(log.strip())
                print("=" * 50)
            else:
                print(f"📋 暂无 {level} 级别的日志")
        except Exception as e:
            print(f"❌ 读取日志失败: {e}")
    
    def do_config(self, args):
        """显示或修改配置
        用法: config [key] [value]
        不带参数: 显示所有配置
        带key: 显示指定配置
        带key和value: 修改配置
        """
        if not args:
            # 显示所有配置
            print("⚙️ 当前配置:")
            print(json.dumps(self.agent.config.settings, indent=2, ensure_ascii=False))
            return
        
        parts = args.split()
        key = parts[0]
        
        if len(parts) == 1:
            # 显示指定配置
            value = self.agent.config.get(key)
            if value is not None:
                print(f"⚙️ {key}: {json.dumps(value, indent=2, ensure_ascii=False)}")
            else:
                print(f"❌ 配置项不存在: {key}")
        
        elif len(parts) >= 2:
            # 修改配置
            try:
                value = " ".join(parts[1:])
                # 尝试解析为JSON
                try:
                    parsed_value = json.loads(value)
                except json.JSONDecodeError:
                    parsed_value = value
                
                self.agent.config.set(key, parsed_value)
                print(f"✅ 配置已更新: {key} = {parsed_value}")
            except Exception as e:
                print(f"❌ 配置更新失败: {e}")
    
    def do_quit(self, args):
        """退出程序"""
        print("👋 正在关闭 Jarvis Agent...")
        if self.agent:
            self.agent.close()
        print("✅ 再见！")
        return True
    
    def do_exit(self, args):
        """退出程序（quit的别名）"""
        return self.do_quit(args)
    
    def _print_result(self, result: Dict[str, Any]):
        """打印执行结果"""
        if result.get("success"):
            print("✅ 执行成功")
            if "message" in result:
                print(f"💬 {result['message']}")
            
            # 显示其他重要信息
            for key, value in result.items():
                if key not in ["success", "message"] and value is not None:
                    if isinstance(value, (dict, list)):
                        print(f"📋 {key}:")
                        print(json.dumps(value, indent=2, ensure_ascii=False))
                    else:
                        print(f"📋 {key}: {value}")
        else:
            print(f"❌ 执行失败: {result.get('error', '未知错误')}")
    
    def emptyline(self):
        """空行时不执行任何操作"""
        pass
    
    def default(self, line):
        """处理未知命令"""
        print(f"❌ 未知命令: {line}")
        print("💡 输入 'help' 查看可用命令")

def main():
    """主函数"""
    try:
        cli = CommandLineInterface()
        cli.cmdloop()
    except KeyboardInterrupt:
        print("\n👋 程序被用户中断")
    except Exception as e:
        print(f"❌ 程序异常退出: {e}")

if __name__ == "__main__":
    main()
