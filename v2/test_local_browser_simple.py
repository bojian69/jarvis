#!/usr/bin/env python3
"""
简单测试本地浏览器配置（不安装扩展）
"""

import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.agent import JarvisAgent

def main():
    """测试本地浏览器配置"""
    print("🧪 测试使用本地浏览器配置")
    print("=" * 50)
    
    try:
        with JarvisAgent() as agent:
            print("✅ Jarvis Agent 初始化成功")
            
            # 启动浏览器，使用本地配置
            print("\n🌐 启动浏览器（使用您的本地配置）...")
            success = agent.setup_browser(
                headless=False,  # 显示浏览器窗口，这样您可以看到效果
                use_local_profile=True,  # 使用本地配置文件
                browser_type="auto"  # 自动选择最佳配置
            )
            
            if success:
                print("✅ 浏览器启动成功！")
                print("💡 现在浏览器使用的是您的本地配置，包括:")
                print("  - 您的登录状态")
                print("  - 您的书签")
                print("  - 您已安装的所有扩展")
                print("  - 您的个人设置")
                
                # 访问一个测试页面
                print("\n🔗 访问测试页面...")
                result = agent.execute_command("browser_navigate", url="https://www.google.com")
                if result.get("success"):
                    print(f"✅ 成功访问: {result.get('title', 'Google')}")
                    
                    # 截图保存
                    print("\n📸 保存截图...")
                    result = agent.execute_command("browser_screenshot", 
                                                 description="本地配置浏览器测试")
                    if result.get("success"):
                        print(f"✅ 截图已保存到: {result.get('filepath')}")
                
                print("\n🎉 测试完成！")
                print("💡 您可以在浏览器中看到所有您熟悉的设置和扩展都在正常工作")
                
                # 等待用户查看
                input("\n按回车键关闭浏览器...")
                
            else:
                print("❌ 浏览器启动失败")
                print("💡 可能的原因:")
                print("  - Chrome浏览器未安装")
                print("  - 浏览器配置文件路径问题")
                print("  - 权限问题")
                
    except KeyboardInterrupt:
        print("\n👋 测试被用户中断")
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")

if __name__ == "__main__":
    main()
