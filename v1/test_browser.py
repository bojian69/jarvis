#!/usr/bin/env python3
"""
简单的浏览器测试脚本
验证修复是否有效
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_standard_chrome():
    """测试标准Chrome驱动"""
    print("🧪 测试标准Chrome驱动...")
    
    try:
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=800,600")
        
        # 创建用户数据目录
        user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome/TestProfile")
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir, exist_ok=True)
        options.add_argument(f"--user-data-dir={user_data_dir}")
        
        driver = webdriver.Chrome(options=options)
        print("✅ 标准Chrome驱动启动成功！")
        
        # 测试页面加载
        print("🌐 测试页面加载...")
        driver.get("https://www.google.com")
        time.sleep(3)
        
        title = driver.title
        url = driver.current_url
        print(f"✅ 页面加载成功")
        print(f"   标题: {title}")
        print(f"   URL: {url}")
        
        # 截图测试
        screenshot_path = "test_success.png"
        driver.save_screenshot(screenshot_path)
        print(f"✅ 截图保存: {screenshot_path}")
        
        print("⏱️ 浏览器将在5秒后关闭...")
        time.sleep(5)
        
        driver.quit()
        print("✅ 浏览器已关闭")
        return True
        
    except Exception as e:
        print(f"❌ 标准Chrome驱动测试失败: {e}")
        return False

def test_undetected_chrome():
    """测试undetected-chromedriver"""
    print("\n🧪 测试undetected-chromedriver...")
    
    try:
        import undetected_chromedriver as uc
        
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=800,600")
        
        # 创建用户数据目录
        user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome/TestUC")
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir, exist_ok=True)
        options.add_argument(f"--user-data-dir={user_data_dir}")
        
        # 指定Chrome版本138
        driver = uc.Chrome(options=options, version_main=138)
        print("✅ undetected-chromedriver启动成功！")
        
        # 测试页面加载
        print("🌐 测试页面加载...")
        driver.get("https://www.google.com")
        time.sleep(3)
        
        title = driver.title
        url = driver.current_url
        print(f"✅ 页面加载成功")
        print(f"   标题: {title}")
        print(f"   URL: {url}")
        
        print("⏱️ 浏览器将在5秒后关闭...")
        time.sleep(5)
        
        driver.quit()
        print("✅ 浏览器已关闭")
        return True
        
    except Exception as e:
        print(f"❌ undetected-chromedriver测试失败: {e}")
        return False

def main():
    print("🔧 浏览器修复验证测试")
    print("=" * 50)
    
    # 测试标准Chrome
    standard_success = test_standard_chrome()
    
    # 测试undetected-chromedriver
    uc_success = test_undetected_chrome()
    
    # 总结结果
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print(f"  标准Chrome: {'✅ 成功' if standard_success else '❌ 失败'}")
    print(f"  UC Chrome: {'✅ 成功' if uc_success else '❌ 失败'}")
    
    if standard_success or uc_success:
        print("\n🎉 至少有一种方法可以工作！")
        print("💡 现在可以正常使用Jarvis了")
        
        if standard_success:
            print("💡 推荐使用标准Chrome驱动（更稳定）")
        
    else:
        print("\n❌ 所有测试都失败了")
        print("💡 建议:")
        print("   1. 更新Chrome浏览器到最新版本")
        print("   2. 重启电脑")
        print("   3. 检查系统权限设置")

if __name__ == "__main__":
    main()
