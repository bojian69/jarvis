#!/usr/bin/env python3
"""
简单的本地浏览器配置测试
"""

import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.agent import JarvisAgent

def test_local_browser():
    """测试本地浏览器配置"""
    print("🧪 测试本地浏览器配置")
    print("=" * 40)
    
    try:
        with JarvisAgent() as agent:
            # 1. 检测浏览器配置
            print("1. 检测浏览器配置...")
            result = agent.execute_command("browser_list_profiles")
            if result.get("success"):
                browsers = result.get("browsers", {})
                print(f"✅ 检测到 {len(browsers)} 个浏览器")
                
                for browser_name, profiles in browsers.items():
                    print(f"  📁 {browser_name}:")
                    for profile_name, info in profiles.items():
                        print(f"    - {profile_name}: {info['extensions_count']} 个扩展")
            
            # 2. 获取扩展信息
            print("\n2. 获取Chrome扩展信息...")
            result = agent.execute_command("browser_get_extensions")
            if result.get("success"):
                extensions = result.get("extensions", [])
                print(f"✅ 找到 {len(extensions)} 个扩展:")
                for ext in extensions[:5]:  # 显示前5个
                    print(f"  🧩 {ext['name']} (v{ext['version']})")
                if len(extensions) > 5:
                    print(f"  ... 还有 {len(extensions) - 5} 个扩展")
            
            # 3. 启动浏览器（无头模式）
            print("\n3. 启动浏览器（使用本地配置）...")
            success = agent.setup_browser(
                headless=True,  # 无头模式，不显示窗口
                use_local_profile=True,
                browser_type="auto"
            )
            
            if success:
                print("✅ 浏览器启动成功！")
                
                # 4. 访问测试页面
                print("\n4. 访问测试页面...")
                result = agent.execute_command("browser_navigate", url="https://httpbin.org/user-agent")
                if result.get("success"):
                    print(f"✅ 页面访问成功: {result.get('title', 'httpbin')}")
                
                # 5. 获取页面信息
                print("\n5. 获取页面信息...")
                result = agent.execute_command("browser_get_page_info")
                if result.get("success"):
                    info = result.get("info", {})
                    print(f"当前URL: {info.get('url')}")
                    print(f"窗口大小: {info.get('window_size')}")
                    print(f"Cookie数量: {info.get('cookies_count')}")
                
                print("\n✅ 本地浏览器配置测试成功！")
                print("💡 浏览器已使用您的本地配置，包括所有扩展和设置")
            else:
                print("❌ 浏览器启动失败")
                
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_local_browser()
