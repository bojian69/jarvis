#!/usr/bin/env python3
"""
学生住房快速启动脚本
直接打开学生住房网站并选择London城市
"""

import os
import sys
import time
from main import JarvisAgent

def main():
    """主程序 - 直接执行学生住房功能"""
    print("🏠 学生住房网站快速启动")
    print("=" * 50)
    print("正在启动浏览器并打开学生住房网站...")
    
    # 创建Jarvis实例
    jarvis = JarvisAgent()
    
    if not jarvis.driver:
        print("❌ 浏览器启动失败")
        print("💡 请检查Chrome浏览器是否正确安装")
        return
    
    try:
        # 直接调用学生住房功能
        print("\n🚀 正在打开学生住房网站...")
        success = jarvis.open_student_housing_london()
        
        if success:
            print("\n✅ 学生住房网站已打开！")
            
            # 显示页面信息
            url = jarvis.get_current_url()
            title = jarvis.get_page_title()
            print(f"📊 当前页面:")
            print(f"   URL: {url}")
            print(f"   标题: {title}")
            
            # 自动截图
            screenshot_name = f"housing_{int(time.time())}.png"
            jarvis.take_screenshot(screenshot_name)
            print(f"   截图: {screenshot_name}")
            
            print("\n💡 浏览器将保持打开状态，您可以继续操作")
            print("💡 按 Ctrl+C 退出程序并关闭浏览器")
            
            # 保持程序运行
            try:
                while True:
                    user_input = input("\n输入命令 (screenshot/info/quit): ").strip().lower()
                    
                    if user_input == 'quit':
                        break
                    elif user_input == 'screenshot':
                        filename = f"housing_screenshot_{int(time.time())}.png"
                        jarvis.take_screenshot(filename)
                    elif user_input == 'info':
                        current_url = jarvis.get_current_url()
                        current_title = jarvis.get_page_title()
                        print(f"URL: {current_url}")
                        print(f"标题: {current_title}")
                    elif user_input == 'help':
                        print("""
可用命令:
- screenshot: 截图
- info: 显示当前页面信息
- quit: 退出程序
                        """)
                    else:
                        print("未知命令，输入 'help' 查看帮助")
            
            except KeyboardInterrupt:
                print("\n🛑 用户中断程序")
        
        else:
            print("❌ 打开学生住房网站失败")
    
    except Exception as e:
        print(f"❌ 程序执行出错: {e}")
    
    finally:
        # 关闭浏览器
        print("\n🔄 正在关闭浏览器...")
        jarvis.close()
        print("👋 程序已退出")

if __name__ == "__main__":
    main()
