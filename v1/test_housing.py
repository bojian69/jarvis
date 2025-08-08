#!/usr/bin/env python3
"""
测试学生住房网站功能
"""

import os
import sys
import time
from main import JarvisAgent

def test_student_housing():
    """测试学生住房网站功能"""
    print("🏠 测试学生住房网站功能")
    print("=" * 50)
    
    # 创建Jarvis实例
    jarvis = JarvisAgent()
    
    if not jarvis.driver:
        print("❌ 浏览器启动失败，无法测试")
        return False
    
    try:
        print("🚀 开始测试学生住房网站功能...")
        
        # 调用学生住房功能
        success = jarvis.open_student_housing_london()
        
        if success:
            print("✅ 学生住房网站功能测试成功！")
            print("💡 请检查浏览器中是否已正确打开网站并选择了London")
            
            # 显示当前页面信息
            current_url = jarvis.get_current_url()
            current_title = jarvis.get_page_title()
            
            print(f"\n📊 当前页面信息:")
            print(f"   URL: {current_url}")
            print(f"   标题: {current_title}")
            
            # 截图保存
            screenshot_name = f"housing_test_{int(time.time())}.png"
            jarvis.take_screenshot(screenshot_name)
            print(f"   截图: {screenshot_name}")
            
            # 等待用户确认
            input("\n按回车键继续...")
            
        else:
            print("❌ 学生住房网站功能测试失败")
        
        return success
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False
    
    finally:
        # 关闭浏览器
        jarvis.close()

def main():
    """主测试程序"""
    print("🧪 Jarvis学生住房功能测试")
    print("=" * 60)
    
    success = test_student_housing()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 测试完成！功能正常工作")
        print("💡 现在可以在Jarvis中使用 'housing' 命令")
        print("💡 或在GUI界面中点击 '🏠 学生住房(London)' 按钮")
    else:
        print("❌ 测试失败，请检查网络连接和浏览器设置")

if __name__ == "__main__":
    main()
