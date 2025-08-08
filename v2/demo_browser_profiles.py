#!/usr/bin/env python3
"""
浏览器配置文件演示脚本
展示如何使用本地浏览器配置和扩展
"""

import sys
import time
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.agent import JarvisAgent
from src.utils.browser_profiles import BrowserProfileDetector

def demo_profile_detection():
    """演示浏览器配置文件检测"""
    print("🔍 浏览器配置文件检测演示")
    print("=" * 50)
    
    detector = BrowserProfileDetector()
    
    # 检测所有可用浏览器
    browsers = detector.get_available_browsers()
    
    if not browsers:
        print("❌ 未检测到任何浏览器配置文件")
        return False
    
    print(f"✅ 检测到 {len(browsers)} 个浏览器:")
    
    for browser_name, profiles in browsers.items():
        print(f"\n📁 {browser_name}:")
        for profile_name, profile_path in profiles.items():
            info = detector.get_profile_info(profile_path)
            print(f"  - {profile_name}:")
            print(f"    路径: {profile_path}")
            print(f"    扩展数量: {len(info['extensions'])}")
            print(f"    大小: {info['size_mb']} MB")
            print(f"    书签: {'✅' if info['bookmarks_exist'] else '❌'}")
            print(f"    历史记录: {'✅' if info['history_exist'] else '❌'}")
            
            # 显示前3个扩展
            if info['extensions']:
                print("    主要扩展:")
                for ext in info['extensions'][:3]:
                    print(f"      • {ext['name']} (v{ext['version']})")
                if len(info['extensions']) > 3:
                    print(f"      ... 还有 {len(info['extensions']) - 3} 个扩展")
    
    # 显示推荐配置
    recommended = detector.get_recommended_profile()
    if recommended:
        browser_name, profile_name, profile_path = recommended
        print(f"\n🎯 推荐使用: {browser_name} - {profile_name}")
    
    return True

def demo_browser_with_local_profile():
    """演示使用本地浏览器配置启动"""
    print("\n🌐 本地浏览器配置启动演示")
    print("=" * 50)
    
    try:
        with JarvisAgent() as agent:
            print("1. 启动浏览器 (使用本地配置)...")
            
            # 启动浏览器，使用本地配置文件
            success = agent.setup_browser(
                headless=False,  # 显示浏览器窗口
                use_local_profile=True,  # 使用本地配置
                browser_type="auto",  # 自动选择
                profile_name="Default"
            )
            
            if not success:
                print("❌ 浏览器启动失败")
                return False
            
            print("✅ 浏览器启动成功！")
            
            # 获取浏览器扩展信息
            print("\n2. 获取浏览器扩展信息...")
            result = agent.execute_command("browser_get_extensions")
            if result.get("success"):
                extensions = result.get("extensions", [])
                print(f"✅ 检测到 {len(extensions)} 个扩展:")
                for ext in extensions[:5]:  # 显示前5个
                    print(f"  🧩 {ext['name']} (v{ext['version']})")
                if len(extensions) > 5:
                    print(f"  ... 还有 {len(extensions) - 5} 个扩展")
            
            # 访问一个网页来测试
            print("\n3. 访问测试网页...")
            result = agent.execute_command("browser_navigate", url="https://www.google.com")
            if result.get("success"):
                print(f"✅ 成功访问: {result.get('title', 'Google')}")
                
                # 截图
                print("\n4. 保存截图...")
                result = agent.execute_command("browser_screenshot", 
                                             description="本地配置浏览器测试")
                if result.get("success"):
                    print(f"✅ 截图已保存: {result.get('filepath')}")
                
                # 获取页面信息
                print("\n5. 获取页面信息...")
                result = agent.execute_command("browser_get_page_info")
                if result.get("success"):
                    info = result.get("info", {})
                    print(f"页面标题: {info.get('title')}")
                    print(f"当前URL: {info.get('url')}")
                    print(f"窗口大小: {info.get('window_size')}")
                    print(f"Cookie数量: {info.get('cookies_count')}")
            
            print("\n✅ 本地浏览器配置演示完成！")
            print("💡 您可以看到浏览器使用了您的本地配置，包括:")
            print("  - 登录状态")
            print("  - 书签")
            print("  - 扩展插件")
            print("  - 个人设置")
            
            # 等待用户查看
            input("\n按回车键继续...")
            
            return True
            
    except KeyboardInterrupt:
        print("\n👋 演示被用户中断")
        return False
    except Exception as e:
        print(f"❌ 演示过程中出错: {e}")
        return False

def demo_extension_comparison():
    """演示扩展对比"""
    print("\n🧩 浏览器扩展对比演示")
    print("=" * 50)
    
    try:
        # 使用本地配置启动
        print("1. 使用本地配置启动浏览器...")
        with JarvisAgent() as agent_local:
            success = agent_local.setup_browser(use_local_profile=True, headless=True)
            if success:
                result = agent_local.execute_command("browser_get_extensions")
                local_extensions = result.get("extensions", []) if result.get("success") else []
                print(f"✅ 本地配置扩展数量: {len(local_extensions)}")
        
        # 使用默认配置启动
        print("\n2. 使用默认配置启动浏览器...")
        with JarvisAgent() as agent_default:
            success = agent_default.setup_browser(use_local_profile=False, headless=True)
            if success:
                result = agent_default.execute_command("browser_get_extensions")
                default_extensions = result.get("extensions", []) if result.get("success") else []
                print(f"✅ 默认配置扩展数量: {len(default_extensions)}")
        
        # 对比结果
        print(f"\n📊 对比结果:")
        print(f"  本地配置: {len(local_extensions)} 个扩展")
        print(f"  默认配置: {len(default_extensions)} 个扩展")
        print(f"  差异: {len(local_extensions) - len(default_extensions)} 个扩展")
        
        if local_extensions:
            print(f"\n🧩 您的浏览器扩展:")
            for ext in local_extensions[:10]:  # 显示前10个
                print(f"  • {ext['name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 对比演示失败: {e}")
        return False

def main():
    """主演示函数"""
    print("🚀 Jarvis AI Agent 浏览器配置演示")
    print("=" * 60)
    
    # 1. 检测浏览器配置文件
    if not demo_profile_detection():
        print("❌ 未检测到浏览器配置，演示结束")
        return
    
    # 询问用户是否继续
    try:
        choice = input("\n是否继续浏览器启动演示? (y/n): ").strip().lower()
        if choice != 'y':
            print("👋 演示结束")
            return
    except KeyboardInterrupt:
        print("\n👋 演示结束")
        return
    
    # 2. 使用本地配置启动浏览器
    demo_browser_with_local_profile()
    
    # 3. 扩展对比演示
    try:
        choice = input("\n是否进行扩展对比演示? (y/n): ").strip().lower()
        if choice == 'y':
            demo_extension_comparison()
    except KeyboardInterrupt:
        print("\n👋 演示结束")
    
    print("\n🎉 所有演示完成！")
    print("\n💡 使用建议:")
    print("  - 使用本地配置可以保持您的登录状态和个人设置")
    print("  - 所有浏览器扩展都会正常工作")
    print("  - 可以通过配置文件选择不同的浏览器配置")
    print("  - 支持Chrome和Edge浏览器")

if __name__ == "__main__":
    main()
