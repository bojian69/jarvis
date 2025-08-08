#!/usr/bin/env python3
"""
浏览器问题诊断脚本
帮助识别和解决浏览器闪退问题
"""

import os
import sys
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc

def check_chrome_installation():
    """检查Chrome安装情况"""
    print("🔍 检查Chrome浏览器安装...")
    
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/local/bin/google-chrome"
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ 找到Chrome: {path}")
            try:
                result = subprocess.run([path, "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ Chrome版本: {result.stdout.strip()}")
                    return path
            except Exception as e:
                print(f"⚠️ 获取Chrome版本失败: {e}")
    
    print("❌ 未找到Chrome浏览器")
    return None

def check_chromedriver():
    """检查ChromeDriver"""
    print("\n🔍 检查ChromeDriver...")
    
    try:
        # 检查系统PATH中的chromedriver
        result = subprocess.run(["which", "chromedriver"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            driver_path = result.stdout.strip()
            print(f"✅ 找到ChromeDriver: {driver_path}")
            
            # 获取版本
            try:
                version_result = subprocess.run([driver_path, "--version"], 
                                              capture_output=True, text=True, timeout=5)
                if version_result.returncode == 0:
                    print(f"✅ ChromeDriver版本: {version_result.stdout.strip()}")
            except Exception as e:
                print(f"⚠️ 获取ChromeDriver版本失败: {e}")
        else:
            print("⚠️ 系统PATH中未找到ChromeDriver")
    except Exception as e:
        print(f"❌ 检查ChromeDriver失败: {e}")

def check_selenium():
    """检查Selenium安装"""
    print("\n🔍 检查Selenium安装...")
    
    try:
        import selenium
        print(f"✅ Selenium版本: {selenium.__version__}")
    except ImportError:
        print("❌ Selenium未安装")
        return False
    
    try:
        import undetected_chromedriver as uc
        print(f"✅ undetected-chromedriver已安装")
    except ImportError:
        print("❌ undetected-chromedriver未安装")
    
    return True

def test_basic_chrome():
    """测试基础Chrome启动"""
    print("\n🧪 测试基础Chrome启动...")
    
    try:
        options = Options()
        options.add_argument("--headless")  # 无头模式测试
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=options)
        print("✅ 基础Chrome启动成功")
        
        # 测试基本功能
        driver.get("data:text/html,<html><body><h1>Test Page</h1></body></html>")
        title = driver.title
        print(f"✅ 页面加载成功，标题: {title}")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ 基础Chrome启动失败: {e}")
        return False

def test_undetected_chrome():
    """测试undetected-chromedriver"""
    print("\n🧪 测试undetected-chromedriver...")
    
    try:
        options = uc.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = uc.Chrome(options=options)
        print("✅ undetected-chromedriver启动成功")
        
        # 测试基本功能
        driver.get("data:text/html,<html><body><h1>UC Test Page</h1></body></html>")
        title = driver.title
        print(f"✅ 页面加载成功，标题: {title}")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ undetected-chromedriver启动失败: {e}")
        return False

def test_visible_chrome():
    """测试可见Chrome窗口"""
    print("\n🧪 测试可见Chrome窗口...")
    
    try:
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=800,600")
        
        driver = webdriver.Chrome(options=options)
        print("✅ 可见Chrome窗口启动成功")
        
        # 测试页面加载
        print("🌐 正在加载测试页面...")
        driver.get("https://www.google.com")
        
        print("⏱️ 等待5秒观察窗口...")
        time.sleep(5)
        
        current_url = driver.current_url
        title = driver.title
        print(f"✅ 当前URL: {current_url}")
        print(f"✅ 页面标题: {title}")
        
        print("📸 尝试截图...")
        screenshot_path = "test_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"✅ 截图保存: {screenshot_path}")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ 可见Chrome窗口测试失败: {e}")
        return False

def check_user_data_directory():
    """检查用户数据目录"""
    print("\n🔍 检查用户数据目录...")
    
    directories = [
        os.path.expanduser("~/Library/Application Support/Google/Chrome/Jarvis"),
        os.path.expanduser("~/Library/Application Support/Google/Chrome/JarvisProfile"),
        os.path.expanduser("~/Library/Application Support/Google/Chrome/JarvisUC")
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✅ 找到目录: {directory}")
            try:
                # 检查目录权限
                test_file = os.path.join(directory, "test_write.tmp")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                print(f"✅ 目录可写: {directory}")
            except Exception as e:
                print(f"❌ 目录权限问题: {directory} - {e}")
        else:
            print(f"⚠️ 目录不存在: {directory}")
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"✅ 已创建目录: {directory}")
            except Exception as e:
                print(f"❌ 创建目录失败: {directory} - {e}")

def check_system_resources():
    """检查系统资源"""
    print("\n🔍 检查系统资源...")
    
    try:
        # 检查内存使用
        result = subprocess.run(["vm_stat"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 内存状态检查完成")
            # 可以解析vm_stat输出，但这里简化处理
        
        # 检查磁盘空间
        result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                disk_info = lines[1].split()
                if len(disk_info) >= 4:
                    print(f"✅ 磁盘空间: 已用 {disk_info[2]}, 可用 {disk_info[3]}")
        
    except Exception as e:
        print(f"⚠️ 系统资源检查失败: {e}")

def provide_solutions():
    """提供解决方案"""
    print("\n💡 常见问题解决方案:")
    print("=" * 50)
    
    print("1. 如果Chrome启动失败:")
    print("   - 确保已安装最新版Google Chrome")
    print("   - 尝试重启Chrome浏览器")
    print("   - 检查Chrome是否被其他程序占用")
    
    print("\n2. 如果ChromeDriver版本不匹配:")
    print("   - 更新undetected-chromedriver: pip install --upgrade undetected-chromedriver")
    print("   - 或手动下载匹配的ChromeDriver")
    
    print("\n3. 如果权限问题:")
    print("   - 在系统偏好设置 > 安全性与隐私中允许Chrome")
    print("   - 检查用户数据目录的读写权限")
    
    print("\n4. 如果页面闪退:")
    print("   - 尝试禁用Chrome扩展")
    print("   - 使用无头模式测试")
    print("   - 清理Chrome用户数据目录")
    
    print("\n5. 如果内存不足:")
    print("   - 关闭其他占用内存的应用")
    print("   - 使用更轻量的浏览器配置")
    
    print("=" * 50)

def main():
    """主诊断程序"""
    print("🔧 Jarvis浏览器问题诊断工具")
    print("=" * 60)
    
    # 1. 检查Chrome安装
    chrome_path = check_chrome_installation()
    
    # 2. 检查ChromeDriver
    check_chromedriver()
    
    # 3. 检查Selenium
    if not check_selenium():
        print("❌ Selenium未正确安装，请先安装依赖")
        return
    
    # 4. 检查用户数据目录
    check_user_data_directory()
    
    # 5. 检查系统资源
    check_system_resources()
    
    print("\n" + "=" * 60)
    print("🧪 开始浏览器功能测试...")
    
    # 6. 测试基础Chrome
    basic_success = test_basic_chrome()
    
    # 7. 测试undetected-chromedriver
    uc_success = test_undetected_chrome()
    
    # 8. 测试可见窗口（如果用户同意）
    visible_test = input("\n❓ 是否测试可见Chrome窗口？(y/n): ").lower().strip()
    visible_success = False
    if visible_test == 'y':
        visible_success = test_visible_chrome()
    
    # 9. 总结结果
    print("\n" + "=" * 60)
    print("📊 诊断结果总结:")
    print(f"  Chrome安装: {'✅' if chrome_path else '❌'}")
    print(f"  基础启动: {'✅' if basic_success else '❌'}")
    print(f"  UC启动: {'✅' if uc_success else '❌'}")
    if visible_test == 'y':
        print(f"  可见窗口: {'✅' if visible_success else '❌'}")
    
    # 10. 提供解决方案
    if not all([chrome_path, basic_success, uc_success]):
        provide_solutions()
    else:
        print("\n🎉 所有测试通过！浏览器应该可以正常工作。")
        print("💡 如果仍有问题，可能是特定网站或操作导致的。")

if __name__ == "__main__":
    main()
