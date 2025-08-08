#!/usr/bin/env python3
"""
Jarvis控制台 - 包含学生住房功能
"""

import os
import sys
import time
from main import JarvisAgent

class JarvisConsole:
    def __init__(self):
        self.jarvis = None
        self.running = True
    
    def start_browser(self):
        """启动浏览器"""
        if self.jarvis is None:
            print("🚀 正在启动浏览器...")
            self.jarvis = JarvisAgent()
            if self.jarvis.driver:
                print("✅ 浏览器启动成功！")
                return True
            else:
                print("❌ 浏览器启动失败")
                return False
        else:
            print("⚠️ 浏览器已经在运行中")
            return True
    
    def close_browser(self):
        """关闭浏览器"""
        if self.jarvis:
            self.jarvis.close()
            self.jarvis = None
            print("✅ 浏览器已关闭")
        else:
            print("⚠️ 浏览器未启动")
    
    def open_student_housing(self):
        """打开学生住房网站并选择London"""
        if not self.jarvis or not self.jarvis.driver:
            print("❌ 请先启动浏览器")
            return False
        
        print("🏠 正在打开学生住房网站并选择London城市...")
        success = self.jarvis.open_student_housing_london()
        
        if success:
            print("✅ 学生住房网站已打开")
            # 显示当前页面信息
            url = self.jarvis.get_current_url()
            title = self.jarvis.get_page_title()
            print(f"   当前URL: {url}")
            print(f"   页面标题: {title}")
        
        return success
    
    def open_url(self, url):
        """打开指定URL"""
        if not self.jarvis or not self.jarvis.driver:
            print("❌ 请先启动浏览器")
            return False
        
        return self.jarvis.open_url(url)
    
    def search_google(self, query):
        """Google搜索"""
        if not self.jarvis or not self.jarvis.driver:
            print("❌ 请先启动浏览器")
            return False
        
        return self.jarvis.search_google(query)
    
    def take_screenshot(self):
        """截图"""
        if not self.jarvis or not self.jarvis.driver:
            print("❌ 请先启动浏览器")
            return False
        
        filename = f"screenshot_{int(time.time())}.png"
        success = self.jarvis.take_screenshot(filename)
        if success:
            print(f"✅ 截图已保存: {filename}")
        return success
    
    def show_info(self):
        """显示当前页面信息"""
        if not self.jarvis or not self.jarvis.driver:
            print("❌ 请先启动浏览器")
            return
        
        url = self.jarvis.get_current_url()
        title = self.jarvis.get_page_title()
        print(f"当前URL: {url}")
        print(f"页面标题: {title}")
    
    def show_help(self):
        """显示帮助信息"""
        print("""
🤖 Jarvis控制台命令帮助:

基础命令:
  start     - 启动浏览器
  close     - 关闭浏览器
  quit/exit - 退出程序
  help      - 显示此帮助信息

网页操作:
  url <网址>        - 打开指定网址
  search <关键词>   - Google搜索
  screenshot       - 截图
  info            - 显示当前页面信息

专用功能:
  housing         - 打开学生住房网站并选择London城市

示例:
  > start
  > housing
  > screenshot
  > url https://www.google.com
  > search Python教程
        """)
    
    def run(self):
        """运行控制台"""
        print("🤖 Jarvis控制台")
        print("=" * 50)
        print("输入 'help' 查看命令帮助")
        print("输入 'start' 启动浏览器")
        print("=" * 50)
        
        while self.running:
            try:
                user_input = input("\nJarvis> ").strip()
                
                if not user_input:
                    continue
                
                # 解析命令
                parts = user_input.split(' ', 1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                # 执行命令
                if command in ['quit', 'exit']:
                    self.running = False
                    print("👋 再见！")
                
                elif command == 'help':
                    self.show_help()
                
                elif command == 'start':
                    self.start_browser()
                
                elif command == 'close':
                    self.close_browser()
                
                elif command == 'housing':
                    self.open_student_housing()
                
                elif command == 'url':
                    if args:
                        self.open_url(args)
                    else:
                        print("❌ 请提供URL，例如: url https://www.google.com")
                
                elif command == 'search':
                    if args:
                        self.search_google(args)
                    else:
                        print("❌ 请提供搜索关键词，例如: search Python教程")
                
                elif command == 'screenshot':
                    self.take_screenshot()
                
                elif command == 'info':
                    self.show_info()
                
                else:
                    print(f"❌ 未知命令: {command}")
                    print("💡 输入 'help' 查看可用命令")
            
            except KeyboardInterrupt:
                print("\n👋 用户中断，正在退出...")
                self.running = False
            
            except Exception as e:
                print(f"❌ 执行命令时出错: {e}")
        
        # 清理资源
        if self.jarvis:
            self.close_browser()

def main():
    """主程序"""
    console = JarvisConsole()
    console.run()

if __name__ == "__main__":
    main()
