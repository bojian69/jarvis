#!/usr/bin/env python3
"""
Jarvis AI Agent v2.0 演示脚本
展示新架构的主要功能
"""

import sys
import time
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.agent import JarvisAgent

def demo_code_execution(agent):
    """演示代码执行功能"""
    print("\n🐍 代码执行演示")
    print("=" * 40)
    
    # Python代码执行
    print("1. 执行Python代码:")
    result = agent.execute_command("code_execute_python", 
                                 code="print('Hello from Jarvis!'); import math; print(f'π = {math.pi:.4f}')")
    if result.get('success'):
        print(f"输出: {result.get('stdout', '').strip()}")
    
    # 文件操作
    print("\n2. 文件操作:")
    # 写入文件
    agent.execute_command("code_write_file", 
                         filepath="demo_file.txt", 
                         content="这是Jarvis创建的演示文件\n当前时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    
    # 读取文件
    result = agent.execute_command("code_read_file", filepath="demo_file.txt")
    if result.get('success'):
        print(f"文件内容: {result.get('content', '').strip()}")
    
    # 目录列表
    print("\n3. 目录列表:")
    result = agent.execute_command("code_list_directory", dirpath=".", pattern="*.py")
    if result.get('success'):
        files = [item['name'] for item in result.get('items', []) if item['type'] == 'file']
        print(f"Python文件: {', '.join(files[:5])}")

def demo_api_calls(agent):
    """演示API调用功能"""
    print("\n🌐 API调用演示")
    print("=" * 40)
    
    # 网络连接测试
    print("1. 网络连接测试:")
    result = agent.execute_command("api_test_connection")
    if result.get('success'):
        success_rate = result.get('success_rate', 0)
        print(f"连接成功率: {success_rate:.1%}")
    
    # 天气查询（使用免费API）
    print("\n2. 天气查询:")
    result = agent.execute_command("api_weather", city="Beijing")
    if result.get('success'):
        print(f"北京天气: {result.get('temperature')}°C, {result.get('description')}")
    else:
        print(f"天气查询失败: {result.get('error')}")

def demo_browser_automation(agent):
    """演示浏览器自动化功能"""
    print("\n🌐 浏览器自动化演示")
    print("=" * 40)
    
    # 检测浏览器配置
    print("1. 检测浏览器配置...")
    result = agent.execute_command("browser_list_profiles")
    if result.get("success"):
        browsers = result.get("browsers", {})
        recommended = result.get("recommended")
        
        print(f"✅ 检测到 {len(browsers)} 个浏览器配置")
        if recommended:
            print(f"🎯 推荐配置: {recommended['browser']} - {recommended['profile']}")
    
    # 启动浏览器
    print("\n2. 启动浏览器 (使用本地配置)...")
    if agent.setup_browser(
        headless=True,  # 使用无头模式避免弹窗
        use_local_profile=True,  # 使用本地配置
        browser_type="auto"
    ):
        print("✅ 浏览器启动成功")
        
        # 获取扩展信息
        print("\n3. 检查浏览器扩展...")
        result = agent.execute_command("browser_get_extensions")
        if result.get("success"):
            extensions = result.get("extensions", [])
            print(f"✅ 检测到 {len(extensions)} 个扩展")
            if extensions:
                print("主要扩展:")
                for ext in extensions[:3]:
                    print(f"  🧩 {ext['name']} (v{ext['version']})")
        
        # 访问网页
        print("\n4. 访问Google首页...")
        result = agent.execute_command("browser_navigate", url="https://www.google.com")
        if result.get('success'):
            print(f"✅ 成功访问: {result.get('title')}")
        
        # 获取页面信息
        print("\n5. 获取页面信息...")
        result = agent.execute_command("browser_get_page_info")
        if result.get('success'):
            info = result.get('info', {})
            print(f"页面标题: {info.get('title')}")
            print(f"窗口大小: {info.get('window_size')}")
        
        # 截图
        print("\n6. 页面截图...")
        result = agent.execute_command("browser_screenshot", description="Google首页演示")
        if result.get('success'):
            print(f"✅ 截图已保存: {result.get('filepath')}")
    else:
        print("❌ 浏览器启动失败，跳过浏览器演示")

def demo_logging_and_screenshots(agent):
    """演示日志和截图功能"""
    print("\n📋 日志和截图演示")
    print("=" * 40)
    
    # 查看最近日志
    print("1. 最近的信息日志:")
    recent_logs = agent.logger.get_recent_logs("info", 3)
    for log in recent_logs[-3:]:
        print(f"  {log.strip()}")
    
    # 截图目录
    screenshots_dir = agent.config.logs_dir / "screenshots"
    if screenshots_dir.exists():
        screenshots = list(screenshots_dir.glob("*.png"))
        print(f"\n2. 截图文件数量: {len(screenshots)}")
        if screenshots:
            latest = max(screenshots, key=lambda x: x.stat().st_mtime)
            print(f"最新截图: {latest.name}")

def main():
    """主演示函数"""
    print("🚀 Jarvis AI Agent v2.0 功能演示")
    print("=" * 50)
    
    try:
        # 创建Agent实例
        with JarvisAgent() as agent:
            print("✅ Jarvis Agent 启动成功！")
            
            # 演示各个功能模块
            demo_code_execution(agent)
            demo_api_calls(agent)
            demo_browser_automation(agent)
            demo_logging_and_screenshots(agent)
            
            print("\n" + "=" * 50)
            print("🎉 演示完成！")
            print("\n💡 更多功能:")
            print("  - 运行 'python run_v2.py --gui' 启动Web界面")
            print("  - 运行 'python run_v2.py --cli' 启动命令行界面")
            print("  - 查看 README_v2.md 了解详细使用方法")
            
    except KeyboardInterrupt:
        print("\n👋 演示被用户中断")
    except Exception as e:
        print(f"❌ 演示过程中出错: {e}")

if __name__ == "__main__":
    main()
